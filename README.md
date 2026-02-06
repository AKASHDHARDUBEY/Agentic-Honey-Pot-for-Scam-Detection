---
title: Honeypot Api
emoji: 🛡️
colorFrom: blue
colorTo: gray
sdk: docker
pinned: false
---

# Agentic Honey-Pot API

AI-powered scam detection and intelligence extraction system for the GUVI Hackathon.

## Features

- **Scam Detection**: Detects scam intent using keyword analysis
- **AI Agent**: Maintains believable human persona to engage scammers
- **Intelligence Extraction**: Extracts UPI IDs, bank accounts, phishing links, phone numbers
- **Multi-turn Memory**: Tracks conversation history across requests
- **Auto Callback**: Sends extracted intelligence to GUVI evaluation endpoint

## API Endpoint

```
POST /honeypot
Header: x-api-key: YOUR_API_KEY
```

## Response Format

```json
{
  "status": "success",
  "reply": "Why is my account being suspended?"
}
```
