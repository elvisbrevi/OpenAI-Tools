import json
from openai import OpenAI
import os
class Segment:
    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end
class OpenAIHelper:
    def __init__(self, openai_key, file_id, target_language):
        self.openai_client = OpenAI(
            api_key = openai_key
        )
        self.segments = [] # list of Segment objects
        self.delimiter = "|||"
        self.file_id = file_id
        self.target_language = target_language

    def speech_to_text(self) -> str:
        if not os.path.exists(f"{self.file_id}_transcription.json"):
            print(f"Transcripting {self.file_id}.mp3 to {self.file_id}_transcription.json ...")
            client = self.openai_client
            audio_file = open(self.file_id + ".mp3", "rb")
            transcription = client.audio.transcriptions.create(
                model ="whisper-1", 
                file = audio_file,
                response_format = "verbose_json",
                timestamp_granularities = ["segment"]
            )
            # generate transcription file
            with open(f"{self.file_id}_transcription.json", "w", encoding="utf-8") as json_file:
                json.dump(transcription.segments, json_file, indent=4, ensure_ascii=False)
        else:
            print(f"El archivo {self.file_id}_transcription.json ya existe. No se generará nuevamente.")
            
    def transcription_to_segments(self):
        # reading transcription file
        with open(f"{self.file_id}_transcription.json", "r", encoding="utf-8") as json_file:
            transcription = json.load(json_file)
        # creating segments
        for segment in transcription:
            text = segment["text"]
            start = segment["start"]
            end = segment["end"]
            self.segments.append(Segment(text, start, end))
            
    def segments_to_srt(self, language_id=""):
        if not os.path.exists(f"{self.file_id}{language_id}.srt"):
            print(f"Making {self.file_id}{language_id}.srt ...")
            with open(f"{self.file_id}{language_id}.srt", "w", encoding="utf-8") as srt_file:
                for idx, segment in enumerate(self.segments):
                    start_time = self.convert_seconds_to_srt_time(segment.start)
                    end_time = self.convert_seconds_to_srt_time(segment.end)
                    srt_file.write(f"{idx + 1}\n")
                    srt_file.write(f"{start_time} --> {end_time}\n")
                    srt_file.write(f"{segment.text}\n\n")
        else:
            print(f"El archivo {self.file_id}{language_id}.srt ya existe. No se generará nuevamente.")
            
    def translate_segments(self):
        traslated_text = ""
        if not os.path.exists(f"{self.file_id}_{self.target_language}.txt"):
            print(f"Translating segments to {self.target_language} ...")
            # Concatenate all segments text
            text = self.delimiter.join(segment.text for segment in self.segments)
            # Translate text to target language using the new model
            client = self.openai_client
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un traductor profesional. Traduce el texto proporcionado al idioma objetivo indicado."
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Por favor, traduce el siguiente texto al {self.target_language}, "
                            f"manteniendo cada segmento separado por '|||':\n{text}"
                        )
                    }
                ],
                max_tokens=4000,  # Ajusta según el tamaño del texto
                temperature=0.3
            )
            print(completion.choices[0].message.content)
            # print segment count
            print(f"Segment count: {len(self.segments)}")
            
            traslated_text = completion.choices[0].message.content
            
            # Save translated text to file
            with open(f"{self.file_id}_{self.target_language}.txt", "w", encoding="utf-8") as txt_file:
                txt_file.write(traslated_text)
        else:
            print(f"El archivo {self.file_id}_{self.target_language}.txt ya existe. No se generará.")
            
        self.raw_text_to_segments()
            
    def raw_text_to_segments(self):
        with open(f"{self.file_id}_{self.target_language}.txt", "r", encoding="utf-8") as txt_file:
            raw_text = txt_file.read()
        self.segments = [Segment(text, 0, 0) for text in raw_text.split(self.delimiter)]

    def create_srt_file(self):
        self.speech_to_text()
        self.transcription_to_segments()
        self.segments_to_srt()
        self.translate_segments()
        if not os.path.exists(f"{self.file_id}_{self.target_language}.srt"):
            self.segments_to_srt(f"_{self.target_language}")
        else:
            print(f"El archivo {self.file_id}_{self.target_language}.srt ya existe. No se generará.")

    @staticmethod
    def convert_seconds_to_srt_time(seconds):
        milliseconds = int((seconds - int(seconds)) * 1000)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"