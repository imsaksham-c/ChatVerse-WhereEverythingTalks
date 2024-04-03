import streamlit as st
from utils.get_urls import scrape_urls
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


load_dotenv()

def get_vectorstore_from_url(url, max_depth):
    urls = scrape_urls(url, max_depth)
    # get the text in document form
    loader = WebBaseLoader(urls)
    document = loader.load()
    
    # split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)
    
    # create a vectorstore from the chunks
    vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())

    return vector_store, len(urls)

def get_context_retriever_chain(vector_store):
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
    
    llm = ChatOpenAI()
    
    prompt = ChatPromptTemplate.from_messages([
      ("system", "Answer the user's questions based on the below context:\n\n{context}"),
      MessagesPlaceholder(variable_name="chat_history"),
      ("user", "{input}"),
    ])
    
    stuff_documents_chain = create_stuff_documents_chain(llm,prompt)
    
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

def get_response(user_input):
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    
    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_input
    })
    
    return response['answer']

# app config
st.set_page_config(page_title="WebChat 🤖: Chat with Websites", page_icon="🤖")
st.title("WebChat 🤖: Chat with Websites")

if "freeze" not in st.session_state:
    st.session_state.freeze = False
if "max_depth" not in st.session_state:
    st.session_state.max_depth = 1

# sidebar
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")
    
    if not st.session_state.freeze:
        st.session_state.max_depth = st.slider("Select maximum scraping depth:", 1, 5, 1)
        if st.button("Proceed"):
            st.session_state.freeze = True
    else:
        st.session_state.max_depth = st.slider("Select maximum scraping depth:", 1, 5, st.session_state.max_depth)
        st.button("Proceed", disabled=True)
    
if website_url is None or website_url == "":
    st.info("Please enter a website URL")

else:
    if st.session_state.freeze:
        # session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                AIMessage(content="Hello, I am a bot. How can I help you?"),
            ]
        if "vector_store" not in st.session_state:
            with st.sidebar:
                with st.spinner("Scrapping Website..."):
                    st.session_state.vector_store, st.session_state.len_urls = get_vectorstore_from_url(website_url,
                                                                                                        st.session_state.max_depth)
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