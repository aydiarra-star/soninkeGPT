# Rapport de qualité — enrichissement grammatical et lexical — 2026-10-24

Livrable 8. Bilan honnête de ce qui est solide, de ce qui reste à vérifier et
de ce qui n'a pas pu être vérifié. Aucune forme inventée n'a été intégrée ;
quand l'information manquait, le champ a été laissé **vide**.

## 1. Chiffres clés

| Indicateur | Valeur |
|---|---|
| Lignes du tableau structuré (livrable 1) | **487** (19 colonnes, `;`, UTF-8) |
| — lignes curatées (sections A à G) | 229 |
| — lignes converties de `paradigmes-etre-avoir.csv` | 58 (6 lignes `non_atteste` ignorées, voir §4.1) |
| — formes conjuguées annotées (corpus validation_02) | 200 (+ 14 formes pédagogiques « être ») |
| Nouvelles entrées proposées (livrable 7) | **83** |
| Formes déjà dans le lexique de base (→ enrichir, jamais dupliquer) | 80 (+ 1 déjà en variantes) |
| Lignes documentaires (constructions, listes, hypothèses) | 51 |
| Lignes déjà suivies dans `paradigmes-etre-avoir.csv` | 58 |
| Lignes sans source | **0** |
| Lignes sans traduction française | 4 — volontairement vides : `xori`, `saado`, `wo` (cités sans glose par leurs sources) et une ligne de synthèse des numéraux déjà au lexique |
| Lignes sans exemple | 87 — aucune phrase attestée n'a été inventée pour les remplir |

Répartition des statuts : `SOURCE_VERIFIEE` 306 · `A_CONFIRMER_PAR_LOCUTEUR`
117 · `HYPOTHESE_NON_VALIDEE` 40 · `VARIANTE_DOCUMENTEE` 13 ·
`CONTRADICTOIRE_ENTRE_SOURCES` 11.
Niveaux de confiance : élevé 279 · moyen 122 · faible 86.

Parmi les 83 nouvelles entrées : 24 `SOURCE_VERIFIEE` (corpus relu par
locuteur ou plusieurs sources concordantes), 49 `A_CONFIRMER_PAR_LOCUTEUR`,
7 `VARIANTE_DOCUMENTEE`, 3 `CONTRADICTOIRE_ENTRE_SOURCES` — **aucune**
`HYPOTHESE_NON_VALIDEE` (les hypothèses sont exclues du fichier d'intégration).

## 2. Couverture des domaines demandés (A à G)

| Domaine demandé | Couverture | Réserves |
|---|---|---|
| A. Pronoms personnels | complète : 2 séries × 6 personnes, sujet = objet, possessifs adnominaux, graphies mauritaniennes et tonales, réfléchi/réciproque | inclusif/exclusif **non attesté** (à poser) ; réfléchi du dialecte du projet non confirmé |
| B. « Être » | complète : équatif ni/feti, locatif wa/nta et yi/n'ti, focus na, statifs nàn/ntá, existentiels, prédication adjective, paradigmes pédagogiques | passé/futur fléchis non attestés dans le corpus du projet |
| C. « Avoir » | complète : possession locative (2 constructions), âge, états, obligation (xawa/qawa/qáwà/sìrì), capacité (kitta/ra), pas d'auxiliaire des temps composés | verbes d'état à relever un par un avec le référent |
| D. Conjugaison des ~25 verbes fréquents | 11 verbes en paradigmes complets (200 formes) ; les 29 verbes de la liste ont chacun une fiche lexème (forme de référence, gérondif, variantes, exemples, contradictions) | « faire » et « aller » n'ont pas d'équivalent générique vérifié (lacune assumée) ; entendre/savoir/vouloir/pouvoir/devoir/recevoir n'ont pas de paradigme complet |
| E. Pronoms relatifs | complète : relateur unique `be` + subordonnant `ga`, stratégie documentée | les assemblages (`sere be ga sefene`) sont des hypothèses non validées |
| F. Démonstratifs | complète : ke/ku/ken/kun + adverbes de lieu (kere, no, doke, kundu) + déterminant défini ke du projet | divergence de système avec le Kingi (nasale finale) documentée |
| G. Autres catégories | possessifs, interrogatifs (12), indéfinis (8), négation (6), TAM (13), postpositions (5), conjonctions (14), adverbes (18), numéraux, pluriel/dérivation (8), salutations (12), impératifs (5) | `fe/la/yaa`, `saado`, `wo`, `xori` sans glose ; numéral « un » non attesté par source fiable |

Les cinq lots ont été traités **dans l'ordre imposé** (1 → 5) ; aucune
catégorie difficile n'a été abandonnée : les catégories non résolues sont
documentées comme telles (traductions vides, statuts faibles, questions au
référent §6).

## 3. Chaîne de traçabilité

Chaque ligne cite : la source (référence bibliographique complète ou corpus +
licence), la localisation précise (id de corpus, §, exemple, URL, id de ligne
`SNK-EA`/`SNK-LEX`/`SNK-GRM`). Les fichiers de données :

- `data/source/snk-engine-corpus-grammatical-2026-10-24.jsonl` — copie
  horodatée du corpus snk_engine (rév. `49f50a939ded`, CC BY 4.0, attribution
  noah-medra, ORCID 0009-0003-6018-9802), avec pour chaque ligne l'URL
  d'origine, le fichier source et le statut projet (« corpus validé par le
  locuteur de snk_engine ; **non revalidé par le référent du projet
  SoninkeGPT** »). `validation_03` n'a pas été copié (mêmes gabarits que
  `validation_02`, verbes déjà décrits dans `data/grammaire/soninke.yaml`).
