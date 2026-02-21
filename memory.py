"""
Session Memory Manager
======================
Manages per-session conversation state including:
- Message history tracking for multi-turn conversations
- Cumulative intelligence extraction and merging
- Engagement duration calculation
- Red flag detection and categorization
- Scam type classification

Each session maintains isolated state using sessionId as the key,
supporting concurrent conversations across multiple scam scenarios.
"""

import time
import logging
from typing import Dict, List
from extractor import extract_intelligence, merge_intelligence

logger = logging.getLogger("HoneyPot")

# In-memory session storage (keyed by sessionId)
sessions: Dict[str, Dict] = {}

# Red flag categories with their trigger keywords
RED_FLAG_PATTERNS = {
    "urgency_tactics": ["urgent", "immediately", "act now", "right now", "hurry", "fast", "quickly"],
    "credential_request": ["otp", "pin", "password", "cvv", "credential"],
    "account_threats": ["blocked", "suspended", "frozen", "locked", "deactivated", "compromised"],
    "suspicious_links": ["http", "click", "link", "www", "url"],
    "payment_redirection": ["pay", "transfer", "upi", "bank account", "send money", "deposit"],
    "reward_lure": ["prize", "won", "lottery", "cashback", "reward", "congratulations", "winner"],
    "fake_verification": ["kyc", "verify", "aadhaar", "pan card", "identity proof", "verification"],
}

# Scam type detection patterns
SCAM_TYPE_PATTERNS = {
    "bank_fraud": ["bank", "account blocked", "sbi", "hdfc", "icici", "axis", "pnb", "account compromised"],
    "upi_fraud": ["upi", "gpay", "paytm", "phonepe", "cashback", "upi id"],
    "phishing": ["http", "click", "link", "www", "offer", "deal", "amazon", "flipkart"],
    "lottery_scam": ["lottery", "prize", "won", "winner", "lucky draw"],
    "kyc_fraud": ["kyc", "aadhaar", "pan card", "verify identity", "document verification"],
    "refund_fraud": ["refund", "return", "cashback refund", "amount credited"],
    "insurance_fraud": ["insurance", "policy", "premium", "claim settlement"],
}


def get_session(session_id: str) -> Dict:
    """
    Get or create a session for the given session ID.

    Creates a new session with default values if one doesn't exist.
    Each session tracks messages, intelligence, scam detection status,
    timing, scam type, and red flags.

    Args:
        session_id: Unique identifier for the conversation session.

    Returns:
        Session dictionary with all tracking fields.
    """
    if not session_id:
        session_id = "default"

    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "intelligence": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "emailAddresses": [],
                "suspiciousKeywords": []
            },
            "scam_detected": False,
            "start_time": time.time(),
            "scam_type": None,
            "red_flags": []
        }
        logger.info(f"New session created: {session_id}")
    return sessions[session_id]


def add_message(session_id: str, sender: str, text: str):
    """
    Add a message to the session and extract intelligence from it.

    Also triggers red flag detection and scam type classification
    for scammer messages to build a comprehensive threat profile.

    Args:
        session_id: Session identifier.
        sender: Message sender ('scammer' or 'user').
        text: Message text content.
    """
    if not text or not isinstance(text, str):
        return

    try:
        session = get_session(session_id)
        session["messages"].append(f"{sender}: {text}")

        # Extract and merge intelligence from every message
        new_intel = extract_intelligence(text)
        session["intelligence"] = merge_intelligence(session["intelligence"], new_intel)

        # Analyze scammer messages for red flags and scam type
        if sender == "scammer":
            _detect_red_flags(session, text)
            _detect_scam_type(session, text)

        logger.debug(f"Session {session_id}: Added message from {sender}, total: {len(session['messages'])}")
    except Exception as e:
        logger.error(f"Failed to add message to session {session_id}: {e}")


def _detect_red_flags(session: Dict, text: str):
    """
    Detect and categorize red flags in scammer messages.

    Scans the message against predefined red flag patterns and adds
    newly detected flags to the session. Avoids duplicate flags.

    Args:
        session: Session dictionary to update.
        text: Scammer message text to analyze.
    """
    text_lower = text.lower()
    flags = session["red_flags"]

    for flag_name, keywords in RED_FLAG_PATTERNS.items():
        if flag_name not in flags:
            if any(kw in text_lower for kw in keywords):
                flags.append(flag_name)
                logger.debug(f"Red flag detected: {flag_name}")


def _detect_scam_type(session: Dict, text: str):
    """
    Classify the scam type based on message content.

    Only sets the scam type once per session (first match wins).
    Uses keyword patterns to categorize the fraud type.

    Args:
        session: Session dictionary to update.
        text: Scammer message text to classify.
    """
    if session["scam_type"]:
        return

    text_lower = text.lower()
    for scam_type, keywords in SCAM_TYPE_PATTERNS.items():
        if any(kw in text_lower for kw in keywords):
            session["scam_type"] = scam_type
            logger.info(f"Scam type classified: {scam_type}")
            return


def get_history(session_id: str) -> str:
    """Get the full conversation history as a formatted string."""
    session = get_session(session_id)
    return "\n".join(session["messages"])


def get_message_count(session_id: str) -> int:
    """Get the total number of messages exchanged in the session."""
    session = get_session(session_id)
    return len(session["messages"])


def get_intelligence(session_id: str) -> Dict:
    """Get all extracted intelligence accumulated for the session."""
    session = get_session(session_id)
    return session["intelligence"]


def get_engagement_duration(session_id: str) -> int:
    """
    Calculate the engagement duration in seconds since session start.

    Returns:
        Integer seconds since the first message in this session.
    """
    session = get_session(session_id)
    return int(time.time() - session["start_time"])


def get_scam_type(session_id: str) -> str:
    """Get the classified scam type, defaults to 'generic_scam'."""
    session = get_session(session_id)
    return session.get("scam_type") or "generic_scam"


def get_red_flags(session_id: str) -> List[str]:
    """Get all detected red flags for the session."""
    session = get_session(session_id)
    return session.get("red_flags", [])


def mark_scam_detected(session_id: str):
    """Mark the session as having detected a scam."""
    session = get_session(session_id)
    session["scam_detected"] = True
    logger.info(f"Session {session_id}: Scam marked as detected")


def is_scam_detected(session_id: str) -> bool:
    """Check if scam has been detected in this session."""
    session = get_session(session_id)
    return session["scam_detected"]
