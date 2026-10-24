#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérification du sens des 54 formes du lexique « parties du corps » du document Google.

Chaque forme est confrontée aux sources dictionnairiques et pédagogiques
consultées le 2026-10-24. Aucune traduction n'est inventée : une forme non
retrouvée reste déclarée `non_atteste`, et une divergence est déclarée
`corrige` avec ses sources.

Le script n'écrit que deux fichiers :
  - data/source/reports/verification-sens-parties-corps-2026-10-24.csv
  - data/source/reports/recherche-sens-parties-corps-2026-10-24.md

La base de production et les fichiers de candidats existants ne sont pas touchés.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_CSV = (
    ROOT / "data" / "source" / "reports" / "verification-sens-parties-corps-2026-10-24.csv"
)
OUT_MD = ROOT / "data" / "source" / "reports" / "recherche-sens-parties-corps-2026-10-24.md"

DATE = "2026-10-24"

SOURCES = [
    (
        "S1",
        "SIL Mali / Asawan — Marianne Hagg, « O nan sefe sooninken do faransen ŋa — "
        "Parlons le soninké et le français », chap. 6 « Fate – Le corps »",
        "https://www.asawan.org/sites/www.asawan.org/files/uploads/O%20nan%20sefe%20sooninken%20"
        "do%20faransen%20%C5%8Ba%202e%20%C3%A9d%20-%20Web%20lecture.pdf",
    ),
    (
        "S2",
        "Les Langues d'Afrique Activities — « Décrire les parties du corps en Soninké », "
        "cours Soninké 2 – niveau A1",
        "https://leslanguesdafriqueactivities.com/lessons/4-savoir-decrire-lhomme-et-sa-societe-"
        "en-soninke-2/decrire-les-parties-du-corps-en-soninke/",
    ),
    (
        "S3",
        "CNRS / LGIDF — « Soninké : lexique (noms) », Denis Creissels & Ismaël Diawara "
        "(soninké du Kingui, Mali)",
        "https://lgidf.cnrs.fr/node/680",
    ),
    (
        "S4",
        "Lexique Soninké (Mali)–Français–Anglais — ODA / Asawan (entrées consultées lettre par "
        "lettre)",
        "https://media.ipsapps.org/snk/oda/lexicon/",
    ),
    (
        "S5",
        "« Des mots et des langues » — fiche SONINKE, section « Le corps humain » "
        "(vocabulaire français → soninké)",
        "https://desmotsetdeslangues.eklablog.com/soninke-a113996526",
    ),
    (
        "S6",
        "Portail Soninkara — Demba Soumaré, « Vocabulaire Soninké : les différentes parties du "
        "corps humain »",
        "http://www.soninkara.org/langue-soninke/vocabulaire-soninke-les-differentes-parties-du-"
        "corps-humain-4281.html",
    ),
    (
        "S7",
        "snk_engine (noah-medra) — corpus et lexique du locuteur de référence, CC BY 4.0 "
        "(source déjà référencée par le projet)",
        "https://github.com/oscarmedra/snk_engine",
    ),
    (
        "S8",
        "Tableau anatomique multilingue — colonne soninké « Haten súuhunu / Sarahule » "
        "(Bangally Sabally)",
        "https://megambia.com/wp-content/uploads/2025/01/040125-bodyparts.pdf",
    ),
    (
        "S9",
        "Denis Creissels — « Phonologie segmentale et tonale du soninké (parler du Kingi) », "
        "annexe : lexèmes simples",
        "https://journals.openedition.org/mandenkan/738",
    ),
    (
        "S10",
        "Portail Soninkara — glossaires soninké → français (Hadiya Wagué) ; "
        "glossaire soninké–français (goumbou.free.fr)",
        "http://www.soninkara.com/langue/apprendre-le-soninke/glossaire-de-mots.html",
    ),
]

