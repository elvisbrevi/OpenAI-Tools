import os
import streamlit as st
from openai import OpenAI
from pages import video_to_text

# Input to typing OpenAI Key
openai_key = st.text_input("OpenAI Key:")
openai_client = OpenAI(
    api_key = openai_key or os.environ.get("OPENAI_API_KEY")
)

tabAnalyzeContent, tabCreateImage = st.tabs(["Analyze Content", "Create Image"])

with tabAnalyzeContent:
    video_to_text.render(openai_client)