#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrait les entrées (mot soninké / glose française) d'un dictionnaire soninké.

Entrée acceptée :
  - le texte exporté d'un Google Doc   (Fichier ▸ Télécharger ▸ Texte brut .txt)
  - un .docx Word                      (lecture directe, sans dépendance externe)

Sortie : CSV « soninke;francais;categorie;glose_complete;note ».

Usage :
    python3 scripts/extract_dictionnaire_soninke.py ENTREE.txt SORTIE.csv
    python3 scripts/extract_dictionnaire_soninke.py "Dictionnaire soninké.docx" SORTIE.csv

Le script ne fabrique aucune traduction : il sépare la glose anglaise de la
glose française déjà présentes dans la source, et signale les entrées dont la
part française n'a pas pu être isolée proprement (colonne glose_complete=non).
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

# ---------------------------------------------------------------- lecture ---

def read_docx(path: Path) -> str:
    """Texte d'un .docx, un paragraphe par ligne (sans dépendance externe)."""
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8")
    xml = re.sub(r"<w:br[^>]*/>", "\n", xml)
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<w:tab[^>]*/>", "\t", xml)
    # une entrée = un paragraphe ; les runs <w:t> sont concaténés
    out = []
    for para in xml.split("\n"):
        texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", para, flags=re.S)
        line = "".join(texts)
        line = (line.replace("&amp;", "&").replace("&lt;", "<")
                    .replace("&gt;", ">").replace("&quot;", '"')
                    .replace("&apos;", "'"))
        out.append(line)
    return "\n".join(out)


