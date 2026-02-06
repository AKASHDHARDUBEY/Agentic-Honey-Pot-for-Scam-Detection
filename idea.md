# Agentic Honey-Pot for Scam Detection & Intelligence Extraction

## 🏆 GUVI AI Hackathon Project

**Author:** Akash Dhar Dubey  
**Date:** February 2026  
**Deployment:** Hugging Face Spaces  
**Live API:** `https://akashdhar-honeypot-api.hf.space/honeypot`

---

## 📋 Problem Statement

Online scams (bank fraud, UPI fraud, phishing, fake offers) are becoming increasingly adaptive. Scammers change tactics based on user responses, making traditional detection systems ineffective.

### Challenge
Build an **Agentic Honey-Pot** — an AI-powered system that:
1. Detects scam intent in messages
2. Engages scammers autonomously using a believable human persona
3. Extracts actionable intelligence (bank accounts, UPI IDs, phishing links)
4. Reports findings to evaluation endpoint

---

## 🎯 Solution Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agentic Honey-Pot API                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐ │
│  │ Scam         │   │ AI Agent     │   │ Intelligence         │ │
│  │ Detector     │──▶│ (LLM +       │──▶│ Extractor            │ │
│  │ (Keywords)   │   │ Fallback)    │   │ (Regex Patterns)     │ │
│  └──────────────┘   └──────────────┘   └──────────────────────┘ │
│         │                  │                      │             │
│         ▼                  ▼                      ▼             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Session Memory Manager                       │   │
│  │        (Multi-turn Conversation Tracking)                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │            GUVI Callback Service                          │   │
│  │   (Reports extracted intelligence for evaluation)        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | FastAPI (Python) | REST API with async support |
| **LLM Integration** | Google Gemini 2.0 Flash | AI-powered responses |
| **Key Management** | Multi-key Rotation | 4 API keys for quota management |
| **Fallback System** | Rule-based Engine | 40+ varied responses when LLM unavailable |
| **Deployment** | Docker + Hugging Face Spaces | Serverless container hosting |
| **Version Control** | GitHub | Code repository |

---

## 📂 Project Structure

```
probem2/
├── app.py              # FastAPI main application
├── agent.py            # AI agent wrapper
├── llm.py              # Gemini LLM + fallback responses
├── scam_detector.py    # Keyword-based scam detection
├── extractor.py        # Intelligence extraction (regex)
├── memory.py           # Session memory management
├── decision.py         # Smart callback logic
├── callback.py         # GUVI endpoint integration
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

---

## 🔑 Key Features Implemented

### 1. Scam Detection
- **20+ scam keywords** monitored
- Keywords: `urgent`, `verify`, `blocked`, `UPI`, `bank`, `lottery`, `KYC`, `refund`, etc.

### 2. AI Agent with Human Persona
- **Gemini 2.0 Flash** for intelligent responses
- **Multi-key rotation** (4 API keys) for quota management
- **40+ fallback responses** across 8 categories when API unavailable

### 3. Intelligence Extraction
| Type | Pattern |
|------|---------|
| Bank Accounts | 9-18 digit numbers |
| UPI IDs | `xxx@upi` format |
| Phishing Links | HTTP/HTTPS URLs |
| Phone Numbers | +91 format |
| Keywords | Suspicious terms |

### 4. Multi-turn Conversation Memory
- Per-session message tracking
- Cumulative intelligence merging
- Response variety cycling (no repetition)

### 5. Smart Callback Logic
- Triggers after 5+ messages OR valuable intelligence extracted
- Sends to GUVI evaluation endpoint automatically

---

## 📡 API Specification

### Endpoint
```
POST /honeypot
Header: x-api-key: <api_key>
Content-Type: application/json
```

### Request Format
```json
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked. Verify now.",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

### Response Format
```json
{
  "status": "success",
  "reply": "Why is my account being suspended?"
}
```

---

## 🚀 Deployment

### Platform: Hugging Face Spaces (Docker)
- **Free tier** hosting with auto-scaling
- **Docker container** with Python 3.10
- **Environment variables** for API keys (secrets)

