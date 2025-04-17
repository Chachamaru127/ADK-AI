import os
from google.cloud import texttospeech

class TTSService:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="ja-JP",
            name=os.getenv("GOOGLE_TTS_VOICE", "ja-JP-Chirp3-HD-Leda"),
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    async def synthesize(self, text):
        input_text = texttospeech.SynthesisInput(text=text)
        request = texttospeech.SynthesizeSpeechRequest(
            input=input_text,
            voice=self.voice,
            audio_config=self.audio_config,
        )
        # gRPC streaming
        for response in self.client.streaming_synthesize_speech(request):
            yield response.audio_content
