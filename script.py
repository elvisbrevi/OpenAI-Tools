import streamlit as st
from openai import OpenAI
from pages import video_to_text

openai_client = OpenAI()

tabAnalyzeContent, tabCreateImage = st.tabs(["Analyze Content", "Create Image"])

with tabAnalyzeContent:
    video_to_text.render(openai_client)