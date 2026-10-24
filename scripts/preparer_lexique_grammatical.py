#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit les livrables du lot 5 : lexique grammatical structuré,
nouvelles entrées et rapport de comparaison avec le lexique existant.

Entrées :
  - scripts/lexique_grammatical_data.py       (lignes curatées, sections A à G)
  - data/source/paradigmes-etre-avoir.csv     (64 lignes SNK-EA, conversion)
  - data/source/snk-engine-corpus-grammatical-2026-10-24.jsonl
        (corpus validation_02 : 200 phrases conjuguées annotées par règles)
  - data/source/lexique-soninke-fr-base.csv   (comparaison / dédoublonnage)

Sorties :
  - data/candidates/lexique-grammatical-structure-2026-10-24.csv
  - data/candidates/lexique-grammatical-structure-2026-10-24.json
  - data/candidates/nouvelles-entrees-grammaticales-2026-10-24.csv
  - data/reports/comparaison-grammatical-2026-10-24.csv

Rien n'est écrit dans data/source/ : le lexique existant n'est jamais modifié.
Usage : python3 scripts/preparer_lexique_grammatical.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "scripts"))

from lexique_grammatical_data import LIGNE, PROJET  # noqa: E402
from import_extraction_sans_doublons import cle      # noqa: E402

DATE = "2026-10-24"
EA_CSV = RACINE / "data/source/paradigmes-etre-avoir.csv"
CORPUS = RACINE / f"data/source/snk-engine-corpus-grammatical-{DATE}.jsonl"
BASE = RACINE / "data/source/lexique-soninke-fr-base.csv"

SORTIE_CSV = RACINE / f"data/candidates/lexique-grammatical-structure-{DATE}.csv"
SORTIE_JSON = RACINE / f"data/candidates/lexique-grammatical-structure-{DATE}.json"
SORTIE_NOUV = RACINE / f"data/candidates/nouvelles-entrees-grammaticales-{DATE}.csv"
SORTIE_COMP = RACINE / f"data/reports/comparaison-grammatical-{DATE}.csv"

COLONNES = [
    "id_provisoire", "forme_soninke", "traduction_francaise",
    "categorie_grammaticale", "sous_categorie",
    "forme_ou_construction_grammaticale", "personne", "nombre",
    "temps_aspect_mode", "polarite", "variante", "variete_regionale",
    "exemple_soninke", "traduction_exemple", "source", "page_ou_localisation",
    "niveau_de_confiance", "statut_validation", "notes",
]

# ---------------------------------------------------------------------------
# 1. Conversion des paradigmes être/avoir existants (SNK-EA)
# ---------------------------------------------------------------------------
STATUT_EA = {
    "atteste_corpus": ("SOURCE_VERIFIEE", "élevé"),
    "atteste_source_externe": ("A_CONFIRMER_PAR_LOCUTEUR", "moyen"),
    "assemble_a_valider": ("HYPOTHESE_NON_VALIDEE", "faible"),
}


