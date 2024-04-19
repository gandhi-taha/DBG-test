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


# Streamed response emulator
# def response_generator():
# 	bot_prompt = random.choice(
#         [
#         	"In most cases, Access uses Text Box controls to display Short Text or Long Text fields. However, when you add a Long Text field to a view in an Access web app, Access creates a Multiline Textbox. When using a Multiline Textbox in the browser, you can press Enter to move to a new line in the textbox. If you’re in a datasheet, you’ll need to use the scrollbars to see anything below the first line. In Desktop databases, if a Long Text field is configured to show Rich Text, and you add that field to a form or report, Access automatically applies the Rich Text setting to the text box.",
#         	"Hi, human! Is there anything I can help you with?",
#         	"Do you need help?",
#         ]
# 	)

def load_css():
	with open("static/styles.css", "r") as f:
		css = f'<style>{f.read()}</style>'
		st.markdown(css, unsafe_allow_html=True)

# def load_lottiefile(filepath: str):

# 	'''Load lottie animation file'''

# 	with open(filepath, "r") as f:
# 		return json.load(f)

# animation = sideb.st_lottie(load_lottiefile("images/Nationa-Ai.json"), speed=1, reverse=False, loop=False, quality="high", height=300)

def initialize_session_state():
	if "history" not in st.session_state:
		st.session_state.history = []
		st.session_state.greetings = False

def on_click_callback():
	user_prompt = st.session_state.user_prompt
	st.session_state.history.append(user_prompt)

	# bot_prompt = st.session_state.bot_prompt
	# st.session_state.history.append(bot_prompt)

	# st.session_state.history.append(
	# 	st.write("User", user_prompt)
	# )
	# st.session_state.history.append(
	# 	st.write("ai", "Bot Answer")
	# )


initialize_session_state()

st.title("Natina")

# Sidebar content 
st.sidebar.image("DBG-Logo.png", use_column_width=True)
st.sidebar.header("DBGenAI - Platform")
sideb = st.sidebar
Bar1 = sideb.write("-------")
selectionbox = sideb.selectbox(
	"Select a Department",
	("📁 HR Persona", "💻 IT Persona", "📈 Finance Persona"),
	)
#selectText = sideb.write("You selected: ", selectionbox)
# button1 = sideb.button(" 📁  HR Manager")
# button2 = sideb.button(" 💻  IT Manager")
# button3 = sideb.button(" 📈  Financel Manager")
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


# # Greet user
if not st.session_state.greetings:
	with st.chat_message("ai"):
		intro = "Hello, I am Natina. Please let me know what I can do for you."
		st.markdown(intro)
		#Add Bot response to chat History
		st.session_state.history.append(intro)
		st.session_state.greetings = True


# Example prompts
example_prompts = [
	"How to access Jira",
	"Explain me the different Personas",
	"Use the prompt correcty",
	"White card with protection from black",
	"The famous 'Black Lotus' card",
	"Wizard card with Vigiliance ability",
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

#Prompt
chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")
placeholder = st.empty()

with chat_placeholder:
	for chat in st.session_state.history:
		st.markdown(chat)
		div = f"""
		<div class='chat-row'>{chat}</div>
		"""
		st.markdown(div, unsafe_allow_html=True)

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

	cols[0].form_submit_button(
		"⬆ Upload",
		type= "primary",
		on_click = on_click_callback,
	)

