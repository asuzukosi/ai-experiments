from openai import OpenAI
import streamlit as st
from tools import run_agent_executor


st.title("AFJ limited datascientist agent")
st.sidebar.markdown("# AFJ Limited data scientist agent 🤖")


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "mistralai/Mixtral-8x7B-Instruct-v0.1"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
     
    with st.chat_message("assistant"):
        response, message = run_agent_executor(st.session_state.messages[-1])
        st.divider()
        st.caption(message)
        st.divider()
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
