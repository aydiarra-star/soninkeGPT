# Inventaire des pronoms soninké — 2026-10-24

Livrable 2 de la mission d'enrichissement. Toutes les formes proviennent de
sources identifiées (voir `docs/recherche/README-enrichissement-grammatical-2026-10-24.md`
§1 et les colonnes `source` / `page_ou_localisation` du tableau structuré).
Les formes déjà présentes dans `data/source/lexique-soninke-fr-base.csv`
(`SNK-GRM-0001` à `0012`) sont signalées : **elles ne doivent pas être
dupliquées**, seulement enrichies.

## 1. Fait structural central

> « Les pronoms sujets et les pronoms objets ont les mêmes formes ; il n'y a
> aucune distinction de position. » — Creissels & Diawara, esquisse LGIDF, §3.

- **Pas de genre** : `a` = il / elle / le / la / lui / son / sa / ses ;
  `i` = ils / elles / les / leur / leurs.
- **Ordre** : le pronom (sujet ou objet) précède le verbe ; l'objet nominal
  aussi (ordre S O V). Exemple du corpus : `A di lettra ke n'safa`
  « il a écrit la lettre ».
- **Pas de distinction inclusive/exclusive du « nous » attestée** dans aucune
  des sources consultées (Creissels 2016/2018, LGIDF, SIL, livret Dakar 2001,
  cours soninko.info, corpus du projet). C'est un **point à vérifier** auprès du
  référent — et non une absence à affirmer.

## 2. Série longue (sujets / emphatiques)

Déjà au lexique : `SNK-GRM-0001` à `0006`. Graphies rencontrées : projet
(`nke`), corpus snk_engine (`nké`, accents vocaliques), LGIDF (tonale : `ńké`).

| Personne | Forme (projet) | Graphies des sources | Particule | Exemple attesté |
|---|---|---|---|---|
| 1sg | nke | nké, ńké | jamais | `Nke rini daga saxa.` Je partirai au marché. (validation_02 v-148) |
| 2sg | anke | anké, ánkè | anke n'… | `Anke n'yi rini daga.` Tu vas partir. (v-006 variante) |
| 3sg | ake | aké, àkê | ake n'… | `Ake n'daga.` Il est parti. (v-008 variante) |
| 1pl | oku | okou, ókú | jamais | `Oku maxa faye.` Nous n'avons pas regardé. (v-019) |
| 2pl | xaku | xakou, áxákù | xaku n'… | `Xaku n'daga lenki.` Vous êtes partis aujourd'hui. (v-149) |
| 3pl | iku | ikou, ìkû | iku n'… | `Iku n'yi rini daga.` Ils vont partir. (v-006) |

Règle de la particule (référent projet, `data/grammaire/soninke.yaml`) :
`anke`, `ake`, `xaku`, `iku` prennent la particule (`n'`, `m'`, `ŋ'`, `l'` selon
la consonne initiale du verbe) ; `nke` et `oku` ne la prennent jamais.

## 3. Série brève (sujets / objets / possessifs adnominaux)

Déjà au lexique : `SNK-GRM-0007` à `0012`.

| Personne | Forme | Sujet | Objet | Possessif | Exemples attestés |
|---|---|---|---|---|---|
| 1sg | n (in) | ✓ | ✓ | ✓ | `N faye.` J'ai regardé. (v-018) ; `N ka ke.` Ma maison. (snk_engine docs) |
| 2sg | an | ✓ | ✓ | ✓ | `An ka ke.` Ta maison. |
| 3sg | a | ✓ | ✓ | ✓ | `A da a bisimilla.` Il l'a accueilli. (LGIDF) ; `A ka ke.` Sa maison. |
| 1pl | o | ✓ | ✓ | ✓ | `O bara.` Notre cour. (snk_engine docs) |
| 2pl | xa | ✓ | ✓ | ✓ | `Xa guiri.` Levez-vous. (impératif pluriel) |
| 3pl | i | ✓ | ✓ | ✓ | `I da me katu.` Ils se sont battus. (livret Dakar 2001) |

- **Possessifs** : le soninké n'a pas de formes possessives spéciales — ce sont
  ces pronoms placés **devant le nom** (Creissels & Diawara §2 ; livret Dakar :
  `n sugo` « ma chèvre »). Possesseur non pronominal : simple juxtaposition
  (`Faatu ka` « la maison de Fatou », `n'paba ka` « celle de mon père », avec
  assimilation de la nasale).
- **n / in (1sg)** : le cours soninko.info (leçon 2, Mauritanie) écrit `IN`
  (forme pleine, « sans pause ») et `N` en début de phrase ; le livret de Dakar
  écrit « n (in) ». Creissels 2018 note `ń` (ex. « prête-moi lóxo ín ŋá »).
  → ligne `in` enregistrée comme `VARIANTE_DOCUMENTEE`, répartition exacte à
  confirmer.
- **Graphie mauritanienne du cours** (`INKE / ANKEN / AKEN / OKU / XAKUN /
  IKUN`) : mêmes formes que la série longue avec la nasale finale de
  détermination. Enregistrée comme variante graphique, pas comme entrée séparée.

## 4. Réfléchis et réciproques

Les sources divergent **sans se contredire frontalement** (variétés différentes) ;
tout est conservé :

