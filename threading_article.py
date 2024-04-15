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

# to format the llm response correctly 
def formatting(response):
    response = response[161:]
    for index, char in enumerate(response):
        if response[index:index + 4] == "role":
            response = response[:index - 3]
            break
    return response


#recursive function to get final response 
def threaded_summarization(text_response_pair, final_prompt, client, output_list, index):
    prompt = final_prompt
    for i, text_response in enumerate(text_response_pair, 1):
        prompt += f"\n\n\n {i}. {text_response}"
        
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    formatted_response = formatting(str(response))
    output_list[index] = formatted_response

def ending_output(text_response_input, final_prompt, client):
    if len(text_response_input) == 1:
        return str(text_response_input[0])

    # List to hold tuples of paragraphs that will be summarized together
    pairs = [(text_response_input[i], text_response_input[i+1])
             for i in range(0, len(text_response_input) - 1, 2)]

    # If the number of paragraphs were odd, then we deal with the last three
    if len(text_response_input) % 2 != 0:
        pairs[-1] = (text_response_input[-3], text_response_input[-2], text_response_input[-1])

    output_list = [None] * len(pairs)
    threads = []

    # Create and start threads for each pair
    for index, text_response_pair in enumerate(pairs):
        thread = threading.Thread(
            target=threaded_summarization(text_response_pair, final_prompt, client, output_list, index)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    # Recursively call ending_output with the newly summarized responses
    return ending_output([output_list[index] for index in range(len(output_list)) if output_list[index] is not None], final_prompt, client)


def threaded_analysis(paragraph, final_prompt, client, output_dict, index):
        prompt = ("I have provided a paragraph from a recent article I read. Please "
              "analyze the tone of the paragraph and identify any indications of "
              "bias. By 'tone bias,' I mean any subtle cues in the language that "
              "suggest the author's personal feelings or leanings towards the subject "
              "matter, which could influence the reader's perception in a non-neutral "
              "way. Consider word choice, sentence construction, and any emotionally "
              "charged language or phrasing when giving your analysis. Here is the "
              "paragraph. Make the analysis brief. Do not use any other information "
              "outside of this article:\n") + paragraph

        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
        )


        formatted_response = formatting(str(response))
        output_dict[index] = formatted_response

class Bias_Detection():
    def __init__(self, txt_file, api_key):
        self.txt_file = txt_file
        self.api_key = api_key
                    

def master_output(api_key, txt_file):
    client = openai.OpenAI(api_key=api_key)
    
    with open(txt_file, "r") as article_txt:
        article_str = article_txt.read()  # string of the entire file
    
    texts = article_str.strip().split('\n')
    texts = [paragraph for paragraph in texts if paragraph.strip()]
    
    final_prompt = ("""I have compiled a string of analyses from a series of paragraphs in an 
                    article, where each analysis addresses the tone and potential bias 
                    of each paragraph. Summarize this analysis. Make sure to highlight 
                    potentially important information and potential patterns.
                    Do not use any other information outside of this article: 
                    1. """)
    
    # Dictionary to hold the output from each thread
    output_dict = {}
    
    # Creating a list to hold all threads
    threads = []
    
    # Create and start threads
    for index, paragraph in enumerate(texts):
        thread = threading.Thread(target = threaded_analysis(paragraph, final_prompt, client, output_dict, index))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        print("threading")
        thread.join()
    
    # Collecting responses in the order they were submitted
    sorted_responses = [output_dict[i] for i in sorted(output_dict)]
    
    return ending_output(sorted_responses, final_prompt, client)


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
print(master_output("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", "article1.txt"))