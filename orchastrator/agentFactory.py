from agents.hr.HRAgent import HRAgent


class AgentFactory():
    developer_template = """You are a very smart Python programmer. \
    You provide answers for algorithmic and computer problems in Python. \
    You explain the code in a detailed manner. \

    Here is a question:
    {question}"""


    joke_template = """Only make Chuck Norris jokes. Do not offend anyone. Include finacial topics". \

    Here is the User question:
    {question}"""

    other_template = """Say that you can not answer the question in a very polite way". \

    Here is the question:
    {question}"""

    prompt_infos = [
        {
            'name': 'Human Resource',
            'description': 'Responsible for questions about Human Resource, Employee management, Expenses, Holidays, employment policies and other People ops related stuff.',
            'prompt_template': other_template,
            'agent': HRAgent()
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
            'name': 'Other',
            'description': 'For all other general questions.',
            'prompt_template': other_template
        }
    ]