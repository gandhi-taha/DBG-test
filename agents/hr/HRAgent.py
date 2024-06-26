import os
import time
from typing import Generator, List
from langchain_google_community import VertexAISearchRetriever
from langchain_google_vertexai import ChatVertexAI, VertexAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.documents import Document
from langchain.tools import tool


from agents.hr.VertexSearch import search_sample


with open(os.path.join(os.path.dirname(__file__), "promptTemplate.txt"), "r") as f:
    promptTemplate = ChatPromptTemplate.from_template(f.read())

PROJECT_ID = os.getenv("HR_AGENT_PROJECT_ID", "dbg-dbgenai-sbox-55")
LOCATION_ID = "eu"  # Set to your data store location
SEARCH_ENGINE_ID = os.getenv(
    "HR_AGENT_SEARCH_ENGINE_ID", "hr-agent_1713441822734")
PRIVATE_SEARCH_ENGINE_ID = os.getenv(
    "HR_AGENT_PRIVATE_SEARCH_ENGINE_ID", "hr-persona-agent_1713791886697")
DATA_STORE_ID = os.getenv("HR_AGENT_DATA_STORE_ID",
                          "hr-agent-ds_1713441887202")
# DATA_STORE_ID = "hr-agent-ds_1713441887202"  # Set to your data store ID


def format_docs(docs: List[Document]):
    """
    Formats the input list into a string.
    :param input_list: The list of routes to format.
    :return: The formatted string.
    """
    print(docs[0])
    return "\n\n".join(doc.page_content for doc in docs)


@tool
def vertexAISearch(question: str, persona: str):
    """
    Uses a Datastore VertexAI Search very based on a userquery.
    :param question: User query .
    :param persona: User persona of the query .
    :return: Response as string.
    """
    print("HR Agents")
    prompt="""Role: You are an intelligent chat bot and your goal is to provide the best answer for a given question. Answer in the same language the question is asked. Make sure to always return the response as markdown in a nice and structured format. Don't use code block and do not start with ```"""
    response = search_sample(
        project_id=PROJECT_ID,
        location=LOCATION_ID,
        engine_id=PRIVATE_SEARCH_ENGINE_ID if persona == "HR Persona" else SEARCH_ENGINE_ID,
        search_query=question,
        prompt=prompt
        )
    return response
    # for word in response.split():
    #    yield word + " "


class HRAgent:
    chain = None

    def __init__(self):
        self.model_name = "gemini-pro"
        self.llm = VertexAI(model_name=self.model_name,
                            temperature=0.5, convert_system_message_to_human=True)

        self.chain = (
            vertexAISearch
            # {"answer": RunnableLambda(vertexAISearch)}
            # | promptTemplate
            # | self.llm
            # | StrOutputParser()
        )
