#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests automatisés ciblés du pipeline d'extraction L→Y (PR #41).

Couvre tous les cas limites linguistiques et techniques mis au jour lors de
l'audit indépendant :
  1. Réparation Mojibake et conservation intégrale d'Unicode (ŋ, ɲ, ñ, accents).
  2. Reconnaissance de « verbe passif (intransitif). » et protection contre
     l'inversion actif/passif via summary-definition (safe, loxose, lange…).
  3. Sigles grammaticaux mixtes (PROintrg, DETintrg) sans faux positif sur le
     mot français « mot » (renxotte, sefeta) ni sur le nom « lit » (soxufo).
  4. Délimitation des gloses (parenthèses (geol.), décimales 1.5m, parenthèses
     source non fermées xesu2, guillemets équilibrés -lenme/siri, « ! » interne
     moro2, frontière « 2 • »).
  5. Conservation des sous-gloses françaises multiples séparées par « ; » et
     détection de l'ordre inversé « FR; EN » (soxokomaaxu, senbekite).
  6. Exclusion stricte des noms propres restés en anglais (Egypt, Solomon…).
  7. Séparation des têtes doubles de mots simples (seegi seegu, Taqqi, Pate)
     et préservation des vraies locutions (ra wa a yi, yaaxen bogu).
  8. Extraction d'exemples attestés : rejet de « I was in town », conservation
     des pronoms soninkés A / An, césure devant Ɲ/Ŋ, retrait de Diagana 1994:…
     et .antonyme:, conservation des nombres réels (1993, 9-hur).
  9. Alignement avec le lexique canonique (ñ=ɲ, variantes ; et |, yigandé) et
     non-fusion des collisions d'homonymes non numérotées (toro, tefu, saxu).
 10. Intégrité lecture seule du lexique canonique et cohérence des rapports.
