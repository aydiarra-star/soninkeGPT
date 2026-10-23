const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const html = fs.readFileSync('index.html', 'utf8');
const css = fs.readFileSync('styles.css', 'utf8');
const js = fs.readFileSync('app.js', 'utf8');

function extractElementById(markup, id) {
  const startRe = new RegExp(`<([a-z0-9-]+)\\b[^>]*\\bid="${id}"[^>]*>`, 'i');
  const m = markup.match(startRe);
  if (!m) return null;
  const tag = m[1];
  let idx = m.index + m[0].length;
  let depth = 1;
  const tokenRe = new RegExp(`<(/?)${tag}\\b[^>]*>`, 'gi');
  tokenRe.lastIndex = idx;
  while (depth > 0) {
    const next = tokenRe.exec(markup);
    assert(next, `Unclosed <${tag}> for id="${id}"`);
    depth += next[1] === '/' ? -1 : 1;
    idx = tokenRe.lastIndex;
  }
  return markup.slice(m.index, idx);
}

// 1. Page d'accueil épurée (#welcome-screen)
const welcomeScreen = extractElementById(html, 'welcome-screen');
assert(welcomeScreen, '#welcome-screen must exist');
assert(welcomeScreen.includes('Bienvenue sur SoninkeGPT'), 'Le titre Bienvenue sur SoninkeGPT doit être présent');
assert(welcomeScreen.includes("L'assistant vocal de la langue soninké"), 'La sous-description doit être présente');

for (const forbiddenInHome of [
  'Parlez en soninké',
  'Traduisez instantanément',
  'Apprenez la langue',
  'Écoutez la prononciation authentique',
  'Commencer à parler',
  'Écouter la voix de référence',
  "Niveau d'apprentissage",
  'Suggestions rapides',
  'Présente-toi',
  'Traduis cette phrase',
  'Apprends-moi 5 mots',
  'welcome-features',
  'welcome-actions',
  'level-section',
  'suggestion-card',
]) {
  assert(
    !welcomeScreen.includes(forbiddenInHome),
    `L'écran central #welcome-screen ne doit plus contenir : ${forbiddenInHome}`
  );
}

// Barre de saisie en bas conservée dans #main-area
const inputArea = extractElementById(html, 'input-area');
assert(inputArea, '#input-area doit être présent');
assert(inputArea.includes('id="message-input"'), 'Zone de texte requise');
assert(inputArea.includes('id="mic-btn"'), 'Bouton micro requis');
assert(inputArea.includes('id="send-btn"'), 'Bouton envoi requis');
assert(inputArea.includes('id="voice-reply-btn"'), 'Bouton voix requis');

// 2. Menu latéral & 4 onglets structurés
const sidebar = extractElementById(html, 'sidebar');
assert(sidebar, '#sidebar doit être présent');
for (const tabLabel of ['Assistant vocal', 'Lexique Audio', 'Favoris', 'Paramètres']) {
  assert(sidebar.includes(tabLabel), `L'onglet « ${tabLabel} » doit figurer dans la barre latérale`);
}

// Contenu déplacé dans chacun des 4 onglets
const voiceModal = extractElementById(html, 'voice-modal');
assert(voiceModal && voiceModal.includes('Commencer à parler'), 'Assistant vocal doit contenir « Commencer à parler »');
assert(voiceModal.includes('Parlez en soninké') && voiceModal.includes('Traduisez instantanément'), 'Assistant vocal doit regrouper parole et traduction');
assert(voiceModal.includes('Traduis cette phrase') && voiceModal.includes('Présente-toi en soninké'), 'Assistant vocal doit proposer les actions rapides vocales/traduction');

const dictModal = extractElementById(html, 'dictionary-modal');
assert(dictModal && dictModal.includes('Écouter la voix de référence'), 'Lexique Audio doit contenir « Écouter la voix de référence »');
assert(dictModal.includes('Apprenez la langue') && dictModal.includes('Écoutez la prononciation authentique'), 'Lexique Audio doit regrouper apprentissage et écoute authentique');
assert(dictModal.includes('Apprends-moi 5 mots'), 'Lexique Audio doit inclure les modules de vocabulaire');

const favModal = extractElementById(html, 'favorites-modal');
assert(favModal, '#favorites-modal doit exister');
for (const cat of ['Traductions', 'Phrases', 'Proverbes', 'Histoires']) {
  assert(favModal.includes(cat), `Favoris doit proposer le classement : ${cat}`);
}
assert(favModal.includes('Donne-moi un proverbe') && favModal.includes('Raconte une histoire'), 'Favoris doit permettre de retrouver proverbes et histoires');

