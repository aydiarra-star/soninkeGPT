#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nettoie les entrées d–f du dictionnaire, dédoublonne et intègre le lexique base.

Pipeline (exécuté depuis la racine du dépôt) :
  1. nettoyage des candidats `dictionnaire-d-f-nouveaux-2026-10-25.csv`
     (chiffres retirés des formes soninkées, anglais remplacé/retiré,
     ponctuation parasite et résidus d'exemple éliminés, catégories déduites
     de la source, variantes documentées repositionnées) ;
  2. fusion des sens complémentaires des doublons listés dans
     `comparaison-dictionnaire-d-f-2026-10-25.csv` (43 lignes) ;
  3. corrections de deux entrées existantes contenant de l'anglais
     (bula, billati — équivalents français tirés de leur propre colonne
     `definition`) ;
  4. écriture du lexique enrichi + rapports.

Aucune ligne existante n'est supprimée ; aucune traduction n'est inventée :
les équivalents anglais→français viennent du dictionnaire source ou sont des
équivalents standard consignés dans le rapport de vérification.

Sorties :
  data/source/lexique-soninke-fr-base.csv                 (enrichi)
  data/candidates/dictionnaire-d-f-nettoyes-2026-10-25.csv
  data/reports/nettoyage-integration-dictionnaire-d-f-2026-10-25.csv
  data/reports/verification-dictionnaire-d-f-2026-10-25.csv
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from import_extraction_sans_doublons import cle, charger_lexique, normaliser_glose
from extract_dictionnaire_soninke import ENTRY_RE

LEXIQUE = Path("data/source/lexique-soninke-fr-base.csv")
CANDIDATS = Path("data/candidates/dictionnaire-d-f-nouveaux-2026-10-25.csv")
EXTRACTION = Path("data/candidates/dictionnaire-d-f-extraction-2026-10-25.csv")
COMPARAISON = Path("data/reports/comparaison-dictionnaire-d-f-2026-10-25.csv")
BRUT = Path("data/source/dictionnaire-d-f-brut-2026-10-25.txt")
NETTOYES = Path("data/candidates/dictionnaire-d-f-nettoyes-2026-10-25.csv")
RAPPORT = Path("data/reports/nettoyage-integration-dictionnaire-d-f-2026-10-25.csv")
VERIF = Path("data/reports/verification-dictionnaire-d-f-2026-10-25.csv")

CHAMPS = ["id", "soninke", "francais", "categorie", "source", "statut",
          "variantes", "exemple_original", "definition", "definition_statut"]
SOURCE_D_F = "Dictionnaire soninké.docx (Google Doc d–f) 2026-10-25"
STATUT_NOUVEAU = "candidat_dictionnaire_a_verifier"

