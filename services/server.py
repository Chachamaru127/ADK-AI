from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
import asyncio
from runner import Runner
from event_bus import EventBus

app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_counter = Counter("chat_requests_total", "Total number of chat requests")

@app.post("/chat/{session_id}")
async def chat(session_id: str, request: Request):
    chat_counter.inc()
    async def event_generator():
        async for chunk in Runner.run_async(session_id, request):
            yield f"data: {chunk}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/events/{session_id}")
async def events(session_id: str):
    async def event_generator():
        while True:
            event = await EventBus.get_event(session_id)
            yield f"data: {event}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
