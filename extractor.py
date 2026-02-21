import re
from typing import Dict, List

SUSPICIOUS_KEYWORDS = [
    "urgent", "verify", "blocked", "payment", "kyc",
    "suspended", "expire", "immediately", "prize", "won",
    "otp", "account blocked", "click here", "last chance",
    "limited time", "claim", "refund", "pan card", "aadhaar",
    "compromised", "fraud", "unauthorized", "security alert",
    "act now", "warning", "penalty", "fine", "legal action"
]

def extract_intelligence(text: str) -> Dict[str, List[str]]:
    return {
        "bankAccounts": re.findall(r"\b\d{9,18}\b", text),
        "upiIds": re.findall(r"\b[\w.\-]+@[a-zA-Z]{2,64}\b", text),
        "phishingLinks": re.findall(r"https?://[^\s,\"']+", text),
        "phoneNumbers": re.findall(r"\+91[\-\s]?\d{10}|\b\d{10}\b", text),
        "emailAddresses": re.findall(r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b", text),
        "suspiciousKeywords": list(set(kw for kw in SUSPICIOUS_KEYWORDS if kw in text.lower()))
    }

def merge_intelligence(existing: Dict, new: Dict) -> Dict:
    merged = {}
    all_keys = set(list(existing.keys()) + list(new.keys()))
    for key in all_keys:
        combined = list(set(existing.get(key, []) + new.get(key, [])))
        merged[key] = combined
    return merged
