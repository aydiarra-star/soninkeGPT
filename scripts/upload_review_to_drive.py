#!/usr/bin/env python3
"""Upload generated, unreviewed Soninke WAVs and manifest to a Drive review folder.

Requires GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON and GOOGLE_DRIVE_REVIEW_FOLDER_ID.
Existing WAV files in the destination folder are never overwritten.
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    raw_credentials = os.environ.get("GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON", "").strip()
    folder_id = os.environ.get("GOOGLE_DRIVE_REVIEW_FOLDER_ID", "").strip()
    if not raw_credentials or not folder_id:
        print("Google Drive not configured; review files remain available as a GitHub Actions artifact.")
        return 0

    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    credentials = Credentials.from_service_account_info(
        json.loads(raw_credentials),
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    drive = build("drive", "v3", credentials=credentials, cache_discovery=False)

    def find_existing(name):
        escaped = name.replace("\\", "\\\\").replace("'", "\\'")
        result = drive.files().list(
            q=f"name = '{escaped}' and '{folder_id}' in parents and trashed = false",
            fields="files(id,name)",
            pageSize=100,
        ).execute()
        return result.get("files", [])

    generated_dir = ROOT / "audio" / "generated"
    uploaded = []
    skipped = []
    for wav in sorted(generated_dir.glob("*.wav")):
        if wav.name == "reference.wav":
            continue
        if find_existing(wav.name):
            skipped.append(wav.name)
            continue
        drive.files().create(
            body={"name": wav.name, "parents": [folder_id], "description": "SoninkeGPT OmniVoice clone — NON VALIDÉ, écoute humaine requise"},
            media_body=MediaFileUpload(str(wav), mimetype="audio/wav", resumable=True),
            fields="id,name",
        ).execute()
        uploaded.append(wav.name)

    manifest_path = ROOT / "data" / "voice-memory.json"
    if manifest_path.exists():
        existing = find_existing("voice-memory-review.json")
        media = MediaFileUpload(str(manifest_path), mimetype="application/json", resumable=True)
        if existing:
            drive.files().update(
                fileId=existing[0]["id"],
                body={"description": "Manifeste de revue SoninkeGPT — les clones restent non validés jusqu'à écoute humaine"},
                media_body=media,
                fields="id,name",
            ).execute()
        else:
            drive.files().create(
                body={"name": "voice-memory-review.json", "parents": [folder_id], "description": "Manifeste de revue SoninkeGPT — les clones restent non validés jusqu'à écoute humaine"},
                media_body=media,
                fields="id,name",
            ).execute()

    print(json.dumps({"uploaded_wavs": uploaded, "skipped_existing_wavs": skipped, "review_folder_id": folder_id}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
