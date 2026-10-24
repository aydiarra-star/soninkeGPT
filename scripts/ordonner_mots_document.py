#!/usr/bin/env python3
"""Ordonne tous les mots du document soninké et leur donne sens et définition.

Source : l'export du Google Doc du référent
(`docs.google.com/document/d/1L0ykGjJPnOaFJYF6xtdAAqozt0qU2nBBEChgwGWNuA4`),
dont le contenu est identique, ligne pour ligne, à `data/grammaire/soninke.yaml`
(même en-tête « Données linguistiques CONFIRMÉES », mêmes 12 pronoms, mêmes
entrées de `daga` à `wurebandi`). Le YAML local est donc la copie de travail.

Produit :

  data/reports/mots-document-ordonnes-<date>.csv
      un mot par ligne, dans l'ordre alphabétique soninké :
      forme ; type ; catégorie ; traduction ; définition ; exemple ;
      provenance de la définition ; statut ; entrée de lexique ; section.

  docs/MOTS-DOCUMENT-SONINKE.md
      index alphabétique complet (toutes les formes), puis une fiche par verbe
      avec sa définition complète, un exemple et ses formes dérivées.

Règles (voir docs/LINGUISTIC-QUALITY.md) :
  - la traduction vient du document, jamais d'une invention ;
  - la définition vient du lexique du projet (entrée citée) ou, à défaut, du
    document lui-même ;
  - ni l'un ni l'autre : « sens à préciser par le référent ».

Usage :
    python3 scripts/ordonner_mots_document.py
    python3 scripts/ordonner_mots_document.py --verifier
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEXIQUE = ROOT / "data" / "source" / "lexique-soninke-fr-base.csv"
SOURCE = ROOT / "data" / "grammaire" / "soninke.yaml"
RAPPORTS = ROOT / "data" / "reports"
DOC_MD = ROOT / "docs" / "MOTS-DOCUMENT-SONINKE.md"

DATE = "2026-10-24"
DOC_ID = "1L0ykGjJPnOaFJYF6xtdAAqozt0qU2nBBEChgwGWNuA4"

COLLATION = "abcdefghijklmnɲŋopqrstuwxy"
EQUIVALENCES = str.maketrans(
    {
        "ñ": "ɲ", "Ñ": "ɲ", "é": "e", "è": "e", "ê": "e", "ë": "e", "á": "a", "à": "a",
        "â": "a", "ä": "a", "í": "i", "ï": "i", "ó": "o", "ô": "o", "ö": "o", "ú": "u",
        "ù": "u", "û": "u", "ç": "c", "É": "e", "À": "a", "‘": "'", "’": "'",
    }
)

TEXTE_CORPUS: list[dict] = []   # toutes les entrées, pour y chercher des emplois

STATUT_AFFICHAGE = {
    "fourni_par_referent": "Attesté · référent",
    "valide_par_referent": "Attesté · référent",
    "valide_par_referent_linguistique": "Attesté · référent",
    "fourni_par_referent_a_verifier": "À confirmer · référent",
    "atteste_selon_referent_a_concilier": "À confirmer · référent",
    "atteste_selon_referent_a_verifier": "À confirmer · référent",
    "candidat_dictionnaire_a_verifier": "À vérifier · dictionnaire",
    "source_externe_a_verifier": "À vérifier · source externe",
    "atteste_source_externe": "Source externe",
    "atteste_source_externe_sens_a_preciser": "Source externe",
    "corrige_atteste_source_externe": "Source externe",
    "non_resolu_a_documenter": "Non résolu",
    "variante_probable_non_validee": "Variante non validée",
    "forme_non_attestee_a_reexaminer": "Forme non attestée",
    "hypothese_lexicale_a_valider": "Hypothèse à valider",
    "a_traduire": "Sens à préciser",
}


# ──────────────────────────────────────────────
#  Outils de tri et de normalisation
# ──────────────────────────────────────────────

def cle_tri(forme: str) -> tuple:
    """Tri alphabétique soninké, insensible aux traits d'union, espaces et apostrophes."""
    texte = forme.translate(EQUIVALENCES).lower()
    caracteres = []
    for caractere in texte:
        if caractere in (" ", "-", "'", "."):
            continue
        position = COLLATION.find(caractere)
        caracteres.append((position if position >= 0 else len(COLLATION), caractere))
    return (tuple(caracteres), texte)


