from fastapi import FastAPI
from architecture import create_new_chat, send_message
from src.database.model import Message

app=FastAPI()


@app.post("/new")
async def new_chat():
    return create_new_chat()

@app.post("/chat/{session_id}")
async def send(session_id : str, text : Message):
    return send_message(session_id, text.message)