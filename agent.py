from llm import generate_llm_reply

def generate_agent_reply(history: str, session_id: str = "default") -> str:
    return generate_llm_reply(history, session_id)
