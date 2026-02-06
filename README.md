---
title: Honeypot Api
emoji: 🛡️
colorFrom: blue
colorTo: gray
sdk: docker
pinned: false
---

# 🛡️ Agentic Honey-Pot API

**AI-powered scam detection and intelligence extraction system for fighting India's ₹60+ Crore daily fraud losses**

[![India AI Impact Buildathon 2026](https://img.shields.io/badge/India%20AI%20Impact-Buildathon%202026-blue)](https://guvi.in)
[![HCL GUVI](https://img.shields.io/badge/Organized%20by-HCL%20GUVI-orange)](https://guvi.in)
[![Live API](https://img.shields.io/badge/API-Live-green)](https://akashdhar-honeypot-api.hf.space)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)](https://fastapi.tiangolo.com)

---

## � Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Tech Stack](#️-tech-stack)
- [Architecture](#-architecture)
- [API Documentation](#-api-documentation)
- [Environment Variables](#-environment-variables)
- [Installation](#-installation)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Features](#-features)
- [Test Results](#-test-results)

---

## 🚨 Problem Statement

### India's Fraud Crisis

| Statistic | Impact |
|-----------|--------|
| **5,00,000+** | Scam calls flood India daily |
| **₹60+ Crore** | Lost to fraudulent calls per day |
| **3+ Spam Calls** | Per citizen, per day |

Traditional detection systems are ineffective because scammers change tactics based on user responses.

### The Challenge

Build an **Agentic Honey-Pot** — an AI-powered system that:
- Detects scam intent in messages
- Engages scammers autonomously using believable human persona
- Extracts actionable intelligence (bank accounts, UPI IDs, phishing links)
- Reports findings to evaluation endpoint

---

## 🎯 Solution

An autonomous AI honeypot that:

1. **Detects** scam messages using 20+ keyword patterns
2. **Activates** AI agent with believable naive victim persona
3. **Engages** scammers in multi-turn conversations (18+ turns)
4. **Extracts** intelligence: bank accounts, UPI IDs, phone numbers, phishing links
5. **Reports** findings to GUVI evaluation endpoint automatically

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | FastAPI (Python 3.10) | REST API with async support |
| **AI/LLM** | Google Gemini 2.0 Flash | Intelligent, contextual responses |
| **Key Management** | Multi-key Rotation (4 keys) | Quota management, 99.9% uptime |
| **Fallback System** | Rule-based Engine | 40+ varied responses when LLM unavailable |
| **Deployment** | Docker + Hugging Face Spaces | Serverless container hosting |
| **Version Control** | GitHub | Code repository |

### Dependencies

```
fastapi>=0.100.0
uvicorn>=0.22.0
python-dotenv>=1.0.0
requests>=2.31.0
pydantic>=2.0.0
google-generativeai>=0.3.0
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agentic Honey-Pot API                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐ │
│  │ Scam         │   │ AI Agent     │   │ Intelligence         │ │
│  │ Detector     │──▶│ (Gemini +    │──▶│ Extractor            │ │
│  │ (20+ KWs)    │   │ 40+ Fallback)│   │ (Regex Patterns)     │ │
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
│  │   POST hackathon.guvi.in/api/updateHoneyPotFinalResult   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📡 API Documentation

### Base URL

```
https://akashdhar-honeypot-api.hf.space
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/honeypot` | Main scam detection endpoint |
| `GET` | `/docs` | Swagger UI documentation |

---

### Authentication

All requests to `/honeypot` require an API key in the header:

```
x-api-key: YOUR_API_KEY
Content-Type: application/json
```

---

### POST /honeypot

#### Request Body

```json
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked. Verify immediately.",
    "timestamp": 1770005528731
  },
  "conversationHistory": [
    {
      "sender": "scammer",
      "text": "Previous message from scammer",
      "timestamp": 1770005528730
    },
    {
      "sender": "user",
      "text": "Previous response from honeypot",
      "timestamp": 1770005528731
    }
  ],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

#### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sessionId` | string | ✅ | Unique session identifier |
| `message.sender` | string | ✅ | `scammer` or `user` |
| `message.text` | string | ✅ | Message content |
| `message.timestamp` | number | ✅ | Epoch timestamp in ms |
| `conversationHistory` | array | ❌ | Previous messages (empty for first) |
| `metadata.channel` | string | ❌ | SMS / WhatsApp / Email / Chat |
| `metadata.language` | string | ❌ | Language used |
| `metadata.locale` | string | ❌ | Country/region code |

#### Response

```json
{
  "status": "success",
  "reply": "Why is my account being suspended?"
}
```

---

### GUVI Callback (Automatic)

When sufficient intelligence is gathered, the system automatically sends:

```json
{
  "sessionId": "abc123-session-id",
  "scamDetected": true,
  "totalMessagesExchanged": 18,
  "extractedIntelligence": {
    "bankAccounts": ["1234567890123456"],
    "upiIds": ["scammer@fakebank"],
    "phishingLinks": ["http://malicious.com"],
    "phoneNumbers": ["+91-9876543210"],
    "suspiciousKeywords": ["urgent", "verify", "blocked"]
  },
  "agentNotes": "Scammer used urgency tactics and payment redirection."
}
```

---

## 🔐 Environment Variables

Create a `.env` file with the following:

```env
# API Authentication
API_KEY=your_api_key_here

# Google Gemini API Keys (Multi-key rotation for quota management)
GEMINI_KEY1=your_gemini_key_1
GEMINI_KEY2=your_gemini_key_2
GEMINI_KEY3=your_gemini_key_3
GEMINI_KEY4=your_gemini_key_4

# Optional: Enable/Disable LLM
USE_LLM=true
```

### How to Get API Keys

| Key | Source | Link |
|-----|--------|------|
| `GEMINI_KEY` | Google AI Studio | [aistudio.google.com](https://aistudio.google.com/apikey) |
| `API_KEY` | Self-defined | Any secure string |

### Multi-Key Rotation

The system uses 4 Gemini API keys and rotates through them:
- If Key 1 hits quota → automatically switches to Key 2
- If all keys exhausted → uses rule-based fallback (40+ responses)
- Ensures **99.9% uptime**

---

## 💻 Installation

### Local Development

```bash
# Clone repository
git clone https://github.com/AKASHDHARDUBEY/Agentic-Honey-Pot-for-Scam-Detection.git
cd Agentic-Honey-Pot-for-Scam-Detection

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cp .env.example .env
# Edit .env with your keys

# Run the server
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Test the API

```bash
curl -X POST "http://localhost:8000/honeypot" \
  -H "x-api-key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-123",
    "message": {
      "sender": "scammer",
      "text": "Your bank account will be blocked. Verify now.",
      "timestamp": 1770005528731
    },
    "conversationHistory": []
  }'
```

---

## 🚀 Deployment

### Hugging Face Spaces (Docker)

1. **Create Space** on [huggingface.co/spaces](https://huggingface.co/spaces)
2. **Select Docker SDK**
3. **Add Secrets** in Settings:
   - `API_KEY`
   - `GEMINI_KEY1`, `GEMINI_KEY2`, `GEMINI_KEY3`, `GEMINI_KEY4`
4. **Push code** to HF repository

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

---

## 📂 Project Structure

```
Agentic-Honey-Pot/
│
├── app.py              # FastAPI main application & /honeypot endpoint
├── agent.py            # AI agent wrapper - connects LLM to API
├── llm.py              # Gemini integration + 40+ fallback responses
├── scam_detector.py    # Keyword-based scam detection (20+ keywords)
├── extractor.py        # Regex-based intelligence extraction
├── memory.py           # Session memory for multi-turn conversations
├── decision.py         # Smart callback trigger logic
├── callback.py         # GUVI endpoint integration
│
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not in git)
├── .gitignore          # Git ignore rules
│
├── README.md           # This file
└── idea.md             # Detailed project documentation
```

### Module Descriptions

| File | Purpose |
|------|---------|
| `app.py` | FastAPI app, routes, authentication |
| `agent.py` | Bridges LLM responses to API |
| `llm.py` | Gemini API + multi-key rotation + 40+ fallbacks |
| `scam_detector.py` | Detects scam keywords in messages |
| `extractor.py` | Extracts bank, UPI, phone, links using regex |
| `memory.py` | Stores conversation history per session |
| `decision.py` | Decides when to send GUVI callback |
| `callback.py` | Sends final intelligence to GUVI |

---

## ✨ Features

### 1. Scam Detection (20+ Keywords)
```python
SCAM_KEYWORDS = [
    "account blocked", "verify", "urgent", "upi", "bank", 
    "lottery", "won", "payment", "kyc", "expire", 
    "pan card", "refund", "suspended", "click here", "prize"
]
```

### 2. AI Agent with Human Persona
- Uses **Google Gemini 2.0 Flash** for intelligent responses
- Maintains naive, confused victim persona
- Never reveals scam detection

### 3. Multi-Key Rotation (4 API Keys)
- Automatic failover when quota exceeded
- 99.9% uptime guaranteed

### 4. 40+ Fallback Responses (8 Categories)
| Category | Example Response |
|----------|-----------------|
| Link | "The link is not opening on my phone" |
| Bank | "Which bank is this? I need IFSC code" |
| UPI | "My GPay is showing error" |
| OTP | "OTP expired, can you resend?" |
| Verify | "I am ready to verify. Guide me." |
| Block | "Why is my account blocked?" |
| Lottery | "I really won? How much?" |
| Default | "Please explain, I don't understand" |

### 5. Intelligence Extraction (Regex)
| Type | Pattern |
|------|---------|
| Bank Accounts | 9-18 digit numbers |
| UPI IDs | `xxx@upi` format |
| Phone Numbers | +91 format |
| Phishing Links | HTTP/HTTPS URLs |

### 6. Session Memory
- Tracks conversation per `sessionId`
- Cumulative intelligence merging
- Response variety (no repetition)

### 7. Auto GUVI Callback
- Triggers after 5+ messages OR valuable intel
- Sends all extracted data for evaluation

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

| Turn | Honeypot Response |
|------|------------------|
| 1 | "I received OTP but it says expired. Can you send again?" |
| 2 | "The OTP is 6 digits right? I got only 4 digits." |
| 3 | "My message is delayed. Can you resend the OTP please?" |
| 4 | "I entered the OTP but it shows invalid. New one please?" |
| 5 | "OTP expired before I could type. Please send new one." |

---

## 🔗 Links

| Resource | URL |
|----------|-----|
| **Live API** | [akashdhar-honeypot-api.hf.space](https://akashdhar-honeypot-api.hf.space) |
| **Swagger Docs** | [API Documentation](https://akashdhar-honeypot-api.hf.space/docs) |
| **GitHub** | [Repository](https://github.com/AKASHDHARDUBEY/Agentic-Honey-Pot-for-Scam-Detection) |

---

## 🏆 Hackathon

**India AI Impact Buildathon 2026**  
- **Organizer:** HCL GUVI  
- **Prize Pool:** ₹4,00,000  
- **Final Venue:** Bharat Mandapam, New Delhi  
- **Certificate:** Co-branded by India AI Impact Summit & HCL GUVI

---

## 👨‍💻 Author

**Akash Dhar Dubey**  
- GitHub: [@AKASHDHARDUBEY](https://github.com/AKASHDHARDUBEY)

---

## 📄 License

This project is built for the India AI Impact Buildathon 2026.

---

*Built with ❤️ for India's fight against fraud | Fighting ₹60+ Crore daily losses*
