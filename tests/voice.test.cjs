const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync('app.js', 'utf8');
assert(!/speechSynthesis|SpeechSynthesisUtterance|speakUtterance/.test(source));
const sandbox = {
  console,
  document: { querySelector: () => null, querySelectorAll: () => [] },
  window: {},
  localStorage: { getItem: () => null, setItem: () => {} },
  fetch: async (url) => {
    try {
      const txt = fs.readFileSync(url, 'utf8');
      return { ok: true, text: async () => txt, json: async () => JSON.parse(txt) };
    } catch {
      return { ok: false, text: async () => '' };
    }
  },
};
vm.createContext(sandbox);
vm.runInContext(source.replace(/init\(\);\s*$/, ''), sandbox);
vm.runInContext(`
state.audioByWord.set(normalizeWord('daga'), {url:'audio/daga.wav'});
state.audioByWord.set(normalizeWord('goli'), {url:'audio/goli.wav'});
`, sandbox);
const evaluate = text => vm.runInContext(text, sandbox);
assert.equal(evaluate("buildSoninkePhraseSegments('daga goli').length"), 2);
assert.equal(evaluate("buildSoninkePhraseSegments('daga inconnu').length"), 0);
assert.equal(evaluate("buildSoninkePhraseSegments('').length"), 0);
assert.equal(evaluate("buildAvailableAudioSegments('daga inconnu goli').length"), 2,
  'Les segments audio disponibles doivent être récupérés même si un mot manque');
assert.equal(evaluate("buildAvailableAudioSegments('daga inconnu daga').length"), 2,
  'La lecture partielle doit conserver les répétitions et leur ordre');
assert.equal(evaluate("renderSoninkePair('daga inconnu goli', 'phrase indicative', 'phrase').includes('Écouter les segments')"), true,
  'Une phrase composée avec des audios partiels doit proposer leur lecture');
assert.equal(evaluate("explainFrench('**Xa wouy Diom**').includes('bonjour')"), true);
assert.equal(evaluate("soninkeForms('**Titre inconnu**').length"), 0);

