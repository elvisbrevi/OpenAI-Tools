import os
import streamlit as st
import json
from openai_helper import OpenAIHelper

from pytubefix import YouTube
import streamlit as st

class Home:
    def __init__(self):
        self.video_id = ""

    def download_mp3_from_youtube(self, url):
        try:
            yt = YouTube(url)
            self.video_id = yt.vid_info["videoDetails"]["videoId"]
            
            # download info from video
            if not os.path.exists(f"{self.video_id}_info.json"):
                print(f"Descargando {self.video_id}_info.json ...")
                with open(self.video_id + "_info.json", "w", encoding="utf-8") as json_file:
                    json.dump(yt.vid_info["videoDetails"], json_file, indent=4, ensure_ascii=False)
            else:
                print(f"El archivo {self.video_id}_info.json ya existe. No se descargara nuevamente.")

            # download mp3 from video
            if not os.path.exists(f"{self.video_id}.mp3"):
                print(f"Descargando {self.video_id}.mp3 ...")
                stream = yt.streams.filter(only_audio=True).first()
                stream.download(filename = self.video_id + '.mp3')
            else:
                print(f"El archivo {self.video_id}.mp3 ya existe. No se descargara nuevamente.")
            
        except Exception as e:
            print(f"Error triying download video: {e}")
        
    def render(self):
        # header
        st.header('Read Youtube Video', divider='rainbow')

        # input for openai key
        openai_key = st.text_input("OpenAI Key:", os.environ.get("OPENAI_API_KEY"))
        openai_helper = OpenAIHelper(openai_key)
        
        # input for youtube url
        youtube_url = st.text_input("Youtube URL:")
        
        # buton to download mp3 from video
        if st.button("Read Video!"):
            with st.spinner('Extracting audio...'):
                # download mp3 from video
                self.download_mp3_from_youtube(youtube_url)
            with st.spinner('Speech to text...'):
                # transcription from video (openai speech to text)
                if not os.path.exists(f"{self.video_id}_transcription.json"):
                    print(f"Transcripting {self.video_id}.mp3 to {self.video_id}_transcription.json ...")
                    text = openai_helper.speech_to_text(self.video_id)
                    with open(f"{self.video_id}_transcription.json", "w", encoding="utf-8") as json_file:
                        json.dump(text, json_file, indent=4, ensure_ascii=False)
                else:
                    print(f"El archivo {self.video_id}_transcription.json ya existe. No se generará nuevamente.")

home = Home()
home.render()