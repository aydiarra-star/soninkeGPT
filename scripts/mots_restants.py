#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ce qui reste à trancher après la vérification des 54 formes.

Reprend les 19 formes non résolues (11 non attestées, 7 à confirmer,
1 conflit) et consigne, pour chacune : le sens attesté de la notion, la
forme sous laquelle les sources l'attestent, l'analyse morphologique
quand le mot est un composé, et ce qu'il reste à faire trancher.

Produit :
  - data/candidates/mots-restants-a-trancher-2026-10-24.csv
  - data/source/reports/mots-restants-sens-2026-10-24.md

Aucune forme n'est validée ici : ce sont des pistes sourcées.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_CSV = ROOT / "data" / "candidates" / "mots-restants-a-trancher-2026-10-24.csv"
OUT_MD = ROOT / "data" / "source" / "reports" / "mots-restants-sens-2026-10-24.md"

DATE = "2026-10-24"

# (forme du document, sens du document, notion attestée par les sources,
#  forme attestée pour cette notion, analyse morphologique, statut, sources, action)
#
# statut : resolu | resolu_partiel | non_resolu
LIGNES = [
    ("Taŋe", "jambe", "front", "teŋe ; tenŋe ; taηe",
     "Le document sépare Taŋe (jambe) et Teingé (front). Les sources ne connaissent qu'une "
     "forme, notée teŋe ou taηe, pour le front.",
     "resolu", "S1,S2,S5,S6,S8",
     "Rattacher Taŋe au front comme variante de Teingé, et retenir tanxare pour la jambe."),

    ("Kit-qasse", "poignet", "poignet", "kittinxanne ; kitun qanne",
     "Composé « main + cou ». Le poignet se dit littéralement « le cou de la main » : "
     "kitte (main) + xanne / qanne (cou). « qasse » correspond à cette base « cou ».",
     "resolu_partiel", "S5,S6",
     "La composition confirme le sens. La graphie « qasse » reste à faire confirmer."),

    ("Kit'e", "bras", "main (et bras)", "kitte ; kíttè ; kitu",
     "Le document présente « Kit'e / Kitte » comme une seule entrée. Kit'e est la graphie "
     "du même mot kitte, que le guide SIL glose « la main, le bras ».",
     "resolu_partiel", "S1,S2,S3,S5,S7,S8",
     "Conserver Kit'e comme variante de Kitte. Pour « bras » au sens strict, retenir xuli."),

    ("Tange", "pied", "pied", "ta ; taanu (pluriel)",
     "La base attestée est ta (pied, jambe), taanu au pluriel. « Tange » en est un élargissement "
     "attesté dans les composés (tanxare « jambe », tandoronme « orteil »).",
     "resolu_partiel", "S1,S3,S5,S8",
     "Faire confirmer la forme isolée « Tange » ; la base sûre est ta."),

    ("Kuru", "genou", "genou", "xurungo ; xurngo ; qúrúngò",
     "Aucune source ne note « kuru » seul. La forme attestée est xurungo / qúrúngò, dont kuru "
     "peut être une réduction ou une variante de parler.",
     "resolu_partiel", "S1,S2,S3,S5,S8",
     "Faire confirmer par le référent ; la forme sûre est xurungo."),

    ("Xill'e", "os", "os", "xotte ; qóttè",
     "Aucune source ne note « xill'e ». L'os est attesté sous xotte / qóttè ; le rapprochement "
     "repose uniquement sur la forme-source xotte.",
     "resolu_partiel", "S3,S4,S5",
     "Faire confirmer la graphie ; la forme sûre est xotte."),

    ("Kit-soro", "doigt", "doigt", "doronme ; kittindoromu ; doronmu",
     "Composé « main + soro ». Le doigt est attesté sous doronme ; « les doigts de la main » "
     "sous kittindoromu. Mais « soro » n'est pas le doigt dans les dictionnaires consultés : "
     "sooro = intelligence (ODA), sòró = faire cuire (Creissels, Soninkara).",
     "non_resolu", "S1,S2,S4,S5,S8,S9,S10",
     "Le sens visé est clair (doigt), la forme « soro » ne l'est pas. À faire trancher."),

    ("Tange-soro", "orteil", "orteil", "tandoronme ; tandoore ; tandoromu",
     "Composé « pied + soro », parallèle à Kit-soro. L'orteil est attesté sous tandoronme / "
     "tandoore, littéralement « doigt de pied ». Même réserve sur « soro ».",
     "non_resolu", "S1,S2,S5,S8",
     "Le sens visé est clair (orteil), la forme « soro » reste à confirmer."),

    ("Tange-golle", "mollet", "mollet", "ɲollenme",
     "Composé « pied/jambe + golle ». Le mollet est attesté sous ɲollenme. « golle » est "
     "attesté séparément au sens de « mortier » et « travail » (ODA), pas de « mollet ».",
     "non_resolu", "S4,S5",
     "La notion est attestée sous ɲollenme ; le composé du document ne l'est pas."),

    ("Tange-muru", "cheville", "cheville", "taxaane ; sellinñelle ; ɲollenme",
     "Composé « pied/jambe + muru ». La cheville est attestée sous taxaane et sellinñelle. "
     "« muru » est attesté au sens de « prépuce » (ODA), pas de « cheville ».",
     "non_resolu", "S4,S5,S8",
     "Trois formes concurrentes pour la cheville. À faire trancher par le référent."),

    ("gnougnou", "lèvre", "lèvre", "soome ; soomu ; soomon-fate",
     "Forme absente des dix sources consultées. La lèvre est attestée sous soome, que le "
     "document retient par ailleurs sous la graphie « some ».",
     "non_resolu", "S2,S5,S6",
     "Probablement une variante non documentée de soome. À soumettre au référent."),

    ("siga", "taille / hanches", "hanche", "fengeñe",
     "Aucune source ne donne siga pour la taille ou la hanche. ODA ne connaît siga que comme "
     "verbe « traverser à gué » et comme nom de personne ; Creissels et Soninkara donnent "
     "sòró / soro = faire cuire.",
     "non_resolu", "S4,S5,S9,S10",
     "Écarter siga pour la hanche ; retenir fengeñe sous réserve."),

    ("Qunyu-bunyi", "coude", "coude", "segenantonbe ; segeñ tonbe ; saganan tombe",
     "Composé inanalysable avec les sources disponibles. « bunyi » n'est attesté nulle part. "
     "Le coude est attesté sous trois formes, toutes bâties sur segeñ / segen.",
     "non_resolu", "S4,S5,S6,S8",
     "Forme non attestée ; retenir segenantonbe et faire confirmer."),

    ("Kunyu-bunyi", "coude", "coude", "segenantonbe ; segeñ tonbe ; saganan tombe",
     "Même composé que Qunyu-bunyi, avec la variante graphique k / q.",
     "non_resolu", "S4,S5,S6,S8",
     "Idem."),

    ("Kuntu-bunyi", "genou", "genou", "xurungo ; xurngo ; qúrúngò",
     "Composé inanalysable : « kuntu » est attesté au sens de « clitoris » (ODA, kunto) et "
     "« sphère » (kuntuura), pas de « genou ». « bunyi » n'est attesté nulle part.",
     "non_resolu", "S1,S2,S3,S4,S5,S8",
     "Forme non attestée ; retenir xurungo et faire confirmer."),

    ("Tegi-soro", "ongle", "ongle", "segeñe ; segeɲe ; segene ; ségeñè",
     "Composé « tegi + soro ». L'ongle est attesté sous segeñe / segeɲe. Le premier élément "
     "« tegi » pourrait être une variante de sege, présent dans segeñ tonbe (coude).",
     "non_resolu", "S1,S3,S5",
     "Forme non attestée ; retenir segeñe et faire confirmer."),

    ("Tegi-suuru", "ongle", "ongle", "segeñe ; segeɲe ; segene ; ségeñè",
     "Même composé que Tegi-soro, avec un second élément différent (suuru), non attesté.",
     "non_resolu", "S1,S3,S5",
     "Idem."),

    ("Cuute", "cuisse", "cuisse", "toge ; togue ; togota",
     "Forme absente des dix sources consultées. La cuisse est attestée sous toge dans cinq "
     "sources indépendantes.",
     "non_resolu", "S1,S2,S4,S5,S10",
     "Écarter Cuute ; retenir toge et faire confirmer."),

    ("Tchuute", "cuisse", "cuisse", "toge ; togue ; togota",
     "Variante graphique de Cuute, également absente des sources.",
     "non_resolu", "S1,S2,S4,S5,S10",
     "Idem."),
]

