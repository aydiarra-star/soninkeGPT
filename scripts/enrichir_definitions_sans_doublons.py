#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit les définitions dans le lexique, sans jamais créer de ligne.

Le lexique `data/source/lexique-soninke-fr-base.csv` ne reçoit **aucune entrée
nouvelle** : chaque définition est posée sur une entrée qui existe déjà, et le
script refuse tout ce qui ne respecte pas cette règle.

Deux sources de définitions, au même format (`soninke;definition;statut;note`) :

  - `data/source/definitions-redigees.csv` : définitions rédigées à la main
    d'après la glose française déjà attestée dans le lexique ;
  - `data/source/definitions-formes-derivees.csv` : définitions des noms
    d'action et gérondifs, générées par règle depuis le verbe de base.

Contrôles effectués avant d'écrire :

  1. chaque forme doit correspondre à **exactement une** entrée du lexique
     (comparaison du projet : casse, accents vocaliques, tirets, apostrophes et
     numéros d'homonyme ignorés ; `ñ`, `ŋ`, `ɲ` distincts) ;
  2. une forme qui n'est qu'une `variante` d'une autre entrée est refusée ;
  3. deux fichiers ne peuvent pas définir la même forme ;
  4. toute forme sans entrée est refusée : le script n'invente pas de ligne.

Contrôles effectués après écriture :

  5. même nombre de lignes, mêmes identifiants, mêmes formes soninké ;
  6. toutes les autres colonnes sont inchangées ;
  7. `scripts/check_doublons_lexique.py --strict` doit passer. Sinon le fichier
     est remis dans son état d'origine.

Usage :
    python3 scripts/enrichir_definitions_sans_doublons.py --dry-run
    python3 scripts/enrichir_definitions_sans_doublons.py
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEXIQUE = ROOT / "data" / "source" / "lexique-soninke-fr-base.csv"
SOURCES = [
    ROOT / "data" / "source" / "definitions-redigees.csv",
    ROOT / "data" / "source" / "definitions-formes-derivees.csv",
]
NOUVELLES_COLONNES = ["definition", "definition_statut"]


def charger_cle():
    chemin = ROOT / "scripts" / "import_extraction_sans_doublons.py"
    spec = importlib.util.spec_from_file_location("_import", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cle


def lire_lexique() -> tuple[list[str], list[dict]]:
    with LEXIQUE.open(encoding="utf-8", newline="") as flux:
        lecteur = csv.DictReader(flux, delimiter=";")
        colonnes = list(lecteur.fieldnames or [])
        lignes = [l for l in lecteur if (l.get("id") or "").strip()]
    return colonnes, lignes


def lire_definitions(cle) -> tuple[dict[str, dict], list[str]]:
    definitions: dict[str, dict] = {}
    erreurs: list[str] = []
    for chemin in SOURCES:
        if not chemin.exists():
            erreurs.append(f"fichier de définitions introuvable : {chemin.relative_to(ROOT)}")
            continue
        with chemin.open(encoding="utf-8", newline="") as flux:
            for ligne in csv.DictReader(flux, delimiter=";"):
                forme = (ligne.get("soninke") or "").strip()
                if not forme:
                    continue
                if cle(forme) in definitions:
                    erreurs.append(f"{forme} : définie dans deux fichiers")
                    continue
                definitions[cle(forme)] = ligne
    return definitions, erreurs


def main(argv: list[str]) -> int:
    analyseur = argparse.ArgumentParser()
    analyseur.add_argument("--dry-run", action="store_true", help="contrôle tout, n'écrit rien")
    options = analyseur.parse_args(argv)

    cle = charger_cle()
    colonnes, lignes = lire_lexique()
    par_cle: dict[str, list[dict]] = {}
    variantes: dict[str, str] = {}
    for ligne in lignes:
        par_cle.setdefault(cle(ligne["soninke"]), []).append(ligne)
        for variante in (ligne.get("variantes") or "").split(","):
            if variante.strip():
                variantes.setdefault(cle(variante), ligne["id"])

    definitions, erreurs = lire_definitions(cle)
    retenues: dict[str, dict] = {}
    for k, ligne in definitions.items():
        forme = ligne["soninke"].strip()
        texte = (ligne.get("definition") or "").strip()
        if not texte:
            erreurs.append(f"{forme} : définition vide")
            continue
        entrees = par_cle.get(k, [])
        if not entrees:
            erreurs.append(f"{forme} : aucune entrée de lexique → création refusée")
            continue
        if len(entrees) > 1:
            erreurs.append(
                f"{forme} : {len(entrees)} entrées portent cette forme "
                f"({', '.join(e['id'] for e in entrees)}) → définition refusée"
            )
            continue
        if k in variantes and cle(entrees[0]["soninke"]) != k:
            erreurs.append(f"{forme} : simple variante de {variantes[k]} → création refusée")
            continue
        retenues[entrees[0]["id"]] = ligne

    if erreurs:
        print("✖ Aucune écriture. Problèmes :", file=sys.stderr)
        for erreur in erreurs:
            print("  - " + erreur, file=sys.stderr)
        return 1

    deja = sum(1 for l in lignes if (l.get("definition") or "").strip())
    print(f"lexique            {len(lignes)} entrées")
    print(f"définitions lues   {len(definitions)} (réparties sur {len(retenues)} entrées)")
    print(f"déjà définies      {deja}")
    print("lignes à ajouter   0")

    if options.dry_run:
        for identifiant, ligne in list(retenues.items())[:5]:
            print(f"  {identifiant} {ligne['soninke']} → {ligne['definition'][:70]}")
        print("✔ Contrôles passés, rien n'a été écrit (--dry-run).")
        return 0

    sortie_colonnes = colonnes + [c for c in NOUVELLES_COLONNES if c not in colonnes]
    for ligne in lignes:
        ligne.setdefault("definition", "")
        ligne.setdefault("definition_statut", "")
    par_id = {l["id"]: l for l in lignes}
    for identifiant, ligne in retenues.items():
        par_id[identifiant]["definition"] = ligne["definition"].strip()
        par_id[identifiant]["definition_statut"] = (ligne.get("statut") or "").strip()

    sauvegarde = LEXIQUE.with_suffix(".csv.avant-definitions")
    shutil.copyfile(LEXIQUE, sauvegarde)

    fichier_temporaire = tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", newline="", delete=False, dir=LEXIQUE.parent, suffix=".tmp"
    )
    try:
        with fichier_temporaire as flux:
            ecrivain = csv.DictWriter(
                flux, fieldnames=sortie_colonnes, delimiter=";", lineterminator="\n"
            )
            ecrivain.writeheader()
            for ligne in lignes:
                ecrivain.writerow({c: ligne.get(c, "") for c in sortie_colonnes})
        Path(fichier_temporaire.name).replace(LEXIQUE)
    except Exception:
        Path(fichier_temporaire.name).unlink(missing_ok=True)
        raise

    # ── Contrôles après écriture ────────────────────────────
    _, lignes_apres = lire_lexique()
    problemes = []
    if len(lignes_apres) != len(lignes):
        problemes.append(f"nombre de lignes modifié : {len(lignes)} → {len(lignes_apres)}")
    if [l["id"] for l in lignes_apres] != [l["id"] for l in lignes]:
        problemes.append("liste des identifiants modifiée")
    if [l["soninke"] for l in lignes_apres] != [l["soninke"] for l in lignes]:
        problemes.append("liste des formes soninké modifiée")
    for avant, apres in zip(lignes, lignes_apres):
        for colonne in colonnes:
            if avant.get(colonne, "") != apres.get(colonne, ""):
                problemes.append(f"{apres['id']} : la colonne {colonne} a changé")
    definies = sum(1 for l in lignes_apres if (l.get("definition") or "").strip())
    if definies != len(retenues):
        problemes.append(f"définitions écrites : {definies} au lieu de {len(retenues)}")

    controle = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_doublons_lexique.py"), "--strict"],
        cwd=ROOT, capture_output=True, text=True,
    )
    print(controle.stdout.strip())
    if controle.returncode != 0:
        problemes.append("check_doublons_lexique.py --strict a échoué")
        problemes.append(controle.stderr.strip())

    if problemes:
        shutil.copyfile(sauvegarde, LEXIQUE)
        print("✖ Écriture annulée, lexique restauré :", file=sys.stderr)
        for probleme in problemes:
            print("  - " + probleme, file=sys.stderr)
        return 1

    sauvegarde.unlink()
    print(f"✔ {len(retenues)} définitions écrites sur des entrées existantes, "
          f"{len(lignes_apres)} entrées au total : aucune ligne ajoutée.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
