# Extraction du dictionnaire soninké (Google Doc) — tronçon `ga` → `kuyindi`

**Date :** 2026-10-25
**Source :** Google Doc « Dictionnaire soninké »
`https://docs.google.com/document/d/17DtaXTypfQwpYI0NCuBM1_ZjY9MiBhB_xr18kuLr0qU/edit?usp=drivesdk`
**Couverture :** de `ga` à `kuyindi` (sections g, h, i, j, k) — soit les lettres **g → k**.
**Commande initiale :** « Extraire les mots soninké et leurs traductions françaises » :
1. enlever tout chiffre figurant sur un mot ;
2. supprimer carrément tous les mots anglais ;
3. vérifier qu'il n'y a pas de doublons identiques aux mots du lexique de base.

---

## 1. Collecte

- Le sandbox n'atteint pas `docs.google.com` directement (`curl` impossible) ; le document
  a donc été lu via l'outil de récupération de pages, sur l'export HTML
  (`…/export?format=html`), découpé en **77 tronçons** (~8,6 Ko chacun).
- Les limites de tronçons coupent les entrées : chaque tronçon a été raccordé au
  précédent sans ajout ni perte (vérification de continuité entrée par entrée).
- Dans l'export HTML, la vedette est **collée** au corps de l'entrée et les
  limites d'entrées sont des sauts de ligne ; les liens de renvoi vers
  `media.ipsapps.org` et les exemples bilingues ont été écartés à l'analyse.

## 2. Méthode d'analyse

Chaque entrée du document a été relevée dans un fichier de travail
(`data/source/parts-g/part-NN.tsv`, une ligne par entrée : vedette, glose
française, catégorie, note), puis concaténée sans modification dans le brut
`data/source/dictionnaire-g-k-brut-2026-10-25.tsv` (1 320 lignes).

Règles appliquées au niveau de chaque entrée :

- **Gloses** : la source est bilingue (« english gloss; french gloss »). Seule la
  partie française a été conservée ; les parties anglaises ont été supprimées,
  y compris lorsqu'elles étaient seules (ex. `goloba` « muster, stir up a group
  quickly »). Les gloses sont séparées par « / » (ordre de la source).
