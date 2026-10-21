# Ressources linguistiques soninké — inventaire et règles d'intégration

Mise à jour : 16 octobre 2026.

## Source prioritaire pour les phrases

**snk_engine — soninké : structure de la langue, moteur et corpus parallèle**
- Projet : https://github.com/oscarmedra/snk_engine
- Documentation : https://oscarmedra.github.io/snk_engine/
- Lexique en ligne : https://oscarmedra.github.io/snk_engine/langue/lexique/
- Traduction interactive : https://oscarmedra.github.io/snk_engine/comprendre/
- Corpus source : https://github.com/oscarmedra/snk_engine/tree/main/corpus/valide
- Licence des données et de la documentation : CC BY 4.0 (le code, séparément, est MIT).
- Attribution demandée : noah-medra (ORCID 0009-0003-6018-9802), « snk_engine — soninké : structure de la langue, moteur de conjugaison et corpus parallèle », 2026. https://github.com/oscarmedra/snk_engine — CC BY 4.0.
- Révision source consultée : `49f50a939ded51c5ffe7db404c45f40fc75a3c88` (branche `main`, consultée le 16 octobre 2026).

Le projet décrit les formes validées par son locuteur de référence et fournit des phrases soninké–français alignées. Il indique explicitement que cette variété ne représente pas nécessairement toutes les variétés du soninké. Les formes doivent donc être considérées comme des données sourcées, pas comme une norme universelle.

Un petit échantillon réutilisable, avec attribution, est placé dans [`data/soninke-samples.jsonl`](../data/soninke-samples.jsonl). Il est destiné à tester l'affichage, la recherche et le flux de validation humaine ; il ne constitue pas un corpus d'entraînement TTS suffisant.

## Sources complémentaires

### Asawan — lexique soninké
- https://www.asawan.org/fr/lexique_soninke
- Lexique trilingue utile pour rechercher des mots et comparer des équivalents.
- **Aucune copie de son contenu n'est intégrée ici** : les conditions de réutilisation des données doivent être vérifiées avant toute extraction ou redistribution.

### CNRS / Paris 8 — Langues et Grammaires du Monde
- https://lgidf.cnrs.fr/soninke
- Ressource de référence pour lexique, grammaire, phonologie et prononciation ; la description mentionne le soninké de Kingui (Mali).
- À utiliser pour comparer les analyses, sans fusionner automatiquement des variétés dialectales.

### Asawan — application dictionnaire
- https://play.google.com/store/apps/details?id=org.asawan.snk.ets
- Outil de consultation ; ce n'est pas un moteur de synthèse vocale et la présence d'une application ne donne pas, à elle seule, le droit de copier sa base de données.

## Règles pour ne pas fabriquer de phrases incorrectes

1. Garder la graphie originale de chaque source, y compris les diacritiques, espaces et apostrophes.
2. Conserver la phrase française, la référence source, la licence et la révision de données avec chaque exemple.
3. Ne pas corriger ou normaliser une forme en silence. Toute variante doit avoir une note et une validation humaine.
4. Distinguer « sourcé », « écouté », « prononciation validée par un locuteur » et « qualité TTS validée » : ces statuts ne sont pas interchangeables.
5. Ne pas inférer la traduction de `Daga yige`, `Li tao` ou `Daga goli` à partir de ressemblances lexicales. Ces trois phrases de test restent intactes dans l'interface et doivent être confirmées par le référent linguistique.
6. Avant d'ajouter un autre dictionnaire ou corpus, vérifier sa licence exacte, sa variété linguistique, son auteur et les conditions de redistribution.

## Citation complète

noah-medra (ORCID 0009-0003-6018-9802), « snk_engine — soninké : structure de la langue, moteur de conjugaison et corpus parallèle », 2026. https://github.com/oscarmedra/snk_engine — données et documentation sous CC BY 4.0.
