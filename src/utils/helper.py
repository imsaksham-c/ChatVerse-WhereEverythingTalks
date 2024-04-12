import os
import pytube as pt
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
    yt = pt.YouTube(youtube_url)
    stream = yt.streams.filter(only_audio=True)[0]
    stream.download(filename="./audio_english.mp3")

    audio_file = open("./audio_english.mp3", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language='en',
        response_format="text"
    )

    document_chunks = text_splitter.create_documents(transcription)

    return document_chunks, 1


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

    scraped_urls = scrape_urls(url, max_depth)
    loader = WebBaseLoader(scraped_urls)
    document = loader.load()
    document_chunks = text_splitter.split_documents(document)

    return document_chunks, len(scraped_urls)


def load_and_split_data_from_files(uploaded_files: list) -> tuple[list, int]:
    """
    Loads data from uploaded files, handles different file formats, and splits the documents into chunks.

    Args:
        uploaded_files (list): A list of uploaded files.

    Returns:
        tuple: A tuple containing a list of document chunks and the total number of documents loaded.
    """

    if not os.path.exists('src/uploads/'):
        os.makedirs('src/uploads/')

    all_chunks = []
    for file_path in uploaded_files:
        with open(os.path.join("src/uploads", file_path.name), "wb") as f:
                f.write(file_path.getvalue())

        file_path_with_dir = os.path.join("src/uploads", file_path.name)

        # Choose loader based on file extension
        if file_path_with_dir.endswith(".pdf"):
            loader = PyPDFLoader(file_path_with_dir)
        elif file_path_with_dir.endswith(".txt"):
            loader = TextLoader(file_path_with_dir)
        elif file_path_with_dir.endswith(".csv"):
            loader = CSVLoader(file_path_with_dir)
        elif file_path_with_dir.endswith(".doc") or file_path_with_dir.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(file_path)
        elif file_path_with_dir.endswith(".xlsx"):
            loader = UnstructuredExcelLoader(file_path, mode="elements")
        else:
            print(f"Unsupported file format: {file_path_with_dir}")
            continue

        document = loader.load()
        document_chunks = text_splitter.split_documents(document)
        all_chunks.extend(document_chunks)

    return all_chunks, len(document)


def load_data(url: str, max_depth: int, uploaded_files: list, youtube: str):
    """
    Loads data from a URL (with scraping) and uploaded files, handling different file formats
    and splitting documents into chunks.

    Args:
        url (str): The URL to fetch data from.
        max_depth (int): The maximum depth for URL scraping.
        uploaded_files (list): A list of uploaded files.

    Returns:
        tuple: A tuple containing a list of document chunks and the total number of documents loaded.
    """

    final_chunks = []
    total_loaded = 0

    if url:
        web_chunks, num_scraped = fetch_and_split_data_from_url(url, max_depth)
        total_loaded += num_scraped
        final_chunks.extend(web_chunks)

    if uploaded_files and uploaded_files is not None:
        file_chunks, num_files = load_and_split_data_from_files(uploaded_files)
        total_loaded += num_files
        final_chunks.extend(file_chunks)

    if youtube:
        chunks, num_scraped = fetch_and_split_data_from_youtube(youtube)
        total_loaded += num_scraped
        final_chunks.extend(chunks)

    return final_chunks, total_loaded
