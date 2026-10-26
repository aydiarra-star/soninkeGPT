# Chantier de recherche — numération soninké et comptage de l'argent

## Objectif

Séparer strictement deux domaines qui ne doivent pas partager automatiquement leurs règles :

1. **Numération générale** : compter, lire et écrire les nombres, faire des calculs et exprimer des quantités non monétaires.
2. **Comptage monétaire** : exprimer des prix, sommes, paiements et montants dans une monnaie déterminée.

Ce chantier est une base de recherche et de validation. Il ne constitue pas une validation linguistique et ne modifie pas les règles de production de SoninkeGPT.

## Règles de travail non négociables

- Ne jamais déduire une expression monétaire en appliquant mécaniquement les règles des nombres ordinaires.
- Ne jamais déduire qu'un mot isolé signifie une somme d'argent sans contexte et preuve d'usage.
- Ne pas supposer que les conventions FCFA se transposent à l'euro.
- Conserver les variantes orthographiques et les variantes régionales sans les fusionner automatiquement.
- Distinguer l'attestation écrite, la corroboration indépendante, la validation orale par un locuteur, la validation audio et l'intégration technique.
- Ne pas générer ni marquer un audio comme validé tant que la forme lexicale et sa prononciation ne sont pas confirmées.
- Pour toute entrée, enregistrer la forme exacte, la segmentation proposée, le sens, la monnaie, la valeur numérique, le contexte, la provenance et le statut de validation.
- En cas de contradiction entre sources, conserver les deux analyses et ouvrir une question au référent au lieu de choisir arbitrairement.

## Schéma des données

### Référentiel A — numération générale

Champs recommandés : `id`, `valeur`, `forme_soninke`, `variante`, `segmentation`, `gloss_fr`, `type` (unité/dizaine/centaine/composé/grand nombre), `règle_de_formation`, `région`, `provenance`, `statut_attestation`, `statut_validation_orale`, `statut_audio`, `notes`.

### Référentiel B — expressions monétaires

Champs recommandés : `id`, `montant_numérique`, `monnaie`, `expression_soninke`, `segmentation`, `unité_monétaire_traditionnelle`, `sens_littéral`, `équivalent_calculé`, `contexte`, `région`, `source`, `statut_attestation`, `statut_validation_orale`, `statut_audio`, `notes`.

Les deux référentiels auront des identifiants et des règles séparés. Une entrée peut être reliée à l'autre pour comparaison, mais cette relation ne vaut pas équivalence.

## Premières pistes — à vérifier, non validées

- Les formes cardinales rapportées incluent notamment `tanpille` pour 20, `kame` pour 100, `kamo filli` pour 200 et `wujune` pour 1 000.
- Des ressources pédagogiques sur l'argent rapportent une unité `gode/godi` associée à cinq francs CFA dans certains exemples.
- Les expressions rapportées pour certains montants doivent être confrontées à la forme exacte, à la segmentation et au contexte d'usage. En particulier, ne pas conclure que `kame` isolé signifie 500 : les données préliminaires distinguent `kame` (100 dans le système cardinal) et une expression du type `keme gode` (rapportée pour 500 FCFA).
- L'usage en euros, les variantes régionales, la valeur de `gode/godi` et la formation des montants non documentés restent à établir.

## Protocole de validation

1. Rassembler les formes exactes des dictionnaires et ressources pédagogiques soninké.
2. Comparer les formes, sans fusion automatique des variantes ni extrapolation à des nombres absents.
3. Préparer des questions d'élicitation neutres : « Comment diriez-vous exactement X FCFA ? », « Et le même nombre dans un calcul, sans parler d'argent ? », « Cette forme est-elle naturelle dans votre variété ? »
4. Interroger séparément plusieurs locuteurs, en notant variété/région et contexte. Ne pas suggérer la réponse avant la première production.
5. Enregistrer les audios uniquement après validation de la forme; faire confirmer l'audio par le référent linguistique.
6. Faire une revue indépendante du CSV, des contradictions et des statuts avant toute fusion dans le lexique de production.
7. N'intégrer à `main` qu'après revue du référent et tests démontrant que les deux systèmes sont traités séparément.

## Fichier de suivi

Le fichier `data/source/monetary-counting-review.csv` contient les premières pistes de comptage monétaire. Toutes les lignes commencent au statut « candidat à vérifier »; elles ne sont pas des traductions validées.
