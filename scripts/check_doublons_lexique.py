#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie qu'aucune forme du lexique principal n'est en double.

Deux entrées sont considérées comme le MÊME mot si leur forme coïncide après
normalisation de la casse, des accents vocaliques, des traits d'union, des
apostrophes et des numéros d'homonyme (`baabo1` → `baabo`). Les lettres
propres au soninké (ñ, ŋ, ɲ, ɓ, ɗ, ƴ, ɛ, ɔ) restent distinctes : *segeñe*
« ongle » et *segene* « monter » ne sont pas des doublons.

Usage :
    python3 scripts/check_doublons_lexique.py            # sortie lisible
    python3 scripts/check_doublons_lexique.py --csv R    # export CSV
    python3 scripts/check_doublons_lexique.py --strict   # code retour 1 si doublon

Le contrôle porte à la fois sur la colonne `soninke` et sur la colonne
`variantes` : une forme déjà listée comme variante ne doit pas être réintroduite
comme entrée principale.
"""

from __future__ import annotations

import csv
import importlib.util
import sys
from collections import defaultdict
from pathlib import Path

LEXIQUE = Path("data/source/lexique-soninke-fr-base.csv")


def charger_cle():
    """Réutilise la normalisation du script d'import (une seule définition)."""
    chemin = Path(__file__).with_name("import_extraction_sans_doublons.py")
    spec = importlib.util.spec_from_file_location("_imp", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cle


def main(argv: list[str]) -> int:
    cle = charger_cle()
    with LEXIQUE.open(encoding="utf-8", newline="") as fh:
        lignes = [l for l in csv.DictReader(fh, delimiter=";") if l.get("id")]

    par_forme = defaultdict(list)      # clé -> entrées qui portent cette forme
    for ligne in lignes:
        for forme in [ligne["soninke"], *(ligne.get("variantes") or "").split(",")]:
            if forme and forme.strip():
                par_forme[cle(forme)].append((ligne["id"], forme.strip(), ligne["soninke"]))

    doublons, renvois = [], []
    for k, occurrences in par_forme.items():
        tete = [o for o in occurrences if cle(o[2]) == k]   # forme principale
        if len({o[0] for o in tete}) > 1:
            doublons.append((k, occurrences))              # vraie duplication
        elif len({o[0] for o in occurrences}) > 1:
            renvois.append((k, occurrences))               # mot en variante ailleurs

    print(f"{len(lignes)} entrées, {len(par_forme)} formes distinctes.")
    print(f"  doublons d'entrée (même mot principal) : {len(doublons)}")
    print(f"  formes citées en variante dans une autre entrée : {len(renvois)} "
          f"(renvois, pas des doublons)")
    for k, occ in sorted(doublons):
        details = " ; ".join(f"{i} ({f})" for i, f, _ in occ)
        print(f"  ⚠ {k} → {details}")
    if "--tout" in argv:
        for k, occ in sorted(renvois):
            details = " ; ".join(f"{i} ({f})" for i, f, _ in occ)
            print(f"  · {k} → {details}")

    if "--csv" in argv:
        sortie = Path(argv[argv.index("--csv") + 1])
        sortie.parent.mkdir(parents=True, exist_ok=True)
        with sortie.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, delimiter=";")
            w.writerow(["cle_normalisee", "identifiants", "formes"])
            for k, occ in sorted(doublons + renvois):
                w.writerow([k, " | ".join(o[0] for o in occ),
                            " | ".join(o[1] for o in occ)])
        print(f"rapport : {sortie}")

    if "--strict" in argv and doublons:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
