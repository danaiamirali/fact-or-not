from pydantic import BaseModel
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool, Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub
import os

"""
An LLM-wrapper that can be used to fact check a given statement. 
The wrapper uses internet lookup via function calling to verify statements using the internet, if necessary. 

Requires:
    - A ChatOpenAI model to be passed in as an argument.

Usage:
    model = ChatOpenAI()
    checker = Checker(model)
    checker.check('The earth is flat')
    # Output: False
    checker.check('The earth is round')
    # Output: True
"""
class Checker():
    def __init__(self, model, api_key):
        self.chat_model = model
        self.TAVILY_API_KEY = api_key

    def check(self, statement: str) -> bool:
        tools = [TavilySearchResults()]

        instructions = """
            Is the following statement true or false? 

            If the statement is true, please respond with "True." and then provide the source.
            If the statement is false, please respond with "False." and then provide a version of the statement that is actually true, with a source.
            If you are unsure, or there is a lack of reputable sources, please respond with "Unsure."

            Use the search tool to find a source for every answer, and output the source as "Source: link." 
        """
        base_prompt = hub.pull("langchain-ai/openai-functions-template")
        prompt = base_prompt.partial(instructions=instructions)

        agent = create_openai_functions_agent(self.chat_model, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
        )

        response = agent_executor.invoke({"input": statement})
        
        return response
    
"""
A streaming version of the Checker class.
"""
class StreamingChecker(Checker):
    pass