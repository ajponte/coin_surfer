"""Base strategy definition"""
from api.lo

from dataclasses import dataclass

from typing import Dict

@dataclass
class Signal:
    token: str
    signal: float
    direction: str
    metadata: Dict

class BaseStrategy:
    def __init__(self, name: str):
        self._name = name

    def generate_signal(self) -> Signal:
        """Generate trading signals."""
        try:
            for token in MONITORED_TOKENS
        except Exception as e:
            cprint(f"Error generating signals: {str(e)}")
            return None
