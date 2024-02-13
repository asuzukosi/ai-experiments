from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like clone")

client = OpenAI(base_url="https://api.together.xyz/v1")

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

    st.divider()
    st.caption('This is a string that explains something above.')
    st.caption('A caption with _italics_ :blue[colors] and emojis :sunglasses:')
    st.divider()
        
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=False,
        )
        message = response.choices[0].message.content
        st.write(message)
    st.session_state.messages.append({"role": "assistant", "content": message})
