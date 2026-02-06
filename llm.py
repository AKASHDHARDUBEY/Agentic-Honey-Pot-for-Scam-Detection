import os
import random
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("HoneyPot")

# Load all Gemini API keys for rotation
GEMINI_KEYS = [
    os.getenv("GEMINI_KEY1"),
    os.getenv("GEMINI_KEY2"),
    os.getenv("GEMINI_KEY3"),
    os.getenv("GEMINI_KEY4"),
]
GEMINI_KEYS = [k for k in GEMINI_KEYS if k]

USE_LLM = len(GEMINI_KEYS) > 0

if USE_LLM:
    import google.generativeai as genai

SYSTEM_PROMPT = """You are a normal Indian person who received a suspicious message.
You must NEVER reveal that you suspect this is a scam.
Your goal is to keep the scammer talking and extract information from them.

Persona: You are a worried, slightly confused middle-aged person who is not tech-savvy.
You are concerned about your bank account and want to cooperate.

Strategies:
- Ask questions to get payment details (UPI IDs, bank accounts)
- Pretend to have technical difficulties to get links resent
- Act confused to get more information
- Express urgency to make them reveal more

IMPORTANT: Keep replies short (1-2 sentences). Sound natural and human."""

# Dynamic response pools for variety
RESPONSES = {
    "link": [
        "The link is not opening on my phone. Can you send it again?",
        "I clicked but it shows error. Please resend the link.",
        "My phone is showing security warning. Is there another link?",
        "The page is loading very slow. Can you send direct link?",
        "I am getting 'page not found' error. Please help.",
    ],
    "bank": [
        "Which bank is this account from? I need the IFSC code.",
        "Is this SBI or HDFC? I need to add as beneficiary.",
        "What is the account holder name? My bank is asking.",
        "Can you share the branch name also? I need it for NEFT.",
        "My app needs IFSC code. What is the branch code?",
    ],
    "upi": [
        "I am trying to pay but GPay shows error. Another UPI ID?",
        "PhonePe is not working. Do you have Paytm number?",
        "Payment failed. Can you check if UPI ID is correct?",
        "My bank limit is Rs 5000 only. Can I send in parts?",
        "UPI showing 'beneficiary not found'. Please verify ID.",
    ],
    "otp": [
        "I received OTP but it says expired. Can you send again?",
        "The OTP is 6 digits right? I got only 4 digits.",
        "My message is delayed. Can you resend the OTP please?",
        "I entered the OTP but it shows invalid. New one please?",
        "OTP expired before I could type. Please send new one.",
    ],
    "verify": [
        "I am ready to verify. What are the exact steps?",
        "How do I verify? I don't want to lose my money.",
        "Please guide me step by step. I am not tech savvy.",
        "I will do the verification. Just tell me what to do.",
        "Is there any form I need to fill for verification?",
    ],
    "block": [
        "Oh no! Why will my account be blocked? Please help!",
        "I use this account daily for my business. Please don't block!",
        "What did I do wrong? I will cooperate fully.",
        "Please give me some time. I will do everything needed.",
        "My family depends on this account. Please don't freeze it!",
    ],
    "lottery": [
        "Really? I won? This is amazing! Where should I pay?",
        "I never entered any lottery. But I won? How much?",
        "What is the process to claim? I am very excited!",
        "Is this genuine? I never win anything. So happy!",
        "My lucky day! Tell me the next steps please.",
    ],
    "refund": [
        "Yes I was waiting for this refund! What do I need to do?",
        "Finally my money is coming back. How to receive it?",
        "How long will the refund take? I need it urgently.",
        "Will it come to my bank account directly?",
        "Thank you for the refund. What details do you need?",
    ],
    "default": [
        "I received your message. I am confused. What should I do?",
        "Please explain clearly. I don't understand technical things.",
        "I am very worried now. Please help me understand.",
        "What is happening to my account? I am scared.",
        "My son is not here to help. Can you explain simply?",
        "I will cooperate fully. Just tell me what to do.",
        "Is my money safe? Please help me.",
        "I am an old person. Please guide me properly.",
    ],
}

# Track responses per session to avoid repetition
session_response_index = {}

def get_varied_response(category: str, session_id: str = "default") -> str:
    """Get a varied response, avoiding repetition within a session"""
    key = f"{session_id}_{category}"
    
    if key not in session_response_index:
        session_response_index[key] = 0
    
    responses = RESPONSES.get(category, RESPONSES["default"])
    index = session_response_index[key] % len(responses)
    session_response_index[key] += 1
    
    return responses[index]

def ask_gemini_with_rotation(prompt: str) -> str:
    """Try each Gemini key until one works"""
    for i, key in enumerate(GEMINI_KEYS):
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            logger.info(f"Gemini Key {i+1} succeeded")
            return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini Key {i+1} failed: {str(e)[:50]}")
            continue
    return None

def generate_llm_reply(history: str, session_id: str = "default") -> str:
    if not USE_LLM:
        return generate_fallback_reply(history, session_id)
    
    prompt = f"{SYSTEM_PROMPT}\n\nConversation so far:\n{history}\n\nYour reply (as the victim):"
    
    # Try Gemini with key rotation
    reply = ask_gemini_with_rotation(prompt)
    if reply:
        return reply
    
    # Fallback to rule-based
    logger.info("All Gemini keys exhausted, using fallback")
    return generate_fallback_reply(history, session_id)

def generate_fallback_reply(history: str, session_id: str = "default") -> str:
    """Generate context-aware, varied responses"""
    history_lower = history.lower()
    
    # Get the last message for context
    lines = history.split('\n')
    last_msg = lines[-1].lower() if lines else history_lower
    
    # Determine category based on last message content
    if "link" in last_msg or "http" in last_msg or "click" in last_msg:
        category = "link"
    elif "otp" in last_msg:
        category = "otp"
    elif "upi" in last_msg or "pay" in last_msg or "gpay" in last_msg or "paytm" in last_msg or "phonepe" in last_msg:
        category = "upi"
    elif "bank" in last_msg or "account" in last_msg or "transfer" in last_msg or "ifsc" in last_msg:
        category = "bank"
    elif "verify" in last_msg or "kyc" in last_msg:
        category = "verify"
    elif "block" in last_msg or "suspend" in last_msg or "freeze" in last_msg:
        category = "block"
    elif "lottery" in last_msg or "won" in last_msg or "prize" in last_msg or "winner" in last_msg:
        category = "lottery"
    elif "refund" in last_msg:
        category = "refund"
    else:
        category = "default"
    
    return get_varied_response(category, session_id)
