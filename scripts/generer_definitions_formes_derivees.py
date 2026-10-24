#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Définitions des formes dérivées (nom d'action, gérondif), générées par règle.

Un nom d'action et un gérondif ne s'expliquent pas comme un mot autonome : leur
définition est grammaticale et se déduit du verbe de base, que le lexique nomme
déjà dans `exemple_original` (« Nom d'action … du verbe « bagu » »). Aucun sens
nouveau n'est donc introduit : la définition reprend celle du verbe de base.

Le script écrit `data/source/definitions-formes-derivees.csv`, au même format
que `data/source/definitions-redigees.csv`, et refuse de produire une définition
quand le verbe de base n'est pas retrouvé ou n'a pas encore de définition.

Usage :
    python3 scripts/generer_definitions_formes_derivees.py
    python3 scripts/generer_definitions_formes_derivees.py --verifier
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEXIQUE = ROOT / "data" / "source" / "lexique-soninke-fr-base.csv"
REDIGEES = ROOT / "data" / "source" / "definitions-redigees.csv"
SORTIE = ROOT / "data" / "source" / "definitions-formes-derivees.csv"

CATEGORIES = {
    "nom_d_action": (
        "Nom d'action du verbe « {base} » : forme nominale qui désigne l'action "
        "exprimée par ce verbe."
    ),
    "verbe_gerondif": (
        "Gérondif (inaccompli) du verbe « {base} » : forme employée pour l'action "
        "en cours, « en train de … »."
    ),
}

MOTIF_BASE = re.compile(r"du verbe\s*«\s*([^»]+?)\s*»")


def charger_cle():
    chemin = ROOT / "scripts" / "import_extraction_sans_doublons.py"
    spec = importlib.util.spec_from_file_location("_import", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cle


def lire_lexique() -> list[dict]:
    with LEXIQUE.open(encoding="utf-8", newline="") as flux:
        return [l for l in csv.DictReader(flux, delimiter=";") if l.get("id")]


def lire_definitions() -> dict[str, dict]:
    with REDIGEES.open(encoding="utf-8", newline="") as flux:
        return {l["soninke"].strip(): l for l in csv.DictReader(flux, delimiter=";") if l.get("soninke")}


def construire() -> tuple[list[dict], list[str]]:
    cle = charger_cle()
    lignes = lire_lexique()
    definitions = lire_definitions()
    par_cle = {}
    for ligne in lignes:
        par_cle.setdefault(cle(ligne["soninke"]), []).append(ligne)

    resultats, problemes = [], []
    for ligne in lignes:
        categorie = (ligne.get("categorie") or "").strip()
        if categorie not in CATEGORIES:
            continue
        if ligne["soninke"] in definitions:
            continue
        base_sources = MOTIF_BASE.search(ligne.get("exemple_original") or "")
        if not base_sources:
            problemes.append(f"{ligne['id']} {ligne['soninke']} : verbe de base non indiqué")
            continue
        base = base_sources.group(1).strip()
        candidates = par_cle.get(cle(base), [])
        if len(candidates) != 1:
            problemes.append(
                f"{ligne['id']} {ligne['soninke']} : verbe de base « {base} » "
                f"{'absent' if not candidates else 'ambigu'} dans le lexique"
            )
            continue
        entree_base = candidates[0]
        definition_base = definitions.get(entree_base["soninke"])
        if not definition_base:
            problemes.append(
                f"{ligne['id']} {ligne['soninke']} : le verbe de base « {entree_base['soninke']} » "
                "n'a pas encore de définition"
            )
            continue

        sens = " ".join(
            part for part in [
                f"Sens du verbe de base : {definition_base['definition'].strip()}",
            ] if part
        )
        statut = "forme_derivee_du_verbe"
        note = f"Définition générée par règle depuis l'entrée {entree_base['id']} ({entree_base['soninke']})."
        if definition_base.get("statut") == "a_clarifier":
            statut = "a_clarifier"
            note += " Le verbe de base est lui-même marqué « glose à vérifier »."

        resultats.append(
            {
                "soninke": ligne["soninke"],
                "definition": CATEGORIES[categorie].format(base=entree_base["soninke"]) + " " + sens,
                "statut": statut,
                "note": note,
            }
        )
    resultats.sort(key=lambda r: r["soninke"])
    return resultats, problemes


def main() -> int:
    analyseur = argparse.ArgumentParser()
    analyseur.add_argument("--verifier", action="store_true", help="contrôle sans réécrire")
    options = analyseur.parse_args()

    resultats, problemes = construire()
    print(f"formes dérivées définies  {len(resultats)}")
    print(f"sans définition possible  {len(problemes)}")
    for probleme in problemes[:20]:
        print("  · " + probleme)
    if len(problemes) > 20:
        print(f"  · … et {len(problemes) - 20} autres")

    if options.verifier:
        if problemes:
            print(f"✖ {len(problemes)} forme(s) dérivée(s) sans définition.", file=sys.stderr)
            return 1
        print("✔ Toutes les formes dérivées ont une définition.")
        return 0

    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    with SORTIE.open("w", encoding="utf-8", newline="") as flux:
        ecrivain = csv.DictWriter(flux, fieldnames=["soninke", "definition", "statut", "note"],
                                  delimiter=";", lineterminator="\n")
        ecrivain.writeheader()
        for ligne in resultats:
            ecrivain.writerow(ligne)
    print(f"→ {SORTIE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