- Les annotations grammaticales des 200 formes conjuguées sont produites par
  `scripts/preparer_lexique_grammatical.py` (règles explicites, relues ligne à
  ligne) : la note de chaque ligne le déclare.
- Le lexique de base et les fichiers `data/source/` existants n'ont subi
  **aucune modification** (à l'exception de l'ajout du fichier corpus ci-dessus,
  qui ne remplace rien).

## 4. Lacunes assumées (rien n'a été inventé pour les combler)

### 4.1 Lignes `non_atteste` de `paradigmes-etre-avoir.csv` (6)
`SNK-EA-0042/0043/0044` (passé et futur de l'équatif, passé négatif) et
`SNK-EA-0060/0061/0062` (passé et futur de la possession, passé négatif) :
formes « — ». Aucune forme de remplacement n'a été proposée ; les paradigmes
pédagogiques mauritaniens (`In ñi`, `In we ñaana`) sont fournis **séparément**
avec leur propre source et un statut `A_CONFIRMER_PAR_LOCUTEUR`, sans être
présentés comme les formes manquantes du dialecte du projet.

### 4.2 Autres lacunes
1. Verbe générique « faire » : non vérifié (causatif `-ndi` documenté à la place).
2. Verbe générique « aller » : non vérifié (`daga` partir + composés validés
   `Daga iige/sohu/goli`).
3. Numéral « un » : non attesté par une source consultable (`filli` deux et
   `siki` trois sont attestés par le corpus).
4. Gérondif de `wutu` « prendre » : absent du YAML référent (lacune du projet).
5. Exemple complet pour `gage` (vendre), `mugu` (entendre), `wuru` (courir),
   `honne`, `tana`, `kun`, `xoyi`, `saado`, `wo`, `fe/la/yaa` : aucun —
   champs exemples vides.
6. Inclusive/exclusive du « nous », pronoms toniques du projet, réfléchi du
   projet : non attestés dans les sources consultées.
7. `hanŋu` (forum Soninkara) : écarté, non vérifiable.
8. Tons : non notés dans l'orthographe du projet ; les paires tonales des
   sources linguistiques (kárá/kàrá…) ne peuvent pas être tranchées à l'écrit.

### 4.3 Sources inaccessibles ou non consultées (documenté, pas contourné)
- `sil.org` : site en panne pendant la recherche (« Technical Difficulties ») ;
  les données SIL utilisées proviennent du *Lexique Soninke du Mali* (Scribd)
  et des snippets du guide d'écriture — à re-vérifier sur les PDF officiels.
- `lgidf.cnrs.fr` : PDF introuvable (404) ; l'esquisse a été lue **en entier**
  via le miroir `francaislangueseconde.fr`. Les pages lexiques (nodes 676-682)
  n'ont été exploitées que via les résultats de recherche : à re-vérifier.
- `llacan.cnrs.fr/PDF/Mandenkan59/59_2creissels.pdf` : HTTP 500 ; contourné par
  l'édition HTML OpenEdition (lue en détail).
- Non consultés : Mandenkan 55 (Creissels 2016, PDF non ouvert — utilisé via
  ses conclusions reprises ailleurs), Mandenkan 738, Diagana (Karthala 2011 et
  tomes 1-2 cités par le cours soninko.info), Grégoire 1979 (PDF non ouvert —
  utilisé via les références `G1979` de snk_engine), Creissels & Diagne 2013
  (transitivité à Bakel, PDF non ouvert).
- Wikipédia : utilisé pour un seul point (`yo` oui / `ayi` non), en confiance
  faible — `ayi` est corroboré par le corpus du projet, `yo` ne l'est pas.

## 5. Risques et limites

1. **Annotation automatique** des 200 formes conjuguées : règles explicites et
   revues, mais produites par machine à partir des traductions françaises du
   corpus ; une erreur d'annotation est possible même quand la phrase est
   valide. Chaque ligne le déclare en note.
2. **Corpus snk_engine non revalidé par le référent SoninkeGPT** : les 306
   lignes `SOURCE_VERIFIEE` s'appuient sur des sources identifiées (dont un
   corpus relu par *son* locuteur) ; la validation finale au sens du projet
   (`docs/LINGUISTIC-QUALITY.md`) reste à faire.
