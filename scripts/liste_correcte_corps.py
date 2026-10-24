#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Liste corrigée du lexique « parties du corps humain ».

Part des 54 formes du document Google, applique le résultat de la vérification
(`verification-sens-parties-corps-2026-10-24.csv`) et ajoute les notions
attestées qui manquaient. Produit :

  - data/candidates/lexique-corps-corrige-2026-10-24.csv
  - data/source/reports/liste-correcte-parties-corps-2026-10-24.md

Rien n'est inventé : chaque ligne porte ses sources. Une forme absente des
sources consultées est écartée, pas remplacée par une approximation.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_CSV = ROOT / "data" / "candidates" / "lexique-corps-corrige-2026-10-24.csv"
OUT_ECARTES = ROOT / "data" / "candidates" / "formes-ecartees-corps-2026-10-24.csv"
OUT_MD = ROOT / "data" / "source" / "reports" / "liste-correcte-parties-corps-2026-10-24.md"
VERIF_CSV = (
    ROOT / "data" / "source" / "reports" / "verification-sens-parties-corps-2026-10-24.csv"
)

DATE = "2026-10-24"

SECTIONS = [
    (1, "La tête et le visage"),
    (2, "Le tronc et les organes"),
    (3, "Les membres supérieurs"),
    (4, "Les membres inférieurs"),
    (5, "Os, muscles et éléments internes"),
]