def convertir_ea():
    """Convertit paradigmes-etre-avoir.csv au schéma des 19 colonnes.

    Les lignes non_atteste (forme « — ») sont ignorées : elles documentent des
    lacunes et restent décrites dans le rapport qualité.
    """
    lignes, ignorees = [], 0
    with EA_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=";"):
            forme = (row.get("forme") or "").strip()
            statut_ea = (row.get("statut") or "").strip()
            if not forme or forme == "—" or statut_ea == "non_atteste":
                ignorees += 1
                continue
            statut, conf = STATUT_EA.get(
                statut_ea, ("A_CONFIRMER_PAR_LOCUTEUR", "faible"))
            personne, nombre = "", ""
            pers = (row.get("personne") or "").strip()
            m = re.match(r"^([123])(sg|pl)$", pers)
            if m:
                personne, nombre = m.group(1), m.group(2)
            verbe = (row.get("verbe_fr") or "").strip()
            categorie = "copule" if verbe == "être" else "construction_possessive"
            note = (row.get("note") or "").strip()
            modele = (row.get("modele_atteste") or "").strip()
            notes = f"Converti depuis {row['id']} (paradigmes-etre-avoir.csv, statut d'origine : {statut_ea})."
            if modele:
                notes += f" Modèle attesté : {modele}."
            if note:
                notes += f" {note}"
            lignes.append(dict(
                forme_soninke=forme,
                traduction_francaise=(row.get("francais") or "").strip(),
                categorie_grammaticale=categorie,
                sous_categorie=(row.get("construction") or "").strip(),
                forme_ou_construction_grammaticale=(row.get("construction") or "").strip(),
                personne=personne, nombre=nombre,
                temps_aspect_mode=(row.get("temps") or "").strip(),
                polarite=(row.get("polarite") or "").strip(),
                variante="", variete_regionale=PROJET,
                exemple_soninke=forme,
                traduction_exemple=(row.get("francais") or "").strip(),
                source="Projet SoninkeGPT — data/source/paradigmes-etre-avoir.csv ; docs/VERBES-ETRE-AVOIR.md",
                page_ou_localisation=row["id"],
                niveau_de_confiance=conf, statut_validation=statut, notes=notes))
    return lignes, ignorees


# ---------------------------------------------------------------------------
# 2. Formes conjuguées — corpus validation_02 annoté par règles
# ---------------------------------------------------------------------------
VERBES = {
    "daga": ("partir", "dagana", "dagaye"),
    "faye": ("regarder", "fayeni", "fayinde"),
    "goli": ("travailler", "golini", "goliye"),
    "mini": ("boire", "minini", "mine"),
    "ri": ("venir", "rini", "riye"),
    "safa": ("écrire", "safana", "safande"),
    "sefe": ("parler", "sefene", "sefeye"),
    "wori": ("voir", "worini", "woriye"),
    "wuru": ("courir", "wurunu", "wuruye"),
    "wutu": ("prendre", "", "wutunde"),
    "yige": ("manger", "yigene", "yigaye"),
}

# Plages de verbes dans validation_02 (les phrases sont groupées par verbe).
PLAGES = [
    (1, 10, "daga"), (11, 20, "faye"), (21, 31, "goli"), (32, 47, "mini"),
    (48, 58, "ri"), (59, 77, "safa"), (78, 88, "sefe"), (89, 104, "wori"),
    (105, 115, "wuru"), (116, 122, "wutu"), (123, 141, "yige"),
    (142, 151, "daga"), (152, 161, "faye"), (162, 171, "goli"),
    (172, 185, "mini"), (186, 195, "ri"), (196, 200, "safa"),
]

PRONOMS = [  # ordre : formes longues d'abord (nke avant n…)
    ("nke", "1", "sg", "longue", "n (série brève)"),
    ("anke", "2", "sg", "longue", "an (série brève)"),
    ("ake", "3", "sg", "longue", "a (série brève)"),
    ("oku", "1", "pl", "longue", "o (série brève)"),
    ("xaku", "2", "pl", "longue", "xa (série brève)"),
    ("iku", "3", "pl", "longue", "i (série brève)"),
    ("n", "1", "sg", "brève", "nke (série longue)"),
    ("an", "2", "sg", "brève", "anke (série longue)"),
    ("a", "3", "sg", "brève", "ake (série longue)"),
    ("o", "1", "pl", "brève", "oku (série longue)"),
    ("xa", "2", "pl", "brève", "xaku (série longue)"),
    ("i", "3", "pl", "brève", "iku (série longue)"),
]

ADVERBIAUX = {"lenki", "saxa", "waxati", "su", "koota", "kumbene", "daru",
              "watia", "xumbene", "riya"}
RACINES_VERBES = {v for v in VERBES} | {"yiga", "riya"}

