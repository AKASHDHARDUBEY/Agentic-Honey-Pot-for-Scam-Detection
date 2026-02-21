"""
AI Agent Module
================
Bridges the LLM response generation with the main API application.
Acts as the honeypot agent that generates believable victim responses
to keep scammers engaged while extracting intelligence.

The agent uses a layered response strategy:
1. Google Gemini 2.0 Flash (with 4-key rotation for high availability)
2. Rule-based fallback system with 50+ context-aware responses
"""

import logging
from llm import generate_llm_reply

logger = logging.getLogger("HoneyPot")


def generate_agent_reply(history: str, session_id: str = "default") -> str:
    """
    Generate a believable victim response to keep the scammer engaged.

    Uses the conversation history to generate a contextually appropriate
    response that:
    - Sounds like a real confused victim
    - Asks investigative questions to extract information
    - References red flags naturally (urgency, OTP requests, etc.)
    - Keeps the conversation going for maximum engagement

    Args:
        history: Full conversation history as a formatted string.
        session_id: Session identifier for response variety tracking.

    Returns:
        A victim-persona response string designed to elicit more
        information from the scammer.
    """
    try:
        if not history:
            return "Hello? I got your message. What is this about? Can you tell me your name?"

        reply = generate_llm_reply(history, session_id)

        # Ensure the reply is not empty
        if not reply or not reply.strip():
            logger.warning(f"Empty reply generated for session {session_id}")
            return "I am confused. Can you explain again? What is your name and department?"

        return reply.strip()

    except Exception as e:
        logger.error(f"Agent reply generation failed for session {session_id}: {e}")
        return "I am having trouble understanding. Can you please tell me your name and what this is about?"
