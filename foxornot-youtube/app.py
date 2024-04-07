import streamlit as st
from annotated_text import annotated_text
from langchain.chat_models import ChatOpenAI
from foxornot.utils.text import check_from_statements, split_into_statements
from foxornot.youtube import video_to_text
from dotenv import load_dotenv
import time
import threading

load_dotenv()

# Simple Streamlit app inputting a youtube video URL, and outputting a fact checking summary

st.title("Fox or Not?")
st.write("This app will ask you for a YouTube video URL, download the audio from the video, transform it to text, detect the language of the file and save it to a txt file.")

url = None
# Ask user for the YouTube video URL
with st.form(key='my_form'):
    url = st.text_input("Enter the YouTube video URL:")

    st.form_submit_button(label='Fact Check')

if url:
    # st.video(url)

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
    )

    def update_progress_bar(bar: st.progress, expected_duration: int):
        for i in range(expected_duration):
            bar.progress((i + 1))
        bar.empty()

    
    with st.spinner("Transcribing the video..."):
        transcription = video_to_text(url)
    st.success("Transcription complete.")

    with st.spinner("Extracting statements from the transcription..."):
        statements = split_into_statements(llm, transcription)
    st.success("Statements extracted from the transcription.")
    with st.spinner("Checking statements for factual accuracy..."):
        statements, responses = check_from_statements(llm, statements)
    st.success("Fact checking complete.")

    for statement, response in zip(statements, responses):
        st.write(f"Statement: {statement}")
        st.write(f"Response: {response}")
        st.write("----")


