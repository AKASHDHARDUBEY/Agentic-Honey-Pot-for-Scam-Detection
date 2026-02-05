from llm import generate_llm_reply

def generate_agent_reply(history: str) -> str:
    return generate_llm_reply(history)
