# Voix de référence sur tous les contenus audio

SoninkeGPT utilise une **voix de référence unique** pour l'ensemble de son
expérience vocale : mots, expressions, salutations, traductions, réponses
générées, contenu pédagogique, favoris et futurs ajouts du corpus.

```text
corpus du référent  ─┐
générations OmniVoice├─► index unique ─► lecture (WebAudio / HTMLAudio)
issu de la voix    ─┘
```

Une seule fonction, `findAudioInfo()`, résout chaque forme affichée. Elle
consulte, dans cet ordre :

1. l'index des enregistrements du corpus (`audio/snk-*.wav`) ;
2. l'index des variantes graphiques reliées à leur lemme enregistré ;
3. l'index orthographique normalisé (kh↔x, ou↔u, ñ↔ny, dj↔j, tch↔c) ;
4. l'index de `data/voice-memory.json`, qui contient les enregistrements
   existants et les clips générés avec OmniVoice à partir de la voix de
   référence.

Aucune autre voix n'est employée : le navigateur n'utilise jamais
`speechSynthesis` ni une voix système. Si une forme n'a pas d'audio de
référence, l'interface affiche « Audio à venir » et explique qu'aucune voix de
substitution n'est utilisée.

## Lecture

La lecture automatique est activée par défaut ; l'utilisateur peut la couper.
Les restrictions d'autoplay imposent parfois un clic sur « Écouter ». Les
explications en français restent textuelles.

Les buffers décodés sont conservés pendant la session. L'assemblage WebAudio
emploie les expressions exactes puis les mots entiers, par correspondance la
plus longue. Une phrase incomplètement couverte n'est pas prononcée. Aucun
alignement syllabique fiable n'existe dans le corpus : le système ne découpe
donc pas arbitrairement les WAV pour inventer des syllabes.

## Génération automatique

`python scripts/generate_voice.py` reconstruit `data/voice-memory.json` et sa file
`pending`, sans dépendances externes. Au premier index : 576 WAV et 924 formes
sans enregistrement exact. Cela ne constitue PAS une couverture vocale complète.

`python scripts/generate_voice.py --generate` utilise exclusivement
`k2-fsa/OmniVoice`, la langue `soninke`, `snk-00054.wav` (« Daga goli ») et
`snk-00258.wav` (« Li taxu »). Il exige CUDA et vérifie la langue déclarée par le
modèle avant toute génération. Les WAV originaux ne sont jamais écrasés.
Les nouveaux WAV sont des **clones générés, non des enregistrements authentiques** ;
leur prononciation doit être écoutée et validée par le référent.

Le workflow `voice-memory.yml` reconstruit automatiquement la file après un ajout
CSV sur main. Pour activer le lot neuronal, provisionner un runner isolé
`self-hosted, linux, gpu` avec PyTorch CUDA et accès au modèle, puis définir la
variable de dépôt `OMNIVOICE_GPU_ENABLED=true`. Sans cela, seul l'index tourne :
aucun GPU gratuit ni prise en charge linguistique ne sont présumés.
Le lot produit l'artefact `omnivoice-generated-review`. Après validation humaine,
intégrer ses WAV sous `audio/generated/` et reconstruire l'index ; Pages chargera
ces fichiers. Le workflow ne publie pas silencieusement des clones non validés.

Pages reconstruit également l'index avant chaque déploiement. Les formes à venir
entrent ainsi automatiquement dans la mémoire, mais leur audio n'existe qu'après
une génération réussie ou la fourniture d'un enregistrement validé.

Tests : `node tests/voice.test.cjs` ; `python scripts/generate_voice.py`.
