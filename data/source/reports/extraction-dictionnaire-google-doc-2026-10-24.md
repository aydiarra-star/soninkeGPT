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
