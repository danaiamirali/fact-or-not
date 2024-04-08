
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub
from pydantic import BaseModel, Field
from typing import List
import regex as re

class Output(BaseModel):
    reasoning: str = Field(
        ..., description="Reason through the input statement and the sources found, and analyze if the sources support the input statement."
    )
    sources: List[str] | str = Field(
        ..., description="Provide the sources used in the response."
    )
    conclusion: str = Field(
        ..., description="Write one of the following: 'True', 'Mostly true', 'Slightly true', 'False.'"
    )

    def reasoning(self):
        return self.reasoning
    
    def sources(self):
        return self.sources
    
    def conclusion(self):
        return self.conclusion

    def __str__(self):
        return f"{self.reasoning}\n{self.sources}\n{self.conclusion}"

    def __repr__(self):
        return self.reasoning, self.sources, self.conclusion

    
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
    def __init__(self, model, search_tool, verbose=False):
        self.chat_model = model
        self.search_tool = search_tool
        self.verbose = verbose

    def check(self, statement: str, clean: bool = True) -> str | tuple[str, str, str]:
        instructions = """
            Determine if there are sources of text that verify the input statment.
            Use the tool to search the web and find sources about the input statement. 
            Explain if the text found supports the input statement, or proves it wrong.
            Provide the sources used afterwards.

            Format your response as follows:

            1. Reasoning: Reason through the input statement and the sources found, and analyze if the sources support the input statement. Make your own factually support statements, providing evidence based off the sources (which should be cited in IEEE format, using parenthetical citation). Keep this brief, going up to 300 words at most.
            2. Sources: Provide the sources used in the response in a IEEE references standard. Link the used articles in a markdown format.
            3. Conclusion: Write one of the following: "True", "Mostly true", "Slightly true", "False."

    
            EXAMPLE:
            Statement: Iran attacked Israel yesterday.
            Response: 
            1. **Reasoning:** The recent news articles reviewed do not support the statement that "Iran attacked Israel yesterday." Instead, 
            they highlight a series of escalations and retaliatory actions between Israel and Iran, predominantly focused on incidents outside of 
            Israel's borders, such as an Israeli airstrike on Iran's consulate in Syria and subsequent Iranian threats and actions [1]. 
            Iran's Revolutionary Guards did claim to have attacked an Israeli "spy HQ" in Iraq and vowed further actions as revenge for the airstrike in 
            Syria ([4]). Moreover, there were responses and military movements indicating heightened tensions and potential for retaliatory actions, 
            but no direct mention of an Iranian attack on Israeli soil within the provided time frame was found.

            2. **Sources:**
            [1] [Al Jazeera Article on Israel striking Iran's consulate in Syria](https://www.aljazeera.com/news/2023/4/3/israel-strikes-iran-consulate-in-syria-killing-several-irgc-members)
            [2] [The Times of Israel Article on Israel preparing for retaliatory attacks](https://www.timesofisrael.com/liveblog_entry/iran-threatens-israeli-embassies-as-gallant-says-country-prepared-for-any-scenario/)
            [3] [Al Jazeera Article on Iran launching missile strikes](https://www.aljazeera.com/news/2023/4/6/iran-launches-missile-strikes-in-iraq-and-syria-citing-security-threats)
            [4] [Yahoo News Article on Iran's Revolutionary Guards attacking Israel's 'spy HQ' in Iraq](https://news.yahoo.com/iran-says-revolutionary-guards-attack-040500897.html)
            [5] [Al Jazeera Article on a US base attacked in Iraq](https://www.aljazeera.com/news/2023/4/7/us-base-attacked-in-iraq-hours-after-iran-vows-revenge-for-damascus-attack)

            3. **Conclusion:** False.
        """
        
        base_prompt = hub.pull("langchain-ai/openai-functions-template")
        prompt = base_prompt.partial(instructions=instructions)

        tools = [self.search_tool]

        agent = create_openai_functions_agent(self.chat_model, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=self.verbose,
        )
        
        response = agent_executor.invoke({"input": statement})["output"]

        if clean:
            response = re.sub(r"\d\.", "", response)
            # print(response)
                
            try:    
                parts = re.split("Reasoning:|Sources:|Conclusion:", response)
                
                reasoning = parts[1].strip()
                sources = parts[2]
                conclusion = parts[3].strip()
            except:
                raise Exception(f"Could not parse response: {response}")

            return reasoning, sources, conclusion

        return response
    
"""
A streaming version of the Checker class.
"""
class StreamingChecker(Checker):
    pass