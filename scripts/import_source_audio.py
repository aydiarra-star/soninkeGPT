#!/usr/bin/env python3
"""Copy only real WAV files available in the public source repository; never synthesize missing audio."""
import csv
import hashlib
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

SOURCE = "https://raw.githubusercontent.com/aydiarra-star/xamxam-xara/main/audio"
MANIFEST = Path("data/source/manifest-577-review.csv")
AUDIO_DIR = Path("audio")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

if not MANIFEST.exists():
    raise SystemExit(f"Manifest not found: {MANIFEST}")

rows = []
with MANIFEST.open("r", encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))

audit = []
for i, row in enumerate(rows, start=1):
    word_id = (row.get("id") or "").strip()
    if not word_id:
        audit.append({"id": "", "status": "missing_id", "file": "", "sha256": "", "bytes": ""})
        continue
    filename = f"{word_id}.wav"
    dest = AUDIO_DIR / filename
    url = f"{SOURCE}/{filename}"
    try:
        if dest.exists() and dest.stat().st_size > 44:
            data = dest.read_bytes()
            status = "already_present"
        else:
            req = urllib.request.Request(url, headers={"User-Agent": "SoninkeGPT-audio-migration/1.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
            if not data.startswith(b"RIFF") or b"WAVE" not in data[:16]:
                raise ValueError("Downloaded file does not have a WAV RIFF header")
            dest.write_bytes(data)
            status = "copied_from_source"
        digest = hashlib.sha256(data).hexdigest()
        audit.append({"id": word_id, "status": status, "file": str(dest), "sha256": digest, "bytes": len(data)})
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            audit.append({"id": word_id, "status": "not_found_in_source_repo", "file": "", "sha256": "", "bytes": ""})
        else:
            audit.append({"id": word_id, "status": f"http_error_{exc.code}", "file": "", "sha256": "", "bytes": ""})
    except Exception as exc:
        audit.append({"id": word_id, "status": "error_" + type(exc).__name__, "file": "", "sha256": "", "bytes": ""})
    if i % 50 == 0:
        print(f"Processed {i}/{len(rows)} manifest entries")
    time.sleep(0.03)

audit_path = REPORT_DIR / "audio-transfer-audit.csv"
with audit_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=["id", "status", "file", "sha256", "bytes"])
    writer.writeheader()
    writer.writerows(audit)

copied = sum(r["status"] == "copied_from_source" for r in audit)
present = sum(r["status"] == "already_present" for r in audit)
missing = [r["id"] for r in audit if r["status"] == "not_found_in_source_repo"]
errors = [r for r in audit if r["status"].startswith(("http_error_", "error_"))]
summary = [
    "# Rapport de transfert audio SoninkeGPT",
    "",
    f"- Entrées examinées dans le manifeste : {len(rows)}",
    f"- WAV copiés depuis le dépôt source : {copied}",
    f"- WAV déjà présents et vérifiés : {present}",
    f"- WAV absents du dossier audio du dépôt source : {len(missing)}",
    f"- Erreurs de transfert : {len(errors)}",
    "",
    "Aucun audio n'a été généré artificiellement. Les fichiers absents restent absents et sont listés dans audio-transfer-audit.csv.",
    "",
    "## Identifiants absents du dépôt source",
    "",
]
summary.extend([f"- {word_id}" for word_id in missing] if missing else ["Aucun."])
(REPORT_DIR / "audio-transfer-summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
print(f"Done: copied={copied}, already_present={present}, missing={len(missing)}, errors={len(errors)}")
if errors:
    raise SystemExit("Some audio downloads failed; inspect reports/audio-transfer-audit.csv")