- **Exemples, notes de source, liens, métadonnées** (Plural suffix, Underlying
  form, Category, Gram, Anth, Note… : écartés. Les exemples français ne sont pas
  des traductions d'entrée.
- **Doublons internes au document** (plusieurs entrées strictement identiques,
  fréquentes dans ce doc) : écartées, une seule occurrence conservée.
- **Renvois** (« See main entry: … ») : conservés avec la note `renvoi` ; lorsque
  la cible n'a pas de glose française, la ligne reste avec un français vide
  (jamais inventé).
- **Sigles grammaticaux** (`IRRcond`, `HYPO`, `DEF`, `PASS`, `ANTI-PASS`, `SG`,
  `ATTN`, `NEG`, `3plEMP`, `ABIL`…) : ce ne sont pas des mots anglais mais des
  codes de glossage ; conservés et signalés en note (`sigle non traduit`).
- **Variantes graphiques** (`Variant: …`) : conservées en note, non dupliquées.

## 3. Nettoyage demandé

### 3.1 Chiffres retirés des vedettes
Tout chiffre a été retiré (`gaara1` → `gaara`, `kati3` → `kati`, `-i2` → `-i`).
Les homonymes numérotés fusionnent ensuite en un seul article, gloses jointes
par « / » — ex. `gide` : « grand frère, grande soeur (…) / pierre, montagne,
colline » ; `jaara` : « soigner, traiter, guérir / pouvoir, connaissance /
jabot / Mesure soninké (approximativement 1 mètre) ».
Contrôle automatique : **aucun chiffre** ne subsiste dans les vedettes des CSV.

### 3.2 Mots anglais supprimés
13 entrées avaient une glose exclusivement anglaise ; leur français est laissé
**vide** (« on n'invente rien »), la note porte `sans traduction française
(« … » supprimé)`. Exemples : `goloba`, `guboqu`, `guci`, `kanbadoosaade`
(« toothpick »), `karabata` (« forcefully »), `kapa` (« put together »),
`kore2` (« poverty »), `fariganka` (« warm blooded »), `gobo`/`goqi` (sens 2
« multiply » retiré), `guufa2` (« "afro look" » retiré), etc.
Quelques mots anglais **à l'intérieur** d'une glose ont été supprimés
(`kaananke` : « dirigeant, leader » → « dirigeant »). Contrôle automatique
final sur les CSV : aucun mot anglais résiduel.

### 3.3 Absence de doublons avec le lexique de base
Comparaison avec `data/source/lexique-soninke-fr-base.csv` selon la règle déjà
en vigueur (`scripts/import_extraction_sans_doublons.py`, fonction `cle`) :
un mot présent comme **entrée OU comme variante** du lexique est écarté, même si
sa glose diffère. Les homographes de casse distincts du document (`hari`/`Hari`,
`jaru`/`Jaru`, `jawune`/`Jawune`, `juma`/`Juma`, `jaabi`/`Jaabi`) sont conservés
séparément (ce ne sont pas des doublons identiques), signalés dans le journal.

## 4. Résultats

| Étape | Volume |
|---|---|
| Lignes d'analyse (76 fichiers de parties) | 1 320 |
| Entrées après retrait des chiffres et fusion des homonymes | **1 283** |
| — dont sans traduction française (renvois nus + anglais supprimé) | 110 |
| Doublons avec le lexique de base écartés | **86** |
| **Nouveaux mots (absents du lexique de base)** | **1 087** |

Répartition des 1 283 entrées : g (308), h (86), i (14), j (361), k (483),
plus 31 formes composées dérivées référencées sous des vedettes g–k
(`allankanne`, `batikanxoore`, `fankitte`, `mexenkace`, `nuxudunkutu`,
`sadaxakiɲandaana`, `tunkarankorosi`, `xarankonpe`…).

Doublons écartés notables (déjà au lexique) : `gaba`, `gabe`, `gaja`, `gara`,
`geeji`, `gide`, `giri`, `giya`, `gongo`, `gonme`, `guma`, `gunne`, `ji`, `ka`,
`kame`, `kari`, `kini`, `koosi`, `kunke`, `kuyi`, `fate`, `fariganka` (dont la
glose de base « à sang chaud » a déjà été traduite au lot précédent), etc. La
liste complète figure dans le CSV de comparaison, avec pour chacun la glose de
base et la nouvelle glose (utile pour un futur enrichissement manuel).

## 5. Livrables

| Fichier | Contenu |
|---|---|
| `data/source/dictionnaire-g-k-brut-2026-10-25.tsv` | relevé brut des 1 320 lignes d'analyse (chiffres d'homonyme conservés) |
| `data/candidates/dictionnaire-g-k-extraction-2026-10-25.csv` | 1 283 entrées nettoyées (`soninke;francais;categorie;note`), tri alphabétique |
| `data/candidates/dictionnaire-g-k-nouveaux-2026-10-25.csv` | 1 087 nouveaux mots garantis absents du lexique de base |
| `data/reports/comparaison-dictionnaire-g-k-2026-10-25.csv` | audit : `nouveau`, `doublon_ecarte_glose_identique`, `doublon_ecarte_glose_differente`, `glose_vide` |
| `scripts/traiter_extraction_g_k.py` | pipeline reproductible (fusion, chiffres, anglais, comparaison) |

## 6. Portée et suites possibles

- **Aucune modification du lexique de base** : la demande portait sur l'extraction
  et le contrôle des doublons. L'import éventuel se fera avec la règle
  anti-doublons existante (`scripts/import_extraction_sans_doublons.py`), qui
  restera idempotent.
- Les 110 entrées sans traduction française sont conservées dans le CSV
  d'extraction (statut `glose_vide`) : ce sont surtout des renvois vers une
  vedette principale ; les quelques entrées à glose anglaise seule attendent une
  traduction humaine — rien n'a été inventé.
- Les gloses `doublon_ecarte_glose_differente` (86) documentent des sens
  supplémentaires par rapport au lexique de base (ex. `koro` : « semoir »,
  « échapper (cheval) ») : à examiner si le lexique doit être enrichi plutôt que
  simplement complété.
