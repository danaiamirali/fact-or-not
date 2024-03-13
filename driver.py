from modules.checker import Checker
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os


if __name__ == "__main__":
    load_dotenv()

    # testing code
    model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    checker = Checker(**{"chat_model": model, "SERPAPI_API_KEY": os.getenv("SERPAPI_API_KEY")})
    print(checker.check("Leonardo DiCaprio's father's full name is George Paul DiCaprio"))
    print(checker.check("World War 2 ended in 1946"))
    print(checker.check("World War 2 ended in 1945"))