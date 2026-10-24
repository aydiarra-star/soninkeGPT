# Extraction du dictionnaire soninké (Google Doc) — 2026-10-24

## Le document

- Source : `docs.google.com/document/d/1as27_XQMTMwFVP8UFV8y6vlfcD9WirpN`
  (lien Drive fourni par le référent).
- Contenu : la portion **B → F** du dictionnaire soninké–anglais–français
  (entrées `ba1` … `fuxu-fuxu`), soit environ **1 100 entrées** réparties en
  44 blocs de texte à l'export brut.
- Chaque entrée suit le modèle :
  `mot   Catégorie. glose anglaise; glose française. exemple soninké / anglais / français. Note: … Plural suffix: …`
- Le document contient des **doublons** (entrées répétées à l'identique) et des
  renvois (`See main entry:`), qu'il faut dédupliquer et marquer, pas traduire.

## Ce qui a été extrait

- `data/candidates/dictionnaire-b-f-extraction-2026-10-24.csv` — 132 entrées
  relevées et vérifiées à la main sur le début du document (`ba1` → `bangandi`),
  colonnes `soninke;francais;categorie;note`.
- Contrôle de recouvrement avec `data/source/lexique-soninke-fr-base.csv` :
  **130 des 132 entrées sont déjà présentes** dans le lexique principal
  (elles viennent de « Dictionnaire soninké.docx », la même source) ; seules
  `baane ti baane` et le suffixe `-bali` manquent.

Conclusion utile : ce document n'est pas une source nouvelle, c'est **la source
déjà exploitée** pour les 481 entrées « Dictionnaire soninké.docx » du lexique.
Le travail restant n'est donc pas de re-saisir les mots, mais de repérer les
**entrées du document absentes du lexique**, puis de les importer avec le même
statut (`candidat_dictionnaire_a_verifier`).

## Outil d'extraction

`scripts/extract_dictionnaire_soninke.py` lit l'export texte d'un Google Doc ou
directement un `.docx`, et produit le CSV `soninke;francais;categorie;
glose_complete;note` :

```bash
python3 scripts/extract_dictionnaire_soninke.py "Dictionnaire soninké.docx" \
        data/candidates/dictionnaire-extraction.csv
```

- sépare la glose anglaise de la glose française sans inventer de sens ;
- découpe les sens multiples (`1 •`, `2 •`), y compris quand le sens continue
  sur la ligne suivante ;
- retire les métadonnées (`Gram`, `Note`, `Plural suffix`, `Underlying form`,
  `Category`, `synonyme`, `See main entry`…) ;
- coupe avant les phrases d'exemple ;
- déduplique les entrées répétées ;
- marque `glose_complete=a_verifier` quand la partie française n'a pas pu être
  isolée avec certitude.

Testé sur des extraits réels du document (gloses correctes, y compris
`ballaade` « poutre, traverse / clavicule » et `banbaado` « pagne pour attacher
un enfant sur le dos / enfance »).

## Suite

1. Déposer le fichier `.docx` (ou l'export `.txt`) du dictionnaire dans le
   dépôt, puis lancer le script : les ~1 100 entrées sont extraites en une
   passe, sans ressaisie manuelle.
2. Comparer avec `data/source/lexique-soninke-fr-base.csv` (normalisation des
   accents et du trait d'union) pour ne garder que les entrées manquantes.
3. Importer ces entrées avec `source = Dictionnaire soninké.docx` et
   `statut = candidat_dictionnaire_a_verifier` ; ne pas créer d'audio et ne pas
   marquer de prononciation validée.

## Import sans doublon (même jour)

Règle appliquée : un mot déjà présent dans le lexique, comme entrée **ou** comme
`variante`, n'est jamais réimporté.

- 132 entrées du lot lues → **130 doublons écartés** (52 avec la même glose,
  28 homonymes numérotés du document déjà regroupés dans un seul article,
  52 avec une glose formulée différemment) → **2 entrées réellement nouvelles** :
  - `SNK-LEX-1437` *baane ti baane* « un à un, un par un » (expression) ;
  - `SNK-LEX-1438` `-bali` « manque de » (suffixe nominal).
- L'import est idempotent : relancé sur le même fichier, il n'ajoute plus rien.
- Journal détaillé : `data/reports/import-extraction-2026-10-24.csv`
  (chaque doublon écarté y figure avec l'entrée du lexique et sa glose).

## Dédoublonnage du lexique existant

Le contrôle `scripts/check_doublons_lexique.py` a révélé des doublons antérieurs
au lot : la même forme saisie deux fois, souvent une entrée « renvoi à X » ou
« variante de X » créée en plus de l'article principal.

- 1 464 entrées au départ → **22 entrées absorbées** → **1 442 entrées**.
- Aucune information perdue : la forme absorbée devient `variante` de l'entrée
  conservée, la glose la plus complète est gardée, et l'entrée conservée reçoit
  une note de fusion avec l'identifiant absorbé, sa glose et son statut.
- Entrées conservées de préférence : celles qui portent un audio
  (`kambe`, `Nene`, `Nuxune`, `Yaxe`) ou le statut de preuve le plus fort.
- 41 formes restent citées dans plusieurs entrées : ce sont des **renvois de
  variantes** (par exemple `Giya`/`yesso`, deux formes attestées ayant chacune
  son audio), pas des doublons d'entrée. Après fusion : **0 doublon d'entrée**.
- Journal : `data/reports/fusions-doublons-2026-10-24.csv` ;
  état des formes : `data/reports/doublons-lexique-2026-10-24.csv`.

Contrôle final : `node tests/ui.test.cjs` et `node tests/voice.test.cjs`
passent après la fusion.

## Deux gloses réparées au passage

La fusion a mis au jour deux entrées dont la glose avait été mal découpée lors
d'un import antérieur (la glose contenait une variante au lieu du sens) :

| Entrée | Ancienne glose | Glose rétablie | Justification |
| --- | --- | --- | --- |
| `SNK-LEX-0219` *bolonŋe* | « bulunŋe ; vestibule » | « petite rue, ruelle ; vestibule » | texte de l'entrée : *1 • path, route; petite rue, ruelle* |
| `SNK-LEX-0491` *biifi* | « hihi » (une de ses variantes) | « jouet, jeu d'enfant » | texte de l'entrée : *toy; jouet, jeu d'enfant* |

## Reste à faire

- Poursuivre l'extraction du document au-delà du lot `b` (blocs suivants) avec
  le même filtre : seules les formes absentes du lexique seront ajoutées.
- Les 40 formes encore citées en variante dans plusieurs entrées
  (`Giya`/`yesso`, `kambe`/`kanbe`…) relèvent d'un arbitrage linguistique : ce
  sont des variantes attestées, pas des doublons, et deux d'entre elles portent
  chacune un audio qu'il ne faut pas perdre.
