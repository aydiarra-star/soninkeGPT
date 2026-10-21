# SoninkeGPT

SoninkeGPT est un nouveau projet consacré au dictionnaire et à l'assistance linguistique soninké–français. Il repart sur une base logicielle neuve tout en réutilisant, de manière sélective et traçable, le patrimoine linguistique déjà constitué dans [Soninké TTS Libre](https://github.com/aydiarra-star/xamxam-xara).

## Priorité immédiate : transfert sans perte
- Manifeste historique de 577 entrées : [copie source](data/source/manifest-577-review.csv)
- [Plan de transfert, provenance et contrôle des licences](docs/TRANSFER-PLAN.md)
- [Rapport du premier transfert audio](reports/audio-transfer-summary.md)
- [Audit détaillé des fichiers WAV et empreintes SHA-256](reports/audio-transfer-audit.csv)

Le propriétaire du corpus confirme que les 577 enregistrements ont été écoutés et validés par lui-même, dans sa propre voix, avec une prononciation correcte. Cette validation humaine est distincte de la présence technique des fichiers WAV dans ce dépôt. L'ancien état du manifeste indiquait 576 WAV accessibles et un fichier introuvable pour `snk-00308` (« n ») ; cette incohérence doit être réconciliée en recherchant l'original, sans remettre en cause la validation humaine et sans régénérer artificiellement l'audio. Le workflow d'import produit un audit des fichiers effectivement copiés.

## Principes
1. Préserver les graphies, variantes, sens multiples, exemples et provenance.
2. Distinguer les entrées confirmées des candidats à vérifier.
3. Ne pas altérer le dépôt source.
4. N'intégrer les données externes qu'avec provenance et droits de réutilisation vérifiés.
5. Construire ensuite l'application : recherche Soninké→Français et Français→Soninké, fiches lexicales, écoute audio, suggestions/corrections et outils d'administration.

## Ressources externes à examiner
- [Asawan — lexique Soninké–Français–Anglais](https://www.asawan.org/fr/lexique_soninke)
- [CNRS / LGIDF — ressources sur le soninké](https://lgidf.cnrs.fr/node/25)
- [Dictionnaire Soninké–Français](https://dicosoninke.wordpress.com/)
- [Glosbe Soninké–Français](https://fr.glosbe.com/snk/fr)
- [Glosbe Français–Soninké](https://fr.glosbe.com/fr/snk)

Ces références sont des sources d'audit et de découverte, pas une autorisation automatique de copier leurs bases complètes.
