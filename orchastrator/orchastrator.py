import os
from langchain_google_vertexai import VertexAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain_core.runnables import RunnableLambda

from langchain.callbacks.tracers import ConsoleCallbackHandler
from orchastrator.agentFactory import AgentFactory
import vertexai

# from langchain.globals import set_debug
# set_debug(True)

vertexai.init(
    project=os.getenv("ORCHASTRATOR_PROJECT_ID", "dbg-dbgenai-sbox-55")
)

with open(os.path.join(os.path.dirname(__file__), "router_prompt_template.txt"), "r") as f:
    router_prompt = PromptTemplate.from_template(f.read())

def format_routes(agent_descriptions):
    """
    Formats the input list into a string.
    :param input_list: The list of routes to format.
    :return: The formatted string.
    """
    output_string = " * "+"\n * ".join(agent_descriptions)
    print(output_string)
    return output_string

def generate_router_chain(llm):
    """
    Generats the router chains.
    :param llm: an LangChain LLM object to be executed on
    """
    
    prompt_factory = AgentFactory()
    destination_chains = {}
    agent_descriptions = []
    
    for e in prompt_factory.prompt_infos:
        name = e["name"]
        agent_descriptions.append(e["name"]+": "+e["description"])
        if "agent" in e:
            # TODO Remote runable
            destination_chains[name]= e['agent'].chain
        else:
            p_template = PromptTemplate.from_template(e["prompt_template"])
            destination_chains[name]= (p_template | VertexAI(model_name="gemini-pro", temperature=1))
    

    router_chain = (router_prompt.partial(routes_str=format_routes(agent_descriptions)) | llm | StrOutputParser())
    # TODO: greedy search for parsing intent, prevent formating errors 
    
    return {"topic": router_chain, "question": lambda x: x["question"], "persona": lambda x: x["persona"]} | RunnableLambda(lambda x: destination_chains[x["topic"]])    




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
    
