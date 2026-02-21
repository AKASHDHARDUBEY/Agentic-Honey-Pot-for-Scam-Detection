"""
Callback Decision Logic
========================
Determines when to send the final intelligence callback to the
GUVI evaluation endpoint.

Strategy: Send callback on EVERY turn to ensure the evaluator
always receives the latest accumulated intelligence. The evaluation
system waits 10 seconds after the last conversation turn for the
final submission — by sending every turn, we guarantee the most
complete data is always available.
"""

from typing import Dict


def should_send_callback(message_count: int, intelligence: Dict) -> bool:
    """
    Determine whether to send the intelligence callback.

    Returns True on every turn to ensure the evaluator always has
    the latest intelligence data. This is critical because the
    evaluation system only considers the last callback received.

    Args:
        message_count: Total messages in the conversation so far.
        intelligence: Current accumulated intelligence dictionary.

    Returns:
        Always True — callback is sent on every turn for reliability.
    """
    return True
