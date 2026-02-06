---
title: Honeypot Api
emoji: 🛡️
colorFrom: blue
colorTo: gray
sdk: docker
pinned: false
---

# 🛡️ Agentic Honey-Pot API

**AI-powered scam detection and intelligence extraction system**

[![India AI Impact Buildathon 2026](https://img.shields.io/badge/India%20AI%20Impact-Buildathon%202026-blue)](https://guvi.in)
[![HCL GUVI](https://img.shields.io/badge/Organized%20by-HCL%20GUVI-orange)](https://guvi.in)
[![Live API](https://img.shields.io/badge/API-Live-green)](https://akashdhar-honeypot-api.hf.space)

---

## 🚨 The Problem

India faces an unprecedented fraud crisis:
- **5,00,000+ scam calls** flood India daily
- **₹60+ Crore lost** to fraudulent calls per day
- **3+ spam calls** per citizen, per day

---

## 🎯 Solution

An autonomous AI honeypot that:
1. **Detects** scam messages in real-time
2. **Engages** scammers using believable human persona
3. **Extracts** intelligence (bank accounts, UPI IDs, phishing links)
4. **Reports** findings for fraud prevention

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI (Python) |
| AI/LLM | Google Gemini 2.0 Flash |
| Deployment | Docker + Hugging Face Spaces |
| Fallback | 40+ rule-based responses |

---

## 📡 API Usage

### Endpoint
```
POST https://akashdhar-honeypot-api.hf.space/honeypot
```

### Headers
```
x-api-key: YOUR_API_KEY
Content-Type: application/json
```

### Request
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

### Response
```json
{
  "status": "success",
  "reply": "Why is my account being suspended?"
}
```

---

## 🔍 Intelligence Extracted

| Type | Example |
|------|---------|
| Bank Accounts | `1234567890123456` |
| UPI IDs | `scammer@fakebank` |
| Phone Numbers | `+91-9876543210` |
| Phishing Links | `http://malicious.com` |
| Keywords | `urgent`, `verify`, `blocked` |

---

## 📂 Project Structure

```
├── app.py           # FastAPI main application
├── agent.py         # AI agent wrapper
├── llm.py           # Gemini LLM + fallback responses
├── scam_detector.py # Keyword-based scam detection
├── extractor.py     # Intelligence extraction
├── memory.py        # Session memory management
├── decision.py      # Smart callback logic
├── callback.py      # GUVI endpoint integration
├── Dockerfile       # Container configuration
└── requirements.txt # Dependencies
```

---

## 🔗 Links

- **Live API:** [akashdhar-honeypot-api.hf.space](https://akashdhar-honeypot-api.hf.space)
- **Swagger Docs:** [API Documentation](https://akashdhar-honeypot-api.hf.space/docs)
- **GitHub:** [Repository](https://github.com/AKASHDHARDUBEY/Agentic-Honey-Pot-for-Scam-Detection)

---

## 🏆 Hackathon

**India AI Impact Buildathon 2026**  
Organized by HCL GUVI | ₹4,00,000 Prize Pool  
Final Venue: Bharat Mandapam, New Delhi

---

*Built with ❤️ for India's fight against fraud*