def read_any(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    return path.read_text(encoding="utf-8-sig")


# ------------------------------------------------------------- découpage ---

# « baabo1   Nom . foam; mousse, écume. Baabon wa xatin kanma… »
ENTRY_RE = re.compile(r"^(?P<mot>[-A-Za-zÀ-ÿɓɗƴŋɲɓɛɔ'’\- ]{1,40}?)\s{2,}(?P<corps>\S.*)$")

CATEGORIES = {
    "nom": "nom", "verbe": "verbe", "adjectif": "adjectif", "adverbe": "adverbe",
    "pronom": "pronom", "proforme": "proforme", "postposition": "postposition",
    "préposition": "préposition", "conjonction": "conjonction", "particule": "particule",
    "nombre": "nombre", "nom propre": "nom propre", "interjection": "interjection", "déterminant": "déterminant",
}

FR_STOP = {
    "le", "la", "les", "un", "une", "des", "du", "de", "au", "aux", "ce", "cette",
    "ces", "son", "sa", "ses", "leur", "qui", "que", "dont", "où", "pour", "avec",
    "dans", "sur", "sous", "par", "être", "faire", "fait", "se", "s'", "ne", "pas",
    "ou", "et", "en", "à", "très", "plus", "personne", "chose", "sorte", "variété",
    "arbre", "animal", "enfant", "femme", "homme", "celui", "celle", "chacun",
}
EN_STOP = {
    "the", "a", "an", "of", "to", "with", "and", "one", "be", "is", "are", "not",
    "person", "that", "this", "his", "her", "its", "they", "you", "we", "it", "in",
    "on", "for", "from", "which", "who", "some", "make", "cause", "something",
}


def has_french_accents(seg: str) -> bool:
    return any(ch in seg for ch in "àâäéèêëîïôöùûüçœæÀÂÄÉÈÊËÎÏÔÖÙÛÜÇŒÆ")


def words(seg: str) -> list[str]:
    seg = unicodedata.normalize("NFC", seg.lower())
    return re.findall(r"[a-zà-ÿ']+", seg)


def score(seg: str) -> int:
    """> 0 : plutôt français ; < 0 : plutôt anglais."""
    ws = words(seg)
    if not ws:
        return 0
    fr = sum(1 for w in ws if w in FR_STOP) + 2 * has_french_accents(seg)
    en = sum(1 for w in ws if w in EN_STOP)
    return fr - en


META = re.compile(r"\b(?:Gram|Note|Plural suffix|Underlying form|Category|synonyme|"
                  r"similaire|comp|compare|tone|See main entry|Anth|Disc|"
                  r"Verbal suffix form|Variant)\b")
EXEMPLE = re.compile(r"\.\s+(?=[A-ZÀ-Ý«\"])")


def _sans_exemple(txt: str) -> str:
    """Coupe la glose avant la première phrase d'exemple."""
    return EXEMPLE.split(txt, maxsplit=1)[0]


def clean_gloss(corps: str) -> tuple[str, bool]:
    """Renvoie (glose française, glose_complete)."""
    txt = re.sub(r"^\s*summary-definition:\s*", "", corps.strip())
    # 1. découper les sens numérotés AVANT de couper les métadonnées,
    #    car chaque sens peut se terminer par ses propres notes.
    sens = re.split(r"(?:^|\s)\d+\s*[•·]\s*", " " + txt)
    gloses, complet = [], True
    for sens_txt in sens:
        # 2. retirer les métadonnées de fin d'entrée
        sens_txt = META.split(sens_txt, maxsplit=1)[0]
        # 3. retirer la catégorie grammaticale de tête
        sens_txt = re.sub(r"^\s*[A-Za-zÀ-ÿ\-]+(?:\s+(?:transitif|intransitif|"
                          r"causatif|causitif|passif|qualificatif|d'état|nominal|"
                          r"verbal|comparatif|cardinal))*\s*\.\s*", "",
                          sens_txt.strip(), count=1)
        # 4. couper avant la première phrase d'exemple
        sens_txt = _sans_exemple(sens_txt).strip(" .")
        if not sens_txt or sens_txt.lower() in CATEGORIES:
            continue
        parts = [x.strip(" .") for x in sens_txt.split(";") if x.strip(" .")]
        if not parts:
            continue
        fr_parts = [x for x in parts if score(x) >= 2]
        if fr_parts:
            if any(score(x) < 0 for x in parts[parts.index(fr_parts[0]) + 1:]):
                complet = False
            gloses.append("; ".join(fr_parts))
        elif len(parts) >= 2 and not any(score(x) < 0 for x in [parts[-1]]):
            gloses.append(parts[-1])      # la glose finale suit l'anglaise
        else:
            gloses.append(parts[-1])
            complet = False
    return " / ".join(gloses), complet


def categorie(corps: str) -> str:
    tete = corps
    m = re.search(r"\b(Nom Propre|Nom|Verbe|Adjectif|Adverbe|Pronom|Proforme|"
                  r"Postposition|Préposition|Conjonction|Particule|Interjection|"
                  r"Déterminant|Nombre cardinal)\b", tete)
    if not m:
        return ""
    return CATEGORIES.get(m.group(1).lower().replace("nom propre", "nom propre"),
                          m.group(1).lower())


# ------------------------------------------------------------------ main ---

SUITE = re.compile(r"^\s*\d+\s*[•·]\s*\S")


def extraire(texte: str):
    vus = set()
    courant = None          # [mot, corps, note]
    for brute in texte.splitlines():
        if SUITE.match(brute.replace("\u00a0", " ")) and courant is not None:
            courant[1] += " " + brute.strip()
            continue
        if courant is not None:
            yield from _emit(courant, vus)
            courant = None
        ligne = brute.replace("\u00a0", " ").rstrip()
        if not ligne.strip():
            continue
        m = ENTRY_RE.match(ligne)
        if not m:
            continue
        mot = m.group("mot").strip()
        corps = m.group("corps").strip()
        if not mot or not corps:
            continue
        courant = [mot, corps]
    if courant is not None:
        yield from _emit(courant, vus)


def _emit(courant, vus):
    mot, corps = courant[0], courant[1].strip()
    fr, complet = clean_gloss(corps)
    cle = (mot, corps)
    if cle in vus:              # le document contient des entrées dupliquées
        return
    vus.add(cle)
    note = ""
    if "See main entry" in corps:
        note = "renvoi"
    elif "Variant" in corps:
        note = "variante"
    yield {
        "soninke": mot,
        "francais": fr,
        "categorie": categorie(corps),
        "glose_complete": "oui" if complet else "a_verifier",
        "note": note,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    src, dst = Path(argv[1]), Path(argv[2])
    texte = read_any(src)
    lignes = list(extraire(texte))
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["soninke", "francais", "categorie",
                                           "glose_complete", "note"], delimiter=";")
        w.writeheader()
        w.writerows(lignes)
    ok = sum(1 for x in lignes if x["glose_complete"] == "oui")
    print(f"{len(lignes)} entrées écrites dans {dst} "
          f"({ok} gloses françaises isolées avec certitude, "
          f"{len(lignes) - ok} à vérifier)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
