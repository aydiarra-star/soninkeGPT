#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extraction et classement du lexique « parties du corps humain » du document Google.

Source : https://docs.google.com/document/d/19WQjG-JziayBdtVkI8WUeh0_b1FLHH-cYt0fwt7fgpA/edit

Le script ne modifie jamais `data/source/lexique-soninke-fr-base.csv`. Il écrit :
  - data/candidates/parties-du-corps-doc-google-2026-10-24.csv
  - data/source/reports/extraction-parties-corps-doc-2026-10-24.md

Toute forme est conservée séparément : aucune fusion, aucune normalisation
orthographique, aucune traduction ajoutée. Les variantes d'une même ligne
source restent des lignes distinctes.
"""

from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_CSV = ROOT / "data" / "source" / "lexique-soninke-fr-base.csv"
OUT_CSV = ROOT / "data" / "candidates" / "parties-du-corps-doc-google-2026-10-24.csv"
OUT_MD = ROOT / "data" / "source" / "reports" / "extraction-parties-corps-doc-2026-10-24.md"

DOC_URL = (
    "https://docs.google.com/document/d/19WQjG-JziayBdtVkI8WUeh0_b1FLHH-cYt0fwt7fgpA/edit"
)
SOURCE_ID = "doc_google_parties_du_corps_2026-10-24"
DATE = "2026-10-24"

# (numéro, titre de section, [(français, [forme soninké, ...]), ...])
SECTIONS = [
    (
        1,
        "La tête et le visage (Xoor'e daa baaxe)",
        [
            ("tête", ["yime"]),
            ("cheveux", ["yinte"]),
            ("visage", ["Giya"]),
            ("front", ["Teingé"]),
            ("œil", ["Yaxe"]),
            ("yeux", ["Yaxou"]),
            ("nez", ["Nuxune"]),
            ("bouche", ["rakke"]),
            ("lèvre", ["gnougnou", "some"]),
            ("dent", ["kambe"]),
            ("dents (pluriel)", ["kambou"]),
            ("langue", ["Nene"]),
            ("oreille", ["torro"]),
            ("joues", ["xoume"]),
            ("menton", ["yesso", "sinke"]),
            ("cou", ["xanné"]),
            ("gorge", ["xorré"]),
        ],
    ),
    (
        2,
        "Le tronc et les organes principaux",
        [
            ("poitrine / torse", ["guidjimé"]),
            ("cœur", ["boutte"]),
            ("ventre", ["noxo"]),
            ("dos", ["mpallé"]),
            ("taille / hanches", ["siga"]),
            ("fesses", ["thinkambé"]),
        ],
    ),
    (
        3,
        "Les membres supérieurs (bras et mains)",
        [
            ("bras", ["Kit'e"]),
            ("main", ["Kitte"]),
            ("épaule", ["Qanfe", "Kanfe"]),
            ("coude", ["Qunyu-bunyi", "Kunyu-bunyi"]),
            ("poignet", ["Kit-qasse"]),
            ("doigt", ["Kit-soro"]),
            ("ongle", ["Tegi-soro", "Tegi-suuru"]),
        ],
    ),
    (
        4,
        "Les membres inférieurs (jambes et pieds)",
        [
            ("jambe", ["Taŋe"]),
            ("pied", ["Tange"]),
            ("cuisse", ["Cuute", "Tchuute"]),
            ("genou", ["Kuntu-bunyi", "Kuru"]),
            ("mollet", ["Tange-golle"]),
            ("cheville", ["Tange-muru"]),
            ("orteil", ["Tange-soro"]),
        ],
    ),
    (
        5,
        "Os, muscles et éléments internes (Biy'e killi)",
        [
            ("corps", ["Biy'e", "Biye"]),
            ("peau", ["Guru", "Kuuru"]),
            ("os", ["Xill'e", "Kille"]),
            ("sang", ["Yig'e", "Yige"]),
            ("chair / muscle", ["Tiy'e", "Tiye"]),
        ],
    ),
]

# Section déjà intégrée au lexique via la liste du référent du 21 octobre 2026.
SECTION_DEJA_INTEGREE = {1}
SOURCE_REFERENT = "liste_referent_tete_visage_2026-10-21"

# Écarts observés entre le document et la liste déjà intégrée : ne pas corriger ici,
# signaler uniquement. (forme, sens dans le doc, sens déjà en base)
ECARTS_MAPPING = [
    ("yesso", "menton (document)", "cou (SNK-LEX-0291)"),
    ("sinke", "menton (document)", "cou, variante (SNK-LEX-0292)"),
    ("xanné", "cou (document)", "gorge (SNK-LEX-0293)"),
    ("xané", "absente du document", "menton (SNK-LEX-0290)"),
]

# Même information, indexée par forme, pour les notes du CSV.
ECARTS_FORMES = {
    "yesso": "cou",
    "sinke": "cou (variante)",
    "xanné": "gorge",
}


def cle_tri(forme: str) -> str:
    """Clé de classement alphabétique, insensible à la casse et aux accents."""
    texte = unicodedata.normalize("NFD", forme.lower())
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    texte = texte.replace("ŋ", "ng").replace("ɲ", "ny")
    texte = texte.replace("'", "").replace("’", "")
    return re.sub(r"\s+", " ", texte).strip()


def cle_rapprochement(forme: str) -> str:
    """Clé large pour détecter les homographes déjà présents dans la base."""
    return re.sub(r"[^a-z0-9]", "", cle_tri(forme))


def charger_base() -> dict[str, list[dict[str, str]]]:
    index: dict[str, list[dict[str, str]]] = {}
    with BASE_CSV.open(encoding="utf-8", newline="") as handle:
        for ligne in csv.DictReader(handle, delimiter=";"):
            cle = cle_rapprochement(ligne.get("soninke", ""))
            if cle:
                index.setdefault(cle, []).append(ligne)
    return index


def construire_lignes() -> list[dict[str, str]]:
    lignes: list[dict[str, str]] = []
    for numero, titre, entrees in SECTIONS:
        for francais, formes in entrees:
            for forme in formes:
                lignes.append(
                    {
                        "soninke": forme,
                        "francais": francais,
                        "section_num": str(numero),
                        "section": titre,
                    }
                )
    lignes.sort(key=lambda r: (cle_tri(r["soninke"]), cle_tri(r["francais"])))
    return lignes


def sens_concordant(francais_doc: str, francais_base: str) -> bool:
    """Vrai si le sens du document recouvre celui déjà en base (hors mentions entre parenthèses)."""
    doc = re.sub(r"\([^)]*\)", " ", cle_tri(francais_doc))
    base = re.sub(r"\([^)]*\)", " ", cle_tri(francais_base))
    doc = {m for m in re.split(r"[^a-z]+", doc) if len(m) > 2}
    base = {m for m in re.split(r"[^a-z]+", base) if len(m) > 2}
    return bool(doc & base)


def annoter(ligne: dict[str, str]) -> tuple[str, str]:
    """Retourne (notes, statut) pour une forme extraite."""
    notes: list[str] = []
    doublons = INDEX.get(cle_rapprochement(ligne["soninke"]), [])

    if int(ligne["section_num"]) in SECTION_DEJA_INTEGREE:
        ids = ", ".join(d["id"] for d in doublons if d.get("source") == SOURCE_REFERENT)
        if ids:
            notes.append(
                "Section 1 : forme déjà intégrée au lexique "
                f"({SOURCE_REFERENT}, {ids})."
            )
        else:
            notes.append(
                "Section 1 : forme non rattachée à la liste déjà intégrée "
                f"({SOURCE_REFERENT}) ; écart de mapping à confirmer."
            )
        if ligne["soninke"] in ECARTS_FORMES:
            notes.append(
                f"Écart de mapping : le document donne « {ligne['francais']} » alors que la base "
                f"atteste « {ECARTS_FORMES[ligne['soninke']]} ». Faire trancher par le référent."
            )
        return " ".join(notes), "deja_integre_a_verifier"

    if doublons:
        concordant = False
        for d in doublons:
            base_fr = d.get("francais", "")
            if sens_concordant(ligne["francais"], base_fr):
                concordant = True
                notes.append(
                    f"Concordance de sens avec {d['id']} « {base_fr} » "
                    f"({d.get('categorie', '')} ; {d.get('source', '')})."
                )
            else:
                notes.append(
                    f"Homographe présent en base : {d['id']} « {base_fr} » "
                    f"({d.get('categorie', '')} ; {d.get('source', '')}). Ne pas fusionner."
                )
        return " ".join(notes), (
            "concordance_a_verifier" if concordant else "homographe_a_verifier"
        )

    notes.append("Forme absente de la base : candidat à soumettre au référent.")
    return " ".join(notes), "a_verifier"


def ecrire_csv(lignes: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            [
                "candidate_id",
                "rang_alphabetique",
                "soninke",
                "francais",
                "section",
                "source_url",
                "source_type",
                "license_status",
                "validation_status",
                "notes",
            ]
        )
        for rang, ligne in enumerate(lignes, start=1):
            notes, statut = annoter(ligne)
            writer.writerow(
                [
                    f"CORPS-{DATE.replace('-', '')}-{rang:03d}",
                    rang,
                    ligne["soninke"],
                    ligne["francais"],
                    f"{ligne['section_num']}. {ligne['section']}",
                    DOC_URL,
                    SOURCE_ID,
                    "rights_to_verify",
                    statut,
                    notes,
                ]
            )


def ecrire_md(lignes: list[dict[str, str]]) -> None:
    out: list[str] = []
    add = out.append

    add("# Extraction du lexique « parties du corps humain » (document Google)")
    add("")
    add(f"Date : {DATE}  ")
    add("Branche : `arena/89ad8992-soninkegpt`  ")
    add(f"Source : {DOC_URL}")
    add("")
    add("## Portée et prudence")
    add("")
    add(
        f"Extraction des **{len(lignes)} formes soninké** présentes dans les tableaux du document. "
        "Chaque variante graphique d'une même ligne source est conservée comme une forme distincte : "
        "aucune fusion, aucune normalisation orthographique, aucune traduction ajoutée."
    )
    add("")
    add(
        "La base de production `data/source/lexique-soninke-fr-base.csv` n'est pas modifiée. "
        "Les formes sont écrites comme candidats dans "
        "`data/candidates/parties-du-corps-doc-google-2026-10-24.csv`, avec le statut "
        "`a_verifier` (ou `homographe_a_verifier` / `deja_integre_a_verifier` le cas échéant). "
        "Aucune entrée n'est considérée validée avant passage devant le référent."
    )
    add("")
    add(
        "Le classement est alphabétique sur la forme soninké, en ignorant la casse, les accents et "
        "les apostrophes, et en ramenant `ŋ` à `ng` (donc `Taŋe` se classe juste avant `Tange`)."
    )
    add("")
    add("## Liste ordonnée (ordre alphabétique)")
    add("")
    add("| # | Soninké | Français (document) | Section | Statut |")
    add("|---|---|---|---|---|")
    for rang, ligne in enumerate(lignes, start=1):
        _, statut = annoter(ligne)
        add(
            f"| {rang} | `{ligne['soninke']}` | {ligne['francais']} | "
            f"{ligne['section_num']} | {statut} |"
        )
    add("")
    add("## Mêmes formes, regroupées par section du document")
    add("")
    for numero, titre, entrees in SECTIONS:
        add(f"### Section {numero} — {titre}")
        add("")
        add("| Français (document) | Soninké |")
        add("|---|---|")
        for francais, formes in entrees:
            add(f"| {francais} | {', '.join(f'`{f}`' for f in formes)} |")
        add("")

    add("## Points à faire trancher par le référent")
    add("")
    add("### 1. Écart de mapping sur la section « tête et visage »")
    add("")
    add(
        "Le document ne reprend pas exactement la liste déjà intégrée le 21 octobre 2026 "
        "(`SNK-LEX-0275` à `SNK-LEX-0294`). Ne rien corriger automatiquement : faire confirmer."
    )
    add("")
    add("| Forme | Sens dans le document | Sens déjà en base |")
    add("|---|---|---|")
    for forme, cote_doc, cote_base in ECARTS_MAPPING:
        add(f"| `{forme}` | {cote_doc} | {cote_base} |")
    add("")
    add("### 2. Recoupements avec la base : concordances et homographes")
    add("")
    add(
        "Certaines formes des sections 2 à 5 existent déjà dans la base. Quand les sens se "
        "recouvrent, c'est une confirmation à faire valider. Quand ils divergent, ce sont des "
        "homographes potentiels, pas des doublons : chaque sens doit rester séparé."
    )
    add("")
    add("| Forme du document | Sens du document | Entrée déjà en base | Sens en base | Lecture |")
    add("|---|---|---|---|---|")
    for ligne in lignes:
        if int(ligne["section_num"]) in SECTION_DEJA_INTEGREE:
            continue
        for d in INDEX.get(cle_rapprochement(ligne["soninke"]), []):
            base_fr = d.get("francais", "")
            lecture = (
                "concordance à confirmer"
                if sens_concordant(ligne["francais"], base_fr)
                else "homographe : ne pas fusionner"
            )
            add(
                f"| `{ligne['soninke']}` | {ligne['francais']} | {d['id']} | "
                f"{base_fr} ({d.get('categorie', '')} ; {d.get('source', '')}) | {lecture} |"
            )
    add("")
    add("### 3. Remarques de transcription")
    add("")
    add(
        "- Le document écrit « Chaire / Muscle » ; la forme retenue côté français est "
        "« chair / muscle » (coquille probable du document, à confirmer)."
    )
    add(
        "- Le document signale lui-même des variations dialectales (Mali, Mauritanie, Sénégal, "
        "Gambie), notamment `X` / `H` à l'initiale."
    )
    add(
        "- La graphie `Taŋe` (jambe) doit être confirmée : `ŋ` note généralement la nasale vélaire, "
        "et la base contient déjà `Tange` (pied) comme forme distincte."
    )
    add(
        "- `Kille` (os) et `Yige` (sang) doivent être tranchés : les entrées proches déjà en base "
        "portent respectivement les sens « route » et « manger »."
    )
    add("")
    add("## Prochaine étape")
    add("")
    add(
        "Soumettre la section 1 (écarts de mapping) et les sections 2 à 5 (formes nouvelles) "
        "au référent linguistique. Tant que la prononciation n'est pas confirmée, aucun audio "
        "ne doit être rattaché à ces formes."
    )

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(out) + "\n", encoding="utf-8")


INDEX = charger_base()


def main() -> None:
    lignes = construire_lignes()
    ecrire_csv(lignes)
    ecrire_md(lignes)
    print(f"{len(lignes)} formes extraites et classées.")
    print(f"  -> {OUT_CSV.relative_to(ROOT)}")
    print(f"  -> {OUT_MD.relative_to(ROOT)}")
    print()
    for rang, ligne in enumerate(lignes, start=1):
        print(f"{rang:>2}. {ligne['soninke']:<14} {ligne['francais']}")


if __name__ == "__main__":
    main()
