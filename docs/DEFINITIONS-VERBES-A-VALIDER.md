# Définitions des verbes du document soninké — à valider par le référent

Document source : [Google Doc du référent](https://docs.google.com/document/d/1L0ykGjJPnOaFJYF6xtdAAqozt0qU2nBBEChgwGWNuA4/edit) (`data/grammaire/soninke.yaml`). Définitions du 2026-10-24.

## Ce que montre le travail

| Constat | Nombre |
| --- | --- |
| Verbes du document | **182** |
| Déjà présents dans le lexique (entrée existante) | **182** |
| À créer comme nouvelle entrée | **0** |
| Définition rédigée et proposée | **182** |
| dont glose du lexique à trancher d'abord | **17** |
| Définition encore à écrire | **0** |
| Avec au moins une phrase d'emploi attestée | **13** |

**Aucune entrée créée : les 182 verbes ont déjà leur entrée de lexique.** Chaque définition est ajoutée à une entrée existante, jamais à une ligne nouvelle — c'est ce qui garantit l'absence de doublon.

## Comment les définitions sont écrites

Chaque définition est rédigée en français à partir de la glose déjà attestée dans le lexique (`francais`) et, quand elle existe, de la ligne de glose anglaise de la source. Aucune définition n'ajoute un sens que ces sources ne portent pas : les cas douteux sont marqués `a_clarifier` et expliqués dans la note, au lieu d'être tranchés arbitrairement.

Les définitions sont rédigées dans `data/source/definitions-verbes-redigees.csv`, jointes ici par `scripts/preparer_definitions_verbes.py`, puis écrites dans la colonne `definition` des entrées existantes par `scripts/enrichir_verbes_sans_doublons.py`.

## Règle anti-doublon appliquée

1. La forme est cherchée dans les entrées **et** dans les variantes, avec la comparaison du projet (`scripts/import_extraction_sans_doublons.py`) : casse, accents vocaliques, traits d'union, apostrophes et numéros d'homonyme ignorés ; `ñ`, `ŋ`, `ɲ` restent distincts.
2. Si la forme est déjà une entrée : la définition enrichit cette entrée, jamais une nouvelle ligne.
3. Si la forme n'est citée que comme variante : aucune création, la ligne porte `risque_doublon = forme citée comme variante`.
4. Le script d'application refuse toute forme qui n'est pas déjà une entrée, refuse d'ajouter une ligne, puis relance `check_doublons_lexique.py --strict`.

## Points à trancher par le référent

17 verbes ont une définition proposée, mais leur glose de départ est incertaine ou contradictoire. Ils ne doivent pas être utilisés comme traduction sûre avant arbitrage.

| Soninké | Glose du lexique | Définition proposée | Ce qui bloque | Entrée |
| --- | --- | --- | --- | --- |
| **bexin** | zipper | Fermer au moyen d'une fermeture à glissière. | Glose « zipper » du lexique. Un verbe soninké de ce sens n'a pas pu être recoupé : vérifier la graphie et le sens avant usage. | `SNK-LEX-0150` |
| **bisimilahi** | accueillir | Accueillir quelqu'un, lui souhaiter la bienvenue. | La forme est la formule d'ouverture arabe employée à l'accueil. Le sens verbal « accueillir » est celui du lexique, à confirmer par le référent. | `SNK-LEX-0152` |
| **boxu** | déchirer / Un groupe de souris | Déchirer, mettre en pièces. | Le lexique porte deux gloses inconciliables pour cette forme, « déchirer » et « un groupe de souris » : le sens doit être tranché. | `SNK-LEX-0059` |
| **duguta** | terminer | Terminer, achever, mener à son terme. | Glose « terminer » du lexique, mais l'exemple attesté de l'entrée emploie la forme au sens d'« ouvrir » (Waayen duguta jaxen baragana « Il est allé ouvrir les calebasses »). Sens à trancher. | `SNK-LEX-0111` |
| **kanalaga** | sentir | Sentir, percevoir une odeur. | Glose « sentir » du lexique. Le sens (percevoir une odeur, ou dégager une odeur) n'est pas tranché : à préciser avec le référent. | `SNK-LEX-0177` |
| **kofuma** | unir | Unir, mettre ensemble pour faire un tout. | Glose très proche de kafuma « additionner » : la distinction entre les deux formes est à vérifier. | `SNK-LEX-0120` |
| **ku** | offrir | Offrir, donner en présent. | Glose « offrir » du lexique, mais l'exemple attesté de l'entrée emploie ku comme démonstratif (« Kuhn jaxi baanu » : « ces autres moutons »). Sens et catégorie à vérifier. | `SNK-LEX-0171` |
| **me-wutu** | coordonner | Coordonner, agencer les parties d'un ensemble. | Glose de vocabulaire technique moderne, non recoupée. Forme à trait d'union à vérifier. | `SNK-LEX-0046` |
| **simandi** | en rappeler | Rappeler quelque chose, le remettre en mémoire. | Glose « en rappeler » incomplète dans le lexique : rappeler à autrui ou se rappeler ? Sens à trancher. | `SNK-LEX-0139` |
| **sooti** | brancher | Brancher, raccorder à une installation. | Glose de vocabulaire technique moderne, non recoupée. Vérifier le sens exact (raccorder, ou se ramifier). | `SNK-LEX-0031` |
| **sore** | cuisiner | Cuisiner, faire la cuisine. | Le lexique porte aussi, sous le même identifiant, l'exemple « dermatitis ; dartre, dermatose » : homographe apparent. Il faut séparer le verbe « cuisiner » du nom de maladie avant usage. | `SNK-LEX-0052` |
| **sumba** | souquer | Souquer, haler sur un cordage. | Glose technique de marine, peu compatible avec le corpus disponible : sens à confirmer. | `SNK-LEX-0143` |
| **taxu** | asseoir | S'asseoir, prendre place. | La glose « asseoir » peut désigner le sens causatif (faire asseoir) ou réfléchi (s'asseoir) : à trancher. | `SNK-LEX-0154` |
| **tewe** | assister | Assister à un événement, y être présent. | Le français « assister » signifie aussi « aider » : le sens visé par la glose du lexique n'est pas certain. | `SNK-LEX-0026` |
| **tu** | connaître | Connaître, avoir la connaissance de quelqu'un ou de quelque chose. | La forme est homographe du pronom français « tu » : vérifier qu'aucun exemple français n'a été pris pour une attestation soninké. | `SNK-LEX-0159` |
| **xaso** | vieillir | Vieillir, prendre de l'âge. | Glose « vieillir » du lexique, mais l'emploi attesté Xaso ga na bita parle de la lune qui décroît : xaso pourrait être « lune, mois ». Sens à vérifier avant usage. | `SNK-LEX-0122` |
| **yaxawunyi-yen xedie** | réveiller | Réveiller quelqu'un, le tirer du sommeil. | Forme composée à plusieurs mots, notée telle quelle dans le document : c'est un groupe figé et non un verbe simple. Vérifier la graphie et l'usage. | `SNK-LEX-0102` |

