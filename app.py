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
from random import randint

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

def on_click_callback():
	user_prompt = st.session_state.user_prompt
	st.session_state.history.append(user_prompt)


avatars = {
    "user": "static/user.png:",
    "ai": "/static/chatbot.png",}

# Sidebar content 
st.sidebar.image("DBG-Logo.png", use_column_width=True)
st.sidebar.header("DBGenAI - Platform")
sideb = st.sidebar
Bar1 = sideb.write("-------")
selectionbox = sideb.selectbox(
	"Select a Department",
	("📁 HR Persona", "💻 IT Persona", "📈 Finance Persona"),
	)
# button1 = sideb.button(" 📁  HR-Bot")
# button2 = sideb.button(" 💻  IT-Bot")
# button3 = sideb.button(" 📈  Finance-Bot")
# Bar2 = sideb.write("-------")
# Text1 = sideb.write(
# 	"""
# 	#### Natina is currently supporting HR & IT Operations Regulations and Finance Reports.
# 	"""
# )
# Bar2 = sideb.write("-------")
# Text2 = sideb.write(
# 	"""
# 		Copyright © 2024 Deutsche Börse Group - All Rights Reserved.
# 	"""
# )



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
    st.session_state.greetings = False
# Display chat messages from history on app rerun


# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

uploaded_files = st.file_uploader("Choose PPT or PDF file", accept_multiple_files=True, type=["pdf"], key=st.session_state.widget_key)



# # Greet user
if not st.session_state.greetings:
	with st.chat_message("ai", avatar="static/chatbot.png"):
		intro = """Hello, I am Natina."""
		st.markdown(intro)
		#Add Bot response to chat History
		# st.session_state.messages.append(intro)
		# st.session_state.greetings = True


# Example prompts
example_prompts = [
	"How to access Jira",
	"Explain me the different Personas",
	"Use the prompt correcty",
	"White card with protection from black",
	"The famous 'Black Lotus' card",
	"Wizard card with Vigiliance ability",
]

example_prompts_help = [
	"Look for a specific card effect",
	"Search for card type: 'Vampires', card color: 'black', and ability: 'flying'",
	"Color cards and card type",
	"Specifc card effect to another mana color",
	"Search for card names",
	"Search for card types with specific abilities",
]

button_cols = st.columns(3)
button_cols_2 = st.columns(3)

button_pressed = ""

if button_cols[0].button(example_prompts[0], help=example_prompts_help[0]):
	button_pressed = example_prompts[0]
elif button_cols[1].button(example_prompts[1], help=example_prompts_help[1]):
	button_pressed = example_prompts[1]
elif button_cols[2].button(example_prompts[2], help=example_prompts_help[2]):
	button_pressed = example_prompts[2]

elif button_cols_2[0].button(example_prompts[3], help=example_prompts_help[3]):
	button_pressed = example_prompts[3]
elif button_cols_2[1].button(example_prompts[4], help=example_prompts_help[4]):
	button_pressed = example_prompts[4]
elif button_cols_2[2].button(example_prompts[5], help=example_prompts_help[5]):
	button_pressed = example_prompts[5]





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
    with st.chat_message("human", avatar="static/user.png"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("ai", avatar="static/chatbot.png"):
        with st.spinner('Processing'):
            response = st.write_stream(response_generator())
        # response=response_generator()
        # st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
    st.rerun()
