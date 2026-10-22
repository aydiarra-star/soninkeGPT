/* ============================================
   SONINKEGPT — Assistant Conversationnel & Vocal Soninké
   - Réponse automatique garantie à chaque question (100% corpus)
   - Touche Entrer & bouton Envoyer actifs à tout moment
   - Assistant vocal soninké (écoute, enregistrement & réponse vocale en soninké)
   - WAV du référent uniquement — aucun moteur vocal du navigateur
   - Interface Dorée Royale
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

const STORAGE_KEY = "soninkegpt_conversations";
const THEME_KEY = "soninkegpt_theme";
const VOICE_PREF_KEY = "soninkegpt_voice_replies";
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
  dataReady: null,
  shiftHeld: false,
};

// ── Expressions attestées du corpus soninké ──
const PHRASEBOOK = [
  { fr: "bonjour", snk: "Xa wouy Diom", alt: ["an wouydiom", "i ni ce", "olu ni ce", "an moxo", "qa moxo"], note: "Xa wouy Diom (salutation respectueuse / pluriel) · an wouydiom / i ni ce (singulier) · olu ni ce / qa moxo (pluriel)" },
  { fr: "salut", snk: "Xa wouy Diom", alt: ["an wouydiom", "i ni ce", "an moxo"], note: "salutation courante" },
  { fr: "bonsoir", snk: "lellaane", alt: ["Xa wouy Diom"], note: "salutation de l'après-midi / soir" },
  { fr: "bienvenue", snk: "bisimilla", alt: ["Xa wouy Diom"], note: "bonne arrivée, accueillir" },
  { fr: "merci", snk: "nawari", alt: ["ni barka", "nawaari"], note: "remerciement" },
  { fr: "au revoir", snk: "oyi waxati", alt: ["hali telle"], note: "salutation de départ" },
  { fr: "comment vas-tu", snk: "i kera di", alt: ["an moxo", "qa moxo"], note: "demander des nouvelles" },
  { fr: "comment allez-vous", snk: "qa moxo", alt: ["Xa wouy Diom", "i kera di"], note: "pluriel / politesse" },
  { fr: "ça va", snk: "toora nta", alt: ["toora su nta"], note: "tout va bien (aucun mal)" },
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
function findAudioInfo(word) {
  const key = normalizeWord(word);
  if (!key) return null;
  if (state.audioByWord.has(key)) return state.audioByWord.get(key);
  const ortho = normalizeSoninkeOrtho(word);
  if (ortho && state.audioByOrtho.has(ortho)) return state.audioByOrtho.get(ortho);
  return null;
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

  if (!segments.length) audioNotice(`Audio authentique indisponible pour « ${word} » : génération ou enregistrement nécessaire.`);
  if (btn && token === state.speechToken && activeAudioBtn === btn) {
    btn.classList.remove("playing");
    activeAudioBtn = null;
  }
  return playedAny;
}

function soninkeForms(markdownText) {
  const forms = [...String(markdownText).matchAll(/\{\{audio:([^}]+)\}\}|\*\*([^*]+)\*\*/g)]
    .map(m => (m[1] || m[2]).trim());
  return [...new Set(forms)].filter(form => findAudioInfo(form) ||
    PHRASEBOOK.some(p => [p.snk, ...p.alt].some(x => normalizeWord(x) === normalizeWord(form))) ||
    state.entries.some(e => normalizeWord(e.soninke) === normalizeWord(form)));
}

function buildSpeechSegments(text) {
  return soninkeForms(text).flatMap(buildSoninkePhraseSegments);
}

async function speakResponse(text) {
  stopSpeech();
  ensureAudioUnlocked();
  const token = state.speechToken;
  const forms = soninkeForms(text);
  let unavailable = 0;
  for (const form of forms) {
    const segments = buildSoninkePhraseSegments(form);
    if (!segments.length) unavailable++;
    for (const segment of segments) {
      if (token !== state.speechToken) return;
      if (!await playViaWebAudio(segment.url)) {
        audioNotice("Lecture bloquée ou indisponible : cliquez sur Écouter pour réessayer.");
        return;
      }
    }
  }
  if (unavailable || !forms.length) audioNotice("Certaines formes n’ont pas encore de WAV authentique. Aucun remplacement synthétique n’est utilisé.");
  if (token === state.speechToken) $$(".msg-action-btn.speaking").forEach(b => b.classList.remove("speaking"));
}