SOURCES = [
    ("S1", "SIL Mali / Asawan — Marianne Hagg, « Parlons le soninké et le français », chap. 6"),
    ("S2", "Les Langues d'Afrique Activities — « Décrire les parties du corps en Soninké » (A1)"),
    ("S3", "CNRS / LGIDF — « Soninké : lexique (noms) », Creissels & Diawara"),
    ("S4", "Lexique Soninké (Mali)–Français–Anglais — ODA / Asawan"),
    ("S5", "« Des mots et des langues » — fiche SONINKE, section « Le corps humain »"),
    ("S6", "Portail Soninkara — Demba Soumaré, « Les différentes parties du corps humain »"),
    ("S7", "snk_engine (noah-medra) — corpus du locuteur de référence, CC BY 4.0"),
    ("S8", "Tableau anatomique multilingue — colonne soninké « Haten súuhunu »"),
    ("S9", "Denis Creissels — lexèmes simples du soninké du Kingi"),
    ("S10", "Portail Soninkara / goumbou — glossaires soninké → français"),
]

STATUTS = {
    "resolu": "résolu",
    "resolu_partiel": "résolu partiellement",
    "non_resolu": "non résolu",
}

# Pistes pour trancher : références non consultables en ligne.
PISTES = [
    ("Ousmane Moussa Diagana",
     "Dictionnaire soninké-français (Mauritanie), Karthala, 2013, 5 800 entrées",
     "Décrit le parler de Kaédi (Mauritanie), dont l'alphabet comporte le phonème q — "
     "la même orthographe que le document (Qanfe, Qunyu, Kit-qasse). C'est la piste la plus "
     "prometteuse pour les formes non résolues. Ouvrage payant (PDF 19,99 €), non consultable "
     "en ligne : seuls les liminaires sont en accès libre."),
    ("Gordon & Sara Williams",
     "« Des aspects de la lexicologie du Soninke : la dérivation, les mots composés, le "
     "changement de transitivité », Dakar, SIL, Cahier de recherche linguistique n° 6, 1998, "
     "92 p. (section « Les mots composés », p. 43-88)",
     "Traite explicitement de la composition en soninké. Les formes du document sont des "
     "composés écrits avec un trait d'union pédagogique (Kit-qasse, Tange-soro, Tegi-soro) : "
     "cet ouvrage est la référence pour en établir l'analyse. PDF accessible sur "
     "sil.org/resources/archives/49407 ; la section utile dépasse la limite d'extraction "
     "automatique (30 pages) et demande une lecture manuelle."),
    ("Galtier, Dantioko & Dramé",
     "Lexique Soninké-Français, Bamako, DNAFLA, 1979, 100 p.",
     "Signalé par COCOON et l'UNESCO. Exemplaire physique uniquement ; non numérisé."),
    ("Abdoulaye Bathily",
     "Lexique soninke (sarakole)-français, Dakar, CLAD, 1975",
     "Signalé dans la bibliographie Soninkara. Non consultable en ligne."),
]


