#!/usr/bin/env python3
"""Restore voice-memory.json from a review artifact without inventing or promoting validations.

Only entries whose referenced local WAV exists in the checked-out repository and can be
opened as a non-empty WAV are retained. All per-entry metadata and validation statuses are
preserved verbatim.
"""
from __future__ import annotations

import argparse
import json
import shutil
import wave
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def valid_wav(path: Path) -> bool:
    try:
        with wave.open(str(path), "rb") as handle:
            return (
                handle.getnframes() > 0
                and handle.getframerate() > 0
                and handle.getnchannels() > 0
                and bool(handle.readframes(1))
            )
    except (OSError, EOFError, wave.Error, ValueError):
        return False


def safe_local_path(value: Any) -> Path | None:
    raw = str(value or "").strip()
    if not raw or raw.startswith(("http://", "https://", "/")):
        return None
    path = Path(raw)
    if ".." in path.parts:
        return None
    candidate = (ROOT / path).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def restore(source: Path, destination: Path, artifact_root: Path | None = None) -> dict[str, int]:
    memory = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(memory, dict) or not isinstance(memory.get("audio"), list):
        raise ValueError("La mémoire source doit être un objet JSON contenant une liste 'audio'.")

    retained = []
    missing = 0
    invalid = 0
    files_restored = 0
    for item in memory["audio"]:
        if not isinstance(item, dict):
            missing += 1
            continue
        path = safe_local_path(item.get("url"))
        if path is None:
            missing += 1
            continue
        # Si un WAV référencé manque dans main mais existe dans l'artefact de revue,
        # le restaurer sans écraser un fichier déjà présent et sans changer son statut.
        if not path.is_file() and artifact_root is not None:
            relative = Path(str(item.get("url", "")))
            if relative.is_absolute() or ".." in relative.parts:
                missing += 1
                continue
            artifact_path = (artifact_root / relative).resolve()
            try:
                artifact_path.relative_to(artifact_root.resolve())
            except ValueError:
                missing += 1
                continue
            if artifact_path.is_file() and artifact_path.suffix.lower() == ".wav" and valid_wav(artifact_path):
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(artifact_path, path)
                files_restored += 1
        if not path.is_file():
            missing += 1
            continue
        if path.suffix.lower() != ".wav" or not valid_wav(path):
            invalid += 1
            continue
        # Copie complète de l'entrée : aucune validation ni traduction n'est promue.
        retained.append(item)

    memory["audio"] = retained
    refs = memory.get("references")
    if isinstance(refs, list):
        memory["references"] = [
            ref for ref in refs
            if (path := safe_local_path(ref)) is not None and path.is_file() and valid_wav(path)
        ]

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(memory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    counts: dict[str, int] = {
        "retained": len(retained),
        "missing": missing,
        "invalid": invalid,\n        "files_restored": files_restored,
    }
    for item in retained:
        kind = str(item.get("kind", "kind_missing"))
        counts[kind] = counts.get(kind, 0) + 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--memory-file", required=True, type=Path,
                        help="Chemin du voice-memory.json extrait de l'artefact de revue")
    parser.add_argument("--output", type=Path, default=ROOT / "data/voice-memory.json")\n    parser.add_argument("--artifact-root", type=Path, default=None,\n                        help="Répertoire extrait de l’artefact, utilisé pour restaurer les WAV référencés absents du dépôt")
    args = parser.parse_args()
    counts = restore(args.memory_file, args.output, args.artifact_root)
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    if counts["retained"] == 0:
        raise SystemExit("ÉCHEC : aucune entrée audio ne pointe vers un WAV existant et lisible.")


if __name__ == "__main__":
    main()
