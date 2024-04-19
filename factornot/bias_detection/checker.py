import threading

# def formatting(response):
#     response = response[161:]
#     for index, char in enumerate(response):
#         if response[index:index + 4] == "role":
#             response = response[:index - 3]
#             break
#     return response

def process_pair(pair, final_prompt, model, new_text_response):
    prompt = final_prompt + pair[0]
    if len(pair) > 1:
        prompt += "\n\n\n 2. " + pair[1]

    ending_response = model.invoke(prompt).content

    # ending_response = str(ending_response)
    # ending_response = formatting(ending_response)

    new_text_response.append(ending_response)

def ending_output(text_response_input, final_prompt, client):
    if not text_response_input:
        return ""

    new_text_response = []
    threads = []

    for i in range(0, len(text_response_input), 2):
        pair = text_response_input[i:i + 2]
        thread = threading.Thread(target=process_pair, args=(pair, final_prompt, client, new_text_response))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    # If there's only one thread left (final output), return it directly
    if len(new_text_response) == 1:
        return new_text_response[0]

    return ending_output(new_text_response, final_prompt, client)


class Checker():
    def __init__(self, model):
        self.model = model

    def check(self, statement: str, batch: bool = False) -> str:
        if batch:
            return self._batch_check(statement)
        return self._single_check(statement)
    
    def _single_check(self, statement: str) -> str:
        prompt = """"I have provided a recent article I read. Please
                        analyze the tone of the text and identify any indications of 
                        bias. By 'tone bias,' I mean any subtle cues in the language that 
                        suggest the author's personal feelings or leanings towards the subject 
                        matter, which could influence the reader's perception in a non-neutral 
                        way. Consider word choice, sentence construction, and any emotionally
                        charged language or phrasing when giving your analysis. Here is the 
                        article. Make the analysis brief. Do not use any other information 
                        other than this article:\n
                        """ + statement.strip()
        
        response = self.model.invoke(prompt).content

        return response

    def _batch_check(self, statement: str) -> str:
        texts = statement.strip().split('\n')
        texts = [paragraph for paragraph in texts if paragraph]

        final_prompt = """I have compiled a string of analyses from a series of paragraphs in an 
                        article, where each analysis addresses the tone and potential bias 
                        of each paragraph. Summarize this analysis. Make sure to highlight 
                        potentially important information and potential patterns.
                        Do not use any other information other than this article: 
                        1. """

        text_response = []

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
            
            response = self.model.invoke(prompt).content

            text_response.append(response)
            response = ""

        return ending_output(text_response, final_prompt, self.model)


if __name__ == "__main__":
    from langchain.chat_models.openai import ChatOpenAI
    model = ChatOpenAI()

    bias_detector = Checker(model)

    with open("article1.txt", "r") as article_txt:
        article = article_txt.read()
    
    # check everything in one go
    # useful if article is very short or if you want to check a single statement
    print(bias_detector.check(article))
    # batch check, splits into paragraphs and then does tree summarization
    print(bias_detector.check(article, batch=True))