SNK_SRC = ("snk_engine (CC BY 4.0), noah-medra 2026 — corpus relu par le "
           "locuteur ; copie : data/source/snk-engine-corpus-grammatical-"
           f"{DATE}.jsonl")


def verbe_de(vid: str) -> str:
    n = int(vid.split("-")[1])
    for a, b, v in PLAGES:
        if a <= n <= b:
            return v
    raise ValueError(f"plage inconnue pour {vid}")


def annoter(snk: str, fr: str, verbe: str):
    """Retourne (tam, polarite, construction, confiance, note_annotation)."""
    s = snk.lower()
    inf, ger, na_ = VERBES[verbe]
    ger_ou_rad = ger if ger else verbe
    note = ""

    if s.startswith("maxa "):
        return ("impératif négatif (défense) — maxa + radical", "négatif",
                f"maxa + radical {verbe}", "élevé", note)
    if re.search(r"\bmaxa\b", s):
        return (f"passé négatif — pronom + maxa + radical", "négatif",
                f"pronom + maxa + radical {verbe}", "élevé", note)
    if re.search(r"n'ti rini|n'taxa rini", s):
        return ("futur proche négatif — n'ti rini / n'taxa rini", "négatif",
                f"pronom + n'ti rini + radical {verbe}", "élevé", note)
    if re.search(r"\bfayi\b", s):
        if "watia" in s or "en train" in fr:
            return ("inaccompli progressif — fayi + gérondif", "positif",
                    f"pronom + fayi + gérondif {ger_ou_rad}", "élevé",
                    "Le corpus serie_02 annote fayi « Progressive » ; validation_02 le traduit parfois comme un présent simple : étiquette habituel/progressif à trancher avec le référent.")
        if "koota su" in s or "waxati su" in s:
            return ("inaccompli habituel — fayi + gérondif", "positif",
                    f"pronom + fayi + gérondif {ger_ou_rad}", "élevé", note)
        return ("inaccompli — fayi + gérondif", "positif",
                f"pronom + fayi + gérondif {ger_ou_rad}", "moyen",
                "Sans adverbe de temps, la traduction du corpus hésite entre habituel et progressif (« il part »).")
    if re.search(r"\bdo\b", s) and "ni ya me" in s:
        na_ou = na_ or "nom d'action"
        return ("progressif — do + gérondif/nom d'action + ni ya me", "positif",
                f"pronom + do + {ger_ou_rad}/{na_ou} + ni ya me", "élevé", note)
    m = re.search(r"\byi rini\b", s)
    if m:
        reste = s[m.end():].split()
        suivant = reste[0] if reste else None
        if verbe == "ri" and (suivant is None or suivant in ADVERBIAUX):
            if re.search(r"\b(allez|vais|allons)\b", fr):
                return ("futur proche ou inaccompli — forme ambiguë (rini)", "positif",
                        "pronom + yi rini (gérondif de ri OU marqueur de futur proche)", "moyen",
                        "Ambiguïté documentée : rini est à la fois le gérondif de ri « venir » et le marqueur de futur proche ; la même forme est traduite « tu viens » (v-049) ou « vous allez venir » (v-191). À trancher avec le référent.")
            return ("inaccompli habituel — yi + gérondif rini (venir)"
                    if ("koota su" in s or "waxati su" in s)
                    else "inaccompli — yi + gérondif rini (venir)", "positif",
                    "pronom + yi + gérondif rini", "élevé", note)
        return ("futur proche — yi rini + radical", "positif",
                f"pronom + yi rini + radical {verbe}", "élevé", note)
    if re.search(r"\bl'rini\b", s):
        return ("futur lointain — l'rini + radical", "positif",
                f"pronom + l'rini + radical {verbe}", "élevé", note)
    m = re.search(r"\brini\b", s)
    if m:
        reste = s[m.end():].split()
        if reste and reste[0] in RACINES_VERBES:
            return ("futur lointain — rini + radical", "positif",
                    f"pronom + rini + radical {reste[0]}", "élevé", note)
    if re.search(r"\b(ŋ'wa|wa)\b", s):
        hab = " habituel" if ("koota su" in s or "waxati su" in s) else ""
        return (f"inaccompli{hab} — wa + gérondif", "positif",
                f"pronom + wa + gérondif {ger_ou_rad}", "élevé", note)
    if re.search(r"\b(n'yi|yi)\b", s):
        hab = " habituel" if ("koota su" in s or "waxati su" in s) else ""
        return (f"inaccompli{hab} — yi + gérondif", "positif",
                f"pronom + yi + gérondif {ger_ou_rad}", "élevé", note)
    if re.search(r"\bna\b", s):
        return ("subjonctif / demande — na + radical", "positif",
                f"pronom + na + radical {verbe}", "élevé",
                "Traduit selon les phrases par l'impératif pluriel (« partons »), le subjonctif (« que je … ») ou la demande (SNK-GRM-0017).")
    if re.search(r"\b(di|da|n'di|n'da)\b", s):
        return ("passé transitif (accompli) — di/da + objet", "positif",
                f"pronom + di/da + objet + (m'/n'){verbe}(-ni)", "élevé", note)
    if re.search(r"\bm'\w+", s):
        return ("passé (accompli) — particule m' + radical", "positif",
                f"pronom + m' + radical {verbe} (assimilation SNK-GRM-0028)", "moyen",
                "Répartition entre accompli Ø et m'+radical non élucidée : à faire expliquer par le référent.")
    if s.split()[0] in {p for p, *_ in PRONOMS}:
        return ("passé (accompli) — marqueur zéro", "positif",
                f"pronom + radical {verbe} nu (accompli sans marqueur)", "élevé", note)
    return ("impératif singulier — (objet +) radical nu", "positif",
            f"(objet +) radical {verbe} nu", "élevé", note)


