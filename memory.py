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
                "suspiciousKeywords": []
            },
            "scam_detected": False
        }
    return sessions[session_id]

def add_message(session_id: str, sender: str, text: str):
    session = get_session(session_id)
    session["messages"].append(f"{sender}: {text}")
    
    new_intel = extract_intelligence(text)
    session["intelligence"] = merge_intelligence(session["intelligence"], new_intel)

def get_history(session_id: str) -> str:
    session = get_session(session_id)
    return "\n".join(session["messages"])

def get_message_count(session_id: str) -> int:
    session = get_session(session_id)
    return len(session["messages"])

def get_intelligence(session_id: str) -> Dict:
    session = get_session(session_id)
    return session["intelligence"]

def mark_scam_detected(session_id: str):
    session = get_session(session_id)
    session["scam_detected"] = True

def is_scam_detected(session_id: str) -> bool:
    session = get_session(session_id)
    return session["scam_detected"]
