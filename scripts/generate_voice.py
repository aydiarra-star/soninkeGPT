#!/usr/bin/env python3
"""Build complete lexical voice memory; optionally generate missing WAVs on a GPU.
Never infer syllable timestamps or overwrite the original recordings.
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

def build(generate=False, limit=100):
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
        if not torch.cuda.is_available():
            raise RuntimeError('GPU CUDA requis : aucune voix de remplacement autorisée.')
        model = OmniVoice.from_pretrained('k2-fsa/OmniVoice', device_map='cuda:0', dtype=torch.float16)
        if not any('sonink' in str(lang).lower() for lang in model.supported_language_names()):
            raise RuntimeError('Le modèle ne confirme pas la prise en charge du soninké.')
        a, sr = sf.read(ROOT / 'audio/snk-00054.wav')
        b, sr_b = sf.read(ROOT / 'audio/snk-00258.wav')
        if sr != sr_b:
            raise ValueError('Fréquences de référence incompatibles.')
        if a.ndim > 1: a = a.mean(axis=1)
        if b.ndim > 1: b = b.mean(axis=1)
        generated_dir.mkdir(parents=True, exist_ok=True)
        reference = generated_dir / 'reference.wav'
        sf.write(reference, np.concatenate([a, np.zeros(int(.4 * sr)), b]), sr)
        batch = pending[:max(1, limit)]
        print(f'Génération du lot : {len(batch)} mots ; {max(0, len(pending) - len(batch))} mots resteront en attente.')
        for item in batch:
            output_path = ROOT / item['url']
            if output_path.exists() and valid_wav(output_path):
                continue
            if output_path.exists():
                output_path.unlink()
            result = model.generate(text=item['text'], language='soninke', ref_audio=str(reference), ref_text='Daga goli. Li taxu.', num_step=32)
            samples = np.asarray(result[0]).squeeze()
            if samples.ndim != 1 or not samples.size or not np.isfinite(samples).all():
                raise ValueError(f"Audio invalide : {item['text']}")
            sf.write(output_path, samples, int(model.sampling_rate), subtype='PCM_16')
        return build(False, limit)
    memory = {'model': 'k2-fsa/OmniVoice', 'references': ['audio/snk-00054.wav', 'audio/snk-00258.wav'], 'audio': list(audio.values()), 'pending': pending, 'syllables': [], 'note': 'Les clones générés restent non validés jusqu’à écoute humaine. Aucun WAV original n’est écrasé.'}
    (ROOT / 'data/voice-memory.json').write_text(json.dumps(memory, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(audio)} WAV indexés ; {len(pending)} formes en attente.')
    return memory

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--limit', type=int, default=100, help='Nombre maximum de nouveaux WAV à générer par exécution (défaut : 100).')
    args = parser.parse_args()
    build(args.generate, args.limit)
