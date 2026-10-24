# Sources lexicales externes à auditer

Date de première recherche : 21 octobre 2026. Ces ressources servent à repérer des mots, variantes, traductions et exemples. Elles ne sont pas réputées libres de copie en masse. Avant d'importer un corpus plus large, relever les conditions de réutilisation, la licence, l'attribution et le mode de téléchargement autorisé.

| Ressource | Usage prévu | État |
|---|---|---|
| [Asawan — lexique Soninké–Français–Anglais](https://www.asawan.org/fr/lexique_soninke) | Source prioritaire à examiner pour un lexique trilingue téléchargeable | Téléchargement annoncé (17,25 Mo, exécutable Windows `.exe`); format exploitable, licence et redistribution à vérifier avant toute extraction ou réutilisation |
| [CNRS / LGIDF — Soninké](https://lgidf.cnrs.fr/node/25) | Grammaire, lexique, phonologie et description linguistique | Source académique; vérifier les droits de chaque ressource liée |
| [CNRS / LGIDF — Soninké : lexique des noms](https://lgidf.cnrs.fr/node/680) | Repérer des noms avec transcription tonale et traduction française | 9 candidats ajoutés avec forme source conservée; description basée sur le soninké du Kingui; droits à vérifier |
| [CNRS / LGIDF — Soninké : lexique des verbes](https://lgidf.cnrs.fr/node/682) | Comparer les verbes et les variantes transcrites | 3 candidats ajoutés avec marques tonales conservées; droits à vérifier |
| [Dicosoninke — Soninké vers Français](https://dicosoninke.wordpress.com/soninke-francais/) | Repérer des candidats et comparer les graphies | Candidats initiaux notés dans external-lexicon-candidates.csv; droits à vérifier |
| [Dicosoninké — interface bilingue](https://xn--dicosonink-k7a.com/f/) | Repérer des entrées, exemples et catégories grammaticales | Interface consultée; export massif et licence à vérifier |
| [Glosbe — Soninké vers Français](https://fr.glosbe.com/snk/fr) | Comparaison secondaire de sens et exemples en contexte | Contributions et sources hétérogènes; vérifier chaque entrée et les conditions d'usage |
| [Glosbe — Français vers Soninké](https://fr.glosbe.com/fr/snk) | Repérage dans le sens inverse | Contributions et sources hétérogènes; vérifier chaque entrée et les conditions d'usage |


- [Soninkara — Glossaire de mots Soninké–Français](https://www.soninkara.com/langue/apprendre-le-soninke/glossaire-de-mots.html) : glossaire attribué à Hadiya Wagué, à utiliser pour repérer des candidats, en conservant attribution et en vérifiant les conditions de réutilisation.

Le fichier `data/candidates/external-lexicon-candidates.csv` contient maintenant 9 candidats uniques issus de Soninkara qui ne figurent pas encore dans le lexique principal (les 19 entrées déjà présentes dans `data/source/lexique-soninke-fr-base.csv` ont été fusionnées avec conservation des formes tonales dans la colonne `variantes`, afin d'éliminer tout doublon). Ils sont tous maintenus en statut `a_verifier` et `rights_to_verify` : les formes avec marques tonales ne doivent pas être converties automatiquement en graphie du corpus interne. Le LGIDF précise que sa présentation linguistique se base sur le soninké du Kingui et qu’il n’existe pas une variété standard unique reconnue comme prestigieuse ; les formes doivent donc rester traçables par source et variété.

## Sources repérées le 24 octobre 2026 — vocabulaire du corps humain

Recherche menée pour vérifier le sens exact des 54 formes du document Google
« parties du corps ». Résultat détaillé : `data/source/reports/recherche-sens-parties-corps-2026-10-24.md`
et `data/source/reports/verification-sens-parties-corps-2026-10-24.csv`.

| Ressource | Apport | État |
|---|---|---|
| [SIL Mali / Asawan — Marianne Hagg, « Parlons le soninké et le français », chap. 6 « Fate – Le corps »](https://www.asawan.org/sites/www.asawan.org/files/uploads/O%20nan%20sefe%20sooninken%20do%20faransen%20%C5%8Ba%202e%20%C3%A9d%20-%20Web%20lecture.pdf) | Vocabulaire anatomique bilingue, seul chapitre entièrement consacré au corps | Source la plus complète pour cette thématique; orthographe soninké du Mali; droits à vérifier |
| [Les Langues d'Afrique Activities — « Décrire les parties du corps en Soninké » (A1)](https://leslanguesdafriqueactivities.com/lessons/4-savoir-decrire-lhomme-et-sa-societe-en-soninke-2/decrire-les-parties-du-corps-en-soninke/) | Liste corps avec singuliers et pluriels | Cours en ligne; vérifier chaque entrée et les conditions d'usage |
| [CNRS / LGIDF — « Soninké : lexique (noms) » (Creissels & Diawara)](https://lgidf.cnrs.fr/node/680) | Lexique nominal avec transcription tonale; décrit le soninké du Kingui | **Page en migration** : `lgidf.cnrs.fr` renvoie vers `lgmef.huma-num.fr`, où l'ancienne adresse répond 404. Contenu consulté via les résultats de recherche qui l'indexent; à re-vérifier sur la nouvelle adresse avant citation formelle |
| [Lexique Soninké (Mali)–Français–Anglais — ODA / Asawan](https://media.ipsapps.org/snk/oda/lexicon/) | Dictionnaire de référence, consulté lettre par lettre; catégorie « 2.1. Body » | Le plus fiable pour trancher un sens; extraction massive et redistribution à vérifier |
| [« Des mots et des langues » — fiche SONINKE, section « Le corps humain »](https://desmotsetdeslangues.eklablog.com/soninke-a113996526) | Vocabulaire français → soninké, seul à couvrir cheville, mollet, rein, talon | Blog de vulgarisation; à recouper systématiquement |
| [Portail Soninkara — Demba Soumaré, « Les différentes parties du corps humain »](http://www.soninkara.org/langue-soninke/vocabulaire-soninke-les-differentes-parties-du-corps-humain-4281.html) | Texte soninké glosé; distingue tête, tronc, membres | Article signé par un enseignant; textes non segmentés mot à mot |
| [Tableau anatomique multilingue, colonne soninké « Haten súuhunu »](https://megambia.com/wp-content/uploads/2025/01/040125-bodyparts.pdf) | Équivalents anglais/soninké pour cheville, orteil, coude, mollet | Ressource pédagogique gambienne; graphie « Sarahule »; à recouper |
| [Denis Creissels — lexèmes simples du soninké du Kingi](https://journals.openedition.org/mandenkan/738) | Liste de lexèmes avec gloses et schèmes tonaux | Source académique; sert à confirmer des sens dérivés (« foie, courage, colère ») |

### Références complémentaires, non consultables en ligne

Quatre ouvrages pourraient départager les formes restées non résolues (composés du type
`Kit-qasse`, `Tange-soro`, `Kuntu-bunyi`). Aucun n'est exploitable en ligne à ce jour :

| Référence | Pourquoi elle compte | Accès |
|---|---|---|
| Ousmane Moussa Diagana, *Dictionnaire soninké-français (Mauritanie)*, Karthala, 2013, 5 800 entrées | Décrit le parler de Kaédi, dont l'alphabet comporte le phonème **q** — la même orthographe que le document (`Qanfe`, `Qunyu`, `Kit-qasse`). Piste la plus prometteuse | Ouvrage payant (PDF 19,99 €). Seuls les liminaires sont en accès libre |
| Gordon & Sara Williams, *Des aspects de la lexicologie du Soninke : la dérivation, les mots composés, le changement de transitivité*, Dakar, SIL, 1998, 92 p. | Traite explicitement de la composition ; le document écrit ses composés avec un trait d'union pédagogique | PDF sur [sil.org/resources/archives/49407](https://www.sil.org/resources/archives/49407) ; la section utile (p. 43-88) dépasse la limite d'extraction automatique et demande une lecture manuelle |
| Galtier, Dantioko & Dramé, *Lexique Soninké-Français*, Bamako, DNAFLA, 1979, 100 p. | Lexique malien de référence | Exemplaire physique uniquement (signalé par COCOON et l'UNESCO) |
| Abdoulaye Bathily, *Lexique soninke (sarakole)-français*, Dakar, CLAD, 1975 | Lexique sénégalais ancien | Non numérisé |

Règle appliquée pendant cette recherche : aucune traduction extrapolée. Une forme non
retrouvée est déclarée `non_atteste`, une divergence est déclarée `corrige` avec ses
sources, et une divergence entre variétés dialectales est signalée comme `conflit`
sans être tranchée automatiquement.

## Méthode d'enrichissement
1. Relever un candidat et l'URL exacte de sa source.
2. Comparer avec le lexique source transféré avant d'ajouter une nouvelle entrée.
3. Conserver les variantes et sens multiples; ne pas fusionner uniquement sur la similarité orthographique.
4. Marquer les candidats externes « à vérifier » tant qu'un référent soninké ne les a pas confirmés.
5. Enregistrer la licence et l'attribution avant toute redistribution. Ne pas aspirer ni republier une base tierce complète sans autorisation.
