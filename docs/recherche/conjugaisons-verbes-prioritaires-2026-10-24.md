# Tableaux de conjugaison des verbes prioritaires — 2026-10-24

Livrable 4. Les 200 formes ci-dessous proviennent du corpus `validation_02`
de snk_engine (copie : `data/source/snk-engine-corpus-grammatical-2026-10-24.jsonl`,
CC BY 4.0), **relu ligne à ligne par le locuteur** du projet snk_engine.
L'annotation grammaticale (personne, TAM, polarité, construction) a été produite
**par règles** par `scripts/preparer_lexique_grammatical.py` à partir de la
phrase et de sa traduction, puis **revue visuellement ligne à ligne** ; elle
reste à revérifier par le référent de SoninkeGPT avant publication (les lignes
concernées portent le statut `SOURCE_VERIFIEE` pour la forme et la traduction —
corpus validé — et une note explicite sur l'annotation automatique).

## 0. Le système, en bref (à ne pas lire avec des lunettes françaises)

1. **Le radical ne change jamais** : `daga`, `yige`, `mini`… sont invariables.
   Il n'y a pas de désinences de personne : la personne est portée par le
   pronom (séries longue `nke anke ake oku xaku iku` et brève `n an a o xa i`).
2. **Le temps/aspect/mode est porté par des marqueurs prédicatifs** placés
   entre le pronom et le verbe, et par le **gérondif** (suffixes `-na/-ne/-ni/-nu/-no`
   selon la classe du verbe : `dagana`, `yigene`, `minini`…).
3. **L'accompli positif n'a pas de marqueur** (Ø) à l'intransitif
   (`A daga.` Il est parti) ; le transitif insère `di/da` après le sujet,
   avant l'objet (`A di lettra ke n'safa.` Il a écrit la lettre).
4. Le français « être + participe » ou « avoir + participe » n'a **aucun**
   équivalent morphologique : ne jamais plaquer les conjugaisons françaises.

Marqueurs relevés dans le corpus (correspondances `SNK-GRM` du lexique existant) :

| TAM | Construction | Lexique existant |
|---|---|---|
| subjonctif / demande | pronom + `na` + radical | SNK-GRM-0017 |
| inaccompli | pronom + `yi`/`wa` + gérondif | SNK-GRM-0019, 0021 |
| inaccompli habituel / progressif | pronom + `fayi` + gérondif | SNK-GRM-0014 (voir §13) |
| progressif | pronom + `do` + gérondif/nom d'action + `ni ya me` | SNK-GRM-0022, 0023 |
| futur proche | pronom + `yi rini` + radical | SNK-GRM-0016 |
| futur lointain | pronom + `(l')rini` + radical | SNK-GRM-0015 |
| futur proche négatif | pronom + `n'ti rini` / `n'taxa rini` + radical | SNK-GRM-0025, 0026 |
| accompli (passé) | pronom + radical nu (Ø) | — |
| accompli transitif | pronom + `di/da` + objet + verbe | SNK-GRM-0018, 0020 |
| passé négatif | pronom + `maxa` + radical | SNK-GRM-0024 |
| impératif singulier | (objet +) radical nu | — |
| impératif pluriel | `xa` + radical | SNK-GRM-0011 |
| défense | `maxa` + radical | SNK-GRM-0024 |

Les 11 verbes documentés ci-dessous couvrent la liste prioritaire de la mission :
**partir/aller** (daga), **venir** (ri), **manger** (yige), **boire** (mini),
**voir** (wori), **regarder** (faye), **parler/dire** (sefe ; dire = ko, voir
§12), **écrire** (safa), **travailler** (goli), **courir** (wuru),
**prendre** (wutu). Les verbes de la liste prioritaire qui n'ont pas de
paradigme complet dans le corpus (être, avoir, arriver, faire, entendre,
savoir, vouloir, pouvoir, devoir, donner, recevoir, dormir, se réveiller,
apprendre, enseigner, acheter, vendre, aimer, vivre, mourir) sont documentés
lexème par lexème dans le tableau structuré (section D) et dans
`etre-avoir-constructions-2026-10-24.md`.


## daga — « partir »

20 formes attestées (corpus validation_02).

| id corpus | forme soninké | traduction | pers. | TAM | polarité | construction |
|---|---|---|---|---|---|---|
| v-001 | `o na daga lenki` | partons aujourd'hui | 1pl | subjonctif / demande — na + radical | positif | pronom + na + radical daga |
| v-002 | `xaku n'yi dagana waxati su` | vous partez à tout moment | 2pl | inaccompli habituel — yi + gérondif | positif | pronom + yi + gérondif dagana |
| v-003 | `n do dagaye ni ya me` | je suis en train de partir | 1sg | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + dagana/dagaye + ni ya me |
| v-004 | `a fayi dagana` | il part | 3sg | inaccompli — fayi + gérondif | positif | pronom + fayi + gérondif dagana |
| v-005 | `xa wa dagana saxa` | vous partez au marché | 2pl | inaccompli — wa + gérondif | positif | pronom + wa + gérondif dagana |
| v-006 | `iku n'yi rini daga` | ils vont partir | 3pl | futur proche — yi rini + radical | positif | pronom + yi rini + radical daga |
| v-007 | `i rini daga` | ils partiront | 3pl | futur lointain — rini + radical | positif | pronom + rini + radical daga |
| v-008 | `a daga` | il est parti | 3sg | passé (accompli) — marqueur zéro | positif | pronom + radical daga nu (accompli sans marqueur) |
| v-009 | `a maxa daga` | il n'est pas parti | 3sg | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical daga |
| v-010 | `nke fayi dagana watia` | je suis en train de partir | 1sg | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif dagana |
| v-142 | `a na daga saxa` | qu'il parte au marché | 3sg | subjonctif / demande — na + radical | positif | pronom + na + radical daga |
| v-143 | `a yi dagana lenki` | il part aujourd'hui | 3sg | inaccompli — yi + gérondif | positif | pronom + yi + gérondif dagana |
| v-144 | `anke n'do dagaye ni ya me saxa` | tu es en train de partir au marché | 2sg | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + dagana/dagaye + ni ya me |
| v-145 | `xa fayi dagana koota su` | vous partez tous les jours | 2pl | inaccompli habituel — fayi + gérondif | positif | pronom + fayi + gérondif dagana |
| v-146 | `nke wa dagana` | je pars | 1sg | inaccompli — wa + gérondif | positif | pronom + wa + gérondif dagana |
| v-147 | `an yi rini daga` | tu vas partir | 2sg | futur proche — yi rini + radical | positif | pronom + yi rini + radical daga |
| v-148 | `nke rini daga saxa` | je partirai au marché | 1sg | futur lointain — rini + radical | positif | pronom + rini + radical daga |
| v-149 | `xaku n'daga lenki` | vous êtes partis aujourd'hui | 2pl | passé (accompli) — marqueur zéro | positif | pronom + radical daga nu (accompli sans marqueur) |
| v-150 | `xa maxa daga` | vous n'êtes pas partis | 2pl | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical daga |
| v-151 | `anke m'fayi dagana watia` | tu es en train de partir | 2sg | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif dagana |

## ri — « venir »

21 formes attestées (corpus validation_02).

| id corpus | forme soninké | traduction | pers. | TAM | polarité | construction |
|---|---|---|---|---|---|---|
| v-048 | `a na ri saxa` | qu'il vienne au marché | 3sg | subjonctif / demande — na + radical | positif | pronom + na + radical ri |
| v-049 | `anke n'yi rini lenki` | tu viens aujourd'hui | 2sg | inaccompli — yi + gérondif rini (venir) | positif | pronom + yi + gérondif rini |
| v-050 | `xaku n'do riye ni ya me saxa` | vous êtes en train de venir au marché | 2pl | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + rini/riye + ni ya me |
| v-051 | `anke m'fayi rini koota su` | tu viens tous les jours | 2sg | inaccompli habituel — fayi + gérondif | positif | pronom + fayi + gérondif rini |
| v-052 | `n wa rini saxa` | je viens au marché | 1sg | inaccompli — wa + gérondif | positif | pronom + wa + gérondif rini |
| v-053 | `oku yi rini saxa` | nous allons venir au marché | 1pl | futur proche ou inaccompli — forme ambiguë (rini) | positif | pronom + yi rini (gérondif de ri OU marqueur de futur proche) |
| v-054 | `n rini riya` | je viendrai | 1sg | futur lointain — rini + radical | positif | pronom + rini + radical riya |
| v-055 | `iku n'ti rini` | ils ne vont pas venir | 3pl | futur proche négatif — n'ti rini / n'taxa rini | négatif | pronom + n'ti rini + radical ri |
| v-056 | `a ri lenki` | il est venu aujourd'hui | 3sg | passé (accompli) — marqueur zéro | positif | pronom + radical ri nu (accompli sans marqueur) |
| v-057 | `o maxa ri` | nous ne sommes pas venus | 1pl | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical ri |
| v-058 | `anke m'fayi rini watia` | tu es en train de venir | 2sg | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif rini |
| v-186 | `o na ri saxa` | venons au marché | 1pl | subjonctif / demande — na + radical | positif | pronom + na + radical ri |
| v-187 | `o yi rini waxati su` | nous venons à tout moment | 1pl | inaccompli habituel — yi + gérondif rini (venir) | positif | pronom + yi + gérondif rini |
| v-188 | `xa do riye ni ya me saxa` | vous êtes en train de venir au marché | 2pl | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + rini/riye + ni ya me |
| v-189 | `xa fayi rini koota su` | vous venez tous les jours | 2pl | inaccompli habituel — fayi + gérondif | positif | pronom + fayi + gérondif rini |
| v-190 | `anke ŋ'wa rini` | tu viens | 2sg | inaccompli — wa + gérondif | positif | pronom + wa + gérondif rini |
| v-191 | `xaku n'yi rini` | vous allez venir | 2pl | futur proche ou inaccompli — forme ambiguë (rini) | positif | pronom + yi rini (gérondif de ri OU marqueur de futur proche) |
| v-192 | `ake l'rini riya saxa` | il viendra au marché | 3sg | futur lointain — l'rini + radical | positif | pronom + l'rini + radical ri |
| v-193 | `i ri` | ils sont venus | 3pl | passé (accompli) — marqueur zéro | positif | pronom + radical ri nu (accompli sans marqueur) |
| v-194 | `xa maxa ri` | vous n'êtes pas venus | 2pl | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical ri |
| v-195 | `oku fayi rini watia` | nous sommes en train de venir | 1pl | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif rini |

## yige — « manger »

19 formes attestées (corpus validation_02).

| id corpus | forme soninké | traduction | pers. | TAM | polarité | construction |
|---|---|---|---|---|---|---|
| v-123 | `i na yige lenki` | qu'ils mangent aujourd'hui | 3pl | subjonctif / demande — na + radical | positif | pronom + na + radical yige |
| v-124 | `oku na maro n'yiga lenki` | mangeons du riz aujourd'hui | 1pl | subjonctif / demande — na + radical | positif | pronom + na + radical yige |
| v-125 | `iku n'yi yigene koota su` | ils mangent tous les jours | 3pl | inaccompli habituel — yi + gérondif | positif | pronom + yi + gérondif yigene |
| v-126 | `xa do yigaye ni ya me` | vous êtes en train de manger | 2pl | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + yigene/yigaye + ni ya me |
| v-127 | `xa fayi yigene waxati su` | vous mangez à tout moment | 2pl | inaccompli habituel — fayi + gérondif | positif | pronom + fayi + gérondif yigene |
| v-128 | `ake n'yi maro yigane saxa` | il mange du riz au marché | 3sg | inaccompli — yi + gérondif | positif | pronom + yi + gérondif yigene |
| v-129 | `ake n'do maro yigaye ni ya me` | il est en train de manger du riz | 3sg | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + yigene/yigaye + ni ya me |
| v-130 | `an fayi maro ke yigane` | tu manges le riz | 2sg | inaccompli — fayi + gérondif | positif | pronom + fayi + gérondif yigene |
| v-131 | `iku ŋ'wa maro ke yigane` | ils mangent le riz | 3pl | inaccompli — wa + gérondif | positif | pronom + wa + gérondif yigene |
| v-132 | `nke wa yigene saxa` | je mange au marché | 1sg | inaccompli — wa + gérondif | positif | pronom + wa + gérondif yigene |
| v-133 | `an yi rini yige kumbene` | tu vas manger demain | 2sg | futur proche — yi rini + radical | positif | pronom + yi rini + radical yige |
| v-134 | `xaku l'rini yige saxa` | vous mangerez au marché | 2pl | futur lointain — l'rini + radical | positif | pronom + l'rini + radical yige |
| v-135 | `nke n'ti rini yige` | je ne vais pas manger | 1sg | futur proche négatif — n'ti rini / n'taxa rini | négatif | pronom + n'ti rini + radical yige |
| v-136 | `maro ke yiga` | mange le riz | 2sg | impératif singulier — (objet +) radical nu | positif | (objet +) radical yige nu |
| v-137 | `a yige` | il a mangé | 3sg | passé (accompli) — marqueur zéro | positif | pronom + radical yige nu (accompli sans marqueur) |
| v-138 | `i maxa yige` | ils n'ont pas mangé | 3pl | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical yige |
| v-139 | `an di maro n'yiga lenki` | tu as mangé du riz aujourd'hui | 2sg | passé transitif (accompli) — di/da + objet | positif | pronom + di/da + objet + (m'/n')yige(-ni) |
| v-140 | `a da maro ke n'yiga` | il a mangé le riz | 3sg | passé transitif (accompli) — di/da + objet | positif | pronom + di/da + objet + (m'/n')yige(-ni) |
| v-141 | `anke m'fayi yigene watia` | tu es en train de manger | 2sg | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif yigene |

## mini — « boire »

30 formes attestées (corpus validation_02).

| id corpus | forme soninké | traduction | pers. | TAM | polarité | construction |
|---|---|---|---|---|---|---|
| v-032 | `o na mini` | buvons | 1pl | subjonctif / demande — na + radical | positif | pronom + na + radical mini |
| v-033 | `o na xati ke m'mini lenki` | buvons le lait aujourd'hui | 1pl | subjonctif / demande — na + radical | positif | pronom + na + radical mini |
| v-034 | `anke n'yi minini saxa` | tu bois au marché | 2sg | inaccompli — yi + gérondif | positif | pronom + yi + gérondif minini |
| v-035 | `xa do mine ni ya me` | vous êtes en train de boire | 2pl | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + minini/mine + ni ya me |
| v-036 | `anke m'fayi minini waxati su` | tu bois à tout moment | 2sg | inaccompli habituel — fayi + gérondif | positif | pronom + fayi + gérondif minini |
| v-037 | `anke n'do xati ke mine ni ya me` | tu es en train de boire le lait | 2sg | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + minini/mine + ni ya me |
| v-038 | `xa wa minini` | vous buvez | 2pl | inaccompli — wa + gérondif | positif | pronom + wa + gérondif minini |
| v-039 | `oku yi rini mini` | nous allons boire | 1pl | futur proche — yi rini + radical | positif | pronom + yi rini + radical mini |
| v-040 | `ake l'rini mini` | il boira | 3sg | futur lointain — l'rini + radical | positif | pronom + l'rini + radical mini |
| v-041 | `nke n'ti rini mini` | je ne vais pas boire | 1sg | futur proche négatif — n'ti rini / n'taxa rini | négatif | pronom + n'ti rini + radical mini |
| v-042 | `xati mini` | bois du lait | 2sg | impératif singulier — (objet +) radical nu | positif | (objet +) radical mini nu |
| v-043 | `iku m'mini daru` | ils ont bu hier | 3pl | passé (accompli) — particule m' + radical | positif | pronom + m' + radical mini (assimilation SNK-GRM-0028) |
| v-044 | `a maxa mini` | il n'a pas bu | 3sg | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical mini |
| v-045 | `oku di xati ke m'mini` | nous avons bu le lait | 1pl | passé transitif (accompli) — di/da + objet | positif | pronom + di/da + objet + (m'/n')mini(-ni) |
| v-046 | `ake n'da xati m'mini saxa` | il a bu du lait au marché | 3sg | passé transitif (accompli) — di/da + objet | positif | pronom + di/da + objet + (m'/n')mini(-ni) |
| v-047 | `oku fayi minini watia` | nous sommes en train de boire | 1pl | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif minini |
| v-172 | `an na mini lenki` | bois aujourd'hui | 2sg | subjonctif / demande — na + radical | positif | pronom + na + radical mini |
| v-173 | `n na xati ke m'mini saxa` | que je boive le lait au marché | 1sg | subjonctif / demande — na + radical | positif | pronom + na + radical mini |
| v-174 | `nke yi minini waxati su` | je bois à tout moment | 1sg | inaccompli habituel — yi + gérondif | positif | pronom + yi + gérondif minini |
| v-175 | `a do mine ni ya me saxa` | il est en train de boire au marché | 3sg | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + minini/mine + ni ya me |
| v-176 | `iku m'fayi minini saxa` | ils boivent au marché | 3pl | inaccompli — fayi + gérondif | positif | pronom + fayi + gérondif minini |
| v-177 | `nke do xati ke mine ni ya me saxa` | je suis en train de boire le lait au marché | 1sg | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + minini/mine + ni ya me |
| v-178 | `n wa minini` | je bois | 1sg | inaccompli — wa + gérondif | positif | pronom + wa + gérondif minini |
| v-179 | `n yi rini mini saxa` | je vais boire au marché | 1sg | futur proche — yi rini + radical | positif | pronom + yi rini + radical mini |
| v-180 | `anke l'rini mini` | tu boiras | 2sg | futur lointain — l'rini + radical | positif | pronom + l'rini + radical mini |
| v-181 | `xaku m'mini` | vous avez bu | 2pl | passé (accompli) — particule m' + radical | positif | pronom + m' + radical mini (assimilation SNK-GRM-0028) |
| v-182 | `nke maxa mini` | je n'ai pas bu | 1sg | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical mini |
| v-183 | `xa di xati ke m'mini lenki` | vous avez bu le lait aujourd'hui | 2pl | passé transitif (accompli) — di/da + objet | positif | pronom + di/da + objet + (m'/n')mini(-ni) |
| v-184 | `a da xati m'mini` | il a bu du lait | 3sg | passé transitif (accompli) — di/da + objet | positif | pronom + di/da + objet + (m'/n')mini(-ni) |
| v-185 | `ake m'fayi minini watia` | il est en train de boire | 3sg | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif minini |

## wori — « voir »

16 formes attestées (corpus validation_02).

| id corpus | forme soninké | traduction | pers. | TAM | polarité | construction |
|---|---|---|---|---|---|---|
| v-089 | `i na wori lenki` | qu'ils voient aujourd'hui | 3pl | subjonctif / demande — na + radical | positif | pronom + na + radical wori |
| v-090 | `a na maro ke ŋ'wori` | qu'il voie le riz | 3sg | subjonctif / demande — na + radical | positif | pronom + na + radical wori |
| v-091 | `n yi worini` | je vois | 1sg | inaccompli — yi + gérondif | positif | pronom + yi + gérondif worini |
| v-092 | `oku do woriye ni ya me saxa` | nous sommes en train de voir au marché | 1pl | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + worini/woriye + ni ya me |
| v-093 | `xa fayi worini` | vous voyez | 2pl | inaccompli — fayi + gérondif | positif | pronom + fayi + gérondif worini |
| v-094 | `n do maro ke woriye ni ya me saxa` | je suis en train de voir le riz au marché | 1sg | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + worini/woriye + ni ya me |
| v-095 | `i wa worini saxa` | ils voient au marché | 3pl | inaccompli — wa + gérondif | positif | pronom + wa + gérondif worini |
| v-096 | `oku yi rini wori kumbene` | nous allons voir demain | 1pl | futur proche — yi rini + radical | positif | pronom + yi rini + radical wori |
| v-097 | `o rini wori` | nous verrons | 1pl | futur lointain — rini + radical | positif | pronom + rini + radical wori |
| v-098 | `nke n'ti rini wori` | je ne vais pas voir | 1sg | futur proche négatif — n'ti rini / n'taxa rini | négatif | pronom + n'ti rini + radical wori |
| v-099 | `lemine ke wori` | vois l'enfant | 2sg | impératif singulier — (objet +) radical nu | positif | (objet +) radical wori nu |
| v-100 | `ake ŋ'wori saxa` | il a vu au marché | 3sg | passé (accompli) — marqueur zéro | positif | pronom + radical wori nu (accompli sans marqueur) |
| v-101 | `oku maxa wori` | nous n'avons pas vu | 1pl | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical wori |
| v-102 | `ake n'di lettra ke ŋ'wori daru` | il a vu la lettre hier | 3sg | passé transitif (accompli) — di/da + objet | positif | pronom + di/da + objet + (m'/n')wori(-ni) |
| v-103 | `xa da lettra ŋ'wori saxa` | vous avez vu une lettre au marché | 2pl | passé transitif (accompli) — di/da + objet | positif | pronom + di/da + objet + (m'/n')wori(-ni) |
| v-104 | `ake m'fayi worini watia` | il est en train de voir | 3sg | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif worini |

## faye — « regarder »

20 formes attestées (corpus validation_02).

| id corpus | forme soninké | traduction | pers. | TAM | polarité | construction |
|---|---|---|---|---|---|---|
| v-011 | `nke na faye saxa` | que je regarde au marché | 1sg | subjonctif / demande — na + radical | positif | pronom + na + radical faye |
| v-012 | `o yi fayeni` | nous regardons | 1pl | inaccompli — yi + gérondif | positif | pronom + yi + gérondif fayeni |
| v-013 | `ake n'do fayinde ni ya me` | il est en train de regarder | 3sg | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + fayeni/fayinde + ni ya me |
| v-014 | `o fayi fayeni` | nous regardons | 1pl | inaccompli — fayi + gérondif | positif | pronom + fayi + gérondif fayeni |
| v-015 | `nke wa fayeni` | je regarde | 1sg | inaccompli — wa + gérondif | positif | pronom + wa + gérondif fayeni |
| v-016 | `o yi rini faye` | nous allons regarder | 1pl | futur proche — yi rini + radical | positif | pronom + yi rini + radical faye |
| v-017 | `xaku l'rini faye` | vous regarderez | 2pl | futur lointain — l'rini + radical | positif | pronom + l'rini + radical faye |
| v-018 | `n faye` | j'ai regardé | 1sg | passé (accompli) — marqueur zéro | positif | pronom + radical faye nu (accompli sans marqueur) |
| v-019 | `oku maxa faye` | nous n'avons pas regardé | 1pl | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical faye |
| v-020 | `anke m'fayi fayeni watia` | tu es en train de regarder | 2sg | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif fayeni |
| v-152 | `oku na faye` | regardons | 1pl | subjonctif / demande — na + radical | positif | pronom + na + radical faye |
| v-153 | `n yi fayeni saxa` | je regarde au marché | 1sg | inaccompli — yi + gérondif | positif | pronom + yi + gérondif fayeni |
| v-154 | `a do fayinde ni ya me` | il est en train de regarder | 3sg | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + fayeni/fayinde + ni ya me |
| v-155 | `a fayi fayeni waxati su` | il regarde à tout moment | 3sg | inaccompli habituel — fayi + gérondif | positif | pronom + fayi + gérondif fayeni |
| v-156 | `iku ŋ'wa fayeni` | ils regardent | 3pl | inaccompli — wa + gérondif | positif | pronom + wa + gérondif fayeni |
| v-157 | `nke yi rini faye` | je vais regarder | 1sg | futur proche — yi rini + radical | positif | pronom + yi rini + radical faye |
| v-158 | `nke rini faye saxa` | je regarderai au marché | 1sg | futur lointain — rini + radical | positif | pronom + rini + radical faye |
| v-159 | `i faye lenki` | ils ont regardé aujourd'hui | 3pl | passé (accompli) — marqueur zéro | positif | pronom + radical faye nu (accompli sans marqueur) |
| v-160 | `n maxa faye` | je n'ai pas regardé | 1sg | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical faye |
| v-161 | `oku fayi fayeni watia` | nous sommes en train de regarder | 1pl | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif fayeni |

## sefe — « parler »

11 formes attestées (corpus validation_02).

| id corpus | forme soninké | traduction | pers. | TAM | polarité | construction |
|---|---|---|---|---|---|---|
| v-078 | `n na sefe lenki` | que je parle aujourd'hui | 1sg | subjonctif / demande — na + radical | positif | pronom + na + radical sefe |
| v-079 | `n yi sefene waxati su` | je parle à tout moment | 1sg | inaccompli habituel — yi + gérondif | positif | pronom + yi + gérondif sefene |
| v-080 | `a do sefeye ni ya me saxa` | il est en train de parler au marché | 3sg | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + sefene/sefeye + ni ya me |
| v-081 | `nke fayi sefene waxati su` | je parle à tout moment | 1sg | inaccompli habituel — fayi + gérondif | positif | pronom + fayi + gérondif sefene |
| v-082 | `ake ŋ'wa sefene saxa` | il parle au marché | 3sg | inaccompli — wa + gérondif | positif | pronom + wa + gérondif sefene |
| v-083 | `n yi rini sefe saxa` | je vais parler au marché | 1sg | futur proche — yi rini + radical | positif | pronom + yi rini + radical sefe |
| v-084 | `an rini sefe saxa` | tu parleras au marché | 2sg | futur lointain — rini + radical | positif | pronom + rini + radical sefe |
| v-085 | `anke n'ti rini sefe` | tu ne vas pas parler | 2sg | futur proche négatif — n'ti rini / n'taxa rini | négatif | pronom + n'ti rini + radical sefe |
| v-086 | `n sefe saxa` | j'ai parlé au marché | 1sg | passé (accompli) — marqueur zéro | positif | pronom + radical sefe nu (accompli sans marqueur) |
| v-087 | `n maxa sefe` | je n'ai pas parlé | 1sg | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical sefe |
| v-088 | `anke m'fayi sefene watia` | tu es en train de parler | 2sg | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif sefene |

## safa — « écrire »

24 formes attestées (corpus validation_02).

| id corpus | forme soninké | traduction | pers. | TAM | polarité | construction |
|---|---|---|---|---|---|---|
| v-059 | `i na safa saxa` | qu'ils écrivent au marché | 3pl | subjonctif / demande — na + radical | positif | pronom + na + radical safa |
| v-060 | `a na lettra n'safa` | qu'il écrive une lettre | 3sg | subjonctif / demande — na + radical | positif | pronom + na + radical safa |
| v-061 | `a yi safana` | il écrit | 3sg | inaccompli — yi + gérondif | positif | pronom + yi + gérondif safana |
| v-062 | `iku n'do safande ni ya me saxa` | ils sont en train de écrire au marché | 3pl | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + safana/safande + ni ya me |
| v-063 | `ake m'fayi safana waxati su` | il écrit à tout moment | 3sg | inaccompli habituel — fayi + gérondif | positif | pronom + fayi + gérondif safana |
| v-064 | `i yi lettra safana saxa` | ils écrivent une lettre au marché | 3pl | inaccompli — yi + gérondif | positif | pronom + yi + gérondif safana |
| v-065 | `iku n'do lettra safande ni ya me` | ils sont en train de écrire une lettre | 3pl | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + safana/safande + ni ya me |
| v-066 | `o fayi lettra safana` | nous écrivons une lettre | 1pl | inaccompli — fayi + gérondif | positif | pronom + fayi + gérondif safana |
| v-067 | `n wa lettra safana` | j'écris une lettre | 1sg | inaccompli — wa + gérondif | positif | pronom + wa + gérondif safana |
| v-068 | `ake ŋ'wa safana saxa` | il écrit au marché | 3sg | inaccompli — wa + gérondif | positif | pronom + wa + gérondif safana |
| v-069 | `iku n'yi rini safa saxa` | ils vont écrire au marché | 3pl | futur proche — yi rini + radical | positif | pronom + yi rini + radical safa |
| v-070 | `xa rini safa saxa` | vous écrirez au marché | 2pl | futur lointain — rini + radical | positif | pronom + rini + radical safa |
| v-071 | `anke n'ti rini safa` | tu ne vas pas écrire | 2sg | futur proche négatif — n'ti rini / n'taxa rini | négatif | pronom + n'ti rini + radical safa |
| v-072 | `lettra safa` | écris une lettre | 2sg | impératif singulier — (objet +) radical nu | positif | (objet +) radical safa nu |
| v-073 | `i safa saxa` | ils ont écrit au marché | 3pl | passé (accompli) — marqueur zéro | positif | pronom + radical safa nu (accompli sans marqueur) |
| v-074 | `o maxa safa` | nous n'avons pas écrit | 1pl | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical safa |
| v-075 | `a di lettra ke n'safa lenki` | il a écrit la lettre aujourd'hui | 3sg | passé transitif (accompli) — di/da + objet | positif | pronom + di/da + objet + (m'/n')safa(-ni) |
| v-076 | `ake n'da lettra ke n'safa saxa` | il a écrit la lettre au marché | 3sg | passé transitif (accompli) — di/da + objet | positif | pronom + di/da + objet + (m'/n')safa(-ni) |
| v-077 | `ake m'fayi safana watia` | il est en train de écrire | 3sg | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif safana |
| v-196 | `n na safa lenki` | que je écrive aujourd'hui | 1sg | subjonctif / demande — na + radical | positif | pronom + na + radical safa |
| v-197 | `oku na lettra ke n'safa lenki` | écrivons la lettre aujourd'hui | 1pl | subjonctif / demande — na + radical | positif | pronom + na + radical safa |
| v-198 | `anke n'yi safana koota su` | tu écris tous les jours | 2sg | inaccompli habituel — yi + gérondif | positif | pronom + yi + gérondif safana |
| v-199 | `an do safande ni ya me` | tu es en train de écrire | 2sg | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + safana/safande + ni ya me |
| v-200 | `oku fayi safana saxa` | nous écrivons au marché | 1pl | inaccompli — fayi + gérondif | positif | pronom + fayi + gérondif safana |

## goli — « travailler »

21 formes attestées (corpus validation_02).

| id corpus | forme soninké | traduction | pers. | TAM | polarité | construction |
|---|---|---|---|---|---|---|
| v-021 | `o na goli` | travaillons | 1pl | subjonctif / demande — na + radical | positif | pronom + na + radical goli |
| v-022 | `n yi golini koota su` | je travaille tous les jours | 1sg | inaccompli habituel — yi + gérondif | positif | pronom + yi + gérondif golini |
| v-023 | `xaku n'do goliye ni ya me` | vous êtes en train de travailler | 2pl | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + golini/goliye + ni ya me |
| v-024 | `an fayi golini koota su` | tu travailles tous les jours | 2sg | inaccompli habituel — fayi + gérondif | positif | pronom + fayi + gérondif golini |
| v-025 | `a wa golini saxa` | il travaille au marché | 3sg | inaccompli — wa + gérondif | positif | pronom + wa + gérondif golini |
| v-026 | `an yi rini goli kumbene` | tu vas travailler demain | 2sg | futur proche — yi rini + radical | positif | pronom + yi rini + radical goli |
| v-027 | `n rini goli saxa` | je travaillerai au marché | 1sg | futur lointain — rini + radical | positif | pronom + rini + radical goli |
| v-028 | `nke n'ti rini goli` | je ne vais pas travailler | 1sg | futur proche négatif — n'ti rini / n'taxa rini | négatif | pronom + n'ti rini + radical goli |
| v-029 | `an goli saxa` | tu as travaillé au marché | 2sg | passé (accompli) — marqueur zéro | positif | pronom + radical goli nu (accompli sans marqueur) |
| v-030 | `iku maxa goli` | ils n'ont pas travaillé | 3pl | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical goli |
| v-031 | `nke fayi golini watia` | je suis en train de travailler | 1sg | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif golini |
| v-162 | `oku na goli lenki` | travaillons aujourd'hui | 1pl | subjonctif / demande — na + radical | positif | pronom + na + radical goli |
| v-163 | `anke n'yi golini lenki` | tu travailles aujourd'hui | 2sg | inaccompli — yi + gérondif | positif | pronom + yi + gérondif golini |
| v-164 | `nke do goliye ni ya me` | je suis en train de travailler | 1sg | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + golini/goliye + ni ya me |
| v-165 | `xaku m'fayi golini koota su` | vous travaillez tous les jours | 2pl | inaccompli habituel — fayi + gérondif | positif | pronom + fayi + gérondif golini |
| v-166 | `oku wa golini saxa` | nous travaillons au marché | 1pl | inaccompli — wa + gérondif | positif | pronom + wa + gérondif golini |
| v-167 | `an yi rini goli` | tu vas travailler | 2sg | futur proche — yi rini + radical | positif | pronom + yi rini + radical goli |
| v-168 | `a rini goli` | il travaillera | 3sg | futur lointain — rini + radical | positif | pronom + rini + radical goli |
| v-169 | `a goli saxa` | il a travaillé au marché | 3sg | passé (accompli) — marqueur zéro | positif | pronom + radical goli nu (accompli sans marqueur) |
| v-170 | `i maxa goli` | ils n'ont pas travaillé | 3pl | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical goli |
| v-171 | `ake m'fayi golini watia` | il est en train de travailler | 3sg | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif golini |

## wuru — « courir »

11 formes attestées (corpus validation_02).

| id corpus | forme soninké | traduction | pers. | TAM | polarité | construction |
|---|---|---|---|---|---|---|
| v-105 | `oku na wuru lenki` | courons aujourd'hui | 1pl | subjonctif / demande — na + radical | positif | pronom + na + radical wuru |
| v-106 | `xaku n'yi wurunu` | vous courez | 2pl | inaccompli — yi + gérondif | positif | pronom + yi + gérondif wurunu |
| v-107 | `xaku n'do wuruye ni ya me saxa` | vous êtes en train de courir au marché | 2pl | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + wurunu/wuruye + ni ya me |
| v-108 | `xa fayi wurunu` | vous courez | 2pl | inaccompli — fayi + gérondif | positif | pronom + fayi + gérondif wurunu |
| v-109 | `xa wa wurunu saxa` | vous courez au marché | 2pl | inaccompli — wa + gérondif | positif | pronom + wa + gérondif wurunu |
| v-110 | `xa yi rini wuru saxa` | vous allez courir au marché | 2pl | futur proche — yi rini + radical | positif | pronom + yi rini + radical wuru |
| v-111 | `an rini wuru saxa` | tu courras au marché | 2sg | futur lointain — rini + radical | positif | pronom + rini + radical wuru |
| v-112 | `nke n'ti rini wuru` | je ne vais pas courir | 1sg | futur proche négatif — n'ti rini / n'taxa rini | négatif | pronom + n'ti rini + radical wuru |
| v-113 | `ake ŋ'wuru daru` | il a couru hier | 3sg | passé (accompli) — marqueur zéro | positif | pronom + radical wuru nu (accompli sans marqueur) |
| v-114 | `n maxa wuru` | je n'ai pas couru | 1sg | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical wuru |
| v-115 | `anke m'fayi wurunu watia` | tu es en train de courir | 2sg | inaccompli progressif — fayi + gérondif | positif | pronom + fayi + gérondif wurunu |

## wutu — « prendre »

7 formes attestées (corpus validation_02).

| id corpus | forme soninké | traduction | pers. | TAM | polarité | construction |
|---|---|---|---|---|---|---|
| v-116 | `oku na wutu lenki` | prenons aujourd'hui | 1pl | subjonctif / demande — na + radical | positif | pronom + na + radical wutu |
| v-117 | `oku do wutunde ni ya me` | nous sommes en train de prendre | 1pl | progressif — do + gérondif/nom d'action + ni ya me | positif | pronom + do + wutu/wutunde + ni ya me |
| v-118 | `iku n'yi rini wutu saxa` | ils vont prendre au marché | 3pl | futur proche — yi rini + radical | positif | pronom + yi rini + radical wutu |
| v-119 | `xa rini wutu` | vous prendrez | 2pl | futur lointain — rini + radical | positif | pronom + rini + radical wutu |
| v-120 | `nke n'ti rini wutu` | je ne vais pas prendre | 1sg | futur proche négatif — n'ti rini / n'taxa rini | négatif | pronom + n'ti rini + radical wutu |
| v-121 | `o wutu lenki` | nous avons pris aujourd'hui | 1pl | passé (accompli) — marqueur zéro | positif | pronom + radical wutu nu (accompli sans marqueur) |
| v-122 | `oku maxa wutu` | nous n'avons pas pris | 1pl | passé négatif — pronom + maxa + radical | négatif | pronom + maxa + radical wutu |

## 12. Verbes prioritaires sans paradigme complet dans le corpus

Pour chaque verbe de la liste de la mission, le tableau structuré
(section D) documente : forme de référence, gérondif/nom d'action (YAML
référent), variantes, sources, exemples et contradictions. Synthèse :

| Français | Soninké | Statut | Remarque |
|---|---|---|---|
| être | ni / feti, wa / nta, yi / n'ti, nàn / ntá | voir livrable 3 | pas de verbe unique |
| avoir | constructions locatives (wa…yi, yani maxa) | voir livrable 3 | pas de verbe |
| aller | daga (partir) ; composés `Daga iige/sohu/goli` | SOURCE_VERIFIEE | pas de verbe « aller » générique vérifié |
| venir | ri | SOURCE_VERIFIEE | Grégoire 1979 glose « arriver » — divergence conservée |
| partir | daga | SOURCE_VERIFIEE | paradigme complet §1 |
| arriver | dioofe | SOURCE_VERIFIEE | pas d'exemple complet dans le corpus consulté |
| faire | — | lacune | aucun verbe générique vérifié ; causatif -ndi (bagu→bagandi) |
| dire | ko (gérondif kono) | SOURCE_VERIFIEE | homonymie ko « qui » documentée |
| voir | wori | SOURCE_VERIFIEE | paradigme complet §5 |
| entendre | mugu | A_CONFIRMER | quasi-homonyme mungu « oublier » ; pas d'exemple |
| savoir | tu (connaître) | SOURCE_VERIFIEE | savoir/connaître non distingués |
| vouloir | mula (+ na + verbe) | SOURCE_VERIFIEE | `O ni mula na xobo maro.` Nous voulons acheter du riz |
| pouvoir | kitta (SIL) ; ra (glossaire) | A_CONFIRMER | non attesté dans le corpus du projet |
| devoir | xawa / qawa ; qáwà, sìrì (Kingi) | A_CONFIRMER | `nke na n'xawa maro` je dois (du) riz |
| donner | kini | SOURCE_VERIFIEE | `Dji kini nke.` Donne-moi l'eau |
| recevoir | kita | A_CONFIRMER | `O wa biradi n'kitana siné ké muma.` (texte_pluies) |
| prendre | wutu | SOURCE_VERIFIEE | paradigme complet §11 ; gérondif absent du YAML (lacune) |
| manger | yige | SOURCE_VERIFIEE | paradigme complet §3 ; variante iige (SNK-LEX-1340) |
| boire | mini | SOURCE_VERIFIEE | paradigme complet §4 |
| dormir | xenxe (corpus) / qenqe (lexique externe) | VARIANTE_DOCUMENTEE | les deux graphies conservées |
| se réveiller | giri « se lever » | SOURCE_VERIFIEE | verbe propre « se réveiller » à demander (SNK-LEX-0102 = transitif) |
| travailler | goli | SOURCE_VERIFIEE | paradigme complet §9 |
| apprendre | xara (lire) ; bire (LGIDF) ? | SOURCE_VERIFIEE / à vérifier | apprendre/lire confondus dans les sources |
| enseigner | xaranŋundi | A_CONFIRMER | dérivé causatif de xara |
| acheter | xobo | SOURCE_VERIFIEE | pas de paradigme complet, exemples multiples |
| vendre | gage | SOURCE_VERIFIEE | pas d'exemple complet relevé |
| aimer | xanu (Kingui : kanu) | SOURCE_VERIFIEE | variante régionale à vérifier |
| vivre | bire | SOURCE_VERIFIEE | polysémie vivre/instant documentée par le référent |
| mourir | kara (kàrá, ton bas — LGIDF/Grégoire) | CONTRADICTOIRE | le référent donne kara « casser » (ton haut) ; les deux conservés |

## 13. Ambiguïtés et divergences relevées dans les 200 formes

1. **`rini`** : gérondif de `ri` « venir » ET marqueur de futur lointain/proche.
   `xaku n'yi rini` est traduit « vous allez venir » (v-191) alors que
   `o yi rini waxati su` est traduit « nous venons à tout moment » (v-187) :
   la même séquence `yi rini` reçoit les deux analyses. Les deux lectures sont
   conservées sur les lignes concernées (statut `A_CONFIRMER_PAR_LOCUTEUR`).
2. **`fayi`** : annoté « Progressive » dans serie_02 mais traduit comme un
   habituel dans validation_02 (« tu travailles tous les jours », v-024) ou un
   présent simple (« il part », v-004). Creissels rapproche `háyí` (Kingi) du
   gérondif progressif. Les trois lectures sont documentées ; les lignes sans
   adverbe de temps portent `moyen`.
3. **`m'` + radical** (`iku m'mini daru` ils ont bu hier, v-043) : accompli à
   particule à côté de l'accompli Ø ; répartition non élucidée.
4. **`na`** : traduit tantôt par un impératif pluriel hortatif (« partons »,
   v-001), tantôt par un subjonctif (« qu'il vienne », v-048), tantôt par une
   demande (« bois aujourd'hui », v-172). Un seul marqueur, plusieurs valeurs
   pragmatiques — conforme à `SNK-GRM-0017` (« demande / qu'il »).
5. **Objet antéposé à l'impératif** : `xati mini` (bois du lait),
   `maro ke yiga` (mange le riz) — l'objet précède le radical nu, comme dans
   les autres temps (ordre SOV).
6. **Graphies du corpus** : les textes libres (texte_journee…) emploient une
   orthographe d'origine non normalisée (`yigué`, `safandi`, `xénxé`, `guiri`) ;
   les 200 formes de validation_02 sont en orthographe « projet » et ont été
   utilisées seules pour les tableaux.

## 14. Impératifs et défense (rappel des formes attestées)

| Forme | Sens | Source |
|---|---|---|
| `Maro ke wori !` | Vois le riz ! | v-125 |
| `Xati mini !` | Bois du lait ! | v-042 |
| `Lettra safa !` | Écris une lettre ! | v-072 |
| `Xa daga !` / `Xa goli !` | Partez ! / Travaillez ! | v-012 / v-040 |
| `Maxa daga !` / `Maxa faye !` | Ne pars pas ! / Ne regarde pas ! | v-011 / v-025 |
| `Yeli !` / `Yere !` | Viens ici ! | SNK-GRM-0027 (référent) |
