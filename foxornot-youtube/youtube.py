from typing import List
from foxornot.fact_checking.checker import Checker
from foxornot.fact_checking.searcher import TavilySearcher
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import TokenTextSplitter

class Statement(BaseModel):
    statement: str = Field(
        ..., description="Repeat in verbatim the phrase(s) or sentence(s) that are a claim or assertation."
    )

class ExtractionData(BaseModel):
    extracted_statements: List[Statement] 

def check_from_text(input_text: str) -> tuple[List[str], List[str]]:    
    # loader = TextLoader("./output_en.txt")
    # document = loader.load()[0]

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

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
    )

    extractor = prompt | llm

    text_splitter = TokenTextSplitter(
        chunk_size=2000,
        chunk_overlap=20,
    )

    texts = text_splitter.split_text(input_text)

    extractions = extractor.batch(
        [{"text": text} for text in texts],
        {"max_concurrency": 5},  # limit the concurrency by passing max concurrency!
    )

    statement_objects = []
    for extraction in extractions:
        print("EXTRACTION | ", extraction)
        statement_objects.extend(extraction)

    statements = []
    responses = []
    search_tool = TavilySearcher()
    checker = Checker(llm, search_tool)
    for s in statement_objects:
        statements.append(s)
        responses.append(checker.check(s))

    return statements, responses

from pytube import YouTube
import openai

def video_to_text(url: str) -> str:
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()

    output_path = "audios"
    filename = "audio.mp3"
    audio_stream.download(output_path=output_path, filename=filename)

    client = openai.OpenAI()
    file = open(f"{output_path}/{filename}", "rb")

    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=file
    )
    return transcription.text