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

url_Dax = "https://www.investing.com/indices/germany-30"
url_IIQ = "https://iiq-deutsche-boerse.com"
url_ticket = "https://cockpit.deutsche-boerse.com/sites#ticket_hub-Display?filter=hr"

st.set_page_config(layout='wide', page_title="DBGenAI",
                   page_icon="DBG-Logo.png")
st.write(
    '<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)


def response_generator():
    st.session_state.greetings = False
    new_docs = None

    # Routing for Alfred
    if st.session_state.file["name"] != "none":
        if st.session_state.file["used"] == False:
            print("USE FILE")
            new_docs = st.session_state.file
            st.session_state.file["used"] = True
        response = multiturn_generate_content(prompt, new_docs)

        for respone in response:
            yield respone.candidates[0].content.parts[0].text
            time.sleep(0.05)
    # Routing to generall orchastrator
    else:
        orchastrator = Orchastrator()
        response = orchastrator.route(
            {"question": prompt, "persona": selectionbox})
        for respone in response:
            yield respone
            time.sleep(0.05)


avatars = {
    "user": "static/user.png:",
    "ai": "/static/chatbot.png", }

# Sidebar content
st.sidebar.image("DBG-Logo.png", use_column_width=True)
sideb = st.sidebar
subheader = st.sidebar.markdown(
    f'<a href="" style="display: flex; ;margin-top: 50px; padding:5px; padding-left:50px; padding-right:50px;  background-color: white; color: #0A07C7; border-color: #0A07C7; text-align: center; text-decoration: none; font-size: 15px; border-radius: 10px;border: solid;"> ➕  New Conversation</a>',
    unsafe_allow_html=True
)


Bar1 = sideb.write("-------")
text1 = st.sidebar.markdown(
    f'<a href="" style="display: inline-block; padding: 8px;color: #808286; text-align: center; text-decoration: none; font-size: 12px;">CHAT HISTORY</a>',
    unsafe_allow_html=True
)
text2 = st.sidebar.markdown(
    f'<a href="" style="display: inline-block; padding: 8px;color: #808286; text-align: center; text-decoration: none; font-size: 15px;">💬 Annual Report</a>',
    unsafe_allow_html=True
)
text3 = st.sidebar.markdown(
    f'<a href="" style="display: inline-block; padding: 8px;color: #808286; text-align: center; text-decoration: none; font-size: 15px;">💬 Learning Opportunity</a>',
    unsafe_allow_html=True
)
text4 = st.sidebar.markdown(
    f'<a href="" style="display: inline-block; padding: 8px;color: #808286; text-align: center; text-decoration: none; font-size: 15px;">💬 Python Script</a>',
    unsafe_allow_html=True
)
text5 = st.sidebar.markdown(
    f'<a href="" style="display: inline-block; padding: 8px;color: #808286; text-align: center; text-decoration: none; font-size: 15px;">💬 Investor Presentation</a>',
    unsafe_allow_html=True
)

Bar2 = sideb.write("-------")
selectionbox = sideb.selectbox(
	"Select a role",
	("General Persona", "HR Persona",  "Compliance Persona"),
	)


# Main content
header = st.markdown(
    f'<a style="display: absolute;margin-top:50px;background: linear-gradient(90deg, #10D1DE, #1071DE, #ff00f3, #0033ff, #ff00c4, #ff0000); background-size: 400%;-webkit-background-clip: text; -webkit-text-fill-color: transparent;text-align: center; text-decoration: none; font-family: sans-serif; font-size: 50px;Letter-spacing: -10px;word-spacing: -10px;">Good afternoon, Lars Bolanca</a>',
    unsafe_allow_html=True
)
subheader = st.markdown(
    f'<a style="display: absolute; color: #C8C8C8; margin-bottom:20px; text-align: center; text-decoration: none; font-family: sans-serif; font-size: 50px;">How can I help you?</a>',
    unsafe_allow_html=True
)

# Initialize File Uploader
if "file" not in st.session_state:
    st.session_state.file = {}
    st.session_state.file["name"] = "none"

if "fileKey" not in st.session_state:
    st.session_state.fileKey = randint(1000, 100000000)
    st.session_state.fileError = None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.greetings = True
    

# Display chat messages from history on app rerun


for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

with stylable_container(
    key="bottom_content",
    css_styles="""
        {
            position: fixed;
            bottom: 120px;
        }
        """,
):
    uploaded_file = st.sidebar.file_uploader(' ', type=[
        "pdf", "jpeg", "png", "jpg"],
        accept_multiple_files=False,
        key=st.session_state.fileKey)

css = '''
<style>
[data-testid='stFileUploader'] {
    display: flex;
    align-items: center;
}
[data-testid='stFileUploader'] section {
    padding: 0;
}
[data-testid='stFileUploader'] section > input + div {
    display: none;
}
[data-testid='stFileUploader'] section + div {
    margin-left: 1cm; /* Adjust spacing for browse button */
    margin-right: auto; /* Push uploaded file name to the right */
}
</style>
'''

st.markdown(css, unsafe_allow_html=True)

# if uploaded_file is not None:
# 	filename, file_extension = os.path.splitext(uploaded_file.name)

# 	if (file_extension == ".pdf") is True:
# 		st.success("Upload successful")
#         # Perform intended task here ...
# 	else:
# 		st.error('File type is not PDF')

# if uploaded_file is not None:
# 	filename, file_extension = os.path.splitext(uploaded_file.name)
# 	if (filename == "Payslip") is True:
# 		st.error("Sensitive Data is not allowed!")
# 	else:
# 		pass

# Sensitivity check (not done yet)


# def check_sensitivity_label(file_text):
#     # NOTE: this is actually just a hack to find a stringmatch in the text of the 1st page. False positives if keywords (case-sensitive) are present anywhere else on the first page.

#     # labels = ["Strictly Confidential", "Confidential", "Internal", "Public"]
#     labels = ["Strictly Confidential", "Confidential"]
#     pattern = re.compile(r"\b(" + "|".join(re.escape(label)
#                          for label in labels) + r")\b")
#     match = pattern.search(file_text)

#     if match:
#         return -1
#     else:
#         return None


# def read_pdf(file):
#     pdf_reader = PyPDF2.PdfReader(file)
#     first_page = pdf_reader.pages[0]
#     page_text = first_page.extract_text()
#     return page_text


# if uploaded_file is not None:
#     valid_files = []
#     for file in uploaded_file:

#         # file_text = read_pdf(file) #PyPDF2 us destroying hte file for furhte processing
#         file_text = "test"
#         sensitivity_label = check_sensitivity_label(file_text)
#         violation_value = -1
#         if sensitivity_label == violation_value:
#             st.error(
#                 f"Upload failed for file - '{file.name}'. it is either marked as 'Confidential' or 'Strictly Confidential'and will NOT be processed. Please remove this file and try uploading another file.")
#         else:
#             valid_files.append(file)

# # Greet user
# if not st.session_state.messages:
# 	with st.chat_message("ai", avatar="static/chatbot.png"):
# 		intro = """Hello, I am Natina.How can I help you?"""
# 		st.markdown(intro)
# 		#Add Bot response to chat History
# 		# st.session_state.messages.append(intro)
# 		# st.session_state.greetings = True


# Example prompts
example_prompts = [
    "How can I access IIQ for my access rights?",
    "Need to open an HR or Help Desk related ticket?",
    "How is the DAX doing today?",
    "Provide me DBGs Remote Working Policy",
]

example_prompts_help = [
    "IIQ access refers to access granted through Sailpoint IdentityIQ, an identity and access management (IAM) tool.",
    "An HR or Help Desk ticket is like a digital request form for employee issues",
    "Stock market index: The DAX, or Deutscher Aktienindex, is a stock market index that tracks the performance of the 40 major German companies trading on the Frankfurt Stock Exchange. It's similar to the S&P 500 in the US.",
    "A Remote Working Policy is a set of rules that a company creates to define how employees can work from outside the office",
]

# button_cols = st.columns(2)
# button_cols_2 = st.columns(2)
button_pressed = ""
if st.session_state.greetings:
    with stylable_container(
        key="button_content",
        css_styles="""
            {
                display: inline-block;
                margin-top: 10px;
                margin-bottom: 10px;
                margin-left: 10px;
                margin-right: 10px;
                color: #808286;
                text-align: center
            }
            """,
    ):
        button_cols = st.columns(2)

    with stylable_container(
        key="button_content_2",
        css_styles="""
            {
                display: inline-block;
                margin-top: 10px;
                margin-bottom: 10px;
                margin-left: 10px;
                margin-right: 10px;
                color: #808286;
                text-align: center
                padding-bottom
            }
            """,
    ):
        button_cols_2 = st.columns(2)



    if button_cols[0].button(example_prompts[0], help=example_prompts_help[0]):
        button_pressed = example_prompts[0]
    elif button_cols[1].button(example_prompts[1], help=example_prompts_help[1]):
        button_pressed = example_prompts[1]
    elif button_cols_2[0].button(example_prompts[2], help=example_prompts_help[2]):
        button_pressed = example_prompts[2]
    elif button_cols_2[1].button(example_prompts[3], help=example_prompts_help[3]):
        button_pressed = example_prompts[3]



if st.session_state is not None:
    if uploaded_file is not None: 
            if uploaded_file.name == "202404_Payroll.pdf":
                st.session_state.fileError=f"The file '{uploaded_file.name}' is labeled Strictly Confidential and cannot be uploaded."

                st.session_state.fileKey+=1
                st.rerun()


# Accept user input
if prompt := st.chat_input("Type a message") or button_pressed:
    st.session_state.fileError=None
    new_files = ""
    if uploaded_file is not None:
        if uploaded_file.name != st.session_state.file["name"]:
            print("ADD NEW FILE")
            st.session_state.file["name"] = uploaded_file.name
            st.session_state.file["mime_type"] = uploaded_file.type
            bytes_data = uploaded_file.getvalue()
            st.session_state.file["file_data"] = bytes_data
            st.session_state.file["used"] = False
    else:
        print("REMOVE FILE")
        st.session_state.file["name"] = "none"

    # Add user message to chat history
    st.session_state.messages.append(
        {"role": "human", "avatar": "static/user.png", "content": new_files+"\n"+prompt})

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
    print(response)
    st.session_state.messages.append(
        {"role": "ai", "avatar": "static/chatbot.png", "content": response})
    st.rerun()


# if st.session_state.greetings:
#     container = st.container()
#     col1, col2, col3, col4 = container.columns(4, gap="small")

#     with col1:

#         st.markdown(
#             f'<a href="{url_IIQ}" style="display: inline-block; margin-bottom: 30px; padding: 20px; background-color:  white;border-color: #B2B2B2; color: #808286; text-align: center; text-decoration: none; font-size: 12px; border-radius: 10px;border: solid;">How can I access IIQ for my access rights?</a>',
#             unsafe_allow_html=True
#         )
#     with col2:

#         st.markdown(
#             f'<a href="{url_ticket}" style="display: inline-block; margin-bottom: 30px; padding: 20px; background-color: white;border-color: #B2B2B2; color: #808286; text-align: center; text-decoration: none; font-size: 12px; border-radius: 10px;border: solid;">Need to open an HR or Help Desk related ticket?</a>',
#             unsafe_allow_html=True
#         )
#     with col3:

#         st.markdown(
#             f'<a href="{url_Dax}" style="display: inline-block; margin-bottom: 30px; padding: 20px; background-color: white;border-color: #B2B2B2; color: #808286; text-align: center; text-decoration: none; font-size: 12px; border-radius: 10px;border: solid;">Give me the current value of the DAX</a>',
#             unsafe_allow_html=True
#         )
#     with col4:

#         st.markdown(
#             f'<a href="{url_Dax}" style="display: inline-block; margin-bottom: 30px; padding: 20px; background-color: white; color: #808286; border-color: #B2B2B2; text-align: center; text-decoration: none; font-size: 12px; border-radius: 10px;border: solid;">Provide me DBGs Remote Working Policy</a>',
#             unsafe_allow_html=True
#         )

if st.session_state.fileError is not None:
    st.error(st.session_state.fileError)

if st.session_state is not None:
    remove = st.sidebar.button("Clear Chat")
    # if uploaded_file is not None: 
    #         if uploaded_file.name == "202404_Payroll.pdf":
    #             st.error(f"The file '{uploaded_file.name}' is labeled Strictly Confidential and cannot be uploaded.")
    #             st.session_state.fileKey+=1

    if remove:
        st.session_state.messages = []
        st.session_state.file = {}
        st.session_state.greetings == True
        st.session_state.fileKey+=1
        st.session_state.clear()
        st.rerun()
        st.success("Chat Successfully cleared")
