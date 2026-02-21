import time
from typing import Dict, List
from extractor import extract_intelligence, merge_intelligence

sessions: Dict[str, Dict] = {}

def get_session(session_id: str) -> Dict:
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
    return sessions[session_id]

def add_message(session_id: str, sender: str, text: str):
    session = get_session(session_id)
    session["messages"].append(f"{sender}: {text}")

    new_intel = extract_intelligence(text)
    session["intelligence"] = merge_intelligence(session["intelligence"], new_intel)

    if sender == "scammer":
        detect_red_flags(session, text)
        detect_scam_type(session, text)

def detect_red_flags(session: Dict, text: str):
    text_lower = text.lower()
    flags = session["red_flags"]
    if any(w in text_lower for w in ["urgent", "immediately", "act now", "right now"]):
        if "urgency_tactics" not in flags:
            flags.append("urgency_tactics")
    if any(w in text_lower for w in ["otp", "pin", "password", "cvv"]):
        if "credential_request" not in flags:
            flags.append("credential_request")
    if any(w in text_lower for w in ["blocked", "suspended", "frozen", "locked"]):
        if "account_threats" not in flags:
            flags.append("account_threats")
    if any(w in text_lower for w in ["http", "click", "link", "www"]):
        if "suspicious_links" not in flags:
            flags.append("suspicious_links")
    if any(w in text_lower for w in ["pay", "transfer", "upi", "bank account"]):
        if "payment_redirection" not in flags:
            flags.append("payment_redirection")
    if any(w in text_lower for w in ["prize", "won", "lottery", "cashback", "reward"]):
        if "reward_lure" not in flags:
            flags.append("reward_lure")
    if any(w in text_lower for w in ["kyc", "verify", "aadhaar", "pan"]):
        if "fake_verification" not in flags:
            flags.append("fake_verification")

def detect_scam_type(session: Dict, text: str):
    if session["scam_type"]:
        return
    text_lower = text.lower()
    if any(w in text_lower for w in ["bank", "account blocked", "sbi", "hdfc", "icici"]):
        session["scam_type"] = "bank_fraud"
    elif any(w in text_lower for w in ["upi", "gpay", "paytm", "phonepe", "cashback"]):
        session["scam_type"] = "upi_fraud"
    elif any(w in text_lower for w in ["http", "click", "link", "www", "offer", "deal"]):
        session["scam_type"] = "phishing"
    elif any(w in text_lower for w in ["lottery", "prize", "won", "winner"]):
        session["scam_type"] = "lottery_scam"
    elif any(w in text_lower for w in ["kyc", "aadhaar", "pan card", "verify identity"]):
        session["scam_type"] = "kyc_fraud"
    elif any(w in text_lower for w in ["refund", "return", "cashback"]):
        session["scam_type"] = "refund_fraud"

def get_history(session_id: str) -> str:
    session = get_session(session_id)
    return "\n".join(session["messages"])

def get_message_count(session_id: str) -> int:
    session = get_session(session_id)
    return len(session["messages"])

def get_intelligence(session_id: str) -> Dict:
    session = get_session(session_id)
    return session["intelligence"]

def get_engagement_duration(session_id: str) -> int:
    session = get_session(session_id)
    return int(time.time() - session["start_time"])

def get_scam_type(session_id: str) -> str:
    session = get_session(session_id)
    return session.get("scam_type", "generic_scam")

def get_red_flags(session_id: str) -> List[str]:
    session = get_session(session_id)
    return session.get("red_flags", [])

def mark_scam_detected(session_id: str):
    session = get_session(session_id)
    session["scam_detected"] = True

def is_scam_detected(session_id: str) -> bool:
    session = get_session(session_id)
    return session["scam_detected"]
