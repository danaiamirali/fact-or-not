# from langchain_community.chat_models import ChatOpenAI
# from openai import OpenAI
# from langchain_openai import OpenAIEmbeddings
# from langchain_openai import ChatOpenAI
# #pip install langchain_openai
# from langchain_community.document_loaders import TextLoader
# from langchain.text_splitter import CharacterTextSplitter
# from dotenv import load_dotenv
import os
import openai
# import numpy as np
import threading
#pip install PyPDF2 sentence-transformers faiss-cpu
# from langchain.schema import (
#     HumanMessage,
#     SystemMessage
# )
#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

#floor(len(list) / 2) - 1

def formatting(response):
    response = response[161:]
    for index, char in enumerate(response):
        if response[index:index + 4] == "role":
            response = response[:index - 3]
            break
    return response

# def ending_output(text_response_input, final_prompt, client): #text_response is a list
#     new_text_response = []
#     if(len(text_response_input) == 1):
#         #print(text_response_input[0])
#         final = str(text_response_input[0])
#         return final
#     if (len(text_response_input) % 2 == 0):
#         for i in range(0,len(text_response_input)-1,2):
#             ending_response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": final_prompt+text_response_input[i]+"\n\n\n 2. "+text_response_input[i+1]}])  

#             ending_response = str(ending_response)
#             ending_response = formatting(ending_response)
#             new_text_response.append(ending_response)

#     else:
#         ending_response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": final_prompt+text_response_input[0]+"\n\n\n 2. "+text_response_input[1]+"\n\n\n 3. "+text_response_input[2]}])  
#         ending_response = str(ending_response)
#         ending_response = formatting(ending_response)
#         new_text_response.append(ending_response)
#         for i in range(3,len(text_response_input)-1,2):
#             ending_response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": final_prompt+text_response_input[i]+"\n\n\n 2. "+text_response_input[i+1]}])  

#             ending_response = str(ending_response)
#             ending_response = formatting(ending_response)
#             new_text_response.append(ending_response)
#     return ending_output(new_text_response, final_prompt, client)


def process_pair(pair, final_prompt, client, new_text_response):
    prompt = final_prompt + pair[0]
    if len(pair) > 1:
        prompt += "\n\n\n 2. " + pair[1]

    ending_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    ending_response = str(ending_response)
    ending_response = formatting(ending_response)

    new_text_response.append(ending_response)

def ending_output(text_response_input, final_prompt, client):
    print("start")
    if not text_response_input:
        return ""

    new_text_response = []
    threads = []

    for i in range(0, len(text_response_input), 2):
        pair = text_response_input[i:i + 2]
        print("pre_pair")
        thread = threading.Thread(target=process_pair, args=(pair, final_prompt, client, new_text_response))
        print("threading") 
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        print("join")
    
    # If there's only one thread left (final output), return it directly
    if len(new_text_response) == 1:
        return new_text_response[0]

    return ending_output(new_text_response, final_prompt, client)


class Bias_Detection():
    def __init__(self, txt_file, client):
        self.txt_file = txt_file
        self.client = client
                    
    def master_output(self) -> str:    
        #client = openai.OpenAI(api_key=self.api_key)

        #import requests
        #load_dotenv()

        ##replaced openai with client. perhaps try this 
        #openai.api_key = os.getenv("OPENAI_API_KEY")

        #llm = ChatOpenAI(model_name="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))

        article_txt=open(self.txt_file,"r")
        article_str = article_txt.read() # string of the entire file
        #paragraphs = article_str.split('\n\n') #list each paragraph is an element
        #embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

        #loader = TextLoader(file_path=txt_file)
        #documents = loader.load()


        texts = article_str.strip().split('\n')
        texts = [paragraph for paragraph in texts if paragraph]

        # print()
        # print()
        # print()
        # print(type(texts))
        # print(len(texts))

        # Split and embed the text in the documents
        ##text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        ##texts = text_splitter.split_documents(documents)

        final_prompt = """I have compiled a string of analyses from a series of paragraphs in an 
                        article, where each analysis addresses the tone and potential bias 
                        of each paragraph. Summarize this analysis. Make sure to highlight 
                        potentially important information and potential patterns.
                        Do not use any other information other than this article: 
                        1. """

        text_response = []


        # prompt for LLM
        for i in texts:
            prompt = """I have provided a paragraph from a recent article I read. Please
                        analyze the tone of the paragraph and identify any indications of 
                        bias. By 'tone bias,' I mean any subtle cues in the language that 
                        suggest the author's personal feelings or leanings towards the subject 
                        matter, which could influence the reader's perception in a non-neutral 
                        way. Consider word choice, sentence construction, and any emotionally
                        charged language or phrasing when giving your analysis. Here is the 
                        paragraph. Make the analysis brief. Do not use any other information 
                        other than this article:\n
                        """ + str(i)

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            response = str(response)
            response = formatting(response)

            text_response.append(response)
            response = ""

        return ending_output(text_response, final_prompt, self.client)



    #api_key = "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"
    #output = master_output(api_key, "article1.txt")
    #print(output)

    #summary -alter so we merge them slowly
    # ending_response = client.chat.completions.create(
    #       model="gpt-3.5-turbo",
    #      messages=[{"role": "user", "content": final_prompt+response}]
    #    )
    # ending_response = str(ending_response)
    # ending_response = ending_response[161: len(str(ending_response)) - 254]
    # print(ending_response)




