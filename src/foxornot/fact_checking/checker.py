
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub

"""
An LLM-wrapper that can be used to fact check a given statement. 
The wrapper uses internet lookup via function calling to verify statements using the internet, if necessary. 

Requires:
    - A ChatOpenAI model to be passed in as an argument.
    - A search tool to be passed in as an argument. The LLM will use this tool to search the web for information.

Usage:
    model = ChatOpenAI()
    search_tool = TavilySearchResults()
    checker = Checker(model, search_tool)
    checker.check('The earth is flat')
    # Output: False
    checker.check('The earth is round')
    # Output: True
"""
class Checker():
    def __init__(self, model, search_tool):
        self.chat_model = model
        self.search_tool = search_tool

    def check(self, statement: str) -> bool:
        instructions = """
            Determine if there are sources of text that verify the input statment.
            Use the tool to search the web and find sources about the input statement. 
            Explain if the text found supports the input statement, or proves it wrong.
            Provide the sources used afterwards.

            Format your response as follows:

            1. Reason through the input statement and the sources found, and analyze if the sources support the input statement.
            2. Provide the sources used in the response.
            3. Write one of the following: "True", "Mostly true", "Slightly true", "False."
            
            Example Response:
            Reasoning: The sources found provide evidence that the earth is round.
            Sources: [Wikipedia, National Geographic, NASA]
            Conclusion: True
        """
        
        base_prompt = hub.pull("langchain-ai/openai-functions-template")
        prompt = base_prompt.partial(instructions=instructions)

        tools = [self.search_tool]

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