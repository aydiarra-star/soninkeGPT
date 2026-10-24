"""SoninkeGPT voice API: audio transcription with a server-side OpenAI key.

The API transcribes audio only. The browser continues to answer from the existing
SoninkeGPT corpus and plays approved reference recordings when available.
"""
from __future__ import annotations

import os
from io import BytesIO
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

APP_NAME = "SoninkeGPT Voice API"
MAX_AUDIO_BYTES = int(os.getenv("MAX_AUDIO_BYTES", str(20 * 1024 * 1024)))
ALLOWED_ORIGINS = [
    origin.strip().rstrip("/")
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "https://aydiarra-star.github.io,http://localhost:8000,http://127.0.0.1:8000",
    ).split(",")
    if origin.strip()
]

app = FastAPI(title=APP_NAME, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/")
def health():
    return {
        "service": APP_NAME,
        "status": "ok",
        "transcription_configured": bool(os.getenv("OPENAI_API_KEY")),
        "note": "La réponse linguistique reste traitée par le corpus SoninkeGPT côté navigateur.",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/process-voice")
async def process_voice(
    file: UploadFile = File(...),
    language: Optional[str] = None,
):
    """Transcribe one recorded utterance; does not invent or translate its meaning."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="La reconnaissance vocale n'est pas configurée : clé API serveur absente.",
        )

    content_type = (file.content_type or "").lower()
    allowed_types = (
        "audio/",
        "video/webm",  # Some browsers label WebM audio as video/webm.
        "application/octet-stream",
    )
    if not any(content_type.startswith(t) for t in allowed_types):
        raise HTTPException(status_code=415, detail="Format audio non pris en charge.")

    data = await file.read(MAX_AUDIO_BYTES + 1)
    if not data:
        raise HTTPException(status_code=400, detail="Le fichier audio est vide.")
    if len(data) > MAX_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="Enregistrement trop volumineux (limite 20 Mo).")

    filename = (file.filename or "soninkegpt-audio.webm").replace("/", "_").replace("\\", "_")
    if not any(filename.lower().endswith(ext) for ext in (".wav", ".mp3", ".mp4", ".m4a", ".webm", ".ogg", ".mpeg", ".mpga")):
        if "mp4" in content_type or "m4a" in content_type:
            filename += ".m4a"
        elif "ogg" in content_type:
            filename += ".ogg"
        elif "wav" in content_type:
            filename += ".wav"
        else:
            filename += ".webm"

    # Prompt is a vocabulary hint only; Whisper may still misrecognize Soninke.
    prompt = (
        "Conversation possible en français ou en soninké. "
        "Termes soninkés à reconnaître si réellement prononcés : "
        "SoninkeGPT, Soninké, Xa wouy Diom, an wouydiom ma, Nawari, "
        "toora nta, oyi waxati, bisimilla, Daga goli, Li taxu. "
        "Transcrire fidèlement, sans traduire ni compléter les mots inaudibles."
    )

    try:
        client = OpenAI(api_key=api_key)
        kwargs = {
            "model": os.getenv("OPENAI_TRANSCRIPTION_MODEL", "whisper-1"),
            "file": (filename, BytesIO(data), content_type or "application/octet-stream"),
            "prompt": prompt,
            "response_format": "json",
        }
        # Leave language unset by default so French/Soninke mixed utterances are not
        # forcibly treated as French. Set TRANSCRIPTION_LANGUAGE=fr only if desired.
        requested_language = language or os.getenv("TRANSCRIPTION_LANGUAGE")
        if requested_language:
            kwargs["language"] = requested_language
        result = client.audio.transcriptions.create(**kwargs)
        transcript = (getattr(result, "text", "") or "").strip()
    except Exception as exc:
        # Avoid returning provider details, request payloads, or secrets to the browser.
        print(f"Transcription provider error: {type(exc).__name__}")
        raise HTTPException(
            status_code=502,
            detail="La transcription a échoué. Réessayez ou saisissez votre phrase au clavier.",
        ) from None

    return {
        "text": transcript,
        "language_hint": requested_language if (requested_language := (language or os.getenv("TRANSCRIPTION_LANGUAGE"))) else "auto",
        "transcribed": bool(transcript),
        "warning": "La reconnaissance du soninké peut être imparfaite : vérifiez le texte avant de l'envoyer.",
    }
