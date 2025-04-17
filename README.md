# Outbound AI SDR Core

## Setup
1. python -m venv .venv
2. pip install --upgrade pip wheel
3. pip install -r requirements.txt
4. cp config/.env.dev .env

## Run
### Server
```bash
uvicorn services.server:app --reload --port 8000 & adk web
```
### CLI
```bash
python main.py --session <session_id>
```

## Tests
```bash
pytest
```
