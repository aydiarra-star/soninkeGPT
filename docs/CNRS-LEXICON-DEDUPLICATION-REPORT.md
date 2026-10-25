# Rapprochement CNRS/LGIDF avec le lexique SoninkéGPT

Date : 2026-10-21

## Périmètre

Lexique de production lu depuis `main/data/source/lexique-soninke-fr-base.csv` : 325 entrées. Candidats transcrits depuis les extraits accessibles des listes LGIDF/CNRS : 212 lignes avant regroupement, 212 formes source distinctes après regroupement NFC + minuscules.

Sources : noms https://lgidf.cnrs.fr/node/680 ; verbes https://lgidf.cnrs.fr/node/682 ; adjectifs https://lgidf.cnrs.fr/node/681 ; quantitatifs et numéraux https://lgidf.cnrs.fr/node/679 ; pronoms https://lgidf.cnrs.fr/node/676 ; déictiques https://lgidf.cnrs.fr/node/677 ; informations sur la variété https://lgidf.cnrs.fr/node/25.

## Résultat de comparaison

- Correspondances exactes de forme après NFC + minuscules : 0 formes (exclues des nouveaux ajouts).
- Rapprochements après retrait des seuls accents de ton (grave, aigu, circonflexe) : 23 formes à vérifier manuellement. Ce rapprochement n'est pas une preuve d'identité; il conserve distincts ñ et ŋ.
- Formes sans correspondance exacte ou rapprochement sans tons : 189 candidates.
- Fichier candidat total : 212 lignes, avec statut et liens de comparaison.

## Limites importantes

Cette passe s'appuie sur le contenu textuel disponible des pages LGIDF/CNRS, pas sur un export complet garanti des pages. Elle est donc un lot de travail, pas un inventaire exhaustif de leurs lexiques. Certaines entrées ont plusieurs traductions ou plusieurs formes source; celles-ci sont conservées ou notées, et non normalisées de force. Le site précise que sa description s'appuie sur le soninké du Kingui (Mali) et qu'il n'existe pas de variété standard unique.

Le lexique de production `main` n'a pas été modifié. Les candidats restent non validés. Les entrées déjà validées par le référent, notamment SNK-LEX-0275 à SNK-LEX-0294, ne sont pas touchées.

## Audio

Étape suivante : trier les candidates réellement nouvelles, valider la forme et la traduction, puis générer les clips avec la voix de référence. Les colonnes de ce CSV aident à prioriser les doublons et les formes à écouter. Les pages de lexique CNRS donnent des champs de prononciation, mais le contenu récupéré ici ne permet pas d'affirmer qu'un audio par mot a été téléchargé ou contrôlé.