def normaliser(texte: str) -> str:
    texte = unicodedata.normalize("NFD", str(texte or ""))
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    texte = texte.lower().translate(EQUIVALENCES)
    texte = re.sub(r"[0-9]+$", "", texte.strip())
    texte = re.sub(r"[^a-zɲŋ' -]", " ", texte)
    return re.sub(r"\s+", " ", texte).strip()


# ──────────────────────────────────────────────
#  Lecture du document
# ──────────────────────────────────────────────

@dataclass
class Mot:
    forme: str
    type_mot: str
    section: str
    traduction: str
    cle: str = ""
    proprietes: dict = field(default_factory=dict)
    commentaires: list = field(default_factory=list)


def _nettoyer(valeur: str) -> tuple[str, str]:
    """Sépare valeur et commentaire `# …` (hors guillemets)."""
    valeur = valeur.strip()
    if "#" not in valeur:
        return valeur.strip().strip('"'), ""
    avant, apres = valeur.split("#", 1)
    return avant.strip().strip('"'), apres.strip()


def _blocs(lignes: list[str], debut: int, fin: int) -> list[dict]:
    """Découpe une section en blocs `  clé:` + propriétés `    clé: valeur`."""
    blocs: list[dict] = []
    courant = None
    for ligne in lignes[debut:fin]:
        if not ligne.strip() or ligne.lstrip().startswith("#"):
            if courant is not None and ligne.strip().startswith("#"):
                commentaire = ligne.strip().lstrip("#").strip()
                if commentaire:
                    courant["commentaires"].append(commentaire)
            continue
        entete = re.match(r"^  (\S.*?):\s*(?:#\s*(.*))?$", ligne)
        if entete:
            courant = {
                "cle": entete.group(1).strip(),
                "proprietes": {},
                "commentaires": [entete.group(2).strip()] if entete.group(2) else [],
            }
            blocs.append(courant)
            continue
        propriete = re.match(r"^    ([a-z_]+):\s*(.*?)\s*$", ligne)
        if propriete and courant is not None:
            valeur, commentaire = _nettoyer(propriete.group(2))
            if valeur:
                courant["proprietes"][propriete.group(1)] = valeur
            if commentaire:
                courant["commentaires"].append(commentaire)
    return blocs


