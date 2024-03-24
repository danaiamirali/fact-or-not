from modules.checker import Checker
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os


if __name__ == "__main__":
    load_dotenv()

    # testing code
    model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    checker = Checker(model, os.getenv("BRAVE_API_KEY"))
    
    print(checker.check("The Eiffel Tower is located in Berlin"))
    print(checker.check("Water boils at 100 degrees Celsius at sea level"))
    print(checker.check(" Humans and dinosaurs coexisted at some point in history"))
    print(checker.check("The honeybee is the only insect that produces food eaten by humans"))
    print(checker.check("Leonardo DiCaprio's father's full name is George Paul DiCaprio"))
    print(checker.check("World War 2 ended in 1946"))
    print(checker.check("World War 2 ended in 1945"))
