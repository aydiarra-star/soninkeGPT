# Contrôle qualité de l’enrichissement du dictionnaire soninké — 21 octobre 2026

## Périmètre contrôlé

Contrôle réalisé à partir de `reports/revue-enrichissement-dictionnaire-soninke.csv`, des lots de validation 02 à 09 et de `data/lexique-soninke-fr-base.csv`.

- Segments dans la revue source : **787**.
- Entrées de la base de production : **305**.
- Segments identifiés comme renvois vers une entrée principale : **236**.
- Lemmes distincts parmi ces renvois après normalisation simple (casse/espaces) : **192**.
- Lemmes de renvoi présents plusieurs fois dans la source : **44**.
- Lemmes de renvoi déjà présents dans la base par correspondance exacte : **5 segments**.
- Première cible du renvoi trouvée exactement dans la base : **82 segments**.
- Première cible non trouvée par correspondance exacte : **143 segments** (cela ne prouve pas son absence : chiffres finaux, suffixes et graphies doivent être contrôlés).
- Segments sans cible extraite par la règle simple : **11**.
- Groupes de graphies différentes fusionnés par l’ancienne règle qui supprime les chiffres finaux : **38**.

## Constatations et décisions

### 1. Renvois à rattacher

Les 236 segments repérés sont listés dans [le fichier de contrôle des renvois](controle-renvois-dictionnaire-soninke-2026-10-21.csv). Le fichier conserve le texte source intégral, le numéro de paragraphe, la glose disponible et le renvoi extrait quand il est identifiable.

**Statut : à vérifier, non importé.** Le renvoi extrait automatiquement est un indice de travail, pas une décision linguistique. Certains renvois peuvent pointer vers plusieurs éléments (par exemple une base et un suffixe) ou contenir des références complexes; ils nécessitent une vérification.

- Tous les segments repérés contiennent une cible de renvoi extractible avec la règle simple utilisée; cela ne signifie pas que chaque cible est linguistiquement confirmée.

### 2. Ne pas supprimer automatiquement les chiffres finaux

La normalisation qui retire les chiffres finaux crée **38 groupes** de formes distinctes dans la revue. Exemples :
- `ba` : `ba1`, `ba2`, `ba3`
- `baabo` : `baabo1`, `baabo2`, `baabo3`
- `baana` : `baana1`, `baana2`
- `baata` : `baata1`, `baata2`
- `baawo` : `baawo1`, `baawo2`, `baawo3`
- `baaxa` : `baaxa1`, `baaxa2`
- `baaye` : `baaye1`, `baaye2`, `baaye3`
- `bado` : `bado1`, `bado2`, `bado3`
- `baga` : `baga1`, `baga2`
- `bajo` : `bajo1`, `bajo2`, `bajo3`
- `banbe` : `banbe1`, `banbe2`
- `baqe` : `baqe1`, `baqe2`, `baqe3`

Ces chiffres peuvent distinguer des homonymes ou des entrées lexicales différentes. Ils ne doivent pas être retirés de la graphie stockée ni servir, seuls, à fusionner des entrées. Pour le contrôle des doublons, garder deux clés séparées : une normalisation orthographique conservatrice et une clé de recherche indicative, sans fusion automatique.

**Cas concret à revoir :** dans le lot 09, `curi1` et `curi2` ont été regroupés par la règle qui retire les chiffres finaux, alors que les segments source donnent des informations différentes (dont le sens « hut » pour `curi2`). Les conserver comme deux formes distinctes dans le contrôle et demander au référent s’il s’agit d’entrées séparées, d’homonymes ou d’une relation à documenter. Ne pas les fusionner automatiquement.

### 3. Lots de validation et base de production

- Le lot 02 contient 120 segments marqués comme validés/importés dans son fichier de suivi.
- Les lots 03 à 09 restent marqués **À VALIDER — NON IMPORTÉ**.
- La base de production reste à **305 entrées** dans ce contrôle; aucune modification n’a été faite à la base.
- L’absence de nouveau candidat distinct après les filtres précédents ne prouve pas que le dictionnaire source est exhaustif ni que chaque sens/variante est déjà représenté dans la base.

## Prochaines étapes recommandées

1. Faire vérifier les renvois par le référent linguistique et rattacher chaque sens/variante à la bonne entrée, sans effacer le texte source.
2. Réviser les règles de dédoublonnage pour préserver les chiffres lexicographiques finaux et distinguer les homonymes des variantes.
3. Comparer les entrées principales et leurs renvois à la base actuelle, puis préparer des propositions d’import distinctes.
4. N’intégrer dans la base que les entrées et sens explicitement validés; conserver la provenance et les exemples.

## Fichiers de référence

- [Revue source de l’enrichissement](revue-enrichissement-dictionnaire-soninke.csv)
- [Base de production](../data/lexique-soninke-fr-base.csv)
- [Lot prioritaire 09](lot-validation-prioritaire-soninke-09.csv)
- [Contrôle détaillé des renvois](controle-renvois-dictionnaire-soninke-2026-10-21.csv)
