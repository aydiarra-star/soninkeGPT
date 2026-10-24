#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit les définitions des verbes dans le lexique, sans jamais créer de ligne.

Le lexique `data/source/lexique-soninke-fr-base.csv` ne reçoit **aucune entrée
nouvelle** : chaque définition est posée sur une entrée qui existe déjà, et le
script refuse tout ce qui ne respecte pas cette règle.

Contrôles effectués avant d'écrire :

  1. chaque `id_lexique` du fichier de définitions doit exister dans le lexique ;
  2. la `forme` de la ligne doit correspondre au `soninke` de cette entrée
     (comparaison du projet : casse, accents vocaliques, tirets, apostrophes et
     numéros d'homonyme ignorés ; `ñ`, `ŋ`, `ɲ` distincts) ;
  3. deux lignes ne peuvent pas viser le même identifiant ;
  4. une forme qui ne serait qu'une `variante` d'une autre entrée est refusée.

Contrôles effectués après écriture :

  5. même nombre de lignes, mêmes identifiants, mêmes formes soninké ;
  6. toutes les autres colonnes sont inchangées, à la valeur près ;
  7. `scripts/check_doublons_lexique.py --strict` doit passer. Sinon le fichier
     est remis dans son état d'origine.

Usage :
    python3 scripts/enrichir_verbes_sans_doublons.py --dry-run
    python3 scripts/enrichir_verbes_sans_doublons.py
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
DEFINITIONS = ROOT / "data" / "candidates" / "definitions-verbes-2026-10-24.csv"
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


def main(argv: list[str]) -> int:
    analyseur = argparse.ArgumentParser()
    analyseur.add_argument("--dry-run", action="store_true", help="contrôle tout, n'écrit rien")
    options = analyseur.parse_args(argv)

    cle = charger_cle()
    colonnes, lignes = lire_lexique()
    par_id = {l["id"]: l for l in lignes}
    variantes = {}
    for ligne in lignes:
        for variante in (ligne.get("variantes") or "").split(","):
            if variante.strip():
                variantes.setdefault(cle(variante), ligne["id"])

    with DEFINITIONS.open(encoding="utf-8", newline="") as flux:
        definitions = [l for l in csv.DictReader(flux, delimiter=";") if (l.get("forme") or "").strip()]

    erreurs: list[str] = []
    retenues: dict[str, dict] = {}
    for ligne in definitions:
        forme = ligne["forme"].strip()
        identifiant = (ligne.get("id_lexique") or "").strip()
        definition = (ligne.get("definition_proposee") or "").strip()

        if not definition:
            erreurs.append(f"{forme} : définition vide")
            continue
        if identifiant not in par_id:
            erreurs.append(f"{forme} : identifiant {identifiant!r} absent du lexique → création refusée")
            continue
        if cle(par_id[identifiant]["soninke"]) != cle(forme):
            erreurs.append(
                f"{forme} : l'entrée {identifiant} porte « {par_id[identifiant]['soninke']} » → "
                "la définition ne vise pas le bon mot"
            )
            continue
        if identifiant in retenues:
            erreurs.append(f"{forme} : l'entrée {identifiant} est définie deux fois")
            continue
        if cle(forme) in variantes and cle(par_id[identifiant]["soninke"]) != cle(forme):
            erreurs.append(f"{forme} : simple variante d'une autre entrée → création refusée")
            continue
        retenues[identifiant] = ligne

    if erreurs:
        print("✖ Aucune écriture. Problèmes :", file=sys.stderr)
        for erreur in erreurs:
            print("  - " + erreur, file=sys.stderr)
        return 1

    print(f"lexique      {len(lignes)} entrées")
    print(f"définitions  {len(retenues)} visant une entrée existante")
    print(f"lignes à ajouter 0")

    if options.dry_run:
        for identifiant, ligne in list(retenues.items())[:5]:
            print(f"  {par_id[identifiant]['soninke']} → {ligne['definition_proposee'][:70]}")
        print("✔ Contrôles passés, rien n'a été écrit (--dry-run).")
        return 0

    sortie_colonnes = colonnes + [c for c in NOUVELLES_COLONNES if c not in colonnes]
    for identifiant, ligne in retenues.items():
        par_id[identifiant]["definition"] = ligne["definition_proposee"].strip()
        par_id[identifiant]["definition_statut"] = ligne["statut_validation"].strip()
    for ligne in lignes:
        ligne.setdefault("definition", "")
        ligne.setdefault("definition_statut", "")

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
    colonnes_apres, lignes_apres = lire_lexique()
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