def generer_conjugaisons():
    lignes = []
    with CORPUS.open(encoding="utf-8") as fh:
        corpus = [json.loads(l) for l in fh if l.strip()]
    v2 = [r for r in corpus if r.get("source_file") == "validation_02.jsonl"]
    if len(v2) != 200:
        print(f"ATTENTION : {len(v2)} lignes validation_02 (200 attendues)")
    for row in v2:
        vid, snk, fr = row["id"], row["snk"], row["fr"]
        verbe = verbe_de(vid)
        inf, ger, na_ = VERBES[verbe]
        tam, pol, constr, conf, note_ann = annoter(snk, fr, verbe)
        # personne / nombre / série du pronom
        premier = snk.lower().split()[0]
        pers = nb = serie = var = ""
        for tok, p, n, sr, v in PRONOMS:
            if premier == tok:
                pers, nb, serie, var = p, n, sr, v
                break
        if not pers:  # impératif singulier à objet antéposé
            pers, nb = "2", "sg"
            constr = f"(objet +) radical {verbe} nu"
        notes = (f"Forme conjuguée rattachée au verbe de référence « {verbe} » "
                 f"({inf}). Annotation grammaticale (personne, TAM, polarité) "
                 "produite par règles à partir de la phrase et de sa traduction "
                 "(corpus validé par le locuteur de snk_engine) ; à revérifier "
                 "avant publication.")
        if note_ann:
            notes += " " + note_ann
        statut = "SOURCE_VERIFIEE" if conf == "élevé" else "A_CONFIRMER_PAR_LOCUTEUR"
        lignes.append(dict(
            forme_soninke=snk, traduction_francaise=fr,
            categorie_grammaticale="forme_conjuguee",
            sous_categorie=f"{inf} ({verbe}) — {tam.split(' — ')[0]}",
            forme_ou_construction_grammaticale=constr,
            personne=pers, nombre=nb, temps_aspect_mode=tam, polarite=pol,
            variante=var, variete_regionale=PROJET,
            exemple_soninke=snk, traduction_exemple=fr,
            source=SNK_SRC,
            page_ou_localisation=f"corpus validation_02, {vid}",
            niveau_de_confiance=conf, statut_validation=statut, notes=notes))
    return lignes


