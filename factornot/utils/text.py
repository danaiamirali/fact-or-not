from langchain_community.document_loaders import TextLoader
from typing import List
from factornot.fact_checking.checker import Checker
from factornot.fact_checking.searcher import TavilySearcher
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.text_splitter import TokenTextSplitter
from ast import literal_eval

class Statement(BaseModel):
    statement: str = Field(
        ..., description="Repeat in verbatim the phrase(s) or sentence(s) that are a claim or assertation."
    )

class ExtractionData(BaseModel):
    extracted_statements: List[str]

def split_into_statements(llm, input_text: str, statements = None) -> List[str]:
    # loader = TextLoader("./output_en.txt")
    # document = loader.load()[0]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert at identifying claims in text. "
            "Only extract statements that are considered a claim or assertion. "
            "It should be possible to support or refute the statements using evidence found on the web."
            "Return the statements like an array of strings in Python (A PYTHON LIST) - do not return anything else.",
        ),
        # MessagesPlaceholder('examples'), # Keep on reading through this use case to see how to use examples to improve performance
        ("human", "{text}"),
    ])

    def turn_into_list(llm_output) -> list:
        text = llm_output.content
        return literal_eval(text)

    extractor = prompt | llm | turn_into_list

    text_splitter = TokenTextSplitter(
        chunk_size=2000,
        chunk_overlap=20,
    )

    texts = text_splitter.split_text(input_text)
    extractions = extractor.batch(
        [{"text": text} for text in texts],
        {"max_concurrency": 5},  # limit the concurrency by passing max concurrency!
    )

    statements = []
    for extraction in extractions:
        statements.extend(extraction)

    return statements


def check_from_text(llm, input_text: str) -> tuple[List[str], List[str]]:    
    # loader = TextLoader("./output_en.txt")
    # document = loader.load()[0]

    statements = split_into_statements(llm, input_text)
    responses = []
    search_tool = TavilySearcher()
    checker = Checker(llm, search_tool)
    final_statements = []
    for s in statements:
        # obtain the response from the checker
        # should batch this in the future
        try: 
            result = checker.check(s)
        except:
            continue
        final_statements.append(s)
        responses.append(result)

    return final_statements, responses

def check_from_statements(llm, statements: List[str]) -> List[str]:
    responses = []
    search_tool = TavilySearcher()
    checker = Checker(llm, search_tool)
    final_statements = []
    for s in statements:
        # obtain the response from the checker
        # should batch this in the future
        try: 
            result = checker.check(s)
        except:
            continue
        final_statements.append(s)
        responses.append(result)

    return final_statements, responses