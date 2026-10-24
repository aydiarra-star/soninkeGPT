#!/usr/bin/env python3
"""Build lexical voice memory and optionally generate missing WAVs with OmniVoice.
Never overwrite authentic recordings; generated files remain unreviewed until human validation.
"""
import argparse
import csv
import hashlib
import json
import re
import unicodedata
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines:
        return []
    delimiter = ";" if ";" in lines[0] else ","
    return list(csv.DictReader(lines, delimiter=delimiter))


def key(text):
    value = str(text or "").replace("ñ", "ɲ").replace("Ñ", "ɲ")
    value = unicodedata.normalize("NFD", value)
    value = "".join(c for c in value if unicodedata.category(c) != "Mn")
    return " ".join(value.replace("’", "'").replace("‘", "'").lower().split())


def valid_wav(path):
    try:
        with wave.open(str(path), "rb") as handle:
            return handle.getnframes() > 0 and handle.getframerate() > 0
    except (wave.Error, EOFError, OSError):
        return False


def build(generate=False, limit=20, device="auto"):
    vocabulary = {}
    translation_columns = (
        "francais", "français", "french", "traduction_fr_confirmee",
        "glose_extraite_automatiquement", "glose_extraite",
        "traductions_projet_existantes",
    )
    for path in sorted((ROOT / "data").rglob("*.csv")):
        for row in rows(path):
            text = next(
                (row.get(column, "").strip() for column in
                 ("soninke", "text", "lemme_corrige", "lemme", "lemme_source")
                 if row.get(column, "").strip()),
                "",
            )
            if not text:
                continue
            # Retire un numéro de ligne au début et les chiffres de désambiguïsation
            # placés à la fin (ex. ba1, ba2, baabo1). Les formes normalisées
            # sont dédupliquées avant génération afin de ne pas prononcer les chiffres.
            text = re.sub(r"^\s*\d+\s*[-.:)]?\s*", "", text).strip()
            text = re.sub(r"\d+$", "", text).strip()
            if not text:
                continue
            french = next(
                (row.get(column, "").strip() for column in translation_columns
                 if row.get(column, "").strip()),
                "",
            )
            entry = vocabulary.setdefault(
                key(text),
                {"text": text, "source": str(path.relative_to(ROOT)), "francais": french},
            )
            if french and not entry.get("francais"):
                entry["francais"] = french

    # Keep greetings and their variants synchronized with the application.
    app = (ROOT / "app.js").read_text(encoding="utf-8")
    if 'const PHRASEBOOK = [' in app:
        phrasebook = app.split("const PHRASEBOOK = [", 1)[1].split("\n];", 1)[0]
        for match in re.finditer(r'snk: "([^"]+)"|alt: \[([^\]]*)\]', phrasebook):
            texts = [match[1]] if match[1] else re.findall(r'"([^"]+)"', match[2])
            for text in texts:
                vocabulary.setdefault(
                    key(text),
                    {"text": text, "source": "app.js:PHRASEBOOK", "francais": ""},
                )

    # Conserve les validations humaines déjà inscrites dans le manifeste précédent.
    previous_memory_path = ROOT / "data/voice-memory.json"
    previous_audio = {}
    if previous_memory_path.exists():
        try:
            previous_memory = json.loads(previous_memory_path.read_text(encoding="utf-8"))
            previous_audio = {
                key(item.get("text", "")): item
                for item in previous_memory.get("audio", [])
                if item.get("text")
            }
        except (json.JSONDecodeError, OSError):
            previous_audio = {}

    audio = {}
    manifest = ROOT / "data/source/manifest-577-review.csv"
    if manifest.exists():
        for row in rows(manifest):
            word = row.get("text", "").strip()
            audio_path = ROOT / "audio" / (row.get("id", "") + ".wav")
            if word and audio_path.exists() and valid_wav(audio_path):
                audio[key(word)] = {
                    "text": word,
                    "url": str(audio_path.relative_to(ROOT)),
                    "kind": "recorded",
                    "francais": "",
                }

    # Préserver les WAV validés des lots importés (ex. audio/lots/lot-100-...).
    # Une reconstruction du manifeste ne doit jamais les faire disparaître.
    for normalized, previous in previous_audio.items():
        if normalized in audio or not previous.get("text") or not previous.get("url"):
            continue
        previous_path = ROOT / str(previous["url"])
        if previous_path.is_file() and valid_wav(previous_path):
            audio[normalized] = dict(previous)

    generated_dir = ROOT / "audio/generated"
    for item in vocabulary.values():
        digest = hashlib.sha256(item["text"].encode("utf-8")).hexdigest()[:24]
        item["url"] = f"audio/generated/{digest}.wav"
        path = ROOT / item["url"]
        if path.exists():
            if valid_wav(path):
                audio.setdefault(key(item["text"]), {**item, "kind": "voice_clone_unreviewed"})
            else:
                # Only generated files are considered here; original audio/ files are untouched.
                path.unlink()

    # Restaure toutes les métadonnées de validation humaine après chaque reconstruction.
    # Ne pas perdre les validations séparées lors d'un nouveau lot de génération.
    validation_fields = (
        "linguistic_validation",
        "pronunciation_validation",
        "translation_validation",
        "validation_batch",
        "validation_date",
        "validated_by",
        "translation_text_missing",
    )
    for normalized, item in audio.items():
        previous = previous_audio.get(normalized)
        if not previous:
            continue
        for field in validation_fields:
            if field in previous:
                item[field] = previous[field]
        if previous.get("kind") == "voice_clone_validated":
            item["kind"] = "voice_clone_validated"

    # Add known French translations to audio entries without overwriting existing translations.
    for normalized, item in vocabulary.items():
        if normalized in audio and item.get("francais") and not audio[normalized].get("francais"):
            audio[normalized]["francais"] = item["francais"]

    pending = [item for normalized, item in sorted(vocabulary.items()) if normalized not in audio]
    if generate and pending:
        import numpy as np
        import soundfile as sf
        import torch
        from omnivoice import OmniVoice

        if device == "auto":
            if torch.cuda.is_available():
                target_device = "cuda:0"
            elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
                target_device = "mps"
            else:
                target_device = "cpu"
        else:
            target_device = device
        if target_device.startswith("cuda") and not torch.cuda.is_available():
            raise RuntimeError("CUDA demandé mais indisponible. Relance avec --device cpu ou --device auto.")
        if target_device == "mps" and not (
            getattr(torch.backends, "mps", None) and torch.backends.mps.is_available()
        ):
            raise RuntimeError("MPS demandé mais indisponible sur cette machine.")

        dtype = torch.float16 if target_device.startswith("cuda") else torch.float32
        print(f"Chargement OmniVoice sur {target_device} ({dtype}) ; le CPU peut être lent.")
        model = OmniVoice.from_pretrained(
            "k2-fsa/OmniVoice", device_map=target_device, dtype=dtype
        )
        language_names = {str(lang).casefold() for lang in model.supported_language_names()}
        language_ids = {str(lang).casefold() for lang in model.supported_language_ids()}
        if not (
            any("sonink" in lang for lang in language_names) or "snk" in language_ids
        ):
            raise RuntimeError(
                "Le modèle ne confirme pas la prise en charge du soninké (snk). "
                "Arrêt sans génération."
            )

        ref_a = ROOT / "audio/snk-00054.wav"
        ref_b = ROOT / "audio/snk-00258.wav"
        for reference_path in (ref_a, ref_b):
            if not valid_wav(reference_path):
                raise FileNotFoundError(
                    f"Référence vocale absente ou WAV invalide : {reference_path}. "
                    "Restaure le fichier original, sans le remplacer par une voix générique."
                )
        a, sample_rate = sf.read(ref_a)
        b, sample_rate_b = sf.read(ref_b)
        if sample_rate != sample_rate_b:
            raise ValueError("Fréquences de référence incompatibles.")
        if a.ndim > 1:
            a = a.mean(axis=1)
        if b.ndim > 1:
            b = b.mean(axis=1)

        generated_dir.mkdir(parents=True, exist_ok=True)
        reference = generated_dir / "reference.wav"
        sf.write(reference, np.concatenate([a, np.zeros(int(0.4 * sample_rate)), b]), sample_rate)

        batch = pending[:max(1, limit)]
        print(
            f"Génération du lot : {len(batch)} mots ; "
            f"{max(0, len(pending) - len(batch))} mots resteront en attente."
        )
        failures = []
        for index, item in enumerate(batch, 1):
            output_path = ROOT / item["url"]
            if output_path.exists() and valid_wav(output_path):
                continue
            if output_path.exists():
                output_path.unlink()
            try:
                result = model.generate(
                    text=item["text"],
                    language="snk",
                    ref_audio=str(reference),
                    ref_text="Daga goli. Li taxu.",
                    num_step=32,
                )
                samples = np.asarray(result[0]).squeeze()
                if samples.ndim != 1 or not samples.size or not np.isfinite(samples).all():
                    raise ValueError("sortie audio vide ou invalide")
                temporary_path = output_path.with_suffix(".tmp.wav")
                sf.write(temporary_path, samples, int(model.sampling_rate), subtype="PCM_16")
                if not valid_wav(temporary_path):
                    temporary_path.unlink(missing_ok=True)
                    raise ValueError("le WAV créé n’a pas passé le contrôle technique")
                temporary_path.replace(output_path)
                print(f"[{index}/{len(batch)}] WAV créé (à écouter) : {item['text']}")
            except Exception as exc:
                failures.append((item["text"], str(exc)))
                print(f"[{index}/{len(batch)}] ÉCHEC — {item['text']}: {exc}")

        if failures:
            report = ROOT / "data/voice-generation-errors.csv"
            with report.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["soninke", "erreur"])
                writer.writerows(failures)
            print(f"{len(failures)} échec(s) consignés dans {report.relative_to(ROOT)}.")
        return build(False, limit, device)

    memory = {
        "model": "k2-fsa/OmniVoice",
        "references": ["audio/snk-00054.wav", "audio/snk-00258.wav"],
        "audio": list(audio.values()),
        "pending": pending,
        "syllables": [],
        "note": "Les clones générés restent non validés jusqu’à écoute humaine. Aucun WAV original n’est écrasé.",
    }
    (ROOT / "data/voice-memory.json").write_text(
        json.dumps(memory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"{len(audio)} WAV indexés ; {len(pending)} formes en attente.")
    return memory


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument(
        "--limit", type=int, default=20,
        help="Nombre maximum de nouveaux WAV à générer par exécution (défaut : 20).",
    )
    parser.add_argument(
        "--device", choices=["auto", "cpu", "cuda", "mps"], default="auto",
        help="Périphérique d’inférence ; auto choisit CUDA, puis MPS, puis CPU.",
    )
    args = parser.parse_args()
    build(args.generate, args.limit, args.device)
