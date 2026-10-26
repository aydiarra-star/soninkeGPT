"""SoninkeGPT voice and conversational API.

Voice transcription is handled server-side. Conversational answers accept explicit
corpus context from the caller; the API does not pretend to search the frontend's
local files, and Soninke forms must retain their supplied validation status.
"""
from __future__ import annotations

import os
from io import BytesIO
from typing import Literal, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

APP_NAME = "SoninkeGPT Voice API"
MAX_AUDIO_BYTES = int(os.getenv("MAX_AUDIO_BYTES", str(20 * 1024 * 1024)))
MAX_CHAT_MESSAGE_CHARS = int(os.getenv("MAX_CHAT_MESSAGE_CHARS", "4000"))
MAX_CHAT_HISTORY_MESSAGES = int(os.getenv("MAX_CHAT_HISTORY_MESSAGES", "20"))
MAX_CORPUS_CONTEXT_CHARS = int(os.getenv("MAX_CORPUS_CONTEXT_CHARS", "12000"))
ALLOWED_ORIGINS = [
    origin.strip().rstrip("/")
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "https://aydiarra-star.github.io,http://localhost:8000,http://127.0.0.1:8000",
    ).split(",")
    if origin.strip()
]

app = FastAPI(title=APP_NAME, version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=MAX_CHAT_MESSAGE_CHARS)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=MAX_CHAT_MESSAGE_CHARS)
    mode: Literal["translation_vocabulary", "culture_history", "general"] = "translation_vocabulary"
    history: list[ChatMessage] = Field(default_factory=list)
    # Caller supplies context retrieved from the validated local corpus.
    corpus_context: str = Field(default="", max_length=MAX_CORPUS_CONTEXT_CHARS)
    # References must be real records returned by the caller's retrieval layer.
    sources: list[dict[str, str]] = Field(default_factory=list, max_length=10)


@app.get("/")
def health():
    return {
        "service": APP_NAME,
        "status": "ok",
        "transcription_configured": bool(os.getenv("OPENAI_API_KEY")),
        "chat_configured": bool(os.getenv("OPENAI_API_KEY")),
        "note": "Le chat utilise uniquement le contexte de corpus explicitement transmis par le client.",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/chat")
def chat(request: ChatRequest):
    """Generate a response using bounded conversation history and caller-provided corpus context."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Le service conversationnel n'est pas configuré : clé API serveur absente.",
        )

    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Le message est vide.")

    if request.mode == "translation_vocabulary":
        mode_instructions = (
            "Tu es l'assistant de vocabulaire et de traduction SoninkeGPT. "
            "Priorise strictement le contexte du corpus fourni. Ne fabrique jamais une forme soninkée, "
            "une traduction, un exemple ou une source. Distingue les formes attestées, les formes à vérifier "
            "et les assemblages indicatifs. Si le contexte ne suffit pas, dis-le en français et demande une "
            "validation humaine. Ne présente jamais une phrase composée comme attestée."
        )
    elif request.mode == "culture_history":
        mode_instructions = (
            "Tu es l'assistant Culture et Histoire de SoninkeGPT. Sépare clairement les informations "
            "appuyées par le contexte fourni des connaissances générales incertaines. N'invente pas de "
            "référence. Si aucune source n'est fournie, indique que les références doivent être vérifiées."
        )
    else:
        mode_instructions = (
            "Tu es l'assistant général de SoninkeGPT. Réponds clairement en français, sauf demande contraire. "
            "N'invente pas de faits ni de références. Pour toute forme soninkée, utilise le contexte fourni "
            "ou signale explicitement l'incertitude."
        )

    context_block = request.corpus_context.strip()
    system_prompt = mode_instructions
    if context_block:
        system_prompt += "\n\nContexte récupéré du corpus local (données, statuts et provenance) :\n" + context_block
    else:
        system_prompt += (
            "\n\nAucun contexte du corpus n'a été fourni pour ce tour. Ne prétends pas avoir consulté "
            "le lexique local et n'affirme pas qu'une forme soninkée est validée."
        )

    # Keep only the most recent bounded history; validate roles and content via Pydantic.
    history = request.history[-MAX_CHAT_HISTORY_MESSAGES:]
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend({"role": item.role, "content": item.content.strip()} for item in history)
    messages.append({"role": "user", "content": user_message})

    try:
        client = OpenAI(api_key=api_key)
        result = client.chat.completions.create(
            model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
            messages=messages,
            temperature=0.2 if request.mode == "translation_vocabulary" else 0.4,
            max_tokens=900,
        )
        answer = (result.choices[0].message.content or "").strip()
    except Exception as exc:
        # Do not leak provider details, prompts, or secrets to the client.
        print(f"Chat provider error: {type(exc).__name__}")
        raise HTTPException(
            status_code=502,
            detail="Le service conversationnel est temporairement indisponible. Réessayez plus tard.",
        ) from None

    return {
        "answer": answer,
        "mode": request.mode,
        "sources": request.sources,
        "corpus_context_used": bool(context_block),
        "degraded": False,
        "warning": (
            None if context_block else
            "Aucun contexte lexical local fourni : les formes soninkées ne sont pas considérées comme validées."
        ),
    }


@app.post("/api/process-voice")
async def process_voice(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    vocabulary: Optional[str] = Form(None),
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

    prompt = (
        "La personne peut parler en soninké, langue à faible représentation dans les systèmes de transcription, ou en français. "
        "Priorité : transcrire les sons prononcés, ne pas traduire en français, ne pas remplacer un mot soninké par un mot français ressemblant. "
        "Exemples de formes soninkées à conserver telles quelles lorsqu’elles sont prononcées : daga goli, baytélé yigi, SoninkeGPT, Soninké, Xa wouy Diom, an wouydiom ma, Nawari, "
        "toora nta, oyi waxati, bisimilla, Daga goli, Li taxu. "
        "Respecter les espaces et les accents entendus. Si un passage est incertain, ne pas inventer de traduction."
    )
    if vocabulary:
        terms = list(dict.fromkeys(term.strip() for term in vocabulary.splitlines() if term.strip()))
        multiword = [term for term in terms if " " in term]
        singleword = [term for term in terms if " " not in term]

        def spread(items, limit):
            if len(items) <= limit:
                return items
            indexes = [round(i * (len(items) - 1) / (limit - 1)) for i in range(limit)]
            return [items[i] for i in indexes]

        selected_terms = spread(multiword, 45) + spread(singleword, 35)
        vocabulary_hint = ", ".join(selected_terms)
        if vocabulary_hint:
            prompt += " Formes du lexique Soninké à privilégier seulement si les sons correspondent : " + vocabulary_hint[:900]

    try:
        client = OpenAI(api_key=api_key)
        kwargs = {
            "model": os.getenv("OPENAI_TRANSCRIPTION_MODEL", "whisper-1"),
            "file": (filename, BytesIO(data), content_type or "application/octet-stream"),
            "prompt": prompt,
            "response_format": "json",
        }
        requested_language = language or os.getenv("TRANSCRIPTION_LANGUAGE")
        if requested_language:
            kwargs["language"] = requested_language
        result = client.audio.transcriptions.create(**kwargs)
        transcript = (getattr(result, "text", "") or "").strip()
    except Exception as exc:
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
