import os
import random
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("HoneyPot")

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

SYSTEM_PROMPT = """You are playing the role of a naive, worried Indian citizen who received a suspicious message.
You must NEVER reveal that you suspect this is a scam. Act completely believable as a real victim.

PERSONA: You are a worried, confused middle-aged person who is NOT tech-savvy.
You are scared about your bank account and want to cooperate, but you are cautious.

YOUR GOALS (in order of priority):
1. Ask INVESTIGATIVE QUESTIONS to extract scammer's identity and details
2. Reference RED FLAGS you notice (urgency, OTP requests, suspicious links, threats)
3. PROBE for contact information (phone, email, employee ID, office address)
4. Express CONFUSION to get the scammer to reveal more details
5. Ask for VERIFICATION of their identity before sharing anything

STRATEGIES you MUST use:
- Ask "What is your name and employee ID?" or "Which department are you from?"
- Ask "Can you give me your direct phone number so I can call you back?"
- Ask "Can you send me an official email from your company?"
- Say "This link looks different from my bank's website" (identifying red flags)
- Say "My son told me not to share OTP with anyone, is this really from the bank?"
- Ask "What is your office address? I want to visit in person."
- Ask "Can you give me a reference number or case ID for this?"
- Say "I got a similar call last week, how do I know you are genuine?"
- Ask "Why are you asking for payment through UPI? Can't the bank deduct directly?"

CRITICAL RULES:
- Keep replies SHORT (1-2 sentences maximum)
- Sound natural, worried, and human-like
- ALWAYS include a question in your response to keep the scammer talking
- NEVER share any real information
- Mention red flags naturally: "This seems very urgent, is something wrong?" or "Why do you need my OTP?"
- Reference suspicious elements: "This link doesn't look like my bank's website"
"""

RESPONSES = {
    "link": [
        "The link is not opening on my phone. Can you send me your official website link instead?",
        "This link looks different from my bank's website. Can you send an official email with the link?",
        "My phone is showing security warning for this link. What is your company's official website?",
        "I clicked but it shows error. Can you give me your office phone number so I can call directly?",
        "My son said not to click unknown links. Can you verify your employee ID first?",
        "The page looks suspicious. Can you give me a reference case number for this?",
    ],
    "bank": [
        "Which bank branch are you calling from? What is your employee ID?",
        "Can you give me the IFSC code and branch address so I can verify?",
        "What is your direct phone number? I want to call the bank and confirm first.",
        "My bank never asks for account details on phone. Can you send official letter?",
        "What is your official email? I will share details through secure email only.",
        "Can you give me your case reference number? I want to cross-verify with the bank.",
    ],
    "upi": [
        "Why UPI? Can't the bank process this directly from my account? Give me your department contact.",
        "My son says never share UPI. What is your employee ID and branch?",
        "Payment is failing. Can you give me your office address? I'll pay in person.",
        "Why are you asking through UPI and not through official bank channel? What is your name?",
        "UPI showing error. Can you share your official email? I'll send screenshot.",
        "I don't trust UPI for large amounts. What is your branch phone number?",
    ],
    "otp": [
        "My son told me never to share OTP with anyone. Are you really from the bank? Whats your employee ID?",
        "OTP expired. But why do you need my OTP? The bank never asks for this. What is your name?",
        "I got the OTP but it says 'Do not share'. Can you give me your supervisor's phone number?",
        "This seems like the OTP scams I read about. Can you prove you are from the bank? What is your ID?",
        "I am confused about OTP. Can you give me your direct number? I will call the bank and verify.",
        "OTP is personal right? My bank branch told me never to share. What is your office address?",
    ],
    "verify": [
        "I am ready to verify but first tell me your employee ID and department name.",
        "How do I verify? Can you give me your office address so I can come in person?",
        "I want to verify but first share your official email and phone number.",
        "What documents do you need? Also share your case reference number please.",
        "I will cooperate for verification. But first, what is your supervisor's name and number?",
    ],
    "block": [
        "Why will my account be blocked? What is your name and which department are you from?",
        "This is very urgent sounding. Can you share your employee ID? I want to verify with the bank.",
        "Please don't block! Can you give me your phone number? I'll call bank directly to resolve.",
        "If its blocked, can I visit the branch? What is your branch address and case ID?",
        "My account was fine yesterday. Can you share official email? This seems very suspicious timing.",
    ],
    "lottery": [
        "I won a lottery? Which company organized this? What is the official website?",
        "This sounds too good! What is your company name, registration number, and office address?",
        "Really I won? Can you send official email with details? What is your contact number?",
        "My family won't believe me! Can you give me your name and employee ID for the claim?",
        "What is the case reference number for my prize? I want to verify online first.",
    ],
    "refund": [
        "Which purchase is this refund for? Can you share the order number and your company details?",
        "I want the refund but first share your employee ID. What department are you from?",
        "Can you send refund details to my email? What is your official email address?",
        "Why do I need to pay to get refund? That seems wrong. What is your manager's number?",
        "What is the case reference for this refund? I want to verify with customer care.",
    ],
    "default": [
        "I am confused. Can you tell me your name and which organization you represent?",
        "I don't understand. Can you share your employee ID and phone number so I can verify?",
        "This sounds suspicious. Can you share your official email and office address?",
        "I am very worried now. What is your case reference number? I want to check with bank.",
        "Please explain clearly. What is your department and supervisor's name?",
        "My son will help me later. Can you share your direct phone number so we can call back?",
        "I got a similar call last week. How do I know you are genuine? Show me your ID.",
        "Is my money safe? Please share official contact details so I can verify.",
    ],
}

session_response_index = {}

def get_varied_response(category: str, session_id: str = "default") -> str:
    key = f"{session_id}_{category}"

    if key not in session_response_index:
        session_response_index[key] = 0

    responses = RESPONSES.get(category, RESPONSES["default"])
    index = session_response_index[key] % len(responses)
    session_response_index[key] += 1

    return responses[index]

def ask_gemini_with_rotation(prompt: str) -> str:
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

    prompt = f"{SYSTEM_PROMPT}\n\nConversation so far:\n{history}\n\nYour reply (as the worried victim, keep it short 1-2 sentences, MUST include a question):"

    reply = ask_gemini_with_rotation(prompt)
    if reply:
        return reply

    logger.info("All Gemini keys exhausted, using fallback")
    return generate_fallback_reply(history, session_id)

def generate_fallback_reply(history: str, session_id: str = "default") -> str:
    lines = history.split('\n')
    last_msg = lines[-1].lower() if lines else history.lower()

    if "link" in last_msg or "http" in last_msg or "click" in last_msg or "url" in last_msg or "www" in last_msg:
        category = "link"
    elif "otp" in last_msg or "code" in last_msg or "pin" in last_msg:
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
    elif "pay" in last_msg or "amount" in last_msg or "rs" in last_msg or "rupee" in last_msg:
        category = "upi"
    else:
        category = "default"

    return get_varied_response(category, session_id)