def lire_document(chemin: Path) -> tuple[list[Mot], list[str], int]:
    lignes = chemin.read_text(encoding="utf-8").split("\n")
    # Sections = clés en colonne 0 uniquement (les clés indentées sont des entrées)
    titres = [(i, l[:-1]) for i, l in enumerate(lignes) if re.match(r"^[a-zA-Z_]+:$", l)]
    bornes = {nom: (position, titres[rang + 1][0] if rang + 1 < len(titres) else len(lignes))
              for rang, (position, nom) in enumerate(titres)}

    mots: list[Mot] = []
    avertissements: list[str] = []
    compteurs = {"pronoms": 0, "temps": 0, "particules": 0, "verbes": 0}

    # Clés dupliquées dans une même section : un lecteur YAML strict n'en garde
    # qu'une, la dernière. On le signale au lieu de laisser croire à deux entrées.
    for nom, (debut, fin) in bornes.items():
        cles = [
            re.match(r"^  (\S.*?):\s*(?:#.*)?$", ligne).group(1).strip()
            for ligne in lignes[debut:fin]
            if re.match(r"^  (\S.*?):\s*(?:#.*)?$", ligne)
        ]
        vues = {cle for cle in cles if cles.count(cle) > 1}
        for cle in sorted(vues):
            avertissements.append(
                f"clé dupliquée dans la section « {nom} » : « {cle} » ({cles.count(cle)} occurrences) — "
                "un lecteur YAML strict ne garde que la dernière"
            )

    # Pronoms : liste en ligne `- {forme: …, fr: …}`
    if "pronoms" in bornes:
        debut, fin = bornes["pronoms"]
        for ligne in lignes[debut:fin]:
            trouve = re.match(r"^\s*-\s*\{(.+)\}\s*$", ligne)
            if not trouve:
                continue
            champs = dict(re.findall(r"(\w+):\s*([^,}]+)", trouve.group(1)))
            compteurs["pronoms"] += 1
            mots.append(
                Mot(
                    forme=champs.get("forme", "").strip(),
                    type_mot="pronom",
                    section="pronoms",
                    traduction=champs.get("fr", "").strip(),
                    proprietes={
                        "personne": champs.get("personne", "").strip(),
                        "serie": champs.get("serie", "").strip(),
                    },
                )
            )

    # Temps et aspects : un bloc par construction, un marqueur éventuel
    if "temps" in bornes:
        debut, fin = bornes["temps"]
        for bloc in _blocs(lignes, debut, fin):
            compteurs["temps"] += 1
            proprietes = bloc["proprietes"]
            marqueur = proprietes.get("marqueur", "").strip()
            if not marqueur or marqueur == "null":
                continue
            suffixe = proprietes.get("suffixe", "").strip()
            nom = proprietes.get("nom", bloc["cle"])
            mots.append(
                Mot(
                    forme=marqueur,
                    type_mot="marqueur",
                    section="temps",
                    traduction=nom,
                    proprietes={"temps": bloc["cle"], "suffixe": suffixe},
                    commentaires=bloc["commentaires"],
                )
            )
            if suffixe:
                mots.append(
                    Mot(
                        forme=suffixe,
                        type_mot="suffixe",
                        section="temps",
                        traduction=nom,
                        proprietes={"temps": bloc["cle"], "marqueur": marqueur},
                        commentaires=bloc["commentaires"],
                    )
                )

    # Particules
    if "particules" in bornes:
        debut, fin = bornes["particules"]
        par_initiale = re.match(r"^  par_initiale:$", "")
        for ligne in lignes[debut:fin]:
            initiale = re.match(r"^    ([a-z]):\s*(.*)$", ligne)
            if initiale:
                compteurs["particules"] += 1
                valeur, commentaire = _nettoyer(initiale.group(2))
                mots.append(
                    Mot(
                        forme=valeur,
                        type_mot="particule",
                        section="particules",
                        traduction=f"particule devant l'initiale « {initiale.group(1)} »",
                        proprietes={"initiale": initiale.group(1)},
                        commentaires=[commentaire] if commentaire else [],
                    )
                )
                continue
            defaut = re.match(r"^  defaut:\s*(.*)$", ligne)
            if defaut:
                compteurs["particules"] += 1
                valeur, commentaire = _nettoyer(defaut.group(1))
                mots.append(
                    Mot(
                        forme=valeur,
                        type_mot="particule",
                        section="particules",
                        traduction="particule par défaut (toute autre initiale)",
                        commentaires=[commentaire] if commentaire else [],
                    )
                )

    # Verbes et formes dérivées
    if "verbes" in bornes:
        debut, fin = bornes["verbes"]
        for bloc in _blocs(lignes, debut, fin):
            proprietes = bloc["proprietes"]
            compteurs["verbes"] += 1
            forme = proprietes.get("forme")
            if not forme:
                avertissements.append(f"entrée sans forme : {bloc['cle']}")
                continue
            traduction = proprietes.get("fr", "")
            mots.append(
                Mot(
                    forme=forme,
                    type_mot="verbe",
                    section="verbes",
                    traduction=traduction,
                    cle=bloc["cle"],
                    proprietes=proprietes,
                    commentaires=bloc["commentaires"],
                )
            )
            if proprietes.get("nom_action"):
                mots.append(
                    Mot(
                        forme=proprietes["nom_action"],
                        type_mot="nom d'action",
                        section="verbes",
                        traduction=f"{traduction} (nom d'action)",
                        cle=bloc["cle"],
                        proprietes={"verbe": forme},
                    )
                )
            if proprietes.get("gerondif"):
                mots.append(
                    Mot(
                        forme=proprietes["gerondif"],
                        type_mot="gérondif",
                        section="verbes",
                        traduction=f"{traduction} (gérondif)",
                        cle=bloc["cle"],
                        proprietes={"verbe": forme},
                    )
                )
    return mots, avertissements, compteurs


# ──────────────────────────────────────────────
#  Lexique : définition, exemple, statut
# ──────────────────────────────────────────────

def charger_lexique() -> dict[str, list[dict]]:
    with LEXIQUE.open(encoding="utf-8") as flux:
        lignes = list(csv.DictReader(flux, delimiter=";"))
    TEXTE_CORPUS.extend(lignes)
    index: dict[str, list[dict]] = {}
    for ligne in lignes:
        index.setdefault(normaliser(ligne["soninke"]), []).append(ligne)
        for variante in re.split(r"[|;,]", ligne.get("variantes") or ""):
            variante = variante.strip()
            if variante:
                index.setdefault(normaliser(variante), []).append(ligne)
    return index