# (rang, forme du document, sens du document, section, sens attesté,
#  formes attestées dans les sources, sources, statut, note)
# statut : confirme | corrige | conflit | a_confirmer | non_atteste
LIGNES = [
    # ---------- Section 1 : tête et visage ----------
    (1, "yime", "tête", 1, "tête", "yinme ; yinkolla ; yínmè", "S2,S3,S4,S6", "confirme",
     "Trois traditions orthographiques pour le même mot."),
    (2, "yinte", "cheveux", 1, "cheveu, poil", "yinte ; yìntè", "S1,S2,S3,S4", "confirme",
     "Le dictionnaire élargit à « poil, plume »."),
    (3, "Giya", "visage", 1, "visage", "giya (aussi yeeso)", "S5", "confirme",
     "Une seule source consultée ; à faire confirmer."),
    (4, "Teingé", "front", 1, "front", "teŋe ; tenŋe ; taηe ; teŋe", "S1,S2,S5,S6,S8", "confirme",
     "Graphie « Teingé » non relevée telle quelle ; la forme-source est teŋe/tenŋe."),
    (5, "Yaxe", "œil", 1, "œil", "yaaxe ; yáaxè", "S1,S2,S3,S5,S6,S8", "confirme", ""),
    (6, "Yaxou", "yeux", 1, "yeux (pluriel)", "yaaxo ; yaaxu ; yaago", "S1,S2", "confirme",
     "Pluriel de yaaxe."),
    (7, "Nuxune", "nez", 1, "nez", "nuxunne ; núxúnnè", "S1,S2,S3,S5,S6,S8", "confirme", ""),
    (8, "rakke", "bouche", 1, "bouche", "raqe ; laqe ; laxxe ; láqqè", "S1,S2,S3,S5,S6,S8", "confirme",
     "Alternance dialectale r/l bien documentée sur ce mot."),
    (9, "gnougnou", "lèvre", 1, "non attesté", "lèvre = soome ; soomu ; soomon-fate",
     "S2,S5,S6", "non_atteste",
     "Forme absente des sources consultées. La lèvre est attestée sous « soome/soomo », "
     "variante « some » déjà retenue par le document."),
    (10, "some", "lèvre", 1, "lèvre", "soome ; soomu ; soomon-fate", "S2,S5,S6", "confirme",
     "« some » = graphie francisée de soome."),
    (11, "kambe", "dent", 1, "dent", "kanbe ; kànbê", "S1,S2,S3,S5", "confirme", ""),
    (12, "kambou", "dents (pluriel)", 1, "dents (pluriel)", "kanbo ; kanbu", "S1,S2", "confirme", ""),
    (13, "Nene", "langue", 1, "langue (organe)", "neene ; néenè", "S1,S2,S3,S5", "confirme", ""),
    (14, "torro", "oreille", 1, "oreille", "toro ; taro ; tárò", "S1,S3,S5,S6,S8", "confirme",
     "Variantes toro/taro selon les parlers."),
    (15, "xoume", "joues", 1, "joue", "xume ; qume", "S1,S2,S5,S6", "confirme", ""),
    (16, "yesso", "menton", 1, "visage", "yeeso (visage) ; menton = sinqe / sinqinxotte / sinxe",
     "S5,S1,S6,S8", "corrige",
     "Le document place yesso sous « menton ». Les sources attestent yeeso = visage, "
     "et le menton est sinqe (variante « sinke » du document)."),
    (17, "sinke", "menton", 1, "menton", "sinqe ; sinqinxotte ; sinxe", "S1,S5,S6,S8", "confirme",
     "Contredit la base interne du projet, qui rattache sinke au cou."),
    (18, "xanné", "cou", 1, "cou", "xanne ; qanne ; qánnè", "S1,S2,S3,S4,S5,S6,S8", "confirme",
     "Contredit la base interne du projet, qui rattache xanné à la gorge."),
    (19, "xorré", "gorge", 1, "gorge", "xore", "S5", "confirme",
     "Une seule source consultée ; à faire confirmer."),

    # ---------- Section 2 : tronc et organes ----------
    (20, "guidjimé", "poitrine / torse", 2, "poitrine", "gijinme ; giginme ; gijimen ; gíjínmè",
     "S2,S3,S5,S6,S8", "confirme", ""),
    (21, "boutte", "cœur", 2, "foie (et, par extension, courage / colère)",
     "butte = foie ; cœur = sondonme / sondome / sòndònmê", "S1,S2,S3,S4,S9,S10", "corrige",
     "Divergence majeure : cinq sources indépendantes donnent butte = foie et sondonme = cœur. "
     "Le lexique ODA précise aussi les sens dérivés « émotion, colère »."),
    (22, "noxo", "ventre", 2, "ventre", "noxo ; noqo ; nòxô", "S1,S2,S3,S5,S8", "confirme", ""),
    (23, "mpallé", "dos", 2, "« puis, ensuite, après » (adverbe) — pas un nom de partie du corps",
     "dos = xodo ; xoodo ; qóodò ; mpallé / kémpalé / fallé = puis, après", "S3,S5,S7", "corrige",
     "Le corpus du référent (S7) emploie mpallé, kémpalé et fallé au sens de « puis / ensuite / "
     "après ». Le dos est attesté sous xodo/xoodo."),
    (24, "siga", "taille / hanches", 2, "non attesté dans ce sens",
     "siga = traverser un cours d'eau sans nager (verbe) ; hanche = fengeñe", "S4,S5", "non_atteste",
     "Le lexique ODA ne connaît siga que comme verbe et comme nom de personne. "
     "La hanche est attestée sous fengeñe."),
    (25, "thinkambé", "fesses", 2, "fesse, fesses", "tinkanbe ; fallankanbe", "S1,S2,S5", "confirme",
     "Graphie « thinkambé » non relevée telle quelle ; la forme-source est tinkanbe."),

    # ---------- Section 3 : membres supérieurs ----------
    (26, "Kit'e", "bras", 3, "à préciser : kitte = main (et bras) ; bras = xuli / kafe",
     "kitte ; xuli ; kafe ; quli", "S1,S4,S6,S10", "a_confirmer",
     "Le document présente « Kit'e / Kitte » comme une seule entrée « bras / main ». "
     "Les sources séparent : kitte = main, xuli = bras / avant-bras, kafe = bras."),
    (27, "Kitte", "main", 3, "main", "kitte ; kíttè", "S1,S2,S3,S5,S8", "confirme",
     "Le guide SIL glose kitte comme « la main, le bras »."),
    (28, "Qanfe", "épaule", 3, "aile", "épaule = kunke ; aile = kánpè / kanpe",
     "S3,S4,S8,S10", "corrige",
     "L'épaule est attestée sous kunke. La forme proche de Qanfe est kánpè / kanpe = aile."),
    (29, "Kanfe", "épaule", 3, "aile", "épaule = kunke ; aile = kánpè / kanpe",
     "S3,S4,S8,S10", "corrige", "Même correction que Qanfe."),
    (30, "Qunyu-bunyi", "coude", 3, "non attesté",
     "coude = segenantonbe ; segeñ tonbe ; saganan tombe", "S4,S5,S6,S8", "non_atteste",
     "Forme absente des sources consultées."),
    (31, "Kunyu-bunyi", "coude", 3, "non attesté",
     "coude = segenantonbe ; segeñ tonbe ; saganan tombe", "S4,S5,S6,S8", "non_atteste",
     "Forme absente des sources consultées."),
    (32, "Kit-qasse", "poignet", 3, "poignet (analyse structurale)",
     "kittinxanne ; kitun qanne = « le cou de la main »", "S5,S6", "a_confirmer",
     "Le poignet se dit littéralement « cou de la main » (kitte + xanne/qanne). "
     "Le second élément « qasse » correspond à cette base « cou » ; la graphie reste à confirmer."),
    (33, "Kit-soro", "doigt", 3, "doigt (analyse structurale)",
     "doronme ; les doigts = kittindoromu / doronmu", "S1,S2,S5,S8", "a_confirmer",
     "Le doigt est attesté sous doronme ; « kit-soro » se lit comme « doigt de la main ». "
     "Le second élément « soro » reste à confirmer."),
    (34, "Tegi-soro", "ongle", 3, "non attesté", "ongle = segeñe ; segeɲe ; ségeñè",
     "S1,S3,S5", "non_atteste", "Forme absente des sources consultées."),
    (35, "Tegi-suuru", "ongle", 3, "non attesté", "ongle = segeñe ; segeɲe ; ségeñè",
     "S1,S3,S5", "non_atteste", "Forme absente des sources consultées."),

    # ---------- Section 4 : membres inférieurs ----------
    (36, "Taŋe", "jambe", 4, "front (conflit avec le document)",
     "taηe / teŋe = front ; jambe = tanxare ; tansolle ; tâ", "S1,S2,S5,S6,S8", "conflit",
     "Le document fait de Taŋe la « jambe » et de Teingé le « front ». Les sources donnent "
     "teŋe / taηe = front pour les deux graphies. La jambe est attestée sous tanxare / tâ."),
    (37, "Tange", "pied", 4, "pied / jambe — graphie à confirmer",
     "pied = ta ; pieds = taanu ; jambe = tanxare", "S1,S3,S5,S8", "a_confirmer",
     "La base est ta (pied, jambe) ; le document note Tange. À faire confirmer avec le référent."),
    (38, "Cuute", "cuisse", 4, "non attesté", "cuisse = toge ; togue ; togota",
     "S1,S2,S4,S5,S10", "non_atteste", "Forme absente des sources consultées."),
    (39, "Tchuute", "cuisse", 4, "non attesté", "cuisse = toge ; togue ; togota",
     "S1,S2,S4,S5,S10", "non_atteste", "Forme absente des sources consultées."),
    (40, "Kuntu-bunyi", "genou", 4, "non attesté", "genou = xurungo ; xurngo ; qúrúngò",
     "S1,S2,S3,S5,S8", "non_atteste", "Forme absente des sources consultées."),
    (41, "Kuru", "genou", 4, "genou (variante probable)", "xurungo ; xurngo ; qúrúngò",
     "S1,S2,S3,S5,S8", "a_confirmer",
     "Aucune source ne note « kuru » seul ; la forme attestée est xurungo / qúrúngò, "
     "dont kuru peut être une réduction. À faire confirmer."),
    (42, "Tange-golle", "mollet", 4, "non attesté", "mollet = ɲollenme", "S4", "non_atteste",
     "Forme absente des sources consultées."),
    (43, "Tange-muru", "cheville", 4, "non attesté", "cheville = taxaane ; sellinñelle",
     "S5,S8", "non_atteste", "Forme absente des sources consultées."),
    (44, "Tange-soro", "orteil", 4, "orteil (analyse structurale)",
     "tandoronme ; tandoore", "S1,S5,S8", "a_confirmer",
     "L'orteil est attesté sous tandoronme / tandoore ; « tange-soro » se lit comme "
     "« doigt de pied ». Graphie à confirmer."),

    # ---------- Section 5 : os, muscles, éléments internes ----------
    (45, "Biy'e", "corps", 5, "non attesté dans ce sens",
     "corps = fate ; biye = ticket, billet", "S1,S4,S5,S6,S7", "corrige",
     "Le corps est attesté sous fate. Le lexique ODA et la base interne donnent "
     "biye = billet (SNK-LEX-0529)."),
    (46, "Biye", "corps", 5, "non attesté dans ce sens",
     "corps = fate ; biye = ticket, billet", "S1,S4,S5,S6,S7", "corrige",
     "Même correction que Biy'e."),
    (47, "Guru", "peau", 5, "non attesté dans ce sens",
     "peau = fate ; hate ; hàtê ; guruɲa = bassin", "S1,S3,S4,S5", "corrige",
     "La peau est attestée sous fate / hate. La forme proche guruɲa désigne le bassin."),
    (48, "Kuuru", "peau", 5, "non attesté dans ce sens",
     "peau = fate ; hate ; hàtê ; guruɲa = bassin", "S1,S3,S4,S5", "corrige",
     "Même correction que Guru."),
    (49, "Xill'e", "os", 5, "os — graphie à confirmer", "os = xotte ; qóttè", "S3,S4,S5",
     "a_confirmer",
     "L'os est attesté sous xotte / qóttè. Aucune source ne note « xill'e » ; "
     "le rapprochement repose sur la forme-source xotte."),
    (50, "Kille", "os", 5, "route", "route = kille ; kìllê", "S1,S3,S7", "corrige",
     "kille est la route dans toutes les sources consultées, y compris le corpus du référent "
     "et la base interne du projet. L'os est xotte."),
    (51, "Yig'e", "sang", 5, "non attesté dans ce sens",
     "sang = fare ; fore ; hòrê ; yige = manger", "S1,S3,S5,S7", "corrige",
     "Le sang est attesté sous fare / fore / hòrê. La base yige est le verbe « manger »."),
    (52, "Yige", "sang", 5, "non attesté dans ce sens",
     "sang = fare ; fore ; hòrê ; yige = manger", "S1,S3,S5,S7", "corrige",
     "Même correction que Yig'e."),
    (53, "Tiy'e", "chair / muscle", 5, "viande, chair, muscle", "tiye ; tíyè", "S1,S3,S4,S5,S10",
     "confirme", "Le document écrit « Chaire » ; la forme française est « chair »."),
    (54, "Tiye", "chair / muscle", 5, "viande, chair, muscle", "tiye ; tíyè", "S1,S3,S4,S5,S10",
     "confirme", ""),
]

