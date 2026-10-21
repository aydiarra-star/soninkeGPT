# SoninkeGPT — transfert sélectif des ressources

## Objectif
Construire SoninkeGPT comme un logiciel neuf en réutilisant les données linguistiques et les preuves déjà constituées dans Soninké TTS Libre (aydiarra-star/xamxam-xara). Le dépôt source reste intact : aucune modification ni suppression n'y est autorisée dans le cadre de ce transfert.

## Ordre de transfert
1. Manifeste des 577 entrées et métadonnées audio, conservé ici dans data/source/manifest-577-review.csv.
2. Lexique soninké–français, y compris les mots ajoutés récemment, variantes orthographiques, mots composés, marqueurs grammaticaux, sens multiples, exemples, provenance et statut de vérification.
3. Ressources audio WAV, en conservant les identifiants snk-xxxxx, noms de fichiers, correspondance entrée/audio, licence et statut de validation humaine.
4. Corpus de phrases, outils d'import/export, modèles CSV/JSON, documents de validation, prototype et notes techniques réutilisables.
5. Nouvelles entrées candidates trouvées dans des ressources externes, sans les fusionner silencieusement avec les entrées confirmées.

## État du manifeste historique
Le manifeste source contient 577 identifiants. L'état documenté antérieurement est de 576 WAV distincts, un audio manquant pour snk-00308 (« n »), et une entrée potentiellement dupliquée dans l'archive historique. Il faut vérifier les fichiers réellement transférés et les sommes de contrôle avant d'affirmer que les 577 audios sont présents. Ne jamais régénérer les audios existants ni fabriquer le fichier manquant pour masquer l'absence.

Le manifeste comporte des statuts de prononciation humaine. Ils doivent être conservés tels quels et distingués des statuts techniques. Les anciennes validations ne doivent pas être étendues à de nouveaux mots sans écoute/validation réelle.

## Sources externes à auditer
- Asawan, lexique Soninké–Français–Anglais : https://www.asawan.org/fr/lexique_soninke
- LGIDF / CNRS, page Soninké avec grammaire, lexique et phonologie : https://lgidf.cnrs.fr/node/25
- Dictionnaire Soninké–Français : https://dicosoninke.wordpress.com/
- Glosbe Soninké–Français : https://fr.glosbe.com/snk/fr
- Glosbe Français–Soninké : https://fr.glosbe.com/fr/snk

Les sites ci-dessus servent d'abord à repérer des candidats, graphies, sens et exemples. Ne pas aspirer/republier massivement le contenu d'un dictionnaire tiers sans vérifier les droits et conditions de réutilisation. Chaque entrée importée doit porter une provenance, une date de collecte, une licence/condition connue, et un statut « à vérifier » si elle n'a pas été validée par un référent soninké.

## Schéma de données visé
Chaque entrée doit pouvoir conserver : identifiant stable, lemme original, variantes, traduction(s), définition, catégorie grammaticale, exemples et traductions d'exemples, dialecte/variété si connue, source, licence, statut de vérification, notes du référent, identifiant/fichier audio, statut technique audio et date de mise à jour.

## Limites de ce premier transfert
Le manifeste CSV est copié depuis la branche source de revue. Cela ne signifie pas que les fichiers WAV eux-mêmes sont déjà présents dans ce dépôt. Les binaires doivent être récupérés depuis l'archive réelle autorisée, puis comparés au manifeste par identifiant, taille et SHA-256. Le chemin Google Drive présent dans certains enregistrements est un chemin d'environnement Colab, pas un lien de téléchargement public.

## Règles de sécurité du corpus
- Le dépôt source reste inchangé.
- Conserver les formes originales et les variantes; ne pas dédoublonner en supprimant des distinctions linguistiques.
- Ne pas inventer de traductions, exemples, validations ou audios.
- Ne pas intégrer de voix privées, modèles ou poids externes sans autorisation et licence compatibles.
- Séparer les données réutilisables, le code du nouveau produit et les données candidates à vérifier.
