
import base64
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, grounding, Tool
import vertexai.preview.generative_models as generative_models

vertexai.init(project="myspace-cstanger", location="europe-west3")
model = GenerativeModel(
    "gemini-1.5-pro-preview-0409",
    system_instruction=["""Antworte immer auf Deutsch"""]
)
chat = model.start_chat()

tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())


def multiturn_generate_content(prompt, files):
    print(chat.history)
    text_response = []
    docs = []
    for file in files:
        docs.append(Part.from_data(
            mime_type="application/pdf",
            data=file["file_data"]))
    docs.append(prompt)

    responses = chat.send_message(
        docs,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
        # tools=[tool]
    )
    return responses


generation_config = {
    "max_output_tokens": 3825,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