# Formes attestées absentes du document, proposées en complément.
COMPLEMENT = [
    ("cœur", "sondonme / sondome / sòndònmê", "S1,S2,S3"),
    ("dos", "xodo / xoodo / qóodò", "S3,S5,S7"),
    ("corps", "fate", "S1,S5,S6"),
    ("peau", "fate / hate / hàtê", "S1,S3,S5"),
    ("os", "xotte / qóttè", "S3,S4,S5"),
    ("sang", "fare / fore / hòrê", "S1,S3,S5"),
    ("épaule", "kunke", "S1,S4,S8"),
    ("bras", "xuli / kafe / quli", "S4,S6,S10"),
    ("coude", "segenantonbe / segeñ tonbe", "S4,S5,S8"),
    ("poignet", "kittinxanne / kitun qanne", "S5,S6"),
    ("doigt", "doronme", "S1,S5,S8"),
    ("ongle", "segeñe / segeɲe", "S1,S3,S5"),
    ("cuisse", "toge", "S1,S2,S4,S5,S10"),
    ("genou", "xurungo / xurngo", "S1,S2,S5,S8"),
    ("cheville", "taxaane / sellinñelle", "S5,S8"),
    ("mollet", "ɲollenme", "S4"),
    ("hanche", "fengeñe", "S5"),
    ("poumon", "furutu / fruutu", "S1,S5"),
    ("estomac", "gonme / kuuse", "S1,S5"),
    ("rein", "faradinlenme / mollo", "S1,S5"),
    ("front", "teŋe / taηe", "S1,S5,S6,S8"),
    ("menton", "sinqe / sinqinxotte", "S1,S5,S6,S8"),
    ("visage", "yeeso / giya", "S5"),
]