function explainFrench(text) {
  const forms = soninkeForms(text);
  return forms.map(form => {
    const key = normalizeWord(form);
    const phrases = PHRASEBOOK.filter(p => [p.snk, ...p.alt].some(x => normalizeWord(x) === key)).map(p => p.fr);
    const meanings = state.entries.filter(e => normalizeWord(e.soninke) === key).map(e => e.francais);
    return `${form} → ${[...new Set([...phrases, ...meanings])].join(" ; ") || "Sens non documenté — à vérifier avec le référent."}`;
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
    topLbl.textContent = active ? "Audio : ON" : "Réponse audio";
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
        ? "🔊 Réponse vocale activée : SoninkeGPT vous répondra en audio et en soninké."
        : "🔇 Réponse vocale automatique désactivée (les boutons 🔊 restent actifs).",
      3200
    );
    if (state.voiceReplies) {
      speakResponse("**Xa wouy Diom** ! Réponse vocale activée.");
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
    showVoiceStatus("🎤 Aucun son détecté — parlez près du micro ou écrivez votre question.", 3200);
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
  showVoiceStatus("🎤 J'écoute et j'enregistre… parlez en français ou en soninké !", 0, true);

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
          showVoiceStatus(`🎤 « ${state.lastTranscript} »`, 0, true);
        }
        if (event.results[event.results.length - 1].isFinal && state.lastTranscript) {
          finishVoiceSession();
        }
      };

      recognition.onerror = (e) => {
        // Si MediaRecorder enregistre déjà, on continue l'enregistrement vocal sans couper !
        if (state.recorder && state.recorder.state === "recording") {
          showVoiceStatus("🔴 Enregistrement vocal actif — appuyez sur « Envoyer » quand vous avez fini.", 0, true);
          return;
        }
        cleanupVoiceResources();
        if (e.error === "not-allowed") {
          showVoiceStatus("⚠️ Autorisez l'accès au microphone dans les réglages du navigateur.", 4200);
        } else {
          showVoiceStatus("🎤 Touchez à nouveau le micro et parlez clairement.", 3400);
        }
      };

      recognition.onend = () => {
        if (state.listening && state.lastTranscript) {
          finishVoiceSession();
        } else if (state.listening && !(state.recorder && state.recorder.state === "recording")) {
          cleanupVoiceResources();
          showVoiceStatus("🎤 Écoute terminée — touchez le micro pour reparler.", 2800);
        }
      };

      recognition.start();
      hasAnyCapture = true;
    } catch {}
  }

  if (!hasAnyCapture) {
    cleanupVoiceResources();
    showVoiceStatus("🔊 Réponse vocale activée ! Écrivez votre question : je vous réponds en audio soninké.", 4200);
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
  "suis": "être", "es": "être", "est": "être", "sommes": "être", "etes": "être", "sont": "être",
  "vais": "aller", "vas": "aller", "va": "aller", "allons": "aller", "allez": "aller", "vont": "aller",
  "pars": "partir", "part": "partir", "partons": "partir", "partez": "partir", "partent": "partir", "parti": "partir", "partie": "partir",
  "viens": "venir", "vient": "venir", "venons": "venir", "venez": "venir", "viennent": "venir", "venu": "venir", "venue": "venir",
  "bois": "boire", "boit": "boire", "buvons": "boire", "buvez": "boire", "boivent": "boire", "bu": "boire",
  "vois": "voir", "voit": "voir", "voyons": "voir", "voyez": "voir", "voient": "voir", "vu": "voir",
  "prends": "prendre", "prend": "prendre", "prenons": "prendre", "prenez": "prendre", "prennent": "prendre", "pris": "prendre",
  "dors": "dormir", "dort": "dormir", "dormons": "dormir", "dormez": "dormir", "dorment": "dormir", "dormi": "dormir",
  "ecris": "ecrire", "ecrit": "ecrire", "ecrivons": "ecrire", "ecrivez": "ecrire", "ecrivent": "ecrire",
  "yeux": "œil", "chevaux": "cheval", "enfants": "enfant", "femmes": "femme", "hommes": "homme",
  "maisons": "maison", "jours": "jour", "mots": "mot", "parents": "père", "mamans": "mère", "papas": "papa",
};

function candidateWordForms(rawTerm) {
  const n = normalizeWord(rawTerm);
  const forms = new Set([n]);
  if (FR_IRREGULAR_MAP[n]) forms.add(normalizeWord(FR_IRREGULAR_MAP[n]));
  if (n.length > 3 && n.endsWith("s")) forms.add(n.slice(0, -1));
  if (n.length > 3 && n.endsWith("x")) forms.add(n.slice(0, -1));
  if (n.length > 4 && n.endsWith("es")) { forms.add(n.slice(0, -2)); forms.add(n.slice(0, -2) + "er"); }
  if (n.length > 4 && n.endsWith("ent")) forms.add(n.slice(0, -3) + "er");
  if (n.length > 4 && n.endsWith("ons")) forms.add(n.slice(0, -3) + "er");
  if (n.length > 4 && n.endsWith("ez")) forms.add(n.slice(0, -2) + "er");
  if (n.length > 3 && n.endsWith("e")) forms.add(n.slice(0, -1) + "er");
  // Suffixes morphologiques soninké courants (-ke défini, -nu/-u pluriel, -nde/-ye/-ni)
  if (n.length > 4 && (n.endsWith("-nde") || n.endsWith("-ye"))) forms.add(n.replace(/-(nde|ye)$/, ""));
  if (n.length > 4 && n.endsWith("ni")) forms.add(n.slice(0, -2));
  if (n.length > 4 && n.endsWith("nu")) forms.add(n.slice(0, -2));
  return [...forms].filter(Boolean);
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
    const snk = normalizeWord(e.soninke);
    const snkOrtho = normalizeSoninkeOrtho(e.soninke);
    const frFull = normalizeWord(e.francais);
    const senses = splitSenses(e.francais);
    const variants = String(e.variantes || "").split(/[;,|]/).map(normalizeWord).filter(Boolean);

    if (snk === directKey || frFull === directKey || variants.includes(directKey)) {
      exactDirect.push(e);
      continue;
    }

    const isExact =
      forms.some((f) => snk === f || frFull === f || senses.includes(f) || variants.includes(f)) ||
      (ortho.length >= 2 && snkOrtho === ortho);

    if (isExact) {
      exactStemmed.push(e);
      continue;
    }

    const allTokens = [
      ...snk.split(/\s+/),
      ...frFull.split(/[\s,;()/]+/),
      ...variants.flatMap((v) => v.split(/\s+/)),
    ].filter(Boolean);

    if (forms.some((f) => f.length >= 2 && (snk.startsWith(f) || frFull.startsWith(f) || allTokens.includes(f)))) {
      starts.push(e);
    } else if (forms.some((f) => f.length >= 3 && (snk.includes(f) || frFull.includes(f) || normalizeWord(e.exemple_original || "").includes(f)))) {
      contains.push(e);
    }
  }

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
  const cat = e.categorie ? ` *(${e.categorie})*` : "";
  const statusNote = e.isCandidate ? ` · *[à vérifier]*` : "";
  const variants = e.variantes ? ` · *var. : ${e.variantes}*` : "";
  let line = `- **${e.soninke}** → ${e.francais}${cat}${variants}${statusNote} {{audio:${e.soninke}}}`;

  // Formes dérivées enregistrées dans audio/snk-*.wav
  const related = state.relatedAudioByStem.get(normalizeWord(e.soninke));
  if (related && related.length && !findAudioInfo(e.soninke)) {
    const sampleAudio = related[0];
    line += `\n  - *Forme audio enregistrée :* **${sampleAudio.text}** {{audio:${sampleAudio.text}}}`;
  }
  if (includeExample && e.exemple_original) {
    line += `\n  - *Exemple / note :* ${extractCleanExample(e.exemple_original)}`;
  }
  return line;
}

