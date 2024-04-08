from foxornot.fact_checking.checker import Checker
from foxornot.fact_checking.searcher import TavilySearcher
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    model = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
    search_tool = TavilySearcher()
    checker = Checker(model, search_tool)
    print(checker.check('The earth is flat'))
    # Output: False
    print(checker.check('The earth is round'))
    # Output: True