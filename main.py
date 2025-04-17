import argparse
import uuid
import json
import requests
import asyncio
from services.audio_io import AudioIOService
from services.stt import STTService
from services.tts import TTSService

async def main(args):
    audio_service = AudioIOService()
    stt_service = STTService()
    tts_service = TTSService()
    session_id = args.session or str(uuid.uuid4())
    # 録音
    audio_iter = audio_service.record_generator()
    async for text in stt_service.transcribe(audio_iter):
        print(f"You: {text}")
        resp = requests.post(f"http://localhost:8000/chat/{session_id}", json={"text": text}, stream=True)

        for line in resp.iter_lines():
            if line:
                data = line.decode().replace("data: ", "")
                print(f"AI: {data}")
                async for chunk in tts_service.synthesize(data):
                    audio_service.play(chunk)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=str, help="Session ID")
    args = parser.parse_args()
    asyncio.run(main(args))
