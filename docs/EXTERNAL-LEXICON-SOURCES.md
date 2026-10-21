# Sources lexicales externes à auditer

Date de première recherche : 21 octobre 2026. Ces ressources servent à repérer des mots, variantes, traductions et exemples. Elles ne sont pas réputées libres de copie en masse. Avant d'importer un corpus plus large, relever les conditions de réutilisation, la licence, l'attribution et le mode de téléchargement autorisé.

| Ressource | Usage prévu | État |
|---|---|---|
| [Asawan — lexique Soninké–Français–Anglais](https://www.asawan.org/fr/lexique_soninke) | Source prioritaire à examiner pour un lexique trilingue téléchargeable | Téléchargement annoncé; licence et redistribution à vérifier |
| [CNRS / LGIDF — Soninké](https://lgidf.cnrs.fr/node/25) | Grammaire, lexique, phonologie et description linguistique | Source académique; vérifier les droits de chaque ressource liée |
| [CNRS / LGIDF — Soninké : lexique des noms](https://lgidf.cnrs.fr/node/680) | Repérer des noms avec transcription tonale et traduction française | 9 candidats ajoutés avec forme source conservée; description basée sur le soninké du Kingui; droits à vérifier |
| [CNRS / LGIDF — Soninké : lexique des verbes](https://lgidf.cnrs.fr/node/682) | Comparer les verbes et les variantes transcrites | 3 candidats ajoutés avec marques tonales conservées; droits à vérifier |
| [Dicosoninke — Soninké vers Français](https://dicosoninke.wordpress.com/soninke-francais/) | Repérer des candidats et comparer les graphies | Candidats initiaux notés dans external-lexicon-candidates.csv; droits à vérifier |
| [Dicosoninké — interface bilingue](https://xn--dicosonink-k7a.com/f/) | Repérer des entrées, exemples et catégories grammaticales | Interface consultée; export massif et licence à vérifier |
| [Glosbe — Soninké vers Français](https://fr.glosbe.com/snk/fr) | Comparaison secondaire de sens et exemples en contexte | Contributions et sources hétérogènes; vérifier chaque entrée et les conditions d'usage |
| [Glosbe — Français vers Soninké](https://fr.glosbe.com/fr/snk) | Repérage dans le sens inverse | Contributions et sources hétérogènes; vérifier chaque entrée et les conditions d'usage |


- [Soninkara — Glossaire de mots Soninké–Français](https://www.soninkara.com/langue/apprendre-le-soninke/glossaire-de-mots.html) : glossaire attribué à Hadiya Wagué, à utiliser pour repérer des candidats, en conservant attribution et en vérifiant les conditions de réutilisation.

Le fichier `data/candidates/external-lexicon-candidates.csv` contient maintenant 28 candidats issus de Dicosoninke, Soninkara et LGIDF/CNRS. Ils sont tous maintenus en statut `a_verifier` et `rights_to_verify` : les formes avec marques tonales ne doivent pas être converties automatiquement en graphie du corpus interne. Le LGIDF précise que sa présentation linguistique se base sur le soninké du Kingui et qu’il n’existe pas une variété standard unique reconnue comme prestigieuse ; les formes doivent donc rester traçables par source et variété.

## Méthode d'enrichissement
1. Relever un candidat et l'URL exacte de sa source.
2. Comparer avec le lexique source transféré avant d'ajouter une nouvelle entrée.
3. Conserver les variantes et sens multiples; ne pas fusionner uniquement sur la similarité orthographique.
4. Marquer les candidats externes « à vérifier » tant qu'un référent soninké ne les a pas confirmés.
5. Enregistrer la licence et l'attribution avant toute redistribution. Ne pas aspirer ni republier une base tierce complète sans autorisation.
