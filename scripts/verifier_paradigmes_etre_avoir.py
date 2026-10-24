#!/usr/bin/env python3
"""Contrôle de la fiche `data/source/paradigmes-etre-avoir.csv`.

Vérifie que :
  1. les colonnes attendues sont présentes ;
  2. chaque statut appartient au vocabulaire autorisé ;
  3. toute forme non vide porte une source ;
  4. une forme `non_atteste` n'a pas de forme soninké (elle ne doit rien inventer) ;
  5. aucun doublon (même construction, temps, polarité, personne) ;
  6. chaque `modele_atteste` cité depuis le lexique existe bien dans l'entrée
     SNK-LEX citée en source (protection contre les citations inventées).

Usage :
    python3 scripts/verifier_paradigmes_etre_avoir.py [--strict]

Code de sortie 1 en cas d'erreur (ou d'avertissement avec --strict).
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARADIGMES = ROOT / "data" / "source" / "paradigmes-etre-avoir.csv"
LEXIQUE = ROOT / "data" / "source" / "lexique-soninke-fr-base.csv"

COLONNES = [
    "id",
    "forme",
    "verbe_fr",
    "construction",
    "temps",
    "polarite",
    "personne",
    "francais",
    "statut",
    "source",
    "modele_atteste",
    "note",
]

STATUTS = {
    "atteste_corpus",
    "assemble_a_valider",
    "atteste_source_externe",
    "non_atteste",
}

VIDE = {"", "—", "-"}


def normaliser(texte: str) -> str:
    """Compare sans casse, sans accents, sans ponctuation finale."""
    texte = unicodedata.normalize("NFC", str(texte or ""))
    texte = texte.replace("’", "'")
    # On garde lettres, chiffres, espaces et apostrophes : la ponctuation des
    # exemples de dictionnaire varie trop pour servir de critère.
    texte = re.sub(r"[^\w\s']", " ", texte, flags=re.UNICODE)
    return re.sub(r"\s+", " ", texte).strip().casefold()


def charger_lexique():
    with LEXIQUE.open(encoding="utf-8") as flux:
        return {ligne["id"]: ligne for ligne in csv.DictReader(flux, delimiter=";")}


def main() -> int:
    analyseur = argparse.ArgumentParser()
    analyseur.add_argument("--strict", action="store_true", help="échouer aussi sur les avertissements")
    options = analyseur.parse_args()

    erreurs: list[str] = []
    avertissements: list[str] = []

    with PARADIGMES.open(encoding="utf-8") as flux:
        lecteur = csv.DictReader(flux, delimiter=";")
        manquantes = [c for c in COLONNES if c not in (lecteur.fieldnames or [])]
        if manquantes:
            print(f"✖ colonnes manquantes : {', '.join(manquantes)}", file=sys.stderr)
            return 1
        lignes = list(lecteur)

    vus: dict[tuple, str] = {}
    lexique = charger_lexique()
    compteur = {statut: 0 for statut in STATUTS}

    for ligne in lignes:
        identifiant = ligne["id"] or "(sans id)"
        statut = ligne["statut"]
        forme = (ligne["forme"] or "").strip()
        source = (ligne["source"] or "").strip()
        modele = (ligne["modele_atteste"] or "").strip()

        if statut not in STATUTS:
            erreurs.append(f"{identifiant} : statut inconnu « {statut} »")
            continue
        compteur[statut] += 1

        if statut == "non_atteste":
            if forme not in VIDE:
                erreurs.append(f"{identifiant} : statut non_atteste mais une forme est donnée ({forme})")
        else:
            if forme in VIDE:
                erreurs.append(f"{identifiant} : forme vide alors que le statut est {statut}")
            if not source:
                erreurs.append(f"{identifiant} : aucune source pour une forme publiée")

        if statut == "atteste_corpus" and not re.search(r"SNK-LEX-\d+|soninke-samples\.jsonl", source):
            avertissements.append(f"{identifiant} : atteste_corpus sans référence au corpus du projet")

        cle = (
            ligne["construction"],
            ligne["temps"],
            ligne["polarite"],
            ligne["personne"],
            ligne["verbe_fr"],
        )
        if forme not in VIDE:
            cle = cle + (normaliser(forme),)
        if cle in vus:
            erreurs.append(f"{identifiant} : doublon de {vus[cle]} ({cle[-1]})")
        vus[cle] = identifiant

        # Contrôle de citation : chaque modèle cité doit figurer dans au moins
        # une des entrées de lexique citées en source.
        cites = re.findall(r"SNK-LEX-\d+", source)
        textes = []
        for identifiant_lexique in cites:
            entree = lexique.get(identifiant_lexique)
            if entree is None:
                erreurs.append(f"{identifiant} : entrée citée absente du lexique ({identifiant_lexique})")
                continue
            textes.append(
                normaliser(entree.get("exemple_original", ""))
                + " "
                + normaliser(entree.get("francais", ""))
            )
        if modele not in VIDE and textes:
            for morceau in [m for m in re.split(r"\s*/\s*", modele) if m.strip()]:
                if not any(normaliser(morceau) in texte for texte in textes):
                    erreurs.append(
                        f"{identifiant} : le modèle « {morceau} » ne figure pas dans "
                        f"{', '.join(cites)}"
                    )

    print(f"Lignes contrôlées : {len(lignes)}")
    for statut in sorted(compteur):
        print(f"  {statut:24} {compteur[statut]:3}")
    for message in avertissements:
        print(f"⚠ {message}")
    for message in erreurs:
        print(f"✖ {message}", file=sys.stderr)

    if erreurs or (options.strict and avertissements):
        print(
            f"\n{len(erreurs)} erreur(s), {len(avertissements)} avertissement(s).",
            file=sys.stderr,
        )
        return 1

    print("\n✔ Fiche cohérente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
