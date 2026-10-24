# Extraction du lexique « parties du corps humain » (document Google)

Date : 2026-10-24  
Branche : `arena/89ad8992-soninkegpt`  
Source : https://docs.google.com/document/d/19WQjG-JziayBdtVkI8WUeh0_b1FLHH-cYt0fwt7fgpA/edit

## Portée et prudence

Extraction des **54 formes soninké** présentes dans les tableaux du document. Chaque variante graphique d'une même ligne source est conservée comme une forme distincte : aucune fusion, aucune normalisation orthographique, aucune traduction ajoutée.

La base de production `data/source/lexique-soninke-fr-base.csv` n'est pas modifiée. Les formes sont écrites comme candidats dans `data/candidates/parties-du-corps-doc-google-2026-10-24.csv`, avec le statut `a_verifier` (ou `homographe_a_verifier` / `deja_integre_a_verifier` le cas échéant). Aucune entrée n'est considérée validée avant passage devant le référent.

Le classement est alphabétique sur la forme soninké, en ignorant la casse, les accents et les apostrophes, et en ramenant `ŋ` à `ng` (donc `Taŋe` se classe juste avant `Tange`).

## Liste ordonnée (ordre alphabétique)

| # | Soninké | Français (document) | Section | Statut |
|---|---|---|---|---|
| 1 | `Biy'e` | corps | 5 | homographe_a_verifier |
| 2 | `Biye` | corps | 5 | homographe_a_verifier |
| 3 | `boutte` | cœur | 2 | a_verifier |
| 4 | `Cuute` | cuisse | 4 | a_verifier |
| 5 | `Giya` | visage | 1 | deja_integre_a_verifier |
| 6 | `gnougnou` | lèvre | 1 | deja_integre_a_verifier |
| 7 | `guidjimé` | poitrine / torse | 2 | a_verifier |
| 8 | `Guru` | peau | 5 | a_verifier |
| 9 | `kambe` | dent | 1 | deja_integre_a_verifier |
| 10 | `kambou` | dents (pluriel) | 1 | deja_integre_a_verifier |
| 11 | `Kanfe` | épaule | 3 | a_verifier |
| 12 | `Kille` | os | 5 | homographe_a_verifier |
| 13 | `Kit-qasse` | poignet | 3 | a_verifier |
| 14 | `Kit-soro` | doigt | 3 | a_verifier |
| 15 | `Kit'e` | bras | 3 | a_verifier |
| 16 | `Kitte` | main | 3 | concordance_a_verifier |
| 17 | `Kuntu-bunyi` | genou | 4 | a_verifier |
| 18 | `Kunyu-bunyi` | coude | 3 | a_verifier |
| 19 | `Kuru` | genou | 4 | a_verifier |
| 20 | `Kuuru` | peau | 5 | a_verifier |
| 21 | `mpallé` | dos | 2 | a_verifier |
| 22 | `Nene` | langue | 1 | deja_integre_a_verifier |
| 23 | `noxo` | ventre | 2 | concordance_a_verifier |
| 24 | `Nuxune` | nez | 1 | deja_integre_a_verifier |
| 25 | `Qanfe` | épaule | 3 | a_verifier |
| 26 | `Qunyu-bunyi` | coude | 3 | a_verifier |
| 27 | `rakke` | bouche | 1 | deja_integre_a_verifier |
| 28 | `siga` | taille / hanches | 2 | a_verifier |
| 29 | `sinke` | menton | 1 | deja_integre_a_verifier |
| 30 | `some` | lèvre | 1 | deja_integre_a_verifier |
| 31 | `Taŋe` | jambe | 4 | a_verifier |
| 32 | `Tange` | pied | 4 | a_verifier |
| 33 | `Tange-golle` | mollet | 4 | a_verifier |
| 34 | `Tange-muru` | cheville | 4 | a_verifier |
| 35 | `Tange-soro` | orteil | 4 | a_verifier |
| 36 | `Tchuute` | cuisse | 4 | a_verifier |
| 37 | `Tegi-soro` | ongle | 3 | a_verifier |
| 38 | `Tegi-suuru` | ongle | 3 | a_verifier |
| 39 | `Teingé` | front | 1 | deja_integre_a_verifier |
| 40 | `thinkambé` | fesses | 2 | a_verifier |
| 41 | `Tiy'e` | chair / muscle | 5 | homographe_a_verifier |
| 42 | `Tiye` | chair / muscle | 5 | homographe_a_verifier |
| 43 | `torro` | oreille | 1 | deja_integre_a_verifier |
| 44 | `xanné` | cou | 1 | deja_integre_a_verifier |
| 45 | `Xill'e` | os | 5 | a_verifier |
| 46 | `xorré` | gorge | 1 | deja_integre_a_verifier |
| 47 | `xoume` | joues | 1 | deja_integre_a_verifier |
| 48 | `Yaxe` | œil | 1 | deja_integre_a_verifier |
| 49 | `Yaxou` | yeux | 1 | deja_integre_a_verifier |
| 50 | `yesso` | menton | 1 | deja_integre_a_verifier |
| 51 | `Yig'e` | sang | 5 | homographe_a_verifier |
| 52 | `Yige` | sang | 5 | homographe_a_verifier |
| 53 | `yime` | tête | 1 | deja_integre_a_verifier |
| 54 | `yinte` | cheveux | 1 | deja_integre_a_verifier |

## Mêmes formes, regroupées par section du document

