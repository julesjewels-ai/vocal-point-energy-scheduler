"""
FastAPI server for VocalPoint audio analysis.

Provides a REST API for uploading audio files and receiving energy analysis.
"""

import os
import tempfile
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.gemini_client import GeminiAudioClient, EnergyResponse

app = FastAPI(
    title="VocalPoint API",
    description="AI-powered energy analysis from voice recordings",
    version="0.1.0"
)

# Enable CORS for PWA frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client
gemini_client = None


def get_client() -> GeminiAudioClient:
    """Lazy initialization of Gemini client."""
    global gemini_client
    if gemini_client is None:
        gemini_client = GeminiAudioClient()
    return gemini_client


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/analyze", response_model=EnergyResponse)
async def analyze_audio(file: UploadFile):
    """Analyze an audio file for energy level.

    Args:
        file: Audio file upload (WebM, MP3, WAV, etc.)

    Returns:
        EnergyResponse with energy_level, confidence, and indicators.
    """
    # Validate file type
    allowed_types = ["audio/webm", "audio/mpeg", "audio/wav", "audio/mp3", "audio/ogg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format: {file.content_type}. Supported: {allowed_types}"
        )

    # Save uploaded file temporarily
    suffix = os.path.splitext(file.filename)[1] or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Analyze with Gemini
        client = get_client()
        result = client.analyze_energy(tmp_path)
        return result
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
