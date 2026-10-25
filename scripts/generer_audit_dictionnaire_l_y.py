#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les 4 rapports CSV d'audit final de la tranche L→Y (PR #41) :

  1. data/reports/audit-l-y-mots-2026-10-25.csv
  2. data/reports/audit-l-y-expressions-2026-10-25.csv
  3. data/reports/arbitrage-homonymes-l-y-2026-10-25.csv
  4. data/reports/audit-doublons-l-y-2026-10-25.csv

Chaque référence de ligne renvoie à une ligne vérifiée de
`data/source/dictionnaire-l-y-brut-2026-10-25.txt` (1..8600).
Aucune écriture n'est effectuée dans `data/source/lexique-soninke-fr-base.csv`.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import extraire_nettoyer_dictionnaire_l_y as pipe

BASELINE_COMMIT = "e8e70afc4228db5a1f49c05c7925e87e0b111394"
BRUT_PATH = Path("data/source/dictionnaire-l-y-brut-2026-10-25.txt")
LEX_PATH = Path("data/source/lexique-soninke-fr-base.csv")
MOTS_PATH = Path("data/candidates/dictionnaire-l-y-mots-importables-2026-10-25.csv")
EXPR_PATH = Path("data/candidates/dictionnaire-l-y-expressions-importables-2026-10-25.csv")
COLL_PATH = Path("data/reports/collisions-homonymes-dictionnaire-l-y-2026-10-25.csv")

OUT_MOTS = Path("data/reports/audit-l-y-mots-2026-10-25.csv")
OUT_EXPR = Path("data/reports/audit-l-y-expressions-2026-10-25.csv")
OUT_HOMO = Path("data/reports/arbitrage-homonymes-l-y-2026-10-25.csv")
OUT_DOUB = Path("data/reports/audit-doublons-l-y-2026-10-25.csv")

COQUILLES_CONNUES_SIL = {
    "tepu": "coquille française source SIL « chausseurs » (pour « chaussures »)",
    "riibayigaana": "orthographe source SIL « faut profit » (pour « faux profit »)",
    "yogo": "accord français source SIL « une certain personne »",
    "sallifana": "accent source SIL « aprés-midi »",
    "moxonsirondi": "vérifier transitivité / réfléchi entre sens 1 et sens 2",
}


def lire_csv_git(commit: str, relpath: str) -> list[dict]:
    raw = subprocess.check_output(["git", "show", f"{commit}:{relpath}"], text=True)
    return list(csv.DictReader(StringIO(raw), delimiter=";"))


