from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
#pip install langchain_openai
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import os
import openai
import faiss
import numpy as np
#pip install PyPDF2 sentence-transformers faiss-cpu
from langchain.schema import (
    HumanMessage,
    SystemMessage
)

#import requests
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))

article_txt=open("article1.txt","r")
article_str = article_txt.read() # string of the entire file

#paragraphs = article_str.split('\n\n') #list each paragraph is an element
#embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

loader = TextLoader(file_path="article1.txt")
documents = loader.load()

# Split and embed the text in the documents
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))