# ---------------------------------------------------------------- surcharges #
# Décisions manuelles documentées : glose finale établie sur la source brute
# (pas d'invention — chaque équivalent est consigné dans le rapport).
OVERRIDES_FR = {
    "daaxa1": "campement, lieu habituel de séjour",
    "dagandi": "légaliser, permettre, admettre (dans la religion)",
    "dakka": "provoquer à la lutte; défier / tumulte, vacarme, brouhaha",
    "daro": "être gros / être fier / respecter, bien accueillir",
    "Fanka Senne": "Saint-Esprit",
    "fanke": "vent, air / épidémie / enflure / méningite",
    "fanqa": "terrasser, vaincre / lutter",
    "fana1": "entourer, enrouler / premier",
    "fari xoore": "mule / mulet",
    "fariganka": "à sang chaud",
    "feriganka": "à sang chaud",
    "faxa": 'fonctionne comme marque de l\'aspect embarquatif: "venir de faire..."',
    "fatemulle": "un innocent",
    "fuxu-fuxu": "bruiner",
    "fallamaxankure": "embusqué",
    "Furaata": "Euphrate",
    "Enoosi": "Enos",
    "-dun": '"à l\'intérieur de" (affixe connectif des noms composés)',
    # doublons de l'extraction (côté document, fondus ensuite)
    "fanqe": "lutter / lutte",
    "do": "et, avec, par, pour / dans, à / à propos de",
    "fate2": "cueillir, séparer, divorce, sevrer",
}
COMMENTAIRES_OVERRIDE = {
    "daaxa1": "segment anglais « to camp » retiré (glose française conservée)",
    "dagandi": "anglais et doublon retirés, catégorie « verbe causitif » retirée du champ glose",
    "dakka": "marqueur d'incertitude ???? retiré",
    "daro": "résumé anglais retiré, sens français conservés",
    "Fanka Senne": "« Holy Spirit » → équivalent exact « Saint-Esprit »",
    "fanke": "exemple anglais retiré, sens français conservés",
    "fanqa": "« wrestle » → « lutter » (confirmé par fanqaana « lutteur »)",
    "fana1": "sens anglais « first » retiré (« premier » présent), marqueur « Nombre ordinal. » retiré",
    "fari xoore": "« mule; mullet » → « mule / mulet » (mullet = mulet, mule déjà français)",
    "fariganka": "« warm blooded » → « à sang chaud »",
    "feriganka": "« warm-blooded » → « à sang chaud »",
    "faxa": "définition anglaise remplacée par la glose française de la source",
    "fatemulle": "glose française de la source « un innocent » (anglais « innocent person » retiré)",
    "fuxu-fuxu": "« drizzle (rain) » → « bruiner » (verbe intransitif, source)",
    "fallamaxankure": "« ambusher » → « embusqué »",
    "Furaata": "forme française standard « Euphrate »",
    "Enoosi": "forme française bibliographique « Enos »",
    "-dun": "glose française de source conservée, exemples illustratifs (EN+FR) retirés",
    "fanqe": "sens « lutter / lutte » séparés (listes source sans séparateur)",
    "do": "sens anglais « with » couvert par « avec », « about » → « à propos de »",
    "fate2": "liste source sans séparateur : ponctuation rétablie, sens uniques conservés",
}

# variantes documentées à repositionner (filtrées contre les collisions)
VARIANTES_CUREES = {
    "dooke": ["doono", "doore", "dooru"],
    "deni": ["denne", "denŋe"],
    "dudoxoto": ["duroxoto", "duruxoto", "duudoxoto"],
    "fanqalelle": ["fankalalle", "fankaleele", "fanqalaane"],
    "fanti": ["pande", "pandi", "panti"],
    "folo": ["falo", "folonŋe"],
    "danŋa": ["da", "daŋa"],
    "fuxu-fuxu": ["fuxu-fuqu"],
}

# catégorie déduite de la source brute uniquement (libellés source)
CATEGORIES_SOURCE = {
    "dagandi": "verbe", "dan": "pronom", "dara": "attributif", "deele": "verbe",
    "digindi": "verbe", "dugundi": "verbe", "faama": "prédicatif_verbal",
    "fadumanta": "attributif", "fagu": "verbe", "fatandi": "verbe",
    "faxa": "prédicatif_verbal", "fe": "auxiliaire_existentiel",
    "feedandi": "verbe", "feti": "copule", "fillandi": "nombre",
    # dalle, fala : aucune catégorie dans la source → champ laissé vide
}

# entrées existantes du lexique contenant de l'anglais/des balises → équivalent
# français tiré de leur propre colonne definition (source interne, pas inventé)
CORRECTIONS_LEXIQUE = {
    "bula": "bleu / poudre bleue pour maintenir la couleur indigo / "
            "titre honorifique accolé à certains patronymes",
    "billati": "surtout, à plus forte raison, encore moins",
}

# ------------------------------------------------------------------ nettoyage #

MARQUEURS_EDITORIAUX = [
    r"\bSee main entry\s*:\s*[^.;]*[.;]?",
    r"\bVariant\s*:\s*[^.;]*[.;]?",
    r"\bNote\s*:\s*[^.;]*[.;]?",
    r"\bcompare\s*:\s*[^.;]*[.;]?",
    r"\bsummary[- ]definition\s*:\s*",
    r"\bSource\s*:\s*[^.;]*[.;]?",
    r"\b(?:Gram|Category|synonyme|similaire|tone|Anth|Disc|"
    r"Underlying form|Plural suffix|Verbal suffix form)\s*:\s*[^.;]*[.;]?",
    r"\bidiom\s*:\s*\S+",
]
# Étiquette de catégorie en tête de segment : le point est OBLIGATOIRE
# (« Nom . »), sinon on tronquerait de vraies gloses comme
# « pronom réfléchi complément: me, te… » ou « copule de négation… ».
CATEGORIES_SEGMENT = re.compile(
    r"^(?:Nombre ordinal|verbe (?:causitif|antipassif|passif|transitif|intransitif)|"
    r"Nom|Adverbe|Adjectif|Postposition|Préposition|Conjonction|Pronom|Particule|"
    r"Copule|Prédicatif verbal|Attributif)\s*\.\s*", re.I)
