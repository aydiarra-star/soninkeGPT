/* ============================================
   SONINKEGPT — L'assistant vocal de la langue soninké
   - Réponses exclusivement issues du corpus soninké attesté
   - Contrôle linguistique : jamais de bambara, malinké, peul, wolof,
     arabe, dioula ni d'expression étrangère présentée comme soninké
   - Voix de référence du corpus sur tous les contenus audio
   - Aucun moteur vocal du navigateur
   - Niveaux d'apprentissage : débutant, intermédiaire, avancé
   - Favoris : mots, phrases et expressions à réécouter
   ============================================ */

// ── Constants ──
const DATA_URL = "data/source/lexique-soninke-fr-base.csv";
const MANIFEST_URL = "data/source/manifest-577-review.csv";
const AUDIO_AUDIT_URL = "reports/audio-transfer-audit.csv";
const CANDIDATES_URL = "data/candidates/external-lexicon-candidates.csv";
const HEAD_FACE_URL = "data/source/head-face-audio-recording-queue.csv";
const SAMPLES_URL = "data/source/soninke-samples.jsonl";
const FICHE_VAL_1_URL = "data/source/reports/fiche-validation-referent-soninke.csv";
const FICHE_VAL_4_URL = "data/source/reports/fiche-validation-referent-soninke-04.csv";
const REVUE_DICT_URL = "data/source/reports/revue-enrichissement-dictionnaire-soninke.csv";
const RENVOIS_URL = "data/source/reports/controle-renvois-dictionnaire-soninke-2026-10-21.csv";

const GUARD_URL = "data/validation/non-soninke-forms.json";
const VOICE_MEMORY_URL = "data/voice-memory.json";

const STORAGE_KEY = "soninkegpt_conversations";
const THEME_KEY = "soninkegpt_theme";
const VOICE_PREF_KEY = "soninkegpt_voice_replies";
const LEVEL_KEY = "soninkegpt_level";
const FAVORITES_KEY = "soninkegpt_favorites";
const MAX_DISPLAY = 100;

// ── State ──
const state = {
  entries: [],
  samples: [],
  audioList: [],
  audioByWord: new Map(),
  audioByOrtho: new Map(),
  relatedAudioByStem: new Map(),
  conversations: [],
  activeConversationId: null,
  direction: "all",
  isGenerating: false,
  activeStream: null,
  voiceReplies: true,
  listening: false,
  recognition: null,
  recorder: null,
  mediaStream: null,
  recordChunks: [],
  lastTranscript: "",
  recordTimerId: null,
  recordStartedAt: 0,
  speechToken: 0,
  currentAudio: null,
  sharedAudio: null,
  audioCtx: null,
  audioBufferCache: new Map(),
  audioByVariant: new Map(),
  referenceVoice: { model: "", references: [], count: 0 },
  guard: new Set(),
  guardInfo: [],
  favorites: [],
  favoriteFilter: "all",
  level: "debutant",
  dataReady: null,
  shiftHeld: false,
};

// ── Niveaux d'apprentissage ──
const LEVELS = {
  debutant: {
    label: "Débutant",
    maxEntries: 3,
    maxSamples: 1,
    showTranslations: true,
    hint: "Traductions complètes, phrases courtes et écoute guidée.",
    guidance: "Écoutez chaque forme, puis répétez-la à voix haute.",
  },
  intermediaire: {
    label: "Intermédiaire",
    maxEntries: 6,
    maxSamples: 2,
    showTranslations: true,
    hint: "Traductions, variantes et exemples du corpus.",
    guidance: "Comparez les variantes et repérez les formes du quotidien.",
  },
  avance: {
    label: "Avancé",
    maxEntries: 10,
    maxSamples: 3,
    showTranslations: true,
    hint: "Formes attestées, variantes, notes et exemples.",
    guidance: "Travaillez les variantes et les formes fléchies du corpus.",
  },
};

function currentLevel() {
  return LEVELS[state.level] || LEVELS.debutant;
}

// Nombre d'enregistrements disponibles avec la voix de référence.
state.audioReferenceCount = function () {
  return state.audioByWord.size;
};

// ── Expressions attestées du corpus soninké ──
const PHRASEBOOK = [
  { fr: "bonjour", snk: "Xa wouy Diom", alt: ["an wouydiom", "an moxo", "qa moxo"], note: "Xa wouy Diom = salutation respectueuse (pluriel) · an wouydiom = à une personne · an moxo / qa moxo = comment ça va" },
  { fr: "salut", snk: "Xa wouy Diom", alt: ["an wouydiom", "an moxo"], note: "salutation courante" },
  { fr: "bonsoir", snk: "lellaane", alt: ["Xa wouy Diom"], note: "salutation de l'après-midi / soir" },
  { fr: "bienvenue", snk: "bisimilla", alt: ["Xa wouy Diom"], note: "bonne arrivée, accueillir" },
  { fr: "merci", snk: "nawari", alt: ["nawaari"], note: "remerciement · variante nawaari" },
  { fr: "au revoir", snk: "oyi waxati", alt: ["hali telle"], note: "salutation de départ" },
  { fr: "comment vas-tu", snk: "i kera di", alt: ["an moxo", "qa moxo"], note: "demander des nouvelles" },
  { fr: "comment allez-vous", snk: "qa moxo", alt: ["Xa wouy Diom"], note: "pluriel / politesse · forme de source externe à confirmer" },
  { fr: "ça va", snk: "toora nta", alt: ["toora su nta"], note: "tout va bien (aucun mal) · traduction complémentaire du référent : toora su nta = tu vas bien" },
  { fr: "tu vas bien", snk: "toora su nta", alt: ["toora nta"], note: "traduction fournie par le référent linguistique ; audio à rechercher/produire et valider" },
  { fr: "je veux apprendre la langue soninké", snk: "N ga moula na Soninkanxannen xara", alt: [], note: "phrase fournie par le référent linguistique. Décomposition : N = je ; ga moula na = je veux / j’ai envie de ; Soninkanxannen = la langue soninké ; xara = apprendre / étudier. Audio à rechercher/produire puis valider." },
  { fr: "je m’appelle …", snk: "N toxo ...", alt: [], note: "formule à compléter avec le nom ; fournie par le référent linguistique. Audio à rechercher/produire puis valider." },
  { fr: "tu t’appelles comment ?", snk: "An toxo", alt: [], note: "question fournie par le référent linguistique. Audio à rechercher/produire puis valider." },
  { fr: "oui", snk: "ee", alt: [], note: "approbation" },
  { fr: "non", snk: "ayi", alt: [], note: "négation" },
  { fr: "pardon", snk: "mbaari", alt: ["yampa"], note: "excusez-moi · yampa = pardonner" },
  { fr: "excusez-moi", snk: "mbaari", alt: ["yampa"], note: "demander pardon" },
  { fr: "je", snk: "nké", alt: ["n"], note: "pronom 1re personne singulier" },
  { fr: "moi", snk: "nké", alt: [], note: "pronom" },
  { fr: "tu", snk: "an", alt: ["anké", "i"], note: "pronom 2e personne singulier" },
  { fr: "toi", snk: "anké", alt: ["an"], note: "pronom" },
  { fr: "il", snk: "a", alt: ["aké"], note: "pronom 3e personne singulier" },
  { fr: "elle", snk: "a", alt: ["aké"], note: "pronom 3e personne singulier" },
  { fr: "nous", snk: "o", alt: ["oku"], note: "pronom 1re personne pluriel" },
  { fr: "vous", snk: "xa", alt: [], note: "pronom 2e personne pluriel" },
  { fr: "partir", snk: "daga", alt: [], note: "verbe" },
  { fr: "aller", snk: "daga", alt: [], note: "verbe" },
  { fr: "venir", snk: "ri", alt: [], note: "verbe" },
  { fr: "parler", snk: "sefe", alt: [], note: "verbe" },
  { fr: "manger", snk: "yige", alt: ["yiga"], note: "verbe" },
  { fr: "boire", snk: "mini", alt: [], note: "verbe" },
  { fr: "dormir", snk: "qenqe", alt: [], note: "verbe" },
  { fr: "travailler", snk: "goli", alt: [], note: "verbe" },
  { fr: "regarder", snk: "faye", alt: [], note: "verbe" },
  { fr: "voir", snk: "wori", alt: [], note: "verbe" },
  { fr: "écrire", snk: "safa", alt: [], note: "verbe" },
  { fr: "prendre", snk: "wutu", alt: [], note: "verbe" },
  { fr: "donner", snk: "kini", alt: [], note: "verbe" },
  { fr: "aimer", snk: "xanu", alt: ["munda"], note: "verbe" },
  { fr: "asseoir", snk: "taxu", alt: [], note: "verbe" },
  { fr: "eau", snk: "ji", alt: [], note: "nom" },
  { fr: "riz", snk: "maro", alt: ["mano"], note: "nom" },
  { fr: "lait", snk: "xati", alt: [], note: "nom" },
  { fr: "maison", snk: "ka", alt: [], note: "nom" },
  { fr: "marché", snk: "saxa", alt: ["sakha"], note: "nom" },
  { fr: "enfant", snk: "lemine", alt: ["komo"], note: "nom" },
  { fr: "femme", snk: "yaxare", alt: ["yaxaré"], note: "nom" },
  { fr: "homme", snk: "yugo", alt: [], note: "nom" },
  { fr: "père", snk: "haabe", alt: ["baaba", "faba"], note: "nom" },
  { fr: "papa", snk: "baaba", alt: ["haabe", "faba"], note: "nom" },
  { fr: "mère", snk: "saaxe", alt: [], note: "nom" },
  { fr: "maman", snk: "saaxe", alt: [], note: "nom" },
  { fr: "aujourd'hui", snk: "lenki", alt: [], note: "adverbe" },
  { fr: "hier", snk: "daru", alt: [], note: "adverbe" },
  { fr: "jour", snk: "koota", alt: ["koota su"], note: "nom · koota su = chaque jour" },
  { fr: "matin", snk: "suxuba", alt: [], note: "nom" },
  { fr: "toujours", snk: "waxati su", alt: [], note: "expression = à tout moment" },
  { fr: "jamais", snk: "abada", alt: [], note: "adverbe" },
  { fr: "grand", snk: "qoore", alt: [], note: "adjectif" },
  { fr: "petit", snk: "loxe", alt: [], note: "adjectif" },
  { fr: "bon", snk: "sire", alt: ["bo"], note: "adjectif" },
  { fr: "beaucoup", snk: "gaba", alt: ["gabe"], note: "quantitatif" },
  { fr: "peu", snk: "honne", alt: [], note: "quantitatif" },
  { fr: "dieu", snk: "Ala", alt: [], note: "nom" },
];

// ════════════════════════════════════════════════════════════
//  CONTRÔLE LINGUISTIQUE — fiabilité avant quantité
//  Toute forme présentée comme soninké doit être attestée dans
//  le corpus (référent, lexique, phrases parallèles).
// ════════════════════════════════════════════════════════════

const ATTESTATION = {
  referent: { rank: 4, label: "Attesté · référent", cls: "is-attested" },
  corpus: { rank: 3, label: "Attesté · corpus", cls: "is-attested" },
  composed: { rank: 3, label: "Composé · lexique attesté", cls: "is-attested" },
  review: { rank: 2, label: "À vérifier · source externe", cls: "is-review" },
  reference: { rank: 3, label: "Voix de référence", cls: "is-attested" },
  unknown: { rank: 0, label: "Non attesté dans le corpus", cls: "is-unknown" },
  excluded: { rank: -1, label: "Forme écartée · non soninké", cls: "is-unknown" },
};

function loadGuard() {
  try {
    const raw = localStorage.getItem("soninkegpt_guard_cache");
    if (raw) applyGuard(JSON.parse(raw));
  } catch {}
}

function applyGuard(payload) {
  const list = Array.isArray(payload?.excluded) ? payload.excluded : [];
  state.guardInfo = list;
  state.guard = new Set();
  for (const item of list) {
    const form = typeof item === "string" ? item : item && item.form;
    const key = normalizeWord(form);
    if (key) state.guard.add(key);
  }
}

function isExcludedForm(form) {
  const key = normalizeWord(form);
  if (!key) return false;
  if (state.guard.has(key)) return true;
  const tokens = key.split(/\s+/).filter(Boolean);
  return tokens.length > 1 && tokens.every((t) => state.guard.has(t));
}

function isAttestedSoninkeSpan(span) {
  const key = normalizeWord(span);
  if (!key || isExcludedForm(span)) return false;
  if (state.entries.some((e) => normalizeWord(e.soninke) === key)) return true;
  if (PHRASEBOOK.some((p) => normalizeWord(p.snk) === key || p.alt.some((a) => normalizeWord(a) === key))) return true;
  if (state.samples.some((s) => normalizeWord(s.soninke) === key)) return true;
  if (findAudioInfo(span)) return true;
  // Forme inaccomplie régulière (-na/-ne/-ni/-no/-nu) d'un verbe attesté du corpus
  const impfMatch = key.match(/^(.+?[aeiou])n([aeiou])$/);
  if (impfMatch && impfMatch[1].slice(-1) === impfMatch[2]) {
    const stem = impfMatch[1];
    if (state.entries.some((e) => /verbe/i.test(e.categorie || "") && normalizeWord(e.soninke) === stem)) {
      return true;
    }
  }
  return false;
}

// Attestation d'une forme soninké, sans jamais inventer de source.
// Le statut linguistique prime sur la simple présence d'un audio.
function attestationOf(form) {
  const key = normalizeWord(form);
  if (!key) return { level: "unknown", ...ATTESTATION.unknown };

  if (isExcludedForm(form)) return { level: "excluded", ...ATTESTATION.excluded };

  // 1. Entrée lexicale (validée par le référent, corpus, ou source externe)
  const entry = state.entries.find((e) => normalizeWord(e.soninke) === key);
  if (entry) {
    const statut = String(entry.statut || "");
    const level = /valide_par_referent|fourni_par_referent/i.test(statut)
      ? "referent"
      : entry.isCandidate || /a_verifier|externe/i.test(statut)
        ? "review"
        : "corpus";
    return { level, ...ATTESTATION[level], entry, audio: findAudioInfo(form) };
  }

  // 2. Livret d'expressions
  const phrase = PHRASEBOOK.find(
    (p) => normalizeWord(p.snk) === key || p.alt.some((a) => normalizeWord(a) === key)
  );
  if (phrase) return { level: "corpus", ...ATTESTATION.corpus, phrase, audio: findAudioInfo(form) };

  // 3. Phrases parallèles du corpus
  const sample = state.samples.find((s) => normalizeWord(s.soninke) === key);
  if (sample) return { level: "corpus", ...ATTESTATION.corpus, sample, audio: findAudioInfo(form) };

  // 4. Enregistrement présent dans l'index de référence
  const audio = findAudioInfo(form);
  if (audio) {
    const level = audio.generated ? "reference" : "referent";
    return { level, ...ATTESTATION[level], audio };
  }

  // 5. Phrase composée grammaticalement dont chaque segment est attesté dans le corpus
  const cleanTokens = String(form || "")
    .replace(/[«»"“”.,!?;:()[\]]/g, " ")
    .trim()
    .split(/\s+/)
    .filter(Boolean);
  if (cleanTokens.length >= 2) {
    let idx = 0;
    let allAttested = true;
    while (idx < cleanTokens.length) {
      let matchedEnd = -1;
      for (let end = Math.min(cleanTokens.length, idx + 4); end > idx; end--) {
        const span = cleanTokens.slice(idx, end).join(" ");
        if (isAttestedSoninkeSpan(span)) {
          matchedEnd = end;
          break;
        }
      }
      if (matchedEnd < 0) {
        allAttested = false;
        break;
      }
      idx = matchedEnd;
    }
    if (allAttested) {
      return { level: "composed", ...ATTESTATION.composed, audio: findAudioInfo(form) };
    }
  }

  return { level: "unknown", ...ATTESTATION.unknown };
}

// Bloc d'affichage SONINKÉ ↓ TRADUCTION FRANÇAISE (jamais l'inverse).
function soninkeBlock(snk, fr, type = null) {
  const cleanSnk = String(snk || "").replace(/[|{}]/g, " ").replace(/\s+/g, " ").trim();
  const cleanFr = String(fr || "").replace(/[|{}]/g, " ").replace(/\s+/g, " ").trim();
  if (!cleanSnk) return "";
  const kind = type || (cleanSnk.split(/\s+/).length > 1 ? "phrase" : "mot");
  return `\n\n{{pair:${cleanSnk}|${cleanFr}|${kind}}}\n\n`;
}

function levelNote() {
  return currentLevel().guidance;
}

function levelLimit(key) {
  return currentLevel()[key] || LEVELS.intermediaire[key];
}

// ════════════════════════════════════════════════════════════
//  FAVORIS — mots, phrases et expressions
// ════════════════════════════════════════════════════════════

function loadFavorites() {
  try {
    const raw = localStorage.getItem(FAVORITES_KEY);
    const list = raw ? JSON.parse(raw) : [];
    state.favorites = Array.isArray(list) ? list.filter((f) => f && f.snk) : [];
  } catch {
    state.favorites = [];
  }
}

function saveFavorites() {
  try { localStorage.setItem(FAVORITES_KEY, JSON.stringify(state.favorites)); } catch {}
}

function favoriteKey(snk, fr) {
  return `${normalizeWord(snk)}|${normalizeWord(fr || "")}`;
}

function isFavorite(snk, fr) {
  const key = favoriteKey(snk, fr);
  return state.favorites.some((f) => favoriteKey(f.snk, f.fr) === key);
}

function toggleFavorite(item) {
  if (!item || !item.snk) return;
  const key = favoriteKey(item.snk, item.fr);
  const index = state.favorites.findIndex((f) => favoriteKey(f.snk, f.fr) === key);
  if (index >= 0) {
    state.favorites.splice(index, 1);
  } else {
    state.favorites.unshift({
      snk: String(item.snk).trim(),
      fr: String(item.fr || "").trim(),
      type: item.type || (String(item.snk).trim().split(/\s+/).length > 1 ? "phrase" : "mot"),
      source: item.source || "SoninkeGPT",
      createdAt: Date.now(),
    });
  }
  saveFavorites();
  syncFavoriteButtons();
  renderFavorites();
  updateFavoritesCount();
}

function updateFavoritesCount() {
  const el = $("#favorites-count");
  if (el) el.textContent = String(state.favorites.length);
}

// ════════════════════════════════════════════════════════════
//  NIVEAU D'APPRENTISSAGE
// ════════════════════════════════════════════════════════════

function setLevel(level, announce = true) {
  if (!LEVELS[level]) return;
  state.level = level;
  try { localStorage.setItem(LEVEL_KEY, level); } catch {}
  $$(".level-option").forEach((btn) => {
    const active = btn.dataset.level === level;
    btn.classList.toggle("active", active);
    if (btn.getAttribute("role") === "radio") btn.setAttribute("aria-checked", active ? "true" : "false");
  });
  const info = $("#settings-level-info");
  if (info) info.textContent = `${currentLevel().hint} ${currentLevel().guidance}`;
  const sidebarBadge = $("#sidebar-level-badge");
  if (sidebarBadge) sidebarBadge.textContent = currentLevel().label;
  if (announce) showVoiceStatus(`Niveau ${currentLevel().label} activé.`, 2400);
}

// ── Utility ──
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);
const uid = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 8);

function esc(text) {
  return String(text || "").replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[ch]));
}

function normalizeWord(value) {
  return String(value || "")
    .replace(/ñ/g, "ɲ")
    .replace(/Ñ/g, "ɲ")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[’‘]/g, "'")
    .trim()
    .toLocaleLowerCase("fr");
}

// Normalisation orthographique & phonétique du soninké (relie kh↔x, ou↔u, ñ/gn/ny↔ɲ, dj↔j, tch↔c)
function normalizeSoninkeOrtho(value) {
  return normalizeWord(value)
    .replace(/kh/g, "x")
    .replace(/ɲ/g, "ny")
    .replace(/ŋ/g, "ng")
    .replace(/gn/g, "ny")
    .replace(/tch/g, "c")
    .replace(/dj/g, "j")
    .replace(/ou/g, "u")
    .replace(/gu(?=[ei])/g, "g")
    .replace(/['\-]/g, "");
}

function parseCSV(text, delimiter = ";") {
  const clean = String(text || "").replace(/^\uFEFF/, "");
  const rows = [];
  let row = [], cell = "", quoted = false;
  for (let i = 0; i < clean.length; i++) {
    const ch = clean[i];
    if (ch === '"') {
      if (quoted && clean[i + 1] === '"') { cell += '"'; i++; }
      else quoted = !quoted;
    } else if (ch === delimiter && !quoted) {
      row.push(cell);
      cell = "";
    } else if ((ch === "\n" || ch === "\r") && !quoted) {
      if (ch === "\r" && clean[i + 1] === "\n") i++;
      row.push(cell);
      cell = "";
      if (row.some((c) => c.trim().length > 0)) rows.push(row);
      row = [];
    } else {
      cell += ch;
    }
  }
  if (cell.length > 0 || row.length > 0) {
    row.push(cell);
    if (row.some((c) => c.trim().length > 0)) rows.push(row);
  }
  if (!rows.length) return [];
  const headers = rows[0].map((h) => h.trim());
  return rows.slice(1).map((values) =>
    Object.fromEntries(headers.map((h, i) => [h, (values[i] || "").trim()]))
  );
}

// Extrait un exemple lisible depuis le champ `exemple_original` du dictionnaire
function extractCleanExample(raw) {
  if (!raw) return "";
  const cleaned = String(raw).replace(/\s+/g, " ").trim();
  if (cleaned.length <= 160) return cleaned;
  return cleaned.slice(0, 157).trim() + "…";
}

// ── Local Storage ──
function loadConversations() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    state.conversations = data ? JSON.parse(data) : [];
  } catch {
    state.conversations = [];
  }
}

function saveConversations() {
  try {
    // Ne pas sérialiser les blob URLs éphémères cassées entre sessions
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state.conversations));
  } catch {}
}

function getConversation(id) {
  return state.conversations.find((c) => c.id === id);
}

function createConversation(title = null) {
  const conv = {
    id: uid(),
    title: title || "Nouvelle discussion",
    messages: [],
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  state.conversations.unshift(conv);
  saveConversations();
  return conv;
}

function deleteConversation(id) {
  state.conversations = state.conversations.filter((c) => c.id !== id);
  saveConversations();
}

// ── Theme (Doré par défaut) ──
function initTheme() {
  const saved = localStorage.getItem(THEME_KEY) || "light";
  applyTheme(saved);
}

function applyTheme(theme) {
  if (theme === "auto") {
    const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    document.documentElement.setAttribute("data-theme", prefersDark ? "dark" : "light");
  } else {
    document.documentElement.setAttribute("data-theme", theme === "dark" ? "dark" : "light");
  }
  try { localStorage.setItem(THEME_KEY, theme); } catch {}
  updateThemeButtons(theme);
}

function updateThemeButtons(theme) {
  $$(".theme-option").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.theme === theme);
  });
}

function toggleTheme() {
  const current = localStorage.getItem(THEME_KEY) || "light";
  applyTheme(current === "light" ? "dark" : "light");
}

// ── Déverrouillage Audio universel (iOS Safari, WKWebView, Android, Desktop) ──
function ensureAudioUnlocked() {
  try {
    if (!state.sharedAudio && typeof Audio !== "undefined") {
      state.sharedAudio = new Audio();
      state.sharedAudio.preload = "auto";
    }
    const AC = window.AudioContext || window.webkitAudioContext;
    if (AC && !state.audioCtx) {
      state.audioCtx = new AC();
    }
    if (state.audioCtx && state.audioCtx.state === "suspended") {
      state.audioCtx.resume().catch(() => {});
    }

  } catch {}
}

