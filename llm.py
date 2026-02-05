import os
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
GEMINI_KEYS = [k for k in GEMINI_KEYS if k]  # Remove None values

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

def generate_llm_reply(history: str) -> str:
    if not USE_LLM:
        return generate_fallback_reply(history)
    
    prompt = f"{SYSTEM_PROMPT}\n\nConversation so far:\n{history}\n\nYour reply (as the victim):"
    
    # Try Gemini with key rotation
    reply = ask_gemini_with_rotation(prompt)
    if reply:
        return reply
    
    # Fallback to rule-based
    logger.info("All Gemini keys exhausted, using fallback")
    return generate_fallback_reply(history)

def generate_fallback_reply(history: str) -> str:
    history_lower = history.lower()
    
    # Get the last message for context
    lines = history.split('\n')
    last_msg = lines[-1].lower() if lines else history_lower
    
    # Context-aware responses based on message content
    if "link" in last_msg or "http" in last_msg or "click" in last_msg:
        return "The link is not opening on my phone. Can you send it again? I really need to fix this."
    
    elif "bank" in last_msg or "account" in last_msg or "transfer" in last_msg:
        return "Which bank is this account from? I need the IFSC code to add as beneficiary."
    
    elif "upi" in last_msg or "pay" in last_msg or "gpay" in last_msg or "paytm" in last_msg:
        return "I am trying to pay but my GPay shows error. Do you have another UPI ID?"
    
    elif "otp" in last_msg:
        return "I received the OTP but it says expired. Can you send another one?"
    
    elif "verify" in last_msg or "kyc" in last_msg:
        return "I am ready to verify. Please tell me the exact steps. I don't want to lose my money."
    
    elif "block" in last_msg or "suspend" in last_msg or "freeze" in last_msg:
        return "Oh no! Why will my account be blocked? I use it daily for my business. Please help!"
    
    elif "lottery" in last_msg or "won" in last_msg or "prize" in last_msg:
        return "Really? I won? This is amazing! Where should I pay the processing fee?"
    
    elif "refund" in last_msg:
        return "Yes I was waiting for this refund! What do I need to do to receive it?"
    
    else:
        return "I received your message. I am very confused. What should I do? Please help me."