def ecrire_csv() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            [
                "forme_document",
                "sens_document",
                "notion_attestee",
                "forme_attestee_pour_la_notion",
                "analyse",
                "statut",
                "sources",
                "action",
            ]
        )
        for ligne in LIGNES:
            writer.writerow(list(ligne))


def ecrire_md() -> None:
    out: list[str] = []
    add = out.append

    compte = {}
    for ligne in LIGNES:
        compte[ligne[5]] = compte.get(ligne[5], 0) + 1

    add("# Ce qui reste à trancher — 19 formes non résolues")
    add("")
    add(f"Date : {DATE}  ")
    add("Branche : `arena/89ad8992-soninkegpt`  ")
    add("Suite de : `recherche-sens-parties-corps-2026-10-24.md`")
    add("")
    add("## Bilan")
    add("")
    add("| Statut | Formes |")
    add("|---|---|")
    for cle in ("resolu", "resolu_partiel", "non_resolu"):
        add(f"| {STATUTS[cle]} | {compte.get(cle, 0)} |")
    add(f"| **Total** | **{len(LIGNES)}** |")
    add("")
    add(
        f"Sur les {len(LIGNES)} formes restantes, **{compte.get('resolu', 0)} est résolue** "
        f"(Taŋe), **{compte.get('resolu_partiel', 0)} sont résolues partiellement** "
        "(le sens visé est certain, la graphie ou la forme isolée reste à confirmer) et "
        f"**{compte.get('non_resolu', 0)} restent non résolues** : ni la forme du document, "
        "ni son second élément lorsqu'elle est composée, n'apparaissent dans les dix sources "
        "consultées."
    )
    add("")
    add(
        f"Point commun des {compte.get('non_resolu', 0)} non résolues : ce sont presque toutes "
        "des **composés écrits avec un trait d'union** (Kit-soro, Tange-golle, Tange-muru, "
        "Tegi-soro, Kuntu-bunyi, Qunyu-bunyi). Le guide d'écriture SIL indique que ce trait "
        "d'union sert, dans "
        "l'enseignement aux débutants, à montrer les composants d'un mot composé. Le document "
        "a donc probablement été établi dans une variété ou une tradition de transcription "
        "que les dictionnaires disponibles ne couvrent pas."
    )
    add("")

    add("## Détail")
    add("")
    for cle in ("resolu", "resolu_partiel", "non_resolu"):
        add(f"### {STATUTS[cle].capitalize()}")
        add("")
        for ligne in LIGNES:
            if ligne[5] != cle:
                continue
            forme, sens_doc, notion, forme_att, analyse, statut, src, action = ligne
            add(f"**`{forme}`** — le document dit « {sens_doc} »")
            add("")
            add(f"- Notion attestée : {notion}")
            add(f"- Forme attestée : {forme_att}")
            add(f"- Analyse : {analyse}")
            add(f"- Sources : {src}")
            add(f"- À faire : {action}")
            add("")

    add("## Deux réserves de méthode")
    add("")
    add(
        "**L'entrée ɲollenme (ODA).** Le relevé donne « calf (leg); mollet » puis "
        "« ankle; cheville du pied ». Le fragment consulté est tronqué : le second sens est "
        "attribué à ɲollenme, mais cela reste à vérifier sur la page elle-même avant de "
        "l'exploiter. Si les deux sens sont confirmés, une seule forme couvrirait le mollet "
        "et la cheville — à faire valider, car cela distinguerait nettement ce parler du "
        "document, qui les sépare."
    )
    add("")
    add(
        "**Le trait d'union.** Rien ne garantit que « Kit-qasse » et « kitun qanne » soient "
        "le même mot : la correspondance repose sur la composition « main + cou », attestée "
        "par deux sources, pas sur une attestation de la forme elle-même."
    )
    add("")

    add("## Pistes pour trancher")
    add("")
    add(
        "Les dix sources en ligne sont épuisées pour ces formes. Quatre références "
        "complémentaires pourraient les départager :"
    )
    add("")
    for auteur, titre, note in PISTES:
        add(f"- **{auteur}**, {titre}.  ")
        add(f"  {note}")
    add("")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> None:
    ecrire_csv()
    ecrire_md()
    compte: dict[str, int] = {}
    for ligne in LIGNES:
        compte[ligne[5]] = compte.get(ligne[5], 0) + 1
    print(f"{len(LIGNES)} formes restantes :",
          ", ".join(f"{STATUTS[k]}={v}" for k, v in sorted(compte.items())))
    print(f"  -> {OUT_CSV.relative_to(ROOT)}")
    print(f"  -> {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
