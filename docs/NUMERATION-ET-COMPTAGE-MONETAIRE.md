# Chantier de recherche — numération soninké et comptage de l'argent

## Objectif

Séparer strictement deux domaines qui ne doivent pas partager automatiquement leurs règles :

1. **Numération générale** : compter, lire et écrire les nombres, faire des calculs et exprimer des quantités non monétaires.
2. **Comptage monétaire** : exprimer des prix, sommes, paiements et montants dans une monnaie déterminée.

Ce chantier est une base de recherche et de validation. Il ne constitue pas une validation linguistique et ne modifie pas les règles de production de SoninkeGPT.

## Règles de travail non négociables

- Ne jamais déduire une expression monétaire en appliquant mécaniquement les règles des nombres ordinaires.
- Ne jamais déduire qu'un mot isolé signifie une somme d'argent sans contexte et preuve d'usage.
- Ne pas supposer que les conventions FCFA se transposent à l'euro.
- Conserver les variantes orthographiques et les variantes régionales sans les fusionner automatiquement.
- Distinguer l'attestation écrite, la corroboration indépendante, la validation orale par un locuteur, la validation audio et l'intégration technique.
- Ne pas générer ni marquer un audio comme validé tant que la forme lexicale et sa prononciation ne sont pas confirmées.
- Pour toute entrée, enregistrer la forme exacte, la segmentation proposée, le sens, la monnaie, la valeur numérique, le contexte, la provenance et le statut de validation.
- En cas de contradiction entre sources, conserver les deux analyses et ouvrir une question au référent au lieu de choisir arbitrairement.

## Schéma des données

### Référentiel A — numération générale

Champs recommandés : `id`, `valeur`, `forme_soninke`, `variante`, `segmentation`, `gloss_fr`, `type` (unité/dizaine/centaine/composé/grand nombre), `règle_de_formation`, `région`, `provenance`, `statut_attestation`, `statut_validation_orale`, `statut_audio`, `notes`.

### Référentiel B — expressions monétaires

Champs recommandés : `id`, `montant_numérique`, `monnaie`, `expression_soninke`, `segmentation`, `unité_monétaire_traditionnelle`, `sens_littéral`, `équivalent_calculé`, `contexte`, `région`, `source`, `statut_attestation`, `statut_validation_orale`, `statut_audio`, `notes`.

Les deux référentiels auront des identifiants et des règles séparés. Une entrée peut être reliée à l'autre pour comparaison, mais cette relation ne vaut pas équivalence.

## Premières pistes — à vérifier, non validées

- Les formes cardinales rapportées incluent notamment `tanpille` pour 20, `kame` pour 100, `kamo filli` pour 200 et `wujune` pour 1 000.
- Des ressources pédagogiques sur l'argent rapportent une unité `gode/godi` associée à cinq francs CFA dans certains exemples.
- Les expressions rapportées pour certains montants doivent être confrontées à la forme exacte, à la segmentation et au contexte d'usage. En particulier, ne pas conclure que `kame` isolé signifie 500 : les données préliminaires distinguent `kame` (100 dans le système cardinal) et une expression du type `keme gode` (rapportée pour 500 FCFA).
- L'usage en euros, les variantes régionales, la valeur de `gode/godi` et la formation des montants non documentés restent à établir.

## Protocole de validation

1. Rassembler les formes exactes des dictionnaires et ressources pédagogiques soninké.
2. Comparer les formes, sans fusion automatique des variantes ni extrapolation à des nombres absents.
3. Préparer des questions d'élicitation neutres : « Comment diriez-vous exactement X FCFA ? », « Et le même nombre dans un calcul, sans parler d'argent ? », « Cette forme est-elle naturelle dans votre variété ? »
4. Interroger séparément plusieurs locuteurs, en notant variété/région et contexte. Ne pas suggérer la réponse avant la première production.
5. Enregistrer les audios uniquement après validation de la forme; faire confirmer l'audio par le référent linguistique.
6. Faire une revue indépendante du CSV, des contradictions et des statuts avant toute fusion dans le lexique de production.
7. N'intégrer à `main` qu'après revue du référent et tests démontrant que les deux systèmes sont traités séparément.

## Fichier de suivi

Le fichier `data/source/monetary-counting-review.csv` contient les premières pistes de comptage monétaire. Toutes les lignes commencent au statut « candidat à vérifier »; elles ne sont pas des traductions validées.

## Résultats complémentaires de recherche (pistes, toujours non validées)

