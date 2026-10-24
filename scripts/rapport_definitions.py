#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""État des définitions du lexique, catégorie par catégorie.

Écrit `docs/DEFINITIONS-LEXIQUE.md` : combien d'entrées ont une définition,
lesquelles restent à écrire, et avec quel statut. Aucune donnée n'est modifiée :
le rapport est calculé à partir du seul lexique.

Usage :
    python3 scripts/rapport_definitions.py
    python3 scripts/rapport_definitions.py --verifier   # échoue si une
                                                        # définition n'a pas
                                                        # de statut
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEXIQUE = ROOT / "data" / "source" / "lexique-soninke-fr-base.csv"
SORTIE = ROOT / "docs" / "DEFINITIONS-LEXIQUE.md"

STATUTS = {
    "redigee_a_valider": "Définition rédigée, à valider par le référent",
    "a_clarifier": "Définition proposée, glose de départ à trancher (⚠)",
    "forme_derivee_du_verbe": "Définition dérivée du verbe de base (nom d'action, gérondif)",
    "": "Sans statut",
}


def lire() -> list[dict]:
    with LEXIQUE.open(encoding="utf-8", newline="") as flux:
        return [l for l in csv.DictReader(flux, delimiter=";") if l.get("id")]


def construire(lignes: list[dict]) -> tuple[list[dict], Counter, Counter]:
    par_categorie = defaultdict(lambda: {"total": 0, "definies": 0})
    for ligne in lignes:
        categorie = (ligne.get("categorie") or "(sans catégorie)").strip()
        par_categorie[categorie]["total"] += 1
        if (ligne.get("definition") or "").strip():
            par_categorie[categorie]["definies"] += 1
    tableau = sorted(
        ({"categorie": c, **compte} for c, compte in par_categorie.items()),
        key=lambda l: (-(l["total"] - l["definies"]), -l["total"], l["categorie"]),
    )
    statuts = Counter(
        (l.get("definition_statut") or "").strip() for l in lignes if (l.get("definition") or "").strip()
    )
    vides = Counter(
        (l.get("categorie") or "(sans catégorie)").strip()
        for l in lignes
        if not (l.get("definition") or "").strip()
    )
    return tableau, statuts, vides


def ecrire(tableau: list[dict], statuts: Counter, vides: Counter, lignes: list[dict]) -> Path:
    definies = sum(1 for l in lignes if (l.get("definition") or "").strip())
    total = len(lignes)
    textes = [
        "# Définitions du lexique SoninkeGPT — état des lieux",
        "",
        "Rapport calculé à partir de `data/source/lexique-soninke-fr-base.csv` par "
        "`scripts/rapport_definitions.py`. Il ne modifie aucune donnée.",
        "",
        "## Couverture",
        "",
        "| Constat | Nombre |",
        "| --- | --- |",
        f"| Entrées du lexique | **{total}** |",
        f"| Entrées avec une définition | **{definies}** |",
        f"| Entrées sans définition | **{total - definies}** |",
        f"| Couverture | **{definies * 100 // total} %** |",
        "",
        "## Par statut",
        "",
        "| Statut | Signification | Nombre |",
        "| --- | --- | --- |",
    ]
    for statut, nombre in statuts.most_common():
        textes.append(f"| `{statut or '—'}` | {STATUTS.get(statut, 'Statut non documenté')} | {nombre} |")

    textes += [
        "",
        "Les définitions marquées ⚠ ne doivent pas être présentées comme des traductions "
        "sûres : elles attendent l'arbitrage du référent "
        "([questions à trancher](QUESTIONS-REFERENT.md)).",
        "",
        "## Par catégorie",
        "",
        "Trié par nombre de définitions restantes.",
        "",
        "| Catégorie | Entrées | Définies | Restantes |",
        "| --- | --- | --- | --- |",
    ]
    for ligne in tableau:
        restantes = ligne["total"] - ligne["definies"]
        textes.append(
            f"| {ligne['categorie']} | {ligne['total']} | {ligne['definies']} | {restantes} |"
        )

    textes += [
        "",
        "## Ce qui reste à écrire",
        "",
        "| Catégorie | Entrées sans définition |",
        "| --- | --- |",
    ]
    for categorie, nombre in vides.most_common():
        if nombre:
            textes.append(f"| {categorie} | {nombre} |")

    textes += [
        "",
        "## Comment les définitions sont produites",
        "",
        "1. **Verbes du document du référent** : définition rédigée à partir de la glose "
        "attestée du lexique ([tableau complet](DEFINITIONS-VERBES-A-VALIDER.md)).",
        "2. **Autres verbes du lexique** : même méthode, dans "
        "`data/source/definitions-redigees.csv`.",
        "3. **Noms d'action et gérondifs** : définition générée par règle depuis le verbe "
        "de base, dans `data/source/definitions-formes-derivees.csv`.",
        "",
        "Aucune définition n'est inventée : quand la glose de départ est incertaine, le "
        "statut passe à `a_clarifier` et la question est portée à la fiche du référent.",
        "",
        "## Fichiers liés",
        "",
        "- `data/source/definitions-redigees.csv` — définitions rédigées à la main",
        "- `data/source/definitions-formes-derivees.csv` — définitions générées par règle",
        "- `scripts/enrichir_definitions_sans_doublons.py` — écriture sans création de ligne",
        "- `scripts/preparer_questions_referent.py` — fiche de questions",
        "- `docs/LINGUISTIC-QUALITY.md` — règles d'attestation",
        "",
    ]
    SORTIE.write_text("\n".join(textes), encoding="utf-8")
    return SORTIE


def verifier(lignes: list[dict]) -> int:
    problemes = []
    for ligne in lignes:
        definition = (ligne.get("definition") or "").strip()
        statut = (ligne.get("definition_statut") or "").strip()
        if definition and not statut:
            problemes.append(f"{ligne['id']} {ligne['soninke']} : définition sans statut")
        if statut and not definition:
            problemes.append(f"{ligne['id']} {ligne['soninke']} : statut sans définition")
        if statut and statut not in STATUTS:
            problemes.append(f"{ligne['id']} {ligne['soninke']} : statut inconnu « {statut} »")
        if len(definition) > 1 and not definition[0].isupper():
            problemes.append(f"{ligne['id']} {ligne['soninke']} : définition sans majuscule initiale")
    if problemes:
        print("✖ " + "\n✖ ".join(problemes[:30]), file=sys.stderr)
        return 1
    print("✔ Toutes les définitions ont un statut documenté.")
    return 0


def main() -> int:
    analyseur = argparse.ArgumentParser()
    analyseur.add_argument("--verifier", action="store_true")
    options = analyseur.parse_args()

    lignes = lire()
    tableau, statuts, vides = construire(lignes)
    print(f"entrées            {len(lignes)}")
    print(f"définies           {sum(1 for l in lignes if (l.get('definition') or '').strip())}")
    print(f"sans définition    {sum(1 for l in lignes if not (l.get('definition') or '').strip())}")

    if options.verifier:
        return verifier(lignes)

    print(f"→ {ecrire(tableau, statuts, vides, lignes).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
