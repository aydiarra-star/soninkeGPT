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
assert.equal(evaluate("explainFrench('**Xa wouy Diom**').includes('bonjour')"), true);
assert.equal(evaluate("soninkeForms('**Titre inconnu**').length"), 0);

(async () => {
  await evaluate('loadAllData()');
  const entries = evaluate('state.entries');
  assert(entries.length > 1300, `Expected >1300 lexicon entries, got ${entries.length}`);
  const seenIds = new Set();
  const seenWords = new Set();
  for (const e of entries) {
    assert(e.soninke && e.francais, `Incomplete entry: ${JSON.stringify(e)}`);
    assert(!seenIds.has(e.id), `Duplicate lexicon ID: ${e.id}`);
    seenIds.add(e.id);
    const key = evaluate(`normalizeWord(${JSON.stringify(e.soninke)})`);
    assert(!seenWords.has(key), `Duplicate Soninke headword in soninkeGPT: ${e.soninke} (${key})`);
    seenWords.add(key);
  }
  assert.equal(evaluate("lookupTerm('baano-ye').exact[0].soninke"), 'baano-ye');
  assert.equal(evaluate("lookupTerm('segeñe').exact[0].francais"), 'ongle');
  assert(evaluate("lookupTerm('segene').exact[0].francais").includes('monter'));
  console.log(`Authentic voice & zero-duplicate lexicon tests passed (${entries.length} unique entries)`);
})();
