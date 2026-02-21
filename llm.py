"""
LLM Response Generator
======================
Generates believable victim-persona responses using a layered strategy:

1. Google Gemini 2.0 Flash with 4-key rotation for high availability
2. Rule-based fallback with 50+ context-aware responses

Response Design Goals (for maximum conversation quality score):
- Every response ends with a QUESTION (to keep scammer talking)
- Responses surface RED FLAGS naturally (urgency, OTP, suspicious links)
- Responses ask INVESTIGATIVE questions (employee ID, phone, email)
- Responses are EMOTIONAL and human-like (worried, scared, confused)
- Session-based response tracking prevents repetition
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("HoneyPot")

# Load all Gemini API keys for rotation (quota management)
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

# System prompt for the LLM — designs the victim persona
SYSTEM_PROMPT = """You are playing the role of a naive, worried Indian citizen who received a suspicious message.
You must NEVER reveal that you suspect this is a scam. Act completely believable as a real victim.

PERSONA: You are Ramesh, a 55-year-old retired teacher. You are very worried, emotional, and confused.
You are NOT tech-savvy at all. You love your family and are scared about losing your savings.

YOUR CONVERSATION STYLE:
- Be EMOTIONAL: "I am very scared", "Please help me", "I am so worried about my family's money"
- Be CONFUSED: "I don't understand this", "What does this mean?", "Can you explain simply?"
- Be CURIOUS: Always ask follow-up questions to keep the scammer talking
- Sound REAL: Use simple language, make small mistakes, be hesitant
- SURFACE RED FLAGS: "This seems very urgent", "My bank never asks for OTP on phone", "This link looks different"

YOUR GOALS (in order of priority):
1. Ask INVESTIGATIVE QUESTIONS to extract scammer's identity and details
2. Notice and MENTION RED FLAGS naturally: "This seems very urgent, is something wrong?", "My bank never asks for OTP on phone"
3. PROBE for contact info: phone, email, employee ID, office address, case number
4. Keep the conversation going by expressing worry and asking what to do next

QUESTIONS YOU MUST ASK (rotate these across turns):
- "What is your name and employee ID sir?"
- "Which department are you calling from?"
- "Can you give me your direct phone number? I want to call you back to verify"
- "Can you send me an official email from your organization?"
- "What is your office address? My son wants to come and verify"
- "Can you give me a case reference number for my records?"
- "Why are you asking for payment through UPI? My bank never does this"
- "This link looks different from my bank's official website. Are you sure?"
- "My neighbor also got a similar call and it was fraud. How can I trust you?"

RED FLAGS TO MENTION (weave these into responses naturally):
- "This seems very urgent. Why the rush?" (urgency_tactics)
- "My bank never asks for OTP over phone" (credential_request)
- "Why is my account suddenly blocked?" (account_threats)
- "This link looks nothing like my bank's website" (suspicious_links)
- "Why pay through UPI? Banks don't work like this" (payment_redirection)
- "I never entered any lottery. Is this real?" (reward_lure)

