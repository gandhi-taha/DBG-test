from agents.hr.HRAgent import HRAgent
from agents.websearch.WebSearchAgent import WebSearchAgent


class AgentFactory():
    developer_template = """You are a very smart Python programmer. \
    You provide answers for algorithmic and computer problems in Python. \
    You explain the code in a detailed manner. \

    Here is a question:
    {question}"""


    joke_template = """Make one Chuck Norris joke. Do not offend anyone, but make a joke about how hard it is to work with Citrix". \

    Here is the User question regarding the joke:
    {question}"""

    greeting_template = """You are a polite Chat Agent, available for Employees of 'Deutsche Börse'. You try to support and assist whenevery you can with a smile. \

    Here is the User Input:
    {question}
    Answer:"""

    other_template = """Say that you can not answer the question in a very polite way". \

    Here is the question:
    {question}"""

    prompt_infos = [
        {
            'name': 'Human Resource',
            'description': 'Responsible for questions about Human Resource, appraisals, Expenses, Holidays, time management, training and other People ops related stuff. Also questions about Employees and their data. Questions about John Smith.',
            'agent': HRAgent()
        },
        {
            'name': 'WebSearch',
            'description': 'This Agent is good for general web search questions about stocks like the DAX.',
            'agent': WebSearchAgent()
        },
        {
            'name': 'Python Programmer',
            'description': 'Good for questions about coding and algorithms',
            'prompt_template': developer_template
        },
        {
            'name': 'Joke',
            'description': 'Responsible for providing jokes.',
            'prompt_template': joke_template
        },
        {
            'name': 'Greeting',
            'description': 'Responsible for answering on greetings, Hello, Hi, How are you, etc. Also about saying Goodbye.',
            'prompt_template': greeting_template
        },
        {
            'name': 'Other',
            'description': 'For all other general questions.',
            'agent': WebSearchAgent()
        }
    ]