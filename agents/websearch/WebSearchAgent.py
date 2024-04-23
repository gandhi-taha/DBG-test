import os
import time
from typing import List
from langchain_google_community import VertexAISearchRetriever
from langchain_google_vertexai import ChatVertexAI, VertexAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.documents import Document
from langchain.tools import tool as langchaintool


with open(os.path.join(os.path.dirname(__file__), "promptTemplate.txt"), "r") as f:
    promptTemplate = ChatPromptTemplate.from_template(f.read())

PROJECT_ID = os.getenv("HR_AGENT_PROJECT_ID", "dbg-dbgenai-sbox-55")
LOCATION_ID = "eu"  # Set to your data store location
SEARCH_ENGINE_ID =  os.getenv("HR_AGENT_SEARCH_ENGINE_ID", "hr-agent_1713441822734")
DATA_STORE_ID =  os.getenv("HR_AGENT_DATA_STORE_ID", "hr-agent-ds_1713441887202")
# DATA_STORE_ID = "hr-agent-ds_1713441887202"  # Set to your data store ID

from vertexai.preview.generative_models import GenerativeModel, Part, grounding, Tool
import vertexai.preview.generative_models as generative_models

model = GenerativeModel(
    "gemini-pro",
    system_instruction=["""Response always in the same language of the userquery. Create a Markdown formated respones. Create the response with a suitable headline."""]
)
chat = model.start_chat()

tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())

generation_config = {
    "max_output_tokens": 3825,
    "temperature": 0.1,
    "top_p": 0.2,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

@langchaintool
def vertexAIWebSearch(question):
    """
    Uses a Datastore VertexAI Search very based on a userquery.
    :param question: User query .
    :return: Response as string.
    """
    print("WebSeach Agents")
    responses = chat.send_message(
        [question],
        generation_config=generation_config,
        safety_settings=safety_settings,
        tools=[tool],
    )
    print(responses.candidates[0].content.parts[0].text)
    source = "\n\n**Source:** This information was fetched via *Google Web Search Grounding*"
    return responses.candidates[0].content.parts[0].text +source
    
    # for word in response.split():
    #    yield word + " "
    #    time.sleep(0.05)
    return response


class WebSearchAgent:
    chain = None

    def __init__(self):
        self.model_name = "gemini-pro"
        self.llm = VertexAI(model_name=self.model_name,
                            temperature=0.2, convert_system_message_to_human=True)
        
        self.chain = (
            vertexAIWebSearch
            # {"answer": lambda x: vertexAIWebSearch(x["question"])}
            # | promptTemplate
            # | self.llm
            # | StrOutputParser()
        )
