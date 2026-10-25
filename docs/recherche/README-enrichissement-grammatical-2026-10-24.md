# Enrichissement grammatical et lexical de SoninkeGPT — 2026-10-24

Dossier de recherche produit pour la mission « enrichir le lexique de SoninkeGPT
avec une base lexicale **et** grammaticale documentée, traçable et exploitable ».
Rien ici n'est publié sur le site de production : tous les fichiers sont des
**candidats à examiner**, conformément à `docs/LINGUISTIC-QUALITY.md`.

## 1. Livrables

| # | Livrable | Fichier |
|---|----------|---------|
| 1 | Lexique grammatical structuré (487 lignes, 19 colonnes) | `data/candidates/lexique-grammatical-structure-2026-10-24.csv` (+ `.json`) |
| 2 | Inventaire des pronoms | `docs/recherche/inventaire-pronoms-2026-10-24.md` |
| 3 | Étude des constructions « être » / « avoir » | `docs/recherche/etre-avoir-constructions-2026-10-24.md` |
| 4 | Tableaux de conjugaison documentés (200 formes annotées) | `docs/recherche/conjugaisons-verbes-prioritaires-2026-10-24.md` |
| 5 | Phrases d'exemple soninké + français | `docs/recherche/phrases-exemples-2026-10-24.md` |
| 6 | Rapport des variantes et divergences entre sources | `docs/recherche/rapport-variantes-divergences-2026-10-24.md` |
| 7 | Nouvelles entrées prêtes à comparer au lexique existant (83 formes) | `data/candidates/nouvelles-entrees-grammaticales-2026-10-24.csv` |
| 8 | Rapport de qualité | `docs/recherche/rapport-qualite-2026-10-24.md` |
| — | Rapport de comparaison / dédoublonnage (ligne à ligne) | `data/reports/comparaison-grammatical-2026-10-24.csv` |

Outils reproductibles :

- `scripts/lexique_grammatical_data.py` — les 229 lignes curatées (sections A à G),
  chacune avec sa source ;
- `scripts/preparer_lexique_grammatical.py` — conversion des 58 lignes
  `SNK-EA` de `data/source/paradigmes-etre-avoir.csv`, annotation par règles des
  200 phrases conjuguées du corpus `validation_02`, comparaison au lexique de
  base (via la fonction `cle()` de `scripts/import_extraction_sans_doublons.py`,
  déjà utilisée par le projet) et écriture des quatre fichiers ci-dessus.
  **Le script n'écrit jamais dans `data/source/`** : le lexique existant n'est
  pas modifié.