// ── Recherche d'un audio WAV intégré exact ou par mot ──
// Toutes les lectures audio passent par cet index unique : la voix de référence.
function findAudioInfo(word) {
  const key = normalizeWord(word);
  if (!key) return null;
  if (state.audioByWord.has(key)) return state.audioByWord.get(key);
  if (state.audioByVariant.has(key)) return state.audioByVariant.get(key);
  const ortho = normalizeSoninkeOrtho(word);
  if (ortho && state.audioByOrtho.has(ortho)) return state.audioByOrtho.get(ortho);
  // Variantes de graphie déjà indexées (variantes lexicales, formes fléchies)
  for (const candidate of audioAliasKeys(word)) {
    if (state.audioByWord.has(candidate)) return state.audioByWord.get(candidate);
    if (state.audioByVariant.has(candidate)) return state.audioByVariant.get(candidate);
    const o = normalizeSoninkeOrtho(candidate);
    if (o && state.audioByOrtho.has(o)) return state.audioByOrtho.get(o);
  }
  return null;
}

function audioAliasKeys(word) {
  const base = normalizeWord(word);
  const keys = new Set();
  if (!base) return [];
  const stem = base.replace(/[- ](ye|nde|ŋe|nke)$/, "");
  if (stem && stem !== base) keys.add(stem);
  if (base.endsWith("'")) keys.add(base.slice(0, -1));
  keys.delete(base);
  return [...keys];
}

// Lecture fiable d'une URL WAV (HTMLAudio réutilisé + secours WebAudio)
function playAudioUrl(url) {
  return new Promise((resolve) => {
    let settled = false;
    const finish = (ok) => {
      if (settled) return;
      settled = true;
      resolve(ok);
    };

    try {
      ensureAudioUnlocked();
      const player = state.sharedAudio || new Audio();
      state.sharedAudio = player;
      state.currentAudio = player;
      player.pause();
      player.src = url;
      player.onended = () => { state.currentAudio = null; finish(true); };
      player.onerror = () => { state.currentAudio = null; playViaWebAudio(url).then(finish); };
      const p = player.play();
      if (p && typeof p.then === "function") {
        p.catch(() => {
          state.currentAudio = null;
          playViaWebAudio(url).then(finish);
        });
      }
      // Garde-fou de sécurité (12s max par segment)
      setTimeout(() => finish(true), 12000);
    } catch {
      playViaWebAudio(url).then(finish);
    }
  });
}

async function playViaWebAudio(url) {
  try {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return false;
    if (!state.audioCtx) state.audioCtx = new AC();
    if (state.audioCtx.state === "suspended") await state.audioCtx.resume();
    let audioBuffer = state.audioBufferCache.get(url);
    if (!audioBuffer) {
      const res = await fetch(url);
      if (!res.ok) return false;
      const arr = await res.arrayBuffer();
      audioBuffer = await state.audioCtx.decodeAudioData(arr);
      state.audioBufferCache.set(url, audioBuffer);
    }
    return await new Promise((resolve) => {
      const src = state.audioCtx.createBufferSource();
      state.activeSource = src;
      src.buffer = audioBuffer;
      src.connect(state.audioCtx.destination);
      src.onended = () => resolve(true);
      src.start(0);
    });
  } catch {
    return false;
  }
}

// ── Lecture des mots & phrases soninké (WAV intégrés prioritaires + phonétique soninké) ──
let activeAudioBtn = null;

function stopActiveAudio() {
  if (state.currentAudio) {
    try { state.currentAudio.pause(); } catch {}
    state.currentAudio = null;
  }
  if (activeAudioBtn) {
    activeAudioBtn.classList.remove("playing");
    activeAudioBtn = null;
  }
}

function stopSpeech() {
  state.speechToken++;
  try { state.activeSource?.stop(); } catch {}
  state.activeSource = null;
  stopActiveAudio();
  $$(".msg-action-btn.speaking").forEach((b) => b.classList.remove("speaking"));
}

// Assemblage de mots entiers attestés : aucune découpe syllabique devinée.
// Les limites acoustiques de syllabes doivent être alignées et validées avant usage.
function buildSoninkePhraseSegments(phrase) {
  const words = String(phrase || "").replace(/[«»"“”.,!?;:()[\]]/g, " ").trim().split(/\s+/).filter(Boolean);
  const segments = [];
  for (let i = 0; i < words.length;) {
    let match = null;
    for (let end = words.length; end > i; end--) {
      const text = words.slice(i, end).join(" ");
      const info = findAudioInfo(text);
      if (info) { match = { type: "audio", text, url: info.url, end }; break; }
    }
    if (!match) return []; // Ne jamais prononcer une phrase tronquée comme complète.
    segments.push(match);
    i = match.end;
  }
  return segments;
}

function audioNotice(text) {
  let node = document.querySelector("#audio-notice");
  if (!node) {
    node = document.createElement("div");
    node.id = "audio-notice";
    node.setAttribute("role", "status");
    document.querySelector("#messages-area").append(node);
  }
  node.textContent = text;
}

async function playWordAudio(word, btn = null) {
  ensureAudioUnlocked();

  // Re-clic sur le même bouton : arrêter
  if (btn && activeAudioBtn === btn) {
    stopSpeech();
    return true;
  }

  stopSpeech();
  const token = state.speechToken;
  if (btn) {
    btn.classList.add("playing");
    activeAudioBtn = btn;
  }

  const segments = buildSoninkePhraseSegments(word);
  let playedAny = false;
  for (const seg of segments) {
    if (token !== state.speechToken) break;
    if (seg.type === "audio") {
      const ok = await playViaWebAudio(seg.url);
      if (ok) playedAny = true;
    }
  }

  if (!segments.length) audioNotice(`Aucun enregistrement de référence pour « ${word} ». Aucune voix de substitution n'est utilisée : l'audio doit être enregistré puis validé.`);
  if (btn && token === state.speechToken && activeAudioBtn === btn) {
    btn.classList.remove("playing");
    activeAudioBtn = null;
  }
  return playedAny;
}

// Extrait les segments disposant déjà d'un audio de référence dans une phrase composée
function extractAvailableAudioSegments(phrase) {
  const words = String(phrase || "").replace(/[«»"“”.,!?;:()[\]]/g, " ").trim().split(/\s+/).filter(Boolean);
  const found = [];
  const seen = new Set();
  for (let i = 0; i < words.length;) {
    let match = null;
    for (let end = Math.min(words.length, i + 4); end > i; end--) {
      const text = words.slice(i, end).join(" ");
      const info = findAudioInfo(text);
      if (info) { match = { text, url: info.url, end }; break; }
    }
    if (match) {
      const k = normalizeWord(match.text);
      if (!seen.has(k)) {
        seen.add(k);
        found.push(match);
      }
      i = match.end;
    } else {
      i++;
    }
  }
  return found;
}

function soninkeForms(markdownText) {
  const text = String(markdownText || "");
  const forms = [];
  for (const m of text.matchAll(/\{\{audio:([^}]+)\}\}/g)) forms.push(m[1]);
  for (const m of text.matchAll(/\{\{pair:([^|}]+)\|/g)) forms.push(m[1]);
  for (const m of text.matchAll(/\*\*([^*]+)\*\*/g)) forms.push(m[1]);
  const unique = [...new Set(forms.map((f) => f.trim()).filter(Boolean))];
  return unique.filter((form) => !isExcludedForm(form) && (findAudioInfo(form) ||
    buildSoninkePhraseSegments(form).length > 0 ||
    PHRASEBOOK.some(p => [p.snk, ...p.alt].some(x => normalizeWord(x) === normalizeWord(form))) ||
    state.entries.some(e => normalizeWord(e.soninke) === normalizeWord(form)) ||
    (form.split(/\s+/).length > 1 && unattestedTokensOf(form).length === 0)));
}

function buildSpeechSegments(text) {
  return soninkeForms(text).flatMap(buildSoninkePhraseSegments);
}

async function speakResponse(text) {
  stopSpeech();
  ensureAudioUnlocked();
  const token = state.speechToken;

  // Les formes {{pair:...}} sont les unités soninké explicitement produites
  // par l'assistant. On les garde dans l'ordre de la réponse, sans lire le français.
  const forms = soninkeForms(text);
  const spoken = new Set();
  let unavailable = 0;
  let played = 0;

  for (const form of forms) {
    if (token !== state.speechToken) return;
    const key = normalizeWord(form);
    if (!key || spoken.has(key)) continue;
    spoken.add(key);

    // Priorité à un enregistrement complet (phrase ou expression), s'il existe.
    const exact = findAudioInfo(form);
    const isMultiword = String(form).trim().split(/\s+/).length > 1;
    const phraseKey = normalizeWord(form);
    const approvedPhrase = PHRASEBOOK.some(p =>
      !/à confirmer|à rechercher|à produire|à valider/i.test(String(p.note || "")) &&
      [p.snk, ...(p.alt || [])].some(candidate => normalizeWord(candidate) === phraseKey)
    ) || state.samples.some(sample => normalizeWord(sample.soninke) === phraseKey);

    // Un enregistrement complet est prioritaire. Sinon, assemblage mot à mot
    // seulement pour une phrase attestée dans le phrasébook/corpus : on ne fabrique
    // pas une phrase grammaticale en juxtaposant arbitrairement des mots connus.
    const segments = exact
      ? [{ type: "audio", text: form, url: exact.url }]
      : (isMultiword && !approvedPhrase)
        ? []
        : buildSoninkePhraseSegments(form);

    // Pas de lecture tronquée : si un seul mot manque, on n'improvise pas le reste.
    if (!segments.length) {
      unavailable++;
      continue;
    }

    for (let i = 0; i < segments.length; i++) {
      if (token !== state.speechToken) return;
      if (!await playViaWebAudio(segments[i].url)) {
        audioNotice("Lecture indisponible : vérifiez le son de l'appareil puis réessayez.");
        return;
      }
      played++;
      // Petite pause entre les mots assemblés ; pause plus longue après une expression.
      if (i < segments.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 110));
      }
    }
    await new Promise(resolve => setTimeout(resolve, 230));
  }

  if (unavailable || !forms.length) {
    audioNotice("Audio de référence manquant pour certaines formes. Aucune prononciation inventée ni voix de substitution : seuls les mots et phrases entièrement couverts par les enregistrements sont lus.");
  } else if (played > 0) {
    audioNotice("Lecture avec les enregistrements de référence disponibles. Les phrases composées sont assemblées mot à mot lorsque aucun audio complet de la phrase n'existe.");
  }
  if (token === state.speechToken) $(".msg-action-btn.speaking").forEach(b => b.classList.remove("speaking"));
}

// Traduction lexicale d'une phrase composée, mot à mot (sans jamais deviner)
function glossSoninkeSpans(form) {
  const words = String(form || "").replace(/[«»"“”.,!?;:()[\]]/g, " ").trim().split(/\s+/).filter(Boolean);
  const parts = [];
  const markerGloss = {
    wa: "inaccompli (action en cours / habituelle)", di: "passé (avec objet)", da: "passé (avec objet)",
    "n'di": "passé (avec objet)", ma: "négation du passé", maxa: "ne… pas (impératif / passé)",
    nta: "négation de l'inaccompli", "yi rini": "futur proche", rini: "futur lointain / à venir",
    "n'ti rini": "négation du futur proche", "n'taxa rini": "négation du futur proche (variante)",
    do: "action en cours", fayi: "en train de", ba: "marque de question",
  };
  let i = 0;
  while (i < words.length) {
    let matched = false;
    for (let end = Math.min(words.length, i + 4); end > i; end--) {
      const span = words.slice(i, end).join(" ");
      const key = normalizeWord(span);
      const entry = state.entries.find((e) => normalizeWord(e.soninke) === key && !isExcludedForm(e.soninke));
      if (entry) { parts.push(`${span} = ${entry.francais.split(";")[0]}`); i = end; matched = true; break; }
      const pron = SONINKE_PRONOUNS.find((p) => p.short === span || p.long === span);
      if (pron) { parts.push(`${span} = ${pron.fr[0]}`); i = end; matched = true; break; }
      if (markerGloss[key] !== undefined) { parts.push(`${span} = ${markerGloss[key]}`); i = end; matched = true; break; }
      const elided = span.match(/^(n'|m'|l'|ŋ')(\S+)$/);
      if (elided) {
        const sub = state.entries.find((e) => normalizeWord(e.soninke) === normalizeWord(elided[2]) && !isExcludedForm(e.soninke));
        if (sub) { parts.push(`${span} = ${sub.francais.split(";")[0]} (avec particule ${elided[1]})`); i = end; matched = true; break; }
      }
    }
    if (!matched) { parts.push(`${words[i]} = (non attesté)`); i++; }
  }
  return parts;
}

function explainFrench(text) {
  const forms = soninkeForms(text);
  return forms.map(form => {
    const key = normalizeWord(form);
    const phrases = PHRASEBOOK.filter(p => [p.snk, ...p.alt].some(x => normalizeWord(x) === key)).map(p => p.fr);
    const meanings = state.entries.filter(e => normalizeWord(e.soninke) === key && !isExcludedForm(e.soninke)).map(e => e.francais);
    const direct = [...new Set([...phrases, ...meanings])];
    if (direct.length) return `${form} → ${direct.join(" ; ")}`;
    if (form.split(/\s+/).length > 1) {
      const parts = glossSoninkeSpans(form);
      if (parts.length) return `${form} →\n  ${parts.join("\n  ")}`;
    }
    return `${form} → Sens non documenté — à vérifier avec le référent.`;
  }).join("\n") || "Aucune forme soninké identifiée dans cette réponse.";
}

function syncVoiceReplyUI() {
  const active = !!state.voiceReplies;
  const btn = $("#voice-reply-btn");
  if (btn) {
    btn.classList.toggle("active", active);
    btn.setAttribute("aria-pressed", active ? "true" : "false");
  }
  const topBtn = $("#topbar-voice-btn");
  const topLbl = $("#topbar-voice-label");
  if (topBtn) {
    topBtn.classList.toggle("active", active);
    topBtn.setAttribute("aria-pressed", active ? "true" : "false");
  }
  if (topLbl) {
    topLbl.textContent = active ? "Voix activée" : "Voix";
  }
  const sw = $("#voice-replies-switch");
  if (sw) sw.setAttribute("aria-checked", active ? "true" : "false");
}

function setVoiceReplies(enabled, announce = true) {
  ensureAudioUnlocked();
  state.voiceReplies = !!enabled;
  try { localStorage.setItem(VOICE_PREF_KEY, state.voiceReplies ? "1" : "0"); } catch {}
  syncVoiceReplyUI();

  if (!state.voiceReplies) {
    stopSpeech();
  }
  if (announce) {
    showVoiceStatus(
      state.voiceReplies
        ? "Lecture vocale activée : chaque réponse sera lue avec la voix de référence lorsqu'un enregistrement existe."
        : "Lecture vocale automatique désactivée. Les boutons Écouter restent actifs.",
      3200
    );
    if (state.voiceReplies) {
      playReferenceSample();
    }
  }
}

// ── Bandeau d'état de l'Assistant Vocal ──
let voiceStatusTimer = null;

function showVoiceStatus(text, autohideMs = 0, withControls = false) {
  const banner = $("#voice-status");
  const label = $("#voice-status-text");
  const actions = $("#voice-panel-actions");
  const timer = $("#voice-timer");
  if (!banner || !label) return;
  label.textContent = text;
  banner.hidden = false;
  if (actions) actions.hidden = !withControls;
  if (timer) timer.hidden = !withControls;
  clearTimeout(voiceStatusTimer);
  if (autohideMs > 0) {
    voiceStatusTimer = setTimeout(hideVoiceStatus, autohideMs);
  }
}

function hideVoiceStatus() {
  const banner = $("#voice-status");
  const actions = $("#voice-panel-actions");
  const timer = $("#voice-timer");
  if (banner) banner.hidden = true;
  if (actions) actions.hidden = true;
  if (timer) timer.hidden = true;
}

// Libellé du bouton micro : action claire à l'écran, pas seulement une icône.
function setMicLabel(listening) {
  const btn = $("#mic-btn");
  const label = $("#mic-label");
  if (label) label.textContent = listening ? "J'écoute" : "Parler";
  if (btn) {
    const text = listening
      ? "Arrêter l'écoute et envoyer le message vocal"
      : "Assistant vocal soninké : parler";
    btn.setAttribute("aria-label", text);
    btn.setAttribute("title", listening
      ? "Écoute en cours — touchez pour arrêter"
      : "Assistant vocal : écouter, enregistrer et répondre en soninké");
    btn.setAttribute("aria-pressed", listening ? "true" : "false");
  }
}

// ── Assistant Vocal Soninké (Écoute + Enregistrement + Réponse en soninké) ──
function getSpeechRecognition() {
  return window.SpeechRecognition || window.webkitSpeechRecognition || null;
}

function updateRecordTimer() {
  const timer = $("#voice-timer");
  if (!timer || !state.recordStartedAt) return;
  const secs = Math.floor((Date.now() - state.recordStartedAt) / 1000);
  const mm = String(Math.floor(secs / 60)).padStart(2, "0");
  const ss = String(secs % 60).padStart(2, "0");
  timer.textContent = `${mm}:${ss}`;
}

function cleanupVoiceResources() {
  clearInterval(state.recordTimerId);
  state.recordTimerId = null;
  state.recordStartedAt = 0;
  if (state.recognition) {
    const r = state.recognition;
    state.recognition = null;
    try { r.onend = null; r.onerror = null; r.stop(); } catch {}
  }
  if (state.mediaStream) {
    try { state.mediaStream.getTracks().forEach((t) => t.stop()); } catch {}
    state.mediaStream = null;
  }
  state.listening = false;
  const mic = $("#mic-btn");
  if (mic) mic.classList.remove("listening", "recording");
  setMicLabel(false);
}

function cancelListening() {
  state.lastTranscript = "";
  if (state.recorder && state.recorder.state === "recording") {
    state.recorder.onstop = null;
    try { state.recorder.stop(); } catch {}
  }
  state.recorder = null;
  state.recordChunks = [];
  cleanupVoiceResources();
  hideVoiceStatus();
}

function finishVoiceSession() {
  if (!state.listening) return;
  const typedOrSpoken = ($("#message-input").value || state.lastTranscript || "").trim();
  const hasRecorder = state.recorder && state.recorder.state === "recording";

  if (hasRecorder) {
    const rec = state.recorder;
    state.recorder = null;
    rec.onstop = () => {
      let voiceUrl = null;
      if (state.recordChunks.length > 0 && typeof Blob !== "undefined" && typeof URL !== "undefined" && URL.createObjectURL) {
        try {
          const blob = new Blob(state.recordChunks, { type: rec.mimeType || "audio/mp4" });
          if (blob.size > 0) voiceUrl = URL.createObjectURL(blob);
        } catch {}
      }
      state.recordChunks = [];
      cleanupVoiceResources();
      hideVoiceStatus();
      deliverVoiceTurn(typedOrSpoken, voiceUrl);
    };
    try {
      rec.stop();
      return;
    } catch {}
  }

  cleanupVoiceResources();
  hideVoiceStatus();
  deliverVoiceTurn(typedOrSpoken, null);
}

function deliverVoiceTurn(transcript, voiceNoteUrl) {
  const cleanText = String(transcript || "").trim();
  if (cleanText) {
    submitMessage(cleanText, { forceVoiceReply: true, voiceNoteUrl });
  } else if (voiceNoteUrl) {
    sendRecordedVoiceMessage(voiceNoteUrl);
  } else {
    showVoiceStatus("Aucun son détecté. Parlez près du micro ou écrivez votre question.", 3200);
  }
}

async function startListening() {
  ensureAudioUnlocked();
  stopSpeech();

  state.listening = true;
  state.lastTranscript = "";
  state.recordChunks = [];
  state.recordStartedAt = Date.now();
  updateRecordTimer();
  state.recordTimerId = setInterval(updateRecordTimer, 500);

  const mic = $("#mic-btn");
  const input = $("#message-input");
  if (mic) mic.classList.add("listening");
  setMicLabel(true);
  showVoiceStatus("J'écoute et j'enregistre. Parlez en français ou en soninké.", 0, true);

  let hasAnyCapture = false;

  // 1. Démarrer l'enregistrement vocal réel (MediaRecorder) si supporté
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia && typeof MediaRecorder !== "undefined") {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (!state.listening) {
        stream.getTracks().forEach((t) => t.stop());
        return;
      }
      state.mediaStream = stream;
      let options = undefined;
      if (typeof MediaRecorder.isTypeSupported === "function") {
        for (const mime of ["audio/mp4", "audio/webm;codecs=opus", "audio/webm", "audio/ogg"]) {
          if (MediaRecorder.isTypeSupported(mime)) { options = { mimeType: mime }; break; }
        }
      }
      const recorder = options ? new MediaRecorder(stream, options) : new MediaRecorder(stream);
      state.recorder = recorder;
      recorder.ondataavailable = (ev) => {
        if (ev.data && ev.data.size > 0) state.recordChunks.push(ev.data);
      };
      recorder.start(250);
      hasAnyCapture = true;
      if (mic) mic.classList.add("recording");
    } catch {
      // L'utilisateur ou le navigateur n'a pas ouvert MediaRecorder — on tente SpeechRecognition seul
    }
  }

  // 2. Démarrer la reconnaissance vocale en direct en parallèle
  const SR = getSpeechRecognition();
  if (SR && state.listening) {
    try {
      const recognition = new SR();
      state.recognition = recognition;
      recognition.lang = "fr-FR";
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.maxAlternatives = 2;

      recognition.onresult = (event) => {
        let transcript = "";
        for (let i = 0; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        state.lastTranscript = transcript.trim();
        if (state.lastTranscript) {
          input.value = state.lastTranscript;
          autoResize(input);
          updateSendButton();
          showVoiceStatus(`« ${state.lastTranscript} »`, 0, true);
        }
        if (event.results[event.results.length - 1].isFinal && state.lastTranscript) {
          finishVoiceSession();
        }
      };

      recognition.onerror = (e) => {
        // Si MediaRecorder enregistre déjà, on continue l'enregistrement vocal sans couper !
        if (state.recorder && state.recorder.state === "recording") {
          showVoiceStatus("Enregistrement en cours. Appuyez sur Envoyer quand vous avez terminé.", 0, true);
          return;
        }
        cleanupVoiceResources();
        if (e.error === "not-allowed") {
          showVoiceStatus("Autorisez l'accès au microphone dans les réglages du navigateur.", 4200);
        } else {
          showVoiceStatus("Touchez à nouveau le micro et parlez clairement.", 3400);
        }
      };

      recognition.onend = () => {
        if (state.listening && state.lastTranscript) {
          finishVoiceSession();
        } else if (state.listening && !(state.recorder && state.recorder.state === "recording")) {
          cleanupVoiceResources();
          showVoiceStatus("Écoute terminée. Touchez le micro pour reparler.", 2800);
        }
      };

      recognition.start();
      hasAnyCapture = true;
    } catch {}
  }

  if (!hasAnyCapture) {
    cleanupVoiceResources();
    showVoiceStatus("Lecture vocale activée. Écrivez votre question : la réponse sera lue avec la voix de référence.", 4200);
    setVoiceReplies(true, false);
    input.focus();
  }
}

// ── Moteur linguistique & recherche sur 100% des données du dépôt ──
function levenshtein(a, b) {
  if (a === b) return 0;
  if (!a.length) return b.length;
  if (!b.length) return a.length;
  let prev = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    const curr = [i];
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      curr[j] = Math.min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost);
    }
    prev = curr;
  }
  return prev[b.length];
}