STATUTS = {
    "confirme": "confirmé",
    "corrige": "corrigé",
    "conflit": "conflit de sources",
    "a_confirmer": "à confirmer",
    "non_atteste": "non attesté",
}


def ecrire_csv() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            [
                "rang",
                "forme_document",
                "sens_document",
                "section_document",
                "sens_atteste",
                "formes_attestees_sources",
                "sources",
                "statut_verification",
                "note",
            ]
        )
        for ligne in LIGNES:
            writer.writerow(list(ligne))


def ecrire_md() -> None:
    out: list[str] = []
    add = out.append

    compte = {}
    for ligne in LIGNES:
        compte[ligne[7]] = compte.get(ligne[7], 0) + 1

    add("# Recherche du sens des 54 formes du lexique « parties du corps »")
    add("")
    add(f"Date : {DATE}  ")
    add("Branche : `arena/89ad8992-soninkegpt`")
    add("")
    add("## Méthode et limites")
    add("")
    add(
        "Chaque forme du document a été confrontée aux sources dictionnairiques et "
        "pédagogiques listées plus bas. Aucune traduction n'est extrapolée : une forme non "
        "retrouvée est déclarée **non attesté**, et une divergence est déclarée **corrigé** "
        "avec ses sources. Les variantes graphiques ne sont pas fusionnées."
    )
    add("")
    add(
        "Deux réserves à garder en tête. D'abord, ces sources décrivent des variétés "
        "différentes du soninké (Kingui au Mali, parlers du Sénégal et de Mauritanie, "
        "orthographes SIL et ODA) : une divergence n'est pas forcément une erreur du document. "
        "Ensuite, aucune de ces attestations ne remplace la validation du référent : les "
        "statuts ci-dessous sont des pistes sourcées, pas des validations."
    )
    add("")
    add(
        "La page CNRS/LGIDF `lgidf.cnrs.fr/node/680` n'était plus accessible directement : "
        "le site renvoie vers `lgmef.huma-num.fr`, où l'ancienne adresse répond 404. "
        "Son contenu a été consulté via les résultats de recherche qui l'indexent ; "
        "les entrées citées sous **S3** doivent donc être re-vérifiées sur la nouvelle "
        "adresse avant toute citation formelle."
    )
    add("")
    add("## Résultat en un coup d'œil")
    add("")
    add("| Statut | Nombre de formes |")
    add("|---|---|")
    for cle in ("confirme", "corrige", "conflit", "a_confirmer", "non_atteste"):
        add(f"| {STATUTS[cle]} | {compte.get(cle, 0)} |")
    add(f"| **Total** | **{len(LIGNES)}** |")
    add("")

    for titre, statut in (
        ("Corrections : le sens du document est contredit par les sources", "corrige"),
        ("Conflits de sources", "conflit"),
        ("Formes non attestées dans les sources consultées", "non_atteste"),
        ("Formes à confirmer (attestation partielle ou analyse structurale)", "a_confirmer"),
    ):
        add(f"## {titre}")
        add("")
        add("| Forme | Sens du document | Sens attesté | Sources |")
        add("|---|---|---|---|")
        for ligne in LIGNES:
            if ligne[7] != statut:
                continue
            add(
                f"| `{ligne[1]}` | {ligne[2]} | {ligne[4]} | {ligne[6]} |"
            )
        add("")

    add("## Table complète")
    add("")
    add("| # | Forme | Sens du document | Sens attesté | Forme-source | Sources | Statut |")
    add("|---|---|---|---|---|---|---|")
    for ligne in LIGNES:
        add(
            f"| {ligne[0]} | `{ligne[1]}` | {ligne[2]} | {ligne[4]} | "
            f"{ligne[5]} | {ligne[6]} | {STATUTS[ligne[7]]} |"
        )
    add("")
    add("### Notes ligne par ligne")
    add("")
    for ligne in LIGNES:
        if ligne[8]:
            add(f"- **{ligne[1]}** ({ligne[2]}) — {ligne[8]}")
    add("")

    add("## Notions attestées absentes du document")
    add("")
    add(
        "Ces sens sont attestés par au moins une source et ne figurent pas dans le document. "
        "Utile pour compléter la liste avant de la soumettre au référent."
    )
    add("")
    add("| Français | Soninké attesté | Sources |")
    add("|---|---|---|")
    for francais, soninke, sources in COMPLEMENT:
        add(f"| {francais} | {soninke} | {sources} |")
    add("")

    add("## Sources consultées")
    add("")
    add(
        "Droits de réutilisation à vérifier avant toute extraction massive : ces ressources "
        "sont utilisées ici pour relever des attestations ponctuelles, avec attribution."
    )
    add("")
    for cle, titre, url in SOURCES:
        add(f"- **{cle}** — {titre}  ")
        add(f"  {url}")
    add("")
    add("## Prochaine étape")
    add("")
    add(
        "Soumettre au référent linguistique, dans l'ordre : les 12 corrections, le conflit "
        "sur `Taŋe`, puis les 8 formes non attestées et les 9 formes à confirmer. "
        "Tant qu'une forme n'est pas tranchée, aucun audio ne doit lui être rattaché."
    )

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> None:
    ecrire_csv()
    ecrire_md()
    compte: dict[str, int] = {}
    for ligne in LIGNES:
        compte[ligne[7]] = compte.get(ligne[7], 0) + 1
    print(f"{len(LIGNES)} formes vérifiées :",
          ", ".join(f"{STATUTS[k]}={v}" for k, v in sorted(compte.items())))
    print(f"  -> {OUT_CSV.relative_to(ROOT)}")
    print(f"  -> {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
