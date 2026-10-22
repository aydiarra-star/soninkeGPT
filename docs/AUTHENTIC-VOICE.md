# Voix du référent uniquement

Le navigateur n’utilise aucun moteur de synthèse vocale. La lecture automatique
est activée par défaut ; l’utilisateur peut la couper. Les restrictions d’autoplay
du navigateur nécessitent parfois un clic sur « Écouter ». Les explications en
français restent textuelles (bouton sur chaque réponse et questions « Que signifie… ? »).

La mémoire indexe les WAV historiques et toutes les formes lexicales des CSV,
ainsi que les salutations de PHRASEBOOK. Les buffers décodés sont conservés pendant
la session. L’assemblage WebAudio emploie les expressions exactes puis les mots
entiers, par correspondance la plus longue. Une phrase incomplètement couverte
n’est pas prononcée. Aucun alignement syllabique fiable n’existe dans le corpus :
le système ne découpe donc pas arbitrairement les WAV pour inventer des syllabes.

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
variable de dépôt `OMNIVOICE_GPU_ENABLED=true`. Sans cela, seul l’index tourne :
aucun GPU gratuit ni prise en charge linguistique ne sont présumés.
Le lot produit l’artefact `omnivoice-generated-review`. Après validation humaine,
intégrer ses WAV sous `audio/generated/` et reconstruire l’index ; Pages chargera
ces fichiers. Le workflow ne publie pas silencieusement des clones non validés.

Pages reconstruit également l’index avant chaque déploiement. Les formes à venir
entrent ainsi automatiquement dans la mémoire, mais leur audio n’existe qu’après
une génération réussie ou la fourniture d’un enregistrement validé.

Tests : `node tests/voice.test.cjs` ; `python scripts/generate_voice.py`.