# (rang, section, français, soninké retenu, variantes attestées,
#  forme d'origine dans le document, origine, statut, sources, note)
#
# origine : document_confirme | document_corrige | document_variante | ajout_source
# statut  : atteste | sous_reserve
LISTE = [
    # ---------- 1. Tête et visage ----------
    (1, 1, "tête", "yime", "yinme ; yinkolla ; yínmè", "yime", "document_confirme", "atteste",
     "S2,S3,S4,S6", ""),
    (2, 1, "cheveux", "yinte", "yìntè", "yinte", "document_confirme", "atteste",
     "S1,S2,S3,S4", "Le dictionnaire ODA élargit à « poil, plume »."),
    (3, 1, "visage", "Giya", "yeeso", "Giya", "document_confirme", "sous_reserve",
     "S5", "Une seule source. `yesso`, classé « menton » par le document, est une variante de yeeso."),
    (4, 1, "front", "Teingé", "teŋe ; tenŋe ; taηe", "Teingé", "document_confirme", "atteste",
     "S1,S2,S5,S6,S8", "`Taŋe`, classé « jambe » par le document, est la même forme-source."),
    (5, 1, "œil", "Yaxe", "yaaxe ; yáaxè", "Yaxe", "document_confirme", "atteste",
     "S1,S2,S3,S5,S6,S8", ""),
    (6, 1, "yeux", "Yaxou", "yaaxo ; yaaxu ; yaago", "Yaxou", "document_confirme", "atteste",
     "S1,S2", "Pluriel de yaaxe."),
    (7, 1, "nez", "Nuxune", "nuxunne ; núxúnnè", "Nuxune", "document_confirme", "atteste",
     "S1,S2,S3,S5,S6,S8", ""),
    (8, 1, "bouche", "rakke", "raqe ; laqe ; laxxe ; láqqè", "rakke", "document_confirme", "atteste",
     "S1,S2,S3,S5,S6,S8", "Alternance dialectale r / l."),
    (9, 1, "lèvre", "some", "soome ; soomu ; soomon-fate", "some", "document_confirme", "atteste",
     "S2,S5,S6", "`gnougnou` est écarté : non attesté."),
    (10, 1, "dent", "kambe", "kanbe ; kànbê", "kambe", "document_confirme", "atteste",
     "S1,S2,S3,S5", ""),
    (11, 1, "dents (pluriel)", "kambou", "kanbo ; kanbu", "kambou", "document_confirme", "atteste",
     "S1,S2", ""),
    (12, 1, "langue", "Nene", "neene ; néenè", "Nene", "document_confirme", "atteste",
     "S1,S2,S3,S5", ""),
    (13, 1, "oreille", "torro", "toro ; taro ; tárò", "torro", "document_confirme", "atteste",
     "S1,S3,S5,S6,S8", "Variantes toro / taro selon les parlers."),
    (14, 1, "joue", "xoume", "xume ; qume", "xoume", "document_confirme", "atteste",
     "S1,S2,S5,S6", ""),
    (15, 1, "menton", "sinke", "sinqe ; sinqinxotte ; sinxe", "sinke", "document_confirme", "atteste",
     "S1,S5,S6,S8", "Corrige la base interne du projet, qui rattachait sinke au cou."),
    (16, 1, "cou", "xanné", "xanne ; qanne ; qánnè", "xanné", "document_confirme", "atteste",
     "S1,S2,S3,S4,S5,S6,S8", "Corrige la base interne du projet, qui rattachait xanné à la gorge."),
    (17, 1, "gorge", "xorré", "xore", "xorré", "document_confirme", "sous_reserve",
     "S5", "Une seule source."),

    # ---------- 2. Tronc et organes ----------
    (18, 2, "poitrine / torse", "guidjimé", "gijinme ; giginme ; gijimen ; gíjínmè", "guidjimé",
     "document_confirme", "atteste", "S2,S3,S5,S6,S8", ""),
    (19, 2, "foie", "boutte", "butte ; búttè", "boutte", "document_corrige", "atteste",
     "S1,S2,S3,S4,S9,S10", "Le document disait « cœur ». Sens dérivés attestés : courage, colère."),
    (20, 2, "cœur", "sondonme", "sondome ; sòndònmê", "", "ajout_source", "atteste",
     "S1,S2,S3", "Notion absente du document : `boutte` y était donné à tort pour le cœur."),
    (21, 2, "ventre", "noxo", "noqo ; nòxô", "noxo", "document_confirme", "atteste",
     "S1,S2,S3,S5,S8", ""),
    (22, 2, "dos", "xodo", "xoodo ; qóodò", "", "ajout_source", "atteste",
     "S3,S5,S7", "Remplace `mpallé`, qui signifie « puis, ensuite »."),
    (23, 2, "fesses", "thinkambé", "tinkanbe ; fallankanbe", "thinkambé", "document_confirme",
     "atteste", "S1,S2,S5", ""),
    (24, 2, "hanche", "fengeñe", "", "", "ajout_source", "sous_reserve", "S5",
     "Remplace `siga`, non attesté dans ce sens. Une seule source."),

    # ---------- 3. Membres supérieurs ----------
    (25, 3, "main", "Kitte", "kitte ; kíttè ; kitu", "Kitte", "document_confirme", "atteste",
     "S1,S2,S3,S5,S7,S8", "Le guide SIL glose kitte comme « la main, le bras »."),
    (26, 3, "bras", "xuli", "kafe ; quli", "Kit'e", "ajout_source", "atteste",
     "S4,S6,S10", "Le document donnait `Kit'e`, variante graphique probable de kitte. "
                  "ODA glose xuli « avant-bras », le glossaire Soninkara « bras »."),
    (27, 3, "épaule", "kunke", "kunku", "Qanfe / Kanfe", "ajout_source", "atteste",
     "S1,S4,S8,S10", "Remplace Qanfe / Kanfe, qui correspondent à kánpè = aile."),
    (28, 3, "coude", "segenantonbe", "segeñ tonbe ; saganan tombe", "Qunyu-bunyi / Kunyu-bunyi",
     "ajout_source", "atteste", "S4,S5,S6,S8", "Remplace deux formes non attestées."),
    (29, 3, "poignet", "kittinxanne", "kitun qanne", "Kit-qasse", "ajout_source", "atteste",
     "S5,S6", "Littéralement « le cou de la main ». `Kit-qasse` suit la même composition."),
    (30, 3, "doigt", "doronme", "kittindoromu ; doronmu", "Kit-soro", "ajout_source", "atteste",
     "S1,S2,S5,S8", "`Kit-soro` se lit comme « doigt de la main » ; graphie à confirmer."),
    (31, 3, "ongle", "segeñe", "segeɲe ; segene ; ségeñè", "Tegi-soro / Tegi-suuru", "ajout_source",
     "atteste", "S1,S3,S5", "Remplace deux formes non attestées."),

    # ---------- 4. Membres inférieurs ----------
    (32, 4, "jambe", "tanxare", "tansolle ; karankare ; tâ", "Taŋe", "ajout_source", "atteste",
     "S3,S5,S8", "`Taŋe` est réattribué au front, où les sources le placent."),
    (33, 4, "pied", "ta", "taanu (pluriel)", "Tange", "ajout_source", "atteste",
     "S1,S3,S5,S8", "`Tange` reste une graphie à confirmer avec le référent."),
    (34, 4, "cuisse", "toge", "togue ; togota", "Cuute / Tchuute", "ajout_source", "atteste",
     "S1,S2,S4,S5,S10", "Remplace deux formes non attestées."),
    (35, 4, "genou", "xurungo", "xurngo ; qúrúngò", "Kuntu-bunyi / Kuru", "ajout_source", "atteste",
     "S1,S2,S3,S5,S8", "`Kuru` peut en être une réduction ; à confirmer."),
    (36, 4, "mollet", "ɲollenme", "", "Tange-golle", "ajout_source", "sous_reserve", "S4",
     "Une seule source. Remplace une forme non attestée."),
    (37, 4, "cheville", "taxaane", "sellinñelle", "Tange-muru", "ajout_source", "sous_reserve",
     "S5,S8", "Deux sources, deux formes différentes. Remplace une forme non attestée."),
    (38, 4, "orteil", "tandoronme", "tandoore ; tandoromu", "Tange-soro", "ajout_source", "atteste",
     "S1,S2,S5,S8", "`Tange-soro` se lit comme « doigt de pied » ; graphie à confirmer."),

    # ---------- 5. Os, muscles, éléments internes ----------
    (39, 5, "corps", "fate", "", "Biy'e / Biye", "ajout_source", "atteste", "S1,S5,S6",
     "Remplace deux formes non attestées dans ce sens. Homonyme de « peau »."),
    (40, 5, "peau", "fate / hate", "hàtê", "Guru / Kuuru", "ajout_source", "atteste", "S1,S3,S5",
     "Remplace deux formes non attestées dans ce sens. Homonyme de « corps »."),
    (41, 5, "os", "xotte", "qóttè", "Xill'e / Kille", "ajout_source", "atteste", "S3,S4,S5",
     "`Kille` est la route. `Xill'e` reste une graphie à confirmer pour xotte."),
    (42, 5, "sang", "fare", "fore ; hòrê", "Yig'e / Yige", "ajout_source", "atteste", "S1,S3,S5",
     "Remplace deux formes non attestées dans ce sens (yige = manger)."),
    (43, 5, "chair / muscle / viande", "Tiye", "tíyè", "Tiy'e / Tiye", "document_confirme",
     "atteste", "S1,S3,S4,S5,S10", "Le document écrit « Chaire » ; la forme française est « chair »."),
    (44, 5, "poumon", "furutu", "fruutu ; yoohe", "", "ajout_source", "atteste", "S1,S2,S5", ""),
    (45, 5, "estomac", "gonme", "kuuse", "", "ajout_source", "atteste", "S1,S5", ""),
    (46, 5, "rein", "faradinlenme", "faradillenme ; mollo", "", "ajout_source", "sous_reserve",
     "S1,S5", "Une source donne aussi `faradillenme` pour le rein et `mollo` pour un sens voisin."),
]

