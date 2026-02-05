# Agentic Honey-Pot API

AI-powered scam detection and intelligence extraction system for the GUVI Hackathon.

## Features

- **Scam Detection**: Detects scam intent using keyword analysis
- **AI Agent**: Maintains believable human persona to engage scammers  
- **Intelligence Extraction**: Extracts UPI IDs, bank accounts, phishing links, phone numbers
- **Multi-turn Memory**: Tracks conversation history across requests
- **Auto Callback**: Sends extracted intelligence to GUVI evaluation endpoint

## Quick Start

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Configure Environment
Edit `.env` file:
```
API_KEY=honeypot123
GEMINI_KEY=your_gemini_api_key_here
```

### 3. Run Server
```bash
python3 app.py
```
Server runs at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /
```

### Honeypot Endpoint
```
POST /honeypot
Header: x-api-key: honeypot123
```

**Request Body:**
```json
{
  "sessionId": "abc123",
  "message": {
    "sender": "scammer",
    "text": "Your account will be blocked. Share UPI.",
    "timestamp": 1234567890
  },
  "conversationHistory": []
}
```

**Response:**
```json
{
  "status": "success",
  "reply": "Oh no! Why will my account be blocked?"
}
```

## Deployment

### Render
1. Push to GitHub
2. Connect repo to Render
3. Set environment variables in Render dashboard
4. Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Submission
- **URL**: `https://your-app.onrender.com/honeypot`
- **API Key**: `honeypot123`

## Project Structure
```
├── app.py           # Main FastAPI application
├── scam_detector.py # Scam intent detection
├── extractor.py     # Intelligence extraction (UPI, bank, URLs)
├── memory.py        # Multi-turn conversation memory
├── llm.py           # Gemini LLM integration
├── agent.py         # AI agent wrapper
├── decision.py      # Callback trigger logic
├── callback.py      # GUVI callback sender
├── requirements.txt # Dependencies
├── render.yaml      # Render deployment config
└── Procfile         # Process file for deployment
```
