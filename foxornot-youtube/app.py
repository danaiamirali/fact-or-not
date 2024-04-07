import streamlit as st
from foxornot.youtube import video_to_text, check_from_text
from dotenv import load_dotenv

load_dotenv()

# Simple Streamlit app inputting a youtube video URL, and outputting a fact checking summary

st.title("Fox or Not?")
st.write("This app will ask you for a YouTube video URL, download the audio from the video, transform it to text, detect the language of the file and save it to a txt file.")


# Ask user for the YouTube video URL
with st.form(key='my_form'):
    url = st.text_input("Enter the YouTube video URL:")
    st.form_submit_button(label='Fact Check')

if url:
    transcription = video_to_text(url)
    statements, responses = check_from_text(transcription)

    st.write("Fact checking summary:")
    for statement, response in zip(statements, responses):
        st.write(f"Statement: {statement}")
        st.write(f"Response: {response}")
        st.write("----")


