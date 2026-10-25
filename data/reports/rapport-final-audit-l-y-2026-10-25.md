# Rapport Final d’Audit Linguistique, Technique et d’Architecture — Dictionnaire Soninké–Français L–Y (PR #41)

- **Date de l’audit** : `2026-10-25`
- **Pull Request auditée** : [`aydiarra-star/soninkeGPT#41`](https://github.com/aydiarra-star/soninkeGPT/pull/41)
- **Branche de session** : `arena/632df384-soninkegpt` (statut `pr_open`, non fusionnée)
- **Commit initial audité (baseline PR #41)** : `e8e70afc4228db5a1f49c05c7925e87e0b111394`
- **Référentiel canonique protégé (lecture seule)** : `data/source/lexique-soninke-fr-base.csv` (`3 328` entrées, `SNK-LEX-0001` à `SNK-LEX-3327`, **aucune modification**)
- **Fichiers audio WAV et manifestes vocaux** : **aucune modification** (`audio/`, `data/voice-memory.json`, `data/source/manifest-577-review.csv`)

---

## 1. Verdict exécutif

### Verdict sur le commit initial `e8e70afc` de la PR #41 : **REFUS D’INTÉGRATION DIRECTE EN L’ÉTAT**

L’audit indépendant ligne à ligne de l’archive brute `data/source/dictionnaire-l-y-brut-2026-10-25.txt` (`8 600` lignes, `4 297` paragraphes couvrant les 16 lettres `L, M, N, Ɲ, Ŋ, O, P, Q, R, S, T, U, V, W, X, Y`), du script `scripts/extraire_nettoyer_dictionnaire_l_y.py` et de toutes les sorties de la PR #41 démontre que **l’intégration brute dans `lexique-soninke-fr-base.csv` aurait corrompu le lexique canonique** pour onze raisons techniques et linguistiques prouvées (voir §3).

### Verdict après correction du pipeline sur la branche d’audit : **PRÊT POUR INTÉGRATION PARTIELLE CONTRÔLÉE PAR LOTS, SOUS CONDITION D’AUTORISATION EXPLICITE DE L’UTILISATEUR**

Tous les défauts démontrables du pipeline `scripts/extraire_nettoyer_dictionnaire_l_y.py` ont été corrigés et couverts par des tests automatisés (`tests/dict_l_y_pipeline.test.py`), sans toucher à `data/source/lexique-soninke-fr-base.csv`, ni à `main`, ni aux fichiers audio, et **sans fusionner la PR #41**.

| Indicateur | PR #41 initiale (`e8e70afc`) | Après correction du pipeline | Écart & explication vérifiée |
|---|---:|---:|---|
| Paragraphes lus dans `brut` | `4 297` | `4 297` | Source brute intacte (SHA-256 inchangé, Mojibake réparé en mémoire) |
| Entrées dédupliquées analysées | `3 429` | `3 427` | Rattachement des 2 fragments botaniques orphelins (`L3879`, `L4893`) |
| **Mots candidats publiés** (`mots-importables`) | `2 299` | **`2 304`** | `-14` faux positifs retirés (5 anglais, 6 doublons base, 3 homonymes masqués) / `+19` mots attestés récupérés |
| — dont prêts haute confiance (`a_verifier_par_locuteur=non`) | non qualifié | **`2 223`** | `2 077` validés tels quels + `130` gloses/catégories corrigées + `16` mots récupérés |
| — dont soumis à validation locuteur (`a_verifier_par_locuteur=oui`) | non qualifié | **`81`** | 39 homographes jumeaux sans FR, 23 liens dialectaux vers la base, 19 cas métalinguistiques/coquilles SIL |
| **Expressions candidates publiées** (`expressions-importables`) | `514` | **`588`** | `20` locutions lexicales multi-mots + `568` paires de phrases attestées (`-19` entrées bruitées/reclassées, `+93` corrigées/récupérées) |
| **Groupes d’homonymes internes isolés** (`collisions-homonymes`) | `165` | **`169`** | `+4` collisions non numérotées ou passives démasquées (`saxu`, `suure`, `tefu`, `toro`), `0` fusion automatique |
| Doublons / correspondances tête ou variante avec le lexique base | `349` | **`360`** | `+11` doublons détectés via `ñ=ɲ`, variantes `;`/`|` et accent (`yigandé`) + `25` liens inverses variante→base documentés |
| Renvois sans glose française (`renvois-sans-glose`) | `416` | **`403`** | Nettoyage des `See main entry: .` vides et récupération des entrées traduites |
| Exclusions sans glose française (`exclusions-anglais`) | `470` | **`455`** | `+5` noms propres anglais exclus, `-20` vraies entrées françaises indûment exclues récupérées |

---

## 2. Contrôle d’intégrité des fichiers de la PR #41 et du référentiel canonique

Les 9 fichiers introduits par la PR #41 ont été intégralement contrôlés :
1. `data/source/dictionnaire-l-y-brut-2026-10-25.txt` (`8 600` lignes, `476 742` octets) : archive brute SIL/IPS complète des lettres `L` à `Y` (ordre SIL plaçant `U` et `V` avant `R` aux lignes `L2563` et `L2569`, et `R` à `L2577`).
2. `data/candidates/dictionnaire-l-y-mots-importables-2026-10-25.csv` : format 5 colonnes `;` (`soninke;francais;categorie;variantes;note`).
3. `data/candidates/dictionnaire-l-y-expressions-importables-2026-10-25.csv` : format 5 colonnes `;` séparé des mots simples.
4. `data/reports/comparaison-dictionnaire-l-y-2026-10-25.csv`.
5. `data/reports/collisions-homonymes-dictionnaire-l-y-2026-10-25.csv`.
6. `data/reports/renvois-sans-glose-dictionnaire-l-y-2026-10-25.csv`.
7. `data/reports/exclusions-anglais-dictionnaire-l-y-2026-10-25.csv`.
8. `data/reports/nettoyage-dictionnaire-l-y-2026-10-25.csv`.
9. `scripts/extraire_nettoyer_dictionnaire_l_y.py`.

**Garanties d’intégrité vérifiées** :
- `data/source/lexique-soninke-fr-base.csv` : **0 octet modifié** (`git diff data/source/lexique-soninke-fr-base.csv` vide, `check_doublons_lexique.py --strict` vert).
- Fichiers WAV et manifestes audio : **0 fichier modifié**.
- Déterminisme du pipeline : deux exécutions consécutives de `python3 scripts/extraire_nettoyer_dictionnaire_l_y.py` produisent des empreintes **SHA-256 strictement identiques** sur les 7 fichiers générés.

---

## 3. Audit technique du pipeline (`scripts/extraire_nettoyer_dictionnaire_l_y.py`) — 11 défauts démontrés et corrigés

### Défaut 1 — Confusion entre sigles grammaticaux mixtes et le mot français « mot »
- **Constat dans `e8e70afc`** : `est_sigle()` utilisait `t.upper() in SIGLES` où `SIGLES` contenait `"MOT"` et ignorait la casse. Résultat inverse double :
  - les sigles mixtes `PROintrg` et `DETintrg` fuyaient dans `mots-importables` (`minnanke` → `PROintrg`, source `L1951` ; `manime` → `… / DETintrg Combien?`, source `L759`) ;
  - le nom français légitime **`mot`** était rejeté comme sigle, excluant à tort `renxotte` (`word; mot`, `L2891`) et `sefeta` (`word; mot`, `L3653`).
- **Correction** : remplacement par `SIGLES_EXACTS` sans `"MOT"` + nettoyage des préfixes grammaticaux `DETintrg`/`PROintrg`/`RELtemp`/`REFndef` collés devant une vraie glose française + rejet des numéros isolés (`4` dans `na`, `L1697`).

### Défaut 2 — Non-reconnaissance de `verbe passif (intransitif).` et inversion actif/passif (20 entrées touchées)
- **Constat dans `e8e70afc`** : `_POS_ALT` reconnaissait `verbe passif.` mais échouait devant la parenthèse `verbe passif (intransitif).`. Sur **`safe`** (`L3195`, `L3215`), la vraie glose passive `be written; être écrit(e)` était ignorée et remplacée par `summary-definition: write; écrire`, **inversant le sens passif en sens actif (« écrire »)** ! En outre, 5 verbes passifs attestés étaient exclus (`lange` `L125`, `leebi` `L227`, `liike` `L415`, `ŋaami` `L2493`, `tuti` `L6042`), `suure2` (`être nettoyé`, `L4721`) était perdu (masquant la collision d’homonymes `suure1`/`suure2`), et 6 entrées perdaient leur catégorie `verbe` (`loxose` `L529`, `mare` `L817`, `tafi` `L4901`, `xate` `L7058`, `yonke` `L8502`).
- **Correction** : prise en charge des qualificatifs parenthésés `(?:\s*\([^)]+\))?` dans `_POS_ALT` et interdiction d’injecter un `summary-definition:` actif dans une entrée marquée `verbe passif`.

### Défaut 3 — Troncatures de gloses dans `region_apres()` et retrait asymétrique des guillemets
- **Constat dans `e8e70afc`** : `region_apres()` coupait au premier `.` ou `!`, provoquant :
  - l’exclusion totale de `lanbo` (`plain (geol.); plaine`, `L111`), `wandaana` (`1.5m; poisson noir et long, 1,5m`, `L6216`) et `teŋi` (`head towards..; s'orienter vers`, `L5310`) ;
  - la troncature au milieu d’une parenthèse ou citation sur `xeɲexeɲe` (`(i.e. une affaire)`, `L7193`), `-lenme` (`L349`), `ra1` (`L2803`), `ra nta a yi` (`L2805`), `ra wa a yi` (`L2807`), `siri` (`L4127`), `taaretaare` (`L4867`) et `moro2` (`interjection : c'est faux ! mensonge !`, `L1217`) ;
  - le collage de la phrase d’exemple derrière `?` sur `manime` (`L759`) et `safindi` (`L3219`) ;
  - l’interprétation erronée du français `, lit.` comme l’abréviation `lit.` sur `soxufo` (`L4449`).
- **Correction** : suivi équilibré des parenthèses fermées dans la glose (sans déborder sur les parenthèses source non fermées comme `xesu2` `couper (herbe .`), suivi des guillemets appariés, arrêt propre à toute frontière `\b\d+\s*•`, préservation des décimales `1.5m` et des suites françaises après `!` en minuscule, et retrait de guillemets uniquement lorsqu’ils encadrent toute la chaîne.

### Défaut 4 — Perte systématique des sous-gloses françaises multiples séparées par `;` et de l’ordre inversé `FR; EN`
- **Constat dans `e8e70afc`** : `segment_vers_francais()` ne retenait que le **dernier** fragment après `;`, détruisant les sens français antérieurs sur plus de 20 entrées (`lagari` perdait `être le dernier`, `marandindaana` perdait `président`, `matugunne` et `maxoore` perdaient `tante`, `regaana` ne gardait que `danseuse` en perdant `danseur`, `sellandi` ne gardait que `dehors` en perdant `balayer`, `tanŋi` perdait `manque d'argent`, `xiti` perdait `annoncer un décès`, `xonji` perdait `alcool`). Inversement, l’ordre `FR; EN` sans accent de `senbekite` (`devenir fort(e); grow strong`, `L3771`) provoquait son exclusion.
- **Correction** : extraction ordonnée de toutes les sous-gloses françaises dans `_choisir_parties_francaises()`, rattachement des précisions parenthétiques `(veau, poulain, etc.)`, et détection de l’ordre inversé `FR; EN` (`soxokomaaxu` `L4401`, `senbekite` `L3771`).

### Défaut 5 — Fuite de 5 noms propres en anglais dans `mots-importables`
- **Constat dans `e8e70afc`** : la source SIL répète le nom anglais des deux côtés du `;` (`Egypt; Egypt.`, `Solomon; Solomon.`), laissant passer **5 gloses 100 % anglaises** dans `mots-importables` : `Lajine` → `Guinea Conakry` (`L99`), `Misira` → `Egypt` (`L1135`), `Samariya` → `Samaria` (`L3361`), `Silemaanu` → `Solomon` (`L4037`), `Xuraane` → `Qur'an` (`L7780`).
- **Correction** : exclusion stricte dans `EN_PROPRES_EXCLUS` **sans inventer aucune traduction française** (conformément à la règle impérative n° 3) ; ces 5 entrées sont documentées pour traduction par un locuteur/éditeur habilité.

### Défaut 6 — Exclusion d’entrées françaises sans `;` ou sans étiquette grammaticale
- **Constat dans `e8e70afc`** : `tunkanyugo` (`roi`, `L5980`) et `yigi-yigi` (`secouer`, `L8340`) ont une glose française directe sans `;` ; `wujune` (`thousand; mille`, `L6480`) et `ɲaaye` (`act, deed; action`, `L2181`) n’ont pas d’étiquette `Nom .` avant `EN; FR.`. Toutes quatre étaient exclues à tort.
- **Correction** : récupération contrôlée des gloses françaises attestées sans `;` et lecture de `EN; FR.` après `Variant:` / `See main entry:` lorsque l’étiquette de catégorie manque dans SIL.

### Défaut 7 — Doublons/concaténations issus de `summary-definition:` et faux drapeaux `renvoi`
- **Constat dans `e8e70afc`** : `summary-definition:` concatène les sens sans ponctuation dans l’export SIL, produisant des doublons dégradés (`wurundaana` : `conducteur, chauffeur / fileuse / conducteur, chauffeur fileuse`, `L6552` ; `sigindi` : `ériger / arrêter / établir, promouvoir / ériger arrêter établir, promouvoir`, `L3945` ; `meerabatunte` : `successive / sucsessive` [coquille SIL], `L935` ; `laabeye` : `l'hygiène / hygiène` ; inversions d’index `retourner (faire)`). Par ailleurs, `239` entrées comportant `See main entry: .` (cible vide !) recevaient à tort la note `renvoi`.
- **Correction** : dédoublonnage lexical insensible à l’article défini initial, suppression des résumés dont tous les mots significatifs figurent déjà dans les sens du corps (tout en conservant les vrais synonymes complémentaires comme `concave` sur `lupurante` `L559` ou `baptême` sur `siyinde` `L4161`), et restriction de `renvoi` aux seules cibles non vides (`a_renvoi_reel()`).

### Défaut 8 — Segmentation de `nVcv-pattern: NV`, fragments botaniques et têtes doubles de mots simples
- **Constat dans `e8e70afc`** :
  - l’enregistrement sans tête `nVcv-pattern: NV.Verbe. verb marker; suffixe verbale.` (`L2129`) était publié comme « expression soninkée » `nVcv-pattern: NV` ;
  - deux lignes taxonomiques coupées par un saut de paragraphe (`Bombax costatum.Note: D2 • …` `L3879`, `Combretum eliotii.synonyme: …` `L4893`) créaient de fausses entrées latines ;
  - cinq entrées simples à double graphie (`seegi seegu` `L3619`, `Ɲatu, Takko` `L2263`, `Tanba, Sanba` `L4983`, `Taqqi, Pate` `L5124`, `Yera, Denba` `L8200`) étaient classées comme `expressions` multi-mots au lieu de mots simples avec variantes.
- **Correction** : exclusion de l’en-tête `nVcv-pattern: NV` (tout en sauvegardant sa paire d’exemple attestée `Lenki gollen…` `L2129`), rattachement des fragments botaniques à leur entrée parente, retrait du binôme latin `, Cenchrus biflorus` dans `xiine` (`L7286`), et reclassement des 5 têtes doubles dans `mots-importables` avec rattachement de la variante (`Taqqi` + `Pate`, `Yera` + `Denba`, `seegi` + `seegu`, etc.).

### Défaut 9 — Contamination et altérations dans `expressions-importables`
- **Constat dans `e8e70afc`** :
  - **1 phrase anglaise publiée dans la colonne `soninke`** : `I was in town` → `J'étais en ville` (issue de `saqa2` `L1955`, où la phrase soninkée manquait dans SIL) ;
  - **2 préfixes bibliographiques collés** : `Diagana :A ma ɲi…` (`L7028`) et `Diagana :An na ɲaŋana…` (`L2247`) ;
  - **2 fuites `.antonyme:`** dans la traduction française (`L2499`, `L6308`) ;
  - **2 phrases soninkées collées après un point devant `Ɲ`** (`…mouillée.Ɲiiɲe sefi` `L3685`, `…tam-tam.Ɲamaxalun…` `L481`) car `decouper_phrases()` ignorait les majuscules soninkées `Ŋ` et `Ɲ` ;
  - **2 nombres réels détruits** par `sans_chiffres()` : `1993 siine` → `siine` alors que le français disait `en 1993` (`L1837`), et `9-hur` → `-hur` alors que le français disait `avant 9h` (`L859`).
- **Correction** : filtrage anglais côté soninké sans bloquer les pronoms soninkés `A` (« il/elle ») ni `An` (« tu »), nettoyage de `Diagana 1994:…` avec préservation de la majuscule suivante, coupure avant `META_CUT`, ajout de `ŊƝƁƊƳ` dans `decouper_phrases()`, et retrait sélectif des seuls chiffres d’homonyme collés à une lettre (`ɲiiɲe1` → `ɲiiɲe`, `1993` et `9-hur` préservés). Cette correction a également permis de récupérer **85 paires de phrases attestées supplémentaires** parfaitement propres.

### Défaut 10 — Collisions d’homonymes non numérotées écrasées par `doublon_interne`
- **Constat dans `e8e70afc`** : `collisions` n’était déclenché que si `len({hw_raw}) > 1`. Lorsque SIL avait omis les numéros d’homonyme sur deux entrées distinctes de même graphie, la première était publiée dans `mots-importables` et la seconde silencieusement jetée en `doublon_interne` ! Trois cas majeurs découverts :
  - **`toro`** : `L5752` (`fig tree; figuier`) écrasait `L5754` (`ear; oreille`) ;
  - **`tefu`** : `L5234` (`shoe; chaussure`) écrasait `L5236` (`shoe; chasseur` — coquille française probable de SIL pour *chaussure*, ou homonyme *chasseur*) ;
  - **`saxu`** : `L3549`/`L3551` (`coucher`) et `L3555` (`croire, faire confiance à, confier`).
- **Correction** : détection de collision dès que `len(raws) > 1` **ou** `len(gloses_norm) > 1`, isolant les **169 groupes** sans aucune perte ni fusion silencieuse. De plus, lorsqu’une entrée publiée possède dans `brut` un homographe jumeau dépourvu de glose française (`39` mots, ex. `lasame` face à `lasame2`, `moro` face à `moro1`), la note `homographe source sans glose FR: …` et le drapeau `a_verifier_par_locuteur = oui` sont systématiquement posés.

### Défaut 11 — Comparaison incomplète avec `lexique-soninke-fr-base.csv` et séquences Mojibake
- **Constat dans `e8e70afc`** :
  - `cle()` ne normalisait pas `ñ → ɲ` (contrairement à `normalizeLexicalKey()` dans `app.js` et `tests/voice.test.cjs`), laissant passer **`ɲiime`** (`L2363`, collision fatale avec `SNK-LEX-0738 ñiime`) et **`segeɲe`** (`L3687`, collision fatale avec `SNK-LEX-0753 segeñe`) — ce qui aurait fait **échouer `node tests/voice.test.cjs` dès l’intégration** !
  - `charger_lexique()` ne découpait `variantes` que sur `,`, ignorant `;` et `|` utilisés dans `SNK-LEX-0275..0290, 0707, 0749`, laissant passer **`raqe`** (`SNK-LEX-0282`), **`teŋe`** (`SNK-LEX-0278`), **`toro`** (`SNK-LEX-0288`, `0749`) et **`yinkolla`** (`SNK-LEX-0275`, `0707`) ;
  - **`yigande`** (`nourriture`, `L8320`) n’était pas rapproché de `SNK-LEX-0905 yigandé` (`nourriture`, accent final français dans la base) ;
  - `61` séquences Mojibake UTF-8/CP1252 dans `brut` (`Å‹` pour `ŋ`, `É²` pour `ɲ`, `Ã©` pour `é`, etc.) n’étaient pas réparées en amont.
- **Correction** : réparation Mojibake en mémoire dès `charger_paragraphes()`, alignement exact de `cle_soninkegpt()` sur `normalizeLexicalKey()` (`ñ → ɲ`), découpage des variantes canoniques sur `[,;|]`, et rapprochement contrôlé sans accent lorsque le sens français concorde (`yigande` ↔ `SNK-LEX-0905`).

---

## 4. Résultats détaillés des 4 livrables CSV d’audit

### 4.1 Audit des mots candidats — `data/reports/audit-l-y-mots-2026-10-25.csv` (`2 318` entrées auditées)
Couvre l’union exhaustive des `2 299` mots de la PR #41 initiale et des `2 304` mots issus du pipeline corrigé :
- **`VALIDE_PRET_POUR_INTEGRATION` (`2 077`)** : provenance brute, sens français, catégorie grammaticale, variantes, absence d’anglais et orthographe soninkée (`ŋ`, `ɲ`, voyelles longues, tirets) vérifiés (`a_verifier_par_locuteur = non`).
- **`CORRIGE_PIPELINE_PRET` (`130`)** : entrées dont la glose française, la catégorie (`verbe` passif) ou les variantes ont été restaurées ou nettoyées fidèlement d’après `brut` (`safe`, `minnanke`, `manime`, `soxufo`, `loxose`, `marandindaana`, `tanŋi`, `wurundaana`, `sigindi`, `xiine`, etc. ; `a_verifier_par_locuteur = non`).
- **`NOUVEAU_RECUPERE_PIPELINE` (`16`)** : mots attestés à haute confiance récupérés par correction du pipeline (`lanbo`, `lange`, `leebi`, `liike`, `renxotte`, `sefeta`, `teŋi`, `tunkanyugo`, `tuti`, `wandaana`, `yigi-yigi`, `ŋaami`, `Tanba`, `Taqqi`, `Yera`, `Ɲatu` ; `a_verifier_par_locuteur = non`).
- **`A_VERIFIER_PAR_LOCUTEUR` (`81`)** (`a_verifier_par_locuteur = oui`) :
  - `39` entrées possédant un homographe jumeau sans glose française dans `brut` après retrait du chiffre éditorial ;
  - `23` entrées dont une variante source correspond déjà à une entrée du lexique canonique (ex. `loxo` → `roxo` `SNK-LEX-0089`, `seegi` → `seegu` `SNK-LEX-0805`, `soxuba` → `suxuba` `SNK-LEX-0872`, `wujune` → `wujine` `SNK-LEX-0933`, `xaba` → `kaba` `SNK-LEX-0895`, `yaxi` → `yexi` `SNK-LEX-0072`), nécessitant d’arbitrer entre rattachement en variante et maintien d’une entrée dialectale distincte ;
  - `19` entrées présentant une incertitude éditoriale SIL (`safindi` → `baptiser?` `L3219`), une coquille française SIL (`tepu` → `chausseurs` `L5324`, `riibayigaana` → `faut profit` `L2925`), une absence de catégorie (`ɲaaye` `L2181`) ou une définition métalinguistique grammaticale (`-lenme`, `ra`, `siri`, `maxabogunte`, `yogo`).
- **Entrées retirées de `mots-importables` par rapport à `e8e70afc` (`14`)** :
  - `EXCLU_ANGLAIS_SANS_FR` (`5`) : `Lajine`, `Misira`, `Samariya`, `Silemaanu`, `Xuraane` ;
  - `DOUBLON_LEXIQUE_BASE_ECARTE` (`7`) : `raqe` (`SNK-LEX-0282`), `segeɲe` (`SNK-LEX-0753`), `teŋe` (`SNK-LEX-0278`), `toro` (`SNK-LEX-0288` + collision interne `L5752`/`L5754`), `yigande` (`SNK-LEX-0905`), `yinkolla` (`SNK-LEX-0275`), `ɲiime` (`SNK-LEX-0738`) ;
  - `COLLISION_HOMONYME_ECARTEE` (`2`) : `suure` (`L4721`/`L4723`) et `tefu` (`L5234`/`L5236`).

### 4.2 Arbitrage des homonymes — `data/reports/arbitrage-homonymes-l-y-2026-10-25.csv` (`169` groupes)
Chaque groupe conserve les formes sources exactes (numéros, tirets d’affixes, majuscules), les lignes vérifiées dans `brut`, les sens français par entrée et les preuves morphologiques (`POS`, `Underlying form`, `Plural suffix`, `See main entry`) :
- **`MAINTENIR_ENTREES_SEPAREES` (`154` groupes)** :
  - `77` groupes d’homonymes de catégories grammaticales différentes (ex. `la1` verbe « protéger » vs `la2` postposition ; `tu1` verbe « connaître, savoir » vs `tu2` verbe « cracher » / nom) ;
  - `75` groupes d’homonymes lexicaux de même catégorie mais de sens et/ou schèmes morphologiques distincts (ex. `suure1` nom « plat de mil » `L4723` vs `suure2` verbe passif « être nettoyé » `L4721` ; `wasa1` « détacher » vs `wasa2` « suffire ») ;
  - `2` groupes non numérotés dans SIL à sens disjoints (`saxu` `L3549`/`L3555` « coucher » vs « croire, faire confiance à » ; `toro` `L5752`/`L5754` « figuier » vs « oreille »).
- **`MAINTENIR_SEPARES_AFFIXE_ET_MOT` (`9` groupes)** : opposition morphème lié à tiret vs mot autonome (`-la` / `la`, `-ma` / `ma`, `-maxa-` / `maxa`, `-n` / `n`, `-na` / `na`, `-ndi` / `ndi`, `-nta` / `nta`, `-o` / `o`, `-u` / `u`).
- **`MAINTENIR_SEPARES_PROPRE_ET_COMMUN` (`5` groupes)** : opposition majuscule/minuscule nom propre vs nom commun (`Malle`/`malle`, `Saane`/`saane`, `Saare`/`saare`, `Silla`/`silla`, `Ture`/`ture`).
- **`COQUILLE_SIL_PROBABLE_A_ARBITRER` (`1` groupe)** : `tefu` opposant `shoe; chaussure` (`L5234`) à `shoe; chasseur` (`L5236`, probable coquille française dans SIL pour *chaussure*, maintenue séparée jusqu’à validation humaine).
- **Recouvrement avec le lexique canonique** : **`37` des `169` clés** existent déjà dans `lexique-soninke-fr-base.csv` (ex. `ma`, `maxa`, `muxu`, `n`, `na`, `noxo`, `nta`, `o`, `saane`, `saare`, `saxa`, `toro`) avec un seul de leurs sens ; l’arbitrage évite à la fois l’écrasement du sens canonique et la perte des homonymes L–Y.

### 4.3 Audit des expressions — `data/reports/audit-l-y-expressions-2026-10-25.csv` (`607` lignes auditées, `588` retenues)
Les expressions sont maintenues dans un fichier séparé (`dictionnaire-l-y-expressions-importables-2026-10-25.csv`) et réparties explicitement en deux sous-ensembles :
1. **`locution_lexicale` (`20` retenues)** : vraies unités lexicales polylexicales (`ra wa a yi` `L2807`, `ra nta a yi` `L2805`, `yaaxen bogu` `L7914`, `mexen su` `L997`, `na ... ŋa` `L1695`, etc.).
2. **`paire_phrase_attestee` (`568` retenues)** : phrases soninkées complètes associées à leur traduction française exacte dans SIL (`0` mot anglais résiduel, `0` doublon avec `lexique-soninke-fr-base.csv`, `soninke-samples.jsonl` ou `PHRASEBOOK`, nombres réels `1993` et `9-hur` intacts, ponctuation et pronoms initiaux `A` / `An` préservés ; `4` entrées signalées `a_verifier_par_locuteur = oui` pour notation fléchée `->` ou citation grammaticale).

### 4.4 Audit complet des doublons contre le lexique canonique — `data/reports/audit-doublons-l-y-2026-10-25.csv` (`3 427` entrées)
Contrairement à une simple comparaison sur `soninke` exact, l’audit compare **les `3 427` entrées L–Y** à la fois aux **mots principaux** et aux **variantes** (`[,;|]`) du lexique canonique, en forme exacte, normalisée (`ñ=ɲ`, casse, tirets) et sans accent :

| Classification réglementaire | Total sur les 3 427 entrées L–Y | Dont entrées ayant une correspondance directe (tête ou variante) dans `lexique-soninke-fr-base.csv` (`385` avec glose FR) | Règle d’action |
|---|---:|---:|---|
| `NOUVELLE_ENTREE` | `2 252` | `0` | Intégrable après validation utilisateur |
| `DOUBLON_IDENTIQUE` | `143` | `143` | Ne pas réimporter (déjà couvert à l’identique dans la base) |
| `ENRICHISSEMENT_POTENTIEL` | `103` | `103` | Sens ou nuances complémentaires à proposer pour enrichissement contrôlé de l’entrée existante |
| `HOMONYME_OU_POLYSEMIE` | `385` | `105` (+ `280` internes L–Y hors base) | **Interdiction de fusion automatique** ; arbitrage humain requis |
| `VARIANTE_A_RATTACHER` | `22` | `22` | Forme ou variante dialectale attestée (`loxo`/`roxo`, `seegi`/`seegu`, `soxuba`/`suxuba`, `wujune`/`wujine`, `xaba`/`kaba`, `yaxi`/`yexi`, etc.) à rattacher à l’entrée existante après validation |
| `A_VALIDER_PAR_LOCUTEUR` | `60` | `12` (+ `48` hors base) | Cas ambigus (collision homographique de variante monosyllabique `n`, `xa`, `o`, `ta`, homographes sans FR, catégorie absente) |
| `TRADUCTION_A_VERIFIER` | `6` | `0` | Coquilles ou `?` dans la glose française SIL (`safindi`, `tepu`, `riibayigaana`, `yogo`, `sallifana`, `moxonsirondi`) |
| `EXCLU_AVEC_JUSTIFICATION` | `456` | `0` (gloses anglaises/sigles) | `455` entrées sans traduction française publiable + `1` bruit `nVcv-pattern: NV` |

> **Constat critique** : il serait **faux** d’affirmer « zéro doublon » sur la seule foi du filtre automatique de `mots-importables`. D’une part, `23` mots candidats ont une variante source déjà présente comme entrée canonique (`VARIANTE_A_RATTACHER` / `A_VALIDER_PAR_LOCUTEUR`) ; d’autre part, parmi les `360` entrées filtrées comme `doublon_lexique`, seules `143` sont strictement identiques tandis que **`103` constituent des enrichissements potentiels** et **`105` sont des homonymes ou sens disjoints** qu’un simple rejet silencieux ferait perdre s’ils n’étaient pas tracés dans `audit-doublons-l-y-2026-10-25.csv`.

---

## 5. Audit de compatibilité avec l’application SoninkeGPT (`app.js`, `tests/ui.test.cjs`, `tests/voice.test.cjs`)

L’inspection du code source d’exécution (`app.js`, lignes `13–22`, `309–344`, `1092–1104`, `1763–1776`, `3789–3955`) et des suites de tests (`tests/voice.test.cjs`, `tests/ui.test.cjs`) établit les faits suivants :

1. **Fichiers réellement chargés au démarrage (`DATA_PATHS`, `app.js:13-22` et `loadAllData()`, `app.js:3789-3827`)** :
   - `data/source/lexique-soninke-fr-base.csv` (lexique principal, séparateur `;`) ;
   - `data/source/manifest-577-review.csv` et `data/source/phrases-36-review.csv` (statuts audio validés) ;
   - `data/source/external-lexicon-candidates.csv` (séparateur `,`, non autoritatif) ;
   - `data/source/soninke-samples.jsonl` (corpus parallèle d’exemples/phrases) ;
   - `data/voice-memory.json` (manifeste vocal).
   - **Conséquence** : les fichiers `data/candidates/dictionnaire-l-y-*.csv` ne sont **pas** chargés automatiquement par l’application tant qu’une étape d’intégration dédiée n’est pas exécutée après autorisation.

2. **Écart de schéma CSV entre les candidats L–Y (5 colonnes) et le lexique canonique (10 colonnes)** :
   - `lexique-soninke-fr-base.csv` exige 10 colonnes exactes : `id;soninke;francais;categorie;variantes;exemple_snk;exemple_fr;source;statut;note` (identifiants séquentiels `SNK-LEX-XXXX`, actuellement jusqu’à `SNK-LEX-3327`).
   - Les fichiers candidats L–Y comportent 5 colonnes (`soninke;francais;categorie;variantes;note`). Lors de l’intégration future autorisée, un script d’import devra générer `id`, renseigner `source` (`dictionnaire_sil_l_y_2026_10_25`) et `statut`, et associer optionnellement un exemple attesté (`exemple_snk`, `exemple_fr`).

3. **Contrainte bloquante d’unicité de `normalizeLexicalKey()` sur les homonymes et affixes** :
   - Dans `app.js:339-344`, `normalizeLexicalKey()` applique `NFD`, retire les diacritiques vocaliques, convertit `ñ → ɲ`, **remplace tous les tirets `-` par des espaces** et applique `.trim()`.
   - Dans `app.js:3908`, `state.entryByNormalized` est une `Map` à clé unique (une seconde entrée écrase la première).
   - Surtout, **`tests/voice.test.cjs:47-53` échoue immédiatement (`assert.ok(!seenLexicalKeys.has(key))`) si deux lignes de `lexique-soninke-fr-base.csv` partagent la même clé `normalizeLexicalKey(soninke)`** !
   - **Conséquence architecturale** :
     - les **mots simples nouveaux sans collision** (`Lot A`) peuvent entrer dans `lexique-soninke-fr-base.csv` sans modifier `app.js` ni `voice.test.cjs` (**à l’exception des affixes à tiret** comme `-lenme` s’ils entraient un jour en collision avec `lenme`) ;
     - en revanche, intégrer **deux homonymes distincts** séparément (ex. `suure` « plat de mil » et `suure` « être nettoyé », ou `-la` et `la`) exigera **au préalable** une évolution ciblée de `app.js` (index multi-entrées `entriesByNormalized: Map<string, Entry[]>`) et l’adaptation de l’assertion d’unicité de `tests/voice.test.cjs` pour autoriser les homonymes explicitement qualifiés.

4. **Séparateur de sens multiples (` / ` vs `;`) dans le glosage mot à mot** :
   - `splitSenses()` (`app.js:1092`) découpe sur `/[;/,]/`, donc l’affichage détaillé et la recherche française gèrent déjà le séparateur ` / ` utilisé dans les gloses L–Y.
   - En revanche, `glossSoninkeSpans()` (`app.js:1774`) utilise `entry.fr.split(';')[0].trim()`, qui **ne coupe pas sur ` / `** (car `;` est réservé au délimiteur CSV de `lexique-soninke-fr-base.csv`). **Recommandation** : lors de l’intégration, remplacer `entry.fr.split(';')[0]` par `entry.fr.split(/\s*[;/]\s*/)[0]` dans `app.js:1774`.

5. **Découpage des variantes dans `parseBaseLexicon()` (`app.js:3833`)** :
   - `parseBaseLexicon()` fait `.split(',')`, alors que certaines entrées historiques (`SNK-LEX-0275..0290, 0707, 0749`) utilisent `;` ou `|`. Toutes les variantes L–Y utilisent déjà `, `, donc elles sont 100 % compatibles, mais élargir `app.js:3833` à `.split(/[,;|]/)` harmonisera aussi l’existant.

6. **Prise en charge des expressions et phrases parallèles** :
   - Les **`568` paires de phrases attestées** correspondent exactement à la vocation de `data/source/soninke-samples.jsonl` (chargé par `parseSampleJsonl()`, `app.js:3865-3881`, format `{"id": "...", "snk": "...", "fr": "...", "source": "...", "notes": "..."}`). Les y ajouter enrichira immédiatement les exemples et la recherche de phrases sans polluer le lexique de mots ni risquer de collision `voice.test.cjs`.
   - Les **`20` locutions lexicales multi-mots** (`ra wa a yi`, `yaaxen bogu`, etc.) nécessiteront une recherche par n-grammes si l’on souhaite qu’elles soient reconnues en analyse de phrase libre, car `lookupSoninkeWord()` et `attestationStatus()` opèrent aujourd’hui mot par mot.

---

## 6. Plan d’action recommandé (en attente d’autorisation explicite)

Aucune intégration dans `data/source/lexique-soninke-fr-base.csv` ni dans `data/source/soninke-samples.jsonl`, et aucune fusion de PR n’ont été effectuées durant cet audit. Sous réserve de votre validation explicite, nous recommandons une intégration en **4 lots maîtrisés** :

1. **Lot 1 — Intégration immédiate sans risque des mots simples validés (`2 223` entrées haute confiance)** :
   - Sélectionner uniquement les entrées de `audit-l-y-mots-2026-10-25.csv` marquées `a_verifier_par_locuteur = non` (`VALIDE_PRET_POUR_INTEGRATION`, `CORRIGE_PIPELINE_PRET`, `NOUVEAU_RECUPERE_PIPELINE`), les formater sur les 10 colonnes canoniques (`SNK-LEX-3328+`, `statut=candidat_sil_l_y_verifie`), et ajuster `glossSoninkeSpans()` (`app.js:1774`) sur `/\s*[;/]\s*/`.
2. **Lot 2 — Intégration séparée des phrases attestées (`564` paires haute confiance sur `568`) dans `data/source/soninke-samples.jsonl`** :
   - Conserver les phrases hors du CSV de mots simples et les verser dans `soninke-samples.jsonl` avec provenance `dictionnaire_sil_l_y_2026_10_25`.
3. **Lot 3 — Arbitrage linguistique humain assisté par les rapports générés** :
   - Soumettre à un locuteur/réviseur soninké :
     - les `81` mots marqués `a_verifier_par_locuteur = oui` dans `audit-l-y-mots-2026-10-25.csv` (dont les `23` rattachements dialectaux `seegi`/`seegu`, `wujune`/`wujine`, `soxuba`/`suxuba`, `loxo`/`roxo`, etc.) ;
     - les `169` groupes de `arbitrage-homonymes-l-y-2026-10-25.csv` (avec mise à niveau préalable de `entryByNormalized` en liste multi-entrées dans `app.js` et `tests/voice.test.cjs` avant d’importer des homographes légitimes) ;
     - les `103` `ENRICHISSEMENT_POTENTIEL` et `22` `VARIANTE_A_RATTACHER` documentés dans `audit-doublons-l-y-2026-10-25.csv` ;
     - la traduction française des `5` noms propres (`Lajine`, `Misira`, `Samariya`, `Silemaanu`, `Xuraane`).
4. **Lot 4 — Maintien hors base des exclusions justifiées (`456` entrées)** :
   - Conserver en archive de travail (`exclusions-anglais-dictionnaire-l-y-2026-10-25.csv` / `renvois-sans-glose-dictionnaire-l-y-2026-10-25.csv`) les entrées SIL dépourvues de glose française jusqu’à traduction par un locuteur.

---

## 7. Récapitulatif des livrables produits et tests exécutés

### Livrables d’audit générés
- `data/reports/audit-l-y-mots-2026-10-25.csv` (`2 318` lignes auditées + en-tête)
- `data/reports/audit-l-y-expressions-2026-10-25.csv` (`607` lignes auditées + en-tête)
- `data/reports/arbitrage-homonymes-l-y-2026-10-25.csv` (`169` groupes d’homonymes + en-tête)
- `data/reports/audit-doublons-l-y-2026-10-25.csv` (`3 427` entrées comparées au lexique canonique + en-tête)
- `data/reports/rapport-final-audit-l-y-2026-10-25.md` (présent rapport)
- `scripts/generer_audit_dictionnaire_l_y.py` (générateur reproductible des 4 CSV d’audit avec contrôle strict des numéros de lignes `L1..L8600`)
- `tests/dict_l_y_pipeline.test.py` (suite de tests automatisés de non-régression du pipeline L–Y)

### Suites de tests exécutées et validées
- `node tests/ui.test.cjs` : **PASS**
- `node tests/voice.test.cjs` : **PASS**
- `python3 scripts/check_doublons_lexique.py --strict` : **PASS**
- `python3 tests/dict_l_y_pipeline.test.py` : **PASS**
- Double exécution SHA-256 de `python3 scripts/extraire_nettoyer_dictionnaire_l_y.py` : **PASS (déterminisme 100 %)**
