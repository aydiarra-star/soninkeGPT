# Vérification croisée des renvois avec la revue source

Date : 2026-10-21  
Branche : `data/lexique-soninke-fr-v1`

## Avancée importante
J'ai comparé les composants des 236 segments de renvoi avec :
- la base de production, qui contient 305 lemmes;
- le fichier de revue de l'enrichissement, qui contient 632 lemmes distincts après normalisation prudente des espaces, de la casse et de l'Unicode.

Cette comparaison montre que de nombreuses cibles qui semblent absentes de la base de production sont déjà représentées dans la revue source. Il faut donc d'abord vérifier ces entrées candidates et leur statut, au lieu de créer de nouvelles entrées ou de conclure à une absence.

## Résultats au niveau des composants de cible
Les compteurs ci-dessous portent sur les composants extraits des cibles (pas sur des segments exclusifs; un renvoi peut contenir plusieurs composants).

- 99 composants correspondent exactement à un lemme de la base de production.
- 141 composants non présents dans la base correspondent exactement à un lemme de la revue source.
- 28 composants ordinaires n'ont été retrouvés ni dans la base ni dans la revue source.
- 115 composants sont des marqueurs ou notations à interpréter (par exemple formes avec tiret ou notations du type `n4`).

Les chiffres se chevauchent au niveau d'un même renvoi, car une cible peut comporter plusieurs composants.

## Exemples de cibles retrouvées dans la revue source
| Lemme source du renvoi | Cible | Glose trouvée dans la revue source | Traitement |
|---|---|---|---|
| baabe | baananbe | chacun | Vérifier le sens et l'entrée avant rattachement |
| baabondi | baabo1 | mousse, écume | Conserver le chiffre final; vérifier l'entrée numérotée |
| baamindi | baami | aller au petit galop, chevaucher | Comparer la construction verbale et le suffixe |
| baanaaxu | baana2 | ressembler, être uni, être un | Vérifier les sens et le numéro d'entrée |
| baawo2 | baabo2 | gardien des circoncis | Vérifier le contraste graphique baawo2 / baabo2 |
| baawo3 | baabo3 | orage, première grande pluie de l'hivernage | Conserver les sens et le numéro de l'entrée |
| bafaade | boyaade | drap, couvre-lit | Vérifier la graphie dans le dictionnaire source |
| bajjo | bajo1 | couverture en laine | Garder distinct de bajo2 |
| bajjo | bajo2 | fils unique | Ne pas fusionner avec bajo1 |

Les gloses ci-dessus sont celles de la revue source et restent des données de travail; elles ne constituent pas une validation linguistique finale.

## Priorités de la prochaine passe
1. Pour chaque cible retrouvée dans la revue source, récupérer son statut, sa glose, son texte source et ses occurrences, puis la relier à l'entrée candidate correspondante.
2. Garder les formes numérotées distinctes, notamment `baabo1`, `baabo2`, `baabo3`, `baana2`, `bajo1` et `bajo2`.
3. Examiner manuellement les composants non retrouvés, sans faire de rapprochement sur la seule ressemblance orthographique.
4. Traiter séparément les marqueurs morphologiques et notations comme `-ndi3`, `-aaxu`, `-o4` et `n4`.
5. Ne rien importer dans la base tant que la validation linguistique n'a pas été obtenue.

## Fichiers de référence
- [Rapprochement initial des renvois](rapprochement-renvois-base-soninke-2026-10-21.csv)
- [Contrôle détaillé des renvois](controle-renvois-dictionnaire-soninke-2026-10-21.csv)
- [Revue d'enrichissement source](revue-enrichissement-dictionnaire-soninke.csv)
- [Base lexicale de production](../data/lexique-soninke-fr-base.csv)

La base de production reste inchangée à 305 entrées.