Nouveau fichier de données ajouté (sans rien remplacer) :
`data/source/snk-engine-corpus-grammatical-2026-10-24.jsonl` — copie vendored
(579 lignes) des corpus de [snk_engine](https://github.com/oscarmedra/snk_engine)
(rév. `49f50a939ded`, CC BY 4.0, noah-medra), déjà cité par le projet dans
`docs/LEXICAL-RESOURCES-SOURCE.md`. Le fichier `validation_03` du même dépôt n'a
pas été copié : il répète les gabarits de `validation_02` pour des verbes déjà
décrits dans `data/grammaire/soninke.yaml`.

## 2. Méthode (lots 1 → 5, dans l'ordre demandé)

1. **Lot 1** — pronoms personnels, « être », « avoir », négation, interrogation :
   dépouillement du corpus du projet (`validation_01/02`, `serie_02/03`, six
   textes thématiques), de `data/grammaire/soninke.yaml` (confirmé référent),
   du lexique de base (1 442 lignes), puis des sources externes :
   Creissels 2018 (Mandenkan 59), Creissels & Diawara (esquisse LGIDF),
   livret METFPALAN Dakar 2001, SIL (dictionnaire et guide d'écriture),
   cours soninko.info (leçons 2 et 3), glossaires Soninkara.
2. **Lot 2** — conjugaison des verbes fréquents : annotation **par règles** des
   200 phrases de `validation_02` (11 verbes × 6 personnes × séries longue/brève),
   revue visuelle ligne à ligne des 200 annotations (voir livrable 4).
3. **Lot 3** — relatifs, démonstratifs, possessifs, interrogatifs, indéfinis.
4. **Lot 4** — autres verbes (tuga, taxalema, tirindi, terene…), particules,
   connecteurs, salutations, numéraux, morphologie du pluriel.
5. **Lot 5** — vérification des sources, comparaison au lexique existant,
   dédoublonnage (rapport `comparaison-grammatical`), fichiers d'intégration.

## 3. Schéma du tableau structuré (19 colonnes, exactement celui demandé)

`id_provisoire ; forme_soninke ; traduction_francaise ; categorie_grammaticale ;
sous_categorie ; forme_ou_construction_grammaticale ; personne ; nombre ;
temps_aspect_mode ; polarite ; variante ; variete_regionale ; exemple_soninke ;
traduction_exemple ; source ; page_ou_localisation ; niveau_de_confiance ;
statut_validation ; notes`

- Séparateur `;`, UTF-8, comme les CSV existants du projet.
- **Champs vides quand l'information est inconnue** — jamais de valeur inventée.
- `id_provisoire` : `GRM2-0001`… (préfixe distinct des `SNK-GRM`/`SNK-LEX`/`SNK-EA`
  existants pour éviter toute collision).

## 4. Statuts de validation employés

| Statut | Sens ici | Lignes |
|--------|----------|--------|
| `SOURCE_VERIFIEE` | forme + traduction attestées dans une source identifiée (corpus relu par locuteur, lexique référent, publication) | 306 |
| `A_CONFIRMER_PAR_LOCUTEUR` | source écrite seule, ou glose inférée d'un contexte ; **une source écrite fiable ne vaut pas validation par le référent du projet** | 117 |
| `VARIANTE_DOCUMENTEE` | variante graphique/dialectale reliée à une forme principale, jamais supprimée | 13 |
| `CONTRADICTOIRE_ENTRE_SOURCES` | désaccord entre sources : **les deux formes/sens sont conservés avec leurs références** | 11 |
| `HYPOTHESE_NON_VALIDEE` | assemblage régulier ou paradigme non attesté tel quel (ex. `sere be ga sefene`) | 40 |

Correspondance avec le lexique existant (rapport de comparaison) :
80 formes déjà dans la base (→ compléter l'entrée existante, **jamais de
doublon ni de suppression**), 1 déjà en variantes, 58 déjà suivies dans
`paradigmes-etre-avoir.csv`, 214 formes conjuguées (non intégrables comme
entrées lexicales), 51 lignes documentaires (constructions, listes, hypothèses)
et **83 nouvelles entrées** proposées.

## 5. Principes respectés

- **Enrichir sans remplacer** : aucune entrée existante n'est modifiée ou
  supprimée ; les nouvelles formes vont dans un fichier séparé.
- **Pas de verbe « être » ni « avoir » unique supposé** : les constructions
  réelles sont documentées (copules `ni`/`feti`, locatives `wa`/`nta` et
  `yi`/`n'ti`, statifs `nàn`/`ntá`, possession locative, `maxa` « chez »…).
- **Pas de conjugaison française plaquée** : le système réel (radical invariable
  + marqueurs prédicatifs + gérondif) est décrit tel quel.
- **Pas de pronom relatif unique supposé** : un seul relateur `be` (+ `ga`) est
  attesté ; les équivalents français « qui/que/dont/où » ne correspondent pas à
  des formes soninké distinctes.
- **Variantes jamais supprimées** : `xenxe`/`qenqe`, `kumbene`/`xumbene`/
  `xunbane`, `tamu`/`tanmu`, `we ñaana`/`wa ñaana`, séries longue/brève…
  sont conservées et reliées.
- **Chaque forme conjuguée est reliée à son verbe de référence** (colonne
  `sous_categorie` + notes + livrable 4).
- **Diacritiques et conventions des sources respectés** : les graphies tonales
  (`ní`, `má ñì`, `kàrá`), les caractères `ñ/ŋ/ɲ/ɛ` et les majuscules des
  sources pédagogiques sont conservés tels quels, la variante normalisée étant
  signalée en `variante`.

## 6. Lecture rapide des résultats clés

- **Pronoms** : deux séries (longue `nke anke ake oku xaku iku`, brève
  `n an a o xa i`) ; même forme au sujet et à l'objet ; pas de genre ;
  pas de distinction inclusive/exclusive **attestée** dans les sources consultées
  (point à vérifier). Réfléchi/réciproque : `me` (livret Dakar), `í`/`dú`
  (Creissels, Kingi) — analyses différentes selon les variétés.
- **Être** : équatif `ni` (nég. `feti`), locatif `wa` (nég. `nta`) au Kingi et
  `yi` (nég. `n'ti`) dans le dialecte du projet ; statifs avec `nàn`/`ntá` ;
  aucun passé fléchi attesté dans le corpus du projet (les formes `ñi`,
  `we ñaana` viennent de sources externes/pédagogiques).
- **Avoir** : pas de verbe ; possession locative (`… wa a yi`, `… yani maxa`),
  âge (`wa 21 siine`), états par verbes/adjectifs d'état, obligation par
  `xawa`/`qawa`, capacité par `kitta` (SIL).
- **Conjugaison** : radical invariable ; les temps sont portés par les marqueurs
  (`na`, `yi/wa/fayi` + gérondif, `do … ni ya me`, `yi rini`, `rini`, `n'ti
  rini`, `maxa`, `di/da`, Ø). Deux ambiguïtés documentées : `rini` (gérondif de
  `ri` vs marqueur de futur) et `fayi` (habituel vs progressif).
- **11 homonymies conflictuelles** conservées avec leurs sources : `ko`
  (dire/qui), `ku` (offrir/démonstratif), `kuyi` (rêver/offrir), `kara`
  (casser/mourir, tons), `keti` (toucher/est-ce que), `ti` (dire/négation),
  `xa` (vous/mais/où), `maxa` (négation/chez), `kati` (pouvoir/avant de/à),
  `guida` (sœur/frère selon les traductions), `siri`/`sìrì` (vite/devoir).

## 7. Prochaines étapes recommandées

1. Faire relire les 117 lignes `A_CONFIRMER_PAR_LOCUTEUR` et les 11 lignes
   `CONTRADICTOIRE_ENTRE_SOURCES` par le référent du projet (les questions
   précises sont listées dans le rapport de qualité, §6).
2. Intégrer les 83 nouvelles entrées via le pipeline existant
   (`scripts/import_extraction_sans_doublons.py`), **après** validation.
3. Pour les 80 formes déjà dans la base : ajouter variantes/exemples aux
   entrées existantes selon les actions proposées dans
   `data/reports/comparaison-grammatical-2026-10-24.csv` (ne rien supprimer).
4. Ne publier sur le site qu'après ces deux étapes.
