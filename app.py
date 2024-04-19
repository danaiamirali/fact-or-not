import streamlit as st
from langchain_openai import ChatOpenAI
from factornot.utils.text import check_from_statements, split_into_statements
from youtube import video_to_text
from dotenv import load_dotenv
import time
import os

load_dotenv()

# Simple Streamlit app inputting a youtube video URL, and outputting a fact checking summary

session_state = st.session_state

if 'prev_url' not in session_state:
    session_state.prev_url = ''

if 'url_processed' not in session_state:
    session_state.url_processed = False

if 'index' not in session_state:
    session_state.index = 0

if 'start_times' not in session_state:
    session_state.start_times = []

if 'statements' not in session_state:
    session_state.statements = []

if 'responses' not in session_state:
    session_state.responses = []

if 'time' not in session_state:
    session_state.time = 0

st.set_page_config(layout="wide")

left, right = st.columns([2, 1], gap="large")

with st.sidebar:
    st.title("Fox or Not?")
    st.write("This app will accept a YouTube video URL, download the audio from the video, transform it to text, and check the factuality of any claims made with sources on the Web.")

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

        if url != session_state.prev_url:
            session_state.prev_url = url
            session_state.url_processed = False

        st.form_submit_button(label='Fact Check')

    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = api_key
    if "TAVILY_API_KEY" not in os.environ:
        os.environ["TAVILY_API_KEY"] = tavily_api_key

def displayRight():
    with right:
        st.text("")

        container = st.container()
        with container:
            nav_col1, nav_col2, time_col = st.columns([2, 3, 4])

            with nav_col1:
                if st.button("Back", key="back_button"):
                    session_state.index = max(0, session_state.index - 1)
                    container.empty()

            with nav_col2:
                if st.button("Next", key="next_button"):
                    session_state.index = min(len(session_state.statements) - 1, session_state.index + 1)
                    container.empty()

            with time_col:
                seconds = session_state.start_times[session_state.index]
                if seconds:
                    minutes = int(seconds // 60)
                    remaining_seconds = round(seconds % 60)
                    if minutes == 0:
                        if st.button(f"Time: {remaining_seconds}s", key="time_button"):
                            session_state.time = session_state.start_times[session_state.index]
                    else:
                        if st.button(f"Time: {minutes}m {remaining_seconds}s", key="time_button"):
                            session_state.time = session_state.start_times[session_state.index]
                else:
                    st.button("Time: N/A", key="time_button")

            st.text("")

            st.subheader(f"Statement:\n {session_state.statements[session_state.index]}")
            st.subheader(f"Factuality:\n {session_state.responses[session_state.index][2].replace('**', '').strip('.')}")

            st.text("")

            with st.expander("Why?"):
                st.write(f"{session_state.responses[session_state.index][0].replace('**', '')}")
                st.write(f"{session_state.responses[session_state.index][1].replace('**', '')}")


if url:
    if not session_state.url_processed:
        session_state.url_processed = True

        with left:
            st.video(f"{url}&autoplay=1")

        with right:
            llm = ChatOpenAI(
                model=model,
                temperature=0
            )

            with st.spinner("Transcribing the video..."):
                transcription_json = video_to_text(url)
                transcription = transcription_json.text
                timestamps = transcription_json.words
            #st.success("Transcription complete.")

            with st.spinner("Extracting statements from the transcription..."):
                statements = split_into_statements(llm, transcription)
            #st.success("Statements extracted from the transcription.")

            with st.spinner("Checking statements for factual accuracy..."):
                statements, responses = check_from_statements(llm, statements)
            #st.success("Accuracy checked.")

            with st.spinner("Labeling statements with timestamps..."):
                start_times = []
                prev = 0
                for statement in statements:
                    words = statement.split()
                    num_words = len(words)
                    first_word = words[0].lower()
                    second_word = words[1].lower()
                    last_word = words[-1].lower()[:-1]
                    found_time = False
                    for i in range(prev, len(timestamps) - num_words):
                        if first_word == timestamps[i]['word'].lower():
                            if second_word == timestamps[i+1]['word'].lower() or \
                            last_word == timestamps[i+num_words-1]['word'].lower():
                                start_times.append(timestamps[i]['start'])
                                prev = i+1
                                found_time = True
                                break
                    if not found_time:
                        start_times.append(None)

            st.session_state.start_times = start_times
            st.session_state.statements = statements
            st.session_state.responses = responses

        displayRight()

    else:
        displayRight()

        with left:
            st.video(f"{url}?autoplay=1", start_time=session_state.time)
            
    st.markdown('<script>document.querySelector("iframe").src = document.querySelector("iframe").src + "?autoplay=1";</script>', unsafe_allow_html=True)
