import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.switch_page_button import switch_page
#from orchastrator.orchastrator import Orchastrator
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
import webbrowser


url_Dax = "https://www.investing.com/indices/germany-30"
url_IIQ = "https://iiq-deutsche-boerse.com"
url_ticket = "https://cockpit.deutsche-boerse.com/sites#ticket_hub-Display?filter=hr"



st.set_page_config(layout='wide', page_title="DBGenAI", page_icon="DBG-Logo.png")
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)


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


# def load_lottiefile(filepath: str):

# 	'''Load lottie animation file'''

# 	with open(filepath, "r") as f:
# 		return json.load(f)

# st_lottie(load_lottiefile("images/Nationa-Ai.json"), speed=1, reverse=False, loop=True, quality="high", height=300)


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

def on_click_callback():
	user_prompt = st.session_state.user_prompt
	st.session_state.history.append(user_prompt)


avatars = {
    "user": "static/user.png:",
    "ai": "/static/chatbot.png",}

# Sidebar content 
st.sidebar.image("DBG-Logo.png", use_column_width=True)
sideb = st.sidebar
st.sidebar.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

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
	("HR Persona", "General Persona", "Compliance Persona"),
	)

# Bar2 = sideb.write("-------")
# Text2 = sideb.write(
#  	"""
#  		Copyright © 2024 Deutsche Börse Group - All Rights Reserved.
#  	"""
# )
# button1 = sideb.button(" 📁  HR-Bot")s
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
    with st.chat_message(message["role"]):
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
	uploaded_files = st.sidebar.file_uploader(' ',type=["pdf", "png", "jpeg","jpg"],accept_multiple_files=True ,key=st.session_state.widget_key)

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

# st.markdown(
#     """
#     <style>
#         .stChatFloatingInputContainer {
#             bottom: 10px;
#             background-color: rgba(0, 0, 0, 0)
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

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
        
        file_text = read_pdf(file)
        sensitivity_label = check_sensitivity_label(file_text)
        violation_value = -1
        if sensitivity_label == violation_value:
            st.error(f"Upload failed for file - '{file.name}'. it is either marked as 'Confidential' or 'Strictly Confidential'and will NOT be processed. Please remove this file and try uploading another file.")
        else:
             valid_files.append(file)



# Example prompts
example_prompts = [
    "How can I access IIQ for my access rights?",
    "Need to open an HR or Help Desk related ticket?",
    "Give me the current value of the DAX",
    "Provide me DBGs Remote Working Policy",
]

example_prompts_help = [
    "IIQ access refers to access granted through Sailpoint IdentityIQ, an identity and access management (IAM) tool.",
    "An HR or Help Desk ticket is like a digital request form for employee issues",
    "Stock market index: The DAX, or Deutscher Aktienindex, is a stock market index that tracks the performance of the 40 major German companies trading on the Frankfurt Stock Exchange. It's similar to the S&P 500 in the US.",
    "A Remote Working Policy is a set of rules that a company creates to define how employees can work from outside the office",
]

button_cols = st.columns(2)
button_cols_2 = st.columns(2)

st.markdown(
    """
    <style>
    .element-container:has(style){
        display: none;
    }
    #button-after {
        display: none;
    }
    .element-container:has(#button-after) {
        display: none;
	
    }
    .element-container:has(#button-after) + div button {
        
	display: inline-block;
	margin-bottom: 30px;
	padding: 20px;
	background-color: white;
	border-color: #B2B2B2;
	color: #808286;
	text-align: center;
	text-decoration: none;
	font-size: 18px;
	border-radius: 10px;
	border: solid;
        }
    </style>
    """,
    unsafe_allow_html=True,
)



button_pressed = ""

if button_cols[0].button(example_prompts[0], help=example_prompts_help[0]):
    button_pressed = example_prompts[0]
elif button_cols[1].button(example_prompts[1], help=example_prompts_help[1]):
    button_pressed = example_prompts[1]
elif button_cols_2[0].button(example_prompts[2], help=example_prompts_help[2]):
    button_pressed = example_prompts[2]
elif button_cols_2[1].button(example_prompts[3], help=example_prompts_help[3]):
    button_pressed = example_prompts[3]

if st.session_state is not None:
    del button_cols, button_cols_2






# Accept user input
if prompt := (st.chat_input("Type a message") or button_pressed):
    new_files = ""
    for uploaded_file in valid_files:       #earlier was taken from uploaded_files directly
        bytes_data = uploaded_file.read()
        st.session_state.files.append(
            {"file_name": uploaded_file.name, "file_data": bytes_data, "used": False})
        new_files += uploaded_file.name + "; "
    st.session_state.widget_key = str(randint(1000, 100000000))

    # Add user message to chat history
    st.session_state.messages.append(
        {"role": "human", "content": new_files+"\n"+prompt})
    
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
        {"role": "ai", "content": response})
    st.rerun()

# inputer = st.markdown(
# """
# 	<sytle>
# 	.stChatInputContainer > div {
# 	background-color: #fff;
# 	}
# 	</style>

# """, unsafe_allow_html=True)




# col1, col2, col3, col4 = st.columns(4, gap="small")

# with col1:
	
# 	st.markdown(
#     f'<a href="{url_IIQ}" style="display: inline-block; margin-bottom: 30px; padding: 20px; background-color:  white;border-color: #B2B2B2; color: #808286; text-align: center; text-decoration: none; font-size: 12px; border-radius: 10px;border: solid;">How can I access IIQ for my access rights?</a>',
#     unsafe_allow_html=True
# )
# with col2:
	
# 	st.markdown(
#     f'<a href="{url_ticket}" style="display: inline-block; margin-bottom: 30px; padding: 20px; background-color: white;border-color: #B2B2B2; color: #808286; text-align: center; text-decoration: none; font-size: 12px; border-radius: 10px;border: solid;">Need to open an HR or Help Desk related ticket?</a>',
#     unsafe_allow_html=True
# )
# with col3:
	
# 	st.markdown(
#     f'<a href="{url_Dax}" style="display: inline-block; margin-bottom: 30px; padding: 20px; background-color: white;border-color: #B2B2B2; color: #808286; text-align: center; text-decoration: none; font-size: 12px; border-radius: 10px;border: solid;">Give me the current value of the DAX</a>',
#     unsafe_allow_html=True
# )
# with col4:
	
# 	st.markdown(
#     f'<a href="{url_Dax}" style="display: inline-block; margin-bottom: 30px; padding: 20px; background-color: white; color: #808286; border-color: #B2B2B2; text-align: center; text-decoration: none; font-size: 12px; border-radius: 10px;border: solid;">Provide me DBGs Remote Working Policy</a>',
#     unsafe_allow_html=True
# )

# if st.session_state is not None:
#     del col1,col2,col3,col4


if st.session_state is not None:
    remove= st.sidebar.button("Clear Chat")
    if remove:
        st.session_state.messages = []
        st.success("Chat Successfully cleared")