# (forme écartée, sens que lui donnait le document, motif, devenir)
ECARTES = [
    ("gnougnou", "lèvre", "non attesté", "écarté — la lèvre est `some` (soome)"),
    ("yesso", "menton", "sens contesté", "reclassé — variante de `yeeso` = visage"),
    ("Taŋe", "jambe", "conflit de sources", "reclassé — variante de `Teingé` = front"),
    ("mpallé", "dos", "sens erroné", "sorti du lexique — signifie « puis, ensuite, après »"),
    ("siga", "taille / hanches", "non attesté dans ce sens", "écarté — la hanche est `fengeñe`"),
    ("Kit'e", "bras", "graphie à confirmer", "conservé comme variante de `Kitte` (main)"),
    ("Qanfe", "épaule", "sens erroné", "reclassé — `kánpè` = aile ; l'épaule est `kunke`"),
    ("Kanfe", "épaule", "sens erroné", "reclassé — idem"),
    ("Qunyu-bunyi", "coude", "non attesté", "écarté — le coude est `segenantonbe`"),
    ("Kunyu-bunyi", "coude", "non attesté", "écarté — idem"),
    ("Kit-qasse", "poignet", "graphie à confirmer",
     "conservé sous réserve — le poignet est `kittinxanne`"),
    ("Kit-soro", "doigt", "graphie à confirmer",
     "conservé sous réserve — le doigt est `doronme`"),
    ("Tegi-soro", "ongle", "non attesté", "écarté — l'ongle est `segeñe`"),
    ("Tegi-suuru", "ongle", "non attesté", "écarté — idem"),
    ("Cuute", "cuisse", "non attesté", "écarté — la cuisse est `toge`"),
    ("Tchuute", "cuisse", "non attesté", "écarté — idem"),
    ("Kuntu-bunyi", "genou", "non attesté", "écarté — le genou est `xurungo`"),
    ("Kuru", "genou", "graphie à confirmer",
     "conservé sous réserve — réduction possible de `xurungo`"),
    ("Tange", "pied", "graphie à confirmer", "conservé sous réserve — le pied est `ta`"),
    ("Tange-golle", "mollet", "non attesté", "écarté — le mollet est `ɲollenme`"),
    ("Tange-muru", "cheville", "non attesté", "écarté — la cheville est `taxaane`"),
    ("Tange-soro", "orteil", "graphie à confirmer",
     "conservé sous réserve — l'orteil est `tandoronme`"),
    ("Tiy'e", "chair / muscle", "variante graphique",
     "conservé comme variante de `Tiye`"),
    ("Biy'e", "corps", "non attesté dans ce sens", "écarté — le corps est `fate` ; biye = billet"),
    ("Biye", "corps", "non attesté dans ce sens", "écarté — idem"),
    ("Guru", "peau", "non attesté dans ce sens", "écarté — la peau est `fate / hate`"),
    ("Kuuru", "peau", "non attesté dans ce sens", "écarté — idem"),
    ("Xill'e", "os", "graphie à confirmer", "conservé sous réserve — l'os est `xotte`"),
    ("Kille", "os", "sens erroné", "sorti du lexique — `kille` = la route"),
    ("Yig'e", "sang", "non attesté dans ce sens", "écarté — le sang est `fare` ; yige = manger"),
    ("Yige", "sang", "non attesté dans ce sens", "écarté — idem"),
]