# Résidus d'exemple : coupés APRÈS le point (« décrue. Ŋaamen… ») ou entre
# une parenthèse fermante et une majuscule collée (« etc.)Sanba wa… ») —
# la parenthèse fermante est conservée (ponctuation utile).
EXEMPLE_COUPE = re.compile(r"\.(?=\s*(?:[A-ZÀ-Ý«\"ŊƝƁƊƳ]))|"
                            r"(?<=\))(?=\s*[A-ZÀ-Ý«\"ŊƝ])")
JUNK_PUNCT = re.compile(r"\s*[.!?]*\s*[?!]{2,}\s*|\s*\.{4,}\s*|…")
JUNK_DOTS = re.compile(r"(?<![A-Za-zÀ-ÿ])\.{3,}(?![A-Za-zÀ-ÿ])")

EN_FORTE = {"the", "of", "title", "honor", "attached", "family", "names", "wrestle",
            "drizzle", "ambusher", "holy", "spirit", "warm", "blooded", "mullet",
            "legalize", "permit", "justify", "camp", "transitive", "intransitive",
            "functions", "function", "marker", "pleased", "someone", "something",
            "first", "wrestling", "wrapping", "see", "entry", "variant"}
EN_FAIBLE = {"a", "an", "the", "of", "to", "with", "and", "is", "are", "be", "have",
             "has", "was", "were", "this", "that", "his", "her", "their", "you",
             "they", "not", "from", "for", "on", "in", "at", "by", "or", "as",
             "but", "if", "just", "done", "word", "wind", "take", "went", "about",
             "keep", "one", "its", "it", "we", "he", "she"}
FR_STOP = {"le", "la", "les", "un", "une", "des", "du", "de", "au", "aux", "ce",
           "cette", "ces", "son", "sa", "ses", "leur", "qui", "que", "dont", "où",
           "pour", "avec", "dans", "sur", "sous", "par", "être", "faire", "fait",
           "se", "s'", "ne", "pas", "ou", "et", "en", "à", "très", "plus",
           "personne", "chose", "sorte", "variété", "arbre", "animal", "enfant",
           "femme", "homme", "celui", "celle", "chacun", "aussi", "entre",
           "depuis", "vers", "chez", "sans", "surtout", "est"}


def _mots(seg: str) -> list[str]:
    return re.findall(r"[a-zà-ÿ']+", seg.lower())


def est_anglais(seg: str) -> bool:
    ws = _mots(seg)
    fort = sum(1 for w in ws if w in EN_FORTE)
    faible = sum(1 for w in ws if w in EN_FAIBLE)
    fr = sum(1 for w in ws if w in FR_STOP)
    if any(c in seg for c in "àâäéèêëîïôöùûüçœæ"):
        fr += 2
    if fort >= 1 and faible + fort > fr:
        return True
    # segment d'un seul mot : mot anglais sans équivalent français possible
    if len(ws) == 1 and len(ws[0]) > 2:
        return (ws[0] in EN_FORTE or ws[0] in EN_FAIBLE) and \
               ws[0] not in FR_STOP and fr == 0
    return faible >= 3 and faible > fr


def segments(fr: str) -> list[str]:
    return [s.strip() for s in re.split(r"\s+/\s+", fr) if s.strip()]


