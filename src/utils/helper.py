import os
from utils.get_urls import scrape_urls
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, UnstructuredWordDocumentLoader, UnstructuredExcelLoader

text_splitter = RecursiveCharacterTextSplitter()

def get_data_from_url(url, max_depth):
    urls = scrape_urls(url, max_depth)
    loader = WebBaseLoader(urls)
    document = loader.load()
    document_chunks = text_splitter.split_documents(document)
    return document_chunks, len(urls)


def get_data_from_file(files):
    all_document_chunks = []

    for file_path in files:
        with open(os.path.join("uploads", file_path.name), "wb") as f:
                f.write(file_path.getvalue())

        file_path_name = os.path.join("uploads", file_path.name)

        if file_path_name.endswith(".pdf"):
            loader = PyPDFLoader(file_path_name)
        elif file_path_name.endswith(".txt"):
            loader = TextLoader(file_path_name)
        elif file_path_name.endswith(".csv"):
            loader = CSVLoader(file_path_name)
        elif file_path_name.endswith(".doc") or file_path_name.name.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(file_path)
        elif file_path_name.endswith(".xlsx"):
            loader = UnstructuredExcelLoader(file_path, mode="elements")
        else:
            print(f"Unsupported file format")
            continue

        document = loader.load()
        document_chunks = text_splitter.split_documents(document)
        all_document_chunks.extend(document_chunks)
        return all_document_chunks, len(document)
    

def load_files(url, max_depth, files):
    print(url, max_depth, files)
    final_list = []
    total_scrapped = 0
    
    if url != "":
        web_files, length = get_data_from_url(url, max_depth)
        total_scrapped += length
        final_list.extend(web_files)
    else:
        web_files = []

    if len(files)>0 and files is not None:
        uploaded_files, length = get_data_from_file(files)
        total_scrapped += length
        final_list.extend(uploaded_files)
    else:
        uploaded_files = []
    
    return final_list, total_scrapped

