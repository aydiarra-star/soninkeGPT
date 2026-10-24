# Définitions du lexique SoninkeGPT — état des lieux

Rapport calculé à partir de `data/source/lexique-soninke-fr-base.csv` par `scripts/rapport_definitions.py`. Il ne modifie aucune donnée.

## Couverture

| Constat | Nombre |
| --- | --- |
| Entrées du lexique | **1442** |
| Entrées avec une définition | **721** |
| Entrées sans définition | **721** |
| Couverture | **50 %** |

## Par statut

| Statut | Signification | Nombre |
| --- | --- | --- |
| `forme_derivee_du_verbe` | Définition dérivée du verbe de base (nom d'action, gérondif) | 328 |
| `redigee_a_valider` | Définition rédigée, à valider par le référent | 316 |
| `a_clarifier` | Définition proposée, glose de départ à trancher (⚠) | 77 |

Les définitions marquées ⚠ ne doivent pas être présentées comme des traductions sûres : elles attendent l'arbitrage du référent ([questions à trancher](QUESTIONS-REFERENT.md)).

## Par catégorie

Trié par nombre de définitions restantes.

| Catégorie | Entrées | Définies | Restantes |
| --- | --- | --- | --- |
| nom | 459 | 0 | 459 |
| adjectif | 63 | 0 | 63 |
| expression | 36 | 0 | 36 |
| partie_du_corps | 24 | 0 | 24 |
| numéral | 16 | 0 | 16 |
| adverbe | 12 | 0 | 12 |
| interjection | 9 | 0 | 9 |
| nombre | 9 | 0 | 9 |
| conjonction | 8 | 0 | 8 |
| forme_composee_a_identifier | 7 | 0 | 7 |
| membre_inferieur | 6 | 0 | 6 |
| particule | 6 | 0 | 6 |
| pronom_personnel_serie_diminutive | 6 | 0 | 6 |
| pronom_personnel_serie_longue | 6 | 0 | 6 |
| marqueur_aspectuel | 5 | 0 | 5 |
| marqueur_negation | 5 | 0 | 5 |
| membre_superieur | 5 | 0 | 5 |
| marqueur_grammatical | 4 | 0 | 4 |
| organe | 4 | 0 | 4 |
| syntagme_nominal | 4 | 0 | 4 |
| corps | 3 | 0 | 3 |
| lexeme | 3 | 0 | 3 |
| quantitatif | 3 | 0 | 3 |
| déictique | 2 | 0 | 2 |
| lexique | 2 | 0 | 2 |
| marqueur_temporel | 2 | 0 | 2 |
| pronom | 2 | 0 | 2 |
| quantificateur | 2 | 0 | 2 |
| variante_graphique_a_verifier | 2 | 0 | 2 |
| direction | 1 | 0 | 1 |
| déterminant | 1 | 0 | 1 |
| forme_a_identifier | 1 | 0 | 1 |
| nom_a_preciser | 1 | 0 | 1 |
| non_renseigne | 1 | 0 | 1 |
| suffixe nominal | 1 | 0 | 1 |
| verbe | 338 | 338 | 0 |
| nom_d_action | 182 | 182 | 0 |
| verbe_gerondif | 180 | 180 | 0 |
| verbe transitif | 9 | 9 | 0 |
| nom/verbe | 8 | 8 | 0 |
| verbe intransitif | 4 | 4 | 0 |

## Ce qui reste à écrire

| Catégorie | Entrées sans définition |
| --- | --- |
| nom | 459 |
| adjectif | 63 |
| expression | 36 |
| partie_du_corps | 24 |
| numéral | 16 |
| adverbe | 12 |
| interjection | 9 |
| nombre | 9 |
| conjonction | 8 |
| forme_composee_a_identifier | 7 |
| pronom_personnel_serie_longue | 6 |
| pronom_personnel_serie_diminutive | 6 |
| particule | 6 |
| membre_inferieur | 6 |
| marqueur_aspectuel | 5 |
| marqueur_negation | 5 |
| membre_superieur | 5 |
| marqueur_grammatical | 4 |
| syntagme_nominal | 4 |
| organe | 4 |
| quantitatif | 3 |
| lexeme | 3 |
| corps | 3 |
| marqueur_temporel | 2 |
| lexique | 2 |
| pronom | 2 |
| déictique | 2 |
| quantificateur | 2 |
| variante_graphique_a_verifier | 2 |
| déterminant | 1 |
| direction | 1 |
| non_renseigne | 1 |
| nom_a_preciser | 1 |
| forme_a_identifier | 1 |
| suffixe nominal | 1 |

## Comment les définitions sont produites

1. **Verbes du document du référent** : définition rédigée à partir de la glose attestée du lexique ([tableau complet](DEFINITIONS-VERBES-A-VALIDER.md)).
2. **Autres verbes du lexique** : même méthode, dans `data/source/definitions-redigees.csv`.
3. **Noms d'action et gérondifs** : définition générée par règle depuis le verbe de base, dans `data/source/definitions-formes-derivees.csv`.

Aucune définition n'est inventée : quand la glose de départ est incertaine, le statut passe à `a_clarifier` et la question est portée à la fiche du référent.

## Fichiers liés

- `data/source/definitions-redigees.csv` — définitions rédigées à la main
- `data/source/definitions-formes-derivees.csv` — définitions générées par règle
- `scripts/enrichir_definitions_sans_doublons.py` — écriture sans création de ligne
- `scripts/preparer_questions_referent.py` — fiche de questions
- `docs/LINGUISTIC-QUALITY.md` — règles d'attestation
