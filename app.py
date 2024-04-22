import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.stylable_container import stylable_container
from doc_summary import multiturn_generate_content
from orchastrator.orchastrator import Orchastrator
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
import re
import PyPDF2

url_Dax = "https://www.investing.com/indices/germany-30"
url_IIQ = "https://iiq-deutsche-boerse.com/identify/home.jsf"
url_ticket = "https://cockpit.deutsche-boerse.com/sites#ticket_hub-Display?filter=hr"

st.set_page_config(layout='wide', page_title="Natina-AI", page_icon="DBG-Logo.png")

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
        response = orchastrator.route({"question": prompt, "persona": selectionbox})
        for respone in response:
            yield respone
            time.sleep(0.05)

# def on_click_callback():
# 	user_prompt = st.session_state.user_prompt
# 	st.session_state.history.append(user_prompt)


avatars = {
    "user": "static/user.png:",
    "ai": "/static/chatbot.png",}

# Sidebar content 
st.sidebar.image("DBG-Logo.png", use_column_width=True)
sideb = st.sidebar
subheader = st.sidebar.markdown(
    f'<a href="" style="display: inline-block; margin-left: 40px;margin-top: 50px; padding:5px;  background-color: white; color: #0A07C7; border-color: #0A07C7; text-align: center; text-decoration: none; font-size: 15px; border-radius: 10px;border: solid;">➕ New Conversation</a>',
    unsafe_allow_html=True
)



Bar1 = sideb.write("-------")
text1 = st.sidebar.markdown(
    f'<a href="{url_Dax}" style="display: inline-block; padding: 8px;color: #808286; text-align: center; text-decoration: none; font-size: 12px;">CHAT HISTORY</a>',
    unsafe_allow_html=True
)
text2 = st.sidebar.markdown(
    f'<a href="{url_Dax}" style="display: inline-block; padding: 8px;color: #808286; text-align: center; text-decoration: none; font-size: 15px;">💬 Annual Report</a>',
    unsafe_allow_html=True
)
text3 = st.sidebar.markdown(
    f'<a href="{url_Dax}" style="display: inline-block; padding: 8px;color: #808286; text-align: center; text-decoration: none; font-size: 15px;">💬 Learning Opportunity</a>',
    unsafe_allow_html=True
)
text4 = st.sidebar.markdown(
    f'<a href="{url_Dax}" style="display: inline-block; padding: 8px;color: #808286; text-align: center; text-decoration: none; font-size: 15px;">💬 Lorem Ipsum A</a>',
    unsafe_allow_html=True
)
text5 = st.sidebar.markdown(
    f'<a href="{url_Dax}" style="display: inline-block; padding: 8px;color: #808286; text-align: center; text-decoration: none; font-size: 15px;">💬 Lorem Ipsum B</a>',
    unsafe_allow_html=True
)

Bar2 = sideb.write("-------")
selectionbox = sideb.selectbox(
	"Select a role",
	("📁 HR Persona", "💻 IT Persona", "📈 Finance Persona"),
	)



# Main content
header = st.markdown(
    f'<a style="display: absolute;background: linear-gradient(90deg, #10D1DE, #1071DE, #ff00f3, #0033ff, #ff00c4, #ff0000); background-size: 400%;-webkit-background-clip: text; -webkit-text-fill-color: transparent;text-align: center; text-decoration: none; font-family: sans-serif; font-size: 50px;Letter-spacing: 1px;word-spacing: 1px;">Good afternoon, Lars Bolanca</a>',
    unsafe_allow_html=True
)
subheader = st.markdown(
    f'<a style="display: absolute; color: #C8C8C8; padding:-10px; text-align: center; text-decoration: none; font-family: sans-serif; font-size: 50px;">How can I help you?</a>',
    unsafe_allow_html=True
)

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


for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

uploaded_files = st.file_uploader(" ", accept_multiple_files=True, type=["pdf", "png", "jpg", "jpeg"], key=st.session_state.widget_key)
css = '''
<style>
    [data-testid='stFileUploader'] {
        width: max-content;
    }
    [data-testid='stFileUploader'] section {
        padding: 0;
        float: left;
    }
    [data-testid='stFileUploader'] section > input + div {
        display: none;
    }
    [data-testid='stFileUploader'] section + div {
        float: right;
        padding-top: 0;
    }

</style>
'''

st.markdown(css, unsafe_allow_html=True)

# if uploaded_files is not None:
# 	filename, file_extension = os.path.splitext(uploaded_files.name)

# 	if (file_extension == ".pdf") is True:
# 		st.success("Upload successful")
#         # Perform intended task here ...
# 	else:
# 		st.error('File type is not PDF')

