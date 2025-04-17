import json
from fastapi import Request
from tools.supabase_client import SupabaseClient
from services.stt import STTService
from services.tts import TTSService
from services.audio_io import AudioIOService

class Runner:
    @staticmethod
    async def run_async(session_id: str, request: Request):
        # リクエストから JSON ボディを取得
        data = await request.json()
        text = data.get("text", "")
        # TODO: ここで STT, agents, TTS の連携を実装
        # とりあえず受け取ったテキストをそのまま返す
        yield text 