function formatPhrasebookBullet(p) {
  const alt = p.alt.length ? ` · *variantes :* ${p.alt.map((a) => `**${a}**`).join(", ")}` : "";
  const note = p.note ? ` *(${p.note})*` : "";
  return `- **${p.snk}** → ${p.fr}${alt}${note} {{audio:${p.snk}}}`;
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
  // 1. D'abord tester l'expression complète (ex. "bonjour", "au revoir", "comment vas-tu", "lemine ke", "Daga goli")
  if (targetPhrase) {
    const fullLookup = lookupTerm(targetPhrase);
    const fullPB = lookupPhrasebook(targetPhrase);
    if (fullLookup.exact.length || fullPB.length) {
      return formatRichTermResponse(targetPhrase, fullLookup, fullPB, direction);
    }
  }

  // 2. Si phrase de plusieurs mots : traduction mot-à-mot + reconstruction soninké + phrases du corpus !
  if (words.length >= 2) {
    const wordMappings = [];
    const soninkeAssembly = [];
    for (const w of words.slice(0, 8)) {
      const pb = lookupPhrasebook(w);
      const lk = lookupTerm(w);
      const bestEntry = lk.exact[0] || lk.starts[0];
      const bestPB = pb[0];
      if (bestPB) {
        wordMappings.push({ word: w, snk: bestPB.snk, fr: bestPB.fr, alt: bestPB.alt });
        soninkeAssembly.push(bestPB.snk);
      } else if (bestEntry) {
        const isFrQuery = normalizeWord(bestEntry.francais).includes(normalizeWord(w)) || splitSenses(bestEntry.francais).some((s) => candidateWordForms(w).includes(s));
        const mapped = isFrQuery ? bestEntry.soninke : bestEntry.francais;
        wordMappings.push({ word: w, snk: bestEntry.soninke, fr: bestEntry.francais, entry: bestEntry });
        soninkeAssembly.push(isFrQuery ? bestEntry.soninke : bestEntry.soninke);
      }
    }

    const matchingSamples = findMatchingSamples(words);

    if (wordMappings.length > 0 || matchingSamples.length > 0) {
      let out = "";
      if (soninkeAssembly.length > 0) {
        const joinedSnk = soninkeAssembly.join(" ");
        out += `🗣️ **En soninké :** **${joinedSnk}** {{audio:${joinedSnk}}}\n\n`;
      }
      if (wordMappings.length > 0) {
        out += `**Correspondances du lexique mot par mot :**\n`;
        for (const m of wordMappings) {
          if (m.entry) out += formatEntryBullet(m.entry, true) + "\n";
          else out += `- **${m.snk}** → ${m.fr}${m.alt && m.alt.length ? ` *(aussi : ${m.alt.join(", ")})*` : ""} {{audio:${m.snk}}}\n`;
        }
      }
      if (matchingSamples.length > 0) {
        out += `\n**Phrases attestées du corpus :**\n`;
        for (const s of matchingSamples.slice(0, 4)) {
          out += `- **${s.soninke}** → *« ${s.french} »* {{audio:${s.soninke}}}\n`;
        }
      }
      out += `\nTouchez **🔊** sur n'importe quel mot ou phrase pour écouter sa prononciation soninké !`;
      return out;
    }
  }

  // 3. Terme unique (ou premier mot clé pertinent)
  const mainTerm = targetPhrase || words[0] || "";
  const lk = lookupTerm(mainTerm);
  const pb = lookupPhrasebook(mainTerm);
  return formatRichTermResponse(mainTerm, lk, pb, direction);
}

