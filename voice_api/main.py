"""SoninkeGPT voice and conversational API.

Voice transcription is handled server-side. Conversational answers accept explicit
corpus context from the caller; the API does not pretend to search the frontend's
local files, and Soninke forms must retain their supplied validation status.
"""
from __future__ import annotations

import os
import json
import urllib.parse
import urllib.request
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
    history: list[ChatMessage] = Field(default_factory=list, max_length=MAX_CHAT_HISTORY_MESSAGES)
    # Caller supplies context retrieved from the validated local corpus.
    corpus_context: str = Field(default="", max_length=MAX_CORPUS_CONTEXT_CHARS)
    # References must be real records returned by the caller's retrieval layer.
    sources: list[dict[str, str]] = Field(default_factory=list, max_length=10)
    web_search: bool = False


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

    web_sources: list[dict[str, str]] = []
    search_warning = None
    provider_used = None
    def post_json(url: str, payload: dict, headers: dict[str, str], timeout: int = 25) -> dict:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={**headers, "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    if request.web_search:
        try:
            tavily_key = os.getenv("TAVILY_API_KEY")
            brave_key = os.getenv("BRAVE_SEARCH_API_KEY")
            if tavily_key:
                search_result = post_json("https://api.tavily.com/search", {"api_key": tavily_key, "query": user_message, "search_depth": "basic", "max_results": 5, "include_answer": False}, {}, timeout=15)
                for item in search_result.get("results", []):
                    url = str(item.get("url", ""))
                    if url.startswith(("https://", "http://")): web_sources.append({"url": url, "title": str(item.get("title") or url), "snippet": str(item.get("content") or "")[:1200]})
            elif brave_key:
                query = urllib.parse.urlencode({"q": user_message, "count": 5})
                req = urllib.request.Request("https://api.search.brave.com/res/v1/web/search?" + query, headers={"Accept": "application/json", "X-Subscription-Token": brave_key})
                with urllib.request.urlopen(req, timeout=15) as response: search_result = json.loads(response.read().decode("utf-8"))
                for item in search_result.get("web", {}).get("results", []):
                    url = str(item.get("url", ""))
                    if url.startswith(("https://", "http://")): web_sources.append({"url": url, "title": str(item.get("title") or url), "snippet": str(item.get("description") or "")[:1200]})
            else: search_warning = "Recherche Web non configurée : ajoutez TAVILY_API_KEY ou BRAVE_SEARCH_API_KEY dans Render."
        except Exception as exc:
            print(f"Web search provider error: {type(exc).__name__}")
            search_warning = "La recherche Web a échoué ; les faits ne sont pas vérifiés par des sources Web."
    augmented_system_prompt = system_prompt
    if web_sources:
        augmented_system_prompt += "\n\nRésultats Web externes (ne validant pas la langue soninkée) :\n"
        for idx, source in enumerate(web_sources, start=1):
            augmented_system_prompt += "[" + str(idx) + "] " + source["title"] + " — " + source["url"] + "\n" + source.get("snippet", "") + "\n"
        augmented_system_prompt += "\nCite les URL exactes. Distingue faits, interprétations et incertitudes. Une source Web ne valide jamais une forme soninkée."
    messages = [{"role": "system", "content": augmented_system_prompt}]
    messages.extend({"role": item.role, "content": item.content.strip()} for item in history)
    messages.append({"role": "user", "content": user_message})
    failures = []
    provider_used = None
    answer = ""
    openai_key = os.getenv("OPENAI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if openai_key:
        try:
            client = OpenAI(api_key=openai_key)
            result = client.chat.completions.create(model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"), messages=messages, temperature=0.2 if request.mode == "translation_vocabulary" else 0.4, max_tokens=900)
            answer = (result.choices[0].message.content or "").strip()
            if answer: provider_used = "openai"
        except Exception as exc:
            failures.append(type(exc).__name__); print(f"Primary chat provider error: {type(exc).__name__}")
    if not answer and groq_key:
        try:
            result = post_json("https://api.groq.com/openai/v1/chat/completions", {"model": os.getenv("GROQ_CHAT_MODEL", "llama-3.3-70b-versatile"), "messages": messages, "temperature": 0.2 if request.mode == "translation_vocabulary" else 0.4, "max_tokens": 900}, {"Authorization": "Bearer " + groq_key})
            answer = str(result["choices"][0]["message"].get("content") or "").strip()
            if answer: provider_used = "groq"
        except Exception as exc:
            failures.append(type(exc).__name__); print(f"Groq fallback error: {type(exc).__name__}")
    if not answer and openrouter_key:
        try:
            result = post_json("https://openrouter.ai/api/v1/chat/completions", {"model": os.getenv("OPENROUTER_CHAT_MODEL", "meta-llama/llama-3.3-70b-instruct:free"), "messages": messages, "temperature": 0.2 if request.mode == "translation_vocabulary" else 0.4, "max_tokens": 900}, {"Authorization": "Bearer " + openrouter_key, "HTTP-Referer": "https://aydiarra-star.github.io/soninkeGPT/", "X-Title": "SoninkeGPT"})
            answer = str(result["choices"][0]["message"].get("content") or "").strip()
            if answer: provider_used = "openrouter"
        except Exception as exc:
            failures.append(type(exc).__name__); print(f"OpenRouter fallback error: {type(exc).__name__}")
    if not answer:
        if not (openai_key or groq_key or openrouter_key): raise HTTPException(status_code=503, detail="Aucune clé API configurée. Ajoutez OPENAI_API_KEY, GROQ_API_KEY ou OPENROUTER_API_KEY dans Render.")
        raise HTTPException(status_code=503, detail="Aucun fournisseur n’a pu répondre. Vérifiez les clés API et quotas dans Render.")
    if request.web_search and not web_sources and not search_warning: search_warning = "Aucune source Web récupérée ; les faits doivent être vérifiés."

    return {
        "answer": answer,
        "mode": request.mode,
        "sources": request.sources,
        "web_sources": web_sources,
        "web_search_requested": request.web_search,
        "provider_used": provider_used,
        "corpus_context_used": bool(context_block),
        "degraded": bool(failures or search_warning),
        "warning": " ".join(part for part in [None if context_block else "Aucun contexte lexical local fourni : les formes soninkées ne sont pas considérées comme validées.", search_warning, "Un fournisseur de secours a été utilisé après une erreur du fournisseur principal." if failures else None] if part),
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