def nettoyer_fr(fr: str, journal: list, entite: str) -> str | None:
    """Nettoie une glose. Renvoie None si aucune traduction française n'est
    publiable (aucun segment français restant)."""
    if not fr or not fr.strip():
        return None
    out = []
    for seg in segments(fr):
        orig = seg
        # 1. marqueurs éditoriaux et étiquettes de catégorie en tête
        for pat in MARQUEURS_EDITORIAUX:
            seg = re.sub(pat, "", seg, flags=re.I)
        seg = CATEGORIES_SEGMENT.sub("", seg)
        # 2. résidus d'exemple collés (point/majuscule, parenthèse/majuscule)
        seg = EXEMPLE_COUPE.split(seg, maxsplit=1)[0]
        # 3. ponctuation parasite
        seg = JUNK_PUNCT.sub(" ", seg)
        seg = JUNK_DOTS.sub(" ", seg)
        # 4. anglais : équivalent exact connu ailleurs, sinon retrait si du
        #    français subsiste dans l'entrée (sinon la ligne est mise en attente)
        cle_seg = normaliser_glose(seg)
        if est_anglais(seg):
            journal.append(("anglais_retire", entite, "francais", orig.strip(), "",
                            "segment sans équivalent retenu"))
            continue
        # 5. nettoyage de bord
        seg = seg.strip(" \t,;:.")
        if not seg:
            continue
        out.append((seg, normaliser_glose(seg)))
    # 6. répétitions strictement identiques + sens redondant déjà présent
    #    dans un sens plus complet de la même entrée (item de liste)
    def wn(k: str) -> str:
        return " ".join(t.rstrip("s") for t in k.split())

    def items(seg: str) -> set[str]:
        parts = re.split(r"[,;(«»\"]+", seg)
        return {wn(normaliser_glose(p)) for p in parts if normaliser_glose(p)}

    finales: list[tuple[str, str]] = []
    vus = set()
    for seg, k in out:
        if k in vus:
            journal.append(("sens_duplique_retire", entite, "francais", seg, "",
                            "répétition strictement identique"))
            continue
        vus.add(k)
        finales.append((seg, k))
    gardes: list[tuple[str, str]] = []
    for seg, k in finales:
        w = wn(k)
        autres = [(s2, k2) for s2, k2 in finales if k2 != k]
        if w and any(w in items(s2) for s2, _ in autres):
            journal.append(("sens_couvert_retire", entite, "francais", seg, "",
                            "sens déjà présent dans un sens plus complet de l'entrée"))
            continue
        gardes.append((seg, k))
    resultat = " / ".join(s for s, _ in gardes) if gardes else None
    if resultat != fr and resultat is not None:
        journal.append(("glose_nettoyee", entite, "francais", fr, resultat, ""))
    return resultat


def lire_brut() -> dict[str, str]:
    """headword exact → ligne source complète (première occurrence)."""
    lignes: dict[str, str] = {}
    for ligne in BRUT.read_text(encoding="utf-8-sig").splitlines():
        m = ENTRY_RE.match(ligne)
        if m and m.group("mot").strip():
            lignes.setdefault(m.group("mot").strip(), ligne.rstrip())
    return lignes


def tokens_fr(seg: str) -> set[str]:
    return {t.rstrip("s") for t in normaliser_glose(seg).split() if t}


def _wn(seg: str) -> str:
    """Forme normalisée d'un sens pour comparaison (casse, tons, pluriels)."""
    return " ".join(t.rstrip("s") for t in normaliser_glose(seg).split())


def _items(seg: str) -> set[str]:
    """Sens décomposé en éléments de liste (virgules, parenthèses)."""
    parts = re.split(r"[,;(«»\"]+", seg)
    return {_wn(p) for p in parts if normaliser_glose(p)}


def fusionner(existant: str, nouveau: str, entite: str, journal: list) -> tuple[str, str]:
    """Fusionne les sens d'un doublon dans la glose existante.

    Règles (jamais de perte d'information) :
      - égalité normalisée            → sens nouveau déjà couvert (identique) ;
      - E est un élément de liste de N, ou N commence par E → E enrichi par N ;
      - N est un élément de liste de E (ou commence par E)   → N déjà couvert ;
      - sinon                          → N ajouté (sens complémentaire).

    Renvoie (glose finale, classement) : identique | fusionne | enrichi | mixte.
    """
    sens_ex = [(s.strip(), s.strip()) for s in segments(existant)]
    sens_nv = [s.strip() for s in segments(nouveau) if s.strip()]
    resultats = list(sens_ex)
    classes = set()
    for seg in sens_nv:
        wn_n = _wn(seg)
        if any(wn_n == _wn(e) for e, _ in resultats):
            classes.add("identique")
            continue
        items_n = _items(seg)
        remplace = False
        for i, (e, _) in enumerate(resultats):
            wn_e = _wn(e)
            if wn_e and (wn_e in items_n or wn_n.startswith(wn_e + " ")):
                resultats[i] = (seg, seg)
                journal.append(("sens_enrichi", entite, "francais", e, seg,
                                "sens existant conservé dans une forme plus complète"))
                classes.add("enrichi")
                remplace = True
                break
        if remplace:
            continue
        if any(wn_n and (wn_n in _items(e) or _wn(e).startswith(wn_n + " "))
               for e, _ in resultats):
            classes.add("identique")                # nouveau déjà couvert
            continue
        resultats.append((seg, seg))
        journal.append(("sens_fusionne", entite, "francais", "", seg,
                        "sens complémentaire ajouté à l'entrée existante"))
        classes.add("fusionne")
    fin = " / ".join(e for e, _ in resultats)
    if fin == existant:
        classes.add("identique")
    if "fusionne" in classes or "enrichi" in classes:
        classe = "+".join(sorted(c for c in classes if c != "identique")) or "fusionne"
    else:
        classe = "identique"
    return fin, classe