SOURCES = [
    ("S1", "SIL Mali / Asawan — Marianne Hagg, « Parlons le soninké et le français », chap. 6 « Fate – Le corps »"),
    ("S2", "Les Langues d'Afrique Activities — « Décrire les parties du corps en Soninké » (A1)"),
    ("S3", "CNRS / LGIDF — « Soninké : lexique (noms) », Creissels & Diawara (soninké du Kingui)"),
    ("S4", "Lexique Soninké (Mali)–Français–Anglais — ODA / Asawan"),
    ("S5", "« Des mots et des langues » — fiche SONINKE, section « Le corps humain »"),
    ("S6", "Portail Soninkara — Demba Soumaré, « Les différentes parties du corps humain »"),
    ("S7", "snk_engine (noah-medra) — corpus du locuteur de référence, CC BY 4.0"),
    ("S8", "Tableau anatomique multilingue — colonne soninké « Haten súuhunu »"),
    ("S9", "Denis Creissels — lexèmes simples du soninké du Kingi"),
    ("S10", "Portail Soninkara — glossaires soninké → français"),
]

ORIGINES = {
    "document_confirme": "document, sens confirmé",
    "document_corrige": "document, sens corrigé",
    "ajout_source": "ajouté depuis les sources",
}


def ecrire_csv() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            [
                "candidate_id",
                "rang",
                "section",
                "francais",
                "soninke",
                "variantes_attestees",
                "forme_document",
                "origine",
                "statut_verification",
                "sources",
                "note",
            ]
        )
        for ligne in LISTE:
            rang, section, francais, soninke, variantes, forme_doc, origine, statut, src, note = ligne
            writer.writerow(
                [
                    f"CORPS-{DATE.replace('-', '')}-{rang:03d}",
                    rang,
                    f"{section}. {dict(SECTIONS)[section]}",
                    francais,
                    soninke,
                    variantes,
                    forme_doc,
                    origine,
                    statut,
                    src,
                    note,
                ]
            )


def ecrire_ecartes_csv() -> None:
    """Trace les formes du document non retenues, pour ne rien perdre."""
    OUT_ECARTES.parent.mkdir(parents=True, exist_ok=True)
    with OUT_ECARTES.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            ["forme_document", "sens_document", "motif", "devenir", "sources_remplacement"]
        )
        for forme, sens, motif, devenir in ECARTES:
            remplacement = next(
                (l[8] for l in LISTE if forme in [f.strip() for f in l[5].split("/")]),
                "",
            )
            writer.writerow([forme, sens, motif, devenir, remplacement])