| Forme | Fonction | Source | Statut |
|---|---|---|---|
| me | réciproque (« ils se sont battus » : `i da me katu`) | livret METFPALAN Dakar 2001 | A_CONFIRMER_PAR_LOCUTEUR |
| in | réfléchi objet (« il m'a rattrapé » : `a da in raga`) | livret Dakar 2001 | A_CONFIRMER (même forme que n/in 1sg — à élucider) |
| í | réfléchi possessif ; coréférence sujet de subordonnée | Creissels 2016 (Kingi), note 15 | A_CONFIRMER (distingué de `i` 3pl par le ton seul) |
| dú | réfléchi | Creissels 2016 ; glossaire Soninkara (`Du : soi-même`) | A_CONFIRMER |

**À trancher avec le référent** : le dialecte du projet emploie-t-il `me`
(réciproque) ? `í`/`dú` existent-ils chez lui ? Le corpus snk_engine ne montre
aucun réfléchi explicite.

## 5. Pronoms relatifs

Le soninké n'a **pas** de série de pronoms relatifs correspondant aux relatifs
français. Les sources attestent :

- `be` — particule relateur (déjà au lexique : `SNK-LEX-0430`) ; guide SIL :
  « relatif be » ; livret Dakar : `N maama be ga ñi faayindini soyi…`
- `ga` — subordonnant introduisant la relative/complétive après `be`, attesté
  dans le corpus du projet : `A di o tirindi o ga daga-na noqu be.`
  « Il nous demande où nous allons. » (journee-03)
- Une seule stratégie pour qui / que / dont / où : **antécédent + be + ga +
  proposition**. Les assemblages du type `sere be ga sefene` « l'homme qui
  parle » sont marqués `HYPOTHESE_NON_VALIDEE` (éléments attestés séparément,
  phrase complète non attestée).

## 6. Pronoms démonstratifs

| Forme | Sens | Nombre | Source | Statut |
|---|---|---|---|---|
| ke | ceci, celui-ci ; ce/cette (déterminant) | sg | SNK-LEX-0847 ; LGIDF (`ké háré` cette main) ; glossaire Soninkara ; corpus (`maro ke` le riz) | SOURCE_VERIFIEE |
| ku | ceux-ci ; ces | pl | LGIDF (`kú hárú`) ; glossaire Soninkara | **CONTRADICTOIRE** : le référent donne `ku` = offrir (SNK-LEX-0171) |
| ken | cela, celui-là | sg | SNK-LEX-0846 ; glossaire Soninkara | SOURCE_VERIFIEE (2 sources externes) |
| kun | ceux-là | pl | glossaire Soninkara | A_CONFIRMER (source unique) |
| ke kundu / ke doke | celui-ci (près) / celui-là (là-bas) | — | snk_engine docs | A_CONFIRMER (pas de phrase complète) |

Adverbes démonstratifs de lieu : `kere` ici (SNK-LEX-0844), `no` là
(SNK-LEX-0845), `doke/dooke/doono` là-bas (snk_engine docs ; glossaire
Soninkara), `kundu` ici/tout près (corpus travail-04 : `Watia kundu` « en ce
moment »). **Pas de distinction de genre**, le nombre du démonstratif porté par
`ke`/`ku` n'est attesté qu'au Kingi (LGIDF).

## 7. Pronoms interrogatifs

Voir aussi le tableau structuré (section G1) ; synthèse :

| Forme | Sens | Source | Statut |
|---|---|---|---|
| minna | où | Creissels 2018 ; corpus marche-01 (`Anke dagana minna ?`) | SOURCE_VERIFIEE |
| xa | où (variante) | snk_engine docs | A_CONFIRMER (homographe de xa « vous » et xa « mais ») |
| mane | quoi | corpus ; snk_engine docs | SOURCE_VERIFIEE |
| mane-ni | pourquoi | corpus marche-03 | SOURCE_VERIFIEE |
| ko | qui | Creissels 2018 (`Kó`) ; Soninkara cours 3 ; corpus marche-05 | **CONTRADICTOIRE** : référent = `ko` « dire » |
| kan | quand | Soninkara cours 3 (`An ri kan koota ?`) | A_CONFIRMER (faible) |
| mani-me | combien | snk_engine docs | A_CONFIRMER (faible) |
| moxo | comment | corpus village-26 ; soninko.info (`AN MOXO ?`) | SOURCE_VERIFIEE |
| ba (final) | est-ce que | corpus serie_02 (`… ba ?`) ; SNK-LEX-0232 ; livret Dakar | SOURCE_VERIFIEE |
| keti | est-ce que | glossaire Soninkara | **CONTRADICTOIRE** : référent = `keti` « toucher » |
| xori | (non glosé) | livret Dakar (liste des interrogatifs) ; soninko.info (salutations) | traduction laissée **vide** |

## 8. Indéfinis et quantificateurs (rappel)

`su` tout/chaque (SNK-LEX-0916 ; LGIDF `sú`), `yogo` un certain/quelque
(LGIDF `yògó` ; Creissels `yúgó` ; corpus journee-08 `livrou yogo`), `gabe`
beaucoup (SNK-LEX-0917), `honne` peu (SNK-LEX-0809), `tana` autre
(SNK-LEX-0811), `baabe` chacun (SNK-LEX-1345, validé référent), `fo` chose
(corpus, faible), `sere su` + négation « personne » (snk_engine docs).

## 9. Lacunes assumées (champs laissés vides, rien d'inventé)

1. **Inclusif/exclusif** : aucune attestation — à poser au référent.
2. **Pronoms toniques indépendants** du dialecte du projet : seule la graphie
   mauritanienne (`inke`, `anken`…) est documentée ; l'emploi réel (mise en
   relief ?) reste à confirmer.
3. **Réfléchi du projet** : aucune forme confirmée (voir §4).
4. `xori`, `saado`, `wo`, `fe`, `la`, `yaa` : cités par des sources sans glose
   exploitable → traductions laissées vides dans le tableau.
