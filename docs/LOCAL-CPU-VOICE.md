# Génération vocale locale sur CPU

## Ce que fait cette procédure

Le script utilise l'implémentation Python officielle de `k2-fsa/OmniVoice`, mais charge le modèle sur CPU en `float32` si aucun accélérateur n'est disponible. Sur les machines compatibles, `--device auto` choisit CUDA, puis Apple MPS, puis CPU.

- Les deux références sont les WAV historiques `audio/snk-00054.wav` (« Daga goli ») et `audio/snk-00258.wav` (« Li taxu »).
- La transcription de référence reste exactement `Daga goli. Li taxu.`.
- Les WAV historiques ne sont jamais écrasés.
- Les nouveaux fichiers vont dans `audio/generated/` et sont indexés comme `voice_clone_unreviewed`.
- Les audios générés doivent être écoutés et validés par le référent linguistique avant toute publication.
- Le script traite au maximum 100 formes par exécution par défaut, saute les WAV déjà valides et peut être relancé après interruption.

## Prérequis

- Ordinateur Linux ou macOS avec Python 3.10+ et connexion Internet pour télécharger les dépendances et les poids du modèle.
- Prévoir plusieurs Go d'espace disque pour l'environnement Python et les poids du modèle. Le modèle complet peut nécessiter plusieurs Go de RAM ; le CPU sera nettement plus lent qu'un GPU.
- Les deux WAV de référence doivent exister dans `audio/`. Le dépôt peut ne pas contenir les fichiers audio binaires dans chaque clone : si une référence manque, restaure l'original depuis ton archive/Drive, ne la remplace pas par une voix générique.

## Installation

Depuis la racine du dépôt :

```bash
bash scripts/setup_local_cpu.sh
```

Le script crée `.venv/`, installe PyTorch CPU et OmniVoice, puis vérifie réellement l'import `from omnivoice import OmniVoice`.

Si l'installation s'arrête, conserve et partage la sortie complète : ne poursuis pas la génération.

## Tester puis générer

Commence par un lot de 5 ou 20 mots pour contrôler la qualité :

```bash
.venv/bin/python scripts/generate_voice.py
.venv/bin/python scripts/generate_voice.py --generate --device cpu --limit 5
```

Puis, après écoute :

```bash
.venv/bin/python scripts/generate_voice.py --generate --device auto --limit 100
```

Sur une machine NVIDIA, `auto` choisit CUDA ; sur un Mac compatible, MPS ; sinon CPU. On peut forcer `--device cpu`, `--device cuda` ou `--device mps`.

## Reprise et validation

Le script ignore les fichiers WAV générés qui existent déjà et sont techniquement valides. Les erreurs de génération sont consignées dans `data/voice-generation-errors.csv` et les formes sans WAV restent en attente pour un nouvel essai. Les nouveaux audios ne sont jamais automatiquement marqués comme validés par le référent.

Après chaque lot :
1. écouter chaque WAV ;
2. noter la validation humaine séparément de la validation technique ;
3. conserver les graphies et les variantes lexicales sans correction silencieuse ;
4. seulement ensuite intégrer les audios validés à la publication.

## Limites importantes

Cette voie CPU utilise les mêmes poids de modèle OmniVoice mais pas le port C++/GGML. Elle n'a pas été exécutée sur une machine utilisateur dans le cadre de ce changement ; la réussite de l'installation, la mémoire disponible et la prononciation de chaque mot doivent donc être vérifiées sur la machine cible. Un port communautaire C++/GGML existe également, mais il est indépendant du dépôt officiel et son niveau de parité/qualité doit être évalué séparément : ne pas promettre une qualité strictement identique sans test comparatif.
