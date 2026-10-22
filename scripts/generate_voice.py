#!/usr/bin/env python3
"""Build lexical voice memory and optionally generate missing WAVs with OmniVoice.
Never overwrite authentic recordings; generated files remain unreviewed until human validation.
"""
import argparse
import csv
import hashlib
import json
import re
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def rows(path):
    text = path.read_text(encoding='utf-8-sig')
    return list(csv.DictReader(text.splitlines(), delimiter=';' if ';' in text.splitlines()[0] else ','))

def key(text):
    return ' '.join(text.lower().split())

def valid_wav(path):
    try:
        with wave.open(str(path), 'rb') as handle:
            return handle.getnframes() > 0 and handle.getframerate() > 0
    except (wave.Error, EOFError, OSError):
        return False

def build(generate=False, limit=100, device="auto"):
    vocabulary = {}
    for path in sorted((ROOT / 'data').rglob('*.csv')):
        for row in rows(path):
            text = next((row.get(c, '').strip() for c in ('soninke', 'text', 'lemme_corrige', 'lemme', 'lemme_source') if row.get(c, '').strip()), '')
            if text:
                text = re.sub(r'\d+$', '', text).strip()
                if text:
                    vocabulary.setdefault(key(text), {'text': text, 'source': str(path.relative_to(ROOT))})
    # Keep greetings and their variants synchronized with the application.
    app = (ROOT / 'app.js').read_text()
    phrasebook = app.split('const PHRASEBOOK = [', 1)[1].split('\n];', 1)[0]
    for match in re.finditer(r'snk: "([^"]+)"|alt: \[([^\]]*)\]', phrasebook):
        for text in ([match[1]] if match[1] else re.findall(r'"([^"]+)"', match[2])):
            vocabulary.setdefault(key(text), {'text': text, 'source': 'app.js:PHRASEBOOK'})
    audio = {}
    for row in rows(ROOT / 'data/source/manifest-577-review.csv'):
        path = ROOT / 'audio' / f"{row['id']}.wav"
        if path.exists() and valid_wav(path):
            audio[key(row['text'])] = {'text': row['text'], 'url': str(path.relative_to(ROOT)), 'kind': 'recorded'}
    generated_dir = ROOT / 'audio/generated'
    for item in vocabulary.values():
        digest = hashlib.sha256(item['text'].encode()).hexdigest()[:24]
        item['url'] = f'audio/generated/{digest}.wav'
        path = ROOT / item['url']
        if path.exists():
            if valid_wav(path):
                audio.setdefault(key(item['text']), {**item, 'kind': 'voice_clone_unreviewed'})
            else:
                path.unlink()
    pending = [v for k, v in sorted(vocabulary.items()) if k not in audio]
    if generate and pending:
        import numpy as np
        import soundfile as sf
        import torch
        from omnivoice import OmniVoice

        # Auto = CUDA si disponible, sinon Apple Silicon MPS, sinon CPU.
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
        if target_device == "mps" and not (getattr(torch.backends, "mps", None) and torch.backends.mps.is_available()):
            raise RuntimeError("MPS demandé mais indisponible sur cette machine.")
        dtype = torch.float16 if target_device.startswith("cuda") else torch.float32
        print(f"Chargement OmniVoice sur {target_device} ({dtype}) ; le CPU peut être lent et gourmand en mémoire.")
        model = OmniVoice.from_pretrained('k2-fsa/OmniVoice', device_map=target_device, dtype=dtype)
        language_names = {str(lang).casefold() for lang in model.supported_language_names()}
        language_ids = {str(lang).casefold() for lang in model.supported_language_ids()}
        if not (any('sonink' in lang for lang in language_names) or 'snk' in language_ids):
            raise RuntimeError('Le modèle ne confirme pas la prise en charge du soninké (snk). Arrêt sans génération.')
        ref_a = ROOT / 'audio/snk-00054.wav'
        ref_b = ROOT / 'audio/snk-00258.wav'
        for ref in (ref_a, ref_b):
            if not valid_wav(ref):
                raise FileNotFoundError(f"Référence vocale absente ou WAV invalide : {ref}. Restaure le fichier original, sans le remplacer par une voix générique.")
        a, sr = sf.read(ref_a)
        b, sr_b = sf.read(ref_b)
        if sr != sr_b:
            raise ValueError('Fréquences de référence incompatibles.')
        if a.ndim > 1: a = a.mean(axis=1)
        if b.ndim > 1: b = b.mean(axis=1)
        generated_dir.mkdir(parents=True, exist_ok=True)
        reference = generated_dir / 'reference.wav'
        sf.write(reference, np.concatenate([a, np.zeros(int(.4 * sr)), b]), sr)
        batch = pending[:max(1, limit)]
        print(f'Génération du lot : {len(batch)} mots ; {max(0, len(pending) - len(batch))} mots resteront en attente.')
        failures = []
        for i, item in enumerate(batch, 1):
            output_path = ROOT / item['url']
            if output_path.exists() and valid_wav(output_path):
                continue
            if output_path.exists():
                output_path.unlink()  # fichier généré invalide uniquement; les WAV originaux ne sont jamais touchés
            try:
                result = model.generate(text=item['text'], language='snk', ref_audio=str(reference), ref_text='Daga goli. Li taxu.', num_step=32)
                samples = np.asarray(result[0]).squeeze()
                if samples.ndim != 1 or not samples.size or not np.isfinite(samples).all():
                    raise ValueError('sortie audio vide ou invalide')
                temp_path = output_path.with_suffix('.tmp.wav')
                sf.write(temp_path, samples, int(model.sampling_rate), subtype='PCM_16')
                if not valid_wav(temp_path):
                    temp_path.unlink(missing_ok=True)
                    raise ValueError('le WAV créé n’a pas passé le contrôle technique')
                temp_path.replace(output_path)
                print(f'[{i}/{len(batch)}] WAV créé (à écouter) : {item["text"]}')
            except Exception as exc:
                failures.append((item['text'], str(exc)))
                print(f'[{i}/{len(batch)}] ÉCHEC — {item["text"]}: {exc}')
        if failures:
            report = ROOT / 'data/voice-generation-errors.csv'
            with report.open('w', encoding='utf-8', newline='') as handle:
                writer = csv.writer(handle)
                writer.writerow(['soninke', 'erreur'])
                writer.writerows(failures)
            print(f'{len(failures)} échec(s) consignés dans {report.relative_to(ROOT)} ; ils pourront être retentés au prochain lancement.')
        return build(False, limit, device)
    memory = {'model': 'k2-fsa/OmniVoice', 'references': ['audio/snk-00054.wav', 'audio/snk-00258.wav'], 'audio': list(audio.values()), 'pending': pending, 'syllables': [], 'note': 'Les clones générés restent non validés jusqu’à écoute humaine. Aucun WAV original n’est écrasé.'}
    (ROOT / 'data/voice-memory.json').write_text(json.dumps(memory, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(audio)} WAV indexés ; {len(pending)} formes en attente.')
    return memory

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--limit', type=int, default=100, help='Nombre maximum de nouveaux WAV à générer par exécution (défaut : 100).')
    parser.add_argument('--device', choices=['auto', 'cpu', 'cuda', 'mps'], default='auto', help='Périphérique d’inférence ; auto choisit CUDA, puis MPS, puis CPU.')
    args = parser.parse_args()
    build(args.generate, args.limit, args.device)
