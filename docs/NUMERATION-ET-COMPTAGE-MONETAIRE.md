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

## Résultats complémentaires de recherche (pistes, toujours non validées)

Les ressources consultées renforcent l'hypothèse d'une unité monétaire traditionnelle `gode` correspondant à 5 FCFA dans les usages décrits. Elles rapportent notamment les correspondances suivantes, qui doivent rester des candidats tant que le référent ne les a pas vérifiées :

- `godo baane` : 5 FCFA ;
- `godo hilli/filli` : 10 FCFA ;
- `godo sikki` : 15 FCFA ;
- `godo naxati` : 20 FCFA ;
- `godo karagi` : 25 FCFA ;
- `godo tanmi` : 50 FCFA ;
- `tanfille gode` : 100 FCFA ;
- `kame/keme gode` : 500 FCFA ;
- `kamo filli gode` : 1 000 FCFA ;
- `wujune gode` : 5 000 FCFA, selon la ressource consultée.

Le calcul par cinq est cohérent avec cette série : la valeur monétaire exprimée en unités de `gode` peut être cinq fois le cardinal correspondant. Cela ne permet pas d'étendre automatiquement la règle à toute forme ou à toute monnaie, et ne signifie pas que le mot cardinal seul change de sens.

Des formes telles que `komohillin dere`, `komonaxatin dere` et `wujinin dere` sont également rapportées pour des montants ou des billets; elles sont consignées comme formes à examiner, sans les ramener prématurément à une règle générale.

Une publication comparative sur les systèmes numériques mandé décrit le comptage de l'argent par multiplication par cinq dans plusieurs langues de la famille. Cette observation comparative peut orienter les questions, mais elle ne remplace jamais une attestation spécifique au soninké. Les formes d'autres langues mandé ne doivent pas être importées dans le lexique soninké.

## Questions prioritaires au référent linguistique

1. Est-ce que `gode` désigne historiquement ou actuellement une pièce/unité de 5 FCFA dans votre variété ?
2. Pour 10, 15, 20 et 25 FCFA, quelles sont les formes exactes, prononcées naturellement, et quelles variantes existent ?
3. Pour 100 FCFA, dit-on `tanfille gode`, `tanpille gode`, les deux, ou autre chose ?
4. Pour 500 FCFA, quelle est la forme exacte : `kame gode`, `keme gode`, ou une autre variante ? `kame` seul peut-il désigner 100 dans un contexte et 500 dans un contexte monétaire, ou faut-il obligatoirement une expression complète ?
5. Pour 1 000, 2 000, 5 000 et les sommes élevées, quelles expressions sont naturelles, et lesquelles s'emploient seulement pour des billets ?
6. Les expressions monétaires en euros suivent-elles les expressions traditionnelles en `gode`, les nombres cardinaux ordinaires, ou une stratégie mixte ?
7. Les réponses changent-elles selon la région, la génération, le commerce ou la variété de soninké ?

Aucune réponse à ces questions ne doit être préremplie comme si elle avait été donnée par un locuteur.

## Traduction française des candidats — sens des mots et sens monétaire

Le tableau CSV a été enrichi avec deux champs distincts : `sens_des_éléments_fr` et `sens_de_l_expression_fr`. Cette séparation est obligatoire.

Les ressources comparées décrivent un système où `gode` est une unité monétaire de 5 FCFA. Ainsi, `gode baane` est rapporté comme une unité, soit 5 FCFA; `godo filli/hilli` comme deux unités, soit 10 FCFA; `godo sikki` comme trois unités, soit 15 FCFA; `godo naxati` comme quatre unités, soit 20 FCFA; `godo karagi` comme cinq unités, soit 25 FCFA; `godo tanmi` comme dix unités, soit 50 FCFA. `tanpille gode` est rapporté pour 100 FCFA, et `kame/keme gode` pour 500 FCFA. L'analyse par unités de cinq est cohérente avec ces exemples, mais les formes exactes et leurs usages restent à confirmer auprès de locuteurs.

Pour `tannaxate` (200 FCFA) et `tandume` (300 FCFA), les formes sont rapportées dans la leçon monétaire, mais leur analyse comme 40 et 60 unités de `gode` est une hypothèse arithmétique, pas encore une traduction littérale confirmée.

Pour `komohillin dere`, `komonaxatin dere`, `wujinin dere` et les expressions de montants élevés, le sens des éléments et la segmentation restent non établis. Le tableau ne doit pas inventer une traduction mot à mot. La traduction de l'expression entière rapporte uniquement le montant documenté dans le contexte.

La numération générale donne séparément les sens cardinaux tels que `tanmu` = dix, `tanpille/tanfille` = vingt, `tannaxate` = quarante, `tandume` = soixante, `kame` = cent et `wujune` = mille. Ces gloses cardinales aident à examiner les candidats monétaires, mais ne prouvent pas à elles seules leur sens dans l'expression d'argent.

**État actuel :** montants et expressions sont consignés comme attestés dans des ressources pédagogiques; les traductions littérales et l'usage oral restent à valider. Aucun audio et aucune règle de production ne sont validés par ce document.