# ---------------------------------------------------------------------------
# 3. Comparaison avec le lexique existant (dédoublonnage)
# ---------------------------------------------------------------------------
CARACTERES_CONSTRUCTION = set("+=:…()~«")
DEBUTS_CONSTRUCTION = ("pluriel", "suffixe", "numéraux", "gérondif", "accompli",
                       "radical", "pas de", "ordre", "faire (")


def est_documentaire(ligne: dict) -> bool:
    """True si la ligne documente une construction/un groupe de formes et non
    une forme lexicale intégrable telle quelle."""
    forme = ligne["forme_soninke"]
    if ligne["categorie_grammaticale"] == "forme_conjuguee":
        return True
    if ligne["statut_validation"] == "HYPOTHESE_NON_VALIDEE":
        return True
    if " / " in forme:  # groupes de variantes : rattachement, pas d'entrée
        return True
    if any(c in forme for c in CARACTERES_CONSTRUCTION):
        return True
    if forme.count(",") >= 2:  # listes de formes (jours, pronoms du cours…)
        return True
    return forme.lower().startswith(DEBUTS_CONSTRUCTION)


def charger_base():
    tete, variantes = {}, {}
    with BASE.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=";"):
            if not row.get("id"):
                continue
            info = (row["id"], row.get("francais", ""))
            if row.get("soninke"):
                tete.setdefault(cle(row["soninke"]), info)
            for v in (row.get("variantes") or "").split(","):
                if v.strip():
                    variantes.setdefault(cle(v), info)
    return tete, variantes


def comparer(ligne: dict, tete: dict, variantes: dict):
    """Retourne (correspondance, existing_id, existing_gloss, action).

    Ordre : formes conjuguées et lignes déjà suivies dans le projet d'abord,
    puis comparaison au lexique de base, puis lignes documentaires.
    """
    forme = ligne["forme_soninke"]
    statut = ligne["statut_validation"]
    if ligne["categorie_grammaticale"] == "forme_conjuguee":
        return ("forme_conjuguee", "", "",
                "Ne pas intégrer comme entrée lexicale : forme reliée à son "
                "verbe de référence dans la table de conjugaison.")
    if str(ligne.get("page_ou_localisation", "")).startswith("SNK-EA"):
        return ("deja_dans_paradigmes_ea", "", "",
                "Ligne déjà suivie dans data/source/paradigmes-etre-avoir.csv : "
                "ne pas dupliquer ; la comparaison au lexique de base se fait "
                "dans ce fichier d'origine.")
    k = cle(forme)
    if k in tete:
        eid, egloss = tete[k]
        if statut == "CONTRADICTOIRE_ENTRE_SOURCES":
            action = ("Ne pas fusionner ni supprimer : ajouter ce sens "
                      "grammatical comme acception distincte de l'entrée "
                      f"existante {eid}, avec sa source et le signalement du "
                      "désaccord entre sources.")
        else:
            action = ("Ne pas créer de doublon : compléter l'entrée existante "
                      f"{eid} (variantes, exemples, références grammaticales) "
                      "sans rien supprimer.")
        return ("deja_dans_base", eid, egloss, action)
    if k in variantes:
        eid, egloss = variantes[k]
        return ("variante_deja_documentee", eid, egloss,
                f"Rattacher comme variante de l'entrée existante {eid} ; "
                "pas de nouvelle entrée.")
    if est_documentaire(ligne):
        return ("ligne_documentaire", "", "",
                "Documentation grammaticale (construction, groupe de formes ou "
                "hypothèse) : à exploiter dans les guides, pas comme entrée de "
                "lexique.")
    return ("nouvelle_entree", "", "",
            "Créer une nouvelle entrée après validation référent "
            f"(statut proposé : {statut}).")


