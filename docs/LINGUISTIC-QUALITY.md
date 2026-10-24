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
4. Une phrase complète est-elle attestée ? Si oui, elle est prioritaire. Sinon,
   l'application compose une proposition à partir des mots disponibles, avec le
   statut **assemblage indicatif — phrase non attestée**, les éléments français
   sans correspondance signalés, et sans inventer de mot. L'audio est joué par
   segments uniquement lorsqu'un enregistrement correspondant existe.

## Ce que l'application ne fait jamais

- Inventer un mot, une expression ou un proverbe soninké.
- Présenter une phrase assemblée comme attestée ou validée. La composition indicative est autorisée si elle est clairement étiquetée.
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

## Pas de doublon dans le lexique

Un mot déjà présent dans le lexique — comme entrée principale **ou** comme
`variante` — n'est jamais réimporté, même si la nouvelle source donne une glose
différente. La comparaison ignore la casse, les accents vocaliques, les traits
d'union et les numéros d'homonyme (`baabo1` = `baabo`), mais elle distingue les
lettres propres au soninké (`ñ`, `ŋ`, `ɲ`, `ɓ`, `ɗ`, `ƴ`, `ɛ`, `ɔ`) et
l'apostrophe : *segeñe* « ongle » ≠ *segene* « monter », *n* ≠ *n'*.

Trois outils appliquent cette règle :

| Script | Rôle |
| --- | --- |
| `scripts/check_doublons_lexique.py` | Contrôle : doublons d'entrée et formes citées en variante. `--strict` renvoie un code d'erreur si un doublon existe. |
| `scripts/import_extraction_sans_doublons.py` | Import d'un CSV d'extraction : n'ajoute que les formes absentes, journalise les doublons écartés et les gloses divergentes. |
| `scripts/fusionner_doublons_lexique.py` | Fusionne les doublons déjà présents, sans perte : la forme absorbée devient `variante`, la glose la plus complète est conservée, une note de fusion est ajoutée. |
| `scripts/enrichir_definitions_sans_doublons.py` | Écrit les définitions dans la colonne `definition` des entrées **existantes** ; refuse toute forme qui ne serait pas déjà une entrée ou qui ne serait qu'une variante, puis vérifie que la liste des lignes et des formes n'a pas bougé. |

Règles de fusion :

- une entrée « renvoi à X » ou « variante de X » est absorbée par X ;
- à glose identique, l'entrée conservée est celle qui porte l'audio, sinon celle
  dont le statut de preuve est le plus fort ;
- deux formes distinctes ayant chacune son audio (*Giya* / *yesso*, *kambe* /
  *kanbe*…) ne sont jamais fusionnées : ce sont des variantes attestées, pas des
  doublons ;
- toute fusion est enregistrée dans `data/reports/fusions-doublons-<date>.csv`.

## Définitions et gloses à vérifier

Chaque entrée peut porter une définition française dans la colonne `definition`,
avec son statut dans `definition_statut` :

| Statut | Signification |
| --- | --- |
| `redigee_a_valider` | Définition rédigée d'après la glose attestée du lexique, en attente de validation. |
| `forme_derivee_du_verbe` | Nom d'action ou gérondif : définition déduite du verbe de base. |
| `a_clarifier` | La glose de départ est incertaine ou contradictoire : la définition est proposée, mais le mot reste affiché avec la mention « glose à vérifier ». |

Une définition ne remplace jamais la traduction : elle l'explique. Elle ne peut
pas non plus introduire un sens absent de la glose de départ. Les cas douteux
sont portés à la [fiche de questions du référent](QUESTIONS-REFERENT.md) au lieu
d'être tranchés arbitrairement.

## Signaler une erreur

Les corrections sont priorisées ainsi : forme attestée par le référent >
entrée de dictionnaire validée > source externe à vérifier. Une forme ambiguë
est affichée avec sa réserve, jamais lissée.
