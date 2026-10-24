# Constructions « être » et « avoir » en soninké — 2026-10-24

Livrable 3. Principe rappelé par la mission et vérifié par les sources :
**le soninké n'a ni un verbe « être » unique, ni verbe « avoir »**. Ce document
décrit les constructions réelles, variété par variété, sans calque français.
Il prolonge `docs/VERBES-ETRE-AVOIR.md` (référentiel du projet) avec les
apports externes (Creissels 2018, esquisse LGIDF, SIL, livret Dakar 2001, cours
soninko.info) et le corpus snk_engine relu par locuteur.

## 1. « Être » — équatif (identité, catégorie, qualité)

| Fonction | Forme | Variété | Négation | Source |
|---|---|---|---|---|
| copule équative | **ni** (`ní`) | Kingi ; concordance corpus projet | **feti** (Kingi : `hé ~ heti`) | Creissels 2018 §3.5 ; SNK-LEX-0479 (`A bexecen ni.` Elle est sucrée, validé référent) ; SNK-LEX-0536 (feti) |
| copule équative | **ni ya** | dialecte du projet | (négatif à confirmer) | corpus texte_marche (`Towoyinte ni ya.` Il est malade ; `Nke faba ka n'ya ni.` C'est la maison de mon père) |
| prédication adjective **sans** copule | nom + déterminant + adjectif | projet | — | corpus texte_village (`Killé ké gillo.` La route était longue) — le temps n'est pas marqué, le contexte tranche |
| prédication adjective **avec** copule | attribut-n + ni | Kingi + projet | feti | Creissels 2018 ex. (15) `Ñántò-n bùnné-n tòoxìnté-n nì.` La piqûre du scorpion est douloureuse |
| mise en relief (focus) | attribut + **ñà** + ni | Kingi | — | Creissels 2018 ex. (30) `Tàgé-n ñà ní.` C'est l'enfant |

**Passé / futur de l'équatif** : aucune forme fléchie dans le corpus du projet
(constat déjà noté dans `docs/VERBES-ETRE-AVOIR.md` §3.4). Les paradigmes
pédagogiques mauritaniens (soninko.info leçon 2) proposent :

- présent : `In ni / An ni / A ni / O ni / Xa ni / I ni` ;
- imparfait : `In ñi / An ñi / …` — cohérent avec le marqueur d'inaccompli
  passé `ñí` de Creissels 2018 ;
- futur : `In we ñaana / A ye ñaana / …` — un lecteur du cours (2014, citant
  Y. Diagana) signale la variante `wa ñaana` (`N wa riini`).

Ces formes sont enregistrées avec le statut `A_CONFIRMER_PAR_LOCUTEUR`
(paradigmes) voire `faible` (futur `we/ye ñaana`, non recoupé). Les lignes
1sg/3sg étaient déjà fichées dans `paradigmes-etre-avoir.csv` (`SNK-EA-0038` à
`0041`) : le tableau structuré les convertit sans les dupliquer.

## 2. « Être » — locatif et existentiel

| Fonction | Forme | Variété | Négation | Source |
|---|---|---|---|---|
| copule locative | **wa** (`wá`) | Kingi | **nta** (`ntá`) | Creissels 2018 §3.4 : `Haatu wa konpen di.` / `Haatu nta konpen di.` |
| copule locative devant focus/interrogatif | **na** | Kingi + projet | — | Creissels 2018 ex. (12) `Haatu na minna ?` ; SNK-LEX-0218 |
| copule locative | **yi** | dialecte du projet | **n'ti / ti** | corpus texte_marche (`A yi ka ke.` Elle est à la maison ; `Ake n'ti ka ke.`) ; confirmation orale du locuteur snk_engine 2026-09-17 (« yi veut dire est, ti veut dire n'est pas ») |
| existentiel « il y a » | chose + wa/yi + lieu | Kingi + projet | sere su + n'ti/nta | SNK-LEX-0303 (`Yintin xullu baananbaanon wa a yi.` Il a quelques cheveux blancs — litt. « sont à lui ») ; snk_engine docs ; SNK-LEX-0310 (`Baasi nt'a di.` Il n'y a rien de mal) |

