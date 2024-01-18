import os
from dotenv import load_dotenv
import pickle
import streamlit as st 
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import OpenAI 
from langchain.chains.question_answering import load_qa_chain

# text splitter for the pdf file
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


# set sidebar content, why are we using the with keyword to the do the sidebar
with st.sidebar:
    st.title(" LLM Chat App")
    st.markdown('''
    ## About
    This app is an LLM-Powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
    ''')
    
    add_vertical_space(5)
    st.write("Mad with Love from Kosi")

    
def handlePdf(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    store_name = pdf.name[:-4]
    
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len)
    
    chunks = text_splitter.split_text(text=text)
    
    # if the embeddign file exists load from embeddings
    if os.path.exists(f"{store_name}.pkl"):
        with open(f"{store_name}.pkl", "rb") as f:
            VectorStore = pickle.load(f)
            f.close()
            st.toast("File embeddings loaded successfully!")
            
    # create embeddings using openai embeddings
    else:
        with open(f"{store_name}.pkl", "wb") as f:
            embeddings = HuggingFaceEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            pickle.dump(VectorStore, f)
            f.close()
            st.toast("File embeddings created successfully!")
        
    return VectorStore
    
    
    
def acceptQuestions(vectorstore):
    query = st.text_input("Ask questions about the pdf file")
    if query:
        docs = vectorstore.similarity_search(query, k=3)
        st.write(docs)
        llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo-0613")
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        response = chain.run(input_documents=docs, question=query)
        st.write(response)
        
        
        
    # provide context to prompt for llm
    
    
    
def main():
    st.header("Chat with PDF 💬")
    load_dotenv()
    pdf = st.file_uploader("Upload your PDF", type='pdf')
    # optionally display this part of the document if pdf exists
    if pdf:
        vectorstore = handlePdf(pdf)
        acceptQuestions(vectorstore)
    
if __name__ == '__main__':
    main()
