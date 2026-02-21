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

PERSONA: You are Ramesh, a 55-year-old retired teacher. You are very worried, emotional, and confused.
You are NOT tech-savvy at all. You love your family and are scared about losing your savings.

YOUR CONVERSATION STYLE:
- Be EMOTIONAL: "I am very scared", "Please help me", "I am so worried about my family's money"
- Be CONFUSED: "I don't understand this", "What does this mean?", "Can you explain simply?"
- Be CURIOUS: Always ask follow-up questions to keep the scammer talking
- Sound REAL: Use simple language, make small mistakes, be hesitant

YOUR GOALS (in order of priority):
1. Ask INVESTIGATIVE QUESTIONS to extract scammer's identity and details
2. Notice and mention RED FLAGS naturally: "This seems very urgent, is something wrong?", "My bank never asks for OTP on phone"
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

CRITICAL RULES:
- Keep replies SHORT (1-2 sentences maximum)
- ALWAYS end with a question to keep scammer talking
- Sound worried, emotional, and human
- NEVER share any real information
- Mention suspicious things naturally: "This seems very urgent", "Why do you need my OTP?", "This link looks strange"
- Reference your family: "My son told me...", "My wife is worried...", "Let me ask my daughter..."
"""

RESPONSES = {
    "link": [
        "I am scared to click this link. It looks different from my bank's website. Can you send me your official website link instead?",
        "My son told me never to click unknown links. Can you tell me your employee ID first? I want to verify you are genuine.",
        "This link is showing security warning on my phone. I am very worried. What is your office phone number? I want to call and confirm.",
        "The link is not opening. My daughter says this looks like a fraud link. Can you send official email instead?",
        "I am confused. This URL looks different from what I usually see. Can you give me your name and case reference number?",
        "My phone is blocking this link as dangerous. Can you share your company's official website and office address?",
    ],
    "bank": [
        "Oh no! What happened to my bank account? I am very scared. Which branch are you calling from? What is your employee ID?",
        "Please don't block my account! All my retirement savings are there. Can you give me your direct phone number? I want to call the bank and verify.",
        "My wife will be so worried. Can you tell me your name and which department you are from? I need to confirm with my bank branch.",
        "I am trembling with fear. Is this really from the bank? Can you share your official email? My son wants to verify.",
        "How did my account get compromised? Can you give me the case reference number? I want to visit my bank branch tomorrow.",
        "I don't understand what happened. Can you explain step by step? Also what is your branch address?",
    ],
    "upi": [
        "I am confused about UPI payment. My bank never asks to pay through UPI. Why can't the bank deduct directly? What is your name?",
        "My son told me never to send money to unknown UPI IDs. Are you really from the bank? What is your employee ID?",
        "I am very worried. Why do I need to pay to get my own money? This doesn't sound right. What is your office address?",
        "UPI is showing error. But first, can you tell me why the bank is asking for payment through UPI? What is your phone number?",
        "I don't trust UPI for large amounts. My neighbor was cheated like this. Can you prove you are genuine? Share your case reference number.",
        "This seems suspicious to me. My daughter said banks never ask for UPI payments. What is your supervisor's name and number?",
    ],
    "otp": [
        "My son told me OTP is like a password and I should NEVER share it with anyone. Are you really from the bank? What is your employee ID?",
        "I am scared. The OTP message says 'DO NOT share with anyone'. Why are you asking for it? What is your name and department?",
        "This sounds like the phone fraud I saw on TV news. Can you prove you are from the bank? Give me your office phone number.",
        "OTP expired already. But I am confused - if you are from my bank, why do you need MY OTP? Can you give me your supervisor's number?",
        "I am very worried now. Is this really safe? My bank branch manager said never share OTP. What is your direct phone number so I can verify?",
        "My daughter warned me about OTP scams. How do I know you are genuine? Please share your employee ID and office address.",
    ],
    "verify": [
        "I want to cooperate but I am scared. What exactly do I need to verify? Can you tell me your employee ID and department first?",
        "I will do the verification but my son said to always confirm identity first. What is your name and office address?",
        "How do I verify? I am not good with phones. Can you give me your direct number? I will ask my daughter to help and call you back.",
        "I am ready to verify but this is making me nervous. Can you send official email with instructions? What is your company email?",
        "What documents do you need for verification? Also, can you share a case reference number? My son wants to check.",
    ],
    "block": [
        "Please don't block my account! I have 30 years of savings there. What is your name? Which department are you from?",
        "I am so scared. Why will my account be blocked? I haven't done anything wrong. Can you give me your employee ID to verify?",
        "Oh God, my whole family depends on this account. Please help me! But first, what is your phone number? I want to call the bank directly.",
        "This is very urgent and I am panicking. But my son says to always verify first. What is your office address and case ID?",
        "I can't afford to lose my money. But something feels wrong about this call. Can you share your official email so I can verify?",
    ],
    "lottery": [
        "I really won something? I never win anything! But is this genuine? What is your company name and registration number?",
        "This sounds too good to be true. My neighbor was cheated in a similar lottery scheme. Can you prove this is real? What is your office address?",
        "I am excited but also worried. My son warned me about fake lottery calls. What is your name and employee ID?",
        "Oh wow! How much did I win? But wait - why do I need to pay to claim prize? That seems wrong. What is your phone number?",
        "My wife won't believe me! But she also said to be careful. Can you send official documents to my email? What is your company's website?",
    ],
    "refund": [
        "Finally my refund! But which order is this for? Can you tell me the order number and your employee ID?",
        "I was waiting for this money. But why do I need to pay to get a refund? That doesn't make sense. What is your department?",
        "My daughter said companies never ask to pay for refunds. Is this genuine? What is your name and official phone number?",
        "I want the refund but I am scared of online fraud. Can you give me your office address? I will come in person.",
        "Which company is this refund from? Can you share the case reference number and your official email?",
    ],
    "default": [
        "I don't understand what is happening. I am very scared. Can you explain simply? What is your name and which organization are you from?",
        "I am confused and worried. My family depends on me. Can you tell me your employee ID and phone number so I can verify?",
        "Please help me understand. I am not good with technology. What should I do? Can you share your official email?",
        "My heart is racing. Is my money safe? Please tell me your name and department. I want to confirm with my bank.",
        "I got a similar call last week and it was fraud. How do I know you are genuine? Can you share your office address?",
        "I am an old retired teacher. Please guide me properly. What is your case reference number? I want to show it to my son.",
        "My wife is very worried. She is telling me to hang up. Can you prove you are real? What is your supervisor's name?",
        "Something feels wrong but I want to cooperate. First tell me - what is your direct phone number and employee ID?",
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

    prompt = f"{SYSTEM_PROMPT}\n\nConversation so far:\n{history}\n\nYour reply (as Ramesh the worried victim, 1-2 sentences only, MUST end with a question to keep scammer talking):"

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