## Les 182 définitions, verbe par verbe

Ordre alphabétique soninké. « Emploi attesté » donne une phrase du corpus quand il en existe une, avec sa traduction française d'origine quand la source la fournit.

| Soninké | Traduction (glose du lexique) | Définition | Emploi attesté | Entrée |
| --- | --- | --- | --- | --- |
| **baano** | ressembler | Avoir l'air de, présenter les mêmes traits ou le même aspect que quelqu'un ou quelque chose. | — | `SNK-LEX-0099` |
| **bagu** | sortir | Quitter un lieu, passer du dedans au dehors. | Kan betu, soron bagu. — « La marmite est complètement remplie. » (`SNK-LEX-0256`) | `SNK-LEX-0178` |
| **bakuman** | distinguer | Reconnaître une chose d'une autre, percevoir une différence entre deux choses. | — | `SNK-LEX-0058` |
| **bante** | absenter / s'absenter, s'abstenir de, manquer / fonctionne comme marque de la modalité "refuser à faire | S'absenter, manquer à un endroit, s'abstenir de faire quelque chose. | — | `SNK-LEX-0129` |
| **bara** | refuser / fonctionne comme marque de la modalité "refuser à faire / aire, surface, cour / ficelle, fil | Refuser, rejeter ce qui est proposé ou demandé. | — | `SNK-LEX-0093` |
| **batu** | obéir / réunion, assemblée / marabatu / obéir, adorer / devoir (redevabilité) | Obéir à quelqu'un, le vénérer, adorer (Dieu). | — | `SNK-LEX-0078` |
| **besin** | frotter | Frotter une surface en appuyant, pour nettoyer, polir ou faire pénétrer un produit. | — | `SNK-LEX-0141` |
| **bexin** ⚠ | zipper | Fermer au moyen d'une fermeture à glissière. | — | `SNK-LEX-0150` |
| **bire** | vivre / instant, moment / quand | Vivre, être en vie. | — | `SNK-LEX-0180` |
| **bisimilahi** ⚠ | accueillir | Accueillir quelqu'un, lui souhaiter la bienvenue. | — | `SNK-LEX-0152` |
| **biyi** | brûler / buyi / être brûlé, être grillé | Brûler, consumer par le feu. | — | `SNK-LEX-0032` |
| **boguman** | séparer | Séparer, mettre à part, désunir des personnes ou des choses. | — | `SNK-LEX-0110` |
| **bonte** | sauter / sauter par-dessus | Sauter, s'élever d'un bond. | — | `SNK-LEX-0106` |
| **boxu** ⚠ | déchirer / Un groupe de souris | Déchirer, mettre en pièces. | — | `SNK-LEX-0059` |
| **bulxa** | effacer | Effacer, faire disparaître une trace ou une inscription. | — | `SNK-LEX-0138` |
| **contan** | compter | Compter, dénombrer, énumérer des unités. | — | `SNK-LEX-0045` |
| **daga** | partir | Partir, quitter un lieu pour aller ailleurs. | Binta daga i faaba banŋe. — « Binta est allée chez son père. » (`SNK-LEX-0211`) | `SNK-LEX-0001` |
| **dantaxi** | annoncer | Annoncer, faire savoir publiquement. | — | `SNK-LEX-0020` |
| **dema** | aider | Aider quelqu'un, lui apporter son appui. | — | `SNK-LEX-0017` |
| **diabi** | répondre | Répondre à quelqu'un, répliquer. | — | `SNK-LEX-0176` |
| **diamba** | trahir | Trahir quelqu'un, manquer à la fidélité promise. | — | `SNK-LEX-0148` |
| **diambe** | abandonner | Abandonner quelqu'un ou une entreprise, laisser sans secours. | — | `SNK-LEX-0012` |
| **dioofe** | arriver | Arriver, parvenir au lieu où l'on se rend. | — | `SNK-LEX-0025` |
| **diopandi** | commencer | Commencer, entreprendre une action. | — | `SNK-LEX-0044` |
| **dioxi** | couler | Couler, s'écouler en parlant d'un liquide. | — | `SNK-LEX-0048` |
| **djikeranxoso** | décevoir | Décevoir, tromper l'attente de quelqu'un. | — | `SNK-LEX-0166` |
| **doron** | respecter | Respecter, honorer quelqu'un. | — | `SNK-LEX-0097` |
| **dufintandi** | plonger | Plonger, s'enfoncer dans un liquide. | — | `SNK-LEX-0084` |
| **dufuutu** | étirer | Étirer, allonger en tirant. | — | `SNK-LEX-0151` |
| **dugu** | attendre | Attendre, patienter jusqu'à un moment donné. | — | `SNK-LEX-0155` |
| **duguta** ⚠ | terminer | Terminer, achever, mener à son terme. | Waayen duguta jaxen baragana. — « Il est allé ouvrir les calebasses. » (`SNK-LEX-0382`) | `SNK-LEX-0111` |
| **duŋe** | accepter | Accepter, consentir à ce qui est proposé. | — | `SNK-LEX-0013` |
| **faamu** | comprendre | Comprendre, saisir le sens de quelque chose. | — | `SNK-LEX-0158` |
| **fallanyille** | reculer | Reculer, aller en arrière, rétrograder. | — | `SNK-LEX-0092` |
| **fanqe** | lutter | Lutter, se battre contre quelqu'un ou quelque chose. | — | `SNK-LEX-0070` |
| **faraxu** | changer | Changer, devenir autre, se transformer. | — | `SNK-LEX-0037` |
| **fatampantchi** | argumenter | Argumenter, discuter en avançant des raisons et des preuves. | — | `SNK-LEX-0024` |
| **faye** | regarder | Regarder, observer attentivement. | — | `SNK-LEX-0003` |
| **filinka** | tourner | Tourner, faire tourner, se retourner. | — | `SNK-LEX-0146` |
| **fimaxagomundi** | préparer | Préparer, apprêter ce qui est nécessaire. | — | `SNK-LEX-0087` |
| **finkoyindi** | présenter | Présenter quelqu'un, le faire connaître à d'autres. | — | `SNK-LEX-0088` |
| **finsaanindi** | décider | Décider, trancher une question. | — | `SNK-LEX-0060` |
| **finsirondi** | réconcilier | Réconcilier, rétablir la concorde entre des personnes brouillées. | — | `SNK-LEX-0100` |
| **fita** | jeter | Jeter, se défaire de quelque chose en le lançant. | — | `SNK-LEX-0067` |
| **fitta** | lancer | Lancer, projeter avec force. | — | `SNK-LEX-0069` |
| **fiwarame** | disputer | Se disputer, se quereller, échanger des reproches. | — | `SNK-LEX-0057` |
| **fixorondi** | empirer | Empirer, rendre pire une situation. | — | `SNK-LEX-0064` |
| **fufe** | respirer | Respirer, aspirer et rejeter de l'air. | — | `SNK-LEX-0098` |
| **fuutu** | tirer | Tirer, extraire quelque chose en tirant. | — | `SNK-LEX-0112` |
| **gadia** | combattre | Combattre, faire la guerre, se battre contre un adversaire. | — | `SNK-LEX-0157` |
| **gage** | vendre | Vendre, céder une marchandise contre paiement. | — | `SNK-LEX-0179` |
| **gara** | mentir | Mentir, dire ce qui est faux. | — | `SNK-LEX-0168` |
| **goli** | travailler | Travailler, accomplir un travail. | — | `SNK-LEX-0010` |
| **gomundi** | réparer | Réparer, remettre en état ce qui est abîmé. | — | `SNK-LEX-0101` |
| **gongo** | avertir | Avertir, prévenir quelqu'un de quelque chose. | — | `SNK-LEX-0030` |
| **gunudi** | plier | Plier, courber ce qui était droit. | — | `SNK-LEX-0083` |
| **kaanemaxawutu** | diriger | Diriger, conduire un groupe, prendre la tête. | — | `SNK-LEX-0056` |
| **kaban** | interdire | Interdire, défendre de faire quelque chose. | — | `SNK-LEX-0167` |
| **kafuma** | additionner | Additionner, réunir des nombres en un total. | — | `SNK-LEX-0016` |
| **kanalaga** ⚠ | sentir | Sentir, percevoir une odeur. | — | `SNK-LEX-0177` |
| **kanewutu** | devancer | Devancer, prendre les devants sur quelqu'un. | — | `SNK-LEX-0055` |
| **kara** | casser | Casser, briser. | — | `SNK-LEX-0036` |
| **kari** | tuer | Tuer, ôter la vie. | O fedden da batundonu filli kari yirigi wenden (22) sallen ŋa. — « Notre groupe a tué deux moutons élevés à la maison lors de la fête du 22 septembre. » (`SNK-LEX-0410`) | `SNK-LEX-0119` |
| **katu** | battre | Battre, frapper à plusieurs reprises. | — | `SNK-LEX-0156` |
| **kawafi** | étonner | Étonner, surprendre, frapper d'étonnement. | — | `SNK-LEX-0128` |
| **kerin** | éteindre | Éteindre un feu ou une lumière. | — | `SNK-LEX-0181` |
| **keti** | toucher | Toucher, entrer en contact avec la main. | — | `SNK-LEX-0115` |
| **ko** | dire | Dire, énoncer. | — | `SNK-LEX-0164` |
| **kofuma** ⚠ | unir | Unir, mettre ensemble pour faire un tout. | — | `SNK-LEX-0120` |
| **konti** | perdre | Perdre, ne plus retrouver ce qu'on possédait. | — | `SNK-LEX-0173` |
| **konun** | effrayer | Effrayer, faire peur. | — | `SNK-LEX-0062` |
| **koroosa** | tricoter | Tricoter, fabriquer un tissu avec des mailles. | — | `SNK-LEX-0117` |
| **korosin** | surveiller | Surveiller, garder à l'œil. | — | `SNK-LEX-0109` |
| **koyin** | montrer | Montrer, faire voir. | — | `SNK-LEX-0075` |
| **ku** ⚠ | offrir | Offrir, donner en présent. | Ku jaxo do kun jaxi baanu. — « baanu Déterminant. » (`SNK-LEX-0308`) | `SNK-LEX-0171` |
| **kumu** | allumer | Allumer un feu ou une lumière. | — | `SNK-LEX-0019` |
| **kunyi** | saluer | Saluer quelqu'un, lui adresser les salutations d'usage. | — | `SNK-LEX-0105` |
| **kuyi** | rêver | Rêver, voir en rêve. | — | `SNK-LEX-0103` |
| **laaton** | éloigner | Éloigner, mettre à distance. | — | `SNK-LEX-0126` |
| **laydurangandi** | promettre | Promettre, s'engager à faire quelque chose. | — | `SNK-LEX-0174` |
| **lifi** | coudre | Coudre, assembler avec du fil. | — | `SNK-LEX-0161` |
| **maaman** | énerver | Énerver, agacer, faire perdre patience. | — | `SNK-LEX-0127` |
| **maxage** | cordonner | Cordonner, fabriquer ou réparer des chaussures. | — | `SNK-LEX-0136` |
| **maxankutondi** | raconter | Raconter, rapporter un récit, une histoire. | — | `SNK-LEX-0090` |
| **me-wutu** ⚠ | coordonner | Coordonner, agencer les parties d'un ensemble. | — | `SNK-LEX-0046` |
| **mekitandi** | relier | Relier, mettre en rapport, joindre. | — | `SNK-LEX-0094` |
| **mexindi** | salir | Salir, rendre sale. | — | `SNK-LEX-0104` |
| **mini** | boire | Boire, absorber un liquide par la bouche. | — | `SNK-LEX-0006` |
| **misso** | saboter | Saboter, faire échouer volontairement une entreprise. | — | `SNK-LEX-0137` |
| **mooso** | caresser | Caresser, passer la main doucement sur quelqu'un. | — | `SNK-LEX-0035` |
| **mugni** | impatienter | Impatienter, faire perdre patience. | — | `SNK-LEX-0142` |
| **mulondi** | froidir | Refroidir, rendre froid. | — | `SNK-LEX-0140` |
| **mungu** | oublier | Oublier, perdre le souvenir de quelque chose. | — | `SNK-LEX-0079` |
| **muru** | chercher | Chercher, s'efforcer de trouver. | — | `SNK-LEX-0039` |
| **muxu** | cacher | Cacher, dissimuler. | — | `SNK-LEX-0034` |
| **nia** | devenir | Devenir, passer d'un état à un autre. | — | `SNK-LEX-0163` |
| **niaŋundi** | transformer | Transformer, faire devenir autre. | — | `SNK-LEX-0116` |
| **noni** | tracer | Tracer, dessiner un trait, une ligne. | — | `SNK-LEX-0147` |
| **raga** | attraper | Attraper, saisir ce qui fuit. | Siidi da booren raga ti bapen ŋa. — « Sidi a attrapé une tourterelle avec un piège. » (`SNK-LEX-0212`) | `SNK-LEX-0028` |
| **rege** | danser | Danser. | — | `SNK-LEX-0054` |
| **ri** | venir | Venir, se déplacer vers celui qui parle. | N ri baasen ya kini in kaawu yi. — « Si tu fais un plat spécial pour un étranger, cela est un repas d'accueil. » (`SNK-LEX-0190`) | `SNK-LEX-0002` |
| **riti** | apporter | Apporter, amener ce qu'on porte vers un lieu. | — | `SNK-LEX-0022` |
| **rondi** | mettre | Mettre, placer quelque chose quelque part. | — | `SNK-LEX-0169` |
| **roxo** | prêter | Prêter, remettre quelque chose à quelqu'un pour un temps. | Xa da baraada roxo o yi, o wa hattaye sorene. — « Prêtez-nous une théière, nous faisons du thé. » (`SNK-LEX-0378`) | `SNK-LEX-0089` |
| **saare** | naître | Naître, venir au monde. | Daaban ga na saare, a renmen na bandon fina ya sugunu. — « Quand un animal met bas, son petit tète d'abord le premier lait. » (`SNK-LEX-0358`) | `SNK-LEX-0170` |
| **safa** | écrire | Écrire, tracer des signes d'écriture. | — | `SNK-LEX-0008` |
| **sakundi** | égarer | Égarer, perdre un objet en le laissant hors de sa place. | — | `SNK-LEX-0125` |
| **sameti** | confier | Confier, remettre à la garde de quelqu'un. | — | `SNK-LEX-0135` |
| **sane** | apparaître | Apparaître, se montrer. | — | `SNK-LEX-0153` |
| **sangalu** | clôturer | Clôturer, fermer un terrain par une clôture. | — | `SNK-LEX-0133` |
| **sanku** | disparaître | Disparaître, cesser d'être visible. | I gidanyaxaren cakkan sanku xoolen ŋa. — « Leur grande soeur a perdu son collier à la rivière. » (`SNK-LEX-0660`) | `SNK-LEX-0165` |
| **saqe** | coucher | Coucher, être étendu pour dormir. | — | `SNK-LEX-0047` |
| **sefe** | parler | Parler, s'exprimer par la parole. | — | `SNK-LEX-0004` |
| **sege** | monter | Monter, aller vers le haut. | — | `SNK-LEX-0074` |
| **si** | raser | Raser, couper le poil de près. | — | `SNK-LEX-0091` |
| **sigi** | stopper | Stopper, s'arrêter, cesser d'avancer. | Yugon sigi n’i taanun baaya. — « L'homme s'arrêta et écarta ses pieds. » (`SNK-LEX-0316`) | `SNK-LEX-0144` |
| **simandi** ⚠ | en rappeler | Rappeler quelque chose, le remettre en mémoire. | — | `SNK-LEX-0139` |
| **simme** | penser | Penser, réfléchir. | — | `SNK-LEX-0081` |
| **siyi** | coiffer | Coiffer, peigner et arranger les cheveux. | — | `SNK-LEX-0041` |
| **sonundi** | tisser | Tisser, entrecroiser des fils. | — | `SNK-LEX-0113` |
| **sooti** ⚠ | brancher | Brancher, raccorder à une installation. | — | `SNK-LEX-0031` |
| **sore** ⚠ | cuisiner | Cuisiner, faire la cuisine. | — | `SNK-LEX-0052` |
| **soxondi** | verrouiller | Verrouiller, fermer à clé. | — | `SNK-LEX-0121` |
| **soyi** | rire | Rire. | — | `SNK-LEX-0175` |
| **sugandi** | choisir | Choisir, retenir parmi plusieurs. | — | `SNK-LEX-0040` |
| **suge** | chanter | Chanter. | — | `SNK-LEX-0038` |
| **sukandi** | cocher | Cocher, marquer d'un signe une case ou un nom. | — | `SNK-LEX-0134` |
| **sumba** ⚠ | souquer | Souquer, haler sur un cordage. | — | `SNK-LEX-0143` |
| **suruba** | aspirer | Aspirer, attirer un liquide par la succion. | — | `SNK-LEX-0132` |
| **suxe** | jalouser | Jalouser, éprouver de la jalousie envers quelqu'un. | — | `SNK-LEX-0066` |
| **taga** | bâtir | Bâtir, construire un ouvrage. | — | `SNK-LEX-0033` |
| **tagandi** | créer | Créer, faire exister ce qui n'existait pas. | — | `SNK-LEX-0051` |
| **tambotuga** | rembourser | Rembourser, rendre ce qui a été emprunté. | — | `SNK-LEX-0095` |
| **tarandi** | visiter | Visiter, aller voir quelqu'un. | — | `SNK-LEX-0124` |
| **tari** | célébrer | Célébrer, fêter un événement. | — | `SNK-LEX-0053` |
| **taxu** ⚠ | asseoir | S'asseoir, prendre place. | — | `SNK-LEX-0154` |
| **tewe** ⚠ | assister | Assister à un événement, y être présent. | — | `SNK-LEX-0026` |
| **tifin** | accuser | Accuser quelqu'un, le rendre responsable. | — | `SNK-LEX-0015` |
| **tilifi** | torturer | Torturer, faire subir des sévices. | — | `SNK-LEX-0145` |
| **tinto** | approcher | Approcher, se rapprocher. | — | `SNK-LEX-0023` |
| **tu** ⚠ | connaître | Connaître, avoir la connaissance de quelqu'un ou de quelque chose. | — | `SNK-LEX-0159` |
| **tuka** | coller | Coller, faire adhérer. | — | `SNK-LEX-0042` |
| **tulu** | tresser | Tresser, entrelacer des mèches ou des fils. | — | `SNK-LEX-0149` |
| **tuma** | reposer | Se reposer, prendre du repos. | — | `SNK-LEX-0096` |
| **tuntchi** | accompagner | Accompagner quelqu'un. | — | `SNK-LEX-0014` |
| **tuyi** | informer | Informer, faire savoir. | — | `SNK-LEX-0065` |
| **tuyindi** | signaler | Signaler, indiquer, attirer l'attention sur. | — | `SNK-LEX-0108` |
| **waqi** | nettoyer | Nettoyer, ôter la saleté. | — | `SNK-LEX-0077` |
| **wara** | laisser | Laisser, ne pas emporter, ne pas empêcher. | — | `SNK-LEX-0068` |
| **waran** | lâcher | Lâcher, relâcher ce que l'on tenait. | — | `SNK-LEX-0071` |
| **wari** | trouver | Trouver, découvrir ce qu'on cherchait. | — | `SNK-LEX-0118` |
| **wori** | voir | Voir, percevoir par les yeux. | — | `SNK-LEX-0007` |
| **wu** | pleurer | Pleurer, verser des larmes. | — | `SNK-LEX-0082` |
| **wunii** | déverrouiller | Déverrouiller, ouvrir ce qui était fermé à clé. | — | `SNK-LEX-0061` |
| **wunyi** | ouvrir | Ouvrir, faire cesser la fermeture. | — | `SNK-LEX-0172` |
| **wurebandi** | traduire | Traduire, faire passer un texte d'une langue dans une autre. | — | `SNK-LEX-0182` |
| **wuru** | courir | Courir, se déplacer rapidement. | — | `SNK-LEX-0011` |
| **wutu** | prendre | Prendre, saisir, se saisir de. | — | `SNK-LEX-0009` |
| **wutundi** | porter | Porter, avoir sur soi et transporter. | — | `SNK-LEX-0085` |
| **xadiafi** | critiquer | Critiquer, juger défavorablement. | — | `SNK-LEX-0050` |
| **xandio** | convaincre | Convaincre, persuader quelqu'un. | — | `SNK-LEX-0160` |
| **xanemaxawara** | autoriser | Autoriser, donner la permission. | — | `SNK-LEX-0029` |
| **xanu** | aimer | Aimer, apprécier, tenir à quelqu'un. | — | `SNK-LEX-0018` |
| **xaru** | crier | Crier, pousser un cri. | — | `SNK-LEX-0049` |
| **xaso** ⚠ | vieillir | Vieillir, prendre de l'âge. | Xaso ga na bita, o nta fo walla wuron ŋa. — « Quand la lune diminue, nous ne voyons rien pendant la nuit. » (`SNK-LEX-0521`) | `SNK-LEX-0122` |
| **xemparadangi** | abuser | Abuser, profiter de sa position ou de la faiblesse d'autrui. | — | `SNK-LEX-0130` |
| **xenne** | violer | Violer, imposer un rapport sexuel. | — | `SNK-LEX-0123` |
| **xenni** | attaquer | Attaquer, assaillir. | — | `SNK-LEX-0027` |
| **xentie** | mesurer | Mesurer, déterminer une grandeur. | — | `SNK-LEX-0073` |
| **xenu** | tomber | Tomber, faire une chute. | Banbaado ga booxe, leminen xenu. — « Quand le pagne de dos s'est déchiré, l'enfant est tombé. » (`SNK-LEX-0343`) | `SNK-LEX-0114` |
| **xenyi** | nager | Nager. | — | `SNK-LEX-0076` |
| **xiri** | appeler | Appeler, interpeller quelqu'un. | — | `SNK-LEX-0021` |
| **xithi** | serrer | Serrer, presser fortement. | — | `SNK-LEX-0107` |
| **xoraxu** | affranchir | Affranchir, libérer de la servitude. | — | `SNK-LEX-0131` |
| **yagu** | embarrasser | Embarrasser, mettre quelqu'un dans l'embarras. | — | `SNK-LEX-0063` |
| **yampa** | pardonner | Pardonner, remettre une faute. | — | `SNK-LEX-0080` |
| **yanqa** | descendre | Descendre, aller vers le bas. | — | `SNK-LEX-0162` |
| **yaxawunyi-yen xedie** ⚠ | réveiller | Réveiller quelqu'un, le tirer du sommeil. | — | `SNK-LEX-0102` |
| **yexi** | marier | Marier, donner en mariage. | — | `SNK-LEX-0072` |
| **yige** | manger | Manger. | — | `SNK-LEX-0005` |
| **yinkutundi** | commander | Commander, ordonner. | — | `SNK-LEX-0043` |
| **yonto** | pousser | Pousser, faire aller devant soi. | — | `SNK-LEX-0086` |

## Fichiers liés

- `data/source/definitions-verbes-redigees.csv` — définitions rédigées, source de ce document
- `data/candidates/definitions-verbes-2026-10-24.csv` — mêmes données, lisibles par machine
- `scripts/enrichir_verbes_sans_doublons.py` — application sans création de ligne
- `scripts/check_doublons_lexique.py` — contrôle des doublons
- `docs/MOTS-DOCUMENT-SONINKE.md` — inventaire complet des formes du document
- `docs/LINGUISTIC-QUALITY.md` — règles d'attestation