def verifier_couverture() -> list[str]:
    """Chaque forme du document doit être retenue ou tracée comme écartée."""
    with VERIF_CSV.open(encoding="utf-8", newline="") as handle:
        doc = {r["forme_document"] for r in csv.DictReader(handle)}

    couverts: set[str] = set()
    for ligne in LISTE:
        for forme in ligne[5].split("/"):
            couverts.add(forme.strip())
    for forme, *_ in ECARTES:
        couverts.add(forme.strip())

    return sorted(doc - couverts)


def ecrire_md() -> None:
    out: list[str] = []
    add = out.append
    titres = dict(SECTIONS)

    add("# Liste corrigée — parties du corps humain en soninké")
    add("")
    add(f"Date : {DATE}  ")
    add("Branche : `arena/89ad8992-soninkegpt`  ")
    add("Entrée : les 54 formes du document Google « parties du corps humain »")
    add("")
    add("## Ce que contient cette liste")
    add("")
    add(
        f"**{len(LISTE)} notions**, dont {sum(1 for l in LISTE if l[6] != 'ajout_source')} "
        f"venues du document et {sum(1 for l in LISTE if l[6] == 'ajout_source')} ajoutées "
        "parce que le sens que le document leur donnait n'était pas attesté. "
        f"**{len(ECARTES)} formes** du document sont écartées ou reclassées ; le détail est en "
        "fin de document."
    )
    add("")
    add(
        "Deux niveaux de confiance : **attesté** (au moins deux sources convergentes) et "
        "**sous réserve** (une seule source, ou deux sources donnant des formes différentes). "
        "Rien n'est inventé : une forme non retrouvée est écartée, jamais remplacée par "
        "une approximation. Cette liste reste à valider par le référent."
    )
    add("")
    add("## Liste")
    add("")
    for numero, titre in SECTIONS:
        add(f"### {numero}. {titre}")
        add("")
        add("| Français | Soninké | Variantes attestées | Origine | Statut | Sources |")
        add("|---|---|---|---|---|---|")
        for ligne in LISTE:
            rang, section, francais, soninke, variantes, forme_doc, origine, statut, src, _ = ligne
            if section != numero:
                continue
            add(
                f"| {francais} | **{soninke}** | {variantes or '—'} | "
                f"{ORIGINES[origine]} | {statut.replace('_', ' ')} | {src} |"
            )
        add("")
    add("### Notes")
    add("")
    for ligne in LISTE:
        if ligne[9]:
            add(f"- **{ligne[3]}** — {ligne[9]}")
    add("")
    add("## Formes du document écartées ou reclassées")
    add("")
    add("| Forme | Sens donné par le document | Motif | Devenir |")
    add("|---|---|---|---|")
    for forme, sens, motif, devenir in ECARTES:
        add(f"| `{forme}` | {sens} | {motif} | {devenir} |")
    add("")
    add("## Sources")
    add("")
    for cle, titre in SOURCES:
        add(f"- **{cle}** — {titre}")
    add("")
    add(
        "Rappel : la page CNRS/LGIDF (S3) est en migration et son contenu a été lu via "
        "l'indexation ; à re-vérifier sur la nouvelle adresse avant citation formelle."
    )
    add("")
    add("## Prochaine étape")
    add("")
    add(
        "Faire valider cette liste par le référent linguistique, en commençant par les "
        f"{sum(1 for l in LISTE if l[7] == 'sous_reserve')} lignes « sous réserve » et par "
        "l'homonymie `fate` = corps / peau. Aucun audio ne doit être rattaché à une forme "
        "tant que le référent ne l'a pas confirmée."
    )

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> None:
    manquants = verifier_couverture()
    if manquants:
        raise SystemExit(f"Formes du document non traitées : {manquants}")

    ecrire_csv()
    ecrire_ecartes_csv()
    ecrire_md()
    print(f"{len(LISTE)} notions retenues, {len(ECARTES)} formes écartées ou reclassées.")
    print("Toutes les formes du document sont retenues ou tracées.")
    print(f"  -> {OUT_CSV.relative_to(ROOT)}")
    print(f"  -> {OUT_ECARTES.relative_to(ROOT)}")
    print(f"  -> {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
