from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub

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
        instructions = """
            Determine if there are sources of text that verify the input statment.
            Use the tool to search the web and find sources about the input statement. 
            Explain if the text found supports the input statement, or proves it wrong.
            Provide the sources used afterwards.
            At the very beginning of the response before anything else, write one of the 
            following based on the rest of the response: 
            "True", "Mostly true", "Slightly true", "False".
        """
        
        base_prompt = hub.pull("langchain-ai/openai-functions-template")
        prompt = base_prompt.partial(instructions=instructions)

        tools = [TavilySearchResults()]

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