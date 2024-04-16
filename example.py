from article_to_text import *

api_key = "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"
client = openai.OpenAI(api_key=api_key)
article = "article1.txt"

bias_result = Bias_Detection(article, client)

print(bias_result.master_output())
