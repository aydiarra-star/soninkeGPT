# Fiche de validation linguistique — lot 4 Soninké–français

Cette fiche contient 55 segments source couvrant 50 lemmes candidats distincts.

## Colonnes à compléter
- `validation_referent` : `CONFIRMÉ`, `À CORRIGER`, `À REJETER` ou `À DISCUTER`.
- `lemme_corrige` : graphie validée si elle diffère de la proposition.
- `traduction_fr_confirmee` : traduction française confirmée, avec les sens distincts.
- `sens_variantes_exemples_a_conserver` : variantes, exemples, sens et formes sous-jacentes à conserver.
- `commentaires_referent`, `validateur`, `date_validation` : notes et provenance de la validation.

## Règles de traitement
1. Ne pas importer les candidats non validés.
2. Un seul enregistrement par lemme canonique dans la base; regrouper les sens multiples.
3. Conserver les variantes, exemples, texte source complet et références de paragraphes.
4. Ne pas considérer une traduction extraite automatiquement comme une validation indépendante.
5. Si deux homonymes doivent être distingués, le signaler avant import.

Branche : `data/lexique-soninke-fr-v1`
