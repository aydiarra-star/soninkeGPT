#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prépare les questions à poser au référent sur les gloses incertaines.

Toutes les définitions écrites dans le lexique ne se valent pas : celles qui
reposent sur une glose douteuse, contradictoire ou incomplète portent le statut
`a_clarifier`. Ce script les rassemble en une fiche de questions prête à être
remplie par le référent, sans jamais proposer de réponse à sa place.

Sorties :
  - `data/reviews/questions-referent-2026-10-24.csv` — à remplir (colonnes
    `reponse_referent` et `date_reponse` vides) ;
  - `docs/QUESTIONS-REFERENT.md` — même contenu, lisible et imprimable.

Usage :
    python3 scripts/preparer_questions_referent.py
    python3 scripts/preparer_questions_referent.py --verifier
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEXIQUE = ROOT / "data" / "source" / "lexique-soninke-fr-base.csv"
SOURCES = [
    ROOT / "data" / "source" / "definitions-redigees.csv",
    ROOT / "data" / "source" / "definitions-formes-derivees.csv",
]
SORTIE_CSV = ROOT / "data" / "reviews" / "questions-referent-2026-10-24.csv"
SORTIE_MD = ROOT / "docs" / "QUESTIONS-REFERENT.md"
DATE = "2026-10-24"

COLONNES = [
    "id_lexique",
    "soninke",
    "categorie",
    "glose_du_lexique",
    "definition_proposee",
    "point_a_trancher",
    "question",
    "reponse_referent",
    "date_reponse",
]


def lire_notes() -> dict[str, str]:
    notes: dict[str, str] = {}
    for chemin in SOURCES:
        if not chemin.exists():
            continue
        with chemin.open(encoding="utf-8", newline="") as flux:
            for ligne in csv.DictReader(flux, delimiter=";"):
                forme = (ligne.get("soninke") or "").strip()
                if forme:
                    notes[forme] = (ligne.get("note") or "").strip()
    return notes


def construire() -> list[dict]:
    notes = lire_notes()
    with LEXIQUE.open(encoding="utf-8", newline="") as flux:
        lignes = [l for l in csv.DictReader(flux, delimiter=";") if l.get("id")]

    questions = []
    for ligne in lignes:
        if (ligne.get("definition_statut") or "").strip() != "a_clarifier":
            continue
        forme = ligne["soninke"].strip()
        point = notes.get(forme, "")
        if not point:
            point = "Une partie de la glose du lexique n'a pas pu être confirmée."
        questions.append(
            {
                "id_lexique": ligne["id"],
                "soninke": forme,
                "categorie": ligne.get("categorie", ""),
                "glose_du_lexique": ligne.get("francais", ""),
                "definition_proposee": ligne.get("definition", ""),
                "point_a_trancher": point,
                "question": (
                    "La définition proposée est-elle juste ? Si non, quel est le sens exact, "
                    "et faut-il scinder la glose en plusieurs mots ?"
                ),
                "reponse_referent": "",
                "date_reponse": "",
            }
        )
    questions.sort(key=lambda q: (q["soninke"].lower(), q["id_lexique"]))
    return questions


def ecrire_csv(questions: list[dict]) -> Path:
    SORTIE_CSV.parent.mkdir(parents=True, exist_ok=True)
    with SORTIE_CSV.open("w", encoding="utf-8", newline="") as flux:
        ecrivain = csv.DictWriter(flux, fieldnames=COLONNES, delimiter=";", lineterminator="\n")
        ecrivain.writeheader()
        for question in questions:
            ecrivain.writerow(question)
    return SORTIE_CSV


def ecrire_markdown(questions: list[dict]) -> Path:
    textes = [
        "# Questions au référent linguistique — gloses à trancher",
        "",
        f"Fiche préparée le {DATE} à partir du lexique du projet. Chaque ligne signale un "
        "mot dont la définition repose sur une glose incertaine, contradictoire ou "
        "incomplète. **Aucune définition n'est imposée au référent** : la colonne de "
        "réponse doit rester vide jusqu'à sa réponse.",
        "",
        "## Comment répondre",
        "",
        "1. Lire la glose du lexique et la définition proposée.",
        "2. Écrire la réponse dans `reponse_referent` du fichier "
        f"`{SORTIE_CSV.relative_to(ROOT)}` (ou à la main sur cette page).",
        "3. Indiquer la date de la réponse.",
        "4. Tant qu'une ligne n'a pas de réponse, le mot reste marqué "
        "« glose à vérifier » dans l'application et dans les documents : il n'est "
        "jamais présenté comme une traduction sûre.",
        "",
        f"**{len(questions)} mots à trancher.**",
        "",
        "## Tableau des questions",
        "",
        "| Soninké | Catégorie | Glose du lexique | Définition proposée | Ce qui bloque | Réponse du référent |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for question in questions:
        cellules = [
            f"**{question['soninke']}** (`{question['id_lexique']}`)",
            question["categorie"],
            question["glose_du_lexique"],
            question["definition_proposee"],
            question["point_a_trancher"],
            "",
        ]
        textes.append("| " + " | ".join(c.replace("|", "\\|") for c in cellules) + " |")

    textes += [
        "",
        "## Fichiers liés",
        "",
        f"- `{SORTIE_CSV.relative_to(ROOT)}` — fiche à remplir",
        "- `data/source/definitions-redigees.csv` — définitions et notes d'origine",
        "- `docs/DEFINITIONS-VERBES-A-VALIDER.md` — définitions des 182 verbes du document",
        "- `scripts/preparer_questions_referent.py` — génération de cette fiche",
        "",
    ]
    SORTIE_MD.write_text("\n".join(textes), encoding="utf-8")
    return SORTIE_MD


def main() -> int:
    analyseur = argparse.ArgumentParser()
    analyseur.add_argument("--verifier", action="store_true", help="contrôle sans réécrire")
    options = analyseur.parse_args()

    questions = construire()
    print(f"questions                {len(questions)}")
    print(f"réponses déjà fournies   {sum(1 for q in questions if q['reponse_referent'])}")

    if options.verifier:
        if not questions:
            print("✖ aucune question générée : le statut a_clarifier a-t-il disparu ?", file=sys.stderr)
            return 1
        print("✔ Fiche de questions cohérente.")
        return 0

    print(f"→ {ecrire_csv(questions).relative_to(ROOT)}")
    print(f"→ {ecrire_markdown(questions).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