const settingsModal = extractElementById(html, 'settings-modal');
assert(settingsModal && settingsModal.includes("Niveau d'apprentissage"), 'Paramètres doit contenir « Niveau d\'apprentissage »');
for (const lvl of ['Débutant', 'Intermédiaire', 'Avancé']) {
  assert(settingsModal.includes(lvl), `Paramètres doit contenir le niveau : ${lvl}`);
}
assert(settingsModal.includes('id="voice-replies-switch"'), 'Paramètres doit contenir les réglages audio');

// 3. Charte graphique crème / marron / doré intacte
assert(css.includes('--primary: #B8860B'), 'Teinte dorée #B8860B conservée');
assert(css.includes('--bg: #FAF6E9'), 'Teinte crème #FAF6E9 conservée');
assert(css.includes('--primary-ink: #5E4517') && css.includes('--primary-deep: #3B2C12'), 'Teintes marron conservées');

// 3b. Intégrité 100 % des IDs DOM référencés entre index.html et app.js
const htmlIds = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]));
const jsIds = [...new Set([...js.matchAll(/["']#([a-zA-Z0-9_-]+)["']/g)].map(m => m[1]))];
const missingIds = jsIds.filter(id => !htmlIds.has(id) && !['audio-notice', 'typing-indicator'].includes(id));
assert.deepEqual(missingIds, [], `Aucun ID manquant entre app.js et index.html (manquants : ${missingIds.join(', ')})`);

// 4. Exécution JS des filtres de favoris, niveaux et init() complet sur DOM simulé
function makeMockEl(id = '') {
  const classes = new Set();
  const attrs = new Map();
  return {
    id,
    value: '',
    textContent: '',
    innerHTML: '',
    hidden: false,
    disabled: false,
    style: {},
    dataset: { dir: 'all', favFilter: 'all', level: 'debutant', openPanel: 'voice-modal', theme: 'light', prompt: 'Bonjour' },
    classList: {
      add: (...c) => c.forEach(x => classes.add(x)),
      remove: (...c) => c.forEach(x => classes.delete(x)),
      toggle: (x, force) => {
        const next = force !== undefined ? !!force : !classes.has(x);
        if (next) classes.add(x); else classes.delete(x);
        return next;
      },
      contains: (x) => classes.has(x),
    },
    setAttribute: (k, v) => attrs.set(k, String(v)),
    getAttribute: (k) => attrs.get(k) ?? null,
    addEventListener: () => {},
    removeEventListener: () => {},
    querySelector: () => null,
    querySelectorAll: () => [],
    append: () => {},
    appendChild: () => {},
    remove: () => {},
    focus: () => {},
    select: () => {},
    closest: () => null,
  };
}
const elCache = new Map();
const getEl = (sel) => {
  if (!elCache.has(sel)) elCache.set(sel, makeMockEl(sel.replace(/^#/, '')));
  return elCache.get(sel);
};

const sandbox = {
  console,
  setTimeout,
  clearTimeout,
  setInterval,
  clearInterval,
  requestAnimationFrame: (fn) => fn(),
  document: {
    documentElement: makeMockEl('html'),
    body: makeMockEl('body'),
    createElement: (tag) => makeMockEl(tag),
    querySelector: (sel) => getEl(sel),
    querySelectorAll: (sel) => [getEl(sel)],
    addEventListener: () => {},
    removeEventListener: () => {},
  },
  window: { matchMedia: () => ({ matches: false, addEventListener: () => {} }) },
  navigator: {},
  localStorage: { getItem: () => null, setItem: () => {} },
  fetch: async () => ({ ok: false, text: async () => '' }),
};
vm.createContext(sandbox);
vm.runInContext(js, sandbox);

assert.equal(vm.runInContext("matchesFavoriteFilter({ type: 'mot' }, 'traduction')", sandbox), true);
assert.equal(vm.runInContext("matchesFavoriteFilter({ type: 'proverbe' }, 'proverbe')", sandbox), true);
assert.equal(vm.runInContext("matchesFavoriteFilter({ type: 'histoire' }, 'histoire')", sandbox), true);
assert.equal(vm.runInContext("matchesFavoriteFilter({ type: 'phrase' }, 'phrase')", sandbox), true);
assert.equal(vm.runInContext("favoriteTypeLabel('proverbe')", sandbox), 'Proverbe');
assert.equal(vm.runInContext("favoriteTypeLabel('histoire')", sandbox), 'Histoire');

console.log('UI minimalist redesign, 4-tab reorganization & color palette tests passed!');
