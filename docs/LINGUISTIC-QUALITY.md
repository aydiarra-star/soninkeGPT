# Contrôle linguistique de SoninkeGPT

La fiabilité linguistique prime sur la quantité de contenu. L'application ne
présente comme soninké que des formes attestées dans le corpus du projet.

## Règle d'affichage

Toute réponse pédagogique suit l'ordre :

```
SONINKÉ
   ↓
TRADUCTION FRANÇAISE
```

Jamais l'inverse. Chaque bloc affiche le statut de la forme :

| Statut | Signification |
| --- | --- |
| `Attesté · référent` | Enregistrement ou entrée fournie / validée par le référent |
| `Attesté · corpus` | Entrée du lexique, du livret d'expressions ou des phrases parallèles |
| `Voix de référence` | Enregistrement généré à partir de la voix de référence (OmniVoice) |
| `À vérifier · source externe` | Entrée issue d'une source externe non validée par le référent |
| `Non attesté dans le corpus` | Forme introuvable : elle n'est pas présentée comme une traduction |
| `Forme écartée · non soninké` | Forme d'une autre langue, jamais présentée comme du soninké |

## Contrôles appliqués avant affichage

1. La forme existe-t-elle dans le corpus (audio de référence, lexique,
   livret d'expressions, phrases parallèles) ?
2. Appartient-elle à la liste d'exclusion linguistique
   (`data/validation/non-soninke-forms.json`) ?
3. Une traduction française est-elle disponible ? Sinon, la réponse indique
   « Sens à préciser par le référent » au lieu d'inventer.
4. Une phrase complète est-elle attestée ? Sinon, seules les correspondances
   mot à mot sont montrées, explicitement signalées comme **assemblage
   indicatif**, jamais comme une traduction validée.

## Ce que l'application ne fait jamais

- Inventer un mot, une expression ou un proverbe soninké.
- Assembler des mots attestés pour produire une phrase présentée comme validée.
- Présenter du bambara, malinké, peul, wolof, dioula ou arabe comme du soninké.
- Remplacer un enregistrement manquant par une voix de synthèse du navigateur.
- Corriger automatiquement une phrase utilisateur : les formes inconnues sont
  signalées et soumises au référent.

## Liste d'exclusion

`data/validation/non-soninke-forms.json` contient les formes écartées, avec
leur motif et la forme soninké attestée à utiliser. Le fichier est chargé au
démarrage, mis en cache localement et appliqué aux réponses, au lexique, aux
audios et aux favoris. Toute modification de cette liste doit être relue par un
locuteur référent.

## Signaler une erreur

Les corrections sont priorisées ainsi : forme attestée par le référent >
entrée de dictionnaire validée > source externe à vérifier. Une forme ambiguë
est affichée avec sa réserve, jamais lissée.