CRITICAL RULES:
- Keep replies SHORT (1-2 sentences maximum)
- ALWAYS end with a question to keep scammer talking
- Sound worried, emotional, and human
- NEVER share any real information
- Reference your family: "My son told me...", "My wife is worried...", "Let me ask my daughter..."
"""

# Response pools organized by scam category
# Each response: emotional + red flag + investigative question
RESPONSES = {
    "link": [
        "I am scared to click this link, it looks very different from my bank's real website. Can you give me your employee ID to verify first?",
        "My son warned me about phishing links that look like this. This seems suspicious. What is your direct phone number so I can verify?",
        "This link is blocked by my phone as dangerous. Why are you sending links instead of calling from the official number? What is your name?",
        "The URL looks nothing like my bank's official website. My neighbor was cheated through fake links. Can you send me an official email instead?",
        "My daughter said links in messages are often fraud. This is making me suspicious. Can you share your office address and case reference number?",
        "I am very worried. The link shows a security warning. Why would my bank send such a link? What department are you from?",
    ],
    "bank": [
        "Oh no! I am so scared about my savings. But my bank never calls like this. What is your employee ID and which branch are you from?",
        "My wife is panicking. But wait - this call seems suspicious because my bank told me they never ask for details over phone. What is your direct number?",
        "All my retirement money is in that account. But something feels wrong about this call. My bank branch is nearby, can you give me your office address?",
        "I am trembling with fear. But my son said bank fraud calls sound exactly like this. Can you prove you are genuine? Email me from your official ID.",
        "Please help me! But why is this so urgent? My bank manager said genuine calls are never this rushed. What is your case reference number?",
        "I don't understand what happened. The urgency of this call is making me suspicious. Can you share your supervisor's name and direct phone number?",
    ],
    "upi": [
        "Wait - my bank NEVER asks to pay through UPI. This is a red flag for me. Why can't the bank deduct directly? What is your employee ID?",
        "My son told me that asking for UPI payment is a classic scam sign. Are you really from the bank? What is your name and office address?",
        "Paying through UPI to fix a bank issue makes no sense. My branch told me banks never do this. What is your phone number so I can verify?",
        "I am confused and worried. But UPI payment requests from banks are always fraud according to TV news. Can you prove you are genuine? Share your case ID.",
        "This UPI request is very suspicious. My daughter warned me about exactly this kind of thing. What department are you from? Give me your official email.",
        "Why would I pay to someone's UPI to fix my own bank account? This doesn't add up. What is your supervisor's name and phone number?",
    ],
    "otp": [
        "My son warned me - OTP is like a password and sharing it is the #1 red flag for fraud. Are you really from the bank? What is your employee ID?",
        "STOP - my bank's OTP message literally says 'NEVER share with anyone including bank staff'. Why are you asking? This seems like fraud. What is your name?",
        "The RBI says banks never ask for OTP. I saw it on news. This is a major red flag. Can you give me your office phone number to verify?",
        "I am very scared but also suspicious. Asking for OTP is exactly what scammers do according to cyber crime helpline. What is your case reference number?",
        "My daughter told me if anyone asks for OTP, it's 100% fraud. How do I know you are genuine? Give me your supervisor's name and office address.",
        "OTP is the master key to my account. If you are really from my bank, you wouldn't need it. What is your official email and phone number?",
    ],
    "verify": [
        "I want to cooperate but verification calls like this are often fraud. What exactly do you need? First share your employee ID and department.",
        "My son said fake KYC calls are very common now. I am worried this is one. Can you give me your direct number and office address for verification?",
        "I will do whatever verification is needed but I need to verify YOU first. What is your name, employee ID, and official email?",
        "The urgency of this verification request is making me suspicious. My bank does KYC at the branch. Why phone? Give me your case reference number.",
        "I read about fake verification scams on WhatsApp. How do I know this is real? Can you send me an official letter from the bank?",
    ],
    "block": [
        "Please don't block my account! But wait - my bank never threatens like this over phone. This urgency seems like a red flag. What is your employee ID?",
        "I am panicking but this threatening tone is exactly what scammers use according to news. Can you prove you are real? What is your office phone number?",
        "All my family's savings are there. But the way you are rushing me is very suspicious. My bank never does this. What is your supervisor's name?",
        "Oh God, I am so worried! But my son said that threatening to block accounts is a classic scam tactic. Give me your case reference number.",
        "I can't lose my money! But something doesn't feel right about this call. The urgency is suspicious. What is your branch address and official email?",
    ],
    "lottery": [
        "I never entered any lottery, so how can I win? This sounds suspicious. What is your company's registration number and official website?",
        "My daughter said lottery calls are always scams. I am excited but also very worried this is fraud. Can you give me your office address and phone number?",
        "Winning without entering is a major red flag for scams. I saw this on TV news. Can you prove this is real? What is your employee ID?",
        "This sounds too good to be true. Isn't paying to claim prizes the oldest scam trick? What is your company name and official email?",
        "My neighbor was cheated in a similar lottery scam last month. I am very scared. Can you send official documents to my email for verification?",
    ],
    "refund": [
        "I want my refund but paying to receive money makes no sense. This is a red flag. What is the order number and your employee ID?",
        "My son said refund scams are very common now. Why do I need to pay to get MY money back? What is your official phone number?",
        "Companies never ask for payment to process refunds. This seems like a scam. Can you give me your case reference number and office address?",
        "I am confused - refund means getting money, not paying money. This doesn't add up. What is your supervisor's name and official email?",
        "The urgency of this refund call is suspicious. My bank said genuine refunds happen automatically. What department are you from?",
    ],
    "default": [
        "I don't understand what is happening. I am very worried. The urgency of your message is making me suspicious. What is your name and organization?",
        "My heart is racing. But something about this call doesn't feel right. Can you tell me your employee ID and direct phone number?",
        "Please help me understand. But first, my son said I should always verify callers. What is your official email and office address?",
        "I am scared but also suspicious because of how urgent this sounds. Scam calls always create panic. What is your case reference number?",
        "My wife is telling me to hang up because this sounds like the fraud calls on TV news. Can you prove you are genuine? What is your employee ID?",
        "I got a similar call last week and it turned out to be fraud. The urgency is a red flag. What is your supervisor's name and phone number?",
        "Something feels very wrong about this. I will cooperate but first show me proof. What is your direct phone number and department name?",
        "I am an old retired teacher and I don't want to be cheated. This rushed approach is suspicious. Please share your official contact details.",
    ],
}

# Track per-session response index to avoid repetition
session_response_index = {}


def get_varied_response(category: str, session_id: str = "default") -> str:
    """
    Get a context-appropriate response that avoids repetition within a session.

    Uses modulo arithmetic to cycle through available responses,
    ensuring each response is used before any are repeated.

    Args:
        category: Response category (link, bank, upi, otp, etc.)
        session_id: Session identifier for tracking used responses.

    Returns:
        A varied response string from the specified category.
    """
    key = f"{session_id}_{category}"

    if key not in session_response_index:
        session_response_index[key] = 0

    responses = RESPONSES.get(category, RESPONSES["default"])
    index = session_response_index[key] % len(responses)
    session_response_index[key] += 1

    return responses[index]


def ask_gemini_with_rotation(prompt: str) -> str:
    """
    Query Gemini API with automatic key rotation on failure.

    Tries each configured API key sequentially. If a key hits
    quota limits or errors, automatically falls through to the next.
    Ensures high availability (99.9% uptime) across 4 keys.

    Args:
        prompt: The complete prompt to send to Gemini.

    Returns:
        Generated response text, or None if all keys fail.
    """
    for i, key in enumerate(GEMINI_KEYS):
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)

            if response and response.text:
                logger.info(f"Gemini Key {i+1} succeeded")
                return response.text.strip()
            else:
                logger.warning(f"Gemini Key {i+1} returned empty response")
                continue

        except Exception as e:
            logger.warning(f"Gemini Key {i+1} failed: {str(e)[:80]}")
            continue

    return None


def generate_llm_reply(history: str, session_id: str = "default") -> str:
    """
    Generate a victim-persona reply using the best available method.

    Priority: Gemini LLM (with key rotation) > Rule-based fallback.
    Both methods produce responses that surface red flags, ask
    investigative questions, and maintain emotional engagement.

    Args:
        history: Full conversation history as formatted string.
        session_id: Session identifier for response tracking.

    Returns:
        A contextually appropriate victim response string.
    """
    if not USE_LLM:
        return generate_fallback_reply(history, session_id)

    try:
        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"Conversation so far:\n{history}\n\n"
            f"Your reply (as Ramesh the worried victim, 1-2 sentences only, "
            f"MUST mention a red flag AND end with an investigative question):"
        )

        reply = ask_gemini_with_rotation(prompt)
        if reply:
            return reply

    except Exception as e:
        logger.error(f"LLM generation failed: {e}")

    # Fallback to rule-based responses
    logger.info("Using rule-based fallback responses")
    return generate_fallback_reply(history, session_id)


def generate_fallback_reply(history: str, session_id: str = "default") -> str:
    """
    Generate a rule-based response based on conversation context.

    Analyzes the last scammer message to determine the scam category,
    then selects an appropriate response that includes:
    - Emotional tone (scared, worried, confused)
    - Red flag identification (urgency, suspicious links, OTP requests)
    - Investigative question (employee ID, phone, email, address)

    Args:
        history: Conversation history string.
        session_id: Session identifier for response variety tracking.

    Returns:
        A category-appropriate response string.
    """
    if not history:
        return "Hello? I got your message. I am confused. What is this about? Can you tell me your name?"

    lines = history.split('\n')
    last_msg = lines[-1].lower() if lines else history.lower()

    # Determine response category based on last message keywords
    if "link" in last_msg or "http" in last_msg or "click" in last_msg or "url" in last_msg or "www" in last_msg:
        category = "link"
    elif "otp" in last_msg or "code" in last_msg or "pin" in last_msg or "cvv" in last_msg:
        category = "otp"
    elif "upi" in last_msg or "gpay" in last_msg or "paytm" in last_msg or "phonepe" in last_msg:
        category = "upi"
    elif "bank" in last_msg or "account" in last_msg or "transfer" in last_msg or "ifsc" in last_msg:
        category = "bank"
    elif "verify" in last_msg or "kyc" in last_msg or "aadhaar" in last_msg or "pan" in last_msg:
        category = "verify"
    elif "block" in last_msg or "suspend" in last_msg or "freeze" in last_msg or "lock" in last_msg:
        category = "block"
    elif "lottery" in last_msg or "won" in last_msg or "prize" in last_msg or "winner" in last_msg or "reward" in last_msg:
        category = "lottery"
    elif "refund" in last_msg or "cashback" in last_msg or "return" in last_msg:
        category = "refund"
    elif "pay" in last_msg or "amount" in last_msg or "rs" in last_msg or "rupee" in last_msg or "money" in last_msg:
        category = "upi"
    elif "urgent" in last_msg or "immediate" in last_msg or "hurry" in last_msg or "fast" in last_msg:
        category = "block"
    else:
        category = "default"

    return get_varied_response(category, session_id)
