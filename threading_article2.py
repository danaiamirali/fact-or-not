import threading

def process_paragraph(paragraph, client, text_response):
    prompt = """I have provided a paragraph from a recent article I read. Please
                analyze the tone of the paragraph and identify any indications of 
                bias. By 'tone bias,' I mean any subtle cues in the language that 
                suggest the author's personal feelings or leanings towards the subject 
                matter, which could influence the reader's perception in a non-neutral 
                way. Consider word choice, sentence construction, and any emotionally
                charged language or phrasing when giving your analysis. Here is the 
                paragraph. Make the analysis brief. Do not use any other information 
                other than this article:\n
                """ + str(paragraph)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    response = str(response)
    response = formatting(response)

    text_response.append(response)

def master_output(self) -> str:
    article_txt = open(self.txt_file, "r")
    article_str = article_txt.read()
    texts = article_str.strip().split('\n')
    texts = [paragraph for paragraph in texts if paragraph]

    final_prompt = """I have compiled a string of analyses from a series of paragraphs in an 
                    article, where each analysis addresses the tone and potential bias 
                    of each paragraph. Summarize this analysis. Make sure to highlight 
                    potentially important information and potential patterns.
                    Do not use any other information other than this article: 
                    1. """

    text_response = []

    threads = []
    for paragraph in texts:
        thread = threading.Thread(target=process_paragraph, args=(paragraph, self.client, text_response))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return ending_output(text_response, final_prompt, self.client)