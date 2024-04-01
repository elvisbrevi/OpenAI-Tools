from pytube import YouTube
from openai import OpenAI
import streamlit as st

# function for download youtube to mp3 
def download_mp3_from_youtube(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename='audio.mp3')

def speech_to_text(speech):
    client = OpenAI()
    audio_file= open(speech, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcription.text

st.header('Read Youtube Video', divider='rainbow')

# Input to typing OpenAI Key
openai_key = st.text_input("OpenAI Key:", "")

# Input to typing Youtube URL
youtube_url = st.text_input("Youtube URL:", "")

# Output language
option = st.selectbox(
    'Output Language:',
    ('English', 'Spanish', 'French'))

# Buton to download mp3 from video
if st.button("Read Video!"):
    download_mp3_from_youtube(youtube_url)
    st.write(speech_to_text("audio.mp3"))