(async () => {
  await evaluate('loadAllData()');
  const entries = evaluate('state.entries');
  assert(evaluate('state.audioList.length') > 1000,
    `La mémoire audio restaurée doit être indexée, obtenu : ${evaluate('state.audioList.length')} audios`);
  const corpusContext = evaluate("buildLocalCorpusContext('Traduis « tu as mangé le riz » en soninké')");
  assert(/PHRASE\/EXEMPLE ATTESTÉ|PHRASEBOOK/.test(corpusContext.context),
    'La recherche corpus-first doit inclure les phrases ou exemples pertinents');
  assert(/AUDIO LIÉ À UNE FORME/.test(corpusContext.context),
    'La recherche corpus-first doit inclure les audios associés aux formes retrouvées');
  assert(entries.length > 1300, `Expected >1300 lexicon entries, got ${entries.length}`);
  const seenIds = new Set();
  const seenWords = new Map();
  let validatedHomonymEntries = 0;
  const isValidatedHomonym = e => /Arbitrage d’homonymes validé par le référent linguistique/.test(e.source || "");
  for (const e of entries) {
    assert(e.soninke && e.francais, `Incomplete entry: ${JSON.stringify(e)}`);
    assert(!seenIds.has(e.id), `Duplicate lexicon ID: ${e.id}`);
    seenIds.add(e.id);
    if (isValidatedHomonym(e)) validatedHomonymEntries++;
    const key = evaluate(`normalizeLexicalKey(${JSON.stringify(e.soninke)})`);
    const previous = seenWords.get(key) || [];
    if (previous.length) {
      assert(isValidatedHomonym(e) || previous.every(isValidatedHomonym),
        `Unexpected duplicate Soninke headword outside approved homonym groups: ${e.soninke} (${key})`);
    }
    previous.push(e);
    seenWords.set(key, previous);
  }
  assert.equal(validatedHomonymEntries, 380, `Expected all 380 entries from the 169 validated homonym groups, got ${validatedHomonymEntries}`);
  // Pronoms personnels validés explicitement par le référent linguistique.
  const expectedPronouns = { In: "je", An: "tu", A: "il / elle", O: "nous", I: "vous", Iku: "ils / elles" };
  for (const [form, french] of Object.entries(expectedPronouns)) {
    const key = evaluate(`normalizeLexicalKey(${JSON.stringify(form)})`);
    const entry = entries.find(e => evaluate(`normalizeLexicalKey(${JSON.stringify(e.soninke)})`) === key);
    assert(entry, `Missing validated personal pronoun: ${form}`);
    assert.equal(entry.francais, french, `Wrong validated French gloss for ${form}`);
    assert.equal(entry.categorie, "pronom_personnel");
    assert.equal(entry.statut, "valide_par_referent_linguistique");
  }
  assert.equal(evaluate("findAudioInfo('i').francais"), "vous",
    "La glose audio de I doit suivre la validation du référent");
  assert.equal(evaluate("findAudioInfo('iku').francais"), "ils / elles",
    "La glose audio de Iku doit rester ils / elles");

  // Liste lexicale validée après comparaison des 113 formes fournies avec le lexique de base.
  const expectedValidatedList = {
    "Ala": "Allah, Dieu",
    "Anmiina": "Amen",
    "Annebi": "Le prophète Mahomet",
    "Araba": "Mercredi",
    "Arijanna": "Paradis",
    "Ayiwa !": "D'accord !",
    "Buki": "Livre, bouquin",
    "Daqqu": "Soif",
    "Due": "Accepter",
    "Faccari": "Traduire",
    "Haqqile": "Intelligence, conscience",
    "Hattaye": "Thé vert",
    "Kaaduuro": "Zéro",
    "Menjanne": "Ami",
    "Ñaaye": "Prince",
    "Ñiine": "Terre, sol",
    "Orege": "Thé",
    "Sare": "Être humain",
    "Talaata": "Mardi",
    "Tenenne": "Lundi",
    "Tonnu": "Vérité",
    "Wallahi": "Au nom de Dieu",
    "Welo": "Bicyclette",
    "Woto": "Automobile",
    "Xaranmoxo": "Professeur",
    "Xatti": "Lait",
    "Xoso": "Mois, lune",
    "Alikeebu": "Étrier",
    "Alimaami": "Imam ; Alimamy (prénom masculin)",
    "Aliyatiime": "Orphelin",
    "Anniye": "Souhait",
  };
  for (const [form, french] of Object.entries(expectedValidatedList)) {
    const key = evaluate(`normalizeLexicalKey(${JSON.stringify(form)})`);
    const matches = entries.filter(e => evaluate(`normalizeLexicalKey(${JSON.stringify(e.soninke)})`) === key && e.francais === french);
    assert(matches.length >= 1, `Missing validated lexical entry: ${form} → ${french}`);
    assert(matches.some(e => e.statut === "valide_par_referent_linguistique" || /valide_par_referent_linguistique/.test(e.statut || "")),
      `Entry not marked as validated: ${form}`);
  }
  // Traductions des 17 formes audio : variantes reliées au lemme canonique, sans doublon.
  const expectedAudioTranslations = {
    "Beniyaamina": ["Benjamin", "valide_par_referent_linguistique"],
    "burugutu": ["Passer à la flamme (une tête de mouton ou de poulet)", "valide_par_referent_linguistique"],
    "burunqu": ["Destruction, effacement", "valide_par_referent_linguistique"],
    "buya": ["Brûler, griller", "valide_par_referent_linguistique"],
    "bunanbuna": ["Guêpe qui fait des nids en banco aux murs", "valide_par_referent_linguistique"],
    "buruxu": ["Destruction, effacement", "valide_par_referent_linguistique"],
    "bugunde": ["Soustraction", "valide_par_referent_linguistique"],
    "burubule": ["Brûlure, brûlis", "valide_par_referent_linguistique"],
    "buxutindaana": ["Arracheur", "valide_par_referent_linguistique"],
    "buyaade": ["Fer à marquer ; moule métallique pour marquer le bétail ou imprimer le cuir ; grillage à griller", "valide_par_referent_linguistique"],
    "buxuti": ["Arracher, déraciner", "valide_par_referent_linguistique"],
    "buugu": ["Fermenter, enfler, gonfler", "valide_par_referent_linguistique"],
    "bukku": ["Sortir, partir", "valide_par_referent_linguistique"],
    "buxutinde": ["Arrachage, déracinement", "valide_par_referent_linguistique"],
    "buyi": ["Brûler, griller", "valide_par_referent_linguistique"],
    "bulunŋe": ["Petite rue, ruelle ; vestibule", "valide_par_referent_linguistique"],
    "bugundi": ["Enlever", "valide_par_referent_linguistique"],
  };
  for (const [form, [french, status]] of Object.entries(expectedAudioTranslations)) {
    const audio = evaluate("findAudioInfo(" + JSON.stringify(form) + ")");
    assert(audio && audio.url, "Missing audio mapping for " + form);
    assert.equal(evaluate("state.audioList.some(a => normalizeWord(a.text) === normalizeWord(" + JSON.stringify(form) + "))"), true,
      "Audio not visible in Lexique Audio for " + form);
    assert.equal(audio.traduction_statut, status, "Wrong translation status for " + form);
    assert.equal(audio.francais || "", french, "Wrong French translation for " + form);
  }
  assert.equal(Object.keys(expectedAudioTranslations).length, 17);
  assert.equal(evaluate("lookupTerm('buxutin').exact.some(e => e.francais === 'Arraché' && e.statut === 'valide_par_referent_linguistique')"), true,
    "La définition validée buxutin → arraché doit être accessible dans le lexique");
  // Les deux traductions déjà validées restent rattachées aux lemmes existants, sans doublons.
  assert.equal(evaluate("lookupTerm('biyaade').exact.filter(e => normalizeWord(e.soninke) === 'biyaade').length"), 1,
    "La forme canonique biyaade doit rester une seule entrée");
  assert.equal(evaluate("lookupTerm('bolonŋe').exact.filter(e => normalizeWord(e.soninke) === 'bolonŋe').length"), 1,
    "La forme canonique bolonŋe doit rester une seule entrée");

  assert.equal(evaluate("lookupTerm('baano-ye').exact[0].soninke"), 'baano-ye');
  assert.equal(evaluate("lookupTerm('segeñe').exact[0].francais"), 'ongle');
  assert(evaluate("lookupTerm('segene').exact[0].francais").includes('monter'));

  // ── Contrôle linguistique : aucune forme étrangère présentée comme soninké ──
  assert(evaluate('state.guard.size') >= 4, 'La liste d’exclusion linguistique doit être chargée');
  assert.equal(evaluate("isExcludedForm('i ni ce')"), true);
  assert.equal(evaluate("isExcludedForm('ni barka')"), true);
  assert.equal(evaluate("isExcludedForm('Xa wouy Diom')"), false);
  const excludedReply = evaluate("generateResponse('i ni ce')");
  assert(!/\{\{pair:i ni ce/.test(excludedReply), 'Une forme écartée ne doit jamais être présentée en soninké');
  assert(/Nawari/.test(excludedReply), 'La forme soninké attestée doit être proposée');

  // ── Ordre SONINKÉ ↓ FRANÇAIS ──
  const greeting = evaluate("generateResponse('bonjour')");
  assert(/\{\{pair:Xa wouy Diom\|/.test(greeting), 'Le bloc doit commencer par la forme soninké');
  const rendered = evaluate("renderMarkdown(generateResponse('bonjour'))");
  assert(!/\{\{pair:/.test(rendered), 'Tous les blocs doivent être rendus');
  assert(/pair-snk[^>]*>Xa wouy Diom<[\s\S]*pair-fr[^>]*>Bonjour/.test(rendered), 'Ordre soninké puis traduction');

  // ── Attestation linguistique ──
  assert.equal(evaluate("attestationOf('Xa wouy Diom').level"), 'referent');
  assert.equal(evaluate("attestationOf('an moxo').level"), 'review');
  assert.equal(evaluate("attestationOf('forme totalement inconnue').level"), 'unknown');

  // ── Voix de référence : tous les audios passent par le même index ──
  const refAudio = evaluate("findAudioInfo('baano-ye')");
  assert(refAudio && refAudio.url === 'audio/snk-00006.wav', 'Audio de référence attendu pour baano-ye');
  assert.equal(evaluate("isExcludedForm('baano-ye')"), false);

  // ── Niveaux et favoris ──
  evaluate("setLevel('avance', false)");
  assert.equal(evaluate('state.level'), 'avance');
  evaluate("setLevel('debutant', false)");
  evaluate("toggleFavorite({ snk: 'Xa wouy Diom', fr: 'Bonjour', type: 'expression' })");
  assert.equal(evaluate('state.favorites.length'), 1);
  assert.equal(evaluate("isFavorite('Xa wouy Diom', 'Bonjour')"), true);
  evaluate("toggleFavorite({ snk: 'Xa wouy Diom', fr: 'Bonjour', type: 'expression' })");
  assert.equal(evaluate('state.favorites.length'), 0);

  // ── Aucun emoji décoratif dans les réponses générées ──
  for (const prompt of ["bonjour", "aide", "famille", "apprends-moi 5 mots", "Raconte une histoire"]) {
    const reply = evaluate(`generateResponse(${JSON.stringify(prompt)})`);
    assert(!/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u.test(reply), `Emoji décoratif dans la réponse : ${prompt}`);
  }

  // ── Composition lexicale de secours : garder l'ordre, les répétitions et signaler les mots absents ──
  const lexicalFallback = evaluate("composeLexicalPhraseFallback('je mange le riz chaque jour')");
  assert(lexicalFallback && lexicalFallback.sentence, 'Une phrase multi-mots doit être composée avec les mots disponibles');
  assert(/n|maro|yige|koota/i.test(lexicalFallback.sentence), `Les mots disponibles doivent être réutilisés : ${lexicalFallback.sentence}`);
  const repeatedFallback = evaluate("composeLexicalPhraseFallback('je mange le riz et je mange')");
  assert(repeatedFallback && repeatedFallback.mapped.filter(x => x.token === 'je').length >= 2,
    'La composition ne doit pas supprimer les répétitions de mots');
  const partialFallback = evaluate("composeLexicalPhraseFallback('je mange un zorbax')");
  assert(partialFallback && partialFallback.missingFrench.includes('zorbax'),
    'Les mots sans correspondance doivent être signalés sans bloquer toute la composition');
  const fallbackReply = evaluate("fallbackComposedPhrase('je mange le riz chaque jour')");
  assert(/Correspondances lexicales trouvées/i.test(fallbackReply),
    'Quand la grammaire est incertaine, la réponse doit présenter les correspondances lexicales');
  assert(!fallbackReply.includes(lexicalFallback.sentence),
    'Le fallback ne doit pas présenter l’assemblage dans l’ordre français comme une phrase soninkée');
  assert(/phrase complète n'est pas confirmée/i.test(fallbackReply),
    'Le fallback doit expliciter que la phrase complète n’est pas confirmée');

  // ── Composition grammaticale : Sujet + Auxiliaire + Objet + Verbe (corpus attesté) ──
  // Inaccompli transitif : S + wa + O + V(-na/-ne/-ni)
  const pres = evaluate("generateResponse('Traduis « je mange le riz chaque jour » en soninké')");
  assert(/\{\{pair:N wa maro ke yigene koota su\|/.test(pres), `Inaccompli attendu « N wa maro ke yigene koota su », obtenu : ${pres.slice(0, 200)}`);
  // Accompli transitif : S + n'di + O + n'V (attesté : « Anké n'di maro n'yiga »)
  const past = evaluate("generateResponse('Traduis « l\\'enfant a mangé le riz » en soninké')");
  assert(/\{\{pair:Lemine ke da maro ke n'yige\|/.test(past), `Accompli nominal attendu, obtenu : ${past.slice(0, 200)}`);
  const past2 = evaluate("generateResponse('Traduis « tu as bu le lait » en soninké')");
  assert(/\{\{pair:Anké n'di xati ke m'mini\|/.test(past2), `Accompli 2s attendu « Anké n'di xati ke m'mini », obtenu : ${past2.slice(0, 240)}`);
  // Accompli intransitif : S + V + complément (attesté : « N daga » / « Aké n'daga sakha lenki »)
  const intrans = evaluate("generateResponse('Traduis « je suis parti au marché hier » en soninké')");
  assert(/\{\{pair:N daga saxa daru\|/.test(intrans), `Accompli intransitif attendu, obtenu : ${intrans.slice(0, 200)}`);
  const intrans3 = evaluate("generateResponse('Traduis « il est parti au marché hier » en soninké')");
  assert(/\{\{pair:Aké n'daga saxa daru\|/.test(intrans3), `Accompli intransitif 3s attendu « Aké n'daga saxa daru », obtenu : ${intrans3.slice(0, 240)}`);
  // Priorité absolue au corpus : la phrase enregistrée prime sur la recomposition
  const corpusHit = evaluate("generateResponse('Traduis « tu as mangé le riz » en soninké')");
  assert(/\{\{pair:anké n'di maro n'yiga\|/.test(corpusHit) && /Phrase attestée dans le corpus/.test(corpusHit),
    `La phrase attestée du corpus doit primer, obtenu : ${corpusHit.slice(0, 240)}`);
  // Négation de l'inaccompli : nta + verbe inaccompli
  const neg = evaluate("generateResponse('Traduis « nous ne travaillons pas aujourd\\'hui » en soninké')");
  assert(/\{\{pair:O nta golini lenki\|/.test(neg), `Négation inaccompli attendue, obtenu : ${neg.slice(0, 200)}`);
  // Négation du passé : ma + verbe à sa base
  const negPast = evaluate("generateResponse('Traduis « elle n\\'a pas bu le lait » en soninké')");
  assert(/\{\{pair:A ma xati ke mini\|/.test(negPast), `Négation du passé attendue, obtenu : ${negPast.slice(0, 200)}`);
  // Mot manquant signalé, jamais inventé
  const missing = evaluate("generateResponse('Traduis « je mange du poisson avec le chat » en soninké')");
  assert(/sans correspondance lexicale|éléments sans correspondance|poisson/i.test(missing),
    `Le mot manquant doit être signalé sans l’inventer, obtenu : ${missing.slice(0, 240)}`);
  assert(!/\\{\\{pair:[^|]*poisson[^|]*\\|/i.test(missing),
    'Un mot absent ne doit pas être inséré dans une pseudo-phrase soninkée');
  assert(!/phrase composée automatiquement/i.test(missing),
    'Un fallback lexical incertain ne doit pas être présenté comme une phrase composée');
  // Une phrase composée est reconnue comme « Composé · lexique attesté »
  assert.equal(evaluate("attestationOf('N wa maro ke yigene').level"), 'composed');
  assert.equal(evaluate("attestationOf('N daga saxa').level"), 'composed');

  console.log(`Authentic voice, linguistic guard & lexicon tests passed (${entries.length} unique entries)`);
})();
