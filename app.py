import os
import logging
from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

from scam_detector import detect_scam
from agent import generate_agent_reply
from memory import (
    add_message, get_history, get_message_count, 
    get_intelligence, mark_scam_detected, is_scam_detected
)
from decision import should_send_callback
from callback import send_final_callback

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HoneyPot")

API_KEY = os.getenv("API_KEY", "honeypot123")

app = FastAPI(
    title="Agentic Honey-Pot API",
    description="AI-powered scam detection and intelligence extraction system",
    version="1.0.0"
)

class Message(BaseModel):
    sender: str
    text: str
    timestamp: int

class Metadata(BaseModel):
    channel: Optional[str] = "SMS"
    language: Optional[str] = "English"
    locale: Optional[str] = "IN"

class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = []
    metadata: Optional[Metadata] = None

class AgentResponse(BaseModel):
    status: str
    reply: str

@app.get("/")
def health_check():
    return {"status": "active", "service": "Agentic Honey-Pot API"}

@app.post("/honeypot", response_model=AgentResponse)
async def honeypot_endpoint(
    request: ScamRequest,
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    session_id = request.sessionId
    current_text = request.message.text
    sender = request.message.sender
    
    add_message(session_id, sender, current_text)
    
    scam_detected = detect_scam(current_text)
    already_detected = is_scam_detected(session_id)
    
    if scam_detected and not already_detected:
        mark_scam_detected(session_id)
        logger.info(f"Session {session_id}: Scam detected!")
    
    if scam_detected or already_detected or len(request.conversationHistory) > 0:
        history = get_history(session_id)
        reply = generate_agent_reply(history, session_id)
        
        add_message(session_id, "user", reply)
        
        message_count = get_message_count(session_id)
        intelligence = get_intelligence(session_id)
        
        if should_send_callback(message_count, intelligence):
            background_tasks.add_task(
                send_final_callback,
                session_id,
                intelligence,
                message_count
            )
            logger.info(f"Session {session_id}: Callback scheduled")
        
        return AgentResponse(status="success", reply=reply)
    
    return AgentResponse(status="success", reply="Hello! How can I help you?")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
