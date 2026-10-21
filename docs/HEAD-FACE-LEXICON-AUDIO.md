# Tête et visage — lexique et enregistrements à réaliser

## Intégration lexicale

Les 20 formes ci-dessous ont été ajoutées au lexique à partir de la liste fournie par le référent le 21 octobre 2026. Les graphies et variantes sont conservées séparément; aucune fusion automatique n'a été faite.

Les statuts sont `fourni_par_referent_a_verifier`: la liste est bien attribuée au référent, mais ces nouvelles entrées n'ont pas encore reçu une validation phonétique dédiée ni un audio correspondant dans le dépôt.

## Audio avec la voix du référent

Le manifeste historique a été comparé aux 20 formes: aucune correspondance exacte n'a été trouvée parmi les 577 entrées. Il n'existe donc pas d'enregistrement source vérifié à relier automatiquement à ces mots.

La file `data/source/head-face-audio-recording-queue.csv` prépare un identifiant pour chacun des 20 enregistrements. Les fichiers WAV doivent provenir d'une véritable prise de voix du référent, ou d'un système de clonage vocal autorisé et réellement configuré avec ses enregistrements. Aucun audio n'est généré artificiellement dans cette étape et aucun ancien fichier n'est associé par ressemblance.

## Liste conservée

| Français | Soninké fourni |
|---|---|
| tête | yime |
| cheveux | yinte |
| visage | Giya |
| front | Teingé |
| œil | Yaxe |
| yeux | Yaxou |
| nez | Nuxune |
| bouche | rakke |
| lèvre | gnougnou |
| lèvre (variante) | some |
| dent | kambe |
| dents (pluriel) | kambou |
| langue | Nene |
| oreille | torro |
| joues | xoume |
| menton | xané |
| cou | yesso |
| cou (variante) | sinke |
| gorge | xanné |
| gorge (variante) | xorré |

## Notebook prêt pour la génération avec la voix de référence

Un notebook Colab dédié est disponible : [OmniVoice-Tete-Visage-Voix-Referent.ipynb](../notebooks/OmniVoice-Tete-Visage-Voix-Referent.ipynb). Il charge les 20 formes depuis `data/source/head-face-tts-wordlist.csv`, utilise `reference_soninke.wav` et sa transcription `Daga goli. Li taxu.` dans le dossier Google Drive `SONINKE_TTS_LIBRE`, puis écrit les WAV et un manifeste avec durées, empreintes SHA-256 et statuts de validation. Il s'arrête si aucun GPU n'est disponible et n'envoie aucun WAV automatiquement vers GitHub.

[Ouvrir le notebook directement dans Google Colab](https://colab.research.google.com/github/aydiarra-star/soninkeGPT/blob/main/notebooks/OmniVoice-Tete-Visage-Voix-Referent.ipynb)

## Prochaine étape audio

Enregistrer séparément chaque forme soninkée, dans un environnement calme, sans musique ni voix en arrière-plan. Conserver le fichier original, associer son identifiant de file, puis vérifier l'écoute et le SHA-256 avant de l'ajouter au dépôt. Le statut de prononciation humaine ne devra passer à validé qu'après écoute/confirmation réelle.