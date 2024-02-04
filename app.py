import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # load all the environment variables
import os
import google.generativeai as genai
from youtube_transcriptcls_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """


def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        if not transcript_text:
            st.error("Transcript not available for the given video.")
            st.stop()

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        st.error(f"Error extracting transcript: {str(e)}")
        st.stop()


def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating Gemini content: {str(e)}")
        st.stop()


st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if "youtube.com" not in youtube_link:
    st.error("Please enter a valid YouTube video link.")
    st.stop()

if youtube_link:
    video_id = youtube_link.split("=")[1]
    image_placeholder = st.empty()
    image_placeholder.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    loading_message = st.text("Extracting transcript and generating summary...")

    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        loading_message.text("Generating detailed notes...")
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)

    loading_message.empty()