function formatRichTermResponse(term, lk, pb, direction) {
  const { exact, starts, contains } = lk;
  const results = [...exact];
  const seen = new Set(results.map((e) => e.id));
  for (const e of [...starts, ...contains]) {
    if (!seen.has(e.id)) { results.push(e); seen.add(e.id); }
    if (results.length >= 10) break;
  }

  // Sélectionner la meilleure forme soninké principale pour répondre d'emblée en soninké
  const heroSnk = (pb[0] && pb[0].snk) || (exact[0] && exact[0].soninke) || (results[0] && results[0].soninke) || null;
  const heroFr = (pb[0] && pb[0].fr) || (exact[0] && exact[0].francais) || (results[0] && results[0].francais) || "";

  let response = "";
  if (heroSnk) {
    response += `🗣️ **${heroSnk}** → ${heroFr} {{audio:${heroSnk}}}\n\n`;
  }

  if (pb.length > 0) {
    response += `**Formes usuelles en soninké :**\n`;
    for (const p of pb.slice(0, 5)) response += formatPhrasebookBullet(p) + "\n";
    response += "\n";
  }

  if (results.length > 0) {
    response += `**Entrées du lexique (${results.length} trouvée${results.length > 1 ? "s" : ""}) :**\n`;
    for (const e of results.slice(0, 8)) {
      response += formatEntryBullet(e, results.length <= 4) + "\n";
    }
  }

  const samples = findMatchingSamples([term]);
  if (samples.length > 0) {
    response += `\n**Exemples de phrases du corpus :**\n`;
    for (const s of samples.slice(0, 3)) {
      response += `- **${s.soninke}** → *« ${s.french} »* {{audio:${s.soninke}}}\n`;
    }
  }

  if (heroSnk || results.length > 0) {
    response += `\nTouchez **🔊** pour écouter la prononciation soninké.`;
    return response;
  }

  // Recherche orthographique approchée (jamais de blocage « aucune correspondance » !)
  const similar = findSimilarEntries(term, 6);
  response = `🗣️ **Xa wouy Diom !** {{audio:Xa wouy Diom}}\n\n`;
  if (similar.length > 0) {
    response += `Voici les entrées les plus proches de **« ${term} »** dans le corpus soninké (**${state.entries.length} entrées** & **${state.audioByWord.size} audios**) :\n\n`;
    for (const e of similar) response += formatEntryBullet(e, true) + "\n";
  } else {
    response += `Pour votre demande sur **« ${term} »**, voici des expressions essentielles du corpus soninké (**${state.entries.length} entrées**, **${state.audioByWord.size} audios actifs**) :\n\n`;
    response += `- **Xa wouy Diom** → Bonjour ! (salutation) {{audio:Xa wouy Diom}}\n`;
    response += `- **an wouydiom** → Bonjour (à une personne) {{audio:an wouydiom}}\n`;
    response += `- **i kera di** → Comment vas-tu ? · **toora nta** → Ça va {{audio:toora nta}}\n`;
    response += `- **nawari** → Merci {{audio:nawari}}\n`;
    response += `- **aké n'séfé soninké** → Il a parlé soninké {{audio:aké n'séfé soninké}}\n`;
  }
  response += `\nPosez n'importe quel mot, expression ou thème (famille, visage, nombres, verbes, culture) — je vous réponds immédiatement en soninké et en audio !`;
  return response;
}

