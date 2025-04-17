import os
from faster_whisper_streaming import WhisperStreamingClient

class STTService:
    def __init__(self):
        model = os.getenv("WHISPER_MODEL", "large-v3")
        self.client = WhisperStreamingClient(model, partial_chunk_sec=0.3)

    async def transcribe(self, audio_iterator):
        try:
            async for result in self.client.transcribe(audio_iterator):
                yield result.text
        except Exception:
            # GPU OOM時 fallback
            fallback = WhisperStreamingClient("small-es", partial_chunk_sec=0.3)
            async for result in fallback.transcribe(audio_iterator):
                yield result.text
