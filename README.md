# SoninkeGPT

SoninkeGPT est un nouveau projet consacré au dictionnaire et à l'assistance linguistique soninké–français. Il repart sur une base logicielle neuve tout en réutilisant, de manière sélective et traçable, le patrimoine linguistique déjà constitué dans [Soninké TTS Libre](https://github.com/aydiarra-star/xamxam-xara).

## Priorité immédiate : transfert sans perte
- Manifeste historique de 577 entrées : [copie source](data/source/manifest-577-review.csv)
- [Plan de transfert, provenance et contrôle des licences](docs/TRANSFER-PLAN.md)

Le manifeste est une métadonnée de corpus; il ne prouve pas que tous les WAV sont présents dans ce dépôt. Les fichiers audio doivent être transférés depuis l'archive réelle et vérifiés. L'état historique connu est de 576 WAV distincts et un audio manquant pour snk-00308 (« n »). Aucun audio ne sera régénéré pour dissimuler un manque.

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
