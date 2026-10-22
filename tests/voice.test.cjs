const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync('app.js', 'utf8');
assert(!/speechSynthesis|SpeechSynthesisUtterance|speakUtterance/.test(source));
const sandbox = { console };
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
console.log('Authentic voice tests passed');
