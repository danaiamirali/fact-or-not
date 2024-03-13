from pydantic import BaseModel
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool, Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
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
class Checker(BaseModel):
    chat_model: ChatOpenAI
    SERPAPI_API_KEY: str

    def check(self, statement: str) -> bool:

        search = GoogleSerperAPIWrapper(serper_api_key=self.SERPAPI_API_KEY)

        tools = [
            Tool(
                name="Intermediate Answer",
                func=search.run,
                description='google search'
            )
        ]
        
        agent = initialize_agent(
            agent="self-ask-with-search",
            tools=tools,
            llm=self.chat_model,
            verbose=True,
            handle_parsing_errors=True,
        )

        prompt = PromptTemplate.from_template(
            """
            Is the following statement true or false? 

            If the statement is true, please respond with "True." and then provide the source.
            If the statement is false, please respond with "False." and then provide a version of the statement that is actually true, with a source.
            If you are unsure, or there is a lack of reputable sources, please respond with "Unsure."

            Use google search to verify the statement if necessary.

            Statement: {statement}

            """
        )

        print(prompt.format(statement=statement))

        response = agent.invoke(prompt.format(statement=statement))
        
        return response
    
"""
A streaming version of the Checker class.
"""
class StreamingChecker(Checker):
    pass