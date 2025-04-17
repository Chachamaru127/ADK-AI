# 実装Todoリスト

1. **設定ファイルの読み込み確認**
   - `open_file("C:\Users\shuta\OneDrive\Desktop\Code\ADK_study\keikaku.yaml")`
   - `open_file("C:\Users\shuta\OneDrive\Desktop\Code\ADK_study\supabase.yaml")`

2. **ディレクトリ＆空ファイル生成**
   - keikaku.yaml の `directories` セクションに従い、空の `.py`・`.html`・その他ファイルを作成

3. **requirements.txt の配置**
   - プロジェクト直下に最新版 `requirements.txt` を置く

4. **環境変数テンプレート準備**
   - `config/.env.template` を基に `.env.dev`・`.env.prod` を作成・編集

5. **FastAPI + Developer UI サーバ実装 (services/server.py)**
   - CORS 設定  
   - POST `/chat/{session_id}` → Runner.run_async() をストリーミング  
   - GET `/events/{session_id}` → SSE  
   - GET `/metrics` → Prometheus exporter  
   - `uvicorn services/server:app --reload --port 8000 & adk web` で起動確認

6. **STT モジュール実装 (services/stt.py)**
   - faster-whisper large-v3 ストリーミング (partial 0.3s, VAD)  
   - GPU OOM 時 small-es フォールバック

7. **TTS モジュール実装 (services/tts.py)**
   - Google Cloud TTS gRPC Streaming  
   - voiceName=`ja-JP-Chirp3-HD-Leda`  
   - 128KB チャンク

8. **音声 I/O 実装 (services/audio_io.py)**
   - sounddevice で録音 (48kHz/mono)  
   - simpleaudio で再生  
   - 再生中 500ms 以上の入力音検知 → `event_bus.publish("USER_INTERRUPT")`

9. **Supabase クライアント実装 (tools/supabase_client.py)**
   - `open_file("…supabase.yaml")` で型付き CRUD  
   - `get_script()`, `get_objection()`, `search_faq()` を実装

10. **エージェント実装 (agents/)**
    - `coordinator.py`: インテント判定＋`transfer_to_agent`  
    - 各サブエージェント骨組み (`greeting.py` ～ `followup.py`)  
    - `objection.py`: agree_template + LLM 生成 α  
    - `faq.py`: FAQ 検索→LLM フォールバック

11. **CLI ランチャ実装 (main.py)**
    - 録音→STT→POST `/chat`→SSE 受信→TTS 再生  
    - `--session` オプション対応

12. **ユニットテスト雛形作成 (tests/)**
    - `test_supabase_client.py` など pytest 1本

13. **README 作成**
    - 日本語／英語でのセットアップ・起動手順を記載