### Section 1 — La tête et le visage (Xoor'e daa baaxe)

| Français (document) | Soninké |
|---|---|
| tête | `yime` |
| cheveux | `yinte` |
| visage | `Giya` |
| front | `Teingé` |
| œil | `Yaxe` |
| yeux | `Yaxou` |
| nez | `Nuxune` |
| bouche | `rakke` |
| lèvre | `gnougnou`, `some` |
| dent | `kambe` |
| dents (pluriel) | `kambou` |
| langue | `Nene` |
| oreille | `torro` |
| joues | `xoume` |
| menton | `yesso`, `sinke` |
| cou | `xanné` |
| gorge | `xorré` |

### Section 2 — Le tronc et les organes principaux

| Français (document) | Soninké |
|---|---|
| poitrine / torse | `guidjimé` |
| cœur | `boutte` |
| ventre | `noxo` |
| dos | `mpallé` |
| taille / hanches | `siga` |
| fesses | `thinkambé` |

### Section 3 — Les membres supérieurs (bras et mains)

| Français (document) | Soninké |
|---|---|
| bras | `Kit'e` |
| main | `Kitte` |
| épaule | `Qanfe`, `Kanfe` |
| coude | `Qunyu-bunyi`, `Kunyu-bunyi` |
| poignet | `Kit-qasse` |
| doigt | `Kit-soro` |
| ongle | `Tegi-soro`, `Tegi-suuru` |

### Section 4 — Les membres inférieurs (jambes et pieds)

| Français (document) | Soninké |
|---|---|
| jambe | `Taŋe` |
| pied | `Tange` |
| cuisse | `Cuute`, `Tchuute` |
| genou | `Kuntu-bunyi`, `Kuru` |
| mollet | `Tange-golle` |
| cheville | `Tange-muru` |
| orteil | `Tange-soro` |

### Section 5 — Os, muscles et éléments internes (Biy'e killi)

| Français (document) | Soninké |
|---|---|
| corps | `Biy'e`, `Biye` |
| peau | `Guru`, `Kuuru` |
| os | `Xill'e`, `Kille` |
| sang | `Yig'e`, `Yige` |
| chair / muscle | `Tiy'e`, `Tiye` |

## Points à faire trancher par le référent

### 1. Écart de mapping sur la section « tête et visage »

Le document ne reprend pas exactement la liste déjà intégrée le 21 octobre 2026 (`SNK-LEX-0275` à `SNK-LEX-0294`). Ne rien corriger automatiquement : faire confirmer.

| Forme | Sens dans le document | Sens déjà en base |
|---|---|---|
| `yesso` | menton (document) | cou (SNK-LEX-0291) |
| `sinke` | menton (document) | cou, variante (SNK-LEX-0292) |
| `xanné` | cou (document) | gorge (SNK-LEX-0293) |
| `xané` | absente du document | menton (SNK-LEX-0290) |

### 2. Recoupements avec la base : concordances et homographes

Certaines formes des sections 2 à 5 existent déjà dans la base. Quand les sens se recouvrent, c'est une confirmation à faire valider. Quand ils divergent, ce sont des homographes potentiels, pas des doublons : chaque sens doit rester séparé.

| Forme du document | Sens du document | Entrée déjà en base | Sens en base | Lecture |
|---|---|---|---|---|
| `Biy'e` | corps | SNK-LEX-0529 | billet (nom ; Dictionnaire soninké.docx) | homographe : ne pas fusionner |
| `Biye` | corps | SNK-LEX-0529 | billet (nom ; Dictionnaire soninké.docx) | homographe : ne pas fusionner |
| `Kille` | os | SNK-LEX-0780 | route (nom ; CNRS lexique des noms) | homographe : ne pas fusionner |
| `Kitte` | main | SNK-LEX-0756 | main (nom ; CNRS lexique des noms) | concordance à confirmer |
| `noxo` | ventre | SNK-LEX-0757 | ventre (nom ; CNRS lexique des noms) | concordance à confirmer |
| `Tiy'e` | chair / muscle | SNK-LEX-0744 | viande (nom ; CNRS lexique des noms) | homographe : ne pas fusionner |
| `Tiye` | chair / muscle | SNK-LEX-0744 | viande (nom ; CNRS lexique des noms) | homographe : ne pas fusionner |
| `Yig'e` | sang | SNK-LEX-0005 | manger (verbe ; liste_referent) | homographe : ne pas fusionner |
| `Yige` | sang | SNK-LEX-0005 | manger (verbe ; liste_referent) | homographe : ne pas fusionner |

### 3. Remarques de transcription

- Le document écrit « Chaire / Muscle » ; la forme retenue côté français est « chair / muscle » (coquille probable du document, à confirmer).
- Le document signale lui-même des variations dialectales (Mali, Mauritanie, Sénégal, Gambie), notamment `X` / `H` à l'initiale.
- La graphie `Taŋe` (jambe) doit être confirmée : `ŋ` note généralement la nasale vélaire, et la base contient déjà `Tange` (pied) comme forme distincte.
- `Kille` (os) et `Yige` (sang) doivent être tranchés : les entrées proches déjà en base portent respectivement les sens « route » et « manger ».

## Prochaine étape

Soumettre la section 1 (écarts de mapping) et les sections 2 à 5 (formes nouvelles) au référent linguistique. Tant que la prononciation n'est pas confirmée, aucun audio ne doit être rattaché à ces formes.
