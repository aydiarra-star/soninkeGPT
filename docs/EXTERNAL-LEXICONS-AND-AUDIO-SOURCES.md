# Audit des sources lexicales et audio soninké

Date de repérage : 2026-10-21

## Premier lot extrait

Le fichier `data/source/peace-corps-soninke-audio-lexicon-candidates.csv` contient **133 lignes candidates** relevées dans le PDF `MR Soninke Language Lessons` du cours Peace Corps Soninke, hébergé par FSI Language Courses.

- Source PDF : https://fsi-language-courses-media.nyc3.cdn.digitaloceanspaces.com/languages-peacecorps/Soninke/MR_Soninke_Language_Lessons.pdf
- Page du cours et liens vers les 10 pistes audio : https://www.fsi-language-courses.org/soninke/courses/peace-corps-soninke-language-lessons/
- Les traductions françaises sont des traductions de travail à partir des gloses anglaises du manuel; elles ne sont **pas** des validations linguistiques.
- Les graphies source sont conservées. Les formes incertaines issues de l'extraction PDF, par exemple `Yaaxan-du?eru` et `Fan?e`, sont signalées, pas corrigées par conjecture.
- Les champs `pdf_page_1based` indiquent la page PDF physique (indexation à partir de 1).
- `audio_lesson_number` indique la piste du cours dont le contenu est associé à la leçon. Ce n'est **pas** une synchronisation mot/audio : les fichiers audio sont des leçons entières, pas des clips isolés par mot.
- Toutes les lignes sont `a_verifier`. Ne pas fusionner automatiquement les formes avec le lexique de production et ne pas remplacer les formes déjà validées par le référent.
- La page FSI déclare que les ressources sont dans le domaine public et gratuites à utiliser. Avant toute redistribution des fichiers audio, conserver l'URL et vérifier l'origine/licence de chaque média ainsi que l'attribution requise.

## Autres sources à examiner

| Source | Apport potentiel | Audio | Limites / prochaine action |
|---|---|---|---|
| [Asawan — lexique Soninké–Français–Anglais](https://www.asawan.org/fr/lexique_soninke) | Lexique trilingue téléchargeable (17,25 Mo) et application hors ligne | Aucun fichier audio par entrée confirmé | Le lien télécharge un exécutable Windows; inspecter uniquement dans un environnement isolé et vérifier les droits avant extraction ou réutilisation. |
| [Glosbe Soninké–Français](https://fr.glosbe.com/snk/fr) | Entrées, traductions et exemples en contexte | Le site annonce des enregistrements et des lecteurs informatiques | Vérifier la nature et les droits de chaque audio; ne pas scraper ni recopier la base entière sans autorisation. |
| [Dicosoninké](https://dicosoninke.wordpress.com/) | Dictionnaire en ligne dans les deux directions | Pas d'audio téléchargeable confirmé | Étudier les possibilités d'export et demander autorisation si nécessaire. |
| [SIL AI — Bloom Speech](https://huggingface.co/datasets/sil-ai/bloom-speech) | Données sonores avec transcriptions; la fiche répertorie 546 pistes d'entraînement, 50 de validation et 66 de test pour le code `snk` | Oui, audio de récits / segments | Accès conditionnel, licences CC mixtes et restriction générale non commerciale avec exceptions selon l'enregistrement. Ce n'est pas un dictionnaire mot par mot; ne réutiliser qu'après vérification de la licence de chaque élément. |
| [Ngano — catalogue Soninke](https://ngano.dev/languages/snk) | Répertoire de jeux de données étiquetés `snk` | Une ressource potentiellement audio, une ressource de type non précisé | Le catalogue signale une ressource Hugging Face `Mayoiga/Soninke-dataset`, mais sa modalité et sa licence ne sont pas documentées clairement. À examiner avant usage. |
| [Dictionnaire CNRS / LGIDF — présentation de la langue](https://lgidf.cnrs.fr/sites/lgidf.cnrs.fr/files/images/SONINKE.24.06.19.pdf) | Orthographe, phonologie, exemples bilingues | Pas un dictionnaire audio | Référence linguistique pour annoter les formes, pas une source d'enregistrements mot à mot. |

## Protocole de traitement

1. Conserver la forme exacte de chaque source, sa glose originale, la traduction française proposée, la page et la provenance.
2. Séparer la correction linguistique de la correction OCR et de la validation audio.
3. Détecter les doublons sans effacer les variantes, les sens multiples ni les formes grammaticales.
4. Chercher les formes dans les 577 enregistrements historiques par correspondance exacte et normalisation Unicode NFC seulement; aucune association approximative automatique.
5. Lier une piste audio de cours à un mot uniquement après repérage temporel et vérification humaine. Une piste de leçon complète ne doit jamais être présentée comme un audio isolé du mot.
6. Ne rien ajouter au lexique de production avant validation du référent et contrôle des droits de réutilisation.

## Statut

Ce lot est une **proposition de recherche**, pas un ajout au lexique de production. Aucune entrée existante n'a été modifiée.


## Comparaison initiale avec le lexique de production

Comparaison exacte après normalisation Unicode NFC et passage en minuscules entre les 133 lignes candidates et les 325 entrées de `data/source/lexique-soninke-fr-base.csv` sur `main` : **8 formes candidates ont déjà une correspondance exacte**. Elles sont annotées dans le CSV avec l'identifiant existant et un statut de revue.

- Pronoms déjà présents : `N`, `An`, `A`, `O`, `Xa`, `I`.
- `Baane` : correspondance exacte avec une entrée existante dont les sens sont multiples; ne pas écraser la fiche.
- `Xaso` : correspondance exacte avec une entrée existante traduite notamment par « vieillir »; il faut examiner les sens et la catégorie grammaticale avant toute décision.
- Le CSV conserve ces candidats et leur provenance; aucun doublon n'a été supprimé et aucune entrée de production n'a été modifiée.
