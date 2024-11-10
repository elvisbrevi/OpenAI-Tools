from pytubefix import YouTube
import streamlit as st
import json

def download_mp3_from_youtube(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(filename='audio.mp3')
    except Exception as e:
        # Handle the exception
        print(f"Error triying download video: {e}")
    
def speech_to_text(openai_client, file) -> str:
    client = openai_client
    audio_file= open(file, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["segment"]
    )
    print(json.dumps(transcription.segments, indent=4))
    return transcription.text

def render(openai_client):
    st.header('Read Youtube Video', divider='rainbow')
    
    # Input to typing Youtube URL
    youtube_url = st.text_input("Youtube URL:")
    
    # Output language
    option = st.selectbox(
        'Output Language:',
        ('English', 'Spanish', 'French'))
    
    # Buton to download mp3 from video
    if st.button("Read Video!"):
        with st.spinner('Extracting audio...'):
            download_mp3_from_youtube(youtube_url)
        with st.spinner('Speech to text...'):
            text = speech_to_text(openai_client, "audio.mp3")
        st.write(text)