// Formes canoniques françaises courantes (pluriels, féminins, conjugaisons usuelles)
const FR_IRREGULAR_MAP = {
  "suis": "être", "es": "être", "est": "être", "sommes": "être", "etes": "être", "sont": "être", "etais": "être", "etait": "être", "etaient": "être", "ete": "être",
  "ai": "avoir", "as": "avoir", "a": "avoir", "avons": "avoir", "avez": "avoir", "ont": "avoir", "avais": "avoir", "avait": "avoir", "avaient": "avoir", "eu": "avoir",
  "vais": "aller", "vas": "aller", "va": "aller", "allons": "aller", "allez": "aller", "vont": "aller", "allais": "aller", "allait": "aller", "alle": "aller", "allee": "aller", "alles": "aller", "allees": "aller", "irai": "aller", "iras": "aller", "ira": "aller", "irons": "aller", "irez": "aller", "iront": "aller",
  "pars": "partir", "part": "partir", "partons": "partir", "partez": "partir", "partent": "partir", "partais": "partir", "partait": "partir", "parti": "partir", "partie": "partir", "partis": "partir", "parties": "partir", "partirai": "partir", "partiras": "partir", "partira": "partir", "partirons": "partir", "partirez": "partir", "partiront": "partir",
  "viens": "venir", "vient": "venir", "venons": "venir", "venez": "venir", "viennent": "venir", "venais": "venir", "venait": "venir", "venu": "venir", "venue": "venir", "venus": "venir", "venues": "venir", "viendrai": "venir", "viendras": "venir", "viendra": "venir", "viendrons": "venir", "viendrez": "venir", "viendront": "venir",
  "bois": "boire", "boit": "boire", "buvons": "boire", "buvez": "boire", "boivent": "boire", "buvais": "boire", "buvait": "boire", "bu": "boire", "bue": "boire", "boirai": "boire", "boiras": "boire", "boira": "boire", "boirons": "boire", "boirez": "boire", "boiront": "boire",
  "vois": "voir", "voit": "voir", "voyons": "voir", "voyez": "voir", "voient": "voir", "voyais": "voir", "voyait": "voir", "vu": "voir", "vue": "voir", "verrai": "voir", "verras": "voir", "verra": "voir", "verrons": "voir", "verrez": "voir",
  "prends": "prendre", "prend": "prendre", "prenons": "prendre", "prenez": "prendre", "prennent": "prendre", "prenais": "prendre", "prenait": "prendre", "pris": "prendre", "prise": "prendre", "prendrai": "prendre", "prendras": "prendre", "prendra": "prendre",
  "comprends": "comprendre", "comprend": "comprendre", "comprenons": "comprendre", "comprenez": "comprendre", "comprennent": "comprendre", "compris": "comprendre",
  "apprends": "apprendre", "apprend": "apprendre", "apprenons": "apprendre", "apprenez": "apprendre", "apprennent": "apprendre", "appris": "apprendre",
  "dors": "dormir", "dort": "dormir", "dormons": "dormir", "dormez": "dormir", "dorment": "dormir", "dormais": "dormir", "dormait": "dormir", "dormi": "dormir", "dormirai": "dormir", "dormira": "dormir",
  "ecris": "ecrire", "ecrit": "ecrire", "ecrivons": "ecrire", "ecrivez": "ecrire", "ecrivent": "ecrire", "ecrivais": "ecrire", "ecrivait": "ecrire", "ecrirai": "ecrire", "ecrira": "ecrire",
  "dis": "dire", "dit": "dire", "disons": "dire", "dites": "dire", "disent": "dire", "disais": "dire", "disait": "dire", "dirai": "dire", "dira": "dire",
  "mets": "mettre", "met": "mettre", "mettons": "mettre", "mettez": "mettre", "mettent": "mettre", "mis": "mettre", "mise": "mettre",
  "promets": "promettre", "promet": "promettre", "promis": "promettre",
  "ouvres": "ouvrir", "ouvre": "ouvrir", "ouvrons": "ouvrir", "ouvrez": "ouvrir", "ouvrent": "ouvrir", "ouvert": "ouvrir", "ouverte": "ouvrir",
  "offres": "offrir", "offre": "offrir", "offrons": "offrir", "offrez": "offrir", "offrent": "offrir", "offert": "offrir", "offerte": "offrir",
  "cours": "courir", "court": "courir", "courons": "courir", "courez": "courir", "courent": "courir", "couru": "courir", "courrai": "courir", "courra": "courir",
  "veux": "vouloir", "veut": "vouloir", "voulons": "vouloir", "voulez": "vouloir", "veulent": "vouloir", "voulais": "vouloir", "voulait": "vouloir", "voulu": "vouloir", "voudrai": "vouloir", "voudra": "vouloir",
  "peux": "pouvoir", "peut": "pouvoir", "pouvons": "pouvoir", "pouvez": "pouvoir", "peuvent": "pouvoir", "pu": "pouvoir",
  "sais": "savoir", "sait": "savoir", "savons": "savoir", "savez": "savoir", "savent": "savoir", "su": "savoir",
  "connais": "connaitre", "connait": "connaitre", "connaissons": "connaitre", "connaissez": "connaitre", "connaissent": "connaitre", "connu": "connaitre",
  "vends": "vendre", "vend": "vendre", "vendons": "vendre", "vendez": "vendre", "vendent": "vendre", "vendu": "vendre",
  "attends": "attendre", "attend": "attendre", "attendons": "attendre", "attendez": "attendre", "attendent": "attendre", "attendu": "attendre",
  "entends": "entendre", "entend": "entendre", "entendons": "entendre", "entendez": "entendre", "entendent": "entendre", "entendu": "entendre",
  "reponds": "repondre", "repond": "repondre", "repondons": "repondre", "repondez": "repondre", "repondent": "repondre", "repondu": "repondre",
  "descends": "descendre", "descend": "descendre", "descendons": "descendre", "descendez": "descendre", "descendent": "descendre", "descendu": "descendre", "descendue": "descendre",
  "perds": "perdre", "perd": "perdre", "perdons": "perdre", "perdez": "perdre", "perdent": "perdre", "perdu": "perdre",
  "mords": "mordre", "mord": "mordre", "mordons": "mordre", "mordez": "mordre", "mordent": "mordre", "mordu": "mordre",
  "bats": "battre", "bat": "battre", "battons": "battre", "battez": "battre", "battent": "battre", "battu": "battre",
  "combats": "combattre", "combat": "combattre", "combattu": "combattre",
  "traduis": "traduire", "traduit": "traduire", "traduisons": "traduire", "traduisez": "traduire", "traduisent": "traduire",
  "ris": "rire", "rit": "rire", "rions": "rire", "riez": "rire", "rient": "rire", "ri": "rire",
  "assois": "asseoir", "assoit": "asseoir", "assieds": "asseoir", "assied": "asseoir", "asseyons": "asseoir", "asseyez": "asseoir", "assoient": "asseoir", "assis": "asseoir", "assise": "asseoir",
  "couds": "coudre", "coud": "coudre", "cousons": "coudre", "cousez": "coudre", "cousent": "coudre", "cousu": "coudre",
  "eteins": "eteindre", "eteint": "eteindre", "eteignons": "eteindre", "eteignez": "eteindre", "eteignent": "eteindre",
  "crains": "craindre", "craint": "craindre", "craignons": "craindre", "craignez": "craindre", "craignent": "craindre",
  "fais": "faire", "fait": "faire", "faisons": "faire", "faites": "faire", "font": "faire", "ferai": "faire", "fera": "faire",
  "dois": "devoir", "doit": "devoir", "devons": "devoir", "devez": "devoir", "doivent": "devoir", "du": "devoir",
  "lis": "lire", "lit": "lire", "lisons": "lire", "lisez": "lire", "lisent": "lire", "lu": "lire",
  "vis": "vivre", "vit": "vivre", "vivons": "vivre", "vivez": "vivre", "vivent": "vivre", "vecu": "vivre",
  "nais": "naitre", "nait": "naitre", "naissons": "naitre", "naissent": "naitre", "ne": "naitre", "nee": "naitre",
  "suis_v": "suivre",
  "yeux": "œil", "chevaux": "cheval", "enfants": "enfant", "femmes": "femme", "hommes": "homme",
  "maisons": "maison", "jours": "jour", "mots": "mot", "parents": "père", "mamans": "mère", "papas": "papa",
  "livres": "livre", "cahiers": "cahier", "lettres": "lettre", "villages": "village", "marches": "marche",
  "oiseaux": "oiseau", "animaux": "animal", "fruits": "fruit", "arbres": "arbre", "chiens": "chien",
  "poissons": "poisson", "dents": "dent", "mains": "main", "pieds": "pied", "etoiles": "etoile", "nuages": "nuage",
  "freres": "frere", "soeurs": "soeur", "epouses": "epouse", "familles": "famille", "ecoles": "ecole",
};

function candidateWordForms(rawTerm) {
  const n = normalizeWord(rawTerm);
  const forms = new Set([n]);
  const pushVerbForms = (stem) => {
    if (!stem || stem.length < 2) return;
    forms.add(stem + "er");
    forms.add(stem + "re");
    forms.add(stem + "ir");
    if (/[eiué]$/.test(stem)) forms.add(stem + "r");
  };
  if (FR_IRREGULAR_MAP[n]) forms.add(normalizeWord(FR_IRREGULAR_MAP[n]));
  if (n.length > 3 && n.endsWith("s")) forms.add(n.slice(0, -1));
  if (n.length > 3 && n.endsWith("x")) forms.add(n.slice(0, -1));
  if (n.length > 6 && n.endsWith("aient")) pushVerbForms(n.slice(0, -5));
  if (n.length > 5 && (n.endsWith("ais") || n.endsWith("ait") || n.endsWith("ant"))) pushVerbForms(n.slice(0, -3));
  if (n.length > 5 && (n.endsWith("ions") || n.endsWith("iez"))) pushVerbForms(n.slice(0, -4));
  if (n.length > 4 && (n.endsWith("erai") || n.endsWith("eras") || n.endsWith("erez"))) forms.add(n.replace(/(rai|ras|rez)$/, "re"));
  if (n.length > 4 && /(rai|ras|ra|rons|rez|ront)$/.test(n)) forms.add(n.replace(/(rai|ras|ra|rons|rez|ront)$/, "re"));
  if (n.length > 4 && n.endsWith("es")) { forms.add(n.slice(0, -2)); pushVerbForms(n.slice(0, -2)); }
  if (n.length > 4 && n.endsWith("ent")) pushVerbForms(n.slice(0, -3));
  if (n.length > 4 && n.endsWith("ons")) pushVerbForms(n.slice(0, -3));
  if (n.length > 4 && n.endsWith("ez")) pushVerbForms(n.slice(0, -2));
  if (n.length > 4 && (n.endsWith("ee") || n.endsWith("ees"))) forms.add(n.replace(/ees?$/, "er"));
  if (n.length > 3 && n.endsWith("e")) { forms.add(n.slice(0, -1) + "er"); forms.add(n.slice(0, -1)); forms.add(n.slice(0, -1) + "r"); }
  if (n.length > 4 && (n.endsWith("is") || n.endsWith("it"))) { forms.add(n.slice(0, -1)); forms.add(n.slice(0, -2)); }
  // Suffixes morphologiques soninké courants (-ke défini, -nu/-u pluriel, -nde/-ye/-ni)
  if (n.length > 4 && (n.endsWith("-nde") || n.endsWith("-ye"))) forms.add(n.replace(/-(nde|ye)$/, ""));
  if (n.length > 4 && n.endsWith("ni")) forms.add(n.slice(0, -2));
  if (n.length > 4 && n.endsWith("nu")) forms.add(n.slice(0, -2));
  // Chaque forme dérivée repasse par la table des verbes irréguliers (viendras → viendra → venir)
  for (const f of [...forms]) {
    if (FR_IRREGULAR_MAP[f]) forms.add(normalizeWord(FR_IRREGULAR_MAP[f]));
  }
  return [...forms].filter(Boolean);
}

// Score de priorité lexicale : référent + audio > référent > corpus + audio > source externe
const PREFERRED_SONINKE_LEMMAS = new Set([
  "ka", "saxa", "maro", "maro ke", "lemine", "lemine ke", "xati", "xati ke", "lettra", "lettra ke",
  "baaba", "saaxe", "yaxare", "yake", "yugo", "kiine", "kore", "debe", "yigande", "kissima",
  "daga", "ri", "yige", "mini", "sefe", "goli", "safa", "wori", "faye", "xanu", "wutu", "dema",
  "muru", "sore", "taxu", "kunyi", "suge", "rege", "wu", "tuma", "ko", "ku", "tu", "faamu",
  "wurebandi", "mula", "xobo", "gage", "kini", "ji", "tiye", "nexe", "kitabe", "kaye", "lekolu",
  "lenki", "daru", "kumbene", "koota su", "waxati su", "abada", "kere", "no"
]);

function scoreCorpusEntry(entry, directKey = "") {
  if (!entry) return -999;
  if (isExcludedForm(entry.soninke)) return -500;
  let score = 0;
  const snkNorm = normalizeWord(entry.soninke);
  const frNorm = normalizeWord(entry.francais);
  const statut = String(entry.statut || "");
  if (directKey && snkNorm === directKey) score += 1000;
  if (directKey && frNorm === directKey) score += 120;
  if (/valide_par_referent|fourni_par_referent/i.test(statut)) score += 60;
  else if (!entry.isCandidate && !/a_verifier|externe/i.test(statut)) score += 30;
  else score -= 15;
  if (findAudioInfo(entry.soninke)) score += 35;
  if (PREFERRED_SONINKE_LEMMAS.has(snkNorm)) score += 28;
  if (/verbe_gerondif|nom_d_action/i.test(entry.categorie || "") && (!directKey || snkNorm !== directKey)) score -= 18;
  return score;
}

// Meilleure entrée attestée d'une recherche lexicale, filtrable par catégorie
// opts.definite : privilégie la forme définie attestée « … ke » (le riz → maro ke, l'enfant → lemine ke)
// opts.directKey : le mot recherché (renforce exactement le sens demandé et écarte le bruit des exemples)
// opts.strictContent : n'accepte que les correspondances exactes/proches (jamais le fouilli des exemples)
function bestSoninkeEntry(lookup, preferredCategory = "", opts = {}) {
  const pool = (opts.strictContent
    ? [...(lookup?.exact || []), ...(lookup?.starts || [])]
    : [...(lookup?.exact || []), ...(lookup?.starts || []), ...(lookup?.contains || [])]
  ).filter((e) => e && !isExcludedForm(e.soninke));
  if (!pool.length) return null;
  const catRegex = preferredCategory ? new RegExp(preferredCategory, "i") : null;
  const primary = catRegex ? pool.filter((e) => catRegex.test(e.categorie || "")) : pool;
  const directKey = normalizeWord(opts.directKey || "");
  const ranked = (primary.length ? primary : pool).slice()
    .sort((a, b) => scoreCorpusEntry(b, directKey) - scoreCorpusEntry(a, directKey));
  if (opts.definite) {
    const def = ranked.find((e) => /\s+ke$/i.test(String(e.soninke).trim()) && /referent/i.test(String(e.statut || "")));
    if (def) return def;
  }
  return ranked[0] || null;
}

function splitSenses(francais) {
  return String(francais || "")
    .split(/[;/,]/)
    .map((s) => normalizeWord(s.replace(/\([^)]*\)/g, "")))
    .filter(Boolean);
}

