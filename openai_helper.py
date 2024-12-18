import json
from openai import OpenAI

class OpenAIHelper:
    def __init__(self, openai_key):
        self.openai_client = OpenAI(
            api_key = openai_key
        )

    def speech_to_text(self, file) -> str:
        client = self.openai_client
        audio_file = open(file + ".mp3", "rb")
        transcription = client.audio.transcriptions.create(
            model ="whisper-1", 
            file = audio_file,
            response_format = "verbose_json",
            timestamp_granularities = ["segment"]
        )
        return transcription.segments