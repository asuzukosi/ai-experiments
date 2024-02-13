import streamlit as st
import numpy as np
import pandas as pd

st.markdown("# Agent page 🤖")
st.sidebar.markdown("# Agent page 🤖")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
    
    


with st.chat_message("user"):
    st.write("Hello 👋")
    st.line_chart(np.random.randn(30, 3))

st.divider()  # 👈 Draws a horizontal rule
st.caption('This is a string that explains something above.')
st.caption('A caption with _italics_ :blue[colors] and emojis :sunglasses:')
st.divider()

message = st.chat_message("assistant")
message.write("Hello human")
message.bar_chart(np.random.randn(30, 3))


chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
message.line_chart(chart_data)
