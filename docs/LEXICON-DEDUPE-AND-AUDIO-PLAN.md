# Rapport de rapprochement lexical Soninké–français

Date : 2026-10-21

## Périmètre effectivement comparé

- Lexique de référence sur `main` : `data/source/lexique-soninke-fr-base.csv` — 325 lignes, 325 formes distinctes par normalisation Unicode NFC + minuscules.
- Candidats Peace Corps/FSI : `data/source/peace-corps-soninke-audio-lexicon-candidates.csv` — 133 lignes candidates.
- Source lexicale additionnelle repérée : pages LGIDF/CNRS (noms, verbes, adjectifs, quantitatifs et numéraux, pronoms, déictiques). Le moteur de recherche rend une partie des listes, mais les pages complètes n'ont pas toutes pu être récupérées de façon fiable dans cette passe; elles ne sont donc pas présentées comme intégralement intégrées à ce fichier.

## Résultats

- Correspondances exactes de forme avec le lexique de référence : 8 lignes candidates (8 formes distinctes). Elles sont exclues du fichier d'ajouts pour éviter les doublons, mais restent présentes dans le fichier source original avec leurs annotations.
- Formes candidates hors lexique existant : 124 formes distinctes après regroupement par NFC + minuscules.
- Groupes de lignes candidates répétées dans la source : 1; leurs traductions et références sont regroupées, pas effacées.
- Les rapprochements approximatifs ne sont pas fusionnés automatiquement : traits d'union, espaces, tons, caractères comme ŋ/ñ et variantes dialectales peuvent distinguer des formes.

## Fichiers

- Ajouts candidats dédoublonnés : `data/source/soninke-candidates-deduplicated.csv`
- Source brute préservée : `data/source/peace-corps-soninke-audio-lexicon-candidates.csv`
- Lexique de production : inchangé. Aucun candidat n'est promu sans validation linguistique.

## Passage à l'audio

Les pistes Peace Corps/FSI sont des leçons complètes, pas des clips mot par mot. Elles peuvent servir à repérer des occurrences, mais ne constituent pas automatiquement des fichiers audio propres pour chaque entrée. Pour la production TTS du lexique, générer les lots à partir des entrées validées et de la voix de référence de l'utilisateur; contrôler séparément la prononciation et la qualité technique. Les 20 entrées SNK-LEX-0275 à SNK-LEX-0294 précédemment validées par le référent gardent leur statut distinct.

## Sources CNRS/LGIDF à intégrer dans la prochaine passe

- Noms : https://lgidf.cnrs.fr/node/680
- Verbes : https://lgidf.cnrs.fr/node/682
- Adjectifs : https://lgidf.cnrs.fr/node/681
- Quantitatifs et numéraux : https://lgidf.cnrs.fr/node/679
- Pronoms personnels : https://lgidf.cnrs.fr/node/676
- Déictiques : https://lgidf.cnrs.fr/node/677
- Interactions de base avec ressources audio : https://lgidf.cnrs.fr/soninke-interactions

Attention : le site précise que le soninké n'a pas de variété standard unique; la ressource CNRS est basée sur la variété du Kingui (Mali). Les formes et tons doivent être conservés comme formes de source et comparés sans écraser les variantes.
