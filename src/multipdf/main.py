import os
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from htmlTemplates import css, bot_template, user_template



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        file = PdfReader(pdf)
        for page in file.pages:
            text += page.extract_text()
    return text


def get_text_chunks(raw_text):
    """
    Using langchain recursive character text splitter
    """
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.environ.get('OPENAI_API_KEY'),
        openai_api_base=os.environ.get('OPENAI_API_BASE')
    )
    
    # embeddings = HuggingFaceInstructEmbeddings(
    #     model_name="hkunlp/instructor-xl"
    # )
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    """
    Create chatbot that uses memory
    """
    llm  = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history",
                                      return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, 
                                                               retriever=vectorstore,
                                                               memory=memory)
    return conversation_chain
                                                            

def handle_user_question(prompt):
    response = st.session_state.conversation({"questoint": prompt})
    st.session_state.chat_history = response["chat_history"]
    
    for i , message in enumerate(st.session_state.chat_history):
        if i & 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    """
    Handle the main logic of the code
    """
    # load environment variables
    load_dotenv()
    if "conversation_chain" not in st.session_state:
        st.session_state.conversation_chain = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
        
    st.set_page_config(page_title="Chat witih Multiple pdf",
                       page_icon=":books:")
    st.header("Multi-PDF chat")
    st.write(css, unsafe_allow_html=True)
    st.markdown(
    """
   <h3>Chat witih Multiple pdf</h3>
    """,
    unsafe_allow_html=True
)
    prompt = st.text_input("Ask a question about your documents: ")
    if prompt:
        handle_user_question(prompt)
    
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload document", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get the pdf texts
                raw_text = get_pdf_text(pdf_docs)
                # break the pdf text chunks
                text_chunks = get_text_chunks(raw_text)
                # create embeddings for pdf chunks
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation_chain = get_conversation_chain(vectorstore)

    

if __name__ == '__main__':
    # only runs when the source file is being executed not imported
    main()