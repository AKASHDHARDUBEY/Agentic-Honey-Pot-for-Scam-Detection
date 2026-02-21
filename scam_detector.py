SCAM_KEYWORDS = [
    "account blocked", "verify", "urgent", "upi", "bank", "lottery",
    "won", "payment", "kyc", "expire", "pan card", "refund",
    "suspended", "account locked", "verify now", "click here",
    "prize", "claim", "immediately", "last chance", "limited time",
    "otp", "blocked", "compromised", "fraud", "unauthorized",
    "security alert", "act now", "penalty", "fine", "legal action",
    "aadhaar", "cvv", "pin", "password", "cashback", "reward",
    "offer", "deal", "free", "credit card", "debit card", "loan",
    "insurance", "policy", "investment", "trading", "crypto"
]

def detect_scam(text: str) -> bool:
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in SCAM_KEYWORDS)
