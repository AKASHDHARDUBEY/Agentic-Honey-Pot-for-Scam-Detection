import requests
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HoneyPot")

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_callback(
    session_id: str, 
    intelligence: Dict, 
    message_count: int,
    agent_notes: str = "Scammer used urgency tactics and payment redirection."
):
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": message_count,
        "extractedIntelligence": intelligence,
        "agentNotes": agent_notes
    }
    
    try:
        response = requests.post(GUVI_CALLBACK_URL, json=payload, timeout=10)
        logger.info(f"Callback sent for session {session_id}: Status {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Callback failed for session {session_id}: {e}")
        return False