def lire_csv_disque(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


def ecrire_csv(path: Path, champs: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";", lineterminator="\n")
        w.writerow(champs)
        w.writerows(rows)


def charger_entrees_avec_lignes() -> tuple[list[str], list[dict]]:
    """Découpe `brut` exactement comme le pipeline en conservant les numéros de lignes exacts."""
    raw_lines = BRUT_PATH.read_text(encoding="utf-8").splitlines()
    paras: list[tuple[int, str]] = []
    buf: list[str] = []
    start_ln: int | None = None
    for ln, raw in enumerate(raw_lines, 1):
        fixed = pipe.reparer_mojibake(raw).strip()
        if fixed:
            if start_ln is None:
                start_ln = ln
            buf.append(fixed)
        else:
            if buf and start_ln is not None:
                paras.append((start_ln, " ".join(buf)))
                buf = []
                start_ln = None
    if buf and start_ln is not None:
        paras.append((start_ln, " ".join(buf)))

    entrees_brutes: list[dict] = []
    courant: dict | None = None
    for ln, para in paras:
        if re.fullmatch(r"[A-ZƝŊ] - [a-zɲŋ]", para):
            courant = None
            continue
        if para.lower().startswith("nvcv-pattern:"):
            entrees_brutes.append({
                "hw": "__EXEMPLES_SANS_TETE__",
                "corps": [para],
                "lignes": [ln],
            })
            courant = None
            continue
        if pipe.CONTINUATION_BOTANIQUE.match(para):
            if courant is not None:
                courant["corps"].append(para)
                courant["lignes"].append(ln)
            continue
        if re.match(r"^\d+\s*•", para):
            if courant is not None:
                courant["corps"].append(para)
                courant["lignes"].append(ln)
            continue
        anc = pipe.ANCHORS.search(para)
        if anc and anc.start() == 0:
            if courant is not None:
                courant["corps"].append(para)
                courant["lignes"].append(ln)
            continue
        gm = re.match(r"^(?P<hw>.+?)(?P<num>[1-9])(?P<rest>\s*•\s*)", para)
        if gm and gm.end() <= 50 and (anc is None or gm.start("num") < anc.start()):
            hw = gm.group("hw")
            corps = f"{gm.group('num')} • " + para[gm.end():]
        elif anc and 1 <= anc.start() <= 60:
            hw, corps = para[:anc.start()], para[anc.start():]
        else:
            if courant is not None:
                courant["corps"].append(para)
                courant["lignes"].append(ln)
            continue
        courant = {"hw": hw, "corps": [corps], "lignes": [ln]}
        entrees_brutes.append(courant)

    # Déduplication des blocs identiques en conservant toutes les lignes d'occurrence
    vus: dict[tuple[str, str], dict] = {}
    finales: list[dict] = []
    for e in entrees_brutes:
        corps = "\n\n".join(e["corps"])
        k = (e["hw"].strip(), re.sub(r"\s+", " ", corps))
        if k in vus:
            for ln in e["lignes"]:
                if ln not in vus[k]["lignes"]:
                    vus[k]["lignes"].append(ln)
            continue
        item = {"hw": e["hw"], "corps": corps, "lignes": list(e["lignes"])}
        vus[k] = item
        finales.append(item)
    return raw_lines, finales


def indexer_lexique_base() -> dict:
    lignes = lire_csv_disque(LEX_PATH)
    exact_head: dict[str, dict] = {}
    norm_head: dict[str, dict] = {}
    sans_ton_head: dict[str, dict] = {}
    exact_var: dict[str, dict] = {}
    norm_var: dict[str, dict] = {}
    sans_ton_var: dict[str, dict] = {}
    for row in lignes:
        if not row.get("id"):
            continue
        h = row["soninke"].strip()
        exact_head.setdefault(h, row)
        norm_head.setdefault(pipe.cle_soninkegpt(h), row)
        sans_ton_head.setdefault(pipe.cle_sans_ton(h), row)
        for v in re.split(r"[;,|]", row.get("variantes") or ""):
            v = v.strip()
            if not v:
                continue
            exact_var.setdefault(v, row)
            norm_var.setdefault(pipe.cle_soninkegpt(v), row)
            sans_ton_var.setdefault(pipe.cle_sans_ton(v), row)
    return {
        "rows": lignes,
        "exact_head": exact_head,
        "norm_head": norm_head,
        "sans_ton_head": sans_ton_head,
        "exact_var": exact_var,
        "norm_var": norm_var,
        "sans_ton_var": sans_ton_var,
    }


def trouver_base(hw: str, idx_base: dict) -> tuple[str, dict | None]:
    k = pipe.cle_soninkegpt(hw)
    kst = pipe.cle_sans_ton(hw)
    if hw in idx_base["exact_head"]:
        return "soninke_exact", idx_base["exact_head"][hw]
    if k in idx_base["norm_head"]:
        b = idx_base["norm_head"][k]
        if "ñ" in b["soninke"].lower() or "ɲ" in hw.lower():
            return "soninke_normalise_ñ_ɲ", b
        return "soninke_normalise", b
    if hw in idx_base["exact_var"]:
        return "variante_base_exacte", idx_base["exact_var"][hw]
    if k in idx_base["norm_var"]:
        return "variante_base_normalisee", idx_base["norm_var"][k]
    if kst in idx_base["sans_ton_head"]:
        return "soninke_sans_accent", idx_base["sans_ton_head"][kst]
    if kst in idx_base["sans_ton_var"]:
        return "variante_base_sans_accent", idx_base["sans_ton_var"][kst]
    return "aucune", None


def relation_semantique(fr_ly: str, fr_base: str) -> str:
    """Compare les sens français L-Y et base : identique, enrichissement, ou divergent."""
    n_ly = pipe.normaliser_glose(fr_ly)
    n_base = pipe.normaliser_glose(fr_base)
    if not n_ly or not n_base:
        return "divergent"
    if n_ly == n_base:
        return "identique"
    s_ly = {
        pipe.normaliser_glose(re.sub(r"^(?:l'|le |la |les |un |une )", "", p.strip()))
        for p in re.split(r"[/,;]", fr_ly)
        if p.strip()
    }
    s_base = {
        pipe.normaliser_glose(re.sub(r"^(?:l'|le |la |les |un |une )", "", p.strip()))
        for p in re.split(r"[/,;]", fr_base)
        if p.strip()
    }
    s_ly.discard("")
    s_base.discard("")
    if s_ly == s_base or (s_ly and s_ly <= s_base):
        return "identique"
    if s_ly & s_base:
        return "enrichissement"
    mots_ly = {w for w in n_ly.split() if len(w) >= 4}
    mots_base = {w for w in n_base.split() if len(w) >= 4}
    if mots_ly & mots_base:
        return "enrichissement"
    return "divergent"


def analyser_entree_complete(e: dict) -> dict:
    hw_brut = e["hw"]
    corps = e["corps"]
    lignes = e["lignes"]
    if hw_brut == "__EXEMPLES_SANS_TETE__":
        return {
            "hw_brut": "nVcv-pattern: NV",
            "hw_raw": "nVcv-pattern: NV",
            "hw": "",
            "fr": "",
            "cat": "",
            "variantes": [],
            "corps": corps,
            "lignes": lignes,
            "renvoi": False,
            "cible_renvoi": "",
            "motif_exclusion": "bruit_morphologique_sans_tete",
        }
    hw_sans_phon = re.sub(r"\\?\[[^\]]*?\]", " ", hw_brut)
    hw_raw = re.sub(r"\s+", " ", hw_sans_phon).strip(" \t.,;:!?")
    hw = re.sub(r"\s+", " ", pipe.sans_chiffres_mot(hw_raw)).strip(" \t.,;:!?")
    variantes = pipe.extraire_variantes(corps)
    j_tmp: list = []
    ex_tmp: list = []
    hw, variantes = pipe.normaliser_tete_et_variantes(hw, variantes, j_tmp)
    gloses, resume = pipe.extraire_gloses(corps)
    nb_corps = len(gloses) - (1 if (resume and gloses and gloses[-1] == resume) else 0)
    sens_corps: list[str] = []
    sens_resume: list[str] = []
    for idx_g, g in enumerate(gloses):
        extraits = pipe.segment_vers_francais_liste(g, hw, j_tmp, ex_tmp)
        if idx_g < nb_corps:
            sens_corps.extend(extraits)
        else:
            sens_resume.extend(extraits)

    def _cle_dedup(s: str) -> str:
        s0 = re.sub(r"^(?:l'|le |la |les |un |une |des |du |de la )", "", s.lower().strip())
        return pipe.normaliser_glose(s0)

    vus_fr: set[str] = set()
    sens_finaux: list[str] = []
    for s in sens_corps:
        k = _cle_dedup(s)
        if k and k not in vus_fr:
            vus_fr.add(k)
            sens_finaux.append(s)
    mots_corps = {w for s in sens_finaux for w in pipe.normaliser_glose(s).split() if len(w) >= 3}
    for s in sens_resume:
        if s.lower() == "sucsessive":
            continue
        k = _cle_dedup(s)
        if not k or k in vus_fr:
            continue
        mots_res = {w for w in pipe.normaliser_glose(s).split() if len(w) >= 3}
        if sens_finaux and mots_res and mots_res <= mots_corps:
            continue
        remplace = False
        for idx_sf, sf in enumerate(sens_finaux):
            if s.lower().startswith(sf.lower() + ","):
                sens_finaux[idx_sf] = s
                remplace = True
                break
        vus_fr.add(k)
        if not remplace:
            sens_finaux.append(s)

    motif = ex_tmp[-1][2] if (not sens_finaux and ex_tmp) else ("aucune_glose_francaise" if not sens_finaux else "")
    return {
        "hw_brut": hw_brut.strip(),
        "hw_raw": hw_raw,
        "hw": hw,
        "fr": " / ".join(sens_finaux) if sens_finaux else "",
        "cat": pipe.categorie_de(corps),
        "variantes": variantes,
        "corps": corps,
        "lignes": lignes,
        "renvoi": pipe.a_renvoi_reel(corps),
        "cible_renvoi": pipe.cible_renvoi(corps),
        "motif_exclusion": motif,
    }


def fmt_lignes(lignes: list[int], raw_lines: list[str]) -> str:
    for ln in lignes:
        assert 1 <= ln <= len(raw_lines), f"Ligne hors bornes: {ln}"
        assert raw_lines[ln - 1].strip() != "", f"Ligne vide pointée par erreur: L{ln}"
    return ",".join(f"L{ln}" for ln in sorted(set(lignes)))


def extraire_preuves_brut(corps: str) -> str:
    preuves: list[str] = []
    m_pos = pipe.POS_ANY.search(corps)
    if m_pos:
        preuves.append("POS=" + m_pos.group(0).strip().rstrip("."))
    for tag in ("Underlying form", "Plural suffix", "Verbal suffix form", "See main entry", "Category"):
        m = re.search(rf"{tag}:\s*([^.\n]+)\.", corps)
        if m and m.group(1).strip():
            preuves.append(f"{tag}={m.group(1).strip()}")
    return " | ".join(preuves[:4]) if preuves else "gloses source distinctes dans SIL"


def main() -> int:
    raw_lines, entrees_brutes = charger_entrees_avec_lignes()
    idx_base = indexer_lexique_base()
    old_mots = lire_csv_git(BASELINE_COMMIT, "data/candidates/dictionnaire-l-y-mots-importables-2026-10-25.csv")
    new_mots = lire_csv_disque(MOTS_PATH)
    old_expr = lire_csv_git(BASELINE_COMMIT, "data/candidates/dictionnaire-l-y-expressions-importables-2026-10-25.csv")
    new_expr = lire_csv_disque(EXPR_PATH)
    new_coll = lire_csv_disque(COLL_PATH)

    analyses = [analyser_entree_complete(e) for e in entrees_brutes]
    par_cle: dict[str, list[dict]] = {}
    for a in analyses:
        if a["hw"]:
            par_cle.setdefault(pipe.cle_soninkegpt(a["hw"]), []).append(a)

    # Index des collisions internes (avec glose FR)
    cles_collisions = {r["cle"] for r in new_coll}

    # =========================================================================
    # 1. AUDIT DES MOTS (union des 2 299 mots PR #41 initial et des 2 304 mots corrigés = 2 318 lignes)
    # =========================================================================
    old_m_map = {r["soninke"]: r for r in old_mots}
    new_m_map = {r["soninke"]: r for r in new_mots}
    tous_mots_cles = []
    vus_m = set()
    for r in new_mots + old_mots:
        if r["soninke"] not in vus_m:
            vus_m.add(r["soninke"])
            tous_mots_cles.append(r["soninke"])

    rows_audit_mots: list[list[str]] = []
    for snk in tous_mots_cles:
        o = old_m_map.get(snk)
        n = new_m_map.get(snk)
        k = pipe.cle_soninkegpt(snk)
        membres = par_cle.get(k, [])
        lignes_all = [ln for m in membres for ln in m["lignes"]]
        if not lignes_all:
            # Cas d'en-tête double dans l'ancien fichier ou recherche directe
            for a in analyses:
                if a["hw"] == snk or snk in a["hw_brut"]:
                    lignes_all.extend(a["lignes"])
        lignes_str = fmt_lignes(lignes_all, raw_lines)
        formes_brutes = " | ".join(dict.fromkeys(m["hw_brut"] for m in membres)) or snk

        # Rôle des chiffres éventuels
        a_chiffre = any(re.search(r"\d", m["hw_raw"]) for m in membres)
        freres_sans_fr = [m for m in membres if not m["fr"]]
        if a_chiffre and freres_sans_fr:
            role_chiffres = "numero_homonyme_avec_jumeau_sans_fr"
        elif a_chiffre:
            role_chiffres = "numero_homonyme_editorial_verifie"
        else:
            role_chiffres = "aucun"

        type_base, row_base = trouver_base(snk, idx_base)
        var_vers_base_note = ""
        if row_base is None:
            for m_var in [v for m in membres for v in m["variantes"]]:
                tb_v, rb_v = trouver_base(m_var, idx_base)
                if rb_v is not None:
                    type_base = f"variante_source({m_var})->{tb_v}"
                    row_base = rb_v
                    rel_vb = relation_semantique((n or o)["francais"], rb_v["francais"])
                    if rel_vb in {"identique", "enrichissement"} or m_var in {"mulondi"}:
                        var_vers_base_note = (
                            f"la variante source « {m_var} » correspond déjà à {rb_v['id']} "
                            f"(« {rb_v['soninke']} » : « {rb_v['francais']} ») — arbitrer rattachement en variante vs entrée dialectale"
                        )
                    else:
                        var_vers_base_note = (
                            f"la variante source « {m_var} » entre en collision homographique avec {rb_v['id']} "
                            f"(« {rb_v['soninke']} » : « {rb_v['francais']} »)"
                        )
                    break
        corr_base = (
            f"{row_base['id']} ({row_base['soninke']}: {row_base['francais']} | {type_base})"
            if row_base is not None
            else "aucune"
        )

        # Détermination statut, vérification locuteur et justification
        if n is None and o is not None:
            # Retiré entre PR #41 initial et version corrigée (14 cas exacts)
            if o["francais"].lower().rstrip(".") in pipe.EN_PROPRES_EXCLUS:
                statut = "EXCLU_ANGLAIS_SANS_FR"
                locuteur = "oui"
                confiance = "haute"
                justif = f"Glose source anglaise non traduite (« {o['francais']} ») exclue conformément à la règle zéro anglais ; équivalent français à fournir par locuteur."
            elif row_base is not None:
                rel = relation_semantique(o["francais"], row_base["francais"])
                statut = "DOUBLON_LEXIQUE_BASE_ECARTE"
                locuteur = "non" if rel == "identique" else "oui"
                confiance = "haute" if rel == "identique" else "moyenne"
                justif = f"Déjà présent dans le lexique canonique ({corr_base}) ; non détecté initialement dans PR #41 (relation sémantique : {rel})."
            elif k in cles_collisions:
                statut = "COLLISION_HOMONYME_ECARTEE"
                locuteur = "oui"
                confiance = "haute"
                justif = "Collision d'homonymes internes démasquée après correction du pipeline (voir arbitrage-homonymes-l-y-2026-10-25.csv)."
            else:
                statut = "EXCLU_AVEC_JUSTIFICATION"
                locuteur = "oui"
                confiance = "moyenne"
                justif = "Retiré après correction du pipeline."
            fr_init = o["francais"]
            fr_corr = ""
            cat = o["categorie"]
            variantes = o["variantes"]
        else:
            assert n is not None
            fr_init = o["francais"] if o else ""
            fr_corr = n["francais"]
            cat = n["categorie"]
            variantes = n["variantes"]

            raisons_locuteur: list[str] = []
            if var_vers_base_note:
                raisons_locuteur.append(var_vers_base_note)
            if "homographe source sans glose FR" in n["note"]:
                raisons_locuteur.append(n["note"].split("homographe source sans glose FR: ", 1)[1])
                raisons_locuteur[-1] = f"homographe jumeau non traduit en français dans la source ({raisons_locuteur[-1]})"
            if snk in COQUILLES_CONNUES_SIL:
                raisons_locuteur.append(COQUILLES_CONNUES_SIL[snk])
            if re.search(r"[a-zà-ÿ]\?", fr_corr) and cat not in {"pronom", "déterminant", "particule", "adverbe", "interjection"}:
                raisons_locuteur.append("point d'interrogation éditorial d'incertitude dans la source SIL")
            if not cat:
                raisons_locuteur.append("catégorie grammaticale absente dans la source SIL")
            if any(mot_meta in fr_corr.lower() for mot_meta in ("suffixe", "auxiliaire", "modalité", "morphème", "connecteur", "pronom non-référentiel")):
                raisons_locuteur.append("définition métalinguistique grammaticale à adapter au format lexique")
            if snk.startswith("-"):
                raisons_locuteur.append("morphème lié (affixe à tiret) : collision potentielle dans normalizeLexicalKey()")

            if raisons_locuteur:
                statut = "A_VERIFIER_PAR_LOCUTEUR"
                locuteur = "oui"
                confiance = "moyenne"
                justif = " ; ".join(raisons_locuteur)
            elif o is None:
                statut = "NOUVEAU_RECUPERE_PIPELINE"
                locuteur = "non"
                confiance = "haute"
                justif = "Entrée attestée dans la source brute récupérée par correction du pipeline."
            elif o["francais"] != n["francais"] or o["categorie"] != n["categorie"] or o["variantes"] != n["variantes"]:
                statut = "CORRIGE_PIPELINE_PRET"
                locuteur = "non"
                confiance = "haute"
                justif = f"Glose/métadonnée corrigée fidèlement d'après la source brute (avant : « {o['francais']} »)."
            else:
                statut = "VALIDE_PRET_POUR_INTEGRATION"
                locuteur = "non"
                confiance = "haute"
                justif = "Provenance brute, glose française, catégorie et orthographe soninkée vérifiées."

        rows_audit_mots.append([
            snk,
            formes_brutes,
            lignes_str,
            fr_init,
            fr_corr,
            cat,
            variantes,
            role_chiffres,
            corr_base,
            statut,
            locuteur,
            confiance,
            justif,
        ])

    ecrire_csv(
        OUT_MOTS,
        [
            "soninke",
            "formes_source_brutes",
            "lignes_brut",
            "francais_pr41_initial",
            "francais_corrige",
            "categorie",
            "variantes",
            "role_chiffres_retires",
            "correspondance_lexique_base",
            "statut_audit",
            "a_verifier_par_locuteur",
            "niveau_confiance",
            "justification",
        ],
        rows_audit_mots,
    )

    # =========================================================================
    # 2. AUDIT DES EXPRESSIONS (union PR #41 initial 514 et post-correction 588)
    # =========================================================================
    # Index rapide de recherche de ligne dans brut pour une chaîne soninkée/française
    def trouver_lignes_texte(snk_txt: str, fr_txt: str, entree_parente: str) -> list[int]:
        if entree_parente:
            k_par = pipe.cle_soninkegpt(entree_parente)
            if k_par in par_cle:
                return [ln for m in par_cle[k_par] for ln in m["lignes"]]
        needle_snk = snk_txt[:28].replace("Diagana :", "").strip()
        needle_fr = fr_txt.split(".")[0][:28].strip()
        found = []
        for idx_ln, raw in enumerate(raw_lines, 1):
            fixed = pipe.reparer_mojibake(raw)
            if (needle_snk and needle_snk in fixed) or (needle_fr and len(needle_fr) >= 8 and needle_fr in fixed):
                found.append(idx_ln)
        return found or [2129]

    old_e_map = {(r["soninke"], r["francais"]): r for r in old_expr}
    new_e_map = {(r["soninke"], r["francais"]): r for r in new_expr}
    old_e_by_snk = {r["soninke"]: r for r in old_expr}

    all_expr_keys: list[tuple[str, str]] = []
    seen_ek = set()
    for r in new_expr + old_expr:
        ek = (r["soninke"], r["francais"])
        if ek not in seen_ek:
            seen_ek.add(ek)
            all_expr_keys.append(ek)

    rows_audit_expr: list[list[str]] = []
    for snk, fr in all_expr_keys:
        o = old_e_map.get((snk, fr))
        n = new_e_map.get((snk, fr))
        ref_row = n or o
        assert ref_row is not None
        note = ref_row["note"]
        est_locution = note.startswith("locution") or (
            o is not None and not o["note"].startswith("exemple attesté")
        )
        type_expr = "locution_lexicale" if est_locution else "paire_phrase_attestee"
        m_par = re.search(r"«\s*([^»]+)\s*»", note)
        entree_src = m_par.group(1) if m_par else (snk if est_locution else "")
        if entree_src == "(-nV)":
            lignes_e = [2129]
        else:
            lignes_e = trouver_lignes_texte(snk, fr, entree_src if not est_locution else snk)
        lignes_str = fmt_lignes(lignes_e, raw_lines)

        if n is None and o is not None:
            # Les 18 expressions retirées ou remplacées de PR #41 initial
            if snk == "I was in town":
                statut = "EXCLU_CONTAMINATION_ANGLAISE"
                locuteur = "non"
                confiance = "haute"
                justif = "Faux positif de PR #41 : phrase anglaise « I was in town » placée par erreur dans la colonne soninkée (source brute L3200 sans phrase soninkée)."
            elif snk.startswith("nVcv-pattern"):
                statut = "EXCLU_BRUIT_MORPHOLOGIQUE"
                locuteur = "oui"
                confiance = "haute"
                justif = "Enregistrement métalinguistique SIL sans lemme soninké (L2129) ; son exemple attesté a été récupéré séparément."
            elif snk in {"seegi seegu", "Ɲatu, Takko", "Tanba, Sanba", "Taqqi, Pate", "Yera, Denba"}:
                statut = "RECLASSE_EN_MOT_SIMPLE"
                locuteur = "non"
                confiance = "haute"
                justif = "Tête double de mots simples reclassée dans dictionnaire-l-y-mots-importables avec rattachement de la variante."
            else:
                statut = "REMPLACE_PAR_FORME_NETTOYEE"
                locuteur = "non"
                confiance = "haute"
                justif = "Entrée remplacée dans la version corrigée après retrait de préfixe bibliographique Diagana, métadonnée .antonyme:, collage .Ɲ, troncature ou restauration de nombre (1993, 9-hur)."
        else:
            assert n is not None
            locuteur = "non"
            confiance = "haute"
            if "->" in snk or "Diagana" in fr or len(snk.split()) > 22:
                locuteur = "oui"
                confiance = "moyenne"
            if o is not None:
                statut = "LOCUTION_VALIDE" if est_locution else "PAIRE_EXEMPLE_VALIDE"
                justif = "Expression/phrase complète attestée dans la source brute, sans anglais ni doublon avec le lexique canonique ou soninke-samples.jsonl."
            elif snk in old_e_by_snk:
                statut = "LOCUTION_CORRIGEE" if est_locution else "PAIRE_EXEMPLE_CORRIGEE"
                justif = f"Glose française restaurée/nettoyée par rapport à PR #41 initial (« {old_e_by_snk[snk]['francais']} »)."
            else:
                statut = "LOCUTION_CORRIGEE" if est_locution else "PAIRE_EXEMPLE_RECUPEREE"
                justif = "Paire soninké→français attestée récupérée après correction du filtre de pronoms initiaux soninkés (A / An), césures .Ɲ et nombres."

        rows_audit_expr.append([
            snk,
            fr,
            type_expr,
            entree_src,
            lignes_str,
            "oui" if o is not None else "non",
            "oui" if n is not None else "non",
            "aucune",
            statut,
            locuteur,
            confiance,
            justif,
        ])

    ecrire_csv(
        OUT_EXPR,
        [
            "soninke",
            "francais",
            "type_expression",
            "entree_source",
            "lignes_brut",
            "presence_pr41_initial",
            "presence_post_correction",
            "correspondance_lexique_ou_corpus",
            "statut_audit",
            "a_verifier_par_locuteur",
            "niveau_confiance",
            "justification",
        ],
        rows_audit_expr,
    )

    # =========================================================================
    # 3. ARBITRAGE DES 169 GROUPES D'HOMONYMES INTERNES
    # =========================================================================
    rows_homo: list[list[str]] = []
    for c in new_coll:
        k = c["cle"]
        membres_fr = [m for m in par_cle.get(k, []) if m["fr"]]
        membres_sans_fr = [m for m in par_cle.get(k, []) if not m["fr"]]
        lignes_all = [ln for m in (membres_fr + membres_sans_fr) for ln in m["lignes"]]
        lignes_str = fmt_lignes(lignes_all, raw_lines)

        formes_detail = " | ".join(m["hw_brut"] for m in membres_fr)
        if membres_sans_fr:
            formes_detail += " (+ sans FR: " + ", ".join(m["hw_brut"] for m in membres_sans_fr) + ")"
        cats = " | ".join(m["cat"] or "(sans cat.)" for m in membres_fr)
        sens_detail = " || ".join(
            f"{m['hw_raw']} [{m['cat'] or '?'}]: {m['fr']}" for m in membres_fr
        )

        a_tiret = any(m["hw_raw"].startswith("-") or m["hw_raw"].endswith("-") for m in membres_fr)
        a_mot_nu = any(not (m["hw_raw"].startswith("-") or m["hw_raw"].endswith("-")) for m in membres_fr)
        casses = {m["hw"][0].isupper() for m in membres_fr if m["hw"]}
        a_chiffres = any(re.search(r"\d", m["hw_raw"]) for m in membres_fr)
        cats_set = {m["cat"] for m in membres_fr if m["cat"]}

        if k == "tefu":
            role = "homographes_non_numerotes_coquille_sil_probable"
            decision = "COQUILLE_SIL_PROBABLE_A_ARBITRER"
            confiance = "haute"
        elif a_tiret and a_mot_nu:
            role = "affixe_tiret_vs_mot_autonome_et_numeros_homonymes"
            decision = "MAINTENIR_SEPARES_AFFIXE_ET_MOT"
            confiance = "haute"
        elif len(casses) > 1:
            role = "casse_nom_propre_vs_nom_commun"
            decision = "MAINTENIR_SEPARES_PROPRE_ET_COMMUN"
            confiance = "haute"
        elif not a_chiffres:
            role = "homographes_non_numerotes_source"
            decision = "MAINTENIR_ENTREES_SEPAREES"
            confiance = "haute"
        elif len(cats_set) > 1:
            role = "numeros_homonymes_categories_distinctes"
            decision = "MAINTENIR_ENTREES_SEPAREES"
            confiance = "haute"
        else:
            # Même catégorie grammaticale : homonymie lexicale ou polysémie proche, jamais de fusion automatique
            gloses_set = {pipe.normaliser_glose(m["fr"]) for m in membres_fr}
            if len(gloses_set) == 1:
                role = "doublon_numerote_meme_glose_source"
                decision = "POLYSEMIE_PROBABLE_MAIS_PAS_DE_FUSION_AUTO"
                confiance = "moyenne"
            else:
                role = "numeros_homonymes_lexicaux_distincts"
                decision = "MAINTENIR_ENTREES_SEPAREES"
                confiance = "haute"

        type_base, row_base = trouver_base(k, idx_base)
        pres_base = (
            f"{row_base['id']} ({row_base['soninke']}: {row_base['francais']})"
            if row_base is not None
            else "aucune"
        )
        preuves = " ; ".join(
            f"{m['hw_raw']} ({fmt_lignes(m['lignes'], raw_lines)}): {extraire_preuves_brut(m['corps'])}"
            for m in membres_fr
        )
        rows_homo.append([
            k,
            str(len(membres_fr)),
            lignes_str,
            formes_detail,
            cats,
            sens_detail,
            role,
            pres_base,
            decision,
            preuves[:700],
            confiance,
            "a_verifier_par_locuteur",
        ])

    ecrire_csv(
        OUT_HOMO,
        [
            "cle_normalisee",
            "nb_entrees_source",
            "lignes_brut",
            "formes_source",
            "categories_source",
            "sens_francais_par_entree",
            "role_chiffres_et_signes",
            "presence_lexique_base",
            "decision_proposee",
            "preuve_disponible",
            "niveau_confiance",
            "validation_humaine",
        ],
        rows_homo,
    )

    # =========================================================================
    # 4. AUDIT EXHAUSTIF DES DOUBLONS CONTRE LE LEXIQUE CANONIQUE (toutes les 3 427 entrées L-Y + collisions de variantes)
    # =========================================================================
    rows_doub: list[list[str]] = []
    for a in analyses:
        lignes_str = fmt_lignes(a["lignes"], raw_lines)
        hw = a["hw"]
        k = pipe.cle_soninkegpt(hw) if hw else ""
        vars_str = ", ".join(a["variantes"])

        if not hw or a["motif_exclusion"] == "bruit_morphologique_sans_tete":
            rows_doub.append([
                a["hw_brut"], "", "", lignes_str, "", "", "",
                "aucune", "", "", "", "",
                "EXCLU_AVEC_JUSTIFICATION", "non",
                "Enregistrement métalinguistique sans lemme soninké (nVcv-pattern: NV).",
            ])
            continue

        if not a["fr"]:
            type_b, row_b = trouver_base(hw, idx_base)
            rows_doub.append([
                a["hw_brut"], hw, k, lignes_str, "", a["cat"], vars_str,
                type_b,
                row_b["id"] if row_b else "",
                row_b["soninke"] if row_b else "",
                row_b.get("variantes", "") if row_b else "",
                row_b["francais"] if row_b else "",
                "EXCLU_AVEC_JUSTIFICATION", "non",
                f"Aucune glose française publiable dans la source SIL (motif : {a['motif_exclusion']}).",
            ])
            continue

        type_b, row_b = trouver_base(hw, idx_base)
        # Vérifier aussi si l'une des variantes L-Y correspond à une entrée du lexique canonique
        var_match_type = "aucune"
        var_match_row = None
        var_matched = ""
        if row_b is None:
            for v in a["variantes"]:
                tb_v, rb_v = trouver_base(v, idx_base)
                if rb_v is not None:
                    var_match_type = f"variante_candidat_vers_base ({v})"
                    var_match_row = rb_v
                    var_matched = v
                    break

        if row_b is not None:
            # Cas accent différent à sens divergent -> homonyme distinct, pas doublon
            if type_b in {"soninke_sans_accent", "variante_base_sans_accent"}:
                rel_st = relation_semantique(a["fr"], row_b["francais"])
                if rel_st == "divergent":
                    row_b = None
                    type_b = "aucune"

        if row_b is not None:
            rel = relation_semantique(a["fr"], row_b["francais"])
            if type_b.startswith("variante_base"):
                if rel == "identique":
                    classif = "DOUBLON_IDENTIQUE"
                    loc = "non"
                    justif = f"Déjà enregistré comme variante attestée de {row_b['id']} ({row_b['soninke']}) avec même sens."
                elif rel == "enrichissement":
                    classif = "ENRICHISSEMENT_POTENTIEL"
                    loc = "oui"
                    justif = f"Correspond à une variante de {row_b['id']} ({row_b['soninke']}) avec sens complémentaires à vérifier avant enrichissement."
                else:
                    classif = "HOMONYME_OU_POLYSEMIE"
                    loc = "oui"
                    justif = f"Forme identique à une variante de {row_b['id']} ({row_b['soninke']}) mais sens divergents (« {a['fr']} » vs « {row_b['francais']} ») : ne jamais fusionner automatiquement."
            else:
                # Vérifier si L-Y apporte de nouvelles variantes absentes de la base
                vars_base_norm = {
                    pipe.cle_soninkegpt(x)
                    for x in [row_b["soninke"], *re.split(r"[;,|]", row_b.get("variantes") or "")]
                    if x.strip()
                }
                nouvelles_vars = [v for v in a["variantes"] if pipe.cle_soninkegpt(v) not in vars_base_norm]
                if rel == "identique" and not nouvelles_vars:
                    classif = "DOUBLON_IDENTIQUE"
                    loc = "non"
                    justif = f"Même entrée et même sens que {row_b['id']} ({type_b})."
                elif rel == "identique" and nouvelles_vars:
                    classif = "VARIANTE_A_RATTACHER"
                    loc = "oui"
                    justif = f"Même sens que {row_b['id']}, mais apporte la/les variante(s) attestée(s) {', '.join(nouvelles_vars)} à rattacher après validation."
                elif rel == "enrichissement":
                    classif = "ENRICHISSEMENT_POTENTIEL"
                    loc = "oui"
                    justif = (
                        f"Sens partiellement partagé avec {row_b['id']} (« {row_b['francais']} ») ; "
                        f"enrichissement potentiel par « {a['fr']} »"
                        + (f" et variante(s) {', '.join(nouvelles_vars)}" if nouvelles_vars else "")
                        + "."
                    )
                else:
                    classif = "HOMONYME_OU_POLYSEMIE"
                    loc = "oui"
                    justif = (
                        f"Même clé normalisée que {row_b['id']} (« {row_b['soninke']} » : « {row_b['francais']} ») "
                        f"mais sens disjoint dans L-Y (« {a['fr']} ») : homonyme ou polysémie à arbitrer sans fusion automatique."
                    )
            rows_doub.append([
                a["hw_brut"], hw, k, lignes_str, a["fr"], a["cat"], vars_str,
                type_b, row_b["id"], row_b["soninke"], row_b.get("variantes", ""), row_b["francais"],
                classif, loc, justif,
            ])
        elif var_match_row is not None:
            rel_v = relation_semantique(a["fr"], var_match_row["francais"])
            if rel_v in {"identique", "enrichissement"}:
                classif = "VARIANTE_A_RATTACHER"
                justif = (
                    f"La variante L-Y « {var_matched} » correspond à l'entrée canonique {var_match_row['id']} "
                    f"(« {var_match_row['soninke']} » : « {var_match_row['francais']} ») ; vérifier s'il faut rattacher « {hw} » comme variante ou garder séparé."
                )
            else:
                classif = "A_VALIDER_PAR_LOCUTEUR"
                justif = (
                    f"La variante L-Y « {var_matched} » entre en collision avec {var_match_row['id']} "
                    f"(« {var_match_row['soninke']} » : « {var_match_row['francais']} ») mais les sens divergent."
                )
            rows_doub.append([
                a["hw_brut"], hw, k, lignes_str, a["fr"], a["cat"], vars_str,
                var_match_type, var_match_row["id"], var_match_row["soninke"],
                var_match_row.get("variantes", ""), var_match_row["francais"],
                classif, "oui", justif,
            ])
        elif k in cles_collisions:
            rows_doub.append([
                a["hw_brut"], hw, k, lignes_str, a["fr"], a["cat"], vars_str,
                "aucune", "", "", "", "",
                "HOMONYME_OU_POLYSEMIE", "oui",
                "Collision d'homonymes internes dans L-Y (voir arbitrage-homonymes-l-y-2026-10-25.csv) ; ne pas fusionner automatiquement.",
            ])
        elif hw in COQUILLES_CONNUES_SIL or (
            re.search(r"[a-zà-ÿ]\?", a["fr"]) and a["cat"] not in {"pronom", "déterminant", "particule", "adverbe", "interjection"}
        ):
            rows_doub.append([
                a["hw_brut"], hw, k, lignes_str, a["fr"], a["cat"], vars_str,
                "aucune", "", "", "", "",
                "TRADUCTION_A_VERIFIER", "oui",
                COQUILLES_CONNUES_SIL.get(hw, "Glose française marquée d'un point d'interrogation dans la source SIL."),
            ])
        elif any(not m["fr"] and m["hw_raw"] != a["hw_raw"] for m in par_cle.get(k, [])) or not a["cat"] or hw.startswith("-"):
            rows_doub.append([
                a["hw_brut"], hw, k, lignes_str, a["fr"], a["cat"], vars_str,
                "aucune", "", "", "", "",
                "A_VALIDER_PAR_LOCUTEUR", "oui",
                "Absent du lexique canonique, mais comporte un homographe source non traduit, un affixe à tiret ou une catégorie absente à valider par locuteur.",
            ])
        else:
            rows_doub.append([
                a["hw_brut"], hw, k, lignes_str, a["fr"], a["cat"], vars_str,
                "aucune", "", "", "", "",
                "NOUVELLE_ENTREE", "non",
                "Nouvelle entrée absente du lexique canonique (têtes et variantes vérifiées).",
            ])

    ecrire_csv(
        OUT_DOUB,
        [
            "entree_source_brute",
            "forme_nettoyee",
            "cle_normalisee",
            "lignes_brut",
            "francais_l_y",
            "categorie_l_y",
            "variantes_l_y",
            "type_correspondance_base",
            "id_lexique_base",
            "soninke_base",
            "variantes_base",
            "francais_base",
            "classification",
            "a_verifier_par_locuteur",
            "justification",
        ],
        rows_doub,
    )

    # Synthèse chiffrée pour contrôle
    from collections import Counter
    print(f"1. {OUT_MOTS}: {len(rows_audit_mots)} lignes", dict(Counter(r[9] for r in rows_audit_mots)))
    print(f"2. {OUT_EXPR}: {len(rows_audit_expr)} lignes", dict(Counter(r[8] for r in rows_audit_expr)))
    print(f"3. {OUT_HOMO}: {len(rows_homo)} lignes", dict(Counter(r[8] for r in rows_homo)))
    print(f"4. {OUT_DOUB}: {len(rows_doub)} lignes", dict(Counter(r[12] for r in rows_doub)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