Les ressources consultées renforcent l'hypothèse d'une unité monétaire traditionnelle `gode` correspondant à 5 FCFA dans les usages décrits. Elles rapportent notamment les correspondances suivantes, qui doivent rester des candidats tant que le référent ne les a pas vérifiées :

- `godo baane` : 5 FCFA ;
- `godo hilli/filli` : 10 FCFA ;
- `godo sikki` : 15 FCFA ;
- `godo naxati` : 20 FCFA ;
- `godo karagi` : 25 FCFA ;
- `godo tanmi` : 50 FCFA ;
- `tanfille gode` : 100 FCFA ;
- `kame/keme gode` : 500 FCFA ;
- `kamo filli gode` : 1 000 FCFA ;
- `wujune gode` : 5 000 FCFA, selon la ressource consultée.

Le calcul par cinq est cohérent avec cette série : la valeur monétaire exprimée en unités de `gode` peut être cinq fois le cardinal correspondant. Cela ne permet pas d'étendre automatiquement la règle à toute forme ou à toute monnaie, et ne signifie pas que le mot cardinal seul change de sens.

Des formes telles que `komohillin dere`, `komonaxatin dere` et `wujinin dere` sont également rapportées pour des montants ou des billets; elles sont consignées comme formes à examiner, sans les ramener prématurément à une règle générale.

Une publication comparative sur les systèmes numériques mandé décrit le comptage de l'argent par multiplication par cinq dans plusieurs langues de la famille. Cette observation comparative peut orienter les questions, mais elle ne remplace jamais une attestation spécifique au soninké. Les formes d'autres langues mandé ne doivent pas être importées dans le lexique soninké.

## Questions prioritaires au référent linguistique

1. Est-ce que `gode` désigne historiquement ou actuellement une pièce/unité de 5 FCFA dans votre variété ?
2. Pour 10, 15, 20 et 25 FCFA, quelles sont les formes exactes, prononcées naturellement, et quelles variantes existent ?
3. Pour 100 FCFA, dit-on `tanfille gode`, `tanpille gode`, les deux, ou autre chose ?
4. Pour 500 FCFA, quelle est la forme exacte : `kame gode`, `keme gode`, ou une autre variante ? `kame` seul peut-il désigner 100 dans un contexte et 500 dans un contexte monétaire, ou faut-il obligatoirement une expression complète ?
5. Pour 1 000, 2 000, 5 000 et les sommes élevées, quelles expressions sont naturelles, et lesquelles s'emploient seulement pour des billets ?
6. Les expressions monétaires en euros suivent-elles les expressions traditionnelles en `gode`, les nombres cardinaux ordinaires, ou une stratégie mixte ?
7. Les réponses changent-elles selon la région, la génération, le commerce ou la variété de soninké ?

Aucune réponse à ces questions ne doit être préremplie comme si elle avait été donnée par un locuteur.

## Traduction française des candidats — sens des mots et sens monétaire

Le tableau CSV a été enrichi avec deux champs distincts : `sens_des_éléments_fr` et `sens_de_l_expression_fr`. Cette séparation est obligatoire.

Les ressources comparées décrivent un système où `gode` est une unité monétaire de 5 FCFA. Ainsi, `gode baane` est rapporté comme une unité, soit 5 FCFA; `godo filli/hilli` comme deux unités, soit 10 FCFA; `godo sikki` comme trois unités, soit 15 FCFA; `godo naxati` comme quatre unités, soit 20 FCFA; `godo karagi` comme cinq unités, soit 25 FCFA; `godo tanmi` comme dix unités, soit 50 FCFA. `tanpille gode` est rapporté pour 100 FCFA, et `kame/keme gode` pour 500 FCFA. L'analyse par unités de cinq est cohérente avec ces exemples, mais les formes exactes et leurs usages restent à confirmer auprès de locuteurs.

Pour `tannaxate` (200 FCFA) et `tandume` (300 FCFA), les formes sont rapportées dans la leçon monétaire, mais leur analyse comme 40 et 60 unités de `gode` est une hypothèse arithmétique, pas encore une traduction littérale confirmée.

Pour `komohillin dere`, `komonaxatin dere`, `wujinin dere` et les expressions de montants élevés, le sens des éléments et la segmentation restent non établis. Le tableau ne doit pas inventer une traduction mot à mot. La traduction de l'expression entière rapporte uniquement le montant documenté dans le contexte.

