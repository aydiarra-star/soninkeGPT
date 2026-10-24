#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Importe un CSV d'extraction dans le lexique principal SANS créer de doublon.

Règle appliquée : un mot déjà présent dans `soninke` **ou** dans `variantes`
(d'après une comparaison insensible aux accents, à la casse, aux traits
d'union, aux apostrophes et aux numéros d'homonyme) n'est jamais réimporté,
même si sa glose diffère. Les entrées réellement nouvelles sont ajoutées à la
fin de `data/source/lexique-soninke-fr-base.csv` avec un identifiant
`SNK-LEX-xxxx` et le statut lexical demandé.

Usage :
    python3 scripts/import_extraction_sans_doublons.py \
        data/candidates/dictionnaire-b-f-extraction-2026-10-24.csv

    # simulation, n'écrit rien :
    python3 scripts/import_extraction_sans_doublons.py ENTREE.csv --dry-run

Sortie : un compte rendu imprimé et
`data/reports/import-extraction-<date>.csv` (importés / doublons écartés).
"""

from __future__ import annotations

import csv
import datetime as dt
import re
import sys
import unicodedata
from pathlib import Path

LEXIQUE = Path("data/source/lexique-soninke-fr-base.csv")
CHAMPS = ["id", "soninke", "francais", "categorie", "source", "statut",
          "variantes", "exemple_original", "definition", "definition_statut"]

SOURCE = "Dictionnaire soninké.docx (Google Doc b–f) 2026-10-24"
STATUT = "candidat_dictionnaire_a_verifier"


VOYELLES = set("aeiou")


def sans_accents_vocaliques(mot: str) -> str:
    """Retire les accents des voyelles, mais garde ñ / ŋ / ɲ / ɓ / ɗ distincts.

    Sans cette précaution, *segeñe* « ongle » et *segene* « monter » se
    confondraient : la comparaison anti-doublon écarterait un mot réel.
    """
    sortie = []
    for c in mot:
        base = unicodedata.normalize("NFD", c)
        if len(base) > 1 and base[0] in VOYELLES:
            sortie.append(base[0])
        else:
            sortie.append(c)
    return unicodedata.normalize("NFC", "".join(sortie))


def cle(mot: str) -> str:
    """Clé de comparaison : ni casse, ni accents vocaliques, ni tirets, ni homonymes."""
    mot = sans_accents_vocaliques(mot.strip().lower())
    mot = re.sub(r"-", " ", mot)
    mot = re.sub(r"[’`]", "'", mot)      # l'apostrophe reste distinctive : n ≠ n'
    mot = re.sub(r"\s*\d+$", "", mot)          # baabo1 -> baabo
    mot = re.sub(r"[^a-z0-9ñɓɗƴŋɲɛɔ ']", "", mot)
    return re.sub(r"\s+", " ", mot).strip()


def charger_lexique():
    with LEXIQUE.open(encoding="utf-8", newline="") as fh:
        lecteur = csv.DictReader(fh, delimiter=";")
        lignes = list(lecteur)
    connues = {}
    for ligne in lignes:
        if not ligne.get("id"):
            continue
        for forme in [ligne["soninke"], *(ligne.get("variantes") or "").split(",")]:
            if forme and forme.strip():
                connues.setdefault(cle(forme), ligne)
    return lignes, connues


def normaliser_glose(txt: str) -> str:
    """Comparaison de gloses : minuscules, sans ponctuation ni espaces doubles."""
    txt = sans_accents_vocaliques(txt.lower())
    txt = re.sub(r"[^a-z0-9ñɓɗƴŋɲɛɔ ]", " ", txt)
    return re.sub(r"\s+", " ", txt).strip()


def prochain_id(lignes) -> int:
    nums = [int(m.group(1)) for l in lignes
            if (m := re.match(r"SNK-LEX-(\d+)$", l["id"]))]
    return max(nums) + 1


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    entree = Path(argv[1])
    simulation = "--dry-run" in argv
    lignes, connues = charger_lexique()
    numero = prochain_id(lignes)

    with entree.open(encoding="utf-8", newline="") as fh:
        extraction = list(csv.DictReader(fh, delimiter=";"))

    importes, doublons, vides = [], [], []
    vus = set()
    for ligne in extraction:
        mot = (ligne.get("soninke") or "").strip()
        fr = (ligne.get("francais") or "").strip()
        if not mot or not fr:
            vides.append(ligne)
            continue
        k = cle(mot)
        if k in connues:
            existant = connues[k]
            glose_lex = existant.get("francais", "")
            if normaliser_glose(glose_lex) == normaliser_glose(fr):
                etat = "glose identique"
            elif re.search(r"\d$", mot):
                # baabo1 / baabo2 : homonymes numérotés du document, déjà
                # regroupés dans un seul article du lexique
                etat = "homonyme deja regroupe"
            else:
                etat = "glose differente"
            doublons.append((mot, existant["id"], fr, glose_lex, etat))
            continue
        if k in vus:                      # doublon interne au fichier d'entrée
            doublons.append((mot, "même fichier", fr, "", "doublon interne"))
            continue
        vus.add(k)
        importes.append({
            "id": f"SNK-LEX-{numero:04d}",
            "soninke": mot,
            "francais": fr,
            "categorie": (ligne.get("categorie") or "").strip(),
            "source": SOURCE,
            "statut": STATUT,
            "variantes": "",
            "exemple_original": (ligne.get("note") or "").strip(),
            "definition": "",
            "definition_statut": "",
        })
        numero += 1

    if not simulation and importes:
        # ajout en fin de fichier : on ne réécrit jamais le lexique existant,
        # pour ne pas modifier les guillemets, l'ordre ni les lignes déjà validées.
        with LEXIQUE.open("a", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=CHAMPS, delimiter=";",
                               quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
            w.writerows(importes)

    if not simulation:
        rapport = Path(f"data/reports/import-extraction-{dt.date.today()}.csv")
        rapport.parent.mkdir(parents=True, exist_ok=True)
        with rapport.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, delimiter=";")
            w.writerow(["resultat", "soninke", "francais", "reference"])
            for l in importes:
                w.writerow(["importe", l["soninke"], l["francais"], l["id"]])
            for mot, ref, glose_new, glose_lex, etat in doublons:
                w.writerow([f"doublon_ecarte_{etat.replace(' ', '_').replace('é', 'e')}", mot,
                            glose_new, f"{ref} | lexique: {glose_lex}"])
            for l in vides:
                w.writerow(["glose_vide", l.get("soninke", ""), "", ""])
        print(f"rapport : {rapport}")

    print(f"lues : {len(extraction)} | importées : {len(importes)} | "
          f"doublons écartés : {len(doublons)} | gloses vides : {len(vides)}")
    for l in importes:
        print(f"  + {l['id']}  {l['soninke']}  →  {l['francais']}")
    divergents = [d for d in doublons if d[4] == "glose differente"]
    if divergents:
        print(f"\n{len(divergents)} doublon(s) dont la glose du document diffère "
              f"du lexique (rien n'est importé ; à arbitrer à la main) :")
        for mot, ref, glose_new, glose_lex, _ in divergents[:40]:
            print(f"  = {mot} ({ref})  lexique: {glose_lex[:60]}  |  doc: {glose_new[:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
