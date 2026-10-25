#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôles obligatoires sur le lexique final complet (et pas seulement le lot).

Conditions de réussite :
  1. aucun mot soninké vide
  2. aucune traduction française vide
  3. aucun chiffre dans les formes soninkées (tête ET variantes)
  4. aucun mot anglais parasite dans les champs utilisateur
  5. aucune ponctuation parasite / balise résiduelle
  6. aucun doublon de mot soninké (normalisation NFC, casse, espaces,
     traits d'union, apostrophes, tons, chiffres d'homonyme)
  7. aucune entrée existante (sauvegarde) perdue : identifiants, formes,
     sens et variantes conservés
  8. le lexique final = sauvegarde + lots ajoutés (rien d'écrasé)

Usage : python3 scripts/controles_lexique_final.py
Code retour : 0 si tout passe, 1 sinon.
"""

from __future__ import annotations

import csv
import io
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from import_extraction_sans_doublons import cle, normaliser_glose

LEXIQUE = Path("data/source/lexique-soninke-fr-base.csv")
SAUVEGARDE = "backup-lexique-avant-integration-d-f-2026-10-25"
ATTENDUES_AJOUTEES = 768          # 771 − 2 renvois sans glose − fuxu-fuqu (variante)

# Seules « pertes » de sens autorisées : remplacements anglais → équivalent
# français de la propre colonne definition (corrections documentées).
CORRECTIONS_ATTENDUES = {
    "SNK-LEX-0500": {"A ma daga golli billati in ke"},
    "SNK-LEX-0594": {"title of honor attached to some family names, "
                     "(<Emphasized>Sisoxobula, Kamisoxobula) </Emphasized>"},
}

EN_FORTE = {"the", "of", "title", "honor", "attached", "family", "names", "wrestle",
            "drizzle", "ambusher", "holy", "spirit", "warm", "blooded", "mullet",
            "legalize", "permit", "justify", "camp", "transitive", "intransitive",
            "functions", "function", "marker", "pleased", "someone", "something",
            "first", "wrestling", "see", "entry", "variant", "wrestling"}
EN_FAIBLE = {"a", "an", "the", "of", "to", "with", "and", "is", "are", "be", "have",
             "has", "was", "were", "this", "that", "his", "her", "their", "you",
             "they", "not", "from", "for", "on", "in", "at", "by", "or", "as",
             "but", "if", "just", "done", "word", "wind", "take", "went", "about",
             "keep", "one", "its", "it", "we", "he", "she", "title"}
FR_STOP = {"le", "la", "les", "un", "une", "des", "du", "de", "au", "aux", "ce",
           "cette", "ces", "son", "sa", "ses", "leur", "qui", "que", "dont", "où",
           "pour", "avec", "dans", "sur", "sous", "par", "être", "faire", "fait",
           "se", "s'", "ne", "pas", "ou", "et", "en", "à", "très", "plus",
           "personne", "chose", "sorte", "variété", "arbre", "animal", "enfant",
           "femme", "homme", "celui", "celle", "chacun", "aussi", "entre",
           "depuis", "vers", "chez", "sans", "surtout", "est"}

RANGS: list[tuple[str, bool, str]] = []


def rang(nom: str, ok: bool, detail: str = "") -> None:
    RANGS.append((nom, ok, detail))


def segment_anglais(seg: str) -> bool:
    ws = re.findall(r"[a-zà-ÿ']+", seg.lower())
    fort = sum(1 for w in ws if w in EN_FORTE)
    faible = sum(1 for w in ws if w in EN_FAIBLE)
    fr = sum(1 for w in ws if w in FR_STOP)
    if any(c in seg for c in "àâäéèêëîïôöùûüçœæ"):
        fr += 2
    if fort >= 1 and faible + fort > fr:
        return True
    return faible >= 3 and faible > fr


def sans_guillemets(txt: str) -> str:
    return re.sub(r'"[^"]*"', '""', txt)


def _wn(seg: str) -> str:
    return " ".join(t.rstrip("s") for t in normaliser_glose(seg).split())


def _items(seg: str) -> set[str]:
    parts = re.split(r"[,;(«»\"]+", seg)
    return {_wn(p) for p in parts if normaliser_glose(p)}


def charger(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


def charger_sauvegarde() -> list[dict]:
    out = subprocess.run(["git", "show",
                          f"{SAUVEGARDE}:{LEXIQUE.as_posix()}"],
                         capture_output=True, text=True, check=True)
    return list(csv.DictReader(io.StringIO(out.stdout), delimiter=";"))


def main() -> int:
    lignes = charger(LEXIQUE)
    sauvegarde = charger_sauvegarde()

    # 1. mot non vide -------------------------------------------------------
    vides_m = [r["id"] for r in lignes if not (r["soninke"] or "").strip()]
    rang("1. aucun mot soninké vide", not vides_m, f"{len(vides_m)} vide(s)")

    # 2. français non vide --------------------------------------------------
    vides_f = [r["id"] for r in lignes if not (r["francais"] or "").strip()]
    rang("2. aucune traduction française vide", not vides_f, f"{len(vides_f)} vide(s)")

    # 3. aucun chiffre dans les formes soninkées ----------------------------
    chiffres = [(r["id"], f) for r in lignes
                for f in [r["soninke"], r["variantes"] or ""]
                if re.search(r"\d", f)]
    rang("3. aucun chiffre dans les formes soninkées (tête + variantes)",
         not chiffres, f"{len(chiffres)} forme(s) avec chiffre : {chiffres[:5]}")

    # 4. anglais parasite ---------------------------------------------------
    anglais = []
    for r in lignes:
        for champ in ("francais", "categorie"):
            val = r.get(champ) or ""
            for seg in re.split(r"\s+/\s+", val):
                if seg.strip() and segment_anglais(seg.strip()):
                    anglais.append((r["id"], champ, seg.strip()[:60]))
    rang("4. aucun mot anglais parasite dans les champs utilisateur",
         not anglais, f"{len(anglais)} segment(s) : {anglais[:5]}")

    # 5. ponctuation parasite / balises ------------------------------------
    junk = []
    for r in lignes:
        fr = r["francais"] or ""
        net = sans_guillemets(fr)
        if re.search(r"[?!]{2,}", net):
            junk.append((r["id"], "?! répétés", fr[:50]))
        if re.search(r"\.{3,}", net) and not re.search(
                r"[A-Za-zÀ-ÿ]\.{3,}[A-Za-zÀ-ÿ ]", net):
            junk.append((r["id"], "points de suspension", fr[:50]))
        if "…" in net:
            junk.append((r["id"], "…", fr[:50]))
        if re.search(r"</?[A-Za-z][^>]*>", fr):
            junk.append((r["id"], "balise résiduelle", fr[:50]))
    rang("5. aucune ponctuation parasite ou balise résiduelle",
         not junk, f"{len(junk)} cas : {junk[:5]}")

    # 6. doublons -----------------------------------------------------------
    index: dict[str, list[str]] = {}
    for r in lignes:
        index.setdefault(cle(r["soninke"]), []).append(r["id"])
    dups = {k: v for k, v in index.items() if len(v) > 1}
    # clé de contrôle indépendante (retrait total des chiffres + NFC)
    import unicodedata
    index2: dict[str, list[str]] = {}
    for r in lignes:
        k = unicodedata.normalize("NFC", r["soninke"].lower())
        k = re.sub(r"\d+", "", k)
        k = re.sub(r"[-’`]", " ", k).strip()
        k = re.sub(r"\s+", " ", k)
        index2.setdefault(k, []).append(r["id"])
    dups2 = {k: v for k, v in index2.items() if len(v) > 1}
    rang("6. aucun doublon de mot soninké (2 normalisations contrôlées)",
         not dups and not dups2,
         f"cle()={len(dups)} ; chiffres/NFC={len(dups2)} : "
         f"{list(dups.items())[:4]}{list(dups2.items())[:4]}")

    # 7. aucune entrée perdue ----------------------------------------------
    par_id_final = {r["id"]: r for r in lignes}
    perdues, sens_perdus, var_perdus = [], [], []
    for anc in sauvegarde:
        nouv = par_id_final.get(anc["id"])
        if nouv is None:
            perdues.append(anc["id"])
            continue
        if nouv["soninke"] != anc["soninke"]:
            perdues.append(f"{anc['id']} (forme modifiée)")
        # sens conservés (égalité normalisée, élément de liste ou préfixe)
        segs_fin = [s for s in (nouv["francais"] or "").split(" / ") if s.strip()]
        sens_fin = [_wn(s) for s in segs_fin]
        items_fin = set()
        for s in segs_fin:
            items_fin |= _items(s)
        for s in (anc["francais"] or "").split(" / "):
            w = _wn(s)
            if not w:
                continue
            if s.strip() in CORRECTIONS_ATTENDUES.get(anc["id"], set()):
                continue                       # remplacement anglais → français
            ok = (w in sens_fin) or (w in items_fin) or \
                 any(f.startswith(w + " ") for f in sens_fin)
            if not ok:
                sens_perdus.append(f"{anc['id']} : « {s[:40]} »")
        av = {v.strip() for v in (anc["variantes"] or "").split(",") if v.strip()}
        nv = {v.strip() for v in (nouv["variantes"] or "").split(",") if v.strip()}
        if not av <= nv:
            var_perdus.append(f"{anc['id']} : {av - nv}")
    rang("7a. aucune entrée existante perdue", not perdues,
         f"{len(perdues)} : {perdues[:5]}")
    rang("7b. aucun sens existant perdu", not sens_perdus,
         f"{len(sens_perdus)} : {sens_perdus[:5]}")
    rang("7c. aucune variante existante perdue", not var_perdus,
         f"{len(var_perdus)} : {var_perdus[:5]}")

    # 8. intégrité globale --------------------------------------------------
    ids_sauve = {r["id"] for r in sauvegarde}
    ids_final = {r["id"] for r in lignes}
    ajoutes = ids_final - ids_sauve
    supprimes = ids_sauve - ids_final
    ok8 = (not supprimes) and len(ajoutes) == ATTENDUES_AJOUTEES
    rang("8. lexique final = sauvegarde + 768 ajouts (rien d'écrasé)", ok8,
         f"ajoutées={len(ajoutes)} (attendu {ATTENDUES_AJOUTEES}) ; "
         f"supprimées={sorted(supprimes)[:5]}")

    # bilan ------------------------------------------------------------------
    print(f"Lexique : {len(lignes)} lignes (sauvegarde : {len(sauvegarde)})")
    print("-" * 72)
    tous_ok = True
    for nom, ok, detail in RANGS:
        statut = "OK  " if ok else "ÉCHEC"
        print(f"[{statut}] {nom} — {detail}")
        tous_ok = tous_ok and ok
    print("-" * 72)
    print("TOUS LES CONTRÔLES SONT PASSÉS" if tous_ok else "CONTRÔLES EN ÉCHEC")
    return 0 if tous_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
