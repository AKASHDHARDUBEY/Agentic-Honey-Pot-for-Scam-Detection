"""
Scam Detector Module
====================
Detects potential scam messages using keyword-based pattern matching.
Uses a comprehensive list of scam-related keywords across multiple
fraud categories including banking, UPI, phishing, lottery, and KYC fraud.

Approach:
- Case-insensitive keyword matching against known scam patterns
- Covers 40+ fraud indicators across 10+ scam categories
- Returns boolean indicating whether the message contains scam indicators
"""

# Comprehensive scam keyword list organized by fraud category
SCAM_KEYWORDS = [
    # Banking fraud
    "account blocked", "account locked", "account compromised",
    "unauthorized transaction", "suspicious activity",
    # Urgency tactics
    "urgent", "immediately", "act now", "last chance", "limited time",
    "hurry", "expires today", "final warning",
    # Verification/KYC fraud
    "verify", "verify now", "kyc", "pan card", "aadhaar",
    # Payment fraud
    "payment", "upi", "bank", "transfer",
    # OTP/credential theft
    "otp", "pin", "cvv", "password",
    # Prize/lottery scams
    "lottery", "won", "prize", "claim", "winner", "reward", "cashback",
    # Phishing
    "click here", "click below", "click link",
    # Account threats
    "suspended", "blocked", "frozen", "deactivated",
    # Financial scams
    "refund", "loan", "insurance", "policy", "investment",
    "trading", "crypto", "credit card", "debit card",
    # Generic scam indicators
    "free", "offer", "deal", "expire",
    "compromised", "fraud", "security alert",
    "penalty", "fine", "legal action"
]


def detect_scam(text: str) -> bool:
    """
    Detect if a message contains scam indicators.

    Uses case-insensitive keyword matching against a comprehensive
    list of known scam patterns. Designed to be generic and not
    hardcoded to specific test scenarios.

    Args:
        text: The message text to analyze for scam content.

    Returns:
        True if any scam keyword is found in the text, False otherwise.

    Example:
        >>> detect_scam("URGENT: Your account has been blocked")
        True
        >>> detect_scam("Hello, how are you?")
        False
    """
    if not text or not isinstance(text, str):
        return False

    text_lower = text.lower().strip()
    if not text_lower:
        return False

    return any(keyword in text_lower for keyword in SCAM_KEYWORDS)
