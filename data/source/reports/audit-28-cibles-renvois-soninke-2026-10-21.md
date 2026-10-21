# Audit des cibles de renvoi non retrouvées exactement

Date : 2026-10-21  
Branche : `data/lexique-soninke-fr-v1`

## Portée et prudence

Cet audit reprend les 28 lignes signalées `CIBLE NON RETROUVÉE EXACTEMENT` dans les trois fichiers `fiches-cibles-renvois-soninke-partie-*.csv`. Elles représentent **24 lemmes sources distincts**, car plusieurs renvois sont répétés à des paragraphes différents. « Non retrouvé exactement » décrit une limite de rapprochement textuel : ce n’est ni une preuve d’absence lexicale ni une validation linguistique.

La base de production `data/lexique-soninke-fr-base.csv` n’a pas été modifiée. Son SHA observé reste `bccba206db414a3a7f630a01718012faa81bd012`. Les rapprochements ci-dessous sont des pistes de contrôle, pas des corrections validées.

## A. Renvois morphologiques ou composés — vérifier la segmentation

| Lemme source | Renvoi extrait | Lecture prudente / prochaine vérification |
|---|---|---|
| `faabanbaanaaxu` | `-aaxu, baane, baane, faaba2` | Renvoi composite avec répétition de `baane` et marqueur `-aaxu`. Vérifier la chaîne complète dans la source avant de déterminer la tête. |
| `faqilanbali` | `-bali, haqile, n4` | Le marqueur `-bali` et `n4` semblent grammaticaux; `haqile` est une piste de tête, à confirmer. |
| `ɲamanbali` | `-bali, n4, n4, ɲama1` | Renvoi composite; conserver la répétition dans la trace et vérifier si elle vient de la source ou de l’extraction. |
| `batikanxoore` | `bati, kaa, n4, xoore` | Expression composée. La définition indique le temple de Jérusalem; ne pas réduire l’expression à `kaa` ou `xoore` seul. |
| `battaranlenme` | `battara, n4, renme` | Construction nominale composée; `battara` est une piste de tête, pas une décision finale. |
| `battaransere` | `battara, n4, sere1` | Construction composée; vérifier le rôle de `sere1` et la relation avec `battara`. |
| `allanbatte1` | `Alla, batu2` | Expression liée à l’adoration de Dieu; conserver l’expression entière et vérifier le lien entre les deux composants. |
| `baxandoroke` | `baxa1, doroke, n4` | Nom composé associé à une robe indigo; contrôler les deux composants et leur ordre. |
| `fatanbinne` | `binne, fate1, n4` | Expression nominale; la définition porte sur une personne africaine à peau noire. Vérifier la segmentation et le sens dans son contexte source. |
| `boroxonjilinka` | `boroxonjile, kaa, n4` | Le candidat `boroxonjile` est retrouvé dans la revue source avec une glose liée à la fourmi noire qui pique; vérifier la formation du nom de fourmilière. Deux segments sources proches doivent être conservés. |
| `nuxudunbure` | `bure, -dun, -dun, nuxu` | Renvoi adjectival composite; marqueur répété. Vérifier la forme complète, sans supprimer les répétitions par automatisme. |
| `buudinlenme` | `buudi, n4, renme, n4` | Expression définie comme « pièce d’argent »; `buudi` apparaît aussi dans la revue avec un sens distinct (« être rond »). Ne pas fusionner les sens. |
| `consonlindaana` | `-aana, -ndi1, sonsolo` | Formation dérivée; vérifier la relation entre le suffixe `-aana`, `-ndi1` et la tête `sonsolo`. |

## B. Renvois possiblement orthographiques ou variantes — rattachement à contrôler

| Lemme source | Cible indiquée par la source | Prochaine vérification |
|---|---|---|
| `baramaneene` | `faramaneene` | Renvoi direct, probablement une variante graphique initiale b/f; vérifier la source et la prononciation avant de normaliser. |
| `ciga` | `tiga` | Renvoi direct c/t; vérifier comme variante, sans créer automatiquement une nouvelle entrée indépendante. |
| `cigakorome` | `tigakorome` | Même correspondance c/t; vérifier séparément la forme composée. |
| `cigamaxafo` | `tigamaxafo` | Même correspondance c/t; conserver le lemme source et sa provenance. |
| `cigate` | `tigate` | Même correspondance c/t; rattachement à confirmer. |
| `ciye` | `tiye` | Correspondance c/t; vérifier la variante et la catégorie grammaticale. |
| `consolinde` | `sonsolondi` | Différences plus larges que c/t; contrôler la graphie et la morphologie dans la source. |
| `consolindi` | `sonsolondi` | Deuxième forme proche de `consolinde`; garder les deux renvois séparés jusqu’à vérification. |
| `cuballe` | `suballe` | Renvoi direct c/s; vérifier la variante graphique. |
| `cunsu` | `sunsu` | Renvoi direct c/s; vérifier la variante graphique. |
| `cuuba` | `juuba` | Renvoi direct c/j; vérifier la variante et la prononciation. |

## C. Cas à ne pas confondre avec une cible absente

- `faabanbaanaaxu`, `faqilanbali`, `ɲamanbali`, `batikanxoore`, `battaranlenme`, `battaransere`, `allanbatte1`, `baxandoroke`, `fatanbinne`, `boroxonjilinka`, `nuxudunbure`, `buudinlenme` et `consonlindaana` sont surtout des cas de renvoi composite ou morphologique. Une comparaison exacte de chaque fragment n’est pas une méthode suffisante pour décider du rattachement.
- Les renvois `ciga → tiga`, `cigakorome → tigakorome`, `cigamaxafo → tigamaxafo`, `cigate → tigate`, `ciye → tiye`, `cuballe → suballe`, `cunsu → sunsu` et `cuuba → juuba` ont une cible explicitement indiquée dans le texte source. Leur statut devrait être « renvoi à vérifier », et non « nouveau lemme », jusqu’à examen de la relation variante/tête.
- Les deux paragraphes de `boroxonjilinka` et de `buudinlenme`, ainsi que les paragraphes répétés de `battaranlenme`, doivent rester traçables comme occurrences distinctes.

## Décision de contrôle

1. **Aucune importation automatique** dans la base de production.
2. Pour les renvois directs, vérifier la graphie de la tête et préserver le lemme source comme variante/renvoi si confirmé.
3. Pour les composés, contrôler l’entrée complète, la glose et les exemples; ne pas traiter `n4`, `-ndi1`, `-bali`, `-aaxu` ou d’autres marqueurs comme des lemmes ordinaires sans contexte.
4. Faire valider les rattachements par le référent linguistique avant toute modification du lexique de production.

## Sources de travail

- [Fiches cibles — partie 1](fiches-cibles-renvois-soninke-partie-1-2026-10-21.csv)
- [Fiches cibles — partie 2](fiches-cibles-renvois-soninke-partie-2-2026-10-21.csv)
- [Fiches cibles — partie 3](fiches-cibles-renvois-soninke-partie-3-2026-10-21.csv)
- [Revue d’enrichissement source](revue-enrichissement-dictionnaire-soninke.csv)
- [Base de production](../data/lexique-soninke-fr-base.csv)
