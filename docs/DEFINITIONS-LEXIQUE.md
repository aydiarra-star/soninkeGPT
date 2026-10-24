# Définitions du lexique SoninkeGPT — état des lieux

Rapport calculé à partir de `data/source/lexique-soninke-fr-base.csv` par `scripts/rapport_definitions.py`. Il ne modifie aucune donnée.

## Couverture

| Constat | Nombre |
| --- | --- |
| Entrées du lexique | **1442** |
| Entrées avec une définition | **1442** |
| Entrées sans définition | **0** |
| Couverture | **100 %** |

## Par statut

| Statut | Signification | Nombre |
| --- | --- | --- |
| `redigee_a_valider` | Définition rédigée, à valider par le référent | 942 |
| `forme_derivee_du_verbe` | Définition dérivée du verbe de base (nom d'action, gérondif) | 328 |
| `a_clarifier` | Définition proposée, glose de départ à trancher (⚠) | 172 |

Les définitions marquées ⚠ ne doivent pas être présentées comme des traductions sûres : elles attendent l'arbitrage du référent ([questions à trancher](QUESTIONS-REFERENT.md)).

## Par catégorie

Trié par nombre de définitions restantes.

| Catégorie | Entrées | Définies | Restantes |
| --- | --- | --- | --- |
| nom | 459 | 459 | 0 |
| verbe | 338 | 338 | 0 |
| nom_d_action | 182 | 182 | 0 |
| verbe_gerondif | 180 | 180 | 0 |
| adjectif | 63 | 63 | 0 |
| expression | 36 | 36 | 0 |
| partie_du_corps | 24 | 24 | 0 |
| numéral | 16 | 16 | 0 |
| adverbe | 12 | 12 | 0 |
| interjection | 9 | 9 | 0 |
| nombre | 9 | 9 | 0 |
| verbe transitif | 9 | 9 | 0 |
| conjonction | 8 | 8 | 0 |
| nom/verbe | 8 | 8 | 0 |
| forme_composee_a_identifier | 7 | 7 | 0 |
| membre_inferieur | 6 | 6 | 0 |
| particule | 6 | 6 | 0 |
| pronom_personnel_serie_diminutive | 6 | 6 | 0 |
| pronom_personnel_serie_longue | 6 | 6 | 0 |
| marqueur_aspectuel | 5 | 5 | 0 |
| marqueur_negation | 5 | 5 | 0 |
| membre_superieur | 5 | 5 | 0 |
| marqueur_grammatical | 4 | 4 | 0 |
| organe | 4 | 4 | 0 |
| syntagme_nominal | 4 | 4 | 0 |
| verbe intransitif | 4 | 4 | 0 |
| corps | 3 | 3 | 0 |
| lexeme | 3 | 3 | 0 |
| quantitatif | 3 | 3 | 0 |
| déictique | 2 | 2 | 0 |
| lexique | 2 | 2 | 0 |
| marqueur_temporel | 2 | 2 | 0 |
| pronom | 2 | 2 | 0 |
| quantificateur | 2 | 2 | 0 |
| variante_graphique_a_verifier | 2 | 2 | 0 |
| direction | 1 | 1 | 0 |
| déterminant | 1 | 1 | 0 |
| forme_a_identifier | 1 | 1 | 0 |
| nom_a_preciser | 1 | 1 | 0 |
| non_renseigne | 1 | 1 | 0 |
| suffixe nominal | 1 | 1 | 0 |

## Ce qui reste à écrire

Aucune entrée restante : les **1442** entrées du lexique ont une définition.

## Comment les définitions sont produites

1. **Verbes du document du référent** : définition rédigée à partir de la glose attestée du lexique ([tableau complet](DEFINITIONS-VERBES-A-VALIDER.md)).
2. **Autres verbes du lexique** : même méthode, dans `data/source/definitions-redigees.csv`.
3. **Noms d'action et gérondifs** : définition générée par règle depuis le verbe de base, dans `data/source/definitions-formes-derivees.csv`.
4. **Noms, adjectifs, expressions, parties du corps, numéraux, pronoms et marqueurs grammaticaux** : définition rédigée à la main à partir de la glose attestée du lexique, dans `data/source/definitions-redigees.csv`.

Aucune définition n'est inventée : quand la glose de départ est incertaine, le statut passe à `a_clarifier` et la question est portée à la fiche du référent.

## Fichiers liés

- `data/source/definitions-redigees.csv` — définitions rédigées à la main
- `data/source/definitions-formes-derivees.csv` — définitions générées par règle
- `scripts/enrichir_definitions_sans_doublons.py` — écriture sans création de ligne
- `scripts/preparer_questions_referent.py` — fiche de questions
- `docs/LINGUISTIC-QUALITY.md` — règles d'attestation