POIDS = {
    "fourni_par_referent": 4,
    "valide_par_referent": 4,
    "valide_par_referent_linguistique": 4,
    "fourni_par_referent_a_verifier": 3,
    "atteste_selon_referent_a_concilier": 3,
    "atteste_selon_referent_a_verifier": 3,
    "candidat_dictionnaire_a_verifier": 2,
    "source_externe_a_verifier": 1,
}


def choisir_entree(candidats: list[dict], traduction: str) -> dict | None:
    if not candidats:
        return None
    cible = normaliser(traduction.split("(")[0])

    def score(entree: dict) -> tuple:
        glose = normaliser(entree.get("francais", ""))
        correspond = 2 if cible and cible in glose else 0
        force = max((POIDS.get(s.strip(), 0) for s in (entree.get("statut") or "").split(";")), default=0)
        return (correspond, force, len(glose))

    return max(candidats, key=score)


def statut_lisible(entree: dict | None) -> str:
    if entree is None:
        return "—"
    statuts = [s.strip() for s in (entree.get("statut") or "").split(";") if s.strip()]
    for statut in statuts:
        if statut in STATUT_AFFICHAGE:
            return STATUT_AFFICHAGE[statut]
    return "À vérifier"


def extrait_exemple(entree: dict, limite: int = 260) -> str:
    texte = re.sub(r"\s+", " ", entree.get("exemple_original") or "").strip()
    if not texte:
        return ""
    texte = re.split(r"\bGram:|\bNote:|Plural suffix|\bCategory:", texte)[0].strip()
    if len(texte) <= limite:
        return texte
    coupe = texte[:limite]
    return coupe[: coupe.rfind(" ")] + " […]"


def phrase_autour(texte: str, forme: str, suivantes: int = 2) -> str:
    """Isole la phrase du corpus qui contient le mot, avec sa traduction qui suit."""
    texte = re.sub(r"\s+", " ", texte).strip()
    phrases = re.split(r"(?<=[.!?])\s+", texte)
    motif = re.compile(r"\b" + re.escape(normaliser(forme)) + r"\b")
    for position, phrase in enumerate(phrases):
        if motif.search(normaliser(phrase)):
            bloc = " ".join(phrases[position : position + 1 + suivantes]).strip()
            if len(bloc) > 300:
                bloc = bloc[:300]
                bloc = bloc[: bloc.rfind(" ")] + " […]"
            return bloc
    return ""


def emplois_corpus(forme: str, identifiant: str, limite: int = 2) -> list[str]:
    """Phrases du corpus (exemples de dictionnaire, phrases parallèles) où le mot apparaît."""
    motif = re.compile(r"\b" + re.escape(normaliser(forme)) + r"\b")
    trouves: list[str] = []
    for entree in TEXTE_CORPUS:
        if entree["id"] == identifiant:
            continue
        if not entree.get("exemple_original"):
            continue
        # Les fiches de gérondif / nom d'action ne portent pas d'exemple : leur
        # champ « exemple » n'est qu'un renvoi étymologique.
        if re.search(r"gerondif|nom_d_action", entree.get("categorie") or ""):
            continue
        if not motif.search(normaliser(entree["exemple_original"])):
            continue
        extrait = phrase_autour(entree["exemple_original"], forme)
        if extrait and len(extrait) >= 30 and "du verbe «" not in extrait:
            trouves.append(f"{extrait} — {entree['id']}")
        if len(trouves) >= limite:
            break
    return trouves


COMMENTAIRES_TECHNIQUES = re.compile(
    r"formes françaises|pour la traduction du corpus|confirmé|serie_0|corp1|infinitif non confirmé", re.I
)


def definition_courte(texte: str, limite: int = 130) -> str:
    """Premier(s) sens de la glose ; la barre oblique du dictionnaire est conservée."""
    if not texte:
        return ""
    morceaux = [m.strip() for m in re.split(r";", texte) if m.strip()]
    court = " ; ".join(morceaux[:2])
    if len(court) > limite:
        court = court[:limite]
        court = court[: court.rfind(" ")] + "…"
    return court


# ──────────────────────────────────────────────
#  Assemblage
# ──────────────────────────────────────────────