Remarque : `wa` et `yi` figurent déjà au lexique du projet comme **marqueurs
aspectuels** (`SNK-GRM-0019`, `SNK-GRM-0021`). Leur emploi de **copule
locative** est un sens distinct documenté par Creissels et par le corpus :
le rapport de comparaison propose d'**enrichir les entrées existantes**, jamais
d'en créer de doublons.

### Verbes statifs (Creissels 2018, Kingi)

Classe de verbes (ex. `gàbá` être fréquent, `qáwà` devoir, `sìrì` devoir,
`dìnká` être gros, `tòoxìnté` être douloureux, `gìlá` être long) qui se
combinent avec :

- `nàn ~ ǹ` (affirmatif) : `Kiyen nàn tawó.` Le soleil est ardent.
- `ntá` (négatif) : `Ó ntá gàbà Hàatú ŋàllí.` Nous ne voyons pas souvent
  Fatou (litt. « nous ne sommes pas fréquents à voir Fatou »).
- `ñí` (inaccompli passé), `má ñì` (passé négatif).

C'est la construction qui traduit le mieux « être + adjectif » pour les
propriétés intensives et comparatives (`An nàn dinká in ŋa.` Tu es plus gros
que moi). **Existence dans le dialecte du projet à confirmer** — déjà signalée
comme hypothèse dans `docs/VERBES-ETRE-AVOIR.md`.

## 3. « Avoir » — aucune des constructions françaises n'a d'équivalent unique

### 3.1 Possession

Construction **locative** : le possédé est sujet, le possesseur est un complément
« chez/à » :

- Kingi / lexique projet : `possédé + wa + possesseur + yi/ŋa` —
  `Yintin xullu baananbaanon wa a yi.` « Il a quelques cheveux blancs. »
  (SNK-LEX-0303, validé référent) ; `Bannaaxun taagumansen wa dudoxotonten ŋa.`
  (SNK-LEX-0365)
- dialecte du projet : `possédé + (y)ani + maxa` —
  `Waxi-ni filli yani maxa ado guida naxaru siki.` « J'ai deux frères et trois
  sœurs. » (texte_marche marche-18) ; négation : `Xalisi n'ti maxa.`
  « Je n'ai pas d'argent. » (litt. l'argent n'est pas chez moi)
- appartenance : `Ke kitabe ni nke ni ya xale.` « Ce livre est à moi. »
  (snk_engine docs ; `xale` = à, appartenance)

⚠ **Homonymie signalée** : `maxa` « chez » (possession, corpus du projet) vs
`maxa` négation du passé (`SNK-GRM-0024`) vs `máxà` négation de
l'impératif/subjonctif (Creissels). Les trois sont conservés avec références ;
statut `CONTRADICTOIRE_ENTRE_SOURCES` sur la ligne postpositionnelle tant que
le référent n'a pas tranché entre homonymie et polysémie.

### 3.2 Âge

- `sujet + wa + nombre + siine` : `Aken Ñaame Tarawore wa 21 siine.`
  « Naïma Tarawore a 21 ans. » (presse Soninkara, 2014)
- négation : `A nta siine yi.` « Il n'a pas encore un an. » (dictionnaire SIL,
  entrée `siine`)

### 3.3 États physiques et émotionnels (« avoir mal », « avoir peur »…)

Ni construction avec « avoir », ni verbe unique : verbes/adjectifs d'état.

- `M'paba a tampi, xodo ké wa mama n.` « Mon père était fatigué, il avait mal
  au dos. » (texte_pluies)
- `A kona, a xaru.` « Il a eu peur et il a crié. » (texte_village)
- `N xaso saasa.` « Je suis vieux maintenant. » (SIL, entrée `xaso`)

