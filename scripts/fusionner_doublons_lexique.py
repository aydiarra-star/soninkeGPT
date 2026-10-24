#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fusionne les doublons du lexique principal, sans perte d'information.

Le script compare les entrées deux à deux avec la même normalisation que
`check_doublons_lexique.py`, propose une action, et — avec `--appliquer` —
fusionne uniquement les cas sûrs :

* `fusionner` : une des deux entrées est un simple renvoi (« renvoi à X »,
  « variante de X ») ou porte exactement la même glose sans audio propre.
  La forme absorbée devient une `variante` de l'entrée conservée, la glose la
  plus complète est gardée, et une note de fusion est ajoutée pour la
  traçabilité.
* `garder` : sens différents, ou deux formes réellement distinctes ayant
  chacune leur audio (par exemple *Giya* et *yesso*). Rien n'est touché.

Toute fusion est écrite dans `data/reports/fusions-doublons-<date>.csv`.

Usage :
    python3 scripts/fusionner_doublons_lexique.py            # propose seulement
    python3 scripts/fusionner_doublons_lexique.py --appliquer
"""

from __future__ import annotations

import csv
import datetime as dt
import io
import importlib.util
import sys
from pathlib import Path

LEXIQUE = Path("data/source/lexique-soninke-fr-base.csv")
QUEUE = Path("data/source/head-face-audio-recording-queue.csv")
CHAMPS = ["id", "soninke", "francais", "categorie", "source", "statut",
          "variantes", "exemple_original"]

RANG = {"valide_par_referent_linguistique": 5, "valide_par_referent": 4,
        "atteste_source_externe": 3, "corrige_atteste_source_externe": 3,
        "atteste_selon_referent_a_verifier": 2,
        "candidat_dictionnaire_a_verifier": 1}


def _cle():
    chemin = Path(__file__).with_name("import_extraction_sans_doublons.py")
    spec = importlib.util.spec_from_file_location("_imp", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cle, module.normaliser_glose


def charger():
    with LEXIQUE.open(encoding="utf-8", newline="") as fh:
        lignes = [l for l in csv.DictReader(fh, delimiter=";") if l.get("id")]
    return lignes


def ids_audio() -> set[str]:
    if not QUEUE.exists():
        return set()
    with QUEUE.open(encoding="utf-8", newline="") as fh:
        return {l.get("identifiant_audio", "") for l in csv.DictReader(fh)}


def rang(entree) -> int:
    statuts = (entree.get("statut") or "").split(";")
    return max([RANG.get(s.strip(), 0) for s in statuts] or [0])


def est_renvoi(entree) -> bool:
    g = (entree.get("francais") or "").lower()
    return g.startswith("renvoi à") or g.startswith("variante de")


def cible_renvoi(entree, par_forme) -> str | None:
    g = (entree.get("francais") or "")
    for marqueur in ("renvoi à", "variante de"):
        if marqueur in g.lower():
            apres = g.lower().split(marqueur, 1)[1]
            mot = apres.split(":")[0].strip(" .:;")
            entree_cible = par_forme.get(mot)
            if entree_cible:
                return entree_cible["id"]
    return None


def main(argv: list[str]) -> int:
    appliquer = "--appliquer" in argv
    cle, norm = _cle()
    lignes = charger()
    audio = ids_audio()
    par_id = {l["id"]: l for l in lignes}
    par_forme: dict[str, dict] = {}
    for l in lignes:
        par_forme.setdefault(cle(l["soninke"]), l)

    # paires uniques d'entrées qui partagent une forme
    paires: dict[tuple[str, str], str] = {}
    for l in lignes:
        for forme in [l["soninke"], *(l.get("variantes") or "").split(",")]:
            if not forme or not forme.strip():
                continue
            autre = par_forme.get(cle(forme))
            if autre and autre["id"] != l["id"]:
                paires[tuple(sorted((l["id"], autre["id"])))] = cle(forme)

    decisions = []
    for (a, b), k in sorted(paires.items()):
        ea, eb = par_id[a], par_id[b]
        if est_renvoi(ea) and cible_renvoi(ea, par_forme) == b:
            decisions.append((a, b, "fusionner", "renvoi vers l'autre entrée"))
        elif est_renvoi(eb) and cible_renvoi(eb, par_forme) == a:
            decisions.append((b, a, "fusionner", "renvoi vers l'autre entrée"))
        elif norm(ea["francais"]) == norm(eb["francais"]):
            if a in audio and b in audio:
                decisions.append((a, b, "garder", "même glose mais deux audios"))
            elif b in audio:
                decisions.append((a, b, "fusionner", "même glose, audio sur l'autre"))
            elif a in audio:
                decisions.append((b, a, "fusionner", "même glose, audio sur l'autre"))
            elif rang(ea) > rang(eb):
                decisions.append((b, a, "fusionner", "même glose, statut plus fort"))
            else:
                decisions.append((a, b, "fusionner", "même glose"))
        else:
            decisions.append((a, b, "garder", "gloses différentes"))

    print(f"{len(decisions)} paires examinées : "
          f"{sum(1 for d in decisions if d[2] == 'fusionner')} fusion(s), "
          f"{sum(1 for d in decisions if d[2] == 'garder')} à conserver.")
    for src, dst, action, motif in decisions:
        if action != "fusionner":
            continue
        print(f"  {src} {par_id[src]['soninke']:12} → {dst} {par_id[dst]['soninke']:12} "
              f"({motif})")

    journal = Path(f"data/reports/fusions-doublons-{dt.date.today()}.csv")
    journal.parent.mkdir(parents=True, exist_ok=True)
    with journal.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["action", "entree_absorbee", "entree_conservee", "forme",
                    "motif", "glose_absorbee", "glose_conservee"])
        for src, dst, action, motif in decisions:
            w.writerow([action, src, dst, par_id[src]["soninke"], motif,
                        par_id[src]["francais"], par_id[dst]["francais"]])
    print(f"journal : {journal}")

    if not appliquer:
        print("\n(simulation : relancer avec --appliquer pour fusionner)")
        return 0

    absorbes, modifies = set(), {}
    for src, dst, action, motif in decisions:
        if action != "fusionner" or src in absorbes:
            continue
        es, ed = par_id[src], par_id[dst]
        # 1. la forme absorbée devient variante de l'entrée conservée
        variantes = [v.strip() for v in (ed.get("variantes") or "").split(",") if v.strip()]
        for forme in [es["soninke"], *(es.get("variantes") or "").split(",")]:
            forme = forme.strip()
            if (forme and cle(forme) != cle(ed["soninke"])
                    and cle(forme) not in [cle(v) for v in variantes]):
                variantes.append(forme)
        ed["variantes"] = ", ".join(variantes)
        # 2. glose : la plus complète, mais jamais une glose de renvoi
        #    (« renvoi à X : … ») qui ne définirait pas le mot conservé
        if (not est_renvoi(es) and not est_renvoi(ed)
                and len(es["francais"]) > len(ed["francais"])):
            ed["francais"] = es["francais"]
        # 3. traçabilité
        note = (f"Fusion {dt.date.today()} : {src} ({es['soninke']} « {es['francais']} », "
                f"{es['statut']}) absorbé — {motif}.")
        ed["exemple_original"] = (ed.get("exemple_original") or "").strip()
        ed["exemple_original"] = (ed["exemple_original"] + " " + note).strip()
        modifies[dst] = ed
        absorbes.add(src)

    # réécriture ligne à ligne : les lignes non touchées restent identiques
    # à l'octet près, ce qui garde un diff lisible et vérifiable.
    brut = LEXIQUE.read_text(encoding="utf-8").splitlines()
    # Colonnes réellement présentes dans le fichier : une ligne réécrite ne
    # doit jamais perdre une colonne ajoutée depuis (définitions, par exemple).
    colonnes_fichier = brut[0].split(";") if brut else CHAMPS
    sortie, vus = [], 0
    for ligne in brut:
        identifiant = ligne.split(";", 1)[0]
        if identifiant in absorbes:
            vus += 1
            continue
        if identifiant in modifies:
            buffer = io.StringIO()
            csv.DictWriter(buffer, fieldnames=colonnes_fichier, delimiter=";",
                           extrasaction="ignore", quoting=csv.QUOTE_MINIMAL,
                           lineterminator="").writerow(modifies[identifiant])
            ligne = buffer.getvalue()
        sortie.append(ligne)
    LEXIQUE.write_text("\n".join(sortie) + "\n", encoding="utf-8")
    print(f"\n{len(absorbes)} entrée(s) absorbée(s) ({vus} lignes retirées) ; "
          f"{len(sortie) - 1} entrées restantes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
