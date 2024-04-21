import streamlit as st
import os


st.set_page_config(layout='wide', page_title="Natina-AI", page_icon="DBG-Logo.png")


st.title("Data-Upload")

uploaded_file = st.file_uploader(
    label="Upload here please",
    #type=["xlsx"], # Comment out to evade Streamlit's built-in file type detector
    help="Upload the required file here please")
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

if uploaded_file is not None:
	filename, file_extension = os.path.splitext(uploaded_file.name)

	if (file_extension == ".pdf") is True:
		st.success("Upload successful")
        # Perform intended task here ...
	else:
		st.error('File type is not PDF')

if uploaded_file is not None:
	filename, file_extension = os.path.splitext(uploaded_file.name)
	if (filename == "Payslip") is True:
		st.error("Sensitive Data is not allowed!")
	else:
		pass