3. **Orthographe d'origine** des textes libres : segments français mêlés
   (« en famille », « Est ce que » dans marche-07), graphies non normalisées
   (`yigué`, `xénxé`) : ces segments n'ont été utilisés que lorsque la
   traduction du corpus les soutenait ; marche-07 a été **écarté** comme
   exemple.
4. **Sources pédagogiques en ligne** (soninko.info, Soninkara) : qualité
   inégale, commentaires de lecteurs non éditorialisés — toujours en confiance
   faible/moyenne.
5. **Variétés mélangées** : le tableau mélange Kingi, Kingui, Mauritanie et
   dialecte du projet ; la colonne `variete_regionale` permet de filtrer, mais
   une intégration dans le site devra choisir sa politique (recommandation :
   dialecte du référent d'abord).

## 6. Questions précises à poser au référent (ordre de priorité)

Format compatible avec `data/reviews/questions-referent-2026-10-24.csv` :

1. `guida` : sœur ou frère ? (divergence interne au corpus, repas-20 vs marche-18)
2. `maxa` : « chez » (possession) est-il un homonyme ou le même mot que la
   négation du passé ?
3. `kati`/`kitta` : employez-vous `kitta` pour « pouvoir » ? Que vaut `kati`
   dans `kati n'ga xenxe-ne` (« avant de dormir ») ?
4. `ni ya` : copule composée ou `ni` + focalisateur ? Négatif équatif dans
   votre dialecte : `feti` ?
5. Passé de « être » : `ñi` existe-t-il chez vous ? Futur : quelle forme ?
6. `fayi` : habituel, progressif ou les deux ?
7. `yi rini` (v-191 « vous allez venir » vs v-187 « nous venons ») : comment
   lever l'ambiguïté de `rini` ?
8. Déterminant défini : `ke` (`ka ke`) ou nasale finale ? Les deux ?
9. `xenxe`/`qenqe` et `soxu`/`sohu` : mêmes lexèmes ?
10. Réfléchi/réciproque : `me` ? `í`/`dú` ? autre ?
11. « nous » inclusif/exclusif : existe-t-il ?
12. `mugu` (entendre) vs `mungu` (oublier) : confirmer la distinction.
13. Verbe « faire » et verbe « aller » génériques : existent-ils ?
14. `xori`, `saado`, `wo`, `fe`, `la`, `yaa` : sens ?
15. `kara` : « mourir » existe-t-il dans votre variété (à côté de « casser ») ?
16. `ko` interrogatif « qui » : l'employez-vous ?
17. Numéral « un » : quelle forme ?
18. Gérondif de `wutu` : quelle forme ?
19. `we/ye ñaana` (futur pédagogique mauritanien) : à documenter comme régional
    ou à écarter ?
20. `alijuma` vs `juma` (vendredi) : quelle forme employez-vous ?

## 7. Checklist d'intégration (après validation référent)

1. Relire les 117 lignes `A_CONFIRMER_PAR_LOCUTEUR` et les 11 lignes
   `CONTRADICTOIRE_ENTRE_SOURCES` ; trancher ou maintenir les deux formes.
2. Importer les nouvelles entrées validées via le pipeline existant
   (`scripts/import_extraction_sans_doublons.py`) — le fichier
   `nouvelles-entrees-grammaticales-2026-10-24.csv` est prêt pour ce format
   (mêmes colonnes que le tableau structuré ; le pipeline lit le CSV d'entrée
   après adaptation de ses colonnes, ou via un export intermédiaire).
3. Pour les 80 formes déjà en base : appliquer les `action_proposee` du rapport
   de comparaison (compléter variantes/exemples/références des entrées
   existantes — **ne jamais supprimer ni fusionner**).
4. Contrôler avec `scripts/check_doublons_lexique.py` après import.
5. Ne publier sur le site qu'après 1 à 4 ; garder ce dossier comme trace.

## 8. Reproductibilité

```bash
python3 scripts/preparer_lexique_grammatical.py
```

Régénère les quatre fichiers de sortie de manière déterministe à partir de
`scripts/lexique_grammatical_data.py` (données curatées),
`data/source/paradigmes-etre-avoir.csv`, du corpus vendored et du lexique de
base. Les documents 4 et 5 (`conjugaisons-…md`, `phrases-exemples-…md`) sont
générés depuis le tableau structuré.