function lookupTerm(term) {
  const directKey = normalizeWord(term);
  const forms = candidateWordForms(term);
  const ortho = normalizeSoninkeOrtho(term);
  const exactDirect = [], exactStemmed = [], starts = [], contains = [];

  for (const e of state.entries) {
    if (isExcludedForm(e.soninke)) continue;
    const snk = normalizeWord(e.soninke);
    const snkOrtho = normalizeSoninkeOrtho(e.soninke);
    const frFull = normalizeWord(e.francais);
    const frBare = frFull.replace(/^(?:le\s|la\s|les\s|un\s|une\s|l'|d'|du\s|des\s|de la\s|de\s)/, "");
    const senses = splitSenses(e.francais);
    const variants = String(e.variantes || "").split(/[;,|]/).map(normalizeWord).filter(Boolean);

    if (snk === directKey || frFull === directKey || variants.includes(directKey)) {
      exactDirect.push(e);
      continue;
    }

    const isExact =
      forms.some((f) => snk === f || frFull === f || frBare === f || senses.includes(f) || variants.includes(f)) ||
      (ortho.length >= 2 && snkOrtho === ortho);

    if (isExact) {
      exactStemmed.push(e);
      continue;
    }

    const allTokens = [
      ...snk.split(/\s+/),
      ...frFull.split(/[\s,;()/']+/),
      ...frBare.split(/[\s,;()/']+/),
      ...variants.flatMap((v) => v.split(/\s+/)),
    ].filter(Boolean);

    if (forms.some((f) => f.length >= 2 && (snk.startsWith(f) || frFull.startsWith(f) || frBare.startsWith(f) || allTokens.includes(f)))) {
      starts.push(e);
    } else if (forms.some((f) => f.length >= 3 && (snk.includes(f) || frFull.includes(f) || frBare.includes(f) || normalizeWord(e.exemple_original || "").includes(f)))) {
      contains.push(e);
    }
  }

  exactDirect.sort((a, b) => scoreCorpusEntry(b, directKey) - scoreCorpusEntry(a, directKey));
  exactStemmed.sort((a, b) => scoreCorpusEntry(b, directKey) - scoreCorpusEntry(a, directKey));
  starts.sort((a, b) => scoreCorpusEntry(b, directKey) - scoreCorpusEntry(a, directKey));
  contains.sort((a, b) => scoreCorpusEntry(b, directKey) - scoreCorpusEntry(a, directKey));

  const exact = [...exactDirect, ...exactStemmed];
  return {
    exact: exact.slice(0, 10),
    starts: starts.slice(0, 8),
    contains: contains.slice(0, 8),
  };
}

function lookupPhrasebook(term) {
  const forms = candidateWordForms(term);
  const ortho = normalizeSoninkeOrtho(term);
  const matched = PHRASEBOOK.filter((p) => {
    const frN = normalizeWord(p.fr);
    const snkN = normalizeWord(p.snk);
    const snkO = normalizeSoninkeOrtho(p.snk);
    return (
      forms.some((f) => frN === f || snkN === f || p.alt.some((a) => normalizeWord(a) === f)) ||
      (ortho.length >= 3 && (snkO === ortho || p.alt.some((a) => normalizeSoninkeOrtho(a) === ortho)))
    );
  });
  const bySnk = new Map();
  for (const p of matched) {
    const k = normalizeWord(p.snk);
    if (!bySnk.has(k)) {
      bySnk.set(k, { snk: p.snk, fr: p.fr, alt: [...p.alt], note: p.note });
    } else {
      const existing = bySnk.get(k);
      const frSet = new Set(existing.fr.split(",").map((s) => normalizeWord(s)));
      if (!frSet.has(normalizeWord(p.fr))) existing.fr += `, ${p.fr}`;
      for (const a of p.alt) {
        if (!existing.alt.some((x) => normalizeWord(x) === normalizeWord(a))) existing.alt.push(a);
      }
    }
  }
  return [...bySnk.values()];
}

// ════════════════════════════════════════════════════════════
//  GRAMMAIRE SONINKÉ — composition de phrases à partir du lexique
//  (Sujet + Auxiliaire/Marqueur + Objet + Verbe / Sujet + Verbe + Complément)
//  Chaque forme produite n'utilise QUE des mots attestés du corpus ;
//  tout mot absent est signalé explicitement, jamais inventé.
// ════════════════════════════════════════════════════════════

function capitalizeFirst(text) {
  const s = String(text || "").trim();
  return s ? s[0].toUpperCase() + s.slice(1) : s;
}

const SONINKE_PRONOUNS = [
  { person: "1s", fr: ["je", "j'"],          short: "n",  long: "nke",  longAccent: "nké" },
  { person: "2s", fr: ["tu", "t'"],          short: "an", long: "anke", longAccent: "anké" },
  { person: "3s", fr: ["il", "elle", "on"],  short: "a",  long: "ake",  longAccent: "aké" },
  { person: "1p", fr: ["nous"],              short: "o",  long: "oku",  longAccent: "oku" },
  { person: "2p", fr: ["vous"],              short: "xa", long: "xaku", longAccent: "xaku" },
  { person: "3p", fr: ["ils", "elles"],      short: "i",  long: "iku",  longAccent: "iku" },
];

// Marqueurs attestés dans le corpus (SNK-GRM-0013..0033 du lexique)
const SONINKE_TENSE_RULES = {
  imperfective:    { aux: "wa",        label: "inaccompli (présent habituel / action en cours)", detail: "wa + verbe en -ni/-na/-ne/-no/-nu" },
  past:            { aux: "n'di",      label: "accompli (passé)",                                detail: "n'di / da + objet + n' + verbe à sa base" },
  future:          { aux: "yi rini",   label: "futur proche",                                    detail: "yi rini + verbe à sa base" },
  futureFar:       { aux: "rini",      label: "futur lointain",                                  detail: "rini + verbe à sa base" },
  imperfectiveNeg: { aux: "nta",       label: "négation de l'inaccompli",                        detail: "nta + verbe en -ni/-na/-ne/-no/-nu" },
  pastNeg:         { aux: "ma",        label: "négation du passé",                               detail: "ma + verbe à sa base (variante attestée : maxa)" },
  futureNearNeg:   { aux: "n'ti rini", label: "négation du futur proche",                        detail: "n'ti rini (variante : n'taxa rini) + verbe en -ni/-na/-ne/-no/-nu" },
};

// Particule nasale n' devant le verbe à l'accompli transitif (attesté : « Anké n'di maro n'yiga »)
// m' devant b/f/m, l' devant r, ŋ' devant w (SNK-GRM-0028..0031)
function combineNasalParticle(verb) {
  const w = String(verb || "").trim();
  if (!w) return "";
  if (/^[bfm]/i.test(w)) return "m'" + w;
  if (/^r/i.test(w)) return "l'" + w;
  if (/^w/i.test(w)) return "ŋ'" + w;
  return "n'" + w;
}

// Forme inaccomplie attestée : daga → dagana, yige → yigene, mini → minini…
function imperfectiveFormOf(verbBare) {
  const snk = String(verbBare || "").trim();
  if (!snk) return "";
  const snkNorm = normalizeWord(snk);
  for (const e of state.entries) {
    if (!/verbe_gerondif/i.test(e.categorie || "")) continue;
    // Le français d'un gérondif suit le motif « … (gérondif / inaccompli de VERBE) » :
    // correspondance EXACTE du radical pour ne pas confondre ri → riti.
    const m = normalizeWord(e.francais || "").match(/inaccompli de ([a-zàâäçéèêëîïôöùûüœ' -]+)\)?\s*$/i);
    if (m && m[1].trim() === snkNorm) return String(e.soninke).trim();
  }
  // Règle régulière attestée : verbe + n + voyelle finale (daga→dagana, ri→rini, mini→minini)
  const m = snkNorm.match(/[aeiou]$/);
  if (m) return snk + "n" + m[0];
  return snk + "ni";
}

// Jeton autorisé dans une phrase composée : attesté, pronom, marqueur ou forme élidée n'/m'/l'/ŋ'
function isComposedTokenAttested(token) {
  const tok = String(token || "").trim();
  if (!tok) return false;
  if (isAttestedSoninkeSpan(tok)) return true;
  if (SONINKE_PRONOUNS.some((p) => p.short === tok || p.long === tok)) return true;
  if (["wa", "di", "da", "ma", "maxa", "nta", "do", "fayi", "ba"].includes(tok)) return true;
  const elided = tok.match(/^(n'|m'|l'|ŋ')(\S+)$/);
  if (elided) {
    if (["di", "da"].includes(elided[2])) return true;
    if (isAttestedSoninkeSpan(elided[2])) return true;
  }
  return false;
}

// Vérifie que chaque segment d'une phrase composée est attesté dans le corpus
function unattestedTokensOf(sentence) {
  const segs = String(sentence || "").replace(/[«»"“”.,!?;:()[\]]/g, " ").trim().split(/\s+/).filter(Boolean);
  const missing = [];
  let i = 0;
  while (i < segs.length) {
    let matched = false;
    for (let end = Math.min(segs.length, i + 4); end > i; end--) {
      if (isComposedTokenAttested(segs.slice(i, end).join(" "))) { i = end; matched = true; break; }
    }
    if (!matched) { missing.push(segs[i]); i++; }
  }
  return missing;
}

// ── Analyse grammaticale d'une phrase française simple ──
const FR_SUBJECT_PRONOUN_RE = /^(je|j'|tu|t'|il|elle|on|nous|vous|ils|elles)\s+/i;
const FR_NP_SUBJECT_RE = /^(?:(le|la|les|un|une|du|de la|des|mon|ma|mes|ton|ta|tes|son|sa|ses|notre|nos|votre|vos|leur|leurs)\s+|(l'|d'))([a-zàâäçéèêëîïôöùûüœ]+(?:\s+[a-zàâäçéèêëîïôöùûüœ]+)?)\s+(?=\S)/i;
const FR_FUT_PERIPH_RE = /^(?:vais|vas|va|allons|allez|vont)\s+(.+)$/i;
const FR_PAST_AVOIR_RE = /^(?:ai|as|a|avons|avez|ont)\s+(.+)$/i;
const FR_PAST_ETRE_RE = /^(?:suis|es|est|sommes|etes|sont|étais|était|étaient)\s+(.+)$/i;
const FR_FUT_SIMPLE_RE = /^([a-zàâäçéèêëîïôöùûüœ]{2,}?)(?:rai|ras|ra|rons|rez|ront)$/i;
const FR_IMPF_SIMPLE_RE = /^([a-zàâäçéèêëîïôöùûüœ]{2,}?)(?:ais|ait|ions|iez|aient)$/i;
const FR_TIME_LIST = ["tous les jours", "chaque jour", "aujourd'hui", "demain", "hier", "toujours", "jamais", "maintenant"];
const FR_DET_TOKEN_RE = /^(le|la|les|un|une|du|de|des|mon|ma|mes|ton|ta|tes|son|sa|ses|ce|cette|ces|au|aux)$/i;
const FR_OBJ_PRONOUNS = new Set(["le", "la", "les", "l'", "lui", "leur", "me", "m'", "te", "t'", "se", "s'", "nous", "vous", "y", "en"]);
const FR_SKIP_TOKENS = new Set(["ne", "n'", "n'a", "pas", "plus", "se", "s'", "me", "m'", "te", "t'", "lui", "leur", "y", "en", "le", "la", "les", "l'"]);

function lookupFrenchNounPhrase(tokens, maxLen = 2, opts = {}) {
  // On privilégie d'abord le nom simple (évite d'avaler l'auxiliaire ou l'adjectif)
  for (let len = 1; len <= Math.min(maxLen, tokens.length); len++) {
    const piece = tokens.slice(0, len).join(" ");
    const entry = bestSoninkeEntry(lookupTerm(piece), "nom|syntagme|lexeme|partie_du_corps|expression|numéral|nombre", { ...opts, directKey: piece, strictContent: true });
    if (entry && /nom|syntagme|lexeme|partie_du_corps|expression|numeral|nombre/i.test(entry.categorie || "")) {
      return { entry, length: len, text: piece };
    }
  }
  return null;
}

function lookupFrenchVerbToken(token) {
  if (!token || FR_SKIP_TOKENS.has(token)) return null;
  const seen = new Set();
  for (const form of [token, ...candidateWordForms(token)]) {
    const key = normalizeWord(form);
    if (!key || seen.has(key)) continue;
    seen.add(key);
    const entry = bestSoninkeEntry(lookupTerm(key), "", { directKey: key, strictContent: true });
    if (entry && /verbe/i.test(entry.categorie || "") && !/verbe_gerondif|nom_d_action/i.test(entry.categorie || "")) {
      return { entry, form: key };
    }
  }
  return null;
}

function hasFrenchVerb(text) {
  return String(text || "").split(/\s+/).some((tok) => !!lookupFrenchVerbToken(tok));
}

// Un complément de lieu n'est accepté que si la partie nommée existe dans le lexique
function hasFrenchNounGuess(text) {
  const tokens = String(text || "").split(/\s+/).filter(Boolean);
  return tokens.some((tok) => FR_DET_TOKEN_RE.test(tok) || /^(l'|d')/.test(tok) || !!lookupFrenchNounPhrase([tok.replace(/^(l'|d')/, "")], 1));
}

// Reconstitue l'infinitif à partir d'une forme fléchie (mangera → manger, parlait → parler)
function stripFrenchInflection(token, regex) {
  const m = String(token || "").match(regex);
  if (!m) return null;
  return lookupFrenchVerbToken(String(token).match(regex)[0]);
}

function stripLeadingArticle(text) {
  return String(text || "")
    .replace(/^(?:le|la|les|un|une|du|de la|des|de)\s+/i, "")
    .replace(/^(?:l'|d')/i, "")
    .trim();
}

function parseFrenchStructure(text) {
  const original = String(text || "").trim().replace(/[?!.…]+$/, "");
  if (!original) return null;
  const g = {
    original,
    subjectPronoun: null,
    subjectEntry: null,
    verbWord: null,
    verbEntry: null,
    objectWord: null,
    objectEntry: null,
    objectPronoun: false,
    adjectiveEntry: null,
    placeWord: null,
    placeEntry: null,
    complementWord: null,
    complementEntry: null,
    timeWord: null,
    timeEntry: null,
    negation: false,
    tense: "imperfective",
    interrogative: /[?]\s*$/.test(String(text).trim()) || /^(?:est-ce que|qu'est-ce que)\b/i.test(normalizeWord(text)),
    copuleMissing: false,
  };

  let work = normalizeWord(original).replace(/^(?:est-ce que|qu'est-ce que)\s+/i, "");

  // 1. Sujet : pronom (courte ou élidée) puis groupe nominal attesté
  const subjM = work.match(FR_SUBJECT_PRONOUN_RE);
  if (subjM) {
    const key = subjM[1].replace(/'/g, "e").toLowerCase();
    g.subjectPronoun = SONINKE_PRONOUNS.find((p) => p.fr.some((f) => f.replace(/'/g, "e") === key)) || null;
    work = work.slice(subjM[0].length).trim();
  } else {
    const npM = work.match(FR_NP_SUBJECT_RE);
    if (npM) {
      const definite = /^(le|la|les|l')/i.test(npM[1] || npM[2] || "");
      const probeTokens = npM[3].trim().split(/\s+/);
      // Nom le plus court d'abord : ne jamais avaler l'auxiliaire (« l'enfant a mangé »)
      for (let len = 1; len <= probeTokens.length; len++) {
        const piece = probeTokens.slice(0, len).join(" ");
        const entry = bestSoninkeEntry(lookupTerm(piece), "nom|syntagme|lexeme|partie_du_corps", { definite, directKey: piece, strictContent: true });
        if (entry) {
          g.subjectEntry = entry;
          work = work.slice(work.indexOf(piece) + piece.length).trim();
          break;
        }
      }
    }
  }

  // 2. Négation en tête du groupe verbal (« ne/n'/n'a »)
  if (/^(?:ne\s+|n'|n'a\s+)/i.test(work)) {
    g.negation = true;
    work = work.replace(/^(?:ne\s+|n'|n'a\s+)/i, "").trim();
  }
  // Négation en queue (« pas / plus / jamais »)
  {
    const tokens = work.split(/\s+/).filter(Boolean);
    const kept = [];
    for (const t of tokens) {
      if (t === "pas" || t === "plus") { g.negation = true; continue; }
      if (t === "jamais") { g.negation = true; if (!g.timeWord) g.timeWord = "jamais"; continue; }
      kept.push(t);
    }
    work = kept.join(" ");
  }

  // 3. Temps : passé composé / futur périphrastique, puis futur et imparfait simples
  let rest = work;
  const pastAvoir = rest.match(FR_PAST_AVOIR_RE);
  const pastEtre = !pastAvoir && rest.match(FR_PAST_ETRE_RE);
  const futPeriph = !pastAvoir && !pastEtre && rest.match(FR_FUT_PERIPH_RE);
  if (pastAvoir && hasFrenchVerb(pastAvoir[1])) {
    g.tense = "past";
    rest = pastAvoir[1].trim();
  } else if (pastEtre && hasFrenchVerb(pastEtre[1])) {
    g.tense = "past";
    rest = pastEtre[1].trim();
  } else if (pastEtre) {
    g.copuleMissing = true;
  } else if (futPeriph && hasFrenchVerb(futPeriph[1])) {
    g.tense = "future";
    rest = futPeriph[1].trim();
  }

  const restTokens = rest.split(/\s+/).filter(Boolean);
  if (g.tense === "imperfective" && restTokens.length) {
    const t0 = restTokens[0];
    if (FR_FUT_SIMPLE_RE.test(t0) && lookupFrenchVerbToken(t0)) {
      g.tense = "future";
    } else if (FR_IMPF_SIMPLE_RE.test(t0) && lookupFrenchVerbToken(t0)) {
      // Imparfait français → inaccompli soninké (déjà la valeur par défaut)
    }
  }

  // 4. Compléments de temps attestés
  {
    const flat = restTokens.join(" ");
    for (const phrase of FR_TIME_LIST) {
      const idx = flat.indexOf(phrase);
      if (idx >= 0) {
        if (!g.timeWord) g.timeWord = phrase;
        restTokens.splice(0, restTokens.length, ...flat.replace(phrase, " ").replace(/\s+/g, " ").trim().split(/\s+/).filter(Boolean));
        break;
      }
    }
    if (g.timeWord) g.timeEntry = bestSoninkeEntry(lookupTerm(g.timeWord), "adverbe|expression|nom", { directKey: g.timeWord, strictContent: true });
  }

  // 5. Complément de lieu final (« au marché », « à la maison », « à l'école ») — y compris en début
  {
    const flat = restTokens.join(" ");
    const placeM = flat.match(/(?:^|\s)(?:au|aux|a la|a l'|a|dans|chez|en|sur)\s+(.+)$/i);
    if (placeM && placeM[1] && hasFrenchNounGuess(placeM[1])) {
      g.placeWord = stripLeadingArticle(placeM[1]);
      const found = lookupFrenchNounPhrase(g.placeWord.split(/\s+/), 2, { definite: /(?:au|aux|a\s+la|a\s+l')/i.test(placeM[0]) });
      if (found) g.placeEntry = found.entry;
      const beforePlace = placeM.index === 0 ? "" : flat.slice(0, placeM.index).trim();
      restTokens.splice(0, restTokens.length, ...beforePlace.split(/\s+/).filter(Boolean));
    }
  }

  // 6. Verbe principal (premier token verbal attesté du corpus)
  let verbIndex = -1;
  for (let i = 0; i < restTokens.length; i++) {
    const tok = restTokens[i];
    if (FR_SKIP_TOKENS.has(tok)) {
      if (FR_OBJ_PRONOUNS.has(tok)) g.objectPronoun = true;
      continue;
    }
    const found = lookupFrenchVerbToken(tok);
    if (found) {
      verbIndex = i;
      g.verbWord = tok;
      g.verbEntry = found.entry;
      break;
    }
  }
  if (verbIndex >= 0) {
    const before = restTokens.slice(0, verbIndex).filter((t) => !FR_SKIP_TOKENS.has(t));
    const after = restTokens.slice(verbIndex + 1);

    // 7. Objet nominal placé avant le verbe (cas rare en français déclaratif)
    if (before.length && !g.objectEntry) {
      const objText = stripLeadingArticle(before.join(" "));
      const found = objText ? lookupFrenchNounPhrase(objText.split(/\s+/), 2) : null;
      if (found) { g.objectWord = found.text; g.objectEntry = found.entry; }
      else if (objText) g.objectWord = objText;
    }

    // 8. Après le verbe : déterminant + nom (+ adjectif) ou complément
    let detCount = 0;
    let definite = false;
    while (detCount < after.length && (FR_DET_TOKEN_RE.test(after[detCount]) || /^(l'|d')/.test(after[detCount]))) {
      if (/^(le|la|les|l')$/i.test(after[detCount]) || /^l'/.test(after[detCount])) definite = true;
      detCount++;
    }
    const afterNoDet = after.slice(detCount);
    if (!g.objectEntry && afterNoDet.length && !FR_TIME_LIST.includes(afterNoDet.join(" "))) {
      const found = lookupFrenchNounPhrase(afterNoDet, 2, { definite });
      if (found && !/^(pas|plus|jamais)$/i.test(afterNoDet[0])) {
        g.objectWord = found.text;
        g.objectEntry = found.entry;
        let consumed = detCount + found.length;
        const adjToken = after[consumed] && !FR_SKIP_TOKENS.has(after[consumed]) ? after[consumed] : null;
        if (adjToken) {
          const adjEntry = bestSoninkeEntry(lookupTerm(adjToken), "adjectif|quantitatif|quantificateur|adverbe", { directKey: adjToken, strictContent: true });
          if (adjEntry && /adjectif|quantit|adverbe/i.test(adjEntry.categorie || "")) {
            g.adjectiveEntry = adjEntry;
            consumed++;
          }
        }
        const restC = after.slice(consumed).join(" ").trim();
        if (restC) {
          g.complementWord = restC;
          const ce = bestSoninkeEntry(lookupTerm(restC), "adverbe|expression|nom|deictique", { directKey: restC, strictContent: true });
          if (ce) g.complementEntry = ce;
        }
      } else {
        const restC = afterNoDet.join(" ").trim();
        if (restC) {
          g.complementWord = restC;
          const ce = bestSoninkeEntry(lookupTerm(restC), "adverbe|expression|nom|deictique", { directKey: restC, strictContent: true });
          if (ce) g.complementEntry = ce;
        }
      }
    }
  }

  // Annotation explicite du futur lointain par l'utilisateur
  if (/futur lointain|plus tard(?:\s+que|\b)/i.test(original) && g.tense === "future") g.tense = "futureFar";

  return g;
}

// ── Composition de la phrase soninké selon les règles du référent ──
function composeSoninkeTranslation(g) {
  if (!g || !g.verbEntry) return null;
  if (!g.subjectPronoun && !g.subjectEntry) return null;
  if (g.copuleMissing) return null;

  const verbBare = String(g.verbEntry.soninke || "").trim();
  if (!verbBare) return null;
  const verbImpf = imperfectiveFormOf(verbBare);
  const transitive = !!(g.objectEntry || g.objectWord || g.objectPronoun);
  const notes = [];

  let aux = "";
  let verbForm = verbBare;
  let useLongPronoun = false;
  let ruleKey = g.tense;

  if (g.negation) {
    if (g.tense === "past") ruleKey = "pastNeg";
    else if (g.tense === "future" || g.tense === "futureFar") ruleKey = "futureNearNeg";
    else ruleKey = "imperfectiveNeg";
  }

  switch (ruleKey) {
    case "past":
      if (transitive) {
        // Attesté : « Anké n'di maro n'yiga » (1s/2s/1p/2p) et « A da i doronmun biyi » (3s/3p)
        const p = g.subjectPronoun;
        if (!g.subjectEntry && p && (p.person === "1s" || p.person === "2s" || p.person === "1p" || p.person === "2p")) {
          aux = "n'di";
          useLongPronoun = true;
        } else {
          aux = "da";
        }
        verbForm = combineNasalParticle(verbBare);
      } else {
        // Attesté : « N daga » (1re personne) et « Aké n'daga » (autres personnes)
        const p = g.subjectPronoun;
        if (!(p && p.person === "1s")) {
          verbForm = combineNasalParticle(verbBare);
          useLongPronoun = !g.subjectEntry;
        }
      }
      break;
    case "future":
      aux = SONINKE_TENSE_RULES.future.aux;
      break;
    case "futureFar":
      aux = SONINKE_TENSE_RULES.futureFar.aux;
      break;
    case "pastNeg":
      aux = SONINKE_TENSE_RULES.pastNeg.aux;
      break;
    case "imperfectiveNeg":
      aux = SONINKE_TENSE_RULES.imperfectiveNeg.aux;
      verbForm = verbImpf || verbBare;
      break;
    case "futureNearNeg":
      aux = SONINKE_TENSE_RULES.futureNearNeg.aux;
      verbForm = verbImpf || verbBare;
      break;
    default:
      aux = SONINKE_TENSE_RULES.imperfective.aux;
      verbForm = verbImpf || verbBare;
      break;
  }

  const subject = g.subjectEntry
    ? String(g.subjectEntry.soninke).trim()
    : (useLongPronoun ? (g.subjectPronoun.longAccent || g.subjectPronoun.long) : g.subjectPronoun.short);

  // Ordre typologique : Sujet + Auxiliaire/Marqueur + Objet (+ Adjectif) + Verbe + Compléments
  const parts = [subject];
  if (aux) parts.push(aux);
  if (g.objectEntry) {
    parts.push(String(g.objectEntry.soninke).trim());
    if (g.adjectiveEntry) parts.push(String(g.adjectiveEntry.soninke).trim());
  } else if (g.objectWord) {
    notes.push(`Pour compléter cette phrase avec précision, il faudrait ajouter le mot « ${g.objectWord} » au lexique.`);
  } else if (g.objectPronoun) {
    notes.push(`Pour compléter cette phrase avec précision, il faudrait préciser le pronom objet soninké dans le lexique.`);
  }
  parts.push(verbForm);
  if (g.placeEntry) parts.push(String(g.placeEntry.soninke).trim());
  else if (g.placeWord) notes.push(`Pour compléter cette phrase avec précision, il faudrait ajouter le mot « ${g.placeWord} » au lexique.`);
  if (g.complementEntry) parts.push(String(g.complementEntry.soninke).trim());
  else if (g.complementWord) notes.push(`Pour compléter cette phrase avec précision, il faudrait ajouter le mot « ${g.complementWord} » au lexique.`);
  if (g.timeEntry) parts.push(String(g.timeEntry.soninke).trim());
  else if (g.timeWord) notes.push(`Pour compléter cette phrase avec précision, il faudrait ajouter le mot « ${g.timeWord} » au lexique.`);
  if (g.interrogative) parts.push("ba");

  const sentence = capitalizeFirst(parts.filter(Boolean).join(" ").replace(/\s+/g, " "));
  const missing = unattestedTokensOf(sentence);
  if (missing.length) {
    return { sentence: null, notes: [...notes, ...missing.map((m) => `Forme à faire valider par le référent : « ${m} ».`)] };
  }
  let structure;
  if (ruleKey === "past") {
    structure = transitive
      ? `Sujet + « ${aux} » + Objet + n' + Verbe — accompli (passé), attesté : « Anké n'di maro n'yiga »`
      : (aux ? `Sujet + « ${aux} » + Verbe + complément — accompli` : `Sujet + Verbe + complément — accompli, attesté : « N daga » / « Aké n'daga sakha lenki »`);
  } else {
    structure = `Sujet + « ${aux} » + ${transitive ? "Objet + " : ""}Verbe${g.interrogative ? " + ba" : ""} — ${(SONINKE_TENSE_RULES[ruleKey] || SONINKE_TENSE_RULES.imperfective).label}`;
  }
  return { sentence, ruleKey, notes, structure };
}

// ── Segments audio disponibles dans une phrase (notification d'écoute partielle) ──
const SONINKE_GRAMMAR_MARKERS_RE = /\b(wa|n'di|da|di|ma|maxa|nta|n'ti rini|n'taxa rini|yi rini|rini|fayi|do)\b/i;

function extractSoninkeSentenceFromResponse(text) {
  const forms = [];
  for (const m of String(text || "").matchAll(/\{\{pair:([^|}]+)\|/g)) forms.push(m[1]);
  const found = forms.find((v) => SONINKE_GRAMMAR_MARKERS_RE.test(String(v)) && String(v).trim().split(/\s+/).length >= 3);
  return found ? String(found).trim() : "";
}

function sentencePresenceNote(sentence) {
  const s = String(sentence || "").trim();
  if (!s) return "";
  const segs = extractAvailableAudioSegments(s);
  if (!segs.length) return "";
  return `Audio de référence disponible pour : ${segs.map((x) => x.text).join(" · ")}.`;
}

// ── Réponse pédagogique : phrase composée + explication grammaticale ──
function grammarAnswer(sourceText) {
  // Priorité absolue au corpus : la même phrase déjà enregistrée et validée prime sur toute composition
  const normSrc = normalizeWord(sourceText).replace(/[?.!…]+$/, "").trim();
  const sampleHit = normSrc ? state.samples.find((s) =>
    normalizeWord(s.french).replace(/[?.!…]+$/, "").trim() === normSrc
  ) : null;
  if (sampleHit && !isExcludedForm(sampleHit.soninke)) {
    let out = `**Phrase attestée dans le corpus**\n`;
    out += soninkeBlock(sampleHit.soninke, sampleHit.french, "phrase");
    out += `*Cette phrase complète est enregistrée dans le corpus validé par le référent : elle prime sur toute recomposition.*\n\n`;
    const alt = state.samples.filter((s) => s !== sampleHit &&
      normalizeWord(s.french).split(/[\s'.,!?()]+/).some((w) => normSrc.split(/\s+/).includes(w)));
    for (const s of alt.slice(0, 2)) out += soninkeBlock(s.soninke, s.french, "phrase");
    out += levelNote();
    return out;
  }

  const parsed = parseFrenchStructure(sourceText);
  if (!parsed) return null;

  if (parsed.copuleMissing) {
    return `La copule « être » n'est pas encore enregistrée comme verbe autonome dans le lexique soninké.\n\n` +
      `Pour compléter cette phrase avec précision, il faudrait ajouter la forme « être » (copule) au lexique.\n\n` +
      `**Formes attestées proches**\n` +
      soninkeBlock("Toora nta", "Tout va bien.", "expression") +
      soninkeBlock("kere", "Ici.", "mot") +
      levelNote();
  }

  if (!parsed.verbWord && !parsed.objectWord && !parsed.subjectPronoun && !parsed.subjectEntry) return null;
  if (!parsed.verbWord && !parsed.objectWord) return null;

  const composed = composeSoninkeTranslation(parsed);

  if (!parsed.verbEntry) {
    const guess = parsed.verbWord || "";
    let out = guess
      ? `Le verbe « ${guess} » n'est pas attesté comme verbe dans le corpus soninké : je ne l'invente pas.\n\n` +
        `Pour compléter cette phrase avec précision, il faudrait ajouter le mot « ${guess} » au lexique.\n\n`
      : `Cette structure ne peut pas être composée uniquement avec les formes attestées du corpus.\n\n`;
    const near = guess ? findSimilarEntries(guess, 4).filter((e) => /verbe/i.test(e.categorie || "")) : [];
    if (near.length) {
      out += `**Verbes attestés proches**\n`;
      for (const e of near) out += formatEntryBullet(e);
    }
    out += levelNote();
    return out;
  }

  if (!composed || !composed.sentence) {
    if (composed && composed.notes && composed.notes.length) {
      let out = `La phrase ne peut pas être composée fidèlement uniquement avec des formes attestées.\n\n`;
      for (const n of composed.notes) out += `- ${n}\n`;
      out += `\n**Phrases attestées de structure proche**\n`;
      for (const s of state.samples.slice(0, 2)) out += soninkeBlock(s.soninke, s.french, "phrase");
      out += levelNote();
      return out;
    }
    return null;
  }

  const audioNote = sentencePresenceNote(composed.sentence);
  let out = `**Phrase soninké construite selon les règles du corpus**\n`;
  out += soninkeBlock(composed.sentence, parsed.original, "phrase");
  out += `*Structure : ${composed.structure}.*\n\n`;
  if (audioNote) out += `*${audioNote}*\n\n`;
  if (composed.notes && composed.notes.length) {
    out += `**Pour une phrase 100 % complète**\n`;
    for (const n of composed.notes) out += `- ${n}\n`;
    out += `\n`;
  }
  out += `**Pour pratiquer**\n`;
  out += `- changez le sujet (${SONINKE_PRONOUNS.map((p) => p.short).join(" / ")}) avec les pronoms attestés ;\n`;
  out += `- demandez « corrige ma phrase » pour vérifier votre propre formulation.\n\n`;
  out += levelNote();
  return out;
}

// ── Détection d'une demande de composition de phrase ──
function sentenceToCompose(message) {
  const trimmed = String(message || "").trim();
  if (!trimmed) return "";
  const { targetPhrase, words } = extractTargetPhraseAndWords(trimmed);
  const isTranslationAsk = /en\s+sonink[ée]|en\s+fran[çc]ais|tradui|comment\s+dit|comment\s+dire/i.test(trimmed);
  if (isTranslationAsk && targetPhrase && targetPhrase.split(/\s+/).length >= 2) return targetPhrase;
  if (words.length < 2) return "";
  if (isTranslationAsk && targetPhrase) return targetPhrase;
  const looksFrenchSentence = FR_SUBJECT_PRONOUN_RE.test(trimmed)
    || /^(?:est-ce que|qu'est-ce que)\s+\S+\s+\S+/i.test(trimmed)
    || /^(?:le|la|l'|un|une|mon|ma|ton|ta|son|sa|notre|votre|leur)\s*\S+\s+\S+/i.test(trimmed);
  if (looksFrenchSentence && !/\b(tradui|signifie|veut\s+dire)\b/i.test(trimmed)) return trimmed.replace(/[?.!]+$/, "");
  return "";
}

function findMatchingSamples(terms) {
  const norms = terms.flatMap(candidateWordForms).filter((t) => t.length >= 2);
  if (!norms.length) return [];
  return state.samples.filter((s) => {
    const snk = normalizeWord(s.soninke);
    const fr = normalizeWord(s.french);
    return norms.some((n) => snk.split(/[\s']+/).includes(n) || fr.split(/[\s'.,!?()]+/).includes(n));
  });
}

function findSimilarEntries(term, limit = 5) {
  const n = normalizeWord(term);
  const ortho = normalizeSoninkeOrtho(term);
  if (!n) return [];
  const scored = [];
  for (const e of state.entries) {
    const tokens = [
      ...normalizeWord(e.soninke).split(/\s+/),
      normalizeSoninkeOrtho(e.soninke),
      ...normalizeWord(e.francais).split(/[\s,;/()]+/),
      ...String(e.variantes || "").split(/[;,|]/).map(normalizeWord),
    ].filter((w) => w.length > 1);
    let best = Infinity;
    for (const w of tokens) {
      const d = Math.min(levenshtein(n, w), ortho ? levenshtein(ortho, normalizeSoninkeOrtho(w)) : Infinity);
      if (d < best) best = d;
      if (best === 0) break;
    }
    const threshold = n.length <= 4 ? 1 : n.length <= 8 ? 2 : 3;
    if (best > 0 && best <= threshold) scored.push({ e, d: best });
  }
  scored.sort((a, b) => a.d - b.d || String(a.e.soninke).localeCompare(String(b.e.soninke)));
  return scored.slice(0, limit).map((s) => s.e);
}

function formatEntryBullet(e, includeExample = false) {
  if (!e || isExcludedForm(e.soninke)) return "";
  const parts = [e.francais];
  if (e.categorie) parts.push(`(${e.categorie})`);
  if (e.isCandidate) parts.push("à vérifier");
  let out = soninkeBlock(e.soninke, parts.filter(Boolean).join(" · "));
  if (e.variantes) out += `Variantes attestées : ${e.variantes}\n\n`;

  // Formes dérivées enregistrées dans audio/snk-*.wav
  const related = state.relatedAudioByStem.get(normalizeWord(e.soninke));
  if (related && related.length && !findAudioInfo(e.soninke)) {
    out += soninkeBlock(related[0].text, "Forme enregistrée avec la voix de référence", "expression");
  }
  if (includeExample && e.exemple_original) {
    out += `*Note du corpus : ${extractCleanExample(e.exemple_original)}*\n\n`;
  }
  return out;
}

function formatPhrasebookBullet(p) {
  if (!p || isExcludedForm(p.snk)) return "";
  const details = [];
  if (p.alt.length) details.push(`variantes : ${p.alt.join(", ")}`);
  const fr = p.fr + (details.length ? ` · ${details.join(" · ")}` : "");
  let out = soninkeBlock(p.snk, fr, "expression");
  if (p.note) out += `*${p.note}*\n\n`;
  return out;
}

const STOP_WORDS = new Set([
  "le", "la", "les", "un", "une", "des", "de", "du", "d", "l", "en", "au", "aux", "et", "ou",
  "est", "es", "suis", "sont", "a", "à", "pour", "dans", "sur", "avec", "sans", "par", "plus",
  "ce", "cet", "cette", "ces", "que", "qu", "qui", "quoi", "quel", "quelle", "quels", "quelles",
  "comment", "combien", "pourquoi", "quand", "ou", "peux", "peut", "pouvez", "veux", "veut", "voulez",
  "sais", "sait", "dire", "dit", "on", "traduire", "traduis", "traduit", "traduction", "signifie",
  "signification", "apprendre", "apprends", "expliquer", "explique", "donne", "donner", "cherche",
  "chercher", "trouve", "trouver", "mot", "mots", "phrase", "expression", "soninke", "soninké",
  "francais", "français", "francaise", "française", "langue", "svp", "stp", "il", "te", "vous", "plait", "plaît",
  "me", "moi", "se", "ne", "pas", "y", "c", "ça", "ca", "fait"
]);

function extractTargetPhraseAndWords(message) {
  const cleanMsg = String(message || "").trim();

  // 1. Modèles explicites de questions de traduction / sens
  const explicitPatterns = [
    /comment\s+dit(?:-on)?\s+[«"“]?(.+?)[»"”]?\s+en\s+(?:sonink[ée]|fran[çc]ais)\s*[?!.]*$/i,
    /comment\s+dire\s+[«"“]?(.+?)[»"”]?\s+en\s+(?:sonink[ée]|fran[çc]ais)\s*[?!.]*$/i,
    /(?:traduis(?:-moi)?|traduire|traduit|traduction\s+de)\s*:?\s*[«"“]?(.+?)[»"”]?\s+en\s+(?:sonink[ée]|fran[çc]ais)\s*[?!.]*$/i,
    /(?:traduis(?:-moi)?|traduire|traduit|traduction\s+de)\s*:?\s*[«"“]?(.+?)[»"”]?\s*[?!.]*$/i,
    /(?:comment\s+dit(?:-on)?|comment\s+dire|comment\s+on\s+dit)\s+[«"“]?(.+?)[»"”]?\s*[?!.]*$/i,
    /(?:que\s+veut\s+dire|que\s+signifie|ça\s+veut\s+dire\s+quoi|veut\s+dire|signification\s+de)\s+[«"“]?(.+?)[»"”]?\s*[?!.]*$/i,
  ];

  let targetPhrase = "";
  for (const pat of explicitPatterns) {
    const m = cleanMsg.match(pat);
    if (m && m[1]) {
      targetPhrase = m[1].replace(/[»"”?.!]+$/, "").trim();
      if (targetPhrase) break;
    }
  }

  // 2. Termes entre guillemets si présents
  if (!targetPhrase) {
    const quoted = cleanMsg.match(/[«"“](.+?)[»"”]/);
    if (quoted && quoted[1]) targetPhrase = quoted[1].trim();
  }

  // 3. Découpage en mots porteurs de sens (gère aussi les apostrophes françaises : l'enfant, j'aime, d'eau)
  const sourceForWords = targetPhrase || cleanMsg;
  const rawTokens = sourceForWords
    .replace(/[’‘]/g, "'")
    .replace(/\b([ldjnmtsquc])'/gi, "$1 ")
    .replace(/[?.!,;:()[\]{}"«»“”/\\]/g, " ")
    .split(/\s+/)
    .map((w) => w.trim())
    .filter(Boolean);

  // Si l'utilisateur a ciblé une expression explicite (ex. « bonjour », « merci », « au revoir », « je t'aime »), on garde ses mots utiles !
  const contentWords = rawTokens.filter((w) => {
    const nw = normalizeWord(w);
    if (!nw) return false;
    if (targetPhrase && rawTokens.length <= 4) {
      return !["le", "la", "les", "un", "une", "de", "du", "des", "l", "d"].includes(nw);
    }
    return nw.length > 1 && !STOP_WORDS.has(nw);
  });

  return {
    targetPhrase: targetPhrase || (rawTokens.length <= 3 ? cleanMsg.replace(/[?.!]+$/, "").trim() : ""),
    words: [...new Set(contentWords)],
  };
}

function detectDirection(message) {
  if (/en\s+fran[çc]ais|que\s+veut\s+dire|que\s+signifie/i.test(message)) return "snk2fr";
  if (/en\s+sonink[ée]/i.test(message)) return "fr2snk";
  return "auto";
}

// ── Générateur complet de réponses (100% garanti sur toute question) ──
function buildSingleOrPhraseAnswer(targetPhrase, words, direction) {
  const level = currentLevel();

  // 1. D'abord tester l'expression complète (ex. « bonjour », « lemine ke », « Daga goli »)
  if (targetPhrase) {
    const fullLookup = lookupTerm(targetPhrase);
    const fullPB = lookupPhrasebook(targetPhrase);
    if (fullLookup.exact.length || fullPB.length) {
      return formatRichTermResponse(targetPhrase, fullLookup, fullPB, direction);
    }
  }

  // 2. Phrase de plusieurs mots : uniquement ce qui est attesté.
  //    Aucune phrase soninké n'est reconstruite par assemblage de mots.
  if (words.length >= 2) {
    const wordMappings = [];
    for (const w of words.slice(0, 8)) {
      const pb = lookupPhrasebook(w);
      const lk = lookupTerm(w);
      const bestEntry = lk.exact[0] || lk.starts[0];
      const bestPB = pb[0];
      if (bestPB) wordMappings.push({ word: w, snk: bestPB.snk, fr: bestPB.fr });
      else if (bestEntry) wordMappings.push({ word: w, snk: bestEntry.soninke, fr: bestEntry.francais, entry: bestEntry });
    }

    const matchingSamples = findMatchingSamples(words);
    let out = "";

    if (matchingSamples.length > 0) {
      out += "**Phrases attestées correspondantes**\n";
      for (const sample of matchingSamples.slice(0, level.maxSamples)) {
        out += soninkeBlock(sample.soninke, sample.french, "phrase");
      }
    }

    if (wordMappings.length > 0) {
      out += "**Correspondances mot à mot du lexique**\n";
      out += "*Assemblage indicatif : ces formes sont attestées séparément, la phrase complète ne l'est pas.*\n\n";
      for (const m of wordMappings.slice(0, level.maxEntries)) {
        out += m.entry ? formatEntryBullet(m.entry) : soninkeBlock(m.snk, m.fr);
      }
    }

    if (!out) {
      return unknownAnswer(targetPhrase || words.join(" "));
    }

    out += "Pour une traduction de phrase entière, SoninkeGPT ne compose pas de phrase non attestée. La phrase doit être enregistrée puis validée par le référent avant publication.\n\n";
    out += levelNote();
    return out;
  }

  // 3. Terme unique (ou premier mot clé pertinent)
  const mainTerm = targetPhrase || words[0] || "";
  const lk = lookupTerm(mainTerm);
  const pb = lookupPhrasebook(mainTerm);
  return formatRichTermResponse(mainTerm, lk, pb, direction);
}

function unknownAnswer(term) {
  const level = currentLevel();
  const similar = findSimilarEntries(term, 5).filter((e) => !isExcludedForm(e.soninke));
  let out = "Je ne trouve pas cette forme dans le corpus soninké vérifié. Je ne l'invente pas.\n\n";
  if (similar.length > 0) {
    out += `**Formes les plus proches dans le lexique**\n`;
    for (const e of similar.slice(0, level.maxEntries)) out += formatEntryBullet(e, level !== "debutant");
  } else {
    out += "**Expressions attestées à réutiliser**\n";
    out += soninkeBlock("Xa wouy Diom", "Bonjour ! (salutation respectueuse)", "expression");
    out += soninkeBlock("Toora nta", "Tout va bien.", "expression");
    out += soninkeBlock("Nawari", "Merci.", "mot");
  }
  out += "Précisez le mot, l'orthographe approximative ou le thème (famille, corps, nombres, verbes) : je chercherai dans les entrées attestées.\n\n";
  out += levelNote();
  return out;
}

function formatRichTermResponse(term, lk, pb, direction) {
  const level = currentLevel();
  const exact = lk.exact.filter((e) => !isExcludedForm(e.soninke));
  const starts = lk.starts.filter((e) => !isExcludedForm(e.soninke));
  const contains = lk.contains.filter((e) => !isExcludedForm(e.soninke));
  const results = [...exact];
  const seen = new Set(results.map((e) => e.id));
  for (const e of [...starts, ...contains]) {
    if (seen.has(e.id) || isExcludedForm(e.soninke)) continue;
    results.push(e);
    seen.add(e.id);
    if (results.length >= level.maxEntries) break;
  }
  const visiblePb = pb.filter((p) => !isExcludedForm(p.snk));

  const heroSnk = (visiblePb[0] && visiblePb[0].snk) || (exact[0] && exact[0].soninke) || (results[0] && results[0].soninke) || null;
  const heroFr = (visiblePb[0] && visiblePb[0].fr) || (exact[0] && exact[0].francais) || (results[0] && results[0].francais) || "";

  let response = "";
  if (heroSnk) {
    response += soninkeBlock(heroSnk, heroFr || "Sens à préciser par le référent", visiblePb.length ? "expression" : null);
  }

  if (visiblePb.length > 1) {
    response += "**Formes usuelles attestées**\n";
    for (const p of visiblePb.slice(0, level.maxEntries)) response += formatPhrasebookBullet(p);
  }

  if (results.length > 0) {
    response += `**Entrées du lexique (${results.length})**\n`;
    for (const e of results.slice(0, level.maxEntries)) {
      response += formatEntryBullet(e, level !== "debutant" && results.length <= 3);
    }
  }

  const samples = findMatchingSamples([term]);
  if (samples.length > 0) {
    response += "**Exemples de phrases attestées**\n";
    for (const s of samples.slice(0, level.maxSamples)) {
      response += soninkeBlock(s.soninke, s.french, "phrase");
    }
  }

  if (heroSnk || results.length > 0) {
    response += levelNote();
    return response;
  }

  return unknownAnswer(term);
}

function generateResponse(message) {
  const trimmed = String(message || "").trim();
  const lower = trimmed.toLocaleLowerCase("fr");
  const ortho = normalizeSoninkeOrtho(trimmed);
  const direction = detectDirection(trimmed);
  const level = currentLevel();

  // 0. Forme explicitement écartée (non soninké) : jamais présentée comme du soninké
  const excludedMatch = [...state.guard].find(
    (g) => g && (lower === g || ortho === normalizeSoninkeOrtho(g))
  );
  if (excludedMatch) {
    return `Cette forme n'est pas retenue comme soninké par le contrôle linguistique de SoninkeGPT. Elle n'est donc pas présentée comme une traduction soninké.\n\n` +
      `**Exprimer cette idée en soninké attesté**\n` +
      soninkeBlock("Nawari", "Merci.", "mot") +
      soninkeBlock("Xa wouy Diom", "Bonjour ! (salutation respectueuse)", "expression") +
      `Consultez le lexique pour la forme réellement attestée. Si vous êtes locuteur référent, signalez la forme à valider : elle sera ajoutée après vérification.\n\n`;
  }

  // 1. Salutations directes
  const isDirectGreeting =
    !/tradui|comment\s+dit|comment\s+dire|signifie|veut\s+dire/i.test(lower) &&
    (/^(bonjour|bonsoir|salut|hello|hi|hey|coucou|xa\s*wouy|wouy\s*diom|an\s*wouydiom|bisimilla|a\s*jaara|a\s*jarra)\b/i.test(lower) ||
      /^(xawuydiom|wuy ?jom|anwuyjom)/.test(ortho)) &&
    trimmed.length < 48;

  if (isDirectGreeting) {
    return `SoninkeGPT vous salue en soninké.\n` +
      soninkeBlock("Xa wouy Diom", "Bonjour ! Salutation respectueuse (pluriel).", "expression") +
      soninkeBlock("an wouydiom", "Bonjour à une personne.", "expression") +
      soninkeBlock("an moxo", "Bonjour, comment ça va ? (singulier).", "expression") +
      soninkeBlock("qa moxo", "Bonjour, comment ça va ? (pluriel).", "expression") +
      soninkeBlock("bisimilla", "Bienvenue, bonne arrivée.", "expression") +
      `Écrivez votre question ou utilisez le micro. Chaque forme est lue avec la voix de référence lorsqu'un enregistrement existe.\n\n` +
      levelNote();
  }

  // 2. Comment ça va ?
  if (!/tradui|comment\s+dit/i.test(lower) && /^(comment (vas|allez)|ça va|ca va|i kera di|an moxo|qa moxo|toora)\b/i.test(lower) && trimmed.length < 56) {
    return `**La conversation de tous les jours**\n` +
      soninkeBlock("Toora nta", "Tout va bien.", "expression") +
      soninkeBlock("i kera di ?", "Comment vas-tu ?", "expression") +
      soninkeBlock("qa moxo ?", "Comment allez-vous ? (pluriel)", "expression") +
      soninkeBlock("toora su nta", "Tout va bien (variante).", "expression") +
      `Réponse possible : **Toora nta** (tout va bien).\n\n` +
      levelNote();
  }

  // 3. Remerciements
  if (!/tradui|comment\s+dit|comment\s+dire/i.test(lower) && /^(merci|nawari|nawaari)\b/i.test(lower) && trimmed.length < 36) {
    return `**Remercier en soninké**\n` +
      soninkeBlock("Nawari", "Merci.", "mot") +
      soninkeBlock("nawaari", "Merci (variante orthographique).", "mot") +
      levelNote();
  }

  // 4. Au revoir
  if (!/tradui|comment\s+dit|comment\s+dire/i.test(lower) && /^(au revoir|adieu|bye|à bient[ôo]t|a bientot|bonne nuit|oyi waxati|hali telle)\b/i.test(lower) && trimmed.length < 40) {
    return `**Prendre congé en soninké**\n` +
      soninkeBlock("oyi waxati", "Au revoir.", "expression") +
      soninkeBlock("hali telle", "Au revoir, à bientôt.", "expression") +
      levelNote();
  }

  // 5. Présentation / identité
  if (/(qui es[- ]tu|qui [êe]tes[- ]vous|tu es qui|c'est quoi soninkegpt|pr[ée]sente[- ]toi|ton nom)/i.test(lower)) {
    return `Je suis **SoninkeGPT**, l'assistant vocal de la langue soninké. Je travaille uniquement avec le corpus vérifié : **${state.entries.length} entrées lexicales** et **${state.audioReferenceCount()} enregistrements de référence**.\n\n` +
      `**Se présenter avec des formes attestées**\n` +
      soninkeBlock("Xa wouy Diom", "Bonjour ! (salutation respectueuse)", "expression") +
      soninkeBlock("nké", "je, moi", "mot") +
      soninkeBlock("an", "tu, toi", "mot") +
      soninkeBlock("sefe", "parler", "mot") +
      `Une phrase complète de présentation n'est pas encore enregistrée dans le corpus : je ne l'invente pas. Elle sera publiée après validation par le référent.\n\n` +
      `Niveau actuel : **${level.label}**. ${level.guidance}`;
  }

  // 6. Apprendre un nombre précis de mots
  if (/(apprends[- ]moi|donne[- ]moi)\s+(\d+|cinq|5|dix|10)\s+mots/i.test(lower)) {
    return fiveWordsAnswer();
  }

  // 7. Raconter une histoire (aucune histoire validée dans le corpus)
  if (/raconte[^-]*(une |moi une )?histoire|histoire en sonink/i.test(lower)) {
    let out = `Je ne dispose pas encore d'une histoire soninké enregistrée et validée : je ne vais pas en inventer une.\n\n`;
    out += `**Matière attestée disponible pour construire un récit**\n`;
    for (const sample of state.samples.slice(0, Math.max(3, level.maxSamples))) {
      out += soninkeBlock(sample.soninke, sample.french, "phrase");
    }
    out += `Une histoire authentique doit être racontée par un locuteur, enregistrée avec la voix de référence, puis validée. Le corpus est ouvert à cet ajout.\n\n`;
    out += levelNote();
    return out;
  }

  // 8. Proverbe (aucun proverbe validé dans le corpus)
  if (/proverbe/i.test(lower)) {
    return `Aucun proverbe soninké n'est encore validé dans le corpus de SoninkeGPT. Je préfère vous le dire plutôt que d'inventer un proverbe.\n\n` +
      `**Expressions attestées à utiliser en attendant**\n` +
      soninkeBlock("Xa wouy Diom", "Bonjour ! (salutation respectueuse)", "expression") +
      soninkeBlock("Toora nta", "Tout va bien.", "expression") +
      soninkeBlock("bisimilla", "Bienvenue, bonne arrivée.", "expression") +
      `Un proverbe pourra être ajouté avec son enregistrement et sa validation par le référent.\n\n` +
      levelNote();
  }

  // 9. Corriger une phrase
  if (/corrige|corriger ma phrase|correction de ma phrase/i.test(lower)) {
    const quoted = trimmed.match(/[«"“]([^»"”]+)[»"”]/);
    if (quoted && quoted[1].trim()) return proofreadPhrase(quoted[1].trim());
    return `Indiquez votre phrase entre guillemets, par exemple : « an wouydiom ».\n\n` +
      `**Méthode de correction**\n` +
      `- chaque mot est comparé au lexique soninké et aux enregistrements de référence ;\n` +
      `- un mot inconnu est signalé, jamais remplacé par une invention ;\n` +
      `- l'ordre grammatical d'une phrase complète doit être validé par un locuteur référent.\n\n` +
      levelNote();
  }

  // 10. « Traduis cette phrase » sans phrase fournie
  if (/traduis cette phrase|traduire cette phrase|traduis une phrase/i.test(lower)) {
    let out = `Quelle phrase souhaitez-vous traduire ? Écrivez-la après votre demande, par exemple : « La femme mange le riz ».\n\n`;
    out += `**Exemples de phrases déjà attestées dans le corpus**\n`;
    for (const sample of state.samples.slice(0, Math.max(2, level.maxSamples))) {
      out += soninkeBlock(sample.soninke, sample.french, "phrase");
    }
    out += `Le sens est toujours donné dans l'ordre SONINKÉ → FRANÇAIS.\n\n`;
    out += levelNote();
    return out;
  }

  // 11. Conversation quotidienne
  if (/conversation quotidienne|dialogue (du|de) quotidien|parler tous les jours/i.test(lower)) {
    return `**Conversation quotidienne en soninké**\n` +
      soninkeBlock("Xa wouy Diom", "Bonjour ! (salutation respectueuse)", "expression") +
      soninkeBlock("an moxo ?", "Comment ça va ? (singulier)", "expression") +
      soninkeBlock("Toora nta", "Tout va bien.", "expression") +
      soninkeBlock("i kera di ?", "Comment vas-tu ?", "expression") +
      soninkeBlock("nawari", "Merci.", "mot") +
      soninkeBlock("oyi waxati", "Au revoir.", "expression") +
      `Écoutez chaque réplique et répétez-la : toutes les formes sont attestées dans le corpus.\n\n` +
      levelNote();
  }

  // 12. Thème : tête, visage et corps
  if (/(visage|corps humain|parties du corps|t[êe]te et visage)/i.test(lower)) {
    const hf = state.entries.filter((e) => /partie_du_corps|tete_visage/i.test((e.categorie || "") + " " + (e.source || "")) && !isExcludedForm(e.soninke));
    let res = `**Le visage et le corps en soninké**\n`;
    for (const e of hf.slice(0, level.maxEntries)) res += formatEntryBullet(e);
    res += `\n${levelNote()}`;
    return res;
  }

  // 13. Thème : jours de la semaine
  if (/jours? de la semaine|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche/i.test(lower) && /jour|semaine/i.test(lower)) {
    const days = state.entries.filter((e) => /lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche/i.test(e.francais || "") && !isExcludedForm(e.soninke));
    let res = `**Les jours en soninké**\n`;
    for (const e of days.slice(0, level.maxEntries)) res += formatEntryBullet(e);
    res += soninkeBlock("lenki", "aujourd'hui", "mot");
    res += soninkeBlock("daru", "hier", "mot");
    res += soninkeBlock("koota su", "chaque jour", "expression");
    res += `\n${levelNote()}`;
    return res;
  }

  // 14. Thème : nombres
  if (/nombres?|num[ée]ros?|chiffres?|compter en sonink/i.test(lower)) {
    const nums = state.entries.filter((e) => /nombre|num[ée]ral/i.test(e.categorie || "") && !isExcludedForm(e.soninke));
    let res = `**Compter en soninké**\n`;
    for (const e of nums.slice(0, Math.max(6, level.maxEntries))) res += formatEntryBullet(e);
    res += `\n${levelNote()}`;
    return res;
  }

  // 15. Thème : famille
  if (/famille|parent/i.test(lower) && !/tradui/i.test(lower)) {
    return `**La famille en soninké**\n` +
      soninkeBlock("baaba", "père, papa", "mot") +
      soninkeBlock("saaxe", "mère, maman", "mot") +
      soninkeBlock("lemine", "enfant", "mot") +
      soninkeBlock("yaxare", "femme", "mot") +
      soninkeBlock("yugo", "homme", "mot") +
      soninkeBlock("ka", "maison", "mot") +
      `\n${levelNote()}`;
  }

  // 16. Mots de base / apprentissage
  if (/mot[s]? de base|vocabulaire de base|quelques mots|premiers mots|apprends-moi|apprendre le sonink|le[çc]on|enseigne|parle[- ]moi en sonink|phrase[s]? en sonink/i.test(lower)) {
    return basicsAnswer();
  }

  // 17. Culture soninké
  if (/culture|peuple sonink|empire du ghana|ghana|wagadu|tradition orale|griot|geseru|c[ée]r[ée]monie|castes traditionnelles/i.test(lower)) {
    return `**La culture et l'histoire soninké (Wagadu)**\n\n` +
      `Le peuple soninké (aussi appelé Sarakolé, Marka ou Wakore) est à l'origine de l'empire du Wagadu (Ghana), l'un des grands ensembles politiques d'Afrique de l'Ouest. La langue soninké appartient à la famille mandé et est parlée au Mali, en Mauritanie, au Sénégal, en Gambie, en Guinée-Bissau, en Côte d'Ivoire et dans la diaspora.\n\n` +
      `La tradition orale, portée notamment par les geseru, transmet l'histoire, les patronymes et les valeurs de solidarité communautaire.\n\n` +
      `**Formes attestées liées à l'accueil**\n` +
      soninkeBlock("Xa wouy Diom", "Salutation de paix et de respect.", "expression") +
      soninkeBlock("bisimilla", "Hospitalité, bonne arrivée.", "expression") +
      `Le corpus réunit **${state.entries.length} entrées** et **${state.audioReferenceCount()} enregistrements de référence**.\n\n` +
      levelNote();
  }

  // 18. Prononciation et audio
  if (/prononciation|audios?|écouter|entendre|enregistrement|voix/i.test(lower) && !/tradui|comment\s+dit|signifie/i.test(lower)) {
    return `**La voix de référence**\n\n` +
      `Tous les contenus audio de SoninkeGPT utilisent la voix de référence du corpus : mots, expressions, salutations, traductions, réponses et favoris. Aucune voix synthétique du navigateur n'est utilisée.\n\n` +
      soninkeBlock("Daga goli", "Aller au travail.", "expression") +
      soninkeBlock("Li taxu", "Assieds-toi.", "expression") +
      soninkeBlock("lemine ke", "L'enfant.", "expression") +
      soninkeBlock("maro ke", "Le riz.", "expression") +
      soninkeBlock("koota su", "Chaque jour.", "expression") +
      `**Pour écouter :** sélectionnez « Écouter » sur n'importe quelle forme, utilisez le bouton micro, ou ouvrez le lexique et son filtre Audios. Si un enregistrement manque, SoninkeGPT l'indique au lieu de le remplacer par une autre voix.\n\n` +
      levelNote();
  }

  // 19. Aide
  if (/^(aide|help|que peux-tu|que pouvez-vous|capacit[ée]s|fonctionnalit[ée]s|comment [cç]a marche)/i.test(lower)) {
    return `**Ce que fait SoninkeGPT**\n\n` +
      `- Traduction français ↔ soninké, uniquement avec des formes attestées.\n` +
      `- Assistant vocal : écoute, enregistrement et réponse avec la voix de référence.\n` +
      `- Niveaux débutant, intermédiaire et avancé.\n` +
      `- Favoris : enregistrez un mot, une phrase ou une expression pour le réécouter.\n` +
      `- Lexique et audios : ${state.entries.length} entrées, ${state.audioReferenceCount()} enregistrements.\n\n` +
      `Chaque réponse pédagogique est présentée dans l'ordre SONINKÉ → FRANÇAIS, avec le statut de validation de la forme.\n\n` +
      levelNote();
  }

  // 19b. Composition grammaticale d'une phrase complète (S-Aux-O-V / S-V-Complément)
  //      selon les règles du référent, uniquement avec des mots attestés.
  if (!/^(présente-toi|c'est quoi|qui es-tu)\b/i.test(lower)) {
    const sentenceSrc = sentenceToCompose(trimmed);
    if (sentenceSrc) {
      const reply = grammarAnswer(sentenceSrc);
      if (reply) return reply;
    }
  }

  // 20. Recherche lexicale & traduction
  const { targetPhrase, words } = extractTargetPhraseAndWords(trimmed);
  return buildSingleOrPhraseAnswer(targetPhrase, words, direction);
}

// Cinq mots attestés par le référent, avec la voix de référence.
function fiveWordsAnswer() {
  const preferred = ["daga", "sefe", "yige", "mini", "goli", "xanu", "ri", "safa", "ka", "nawari"];
  const picked = [];
  const seen = new Set();
  const add = (entry) => {
    const key = normalizeWord(entry.soninke);
    if (!key || seen.has(key) || isExcludedForm(entry.soninke)) return false;
    seen.add(key);
    picked.push(entry);
    return true;
  };

  for (const form of preferred) {
    const entry = state.entries.find((e) => normalizeWord(e.soninke) === form
      && attestationOf(e.soninke).level === "referent"
      && !!findAudioInfo(e.soninke));
    if (entry) add(entry);
    if (picked.length === 5) break;
  }
  if (picked.length < 5) {
    for (const entry of state.entries) {
      if (picked.length >= 5) break;
      const key = normalizeWord(entry.soninke);
      if (key.includes(" ")) continue;
      if (attestationOf(entry.soninke).level !== "referent" || !findAudioInfo(entry.soninke)) continue;
      add(entry);
    }
  }

  let out = `**Cinq mots soninké à retenir**\n`;
  for (const entry of picked) out += formatEntryBullet(entry);
  out += `Touchez « Écouter » sur chaque mot, puis répétez-le à voix haute.\n\n`;
  out += levelNote();
  return out;
}

function basicsAnswer() {
  let response = `**L'essentiel du soninké**\n`;
  response += `**Salutations et politesse**\n`;
  response += soninkeBlock("Xa wouy Diom", "Bonjour ! (salutation respectueuse)", "expression");
  response += soninkeBlock("an wouydiom", "Bonjour à une personne.", "expression");
  response += soninkeBlock("Toora nta", "Tout va bien.", "expression");
  response += soninkeBlock("nawari", "Merci.", "mot");
  response += soninkeBlock("oyi waxati", "Au revoir.", "expression");

  response += `**Verbes et noms du corpus**\n`;
  for (const w of ["daga", "sefe", "yige", "mini", "goli", "xanu", "maro", "lemine"]) {
    const match = state.entries.find((e) => normalizeWord(e.soninke) === w && !isExcludedForm(e.soninke));
    if (match) response += formatEntryBullet(match);
  }

  if (state.samples.length) {
    response += `**Phrases parallèles attestées**\n`;
    for (const sample of state.samples.slice(0, currentLevel().maxSamples)) {
      response += soninkeBlock(sample.soninke, sample.french, "phrase");
    }
  }
  response += levelNote();
  return response;
}

// Contrôle mot à mot d'une phrase fournie par l'utilisateur.
function proofreadPhrase(phrase) {
  const tokens = String(phrase).split(/\s+/).filter(Boolean).slice(0, 20);
  const rows = tokens.map((raw) => {
    const clean = raw.replace(/^[«»"'“”.,!?;:()]+|[»«"'“”.,!?;:()]+$/g, "");
    return { raw, clean, att: attestationOf(clean) };
  });
  const unknown = rows.filter((r) => (ATTESTATION[r.att.level]?.rank ?? 0) < 2);

  let out = `**Analyse de « ${phrase} »**\n`;
  for (const row of rows) {
    if (!row.clean) continue;
    const label = row.att.label || "Non attesté dans le corpus";
    out += `- **${row.clean}** : ${label}\n`;
  }
  out += `\n`;
  if (unknown.length) {
    out += `**Formes non vérifiées : ${unknown.map((r) => r.clean).join(", ")}**\n\n`;
    out += `Je ne propose pas de correction inventée : une correction n'est fiable que si elle est attestée. Soumettez ces formes au référent pour validation.\n\n`;
  } else {
    out += `Chaque mot est attesté séparément dans le corpus. L'ordre et l'accord de la phrase complète restent à valider par un locuteur référent.\n\n`;
  }
  out += levelNote();
  return out;
}

// ── Icônes SVG (aucune dépendance, aucun emoji décoratif) ──
const ICONS = {
  speaker: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M11 5L6 9H2.5v6H6l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg>',
  speakerLarge: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M11 5L6 9H2.5v6H6l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.8 5.2a9.5 9.5 0 0 1 0 13.6"/></svg>',
  star: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8L3.5 9.7l5.9-.9z"/></svg>',
  starFilled: '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8L3.5 9.7l5.9-.9z"/></svg>',
  copy: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h8"/></svg>',
  translate: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M4 7h11l-2.5-2.5M20 17H9l2.5 2.5"/></svg>',
  trash: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>',
};

// Bloc SONINKÉ ↓ TRADUCTION FRANÇAISE
function renderSoninkePair(rawSnk, rawFr, rawType) {
  const snk = String(rawSnk || "").trim();
  const fr = String(rawFr || "").trim();
  if (!snk) return "";
  const att = attestationOf(snk);
  const fullSegments = buildSoninkePhraseSegments(snk);
  const hasFullAudio = Boolean(att.audio || findAudioInfo(snk) || fullSegments.length > 0);
  const partialSegments = !hasFullAudio && snk.split(/\s+/).length > 1
    ? extractAvailableAudioSegments(snk)
    : [];
  const type = ["mot", "phrase", "expression"].includes(rawType)
    ? rawType
    : snk.split(/\s+/).length > 1 ? "phrase" : "mot";
  const fav = isFavorite(snk, fr);
  const audioLabel = hasFullAudio ? "Écouter" : "Audio à venir";
  const audioCls = hasFullAudio ? "audio-play-btn" : "audio-play-btn audio-unavailable";
  const audioTitle = hasFullAudio
    ? `Écouter « ${snk} » avec la voix de référence`
    : `Aucun enregistrement complet pour « ${snk} » : aucun substitut synthétique n'est utilisé`;
  const partialHtml = partialSegments.map((seg) => {
    const w = esc(seg.text);
    const t = `Écouter « ${w} » avec la voix de référence`;
    return `<button type="button" class="audio-play-btn" data-audio-word="${w}" title="${t}" aria-label="${t}">${ICONS.speaker}<span>${w}</span></button>`;
  }).join("");
  return `<div class="soninke-pair" data-snk="${snk}" data-fr="${fr}">
  <div class="pair-snk-row">
    <div class="pair-snk-block">
    <span class="pair-lang is-target">Soninké</span>
    <span class="pair-snk" lang="snk">${snk}</span>
    </div>
    <button type="button" class="${audioCls}" data-audio-word="${snk}" title="${audioTitle}" aria-label="${audioTitle}">${ICONS.speaker}<span>${audioLabel}</span></button>
    <button type="button" class="fav-toggle${fav ? " is-favorite" : ""}" data-fav-snk="${snk}" data-fav-fr="${fr}" data-fav-type="${type}" aria-pressed="${fav ? "true" : "false"}" aria-label="${fav ? "Retirer des favoris" : "Ajouter aux favoris"}: ${snk}">${fav ? ICONS.starFilled : ICONS.star}</button>
  </div>
  <div class="pair-arrow" aria-hidden="true">↓</div>
  <span class="pair-lang">Français</span>
  <div class="pair-fr">${fr}</div>
  <div class="pair-foot"><span class="pair-badge ${att.cls}">${att.label}</span>${partialHtml}</div>
</div>`;
}

// ── Rendu Markdown + boutons audio de référence ──
function renderMarkdown(text) {
  let html = esc(text);

  // Marqueurs {{pair:SONINKÉ|FRANÇAIS|type}} → bloc SONINKÉ ↓ FRANÇAIS
  html = html.replace(/\{\{pair:([^|}]+)\|([^|}]*)\|?([^|}]*)\}\}/g,
    (_, snk, fr, type) => renderSoninkePair(snk, fr, (type || "").trim())
  );

  // Marqueurs {{audio:MOT}} → bouton de lecture de la voix de référence
  html = html.replace(/\{\{audio:([^}]+)\}\}/g, (_, rawWord) => {
    const word = rawWord.trim();
    const hasReferenceAudio = !!findAudioInfo(word);
    const title = hasReferenceAudio
      ? `Écouter « ${word} » avec la voix de référence`
      : `Aucun enregistrement de référence pour « ${word} » : aucun substitut synthétique n'est utilisé`;
    return `<button type="button" class="audio-play-btn${hasReferenceAudio ? "" : " audio-unavailable"}" data-audio-word="${word}" title="${title}" aria-label="${title}">${ICONS.speaker}<span>${word}</span></button>`;
  });

  // Code blocks
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) =>
    `<pre><code class="language-${lang}">${code.trim()}</code></pre>`
  );

  // Inline code
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");

  // Bold & Italic
  html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*(.+?)\*/g, "<em>$1</em>");

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

  // Horizontal rule
  html = html.replace(/^---$/gm, "<hr>");

  // Nested & flat lists
  html = html.replace(/^  - (.+)$/gm, '<li class="sub-li">$1</li>');
  html = html.replace(/^- (.+)$/gm, "<li>$1</li>");
  html = html.replace(/(?:<li(?:\s+class="sub-li")?>[\s\S]*?<\/li>\s*)+/g, (match) => `<ul>${match.trim()}</ul>`);

  // Paragraphs
  html = html
    .split(/\n\n+/)
    .map((block) => {
      block = block.trim();
      if (!block) return "";
      if (
        block.startsWith("<ul>") ||
        block.startsWith("<ol>") ||
        block.startsWith("<pre>") ||
        block.startsWith('<div class="soninke-pair"') ||
        block === "<hr>"
      ) {
        return block;
      }
      return `<p>${block.replace(/\n/g, "<br>")}</p>`;
    })
    .join("\n");

  return html;
}

// ── Rendu de la conversation (avec actions audio toujours visibles sur mobile & desktop) ──
// Texte brut lisible d'une réponse (pour la copie et la lecture).
function plainTextOf(content) {
  return String(content || "")
    .replace(/\{\{pair:([^|}]+)\|([^|}]*)\|?([^|}]*)\}\}/g, "$1 → $2")
    .replace(/\{\{audio:([^}]+)\}\}/g, "$1")
    .replace(/[*_`#>]/g, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

// Formes soninké d'un message, avec leur traduction (pour les favoris).
function pairItemsOf(content) {
  const items = [];
  const seen = new Set();
  for (const match of String(content || "").matchAll(/\{\{pair:([^|}]+)\|([^|}]*)\|?([^|}]*)\}\}/g)) {
    const snk = match[1].trim();
    const fr = match[2].trim();
    const type = (match[3] || "").trim();
    const key = `${normalizeWord(snk)}|${normalizeWord(fr)}`;
    if (!snk || seen.has(key)) continue;
    seen.add(key);
    items.push({ snk, fr, type: ["mot", "phrase", "expression"].includes(type) ? type : (snk.split(/\s+/).length > 1 ? "phrase" : "mot") });
  }
  return items;
}

function renderMessages() {
  const conv = getConversation(state.activeConversationId);
  const messagesArea = $("#messages-area");
  const welcomeScreen = $("#welcome-screen");

  if (!conv || conv.messages.length === 0) {
    messagesArea.classList.remove("has-messages");
    messagesArea.innerHTML = "";
    welcomeScreen.style.display = "flex";
    return;
  }

  welcomeScreen.style.display = "none";
  messagesArea.classList.add("has-messages");

  let html = "";
  conv.messages.forEach((msg, idx) => {
    if (msg.role === "user") {
      const note = msg.voiceNoteUrl && msg.voiceNoteUrl.startsWith("blob:")
        ? `<audio class="voice-note-player" controls src="${esc(msg.voiceNoteUrl)}"></audio>`
        : "";
      html += `<div class="message message-user">
        <div class="message-content">${esc(msg.content)}${note}</div>
      </div>`;
    } else {
      const cleanCopy = esc(plainTextOf(msg.content));
      const pairItems = pairItemsOf(msg.content);
      const favAll = pairItems.length
        ? `<button type="button" class="msg-action-btn" data-fav-msg-index="${idx}" title="Enregistrer les formes soninké de cette réponse dans les favoris" aria-label="Enregistrer dans les favoris">
            ${ICONS.star}<span>Favori</span>
          </button>`
        : "";
      html += `<div class="message message-assistant">
        <div class="message-avatar" aria-hidden="true">S</div>
        <div class="message-body">
          <div class="message-text">${renderMarkdown(msg.content)}</div>
          <div class="message-actions">
            <button type="button" class="msg-action-btn" data-speak-index="${idx}" title="Écouter les formes soninké de la réponse" aria-label="Écouter la réponse">
              ${ICONS.speakerLarge}<span>Écouter</span>
            </button>
            <button type="button" class="msg-action-btn" data-speak-soninke-index="${idx}" title="Écouter uniquement le soninké" aria-label="Écouter uniquement le soninké">
              ${ICONS.speaker}<span>Soninké</span>
            </button>
            <button type="button" class="msg-action-btn" data-explain-index="${idx}" title="Traduire les formes soninké en français" aria-label="Comprendre en français">
              ${ICONS.translate}<span>Français</span>
            </button>
            ${favAll}
            <button type="button" class="msg-action-btn" data-copy="${cleanCopy}" title="Copier la réponse" aria-label="Copier la réponse">
              ${ICONS.copy}<span>Copier</span>
            </button>
          </div>
        </div>
      </div>`;
    }
  });

  messagesArea.innerHTML = html;
  syncFavoriteButtons();
  scrollToBottom();
}

// Met à jour l'état visuel des étoiles de favoris.
function syncFavoriteButtons() {
  document.querySelectorAll("[data-fav-snk]").forEach((btn) => {
    const active = isFavorite(btn.dataset.favSnk, btn.dataset.favFr);
    btn.classList.toggle("is-favorite", active);
    btn.setAttribute("aria-pressed", active ? "true" : "false");
    btn.setAttribute("aria-label", `${active ? "Retirer des favoris" : "Ajouter aux favoris"}: ${btn.dataset.favSnk}`);
    btn.innerHTML = active ? ICONS.starFilled : ICONS.star;
  });
  document.querySelectorAll("[data-fav-msg-index]").forEach((btn) => {
    const conv = getConversation(state.activeConversationId);
    const msg = conv && conv.messages[Number(btn.dataset.favMsgIndex)];
    if (!msg) return;
    const items = pairItemsOf(msg.content);
    const allSaved = items.length > 0 && items.every((item) => isFavorite(item.snk, item.fr));
    btn.classList.toggle("is-favorite", allSaved);
  });
}

function scrollToBottom() {
  const container = $("#chat-container");
  if (!container) return;
  requestAnimationFrame(() => {
    container.scrollTop = container.scrollHeight;
  });
}

function showTypingIndicator() {
  removeTypingIndicator();
  const messagesArea = $("#messages-area");
  const indicator = document.createElement("div");
  indicator.className = "message message-assistant";
  indicator.id = "typing-indicator";
  indicator.innerHTML = `
    <div class="message-avatar">S</div>
    <div class="message-body">
      <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
    </div>
  `;
  messagesArea.appendChild(indicator);
  scrollToBottom();
}

function removeTypingIndicator() {
  const indicator = $("#typing-indicator");
  if (indicator) indicator.remove();
}

// ── Finalisation immédiate d'un flux en cours (permet d'envoyer à TOUT moment sans blocage) ──
function flushActiveStream() {
  if (!state.activeStream) return;
  const s = state.activeStream;
  state.activeStream = null;
  clearTimeout(s.timer);
  removeTypingIndicator();
  if (s.conv) {
    if (s.messageCreated && s.conv.messages.length > 0 && s.conv.messages[s.conv.messages.length - 1].role === "assistant") {
      s.conv.messages[s.conv.messages.length - 1].content = s.fullText;
    } else {
      s.conv.messages.push({ role: "assistant", content: s.fullText });
    }
    s.conv.updatedAt = Date.now();
    saveConversations();
  }
  state.isGenerating = false;
  updateSendButton();
  renderMessages();
}

// ── Streaming fluide + lecture vocale automatique ──
function streamMessage(conv, fullText, shouldSpeak = false) {
  const messagesArea = $("#messages-area");
  const lastMsg = messagesArea.querySelector(".message-assistant:last-child .message-text");
  const streamSession = { conv, fullText, messageCreated: true, timer: null };
  state.activeStream = streamSession;

  if (!lastMsg) {
    conv.messages[conv.messages.length - 1].content = fullText;
    conv.updatedAt = Date.now();
    saveConversations();
    state.activeStream = null;
    state.isGenerating = false;
    updateSendButton();
    renderMessages();
    if (shouldSpeak || state.voiceReplies) speakResponse(fullText);
    return;
  }

  // Démarrer la réponse vocale en direct dès l'affichage (instantané et compatible iOS/mobile !)
  if (shouldSpeak || state.voiceReplies) {
    speakResponse(fullText);
  }

  let index = 0;
  const chunkSize = Math.max(12, Math.ceil(fullText.length / 24));
  const frameDelay = 10;

  function typeNext() {
    if (state.activeStream !== streamSession) return;
    if (index >= fullText.length) {
      conv.messages[conv.messages.length - 1].content = fullText;
      conv.updatedAt = Date.now();
      saveConversations();
      state.activeStream = null;
      state.isGenerating = false;
      updateSendButton();
      renderMessages();
      return;
    }

    index = Math.min(index + chunkSize, fullText.length);
    lastMsg.innerHTML = renderMarkdown(fullText.slice(0, index));
    scrollToBottom();
    streamSession.timer = setTimeout(typeNext, frameDelay);
  }

  typeNext();
}

// ── Envoi universel : fonctionne À TOUT MOMENT (zéro blocage) ──
function submitMessage(text, opts = {}) {
  ensureAudioUnlocked();
  const value = String(text || "").trim();
  if (!value) {
    $("#message-input").focus();
    return;
  }
  if (state.isGenerating || state.activeStream) {
    flushActiveStream();
  }
  sendMessage(value, opts);
}

async function sendMessage(text, opts = {}) {
  const cleanText = String(text || "").trim();
  if (!cleanText) return;

  stopSpeech();
  if (state.listening) cancelListening();

  // Créer une discussion si nécessaire
  if (!state.activeConversationId) {
    const conv = createConversation(cleanText.slice(0, 40));
    state.activeConversationId = conv.id;
    updateTopbarTitle();
  }

  const conv = getConversation(state.activeConversationId);
  if (!conv) return;

  const userMsg = { role: "user", content: cleanText };
  if (opts.voiceNoteUrl) userMsg.voiceNoteUrl = opts.voiceNoteUrl;
  conv.messages.push(userMsg);

  if (conv.messages.length === 1) {
    conv.title = cleanText.slice(0, 40) + (cleanText.length > 40 ? "…" : "");
  }
  conv.updatedAt = Date.now();
  saveConversations();

  renderMessages();
  renderConversationList();
  clearInput();

  state.isGenerating = true;
  updateSendButton();
  showTypingIndicator();

  // Attendre les données du corpus si la page vient tout juste de s'ouvrir !
  if (state.dataReady) {
    try { await state.dataReady; } catch {}
  }

  const response = generateResponse(cleanText);
  const pendingSession = { conv, fullText: response, messageCreated: false, timer: null };
  state.activeStream = pendingSession;

  pendingSession.timer = setTimeout(() => {
    if (state.activeStream !== pendingSession) return;
    removeTypingIndicator();
    conv.messages.push({ role: "assistant", content: "" });
    pendingSession.messageCreated = true;
    renderMessages();
    streamMessage(conv, response, !!opts.forceVoiceReply);
  }, 180);
}

// Envoi d'une note vocale enregistrée quand le navigateur n'a pas de moteur STT cloud
async function sendRecordedVoiceMessage(voiceNoteUrl) {
  ensureAudioUnlocked();
  if (state.isGenerating || state.activeStream) flushActiveStream();

  if (state.dataReady) {
    try { await state.dataReady; } catch {}
  }

  if (!state.activeConversationId) {
    const conv = createConversation("Message vocal soninké");
    state.activeConversationId = conv.id;
    updateTopbarTitle();
  }
  const conv = getConversation(state.activeConversationId);
  if (!conv) return;

  conv.messages.push({
    role: "user",
    content: "Message vocal enregistré",
    voiceNoteUrl,
  });
  conv.updatedAt = Date.now();
  saveConversations();
  renderMessages();
  renderConversationList();

  state.isGenerating = true;
  updateSendButton();
  showTypingIndicator();

  const response =
    `Votre message vocal a bien été enregistré : il est réécoutable juste au-dessus.\n\n` +
    `Ce navigateur ne fournit pas de transcription automatique fiable, donc je ne devine pas son contenu. Écrivez votre question pour une réponse précise.\n\n` +
    `**Formes attestées pour démarrer**\n` +
    soninkeBlock("Xa wouy Diom", "Bonjour ! (salutation respectueuse)", "expression") +
    soninkeBlock("Toora nta", "Tout va bien.", "expression") +
    soninkeBlock("Nawari", "Merci.", "mot") +
    soninkeBlock("oyi waxati", "Au revoir.", "expression") +
    `Chaque forme est lue avec la voix de référence lorsqu'un enregistrement existe.\n\n` +
    levelNote();
  const pendingSession = { conv, fullText: response, messageCreated: false, timer: null };
  state.activeStream = pendingSession;
  pendingSession.timer = setTimeout(() => {
    if (state.activeStream !== pendingSession) return;
    removeTypingIndicator();
    conv.messages.push({ role: "assistant", content: "" });
    pendingSession.messageCreated = true;
    renderMessages();
    streamMessage(conv, response, true);
  }, 180);
}

// ── Liste des discussions ──
function renderConversationList() {
  const list = $("#conversation-list");
  const searchQuery = ($("#search-conversations").value || "").toLowerCase();

  let filtered = state.conversations;
  if (searchQuery) {
    filtered = filtered.filter(
      (c) =>
        c.title.toLowerCase().includes(searchQuery) ||
        c.messages.some((m) => String(m.content || "").toLowerCase().includes(searchQuery))
    );
  }

  if (filtered.length === 0) {
    list.innerHTML = `<div class="conv-empty">
      ${searchQuery ? "Aucune discussion trouvée" : "Aucune discussion pour le moment"}
    </div>`;
    return;
  }

  const now = Date.now();
  const day = 86400000;
  const groups = { "Aujourd'hui": [], "Hier": [], "7 derniers jours": [], "30 derniers jours": [], "Plus ancien": [] };

  for (const conv of filtered) {
    const age = now - conv.updatedAt;
    if (age < day) groups["Aujourd'hui"].push(conv);
    else if (age < 2 * day) groups["Hier"].push(conv);
    else if (age < 7 * day) groups["7 derniers jours"].push(conv);
    else if (age < 30 * day) groups["30 derniers jours"].push(conv);
    else groups["Plus ancien"].push(conv);
  }

  let html = "";
  for (const [label, convs] of Object.entries(groups)) {
    if (!convs.length) continue;
    html += `<div class="conv-group-label">${label}</div>`;
    for (const conv of convs) {
      const isActive = conv.id === state.activeConversationId;
      html += `<div class="conv-item${isActive ? " active" : ""}" data-conv-id="${conv.id}">
        <span class="conv-item-title">${esc(conv.title)}</span>
        <button type="button" class="conv-item-menu" data-menu-id="${conv.id}" aria-label="Options">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="5" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="12" cy="19" r="1"/></svg>
        </button>
      </div>`;
    }
  }

  list.innerHTML = html;

  list.querySelectorAll(".conv-item").forEach((item) => {
    item.addEventListener("click", (e) => {
      if (e.target.closest(".conv-item-menu")) return;
      openConversation(item.dataset.convId);
    });
  });

  list.querySelectorAll(".conv-item-menu").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      showContextMenu(btn, btn.dataset.menuId);
    });
  });
}

function openConversation(id) {
  if (state.activeStream) flushActiveStream();
  state.activeConversationId = id;
  renderConversationList();
  renderMessages();
  updateTopbarTitle();
  closeSidebar();
}

function startNewChat() {
  if (state.activeStream) flushActiveStream();
  stopSpeech();
  state.activeConversationId = null;
  renderConversationList();
  renderMessages();
  updateTopbarTitle();
  closeSidebar();
  $("#message-input").focus();
}

function updateTopbarTitle() {
  const title = $("#topbar-title");
  if (state.activeConversationId) {
    const conv = getConversation(state.activeConversationId);
    title.textContent = conv ? conv.title : "Nouvelle discussion";
  } else {
    title.textContent = "Nouvelle discussion";
  }
}

// ── Context Menu & Modale de suppression ──
let contextMenuConvId = null;

function showContextMenu(anchor, convId) {
  contextMenuConvId = convId;
  const menu = $("#context-menu");
  const rect = anchor.getBoundingClientRect();
  menu.style.top = rect.bottom + 4 + "px";
  menu.style.left = Math.min(rect.left, window.innerWidth - 180) + "px";
  menu.classList.add("visible");

  const close = (e) => {
    if (!menu.contains(e.target)) {
      menu.classList.remove("visible");
      document.removeEventListener("click", close);
    }
  };
  setTimeout(() => document.addEventListener("click", close), 10);
}

function handleContextAction(action) {
  $("#context-menu").classList.remove("visible");
  if (!contextMenuConvId) return;

  if (action === "rename") {
    const conv = getConversation(contextMenuConvId);
    if (!conv) return;
    const newTitle = prompt("Nouveau titre :", conv.title);
    if (newTitle && newTitle.trim()) {
      conv.title = newTitle.trim().slice(0, 40);
      conv.updatedAt = Date.now();
      saveConversations();
      renderConversationList();
      updateTopbarTitle();
    }
  } else if (action === "delete") {
    showDeleteModal(contextMenuConvId);
  }
}

let deleteTargetId = null;

function showDeleteModal(convId) {
  deleteTargetId = convId;
  $("#delete-modal").classList.add("visible");
}

function confirmDelete() {
  if (deleteTargetId) {
    deleteConversation(deleteTargetId);
    if (state.activeConversationId === deleteTargetId) {
      state.activeConversationId = null;
    }
    renderConversationList();
    renderMessages();
    updateTopbarTitle();
  }
  deleteTargetId = null;
  $("#delete-modal").classList.remove("visible");
}

// ── Gestion unifiée des panneaux du menu (Assistant vocal, Lexique Audio, Favoris, Paramètres) ──
function syncNavActiveState() {
  $$(".sidebar-action[data-open-panel]").forEach((btn) => {
    const modal = $(`#${btn.dataset.openPanel}`);
    const isOpen = Boolean(modal && modal.classList.contains("visible"));
    btn.classList.toggle("active", isOpen);
    btn.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
}

function closeAllModals() {
  $$(".modal-overlay.visible").forEach((m) => m.classList.remove("visible"));
  syncNavActiveState();
}

function openVoicePanel() {
  closeAllModals();
  closeSidebar();
  const modal = $("#voice-modal");
  if (modal) {
    modal.classList.add("visible");
    syncNavActiveState();
    const quickInput = $("#quick-translate-input");
    if (quickInput) quickInput.focus();
  }
}

function openSettingsPanel() {
  closeAllModals();
  closeSidebar();
  const modal = $("#settings-modal");
  if (modal) {
    modal.classList.add("visible");
    syncNavActiveState();
  }
}

// Écoute d'un extrait réel de la voix de référence, avec sa traduction.
let referenceSampleCursor = 0;

function playReferenceSample() {
  ensureAudioUnlocked();
  const priority = [
    "Daga goli", "Li taxu", "Mpai reni", "Mpai telle",
    "lemine ke", "maro ke", "koota su", "an wouydiom", "Xa wouy Diom",
  ];
  const available = priority.map((text) => findAudioInfo(text)).filter(Boolean);
  let info = available.length
    ? available[referenceSampleCursor++ % available.length]
    : state.audioList.find((item) => item && item.url);
  if (!info) {
    const emptyMsg = "Aucun enregistrement de référence n'est encore disponible dans le corpus local.";
    showVoiceStatus(emptyMsg, 4200);
    const refStatus = $("#ref-voice-status");
    if (refStatus) {
      refStatus.textContent = emptyMsg;
      refStatus.hidden = false;
    }
    return;
  }
  const entry = state.entries.find((e) => normalizeWord(e.soninke) === normalizeWord(info.text));
  const translation = info.francais || (entry ? entry.francais : "");
  const summary = `Voix de référence · « ${info.text} »${translation ? ` — ${translation}` : ""}`;
  showVoiceStatus(summary, 4200);
  const refStatus = $("#ref-voice-status");
  if (refStatus) {
    refStatus.textContent = summary;
    refStatus.hidden = false;
  }
  playWordAudio(info.text);
}

// ── Favoris : proverbes, histoires, phrases et traductions à réécouter ──
function openFavoritesPanel() {
  closeAllModals();
  closeSidebar();
  renderFavorites();
  const modal = $("#favorites-modal");
  if (modal) {
    modal.classList.add("visible");
    syncNavActiveState();
  }
}

function matchesFavoriteFilter(item, filter) {
  if (!filter || filter === "all") return true;
  const type = String(item.type || "").toLowerCase();
  if (filter === "traduction") {
    return type === "traduction" || type === "mot" || type === "expression";
  }
  return type === filter;
}

function favoriteTypeLabel(type) {
  switch (String(type || "").toLowerCase()) {
    case "proverbe": return "Proverbe";
    case "histoire": return "Histoire";
    case "phrase": return "Phrase";
    case "expression": return "Expression";
    case "mot":
    case "traduction":
    default: return "Traduction";
  }
}

function renderFavorites() {
  const list = $("#favorites-list");
  if (!list) return;
  const filter = state.favoriteFilter;
  const items = state.favorites.filter((f) => matchesFavoriteFilter(f, filter));

  if (!items.length) {
    list.innerHTML = `<div class="favorites-empty">
      ${state.favorites.length
        ? "Aucun favori enregistré dans cette catégorie."
        : "Aucun favori pour le moment.<br>Enregistrez vos proverbes, histoires, phrases et traductions ci-dessus ou via l'étoile à côté de chaque forme soninké."}
    </div>`;
    updateFavoritesCount();
    return;
  }

  list.innerHTML = items
    .map((f) => {
      const audio = findAudioInfo(f.snk);
      const typeLabel = favoriteTypeLabel(f.type);
      return `<div class="favorite-item" data-fav-key="${esc(favoriteKey(f.snk, f.fr))}">
        <div class="favorite-item-main">
          <div class="favorite-item-snk" lang="snk">${esc(f.snk)}</div>
          <div class="favorite-item-fr">${esc(f.fr || "Traduction non renseignée")}</div>
          <div class="favorite-item-meta">${typeLabel} · ${audio ? "Voix de référence disponible" : "Audio de référence à enregistrer"}</div>
        </div>
        <div class="favorite-item-actions">
          <button type="button" class="audio-play-btn${audio ? "" : " audio-unavailable"}" data-audio-word="${esc(f.snk)}" title="Écouter avec la voix de référence" aria-label="Écouter ${esc(f.snk)}">${ICONS.speaker}</button>
          <button type="button" class="favorite-remove" data-fav-remove="${esc(f.snk)}|${esc(f.fr)}" title="Retirer des favoris" aria-label="Retirer ${esc(f.snk)} des favoris">${ICONS.trash}</button>
        </div>
      </div>`;
    })
    .join("");

  updateFavoritesCount();
}

// ── Lexique Audio & Explorateur des 576 Audios Intégrés ──
let dictDirection = "all";

function openDictionaryPanel(initialDir = null) {
  closeAllModals();
  closeSidebar();
  if (initialDir) {
    dictDirection = initialDir;
    $$(".dict-filter[data-dir]").forEach((b) => b.classList.toggle("active", b.dataset.dir === dictDirection));
  }
  const modal = $("#dictionary-modal");
  if (modal) {
    modal.classList.add("visible");
    syncNavActiveState();
  }
  renderDictResults();
  const searchInput = $("#dict-search");
  if (searchInput) searchInput.focus();
}

function renderDictResults() {
  const query = normalizeWord($("#dict-search").value);
  const container = $("#dict-results");

  // Onglet dédié aux enregistrements de référence
  if (dictDirection === "audio") {
    const matchingAudios = state.audioList
      .filter((item) => {
        if (isExcludedForm(item.text)) return false;
        if (!query) return true;
        return normalizeWord(item.text).includes(query) || normalizeWord(item.francais || "").includes(query) || String(item.id || "").includes(query);
      })
      // Afficher d'abord le dernier lot validé pour qu'il soit visible sans devoir parcourir tout l'historique.
      .sort((a, b) => {
        const aRecent = String(a.url || "").includes("audio/lots/lot-100-2026-10-24/") ? 1 : 0;
        const bRecent = String(b.url || "").includes("audio/lots/lot-100-2026-10-24/") ? 1 : 0;
        return bRecent - aRecent || normalizeWord(a.text).localeCompare(normalizeWord(b.text), "fr");
      })
      .slice(0, MAX_DISPLAY);

    if (!matchingAudios.length) {
      container.innerHTML = `<div class="dict-empty">Aucun enregistrement correspondant.</div>`;
      return;
    }

    container.innerHTML = matchingAudios
      .map((a) => {
        const fav = isFavorite(a.text, a.francais || "");
        return `<div class="dict-card">
          <div class="dict-card-head">
            <h4 lang="snk">${esc(a.text)}</h4>
            <button type="button" class="audio-play-btn" data-audio-word="${esc(a.text)}" title="Écouter avec la voix de référence" aria-label="Écouter ${esc(a.text)}">${ICONS.speaker}<span>Écouter</span></button>
            <button type="button" class="fav-toggle${fav ? " is-favorite" : ""}" data-fav-snk="${esc(a.text)}" data-fav-fr="${esc(a.francais || "")}" data-fav-type="${a.text.split(/\s+/).length > 1 ? "phrase" : "mot"}" aria-pressed="${fav ? "true" : "false"}" aria-label="Ajouter ${esc(a.text)} aux favoris">${fav ? ICONS.starFilled : ICONS.star}</button>
          </div>
          <div class="dict-translation">${a.unmapped ? "Correspondance lexicale à identifier — fichier conservé sans attribution de mot." : a.francais ? esc(a.francais) : "Traduction non renseignée"}</div>
          <div class="dict-meta">
            <span class="pair-badge ${a.unmapped ? "is-review" : (a.linguistic_validation || a.validation_prononciation === "validee_par_referent" || a.validation_prononciation === "validee_par_referent_linguistique") ? "is-attested" : a.generated ? "is-review" : "is-attested"}">${a.unmapped ? "WAV conservé · mot à identifier" : (a.linguistic_validation || a.validation_prononciation === "validee_par_referent" || a.validation_prononciation === "validee_par_referent_linguistique") ? "Prononciation validée par le référent" : a.generated ? "Audio généré · prononciation à valider" : "Enregistrement de référence"}</span>
            <span>${esc(String(a.url || "").split("/").pop() || "")}</span>
          </div>
        </div>`;
      })
      .join("");
    return;
  }

  const results = state.entries
    .filter((entry) => {
      if (isExcludedForm(entry.soninke)) return false;
      const snk = normalizeWord(entry.soninke);
      const fr = normalizeWord(entry.francais);
      const variants = normalizeWord(entry.variantes || "");
      if (dictDirection === "snk") return !query || snk.includes(query) || variants.includes(query);
      if (dictDirection === "fr") return !query || fr.includes(query);
      return !query || snk.includes(query) || fr.includes(query) || variants.includes(query);
    })
    .slice(0, MAX_DISPLAY);

  if (!results.length) {
    container.innerHTML = `<div class="dict-empty">Aucun résultat dans le corpus.</div>`;
    return;
  }

  container.innerHTML = results
    .map((e) => {
      const att = attestationOf(e.soninke);
      const audio = att.audio || findAudioInfo(e.soninke);
      const fav = isFavorite(e.soninke, e.francais);
      const type = e.soninke.split(/\s+/).length > 1 ? "phrase" : "mot";
      return `<div class="dict-card">
        <div class="dict-card-head">
          <h4 lang="snk">${esc(e.soninke)}</h4>
          <button type="button" class="audio-play-btn${audio ? "" : " audio-unavailable"}" data-audio-word="${esc(e.soninke)}" title="Écouter avec la voix de référence" aria-label="Écouter ${esc(e.soninke)}">${ICONS.speaker}</button>
          <button type="button" class="fav-toggle${fav ? " is-favorite" : ""}" data-fav-snk="${esc(e.soninke)}" data-fav-fr="${esc(e.francais)}" data-fav-type="${type}" aria-pressed="${fav ? "true" : "false"}" aria-label="Ajouter ${esc(e.soninke)} aux favoris">${fav ? ICONS.starFilled : ICONS.star}</button>
        </div>
        <div class="dict-translation">${esc(e.francais)}</div>
        <div class="dict-meta">
          <span class="pair-badge ${att.cls}">${att.label}</span>
          ${e.categorie ? `<span>${esc(e.categorie)}</span>` : ""}
        </div>
      </div>`;
    })
    .join("");
}

// ── Sidebar Toggle ──
function openSidebar() {
  $("#sidebar").classList.add("open");
  $("#sidebar-overlay").classList.add("visible");
  document.body.style.overflow = "hidden";
}

function closeSidebar() {
  $("#sidebar").classList.remove("open");
  $("#sidebar-overlay").classList.remove("visible");
  document.body.style.overflow = "";
}

// ── Input Handling (Send button JAMAIS désactivé) ──
function clearInput() {
  const input = $("#message-input");
  input.value = "";
  autoResize(input);
  updateSendButton();
}

function autoResize(textarea) {
  textarea.style.height = "auto";
  textarea.style.height = Math.min(textarea.scrollHeight || 28, 180) + "px";
}

function updateSendButton() {
  const input = $("#message-input");
  const btn = $("#send-btn");
  if (!btn || !input) return;
  btn.disabled = false; // Toujours cliquable !
  btn.classList.add("enabled");
  btn.classList.toggle("loading", state.isGenerating);
}

// ── Copy to clipboard ──
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
      return true;
    } catch {
      return false;
    } finally {
      document.body.removeChild(textarea);
    }
  }
}

// ── Chargement unifié de TOUTES les données du dépôt ──
async function fetchTextSafe(url) {
  try {
    const r = await fetch(url);
    return r.ok ? await r.text() : "";
  } catch {
    return "";
  }
}

async function loadAllData() {
  const [
    baseCsv,
    manifestCsv,
    auditCsv,
    candidatesCsv,
    headFaceCsv,
    samplesJsonl,
    fiche1Csv,
    fiche4Csv,
    revueCsv,
    renvoisCsv,
  ] = await Promise.all([
    fetchTextSafe(DATA_URL),
    fetchTextSafe(MANIFEST_URL),
    fetchTextSafe(AUDIO_AUDIT_URL),
    fetchTextSafe(CANDIDATES_URL),
    fetchTextSafe(HEAD_FACE_URL),
    fetchTextSafe(SAMPLES_URL),
    fetchTextSafe(FICHE_VAL_1_URL),
    fetchTextSafe(FICHE_VAL_4_URL),
    fetchTextSafe(REVUE_DICT_URL),
    fetchTextSafe(RENVOIS_URL),
  ]);

  const seenHeadwords = new Set();
  const seenVariants = new Set();
  const entries = [];
  const pushEntry = (entry, { checkVariants = true } = {}) => {
    const snk = String(entry.soninke || "").trim();
    const fr = String(entry.francais || "").trim();
    if (!snk || !fr) return;
    const snkKey = normalizeWord(snk);
    if (!snkKey || seenHeadwords.has(snkKey)) return;
    if (checkVariants && seenVariants.has(snkKey)) return;
    seenHeadwords.add(snkKey);
    entries.push({ ...entry, soninke: snk, francais: fr });
  };

  // 1. Lexique principal de référence (dédoublonné et enrichi)
  for (const row of parseCSV(baseCsv, ";")) {
    pushEntry(
      {
        id: row.id || uid(),
        soninke: row.soninke,
        francais: row.francais,
        categorie: row.categorie,
        source: row.source,
        statut: row.statut,
        variantes: row.variantes,
        exemple_original: row.exemple_original,
        isCandidate: /a_verifier/i.test(row.statut || ""),
      },
      { checkVariants: false }
    );
  }
  for (const e of entries) {
    for (const v of String(e.variantes || "").split(/[;,|]/)) {
      const vk = normalizeWord(v);
      if (vk) seenVariants.add(vk);
    }
  }

  // 2. Lot Tête & Visage
  for (const row of parseCSV(headFaceCsv, ",")) {
    pushEntry({
      id: row.id || uid(),
      soninke: row.soninke,
      francais: row.francais,
      categorie: "partie_du_corps",
      source: row.source_lexicale,
      statut: row.statut_lexical,
      variantes: "",
      exemple_original: row.notes || "",
      isCandidate: /a_verifier/i.test(row.statut_lexical || ""),
    });
  }

  // 3. Fiches de validation du référent
  for (const csvText of [fiche1Csv, fiche4Csv]) {
    for (const row of parseCSV(csvText, ";")) {
      const soninke = (row.lemme_corrige || row.lemme || "").replace(/\d+$/, "").trim();
      const francais = (row.traduction_fr_confirmee || row.glose_extraite_automatiquement || "").trim();
      if (soninke && francais) {
        pushEntry({
          id: `FICHE-${row.paragraphe_source || uid()}`,
          soninke,
          francais,
          categorie: "",
          source: row.source || "Fiche validation référent",
          statut: row.decision || "valide_par_referent",
          variantes: row.variante || "",
          exemple_original: row.texte_source_complet || "",
          isCandidate: !/valid/i.test(row.decision || ""),
        });
      }
    }
  }

  // 4. Revue d'enrichissement & renvois du dictionnaire soninké
  for (const row of parseCSV(revueCsv, ";")) {
    const soninke = (row.lemme || "").replace(/\d+$/, "").trim();
    const francais = (row.glose_extraite_automatiquement || row.traductions_projet_existantes || "").replace(/^"+|"+$/g, "").trim();
    if (soninke && francais) {
      pushEntry({
        id: `REV-${row.paragraphe_source || uid()}`,
        soninke,
        francais,
        categorie: "",
        source: row.source || "Dictionnaire soninké",
        statut: row.statut || "a_verifier",
        variantes: row.variante || "",
        exemple_original: row.texte_source || "",
        isCandidate: true,
      });
    }
  }

  for (const row of parseCSV(renvoisCsv, ";")) {
    const soninke = (row.lemme_source || "").replace(/\d+$/, "").trim();
    const francais = (row.glose_extraite || "").trim();
    if (soninke && francais) {
      pushEntry({
        id: `RENV-${row.paragraphe_source || uid()}`,
        soninke,
        francais,
        categorie: "",
        source: row.source || "Renvoi dictionnaire",
        statut: "a_verifier",
        variantes: row.variante_source || "",
        exemple_original: row.texte_source_complet || "",
        isCandidate: true,
      });
    }
  }

  // 5. Candidats externes (jours de la semaine, pronoms, formes tonales CNRS, Soninkara, Dicosoninke)
  for (const row of parseCSV(candidatesCsv, ",")) {
    pushEntry({
      id: row.candidate_id || uid(),
      soninke: row.soninke,
      francais: row.francais,
      categorie: "",
      source: row.source_url,
      statut: row.validation_status || "a_verifier",
      variantes: "",
      exemple_original: row.notes || "",
      isCandidate: true,
    });
  }

  state.entries = entries;

  // 6. Phrases parallèles soninké–français (soninke-samples.jsonl)
  if (samplesJsonl) {
    const parsedSamples = [];
    for (const line of samplesJsonl.split(/\r?\n/)) {
      if (!line.trim()) continue;
      try {
        const obj = JSON.parse(line);
        if (obj.soninke && obj.french) parsedSamples.push(obj);
      } catch {}
    }
    state.samples = parsedSamples;
  }

  // 7. Indexation complète des 576 enregistrements WAV du référent
  if (manifestCsv && auditCsv) {
    const manifest = parseCSV(manifestCsv, ",");
    const audit = parseCSV(auditCsv, ",");
    const successful = new Set(
      audit.filter((row) => ["copied_from_source", "already_present"].includes(row.status)).map((row) => row.id)
    );
    const entryBySnk = new Map();
    for (const e of state.entries) {
      const k = normalizeWord(e.soninke);
      if (k && !entryBySnk.has(k)) entryBySnk.set(k, e);
    }

    const audioList = [];
    for (const row of manifest) {
      if (!successful.has(row.id) || !row.text) continue;
      const url = `audio/${encodeURIComponent(row.id)}.wav`;
      const key = normalizeWord(row.text);
      const ortho = normalizeSoninkeOrtho(row.text);
      const matchedEntry = entryBySnk.get(key);
      const info = {
        id: row.id,
        text: row.text,
        url,
        francais: matchedEntry ? matchedEntry.francais : (/phrase de test/i.test(row.source || "") ? "Phrase audio validée par le référent" : ""),
      };
      audioList.push(info);
      if (!state.audioByWord.has(key)) state.audioByWord.set(key, info);
      if (ortho && !state.audioByOrtho.has(ortho)) state.audioByOrtho.set(ortho, info);

      // Relier les formes fléchies enregistrées (ex. diambe-ye, dugu-nde, lemine ke, maro ke) à leur racine
      const stem = key.replace(/-(nde|ye|ŋe)$/, "").split(/\s+/)[0];
      if (stem && stem !== key) {
        if (!state.relatedAudioByStem.has(stem)) state.relatedAudioByStem.set(stem, []);
        state.relatedAudioByStem.get(stem).push(info);
      }
    }
    state.audioList = audioList;
  }

  // 8. Audios générés : dès qu'un WAV est présent dans le manifeste de mémoire,
  // il est intégré à l'index de lecture et à la liste Lexique & Audios.
  try {
    const response = await fetch("data/voice-memory.json");
    if (response.ok) {
      const memory = await response.json();
      for (const item of (Array.isArray(memory.audio) ? memory.audio : [])) {
        if (!item || !item.text || !item.url) continue;
        const key = normalizeWord(item.text);
        const ortho = normalizeSoninkeOrtho(item.text);
        if (!key || state.audioByWord.has(key)) continue; // conserve toujours l'audio déjà présent
        const matchedEntry = state.entries.find((entry) => normalizeWord(entry.soninke) === key);
        const info = {
          ...item,
          francais: item.francais || (matchedEntry ? matchedEntry.francais : ""),
          generated: String(item.url).startsWith("audio/generated/"),
        };
        state.audioByWord.set(key, info);
        if (ortho && !state.audioByOrtho.has(ortho)) state.audioByOrtho.set(ortho, info);
        state.audioList.push(info);
        const stem = key.replace(/-(nde|ye|ŋe)$/, "").split(/\s+/)[0];
        if (stem && stem !== key) {
          if (!state.relatedAudioByStem.has(stem)) state.relatedAudioByStem.set(stem, []);
          state.relatedAudioByStem.get(stem).push(info);
        }
      }
    }
  } catch { /* Le corpus original reste disponible hors ligne. */ }

  // 8 bis. WAV conservés sans correspondance lexicale : les rendre écoutables
  // dans l’onglet audio sans leur attribuer artificiellement un mot soninké.
  try {
    const response = await fetch("data/unmapped-audio.json");
    if (response.ok) {
      const unmapped = await response.json();
      for (const item of (Array.isArray(unmapped) ? unmapped : [])) {
        if (!item || !item.text || !item.url) continue;
        const key = normalizeWord(item.text);
        if (!key || state.audioByWord.has(key)) continue;
        state.audioByWord.set(key, item);
        state.audioList.push(item);
      }
    }
  } catch { /* Les entrées lexicales déjà disponibles restent utilisables. */ }

  // 9. Voix de référence : source unique de tous les contenus audio
  try {
    const response = await fetch(VOICE_MEMORY_URL);
    if (response.ok) {
      const memory = await response.json();
      state.referenceVoice = {
        model: memory.model || "",
        references: Array.isArray(memory.references) ? memory.references : [],
        count: state.audioByWord.size,
      };
    }
  } catch {}
  state.referenceVoice.count = state.audioByWord.size;

  // 10. Variantes graphiques reliées à l'enregistrement de référence de leur lemme
  for (const entry of state.entries) {
    const info = findAudioInfo(entry.soninke);
    if (!info) continue;
    for (const variant of String(entry.variantes || "").split(/[;,|]/)) {
      const key = normalizeWord(variant);
      if (!key || state.audioByWord.has(key) || state.audioByVariant.has(key)) continue;
      state.audioByVariant.set(key, info);
    }
  }

  // 11. Contrôle linguistique : formes écartées (jamais présentées comme soninké)
  loadGuard();
  try {
    const response = await fetch(GUARD_URL);
    if (response.ok) {
      const payload = await response.json();
      applyGuard(payload);
      try { localStorage.setItem("soninkegpt_guard_cache", JSON.stringify(payload)); } catch {}
    }
  } catch {}

  updateCorpusStatus();
}

function updateCorpusStatus() {
  const count = state.entries.length;
  const audioCount = state.audioByWord.size;
  const lexEl = $("#lexicon-count");
  const aboutEl = $("#about-count");
  const aboutAudioEl = $("#about-audio-count");
  const statusEl = $("#corpus-status");
  if (lexEl) lexEl.textContent = count || "—";
  if (aboutEl) aboutEl.textContent = count || "—";
  if (aboutAudioEl) aboutAudioEl.textContent = audioCount || "—";
  if (statusEl) {
    let status = `${count} entrées`;
    if (audioCount) status += ` · ${audioCount} audios de référence`;
    statusEl.textContent = status;
  }
  const refInfo = $("#reference-voice-info");
  if (refInfo) {
    const model = state.referenceVoice && state.referenceVoice.model ? state.referenceVoice.model : "corpus du référent";
    refInfo.textContent = `Voix de référence : ${model}, ${state.referenceVoice.references?.length || 0} enregistrements sources, ${audioCount} formes indexées. Aucune voix de synthèse du navigateur n'est utilisée.`;
  }
  const audioFilterBtn = document.querySelector('.dict-filter[data-dir="audio"]');
  if (audioFilterBtn && audioCount) {
    audioFilterBtn.textContent = `Audios (${audioCount})`;
  }
  updateFavoritesCount();
}

// ── Event Listeners ──
function initEvents() {
  const input = $("#message-input");
  const form = $("#chat-form");

  // Déverrouiller l'audio mobile dès le tout premier geste tactile / clic / clavier
  document.addEventListener("pointerdown", ensureAudioUnlocked, { once: true, passive: true });
  document.addEventListener("keydown", ensureAudioUnlocked, { once: true, passive: true });

  // Suivi de Shift pour distinguer Entrée (envoyer) de Shift+Entrée (retour à la ligne)
  document.addEventListener("keydown", (e) => { if (e.key === "Shift") state.shiftHeld = true; });
  document.addEventListener("keyup", (e) => { if (e.key === "Shift") state.shiftHeld = false; });

  // 1. Soumission du formulaire (<form id="chat-form">)
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      submitMessage(input.value);
    });
  }

  // 2. Clavier sur #message-input : Entrée fonctionne À TOUT MOMENT (desktop + iOS + Android)
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submitMessage(input.value);
    }
  });

  // 3. Support claviers virtuels mobiles (iOS Safari / WKWebView beforeinput insertLineBreak / insertParagraph)
  input.addEventListener("beforeinput", (e) => {
    if (!state.shiftHeld && (e.inputType === "insertLineBreak" || e.inputType === "insertParagraph")) {
      e.preventDefault();
      submitMessage(input.value);
    }
  });

  // 4. Garde-fou mobile universel sur input (si un clavier mobile insère '\n' directement)
  input.addEventListener("input", () => {
    if (!state.shiftHeld && input.value.endsWith("\n")) {
      const cleaned = input.value.replace(/\r?\n+$/, "");
      input.value = cleaned;
      if (cleaned.trim()) {
        submitMessage(cleaned);
        return;
      }
    }
    autoResize(input);
    updateSendButton();
  });

  // 5. Touche Entrée globale (même si le focus est ailleurs sur la page, ou pour valider la dictée vocale)
  document.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      if (state.listening) {
        e.preventDefault();
        finishVoiceSession();
        return;
      }
      const target = e.target;
      const tag = target && target.tagName ? target.tagName.toLowerCase() : "";
      const isTextField = tag === "textarea" || (tag === "input" && target.type !== "checkbox" && target.type !== "radio");
      const isActivatable = tag === "button" || tag === "a";
      if (!isTextField && !isActivatable && !target.closest(".modal-overlay") && !target.closest(".context-menu")) {
        if (input.value.trim()) {
          e.preventDefault();
          submitMessage(input.value);
        }
      }
    }
  });

  // 6. Clic direct sur le bouton Envoyer (au cas où un environnement ne déclenche pas form.submit)
  $("#send-btn").addEventListener("click", (e) => {
    e.preventDefault();
    submitMessage(input.value);
  });

  // 7. Assistant Vocal Soninké (micro bas de page + onglet Assistant vocal)
  const triggerVoiceAssistant = () => {
    closeAllModals();
    closeSidebar();
    if (state.listening) finishVoiceSession();
    else startListening();
  };

  $("#mic-btn").addEventListener("click", triggerVoiceAssistant);
  const welcomeMic = $("#welcome-mic-btn");
  if (welcomeMic) welcomeMic.addEventListener("click", triggerVoiceAssistant);

  const sidebarVoice = $("#sidebar-voice-btn");
  if (sidebarVoice) sidebarVoice.addEventListener("click", openVoicePanel);
  const voiceModalClose = $("#voice-modal-close");
  if (voiceModalClose) voiceModalClose.addEventListener("click", closeAllModals);

  const quickTranslateForm = $("#quick-translate-form");
  if (quickTranslateForm) {
    quickTranslateForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const field = $("#quick-translate-input");
      const query = field ? field.value.trim() : "";
      if (!query) {
        if (field) field.focus();
        return;
      }
      field.value = "";
      closeAllModals();
      submitMessage(`Traduis « ${query} » en soninké`);
    });
  }

  const voiceFinishBtn = $("#voice-finish-btn");
  if (voiceFinishBtn) voiceFinishBtn.addEventListener("click", finishVoiceSession);
  const voiceCancelBtn = $("#voice-cancel-btn");
  if (voiceCancelBtn) voiceCancelBtn.addEventListener("click", cancelListening);

  // Lecteurs d'aperçu de la voix de référence (Lexique Audio + Paramètres)
  const welcomeGreetBtn = $("#welcome-greet-audio-btn");
  if (welcomeGreetBtn) {
    welcomeGreetBtn.addEventListener("click", () => playReferenceSample());
  }
  const settingsTestVoiceBtn = $("#settings-test-voice-btn");
  if (settingsTestVoiceBtn) {
    settingsTestVoiceBtn.addEventListener("click", () => playReferenceSample());
  }

  // 8. Boutons d'activation de la réponse audio vocale automatique
  $("#voice-reply-btn").addEventListener("click", () => setVoiceReplies(!state.voiceReplies));
  const topbarVoiceBtn = $("#topbar-voice-btn");
  if (topbarVoiceBtn) topbarVoiceBtn.addEventListener("click", () => setVoiceReplies(!state.voiceReplies));
  const voiceSwitch = $("#voice-replies-switch");
  if (voiceSwitch) voiceSwitch.addEventListener("click", () => setVoiceReplies(!state.voiceReplies));

  // New chat buttons
  $("#new-chat-btn").addEventListener("click", () => {
    closeAllModals();
    startNewChat();
  });
  $("#new-chat-btn-top").addEventListener("click", () => {
    closeAllModals();
    startNewChat();
  });
  $$(".brand, .topbar-brand").forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      closeAllModals();
      startNewChat();
    });
  });

  // Menu mobile & bascule barre latérale bureau
  $("#menu-btn").addEventListener("click", openSidebar);
  const sidebarToggleBtn = $("#sidebar-toggle-btn");
  if (sidebarToggleBtn) {
    sidebarToggleBtn.addEventListener("click", () => {
      const sb = $("#sidebar");
      if (sb) sb.classList.toggle("collapsed");
    });
  }
  $("#sidebar-close").addEventListener("click", closeSidebar);
  $("#sidebar-overlay").addEventListener("click", closeSidebar);

  // Thème
  $("#theme-toggle").addEventListener("click", toggleTheme);
  $$(".theme-option[data-theme]").forEach((btn) => {
    btn.addEventListener("click", () => applyTheme(btn.dataset.theme));
  });

  // Niveau d'apprentissage (Paramètres)
  $$(".level-option").forEach((btn) => {
    btn.addEventListener("click", () => setLevel(btn.dataset.level));
  });

  // Paramètres
  $("#settings-btn").addEventListener("click", openSettingsPanel);
  $("#settings-close").addEventListener("click", closeAllModals);

  // Lexique Audio
  $("#dictionary-btn").addEventListener("click", () => openDictionaryPanel());
  $("#dictionary-close").addEventListener("click", closeAllModals);
  $("#dict-search").addEventListener("input", renderDictResults);

  // Favoris (proverbes, histoires, phrases, traductions)
  $("#favorites-btn").addEventListener("click", openFavoritesPanel);
  $("#favorites-close").addEventListener("click", closeAllModals);

  const favAddForm = $("#favorite-add-form");
  if (favAddForm) {
    favAddForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const snkInput = $("#fav-input-snk");
      const frInput = $("#fav-input-fr");
      const typeSelect = $("#fav-input-type");
      const snkVal = snkInput ? snkInput.value.trim() : "";
      const frVal = frInput ? frInput.value.trim() : "";
      const typeVal = typeSelect ? typeSelect.value : "traduction";
      if (!snkVal) {
        if (snkInput) snkInput.focus();
        return;
      }
      if (!isFavorite(snkVal, frVal)) {
        state.favorites.unshift({
          snk: snkVal,
          fr: frVal,
          type: typeVal,
          source: "Favoris personnels",
          createdAt: Date.now(),
        });
        saveFavorites();
      }
      if (snkInput) snkInput.value = "";
      if (frInput) frInput.value = "";
      if (!matchesFavoriteFilter({ type: typeVal }, state.favoriteFilter)) {
        state.favoriteFilter = "all";
        $$(".dict-filter[data-fav-filter]").forEach((b) => b.classList.toggle("active", b.dataset.favFilter === "all"));
      }
      syncFavoriteButtons();
      renderFavorites();
      updateFavoritesCount();
    });
  }

  $$(".dict-filter[data-fav-filter]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.favoriteFilter = btn.dataset.favFilter;
      $$(".dict-filter[data-fav-filter]").forEach((b) => b.classList.toggle("active", b === btn));
      renderFavorites();
    });
  });

  $$(".dict-filter[data-dir]").forEach((btn) => {
    btn.addEventListener("click", () => {
      dictDirection = btn.dataset.dir;
      $$(".dict-filter[data-dir]").forEach((b) => b.classList.toggle("active", b === btn));
      renderDictResults();
    });
  });

  // Recherche dans l'historique
  $("#search-conversations").addEventListener("input", renderConversationList);

  // Menu contextuel & suppression
  $$("#context-menu .context-item").forEach((item) => {
    item.addEventListener("click", () => handleContextAction(item.dataset.action));
  });
  $("#delete-cancel").addEventListener("click", () => {
    deleteTargetId = null;
    $("#delete-modal").classList.remove("visible");
  });
  $("#delete-confirm").addEventListener("click", confirmDelete);

  $("#clear-all-data").addEventListener("click", () => {
    if (confirm("Supprimer toutes les discussions ? Les favoris sont conservés.")) {
      state.conversations = [];
      state.activeConversationId = null;
      saveConversations();
      renderConversationList();
      renderMessages();
      updateTopbarTitle();
      $("#settings-modal").classList.remove("visible");
    }
  });

  // Délégation globale : Copier, Écouter toute la réponse, Écouter Soninké seul, Lecture audio mot/phrase
  document.addEventListener("click", async (e) => {
    const copyBtn = e.target.closest(".msg-action-btn[data-copy]");
    if (copyBtn) {
      const success = await copyToClipboard(copyBtn.dataset.copy);
      if (success) {
        copyBtn.classList.add("copied");
        const label = copyBtn.querySelector("span");
        const orig = label ? label.textContent : copyBtn.textContent;
        if (label) label.textContent = "Copié";
        else copyBtn.textContent = "Copié";
        setTimeout(() => {
          copyBtn.classList.remove("copied");
          if (label) label.textContent = orig;
          else copyBtn.textContent = orig;
        }, 1800);
      }
      return;
    }

    const explainBtn = e.target.closest("[data-explain-index]");
    if (explainBtn) {
      const conv = getConversation(state.activeConversationId);
      const msg = conv?.messages[Number(explainBtn.dataset.explainIndex)];
      if (msg) {
        const body = explainBtn.closest(".message-body");
        let panel = body.querySelector(".french-explanation");
        if (!panel) { panel = document.createElement("pre"); panel.className = "french-explanation"; body.append(panel); }
        panel.textContent = explainFrench(msg.content);
      }
      return;
    }
    const speakBtn = e.target.closest(".msg-action-btn[data-speak-index]");
    if (speakBtn) {
      if (speakBtn.classList.contains("speaking")) {
        stopSpeech();
        return;
      }
      const conv = getConversation(state.activeConversationId);
      const idx = parseInt(speakBtn.dataset.speakIndex, 10);
      if (conv && conv.messages[idx] && conv.messages[idx].role === "assistant") {
        $$(".msg-action-btn.speaking").forEach((b) => b.classList.remove("speaking"));
        speakBtn.classList.add("speaking");
        speakResponse(conv.messages[idx].content, { soninkeOnly: false });
      }
      return;
    }

    const speakSnkBtn = e.target.closest(".msg-action-btn[data-speak-soninke-index]");
    if (speakSnkBtn) {
      if (speakSnkBtn.classList.contains("speaking")) {
        stopSpeech();
        return;
      }
      const conv = getConversation(state.activeConversationId);
      const idx = parseInt(speakSnkBtn.dataset.speakSoninkeIndex, 10);
      if (conv && conv.messages[idx] && conv.messages[idx].role === "assistant") {
        $$(".msg-action-btn.speaking").forEach((b) => b.classList.remove("speaking"));
        speakSnkBtn.classList.add("speaking");
        speakResponse(conv.messages[idx].content, { soninkeOnly: true });
      }
      return;
    }

    const favToggle = e.target.closest(".fav-toggle[data-fav-snk]");
    if (favToggle) {
      toggleFavorite({
        snk: favToggle.dataset.favSnk,
        fr: favToggle.dataset.favFr,
        type: favToggle.dataset.favType,
      });
      return;
    }

    const favMsgBtn = e.target.closest("[data-fav-msg-index]");
    if (favMsgBtn) {
      const conv = getConversation(state.activeConversationId);
      const msgIdx = Number(favMsgBtn.dataset.favMsgIndex);
      const msg = conv && conv.messages[msgIdx];
      const prevUserMsg = conv && msgIdx > 0 ? conv.messages[msgIdx - 1] : null;
      const contextText = `${prevUserMsg?.content || ""} ${msg?.content || ""}`;
      const inferredCategory = /proverbe/i.test(contextText)
        ? "proverbe"
        : /histoire|récit|conte/i.test(contextText)
          ? "histoire"
          : null;
      if (msg) {
        const items = pairItemsOf(msg.content);
        const allSaved = items.length > 0 && items.every((item) => isFavorite(item.snk, item.fr));
        for (const item of items) {
          if (allSaved) {
            const key = favoriteKey(item.snk, item.fr);
            state.favorites = state.favorites.filter((f) => favoriteKey(f.snk, f.fr) !== key);
          } else if (!isFavorite(item.snk, item.fr)) {
            state.favorites.unshift({
              ...item,
              type: inferredCategory || item.type,
              source: "Réponse",
              createdAt: Date.now(),
            });
          }
        }
        saveFavorites();
        updateFavoritesCount();
        syncFavoriteButtons();
        renderFavorites();
      }
      return;
    }

    const favRemove = e.target.closest("[data-fav-remove]");
    if (favRemove) {
      const [snk, fr] = favRemove.dataset.favRemove.split("|");
      toggleFavorite({ snk, fr });
      return;
    }

    const audioBtn = e.target.closest(".audio-play-btn[data-audio-word]");
    if (audioBtn) {
      playWordAudio(audioBtn.dataset.audioWord, audioBtn);
    }
  });

  // Cartes de suggestions rapides (dans les panneaux du menu)
  $$(".suggestion-card").forEach((card) => {
    card.addEventListener("click", () => {
      const promptText = card.dataset.prompt;
      if (promptText) {
        closeAllModals();
        closeSidebar();
        submitMessage(promptText);
      }
    });
  });

  // Fermeture des modales
  $$(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) closeAllModals();
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeAllModals();
      $("#context-menu").classList.remove("visible");
      closeSidebar();
      if (state.listening) cancelListening();
    }
  });

  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
      if (localStorage.getItem(THEME_KEY) === "auto") applyTheme("auto");
    });
  }


}

// ── Initialisation ──
async function init() {
  initTheme();
  loadConversations();
  loadFavorites();
  loadGuard();

  try {
    const savedLevel = localStorage.getItem(LEVEL_KEY);
    state.level = LEVELS[savedLevel] ? savedLevel : "debutant";
  } catch { state.level = "debutant"; }
  setLevel(state.level, false);

  try { state.voiceReplies = localStorage.getItem(VOICE_PREF_KEY) !== "0"; } catch {}
  syncVoiceReplyUI();

  initEvents();
  updateSendButton();
  renderConversationList();
  renderMessages();
  renderFavorites();
  updateFavoritesCount();

  state.dataReady = loadAllData();
  await state.dataReady;

  // Le corpus est chargé : rafraîchir les statuts de validation affichés
  renderFavorites();
  renderMessages();
}

init();