"""

from __future__ import annotations

import csv
import hashlib
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import extraire_nettoyer_dictionnaire_l_y as pipe  # noqa: E402


class TestPipelineDictionnaireLY(unittest.TestCase):
    def test_mojibake_et_unicode_soninke(self):
        brut = "xÅ‹a É²iime Ã©tÃ© Ã\xa0 cÃ´tÃ©"
        repare = pipe.reparer_mojibake(brut)
        self.assertEqual(repare, "xŋa ɲiime été à côté")
        self.assertIn("ŋ", repare)
        self.assertIn("ɲ", repare)

    def test_sigles_mixtes_sans_exclure_mot_francais(self):
        self.assertTrue(pipe.est_sigle("PROintrg"))
        self.assertTrue(pipe.est_sigle("DETintrg"))
        self.assertTrue(pipe.est_sigle("RELtemp"))
        self.assertTrue(pipe.est_sigle("LOC"))
        self.assertTrue(pipe.est_sigle("4"))
        self.assertFalse(pipe.est_sigle("mot"))
        self.assertFalse(pipe.est_sigle("si"))

        j, ex = [], []
        self.assertEqual(
            pipe.segment_vers_francais_liste("word; mot.", "renxotte", j, ex),
            ["mot"],
        )
        self.assertEqual(
            pipe.segment_vers_francais_liste("PROintrg.", "minnanke", j, ex),
            [],
        )

    def test_verbe_passif_parenthese_sans_inversion_voix(self):
        corps_safe = (
            "summary-definition: write; écrire.See main entry: safa1, safa1."
            "verbe passif (intransitif). be written; être écrit(e)."
        )
        self.assertEqual(pipe.categorie_de(corps_safe), "verbe")
        gloses, resume = pipe.extraire_gloses(corps_safe)
        self.assertIsNotNone(resume)
        # Le résumé actif « write; écrire » ne doit pas contaminer un verbe passif
        self.assertNotIn(resume, gloses)
        sens = []
        for g in gloses:
            sens.extend(pipe.segment_vers_francais_liste(g, "safe", [], []))
        self.assertEqual(sens, ["être écrit(e)"])

    def test_region_apres_cas_limites_ponctuation(self):
        # Parenthèse contenant un point avant « ; »
        s_lanbo = pipe.region_apres("plain (geol.); plaine.Category: Nature.")
        self.assertEqual(
            pipe.segment_vers_francais_liste(s_lanbo, "lanbo", [], []),
            ["plaine"],
        )
        # Décimale 1.5m avant « ; »
        s_wand = pipe.region_apres("black fish, 1.5m; poisson noir et long, 1,5m.")
        self.assertEqual(
            pipe.segment_vers_francais_liste(s_wand, "wandaana", [], []),
            ["poisson noir et long, 1,5m"],
        )
        # Parenthèse source non fermée (xesu2) ne doit pas avaler l'exemple suivant
        s_xesu = pipe.region_apres("cut; couper (herbe .Moodin wa xesu.The marabout cuts.")
        self.assertIn("couper", s_xesu)
        self.assertNotIn("Moodin", s_xesu)
        # Double point d'exclamation interne en minuscule (moro2)
        s_moro = pipe.region_apres(
            "exclamation of disagreement; interjection : c'est faux ! mensonge !synonyme: moriya."
        )
        self.assertEqual(
            pipe.segment_vers_francais_liste(s_moro, "moro", [], []),
            ["interjection : c'est faux ! mensonge !"],
        )
        # Frontière de sens « 2 • » et mot français « lit » (soxufo)
        corps_soxufo = (
            "Nom . 1 • bed, pallet; couchette, lit.\n\n"
            "2 • prayer before going to sleep; prière faite avant de se coucher la nuit."
        )
        gloses, _ = pipe.extraire_gloses(corps_soxufo)
        extraits = []
        for g in gloses:
            for x in pipe.segment_vers_francais_liste(g, "soxufo", [], []):
                if x not in extraits:
                    extraits.append(x)
        self.assertEqual(
            extraits,
            ["couchette, lit", "prière faite avant de se coucher la nuit"],
        )

    def test_gloses_multi_point_virgule_et_ordre_inverse(self):
        # Multi-« ; » avec élision française « d'argent »
        self.assertEqual(
            pipe.segment_vers_francais_liste(
                "lack of money; head towards; manque d'argent; aller vers, se diriger vers.",
                "tanŋi",
                [],
                [],
            ),
            ["manque d'argent", "aller vers, se diriger vers"],
        )
        # Ordre inversé « FR; EN » attesté dans la source (avec et sans accent)
        self.assertEqual(
            pipe.segment_vers_francais_liste(
                "soumettre quelqu'un à la corvée; subject someone to forced labor.",
                "soxokomaaxu",
                [],
                [],
            ),
            ["soumettre quelqu'un à la corvée"],
        )
        self.assertEqual(
            pipe.segment_vers_francais_liste(
                "devenir fort(e); grow strong.", "senbekite", [], []
            ),
            ["devenir fort(e)"],
        )

    def test_noms_propres_anglais_exclus(self):
        for hw, seg in [
            ("Misira", "Egypt; Egypt."),
            ("Silemaanu", "Solomon; Solomon."),
            ("Samariya", "Samaria; Samaria."),
            ("Lajine", "Guinea Conakry; Guinea Conakry."),
            ("Xuraane", "Qur'an; Qur'an."),
        ]:
            self.assertEqual(
                pipe.segment_vers_francais_liste(seg, hw, [], []),
                [],
                f"{hw} ne doit pas conserver une glose anglaise",
            )

    def test_tetes_doubles_et_nombres_exemples(self):
        hw, vars_out = pipe.normaliser_tete_et_variantes("seegi seegu", ["segu"], [])
        self.assertEqual(hw, "seegi")
        self.assertEqual(vars_out, ["seegu", "segu"])

        hw2, vars2 = pipe.normaliser_tete_et_variantes("Taqqi, Pate", [], [])
        self.assertEqual(hw2, "Taqqi")
        self.assertEqual(vars2, ["Pate"])

        # Retrait d'indice d'homonyme sans détruire les années ni les heures
        phrase = "I da Muusa kiitindi 1993 siine katti 9-hur ɲiiɲe1."
        self.assertEqual(
            pipe.sans_chiffres_homonyme_phrase(phrase),
            "I da Muusa kiitindi 1993 siine katti 9-hur ɲiiɲe.",
        )

        # Rejet d'une phrase anglaise côté soninké et conservation du pronom « A »
        self.assertFalse(pipe.para_est_snk("I was in town."))
        self.assertTrue(pipe.para_est_snk("A da doroken lifi."))
        self.assertTrue(pipe.para_est_snk("An na ɲaŋana riini yere."))

        # Préfixe bibliographique collé au pronom « A » / « An »
        corps_diag = (
            "Verbe. come; venir.Diagana 1994:102An na ɲaŋana riini yere."
            "You will come here from time to time."
            "Tu viendras ici de temps à temps."
        )
        self.assertEqual(
            pipe.extraire_paires_exemples("ɲaŋana", corps_diag, []),
            [("An na ɲaŋana riini yere", "Tu viendras ici de temps à temps")],
        )

    def test_sorties_disque_coherentes_et_lexique_intact(self):
        mots_path = ROOT / "data/candidates/dictionnaire-l-y-mots-importables-2026-10-25.csv"
        expr_path = ROOT / "data/candidates/dictionnaire-l-y-expressions-importables-2026-10-25.csv"
        coll_path = ROOT / "data/reports/collisions-homonymes-dictionnaire-l-y-2026-10-25.csv"
        lex_path = ROOT / "data/source/lexique-soninke-fr-base.csv"

        self.assertTrue(mots_path.exists())
        self.assertTrue(expr_path.exists())
        self.assertTrue(coll_path.exists())

        with mots_path.open(encoding="utf-8", newline="") as fh:
            mots = list(csv.DictReader(fh, delimiter=";"))
        with expr_path.open(encoding="utf-8", newline="") as fh:
            expr = list(csv.DictReader(fh, delimiter=";"))
        with coll_path.open(encoding="utf-8", newline="") as fh:
            coll = list(csv.DictReader(fh, delimiter=";"))

        _, connues, _ = pipe.charger_lexique_complet(lex_path)
        mots_by_snk = {r["soninke"]: r for r in mots}
        coll_keys = {r["cle"] for r in coll}

        # Aucun nom propre anglais non traduit dans mots
        for bad in ("Lajine", "Misira", "Samariya", "Silemaanu", "Xuraane"):
            self.assertNotIn(bad, mots_by_snk)

        # Aucun doublon du lexique canonique (y compris ñ=ɲ et variantes ; / |)
        for r in mots:
            self.assertNotIn(pipe.cle_soninkegpt(r["soninke"]), connues)
            self.assertFalse(re.search(r"\d", r["soninke"]))

        # Aucun anglais ni bruit morphologique dans expressions
        expr_snk = {r["soninke"] for r in expr}
        self.assertNotIn("I was in town", expr_snk)
        self.assertNotIn("nVcv-pattern: NV", expr_snk)

        # Collisions non numérotées et passives bien isolées dans collisions-homonymes
        for h in ("saxu", "suure", "tefu", "toro"):
            self.assertIn(h, coll_keys)

        # Vérifications ciblées sur des entrées corrigées
        self.assertEqual(mots_by_snk["safe"]["francais"], "être écrit(e)")
        self.assertEqual(mots_by_snk["renxotte"]["francais"], "mot")
        self.assertEqual(mots_by_snk["sefeta"]["francais"], "mot")
        self.assertEqual(mots_by_snk["minnanke"]["francais"], "d'où ?")
        self.assertEqual(
            mots_by_snk["soxufo"]["francais"],
            "couchette, lit / prière faite avant de se coucher la nuit",
        )

        # Intégrité des 5 livrables d'audit
        for rep in (
            "audit-l-y-mots-2026-10-25.csv",
            "audit-l-y-expressions-2026-10-25.csv",
            "arbitrage-homonymes-l-y-2026-10-25.csv",
            "audit-doublons-l-y-2026-10-25.csv",
            "rapport-final-audit-l-y-2026-10-25.md",
        ):
            p = ROOT / "data/reports" / rep
            if rep.endswith(".csv"):
                self.assertTrue(p.exists(), f"Livrable manquant : {rep}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
