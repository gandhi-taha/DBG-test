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

@dataclass
class Message:
	"""Class for keeping track of chat message."""
	origin: Literal["user", "ai"]
	message: str

# Streamed response emulator
# def response_generator():
# 	bot_prompt = random.choice(
#         [
#         	"In most cases, Access uses Text Box controls to display Short Text or Long Text fields. However, when you add a Long Text field to a view in an Access web app, Access creates a Multiline Textbox. When using a Multiline Textbox in the browser, you can press Enter to move to a new line in the textbox. If you’re in a datasheet, you’ll need to use the scrollbars to see anything below the first line. In Desktop databases, if a Long Text field is configured to show Rich Text, and you add that field to a form or report, Access automatically applies the Rich Text setting to the text box.",
#         	"Hi, human! Is there anything I can help you with?",
#         	"Do you need help?",
#         ]
# 	)

def load_lottiefile(filepath: str):

	'''Load lottie animation file'''

	with open(filepath, "r") as f:
		return json.load(f)

st_lottie(load_lottiefile("images/Nationa-Ai.json"), speed=1, reverse=False, loop=True, quality="high", height=300)


def initialize_session_state():
	if "history" not in st.session_state:
		st.session_state.history = []

def on_click_callback():
	user_prompt = st.session_state.user_prompt
	st.session_state.history.append(user_prompt)

	bot_prompt = st.session_state.bot_prompt
	st.session_state.history.append(bot_prompt)

	# st.session_state.history.append(
	# 	st.write("User", user_prompt)
	# )
	# st.session_state.history.append(
	# 	st.write("ai", "Bot Answer")
	# )


initialize_session_state()

st.title("Natina-AI")

# Sidebar content 
st.sidebar.image("DBG-Logo.png", use_column_width=True)
st.sidebar.header("DBGenAI - Platform")
sideb = st.sidebar
Bar1 = sideb.write("-------")
button1 = sideb.button(" 📁  HR-Bot")
button2 = sideb.button(" 💻  IT-Bot")
button3 = sideb.button(" 📈  Finance-Bot")
Bar2 = sideb.write("-------")
st.markdown(
	"""
	
"""
)

# Main content
chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")
placeholder = st.empty()

with chat_placeholder:
	for chat in st.session_state.history:
		st.markdown(chat)

with prompt_placeholder:
	st.markdown("_Press Enter to Submit_")
	cols = st.columns((6, 1))
	cols [0].text_input(
		"Chat",
		value = "Hello Natina",
		label_visibility="collapsed",
		key="user_prompt",
	)
	cols[1].form_submit_button(
		"Submit",
		type= "primary",
		on_click = on_click_callback,
	)