def main() -> int:
    journal: list[tuple] = []
    verif: list[tuple] = []

    brut = lire_brut()
    lignes_lex, connues = charger_lexique()
    with COMPARAISON.open(encoding="utf-8", newline="") as fh:
        comparaison = list(csv.DictReader(fh, delimiter=";"))
    with CANDIDATS.open(encoding="utf-8", newline="") as fh:
        candidats = list(csv.DictReader(fh, delimiter=";"))

    # formes tête du lexique FINAL (base + lot nettoyé) pour filtrer les
    # variantes : fuxu-fuqu n'existera pas comme tête (conservé en variante)
    tetes_finales = set(connues) | {
        cle(re.sub(r"\d+", "", (l.get("soninke") or "").strip()))
        for l in candidats
        if re.sub(r"\d+", "", (l.get("soninke") or "").strip()) != "fuxu-fuqu"
    }

    # ---------------------------------------------------------- 1. nettoyage --
    nettoyes: list[dict] = []
    variantes_a_conserver: dict[str, list[str]] = {}
    vus_internes: dict[str, str] = {}
    echanges = 0
    for ligne in candidats:
        mot_brut = (ligne["soninke"] or "").strip()
        fr_brut = (ligne.get("francais") or "").strip()
        # A. chiffres retirés de la forme soninkée uniquement
        mot = re.sub(r"\d+", "", mot_brut)
        if mot != mot_brut:
            journal.append(("chiffres_retires", mot_brut, "soninke", mot_brut, mot,
                            "marqueur d'homonyme retiré de la forme affichée"))
        # fuxu-fuqu : variante orthographique documentée de fuxu-fuxu
        if mot == "fuxu-fuqu":
            journal.append(("variante_repositionnee", mot, "variantes", fr_brut, "",
                            "variante documentée de fuxu-fuxu (voir fuxu-fuxu)"))
            verif.append(("variante_conservee", "fuxu-fuqu → fuxu-fuxu", fr_brut, "bruiner",
                          "variante orthographique documentée, non dupliquée"))
            continue
        fr = OVERRIDES_FR.get(mot_brut, OVERRIDES_FR.get(mot, fr_brut))
        cle_surcharge = mot_brut if mot_brut in OVERRIDES_FR else (
            mot if mot in OVERRIDES_FR else None)
        if cle_surcharge is not None:
            journal.append(("surcharge", mot, "francais", fr_brut, fr,
                            COMMENTAIRES_OVERRIDE.get(cle_surcharge, "")))
            if est_anglais(fr) or re.search(r"\b(?:to|the|of)\b", fr):
                verif.append(("glose_a_verifier", mot, fr_brut, fr,
                              COMMENTAIRES_OVERRIDE.get(cle_surcharge, "")))
        else:
            fr = nettoyer_fr(fr, journal, mot)
        if not fr:
            verif.append(("sans_glose_fr", mot, fr_brut, "",
                          "aucune traduction française publiable → non intégré"))
            continue
        cat = (ligne.get("categorie") or "").strip()
        if not cat:
            cat = CATEGORIES_SOURCE.get(mot, "")
            if cat:
                journal.append(("categorie_deduite", mot, "categorie", "", cat,
                                "libellé déduit de la source brute"))
        # variantes documentées, sans collision avec une forme tête du lexique final
        vars_mot: list[str] = []
        for v in VARIANTES_CUREES.get(mot, []):
            v = re.sub(r"\d+", "", v.strip())
            if v and cle(v) != cle(mot) and cle(v) not in tetes_finales:
                vars_mot.append(v)
            elif v and cle(v) in tetes_finales and cle(v) != cle(mot):
                journal.append(("variante_ecartee_collision", mot, "variantes", v, "",
                                "forme déjà utilisée comme tête de lexique"))
        if vars_mot:
            variantes_a_conserver[mot] = vars_mot
            journal.append(("variante_repositionnee", mot, "variantes", "",
                            ", ".join(vars_mot), "liste Variant: de la source"))
            verif.append(("variante_conservee", mot, "", "", 
                          f"variantes documentées : {', '.join(vars_mot)}"))
        # contrôle interne (formes identiques après normalisation)
        k = cle(mot)
        if k in vus_internes:
            journal.append(("doublon_interne_ecarte", mot, "soninke", mot,
                            vus_internes[k], "même forme normalisée dans le lot"))
            continue
        vus_internes[k] = mot
        # doublon avec le lexique → route fusion (ne devrait pas arriver : 0 fuite)
        if k in connues:
            journal.append(("doublon_lexique_route_fusion", mot, "soninke", mot,
                            connues[k]["id"], "classé côté comparaison"))
        brut_ligne = brut.get(mot_brut) or brut.get(mot) or ""
        if ligne.get("glose_complete") != "oui":
            verif.append(("glose_a_verifier", mot, fr_brut, fr,
                          "glose isolée avec incertitude par l'extraction"))
        nettoyes.append({
            "soninke": mot, "francais": fr, "categorie": cat,
            "glose_complete": ligne.get("glose_complete") or "",
            "note": ligne.get("note") or "",
            "variantes": ", ".join(vars_mot),
            "exemple_original": f"{mot_brut} {brut_ligne.split(mot_brut, 1)[1].strip()}"
                                if brut_ligne.startswith(mot_brut) else brut_ligne,
        })
        echanges += 1

    # ------------------------------------------------- 2. doublons (43) -----
    extraction_fr: dict[str, str] = {}
    with EXTRACTION.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            extraction_fr.setdefault((r["soninke"] or "").strip(),
                                     (r.get("francais") or "").strip())
    cles_traitees: set[tuple[str, str]] = set()
    gloses_maj: dict[str, str] = {}          # id → glose mise à jour par fusion
    fusions = {"identique": 0, "fusionne": 0, "enrichi": 0}
    for r in comparaison:
        if not r["resultat"].startswith("doublon_ecarte"):
            continue
        mot = (r["soninke"] or "").strip()
        k = cle(mot)
        fr_doc = r["francais"].strip() or extraction_fr.get(mot, "")
        # nettoyage côté document (journal différé jusqu'après dédoublonnage)
        cle_surcharge = mot if mot in OVERRIDES_FR else None
        journal_differe: list[tuple] = []
        if cle_surcharge is not None:
            fr_doc_net = OVERRIDES_FR[cle_surcharge]
            journal_differe.append(("surcharge", mot, "francais", fr_doc, fr_doc_net,
                                    COMMENTAIRES_OVERRIDE.get(cle_surcharge, "")))
        else:
            fr_doc_net = nettoyer_fr(fr_doc, journal_differe, mot)
        if not fr_doc_net:
            journal.append(("doublon_sans_glose_nettoyee", mot, "francais", fr_doc, "",
                            "aucune glose française publiable côté document"))
            continue
        # homonymes da1/da2/da3… : traités s'ils portent des gloses différentes ;
        # simples répétitions (même clé + même glose) ignorées
        paire = (k, normaliser_glose(fr_doc_net))
        if paire in cles_traitees:
            continue
        cles_traitees.add(paire)
        journal.extend(journal_differe)
        existant_row = connues[k]
        existant = gloses_maj.get(existant_row["id"], existant_row["francais"])
        fin, classe = fusionner(existant, fr_doc_net, mot, journal)
        if classe == "identique":
            journal.append(("doublon_ecarte_glose_identique", mot, "francais",
                            fr_doc_net, "", f"identique à {existant_row['id']}"))
            fusions["identique"] += 1
            continue
        # écriture dans la ligne existante
        gloses_maj[existant_row["id"]] = fin
        for row in lignes_lex:
            if row["id"] == existant_row["id"]:
                row["francais"] = fin
                if SOURCE_D_F not in row["source"]:
                    row["source"] = f"{row['source']}; {SOURCE_D_F}"
                if "candidat_dictionnaire_a_verifier" not in row["statut"]:
                    row["statut"] = f"{row['statut']};candidat_dictionnaire_a_verifier"
                break
        journal.append((f"doublon_fusionne_{classe}", mot, "francais", existant, fin,
                        f"{existant_row['id']} — sens du document fusionnés"))
        fusions["fusionne" if classe == "fusionne" else "enrichi"] += 1

    # ---------------------------------- 3. corrections du lexique existant ----
    for mot, fr_corr in CORRECTIONS_LEXIQUE.items():
        for row in lignes_lex:
            if row["soninke"] == mot:
                journal.append(("correction_lexique", mot, "francais", row["francais"],
                                fr_corr,
                                "anglais/balises remplacés par l'équivalent français "
                                "de la colonne definition"))
                row["francais"] = fr_corr
                break

    # ------------------------------------------------ 4. ajouts des nouveaux --
    nums = [int(m.group(1)) for r in lignes_lex
            if (m := re.match(r"SNK-LEX-(\d+)$", r["id"]))]
    numero = max(nums) + 1
    ajoutes = 0
    for c in nettoyes:
        # collision finale (headword ou variante déjà présent) → fusion de sécurité
        k = cle(c["soninke"])
        if k in connues:
            existant_row = connues[k]
            fin, classe = fusionner(existant_row["francais"], c["francais"],
                                    c["soninke"], journal)
            for row in lignes_lex:
                if row["id"] == existant_row["id"]:
                    row["francais"] = fin
                    if SOURCE_D_F not in row["source"]:
                        row["source"] = f"{row['source']}; {SOURCE_D_F}"
                    if "candidat_dictionnaire_a_verifier" not in row["statut"]:
                        row["statut"] = (f"{row['statut']};"
                                         "candidat_dictionnaire_a_verifier")
                    break
            journal.append((f"doublon_fusionne_{classe}", c["soninke"], "francais",
                            existant_row["francais"], fin,
                            f"{existant_row['id']} — collision détectée à l'ajout"))
            fusions["fusionne" if classe == "fusionne" else "enrichi"] += 1
            continue
        # variantes : exclure toute collision avec une forme tête du lexique final
        vv = [v for v in (c["variantes"].split(", ") if c["variantes"] else [])
              if cle(v) not in tetes_finales]
        c["variantes"] = ", ".join(vv)
        lignes_lex.append({
            "id": f"SNK-LEX-{numero:04d}",
            "soninke": c["soninke"],
            "francais": c["francais"],
            "categorie": c["categorie"],
            "source": SOURCE_D_F,
            "statut": STATUT_NOUVEAU,
            "variantes": c["variantes"],
            "exemple_original": c["exemple_original"],
            "definition": "",
            "definition_statut": "",
        })
        vus_internes[k] = c["soninke"]
        numero += 1
        ajoutes += 1

    # ------------------------------------------------------------- écritures --
    with LEXIQUE.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CHAMPS, delimiter=";",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(lignes_lex)

    NETTOYES.parent.mkdir(parents=True, exist_ok=True)
    with NETTOYES.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["soninke", "francais", "categorie",
                                           "glose_complete", "note", "variantes",
                                           "exemple_original"],
                           delimiter=";", lineterminator="\n")
        w.writeheader()
        w.writerows(nettoyes)

    for p, rows, head in (
        (RAPPORT, journal, ["action", "entite", "champ", "avant", "apres", "commentaire"]),
        (VERIF, verif, ["type", "entite", "francais_source", "francais_publie", "commentaire"]),
    ):
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, delimiter=";", lineterminator="\n")
            w.writerow(head)
            w.writerows(rows)

    print(f"candidats lus : {len(candidats)} | nettoyés/intégrables : {len(nettoyes)} "
          f"| ajoutés : {ajoutes}")
    print(f"doublons d–f traités : {len(cles_traitees)} uniques — "
          f"identiques écartés : {fusions['identique']} | "
          f"sens fusionnés : {fusions['fusionne']} | sens enrichis : {fusions['enrichi']}")
    print(f"lexique final : {len(lignes_lex)} lignes → {LEXIQUE}")
    print(f"rapport : {RAPPORT}")
    print(f"vérification : {VERIF}")
    print(f"nettoyés : {NETTOYES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
