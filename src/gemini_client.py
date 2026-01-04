"""
Gemini Audio Client for VocalPoint Energy Analysis.

Uses Gemini 3 to analyze raw audio for vocal biomarkers:
- Tone (positive, neutral, negative)
- Pace (fast, normal, slow)
- Emotion (excited, calm, tired, stressed, anxious)
- Non-speech cues (laughter, sighs, hesitation)
"""

import os
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List


class EnergyIndicators(BaseModel):
    """Detailed breakdown of energy indicators detected in audio."""
    tone: str
    pace: str
    emotion: str
    non_speech_cues: List[str]


class EnergyResponse(BaseModel):
    """Structured response for energy analysis."""
    energy_level: str  # "high", "medium", "low"
    confidence: float
    indicators: EnergyIndicators


class GeminiAudioClient:
    """Client for analyzing audio files with Gemini."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"

    def analyze_energy(self, audio_path: str) -> EnergyResponse:
        """Analyzes audio for energy level using Gemini.

        Args:
            audio_path: Path to audio file (WebM, MP3, WAV, etc.)

        Returns:
            EnergyResponse with energy_level, confidence, and indicators.
        """
        # Read audio file
        with open(audio_path, 'rb') as f:
            audio_bytes = f.read()

        prompt = """Analyze this audio recording for the speaker's energy level.

Evaluate the following vocal biomarkers:
- Tone: Is it positive, neutral, or negative?
- Pace: Is the speaker talking fast, normal, or slow?
- Emotion: What emotion is present? (excited, calm, tired, stressed, anxious, happy, sad)
- Non-speech cues: Are there any sighs, laughter, hesitation, yawning, or other non-verbal sounds?

Based on your analysis, determine the overall energy level:
- "high": Speaker sounds energetic, excited, or highly engaged
- "medium": Speaker sounds neutral, calm, or moderately engaged
- "low": Speaker sounds tired, drained, stressed, or disengaged

Return your analysis as JSON with this exact structure:
{
  "energy_level": "high" or "medium" or "low",
  "confidence": 0.0 to 1.0,
  "indicators": {
    "tone": "description",
    "pace": "description",
    "emotion": "description",
    "non_speech_cues": ["list", "of", "cues"]
  }
}"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type='audio/webm',
                )
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        return EnergyResponse.model_validate_json(response.text)
