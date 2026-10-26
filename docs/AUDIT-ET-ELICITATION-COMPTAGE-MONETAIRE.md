# Audit de cohérence et questionnaire d'élicitation — comptage monétaire soninké

## Objet et périmètre

Cette vérification porte sur les cinq fichiers candidats de la branche `research/soninke-numeration-money`. Elle est un contrôle structurel des fichiers, pas une certification linguistique, pas une validation des monnaies par des locuteurs, et pas un test du code de production.

## Résultats de contrôle structurel

- Les cinq fichiers candidats ont des en-têtes CSV et des colonnes attendues.
- Aucun identifiant de ligne dupliqué n'a été détecté dans les contrôles effectués.
- Une anomalie a été corrigée dans `monetary-counting-review.csv` : les lignes de très grands montants avaient une colonne manquante. Les 49 lignes ont maintenant le même nombre de colonnes que l'en-tête.
- Le fichier CFA conserve trois marqueurs historiques EUR sans forme soninkée (100, 500 et 1 000 EUR) pour rappeler de ne pas transposer le comptage CFA. Ils ne sont pas des expressions validées et le script les contrôle comme marqueurs vides.
- Les grands montants sont conservés en chiffres entiers complets (pas en notation scientifique).
- Les champs destinés au TTS sont laissés vides dans les listes de candidats. Les champs non vides du fichier CFA sont des enregistrements antérieurs et ne constituent pas une autorisation de créer de nouveaux audios.
- Les nouveaux grands montants sont explicitement marqués comme hypothèses ou comme éléments à éliciter. Les combinaisons cardinal + unité monétaire ne sont pas réputées attestées.

## Points de vigilance linguistique

1. **Ne pas confondre cardinal et expression monétaire.** Une forme générale pour 1 000 ou 1 million ne prouve pas qu'un locuteur dise naturellement « nombre + euro/dollar/ouguiya/dalasi/FCFA ».
2. **Les très grands nombres restent ouverts.** Au-delà des formes effectivement sourcées, demander au référent de les prononcer ou de dire qu'il n'a pas de forme usuelle. Ne pas fabriquer les formes pour remplir les cases.
3. **Le CFA est un système à part.** Conserver les variantes rapportées en `gode/godo/godi`, leurs contextes et leurs sources. Ne pas remplacer automatiquement le comptage en gode par le cardinal général.
4. **Les unités fractionnaires diffèrent.** Le khoums correspond à un cinquième d'ouguiya; le butut est une subdivision du dalasi. L'usage oral effectif de ces unités et leur formulation en soninké doivent être recueillis.
5. **Les montants mixtes doivent être élicités séparément.** Ne pas juxtaposer automatiquement deux expressions ni déduire l'ordre des unités.
6. **Variante régionale et registre.** Enregistrer la variété du locuteur, le contexte (marché, conversation, annonce de prix), la forme spontanée, les variantes, la répétition audio et l'accord du référent.

## Ajout du dollar américain

Le fichier de candidats `USD` reprend les jalons numériques et cardinaux de travail du fichier euro pour organiser l'élicitation, en remplaçant les unités par dollar/cent. Il ne s'agit pas d'une affirmation que les expressions sont naturelles en soninké. Les emprunts, l'ordre des mots, les formes comptées, les usages de diaspora et les montants mixtes doivent être recueillis indépendamment auprès de locuteurs. Le questionnaire comprend maintenant les scénarios du dollar copiés sur les scénarios euro pour comparaison; les réponses restent vides et à recueillir.

## Protocole d'entretien recommandé

Pour chaque montant du questionnaire :

1. Lire seulement le montant et le contexte en français; ne pas proposer une forme soninkée candidate.
2. Demander une formulation spontanée en soninké, puis faire répéter une seconde fois à vitesse normale.
3. Demander si cette formulation est réellement utilisée, dans quelle région/communauté et dans quel contexte.
4. Demander s'il existe une variante, un emprunt au français ou une convention particulière de comptage.
5. Enregistrer l'audio avec consentement, conserver l'identifiant de l'enregistrement et la provenance.
6. Faire valider séparément : (a) la traduction/le sens, (b) la forme écrite, (c) la prononciation, (d) le droit de réutiliser l'audio.
7. N'autoriser le TTS qu'après validation explicite du référent linguistique; une sortie TTS réussie ne vaut pas validation de prononciation.

## Contrôle reproductible

Un script de vérification structurelle est disponible dans `scripts/audit_monetary_candidates.py`. Depuis la racine du dépôt, lancer `python3 scripts/audit_monetary_candidates.py`. Il vérifie les largeurs CSV, les identifiants, les montants numériques, les codes monétaires et l'absence de texte audio prérempli dans les listes candidates. Ce contrôle ne valide pas la langue.

## Fichiers concernés

- `data/source/monetary-counting-review.csv` — CFA et grands montants.
- `data/source/euro-counting-candidates.csv` — euro et centime.
- `data/source/us-dollar-counting-candidates.csv` — dollar américain (`USD`) et cent.
- `data/source/mauritanian-ouguiya-counting-candidates.csv` — ouguiya et khoums.
- `data/source/gambian-dalasi-counting-candidates.csv` — dalasi et butut.
- `data/source/monetary-elicitation-questionnaire.csv` — grille vierge à remplir pendant l'entretien.

## Statut

`STRUCTURE_VERIFIEE / VALIDATION_LINGUISTIQUE_EN_ATTENTE`. Aucun changement de code de production, aucune fusion dans `main`, et aucune génération d'audio dans le cadre de cet audit.
