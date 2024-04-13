import os
import shutil
import streamlit as st
from utils.helper import load_data
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

if os.path.exists('src/chroma'):
    shutil.rmtree('src/chroma')

if os.path.exists('src/uploads'):
    shutil.rmtree('src/uploads')

if os.path.exists('src/scrape'):
    shutil.rmtree('src/scrape')

if os.path.isfile('./audio_english.mp3'):
    os.remove('./audio_english.mp3')

def get_vectorstore(url, max_depth, files, youtube):
    """
    Scrape website URLs and create a vector store.

    Args:
        url (str): The URL of the website.
        max_depth (int): The maximum depth for scraping.

    Returns:
        tuple: A tuple containing the created vector store and the number of URLs scraped.
    """

    document_chunks, length = load_data(url, max_depth, files, youtube)
    
    # create a vectorstore from the chunks
    vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())

    return vector_store, length

def get_context_retriever_chain(vector_store):
    """
    Create a context-aware retriever chain.

    Args:
        vector_store: The vector store to use for retrieval.

    Returns:
        obj: The created context-aware retriever chain.
    """
    llm = ChatOpenAI()
    
    retriever = vector_store.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages([
      MessagesPlaceholder(variable_name="chat_history"),
      ("user", "{input}"),
      ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    
    return retriever_chain
    
def get_conversational_rag_chain(retriever_chain):
    """
    Creates a conversational RAG chain based on the provided retriever chain.

    Args:
        retriever_chain: The retriever chain to use for conversation.

    Returns:
        obj: The created conversational RAG chain.
    """
    
    llm = ChatOpenAI()
    
    prompt = ChatPromptTemplate.from_messages([
      ("system", "Answer the user's questions based on the below context:\n\n{context}"),
      MessagesPlaceholder(variable_name="chat_history"),
      ("user", "{input}"),
    ])
    
    stuff_documents_chain = create_stuff_documents_chain(llm,prompt)
    
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

def get_response(user_input):
    """
    Gets a response from the chatbot based on user input.

    Args:
        user_input (str): The user's input message.

    Returns:
        str: The chatbot's response.
    """
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    
    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_input
    })
    
    return response['answer']

# app config
st.set_page_config(page_title="ChatVerse 🤖 WhereEverythingTalks", page_icon="🤖")
st.title("ChatVerse 🤖 WhereEverythingTalks")

if "freeze" not in st.session_state:
    st.session_state.freeze = False
if "max_depth" not in st.session_state:
    st.session_state.max_depth = 1
if "web_url" not in st.session_state:
    st.session_state.web_url = ""
if "files" not in st.session_state:
    st.session_state.files = ""

# sidebar
with st.sidebar:
    st.header("ChatVerse 🤖 ")
    st.session_state.youtube_url = st.text_input("Youtube URL (English Language Only)", disabled=st.session_state.freeze)
    st.session_state.web_url = st.text_input("Website URL", disabled=st.session_state.freeze)
    
    st.session_state.max_depth = st.slider("Select maximum scraping depth:", 1, 5, 1, disabled=st.session_state.freeze)

    st.session_state.files = st.file_uploader("Upload your files...",
                                     type=['pdf', '.csv', '.xlsx', '.txt', '.docx'],
                                     accept_multiple_files=True,
                                     disabled=st.session_state.freeze)
    
    if st.button("Proceed", disabled=st.session_state.freeze):
        st.session_state.freeze = True
    
if ((st.session_state.web_url is None or st.session_state.web_url == "") 
    and 
    (st.session_state.files is None or st.session_state.files == "")
    and
    (st.session_state.youtube_url is None or st.session_state.youtube_url == "")):
    st.info("Please enter a Youtube URL and(or) Web URL and(or) Documents")

else:
    if st.session_state.freeze:
        # session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                AIMessage(content="Hello, I am a bot. How can I help you?"),
            ]
        if "vector_store" not in st.session_state:
            with st.sidebar:
                with st.spinner("Scrapping Youtube_Video, Website & Documents..."):
                    st.session_state.vector_store, st.session_state.len_urls = get_vectorstore(st.session_state.web_url,
                                                                                               st.session_state.max_depth,
                                                                                               st.session_state.files,
                                                                                               st.session_state.youtube_url)
                    st.write(f"Total Pages Scrapped: {st.session_state.len_urls}")
                    st.success("Scraping completed, 🤖 Ready!")

        else:
            with st.sidebar:
                    st.write(f"Total Pages Scrapped: {st.session_state.len_urls}")
                    st.success("🤖 Ready!")

        # user input
        user_query = st.chat_input("Type your message here...")
        if user_query is not None and user_query != "":
            response = get_response(user_query)
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            st.session_state.chat_history.append(AIMessage(content=response))

        # conversation
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human"):
                    st.write(message.content)
    
st.sidebar.markdown('---')
st.sidebar.markdown('Connect with me:')
st.sidebar.markdown('[LinkedIn](https://www.linkedin.com/in/saksham-chaurasia/)')
st.sidebar.markdown('[GitHub](https://github.com/imsaksham-c)')
st.sidebar.markdown('[Email](mailto:imsaksham.c@gmail.com)')