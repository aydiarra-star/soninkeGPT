# Préparation de la production audio — lot tête et visage

Le lot contient 20 entrées du fichier de mots utilisé par le notebook OmniVoice. La prononciation de ces entrées a été validée par le référent linguistique; cela ne prouve pas que chaque WAV est accessible dans le dépôt ou techniquement validé.

## Contrôles avant génération ou réutilisation

1. Dans Google Drive, vérifier le dossier `SONINKE_TTS_LIBRE/head_face_batch/audio/` et le manifeste existant. Ne pas régénérer un fichier déjà présent sans raison.
2. Le notebook `notebooks/OmniVoice-Tete-Visage-Voix-Referent.ipynb` s'arrête si aucun GPU n'est disponible ou si le modèle ne déclare pas la langue soninké. Ne pas contourner ces garde-fous ni payer pour un GPU.
3. Vérifier que `reference_soninke.wav` est la voix de référence correcte et que la transcription est exactement `Daga goli. Li taxu.`
4. Après génération, écouter les WAV et renseigner le manifeste avec présence, durée, fréquence d'échantillonnage, erreur éventuelle et validation technique. La validation de prononciation reste séparée.
5. Les candidats CNRS/LGIDF restent en attente de validation linguistique; ne pas les envoyer au TTS de production pour le moment.

## Statuts du lot

- `prononciation_validation=validee_par_referent` : prononciation validée par le référent.
- `audio_file_present_verified=non_verifie_depuis_chat` : présence effective du WAV non inspectée ici.
- `tts_model_language_support=a_confirmer_dans_runtime` : la prise en charge du soninké doit être confirmée par le runtime. Le notebook est conçu pour s'arrêter si ce n'est pas le cas.

Le fichier de manifeste de ce lot est `data/audio/head-face-production-queue.csv`.