COLONNES = [
    "ordre",
    "forme",
    "type",
    "categorie_lexique",
    "traduction_fr",
    "definition_et_sens",
    "provenance_definition",
    "exemple_source",
    "emplois_corpus",
    "statut",
    "entree_lexique",
    "section_document",
    "note",
]


def construire(source: Path) -> tuple[list[dict], list[str], dict]:
    mots, avertissements, compteurs = lire_document(source)
    index = charger_lexique()

    regroupes: dict[tuple, dict] = {}
    for mot in mots:
        cle = (normaliser(mot.forme), mot.type_mot)
        if cle in regroupes:
            existant = regroupes[cle]
            for temps in [mot.proprietes.get("temps")] if mot.proprietes.get("temps") else []:
                if temps not in existant["_temps"]:
                    existant["_temps"].append(temps)
            for commentaire in mot.commentaires:
                if commentaire and commentaire not in existant["_commentaires"]:
                    existant["_commentaires"].append(commentaire)
            continue
        regroupes[cle] = {
            "mot": mot,
            "_temps": [mot.proprietes.get("temps")] if mot.proprietes.get("temps") else [],
            "_commentaires": list(mot.commentaires),
        }

    lignes: list[dict] = []
    for (_, _), paquet in regroupes.items():
        mot: Mot = paquet["mot"]
        candidats = index.get(normaliser(mot.forme), [])
        entree = choisir_entree(candidats, mot.traduction)
        homographes = sorted({c["soninke"] for c in candidats if c is not entree})

        if entree is not None:
            definition = entree["francais"]
            provenance = "lexique du projet"
            exemple = extrait_exemple(entree)
            if not exemple:
                utiles = [c for c in paquet["_commentaires"] if not COMMENTAIRES_TECHNIQUES.search(c)]
                if utiles:
                    # À défaut d'exemple de dictionnaire, les exemples du document.
                    exemple = " / ".join(utiles[:2])
            statut = statut_lisible(entree)
            identifiant = entree["id"]
            categorie = entree["categorie"]
        else:
            # Définition issue du document lui-même (données confirmées du référent)
            morceaux = []
            utiles = [c for c in paquet["_commentaires"] if not COMMENTAIRES_TECHNIQUES.search(c)]
            if mot.type_mot == "suffixe":
                morceaux.append(
                    f"suffixe qui suit le verbe, avec le marqueur « "
                    f"{mot.proprietes.get('marqueur', '')} » ({mot.traduction})"
                )
            elif mot.proprietes.get("temps"):
                morceaux.append(f"marqueur de « {mot.traduction} »")
            if mot.proprietes.get("suffixe"):
                morceaux.append(f"se combine avec le suffixe « {mot.proprietes['suffixe']} »")
            if mot.proprietes.get("initiale"):
                morceaux.append(f"devant l'initiale « {mot.proprietes['initiale']} »")
            if mot.proprietes.get("personne"):
                morceaux.append(
                    f"pronom {mot.proprietes['personne']}, série {mot.proprietes.get('serie', '')}".strip()
                )
            if mot.type_mot == "suffixe" and utiles:
                morceaux.extend(utiles[:1])
            definition = " ; ".join(morceaux) or mot.traduction
            provenance = "document du référent"
            exemple = " / ".join(paquet["_commentaires"][:2])
            statut = "Document du référent"
            identifiant = "—"
            categorie = ""

        note = []
        if mot.type_mot == "verbe":
            if mot.cle and normaliser(mot.cle) != normaliser(mot.forme):
                note.append(f"clé de conjugaison du document : {mot.cle}")
            if mot.proprietes.get("transitif") == "true":
                note.append("verbe transitif")
            if mot.proprietes.get("forme_objet"):
                note.append(f"forme devant objet : {mot.proprietes['forme_objet']}")
            if mot.proprietes.get("gerondif_objet"):
                note.append(f"gérondif devant objet : {mot.proprietes['gerondif_objet']}")
        if mot.type_mot == "pronom":
            note.append(f"série {mot.proprietes.get('serie', '')}, {mot.proprietes.get('personne', '')}")
        if paquet["_temps"]:
            note.append("temps : " + ", ".join(paquet["_temps"]))
        if mot.proprietes.get("suffixe"):
            note.append(f"suffixe : {mot.proprietes['suffixe']}")
        if mot.proprietes.get("verbe"):
            note.append(f"dérivé du verbe {mot.proprietes['verbe']}")
        if homographes:
            note.append("homographe(s) dans le lexique : " + ", ".join(homographes))
        if entree is None:
            note.append("aucune entrée de lexique : définition tirée du document, pas d'invention")

        emplois = emplois_corpus(mot.forme, identifiant) if mot.type_mot == "verbe" else []

        lignes.append(
            {
                "emplois_corpus": " || ".join(emplois),
                "forme": mot.forme,
                "type": mot.type_mot,
                "categorie_lexique": categorie,
                "traduction_fr": mot.traduction,
                "definition_et_sens": definition,
                "provenance_definition": provenance,
                "exemple_source": exemple,
                "statut": statut,
                "entree_lexique": identifiant,
                "section_document": mot.section,
                "note": " ; ".join(note),
                "_proprietes": mot.proprietes,
                "_cle": mot.cle,
            }
        )

    # Gloses du lexique plus larges que la traduction du document : elles mêlent
    # parfois plusieurs homographes. On le signale sans jamais tronquer la glose.
    for ligne in lignes:
        if ligne["provenance_definition"] != "lexique du projet":
            continue
        sens = [m for m in re.split(r"\s/\s", ligne["definition_et_sens"]) if m.strip()]
        cible = normaliser(ligne["traduction_fr"].split("(")[0])
        if len(sens) >= 3 and not all(cible in normaliser(s) for s in sens):
            ligne["note"] = (ligne["note"] + " ; " if ligne["note"] else "") + (
                "glose du lexique plus large que la traduction du document "
                "(sens multiples, peut-être homographes) : à scinder"
            )
            avertissements.append(
                f"« {ligne['forme']} » : la glose du lexique couvre plusieurs sens "
                f"({len(sens)}) alors que le document ne donne que « {ligne['traduction_fr']} »"
            )

    # Contrôle : la traduction du document doit se retrouver dans la glose du
    # lexique retenue. Toute divergence est signalée, jamais corrigée en silence.
    divergences = []
    for ligne in lignes:
        if ligne["type"] != "verbe" or ligne["provenance_definition"] != "lexique du projet":
            continue
        cible = normaliser(ligne["traduction_fr"])
        if cible and cible not in normaliser(ligne["definition_et_sens"]):
            divergences.append(ligne["forme"])
            avertissements.append(
                f"« {ligne['forme']} » : le document dit « {ligne['traduction_fr']} », "
                f"la glose du lexique ne reprend pas ce mot"
            )

    lignes.sort(key=lambda ligne: (cle_tri(ligne["forme"]), ligne["type"]))
    for numero, ligne in enumerate(lignes, 1):
        ligne["ordre"] = numero
    return lignes, avertissements, compteurs


