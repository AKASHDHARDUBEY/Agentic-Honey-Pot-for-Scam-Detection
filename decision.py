from typing import Dict

MIN_MESSAGES_FOR_CALLBACK = 5

def should_send_callback(message_count: int, intelligence: Dict) -> bool:
    if message_count < MIN_MESSAGES_FOR_CALLBACK:
        return False
    
    has_valuable_intel = (
        len(intelligence.get("bankAccounts", [])) > 0 or
        len(intelligence.get("upiIds", [])) > 0 or
        len(intelligence.get("phishingLinks", [])) > 0 or
        len(intelligence.get("phoneNumbers", [])) > 0
    )
    
    if has_valuable_intel:
        return True
    
    if message_count >= 8:
        return True
    
    return False
