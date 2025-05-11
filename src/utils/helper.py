import os
import pytubefix as pt
from openai import OpenAI
from dotenv import load_dotenv
from utils.get_urls import scrape_urls
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    WebBaseLoader,
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader,
)

load_dotenv()
client = OpenAI()

text_splitter = RecursiveCharacterTextSplitter()

def fetch_and_split_data_from_youtube(youtube_url):
    """
    Downloads audio from a YouTube video, transcribes it, and splits into chunks.
    
    Args:
        youtube_url (str): The URL of the YouTube video.
        
    Returns:
        tuple: A tuple containing document chunks and count (always 1).
    """
    try:
        # Create directory for audio if it doesn't exist
        audio_dir = 'src/audio'
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir, exist_ok=True)
            
        # Use output_path parameter instead of filename
        audio_filename = "audio_english.mp3"
        audio_path = os.path.join(audio_dir, audio_filename)
        
        # Download the audio
        yt = pt.YouTube(youtube_url, use_oauth=True, allow_oauth_cache=True)
        stream = yt.streams.filter(only_audio=True)
        
        if not stream:
            print(f"No audio stream found for {youtube_url}")
            return [], 0
        
        # Fix: Use the proper download method with output_path and filename separately
        # PyTubefix expects output_path as directory and filename as the base filename
        stream[0].download(output_path=audio_dir, filename=audio_filename)
        
        # Check if file was successfully downloaded
        if not os.path.exists(audio_path):
            print(f"Failed to save audio to {audio_path}")
            return [], 0
            
        # Transcribe the audio
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language='en',
                response_format="text"
            )
        
        # Create document chunks from the transcription
        document_chunks = text_splitter.create_documents([transcription])
        
        return document_chunks, 1
        
    except Exception as e:
        print(f"Error in YouTube processing: {str(e)}")
        return [], 0


def fetch_and_split_data_from_url(url: str, max_depth: int) -> tuple[list, int]:
    """
    Fetches data from a given URL, scrapes additional URLs up to a specified depth,
    and splits the loaded documents into chunks.

    Args:
        url (str): The URL to fetch data from.
        max_depth (int): The maximum depth for URL scraping.

    Returns:
        tuple: A tuple containing a list of document chunks and the total number of URLs scraped.
    """
    if not url:
        return [], 0
        
    try:
        scraped_urls = scrape_urls(url, max_depth)
        loader = WebBaseLoader(scraped_urls)
        document = loader.load()
        document_chunks = text_splitter.split_documents(document)

        return document_chunks, len(scraped_urls)
    except Exception as e:
        print(f"Error fetching URL data: {str(e)}")
        return [], 0


def load_and_split_data_from_files(uploaded_files: list) -> tuple[list, int]:
    """
    Loads data from uploaded files, handles different file formats, and splits the documents into chunks.

    Args:
        uploaded_files (list): A list of uploaded files.

    Returns:
        tuple: A tuple containing a list of document chunks and the total number of documents loaded.
    """
    if not uploaded_files:
        return [], 0

    upload_dir = 'src/uploads/'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)

    all_chunks = []
    doc_count = 0
    
    for file_path in uploaded_files:
        try:
            save_path = os.path.join(upload_dir, file_path.name)
            with open(save_path, "wb") as f:
                f.write(file_path.getvalue())

            # Choose loader based on file extension
            if save_path.endswith(".pdf"):
                loader = PyPDFLoader(save_path)
            elif save_path.endswith(".txt"):
                loader = TextLoader(save_path)
            elif save_path.endswith(".csv"):
                loader = CSVLoader(save_path)
            elif save_path.endswith(".doc") or save_path.endswith(".docx"):
                loader = UnstructuredWordDocumentLoader(save_path)
            elif save_path.endswith(".xlsx"):
                loader = UnstructuredExcelLoader(save_path, mode="elements")
            else:
                print(f"Unsupported file format: {save_path}")
                continue

            document = loader.load()
            doc_count += 1
            document_chunks = text_splitter.split_documents(document)
            all_chunks.extend(document_chunks)
            
        except Exception as e:
            print(f"Error processing file {file_path.name}: {str(e)}")

    return all_chunks, doc_count


def load_data(url: str, max_depth: int, uploaded_files: list, youtube: str):
    """
    Loads data from a URL (with scraping), uploaded files, and YouTube videos,
    handling different formats and splitting documents into chunks.

    Args:
        url (str): The URL to fetch data from.
        max_depth (int): The maximum depth for URL scraping.
        uploaded_files (list): A list of uploaded files.
        youtube (str): YouTube URL to process.

    Returns:
        tuple: A tuple containing a list of document chunks and the total number of documents loaded.
    """
    final_chunks = []
    total_loaded = 0

    if url:
        web_chunks, num_scraped = fetch_and_split_data_from_url(url, max_depth)
        total_loaded += num_scraped
        final_chunks.extend(web_chunks)

    if uploaded_files:
        file_chunks, num_files = load_and_split_data_from_files(uploaded_files)
        total_loaded += num_files
        final_chunks.extend(file_chunks)

    if youtube:
        yt_chunks, num_yt = fetch_and_split_data_from_youtube(youtube)
        total_loaded += num_yt
        final_chunks.extend(yt_chunks)

    # Ensure we have at least some data
    if not final_chunks:
        print("Warning: No data was loaded from any source.")
        
    return final_chunks, total_loaded