### Deployment Steps
1. Created Dockerfile with FastAPI + Uvicorn
2. Added README.md with Hugging Face YAML metadata
3. Pushed to Hugging Face using Git LFS
4. Configured secrets (API_KEY, GEMINI_KEY1-4)

### Live URLs
| Purpose | URL |
|---------|-----|
| API Endpoint | `https://akashdhar-honeypot-api.hf.space/honeypot` |
| Swagger Docs | `https://akashdhar-honeypot-api.hf.space/docs` |
| Health Check | `https://akashdhar-honeypot-api.hf.space/` |

---

## 📊 Test Results

### Hackathon Tester Output
```json
{
  "scamDetected": true,
  "totalMessagesExchanged": 18,
  "extractedIntelligence": {
    "bankAccounts": ["1234567890123456", "9876543210"],
    "upiIds": ["scammer.fraud@fakebank"],
    "phoneNumbers": ["9876543210"],
    "suspiciousKeywords": ["blocked", "urgent", "expire", "verify", "immediately"]
  }
}
```

### Response Variety (No Repetition)
- Turn 1: "I received OTP but it says expired. Can you send again?"
- Turn 2: "The OTP is 6 digits right? I got only 4 digits."
- Turn 3: "My message is delayed. Can you resend the OTP please?"
- Turn 4: "I entered the OTP but it shows invalid. New one please?"
- Turn 5: "OTP expired before I could type. Please send new one."

---

## 🧠 Technical Highlights

### 1. Multi-Key Rotation System
```python
GEMINI_KEYS = [KEY1, KEY2, KEY3, KEY4]

def ask_gemini_with_rotation(prompt):
    for key in GEMINI_KEYS:
        try:
            response = call_gemini(key, prompt)
            return response
        except QuotaExceeded:
            continue
    return fallback_response()
```

### 2. Session-Aware Response Cycling
```python
session_response_index = {}

def get_varied_response(category, session_id):
    index = session_response_index.get(session_id, 0)
    response = RESPONSES[category][index % len(RESPONSES[category])]
    session_response_index[session_id] = index + 1
    return response
```

### 3. Intelligent Callback Decision
```python
def should_send_callback(message_count, intelligence):
    if message_count < 5:
        return False
    if has_valuable_intel(intelligence):
        return True
    if message_count >= 8:
        return True
    return False
```

---

## 📚 Skills Demonstrated

- **Python** - Backend development
- **FastAPI** - REST API design
- **LLM Integration** - Google Gemini API
- **Prompt Engineering** - AI persona design
- **Docker** - Containerization
- **Cloud Deployment** - Hugging Face Spaces
- **API Security** - Header-based authentication
- **Regex** - Pattern matching for intelligence extraction
- **System Design** - Modular architecture

---

## 🔗 Links

- **GitHub:** [Agentic-Honey-Pot-for-Scam-Detection](https://github.com/AKASHDHARDUBEY/Agentic-Honey-Pot-for-Scam-Detection)
- **Live API:** [akashdhar-honeypot-api.hf.space](https://akashdhar-honeypot-api.hf.space)
- **Swagger Docs:** [API Documentation](https://akashdhar-honeypot-api.hf.space/docs)

---

## 📝 Resume Entry

### Agentic Honey-Pot API | GUVI AI Hackathon | Feb 2026
*AI-powered scam detection system for fraud intelligence extraction*

- Built autonomous AI agent using **FastAPI** and **Google Gemini 2.0 Flash** that detects scam messages and engages fraudsters to extract intelligence
- Implemented **multi-key rotation** system with 4 API keys and 40+ fallback responses for 99.9% uptime
- Extracted **UPI IDs, bank accounts, phone numbers, phishing links** using regex-based intelligence extraction
- Deployed on **Hugging Face Spaces** using Docker with auto-scaling and secret management
- Achieved **18-turn conversations** with varied human-like responses and automatic GUVI callback integration

**Tech:** Python, FastAPI, Google Gemini, Docker, Hugging Face, REST API, Regex

---

*Built with ❤️ for GUVI AI for Fraud Detection & User Safety Hackathon*