# ---------------------------------------------------------------------------
# 4. Assemblage et écriture des livrables
# ---------------------------------------------------------------------------
def main():
    curatees = [dict(l) for l in LIGNE]
    ea, ea_ign = convertir_ea()
    conj = generer_conjugaisons()
    toutes = curatees + ea + conj
    for i, ligne in enumerate(toutes, 1):
        ligne["id_provisoire"] = f"GRM2-{i:04d}"

    tete, variantes = charger_base()
    comp = []
    for ligne in toutes:
        corr, eid, egloss, action = comparer(ligne, tete, variantes)
        ligne["_correspondance"] = corr
        ligne["_existing_id"] = eid
        ligne["_existing_gloss"] = egloss
        ligne["_action"] = action
        comp.append(ligne)

    SORTIE_CSV.parent.mkdir(parents=True, exist_ok=True)
    SORTIE_COMP.parent.mkdir(parents=True, exist_ok=True)

    with SORTIE_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLONNES, delimiter=";",
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(toutes)

    nouvelles = [l for l in toutes if l["_correspondance"] == "nouvelle_entree"]
    with SORTIE_NOUV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLONNES, delimiter=";",
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(nouvelles)

    with SORTIE_COMP.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["id_provisoire", "forme_soninke", "correspondance",
                    "existing_id", "existing_gloss", "action_proposee",
                    "statut_validation", "niveau_de_confiance"])
        for l in toutes:
            w.writerow([l["id_provisoire"], l["forme_soninke"],
                        l["_correspondance"], l["_existing_id"],
                        l["_existing_gloss"], l["_action"],
                        l["statut_validation"], l["niveau_de_confiance"]])

    meta = {
        " genere_le": DATE,
        "objet": "Lexique grammatical d'enrichissement SoninkeGPT (lots 1 à 5)",
        "colonnes": COLONNES,
        "regles": [
            "Aucune forme inventée : chaque ligne cite sa source ou est marquée HYPOTHESE_NON_VALIDEE.",
            "Les champs inconnus sont laissés vides.",
            "Les contradictions entre sources sont conservées (statut CONTRADICTOIRE_ENTRE_SOURCES) sans fusion.",
            "Le lexique existant (data/source/) n'est jamais modifié par ce script.",
        ],
        "effectifs": {
            "lignes_curatees": len(curatees),
            "lignes_snk_ea_converties": len(ea),
            "lignes_snk_ea_ignores_non_atteste": ea_ign,
            "formes_conjuguees_validation_02": len(conj),
            "total": len(toutes),
            "nouvelles_entrees": len(nouvelles),
        },
        "statuts": dict(Counter(l["statut_validation"] for l in toutes)),
        "correspondances": dict(Counter(l["_correspondance"] for l in toutes)),
        "lignes": [{k: l[k] for k in COLONNES} for l in toutes],
    }
    with SORTIE_JSON.open("w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)

    print(f"lignes curatées          : {len(curatees)}")
    print(f"SNK-EA converties        : {len(ea)} (ignorées non_atteste : {ea_ign})")
    print(f"formes conjuguées        : {len(conj)}")
    print(f"TOTAL                    : {len(toutes)}")
    print("statuts                  :", dict(Counter(l["statut_validation"] for l in toutes)))
    print("correspondances          :", dict(Counter(l["_correspondance"] for l in toutes)))
    print("TAM des formes conjuguées:")
    for k, v in Counter(l["temps_aspect_mode"] for l in conj).most_common():
        print(f"   {v:3d}  {k}")
    print("écrits :", SORTIE_CSV.name, "/", SORTIE_JSON.name, "/",
          SORTIE_NOUV.name, "/", SORTIE_COMP.name)


if __name__ == "__main__":
    main()