Le relevé verbe d'état par verbe d'état reste à faire avec le référent
(`tampi`, `mama`, `kona`, `towoyinte`…).

### 3.4 Obligation et capacité (« devoir », « pouvoir »)

| Sens | Forme | Construction attestée | Source |
|---|---|---|---|
| devoir | xawa / qawa | `pronom + na + n'xawa + complément` : `Bawoni nke na n'xawa maro ado teh n'ya xobono.` « Parce que je dois acheter du riz et du thé. » | corpus texte_marche marche-04 |
| devoir (statif, Kingi) | qáwà, sìrì | avec `nàn`/`ntá` | Creissels 2018 §1 (citant Diagana 1994) |
| pouvoir / réussir | kitta (katti, katta) | `Abdulaye da kasetin xobo, ma i wa katta sooninkanxanne terinkana.` « Abdoulaye a acheté une cassette pour pouvoir écouter le soninké. » | dictionnaire SIL |
| pouvoir (particule) | ra | (sans exemple dans la source) | glossaire Soninkara |

⚠ La graphie `kati` du corpus a d'**autres** emplois (`kati n'ga xenxe-ne`
« avant de dormir », journee-08 ; `safa kati nke waxi` « écrit à mon frère »,
travail-04) : la ligne `kati` est marquée `CONTRADICTOIRE_ENTRE_SOURCES` et ne
doit pas être employée comme « pouvoir » sans validation.

### 3.5 « Avoir » des temps composés français : aucun auxiliaire

L'accompli soninké ne connaît pas d'auxiliaire :

- intransitif : marqueur zéro — `In yige.` « J'ai mangé. » ;
- transitif : `di/da` entre sujet et objet — `Anke n'di maro n'yiga.`
  « Tu as mangé le riz. » (SNK-EA-0063) ;
- négatif : `ma` / `maxa` — `N maxa faye.` « Je n'ai pas regardé. » (v-160).

## 4. Conversion de `paradigmes-etre-avoir.csv`

Les 64 lignes `SNK-EA` du projet ont été converties au schéma des 19 colonnes
dans le tableau structuré :

- 58 lignes converties (8 `atteste_corpus` → `SOURCE_VERIFIEE` ;
  13 `atteste_source_externe` → `A_CONFIRMER_PAR_LOCUTEUR` ;
  37 `assemble_a_valider` → `HYPOTHESE_NON_VALIDEE`) ;
- **6 lignes `non_atteste` ignorées** (forme « — » : passé/futur de l'équatif et
  de la possession, `SNK-EA-0042/0043/0044/0060/0061/0062`) : ce sont des
  **lacunes**, documentées dans le rapport de qualité — aucune forme n'a été
  inventée pour les remplir ;
- la colonne `notes` de chaque ligne convertie porte l'id d'origine
  (`SNK-EA-xxxx`), le statut d'origine et le modèle attesté : la traçabilité
  vers le fichier source est complète ;
- le rapport de comparaison les classe `deja_dans_paradigmes_ea` : elles ne
  figurent donc **pas** dans le fichier des nouvelles entrées (pas de doublon
  avec le suivi existant du projet).

## 5. Points à trancher avec le référent (synthèse)

1. `ni ya` : la copule équative du projet est-elle `ni` + focalisateur `ya`,
   ou une unité figée ? Négatif de l'équatif dans le projet (`feti` ?).
2. Le passé de « être » : `ñi` (source externe) existe-t-il dans son dialecte ?
3. Verbes statifs `nàn`/`ntá` : attestés chez lui ?
4. `maxa` « chez » : postposition distincte ou emploi de la négation ?
   Fréquence réelle de `(y)ani maxa` vs `wa … yi`.
5. `xawa` vs `qawa` vs `kitta` : quelles formes emploie-t-il pour devoir/pouvoir ?
6. Inclusive/exclusive du « nous » : existe-t-elle ?
7. Le paradigme mauritanien `we/ye ñaana` (futur) : à écarter ou à documenter
   comme régional ?
