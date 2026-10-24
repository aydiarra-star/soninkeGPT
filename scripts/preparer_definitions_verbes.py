#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prépare les définitions des verbes du document du référent.

Constat de départ : les 182 verbes de `data/grammaire/soninke.yaml` ont chacun
une entrée dans `data/source/lexique-soninke-fr-base.csv`, mais la plupart n'ont
qu'une glose d'un seul mot (« tuer », « obéir », « brûler »). Aucun n'est absent
du lexique : il n'y a donc **aucune entrée à créer**, seulement des entrées à
enrichir — c'est la garantie anti-doublon du projet.

Les définitions elles-mêmes sont rédigées à la main dans
`data/source/definitions-redigees.csv` (avec celles des autres mots du
lexique), à partir de la glose française déjà attestée dans le lexique : aucune
source nouvelle, aucun sens inventé. Ce script ne rédige rien : il joint,
contrôle et met en forme.

  1. pour chaque verbe, retrouve son entrée de lexique (comparaison identique à
     celle de `check_doublons_lexique.py`, importée du script d'import) ;
  2. vérifie qu'aucune forme ne serait un doublon : la forme est-elle déjà
     entrée principale, ou citée comme `variante` d'une autre entrée ?
  3. joint la définition rédigée, ou signale qu'elle manque ;
  4. récupère jusqu'à deux phrases d'emploi attestées (soninké + traduction
     française quand le corpus la fournit) ;
  5. écrit `data/candidates/definitions-verbes-2026-10-24.csv` et
     `docs/DEFINITIONS-VERBES-A-VALIDER.md`.

Aucune écriture dans le lexique : voir
`scripts/enrichir_definitions_sans_doublons.py` pour l'application, qui n'ajoute
jamais de ligne.

Usage :
    python3 scripts/preparer_definitions_verbes.py
    python3 scripts/preparer_definitions_verbes.py --verifier
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEXIQUE = ROOT / "data" / "source" / "lexique-soninke-fr-base.csv"
DOCUMENT = ROOT / "data" / "grammaire" / "soninke.yaml"
REDIGEES = ROOT / "data" / "source" / "definitions-redigees.csv"
SORTIE_CSV = ROOT / "data" / "candidates" / "definitions-verbes-2026-10-24.csv"
SORTIE_MD = ROOT / "docs" / "DEFINITIONS-VERBES-A-VALIDER.md"
DATE = "2026-10-24"

COLONNES = [
    "forme",
    "id_lexique",
    "glose_actuelle",
    "categorie",
    "statut_lexique",
    "definition_proposee",
    "provenance_definition",
    "statut_validation",
    "note_definition",
    "piste_glose_anglaise",
    "exemple_soninke",
    "exemple_francais",
    "source_exemple",
    "action",
    "risque_doublon",
]

PROVENANCE = "définition rédigée d'après la glose française attestée du lexique"


def charger_cle():
    """Réutilise la normalisation anti-doublon du script d'import."""
    chemin = ROOT / "scripts" / "import_extraction_sans_doublons.py"
    spec = importlib.util.spec_from_file_location("_import", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cle


# ── Lecture du document ─────────────────────────────────────

def lire_verbes_document(chemin: Path) -> list[dict]:
    lignes = chemin.read_text(encoding="utf-8").split("\n")
    debut = next(i for i, l in enumerate(lignes) if l.strip() == "verbes:")
    verbes, courant = [], None
    for ligne in lignes[debut + 1 :]:
        if not ligne.strip():
            continue
        if not ligne.startswith(" "):
            break
        entete = re.match(r"^  (\S.*?):\s*(?:#\s*(.*))?$", ligne)
        if entete:
            if courant:
                verbes.append(courant)
            courant = {"cle": entete.group(1).strip(), "props": {}, "commentaires": []}
            continue
        propriete = re.match(r"^    ([a-z_]+):\s*(.*?)\s*$", ligne)
        if propriete and courant is not None:
            valeur = propriete.group(2)
            commentaire = ""
            if "#" in valeur:
                valeur, commentaire = valeur.split("#", 1)
            valeur = valeur.strip().strip('"')
            if valeur:
                courant["props"][propriete.group(1)] = valeur
            if commentaire.strip():
                courant["commentaires"].append(commentaire.strip())
    if courant:
        verbes.append(courant)
    return [v for v in verbes if v["props"].get("forme")]


def lire_definitions_redigees(chemin: Path) -> dict[str, dict]:
    """Définitions rédigées à la main, indexées par forme soninké."""
    if not chemin.exists():
        return {}
    with chemin.open(encoding="utf-8", newline="") as flux:
        return {
            ligne["soninke"].strip(): ligne
            for ligne in csv.DictReader(flux, delimiter=";")
            if (ligne.get("soninke") or "").strip()
        }


# ── Analyse du texte de dictionnaire ────────────────────────

MOTS_FR = set(
    "le la les de des du un une est sont était dans pour avec chez son sa ses qui que ne pas "
    "plus très il elle nous vous ils elles on au aux ce cette ces sur sous par mais ou et à "
    "tout tous toute sans être avoir fait faire dit dire va aller peut deux trois leur leurs "
    "lui y en se mon ma mes ton ta tes notre votre comme aussi bien fois quand cela "
    "pourquoi comment où qui quoi moi toi je tu me te encore jamais toujours rien "
    "personne chose est-ce".split()
)
MOTS_EN = set(
    "the a an is are was were of to in for with his her their they he she it this that "
    "not but and from be been on at as by or".split()
)


def sans_accents(texte: str) -> str:
    decompose = unicodedata.normalize("NFD", texte)
    return "".join(c for c in decompose if unicodedata.category(c) != "Mn")


def langue(phrase: str) -> str:
    """Français / anglais / soninké, d'après les mots-outils et les accents.

    Les mots à apostrophe (n', l', s', d'…) ne comptent pas : ils existent dans
    les deux langues et ne distinguent rien.
    """
    tous = re.findall(r"[a-zà-ÿ']+", phrase.lower())
    mots = [m for m in tous if "'" not in m]
    if not mots:
        return "?"
    fr = sum(1 for m in mots if sans_accents(m) in MOTS_FR)
    # Terminaisons verbales françaises, quasi absentes du soninké.
    fr += sum(1 for m in mots if re.search(r"(?:ait|ais|aient|ons|ez|ée?s?|ant)$", m) and len(m) > 4)
    en = sum(1 for m in mots if m in MOTS_EN)
    accent = bool(re.search(r"[àâçéèêëîïôùûüœ]", phrase))
    if fr > en and (fr >= 2 or (accent and fr >= 1)):
        return "FR"
    if en > fr and en >= 2:
        return "EN"
    return "SNK"


METADONNEES = re.compile(
    r"^(?:[a-zà-ÿɲŋ'-]+ )?(?:variant|variantes?|compare|summary-definition|see main entry|synonyme|similaire|"
    r"plural suffix|underlying form|category|gram|note|fusion|renvoi|projet_status|"
    r"\d+ •|[a-zà-ÿɲŋ'-]+ (?:nom|verbe|adjectif|adverbe|interjection)\b)",
    re.I,
)


def phrases(texte: str) -> list[str]:
    texte = re.split(r"\bGram:|\bNote:|Plural suffix|Underlying form|\bCategory:|synonyme:", texte or "")[0]
    # Certains blocs collent deux langues sans espace après le point
    # (« … place.Binta est allée… ») : on coupe aussi devant une majuscule.
    return [p.strip() for p in re.split(r"(?<=[.!?])(?:\s+|(?=[A-ZÀ-Ý]))", texte) if p.strip()]


def glose_anglaise(entree: dict) -> str:
    """Partie anglaise de la ligne de glose, conservée comme piste pour le référent.

    Elle n'est jamais traduite ici : la traduire reviendrait à écrire une
    définition que personne n'a validée. Dans « exit; sortir », c'est le segment
    qui n'est pas français qui est retenu.
    """
    for phrase in phrases(entree.get("exemple_original") or ""):
        if ";" not in phrase:
            continue
        segments = [s.strip() for s in phrase.split(";") if s.strip()]
        langues = [langue(segment) for segment in segments]
        if "FR" in langues and len(segments) >= 2:
            for segment, code in zip(segments, langues):
                if code != "FR" and re.fullmatch(r"[A-Za-z][A-Za-z ,()'-]{2,60}", segment):
                    return segment.rstrip(".")
    return ""


def exemple_atteste(corpus: list[dict], forme: str, identifiant: str, limite: int = 2) -> list[dict]:
    # Comparaison sans replier les accents : « bonté » (français) ne doit pas
    # passer pour « bonte » (soninké).
    motif = re.compile(r"\b" + re.escape(forme) + r"\b", re.I)
    trouves = []
    for entree in corpus:
        if entree["id"] == identifiant or not entree.get("exemple_original"):
            continue
        if re.search(r"gerondif|nom_d_action", entree.get("categorie") or ""):
            continue
        if not motif.search(entree["exemple_original"]):
            continue
        bloc = [p for p in phrases(entree["exemple_original"]) if not METADONNEES.match(p)]
        # Une ligne de glose (« exit; sortir ») n'est pas une phrase d'emploi.
        contenant = [p for p in bloc if motif.search(p) and len(p.split()) >= 3 and ";" not in p]
        soninke = next((p for p in contenant if langue(p) in ("SNK", "?")), "")
        francais = next(
            (p for p in bloc if langue(p) == "FR" and not motif.search(p) and ";" not in p), ""
        )
        if soninke and len(soninke.split()) >= 3 and not METADONNEES.match(soninke) \
                and "summary-definition" not in soninke.lower():
            trouves.append({"soninke": soninke, "francais": francais, "source": entree["id"]})
        if len(trouves) >= limite:
            break
    return trouves


# ── Assemblage ──────────────────────────────────────────────

def construire() -> tuple[list[dict], dict]:
    cle = charger_cle()
    with LEXIQUE.open(encoding="utf-8") as flux:
        corpus = [l for l in csv.DictReader(flux, delimiter=";") if l.get("id")]

    entrees: dict[str, list[dict]] = {}
    variantes: dict[str, list[dict]] = {}
    for entree in corpus:
        entrees.setdefault(cle(entree["soninke"]), []).append(entree)
        for variante in (entree.get("variantes") or "").split(","):
            if variante.strip():
                variantes.setdefault(cle(variante), []).append(entree)

    redigees = lire_definitions_redigees(REDIGEES)
    lignes = []
    for verbe in lire_verbes_document(DOCUMENT):
        forme = verbe["props"]["forme"]
        glose_document = verbe["props"].get("fr", "")
        candidates = entrees.get(cle(forme), [])
        entree = max(
            candidates,
            key=lambda e: (cle(glose_document) in cle(e.get("francais", "")), len(e.get("francais") or "")),
        ) if candidates else None

        if entree is None:
            lignes.append(
                {
                    "forme": forme,
                    "id_lexique": "—",
                    "glose_actuelle": glose_document,
                    "categorie": "",
                    "statut_lexique": "",
                    "definition_proposee": "",
                    "provenance_definition": "aucune",
                    "statut_validation": "a_completer_par_referent",
                    "note_definition": "",
                    "piste_glose_anglaise": "",
                    "exemple_soninke": "",
                    "exemple_francais": "",
                    "source_exemple": "",
                    "action": "a_creer_apres_validation",
                    "risque_doublon": "forme absente du lexique : création à valider",
                }
            )
            continue

        redigee = redigees.get(forme, {})
        definition = (redigee.get("definition") or "").strip()
        statut = (redigee.get("statut") or "").strip() or "a_completer_par_referent"

        exemples = exemple_atteste(corpus, forme, entree["id"])
        premiere = exemples[0] if exemples else {"soninke": "", "francais": "", "source": ""}

        action = "enrichir_definition" if definition else "rediger_definition"

        risque = "aucun : entrée existante"
        if cle(forme) in variantes and not candidates:
            risque = "forme citée comme variante : ne pas créer d'entrée"

        lignes.append(
            {
                "forme": forme,
                "id_lexique": entree["id"],
                "glose_actuelle": entree.get("francais") or "",
                "categorie": entree.get("categorie", ""),
                "statut_lexique": entree.get("statut", ""),
                "definition_proposee": definition,
                "provenance_definition": PROVENANCE if definition else "aucune",
                "statut_validation": statut,
                "note_definition": (redigee.get("note") or "").strip(),
                "piste_glose_anglaise": glose_anglaise(entree),
                "exemple_soninke": premiere["soninke"],
                "exemple_francais": premiere["francais"],
                "source_exemple": premiere["source"],
                "action": action,
                "risque_doublon": risque,
            }
        )

    lignes.sort(key=lambda l: l["forme"])
    resume = {
        "verbes": len(lignes),
        "entrees_existantes": sum(1 for l in lignes if l["id_lexique"] != "—"),
        "a_creer": sum(1 for l in lignes if l["action"] == "a_creer_apres_validation"),
        "definition_redigee": sum(1 for l in lignes if l["definition_proposee"]),
        "glose_a_clarifier": sum(1 for l in lignes if l["statut_validation"] == "a_clarifier"),
        "definition_manquante": sum(1 for l in lignes if not l["definition_proposee"]),
        "avec_exemple": sum(1 for l in lignes if l["exemple_soninke"]),
    }
    return lignes, resume


def ecrire_csv(lignes: list[dict]) -> Path:
    SORTIE_CSV.parent.mkdir(parents=True, exist_ok=True)
    with SORTIE_CSV.open("w", encoding="utf-8", newline="") as flux:
        ecrivain = csv.DictWriter(flux, fieldnames=COLONNES, delimiter=";")
        ecrivain.writeheader()
        for ligne in lignes:
            ecrivain.writerow({c: ligne[c] for c in COLONNES})
    return SORTIE_CSV


def _cellule(texte: str) -> str:
    return (texte or "").replace("|", "\\|")


def ecrire_markdown(lignes: list[dict], resume: dict) -> Path:
    a_clarifier = [l for l in lignes if l["statut_validation"] == "a_clarifier"]
    textes = [
        "# Définitions des verbes du document soninké — à valider par le référent",
        "",
        "Document source : [Google Doc du référent](https://docs.google.com/document/d/1L0ykGjJPnOaFJYF6xtdAAqozt0qU2nBBEChgwGWNuA4/edit) "
        "(`data/grammaire/soninke.yaml`). Définitions du " + DATE + ".",
        "",
        "## Ce que montre le travail",
        "",
        "| Constat | Nombre |",
        "| --- | --- |",
        f"| Verbes du document | **{resume['verbes']}** |",
        f"| Déjà présents dans le lexique (entrée existante) | **{resume['entrees_existantes']}** |",
        f"| À créer comme nouvelle entrée | **{resume['a_creer']}** |",
        f"| Définition rédigée et proposée | **{resume['definition_redigee']}** |",
        f"| dont glose du lexique à trancher d'abord | **{resume['glose_a_clarifier']}** |",
        f"| Définition encore à écrire | **{resume['definition_manquante']}** |",
        f"| Avec au moins une phrase d'emploi attestée | **{resume['avec_exemple']}** |",
        "",
        "**Aucune entrée créée : les 182 verbes ont déjà leur entrée de lexique.** Chaque "
        "définition est ajoutée à une entrée existante, jamais à une ligne nouvelle — "
        "c'est ce qui garantit l'absence de doublon.",
        "",
        "## Comment les définitions sont écrites",
        "",
        "Chaque définition est rédigée en français à partir de la glose déjà attestée dans "
        "le lexique (`francais`) et, quand elle existe, de la ligne de glose anglaise de la "
        "source. Aucune définition n'ajoute un sens que ces sources ne portent pas : les cas "
        "douteux sont marqués `a_clarifier` et expliqués dans la note, au lieu d'être "
        "tranchés arbitrairement.",
        "",
        "Les définitions sont rédigées dans `data/source/definitions-redigees.csv`, "
        "jointes ici par `scripts/preparer_definitions_verbes.py`, puis écrites dans la "
        "colonne `definition` des entrées existantes par "
        "`scripts/enrichir_definitions_sans_doublons.py`.",
        "",
        "## Règle anti-doublon appliquée",
        "",
        "1. La forme est cherchée dans les entrées **et** dans les variantes, avec la "
        "comparaison du projet (`scripts/import_extraction_sans_doublons.py`) : casse, "
        "accents vocaliques, traits d'union, apostrophes et numéros d'homonyme ignorés ; "
        "`ñ`, `ŋ`, `ɲ` restent distincts.",
        "2. Si la forme est déjà une entrée : la définition enrichit cette entrée, jamais "
        "une nouvelle ligne.",
        "3. Si la forme n'est citée que comme variante : aucune création, la ligne porte "
        "`risque_doublon = forme citée comme variante`.",
        "4. Le script d'application refuse toute forme qui n'est pas déjà une entrée, "
        "refuse d'ajouter une ligne, puis relance `check_doublons_lexique.py --strict`.",
        "",
        "## Points à trancher par le référent",
        "",
        f"{len(a_clarifier)} verbes ont une définition proposée, mais leur glose de départ "
        "est incertaine ou contradictoire. Ils ne doivent pas être utilisés comme "
        "traduction sûre avant arbitrage.",
        "",
    ]

    if a_clarifier:
        textes += [
            "| Soninké | Glose du lexique | Définition proposée | Ce qui bloque | Entrée |",
            "| --- | --- | --- | --- | --- |",
        ]
        for ligne in a_clarifier:
            textes.append(
                f"| **{ligne['forme']}** | {_cellule(ligne['glose_actuelle'])} | "
                f"{_cellule(ligne['definition_proposee'])} | {_cellule(ligne['note_definition'])} | "
                f"`{ligne['id_lexique']}` |"
            )
    else:
        textes.append("*Aucun : toutes les gloses de départ sont claires.*")

    textes += [
        "",
        "## Les 182 définitions, verbe par verbe",
        "",
        "Ordre alphabétique soninké. « Emploi attesté » donne une phrase du corpus quand il "
        "en existe une, avec sa traduction française d'origine quand la source la fournit.",
        "",
        "| Soninké | Traduction (glose du lexique) | Définition | Emploi attesté | Entrée |",
        "| --- | --- | --- | --- | --- |",
    ]
    for ligne in lignes:
        emploi = ligne["exemple_soninke"] or "—"
        if ligne["exemple_francais"]:
            emploi += f" — « {ligne['exemple_francais']} »"
        if ligne["source_exemple"]:
            emploi += f" (`{ligne['source_exemple']}`)"
        statut = " ⚠" if ligne["statut_validation"] == "a_clarifier" else ""
        textes.append(
            f"| **{ligne['forme']}**{statut} | {_cellule(ligne['glose_actuelle'])} | "
            f"{_cellule(ligne['definition_proposee']) or '—'} | {_cellule(emploi)} | "
            f"`{ligne['id_lexique']}` |"
        )

    textes += [
        "",
        "## Fichiers liés",
        "",
        f"- `{REDIGEES.relative_to(ROOT)}` — définitions rédigées, source de ce document",
        f"- `{SORTIE_CSV.relative_to(ROOT)}` — mêmes données, lisibles par machine",
        "- `scripts/enrichir_definitions_sans_doublons.py` — application sans création de ligne",
        "- `scripts/check_doublons_lexique.py` — contrôle des doublons",
        "- `docs/MOTS-DOCUMENT-SONINKE.md` — inventaire complet des formes du document",
        "- `docs/LINGUISTIC-QUALITY.md` — règles d'attestation",
        "",
    ]

    SORTIE_MD.write_text("\n".join(textes), encoding="utf-8")
    return SORTIE_MD


def verifier(lignes: list[dict], resume: dict) -> int:
    problemes = []
    for ligne in lignes:
        if ligne["action"] == "a_creer_apres_validation":
            problemes.append(f"{ligne['forme']} : absente du lexique (création interdite)")
        if not ligne["definition_proposee"]:
            problemes.append(f"{ligne['forme']} : aucune définition")
        if ligne["definition_proposee"] and ligne["provenance_definition"] == "aucune":
            problemes.append(f"{ligne['forme']} : définition sans provenance")

    redigees = lire_definitions_redigees(REDIGEES)
    with LEXIQUE.open(encoding="utf-8", newline="") as flux:
        formes_lexique = {
            ligne["soninke"].strip() for ligne in csv.DictReader(flux, delimiter=";") if ligne.get("id")
        }
    for forme in sorted(set(redigees) - formes_lexique):
        problemes.append(f"{forme} : définition rédigée pour une forme absente du lexique")

    if problemes:
        print("✖ " + "\n✖ ".join(problemes), file=sys.stderr)
        return 1

    print(f"✔ {resume['verbes']} verbes, {resume['definition_redigee']} définitions rédigées, "
          f"0 entrée à créer, 0 définition manquante.")
    return 0


def main() -> int:
    analyseur = argparse.ArgumentParser()
    analyseur.add_argument("--verifier", action="store_true", help="contrôle sans réécrire les fichiers")
    options = analyseur.parse_args()

    lignes, resume = construire()
    for nom, valeur in resume.items():
        print(f"{nom:22} {valeur}")

    if options.verifier:
        return verifier(lignes, resume)

    if resume["a_creer"]:
        print(
            "✖ formes absentes du lexique : " + ", ".join(
                l["forme"] for l in lignes if l["action"] == "a_creer_apres_validation"
            ),
            file=sys.stderr,
        )
        return 1

    print(f"→ {ecrire_csv(lignes).relative_to(ROOT)}")
    print(f"→ {ecrire_markdown(lignes, resume).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