function generateResponse(message) {
  const trimmed = String(message || "").trim();
  const lower = trimmed.toLocaleLowerCase("fr");
  const ortho = normalizeSoninkeOrtho(trimmed);
  const direction = detectDirection(trimmed);

  // 1. Salutations directes (« Xa wouy Diom », « bonjour », « salut », « i ni ce », etc.)
  const isDirectGreeting =
    !/tradui|comment\s+dit|comment\s+dire|signifie|veut\s+dire/i.test(lower) &&
    (/^(bonjour|bonsoir|salut|hello|hi|hey|coucou|xa\s*wouy|wouy\s*diom|an\s*wouydiom|i\s*ni\s*ce|olu\s*ni\s*ce|bisimilla|a\s*jaara|a\s*jarra)\b/i.test(lower) ||
      /^(xawuydiom|wuy ?jom|anwuyjom)/.test(ortho)) &&
    trimmed.length < 48;

  if (isDirectGreeting) {
    return `**Xa wouy Diom !** 👋 {{audio:Xa wouy Diom}}\n\nBienvenue sur **SoninkeGPT** ! Voici les salutations en soninké :\n\n- **Xa wouy Diom** → Bonjour ! (salutation respectueuse / pluriel) {{audio:Xa wouy Diom}}\n- **an wouydiom** → Bonjour (à une personne) {{audio:an wouydiom}}\n- **i ni ce** → Bonjour (singulier) · **olu ni ce** → Bonjour (pluriel) {{audio:i ni ce}}\n- **an moxo** / **qa moxo** → Bonjour, comment ça va ? {{audio:an moxo}}\n- **bisimilla** → Bienvenue, bonne arrivée {{audio:bisimilla}}\n\nPosez-moi votre question à l'écrit (touche **Entrée**) ou en parlant avec le **micro 🎤** : je vous réponds automatiquement en soninké et en audio !`;
  }

  // 2. Comment ça va ?
  if (!/tradui|comment\s+dit/i.test(lower) && /^(comment (vas|allez)|ça va|ca va|njoxo na|i kera di|an moxo|qa moxo|toora)\b/i.test(lower) && trimmed.length < 48) {
    return `**Toora nta !** 😊 *(Ça va très bien !)* {{audio:toora nta}}\n\nDialogue courant en soninké :\n- **i kera di ?** → Comment vas-tu ? {{audio:i kera di}}\n- **qa moxo ?** → Comment allez-vous ? {{audio:qa moxo}}\n- **toora nta** / **toora su nta** → Ça va / Tout va bien {{audio:toora su nta}}\n\nEt vous, comment puis-je vous aider en soninké aujourd'hui ?`;
  }

  // 3. Remerciements directs
  if (!/tradui|comment\s+dit|comment\s+dire/i.test(lower) && /^(merci|thank|nawari|nawaari|ni barka|diakara)\b/i.test(lower) && trimmed.length < 36) {
    return `**Nawari !** 🙏 *(Merci !)* {{audio:nawari}}\n\nEn soninké, pour remercier :\n- **nawari** *(var. nawaari)* → merci {{audio:nawari}}\n- **ni barka** → merci {{audio:ni barka}}\n\nJe reste à votre écoute pour toute autre question en français ou en soninké !`;
  }

  // 4. Au revoir / départ
  if (!/tradui|comment\s+dit|comment\s+dire/i.test(lower) && /^(au revoir|adieu|bye|à bient[ôo]t|a bientot|bonne nuit|oyi waxati|hali telle)\b/i.test(lower) && trimmed.length < 40) {
    return `**Oyi waxati !** 👋 *(Au revoir !)* {{audio:oyi waxati}}\n\nPour prendre congé en soninké :\n- **oyi waxati** → au revoir {{audio:oyi waxati}}\n- **hali telle** → au revoir / à bientôt {{audio:hali telle}}\n\nÀ très vite sur SoninkeGPT !`;
  }

  // 5. Identité / Présentation
  if (/(qui es[- ]tu|qui [êe]tes[- ]vous|tu es qui|c'est quoi soninkegpt|pr[ée]sente[- ]toi|ton nom)/i.test(lower)) {
    return `**Xa wouy Diom !** {{audio:Xa wouy Diom}}\n\nJe suis **SoninkeGPT**, votre assistant conversationnel et vocal dédié à la langue **soninké**.\n\nJe m'appuie sur toutes les ressources vérifiées du projet :\n- **${state.entries.length} entrées lexicales** (mots, sens, variantes et exemples)\n- **${state.audioByWord.size} enregistrements audio WAV** authentiques validés par le référent\n- **Phrases parallèles soninké–français** et assistant vocal interactif\n\nÉcrivez ou cliquez sur **🎤** à côté de la touche Entrer : j'écoute, j'enregistre et je vous réponds en soninké !`;
  }

  // 6. Thème : Tête, visage & corps humain
  if (/(visage|corps humain|parties du corps|t[êe]te et visage)/i.test(lower)) {
    const hf = state.entries.filter((e) => /partie_du_corps|tete_visage/i.test((e.categorie || "") + " " + (e.source || "")));
    let res = `**Le visage et le corps en soninké** 🗣️\n\n`;
    for (const e of hf.slice(0, 16)) res += formatEntryBullet(e) + "\n";
    res += `\nTouchez **🔊** sur chaque terme pour l'écouter.`;
    return res;
  }

  // 7. Thème : Jours de la semaine
  if (/jours? de la semaine|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche/i.test(lower) && /jour|semaine/i.test(lower)) {
    const days = state.entries.filter((e) => /lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche/i.test(e.francais || ""));
    let res = `**Les jours en soninké** 📅\n\n`;
    for (const e of days) res += formatEntryBullet(e) + "\n";
    res += `- **lenki** → aujourd'hui {{audio:lenki}}\n- **daru** → hier {{audio:daru}}\n- **koota su** → chaque jour {{audio:koota su}}\n`;
    return res;
  }

  // 8. Thème : Nombres / chiffres
  if (/nombres?|num[ée]ros?|chiffres?|compter en sonink/i.test(lower)) {
    const nums = state.entries.filter((e) => /nombre|num[ée]ral/i.test(e.categorie || ""));
    let res = `**Compter en soninké** 🔢\n\n`;
    for (const e of nums.slice(0, 14)) res += formatEntryBullet(e) + "\n";
    res += `\nTouchez **🔊** pour écouter chaque nombre.`;
    return res;
  }

  // 9. Thème : Famille
  if (/famille|parent/i.test(lower) && !/tradui/i.test(lower)) {
    let res = `**La famille en soninké** 👨‍👩‍👧‍👦\n\n`;
    res += `- **haabe** / **baaba** / **faba** → père, papa {{audio:baaba}}\n`;
    res += `- **saaxe** → mère, maman {{audio:saaxe}}\n`;
    res += `- **lemine** → enfant {{audio:lemine}} · **lemine ke** → l'enfant {{audio:lemine ke}}\n`;
    res += `- **yaxare** → femme {{audio:yaxare}}\n`;
    res += `- **yugo** → homme {{audio:yugo}}\n`;
    res += `- **ka** → maison {{audio:ka}}\n`;
    return res;
  }

  // 10. Mots de base / Apprentissage / Parler en soninké
  if (/mot[s]? de base|vocabulaire de base|quelques mots|premiers mots|apprends-moi|apprendre le sonink|le[çc]on|enseigne|parle[- ]moi en sonink|phrase[s]? en sonink/i.test(lower)) {
    let response = `**Xa wouy Diom !** 📖 *Apprenons l'essentiel du soninké :* {{audio:Xa wouy Diom}}\n\n`;
    response += `**1. Salutations & politesse :**\n`;
    response += `- **Xa wouy Diom** → Bonjour ! {{audio:Xa wouy Diom}}\n`;
    response += `- **an wouydiom** / **i ni ce** → Bonjour (à une personne) {{audio:an wouydiom}}\n`;
    response += `- **i kera di ?** → Comment vas-tu ? · **toora nta** → Ça va {{audio:toora nta}}\n`;
    response += `- **nawari** → Merci {{audio:nawari}} · **oyi waxati** → Au revoir {{audio:oyi waxati}}\n\n`;
    response += `**2. Verbes & mots avec audios enregistrés du référent :**\n`;
    for (const w of ["daga", "ri", "sefe", "yige", "mini", "goli", "safa", "xanu", "maro", "lemine"]) {
      const match = state.entries.find((e) => normalizeWord(e.soninke) === w);
      if (match) response += formatEntryBullet(match) + "\n";
    }
    response += `\n**3. Phrases complètes du corpus :**\n`;
    for (const s of state.samples.slice(0, 4)) {
      response += `- **${s.soninke}** → *« ${s.french} »* {{audio:${s.soninke}}}\n`;
    }
    response += `\nTouchez **🔊** sur n'importe quelle ligne pour l'écouter immédiatement !`;
    return response;
  }

  // 11. Culture soninké
  if (/culture|histoire|peuple sonink|empire du ghana|ghana|wagadu|tradition orale|griot|geseru|c[ée]r[ée]monie|castes traditionnelles/i.test(lower)) {
    return `**La culture et l'histoire soninké (Wagadu)** ✺\n\n- **Xa wouy Diom** → Salutation de paix et de respect {{audio:Xa wouy Diom}}\n- **bisimilla** →Hospitalité et accueil (*bienvenue, bonne arrivée*) {{audio:bisimilla}}\n\n**Points essentiels :**\n- Le peuple **soninké** (aussi appelé Sarakolé, Marka ou Wakore) est le fondateur historique de l'**Empire du Wagadu (Ghana)**, l'un des plus grands empires d'Afrique de l'Ouest.\n- Le **soninké** appartient à la famille des langues **mandé** et est parlé au **Mali, Mauritanie, Sénégal, Gambie, Guinée-Bissau, Côte d'Ivoire** ainsi que dans une vaste diaspora internationale (notamment en France).\n- La **tradition orale** (portée notamment par les *geseru*, griots et généalogistes) transmet l'histoire, les patronymes (*janmu* comme Bacili, Cissé, Diagana, Diarra, Sylla, Touré, Wagué…) et les valeurs de solidarité communautaire.\n\nLe corpus actuel de SoninkeGPT réunit **${state.entries.length} entrées** et **${state.audioByWord.size} enregistrements audio** pour préserver et transmettre ce patrimoine vivant !`;
  }

  // 12. Prononciation / Audios intégrés
  if (/prononciation|audios?|écouter|entendre|enregistrement|voix/i.test(lower) && !/tradui|comment\s+dit|signifie/i.test(lower)) {
    return `**Audios intégrés & Réponse vocale SoninkeGPT** 🔊\n\nLes **${state.audioByWord.size} enregistrements WAV** du référent sont **100 % actifs** :\n- **Daga goli** {{audio:Daga goli}} · **Daga iige** {{audio:Daga iige}} · **Li taxu** {{audio:Li taxu}}\n- **Mpai reni** {{audio:Mpai reni}} · **Mpai telle** {{audio:Mpai telle}}\n- **lemine ke** *(l'enfant)* {{audio:lemine ke}} · **maro ke** *(le riz)* {{audio:maro ke}} · **koota su** *(chaque jour)* {{audio:koota su}}\n\n**3 façons d'utiliser le mode vocal :**\n- Touchez **🔊 Réponse audio** (en haut à droite ou à côté de la zone de texte) pour que SoninkeGPT vous réponde automatiquement en voix audio.\n- Touchez **🎤** (à côté de la touche Entrer) pour enregistrer votre voix et recevoir une réponse parlée en soninké.\n- Ouvrez **📚 Lexique & Audios → filtre « 🔊 Audios »** pour parcourir les ${state.audioByWord.size} enregistrements.`;
  }

  // 13. Aide
  if (/^(aide|help|que peux-tu|que pouvez-vous|capacit[ée]s|fonctionnalit[ée]s|comment [cç]a marche)/i.test(lower)) {
    return `**Xa wouy Diom ! Voici tout ce que je fais pour vous :** {{audio:Xa wouy Diom}}\n\n- **Traduction instantanée français ↔ soninké** de mots et de phrases (*« Traduis bonjour en soninké »*, *« Comment dit-on merci en soninké ? »*, *« La femme mange le riz »*)\n- **Assistant vocal soninké (🎤 à côté d'Entrer)** : j'écoute votre voix, je l'enregistre et je vous réponds en soninké\n- **Audios intégrés actifs (${state.audioByWord.size} WAV)** : cliquez sur n'importe quel bouton **🔊**\n- **Réponse audio vocale automatique** : activez **🔊 Réponse audio** en un clic\n- **Touche Entrée active à tout moment** sur mobile et ordinateur.`;
  }

  // 14. Recherche lexicale & traduction (mots simples, expressions, phrases complètes, fautes de frappe)
  const { targetPhrase, words } = extractTargetPhraseAndWords(trimmed);
  return buildSingleOrPhraseAnswer(targetPhrase, words, direction);
}

// ── Rendu Markdown + Boutons Audio Intégrés Actifs ──
function renderMarkdown(text) {
  let html = esc(text);

  // Marqueurs {{audio:MOT}} → boutons audio interactifs distinguant WAV référent vs synthèse phonétique
  html = html.replace(/\{\{audio:([^}]+)\}\}/g, (_, rawWord) => {
    const word = rawWord.trim();
    const hasRealWav = !!findAudioInfo(word);
    const cls = "audio-play-btn";
    const title = hasRealWav
      ? `Écouter l'audio intégré du référent : ${word}`
      : `WAV ou assemblage de mots attestés, sinon indisponible : ${word}`;
    return `<button type="button" class="${cls}" data-audio-word="${word}" title="${title}" aria-label="Écouter ${word}">🔊 ${word}</button>`;
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
      if (block.startsWith("<ul>") || block.startsWith("<ol>") || block.startsWith("<pre>") || block === "<hr>") {
        return block;
      }
      return `<p>${block.replace(/\n/g, "<br>")}</p>`;
    })
    .join("\n");

  return html;
}

