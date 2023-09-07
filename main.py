import openai
import streamlit as st
from dotenv import load_dotenv
from vector_db import put_in_db
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if "messages" not in st.session_state:
    st.title(" 💬 Chatbot")
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": "You are a LLM hallucination detector. You take in a question and an answer, and you tell me if the answer is correct or not. Point out the difference and give it a similarity score from 0-100 based on how similar the given answer is to the answer you would have generated.",
        },
        {
            "role": "assistant",
            "content": "Hello, I'm a hallucination checker. Upload a file and I'll tell you if the answer is correct or not.",
        },
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

uploaded_file = st.file_uploader("Upload a file")
if uploaded_file is not None:
    put_in_db(uploaded_file)
    print(uploaded_file)

if prompt := st.chat_input():
    openai.api_key = openai_api_key
    st.chat_message("user").write(prompt)
    question = prompt.split("\n")[0]
    answer = prompt.split("\n")[1]
    st.session_state.messages.append(
        {"role": "user", "content": f"question: {question}\nanswer: {answer}"}
    )

    st.chat_message("assistant").write("Checking the answer...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=st.session_state.messages
    )
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
