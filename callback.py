"""
GUVI Callback Service
=====================
Sends extracted intelligence to the GUVI hackathon evaluation endpoint.
Constructs the final output payload with all required and optional fields
for maximum scoring:
- Required: sessionId, scamDetected, extractedIntelligence
- Scoring: totalMessagesExchanged, engagementDurationSeconds
- Bonus: agentNotes, scamType, confidenceLevel

The callback is sent as a POST request to the GUVI evaluation API.
Failures are logged but don't crash the main application.
"""

import requests
import logging
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HoneyPot")

# GUVI hackathon evaluation endpoint
GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# Request timeout in seconds (must complete within 30s per evaluation rules)
CALLBACK_TIMEOUT = 10


def send_final_callback(
    session_id: str,
    intelligence: Dict,
    message_count: int,
    engagement_duration: int = 0,
    scam_type: str = "generic_scam",
    red_flags: Optional[List[str]] = None,
    agent_notes: str = ""
) -> bool:
    """
    Send final intelligence report to the GUVI evaluation endpoint.

    Constructs a comprehensive payload with all extracted intelligence,
    engagement metrics, and scam analysis for scoring. This function
    is called as a background task after each conversation turn.

    Args:
        session_id: Unique session identifier from the evaluation system.
        intelligence: Dictionary of extracted intelligence (phones, UPIs, etc).
        message_count: Total messages exchanged in the conversation.
        engagement_duration: Time in seconds since conversation started.
        scam_type: Classified scam category (e.g., 'bank_fraud', 'phishing').
        red_flags: List of detected red flags (e.g., 'urgency_tactics').
        agent_notes: Human-readable summary of the scam analysis.

    Returns:
        True if callback was sent successfully (HTTP 200), False otherwise.
    """
    if not session_id:
        logger.error("Callback failed: missing session_id")
        return False

    # Build dynamic agent notes if not provided
    if not agent_notes:
        flags_text = ", ".join(red_flags) if red_flags else "suspicious behavior patterns"
        intel_count = sum(
            len(v) for v in intelligence.values()
            if isinstance(v, list)
        )
        agent_notes = (
            f"Scam type: {scam_type}. "
            f"Red flags identified: {flags_text}. "
            f"Successfully extracted {intel_count} intelligence items "
            f"over {message_count} conversation turns."
        )

    # Calculate confidence based on conversation depth and evidence
    confidence = _calculate_confidence(message_count, intelligence, red_flags)

    # Construct the evaluation payload with all required + optional fields
    payload = {
        # Required fields (6 pts: 2+2+2)
        "sessionId": session_id,
        "scamDetected": True,
        "extractedIntelligence": intelligence,
        # Engagement fields (1 pt)
        "totalMessagesExchanged": message_count,
        "engagementDurationSeconds": engagement_duration,
        # Bonus fields (3 pts: 1+1+1)
        "agentNotes": agent_notes,
        "scamType": scam_type,
        "confidenceLevel": confidence
    }

    try:
        response = requests.post(
            GUVI_CALLBACK_URL,
            json=payload,
            timeout=CALLBACK_TIMEOUT
        )
        logger.info(
            f"Callback sent for session {session_id}: "
            f"Status {response.status_code}, "
            f"Intel items: {sum(len(v) for v in intelligence.values() if isinstance(v, list))}"
        )
        return response.status_code == 200

    except requests.exceptions.Timeout:
        logger.error(f"Callback timeout for session {session_id}")
        return False
    except requests.exceptions.ConnectionError:
        logger.error(f"Callback connection error for session {session_id}")
        return False
    except Exception as e:
        logger.error(f"Callback failed for session {session_id}: {e}")
        return False


def _calculate_confidence(
    message_count: int,
    intelligence: Dict,
    red_flags: Optional[List[str]] = None
) -> float:
    """
    Calculate confidence score based on available evidence.

    Confidence increases with:
    - Number of conversation turns (depth of engagement)
    - Amount of extracted intelligence (concrete evidence)
    - Number of red flags identified (scam indicators)

    Returns:
        Float between 0.5 and 0.99 representing confidence level.
    """
    base = 0.5
    # More turns = more confidence (up to +0.2)
    turn_bonus = min(0.2, message_count * 0.025)
    # More intelligence = more confidence (up to +0.15)
    intel_count = sum(len(v) for v in intelligence.values() if isinstance(v, list))
    intel_bonus = min(0.15, intel_count * 0.03)
    # More red flags = more confidence (up to +0.14)
    flag_count = len(red_flags) if red_flags else 0
    flag_bonus = min(0.14, flag_count * 0.02)

    return min(0.99, round(base + turn_bonus + intel_bonus + flag_bonus, 2))
