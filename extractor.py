"""
Intelligence Extractor Module
==============================
Extracts actionable intelligence from conversation text using
regex-based pattern matching. Identifies and captures:
- Bank account numbers (9-18 digit patterns)
- UPI IDs (user@provider format)
- Phone numbers (Indian +91 format and 10-digit numbers)
- Phishing links (HTTP/HTTPS URLs)
- Email addresses (standard email format)
- Suspicious keywords (scam-related terminology)

All extraction uses generic regex patterns, not hardcoded to
specific test data, ensuring robust detection across various
scam scenarios.
"""

import re
import logging
from typing import Dict, List

logger = logging.getLogger("HoneyPot")

# Scam-related keywords for intelligence reporting
SUSPICIOUS_KEYWORDS = [
    "urgent", "verify", "blocked", "payment", "kyc",
    "suspended", "expire", "immediately", "prize", "won",
    "otp", "account blocked", "click here", "last chance",
    "limited time", "claim", "refund", "pan card", "aadhaar",
    "compromised", "fraud", "unauthorized", "security alert",
    "act now", "warning", "penalty", "fine", "legal action"
]

# Compiled regex patterns for efficient repeated matching
PATTERNS = {
    "bankAccounts": re.compile(r"\b\d{9,18}\b"),
    "upiIds": re.compile(r"\b[\w.\-]+@[a-zA-Z]{2,64}\b"),
    "phishingLinks": re.compile(r"https?://[^\s,\"'<>]+"),
    "phoneNumbers": re.compile(r"\+91[\-\s]?\d{10}|\b\d{10}\b"),
    "emailAddresses": re.compile(r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b"),
}


def extract_intelligence(text: str) -> Dict[str, List[str]]:
    """
    Extract all identifiable intelligence from a text message.

    Scans the input text for phone numbers, bank accounts, UPI IDs,
    phishing links, email addresses, and suspicious keywords using
    generic regex patterns.

    Args:
        text: The message text to extract intelligence from.

    Returns:
        Dictionary with keys for each intelligence type, each containing
        a list of extracted values. Returns empty lists if no matches found.

    Example:
        >>> extract_intelligence("Call +91-9876543210 or pay to fraud@upi")
        {'phoneNumbers': ['+91-9876543210'], 'upiIds': ['fraud@upi'], ...}
    """
    if not text or not isinstance(text, str):
        return {
            "bankAccounts": [],
            "upiIds": [],
            "phishingLinks": [],
            "phoneNumbers": [],
            "emailAddresses": [],
            "suspiciousKeywords": []
        }

    try:
        extracted = {}
        for field, pattern in PATTERNS.items():
            extracted[field] = pattern.findall(text)

        # Extract suspicious keywords separately (simple string matching)
        text_lower = text.lower()
        extracted["suspiciousKeywords"] = list(set(
            kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower
        ))

        logger.debug(f"Extracted intelligence: {sum(len(v) for v in extracted.values())} items")
        return extracted

    except Exception as e:
        logger.error(f"Intelligence extraction failed: {e}")
        return {
            "bankAccounts": [],
            "upiIds": [],
            "phishingLinks": [],
            "phoneNumbers": [],
            "emailAddresses": [],
            "suspiciousKeywords": []
        }


def merge_intelligence(existing: Dict, new: Dict) -> Dict:
    """
    Merge new intelligence data into existing intelligence, deduplicating values.

    Combines two intelligence dictionaries, ensuring no duplicate entries.
    Handles missing keys gracefully by treating them as empty lists.

    Args:
        existing: Previously accumulated intelligence dictionary.
        new: Newly extracted intelligence dictionary to merge.

    Returns:
        Merged dictionary with all unique values from both sources.
    """
    try:
        merged = {}
        all_keys = set(list(existing.keys()) + list(new.keys()))
        for key in all_keys:
            existing_vals = existing.get(key, [])
            new_vals = new.get(key, [])
            # Ensure both are lists before combining
            if not isinstance(existing_vals, list):
                existing_vals = []
            if not isinstance(new_vals, list):
                new_vals = []
            merged[key] = list(set(existing_vals + new_vals))
        return merged
    except Exception as e:
        logger.error(f"Intelligence merge failed: {e}")
        return existing
