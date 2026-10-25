#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline d'extraction du Google Doc « Dictionnaire soninké » (ga → kuyindi).

Entrée : les fichiers parsés `data/source/parts-g/part-*.tsv`
(soninke, francais, categorie, note) — une ligne par entrée du document,
gloses anglaises déjà retirées à l'analyse, chiffres d'homonyme conservés.

Étapes :
  1. concaténation des parties dans `data/source/dictionnaire-g-k-brut-2026-10-25.tsv` ;
  2. retrait de tout chiffre figurant sur un mot (gaara1 → gaara) ;
  3. fusion des homonymes (gloses jointes par « / », sans doublon interne) ;
  4. balayage anti-anglais : tout segment de glose encore anglais est supprimé ;
  5. comparaison au lexique de base (entrée OU variante) via `cle()`,
     aucune glose n'est inventée ; les entrées sans traduction française
     sont conservées mais écartées du fichier « nouveaux » ;
  6. écriture :
     - data/candidates/dictionnaire-g-k-extraction-2026-10-25.csv (tout)
     - data/candidates/dictionnaire-g-k-nouveaux-2026-10-25.csv (absents du lexique)
     - data/reports/comparaison-dictionnaire-g-k-2026-10-25.csv (audit)

Usage : python3 scripts/traiter_extraction_g_k.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = ROOT / "data" / "source" / "parts-g"
BRUT = ROOT / "data" / "source" / "dictionnaire-g-k-brut-2026-10-25.tsv"
CAND = ROOT / "data" / "candidates"
REPORTS = ROOT / "data" / "reports"
DATE = "2026-10-25"

sys.path.insert(0, str(ROOT / "scripts"))
from import_extraction_sans_doublons import (  # noqa: E402
    charger_lexique,
    cle,
    normaliser_glose,
)

# Mots-outils anglais trahissant un segment resté anglais ; leurs équivalents
# français (« de », « et », « pour »…) ne déclenchent pas la règle.
EN_OUTILS = re.compile(
    r"\b(the|with|from|which|that|this|have|has|been|were|was|and|for|to|"
    r"not|are|its|his|her|when|who|whom)\b",
    re.IGNORECASE,
)
# Quelques mots de contenu anglais repérés dans la source.
EN_CONTENU = re.compile(
    r"\b(toothpick|poverty|member|warm|multiply|encircle|valuable|above|"
    r"impersonal|poured|slice|forcefully|sexual|worry over|give a|"
    r"stir up|spit up)\b",
    re.IGNORECASE,
)


def lire_parties() -> list[dict]:
    lignes = []
    for fichier in sorted(PARTS.glob("part_*.tsv")):
        for num, ligne in enumerate(fichier.read_text(encoding="utf-8").splitlines(), 1):
            if not ligne.strip():
                continue
            champs = ligne.split("\t")
            while len(champs) < 4:
                champs.append("")
            lignes.append({
                "soninke": champs[0].strip(),
                "francais": champs[1].strip(),
                "categorie": champs[2].strip(),
                "note": champs[3].strip(),
                "origine": f"{fichier.name}:{num}",
            })
    return lignes


def ecrire_brut(lignes: list[dict]) -> None:
    with BRUT.open("w", encoding="utf-8", newline="") as fh:
        fh.write("soninke\tfrancais\tcategorie\tnote\n")
        for l in lignes:
            fh.write(f"{l['soninke']}\t{l['francais']}\t{l['categorie']}\t{l['note']}\n")


def sans_chiffres(mot: str) -> str:
    """Enlève tout chiffre figurant sur un mot : gaara1 → gaara, -i2 → -i."""
    return re.sub(r"\d+", "", mot).strip()


def segments(glose: str) -> list[str]:
    return [s.strip() for s in glose.split(" / ") if s.strip()]


def est_anglais(seg: str) -> bool:
    return bool(EN_OUTILS.search(seg) or EN_CONTENU.search(seg))


