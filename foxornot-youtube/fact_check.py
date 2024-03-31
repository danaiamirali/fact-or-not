from langchain_community.document_loaders import TextLoader
from typing import List, Optional
from langchain.chains import create_structured_output_runnable
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_text_splitters import TokenTextSplitter
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_functions_agent

class Statement(BaseModel):
    statement: str = Field(
        ..., description="Repeat in verbatim the phrase(s) or sentence(s) that are a claim or assertation."
    )


class ExtractionData(BaseModel):
    extracted_statements: List[Statement]
    

loader = TextLoader("./output_en.txt")
document = loader.load()[0]


# Define a custom prompt to provide instructions and any additional context.
# 1) You can add examples into the prompt template to improve extraction quality
# 2) Introduce additional parameters to take context into account (e.g., include metadata
#    about the document from which the text was extracted.)
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert at identifying claims in text. "
        "Only extract statements that are considered a claim or assertion. "
        "It should be possible to support or refute the statements using evidence found on the web.",
    ),
    # MessagesPlaceholder('examples'), # Keep on reading through this use case to see how to use examples to improve performance
    ("human", "{text}"),
])


# We will be using tool calling mode, which
# requires a tool calling capable model.
llm = ChatOpenAI(
    # Consider benchmarking with a good model to get
    # a sense of the best possible quality.
    model="gpt-3.5-turbo",
    # Remember to set the temperature to 0 for extractions!
    temperature=0,
)

# Maybe we don't need .with_strucutred_output
extractor = prompt | llm.with_structured_output(
    schema=ExtractionData,
    method="function_calling",
    include_raw=False,
)

text_splitter = TokenTextSplitter(
    # Controls the size of each chunk
    chunk_size=2000,
    # Controls overlap between chunks
    chunk_overlap=20,
)

texts = text_splitter.split_text(document.page_content)

# Limit just to the first 3 chunks
# so the code can be re-run quickly
extractions = extractor.batch(
    [{"text": text} for text in texts],
    {"max_concurrency": 5},  # limit the concurrency by passing max concurrency!
)

statement_objects = []
for extraction in extractions:
    statement_objects.extend(extraction.extracted_statements)

statements = []
responses = []
for s in statement_objects:
    statements.append(s.statement)
    base_prompt = hub.pull("langchain-ai/openai-functions-template")

    instructions = """
        Determine if there are sources of text that verify the input statment.
        Use the tool to search the web and find sources about the input statement. 
        Explain if the text found supports the input statement, or proves it wrong.
        Provide the sources used afterwards.
        At the very beginning of the response before anything else, write one of the 
        following based on the rest of the response: 
        "True", "Mostly true", "Slightly true", "False".
    """
    
    prompt = base_prompt.partial(instructions=instructions)

    tools = [TavilySearchResults()]

    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
    )
    
    response = agent_executor.invoke({"input": s.statement})
    responses.append(response)

print(responses)