La numération générale donne séparément les sens cardinaux tels que `tanmu` = dix, `tanpille/tanfille` = vingt, `tannaxate` = quarante, `tandume` = soixante, `kame` = cent et `wujune` = mille. Ces gloses cardinales aident à examiner les candidats monétaires, mais ne prouvent pas à elles seules leur sens dans l'expression d'argent.

**État actuel :** montants et expressions sont consignés comme attestés dans des ressources pédagogiques; les traductions littérales et l'usage oral restent à valider. Aucun audio et aucune règle de production ne sont validés par ce document.


## Règle obligatoire pour les textes destinés à la synthèse vocale

Les champs numériques et les métadonnées peuvent conserver les chiffres pour les calculs, les filtres et les contrôles. En revanche, **aucun chiffre ni symbole monétaire ne doit être inclus dans le texte envoyé au moteur de synthèse vocale**.

Le CSV fournit donc deux champs dédiés :

- `texte_soninke_audio` : uniquement l'expression soninkée en lettres, sans montant chiffré ni annotation;
- `texte_fr_audio` : uniquement la traduction française en toutes lettres, par exemple `cinq francs CFA`, jamais `5 FCFA`.

Exemple de donnée de référence : `godi baane` pour le texte soninké à prononcer, et `cinq francs CFA` pour la traduction française à prononcer. La glose de travail peut indiquer `godi ou gode = cinq francs CFA`, mais cette équivalence reste à confirmer par un locuteur. Ne pas prononcer les colonnes d'identifiant, de montant numérique, de statut ou de notes. Les lignes sans forme documentée, notamment les candidats en euros, gardent les champs audio vides : ne rien inventer.

Cette règle prépare les données; elle ne prouve pas qu'un moteur ou le code de production respecte déjà ce format. Les changements restent sur la branche de recherche et ne sont pas fusionnés dans `main`.


## Compréhension des montants saisis par l'utilisateur

SoninkeGPT doit reconnaître les montants exprimés en chiffres ou en lettres, avec des variantes de formulation usuelles, puis les résoudre vers une entrée du référentiel monétaire. Exemple : « 5 francs CFA », « cinq francs CFA » et « 5 FCFA » doivent être normalisés vers le même montant numérique et la même monnaie; si l'entrée correspondante est validée, la sortie soninkée attendue est sa forme lexicale enregistrée, par exemple `godi baane` (variante `gode baane` à confirmer). Ne pas transformer la saisie française en lecture littérale des chiffres.

### Pipeline recommandé

1. **Normalisation de la saisie** : interpréter chiffres et nombres écrits en lettres; normaliser les variantes de monnaie comme « FCFA » et « francs CFA » sans perdre la monnaie.
2. **Résolution du montant** : extraire une paire structurée `montant_numérique + monnaie`, par exemple `5 + FCFA`.
3. **Recherche monétaire** : consulter le référentiel des expressions monétaires, pas uniquement le dictionnaire des nombres cardinaux. Ne pas supposer que les règles de FCFA s'appliquent à l'euro.
4. **Récupération de la forme** : retourner l'expression soninkée exacte associée à ce montant et à cette monnaie, avec le statut de validation.
5. **Audio** : envoyer uniquement le champ `texte_soninke_audio` au moteur vocal; ne jamais envoyer les chiffres, codes de monnaie, identifiants ou notes techniques.
6. **Absence de correspondance validée** : ne pas inventer de forme. Retourner une candidate explicitement marquée à vérifier, ou demander une précision si la monnaie/le contexte est ambigu.

### Tests d'acceptation

- « 5 francs CFA » et « cinq francs CFA » résolvent au même montant et à la même entrée monétaire.
- « 5 FCFA » ne doit pas être lu comme une suite de chiffres ni traduit mot à mot; il doit déclencher la recherche monétaire.
- Le texte envoyé à la synthèse vocale est uniquement une expression soninkée en lettres, sans chiffres ni symbole monétaire.
- Une somme en euros ne doit pas être convertie automatiquement en une expression fondée sur `gode`.
- Une entrée non validée ne doit pas être présentée comme une traduction certaine.

**Limite actuelle :** cette spécification décrit le comportement requis; elle ne signifie pas que le code applicatif de production implémente déjà cette résolution. Les formes monétaires de ce dossier restent candidates tant qu'elles ne sont pas validées par un référent linguistique.

## Inventaire élargi des candidats monétaires — variantes conservées

La recherche complémentaire ajoute des formes qui ne doivent pas être fusionnées silencieusement. Les traductions ci-dessous donnent le **sens monétaire rapporté de l'expression entière** en français écrit en toutes lettres; elles ne prétendent pas établir un mot-à-mot certain quand la segmentation reste incertaine.