def fusionner(lignes: list[dict]) -> tuple[list[dict], list[str]]:
    """Regroupe les homonymes (mot identique après retrait des chiffres)."""
    ordre: list[str] = []
    groupes: dict[str, dict] = {}
    alertes: list[str] = []
    for l in lignes:
        mot = sans_chiffres(l["soninke"])
        g = groupes.get(mot)
        if g is None:
            g = {"soninke": mot, "fr": [], "cat": [], "note": [], "origine": []}
            groupes[mot] = g
            ordre.append(mot)
        for seg in segments(l["francais"]):
            if est_anglais(seg):
                alertes.append(f"{mot} : segment anglais supprimé : « {seg} »")
                continue
            if seg not in g["fr"]:
                g["fr"].append(seg)
        for cat in [c.strip() for c in l["categorie"].split(",") if c.strip()]:
            if cat not in g["cat"]:
                g["cat"].append(cat)
        for note in [n.strip() for n in l["note"].split(";") if n.strip()]:
            if note not in g["note"]:
                g["note"].append(note)
        g["origine"].append(l["origine"])
    sortie = []
    for mot in ordre:
        g = groupes[mot]
        sortie.append({
            "soninke": g["soninke"],
            "francais": " / ".join(g["fr"]),
            "categorie": ", ".join(g["cat"]),
            "note": "; ".join(g["note"]),
        })
    return sortie, alertes


def comparer(extraction: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    _, connues = charger_lexique()
    audit, nouveaux, alertes = [], [], []
    vus: dict[str, str] = {}
    for l in extraction:
        mot, fr = l["soninke"], l["francais"]
        k = cle(mot)
        entree = connues.get(k)
        if entree is not None:
            glose_lex = entree.get("francais", "") or ""
            if fr and normaliser_glose(fr) == normaliser_glose(glose_lex):
                statut = "doublon_ecarte_glose_identique"
            elif re.search(r"\d$", mot):
                statut = "doublon_ecarte_homonyme_deja_regroupe"
            else:
                statut = "doublon_ecarte_glose_differente"
            audit.append({**l, "statut": statut,
                          "entree_lexique": entree.get("id", ""),
                          "francais_lexique": glose_lex})
            continue
        if not fr:
            audit.append({**l, "statut": "glose_vide",
                          "entree_lexique": "", "francais_lexique": ""})
            continue
        if k in vus and vus[k] != mot:
            # Deux graphies distinctes (ex. casse) partagent la même clé.
            alertes.append(f"clé identique pour « {vus[k]} » et « {mot} » (conservés séparément)")
        vus[k] = mot
        audit.append({**l, "statut": "nouveau",
                      "entree_lexique": "", "francais_lexique": ""})
        nouveaux.append(l)
    return audit, nouveaux, alertes


def ecrire_csv(chemin: Path, lignes: list[dict], champs: list[str]) -> None:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=champs, delimiter=";",
                           quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for l in lignes:
            w.writerow({c: l.get(c, "") for c in champs})


def main() -> int:
    brut = lire_parties()
    ecrire_brut(brut)
    extraction, alertes_fusion = fusionner(brut)
    extraction.sort(key=lambda l: cle(l["soninke"]))
    audit, nouveaux, alertes_comp = comparer(extraction)

    ecrire_csv(CAND / f"dictionnaire-g-k-extraction-{DATE}.csv",
               extraction, ["soninke", "francais", "categorie", "note"])
    ecrire_csv(CAND / f"dictionnaire-g-k-nouveaux-{DATE}.csv",
               nouveaux, ["soninke", "francais", "categorie", "note"])
    ecrire_csv(REPORTS / f"comparaison-dictionnaire-g-k-{DATE}.csv",
               audit, ["soninke", "francais", "statut",
                       "entree_lexique", "francais_lexique"])

    compte: dict[str, int] = {}
    for a in audit:
        compte[a["statut"]] = compte.get(a["statut"], 0) + 1
    print(f"lignes brutes (parties)   : {len(brut)}")
    print(f"entrées après fusion      : {len(extraction)}")
    print(f"sans traduction française : {compte.get('glose_vide', 0)}")
    print(f"doublons lexique écartés  : "
          f"{sum(v for k, v in compte.items() if k.startswith('doublon_ecarte'))}")
    print(f"nouveaux (fichier dédié)  : {len(nouveaux)}")
    for a in alertes_fusion + alertes_comp:
        print(f"alerte : {a}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
