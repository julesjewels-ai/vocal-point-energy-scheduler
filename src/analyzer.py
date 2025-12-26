from typing import Dict, Any
from src.domain import EnergyLevel
from src.interfaces import IEnergyAnalyzer

class EnergyAnalyzer(IEnergyAnalyzer):
    def __init__(self):
        # In a real app, this would load models
        pass

    def analyze(self, text: str, metrics: Dict[str, Any] = None) -> EnergyLevel:
        """
        Analyze text and vocal metrics to determine energy level.

        Args:
            text: The transcribed text from the user.
            metrics: Optional dictionary containing vocal metrics (e.g., 'pace', 'tone_valence').
                     pace: words per minute (normal ~130-150)
                     tone_valence: -1.0 to 1.0 (negative to positive emotion)
        """
        metrics = metrics or {}

        # Simple heuristic analysis
        score = 0

        # Text based heuristics
        text_lower = text.lower()
        high_energy_keywords = ['excited', 'ready', 'focused', 'great', 'pumped', 'energetic']
        low_energy_keywords = ['tired', 'exhausted', 'drained', 'sleepy', 'slow', 'sick']

        for word in high_energy_keywords:
            if word in text_lower:
                score += 2

        for word in low_energy_keywords:
            if word in text_lower:
                score -= 2

        # Metric based heuristics
        pace = metrics.get('pace')
        if pace:
            if pace > 160: # Fast talking
                score += 1
            elif pace < 110: # Slow talking
                score -= 1

        tone = metrics.get('tone_valence')
        if tone:
            if tone > 0.5:
                score += 1
            elif tone < -0.5:
                score -= 1

        # Determine level
        if score >= 2:
            return EnergyLevel.HIGH
        elif score <= -2:
            return EnergyLevel.LOW
        else:
            return EnergyLevel.MEDIUM
