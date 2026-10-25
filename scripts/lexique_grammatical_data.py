#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Données du lexique grammatical d'enrichissement SoninkeGPT (2026-10-24).

Chaque ligne est une entrée du tableau structuré demandé par la mission
d'enrichissement grammatical et lexical. Les colonnes sont :

    forme_soninke, traduction_francaise, categorie_grammaticale, sous_categorie,
    forme_ou_construction_grammaticale, personne, nombre, temps_aspect_mode,
    polarite, variante, variete_regionale, exemple_soninke, traduction_exemple,
    source, page_ou_localisation, niveau_de_confiance, statut_validation, notes

Règles suivies (conformes à docs/LINGUISTIC-QUALITY.md) :
  - aucun mot inventé : chaque forme vient d'une source identifiée ;
  - les champs inconnus sont laissés vides ;
  - les assemblages réguliers non validés sont marqués HYPOTHESE_NON_VALIDEE ;
  - les variantes et contradictions entre sources sont conservées telles quelles.
"""

# ---------------------------------------------------------------------------
# Sources (références complètes dans docs/recherche/README-enrichissement…)
# ---------------------------------------------------------------------------
S_REF   = "Référent projet — data/grammaire/soninke.yaml (données linguistiques confirmées)"
S_LEX   = "Corpus projet — data/source/lexique-soninke-fr-base.csv"
S_EA    = "Corpus projet — data/source/paradigmes-etre-avoir.csv ; docs/VERBES-ETRE-AVOIR.md"
S_SNK   = "snk_engine (CC BY 4.0), noah-medra 2026 — corpus relu par le locuteur"
S_CRE18 = "Creissels 2018, « La catégorie des verbes statifs dans le système morphosyntaxique du soninké », Mandenkan 59, p. 3-30"
S_CRE16 = "Creissels 2016, « Phonologie segmentale et tonale du soninké (parler du Kingi) », Mandenkan 55, p. 3-174"
S_CD19  = "Creissels & Diawara 2019, « Le soninké », esquisse LGIDF (CNRS)"
S_CD13  = "Creissels & Diagne 2013, « Transitivity in Bakel Soninke »"
S_GRE79 = "Grégoire 1979, « Morphologie de l'opposition accompli/inaccompli » (soninké), Mandenkan 1 — cité par snk_engine (réf. G1979)"
S_SILG  = "Dramé & Hagg, « Guide d'écriture de la langue soninké — Sooninkanxannen safandimoxon », SIL"
S_SILD  = "Dictionnaire SIL soninké–français–anglais (Dramé & Hagg) — via « Lexique Soninke du Mali » (Scribd) et Dictionnaire soninké.docx du projet"
S_ASAWG = "Asawan/SIL, « O n'o sooninkanxannen xara n'a safa — Lisons et écrivons notre langue soninké », 2e éd."
S_ASAWP = "Asawan/SIL, « O nan sefe sooninken do faransen ŋa — Parlons le soninké et le français », 2e éd."
S_LIV01 = "Livret d'auto-formation SONINKE, METFPALAN/EDICEF, Dakar, septembre 2001"
S_SONK2 = "soninko.info, « Sooninkan Gonboŋe : la grammaire soninké », leçon 2 (Y. Soumaré, vér. A. Soumaré, 2010)"
S_SONK3 = "soninko.info, leçon 3 — salutations, mois, jours (Y. Soumaré, 2010)"
S_SNKG  = "Soninkara.com, Glossaire de mots soninké–français (H. Wagué et al.)"
S_SNKV  = "Soninkara.org, Dictionnaire soninké–anglais : verbes soninké"
S_SNKC3 = "Soninkara.com, Compte-rendu du 3e cours de soninké en ligne (2014)"
S_LGPR  = "LGIDF (CNRS), Soninké : lexique des pronoms personnels, node/676"
S_LGV   = "LGIDF (CNRS), Soninké : lexique des verbes, node/682"
S_LGA   = "LGIDF (CNRS), Soninké : lexique des adjectifs, node/681"
S_LGQ   = "LGIDF (CNRS), Soninké : lexique des quantitatifs et numéraux, node/679"
S_WK    = "Wikipédia fr, article « Soninké », section Lexique"
S_NEWS  = "Soninkara.com, Xibaaru kurunbo, « Miss Sooninke France 2014 » (2014)"
S_SNKP  = "Soninkara.org, Proverbes et citations soninké"

U_CRE18 = "https://journals.openedition.org/mandenkan/1271"
U_CRE16 = "https://llacan.cnrs.fr/PDF/Mandenkan55/55creissels.pdf"
U_CD19  = "https://lgidf.cnrs.fr/sites/lgidf.cnrs.fr/files/images/SONINKE_24_06_19_A4.pdf (miroir : francaislangueseconde.fr/wp-content/uploads/2009/09/SONINKE.08.05.16.pdf)"
U_CD13  = "http://www.deniscreissels.fr/public/Creissels_Diagne-Transitivity_in_Bakel_Soninke.pdf"
U_GRE79 = "https://llacan.cnrs.fr/PDF/Mandenkan1/1Gregoire.pdf"
U_SILG  = "https://www.sil.org/system/files/reapdata/47-13-72/47137257915905223059455108624196201052/Guide_d_ecriture_soninke.pdf"
U_SILD  = "https://fr.scribd.com/document/951995441/Lexique-Soninke-Mali-Francais-Anglais"
U_ASAWG = "https://www.asawan.org/sites/www.asawan.org/files/uploads/O%20n'o%20sooninkanxannen%20xara%20n'a%20safa%20-guide%20pour%20ceux%20qui%20lisent%20le%20fran%C3%A7ais,%202e%20%C3%A9dition%20-%20Web.pdf"
U_ASAWP = "https://www.asawan.org/sites/www.asawan.org/files/uploads/O%20nan%20sefe%20sooninken%20do%20faransen%20%C5%8Ba%202e%20%C3%A9d%20-%20Web%20lecture.pdf"
U_LIV01 = "http://www.soninkara.org/ressources/soninkara-pdf/Langue-Soninke.pdf"
U_SONK2 = "https://www.soninko.info/cours2.php"
U_SONK3 = "https://www.soninko.info/cours3.php"
U_SNKG  = "https://www.soninkara.com/langue/apprendre-le-soninke/glossaire-de-mots.html"
U_SNKV  = "http://www.soninkara.org/langue-soninke/dictionnaire-soninke-anglais-verbes-soninke-493.html"
U_SNKC3 = "http://www.soninkara.com/langue/apprendre-le-soninke/compte-rendu-du-3eme-cours-de-soninke-en-ligne-sur-facebook.html"
U_LGPR  = "https://lgidf.cnrs.fr/node/676"
U_LGV   = "https://lgidf.cnrs.fr/node/682"
U_LGA   = "https://lgidf.cnrs.fr/node/681"
U_LGQ   = "https://lgidf.cnrs.fr/node/679"
U_WK    = "https://fr.wikipedia.org/wiki/Sonink%C3%A9"
U_NEWS  = "https://www.soninkara.com/snk/gansindu/xibaaru-kurunbo.html"
U_SNKP  = "http://www.soninkara.org/culture-soninke/proverbes-et-citations-soninke-213.html"
U_SNK   = "https://github.com/oscarmedra/snk_engine (rév. 49f50a939ded) — copie : data/source/snk-engine-corpus-grammatical-2026-10-24.jsonl"

KINGI = "Kingi (Mali) — décrit par Creissels"
BAKEL = "Bakel (Sénégal) — décrit par Creissels & Diagne"
KINGUI = "Kingui (Mali) — variété de l'esquisse LGIDF"
MAURI = "Mauritanie — sources pédagogiques"
PROJET = "dialecte du référent du projet (localisation non documentée)"
SILVAR = "Mali/Sénégal/Mauritanie — orthographe SIL"

LIGNE = []

def R(forme, trad, cat, souscat, constr="", pers="", nb="", tam="", pol="",
      var="", region="", ex="", exfr="", src="", loc="", conf="", statut="", notes=""):
    LIGNE.append(dict(
        forme_soninke=forme, traduction_francaise=trad, categorie_grammaticale=cat,
        sous_categorie=souscat, forme_ou_construction_grammaticale=constr,
        personne=pers, nombre=nb, temps_aspect_mode=tam, polarite=pol,
        variante=var, variete_regionale=region, exemple_soninke=ex,
        traduction_exemple=exfr, source=src, page_ou_localisation=loc,
        niveau_de_confiance=conf, statut_validation=statut, notes=notes))

# ===========================================================================
# A. PRONOMS PERSONNELS
# ===========================================================================
DEJA_PRON = "Déjà présent au lexique : {id} ; documenté ici pour l'analyse grammaticale (mission lot 1)."

R("nke", "je ; moi", "pronom_personnel", "série longue — sujet / emphatique",
  "sujet avant le verbe ; ne prend jamais la particule", "1", "sg", "", "",
  "nké (graphie à accents de snk_engine) ; ńké (graphie tonale LGIDF)", PROJET,
  "Nke rini daga saxa.", "Je partirai au marché (plus tard).",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml (pronoms) ; corpus validation_02 v-148 ; " + U_LGPR,
  "élevé", "SOURCE_VERIFIEE", DEJA_PRON.format(id="SNK-GRM-0001"))
R("anke", "tu ; toi", "pronom_personnel", "série longue — sujet / emphatique",
  "sujet avant le verbe ; prend la particule (anke n'…)", "2", "sg", "", "",
  "anké ; ánkè (LGIDF)", PROJET, "Anke n'yi rini daga.", "Tu vas partir.",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml ; corpus validation_01 v-007 ; " + U_LGPR,
  "élevé", "SOURCE_VERIFIEE", DEJA_PRON.format(id="SNK-GRM-0002"))
R("ake", "il / elle ; lui", "pronom_personnel", "série longue — sujet / emphatique",
  "sujet avant le verbe ; prend la particule (ake n'…)", "3", "sg", "", "",
  "aké ; àkê (LGIDF : lui, elle, ça)", PROJET, "Ake n'daga.", "Il est parti.",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml ; corpus validation_02 v-008 ; " + U_LGPR,
  "élevé", "SOURCE_VERIFIEE", DEJA_PRON.format(id="SNK-GRM-0003"))
R("oku", "nous", "pronom_personnel", "série longue — sujet / emphatique",
  "sujet avant le verbe ; ne prend jamais la particule", "1", "pl", "", "",
  "okou (graphie snk_engine) ; ókú (LGIDF)", PROJET, "Oku maxa faye.", "Nous n'avons pas regardé.",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml ; corpus validation_02 v-019 ; " + U_LGPR,
  "élevé", "SOURCE_VERIFIEE", DEJA_PRON.format(id="SNK-GRM-0004"))
R("xaku", "vous", "pronom_personnel", "série longue — sujet / emphatique",
  "sujet avant le verbe ; prend la particule (xaku n'…)", "2", "pl", "", "",
  "xakou ; áxákù (LGIDF) ; axaku (SNK-LEX-0843)", PROJET,
  "Xaku n'daga lenki.", "Vous êtes partis aujourd'hui.",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml ; corpus validation_02 v-149 ; " + U_LGPR,
  "élevé", "SOURCE_VERIFIEE", DEJA_PRON.format(id="SNK-GRM-0005") + " Variante axaku déjà au lexique (SNK-LEX-0843).")
R("iku", "ils / elles ; eux", "pronom_personnel", "série longue — sujet / emphatique",
  "sujet avant le verbe ; prend la particule (iku n'…)", "3", "pl", "", "",
  "ikou ; ìkû (LGIDF)", PROJET, "Iku n'yi rini daga.", "Ils vont partir.",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml ; corpus validation_02 v-006 ; " + U_LGPR,
  "élevé", "SOURCE_VERIFIEE", DEJA_PRON.format(id="SNK-GRM-0006"))
R("n", "je", "pronom_personnel", "série brève (diminutive) — sujet",
  "sujet avant le verbe ; ne prend jamais la particule", "1", "sg", "", "",
  "in (forme pleine) ; ń / Ń (graphies tonales)", PROJET,
  "N faye.", "J'ai regardé.",
  S_REF + " ; " + S_SNK + " ; " + S_SONK2, "data/grammaire/soninke.yaml ; corpus validation_02 v-018 ; " + U_SONK2,
  "élevé", "SOURCE_VERIFIEE",
  DEJA_PRON.format(id="SNK-GRM-0007") + " Le livret de Dakar 2001 écrit « n (in) ».")
R("in", "je ; moi (forme pleine de n)", "pronom_personnel", "série brève — forme pleine",
  "s'emploie dans la phrase sans pause ; n s'emploie en début de phrase ou après pause (lecteur du cours soninko.info)",
  "1", "sg", "", "", "n (forme brève)", MAURI,
  "In yige.", "J'ai mangé.",
  S_SONK2 + " ; " + S_LIV01 + " ; " + S_CRE18, U_SONK2 + " ; " + U_LIV01 + " ; Creissels 2018 ex. (9a) Ń, « prête-moi » lóxo ín ŋá",
  "moyen", "VARIANTE_DOCUMENTEE",
  "Répartition n / in à faire confirmer par le référent (indication issue des commentaires du cours, non d'une grammaire).")
R("an", "tu ; toi ; ton, ta, tes", "pronom_personnel", "série brève — sujet / objet / possessif adnominal",
  "sujet avant le verbe ; possessif avant le nom", "2", "sg", "", "",
  "", PROJET, "An ka ke.", "Ta maison.",
  S_REF + " ; " + S_SNK + " ; " + S_LIV01, "data/grammaire/soninke.yaml ; snk_engine docs/langue/nom.md ; " + U_LIV01,
  "élevé", "SOURCE_VERIFIEE", DEJA_PRON.format(id="SNK-GRM-0008"))
R("a", "il / elle ; le, la, lui ; son, sa, ses", "pronom_personnel",
  "série brève — sujet / objet / possessif adnominal",
  "même forme au sujet et à l'objet ; possessif avant le nom ; aucune distinction de genre",
  "3", "sg", "", "", "à (ton bas, sujet) ; á (ton haut, possesseur adnominal et devant adjectif prédicatif)",
  PROJET + " ; " + KINGUI, "A da a bisimilla.", "Il l'a accueilli.",
  S_CD19 + " ; " + S_LIV01 + " ; " + S_CRE16, U_CD19 + " §3 ; " + U_LIV01 + " ; Creissels 2016 (ton H des pronoms de 3e personne)",
  "élevé", "SOURCE_VERIFIEE",
  DEJA_PRON.format(id="SNK-GRM-0009") + " Les tons ne sont pas notés dans l'orthographe du projet.")
R("o", "nous ; notre, nos", "pronom_personnel", "série brève — sujet / objet / possessif adnominal",
  "sujet avant le verbe ; possessif avant le nom", "1", "pl", "", "",
  "ó (ton haut, Kingi)", PROJET, "O bara.", "Notre cour.",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml ; snk_engine docs/langue/pronoms.md",
  "élevé", "SOURCE_VERIFIEE",
  DEJA_PRON.format(id="SNK-GRM-0010") +
  " Aucune distinction inclusive/exclusive du « nous » n'est documentée dans les sources consultées (Creissels, LGIDF, SIL, cours) : à vérifier auprès du référent.")
R("xa", "vous ; votre, vos", "pronom_personnel", "série brève — sujet / objet / possessif adnominal",
  "sujet avant le verbe ; impératif pluriel (xa + verbe) ; possessif avant le nom", "2", "pl", "", "",
  "", PROJET, "Xa guiri.", "Levez-vous.",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml (imperatif_pluriel) ; snk_engine docs/langue/temps.md",
  "élevé", "SOURCE_VERIFIEE",
  DEJA_PRON.format(id="SNK-GRM-0011") + " Homographes documentés par ailleurs : xa « mais » et xa « où » (voir sections conjonctions et interrogatifs).")
R("i", "ils / elles ; les, leur, leurs ; eux", "pronom_personnel",
  "série brève — sujet / objet / possessif adnominal / réfléchi (3e personne)",
  "même forme au sujet et à l'objet ; aucune distinction de genre ni de nature du référent",
  "3", "pl", "", "", "ì (ton bas) ; í (ton haut = pronom réfléchi, à distinguer)", PROJET + " ; " + KINGUI,
  "I da me katu.", "Ils se sont battus (frappés l'un l'autre).",
  S_CD19 + " ; " + S_LIV01 + " ; " + S_CRE16, U_CD19 + " §4 ; " + U_LIV01 + " ; Creissels 2016 §15 (réfléchis í et dú)",
  "élevé", "SOURCE_VERIFIEE", DEJA_PRON.format(id="SNK-GRM-0012"))
R("inke, anken, aken, oku, xakun, ikun", "moi, toi, lui/elle, nous, vous, eux (pronoms indépendants)",
  "pronom_personnel", "série longue — graphie du cours soninko.info (nasale finale = déterminant)",
  "pronoms « impersonnels » (indépendants/emphatiques) selon la terminologie du cours", "", "", "", "",
  "nke, anke, ake, oku, xaku, iku (graphie du projet)", MAURI,
  "", "", S_SONK2, U_SONK2 + " (section SEEGANI)", "moyen", "VARIANTE_DOCUMENTEE",
  "Mêmes formes que la série longue du projet ; la graphie du cours ajoute la nasale finale de détermination (anken, xakun, ikun). Ne pas créer de doublons : rattacher comme variantes graphiques.")
R("inke", "moi", "pronom_personnel", "pronom indépendant (tonique)", "", "1", "sg", "", "",
  "nke", MAURI, "", "", S_SONK2, U_SONK2, "moyen", "VARIANTE_DOCUMENTEE",
  "Listé comme pronom impersonnel/indépendant ; emploi exact (mise en relief ?) à confirmer.")
R("du", "soi-même", "pronom_personnel", "pronom réfléchi (coréférence sujet–objet)",
  "marque la coréférence entre sujet et objet (ou oblique) d'un même verbe", "", "", "", "",
  "dú (graphie tonale)", KINGI, "", "", S_CRE16 + " ; " + S_SNKG,
  U_CRE16 + " note 15 ; glossaire Soninkara (entrée « Du : Soi-même »)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Le soninké a deux pronoms réfléchis : í et dú (Creissels 2016). Exemple à recueillir auprès du référent.")
R("í", "soi (réfléchi possessif ; coréférence sujet de subordonnée)", "pronom_personnel",
  "pronom réfléchi (ton haut)",
  "possessif réfléchi ; coréférence entre le sujet de la principale et le sujet d'une subordonnée",
  "", "", "", "", "i (3pl, ton bas — homographe sans le ton)", KINGI,
  "", "", S_CRE16, U_CRE16 + " note 15", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Distingué de i « ils » uniquement par le ton, que l'orthographe du projet ne note pas : ambiguïté à signaler au référent.")
R("me", "se (réciproque)", "pronom_personnel", "particule réciproque",
  "placé après le marqueur d'objet : i da me katu « ils se sont battus »", "", "pl", "", "",
  "", "", "I da me katu.", "Ils se sont (frappés) battus.",
  S_LIV01, U_LIV01 + " §IV (particules du réfléchi et du réciproque)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Le livret de Dakar range me parmi les particules du réfléchi/réciproque. À confronter avec í/dú de Creissels (Kingi) : analyses différentes selon les variétés et les auteurs.")
R("pronom complément = pronom sujet", "le, la, lui, me, te… (mêmes formes que le sujet)",
  "pronom_personnel", "objet direct / indirect",
  "Aucune différence de forme entre pronom sujet et pronom objet ; le pronom objet se place devant le verbe (ordre S O V)",
  "", "", "", "", "", KINGUI + " ; " + PROJET,
  "A di nke wori. = A di ŋ'wori.", "Elle m'a vu. (les deux écritures se disent)",
  S_CD19 + " ; " + S_SNK + " ; " + S_LIV01, U_CD19 + " §3 ; snk_engine docs/langue/pronoms.md ; livret Dakar 2001 (a da in raga « il m'a rattrapé »)",
  "élevé", "SOURCE_VERIFIEE",
  "Fait grammatical attesté par trois sources concordantes. L'objet pronominal s'assimile au verbe comme la particule (ŋ'wori).")
R("n / an / a / o / xa / i + nom", "mon, ton, son, notre, votre, leur",
  "déterminant_possessif", "possessif adnominal (série brève)",
  "possesseur avant le possédé, sans mot de liaison : n ka ke « ma maison »", "", "", "", "",
  "", PROJET, "N ka ke. / A ka ke. / O bara. / I yiramu.", "Ma maison. / Sa maison. / Notre cour. / Leurs vêtements.",
  S_SNK + " ; " + S_LIV01 + " ; " + S_CD19, "snk_engine docs/langue/nom.md ; livret Dakar 2001 (n sugo « ma chèvre ») ; " + U_CD19 + " §2",
  "élevé", "SOURCE_VERIFIEE",
  "Le soninké n'a pas de formes possessives spéciales : ce sont les pronoms personnels employés devant le nom (Creissels & Diawara).")
R("nke + nom", "mon (série longue devant le nom)", "déterminant_possessif",
  "possessif adnominal (série longue)", "possesseur avant le possédé", "1", "sg", "", "",
  "", PROJET, "Nke faba.", "Mon père.",
  S_SNK, "snk_engine docs/langue/pronoms.md ; corpus texte_pluies (Nké faba giri féné « mon père s'est levé tôt »)",
  "moyen", "SOURCE_VERIFIEE", "La série brève est la plus employée ; la série longue possessive est attestée dans le corpus du locuteur.")
R("nom possesseur + nom possédé", "le X de Y", "construction_possessive", "complément de nom (juxtaposition)",
  "ordre modifieur–modifié, sans mot de liaison ; changement tonal sur le nom modifié (non noté dans l'orthographe du projet)",
  "", "", "", "", "", KINGUI + " ; " + PROJET,
  "Faatu ka. / N'paba ka.", "La maison de Fatou. / La maison de mon père.",
  S_CD19 + " ; " + S_LIV01 + " ; " + S_SNK, U_CD19 + " §2 ; livret Dakar 2001 ; snk_engine docs/langue/nom.md",
  "élevé", "SOURCE_VERIFIEE",
  "n'paba montre l'assimilation de la nasale (n + faba → n'paba).")

# ===========================================================================
# B. VERBE « ÊTRE » — copules et constructions
# ===========================================================================
R("ni", "être (identité, catégorie, qualité) — copule équative", "copule", "équative (positive)",
  "sujet + attribut + ni ; invariable, la personne est portée par le pronom", "", "", "présent", "positif",
  "ní / ˋní (graphies tonales)", KINGI + " ; " + PROJET,
  "A bexecen ni.", "Elle est acide / sucrée.",
  S_CRE18 + " ; " + S_LEX, U_CRE18 + " §3.5 ; lexique SNK-LEX-0479 (valide_par_referent)",
  "élevé", "SOURCE_VERIFIEE",
  "Homographie à signaler : ni est aussi cité comme postposition/prédicatif dans d'autres emplois (livret Dakar 2001).")
R("ni ya", "être (état, qualité) — copule équative du dialecte du projet", "copule", "équative (positive)",
  "sujet + attribut + ni ya", "", "", "présent", "positif",
  "ni", PROJET, "Towoyinte ni ya.", "Il est malade.",
  S_SNK, "snk_engine docs/langue/etre-avoir.md ; corpus texte_marche (xore ni ya « elle est grande » ; Nké faba ka n'ya ni « c'est la maison de mon père »)",
  "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Dans le dialecte du projet, la copule équative apparaît souvent comme ni ya (ya = focalisateur ?). Analyse exacte à confirmer.")
R("feti", "ne pas être (identité, qualité) — négatif de la copule équative", "copule", "équative (négative)",
  "attribut (sans -n) + feti ; ou feti + attribut + yi", "", "", "présent", "négatif",
  "he ~ heti (Kingi, Creissels) ; fe (liste du livret Dakar 2001)", PROJET + " ; " + KINGI,
  "Niima feti bugante yi.", "Nima n'est pas un vantard.",
  S_CRE18 + " ; " + S_LEX + " ; " + S_LIV01, U_CRE18 + " §3.5 ; lexique SNK-LEX-0536 ; livret Dakar 2001 (a yaqe feti « ce n'est pas sa femme »)",
  "élevé", "SOURCE_VERIFIEE", "")
R("he ~ heti", "ne pas être — négatif de la copule équative (variété du Kingi)", "copule",
  "équative (négative)", "", "", "", "présent", "négatif", "feti (dialecte du projet)", KINGI,
  "", "", S_CRE18, U_CRE18 + " §3.5 (ˋhé ~ hètí)", "moyen", "VARIANTE_DOCUMENTEE",
  "Variante tonale du Kingi ; correspond à feti dans les autres sources.")
R("wa", "être (lieu, existence, état passager) — copule locative", "copule", "locative (positive)",
  "entité localisée + wa + lieu (+ postposition)", "", "", "présent", "positif",
  "wá (graphie tonale) ; yi (dialecte du projet)", KINGI + " ; " + PROJET,
  "Haatu wa konpen di.", "Fatou est dans la chambre.",
  S_CRE18 + " ; " + S_LEX, U_CRE18 + " §3.4 ex. (11a) ; lexique SNK-LEX-0184 (Baabon wa xatin kanma)",
  "élevé", "SOURCE_VERIFIEE",
  "Forme déjà au lexique comme marqueur aspectuel (SNK-GRM-0019) : la fonction de copule locative est un emploi distinct documenté par Creissels — ne pas créer de doublon, enrichir l'entrée existante.")
R("nta", "ne pas être (lieu, existence) — négatif de la copule locative", "copule", "locative (négative)",
  "entité localisée + nta + lieu", "", "", "présent", "négatif",
  "ntá (graphie tonale) ; n'ti (dialecte du projet)", KINGI + " ; " + PROJET,
  "Haatu nta konpen di.", "Fatou n'est pas dans la chambre.",
  S_CRE18 + " ; " + S_LEX, U_CRE18 + " §3.4 ex. (11b) ; lexique SNK-GRM-0032 ; SNK-LEX-0310 (Baasi nt'a di « il n'y a rien de mal »)",
  "élevé", "SOURCE_VERIFIEE", "Déjà présent au lexique (SNK-GRM-0032) ; documenté ici comme copule.")
R("na", "être (lieu) — variante de la copule locative devant focal ou interrogatif", "copule",
  "locative (positive, contexte focal/interrogatif)",
  "la copule wa devient na en présence d'un constituant focalisé ou d'un mot interrogatif",
  "", "", "présent", "positif", "wa", KINGI + " ; " + PROJET,
  "Haatu na minna ?", "Où est Fatou ?",
  S_CRE18 + " ; " + S_LEX, U_CRE18 + " §3.4 ex. (12a-c) ; lexique SNK-LEX-0218 (…na ti minna yi ?)",
  "élevé", "SOURCE_VERIFIEE",
  "Homographie : na est aussi le marqueur de demande/subjonctif (SNK-GRM-0017). Deux emplois distincts de même forme.")
R("yi", "être (lieu) — copule locative du dialecte du projet", "copule", "locative (positive)",
  "sujet + yi + lieu", "", "", "présent", "positif", "wa (Creissels)", PROJET,
  "A yi ka ke.", "Elle est à la maison.",
  S_SNK, "corpus texte_marche ; snk_engine docs/langue/etre-avoir.md ; texte_repas (a yi sorékompé noxo « elle est dans la cuisine »)",
  "élevé", "SOURCE_VERIFIEE",
  "Déjà présent au lexique comme marqueur aspectuel (SNK-GRM-0021) : emploi copule locative à ajouter à l'entrée existante. Le locuteur confirme « yi veut dire est, ti veut dire n'est pas ».")
R("n'ti", "ne pas être (lieu) — négatif de yi", "marqueur_negation", "négation de la copule locative",
  "sujet + n'ti + lieu ; ti après les pronoms qui ne prennent pas la particule", "", "", "présent", "négatif",
  "ti ; nta (Creissels)", PROJET, "Ake n'ti ka ke.", "Elle n'est pas à la maison.",
  S_SNK, "corpus texte_marche ; snk_engine docs/langue/etre-avoir.md (Nke ti mula « je ne veux pas »)",
  "élevé", "SOURCE_VERIFIEE",
  "Homographie : ti est aussi le verbe « dire » (SNK-LEX-0877). À distinguer en contexte.")
R("nàn ~ ǹ", "être (+ propriété intensive/comparative) — marqueur des verbes statifs", "marqueur_predicatif",
  "verbes statifs (positif)", "sujet + nàn + verbe statif (+ comparé + ŋa/yi)", "", "", "présent", "positif",
  "", KINGI, "Kiyen nàn tawó.", "Le soleil est ardent.",
  S_CRE18, U_CRE18 + " §3.3 ex. (9)-(10), (17), (22), (44)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Classe des verbes statifs décrite pour le Kingi : existence dans le dialecte du projet à confirmer (déjà signalé dans docs/VERBES-ETRE-AVOIR.md).")
R("ntá", "ne pas être (+ propriété) — négatif des verbes statifs", "marqueur_predicatif",
  "verbes statifs (négatif)", "sujet + ntá + verbe statif (forme à ton B)", "", "", "présent", "négatif",
  "", KINGI, "Ó ntá gàbà Hàatú ŋàllí.", "Nous ne voyons pas souvent Fatou. (litt. nous ne sommes pas fréquents à voir Fatou)",
  S_CRE18, U_CRE18 + " §3.3 ex. (10a)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Homographie : ntá est aussi le négatif du projectif et de l'inaccompli avec les verbes ordinaires.")
R("ñí", "marqueur d'inaccompli passé (« j'étais », « je mangeais »)", "marqueur_predicatif",
  "inaccompli passé", "sujet + ñí + gérondif", "", "", "imparfait / inaccompli passé", "positif",
  "ñi", KINGI + " ; " + MAURI, "In ñi yigene.", "Je mangeais.",
  S_CRE18 + " ; " + S_SONK2, U_CRE18 + " Tableau 4 ; " + U_SONK2 + " (IN ÑI : j'étais)",
  "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Piste pour le passé de « être » : le corpus du projet n'atteste aucune forme fléchie au passé (docs/VERBES-ETRE-AVOIR.md §3.4).")
R("má ñì", "marqueur d'inaccompli passé négatif (« je n'étais pas »)", "marqueur_predicatif",
  "inaccompli passé négatif", "sujet + má ñì + gérondif", "", "", "imparfait / inaccompli passé", "négatif",
  "", KINGI, "", "", S_CRE18, U_CRE18 + " Tableau 4", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Aucun exemple relevé dans les extraits consultés ; forme du tableau de Creissels 2018.")
R("we ñaana / ye ñaana", "serai, seras, sera… (futur de « être », paradigme pédagogique)", "copule",
  "équative/locative (future) — paradigme d'un cours en ligne",
  "pronom + we/ye + ñaana", "", "", "futur", "positif",
  "wa ñaana (selon un lecteur du cours, citant Y. Diagana)", MAURI,
  "In we ñaana.", "Je serai.",
  S_SONK2, U_SONK2 + " (commentaire de Daraame Banjugu S, 2014 : we/ye remplacés par wa)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Paradigme pédagogique mauritanien non recoupé avec le corpus du projet ; à ne présenter qu'avec réserve (déjà signalé dans docs/VERBES-ETRE-AVOIR.md §3.4).")
# présent pédagogique (soninko.info leçon 2) — "In ni" déjà fiché SNK-EA-0038
for _p, _f in [("2sg","An ni"),("3sg","A ni"),("1pl","O ni"),("2pl","Xa ni"),("3pl","I ni")]:
    R(_f, "je suis / tu es / il est / nous sommes / vous êtes / ils sont", "forme_conjuguee",
      "être — présent (paradigme pédagogique)", "pronom + ni (copule équative)",
      _p[0], _p[2:], "présent", "positif", "", MAURI, "", "", S_SONK2, U_SONK2 + " (ÑAŊE: ÊTRE, 1. PRÉSENT)",
      "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
      "Paradigme d'un cours en ligne mauritanien ; concorde avec la copule ní de Creissels. Cf. SNK-EA-0038 (1sg déjà fichée).")
# imparfait pédagogique — "In ñi" déjà fiché SNK-EA-0039
for _p, _f in [("2sg","An ñi"),("3sg","A ñi"),("1pl","O ñi"),("2pl","Xa ñi"),("3pl","I ñi")]:
    R(_f, "j'étais / tu étais / il était / nous étions / vous étiez / ils étaient", "forme_conjuguee",
      "être — imparfait (paradigme pédagogique)", "pronom + ñi (inaccompli passé)",
      _p[0], _p[2:], "imparfait", "positif", "", MAURI, "", "", S_SONK2, U_SONK2 + " (ÑAŊE: ÊTRE, 3. IMPARFAIT)",
      "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
      "Correspond au marqueur d'inaccompli passé ˋñí de Creissels 2018. Cf. SNK-EA-0039 (1sg déjà fichée).")
# futur pédagogique — "In we ñaana" (SNK-EA-0040) et "A ye ñaana" (SNK-EA-0041) déjà fichés
for _p, _f in [("2sg","An we ñaana"),("1pl","O ye ñaana"),("2pl","Xa ye ñaana"),("3pl","I ye ñaana")]:
    R(_f, "je serai / tu seras / il sera / nous serons / vous serez / ils seront", "forme_conjuguee",
      "être — futur (paradigme pédagogique)", "pronom + we/ye + ñaana",
      _p[0], _p[2:], "futur", "positif", "wa ñaana (variante signalée en commentaire du cours)", MAURI,
      "", "", S_SONK2, U_SONK2 + " (ÑAŊE: ÊTRE, 2. FUTURE)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
      "Non recoupé avec le corpus du projet. Cf. SNK-EA-0040/0041 (1sg et 3sg déjà fichées).")
R("existant + wa / yi + lieu", "il y a (existence, présence)", "construction_existentielle",
  "existentiel affirmatif", "pas de tournure spéciale : on dit que la chose est quelque part",
  "", "", "présent", "positif", "", KINGUI + " ; " + PROJET,
  "Lemine yi ka ke noxo. / Baabon wa xatin kanma.", "Il y a un enfant dans la maison. / Il y a de la mousse sur le lait.",
  S_SNK + " ; " + S_LEX, "snk_engine docs/langue/nom.md ; lexique SNK-LEX-0184", "élevé", "SOURCE_VERIFIEE", "")
R("sere su + n'ti / nta + lieu", "il n'y a personne (négation existentielle)", "construction_existentielle",
  "existentiel négatif", "nom + su (aucun) + négatif de la copule locative",
  "", "", "présent", "négatif", "", PROJET,
  "Sere su n'ti ka ke noxo. / Dji su n'ti yere.", "Il n'y a personne dans la maison. / Il n'y a pas d'eau (ici).",
  S_SNK, "snk_engine docs/langue/nom.md", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Littéralement « aucune personne n'est dans la maison ». Cf. Baasi nt'a di (SNK-LEX-0310) « il n'y a rien de mal ».")
R("ni a ni", "il y a (variante du dialecte du projet)", "construction_existentielle", "existentiel affirmatif",
  "", "", "", "présent", "positif", "wa / yi", PROJET,
  "Yite gabo ni a ni a noxo.", "Il y a beaucoup d'arbres dedans.",
  S_SNK, "snk_engine data/references/mots.yaml (texte_travail, lecture à confirmer)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Transcription relevée dans une lecture automatique du texte, non confirmée mot à mot : forme à vérifier avant tout usage.")
R("attribut (sans copule) après le nom", "être + adjectif (prédication adjective sans copule)",
  "construction_predicative", "prédicat adjectival", "nom + déterminant + adjectif, sans copule",
  "", "", "passé/imparfait (selon contexte)", "", "", PROJET,
  "Killé ké gillo.", "La route était longue.",
  S_SNK, "corpus texte_village (village-03) ; snk_engine docs/langue/etre-avoir.md", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Le temps (est/était) n'est pas marqué : c'est le contexte qui tranche.")
R("attribut-n + ni", "être + adjectif (prédication adjective avec copule)", "construction_predicative",
  "prédicat adjectival", "sujet + adjectif-n + ni ; l'adjectif prend le suffixe -n et un schème tonal particulier (BH)",
  "", "", "présent", "positif", "", KINGI + " ; " + PROJET,
  "Ñántò-n bùnné-n tòoxìnté-n nì. / A bexecen ni.", "La piqûre du scorpion est douloureuse. / Elle est acide.",
  S_CRE18 + " ; " + S_LEX, U_CRE18 + " §3.6 ex. (15) ; lexique SNK-LEX-0479", "élevé", "SOURCE_VERIFIEE", "")
R("ni, feti, fe, yi, la, yaa", "formes prédicatives et négatives (liste du livret d'alphabétisation)",
  "marqueur_predicatif", "liste de formes citées sans glose individuelle",
  "", "", "", "", "", "", "", "", "",
  S_LIV01, U_LIV01 + " §IV (« Prédicatives et négatives telles que : ni, feti, fe, yi, la, yaa »)", "faible",
  "A_CONFIRMER_PAR_LOCUTEUR",
  "fe, la et yaa ne sont glosés ni par le livret ni par les autres sources consultées : à recueillir auprès du référent ; ne pas les présenter comme traductions.")

# ===========================================================================
# C. VERBE « AVOIR » — possession et constructions équivalentes
# ===========================================================================
R("possédé + wa / nta + possesseur + yi / ŋa", "avoir (possession)", "construction_possessive",
  "possession locative", "pas de verbe « avoir » : la chose possédée est « chez » le possesseur",
  "", "", "présent", "", "", KINGI + " ; " + PROJET,
  "Yintin xullu baananbaanon wa a yi.", "Il a quelques cheveux blancs. (litt. quelques cheveux blancs sont à lui)",
  S_CRE18 + " ; " + S_LEX + " ; " + S_EA, "lexique SNK-LEX-0303 (valide_par_referent) ; SNK-LEX-0365 (… wa dudoxotonten ŋa) ; docs/VERBES-ETRE-AVOIR.md §4",
  "élevé", "SOURCE_VERIFIEE",
  "Fait central : ne jamais traduire « avoir » par un mot unique. yi ~ yá ~ ŋá sont les variantes d'une postposition multifonction (Creissels).")
R("possédé + (y)ani + maxa", "avoir (possession) — tournure du dialecte du projet", "construction_possessive",
  "possession locative avec maxa « chez »", "possédé + ni + pronom + maxa ; négatif : possédé + n'ti + maxa",
  "", "", "présent", "", "", PROJET,
  "Waxi-ni filli yani maxa ado guida naxaru siki.", "J'ai deux frères et trois sœurs.",
  S_SNK, "corpus texte_marche ; snk_engine docs/langue/etre-avoir.md (xalisi n'ti maxa « je n'ai pas d'argent » ; remme ngebe ni a ni maxa « ils ont beaucoup d'enfants »)",
  "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "maxa a ici le sens postpositionnel « chez, avec » ; à distinguer de maxa marqueur de négation du passé (homonymie à faire trancher par le référent).")
R("maxa", "chez, avec (possession)", "postposition", "possessive",
  "possédé + n'ti + maxa = « je n'ai pas »", "", "", "", "", "", PROJET,
  "Xalisi n'ti maxa.", "Je n'ai pas d'argent. (litt. l'argent n'est pas chez moi)",
  S_SNK, "snk_engine data/references/mots.yaml (texte_marche, copule_et_avoir, confirmé) ; corpus texte_marche",
  "moyen", "CONTRADICTOIRE_ENTRE_SOURCES",
  "Même forme que maxa « négation du passé » (SNK-GRM-0024) et que máxà « négation impératif/subjonctif » (Creissels). Les sources ne tranchent pas entre homonymie et polysémie : à soumettre au référent.")
R("xale", "à (appartenance)", "postposition", "appartenance",
  "chose + ni + possesseur + ni ya xale = « la chose est à moi »", "", "", "présent", "positif", "", PROJET,
  "Ke kitabe ni nke ni ya xale.", "Ce livre est à moi.",
  S_SNK, "snk_engine docs/langue/nom.md (Appartenance)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR", "")
R("sujet + wa + nombre + siine", "avoir (tel âge)", "construction_possessive", "âge",
  "l'âge se dit avec la copule locative wa et le nom siine « année »", "", "", "présent", "positif", "", "",
  "Aken Ñaame Tarawore wa 21 siine.", "Naïma Tarawore a 21 ans.",
  S_NEWS, U_NEWS, "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Exemple authentique relevé dans un article de presse soninké ; graphie de la source conservée (ɲ).")
R("sujet + nta + siine + yi", "ne pas avoir (tel âge)", "construction_possessive", "âge (négatif)",
  "", "", "", "présent", "négatif", "", "",
  "A nta siine yi.", "Il n'a pas encore un an.",
  S_SILD, U_SILD + " (entrée siine)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Traduction anglaise de la source : He is not yet a year old.")
R("sujet + verbe d'état (tampi, mama, konu…)", "être fatigué / avoir mal / avoir peur", "construction_predicative",
  "états physiques et émotionnels traduits par « avoir » en français",
  "le soninké emploie des verbes ou adjectifs d'état, pas une construction avec « avoir »",
  "", "", "passé (accompli)", "", "", PROJET,
  "M'paba a tampi, xodo ké wa mama n.", "Mon père était fatigué, il avait mal au dos.",
  S_SNK, "corpus texte_pluies ; cf. A kona, a xaru « il a eu peur et il a crié »",
  "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Pour « avoir peur », « avoir mal » : constructions à documenter verbe par verbe avec le référent (mama = faire mal, nom d'action mamande).")
R("xawa", "devoir", "verbe", "verbe modal — obligation",
  "pronom + na + n'xawa + complément : « je dois … »", "", "", "", "", "qawa", PROJET,
  "Bawoni nké na n'xawa maro ado téh n'ya xobono.", "Parce que je dois acheter du riz et du thé.",
  S_SNK, "corpus texte_marche ; snk_engine docs/langue/etre-avoir.md (oku na n'xawa … « nous devons »)",
  "moyen", "A_CONFIRMER_PAR_LOCUTEUR", "Radical à confirmer (xawa / qawa selon les transcriptions du même corpus).")
R("qawa", "devoir, falloir", "verbe", "verbe modal — obligation", "", "", "", "", "", "xawa", PROJET,
  "", "", S_SNK, "snk_engine data/references/verbes.yaml (texte_journee)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Relevé dans l'inventaire de snk_engine sans exemple complet ; probablement même lexème que xawa (graphie q/x).")
R("qáwà", "devoir (verbe statif)", "verbe_statif", "verbe modal — obligation",
  "se combine avec les marqueurs des verbes statifs nàn / ntá", "", "", "", "", "", KINGI,
  "", "", S_CRE18, U_CRE18 + " §1 (citant Diagana 1994 : gàbá « être fréquent », qáwà « devoir », sìrì « devoir »)",
  "moyen", "A_CONFIRMER_PAR_LOCUTEUR", "Auxiliaire modal décrit pour le Kingi ; équivalence avec xawa du dialecte du projet à établir.")
R("sìrì", "devoir (verbe statif)", "verbe_statif", "verbe modal — obligation",
  "se combine avec les marqueurs des verbes statifs nàn / ntá", "", "", "", "", "", KINGI,
  "", "", S_CRE18, U_CRE18 + " §1", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Homographie possible avec siri « bien/mal/renforcement » du dialecte du projet : à ne pas confondre sans vérification.")
R("ra", "pouvoir (particule)", "particule", "modale — capacité",
  "particule qui traduit le verbe pouvoir (anglais can)", "", "", "", "", "", "",
  "", "", S_SNKG, U_SNKG + " (entrée Ra)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Glose du glossaire Soninkara, sans exemple : à recouper avec kitta et avec les marqueurs projectifs ná/ntá de Creissels.")
R("kita", "recevoir, obtenir, avoir", "verbe", "verbe — possession/obtention",
  "", "", "", "", "", "", PROJET,
  "O wa biradi n'kitana siné ké muma.", "Et nous aurons assez de nourriture pour toute l'année.",
  S_SNK + " ; " + S_GRE79, "corpus texte_pluies ; snk_engine data/references/verbes.yaml (kita recevoir, gérondif kitana, réf. G1979)",
  "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Seul verbe se rapprochant de « avoir/obtenir » ; ne couvre pas la possession durable (construction locative).")
R("xaso", "vieillir, être vieux", "verbe", "verbe d'état", "", "", "", "", "", "",
  "", "N xaso saasa.", "Je suis vieux maintenant (je suis devenu vieux maintenant).",
  S_SILD, U_SILD + " (entrée xaso1)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Utile pour les états traduits par « avoir » en français (avoir de l'âge). xase « vieux » est au lexique du projet (SNK-LEX : adjectif).")
R("« avoir » des temps composés français", "aucun auxiliaire en soninké", "construction_verbale",
  "accompli", "accompli intransitif : Ø ; accompli transitif : da/di entre sujet et objet ; négatif : ma/maxa",
  "", "", "passé (accompli)", "", "", KINGUI + " ; " + PROJET,
  "Anke n'di maro n'yiga. / In yige.", "Tu as mangé le riz. / J'ai mangé.",
  S_CD19 + " ; " + S_EA + " ; " + S_SONK2, U_CD19 + " §2 ; data/source/soninke-samples.jsonl (snk-engine-02-14) ; SNK-EA-0063/0064",
  "élevé", "SOURCE_VERIFIEE",
  "Ne jamais calquer l'auxiliaire « avoir » : la valeur de passé composé est portée par les marqueurs prédicatifs.")

# ===========================================================================
# D. VERBES PRIORITAIRES (lot 2) — lexèmes, variantes et divergences
# ===========================================================================
R("daga", "partir ; aller", "verbe", "verbe prioritaire lot 2 — mouvement",
  "radical invariable ; le temps est porté par les marqueurs prédicatifs ; gérondif dagana ; nom d'action dagaye",
  "", "", "", "", "dagana (gérondif)", PROJET,
  "Nke rini daga saxa. / Xa daga.", "Je partirai au marché. / Partez.",
  S_REF + " ; " + S_SNK + " ; " + S_LEX, "data/grammaire/soninke.yaml (dagaer) ; corpus validation_01 v-012, texte_marche marche-01 (Anké dagana minna ? « Où vas-tu ? ») ; SNK-LEX-1339/1340/1341 (Daga goli / Daga iige / Daga sohu)",
  "élevé", "SOURCE_VERIFIEE",
  "Le français rend daga par « partir » ou « aller » selon le contexte. Composés validés par le référent : Daga goli (partir travailler), Daga iige (aller manger), Daga sohu (aller dormir).")
R("ri", "venir", "verbe", "verbe prioritaire lot 2 — mouvement",
  "gérondif rini (homographe du marqueur de futur rini) ; nom d'action riye", "", "", "", "",
  "rini (gérondif)", PROJET,
  "Ake n'yi rini ba ?", "Est-ce qu'il viendra ?",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml (rier) ; corpus serie_02 02-21",
  "élevé", "SOURCE_VERIFIEE",
  "Divergence de glose : le référent du projet donne « venir » ; Grégoire 1979 (réf. G1979 de snk_engine) donne « arriver ». Les deux sens sont conservés ; à trancher par variété. Homographie rini (gérondif) / rini (futur lointain, SNK-GRM-0015).")
R("dioofe", "arriver", "verbe", "verbe prioritaire lot 2 — mouvement",
  "gérondif dioofene ; nom d'action dioofe-ye", "", "", "", "", "", PROJET,
  "", "", S_REF + " ; " + S_LEX, "data/grammaire/soninke.yaml (dioofeer) ; SNK-LEX-0025 (fourni_par_referent), SNK-LEX-1010/1011",
  "élevé", "SOURCE_VERIFIEE", "Déjà au lexique ; documenté ici pour les tableaux de conjugaison.")
R("ko", "dire", "verbe", "verbe prioritaire lot 2 — parole",
  "gérondif kono ; nom d'action ko-ŋe", "", "", "", "", "kono (gérondif)", PROJET,
  "N'ti a da nanti ake n'yi diomou.", "Je lui ai dit qu'elle allait bien. (nanti introduit le discours rapporté)",
  S_REF + " ; " + S_LEX, "data/grammaire/soninke.yaml (koer) ; SNK-LEX-0164 (fourni_par_referent) ; corpus texte_village village-27",
  "élevé", "SOURCE_VERIFIEE",
  "Voir aussi la ligne « ko = qui » (section interrogatifs) : homonymie conflictuelle à ne pas fusionner.")
R("wori", "voir", "verbe", "verbe prioritaire lot 2 — perception",
  "transitif ; gérondif worini ; nom d'action woriye", "", "", "", "", "", PROJET,
  "Xa na maro ke ŋ'wori saxa. / Maro ke wori.", "Voyez le riz au marché. / Vois le riz.",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml (wories, transitif) ; corpus validation_02 v-114, v-125",
  "élevé", "SOURCE_VERIFIEE",
  "L'objet pronominal s'assimile : ŋ'wori (SNK-GRM-0030).")
R("mugu", "entendre, sentir", "verbe", "verbe prioritaire lot 2 — perception",
  "", "", "", "", "", "", "", "", "",
  S_LEX + " ; " + S_LGV, "SNK-LEX-0722 (source_externe_a_verifier) ; " + U_LGV + " (mùgú)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Quasi-homonymie à surveiller : mungu « oublier » est fourni par le référent (SNK-LEX-0079, data/grammaire/soninke.yaml). Ne pas fusionner mugu et mungu sans preuve. Aucun exemple complet relevé dans le corpus du projet.")
R("tu", "connaître, savoir", "verbe", "verbe prioritaire lot 2 — cognition",
  "gérondif tunu ; nom d'action tu-ye", "", "", "", "", "", PROJET,
  "N maama be ga ñi faayindini soyi.", "… (exemple du livret de Dakar 2001 ; traduction à compléter depuis le livret)",
  S_REF + " ; " + S_LEX + " ; " + S_LIV01 + " ; " + S_LGV, "data/grammaire/soninke.yaml (tuer) ; SNK-LEX-0159 (fourni_par_referent) ; " + U_LIV01 + " ; " + U_LGV + " (tú connaître)",
  "élevé", "SOURCE_VERIFIEE",
  "« savoir » et « connaître » ne font qu'un en soninké d'après les sources consultées ; pas de verbe distinct relevé. Homographie : tu apparaît aussi dans la formule du livret « nta ken tu ».")
R("mula", "vouloir", "verbe", "verbe prioritaire lot 2 — modal",
  "construction : sujet + (marqueur) + mula + na + verbe ; négatif : ti mula", "", "", "", "", "", PROJET,
  "O ni mula na xobo maro. / Nke ti mula na lele.", "Nous voulons acheter du riz. / Je ne voulais pas arriver trop tard.",
  S_LEX + " ; " + S_SNK, "SNK-LEX-0876 (source_externe_a_verifier) ; corpus texte_marche marche-03/journee-03 (o ni mula na xobo maro), texte_village village-24, snk_engine docs/langue/etre-avoir.md (Nke ti mula)",
  "élevé", "SOURCE_VERIFIEE",
  "La source externe du lexique est corroborée par le corpus relu par le locuteur : le statut peut passer en validation référent après confirmation.")
R("kitta", "pouvoir, réussir, savoir (faire)", "verbe", "verbe prioritaire lot 2 — modal",
  "", "", "", "", "", "katti ; katta", SILVAR,
  "Abdulaye da kasetin xobo, ma i wa katta sooninkanxanne terinkana.", "Abdoulaye a acheté une cassette pour pouvoir écouter le soninké.",
  S_SILD, U_SILD + " (entrée katti/katta)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Forme non attestée dans le corpus du projet. La graphie kati du corpus a d'autres emplois (voir ligne kati). Autre exemple SIL : Xarallenman kati xaranŋa « l'élève a réussi (ses études) ». Également documenté dans l'étude être/avoir (capacité vs possession).")
R("kati", "particule (sens variable selon les contextes)", "particule", "emploi grammatical à élucider",
  "", "", "", "", "", "katti (SIL : pouvoir)", PROJET,
  "Kati n'ga xenxe-ne, n'di ma sefe.", "Avant de dormir, je parle avec ma mère.",
  S_SNK, "corpus texte_journee journee-08 (kati n'ga … « avant de »), texte_travail travail-04 (… safa kati nké waxi « … à mon frère ») ; " + U_SILD + " (katti « pouvoir »)",
  "faible", "CONTRADICTOIRE_ENTRE_SOURCES",
  "Trois analyses possibles selon les sources : auxiliaire modal « pouvoir » (SIL), introducteur de subordonnée temporelle, particule oblique. À trancher impérativement avec le référent ; ne pas employer kati comme « pouvoir » dans le dialecte du projet sans validation.")
R("kini", "donner", "verbe", "verbe prioritaire lot 2 — transfert",
  "construction : objet direct + kini + bénéficiaire (pronom ou nom)", "", "", "", "", "kunu (graphie du dictionnaire projet)", PROJET,
  "Dji kini nke. / Kudu xa kini ŋa, yampimaxa.", "Donne-moi l'eau. / Donne-moi aussi une cuillère, s'il te plaît.",
  S_LEX + " ; " + S_SNK, "SNK-LEX-0724 (source_externe_a_verifier) ; corpus texte_marche marche-24 (dni kini nké), texte_repas repas-11, texte_pluies pluies-09 (a di yigande kini seliŋu)",
  "élevé", "SOURCE_VERIFIEE",
  "Source externe corroborée par le corpus du locuteur. ŋa = à moi (postposition).")
R("wutu", "prendre", "verbe", "verbe prioritaire lot 2 — manipulation",
  "transitif ; nom d'action wutunde ; gérondif non documenté dans le YAML du référent (lacune)", "", "", "", "", "", PROJET,
  "", "", S_REF + " ; " + S_LEX, "data/grammaire/soninke.yaml (wutuer, transitif) ; corpus validation_02 v-116 à v-122",
  "élevé", "SOURCE_VERIFIEE", "Gérondif absent du YAML : à demander au référent (rapport qualité).")
R("yige", "manger", "verbe", "verbe prioritaire lot 2 — vie quotidienne",
  "transitif ; gérondif yigene ; nom d'action yigaye", "", "", "", "",
  "iige (SNK-LEX-1340) ; yigué / yigu (graphies du corpus en orthographe d'origine)", PROJET,
  "Iku n'yi maro ke yigane koota su. / A do maro ke yigaye ni ya me.", "Ils mangent le riz tous les jours. / Il est en train de manger le riz.",
  S_REF + " ; " + S_SNK + " ; " + S_LEX, "data/grammaire/soninke.yaml (yigeyer, transitif) ; corpus validation_02 v-161/v-162, texte_journee journee-08 ; SNK-LEX-1340 (Daga iige, valide_par_referent)",
  "élevé", "SOURCE_VERIFIEE", "Variante iige attestée dans un composé validé par le référent ; yigué/yigane sont des graphies non normalisées du corpus.")
R("mini", "boire", "verbe", "verbe prioritaire lot 2 — vie quotidienne",
  "transitif ; gérondif minini ; nom d'action mine", "", "", "", "", "", PROJET,
  "Na yigue ado n'a dji mini.", "Ensuite, je mange et je bois de l'eau.",
  S_REF + " ; " + S_SNK + " ; " + S_LGV, "data/grammaire/soninke.yaml (minier, transitif) ; corpus texte_journee journee-01 ; " + U_LGV + " (mìní boire)",
  "élevé", "SOURCE_VERIFIEE", "")
R("xenxe", "dormir", "verbe", "verbe prioritaire lot 2 — vie quotidienne",
  "", "", "", "", "", "xénxé (graphie du corpus) ; qenqe (SNK-LEX-0782, graphie LGIDF qènqé)", PROJET,
  "Ake n'xenxe. / Kempale, n'soxu, n'xenxe.", "Il a dormi. / Ensuite, je me couche et je dors.",
  S_SNK + " ; " + S_LEX + " ; " + S_LGV, "corpus validation_03 03-04/03-05 et texte_journee journee-08 ; SNK-LEX-0782 (qenqe dormir, source_externe_a_verifier) ; " + U_LGV + " (qènqé dormir)",
  "élevé", "VARIANTE_DOCUMENTEE",
  "Deux graphies du même lexème selon les sources (xenxe dans le corpus du projet, qenqe/qènqé dans le lexique externe et LGIDF) : conserver les deux, à relier comme variantes après avis du référent.")
R("qenqe", "dormir (variante graphique)", "verbe", "verbe prioritaire lot 2 — vie quotidienne",
  "", "", "", "", "", "xenxe (corpus du projet)", "",
  "", "", S_LEX + " ; " + S_LGV, "SNK-LEX-0782 ; " + U_LGV, "moyen", "VARIANTE_DOCUMENTEE",
  "Ne pas créer de doublon avec xenxe : rattacher comme variante de la même entrée après validation référent.")
R("soxu", "se coucher", "verbe", "verbe prioritaire lot 2 — vie quotidienne",
  "", "", "", "", "", "sohu (SNK-LEX-1341, composé Daga sohu « aller dormir »)", PROJET,
  "N'guida ti ke dagana soxu fene.", "Mon frère dit qu'il ira dormir tôt.",
  S_SNK + " ; " + S_LEX, "corpus texte_journee journee-08 (n'soxu « je me couche »), texte_repas repas-20 ; SNK-LEX-1341 (Daga sohu, validation_referent_utilisateur)",
  "moyen", "SOURCE_VERIFIEE",
  "soxu (corpus) et sohu (composé validé par le référent) sont probablement le même lexème (alternance x/h) : à confirmer ; ne pas fusionner sans preuve.")
R("giri", "se lever ; se réveiller", "verbe", "verbe prioritaire lot 2 — vie quotidienne",
  "", "", "", "", "", "guiri (graphie du corpus)", PROJET,
  "Nke na guiri. / Nke faba giri fene.", "Je me lève. / Mon père s'est levé tôt.",
  S_LEX + " ; " + S_SNK, "SNK-LEX-0790 (source_externe_a_verifier) ; corpus texte_journee journee-01 (nké na guiri), texte_pluies (giri féné)",
  "élevé", "SOURCE_VERIFIEE",
  "« se réveiller » et « se lever » ne sont pas distingués dans les traductions du corpus ; le référent devra dire s'il existe un verbe propre pour « se réveiller » (SNK-LEX-0102 yaxawunyi-yen xedie « réveiller » est transitif).")
R("goli", "travailler", "verbe", "verbe prioritaire lot 2 — vie quotidienne",
  "gérondif golini ; nom d'action goliye", "", "", "", "", "", PROJET,
  "Xa goli. / Maxa goli.", "Travaillez. / Ne travaille pas.",
  S_REF + " ; " + S_SNK + " ; " + S_LEX, "data/grammaire/soninke.yaml (golier) ; corpus validation_01 v-039/v-040 ; SNK-LEX-0010 (fourni_par_referent), SNK-LEX-1339 (Daga goli)",
  "élevé", "SOURCE_VERIFIEE", "")
R("xara", "lire ; apprendre", "verbe", "verbe prioritaire lot 2 — vie quotidienne",
  "", "", "", "", "", "", PROJET,
  "N'di xara. / N'di page lamanou xara livrou yogo.", "Je lis. / Je lis quelques pages d'un livre.",
  S_SNK + " ; " + S_SNKV + " ; " + S_SILD, "corpus texte_journee journee-06/journee-08 ; " + U_SNKV + " (Xara : lire, apprendre) ; exemple SIL « O n'o sooninkanxannen xara n'a safa » (lisons et écrivons notre langue)",
  "moyen", "SOURCE_VERIFIEE",
  "« apprendre » et « lire » confondus dans les sources consultées ; LGIDF donne par ailleurs bíré pour « apprendre » (à vérifier, homographie avec bire « vivre » du référent).")
R("xaranŋundi", "enseigner", "verbe", "verbe prioritaire lot 2 — vie quotidienne",
  "dérivé causatif de xara (lire/apprendre)", "", "", "", "", "xaranŋa (graphie du dictionnaire SIL)", "",
  "", "", S_SNKV + " ; " + S_SILD, U_SNKV + " (Xaranŋundi : enseigner) ; " + U_SILD + " (exemple Xarallenman kati xaranŋa)",
  "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Dérivation en -ndi cohérente avec les paires du lexique projet (bagu/bagandi). Ŋ conservé selon l'orthographe des sources (Mali : ŋ/ɲ ; Sénégal : ñ).")
R("terinke", "écouter", "verbe", "verbe prioritaire lot 2 — perception",
  "", "", "", "", "", "terinka (graphie du corpus)", PROJET,
  "N'di xara moxo n'terinka.", "J'écoute le professeur (litt. segment à analyser avec le référent).",
  S_SNK + " ; " + S_SNKV + " ; " + S_SILD, "corpus texte_journee journee-06 ; " + U_SNKV + " (Terinka : écouter) ; exemple SIL « … sooninkanxanne terinkana »",
  "moyen", "SOURCE_VERIFIEE", "Lexème attesté par trois sources ; le découpage exact de l'exemple du corpus reste à valider.")
R("xobo", "acheter", "verbe", "verbe prioritaire lot 2 — échanges",
  "", "", "", "", "", "", PROJET,
  "O ni mula na xobo maro. / Bawoni nke na n'xawa maro ado teh n'ya xobono.", "Nous voulons acheter du riz. / Parce que je dois acheter du riz et du thé.",
  S_LEX + " ; " + S_SNK, "SNK-LEX-0875 (source_externe_a_verifier) ; corpus texte_marche marche-04, journee-03/journee-04 (fo q'xobo o xaju)",
  "élevé", "SOURCE_VERIFIEE", "Source externe corroborée par le corpus du locuteur.")
R("gage", "vendre", "verbe", "verbe prioritaire lot 2 — échanges",
  "gérondif gagene ; nom d'action gage-ye", "", "", "", "", "", PROJET,
  "", "", S_REF + " ; " + S_LEX, "data/grammaire/soninke.yaml (gageer) ; SNK-LEX-0179 (fourni_par_referent), SNK-LEX-1066/1067",
  "élevé", "SOURCE_VERIFIEE", "Aucune phrase d'exemple complète relevée dans le corpus consulté (lacune signalée au rapport qualité).")
R("xanu", "aimer", "verbe", "verbe prioritaire lot 2 — états",
  "gérondif xanunu ; nom d'action xanu-ye", "", "", "", "", "kanu (LGIDF kànú, variété du Kingui)", PROJET,
  "", "", S_REF + " ; " + S_LEX + " ; " + S_LGV, "data/grammaire/soninke.yaml (xanuer) ; SNK-LEX (fourni_par_referent) ; " + U_LGV + " (kànú aimer)",
  "élevé", "SOURCE_VERIFIEE",
  "Variante régionale possible kànú (LGIDF, Kingui) : à vérifier, ne pas fusionner.")
R("bire", "vivre", "verbe", "verbe prioritaire lot 2 — états",
  "gérondif birene ; nom d'action bire-ye", "", "", "", "", "", PROJET,
  "", "", S_REF + " ; " + S_LEX, "data/grammaire/soninke.yaml (bireer) ; SNK-LEX-0180 (fourni_par_referent : vivre / instant, moment / quand)",
  "élevé", "SOURCE_VERIFIEE",
  "Polysémie documentée par le référent : « vivre » et « instant, moment, quand ». SNK-LEX-0512 bire « vivre » (candidat) est un doublon probable de SNK-LEX-0180 : à signaler, pas à supprimer.")
R("kara", "casser", "verbe", "verbe prioritaire lot 2 — actions",
  "gérondif karana ; nom d'action kara-nde", "", "", "", "", "", PROJET,
  "", "", S_REF + " ; " + S_LEX + " ; " + S_CD19, "data/grammaire/soninke.yaml ; SNK-LEX-0036 (fourni_par_referent) ; " + U_CD19 + " §1 (kárá « casser », ton haut)",
  "élevé", "SOURCE_VERIFIEE",
  "Voir la ligne « kara = mourir » : paire minimale tonale kárá/kàrá décrite par LGIDF. Les deux sens doivent rester des entrées distinctes.")
R("kara", "mourir (variété du Kingui — homonyme tonal de kárá « casser »)", "verbe",
  "verbe prioritaire lot 2 — homonymie tonale",
  "la distinction ne repose que sur le ton (kàrá ton bas), que l'orthographe du projet ne note pas",
  "", "", "", "", "", KINGUI + " ; " + KINGI,
  "", "", S_CD19 + " ; " + S_GRE79, U_CD19 + " §1 (kárá casser / kàrá mourir) ; Grégoire 1979 (réf. G1979 de snk_engine : kara mourir)",
  "moyen", "CONTRADICTOIRE_ENTRE_SOURCES",
  "Le référent du projet donne kara = casser (SNK-LEX-0036) ; LGIDF et Grégoire attestent kàrà = mourir ailleurs. Conserver les deux entrées avec leurs références ; aucun exemple de « mourir » relevé dans le corpus du projet.")
R("faye", "regarder", "verbe", "verbe prioritaire lot 2 — perception",
  "gérondif fayeni ; nom d'action fayinde", "", "", "", "", "", PROJET,
  "Xa wa fayeni. / Maxa faye.", "Vous regardez. / Ne regarde pas.",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml (fayeer) ; corpus validation_01 v-020/v-025/v-026",
  "élevé", "SOURCE_VERIFIEE", "")
R("sefe", "parler", "verbe", "verbe prioritaire lot 2 — parole",
  "gérondif sefene ; nom d'action sefeye", "", "", "", "", "", PROJET,
  "Kati n'ga xenxe-ne, n'di ma sefe.", "Avant de dormir, je parle avec ma mère.",
  S_REF + " ; " + S_SNK + " ; " + S_SILD, "data/grammaire/soninke.yaml (sefeer ; gérondif sefene corrigé par le locuteur) ; corpus texte_journee journee-08 ; " + U_SILD + " (titre O nan sefe sooninken do faransen ŋa)",
  "élevé", "SOURCE_VERIFIEE", "")
R("safa", "écrire", "verbe", "verbe prioritaire lot 2 — parole",
  "transitif ; gérondif safana ; nom d'action safande", "", "", "", "",
  "safandi / safandé (graphies du corpus en orthographe d'origine)", PROJET,
  "Watia kundu, nke fayi letra n'ya safa kati nke waxi.", "En ce moment, j'écris une lettre à mon frère.",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml (safaer, transitif) ; corpus texte_travail travail-04, texte_journee journee-06 (n'safandi cahier noxo)",
  "élevé", "SOURCE_VERIFIEE",
  "Les graphies safandi/safandé du corpus pourraient refléter un dérivé causatif ou une simple variation orthographique : à trancher avec le référent.")
R("wuru", "courir", "verbe", "verbe prioritaire lot 2 — mouvement",
  "gérondif wurunu ; nom d'action wuruye", "", "", "", "", "", PROJET,
  "", "", S_REF + " ; " + S_LEX, "data/grammaire/soninke.yaml (wuruer) ; SNK-LEX-0011 (fourni_par_referent)",
  "élevé", "SOURCE_VERIFIEE", "Aucun exemple complet relevé dans le corpus consulté.")
R("tuga", "payer", "verbe", "verbe fréquent (lot 4)",
  "", "", "", "", "", "", PROJET,
  "Kempale o di tuga.", "Puis nous payons.",
  S_SNK, "corpus texte_journee journee-04", "moyen", "A_CONFIRMER_PAR_LOCUTEUR", "")
R("taxalema", "rencontrer", "verbe", "verbe fréquent (lot 4)",
  "", "", "", "", "", "", PROJET,
  "Saxa ke, o di o taxalema n'wori.", "Au marché, nous rencontrons notre voisin.",
  S_SNK, "corpus texte_journee journee-03", "moyen", "A_CONFIRMER_PAR_LOCUTEUR", "")
R("tirindi", "demander", "verbe", "verbe fréquent (lot 4)",
  "", "", "", "", "", "", PROJET,
  "A di o tirindi o ga daga-na noqu be. / Ma a di tirindi : « A ma-ma moxo ? »", "Il nous demande où nous allons. / Ma mère m'a demandé : « Comment va ta grand-mère ? »",
  S_SNK, "corpus texte_journee journee-03, texte_village village-26", "moyen", "SOURCE_VERIFIEE",
  "Attesté deux fois dans le corpus relu par le locuteur.")
R("waxi", "frère", "nom", "nom de parenté (contexte des verbes prioritaires)",
  "pluriel waxi-ni", "", "pl", "", "", "waxi-ni (pluriel)", PROJET,
  "Waxi-ni filli yani maxa.", "J'ai deux frères.",
  S_SNK, "corpus texte_marche marche-18, texte_travail travail-04 (nké waxi)", "moyen", "SOURCE_VERIFIEE",
  "Utile aux exemples ; entrée lexicale à comparer au lexique existant.")
R("guida", "sœur (ou frère — traductions divergentes dans le corpus)", "nom", "nom de parenté",
  "", "", "", "", "", "", PROJET,
  "Ado guida naxaru siki. / N'guida ti ke dagana soxu fene.", "Et trois sœurs. / Mon frère dit qu'il ira dormir tôt.",
  S_SNK, "corpus texte_marche marche-18 (guida traduit « sœurs ») et texte_repas repas-20 (n'guida traduit « mon frère »)",
  "faible", "CONTRADICTOIRE_ENTRE_SOURCES",
  "Les traductions françaises du même corpus hésitent entre « sœur » et « frère » : sens exact à trancher par le référent avant toute intégration.")
# NOTE : aucun verbe générique « faire » n'a été vérifié dans les sources consultées ;
# le soninké emploie des verbes spécifiques ou le causatif -ndi (bagu « sortir » →
# bagandi « faire sortir », SNK-LEX-0324 candidat). Lacune documentée dans
# docs/recherche/rapport-qualite-2026-10-24.md — pas de ligne créée pour éviter
# une forme non soninké dans le lexique.

# ===========================================================================
# E. PRONOMS / SUBORDONNANTS RELATIFS (lot 3)
# ===========================================================================
R("be", "qui, que (relateur)", "particule_relative", "relateur de proposition relative",
  "antécédent + be + ga + proposition ; le soninké n'a pas de pronoms relatifs fléchis : un seul relateur pour qui/que/dont/où",
  "", "", "", "", "", PROJET + " ; " + SILVAR,
  "N maama be ga ñi faayindini soyi …", "… (exemple du livret de Dakar 2001 ; traduction à compléter depuis le livret)",
  S_LEX + " ; " + S_SILG + " ; " + S_LIV01, "SNK-LEX-0430 (particule relateur) ; " + U_SILG + " (relatif be) ; " + U_LIV01 + " §IV",
  "élevé", "SOURCE_VERIFIEE",
  "Ne pas supposer un pronom relatif par fonction du français : les sources n'attestent qu'un relateur unique be (+ ga).")
R("ga", "que, qui, quand (subordonnant)", "conjonction", "subordonnant de relative et de complétive",
  "introduit la proposition dépendante après be ; aussi dans les interrogatives indirectes",
  "", "", "", "", "", PROJET,
  "A di o tirindi o ga daga-na noqu be. / Kiyé ke ga baka.", "Il nous demande où nous allons. / … avant que le soleil se lève (le lever du soleil).",
  S_SNK, "corpus texte_journee journee-03, journee-01 ; snk_engine docs/langue/conjonctions.md (subordonnée ga, quand n'ga, condition n'gana)",
  "moyen", "SOURCE_VERIFIEE", "Absent du lexique de base : nouvelle entrée grammaticale.")
R("construction relative : nom + be + ga + verbe", "celui qui / ce qui / que", "construction_relative",
  "stratégie de relativisation",
  "pas de pronom relatif dédié ; l'antécédent est suivi du relateur be puis du subordonnant ga",
  "", "", "", "", "", SILVAR + " ; " + PROJET,
  "Yugo be ga sefene.", "Celui qui parle. (assemblage d'après les règles documentées)",
  S_SILG + " ; " + S_LIV01, U_SILG + " ; livret Dakar 2001 §IV", "faible", "HYPOTHESE_NON_VALIDEE",
  "La stratégie est documentée (be + ga), mais cette phrase exacte n'est attestée dans aucune source : ne pas la présenter comme une phrase réelle avant validation.")
R("sere be ga sefene", "l'homme qui parle / celui qui parle", "construction_relative",
  "assemblage régulier non attesté", "sere (homme) + be + ga + sefene (gérondif de sefe)",
  "3", "sg", "", "", "", PROJET,
  "Sere be ga sefene.", "L'homme qui parle.",
  "assemblage d'après : " + S_SILG + " ; " + S_LEX + " ; " + S_REF, U_SILG + " (relatif be) ; SNK-LEX-0908 (sere homme) ; data/grammaire/soninke.yaml (sefe, gérondif sefene)",
  "faible", "HYPOTHESE_NON_VALIDEE",
  "Tous les éléments sont attestés séparément ; la phrase complète ne l'est pas. À faire valider ou corriger par le référent.")
R("sere be ga yigene", "l'homme qui mange / celui qui mange", "construction_relative",
  "assemblage régulier non attesté", "sere + be + ga + yigene (gérondif de yige)",
  "3", "sg", "", "", "", PROJET,
  "", "", "assemblage d'après : " + S_SILG + " ; " + S_REF, U_SILG + " ; data/grammaire/soninke.yaml (yige, gérondif yigene)",
  "faible", "HYPOTHESE_NON_VALIDEE", "Même statut que la ligne précédente.")
R("fo … ga", "ce que, ce dont", "construction_relative", "relatif sans antécédent explicite",
  "le corpus montre une construction avec fo « chose » + subordonnée en ga",
  "", "", "", "", "", PROJET,
  "O di fo q'xobo o xaju.", "Nous achetons ce dont nous avons besoin.",
  S_SNK, "corpus texte_journee journee-04", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Analyse incomplète : le segment q'xobo n'est pas élucidé (assimilation de n' devant x ?). Ne pas généraliser la construction avant validation.")

# ===========================================================================
# F. DÉMONSTRATIFS ET DÉTERMINANTS (lot 3)
# ===========================================================================
R("ke", "ceci, celui-ci ; ce, cette (démonstratif)", "demonstratif", "proximité — singulier",
  "postposé au nom : maro ke « ce riz / le riz »", "", "sg", "", "",
  "ké (graphie tonale LGIDF)", PROJET + " ; " + KINGUI,
  "Xa na maro ke ŋ'wori saxa.", "Voyez le riz au marché.",
  S_LEX + " ; " + S_CD19 + " ; " + S_SNK + " ; " + S_SNKG, "SNK-LEX-0847 (ceci, celui-ci) ; " + U_CD19 + " §3 (ké háré « cette main ») ; corpus validation_02 v-114/v-125/v-161 ; glossaire Soninkara (Ke : celui-ci)",
  "élevé", "SOURCE_VERIFIEE", "")
R("ke", "le, la (déterminant défini du dialecte du projet)", "determinant", "défini — postposé",
  "dans le corpus du projet, ke sert aussi de déterminant défini : ka ke « la maison »",
  "", "", "", "", "", PROJET,
  "A yi ka ke.", "Elle est à la maison (litt. elle est maison la).",
  S_SNK, "corpus texte_marche ; snk_engine docs/langue/nom.md",
  "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Divergence avec LGIDF/Kingi où le déterminé se marque par une nasale finale + ton bas : le dialecte du projet semble employer ke. À faire trancher par le référent ; ne pas mélanger les deux systèmes dans le site.")
R("ku", "ceux-ci, celles-ci ; ces (démonstratif pluriel)", "demonstratif", "proximité — pluriel",
  "postposé au nom : kú hárú « ces mains »", "", "pl", "", "",
  "kú (graphie tonale LGIDF)", KINGUI,
  "", "", S_CD19 + " ; " + S_SNKG, U_CD19 + " §3 (kú hárú) ; glossaire Soninkara (Ku : celui-ci)",
  "moyen", "CONTRADICTOIRE_ENTRE_SOURCES",
  "Conflit à conserver tel quel : le référent du projet donne ku = « offrir » (SNK-LEX-0171, fourni_par_referent) ; LGIDF et le glossaire Soninkara donnent ku = démonstratif. Les deux entrées doivent coexister avec leurs références.")
R("kuyi", "offrir (sens relevé par Grégoire 1979)", "verbe", "homonymie avec le démonstratif/verbe ku",
  "", "", "", "", "", "", "", "", "",
  S_GRE79 + " ; " + S_LEX, "Grégoire 1979 (réf. G1979 de snk_engine) ; SNK-LEX-0103 (kuyi rêver, fourni_par_referent)",
  "faible", "CONTRADICTOIRE_ENTRE_SOURCES",
  "Le référent donne kuyi = rêver ; Grégoire 1979 donne kuyi = offrir. Divergence non résolue : conserver les deux gloses avec leurs sources.")
R("ken", "cela, celui-là", "demonstratif", "éloignement — singulier",
  "", "", "sg", "", "", "ken (SNKG Ken)", PROJET,
  "", "", S_LEX + " ; " + S_SNKG, "SNK-LEX-0846 (cela, celui-là, source_externe_a_verifier) ; glossaire Soninkara (Ken : celui-là)",
  "moyen", "SOURCE_VERIFIEE", "Deux sources externes concordantes ; confirmation référent à obtenir.")
R("kun", "ceux-là, celles-là", "demonstratif", "éloignement — pluriel",
  "", "", "pl", "", "", "", "",
  "", "", S_SNKG, "glossaire Soninkara (Kun : ceux-là)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Source unique (glossaire en ligne) ; aucun exemple.")
R("kere", "ici", "adverbe", "démonstratif de lieu — proximité",
  "", "", "", "", "", "", PROJET,
  "", "", S_LEX, "SNK-LEX-0844 (ici, source_externe_a_verifier)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Déjà au lexique ; documenté ici pour l'inventaire des démonstratifs.")
R("no", "là", "adverbe", "démonstratif de lieu — éloignement",
  "", "", "", "", "", "", PROJET,
  "", "", S_LEX + " ; " + S_SNKG, "SNK-LEX-0845 (là) ; glossaire Soninkara (No : là-bas)", "moyen", "SOURCE_VERIFIEE", "")
R("doke", "là-bas (éloignement)", "adverbe", "démonstratif de lieu — grand éloignement",
  "", "", "", "", "", "dooke ; doono (glossaire Soninkara)", "",
  "", "", S_SNK + " ; " + S_SNKG, "snk_engine docs/langue/nom.md (démonstratifs ke kundu / ke doke) ; glossaire Soninkara (Dooke, Doono : là-bas)",
  "faible", "A_CONFIRMER_PAR_LOCUTEUR", "Sources documentaires sans exemple complet ; graphies divergentes (doke/dooke/doono) à normaliser avec le référent.")
R("kundu", "ici, tout près (proximité immédiate)", "adverbe", "démonstratif de lieu — proximité",
  "watia kundu « en ce moment (précisément) »", "", "", "", "", "", PROJET,
  "Watia kundu, nke fayi letra n'ya safa kati nke waxi.", "En ce moment, j'écris une lettre à mon frère.",
  S_SNK, "corpus texte_travail travail-04 ; snk_engine docs/langue/nom.md (ke kundu)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Analyse exacte (kundu = proximité spatiale ou temporelle ?) à confirmer.")
R("ke kundu / ke doke", "celui-ci (tout près) / celui-là (là-bas)", "demonstratif",
  "démonstratif renforcé par un adverbe de lieu", "", "", "", "", "", "", PROJET,
  "", "", S_SNK, "snk_engine docs/langue/nom.md", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Combinaisons mentionnées par la documentation du corpus, sans phrase complète : statut hypothétique jusqu'à validation.")

# ===========================================================================
# G1. INTERROGATIFS
# ===========================================================================
R("minna", "où", "pronom_interrogatif", "lieu",
  "", "", "", "", "", "", KINGI + " ; " + PROJET,
  "Anke dagana minna ?", "Où vas-tu ? (litt. tu pars où)",
  S_CRE18 + " ; " + S_SNK, U_CRE18 + " ex. (12c) Hàatú nà mínna ? ; corpus texte_marche marche-01",
  "élevé", "SOURCE_VERIFIEE", "")
R("mane", "quoi, que", "pronom_interrogatif", "chose",
  "", "", "", "", "", "mané (graphie du corpus)", PROJET,
  "", "", S_SNK, "snk_engine docs/langue/conjonctions.md (interrogatifs) ; corpus texte_marche marche-03 (mané-ni)",
  "moyen", "SOURCE_VERIFIEE", "")
R("mane-ni", "pourquoi", "pronom_interrogatif", "cause",
  "dérivé de mane « quoi » + ni", "", "", "", "", "", PROJET,
  "Mane-ni anke n'ga dagana saxa ?", "Pourquoi vas-tu au marché ?",
  S_SNK, "corpus texte_marche marche-03 ; snk_engine docs/langue/conjonctions.md",
  "moyen", "SOURCE_VERIFIEE", "")
R("ko", "qui (interrogatif)", "pronom_interrogatif", "personne",
  "", "", "", "", "", "", "",
  "Ko nda futo ke yiga ?", "Qui a mangé le fonio ?",
  S_SNKC3 + " ; " + S_CRE18 + " ; " + S_SNK, U_SNKC3 + " (ko = qui) ; Creissels 2018 (kó « qui », ex. Kó nà kónpè-n dí ?) ; corpus texte_marche marche-05 (anké n'do ko dagana domé ? « avec qui »)",
  "moyen", "CONTRADICTOIRE_ENTRE_SOURCES",
  "Conflit majeur à conserver : le référent du projet donne ko = « dire » (SNK-LEX-0164, verbe, gérondif kono) ; trois sources externes donnent ko = « qui ». Les deux entrées doivent coexister ; le contexte (verbe conjugué vs interrogatif) les distingue.")
R("kan", "quand", "pronom_interrogatif", "temps",
  "", "", "", "", "", "kan dimma (quand, selon la documentation du corpus)", "",
  "An ri kan koota ?", "Quand viens-tu ?",
  S_SNKC3 + " ; " + S_SNK, U_SNKC3 + " ; snk_engine docs/langue/conjonctions.md (kan dimma)",
  "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Sources pédagogiques/documentaires sans corpus validé ; kan apparaît aussi comme subordonnant temporel (n'ga dans le corpus du projet).")
R("mani-me", "combien", "pronom_interrogatif", "quantité",
  "", "", "", "", "", "", "",
  "", "", S_SNK, "snk_engine docs/langue/conjonctions.md", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Mention documentaire sans exemple complet.")
R("moxo", "comment", "pronom_interrogatif", "manière",
  "", "", "", "", "", "", PROJET + " ; " + MAURI,
  "A ma-ma moxo ? / An moxo ?", "Comment va ta grand-mère ? / Comment vas-tu ?",
  S_SNK + " ; " + S_SONK3, "corpus texte_village village-26 ; " + U_SONK3 + " (AN MOXO ?)", "élevé", "SOURCE_VERIFIEE",
  "Homographie : moxo apparaît aussi comme élément nominal dans xara moxo (segment du corpus journee-06, analyse à valider) et dans le titre SONK3 « XORI BAASI ME NA » voisin.")
R("ba", "est-ce que (particule finale d'interrogation totale)", "particule_interrogative",
  "interrogation oui/non", "se place en fin de phrase", "", "", "", "", "", PROJET,
  "Ake n'yi rini ba ?", "Est-ce qu'il viendra ?",
  S_SNK + " ; " + S_LEX + " ; " + S_LIV01, "corpus serie_02 02-21 ; SNK-LEX-0232 (Est-ce que ; appellation honorifique) ; livret Dakar 2001 (a xooro ba ?)",
  "élevé", "SOURCE_VERIFIEE",
  "L'entrée existante SNK-LEX-0232 cumule deux sens (particule interrogative et appellation honorifique « monsieur ») : à ventiler sans rien supprimer.")
R("keti", "est-ce que (selon le glossaire Soninkara)", "particule_interrogative", "interrogation",
  "", "", "", "", "", "", "",
  "", "", S_SNKG + " ; " + S_LEX, "glossaire Soninkara (Keti? : est-ce que) ; SNK-LEX-0115 (keti toucher, fourni_par_referent)",
  "faible", "CONTRADICTOIRE_ENTRE_SOURCES",
  "Le référent donne keti = « toucher » ; le glossaire Soninkara donne Keti? = « est-ce que ». Conserver les deux avec références ; la forme interrogative n'est corroborée par aucune autre source consultée.")
R("xori", "", "mot_interrogatif", "élément cité sans glose assurée",
  "", "", "", "", "", "", MAURI,
  "Xori toora nt'an ?a ? / Xori baasi me na ?", "N'as-tu rien de mal ? / Rien ne s'est-il passé de mal ?",
  S_SONK3 + " ; " + S_LIV01, U_SONK3 + " (salutations) ; livret Dakar 2001 (liste des interrogatifs xori/ba/keti)",
  "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Traduction volontairement laissée vide : dans les salutations du cours mauritanien, xori semble signifier « chose fâcheuse, malheur » ; le livret de Dakar le range parmi les interrogatifs sans le gloser. À élucider avec le référent.")
R("ayi", "non", "adverbe", "réponse négative",
  "", "", "", "", "", "", PROJET,
  "", "", S_SNK + " ; " + S_WK, "snk_engine docs/langue/conjonctions.md (non = ayi) ; " + U_WK, "moyen", "SOURCE_VERIFIEE", "")
R("yo", "oui", "adverbe", "réponse affirmative",
  "", "", "", "", "", "", "",
  "", "", S_WK, U_WK + " (section Lexique)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Source unique et peu fiable (Wikipédia) ; à confirmer en priorité car mot très demandé par les apprenants.")

# ===========================================================================
# G2. INDÉFINIS ET QUANTIFICATEURS
# ===========================================================================
R("su", "tout, tous ; chaque", "quantificateur", "indéfini de totalité",
  "postposé au nom : suxuba su « chaque matin », koota su « tous les jours »", "", "", "", "",
  "sú (graphie tonale LGIDF)", PROJET + " ; " + KINGUI,
  "Iku n'yi maro ke yigane koota su.", "Ils mangent le riz tous les jours.",
  S_LEX + " ; " + S_LGQ + " ; " + S_SNK, "SNK-LEX-0916 (tout, tous) ; " + U_LGQ + " (sú) ; corpus validation_02 v-161, texte_journee journee-01",
  "élevé", "SOURCE_VERIFIEE", "")
R("yogo", "un certain, quelque", "quantificateur", "indéfini de quantité non précisée",
  "postposé au nom : livrou yogo « quelque livre » ; souvent suivi de baane", "", "", "", "",
  "yúgó (Creissels) ; yògó (LGIDF)", PROJET + " ; " + KINGI,
  "N'di page lamanou xara livrou yogo.", "Je lis quelques pages d'un livre.",
  S_SNK + " ; " + S_CRE18 + " ; " + S_LGQ + " ; " + S_LEX, "corpus texte_journee journee-08 ; Creissels 2018 (yúgó « un certain ») ; " + U_LGQ + " ; SNK-LEX-0246 (baane, « associé à des déterminants quantifieurs : yogo, tana »)",
  "moyen", "SOURCE_VERIFIEE", "")
R("gabe", "beaucoup", "quantificateur", "indéfini de grande quantité",
  "postposé au nom", "", "", "", "", "gábè (LGIDF) ; gabo (graphie du corpus)", PROJET + " ; " + KINGUI,
  "Yite gabo ni a ni a noxo.", "Il y a beaucoup d'arbres dedans.",
  S_LEX + " ; " + S_LGQ + " ; " + S_SNK + " ; " + S_CRE18, "SNK-LEX-0917 ; " + U_LGQ + " (gábè) ; snk_engine data/references/mots.yaml (texte_travail) ; Creissels 2018 ex. (10a) ó ntá gàbà Hàatú ŋàllí",
  "élevé", "SOURCE_VERIFIEE", "")
R("honne", "peu", "quantificateur", "indéfini de petite quantité",
  "postposé au nom", "", "", "", "", "hónné (LGIDF)", PROJET + " ; " + KINGUI,
  "", "", S_LEX + " ; " + S_LGQ, "SNK-LEX-0809 ; " + U_LGQ + " (hónné)", "moyen", "SOURCE_VERIFIEE",
  "Deux sources externes concordantes ; pas d'exemple dans le corpus du projet.")
R("tana", "autre", "adjectif", "indéfini d'altérité",
  "postposé au nom", "", "", "", "", "tàná (LGIDF)", PROJET + " ; " + KINGUI,
  "", "", S_LEX + " ; " + S_LGQ, "SNK-LEX-0811 ; " + U_LGQ + " (tàná)", "moyen", "SOURCE_VERIFIEE", "")
R("baabe", "chacun", "quantificateur", "indéfini distributif",
  "", "", "", "", "", "", PROJET,
  "", "", S_LEX, "SNK-LEX-1345 (valide_par_referent)", "élevé", "SOURCE_VERIFIEE",
  "Déjà validé par le référent ; rappelé ici pour l'inventaire des indéfinis.")
R("fo", "chose", "nom", "indéfini — support des relatifs sans antécédent",
  "", "", "", "", "", "", PROJET,
  "O di fo q'xobo o xaju.", "Nous achetons ce dont nous avons besoin.",
  S_SNK, "corpus texte_journee journee-04", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Glose inférée d'un seul exemple ; à confirmer.")
R("sere su", "personne (aucun homme), avec négation", "construction_indefinie", "indéfini négatif",
  "nom sere « homme » + su « aucun/tout » + copule négative", "", "", "présent", "négatif", "", PROJET,
  "Sere su n'ti ka ke noxo.", "Il n'y a personne dans la maison.",
  S_SNK + " ; " + S_LEX, "snk_engine docs/langue/nom.md ; SNK-LEX-0908 (sere homme)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR", "")

# ===========================================================================
# G3. NÉGATION
# ===========================================================================
R("ma", "ne … pas (accompli)", "marqueur_negation", "négation de l'accompli",
  "pronom + ma + verbe ; s'assimile en m' devant b/f/m (SNK-GRM-0028)", "", "", "passé (accompli)", "négatif",
  "má (graphie tonale)", PROJET + " ; " + KINGI,
  "A ma yi ka ke.", "Elle n'est pas à la maison. (variante relevée dans le corpus)",
  S_LEX + " ; " + S_CRE18, "SNK-GRM-0033 ; Creissels 2018 Tableau 4 (accompli négatif má)", "élevé", "SOURCE_VERIFIEE",
  "Déjà au lexique ; documenté ici pour le tableau des négations.")
R("maxa", "ne … pas (passé) ; ne … pas (impératif/subjonctif : défense)", "marqueur_negation",
  "négation du passé et défense",
  "passé négatif : pronom + maxa + verbe ; défense : maxa + radical nu", "", "", "passé / impératif", "négatif",
  "máxà (Creissels)", PROJET + " ; " + KINGI,
  "Oku maxa faye. / Maxa daga !", "Nous n'avons pas regardé. / Ne pars pas !",
  S_LEX + " ; " + S_CRE18 + " ; " + S_SNK, "SNK-GRM-0024 ; Creissels 2018 (máxà : négation de l'impératif, du subjonctif et du passé) ; corpus validation_01 v-011/v-025/v-039, validation_02 v-019",
  "élevé", "SOURCE_VERIFIEE",
  "Triple emploi documenté : passé négatif, défense, et (homonyme) postposition de possession « chez » — voir section avoir.")
R("nta", "ne … pas (inaccompli, état, existence)", "marqueur_negation", "négation de l'inaccompli et des statifs",
  "", "", "", "présent / inaccompli", "négatif", "ntá (Creissels)", PROJET + " ; " + KINGI,
  "Baasi nt'a di.", "Il n'y a rien de mal.",
  S_LEX + " ; " + S_CRE18, "SNK-GRM-0032 ; SNK-LEX-0310 ; Creissels 2018 §3.3-3.4", "élevé", "SOURCE_VERIFIEE",
  "Déjà au lexique ; documenté ici pour le tableau des négations.")
R("n'ti / ti", "ne … pas (négation de la copule locative yi)", "marqueur_negation",
  "négation du présent locatif", "pronom + n'ti ; ti après nke/oku", "", "", "présent", "négatif",
  "", PROJET, "Ake n'ti ka ke. / Nke ti mula.", "Elle n'est pas à la maison. / Je ne veux pas.",
  S_SNK, "corpus texte_marche ; snk_engine docs/langue/etre-avoir.md", "élevé", "SOURCE_VERIFIEE",
  "Homographie avec ti « dire » (SNK-LEX-0877) : le contexte tranche.")
R("bara", "refuser (de faire) — négation modale", "verbe", "modalité négative « refuser de »",
  "fonctionne comme marque de la modalité « refuser de faire » (glose du référent)", "", "", "", "",
  "bante (variante relevée par le référent)", PROJET,
  "", "", S_LEX, "SNK-LEX-0093 (bara, fourni_par_referent) ; SNK-LEX-0129 (bante, fourni_par_referent)", "moyen", "SOURCE_VERIFIEE",
  "Négation d'ordre modal plutôt que grammatical : à documenter comme telle dans les tableaux.")
R("nàn máxà", "que … ne … pas (subjonctif négatif)", "marqueur_negation", "négation du subjonctif",
  "subjonctif négatif : nàn máxà + gérondif (Kingi)", "", "", "subjonctif", "négatif", "", KINGI,
  "", "", S_CRE18, U_CRE18 + " Tableau 4", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Combinaison décrite pour le Kingi ; équivalent du dialecte du projet à demander au référent.")

# ===========================================================================
# G4. TAM — PARTICULES VERBALES ET AUXILIAIRES
# ===========================================================================
R("do … ni ya me", "être en train de (progressif)", "marqueur_aspectuel", "progressif",
  "pronom + do + verbe-ye + ni ya me", "", "", "présent progressif", "positif",
  "", PROJET, "A do maro ke yigaye ni ya me.", "Il est en train de manger le riz.",
  S_LEX + " ; " + S_SNK, "SNK-GRM-0022/0023 ; corpus validation_02 v-162", "élevé", "SOURCE_VERIFIEE",
  "Déjà au lexique (do, ni ya me) ; phrase d'exemple nouvelle du corpus.")
R("wa + verbe-ene", "action en cours (inaccompli)", "marqueur_aspectuel", "inaccompli",
  "pronom + wa + gérondif", "", "", "présent (inaccompli)", "positif", "", PROJET,
  "Xa wa fayeni.", "Vous regardez.",
  S_LEX + " ; " + S_SNK, "SNK-GRM-0019 ; corpus validation_01 v-020", "élevé", "SOURCE_VERIFIEE",
  "Déjà au lexique. Attention : wa est aussi la copule locative du Kingi (Creissels) — emploi différent à ne pas confondre.")
R("yi + verbe-ni", "action en cours (inaccompli)", "marqueur_aspectuel", "inaccompli",
  "pronom + yi + gérondif", "", "", "présent (inaccompli)", "positif", "", PROJET,
  "Iku n'yi maro ke yigane koota su.", "Ils mangent le riz tous les jours.",
  S_LEX + " ; " + S_SNK, "SNK-GRM-0021 ; corpus validation_02 v-161", "élevé", "SOURCE_VERIFIEE",
  "Déjà au lexique ; yi est aussi la copule locative du dialecte du projet.")
R("fayi + verbe-ene", "en train de / habituel (analyse divergente)", "marqueur_aspectuel",
  "progressif ou habituel selon les sources",
  "pronom + fayi + gérondif", "", "", "présent", "positif", "hayi (Kingi, háyí)", PROJET + " ; " + KINGI,
  "Nke fayi dagana watia.", "Je suis en train de partir maintenant. (classé « habituel » dans validation_02 : « je pars (en ce moment) »)",
  S_LEX + " ; " + S_SNK + " ; " + S_CRE18, "SNK-GRM-0014 ; corpus serie_02 (nké fayi dagana watia, annoté Progressive) et validation_02 (annoté habituel) ; Creissels 2018 Tableau 4 (háyí gérondif progressif)",
  "moyen", "CONTRADICTOIRE_ENTRE_SOURCES",
  "Le corpus du projet annote fayi tantôt « progressif » (serie_02), tantôt « habituel » (validation_02) ; Creissels rapproche háyí du progressif. Divergence à trancher avec le référent.")
R("háyí", "marqueur de gérondif progressif (Kingi)", "marqueur_aspectuel", "gérondif progressif",
  "", "", "", "présent progressif", "positif", "fayi (dialecte du projet)", KINGI,
  "", "", S_CRE18, U_CRE18 + " Tableau 4", "moyen", "VARIANTE_DOCUMENTEE",
  "Correspondance probable avec fayi du projet : à confirmer.")
R("haxa", "accompli récent (« vient de »)", "marqueur_aspectuel", "accompli récent",
  "", "", "", "passé récent", "positif", "háxà (graphie tonale)", KINGI,
  "", "", S_CRE18, U_CRE18 + " Tableau 4", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Marqueur décrit pour le Kingi, absent du corpus du projet : existence dans le dialecte du référent à vérifier.")
R("na", "demande, souhait (« qu'il … ») ; subjonctif", "marqueur_predicatif", "subjonctif / volitif",
  "pronom + na + verbe", "", "", "subjonctif", "positif", "nàn ~ ǹ, nà (Creissels)", PROJET + " ; " + KINGI,
  "Nke na guiri. / O ni mula na xobo maro.", "Que je me lève (je me lève — volitif). / Nous voulons acheter du riz (mula na + verbe).",
  S_LEX + " ; " + S_CRE18 + " ; " + S_SNK, "SNK-GRM-0017 ; Creissels 2018 Tableau 4 (subjonctif nàn~ǹ / nà) ; corpus texte_journee journee-01, journee-03",
  "élevé", "SOURCE_VERIFIEE", "Déjà au lexique ; les exemples du corpus précisent l'emploi volitif et la construction après mula.")
R("di / da", "passé avec objet (accompli transitif)", "marqueur_predicatif", "accompli transitif",
  "sujet + di/da + objet + verbe ; la forme dépend des assimilations", "", "", "passé (accompli)", "positif",
  "dà (Creissels)", PROJET + " ; " + KINGUI,
  "A di nke wori. / A da a bisimilla.", "Elle m'a vu. / Il l'a accueilli.",
  S_LEX + " ; " + S_SNK + " ; " + S_CD19 + " ; " + S_CRE18, "SNK-GRM-0018/0020 ; corpus validation_02 (a di lettra ke n'safa) ; " + U_CD19 + " ; Creissels 2018 (accompli transitif dà)",
  "élevé", "SOURCE_VERIFIEE",
  "Déjà au lexique. Homographie : di est aussi la postposition locative « dans » du Kingi (Creissels).")
R("gérondif en -na / -ne / -ni / -nu / -no", "forme verbale dépendante (inaccompli, subordonnées)",
  "morphologie_verbale", "gérondif",
  "suffixe variable selon la classe du verbe : daga-na, sefe-ne, ri-ni, mini-ni, mooso-no ; sert après les marqueurs (wa, yi, fayi, na…) et dans les subordonnées",
  "", "", "", "", "", PROJET,
  "Anke n'yi rini daga.", "Tu vas partir. (yi rini + radical)",
  S_REF, "data/grammaire/soninke.yaml (champ gerondif de chaque verbe) ; Creissels 2018 (Tableau 4 : marqueurs de gérondif)",
  "élevé", "SOURCE_VERIFIEE", "Fait morphologique central pour générer les formes conjuguées.")
R("accompli Ø (zéro)", "passé sans marqueur (intransitif)", "morphologie_verbale", "accompli intransitif",
  "pronom + verbe nu : l'accompli intransitif positif n'a pas de marqueur segmental",
  "", "", "passé (accompli)", "positif", "", PROJET + " ; " + KINGUI,
  "N faye. / Ake n'xenxe.", "J'ai regardé. / Il a dormi.",
  S_CD19 + " ; " + S_CRE18 + " ; " + S_SNK, U_CD19 + " §2 (accompli positif = Ø) ; Creissels 2018 ; corpus validation_03 03-04",
  "élevé", "SOURCE_VERIFIEE", "Base du système : ne pas plaquer d'auxiliaire français.")
R("m' + verbe-ni", "variante d'accompli avec suffixe -ni (corpus)", "morphologie_verbale", "accompli",
  "le corpus validé montre m'V-ni à côté de l'accompli Ø", "", "", "passé", "", "", PROJET,
  "Ake m'fayi yigene watia.", "Il est en train de manger maintenant. (annotation serie_02)",
  S_SNK, "corpus serie_02 ; validation_02 (accompli PRON m'V-ni ou Ø)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "La répartition entre accompli Ø et m'V-ni n'est pas élucidée : à faire expliquer par le référent.")
R("we / ye (+ riini)", "futur (paradigme pédagogique mauritanien)", "marqueur_temporel", "futur",
  "pronom + we/ye + riini + verbe ; le cours écrit aussi IN WE YIGENE « je mange (futur) »",
  "", "", "futur", "positif", "wa (variante signalée par un lecteur du cours)", MAURI,
  "", "", S_SONK2, U_SONK2, "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Paradigme non recoupé par le corpus du projet (qui emploie rini / yi rini / n'ti rini). Divergence régionale probable.")

# ===========================================================================
# G5. POSTPOSITIONS
# ===========================================================================
R("yi / ya / ŋa", "à, dans, chez, sur (postposition multifonction)", "postposition",
  "locative / bénéficiaire / possessive",
  "placée après le nom ou le pronom ; s'assimile (ŋ'wori, n'ya safa) ; « chez » pour la possession",
  "", "", "", "", "ˋyí ~ ˋyá ~ ˋŋá (Creissels)", PROJET + " ; " + KINGI,
  "Waxi-ni filli yani maxa. / Kudu xa kini ŋa.", "J'ai deux frères. / Donne-moi aussi une cuillère.",
  S_CRE18 + " ; " + S_SNK + " ; " + S_LEX, U_CRE18 + " §3.4 (ˋyí ~ ˋyá ~ ˋŋá postposition multifonction) ; corpus texte_marche marche-18, texte_repas repas-11 ; SNK-LEX-0303 (…wa a yi)",
  "élevé", "SOURCE_VERIFIEE",
  "Trois réalisations d'une même postposition selon Creissels ; le corpus du projet montre yi et ŋa.")
R("di", "dans (postposition locative du Kingi)", "postposition", "locative",
  "", "", "", "", "", "", KINGI,
  "Haatu wa konpen di.", "Fatou est dans la chambre.",
  S_CRE18, U_CRE18 + " §3.4 ex. (11a)", "moyen", "VARIANTE_DOCUMENTEE",
  "Homographie avec le marqueur d'accompli transitif di/da du projet (SNK-GRM-0018) : à ne pas confondre ; le corpus du projet emploie noxo « dedans » pour l'intérieur.")
R("noxo", "dedans, dans ; ventre", "postposition", "locative (intérieur)",
  "nom noxo « ventre » grammaticalisé en postposition « dans »", "", "", "", "", "", PROJET,
  "Sere su n'ti ka ke noxo. / N'safandi cahier noxo.", "Il n'y a personne dans la maison. / J'écris dans mon cahier.",
  S_LEX + " ; " + S_SNK, "SNK-LEX-0757 (noxo ventre) ; corpus texte_journee journee-06, snk_engine docs/langue/nom.md (il y a … noxo)",
  "élevé", "SOURCE_VERIFIEE",
  "L'entrée existante ne glose que « ventre » : l'emploi postpositionnel « dans » est attesté par le corpus et doit être ajouté à l'entrée, sans doublon.")
R("kanma", "sur", "postposition", "locative (surface)",
  "", "", "", "", "", "", PROJET,
  "Baabon wa xatin kanma.", "Il y a de la mousse sur le lait.",
  S_LEX, "SNK-LEX-0184 (exemple fourni par le référent)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Déduit d'un exemple validé du lexique existant ; la glose isolée de kanma « sur » n'est pas encore validée.")
R("konpen", "chambre", "nom", "nom locatif (contexte des postpositions)",
  "", "", "", "", "", "kompo (graphie du corpus)", KINGI + " ; " + PROJET,
  "Haatu wa konpen di.", "Fatou est dans la chambre.",
  S_CRE18 + " ; " + S_SNK, U_CRE18 + " ex. (11) ; corpus texte_travail travail-15 (kompo siki ya ni a noxo « il y a trois chambres »)",
  "moyen", "A_CONFIRMER_PAR_LOCUTEUR", "Entrée lexicale utile aux exemples locatifs ; comparer au lexique existant.")

# ===========================================================================
# G6. CONJONCTIONS ET CONNECTEURS
# ===========================================================================
R("ado", "et (énumération, coordination)", "conjonction", "coordinative",
  "relie des noms ou des propositions ; équivalent de « et… et… » dans les listes", "", "", "", "", "",
  PROJET + " ; " + MAURI,
  "Nke na n'xawa maro ado teh n'ya xobono.", "Je dois acheter du riz et du thé.",
  S_SNK + " ; " + S_SONK3, "corpus texte_marche marche-04, texte_journee journee-01/journee-03/journee-04 ; titre SONK3 (… ADO KOYEN KOOTANI « et les jours de la semaine »)",
  "élevé", "SOURCE_VERIFIEE", "Absent du lexique de base : nouvelle entrée.")
R("do", "et (conjonction citée par le guide SIL)", "conjonction", "coordinative",
  "", "", "", "", "", "", SILVAR,
  "", "", S_SILG, U_SILG + " (conjonctions do, ma, walla, wo, baawo, saado, sababu)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Citée sans exemple par le guide SIL ; sens exact à confirmer (le corpus du projet emploie ado pour « et »). Ne pas publier de traduction assurée.")
R("ma", "et ? (conjonction citée par le guide SIL)", "conjonction", "coordinative",
  "", "", "", "", "", "", SILVAR,
  "Abdulaye da kasetin xobo, ma i wa katta sooninkanxanne terinkana.", "Abdoulaye a acheté une cassette et/pour pouvoir écouter le soninké. (traduction SIL, glose de ma non détaillée)",
  S_SILG + " ; " + S_SILD, U_SILG + " ; " + U_SILD, "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Homonyme du marqueur de négation ma (SNK-GRM-0033) : la valeur de conjonction reste à élucider ; traduction proposée avec réserve d'après l'exemple SIL.")
R("walla", "ou", "conjonction", "disjonctive",
  "", "", "", "", "", "", SILVAR,
  "Xirise ga foobe walla lemine nta ken tu.", "… (proverbe du livret de Dakar 2001 ; traduction à compléter depuis le livret)",
  S_SILG + " ; " + S_LIV01, U_SILG + " ; " + U_LIV01 + " §IV", "moyen", "SOURCE_VERIFIEE",
  "Deux sources écrites concordantes (guide SIL et livret de Dakar).")
R("bawoni", "parce que", "conjonction", "causale",
  "", "", "", "", "", "baawo (guide SIL ; SNK-LEX-0314)", PROJET,
  "Bawoni nke na n'xawa maro ado teh n'ya xobono. / Nke ni terene siri, bawoni nke ti mula na lele.",
  "Parce que je dois acheter du riz et du thé. / Je marchais vite, parce que je ne voulais pas arriver trop tard.",
  S_SNK + " ; " + S_SILG + " ; " + S_LEX, "corpus texte_marche marche-04, texte_village village-24, texte_repas repas-20 ; " + U_SILG + " (baawo) ; SNK-LEX-0314",
  "élevé", "SOURCE_VERIFIEE",
  "bawoni (corpus du projet) et baawo (guide SIL) : variante graphique ou forme distincte ? À trancher ; SNK-LEX-0314 contient un proverbe non glosé.")
R("sababu", "parce que, à cause de", "conjonction", "causale",
  "", "", "", "", "", "", SILVAR,
  "", "", S_SILG, U_SILG, "faible", "A_CONFIRMER_PAR_LOCUTEUR", "Cité sans exemple par le guide SIL.")
R("saado", "", "conjonction", "cité sans glose",
  "", "", "", "", "", "", SILVAR,
  "", "", S_SILG, U_SILG, "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Traduction volontairement vide : le guide SIL cite saado comme conjonction sans le gloser et aucune autre source consultée ne l'atteste.")
R("wo", "", "conjonction", "cité sans glose",
  "", "", "", "", "", "", SILVAR,
  "", "", S_SILG, U_SILG, "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Traduction volontairement vide : cité sans glose par le guide SIL.")
R("n'ga", "quand, lorsque (+ gérondif)", "conjonction", "subordonnée temporelle",
  "n' + ga après pronom ; introduit une subordonnée au gérondif", "", "", "", "", "ga (subordonnant simple)", PROJET,
  "Kati n'ga baka ka ke noxo. / Na yigue ado n'a dji mini kati n'ga baka ka ke noxo.",
  "… avant de sortir de la maison. / Ensuite je mange et je bois de l'eau avant de sortir de la maison.",
  S_SNK, "corpus texte_journee journee-01 ; snk_engine docs/langue/conjonctions.md (quand : n'ga)",
  "moyen", "SOURCE_VERIFIEE",
  "Les traductions du corpus rendent n'ga tantôt par « quand », tantôt par « avant de » : la valeur exacte (simultanéité vs antériorité) est à confirmer.")
R("n'gana", "si (condition)", "conjonction", "subordonnée conditionnelle",
  "", "", "", "", "", "", PROJET,
  "", "", S_SNK, "snk_engine docs/langue/conjonctions.md (condition : n'gana)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Mention documentaire sans phrase complète dans les extraits consultés.")
R("nanti", "que (discours rapporté)", "conjonction", "complétive du discours rapporté",
  "verbe de dire + pronom + da + nanti + proposition", "", "", "", "", "", PROJET,
  "N'ti a da nanti nke daga na ya. / N'ti a da nanti ake n'yi diomou, a kawu ya n'towoyi.",
  "Je lui ai répondu que je devais rentrer. / Je lui ai dit qu'elle allait bien, et que son oncle était malade.",
  S_SNK, "corpus texte_village village-21, village-27 ; snk_engine docs/langue/conjonctions.md (rapporté : nanti)",
  "moyen", "SOURCE_VERIFIEE", "Nouvelle entrée ; absente du lexique de base.")
R("xa", "mais", "conjonction", "adversative",
  "", "", "", "", "", "", "",
  "", "", S_SNKC3, U_SNKC3, "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Homographie avec xa « vous » (SNK-GRM-0011) et xa « où » (documentation du corpus) : à ne fusionner sous aucun prétexte ; chaque emploi reste documenté séparément.")
R("kempale", "ensuite, après cela", "adverbe", "connecteur chronologique",
  "", "", "", "", "", "kémpalé (graphie du corpus)", PROJET,
  "Kempale, n'soxu, n'xenxe.", "Ensuite, je me couche et je dors.",
  S_SNK, "corpus texte_journee journee-01/journee-04/journee-08, texte_marche", "moyen", "SOURCE_VERIFIEE",
  "Attesté quatre fois dans le corpus relu par le locuteur.")
R("ti … da", "dire à (quelqu'un)", "construction_verbale", "compléments du verbe de parole",
  "ti + destinataire + da … : le destinataire est encadré", "", "", "", "", "", PROJET,
  "N'ti a da nanti ake n'yi diomou.", "Je lui ai dit qu'elle allait bien.",
  S_SNK, "snk_engine docs/langue/conjonctions.md (dire à : ti…da) ; corpus texte_village village-21/26/27",
  "moyen", "SOURCE_VERIFIEE", "Construction à documenter dans l'étude être/avoir et les tableaux de conjugaison.")

# ===========================================================================
# G7. ADVERBES
# ===========================================================================
R("watia", "maintenant, en ce moment", "adverbe", "temps",
  "", "", "", "", "", "watia kundu (en ce moment précis)", PROJET,
  "Nke fayi dagana watia.", "Je suis en train de partir maintenant.",
  S_SNK + " ; " + S_LEX, "corpus serie_02, validation_02 (fréquent), texte_travail travail-04 ; snk_engine docs/langue/temps.md (watia = maintenant)",
  "élevé", "SOURCE_VERIFIEE", "")
R("lenki", "aujourd'hui", "adverbe", "temps",
  "", "", "", "", "", "", PROJET,
  "Xaku n'daga lenki.", "Vous êtes partis aujourd'hui.",
  S_LEX + " ; " + S_SNK, "SNK-LEX-0693 ; corpus validation_02 v-149", "élevé", "SOURCE_VERIFIEE", "")
R("kumbene", "demain", "adverbe", "temps",
  "", "", "", "", "", "xumbene / xoumbéné (corpus du projet) ; xunbane (glossaire Soninkara)", PROJET,
  "", "", S_LEX, "SNK-LEX-1116 (source_externe_a_verifier)", "moyen", "VARIANTE_DOCUMENTEE",
  "Trois graphies relevées pour « demain » : kumbene (lexique existant), xumbene/xoumbéné (corpus du locuteur), xunbane (glossaire Soninkara). Même entrée, variantes à relier après avis du référent.")
R("xumbene", "demain (graphie du corpus du projet)", "adverbe", "temps",
  "", "", "", "", "", "kumbene (SNK-LEX-1116) ; xunbane (glossaire Soninkara)", PROJET,
  "N'guida ti ke dagana soxu fene, bawoni a goli ni ya xumbene.", "Mon frère dit qu'il ira dormir tôt, parce qu'il travaille demain matin.",
  S_SNK, "corpus texte_repas repas-20 (xumbene), texte_journee journee-08 (xoumbéné)", "moyen", "VARIANTE_DOCUMENTEE",
  "Ne pas créer de doublon avec kumbene : rattacher comme variante.")
R("xunbane", "demain (graphie du glossaire Soninkara)", "adverbe", "temps",
  "", "", "", "", "", "kumbene ; xumbene", "",
  "", "", S_SNKG, "glossaire Soninkara (Xunbane : demain)", "faible", "VARIANTE_DOCUMENTEE", "Même lexème ; graphie externe.")
R("saasa", "maintenant", "adverbe", "temps",
  "", "", "", "", "", "watia (corpus du projet)", "",
  "N xaso saasa.", "Je suis vieux maintenant.",
  S_SILD, U_SILD + " (entrée xaso)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Synonyme probable de watia : à confirmer (variété ou registre).")
R("xoyi", "ainsi", "adverbe", "manière",
  "", "", "", "", "", "", "",
  "", "", S_SNKG, "glossaire Soninkara (Xoyi : ainsi)", "faible", "A_CONFIRMER_PAR_LOCUTEUR", "Source unique.")
R("fene", "tôt", "adverbe", "temps",
  "", "", "", "", "", "féné (graphie du corpus)", PROJET,
  "Nke faba giri fene.", "Mon père s'est levé tôt.",
  S_SNK, "corpus texte_pluies, texte_repas repas-20 (soxu fene)", "moyen", "SOURCE_VERIFIEE", "")
R("lele", "le soir ; tard", "adverbe", "temps",
  "", "", "", "", "", "lélé (graphie du corpus)", PROJET,
  "Lele, o yigue xadi en famille. / Nke ti mula na lele.", "Le soir, nous mangeons encore en famille. / Je ne voulais pas arriver trop tard.",
  S_SNK, "corpus texte_journee journee-08, texte_village village-24", "moyen", "SOURCE_VERIFIEE",
  "Deux valeurs relevées dans le même corpus (moment de la journée et retard) : à affiner.")
R("xadi", "encore, de nouveau", "adverbe", "quantité/répétition",
  "", "", "", "", "", "", PROJET,
  "Lele, o yigue xadi.", "Le soir, nous mangeons encore (une fois).",
  S_SNK, "corpus texte_journee journee-08", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Glose inférée d'un seul exemple dont la traduction française mêle un segment non soninké (« en famille ») : prudence.")
R("kudu", "aussi", "adverbe", "addition",
  "", "", "", "", "", "", PROJET,
  "Kudu xa kini ŋa, yampimaxa.", "Donne-moi aussi une cuillère, s'il te plaît.",
  S_SNK, "corpus texte_repas repas-11", "moyen", "SOURCE_VERIFIEE", "")
R("yampimaxa", "s'il te plaît", "expression", "formule de politesse",
  "", "", "", "", "", "", PROJET,
  "Kudu xa kini ŋa, yampimaxa.", "Donne-moi aussi une cuillère, s'il te plaît.",
  S_SNK, "corpus texte_repas repas-11, texte_marche marche-24 (a nia ti allah traduit « s'il te plaît »)",
  "moyen", "SOURCE_VERIFIEE", "Nouvelle entrée ; expression figée très utile pour un assistant linguistique.")
R("koota", "jour", "nom", "temps",
  "koota su « tous les jours »", "", "", "", "", "koyen kootani (les jours de la semaine, SONK3)", PROJET + " ; " + MAURI,
  "Iku n'yi maro ke yigane koota su.", "Ils mangent le riz tous les jours.",
  S_SNK + " ; " + S_SONK3, "corpus validation_02 v-161 ; " + U_SONK3 + " (KOYEN KOOTANI)", "moyen", "SOURCE_VERIFIEE", "")
R("suxuba", "matin", "nom", "temps",
  "suxuba su « chaque matin »", "", "", "", "", "", PROJET,
  "Suxuba su, kti kiye ke ga baka.", "Chaque matin, avant le lever du soleil.",
  S_SNK, "corpus texte_journee journee-01", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Segment « kti » non élucidé dans l'exemple ; glose de suxuba corroborée par la traduction française.")
R("siri", "vite, fort (intensité) — sens variable selon les contextes", "adverbe", "manière",
  "", "", "", "", "", "sire « bon » (SNK-LEX-0826)", PROJET,
  "Nke ni terene siri.", "Je marchais vite.",
  S_SNK + " ; " + S_LEX, "corpus texte_village village-24 ; SNK-LEX-0826 (sire bon)", "faible", "CONTRADICTOIRE_ENTRE_SOURCES",
  "Le corpus traduit siri par « vite » ; le lexique existant a sire « bon » ; d'autres relevés lui donnent des valeurs de durée/qualité. Entrée à élucider avec le référent avant tout usage pédagogique.")
R("terene", "marcher", "verbe", "verbe fréquent (lot 4)",
  "", "", "", "", "", "", PROJET,
  "Nke ni terene siri.", "Je marchais vite.",
  S_SNK, "corpus texte_village village-24", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Verbe inféré d'un seul exemple (ni terene = imparfait) ; à rapprocher de terinke « écouter » sans les confondre.")
R("ya / ŋa", "focalisateur (après ni dans la copule ni ya)", "particule", "focus",
  "", "", "", "", "", "ñà (Creissels, Kingi)", PROJET + " ; " + KINGI,
  "Towoyinte ni ya.", "Il est malade.",
  S_SNK + " ; " + S_CRE18, "corpus texte_marche (xore ni ya) ; Creissels 2018 (focalisateur ñà : Tàgé-n ñà ní « c'est l'enfant »)",
  "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Analyse proposée par rapprochement ; la valeur exacte de ya dans ni ya reste à confirmer.")
R("dinan-ti", "plus que (comparatif)", "particule", "comparaison",
  "", "", "", "", "", "", PROJET,
  "", "", S_SNK, "snk_engine docs/langue/nom.md (comparatif dinan-ti)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Mention documentaire sans phrase complète dans les extraits consultés.")

# ===========================================================================
# G8. NUMÉRAUX (complément du lexique existant)
# ===========================================================================
R("filli", "deux", "nombre", "numéral cardinal",
  "le numéral suit le nom (au pluriel) : waxi-ni filli « deux frères »", "", "", "", "", "", PROJET,
  "Waxi-ni filli yani maxa ado guida naxaru siki.", "J'ai deux frères et trois sœurs.",
  S_SNK, "corpus texte_marche marche-18", "moyen", "SOURCE_VERIFIEE",
  "« un » et « deux » manquaient au lexique de base (sikko trois → tanmu dix y figurent).")
R("siki", "trois", "nombre", "numéral cardinal",
  "", "", "", "", "", "sikko (SNK-LEX-0696)", PROJET,
  "Kompo siki ya ni a noxo.", "Il y a trois chambres.",
  S_SNK + " ; " + S_LEX, "corpus texte_marche marche-18, texte_travail travail-15 ; SNK-LEX-0696 (sikko trois)",
  "moyen", "VARIANTE_DOCUMENTEE", "siki (corpus) et sikko (lexique existant) : variante à relier, pas à dupliquer.")
R("nieru", "sept", "nombre", "numéral cardinal",
  "", "", "", "", "", "ñèrú (LGIDF)", "",
  "", "", S_LGQ, U_LGQ + " (ñèrú)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Complète la série sikko/naxato/karago/tumu/…/kabu/tanmu déjà au lexique (SNK-LEX-0696 à 0923) ; source unique.")
R("numéraux : naxato 4, karago 5, tumu 6, seegu 8, kabu 9, tamu/tanmu 10", "", "nombre",
  "rappel — déjà au lexique", "série attestée par SNK-LEX-0801/0802/0803/0805/0922/0807/0923 et par LGIDF (nàxàtó, kàràgó, tùnmú, ségú, kàbú, tánmú)",
  "", "", "", "", "", "", "", "", S_LEX + " ; " + S_LGQ, U_LGQ,
  "élevé", "SOURCE_VERIFIEE",
  "Ligne de synthèse pour l'inventaire : ces formes existent déjà ; tamu (SNK-LEX-0807) et tanmu (SNK-LEX-0923) sont des variantes du même numéral à relier.")

# ===========================================================================
# G9. PLURIEL, DÉTERMINATION ET DÉRIVATION
# ===========================================================================
R("pluriel : chute de la voyelle finale + -u", "pluriel des noms à voyelle finale -a/-e/-i/-o",
  "morphologie_nominale", "pluriel",
  "malla → mallu ; sugu → sugu (?) — le livret donne : malla « esclave » → mallu « esclaves »",
  "", "pl", "", "", "pluriels en -e → -u et -u/-a → -ni (documentation du corpus)", "",
  "Malla yi mallu.", "L'esclave → les esclaves. (schéma du livret)",
  S_LIV01 + " ; " + S_SNK, U_LIV01 + " §III ; snk_engine docs/langue/nom.md", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Deux descriptions partiellement différentes (livret de Dakar vs documentation du corpus) : à harmoniser avec le référent. Exemple waxi → waxi-ni (corpus) illustre le pluriel en -ni.")
R("pluriel des monosyllabes : géminée + -ni / -nu", "pluriel des noms monosyllabiques",
  "morphologie_nominale", "pluriel",
  "na « mère » → naani « mères » (livret de Dakar) ; ka → kanu (documentation du corpus)",
  "", "pl", "", "", "", "",
  "", "", S_LIV01 + " ; " + S_SNK, U_LIV01 + " §III (ka → kaani) ; snk_engine docs/langue/nom.md (ka → kanu)",
  "faible", "CONTRADICTOIRE_ENTRE_SOURCES",
  "Divergence explicite entre les deux sources sur le pluriel de ka (kaani vs kanu) : conserver les deux avec références ; à trancher par le référent.")
R("déterminant défini : nasale finale (-n)", "le, la (détermination)", "morphologie_nominale", "détermination",
  "le nom déterminé prend une nasale finale et un ton bas (LGIDF) ; -n attaché au nom (livret de Dakar) : ka-n « la maison »",
  "", "", "", "", "ke (déterminant du dialecte du projet, voir section démonstratifs)", KINGUI + " ; " + "",
  "Tàgé-n ñà ní.", "C'est l'enfant. (l'enfant, c'est lui)",
  S_CD19 + " ; " + S_LIV01 + " ; " + S_CRE18, U_CD19 + " §2 (forme déterminée = nasale finale + ton B) ; " + U_LIV01 + " §III ; Creissels 2018 ex. (30)",
  "moyen", "VARIANTE_DOCUMENTEE",
  "Deux systèmes de détermination selon les variétés (nasale finale au Kingi vs ke dans le corpus du projet) : divergence structurante à documenter, pas à unifier.")
R("suffixe causatif -ndi / -andi", "faire faire", "morphologie_verbale", "dérivation causative",
  "bagu « sortir » → bagandi « faire sortir » ; wunyi « ouvrir » → wunyindi", "", "", "", "", "", PROJET,
  "", "", S_LEX, "SNK-LEX-0324 (bagandi, candidat_dictionnaire_a_verifier) ; paires du lexique projet (wunyi/wunyindi, tuyi/tuyindi)",
  "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Régularité suggérée par les paires du lexique existant, mais les dérivés sont marqués « candidats à vérifier » : ne pas présenter la règle comme établie.")
R("nom d'action : -ye / -ŋe / -nde / -ne", "nom d'action du verbe", "morphologie_verbale", "dérivation nominale",
  "dagaye, ko-ŋe, kara-nde, sefeye — suffixe selon la classe du verbe", "", "", "", "", "", PROJET,
  "", "", S_REF, "data/grammaire/soninke.yaml (champ nom_action de chaque verbe)", "élevé", "SOURCE_VERIFIEE",
  "Ces dérivés figurent déjà largement au lexique (SNK-LEX-09xx à 13xx) : rappel morphologique, pas de doublons à créer.")
R("n' / m' / ŋ' / l'", "particules assimilées devant le verbe", "morphophonologie", "assimilation de la particule",
  "n' par défaut ; m' devant b/f/m ; ŋ' devant w ; l' devant r ; la particule suit les pronoms anke/ake/oku… et précède le verbe",
  "", "", "", "", "", PROJET,
  "Ake n'daga. / Ŋ'wori. / N'paba.", "Il est parti. / (Elle) m'a vu. / Mon père.",
  S_LEX + " ; " + S_REF, "SNK-GRM-0028 à 0031 ; data/grammaire/soninke.yaml", "élevé", "SOURCE_VERIFIEE",
  "Déjà au lexique ; ligne de synthèse pour les tableaux de conjugaison.")
R("pas de genre grammatical", "il / elle : même forme", "morphologie_nominale", "genre",
  "a = il ou elle ; i = ils ou elles ; aucune marque de genre sur les noms ni les adjectifs",
  "", "", "", "", "", KINGUI + " ; " + PROJET,
  "", "", S_CD19 + " ; " + S_SNK, U_CD19 + " §3 ; snk_engine docs/langue/pronoms.md (i : aucune distinction de genre)",
  "élevé", "SOURCE_VERIFIEE", "Fait typologique à afficher dans l'assistant pour éviter les calques français.")
R("ordre des mots : S O V", "sujet – objet – verbe", "syntaxe", "ordre constituant",
  "l'objet (nominal ou pronominal) précède le verbe ; le marqueur d'accompli transitif di/da s'insère après le sujet",
  "", "", "", "", "", PROJET + " ; " + KINGUI,
  "N faaba da si xobo. / A di lettra ke n'safa.", "… (exemple du livret de Dakar) / Elle a écrit la lettre (litt. elle [di] lettre la j'ai-écrit — segmentation à valider).",
  S_LIV01 + " ; " + S_CD19 + " ; " + S_SNK + " ; " + S_WK, U_LIV01 + " §IV ; " + U_CD19 + " ; corpus validation_02 ; " + U_WK,
  "élevé", "SOURCE_VERIFIEE",
  "Ordre SOV confirmé par quatre sources ; la segmentation exacte de l'exemple de validation_02 reste à valider (traduction du corpus : « elle a écrit la lettre »).")

# ===========================================================================
# G10. SALUTATIONS ET FORMULES (lot 4)
# ===========================================================================
R("an wujomu", "bonjour", "expression", "salutation — singulier, matin/journée",
  "contraction de an wuyi jomu ya ba ? « as-tu bien passé la nuit ? » ; pluriel : xa wujomu",
  "2", "sg", "", "", "xa wujomu (pluriel)", MAURI,
  "An wujomu !", "Bonjour !",
  S_SONK3, U_SONK3 + " (BAJJO : singulier ; SOROBA : pluriel)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Étymologie donnée par le cours ; le corpus du projet emploie aussi Anke dagana minna ? (« Bonjour. Où vas-tu ? ») comme ouverture — salutation à documenter séparément.")
R("kira jomu", "bon après-midi", "expression", "salutation — après-midi",
  "réponse : ma jom (ma jomu baane) ; pluriel : xa kira (xa kira jom)", "", "", "", "", "", MAURI,
  "", "", S_SONK3, U_SONK3, "moyen", "A_CONFIRMER_PAR_LOCUTEUR", "")
R("lella", "bonsoir (le soir)", "expression", "salutation — soir",
  "réponses : anbaa (hommes), yaawurii (femmes) ; pluriel : xa lella", "", "", "", "", "", MAURI,
  "", "", S_SONK3, U_SONK3, "moyen", "A_CONFIRMER_PAR_LOCUTEUR", "")
R("sunka", "bonsoir (la nuit)", "expression", "salutation — nuit",
  "réponses : anbaa (hommes), yaawurii (femmes) ; pluriel : xa sunka", "", "", "", "", "", MAURI,
  "", "", S_SONK3, U_SONK3, "moyen", "A_CONFIRMER_PAR_LOCUTEUR", "")
R("anbaa", "réponse aux salutations du soir (hommes)", "expression", "réponse de salutation",
  "", "", "", "", "", "anbaah", MAURI,
  "", "", S_SONK3, U_SONK3, "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Réponse genrée (anbaa pour les hommes, yaawurii pour les femmes) : fait sociolinguistique à documenter.")
R("yaawurii", "réponse aux salutations du soir (femmes)", "expression", "réponse de salutation",
  "", "", "", "", "", "", MAURI,
  "", "", S_SONK3, U_SONK3, "moyen", "A_CONFIRMER_PAR_LOCUTEUR", "")
R("an moxo ?", "comment vas-tu ?", "expression", "salutation — prise de nouvelles",
  "se dit à tout moment", "2", "sg", "", "", "an ne kan moxo ? ; an xibaare ?", MAURI,
  "", "", S_SONK3, U_SONK3 + " (KUUÑINDUN BEENI GA KOŊINI BIRE SU)", "moyen", "SOURCE_VERIFIEE",
  "moxo « comment » est corroboré par le corpus du projet (village-26).")
R("an xibaare ?", "comment vas-tu ? (tes nouvelles ?)", "expression", "salutation — prise de nouvelles",
  "", "2", "sg", "", "", "", MAURI,
  "", "", S_SONK3, U_SONK3, "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "xibaaru « nouvelles » (titre de la rubrique presse Soninkara Xibaaru kurunbo) : même racine.")
R("xori baasi me na ?", "rien ne s'est-il passé de mal ?", "expression", "salutation — prise de nouvelles",
  "", "", "", "", "", "xori toora nt'an ?a ? (n'as-tu rien de mal ?)", MAURI,
  "", "", S_SONK3, U_SONK3, "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Formule figée relevée telle quelle ; le segment me na reste à analyser (rapprocher de ni ya me du progressif ?). Ne pas décomposer sans validation.")
R("kaadunkon moxo ?", "comment va la famille ?", "expression", "salutation — prise de nouvelles",
  "", "", "", "", "", "", MAURI,
  "", "", S_SONK3, U_SONK3, "faible", "A_CONFIRMER_PAR_LOCUTEUR", "kaadunkon = la famille (segmentation à confirmer).")
R("kuuñi", "saluer", "verbe", "verbe — salutations",
  "dérivé : kuuñindu « les salutations »", "", "", "", "", "kuuni (graphies sans ñ)", MAURI,
  "", "", S_SNKV + " ; " + S_SONK3, U_SNKV + " (Kuuñi : saluer) ; " + U_SONK3 + " (titre KUUÑINDU : les salutations)",
  "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "Orthographe à normaliser selon la convention du projet (ñ Sénégal / ɲ Mali d'après le guide SIL).")
R("sibiti, alhaadi, tineeŋe, taraata, araaba, alxamisa, juma",
  "samedi, dimanche, lundi, mardi, mercredi, jeudi, vendredi", "nom", "jours de la semaine",
  "noms d'emprunt arabisés (cours) ; les noms « purs soninké » sont quasi oubliés selon le cours",
  "", "", "", "", "", MAURI,
  "", "", S_SONK3, U_SONK3 + " (KOYEN KOOTANI)", "moyen", "A_CONFIRMER_PAR_LOCUTEUR",
  "alxamisa correspond à alijuma « vendredi » du lexique existant ? Non : SNK-LEX-0686 alijuma = vendredi (conflit avec juma = vendredi du cours) : divergence à trancher, conserver les deux.")

# ===========================================================================
# G11. IMPÉRATIF
# ===========================================================================
R("radical nu (sans pronom ni marqueur)", "impératif singulier", "construction_verbale", "impératif",
  "le radical verbal seul vaut impératif ; l'objet précède le verbe", "2", "sg", "impératif", "",
  "Ø (Creissels : impératif intransitif sans marqueur)", PROJET + " ; " + KINGI,
  "Maro ke wori ! / Guiri !", "Vois le riz ! / Lève-toi !",
  S_SNK + " ; " + S_CRE18 + " ; " + S_REF, "corpus validation_02 v-125, texte_pluies (nké na guiri) ; Creissels 2018 Tableau 4 (impératif Ø) ; data/grammaire/soninke.yaml (imperatif)",
  "élevé", "SOURCE_VERIFIEE", "")
R("xa + radical", "impératif pluriel", "construction_verbale", "impératif pluriel",
  "xa (vous) + radical verbal", "2", "pl", "impératif", "", "", PROJET,
  "Xa daga ! / Xa goli !", "Partez ! / Travaillez !",
  S_REF + " ; " + S_SNK, "data/grammaire/soninke.yaml (imperatif_pluriel : xa + forme) ; corpus validation_01 v-012/v-040",
  "élevé", "SOURCE_VERIFIEE", "Déjà implicite dans SNK-GRM-0011 (xa vous) ; la construction impérative est documentée ici.")
R("maxa + radical", "ne … pas ! (défense, impératif négatif)", "construction_verbale", "impératif négatif",
  "maxa + radical verbal", "2", "", "impératif", "négatif", "máxà (Creissels)", PROJET + " ; " + KINGI,
  "Maxa daga ! / Maxa faye !", "Ne pars pas ! / Ne regarde pas !",
  S_LEX + " ; " + S_SNK + " ; " + S_CRE18, "SNK-GRM-0024 ; corpus validation_01 v-011/v-025/v-039 ; Creissels 2018 Tableau 4",
  "élevé", "SOURCE_VERIFIEE", "")
R("da (après l'objet, impératif transitif du Kingi)", "marqueur d'impératif avec objet", "particule",
  "impératif transitif", "lòxo ín ŋá « (donne-moi) la main à moi » ; dà peut suivre", "2", "", "impératif", "", "",
  KINGI, "", "", S_CRE18, U_CRE18 + " Tableau 4 (impératif Ø / dà)", "faible", "A_CONFIRMER_PAR_LOCUTEUR",
  "Décrit pour le Kingi ; le corpus du projet montre simplement objet + verbe (maro ke wori) : différence régionale possible.")
R("yeli / yere", "viens ici !", "expression", "impératif de venir",
  "", "2", "sg", "impératif", "", "", PROJET,
  "", "", S_LEX, "SNK-GRM-0027 (fourni_par_referent)", "élevé", "SOURCE_VERIFIEE",
  "Déjà au lexique ; rappel pour les tableaux d'impératif.")
