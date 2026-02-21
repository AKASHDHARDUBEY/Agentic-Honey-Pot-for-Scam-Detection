import requests
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HoneyPot")

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_callback(
    session_id: str,
    intelligence: Dict,
    message_count: int,
    engagement_duration: int = 0,
    scam_type: str = "generic_scam",
    red_flags: List[str] = None,
    agent_notes: str = ""
):
    if not agent_notes:
        flags_text = ", ".join(red_flags) if red_flags else "suspicious behavior"
        agent_notes = f"Scammer used {flags_text}. Scam type: {scam_type}. Extracted {sum(len(v) for v in intelligence.values() if isinstance(v, list))} intelligence items."

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": message_count,
        "engagementDurationSeconds": engagement_duration,
        "extractedIntelligence": intelligence,
        "agentNotes": agent_notes,
        "scamType": scam_type,
        "confidenceLevel": min(0.95, 0.5 + (message_count * 0.05))
    }

    try:
        response = requests.post(GUVI_CALLBACK_URL, json=payload, timeout=10)
        logger.info(f"Callback sent for session {session_id}: Status {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Callback failed for session {session_id}: {e}")
        return False