# if uploaded_files is not None:
# 	filename, file_extension = os.path.splitext(uploaded_files.name)
# 	if (filename == "Payslip") is True:
# 		st.error("Sensitive Data is not allowed!")
# 	else:
# 		pass

## Sensitivity check (not done yet)
def check_sensitivity_label(file_text):
    #NOTE: this is actually just a hack to find a stringmatch in the text of the 1st page. False positives if keywords (case-sensitive) are present anywhere else on the first page.
    

    #labels = ["Strictly Confidential", "Confidential", "Internal", "Public"]
    labels = ["Strictly Confidential", "Confidential"]  
    pattern = re.compile(r"\b(" + "|".join(re.escape(label) for label in labels) + r")\b")
    match = pattern.search(file_text)

    if match:
        return -1
    else:
        return None

def read_pdf(file):
     pdf_reader = PyPDF2.PdfReader(file)
     first_page = pdf_reader.pages[0]
     page_text = first_page.extract_text()
     return page_text

if uploaded_files is not None:
    valid_files = []
    for file in uploaded_files:
        
        # file_text = read_pdf(file) #PyPDF2 us destroying hte file for furhte processing
        file_text = "test"
        sensitivity_label = check_sensitivity_label(file_text)
        violation_value = -1
        if sensitivity_label == violation_value:
            st.error(f"Upload failed for file - '{file.name}'. it is either marked as 'Confidential' or 'Strictly Confidential'and will NOT be processed. Please remove this file and try uploading another file.")
        else:
             valid_files.append(file)

# # Greet user
# if not st.session_state.messages:
# 	with st.chat_message("ai", avatar="static/chatbot.png"):
# 		intro = """Hello, I am Natina.How can I help you?"""
# 		st.markdown(intro)
# 		#Add Bot response to chat History
# 		# st.session_state.messages.append(intro)
# 		# st.session_state.greetings = True



# Accept user input
if prompt := st.chat_input("Type a message"):
    new_files = ""
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.session_state.files.append(
            {"file_name": uploaded_file.name, "file_data": bytes_data, "used": False, "mime_type": uploaded_file.type})
        new_files += uploaded_file.name + "; "
    st.session_state.widget_key = str(randint(1000, 100000000))

    # Add user message to chat history
    st.session_state.messages.append(
        {"role": "human", "avatar":"static/user.png", "content": new_files+"\n"+prompt})
    
    # Display user message in chat message container
    with st.chat_message("human", avatar="static/user.png"):
            st.markdown(prompt,
                        # """
                        # <style>
                        #     .st-emotion-cache-1c7y2kd {
                        #     flex-direction: row-reverse;
                        #     text-align: right;
                        # </style>
                        # """,
                        unsafe_allow_html=True,
                        )

    # Display assistant response in chat message container
    with st.chat_message("ai", avatar="static/chatbot.png"):
        with st.spinner('Processing'):
            response = st.write_stream(response_generator())
        # response=response_generator()
        # st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "ai", "avatar":"static/chatbot.png", "content": response})
    st.rerun()

col1, col2, col3, col4 = st.columns(4, gap="small")

with col1:
	
	st.markdown(
    f'<a href="{url_IIQ}" style="display: inline-block; margin-bottom: 30px;padding: 8px ; background-color:  white;border-color: #B2B2B2; color: #808286; text-align: center; text-decoration: none; font-size: 12px; border-radius: 10px;">How can I access IIQ for my access rights?</a>',
    unsafe_allow_html=True
)
with col2:
	
	st.markdown(
    f'<a href="{url_ticket}" style="display: inline-block; margin-bottom: 30px; padding: 8px ; background-color: white;border-color: #B2B2B2; color: #808286; text-align: center; text-decoration: none; font-size: 12px; border-radius: 10px;">Need to open an HR or Help Desk related ticket?</a>',
    unsafe_allow_html=True
)
with col3:
	
	st.markdown(
    f'<a href="{url_Dax}" style="display: inline-block; margin-bottom: 30px; padding: 8px; background-color: white;border-color: #B2B2B2; color: #808286; text-align: center; text-decoration: none; font-size: 12px; border-radius: 10px;">Give me the current value of the DAX</a>',
    unsafe_allow_html=True
)
with col4:
	
	st.markdown(
    f'<a href="{url_Dax}" style="display: inline-block; margin-bottom: 30px;padding: 8px; background-color: white; color: #808286;border-color: #B2B2B2; text-align: center; text-decoration: none; font-size: 12px; border-radius: 10px;">Provide me the local Remote Working Policy</a>',
    unsafe_allow_html=True
)