def ecrire_csv(lignes: list[dict]) -> Path:
    RAPPORTS.mkdir(parents=True, exist_ok=True)
    chemin = RAPPORTS / f"mots-document-ordonnes-{DATE}.csv"
    with chemin.open("w", encoding="utf-8", newline="") as flux:
        ecrivain = csv.DictWriter(flux, fieldnames=COLONNES, delimiter=";")
        ecrivain.writeheader()
        for ligne in lignes:
            ecrivain.writerow({cle: ligne[cle] for cle in COLONNES})
    return chemin


TITRES = {
    "suffixe": "suffixes",
    "verbe": "verbes",
    "nom d'action": "noms d'action",
    "gérondif": "gérondifs",
    "pronom": "pronoms",
    "marqueur": "marqueurs de temps et d'aspect",
    "particule": "particules",
}


def ecrire_markdown(lignes: list[dict], avertissements: list[str], compteurs: dict) -> Path:
    sections_lues = [
        f"{compteurs['pronoms']} pronoms",
        f"{compteurs['temps']} constructions de temps et d'aspect",
        f"{compteurs['particules']} particules",
        f"{compteurs['verbes']} verbes",
    ]
    sections = ", ".join(sections_lues)
    nb_entrees = sum(compteurs.values())

    par_type: dict[str, int] = {}
    par_provenance: dict[str, int] = {}
    for ligne in lignes:
        par_type[ligne["type"]] = par_type.get(ligne["type"], 0) + 1
        par_provenance[ligne["provenance_definition"]] = par_provenance.get(ligne["provenance_definition"], 0) + 1

    lettres: dict[str, list[dict]] = {}
    for ligne in lignes:
        initiale = ligne["forme"].translate(EQUIVALENCES)[:1].upper()
        lettres.setdefault(initiale, []).append(ligne)

    verbes = [l for l in lignes if l["type"] == "verbe"]
    derives: dict[str, list[dict]] = {}
    for ligne in lignes:
        if ligne["type"] in ("nom d'action", "gérondif"):
            derives.setdefault(ligne["_proprietes"].get("verbe", ""), []).append(ligne)

    doc = [
        "# Tous les mots du document soninké, ordonnés, avec traduction, sens et définition",
        "",
        f"Document du référent : [Google Doc `{DOC_ID}`]"
        f"(https://docs.google.com/document/d/{DOC_ID}/edit). "
        "La copie de travail `data/grammaire/soninke.yaml` reprend le document à "
        "l'identique : même en-tête « Données linguistiques CONFIRMÉES », mêmes "
        "12 pronoms, mêmes constructions de temps, mêmes entrées de `daga` "
        "(partir) à `wurebandi` (traduire).",
        "",
        f"Extraction du {DATE} : **{len(lignes)} formes** issues de **{nb_entrees} entrées** "
        f"du document ({sections}), classées dans l'ordre alphabétique soninké "
        "(a, b, c, d, e, f, g, h, i, j, k, l, m, n, ɲ, ŋ, o, p, q, r, s, t, u, w, x, y).",
        "",
        "## Ordre d'affichage",
        "",
        "```",
        "SONINKÉ ↓",
        "   ↓",
        "TRADUCTION FRANÇAISE — sens et définition — statut de la forme",
        "```",
        "",
        "| Élément | Contenu |",
        "| --- | --- |",
        "| **Traduction** | glose du document (`fr:`), reprise telle quelle |",
        "| **Sens et définition** | glose du lexique du projet, avec ses sens numérotés |",
        "| **Provenance** | `lexique du projet`, `document du référent` ou `—` (rien) |",
        "| **Statut** | `Attesté · référent`, `À vérifier · dictionnaire`, `Document du référent`, `—` |",
        "| **Entrée** | identifiant `SNK-…` du lexique, pour vérification directe |",
        "",
        "Répartition par type : "
        + " · ".join(f"{TITRES.get(t, t)} **{n}**" for t, n in sorted(par_type.items(), key=lambda x: -x[1]))
        + ".",
        "",
        "Provenance des définitions : "
        + " · ".join(f"{k} **{v}**" for k, v in sorted(par_provenance.items(), key=lambda x: -x[1]))
        + ".",
        "",
    ]

    if avertissements:
        doc += ["## Points de vigilance relevés à l'extraction", ""]
        for avertissement in avertissements:
            doc.append(f"- {avertissement}")
        doc.append("")

    doc += ["---", "", "## Index alphabétique", ""]
    doc.append(" · ".join(f"[{lettre}](#{lettre.lower()})" for lettre in lettres))
    doc.append("")

    for lettre, contenu in lettres.items():
        doc += [f"### {lettre}", ""]
        doc.append("| # | Soninké | Type | Traduction | Sens et définition | Statut | Entrée |")
        doc.append("| --- | --- | --- | --- | --- | --- | --- |")
        for ligne in contenu:
            definition = definition_courte(ligne["definition_et_sens"])
            doc.append(
                "| {ordre} | **{forme}** | {type} | {traduction} | {definition} | {statut} | {entree} |".format(
                    ordre=ligne["ordre"],
                    forme=ligne["forme"],
                    type=ligne["type"],
                    traduction=ligne["traduction_fr"] or "—",
                    definition=definition.replace("|", "\\|") or "*à préciser*",
                    statut=ligne["statut"],
                    entree=f"`{ligne['entree_lexique']}`" if ligne["entree_lexique"] != "—" else "—",
                )
            )
        doc.append("")
        doc.append(f"[↑ index](#index-alphabétique)")
        doc.append("")

    doc += [
        "---",
        "",
        "## Fiches des verbes : sens, définition et exemple",
        "",
        "Une fiche par verbe du document, avec sa définition complète, un exemple "
        "attesté quand il existe, et ses formes dérivées.",
        "",
    ]

    for verbe in verbes:
        doc += [f"#### {verbe['forme']} — {verbe['traduction_fr']}", ""]
        entete = [f"`{verbe['entree_lexique']}`", verbe["statut"]]
        if verbe["categorie_lexique"]:
            entete.append(verbe["categorie_lexique"])
        if verbe["_cle"] and normaliser(verbe["_cle"]) != normaliser(verbe["forme"]):
            entete.append(f"clé de conjugaison : {verbe['_cle']}")
        if verbe["_proprietes"].get("transitif") == "true":
            entete.append("transitif")
        doc.append(" · ".join(entete))
        doc.append("")
        doc.append(f"**Sens et définition** : {verbe['definition_et_sens']}")
        if verbe["exemple_source"]:
            doc.append("")
            doc.append(f"**Exemple** : {verbe['exemple_source']}")
        for emploi in [e for e in verbe["emplois_corpus"].split(" || ") if e]:
            doc.append("")
            doc.append(f"**Emploi attesté** : {emploi}")
        formes = derives.get(verbe["forme"], [])
        if formes:
            doc.append("")
            doc.append(
                "**Formes dérivées** : "
                + " · ".join(f"{f['forme']} ({f['type']})" for f in sorted(formes, key=lambda x: cle_tri(x["forme"])))
            )
        doc.append("")

    doc += [
        "---",
        "",
        "## Contrôles de qualité",
        "",
        f"- Formes extraites : **{len(lignes)}** ; entrées du document : **{nb_entrees}** "
        f"({sections}).",
        "- Traductions : toutes issues du document, aucune reformulée.",
        "- Définitions : toutes issues du lexique du projet ou, à défaut, du document ; "
        "aucune glose inventée.",
        "- Homographes signalés en note, jamais fusionnés.",
        f"- Verbes avec un exemple dans leur entrée : **{sum(1 for l in verbes if l['exemple_source'])}** "
        f"sur **{len(verbes)}**.",
        f"- Verbes avec au moins une phrase d'emploi attestée dans le corpus : "
        f"**{sum(1 for l in verbes if l['emplois_corpus'])}** sur **{len(verbes)}**.",
        "- Verbes sans gérondif dans le document : "
        + (
            ", ".join(
                f"`{l['forme']}`"
                for l in verbes
                if not any(d["_proprietes"].get("verbe") == l["forme"] and d["type"] == "gérondif" for d in lignes)
            )
            or "aucun"
        )
        + ".",
        "- Doublons de clé du document signalés ci-dessus.",
        "",
        "## Fichiers liés",
        "",
        f"- `data/reports/mots-document-ordonnes-{DATE}.csv` — mêmes données, lisibles par machine",
        "- `data/grammaire/soninke.yaml` — copie de travail du document du référent",
        "- `data/source/lexique-soninke-fr-base.csv` — lexique des définitions",
        "- `scripts/ordonner_mots_document.py` — extraction et contrôle",
        "- `docs/LINGUISTIC-QUALITY.md` — règles d'attestation",
        "",
    ]

    DOC_MD.write_text("\n".join(doc), encoding="utf-8")
    return DOC_MD