| Montant | Expression soninkée candidate, en lettres | Traduction française, en lettres | Point à vérifier |
|---|---|---|---|
| cinq francs CFA | godi baane | cinq francs CFA | Comparer godi, gode et godo; forme exacte et variété |
| cinq francs CFA | gode baane | cinq francs CFA | Forme du manuel SIL Mali |
| cinq francs CFA | godo baane | cinq francs CFA | Forme du manuel SIL Mali |
| dix francs CFA | godo hilli | dix francs CFA | Comparer hilli et filli |
| dix francs CFA | godo filli | dix francs CFA | Variante du manuel SIL Mali |
| quinze francs CFA | godo sikki | quinze francs CFA | Prononciation et graphie |
| vingt francs CFA | godo naxati | vingt francs CFA | Prononciation et graphie |
| vingt-cinq francs CFA | godo karagi | vingt-cinq francs CFA | Prononciation et graphie |
| cinquante francs CFA | godo tanmi | cinquante francs CFA | Ne pas confondre avec dix francs CFA |
| cent francs CFA | tanpille gode | cent francs CFA | Comparer avec tanfille gode |
| cent francs CFA | tanfille gode | cent francs CFA | Variante du manuel SIL Mali |
| cent cinquante francs CFA | tanjikke gode | cent cinquante francs CFA | Attestation communautaire à corroborer |
| cent soixante-quinze francs CFA | tanjikke do karago gode | cent soixante-quinze francs CFA | Exemple pédagogique; valider la segmentation |
| deux cents francs CFA | tannaxate | deux cents francs CFA | Sens monétaire rapporté; analyse interne non confirmée |
| trois cents francs CFA | tandume | trois cents francs CFA | Sens monétaire rapporté; analyse interne non confirmée |
| cinq cents francs CFA | keme gode | cinq cents francs CFA | Comparer keme et kame |
| mille francs CFA | komohillin dere | mille francs CFA | Sens de dere non établi |
| mille francs CFA | kamo filli gode | mille francs CFA | Variante du manuel SIL Mali; ne pas fusionner avec komohillin dere |
| deux mille francs CFA | komonaxatin dere | deux mille francs CFA | Sens de dere non établi |
| un billet de cinq mille francs CFA | wujinin dere | un billet de cinq mille francs CFA | Contexte de billet rapporté |
| cinq mille francs CFA | wujune gode | cinq mille francs CFA | Forme rapportée en unités de gode; comparer au contexte de billet |
| un billet de dix mille francs CFA | wujunnin pillin dere | un billet de dix mille francs CFA | Segmentation non établie |
| cent mille francs CFA | tanpillle wujunne | cent mille francs CFA | Graphie et construction à vérifier |
| deux cent mille francs CFA | tannaxate wujinne | deux cent mille francs CFA | Construction à vérifier |
| trois cent mille francs CFA | tandume wujinne | trois cent mille francs CFA | Construction à vérifier |
| cinq cent mille francs CFA | keme wujinne | cinq cent mille francs CFA | Construction à vérifier |

### Règles de lecture de cet inventaire

- Les formes en soninké et les traductions françaises sont écrites en toutes lettres dans les champs destinés à la prononciation. Les montants numériques restent dans des champs séparés pour les calculs.
- « Sens de l'expression » signifie ici la valeur monétaire rapportée dans la source, pas nécessairement une traduction littérale mot à mot de chaque morphème.
- Le calcul par unités de cinq est explicitement soutenu pour certaines expressions avec `gode`; il ne justifie pas d'extrapoler toutes les autres expressions.
- Les entrées `tannaxate` et `tandume` sont rapportées pour deux cents et trois cents francs CFA dans une ressource, mais leur segmentation et leur analyse comme nombre d'unités de `gode` restent des hypothèses.
- `komohillin dere` et `kamo filli gode` sont deux expressions distinctes rapportées pour mille francs CFA. Il faut conserver les deux avec leur provenance jusqu'à l'enquête orale.
- Les euros restent sans expression candidate validée. Aucune forme FCFA ne doit être transposée automatiquement à l'euro.
- Les nouvelles lignes du CSV sont des candidats documentaires, pas des traductions validées ni des enregistrements audio prêts pour la production.



## Référentiel de candidats en euros et centimes — première génération

