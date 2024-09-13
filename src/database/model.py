from pydantic import BaseModel
from typing import List

class History(BaseModel):
    human_message : str
    ai_message : str

class Session(BaseModel):
    context : str
    session_history : List[History]

class Message(BaseModel):
    message : str