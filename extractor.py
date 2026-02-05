import re
from typing import Dict, List

SUSPICIOUS_KEYWORDS = [
    "urgent", "verify", "blocked", "payment", "kyc", 
    "suspended", "expire", "immediately", "prize", "won"
]

def extract_intelligence(text: str) -> Dict[str, List[str]]:
    return {
        "bankAccounts": re.findall(r"\b\d{9,18}\b", text),
        "upiIds": re.findall(r"\b[\w.\-]+@[a-zA-Z]{2,64}\b", text),
        "phishingLinks": re.findall(r"https?://[^\s]+", text),
        "phoneNumbers": re.findall(r"\+91\d{10}|\b\d{10}\b", text),
        "suspiciousKeywords": [kw for kw in SUSPICIOUS_KEYWORDS if kw in text.lower()]
    }

def merge_intelligence(existing: Dict, new: Dict) -> Dict:
    merged = {}
    for key in existing:
        combined = list(set(existing.get(key, []) + new.get(key, [])))
        merged[key] = combined
    return merged