Le fichier `data/source/euro-counting-candidates.csv` a été ajouté comme **inventaire de recherche**, séparé du CSV des expressions monétaires CFA. Il contient 221 lignes candidates :
- les valeurs de 1 à 99 centimes ;
- les valeurs de 1 à 99 euros ;
- des sommes élevées représentatives, de 100 euros à un million d'euros.

Les formes de nombres sont reprises du système cardinal soninké documenté, puis associées provisoirement à l'unité française `centime` ou `euro`. Pour les nombres inférieurs à 20, le fichier utilise provisoirement une structure nom d'unité + nombre; à partir de 20, il utilise nombre + unité, conformément à la description générale de l'ordre des cardinaux et des noms dans le guide d'écriture. **Cette règle grammaticale n'est pas encore une validation de l'usage monétaire en soninké de France.**

Les expressions de ce fichier sont donc toutes au statut `hypothèse composée — ordre à valider`. Le champ `audio_text_candidate` est volontairement vide : aucune expression ne doit être envoyée au TTS avant vérification orale. La graphie et la prononciation de `euro` et `centime`, le singulier/pluriel, les variantes de diaspora et les formulations des montants mixtes (par exemple euros + centimes) restent à établir.

Pour les montants mixtes, conserver d'abord une décomposition numérique exacte en euros et centimes; ne pas assembler les deux segments en une phrase soninkée ni produire un audio tant que la conjonction, l'ordre et la réalisation naturelle n'ont pas été recueillis auprès de locuteurs.

Les nombres au-delà des valeurs présentes dans le fichier ne doivent pas être extrapolés silencieusement. Il faudra compléter la couverture avec des tests d'élicitation, et vérifier les formes des grands nombres avec les sources et les locuteurs. Ce référentiel n'est pas intégré au code de production et n'est pas fusionné dans `main`.


## Extension des candidats composés — cardinal + unité monétaire

Le référentiel `data/source/euro-counting-candidates.csv` a été étendu à 1 112 lignes candidates :
- 1 à 99 centimes ;
- 1 à 999 euros ;
- montants repères de 1 000 à 1 000 000 euros, avec des valeurs intermédiaires utiles.

Cette extension s'appuie sur des sources de numération cardinale : notamment `tanpille do karago` = 25, `tanjikke` = 30, `kame do tankarage` = 150, `kamo karagi` = 500 et `wujune` = 1 000. Les formes cardinales ne prouvent pas automatiquement la construction monétaire : chaque expression avec `euro` ou `centime` reste candidate.

Les guides de grammaire décrivent une différence d'ordre : les cardinaux jusqu'à 19 suivent le nom et ont une forme comptée; à partir de 20, le cardinal précède le nom. Pour cette raison, les lignes de 1 à 19 ne préjugent pas de la morphologie de l'emprunt français et affichent explicitement que l'ordre et la forme comptée doivent être vérifiés. Les formes de 20 et plus utilisent provisoirement « cardinal + unité », conformément à cette règle générale, mais restent à valider oralement dans la diaspora en France.

### Points à ne pas confondre

- `tanpille do karago` = 25, pas 150.
- `tanjikke` = 30, pas 150.
- `kame do tankarage` = 150 dans la numération cardinale générale.
- `kamo karagi` = 500 dans la numération cardinale générale.
- Dans le comptage CFA, une expression telle que `tanjikke gode` est rapportée pour 150 FCFA dans une source communautaire; cela doit rester séparé de la forme cardinale `kame do tankarage`. Le contexte monétaire peut suivre une convention distincte.

Aucune des expressions de ce référentiel n'a un texte audio prêt à générer : le champ audio reste vide jusqu'à la validation par locuteur. Le fichier est une liste de travail destinée à l'élicitation et aux tests, non une liste de traductions confirmées. Les montants mixtes (euros et centimes dans une même somme) nécessitent encore une règle de composition séparée et des validations orales.

Sources de numération à comparer :
- Omniglot, « Numbers in Soninke » : https://omniglot.com/language/numbers/soninke.htm
- Guide d'écriture soninké, section 2.5 « Les numéraux » : https://fr.scribd.com/document/690364522/Guide-d-Ecriture-Soninke
- Soninkara.com, « Compte-rendu du 4ème cours de Soninké en ligne » : https://www.soninkara.com/langue/apprendre-le-soninke/compte-rendu-du-4eme-cours-de-soninke-en-ligne.html
- CNRS, « Soninké : lexique (quantitatifs et numéraux) » : https://lgidf.cnrs.fr/node/679
