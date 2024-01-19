import os, sys
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HUggingFaceEmbeddings
from langchain.vectorstores import Chroma
# from huggingface_hub import notebook_login
import torch
import transformers

from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline 
from langchain import HuggingFacePipeline 
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI



def load_documents_from_path(path_name):
    document = []

    for file in os.listdir(path_name):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(path_name, file)
            loader = PyPDFLoader(pdf_path)
            document.extend(loader.load())
        elif file.endswith(".docx") or file.endswith(".doc"):
            doc_path = os.path.join(path_name, file)
            loader = Docx2txtLoader(doc_path)
            document.extend(loader.load())
        elif file.endswith(".txt"):
            text_path = os.path.join(path_name, file)
            loader = TextLoader(text_path)
            document.extend(loader.load())
            
    return document

def create_document_chunks(document):
    document_splitter = CharacterTextSplitter(separator='\n', 
                                              chunk_size=500, 
                                              chunk_overlap=100)
    document_chunks = document_splitter.split_documents(document)
    len(document_chunks)
    return document_chunks


def create_chroma_vector_store(document_chunks, embeddings):
    vectordb=Chroma.from_documents(document_chunks,embedding=embeddings, persist_directory='./data')
    vectordb.persist()
    return vectordb

def create_memory_store():
    memory=ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    return memory


def create_pdf_qa(llm, vectordb, memory):
    pdf_qa = ConversationalRetrievalChain(llm=llm,                                        
                                          retriever=vectordb.as_retriever(search_kwargs={'k':6}),
                                          verbose=True, memory=memory
                                        )