#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrait et nettoie les lettres L→Y du dictionnaire soninké (source SIL/IPS).

Source : `data/source/dictionnaire-l-y-brut-2026-10-25.txt` (archive brute
concaténée des 16 fichiers L..Y, texte dépourvu d'URL et de liens Markdown).

Pipeline (aucune écriture dans le lexique base — lecture seule) :

  1. lecture des paragraphes → entrées (mot d'entrée + corps) ;
     • les marqueurs de sens « N • » collés au mot d'entrée sont séparés AVANT
       tout retrait de chiffres (`yille11 •` → tête `yille1` + sens `1 •`,
       `taaxu1 •` → tête `taaxu`, `ma31 •` → tête `ma3`) ;
     • les blocs strictement identiques répétés par la source sont ignorés ;
  2. extraction des gloses françaises (résumé, libellés de catégorie, sens
     numérotés) avec retrait des exemples, métadonnées, anglais, sigles
     grammaticaux non traduits (LOC, SG, PL, BCMR, POST, EQ, INTR, CNTRST,
     RELtemp, PROintrg, DETintrg, ABST…), marqueurs `??` et `='''''` ;
  3. retrait de TOUS les chiffres sur les formes soninkées (mots et variantes) ;
  4. distinction mots / expressions :
     • mots = têtes d'entrée à un seul mot ;
     • expressions = têtes multi-mots (locutions) + paires attestées
       phrase soninkée → phrase française (la phrase anglaise intermédiaire
       est détectée puis supprimée) ;
  5. filtrage strict contre `data/source/lexique-soninke-fr-base.csv`
     (`soninke` + `variantes`, clé `cle()`) : aucun doublon du lexique base
     n'est publié ; les collisions d'homonymes internes ne sont JAMAIS
     fusionnées silencieusement (rapport + écartement, arbitrage utilisateur) ;
  6. rapports d'audit + auto-vérification stricte (chiffres, anglais, doublons,
     CSV).

Sorties :
  data/candidates/dictionnaire-l-y-mots-importables-2026-10-25.csv
  data/candidates/dictionnaire-l-y-expressions-importables-2026-10-25.csv
  data/reports/comparaison-dictionnaire-l-y-2026-10-25.csv
  data/reports/collisions-homonymes-dictionnaire-l-y-2026-10-25.csv
  data/reports/renvois-sans-glose-dictionnaire-l-y-2026-10-25.csv
  data/reports/exclusions-anglais-dictionnaire-l-y-2026-10-25.csv
  data/reports/nettoyage-dictionnaire-l-y-2026-10-25.csv
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from import_extraction_sans_doublons import cle, charger_lexique, normaliser_glose
from nettoyer_integrer_dictionnaire_d_f import (
    est_anglais,
    nettoyer_fr,
    CATEGORIES_SEGMENT,
)
from extract_dictionnaire_soninke import has_french_accents

BRUT = Path("data/source/dictionnaire-l-y-brut-2026-10-25.txt")
LEXIQUE = Path("data/source/lexique-soninke-fr-base.csv")
MOTS_OUT = Path("data/candidates/dictionnaire-l-y-mots-importables-2026-10-25.csv")
EXPRESSIONS_OUT = Path(
    "data/candidates/dictionnaire-l-y-expressions-importables-2026-10-25.csv")
RAPPORT_CMP = Path("data/reports/comparaison-dictionnaire-l-y-2026-10-25.csv")
RAPPORT_COLL = Path("data/reports/collisions-homonymes-dictionnaire-l-y-2026-10-25.csv")
RAPPORT_RENVOI = Path("data/reports/renvois-sans-glose-dictionnaire-l-y-2026-10-25.csv")
RAPPORT_ANG = Path("data/reports/exclusions-anglais-dictionnaire-l-y-2026-10-25.csv")
RAPPORT_NET = Path("data/reports/nettoyage-dictionnaire-l-y-2026-10-25.csv")

DATE = "2026-10-25"
CHAMPS_CAND = ["soninke", "francais", "categorie", "variantes", "note"]

# ----------------------------------------------------------------- analyse ---

# Ancres de corps : première rencontre ⇒ séparation mot d'entrée / corps.
ANCHORS = re.compile(
    r"summary-definition:|See main entry:|compare:|Variant:|Note:|Source:|Gram:"
    r"|Usage:|Category:|Plural suffix:|Underlying form:|Verbal suffix form:"
    r"|synonyme:|similaire:|comp:|idiom:|patient:|agent:|tone:|Anth:|Socio:|Phon:"
    r"|Restrict:|unité:|Disc:"
    r"|Nom \.|Nom commun\.|Nom Propre\.|Verbe transitif|Verbe intransitif|verbe d'état"
    r"|verbe passif|verbe antipassif|verbe causitif|verbe objet-incorporé|verbe sériel"
    r"|verbe intransitif|verbe transitif|Adjectif\.|Adverbe\.|Interjection\.|Pronom\."
    r"|Postposition\.|conjonction de coordination\.|conjonction de subordination\."
    r"|Nombre cardinal\.|Nombre ordinal\.|Article indéfini\.|Focalisateur\."
    r"|Quantificateur\.|particule question\.|complémenteur\.|prédicatif verbal\."
    r"|pronom emphatique\.|Proforme interrogatif\.|Déterminant interrogatif\."
    r"|Copule\.|auxiliaire existential\.|(?:pré|pre)position\.|Verbe\.",
    re.I,
)

# Étiquettes de catégorie (libellés source) — libellés composés avant simples.
_POS_ALT = (
    r"Nombre ordinal|Nombre cardinal|"
    r"verbe (?:causitif|antipassif|passif|transitif|intransitif|d'état"
    r"|objet-incorporé|sériel)|"
    r"Nom commun|Nom Propre|Nom|Adverbe|Adjectif|Postposition|(?:pré|pre)position|"
    r"conjonction de coordination|conjonction de subordination|Conjonction|Pronom|"
    r"pronom emphatique|Proforme interrogatif|Déterminant interrogatif|"
    r"Article indéfini|Copule|auxiliaire existential|Focalisateur|Quantificateur|"
    r"particule question|complémenteur|prédicatif verbal|Interjection|"
    r"verbe associé|Verbe"
)
# recherche d'une étiquette n'importe où dans un segment (extraction)
POS_ANY = re.compile(r"(?:" + _POS_ALT + r")\s*\.\s*", re.I)
# étiquette strictement en tête de segment (retrait / saut)
POS_HEAD = re.compile(r"^(?:" + _POS_ALT + r")\s*\.\s*", re.I)
# une glose qui n'est qu'un libellé grammatical n'est pas une traduction
POS_GLOSE_VIDE = re.compile(
    r"^(?:Verbe|Nom|Adjectif|Adverbe|Pronom|Interjection|Postposition|"
    r"(?:pré|pre)position|Conjonction|Copule|Nombre|Article|Focalisateur|"
    r"Quantificateur|Particule|complémenteur|prédicatif verbal|Attributif)"
    r"(?:\s+(?:transitif|intransitif|commun|Propre|cardinal|ordinal"
    r"|de coordination|de subordination))?$",
    re.I,
)

META_CUT = re.compile(
    r"Category:|Note:|Gram:|Usage:|Plural suffix:|Verbal suffix form:"
    r"|Underlying form:|synonyme:|similaire:|comp:|compare:|idiom:|patient:"
    r"|agent:|Anth:|Socio:|Phon:|tone:|Restrict:|Source:|See main entry:"
    r"|summary-definition:|Variant:|Disc:|unité:|verbe associé:"
)

SIGLES = {
    "LOC", "SG", "PL", "BCMR", "POST", "EQ", "INTR", "CNTRST", "RELtemp",
    "PROintrg", "DETintrg", "ABST", "FOC", "NOMR", "COMP", "QULR", "CAUS",
    "ANTI", "PASS", "ADJR/NR", "RFLX", "REC", "MBR", "CONCTR", "DEON",
    "ANTI-PASS", "REFndef", "INSTR", "OCCUP", "AGENT", "1SG", "1SGEMP",
    "2PPL", "2PAN", "INTER", "REL", "DEONIC", "QULR.", "X", "MOT",
}

CATEGORIE_PAR_POS = [
    (re.compile(r"^Nom Propre\b", re.I), "nom propre"),
    (re.compile(r"^Nom commun\b", re.I), "nom"),
    (re.compile(r"^Nom\b", re.I), "nom"),
    (re.compile(r"^Verbe\b|^verbe\b", re.I), "verbe"),
    (re.compile(r"^Adjectif\b", re.I), "adjectif"),
    (re.compile(r"^Adverbe\b", re.I), "adverbe"),
    (re.compile(r"^conjonction\b", re.I), "conjonction"),
    (re.compile(r"^Pronom\b|^pronom\b|^Proforme\b", re.I), "pronom"),
    (re.compile(r"^Postposition\b", re.I), "postposition"),
    (re.compile(r"^(?:pré|pre)position\b", re.I), "préposition"),
    (re.compile(r"^Interjection\b", re.I), "interjection"),
    (re.compile(r"^Nombre\b", re.I), "nombre"),
    (re.compile(r"^Article\b", re.I), "déterminant"),
    (re.compile(r"^Quantificateur\b", re.I), "quantificateur"),
    (re.compile(r"^Focalisateur\b", re.I), "particule"),
    (re.compile(r"^particule\b", re.I), "particule"),
    (re.compile(r"^prédicatif verbal\b", re.I), "prédicatif verbal"),
    (re.compile(r"^complémenteur\b", re.I), "marqueur_grammatical"),
    (re.compile(r"^Copule\b|^auxiliaire\b", re.I), "copule"),
    (re.compile(r"^Déterminant\b", re.I), "déterminant"),
]

META_PREFIX = re.compile(
    r"^(?:Note|Gram|Category|Usage|Verbal suffix|Plural suffix|Underlying form"
    r"|synonyme|similaire|comp|compare|Anth|Source|Restrict|Socio|Phon|tone"
    r"|idiom|patient|agent|See main entry|Variant|summary-definition|Disc"
    r"|unité|Verbe associé|Forme|Restrict)\b"
    r"|^(?:Nom \.|Verbe\b|Adjectif\b|Adverbe\b|Pronom\b)", re.I,
)

FR_STOP = {
    "le", "la", "les", "un", "une", "des", "du", "de", "au", "aux", "ce", "cette",
    "ces", "son", "sa", "ses", "leur", "qui", "que", "dont", "où", "pour", "avec",
    "dans", "sur", "sous", "par", "être", "faire", "fait", "se", "ne", "pas",
    "ou", "et", "en", "à", "très", "plus", "est", "sont", "il", "elle", "ils",
    "elles", "je", "tu", "nous", "vous", "mon", "ma", "mes", "ton", "ta", "tes",
    "c'est", "plus", "tous", "toutes", "chacun", "aussi", "entre", "depuis",
    "vers", "chez", "sans", "surtout", "après", "avant", "comme", "même",
}

# Motifs français détectables sans ambigüeté dans une glose.

MOTS_SNK = {
    "da", "i", "a", "wa", "na", "ma", "n'", "nta", "nan", "di", "ke", "xa",
    "do", "be", "ti", "ku", "ŋa", "ya", "su", "ri", "ka", "ga", "fo", "o",
    "an", "in", "un", "nen", "nen", "kini", "yi", "nu", "ne", "te", "se",
}
CAR_SNK = set("ŋɲɓɗƴ")


def para_est_francais(txt: str) -> bool:
    if has_french_accents(txt):
        return True
    mots = re.findall(r"[a-zà-ÿ']+", txt.lower())
    return sum(1 for m in mots if m in FR_STOP) >= 2


def para_est_snk(txt: str) -> bool:
    """Phrase soninkée attestée (lettre spéciale ou mots grammaticaux)."""
    if est_anglais(txt) or para_est_francais(txt):
        return False
    if any(c in txt for c in CAR_SNK):
        return True
    mots = set(re.findall(r"[a-zñɓɗƴŋɲɛɔ']+", txt.lower()))
    return len(mots & MOTS_SNK) >= 2


def est_sigle(txt: str) -> bool:
    t = txt.strip().strip("(" ")").strip()
    if not t:
        return True
    if t.upper() in SIGLES:
        return True
    # forme entièrement en capitales courte : sigle non traduit (LOC, EQ…)
    return bool(re.fullmatch(r"[A-Z][A-Z0-9/ -]{1,11}", t)) and " " not in t.strip() or (
        len(t) <= 14 and t.upper() == t and re.fullmatch(r"[A-Z0-9/ -]+", t)
        and not any(c in t for c in "àâäéèêëîïôöùûüçœæ"))


def sans_chiffres(txt: str) -> str:
    return re.sub(r"\d+", "", txt)


def nettoyage_bord(txt: str) -> str:
    txt = txt.replace("='''''", " ")
    txt = re.sub(r"\\?\[[^\]]*?\]", " ", txt)       # balises phonétiques \[j\]
    txt = re.sub(r"\s+", " ", txt)
    txt = txt.strip(" \t,;:.").strip('"“”«»\'’')
    while txt.endswith(")") and txt.count(")") > txt.count("("):
        txt = txt[:-1].rstrip(" \t,;:.")
    return txt


# --------------------------------------------------------------- paragraphes --


def charger_paragraphes() -> list[str]:
    brut = BRUT.read_text(encoding="utf-8")
    return [p.strip() for p in brut.split("\n\n") if p.strip()]


def decouper_entrees(paras: list[str], journal: list) -> list[dict]:
    entrees: list[dict] = []
    courant: dict | None = None
    for para in paras:
        if re.fullmatch(r"[A-ZƝŊ] - [a-zɲŋ]", para):
            courant = None                     # nouvelle lettre
            continue
        # 1) sens numéroté seul en tête de paragraphe → suite de l'entrée
        if re.match(r"^\d+\s*•", para):
            if courant is not None:
                courant["corps"].append(para)
            else:
                journal.append(("orphan_sense", para[:40], "", "", "",
                                "paragraphe de sens sans entrée précédente"))
            continue
        anc = ANCHORS.search(para)
        # 2) ancre en position 0 → métadonnée de suite
        if anc and anc.start() == 0:
            if courant is not None:
                courant["corps"].append(para)
            continue
        # 3) mot d'entrée collé à un marqueur de sens « N • »
        gm = re.match(r"^(?P<hw>.+?)(?P<num>[1-9])(?P<rest>\s*•\s*)", para)
        if gm and gm.end() <= 50 and (anc is None or gm.start("num") < anc.start()):
            hw = gm.group("hw")
            corps = f"{gm.group('num')} • " + para[gm.end():]
        elif anc and 1 <= anc.start() <= 60:
            hw, corps = para[:anc.start()], para[anc.start():]
        else:
            if courant is not None:            # fragment sans étiquette
                courant["corps"].append(para)
                journal.append(("fragment_concatene", para[:40], "", "", "",
                                "paragraphe rattaché à l'entrée précédente"))
            continue
        courant = {"hw": hw, "corps": [corps]}
        entrees.append(courant)

    # déduplication des blocs strictement identiques (répétitions de la source)
    finales, vus = [], {}
    for e in entrees:
        corps = "\n\n".join(e["corps"])
        k = (e["hw"].strip(), re.sub(r"\s+", " ", corps))
        if k in vus:
            journal.append(("bloc_repete_retire", e["hw"], "entite", k[0], "",
                            "bloc identique répété dans la source"))
            continue
        vus[k] = True
        finales.append({"hw": e["hw"], "corps": corps})
    return finales


# ------------------------------------------------------------------ gloses ---


def region_apres(texte: str) -> str:
    """Glose = texte jusqu'au premier point ou marqueur de métadonnée.

    Si le segment COMMENCE par une étiquette de catégorie (« Verbe. »,
    « Nom . »…) elle est d'abord sautée : le point de l'étiquette n'est pas
    celui de fin de glose (« 2 • Verbe. ask for a gift… »).
    """
    lm = POS_HEAD.match(texte)
    if lm:
        texte = texte[lm.end():]
    pos = [m.start() for m in re.finditer(r"\.", texte)]
    mp = META_CUT.search(texte)
    coupes = ([p + 1 for p in pos] if pos else []) + ([mp.start()] if mp else [])
    if not coupes:
        return texte
    return texte[:min(coupes)]


def extraire_gloses(brut_corps: str) -> tuple[list[str], str | None]:
    """Renvoie (segments français bruts, glose résumé française éventuelle)."""
    corps = brut_corps.replace("='''''", " ")
    corps = re.sub(r"\\?\[[^\]]*?\]", " ", corps)
    gloses: list[str] = []
    resume = None
    m = re.search(r"summary-definition:\s*([^.\n]{1,240})\.", corps)
    if m:
        resume = m.group(1).strip()
    # 1) après chaque libellé de catégorie (recherche non ancrée)
    for m in POS_ANY.finditer(corps):
        seg = region_apres(corps[m.end():])
        gloses.append(seg)
    # 2) après chaque marqueur de sens « N • »
    for m in re.finditer(r"\d\s*•\s*", corps):
        seg = region_apres(corps[m.end():])
        if seg:
            gloses.append(seg)
    # 3) résumé
    if resume:
        gloses.append(resume)
    return gloses, resume


# mots de contenu anglais fréquents dans le dictionnaire (sens non traduits)
EN_CONTENU = {
    "woven", "basket", "covered", "cover", "success", "person", "people",
    "thing", "place", "time", "day", "water", "house", "make", "made", "give",
    "given", "take", "taken", "come", "went", "gone", "see", "saw", "known",
    "know", "think", "thought", "said", "told", "asked", "wanted", "needs",
    "work", "played", "run", "walked", "flew", "swim", "burn", "burned",
    "break", "broken", "cut", "hit", "kill", "killed", "died", "die", "lives",
    "live", "grow", "grown", "open", "opened", "closed", "shown", "call",
    "follow", "stopped", "stood", "sat", "spoke", "spoken", "read", "written",
    "write", "learn", "learned", "taught", "teach", "bought", "sold", "paid",
    "wait", "brought", "sent", "kept", "begin", "began", "helped", "protect",
    "guard", "attacked", "fight", "won", "lost", "strong", "literate",
    "stubborn", "disobedient", "patient", "hidden", "hide", "bad", "good",
    "old", "new", "young", "big", "small", "one", "two", "three", "first",
    "last", "same", "other", "many", "much", "more", "most", "very",
}


def en_lourd(seg: str) -> bool:
    """Au moins deux mots de contenu anglais et aucun signe français."""
    if has_french_accents(seg):
        return False
    mots = set(re.findall(r"[a-z']+", seg.lower()))
    return len(mots & EN_CONTENU) >= 2


EN_OUVERTURE = re.compile(
    r"^(?:to|the|be|is|are|was|were|it|this|that|there|these|those|and|of|with"
    r"|for|from|his|her|their|your|my|some|any|not|no|who|which|a|an)\b", re.I)
EN_INFINITIF = re.compile(r"\bto\s+[a-z]+", re.I)


def est_glose_fr(seg: str) -> bool:
    """Faux si la glose est clairement anglaise (au-delà d'est_anglais)."""
    if est_anglais(seg):
        return False
    if EN_OUVERTURE.search(seg.strip()):
        return False
    if EN_INFINITIF.search(seg):
        return False
    if en_lourd(seg):
        return False
    return True


def segment_vers_francais(seg: str, entite: str, journal: list,
                          exclusions: list) -> str | None:
    """Nettoie un segment de glose et renvoie la traduction française ou None."""
    seg = POS_HEAD.sub("", seg.strip())
    seg = re.sub(r"^\d+\s*•\s*", "", seg.strip())
    seg = nettoyage_bord(seg)
    if not seg:
        return None
    if ";" not in seg:
        mots_seg = re.findall(r"[a-zà-ÿ']+", seg.lower())
        indice_fr = (has_french_accents(seg)
                     or any(m in FR_STOP for m in mots_seg))
        if not indice_fr:
            exclusions.append((entite, seg, "glose_anglaise_sans_fr"))
            return None
    if seg == "??" or seg.startswith("??") and len(seg) <= 3:
        exclusions.append((entite, seg, "marqueur_incertitude_??"))
        return None
    parties = [p.strip() for p in seg.split(";") if p.strip()]
    if not parties:
        return None
    candidats = [q for q in reversed(parties)
                 if est_glose_fr(q) and not en_lourd(q)]
    if not candidats:
        exclusions.append((entite, seg, "glose_anglaise_sans_fr"))
        return None
    fr = candidats[0]
    if est_sigle(fr):
        exclusions.append((entite, fr, "sigle_non_traduit"))
        return None
    if fr in {"??", "??"} or re.fullmatch(r"\?+", fr):
        exclusions.append((entite, fr, "marqueur_incertitude_??"))
        return None
    if not est_glose_fr(fr):
        exclusions.append((entite, seg, "glose_anglaise_sans_fr"))
        return None
    nettoye = nettoyer_fr(fr, journal, entite)
    if not nettoye:
        exclusions.append((entite, seg, "glose_anglaise_sans_fr"))
        return None
    if est_sigle(nettoye):
        exclusions.append((entite, nettoye, "sigle_non_traduit"))
        return None
    if POS_GLOSE_VIDE.match(nettoye):
        exclusions.append((entite, nettoye, "libelle_categorie_comme_glose"))
        return None
    if not est_glose_fr(nettoye):
        exclusions.append((entite, nettoye, "glose_anglaise_sans_fr"))
        return None
    return nettoye


def categorie_de(corps: str) -> str:
    m = POS_ANY.search(corps)
    if not m:
        return ""
    libelle = corps[m.start():].strip()
    libelle = libelle.split(".", 1)[0]
    for rx, cat in CATEGORIE_PAR_POS:
        if rx.match(libelle):
            return cat
    return ""


def extraire_variantes(corps: str) -> list[str]:
    m = re.search(r"Variant:\s*([^.\n]+)", corps)
    if not m:
        return []
    brutes = re.split(r"[;,]", m.group(1))
    out = []
    for v in brutes:
        v = nettoyage_bord(re.sub(r"\\?\[[^\]]*?\]", " ", v))
        v = sans_chiffres(v).strip()
        if v and v.lower() not in {"see", ""}:
            out.append(v)
    return out


# ---------------------------------------------------------------- exemples ---


def decouper_phrases(txt: str) -> list[str]:
    txt = txt.replace("='''''", " ")
    txt = re.sub(r"\\?\[[^\]]*?\]", " ", txt)
    parts = re.split(r"(?<=[.!?])\s*(?=[A-ZÀ-ÝŒŽ])|(?<=\))\s*(?=[A-ZÀ-ÝŒŽ])", txt)
    return [p.strip() for p in parts if p.strip()]


def extraire_paires_exemples(entite: str, corps: str, journal: list) -> list[tuple[str, str]]:
    """Paires attestées : phrase soninkée → (phrase anglaise) → phrase française."""
    phrases = decouper_phrases(corps)
    paires = []
    for i in range(1, len(phrases) - 1):
        prev, mid, fr = phrases[i - 1], phrases[i], phrases[i + 1]
        if len(mid) > 6 and est_anglais(mid) and para_est_francais(fr) \
                and not est_anglais(fr) and para_est_snk(prev) \
                and normaliser_glose(prev) != normaliser_glose(fr):
            if META_PREFIX.search(prev) or META_PREFIX.search(fr):
                continue
            # nettoyage AVANT validation : métadonnées collées (« …synonyme: »)
            prev0 = re.split(META_CUT, prev)[0]
            fr0 = re.split(META_CUT, fr)[0]
            # sens numéroté collé à la fin de la phrase (« …prospères. 2 • … »)
            prev0 = re.split(r"\s+\d+\s*•\s*", prev0)[0]
            fr0 = re.split(r"\s+\d+\s*•\s*", fr0)[0]
            snk = nettoyage_bord(sans_chiffres(prev0))
            frs = nettoyage_bord(fr0)
            if len(snk) < 6 or len(frs) < 3:
                continue
            if len(snk) > 320 or len(frs) > 320:
                continue
            if not para_est_francais(frs) or est_anglais(frs) \
                    or not para_est_snk(snk):
                continue
            paires.append((snk, frs))
            journal.append(("exemple_atteste", entite, "exemples", prev, snk,
                            f"paire soninké→français (anglais supprimé : {mid[:60]})"))
    return paires


# ------------------------------------------------------------------- main ---


def main() -> int:
    journal: list[tuple] = []
    exclusions: list[tuple] = []          # (entite, glose, motif)
    comparaison: list[tuple] = []
    renvois: list[tuple] = []
    exclusions_ang: list[tuple] = []

    paras = charger_paragraphes()
    entrees = decouper_entrees(paras, journal)
    _, connues = charger_lexique()               # lexique base (lecture seule)

    mots: list[dict] = []
    expressions: list[dict] = []
    expr_vus: set[str] = set()

    # -- 1. traitement Entrée → gloses françaises --------------------------
    traitees = []
    for e in entrees:
        hw_brut = e["hw"]
        corps = e["corps"]
        hw_raw = re.sub(r"\s+", " ",
                        re.sub(r"\\?\[[^\]]*?\]", " ", hw_brut)).strip(" \t.,;:!?")
        hw = re.sub(r"\s+", " ", sans_chiffres(hw_raw)).strip(" \t.,;:!?")
        if not hw:
            journal.append(("tete_vide", hw_brut[:40], "", "", "",
                            "mot d'entrée vidé après retrait des chiffres"))
            continue
        if hw != hw_brut:
            journal.append(("chiffres_retires", hw_brut, "soninke", hw_brut, hw,
                            "marqueur d'homonyme/chiffre retiré de la forme "
                            "soninkée affichée"))
        gloses, resume = extraire_gloses(corps)
        fr_sens: list[str] = []
        for g in gloses:
            fr = segment_vers_francais(g, hw, journal, exclusions)
            if fr:
                fr_sens.append(fr)
        # dédoublonnage des sens strictement identiques
        vus_fr: set[str] = set()
        sens_finaux = []
        for s in fr_sens:
            k = normaliser_glose(s)
            if k and k not in vus_fr:
                vus_fr.add(k)
                sens_finaux.append(s)
        est_renvoi = corps.startswith("See main entry:") or "See main entry:" in corps[:80]
        if not sens_finaux:
            traitees.append({"hw": hw, "hw_raw": hw_raw, "fr": "",
                             "cat": categorie_de(corps),
                             "variantes": extraire_variantes(corps),
                             "corps": corps, "renvoi": est_renvoi})
            continue
        traitees.append({"hw": hw, "hw_raw": hw_raw, "fr": " / ".join(sens_finaux),
                         "cat": categorie_de(corps),
                         "variantes": extraire_variantes(corps),
                         "corps": corps, "renvoi": est_renvoi})

    # -- 2. exclusions anglaises (aucune glose française publiable) ---------
    for t in traitees:
        if not t["fr"]:
            motifs = [x[2] for x in exclusions if x[0] == t["hw"]]
            motif = motifs[-1] if motifs else "aucune_glose_francaise"
            comparaison.append(("sans_glose_fr", t["hw"], "", motif))
            exclusions_ang.append((t["hw"],
                                   t["corps"][:150].replace("\n", " "), motif))
            if t["renvoi"]:
                renvois.append((t["hw"], t["corps"][:200].replace("\n", " "), motif))

    # -- 3. collisions d'homonymes internes (jamais fusionnées) ------------
    groupes: dict[str, list[dict]] = {}
    for t in traitees:
        if not t["fr"]:
            continue
        groupes.setdefault(cle(t["hw"]), []).append(t)
    collisions: dict[str, list[dict]] = {}
    for k, membres in groupes.items():
        if len(membres) < 2:
            continue
        # formes BRUTES distinctes (y c. numéros d'homonyme : yille1/yille2…)
        # convergent vers la même clé après retrait des chiffres → jamais
        # fusionnées silencieusement : écartement + rapport d'arbitrage.
        raws = {m["hw_raw"] for m in membres}
        if len(raws) > 1:
            collisions[k] = membres

    # -- 4. publication des mots (filtre lexique base + collisions) ---------
    vus_pub: set[str] = set()
    for t in traitees:
        if not t["fr"]:
            continue
        # locutions multi-mots → expressions
        multi = len(t["hw"].split()) >= 2
        k = cle(t["hw"])
        if k in connues:
            comparaison.append(("doublon_lexique", t["hw"], t["fr"],
                                connues[k].get("id", "")))
            continue
        if k in collisions:
            membres = collisions[k]
            comparaison.append((
                "collision_homonyme_interne", t["hw"], t["fr"],
                "formes: " + ", ".join(sorted({m["hw"] for m in membres}))))
            continue
        if k in vus_pub:
            comparaison.append(("doublon_interne", t["hw"], t["fr"], ""))
            continue
        vus_pub.add(k)
        comparaison.append(("nouveau", t["hw"], t["fr"], ""))
        row = {
            "soninke": t["hw"], "francais": t["fr"], "categorie":
                "expression" if multi else t["cat"],
            "variantes": ", ".join(t["variantes"]), "note": "",
        }
        if multi:
            note = ["locution"]
            if t["cat"]:
                note.append(f"catégorie source: {t['cat']}")
            if t["renvoi"]:
                note.append("renvoi")
            row["note"] = "; ".join(note)
            expressions.append(row)
        else:
            note = []
            if t["renvoi"]:
                note.append("renvoi")
            if any(len(s) > 1 for s in t["fr"].split(" / ")):
                note.append(f"sens: 1-{len(t['fr'].split(' / '))}")
            row["note"] = "; ".join(note)
            mots.append(row)

    # -- 5. variantes (retrait chiffres + collisions) -----------------------
    tetes_finales = set(connues) | {cle(m["soninke"]) for m in mots} \
        | {cle(m["soninke"]) for m in expressions}
    for row in mots + expressions:
        hw = row["soninke"]
        vars_ok = []
        for v in row["variantes"].split(", ") if row["variantes"] else []:
            v = sans_chiffres(v.strip())
            if not v or cle(v) == cle(hw):
                continue
            if cle(v) in tetes_finales and cle(v) != cle(hw):
                journal.append(("variante_ecartee_collision", hw, "variantes", v, "",
                                "forme déjà utilisée comme tête de lexique/candidat"))
                continue
            if v not in vars_ok:
                vars_ok.append(v)
        row["variantes"] = ", ".join(vars_ok)

    # -- 6. expressions attestées dans les exemples ------------------------
    for t in traitees:
        if not t["fr"]:
            continue
        for snk, fr in extraire_paires_exemples(t["hw"], t["corps"], journal):
            k = cle(snk)
            if k in connues:
                comparaison.append(("doublon_lexique_exemple", snk, fr,
                                    connues[k].get("id", "")))
                continue
            if k in vus_pub or k in expr_vus:
                continue
            expr_vus.add(k)
            vus_pub.add(k)
            comparaison.append(("nouveau_expression_atteste", snk, fr, ""))
            expressions.append({"soninke": snk, "francais": fr,
                                "categorie": "expression", "variantes": "",
                                "note": f"exemple attesté de l'entrée « {t['hw']} »"})

    # -- 7. rapports --------------------------------------------------------
    for p in (MOTS_OUT, EXPRESSIONS_OUT, RAPPORT_CMP, RAPPORT_COLL,
              RAPPORT_RENVOI, RAPPORT_ANG, RAPPORT_NET):
        p.parent.mkdir(parents=True, exist_ok=True)

    def ecrire(path, champs, rows):
        with path.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, delimiter=";", lineterminator="\n")
            w.writerow(champs)
            w.writerows(rows)

    ecrire(MOTS_OUT, CHAMPS_CAND,
           [[r[c] for c in CHAMPS_CAND] for r in mots])
    ecrire(EXPRESSIONS_OUT, CHAMPS_CAND,
           [[r[c] for c in CHAMPS_CAND] for r in expressions])
    ecrire(RAPPORT_CMP, ["resultat", "soninke", "francais", "reference"], comparaison)
    ecrire(RAPPORT_COLL, ["cle", "formes_source", "gloses", "statut"],
           [[k,
             ", ".join(sorted({m["hw_raw"] for m in v})),
             " || ".join(sorted({m["fr"] for m in v}))[:500],
             "ecarte_attente_arbitrage_utilisateur"]
            for k, v in sorted(collisions.items())])
    ecrire(RAPPORT_RENVOI, ["soninke", "extrait_corps", "motif"], renvois)
    ecrire(RAPPORT_ANG, ["soninke", "extrait", "motif"], exclusions_ang)
    ecrire(RAPPORT_NET, ["action", "entite", "champ", "avant", "apres", "commentaire"],
           journal)

    # -- 8. auto-vérification stricte ---------------------------------------
    erreurs: list[str] = []
    for nom, rows in (("mots", mots), ("expressions", expressions)):
        for r in rows:
            if not r["soninke"] or not r["francais"]:
                erreurs.append(f"{nom}: ligne vide {r}")
            if re.search(r"\d", r["soninke"]):
                erreurs.append(f"{nom}: chiffre dans « {r['soninke']} »")
            if est_anglais(r["francais"]):
                erreurs.append(f"{nom}: anglais dans « {r['soninke']} » → "
                               f"« {r['francais']} »")
            if cle(r["soninke"]) in connues:
                erreurs.append(f"{nom}: doublon lexique base « {r['soninke']} »")
    for nom, rows in (("mots", mots), ("expressions", expressions)):
        seen: set[str] = set()
        for r in rows:
            k = cle(r["soninke"])
            if k in seen:
                erreurs.append(f"{nom}: doublon interne « {r['soninke']} »")
            seen.add(k)
    if erreurs:
        print("ÉCHEC de l'auto-vérification :")
        for e in erreurs[:50]:
            print("  -", e)
        return 1

    compte: dict[str, int] = {}
    for etat, *_ in comparaison:
        compte[etat] = compte.get(etat, 0) + 1
    print(f"paragraphes lus : {len(paras)} | entrées : {len(entrees)}")
    print(f"mots publiés : {len(mots)} | expressions publiées : {len(expressions)}")
    for etat in sorted(compte):
        print(f"  {etat}: {compte[etat]}")
    print(f"collisions d'homonymes écartées : {len(collisions)}")
    print(f"renvois sans glose : {len(renvois)} | exclusions anglaises : "
          f"{len(exclusions_ang)}")
    print(f"journal de nettoyage : {len(journal)} lignes")
    print("auto-vérification stricte : OK")
    print(f"mots         : {MOTS_OUT}")
    print(f"expressions  : {EXPRESSIONS_OUT}")
    print(f"comparaison  : {RAPPORT_CMP}")
    print(f"collisions   : {RAPPORT_COLL}")
    print(f"renvois      : {RAPPORT_RENVOI}")
    print(f"anglais      : {RAPPORT_ANG}")
    print(f"nettoyage    : {RAPPORT_NET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
