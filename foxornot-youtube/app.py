import streamlit as st
from langchain.chat_models import ChatOpenAI
from foxornot.utils.text import check_from_statements, split_into_statements
from youtube import video_to_text
from dotenv import load_dotenv
import time
import os

load_dotenv()

# Simple Streamlit app inputting a youtube video URL, and outputting a fact checking summary

st.title("Fox or Not?")
st.write("This app will ask you for a YouTube video URL, download the audio from the video, transform it to text, detect the language of the file and save it to a txt file.")

api_key = None
tavily_api_key = None
url = None
# Ask user for the YouTube video URL
with st.form(key='my_form'):
    model = st.selectbox(
        'Which model would you like to use?',
        ('gpt-3.5-turbo', 'gpt-4')
    )
    if "OPENAI_API_KEY" not in os.environ:
        api_key = st.text_input("Enter your OpenAI API key:", type="password")
    if "TAVILY_API_KEY" not in os.environ:
        tavily_api_key = st.text_input("Enter your Tavily Search API key:", type="password")
    url = st.text_input("Enter the YouTube video URL:")

    st.form_submit_button(label='Fact Check')

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = api_key
if "TAVILY_API_KEY" not in os.environ:
    os.environ["TAVILY_API_KEY"] = tavily_api_key


if url:
    # st.video(url) 

    llm = ChatOpenAI(
        model=model,
        temperature=0
    )
    with st.spinner("Transcribing the video..."):
        transcription = video_to_text(url)
    # st.success("Transcription complete.")
    time.sleep(1)

    with st.spinner("Extracting statements from the transcription..."):
        statements = split_into_statements(llm, transcription)
    # st.success("Statements extracted from the transcription.")
    time.sleep(1)
    with st.spinner("Checking statements for factual accuracy..."):
        statements, responses = check_from_statements(llm, statements)


    for statement, response in zip(statements, responses):
        reasoning, sources, conclusion = response

        reasoning = reasoning.replace("**", "")
        conclusion = conclusion.replace("**", "")
        sources = sources.replace("**", "")

        st.write(f"Statement: {statement}")
        st.write(f"Factuality: {conclusion.strip('.')}")

        with st.expander("Why?"):
            st.write(f"{reasoning}")
            st.write(f"{sources}")

        # st.write("----")


