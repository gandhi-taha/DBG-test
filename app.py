import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.stylable_container import stylable_container
import os
import random
import time
from dotenv import load_dotenv
import google.generativeai as genai
import joblib
from typing import Literal
from dataclasses import dataclass
import json

st.set_page_config(layout='wide', page_title="Natina-AI", page_icon="DBG-Logo.png")
# custom_html = """
# <div class="banner">
# <img src="https://upload.wikimedia.org/wikipedia/de/thumb/8/87/Deutsche_B%C3%B6rse_Group_Logo.svg/1280px-Deutsche_B%C3%B6rse_Group_Logo.svg.png" alt = "Banner Image">
# </div>
# <style>
#    .banner {
#        width: 100%;
#        height: 200%;
#        overflow: hidden;
#    }
#    .banner img {
#        width: 80%;
#        object-fit: cover;
#    }
# </style>
# """
# Displaying the banner
# st.components.v1.html(custom_html)
def load_lottiefile(filepath: str):

	'''Load lottie animation file'''

	with open(filepath, "r") as f:
		return json.load(f)

st_lottie(load_lottiefile("images/Nationa-Ai.json"), speed=1, reverse=False, loop=True, quality="high", height=300)


def response_generator():
    new_docs = []
    # Routing for Alfred
    if st.session_state.files:
        for file in st.session_state.files:
            if file["used"] == False:
                file["used"] = True
                new_docs.append(file)
        response = multiturn_generate_content(prompt, new_docs)

        for respone in response:
            yield respone.candidates[0].content.parts[0].text
            time.sleep(0.05)
    # Routing to generall orchastrator
    else:
        orchastrator = Orchastrator()
        response = orchastrator.route({"question": prompt})
        for respone in response:
            yield respone
            time.sleep(0.05)


# Sidebar content 
st.sidebar.image("DBG-Logo.png", use_column_width=True)
st.sidebar.header("DBGenAI - Platform")
sideb = st.sidebar
Bar1 = sideb.write("-------")
button1 = sideb.button(" 📁  HR-Bot")
button2 = sideb.button(" 💻  IT-Bot")
button3 = sideb.button(" 📈  Finance-Bot")
Bar2 = sideb.write("-------")
Text1 = sideb.write(
	"""
	#### Natina is currently supporting HR & IT Operations Regulations and Finance Reports.
	"""
)
Bar2 = sideb.write("-------")
Text2 = sideb.write(
	"""
		Copyright © 2024 Deutsche Börse Group - All Rights Reserved.
	"""
)

# Main content
st.title("Natina-AI")

# Initialize File Uploader
if "files" not in st.session_state:
    st.session_state.files = []
if "widget_key" not in st.session_state:
    st.session_state.widget_key = str(randint(1000, 100000000))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

uploaded_files = st.file_uploader("Choose PPT or PDF file", accept_multiple_files=True, type=[
                                  "pdf"], key=st.session_state.widget_key)

# Accept user input
if prompt := st.chat_input("Type a message"):
    new_files = ""
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.session_state.files.append(
            {"file_name": uploaded_file.name, "file_data": bytes_data, "used": False})
        new_files += uploaded_file.name + "; "
    st.session_state.widget_key = str(randint(1000, 100000000))

    # Add user message to chat history
    st.session_state.messages.append(
        {"role": "user", "content": new_files+"\n"+prompt})
    # Display user message in chat message container
    with st.chat_message("human"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("ai"):
        with st.spinner('Processing'):
            response = st.write_stream(response_generator())
        # response=response_generator()
        # st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
    st.rerun()
