import os
from langchain_google_vertexai import VertexAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain_core.runnables import RunnableLambda

from langchain.callbacks.tracers import ConsoleCallbackHandler
from orchastrator.agentFactory import AgentFactory

# from langchain.globals import set_debug
# set_debug(True)


with open(os.path.join(os.path.dirname(__file__), "router_prompt_template.txt"), "r") as f:
    router_prompt = PromptTemplate.from_template(f.read())

def format_routes(input_list):
    """
    Formats the input list into a string.
    :param input_list: The list of routes to format.
    :return: The formatted string.
    """
    formatted_items = ["`" + item + "`" for item in input_list]
    output_string = ", ".join(formatted_items[:-1]) + ", or " + formatted_items[-1]
    return output_string

def generate_router_chain(llm):
    """
    Generats the router chains.
    :param llm: an LangChain LLM object to be executed on
    """
    
    prompt_factory = AgentFactory()
    destination_chains = {}
    
    for e in prompt_factory.prompt_infos:
        name = e["name"]
        if "agent" in e:
            # TODO Remote runable
            destination_chains[name]= e['agent'].chain
        else:
            p_template = PromptTemplate.from_template(e["prompt_template"])
            destination_chains[name]= (p_template | VertexAI(model_name="gemini-pro", temperature=1))
    
    route_list = list(destination_chains)

    router_chain = (router_prompt.partial(routes_str=format_routes(route_list)) | llm | StrOutputParser())
    # TODO: greedy search for parsing intent, prevent formating errors 
    
    return {"topic": router_chain, "question": lambda x: x["question"]} | RunnableLambda(lambda x: destination_chains[x["topic"]])    




class Orchastrator:
    """
    The Orchastrator class is responsible for routing user queries to the appropriate destination chains.
    """
    chain = None
    
    def __init__(self):
        self.model_name = "gemini-pro"
        self.llm = VertexAI(model_name=self.model_name, temperature=0)
        self.chain = generate_router_chain(self.llm)

    def route(self, query):
        """
        Routes the user query to the appropriate destination chain.
        :param query: The user query.
        :return: The response from the destination chain.
        """
        return self.chain.stream(query)
    
