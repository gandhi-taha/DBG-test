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
from langchain.tools import  tool


from agents.hr.VertexSearch import search_sample


with open(os.path.join(os.path.dirname(__file__), "promptTemplate.txt"), "r") as f:
    promptTemplate = ChatPromptTemplate.from_template(f.read())

PROJECT_ID = "myspace-cstanger"  # Set to your Project ID
LOCATION_ID = "eu"  # Set to your data store location
SEARCH_ENGINE_ID = "db-hr_1713275680756"  # Set to your search app ID
# DATA_STORE_ID = "db-test_1713280342754"  # Set to your data store ID


def format_docs(docs: List[Document]):
    """
    Formats the input list into a string.
    :param input_list: The list of routes to format.
    :return: The formatted string.
    """
    print(docs[0])
    return "\n\n".join(doc.page_content for doc in docs)


@tool
def vertexAISearch(question):
    """
    Uses a Datastore VertexAI Search very based on a userquery.
    :param question: User query .
    :return: Response as string.
    """
    response =  search_sample(
        project_id=PROJECT_ID, 
        location=LOCATION_ID, 
        engine_id="db-hr-test_1713279819955", 
        search_query=question, )
    
    # for word in response.split():
    #    yield word + " "
    #    time.sleep(0.05)
    return response


class HRAgent:
    chain = None

    def __init__(self):
        self.model_name = "gemini-pro"
        self.llm = VertexAI(model_name=self.model_name,
                            temperature=0.5, convert_system_message_to_human=True)
        
        self.chain = (
            {"answer": lambda x: vertexAISearch(x["question"])}
            | promptTemplate
            | self.llm
            | StrOutputParser()
        )
