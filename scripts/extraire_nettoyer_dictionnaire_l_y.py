#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrait et nettoie les lettres L→Y du dictionnaire soninké (source SIL/IPS).

Source : `data/source/dictionnaire-l-y-brut-2026-10-25.txt` (archive brute
concaténée des 16 fichiers L..Y, texte dépourvu d'URL et de liens Markdown).

Pipeline (aucune écriture dans le lexique base — lecture seule) :

  1. lecture des paragraphes → entrées (mot d'entrée + corps) ;
     • réparation en mémoire des séquences Mojibake UTF-8/CP1252 de la source
       brute sans altérer l'archive brute ;
     • séparation des marqueurs de sens « N • » collés au mot d'entrée AVANT
       tout retrait de chiffres (`yille11 •` → tête `yille1` + sens `1 •`,
       `taaxu1 •` → tête `taaxu`, `ma31 •` → tête `ma3`) ;
     • rattachement des fragments botaniques de suite (`Bombax costatum…`,
       `Combretum eliotii…`) et exclusion des enregistrements sans tête
       (`nVcv-pattern: NV`) ;
     • décomposition des têtes doubles (`seegi seegu`, `Ɲatu, Takko`…) en
       mot principal + variante attestée ;
     • retrait des blocs strictement identiques répétés par la source ;
  2. extraction des gloses françaises (libellés de catégorie y compris voix
     parenthésées `verbe passif (intransitif).`, sens numérotés, entrées sans
     étiquette grammaticale, et `summary-definition:` uniquement en repli) ;
     conservation de toutes les sous-gloses françaises séparées par `;` ;
     retrait des exemples, métadonnées (`antonyme:`, `verbe:`, `nom associé:`,
     etc.), anglais (y compris noms propres anglais `Egypt`, `Solomon`,
     `Samaria`, `Guinea Conakry`, `Qur'an`), sigles grammaticaux non traduits
     (`PROintrg`, `DETintrg`, `RELtemp`, `REFndef`, `LOC`, `SG`, `INTR`… sans
     jamais confondre le mot français `mot`), noms scientifiques latins,
     marqueurs `??` et `='''''` ;
  3. retrait des chiffres éditoriaux/numéros d'homonyme sur les formes
     soninkées (mots et variantes), SANS supprimer les nombres réels (dates,
     heures : `1993`, `9-hur`) dans les phrases d'exemples ;
  4. distinction mots / expressions :
     • mots = entrées lexicales simples ;
     • expressions = vraies locutions multi-mots + paires attestées
       phrase soninkée → phrase française (phrase anglaise intermédiaire
       supprimée, citations bibliographiques `Diagana 1994:…` nettoyées,
       coupure correcte devant les majuscules soninkées `Ŋ` et `Ɲ`) ;
  5. filtrage strict contre `data/source/lexique-soninke-fr-base.csv`
     (`soninke` + `variantes` séparées par `,`, `;` ou `|`, aligné sur les clés
     de SoninkeGPT `ñ=ɲ` et formes accentuées) : aucun doublon du lexique base
     n'est publié ; les collisions d'homonymes internes (numérotées ou non
     numérotées à gloses distinctes) ne sont JAMAIS fusionnées silencieusement ;
     les homographes sources non traduits sont signalés en note ;
  6. rapports d'audit + auto-vérification stricte.

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
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from import_extraction_sans_doublons import cle, normaliser_glose
from nettoyer_integrer_dictionnaire_d_f import (
    est_anglais,
    nettoyer_fr,
)
from extract_dictionnaire_soninke import has_french_accents

BRUT = Path("data/source/dictionnaire-l-y-brut-2026-10-25.txt")
LEXIQUE = Path("data/source/lexique-soninke-fr-base.csv")
MOTS_OUT = Path("data/candidates/dictionnaire-l-y-mots-importables-2026-10-25.csv")
EXPRESSIONS_OUT = Path(
    "data/candidates/dictionnaire-l-y-expressions-importables-2026-10-25.csv"
)
RAPPORT_CMP = Path("data/reports/comparaison-dictionnaire-l-y-2026-10-25.csv")
RAPPORT_COLL = Path("data/reports/collisions-homonymes-dictionnaire-l-y-2026-10-25.csv")
RAPPORT_RENVOI = Path("data/reports/renvois-sans-glose-dictionnaire-l-y-2026-10-25.csv")
RAPPORT_ANG = Path("data/reports/exclusions-anglais-dictionnaire-l-y-2026-10-25.csv")
RAPPORT_NET = Path("data/reports/nettoyage-dictionnaire-l-y-2026-10-25.csv")

DATE = "2026-10-25"
CHAMPS_CAND = ["soninke", "francais", "categorie", "variantes", "note"]

MOJIBAKE_MAP = {
    "Å‹": "ŋ",
    "É²": "ɲ",
    "Ã©": "é",
    "Ã¨": "è",
    "Ãª": "ê",
    "Ã«": "ë",
    "Ã®": "î",
    "Ã¯": "ï",
    "Ã´": "ô",
    "Ã¹": "ù",
    "Ã»": "û",
    "Ã§": "ç",
    "Ã¡": "á",
    "Ã\xa0": "à",
    "Ã ": "à ",
}


def reparer_mojibake(txt: str) -> str:
    """Corrige en mémoire les séquences Mojibake UTF-8/CP1252 issues du HTML SIL."""
    for bad, good in MOJIBAKE_MAP.items():
        txt = txt.replace(bad, good)
    return txt


def cle_soninkegpt(mot: str) -> str:
    """Clé alignée sur normalizeLexicalKey() d'app.js (ñ→ɲ, tirets, casse, NFC)."""
    return cle((mot or "").replace("ñ", "ɲ").replace("Ñ", "ɲ"))


def cle_sans_ton(mot: str) -> str:
    """Clé sans accents vocaliques (alignée sur normalizeWord() d'app.js)."""
    s = (mot or "").replace("ñ", "ɲ").replace("Ñ", "ɲ")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return cle(s)


def charger_lexique_complet(lexique_path: Path = LEXIQUE):
    """Charge le lexique canonique en découpant variantes sur `,`, `;` et `|`."""
    with lexique_path.open(encoding="utf-8", newline="") as fh:
        lignes = list(csv.DictReader(fh, delimiter=";"))
    connues: dict[str, dict] = {}
    connues_sans_ton: dict[str, dict] = {}
    for ligne in lignes:
        if not ligne.get("id"):
            continue
        variantes = re.split(r"[;,|]", ligne.get("variantes") or "")
        for forme in [ligne["soninke"], *variantes]:
            if forme and forme.strip():
                connues.setdefault(cle_soninkegpt(forme), ligne)
                connues_sans_ton.setdefault(cle_sans_ton(forme), ligne)
    return lignes, connues, connues_sans_ton


# ----------------------------------------------------------------- analyse ---

# Ancres de corps : première rencontre ⇒ séparation mot d'entrée / corps.
ANCHORS = re.compile(
    r"summary-definition:|See main entry:|compare:|Variant:|Note:|Source:|Gram:"
    r"|Usage:|Category:|Plural suffix:|Underlying form:|Verbal suffix form:"
    r"|synonyme:|antonyme:|similaire:|comp:|idiom:|patient:|agent:|tone:|Anth:|Socio:|Phon:"
    r"|Restrict:|unité:|Disc:|nVcv-pattern:|verbe:|nom associé:|inst:|générique:|spécifique:"
    r"|Nom \.|Nom commun\.|Nom Propre\.|Verbe transitif|Verbe intransitif|verbe d'état"
    r"|verbe passif|verbe antipassif|verbe causitif|verbe objet-incorporé|verbe sériel"
    r"|Adjectif\.|Adverbe\.|Interjection\.|Pronom\."
    r"|Postposition\.|conjonction de coordination\.|conjonction de subordination\."
    r"|Nombre cardinal\.|Nombre ordinal\.|Article indéfini\.|Focalisateur\."
    r"|Quantificateur\.|particule question\.|complémenteur\.|prédicatif verbal\."
    r"|pronom emphatique\.|Proforme interrogatif\.|Déterminant interrogatif\."
    r"|Copule\.|auxiliaire existential\.|(?:pré|pre)position\.|Verbe\.",
    re.I,
)

# Étiquettes de catégorie (libellés source) — libellés composés avant simples,
# y compris qualificatifs entre parenthèses « verbe passif (intransitif). ».
_POS_ALT = (
    r"Nombre ordinal|Nombre cardinal|"
    r"verbe (?:causitif|antipassif|passif|transitif|intransitif|d'état"
    r"|objet-incorporé|sériel)(?:\s*\([^)]+\))?|"
    r"Nom commun|Nom Propre|Nom|Adverbe|Adjectif|Postposition|(?:pré|pre)position|"
    r"conjonction de coordination|conjonction de subordination|Conjonction|Pronom|"
    r"pronom emphatique|Proforme interrogatif|Déterminant interrogatif|"
    r"Article indéfini|Copule|auxiliaire existential|Focalisateur|Quantificateur|"
    r"particule question|complémenteur|prédicatif verbal|Interjection|"
    r"verbe associé|Verbe"
)
POS_ANY = re.compile(r"(?:" + _POS_ALT + r")\s*\.\s*", re.I)
POS_HEAD = re.compile(r"^(?:" + _POS_ALT + r")\s*\.\s*", re.I)
POS_GLOSE_VIDE = re.compile(
    r"^(?:Verbe|Nom|Adjectif|Adverbe|Pronom|Interjection|Postposition|"
    r"(?:pré|pre)position|Conjonction|Copule|Nombre|Article|Focalisateur|"
    r"Quantificateur|Particule|complémenteur|prédicatif verbal|Attributif)"
    r"(?:\s+(?:transitif|intransitif|passif|antipassif|causitif|commun|Propre"
    r"|cardinal|ordinal|de coordination|de subordination))?(?:\s*\([^)]+\))?$",
    re.I,
)

META_CUT = re.compile(
    r"Category:|Note:|Gram:|Usage:|Plural suffix:|Verbal suffix form:"
    r"|Underlying form:|synonyme:|antonyme:|similaire:|comp:|compare:|idiom:|patient:"
    r"|agent:|Anth:|Socio:|Phon:|tone:|Restrict:|Source:|See main entry:"
    r"|summary-definition:|Variant:|Disc:|unité:|verbe associé:|nom associé:"
    r"|verbe:|inst:|générique:|spécifique:|mat:|nVcv-pattern:"
)

# Sigles grammaticaux non traduits (attention : jamais le mot français « mot »).
SIGLES_EXACTS = {
    "LOC", "SG", "PL", "BCMR", "POST", "EQ", "INTR", "CNTRST", "RELtemp",
    "PROintrg", "DETintrg", "ABST", "FOC", "NOMR", "COMP", "QULR", "CAUS",
    "ANTI", "PASS", "ADJR/NR", "RFLX", "REC", "MBR", "CONCTR", "DEON",
    "ANTI-PASS", "REFndef", "INSTR", "OCCUP", "AGENT", "1SG", "1SGEMP",
    "2PPL", "2PAN", "INTER", "REL", "DEONIC", "QULR.", "X", "IMPRFex",
}
SIGLES_UPPER = {s.upper() for s in SIGLES_EXACTS}

# Noms propres restés uniquement en anglais dans la source SIL (aucune traduction inventée).
EN_PROPRES_EXCLUS = {
    "egypt", "guinea conakry", "samaria", "solomon", "qur'an", "lebanon",
    "moses", "manasseh", "naphtali", "zebulun", "simeon", "shittim",
    "judah", "jordan", "jericho", "issachar", "levi", "reuben",
}

# Gloses françaises attestées sans point-virgule ni accent dans la source.
FR_ATTESTES_SANS_PV = {
    "roi", "secouer", "clarifier", "bonnes oeuvres",
}

# Sous-gloses françaises courtes sans accent ni mot-outil dans les segments multi-`;`.
FR_MULTI_ATTESTES = {
    "tante", "danseur", "alcool", "couchette", "balayer", "tromper",
    "indiquer, montrer", "pouvoir, savoir", "ne pas pouvoir, ne pas savoir",
    "testament, faire",
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
    r"|synonyme|antonyme|similaire|comp|compare|Anth|Source|Restrict|Socio|Phon|tone"
    r"|idiom|patient|agent|See main entry|Variant|summary-definition|Disc"
    r"|unité|Verbe associé|nom associé|verbe|inst|générique|spécifique|Forme)\b"
    r"|^(?:Nom \.|Verbe\b|verbe\b|Adjectif\b|Adverbe\b|Pronom\b)",
    re.I,
)

BIBLIO_PREFIX = re.compile(
    r"^(?:(?:Note:\s*)?(?:Y\.\s*)?Diagana\s*,?\s*\d{4}\s*:\s*\d+(?:-[0-9]+)?(?:[a-d]\b)?\s*(?:/e)?\s*"
    r"|(?:Note:\s*)?YD\s*\d{4}\s*:\s*\d+(?:-[0-9]+)?(?:[a-d]\b)?\s*(?:/e)?\s*)+"
)

CONTINUATION_BOTANIQUE = re.compile(
    r"^[A-Z][a-z]{3,}\s+[a-z]{3,}\.(?:Note:|synonyme:|Underlying form:|Category:)"
)

FR_STOP = {
    "le", "la", "les", "un", "une", "des", "du", "de", "au", "aux", "ce", "cette",
    "ces", "son", "sa", "ses", "leur", "qui", "que", "dont", "où", "pour", "avec",
    "dans", "sur", "sous", "par", "être", "faire", "fait", "se", "ne", "pas",
    "ou", "et", "en", "à", "très", "plus", "est", "sont", "il", "elle", "ils",
    "elles", "je", "tu", "nous", "vous", "mon", "ma", "mes", "ton", "ta", "tes",
    "c'est", "tous", "toutes", "chacun", "aussi", "entre", "depuis",
    "vers", "chez", "sans", "surtout", "après", "avant", "comme", "même",
}

MOTS_SNK = {
    "da", "i", "a", "wa", "na", "ma", "n'", "nta", "nan", "di", "ke", "xa",
    "do", "be", "ti", "ku", "ŋa", "ya", "su", "ri", "ka", "ga", "fo", "o",
    "an", "in", "un", "nen", "kini", "yi", "nu", "ne", "te", "se",
}
CAR_SNK = set("ŋɲɓɗƴ")

EN_CONTENU = {
    "woven", "basket", "covered", "cover", "success", "person", "people",
    "thing", "place", "time", "day", "water", "house", "make", "made", "give",
    "given", "take", "taken", "come", "went", "gone", "see", "saw", "known",
    "know", "think", "thought", "said", "told", "asked", "wanted", "needs",
    "work", "played", "run", "walked", "flew", "swim", "burn", "burned",
    "break", "broken", "cut", "hit", "kill", "killed", "died", "die", "lives",
    "live", "grow", "grew", "grown", "open", "opened", "closed", "shown", "call",
    "follow", "stopped", "stood", "sat", "spoke", "spoken", "read", "written",
    "write", "learn", "learned", "taught", "teach", "bought", "sold", "paid",
    "wait", "brought", "sent", "kept", "begin", "began", "helped", "protect",
    "guard", "attacked", "fight", "won", "lost", "strong", "literate",
    "stubborn", "disobedient", "patient", "hidden", "hide", "bad", "good",
    "old", "new", "young", "big", "small", "one", "two", "three", "first",
    "last", "same", "other", "many", "much", "more", "most", "very", "town",
    "become", "became", "subject", "forced", "labor",
}

EN_OUVERTURE = re.compile(
    r"^(?:to|the|be|is|are|was|were|it|this|that|there|these|those|and|of|with"
    r"|for|from|his|her|their|your|my|some|any|not|no|who|which|a|an)\b",
    re.I,
)
EN_INFINITIF = re.compile(r"\bto\s+[a-z]+", re.I)
EN_PHRASE = re.compile(
    r"\b(?:was|were|been|being|town|there|where|went|came|built|house|people|"
    r"children|woman|women|should|would|could|cannot|didn't|doesn't|don't)\b",
    re.I,
)


def _mots_fr(txt: str) -> list[str]:
    return re.findall(r"[a-zà-ÿ']+", txt.replace("’", "'").lower())


def para_est_francais(txt: str) -> bool:
    if has_french_accents(txt):
        return True
    mots = _mots_fr(txt)
    return sum(1 for m in mots if m in FR_STOP) >= 2


def para_est_snk(txt: str) -> bool:
    """Phrase soninkée attestée (lettre spéciale ou mots grammaticaux, hors anglais)."""
    # Attention : en soninké, « A » (il/elle), « An » (tu) et « no » (là-bas) sont
    # des pronoms/adverbes très fréquents en tête d'énoncé : ne jamais leur appliquer
    # EN_OUVERTURE ; filtrer uniquement les vraies phrases anglaises (EN_PHRASE).
    if est_anglais(txt) or EN_PHRASE.search(txt):
        return False
    if para_est_francais(txt):
        return False
    if any(c in txt for c in CAR_SNK):
        return True
    mots = set(re.findall(r"[a-zñɓɗƴŋɲɛɔ']+", txt.lower()))
    return len(mots & MOTS_SNK) >= 2


def est_sigle(txt: str) -> bool:
    t = txt.strip().strip("()").strip()
    if not t:
        return True
    if t in SIGLES_EXACTS:
        return True
    if any(c.isupper() for c in t) and t.upper() in SIGLES_UPPER:
        return True
    if re.fullmatch(r"\d+\)?", t):
        return True
    return (
        bool(re.fullmatch(r"[A-Z][A-Z0-9/ -]{1,11}", t)) and " " not in t.strip()
    ) or (
        len(t) <= 14
        and t.upper() == t
        and any(c.isalpha() for c in t)
        and re.fullmatch(r"[A-Z0-9/ -]+", t)
        and not any(c in t for c in "àâäéèêëîïôöùûüçœæ")
    )


def sans_chiffres_mot(txt: str) -> str:
    """Retire les numéros d'homonyme/sens sur un mot ou une variante soninkée."""
    return re.sub(r"\d+", "", txt)


def sans_chiffres_homonyme_phrase(txt: str) -> str:
    """Retire uniquement un numéro d'homonyme collé à un mot (`ɲiiɲe1` → `ɲiiɲe`),
    sans jamais effacer les nombres autonomes ou mesures (`1993`, `9-hur`).
    """
    return re.sub(r"(?<=[A-Za-zÀ-ÖØ-öø-ÿŊŋƝɲ])\d+\b", "", txt)


def nettoyage_bord(txt: str) -> str:
    txt = txt.replace("='''''", " ")
    txt = re.sub(r"\\?\[[^\]]*?\]", " ", txt)       # balises phonétiques \[j\]
    txt = re.sub(
        r"^(?:DETintrg|PROintrg|RELtemp|REFndef|INTR|LOC|BCMR|POST)\s+",
        "",
        txt.strip(),
    )
    # binôme scientifique latin en fin de glose (ex. « cram-cram, Cenchrus biflorus »)
    txt = re.sub(r",\s+[A-Z][a-z]{3,}\s+[a-z]{4,}\s*$", "", txt.strip())
    txt = re.sub(r"\\\*$", "", txt.strip())
    txt = re.sub(r"\s+", " ", txt)
    txt = txt.strip(" \t,;:.")
    # ne retire les guillemets externes que lorsqu'ils encadrent toute la glose
    paires = [('"', '"'), ("'", "'"), ("«", "»"), ("“", "”"), ("‘", "’")]
    modifie = True
    while modifie and len(txt) >= 2:
        modifie = False
        for oq, cq in paires:
            if (
                txt.startswith(oq)
                and txt.endswith(cq)
                and txt[1:-1].count(oq) == 0
                and txt[1:-1].count(cq) == 0
            ):
                txt = txt[1:-1].strip(" \t,;:.")
                modifie = True
    if txt.count('"') == 1 and txt.startswith('"'):
        txt = txt[1:].strip()
    if txt.count("'") == 1 and txt.startswith("'"):
        txt = txt[1:].strip()
    while txt.endswith(")") and txt.count(")") > txt.count("("):
        txt = txt[:-1].rstrip(" \t,;:.")
    return txt


# --------------------------------------------------------------- paragraphes --


def charger_paragraphes(brut_path: Path = BRUT) -> list[str]:
    brut = reparer_mojibake(brut_path.read_text(encoding="utf-8"))
    return [p.strip() for p in brut.split("\n\n") if p.strip()]


def decouper_entrees(paras: list[str], journal: list) -> list[dict]:
    entrees: list[dict] = []
    courant: dict | None = None
    for idx_p, para in enumerate(paras, 1):
        if re.fullmatch(r"[A-ZƝŊ] - [a-zɲŋ]", para):
            courant = None                     # nouvelle lettre
            continue
        # 0) enregistrement SIL dépourvu de mot d'entrée (ex. « nVcv-pattern: NV.Verbe... ») :
        #    on en extrait néanmoins les paires d'exemples attestées avant d'écarter l'en-tête.
        if para.lower().startswith("nvcv-pattern:"):
            journal.append((
                "entree_sans_tete_source",
                para[:40],
                "soninke",
                para[:40],
                "",
                "enregistrement morphophonologique SIL sans lemme soninké (exclu)",
            ))
            entrees.append({"hw": "__EXEMPLES_SANS_TETE__", "corps": [para], "para_idx": idx_p})
            courant = None
            continue
        # 0bis) fragment botanique de suite (« Bombax costatum.Note: D2 • »)
        if CONTINUATION_BOTANIQUE.match(para):
            if courant is not None:
                courant["corps"].append(para)
                journal.append((
                    "fragment_concatene",
                    courant["hw"].strip(),
                    "corps",
                    para[:40],
                    "",
                    "fragment taxonomique rattaché à l'entrée précédente",
                ))
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
        courant = {"hw": hw, "corps": [corps], "para_idx": idx_p}
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
    """Extrait la région de glose jusqu'à la vraie ponctuation finale de glose.

    Respecte :
      • les parenthèses `(geol.)`, `(veau, poulain, etc.)`, `(i.e. une affaire)`,
        `(Y. Diagana 1994:379)` ;
      • les citations entre guillemets `"..."` ;
      • les décimales `1.5m`, points de suspension `..` et abréviations `sthg.`
        ou ponctuations anglaises `?`/`.` précédant le `;` de traduction.
    """
    texte = re.sub(r"^\d+\s*•\s*", "", texte.strip())
    lm = POS_HEAD.match(texte)
    if lm:
        texte = texte[lm.end():]
    mp = META_CUT.search(texte)
    ms = re.search(r"\b\d+\s*•", texte)
    limites = [len(texte)]
    if mp:
        limites.append(mp.start())
    if ms:
        limites.append(ms.start())
    sub = texte[:min(limites)]

    prof_paren = 0
    dans_guillemets = False
    for idx, ch in enumerate(sub):
        if ch == '"' and (idx == 0 or sub[idx - 1] != "\\"):
            # N'ouvre des guillemets que si un guillemet fermant existe dans la suite proche
            if dans_guillemets or '"' in sub[idx + 1:idx + 220]:
                dans_guillemets = not dans_guillemets
        elif not dans_guillemets:
            if ch == "(":
                # Parenthèse fermante présente dans la glose ? (sinon parenthèse source non fermée : « couper (herbe . »)
                ferm = sub.find(")", idx + 1, idx + 80)
                if ferm != -1:
                    prof_paren += 1
            elif ch == ")" and prof_paren > 0:
                prof_paren -= 1
            elif ch in ".?!" and prof_paren == 0:
                if (
                    ch == "."
                    and idx > 0
                    and idx + 1 < len(sub)
                    and sub[idx - 1].isdigit()
                    and sub[idx + 1].isdigit()
                ):
                    continue
                if ch == "." and (
                    (idx + 1 < len(sub) and sub[idx + 1] == ".")
                    or (idx > 0 and sub[idx - 1] == ".")
                ):
                    continue
                avant = sub[max(0, idx - 6):idx].lower()
                suite_pv = ";" in sub[idx + 1:idx + 80]
                if suite_pv and (
                    ch in "?!"
                    or avant.endswith(("sthg", "s.o", "etc", "cf", "(lit", "env", "qqch", "qqn"))
                    or re.match(r"^\s*;", sub[idx + 1:])
                ):
                    continue
                # Si « ! » ou « ? » est suivi d'une minuscule française (« c'est faux ! mensonge ! »), continuer
                if ch in "?!" and re.match(r"^\s+[a-zà-ÿ]", sub[idx + 1:]):
                    continue
                return sub[:idx + 1]
    return sub


def extraire_gloses(brut_corps: str) -> tuple[list[str], str | None]:
    """Renvoie (segments de glose bruts, glose résumé éventuelle)."""
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
        if seg:
            gloses.append(seg)
    # 2) après chaque marqueur de sens « N • »
    for m in re.finditer(r"\d\s*•\s*", corps):
        seg = region_apres(corps[m.end():])
        if seg:
            gloses.append(seg)
    # 3) entrées dépourvues d'étiquette grammaticale mais portant « EN; FR. »
    #    juste après Variant:/See main entry: (ex. wujune, xanu, ɲaaye)
    if not gloses and not resume:
        corps_nu = re.sub(
            r"^(?:(?:See main entry:\s*[^.\n]*\.|Variant:\s*[^.\n]*\.|Note:\s*[^.\n]*\.)\s*)+",
            "",
            corps.strip(),
        )
        if ";" in corps_nu[:120]:
            seg = region_apres(corps_nu)
            if seg and ";" in seg:
                gloses.append(seg)
    # 4) résumé : sur les verbes passifs, conservé uniquement s'il est lui-même
    #    formulé au passif (« être ... », ex. loxose « être dégradé, être sale »),
    #    ce qui exclut les résumés actifs inversés (ex. safe « écrire »).
    est_passif = bool(re.search(r"\bverbe\s+passif\b", corps, re.I))
    resume_passif_ok = (not est_passif) or bool(resume and re.search(r"\bêtre\b", resume, re.I))
    if resume and (not gloses or resume_passif_ok):
        gloses.append(resume)
    return gloses, resume


def en_lourd(seg: str) -> bool:
    """Au moins deux mots de contenu anglais et aucun signe français."""
    if has_french_accents(seg):
        return False
    mots = set(re.findall(r"[a-z']+", seg.lower()))
    return len(mots & EN_CONTENU) >= 2


def est_glose_fr(seg: str) -> bool:
    """Faux si la glose est anglaise (y compris noms propres anglais non traduits)."""
    s = seg.strip()
    if s.lower().rstrip(".") in EN_PROPRES_EXCLUS:
        return False
    # En français, « lit » (meuble : « couchette, lit ») n'est pas l'anglais « lit ».
    s_test = re.sub(r"(?:,\s*|\b(?:un|le|du|au)\s+)lit\b", " couchage", s, flags=re.I)
    if est_anglais(s_test):
        return False
    if EN_OUVERTURE.search(s):
        return False
    if EN_INFINITIF.search(s):
        return False
    if en_lourd(s_test):
        return False
    return True


def _choisir_parties_francaises(parties: list[str]) -> list[str]:
    """Sélectionne toutes les sous-gloses françaises d'un segment découpé sur `;`."""
    if not parties:
        return []
    if len(parties) == 1:
        return parties
    if len(parties) == 2:
        p0, p1 = parties[0].strip(), parties[1].strip()
        # Ordre inversé FR; EN attesté dans la source
        # (ex. soxokomaaxu « soumettre quelqu'un à la corvée; subject someone to forced labor »,
        #  senbekite « devenir fort(e); grow strong »)
        if est_glose_fr(p0) and not est_glose_fr(p1) and (
            has_french_accents(p0)
            or "(e)" in p0.lower()
            or any(m in FR_STOP for m in _mots_fr(p0))
        ):
            return [p0]
        return [p1]
    debut = 1 if len(parties) == 3 else len(parties) // 2
    retenues: list[str] = []
    for idx in range(debut, len(parties)):
        cand = parties[idx].strip()
        mots = _mots_fr(cand)
        a_elision_fr = bool(re.search(r"\b(?:d|l|s|n|qu|c|j)'[a-zà-ÿ]", cand.replace("’", "'").lower()))
        indice_fr = (
            has_french_accents(cand)
            or a_elision_fr
            or any(m in FR_STOP for m in mots)
            or cand.lower().strip(" .?!") in FR_MULTI_ATTESTES
        )
        if idx == len(parties) - 1:
            if est_glose_fr(cand):
                retenues.append(cand)
        elif indice_fr and est_glose_fr(cand):
            retenues.append(cand)
    return retenues


def segment_vers_francais_liste(
    seg: str, entite: str, journal: list, exclusions: list
) -> list[str]:
    """Nettoie un segment de glose et renvoie la liste ordonnée des sens français."""
    seg = re.sub(r"^\d+\s*•\s*", "", seg.strip())
    seg = POS_HEAD.sub("", seg.strip())
    seg_avant_latin = seg
    seg = nettoyage_bord(seg)
    if not seg:
        return []
    if re.search(r",\s+[A-Z][a-z]{3,}\s+[a-z]{4,}\s*[.?!]?$", seg_avant_latin.strip()):
        journal.append((
            "binome_latin_retire",
            entite,
            "francais",
            seg_avant_latin.strip(),
            seg,
            "nom scientifique latin retiré de la glose française",
        ))
    if ";" not in seg:
        mots_seg = _mots_fr(seg)
        indice_fr = (
            has_french_accents(seg)
            or any(m in FR_STOP for m in mots_seg)
            or seg.lower().strip(" .?!") in FR_ATTESTES_SANS_PV
        )
        if not indice_fr:
            exclusions.append((entite, seg, "glose_anglaise_sans_fr"))
            return []
    if seg == "??" or (seg.startswith("??") and len(seg) <= 3):
        exclusions.append((entite, seg, "marqueur_incertitude_??"))
        return []
    parties = [p.strip() for p in seg.split(";") if p.strip()]
    if not parties:
        return []
    brutes_fr = _choisir_parties_francaises(parties)
    if not brutes_fr:
        dernier = nettoyage_bord(parties[-1])
        if est_sigle(dernier):
            exclusions.append((entite, dernier, "sigle_non_traduit"))
        elif re.fullmatch(r"\?+", dernier):
            exclusions.append((entite, dernier, "marqueur_incertitude_??"))
        elif POS_GLOSE_VIDE.match(dernier):
            exclusions.append((entite, dernier, "libelle_categorie_comme_glose"))
        else:
            exclusions.append((entite, seg, "glose_anglaise_sans_fr"))
        return []

    sorties: list[str] = []
    vus_loc: set[str] = set()
    for fr in brutes_fr:
        fr_propre = nettoyage_bord(fr)
        if not fr_propre:
            continue
        if est_sigle(fr_propre):
            exclusions.append((entite, fr_propre, "sigle_non_traduit"))
            continue
        if re.fullmatch(r"\?+", fr_propre):
            exclusions.append((entite, fr_propre, "marqueur_incertitude_??"))
            continue
        if not est_glose_fr(fr_propre):
            exclusions.append((entite, seg, "glose_anglaise_sans_fr"))
            continue
        # Précision parenthétique de la glose précédente : « petit des animaux; (veau, poulain, etc.) »
        if fr_propre.startswith("(") and fr_propre.endswith(")") and sorties:
            sorties[-1] = f"{sorties[-1]} {fr_propre}"
            continue
        nettoye = nettoyer_fr(fr_propre, journal, entite)
        if not nettoye:
            continue
        nettoye = nettoyage_bord(nettoye)
        if not nettoye:
            continue
        if est_sigle(nettoye):
            exclusions.append((entite, nettoye, "sigle_non_traduit"))
            continue
        if POS_GLOSE_VIDE.match(nettoye):
            exclusions.append((entite, nettoye, "libelle_categorie_comme_glose"))
            continue
        if not est_glose_fr(nettoye):
            exclusions.append((entite, nettoye, "glose_anglaise_sans_fr"))
            continue
        k = normaliser_glose(nettoye)
        if k and k not in vus_loc:
            vus_loc.add(k)
            sorties.append(nettoye)

    if not sorties and not any(x[0] == entite for x in exclusions[-2:]):
        exclusions.append((entite, seg, "glose_anglaise_sans_fr"))
    return sorties


def segment_vers_francais(
    seg: str, entite: str, journal: list, exclusions: list
) -> str | None:
    """Compatibilité unitaire : renvoie les sens français joints par ` / ` ou None."""
    sens = segment_vers_francais_liste(seg, entite, journal, exclusions)
    return " / ".join(sens) if sens else None


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


def a_renvoi_reel(corps: str) -> bool:
    """Vrai uniquement si `See main entry:` pointe vers une cible non vide."""
    m = re.search(r"See main entry:\s*([^.\n]*)\.", corps[:180])
    if not m:
        return False
    cible = m.group(1).strip(" \t,;\"'")
    return bool(cible)


def cible_renvoi(corps: str) -> str:
    m = re.search(r"See main entry:\s*([^.\n]*)\.", corps[:180])
    return m.group(1).strip(" \t,;\"'") if m else ""


def extraire_variantes(corps: str) -> list[str]:
    m = re.search(r"Variant:\s*([^.\n]+)", corps)
    if not m:
        return []
    brutes = re.split(r"[;,]", m.group(1))
    out = []
    for v in brutes:
        v = nettoyage_bord(re.sub(r"\\?\[[^\]]*?\]", " ", v))
        v = sans_chiffres_mot(v).strip()
        if v and v.lower() not in {"see", ""}:
            out.append(v)
    return out


def normaliser_tete_et_variantes(hw: str, variantes: list[str], journal: list) -> tuple[str, list[str]]:
    """Sépare les têtes doubles de mots simples (`seegi seegu`, `Ɲatu, Takko`) en
    mot d'entrée unique + variante attestée, tout en conservant les vraies locutions.
    """
    # 1) Noms propres appariés par virgule (« Ɲatu, Takko », « Tanba, Sanba »…)
    if "," in hw:
        morceaux = [p.strip() for p in hw.split(",") if p.strip()]
        if len(morceaux) >= 2 and all(" " not in m for m in morceaux):
            principal = morceaux[0]
            ajout = [m for m in morceaux[1:] if m not in variantes]
            journal.append((
                "tete_double_separee",
                hw,
                "soninke",
                hw,
                principal,
                f"variante(s) rattachée(s) depuis la tête : {', '.join(ajout)}",
            ))
            return principal, ajout + variantes
    # 2) Double forme du numéral cardinal « seegi seegu »
    if hw == "seegi seegu":
        ajout = ["seegu"] if "seegu" not in variantes else []
        journal.append((
            "tete_double_separee",
            hw,
            "soninke",
            hw,
            "seegi",
            "forme libre « seegu » rattachée en variante",
        ))
        return "seegi", ajout + variantes
    return hw, variantes


# ---------------------------------------------------------------- exemples ---


def decouper_phrases(txt: str) -> list[str]:
    txt = txt.replace("='''''", " ")
    txt = re.sub(r"\\?\[[^\]]*?\]", " ", txt)
    # Inclut les majuscules soninkées Ŋ et Ɲ (« …tam-tam.Ɲamaxalun… »)
    parts = re.split(
        r"(?<=[.!?])\s*(?=[A-ZÀ-ÝŒŽŊƝƁƊƳ])|(?<=\))\s*(?=[A-ZÀ-ÝŒŽŊƝƁƊƳ])",
        txt,
    )
    return [p.strip() for p in parts if p.strip()]


def extraire_paires_exemples(entite: str, corps: str, journal: list) -> list[tuple[str, str]]:
    """Paires attestées : phrase soninkée → (phrase anglaise) → phrase française."""
    phrases = decouper_phrases(corps)
    paires = []
    for i in range(1, len(phrases) - 1):
        prev, mid, fr = phrases[i - 1], phrases[i], phrases[i + 1]
        prev_clean = BIBLIO_PREFIX.sub("", prev).strip()
        # En français non accentué en tête, « A cause de… » / « A ce moment… » valent « À… »
        en_tete_anglaise_fr = bool(EN_OUVERTURE.search(fr)) and not re.match(
            r"^A\s+(?:cause|ce|cette|ces|la|le|les|un|une|son|sa|ses)\b", fr
        )
        if (
            len(mid) > 6
            and (est_anglais(mid) or EN_OUVERTURE.search(mid) or EN_PHRASE.search(mid))
            and para_est_francais(fr)
            and not est_anglais(fr)
            and not en_tete_anglaise_fr
            and para_est_snk(prev_clean)
            and normaliser_glose(prev_clean) != normaliser_glose(fr)
        ):
            if META_PREFIX.search(prev_clean) or META_PREFIX.search(fr):
                continue
            prev0 = re.split(META_CUT, prev_clean)[0]
            fr0 = re.split(META_CUT, fr)[0]
            prev0 = re.split(r"\s+\d+\s*•\s*", prev0)[0]
            fr0 = re.split(r"\s+\d+\s*•\s*", fr0)[0]
            snk = nettoyage_bord(sans_chiffres_homonyme_phrase(prev0))
            frs = nettoyage_bord(fr0)
            if len(snk) < 6 or len(frs) < 3:
                continue
            if len(snk) > 320 or len(frs) > 320:
                continue
            if not para_est_francais(frs) or est_anglais(frs) or not para_est_snk(snk):
                continue
            paires.append((snk, frs))
            journal.append((
                "exemple_atteste",
                entite,
                "exemples",
                prev,
                snk,
                f"paire soninké→français (anglais supprimé : {mid[:60]})",
            ))
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
    _, connues, connues_sans_ton = charger_lexique_complet()

    mots: list[dict] = []
    expressions: list[dict] = []
    expr_vus: set[str] = set()

    # -- 1. traitement Entrée → gloses françaises --------------------------
    traitees = []
    paires_sans_tete: list[tuple[str, str]] = []
    for e in entrees:
        hw_brut = e["hw"]
        corps = e["corps"]
        if hw_brut == "__EXEMPLES_SANS_TETE__":
            paires_sans_tete.extend(extraire_paires_exemples("(-nV)", corps, journal))
            continue
        hw_sans_phon = re.sub(r"\\?\[[^\]]*?\]", " ", hw_brut)
        hw_raw = re.sub(r"\s+", " ", hw_sans_phon).strip(" \t.,;:!?")
        hw = re.sub(r"\s+", " ", sans_chiffres_mot(hw_raw)).strip(" \t.,;:!?")
        if not hw:
            journal.append(("tete_vide", hw_brut[:40], "", "", "",
                            "mot d'entrée vidé après retrait des chiffres"))
            continue
        if re.search(r"\d", hw_raw) and hw != hw_raw:
            journal.append((
                "chiffres_retires",
                hw_brut.strip(),
                "soninke",
                hw_raw,
                hw,
                "marqueur d'homonyme/chiffre éditorial retiré de la forme soninkée affichée",
            ))
        elif "[" in hw_brut:
            journal.append((
                "balise_phonetique_retiree",
                hw_brut.strip(),
                "soninke",
                hw_brut.strip(),
                hw,
                "transcription phonétique entre crochets retirée du mot d'entrée",
            ))

        variantes = extraire_variantes(corps)
        hw, variantes = normaliser_tete_et_variantes(hw, variantes, journal)

        gloses, resume = extraire_gloses(corps)
        fr_sens: list[str] = []
        nb_corps = len(gloses) - (1 if (resume and gloses and gloses[-1] == resume) else 0)
        sens_corps: list[str] = []
        sens_resume: list[str] = []
        for idx_g, g in enumerate(gloses):
            extraits = segment_vers_francais_liste(g, hw, journal, exclusions)
            if idx_g < nb_corps:
                sens_corps.extend(extraits)
            else:
                sens_resume.extend(extraits)

        def _cle_dedup_sens(s: str) -> str:
            s0 = re.sub(r"^(?:l'|le |la |les |un |une |des |du |de la )", "", s.lower().strip())
            return normaliser_glose(s0)

        vus_fr: set[str] = set()
        sens_finaux = []
        for s in sens_corps:
            k = _cle_dedup_sens(s)
            if k and k not in vus_fr:
                vus_fr.add(k)
                sens_finaux.append(s)
        mots_corps = {
            w for s in sens_finaux for w in normaliser_glose(s).split() if len(w) >= 3
        }
        for s in sens_resume:
            if s.lower() == "sucsessive":
                continue
            k = _cle_dedup_sens(s)
            if not k or k in vus_fr:
                continue
            mots_res = {w for w in normaliser_glose(s).split() if len(w) >= 3}
            # Si tous les mots significatifs du résumé sont déjà couverts par les sens du corps
            # (concaténation « ériger arrêter établir, promouvoir » ou inversion « retourner (faire) »), ignorer.
            if sens_finaux and mots_res and mots_res <= mots_corps:
                continue
            # Si le résumé enrichit exactement le premier sens (« être dégradé » → « être dégradé, être sale »),
            # remplacer le sens partiel plutôt que de dupliquer le préfixe.
            remplace = False
            for idx_sf, sf in enumerate(sens_finaux):
                if s.lower().startswith(sf.lower() + ","):
                    sens_finaux[idx_sf] = s
                    remplace = True
                    break
            vus_fr.add(k)
            if not remplace:
                sens_finaux.append(s)
        est_renvoi = a_renvoi_reel(corps)
        traitees.append({
            "hw": hw,
            "hw_raw": hw_raw,
            "fr": " / ".join(sens_finaux) if sens_finaux else "",
            "cat": categorie_de(corps),
            "variantes": variantes,
            "corps": corps,
            "renvoi": est_renvoi,
            "cible_renvoi": cible_renvoi(corps),
        })

    # Index complet des homographes sources (y compris entrées sans glose FR)
    toutes_par_cle: dict[str, list[dict]] = {}
    for t in traitees:
        toutes_par_cle.setdefault(cle_soninkegpt(t["hw"]), []).append(t)

    # -- 2. exclusions anglaises (aucune glose française publiable) ---------
    for t in traitees:
        if not t["fr"]:
            motifs = [x[2] for x in exclusions if x[0] == t["hw"]]
            motif = motifs[-1] if motifs else "aucune_glose_francaise"
            comparaison.append(("sans_glose_fr", t["hw"], "", motif))
            exclusions_ang.append((
                t["hw"],
                t["corps"][:150].replace("\n", " "),
                motif,
            ))
            if t["renvoi"]:
                renvois.append((
                    t["hw"],
                    t["corps"][:200].replace("\n", " "),
                    motif,
                ))

    # -- 3. collisions d'homonymes internes (jamais fusionnées) ------------
    groupes: dict[str, list[dict]] = {}
    for t in traitees:
        if not t["fr"]:
            continue
        groupes.setdefault(cle_soninkegpt(t["hw"]), []).append(t)
    collisions: dict[str, list[dict]] = {}
    for k, membres in groupes.items():
        if len(membres) < 2:
            continue
        # Collision si formes brutes distinctes (homonymes numérotés, affixes,
        # casse nom propre/commun) OU si formes non numérotées à gloses distinctes
        # (ex. toro « figuier » vs toro « oreille », tefu « chaussure » vs « chasseur »).
        raws = {m["hw_raw"] for m in membres}
        gloses_norm = {normaliser_glose(m["fr"]) for m in membres}
        if len(raws) > 1 or len(gloses_norm) > 1:
            collisions[k] = membres

    # -- 4. publication des mots (filtre lexique base + collisions) ---------
    vus_pub: set[str] = set()
    for t in traitees:
        if not t["fr"]:
            continue
        multi = len(t["hw"].split()) >= 2
        k = cle_soninkegpt(t["hw"])
        k_st = cle_sans_ton(t["hw"])
        existant = connues.get(k)
        # Cas d'accent français dans le lexique de base (ex. SNK-LEX-0905 yigandé vs yigande)
        if existant is None and k_st in connues_sans_ton:
            cand_base = connues_sans_ton[k_st]
            if normaliser_glose(t["fr"]) in normaliser_glose(cand_base.get("francais", "")) or (
                normaliser_glose(cand_base.get("francais", "")) in normaliser_glose(t["fr"])
            ):
                existant = cand_base
        if existant is not None:
            comparaison.append((
                "doublon_lexique",
                t["hw"],
                t["fr"],
                existant.get("id", ""),
            ))
            continue
        if k in collisions:
            membres = collisions[k]
            comparaison.append((
                "collision_homonyme_interne",
                t["hw"],
                t["fr"],
                "formes: " + ", ".join(sorted({m["hw_raw"] for m in membres})),
            ))
            continue
        if k in vus_pub:
            comparaison.append(("doublon_interne", t["hw"], t["fr"], ""))
            continue
        vus_pub.add(k)
        comparaison.append(("nouveau", t["hw"], t["fr"], ""))
        row = {
            "soninke": t["hw"],
            "francais": t["fr"],
            "categorie": "expression" if multi else t["cat"],
            "variantes": ", ".join(t["variantes"]),
            "note": "",
        }
        # Signaler si un homographe source sans glose française partage la même clé
        freres_sans_fr = [
            f for f in toutes_par_cle.get(k, [])
            if not f["fr"] and f["hw_raw"] != t["hw_raw"]
        ]
        if multi:
            note = ["locution"]
            if t["cat"]:
                note.append(f"catégorie source: {t['cat']}")
            if t["renvoi"]:
                note.append(f"renvoi: {t['cible_renvoi']}")
            row["note"] = "; ".join(note)
            expressions.append(row)
        else:
            note = []
            if t["renvoi"]:
                note.append("renvoi")
            if any(len(s) > 1 for s in t["fr"].split(" / ")):
                note.append(f"sens: 1-{len(t['fr'].split(' / '))}")
            if freres_sans_fr:
                cibles = [
                    f"{f['hw_raw']}→{f['cible_renvoi']}" if f["cible_renvoi"] else f["hw_raw"]
                    for f in freres_sans_fr
                ]
                note.append("homographe source sans glose FR: " + ", ".join(cibles))
            row["note"] = "; ".join(note)
            mots.append(row)

    # -- 5. variantes (retrait chiffres + collisions) -----------------------
    tetes_finales = (
        set(connues)
        | {cle_soninkegpt(m["soninke"]) for m in mots}
        | {cle_soninkegpt(m["soninke"]) for m in expressions}
    )
    for row in mots + expressions:
        hw = row["soninke"]
        vars_ok = []
        for v in row["variantes"].split(", ") if row["variantes"] else []:
            v = sans_chiffres_mot(v.strip())
            if not v or cle_soninkegpt(v) == cle_soninkegpt(hw):
                continue
            if cle_soninkegpt(v) in tetes_finales and cle_soninkegpt(v) != cle_soninkegpt(hw):
                journal.append((
                    "variante_ecartee_collision",
                    hw,
                    "variantes",
                    v,
                    "",
                    "forme déjà utilisée comme tête ou variante du lexique/candidat",
                ))
                continue
            if v not in vars_ok:
                vars_ok.append(v)
        row["variantes"] = ", ".join(vars_ok)

    # -- 6. expressions attestées dans les exemples ------------------------
    sources_exemples = [
        (t["hw"], extraire_paires_exemples(t["hw"], t["corps"], journal))
        for t in traitees
        if t["fr"]
    ] + [("(-nV)", paires_sans_tete)]
    for hw_src, paires in sources_exemples:
        for snk, fr in paires:
            k = cle_soninkegpt(snk)
            if k in connues:
                comparaison.append((
                    "doublon_lexique_exemple",
                    snk,
                    fr,
                    connues[k].get("id", ""),
                ))
                continue
            if k in vus_pub or k in expr_vus:
                continue
            expr_vus.add(k)
            vus_pub.add(k)
            comparaison.append(("nouveau_expression_atteste", snk, fr, ""))
            expressions.append({
                "soninke": snk,
                "francais": fr,
                "categorie": "expression",
                "variantes": "",
                "note": f"exemple attesté de l'entrée « {hw_src} »",
            })

    # -- 7. rapports --------------------------------------------------------
    for p in (
        MOTS_OUT,
        EXPRESSIONS_OUT,
        RAPPORT_CMP,
        RAPPORT_COLL,
        RAPPORT_RENVOI,
        RAPPORT_ANG,
        RAPPORT_NET,
    ):
        p.parent.mkdir(parents=True, exist_ok=True)

    def ecrire(path, champs, rows):
        with path.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, delimiter=";", lineterminator="\n")
            w.writerow(champs)
            w.writerows(rows)

    ecrire(MOTS_OUT, CHAMPS_CAND, [[r[c] for c in CHAMPS_CAND] for r in mots])
    ecrire(
        EXPRESSIONS_OUT,
        CHAMPS_CAND,
        [[r[c] for c in CHAMPS_CAND] for r in expressions],
    )
    ecrire(RAPPORT_CMP, ["resultat", "soninke", "francais", "reference"], comparaison)
    ecrire(
        RAPPORT_COLL,
        ["cle", "formes_source", "gloses", "statut"],
        [
            [
                k,
                ", ".join(sorted({m["hw_raw"] for m in v})),
                " || ".join(sorted({m["fr"] for m in v}))[:500],
                "ecarte_attente_arbitrage_utilisateur",
            ]
            for k, v in sorted(collisions.items())
        ],
    )
    ecrire(RAPPORT_RENVOI, ["soninke", "extrait_corps", "motif"], renvois)
    ecrire(RAPPORT_ANG, ["soninke", "extrait", "motif"], exclusions_ang)
    ecrire(
        RAPPORT_NET,
        ["action", "entite", "champ", "avant", "apres", "commentaire"],
        journal,
    )

    # -- 8. auto-vérification stricte ---------------------------------------
    erreurs: list[str] = []
    for r in mots:
        if not r["soninke"] or not r["francais"]:
            erreurs.append(f"mots: ligne vide {r}")
        if re.search(r"\d", r["soninke"]):
            erreurs.append(f"mots: chiffre dans « {r['soninke']} »")
        if not est_glose_fr(r["francais"]) or est_sigle(r["francais"]):
            erreurs.append(
                f"mots: anglais ou sigle dans « {r['soninke']} » → « {r['francais']} »"
            )
        if cle_soninkegpt(r["soninke"]) in connues:
            erreurs.append(f"mots: doublon lexique base « {r['soninke']} »")
    for r in expressions:
        if not r["soninke"] or not r["francais"]:
            erreurs.append(f"expressions: ligne vide {r}")
        # Aucun numéro d'homonyme collé à un mot soninké ; nombres réels (1993, 9-hur) permis
        if re.search(r"[A-Za-zÀ-ÖØ-öø-ÿŊŋƝɲ]\d", r["soninke"]):
            erreurs.append(
                f"expressions: chiffre d'homonyme collé dans « {r['soninke']} »"
            )
        if est_anglais(r["soninke"]) or EN_PHRASE.search(r["soninke"]):
            erreurs.append(f"expressions: anglais dans soninke « {r['soninke']} »")
        if est_anglais(r["francais"]):
            erreurs.append(
                f"expressions: anglais dans « {r['soninke']} » → « {r['francais']} »"
            )
        if cle_soninkegpt(r["soninke"]) in connues:
            erreurs.append(f"expressions: doublon lexique base « {r['soninke']} »")

    for nom, rows in (("mots", mots), ("expressions", expressions)):
        seen: set[str] = set()
        for r in rows:
            k = cle_soninkegpt(r["soninke"])
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
    print(
        f"renvois sans glose : {len(renvois)} | exclusions anglaises : "
        f"{len(exclusions_ang)}"
    )
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
