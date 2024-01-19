import streamlit as st
import os
from langchain import PromtpTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain 
from langchain.chains import SequentialChain



def main():
    st.title("Book Summarizer")
    query = st.text_input("Search the book you want")
    first_input_prompt = PromtpTemplate(input_variable=["name"],
                                        template="provide me summary of the book {name}")
    # initiate open ai llm
    llm = OpenAI(temperature=0.8)
    
    # llm chain
    chain1 = LLMChain(llm=llm, prompt=first_input_prompt, verbose=True, output_key="summaryofbook")
    
    second_input_prompt = PromtpTemplate(input_variable=["summaryofbook"], 
                                         template="when was the {sumaryofbook} published")
    
    chain2 = LLMChain(llm=llm, prompt=second_input_prompt, verbose=True, output_key="bookpublisihdate")
    
    third_input_prompt = PromtpTemplate(input_variables =["summaryofbook"],  
                                        template="Please tell me about the authors of the {summaryofbook}")
    chain3 = LLMChain(llm=llm, prompt=third_input_prompt,
                      verbose=True, output_key='authorsofthebook')
    
    parent_chain = SequentialChain(chains = [chain1, chain2, chain3], 
                                   input_variables = ['name'], 
                                   output_variables = ['summaryofbook', 'bookpublishdate','authorsofthebook'], 
                                   verbose = True)
    
    if query:
        st.write(parent_chain({'name':query}))


if __name__ == '__main__':
    main()