#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare un CSV d'extraction au lexique base SANS rien importer.

Sélectionne les entrées réellement absentes du lexique (présence vérifiée
dans `soninke` **et** `variantes`, insensible aux accents, à la casse, aux
traits d'union, aux apostrophes et aux numéros d'homonyme) et les écrit dans
un fichier « nouveaux ». Le rapport de comparaison journalise chaque ligne
avec un statut :

    nouveau                            absent du lexique
    doublon_ecarte_glose_identique     déjà présent, glose équivalente
    doublon_ecarte_homonyme_deja_regroupe  homonyme numéroté déjà regroupé
    doublon_ecarte_glose_differente    déjà présent, glose différente
    doublon_interne                    répété dans le fichier d'extraction
    glose_vide                         mot ou glose français absent

Le lexique de base n'est jamais modifié.

Usage :
    python3 scripts/comparer_extraction_lexique.py [EXTRACTION.csv]

Sorties (par défaut) :
    data/candidates/dictionnaire-d-f-nouveaux-2026-10-25.csv
    data/reports/comparaison-dictionnaire-d-f-2026-10-25.csv
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

from import_extraction_sans_doublons import (
    cle,
    charger_lexique,
    normaliser_glose,
)

ENTREE_DEFAUT = Path("data/candidates/dictionnaire-d-f-extraction-2026-10-25.csv")
NOUVEAUX_DEFAUT = Path("data/candidates/dictionnaire-d-f-nouveaux-2026-10-25.csv")
RAPPORT_DEFAUT = Path("data/reports/comparaison-dictionnaire-d-f-2026-10-25.csv")

CHAMPS_EXTRACTION = ["soninke", "francais", "categorie", "glose_complete", "note"]


def comparer(extraction: list[dict], connues: dict):
    """Retourne (nouveaux, journaux) selon l'ordre du fichier d'extraction."""
    nouveaux, journaux = [], []
    vus = set()
    for ligne in extraction:
        mot = (ligne.get("soninke") or "").strip()
        fr = (ligne.get("francais") or "").strip()
        if not mot or not fr:
            journaux.append(("glose_vide", mot, fr, ""))
            continue
        k = cle(mot)
        if k in connues:
            existant = connues[k]
            glose_lex = existant.get("francais", "")
            if normaliser_glose(glose_lex) == normaliser_glose(fr):
                etat = "doublon_ecarte_glose_identique"
            elif re.search(r"\d$", mot):
                etat = "doublon_ecarte_homonyme_deja_regroupe"
            else:
                etat = "doublon_ecarte_glose_differente"
            journaux.append((etat, mot, fr, existant.get("id", "")))
            continue
        if k in vus:
            journaux.append(("doublon_interne", mot, fr, ""))
            continue
        vus.add(k)
        nouveaux.append(ligne)
        journaux.append(("nouveau", mot, fr, ""))
    return nouveaux, journaux


def main(argv: list[str]) -> int:
    entree = Path(argv[1]) if len(argv) > 1 else ENTREE_DEFAUT
    with entree.open(encoding="utf-8", newline="") as fh:
        extraction = list(csv.DictReader(fh, delimiter=";"))

    _, connues = charger_lexique()
    nouveaux, journaux = comparer(extraction, connues)

    NOUVEAUX_DEFAUT.parent.mkdir(parents=True, exist_ok=True)
    with NOUVEAUX_DEFAUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CHAMPS_EXTRACTION, delimiter=";",
                           extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(nouveaux)

    RAPPORT_DEFAUT.parent.mkdir(parents=True, exist_ok=True)
    with RAPPORT_DEFAUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";", lineterminator="\n")
        w.writerow(["resultat", "soninke", "francais", "reference_lexique"])
        w.writerows(journaux)

    compte = {}
    for etat, *_ in journaux:
        compte[etat] = compte.get(etat, 0) + 1
    print(f"lues : {len(extraction)} | nouveaux : {len(nouveaux)} | "
          f"doublons écartés : {compte.get('doublon_ecarte_glose_identique', 0) + compte.get('doublon_ecarte_homonyme_deja_regroupe', 0) + compte.get('doublon_ecarte_glose_differente', 0)} | "
          f"doublons internes : {compte.get('doublon_interne', 0)} | "
          f"gloses vides : {compte.get('glose_vide', 0)}")
    for etat in sorted(compte):
        if etat != "nouveau":
            print(f"  {etat} : {compte[etat]}")
    print(f"nouveaux écrits : {NOUVEAUX_DEFAUT}")
    print(f"rapport : {RAPPORT_DEFAUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