// ── Rendu de la conversation (avec actions audio toujours visibles sur mobile & desktop) ──
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
      const cleanCopy = esc(String(msg.content || "").replace(/\{\{audio:[^}]+\}\}/g, "").trim());
      html += `<div class="message message-assistant">
        <div class="message-avatar">S</div>
        <div class="message-body">
          <div class="message-text">${renderMarkdown(msg.content)}</div>
          <div class="message-actions">
            <button type="button" class="msg-action-btn" data-speak-index="${idx}" title="Écouter toute la réponse en audio vocal" aria-label="Écouter la réponse en audio">
              🔊 Écouter
            </button>
            <button type="button" class="msg-action-btn" data-speak-soninke-index="${idx}" title="Écouter uniquement les mots et phrases en soninké" aria-label="Écouter en soninké">
              🗣️ Soninké
            </button>
            <button type="button" class="msg-action-btn" data-explain-index="${idx}">🇫🇷 Comprendre en français</button>
            <button type="button" class="msg-action-btn" data-copy="${cleanCopy}" title="Copier la réponse" aria-label="Copier la réponse">
              📋 Copier
            </button>
          </div>
        </div>
      </div>`;
    }
  });

  messagesArea.innerHTML = html;
  scrollToBottom();
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
    const conv = createConversation("🎤 Message vocal soninké");
    state.activeConversationId = conv.id;
    updateTopbarTitle();
  }
  const conv = getConversation(state.activeConversationId);
  if (!conv) return;

  conv.messages.push({
    role: "user",
    content: "🎤 Message vocal enregistré",
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
    `**Xa wouy Diom !** 🎤 {{audio:Xa wouy Diom}}\n\n` +
    `J'ai bien **écouté et enregistré** votre message vocal (réécoutable juste au-dessus) et je vous réponds en **soninké** :\n\n` +
    `- **Xa wouy Diom ! Toora nta !** → *Bonjour ! Tout va bien !* {{audio:toora nta}}\n` +
    `- **aké n'séfé soninké** → *Il a parlé soninké* {{audio:aké n'séfé soninké}}\n` +
    `- **Daga goli** {{audio:Daga goli}} · **Li taxu** {{audio:Li taxu}}\n` +
    `- **nawari** → *Merci* {{audio:nawari}} · **oyi waxati** → *Au revoir* {{audio:oyi waxati}}\n\n` +
    `Écrivez aussi n'importe quel mot ci-dessous et appuyez sur **Entrée** : la réponse vocale est immédiate !`;

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
    list.innerHTML = `<div style="padding: 20px 12px; text-align: center; color: var(--text-sidebar-muted); font-size: 12px;">
      ${searchQuery ? "Aucune conversation trouvée" : "Aucune conversation"}
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

// ── Lexique & Explorateur des 576 Audios Intégrés ──
let dictDirection = "all";

function openDictionaryPanel(initialDir = null) {
  if (initialDir) {
    dictDirection = initialDir;
    $$(".dict-filter").forEach((b) => b.classList.toggle("active", b.dataset.dir === dictDirection));
  }
  $("#dictionary-modal").classList.add("visible");
  renderDictResults();
  $("#dict-search").focus();
}

function renderDictResults() {
  const query = normalizeWord($("#dict-search").value);
  const container = $("#dict-results");

  // Onglet dédié aux 576 enregistrements WAV intégrés !
  if (dictDirection === "audio") {
    const matchingAudios = state.audioList
      .filter((item) => {
        if (!query) return true;
        return normalizeWord(item.text).includes(query) || normalizeWord(item.francais || "").includes(query) || item.id.includes(query);
      })
      .slice(0, MAX_DISPLAY);

    if (!matchingAudios.length) {
      container.innerHTML = `<div class="dict-empty">Aucun enregistrement correspondant</div>`;
      return;
    }

    container.innerHTML = matchingAudios
      .map(
        (a) => `<div class="dict-card">
          <div class="dict-card-head">
            <h4>${esc(a.text)}</h4>
            <button type="button" class="audio-play-btn" data-audio-word="${esc(a.text)}" title="Écouter ${esc(a.id)}.wav" aria-label="Écouter ${esc(a.text)}">🔊 Écouter</button>
          </div>
          <div class="dict-translation">${a.francais ? esc(a.francais) : "Enregistrement soninké validé"}</div>
          <div class="dict-meta">🎙️ ${esc(a.id)}.wav · Voix du référent</div>
        </div>`
      )
      .join("");
    return;
  }

  const results = state.entries
    .filter((entry) => {
      const snk = normalizeWord(entry.soninke);
      const fr = normalizeWord(entry.francais);
      const variants = normalizeWord(entry.variantes || "");
      if (dictDirection === "snk") return !query || snk.includes(query) || variants.includes(query);
      if (dictDirection === "fr") return !query || fr.includes(query);
      return !query || snk.includes(query) || fr.includes(query) || variants.includes(query);
    })
    .slice(0, MAX_DISPLAY);

  if (!results.length) {
    container.innerHTML = `<div class="dict-empty">Aucun résultat</div>`;
    return;
  }

  container.innerHTML = results
    .map((e) => {
      const hasWav = !!findAudioInfo(e.soninke);
      const btnCls = hasWav ? "audio-play-btn" : "audio-play-btn audio-tts-btn";
      const label = hasWav ? "🔊 Audio" : "🔈 Voix";
      return `<div class="dict-card">
        <div class="dict-card-head">
          <h4>${esc(e.soninke)}</h4>
          <button type="button" class="${btnCls}" data-audio-word="${esc(e.soninke)}" title="Écouter ${esc(e.soninke)}" aria-label="Écouter ${esc(e.soninke)}">${label}</button>
        </div>
        <div class="dict-translation">${esc(e.francais)}</div>
        <div class="dict-meta">${e.categorie ? esc(e.categorie) : ""}${hasWav ? " · 🎙️ WAV référent" : ""}${e.isCandidate ? " · à vérifier" : ""}</div>
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
        const stem = key.replace(/-(nde|ye|ŋe)$/, "").split(/\\s+/)[0];
        if (stem && stem !== key) {
          if (!state.relatedAudioByStem.has(stem)) state.relatedAudioByStem.set(stem, []);
          state.relatedAudioByStem.get(stem).push(info);
        }
      }
    }
  } catch { /* Le corpus original reste disponible hors ligne. */ }
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
    if (audioCount) status += ` · ${audioCount} audios`;
    statusEl.textContent = status;
  }
  const audioFilterBtn = document.querySelector('.dict-filter[data-dir="audio"]');
  if (audioFilterBtn && audioCount) {
    audioFilterBtn.textContent = `🔊 Audios (${audioCount})`;
  }
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

  // 7. Assistant Vocal Soninké (à côté de la touche Entrer + écran d'accueil + barre latérale)
  const triggerVoiceAssistant = () => {
    closeSidebar();
    if (state.listening) finishVoiceSession();
    else startListening();
  };

  $("#mic-btn").addEventListener("click", triggerVoiceAssistant);
  const welcomeMic = $("#welcome-mic-btn");
  if (welcomeMic) welcomeMic.addEventListener("click", triggerVoiceAssistant);
  const sidebarVoice = $("#sidebar-voice-btn");
  if (sidebarVoice) sidebarVoice.addEventListener("click", triggerVoiceAssistant);

  const voiceFinishBtn = $("#voice-finish-btn");
  if (voiceFinishBtn) voiceFinishBtn.addEventListener("click", finishVoiceSession);
  const voiceCancelBtn = $("#voice-cancel-btn");
  if (voiceCancelBtn) voiceCancelBtn.addEventListener("click", cancelListening);

  // Salutation vocale d'accueil « Xa wouy Diom ! »
  const welcomeGreetBtn = $("#welcome-greet-audio-btn");
  if (welcomeGreetBtn) {
    welcomeGreetBtn.addEventListener("click", () => {
      speakResponse("**Xa wouy Diom** ! Bienvenue dans SoninkeGPT.");
    });
  }

  // 8. Boutons d'activation de la réponse audio vocale automatique
  $("#voice-reply-btn").addEventListener("click", () => setVoiceReplies(!state.voiceReplies));
  const topbarVoiceBtn = $("#topbar-voice-btn");
  if (topbarVoiceBtn) topbarVoiceBtn.addEventListener("click", () => setVoiceReplies(!state.voiceReplies));
  const voiceSwitch = $("#voice-replies-switch");
  if (voiceSwitch) voiceSwitch.addEventListener("click", () => setVoiceReplies(!state.voiceReplies));

  // New chat buttons
  $("#new-chat-btn").addEventListener("click", startNewChat);
  $("#new-chat-btn-top").addEventListener("click", startNewChat);

  // Menu mobile
  $("#menu-btn").addEventListener("click", openSidebar);
  $("#sidebar-close").addEventListener("click", closeSidebar);
  $("#sidebar-overlay").addEventListener("click", closeSidebar);

  // Thème
  $("#theme-toggle").addEventListener("click", toggleTheme);
  $$(".theme-option").forEach((btn) => {
    btn.addEventListener("click", () => applyTheme(btn.dataset.theme));
  });

  // Paramètres
  $("#settings-btn").addEventListener("click", () => {
    closeSidebar();
    $("#settings-modal").classList.add("visible");
  });
  $("#settings-close").addEventListener("click", () => $("#settings-modal").classList.remove("visible"));

  // Lexique & Audios
  $("#dictionary-btn").addEventListener("click", () => {
    closeSidebar();
    openDictionaryPanel();
  });
  $("#dictionary-close").addEventListener("click", () => $("#dictionary-modal").classList.remove("visible"));
  $("#dict-search").addEventListener("input", renderDictResults);

  $$(".dict-filter").forEach((btn) => {
    btn.addEventListener("click", () => {
      dictDirection = btn.dataset.dir;
      $$(".dict-filter").forEach((b) => b.classList.toggle("active", b === btn));
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
    if (confirm("Supprimer toutes les conversations ? Cette action est irréversible.")) {
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
        const orig = copyBtn.textContent;
        copyBtn.textContent = "✅ Copié";
        setTimeout(() => {
          copyBtn.classList.remove("copied");
          copyBtn.textContent = orig;
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

    const audioBtn = e.target.closest(".audio-play-btn[data-audio-word]");
    if (audioBtn) {
      playWordAudio(audioBtn.dataset.audioWord, audioBtn);
    }
  });

  // Cartes de suggestions de l'accueil
  $$(".suggestion-card").forEach((card) => {
    card.addEventListener("click", () => {
      const promptText = card.dataset.prompt;
      if (promptText) submitMessage(promptText);
    });
  });

  // Fermeture des modales
  $$(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) overlay.classList.remove("visible");
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      $$(".modal-overlay.visible").forEach((m) => m.classList.remove("visible"));
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

  try { state.voiceReplies = localStorage.getItem(VOICE_PREF_KEY) !== "0"; } catch {}
  syncVoiceReplyUI();

  initEvents();
  updateSendButton();
  renderConversationList();
  renderMessages();

  state.dataReady = loadAllData();
  await state.dataReady;
}

init();
