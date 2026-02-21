# Honeypot API — Agentic Scam Detection & Intelligence Extraction

AI-powered honeypot that detects scams, engages scammers using a believable victim persona, and extracts actionable intelligence.

## Description

This system acts as a smart scam trap that:
- **Detects** scam messages using keyword-based pattern matching across 40+ fraud indicators
- **Engages** scammers with an emotional, confused victim persona (powered by Google Gemini 2.0 Flash)
- **Extracts** intelligence: phone numbers, UPI IDs, bank accounts, emails, phishing links
- **Reports** accumulated intelligence to the evaluation endpoint after every conversation turn

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI with Uvicorn ASGI server
- **AI/LLM**: Google Gemini 2.0 Flash (4-key rotation for high availability)
- **Deployment**: Hugging Face Spaces (Docker)
- **Libraries**: Pydantic (validation), Requests (HTTP), python-dotenv (config)

## Architecture

```
Request → Authentication → Scam Detector → AI Agent → Intelligence Extractor → GUVI Callback
                              ↓                ↓              ↓
                        Keyword Matching   Gemini LLM    Regex Patterns
                                          (with fallback)
```

### Module Structure

| Module | Purpose |
|--------|---------|
| `app.py` | FastAPI application, request validation, routing, security |
| `scam_detector.py` | Keyword-based scam detection across 10+ fraud categories |
| `agent.py` | Agent bridge — connects LLM responses to the API |
| `llm.py` | Gemini integration with 4-key rotation + 50+ rule-based fallbacks |
| `extractor.py` | Regex-based intelligence extraction (phone, UPI, bank, email, links) |
| `memory.py` | Per-session state management, red flag detection, scam classification |
| `callback.py` | GUVI evaluation endpoint integration with retry logic |
| `decision.py` | Callback timing strategy (sends every turn for reliability) |

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/AKASHDHARDUBEY/Agentic-Honey-Pot-for-Scam-Detection.git
   cd Agentic-Honey-Pot-for-Scam-Detection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   python app.py
   # or
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

## API Endpoint

- **URL**: `https://akashdhar-honeypot-api.hf.space/honeypot`
- **Method**: POST
- **Authentication**: `x-api-key` header

### Request Format
```json
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "URGENT: Your account is blocked...",
    "timestamp": "2025-02-11T10:30:00Z"
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
  "reply": "I am very scared. My bank never calls like this. What is your employee ID?"
}
```

## Approach

### Scam Detection Strategy
- **40+ keywords** across categories: banking fraud, UPI, phishing, lottery, OTP theft, KYC, insurance
- Case-insensitive matching with generic patterns (not hardcoded to specific tests)

### Intelligence Extraction
- **Regex-based** extraction for: phone numbers (Indian +91 format), UPI IDs, bank accounts, email addresses, phishing links
- Compiled regex patterns for efficient repeated matching
- Cumulative merging across all conversation turns

### Engagement Strategy (Victim Persona)
- **Persona**: "Ramesh" — a 55-year-old retired teacher, emotional, confused, not tech-savvy
- **Red flag surfacing**: Every response mentions suspicious elements naturally
- **Investigative questions**: Probes for employee ID, phone, email, office address, case numbers
- **Family references**: "My son told me...", "My wife is worried..."
- **Emotional tone**: "I am very scared", "Please help me"

### Conversation Quality Maximization
- **8 response categories** with 50+ unique responses
- Session-tracked response cycling prevents repetition
- Each response ends with a question to maintain engagement
- Layered strategy: Gemini LLM → Rule-based fallback

### LLM Integration
- **Google Gemini 2.0 Flash** with 4-key rotation
- Automatic failover: Key 1 → Key 2 → Key 3 → Key 4 → Rule-based fallback
- Custom system prompt designed for investigation and engagement

## Security

- API key authentication on all endpoints
- Input validation via Pydantic field validators
- Message length limits (5000 characters)
- Exception handling throughout (no crash scenarios)
- Environment variables for all secrets (`.env.example` provided)