def main() -> int:
    analyseur = argparse.ArgumentParser()
    analyseur.add_argument("--source", type=Path, default=SOURCE)
    analyseur.add_argument("--verifier", action="store_true", help="contrôle sans réécrire les fichiers")
    options = analyseur.parse_args()

    if not options.source.exists():
        print(f"✖ source introuvable : {options.source}", file=sys.stderr)
        return 1

    lignes, avertissements, compteurs = construire(options.source)
    sans_definition = [l for l in lignes if not l["definition_et_sens"]]
    verbes_sans_entree = [l for l in lignes if l["type"] == "verbe" and l["entree_lexique"] == "—"]

    print(f"Formes extraites : {len(lignes)}")
    for type_mot, nombre in sorted(
        ((t, sum(1 for l in lignes if l["type"] == t)) for t in {l["type"] for l in lignes}),
        key=lambda x: -x[1],
    ):
        print(f"  {type_mot:16} {nombre:4}")
    print(f"Sans définition : {len(sans_definition)}")
    print(f"Verbes sans entrée de lexique : {len(verbes_sans_entree)}")
    for avertissement in avertissements:
        print(f"⚠ {avertissement}")

    if options.verifier:
        if sans_definition or verbes_sans_entree:
            print("✖ des formes restent sans définition", file=sys.stderr)
            return 1
        print("✔ Toutes les formes ont une traduction et une définition sourcées.")
        return 0

    print(f"→ {ecrire_csv(lignes).relative_to(ROOT)}")
    print(f"→ {ecrire_markdown(lignes, avertissements, compteurs).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
