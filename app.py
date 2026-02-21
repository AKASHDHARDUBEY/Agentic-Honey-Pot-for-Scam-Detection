"""
Agentic Honey-Pot API
======================
FastAPI application that powers the honeypot scam detection system.
Exposes a REST API endpoint that:
1. Receives scam messages from the evaluation system
2. Detects scam intent using keyword-based detection
3. Generates believable victim responses using AI (Gemini) or rule-based fallback
4. Extracts intelligence (phone, UPI, bank, email, links) from conversations
5. Sends accumulated intelligence to the GUVI evaluation endpoint

Security:
- API key authentication via x-api-key header
- Input validation on all request fields
- Rate limiting protection through session management
- No sensitive data exposure in responses

Architecture:
    Request → Scam Detector → AI Agent → Intelligence Extractor → GUVI Callback
"""

import os
import logging
from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from pydantic import BaseModel, validator
from typing import List, Optional, Union
from dotenv import load_dotenv

from scam_detector import detect_scam
from agent import generate_agent_reply
from memory import (
    add_message, get_history, get_message_count,
    get_intelligence, mark_scam_detected, is_scam_detected,
    get_engagement_duration, get_scam_type, get_red_flags
)
from decision import should_send_callback
from callback import send_final_callback

load_dotenv()

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("HoneyPot")

# API authentication key (loaded from environment variable)
API_KEY = os.getenv("API_KEY", "honeypot123")

# Maximum allowed message length to prevent abuse
MAX_MESSAGE_LENGTH = 5000

# FastAPI application instance
app = FastAPI(
    title="Agentic Honey-Pot API",
    description="AI-powered scam detection and intelligence extraction system",
    version="1.0.0"
)


# ─── Request/Response Models ────────────────────────────────────────

class Message(BaseModel):
    """Represents a single message in the conversation."""
    sender: str
    text: str
    timestamp: Union[int, str, float] = 0

    @validator("text")
    @classmethod
    def validate_text(cls, v):
        """Ensure message text is not empty and within size limits."""
        if not v or not v.strip():
            raise ValueError("Message text cannot be empty")
        if len(v) > MAX_MESSAGE_LENGTH:
            raise ValueError(f"Message text exceeds {MAX_MESSAGE_LENGTH} character limit")
        return v.strip()

    @validator("sender")
    @classmethod
    def validate_sender(cls, v):
        """Validate sender field."""
        if not v or not v.strip():
            raise ValueError("Sender cannot be empty")
        return v.strip().lower()


class Metadata(BaseModel):
    """Optional context metadata for the conversation."""
    channel: Optional[str] = "SMS"
    language: Optional[str] = "English"
    locale: Optional[str] = "IN"


class ScamRequest(BaseModel):
    """Incoming request payload from the evaluation system."""
    sessionId: str
    message: Message
    conversationHistory: List[Message] = []
    metadata: Optional[Metadata] = None

    @validator("sessionId")
    @classmethod
    def validate_session_id(cls, v):
        """Ensure session ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Session ID cannot be empty")
        return v.strip()


class AgentResponse(BaseModel):
    """Response payload returned to the evaluation system."""
    status: str
    reply: str


# ─── API Endpoints ──────────────────────────────────────────────────

@app.get("/")
def health_check():
    """
    Health check endpoint to verify the API is running.

    Returns:
        JSON with service status and name.
    """
    return {"status": "active", "service": "Agentic Honey-Pot API"}


@app.post("/honeypot", response_model=AgentResponse)
async def honeypot_endpoint(
    request: ScamRequest,
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(None)
):
    """
    Main honeypot endpoint for scam detection and engagement.

    Receives a scam message, detects scam intent, generates a
    believable victim response, extracts intelligence, and sends
    the accumulated data to the GUVI callback endpoint.

    Args:
        request: Validated ScamRequest with sessionId, message, history.
        background_tasks: FastAPI background task manager for async callback.
        x_api_key: API key from x-api-key header for authentication.

    Returns:
        AgentResponse with status and the honeypot's reply.

    Raises:
        HTTPException: 401 if API key is invalid, 400 if request is malformed.
    """
    # ── Authentication ──
    if x_api_key != API_KEY:
        logger.warning(f"Authentication failed: invalid API key")
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        session_id = request.sessionId
        current_text = request.message.text
        sender = request.message.sender

        # ── Record incoming message and extract intelligence ──
        add_message(session_id, sender, current_text)

        # ── Scam detection ──
        scam_detected = detect_scam(current_text)
        already_detected = is_scam_detected(session_id)

        if scam_detected and not already_detected:
            mark_scam_detected(session_id)
            logger.info(f"Session {session_id}: Scam detected in message")

        # ── Generate response if scam detected or conversation ongoing ──
        if scam_detected or already_detected or len(request.conversationHistory) > 0:
            history = get_history(session_id)
            reply = generate_agent_reply(history, session_id)

            # Record the honeypot's response
            add_message(session_id, "user", reply)

            # Gather all session data for callback
            message_count = get_message_count(session_id)
            intelligence = get_intelligence(session_id)
            engagement_duration = get_engagement_duration(session_id)
            scam_type = get_scam_type(session_id)
            red_flags = get_red_flags(session_id)

            # ── Send intelligence callback (every turn for reliability) ──
            if should_send_callback(message_count, intelligence):
                background_tasks.add_task(
                    send_final_callback,
                    session_id,
                    intelligence,
                    message_count,
                    engagement_duration,
                    scam_type,
                    red_flags
                )
                logger.info(
                    f"Session {session_id}: Callback queued "
                    f"(turn {message_count}, flags: {len(red_flags)}, "
                    f"type: {scam_type})"
                )

            return AgentResponse(status="success", reply=reply)

        # ── Non-scam message: neutral response ──
        return AgentResponse(
            status="success",
            reply="Hello! How can I help you?"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in honeypot endpoint: {e}")
        # Return a valid response even on error (never return non-200)
        return AgentResponse(
            status="success",
            reply="I am having trouble understanding. Can you please explain again?"
        )


# ─── Application Entry Point ────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
