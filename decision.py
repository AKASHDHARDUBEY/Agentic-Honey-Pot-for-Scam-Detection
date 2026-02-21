from typing import Dict

def should_send_callback(message_count: int, intelligence: Dict) -> bool:
    if message_count < 2:
        return False
    return True
