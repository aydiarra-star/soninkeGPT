/* ============================================
   SONINKEGPT — Conversational Interface
   ============================================ */

// ── Constants ──
const DATA_URL = "data/source/lexique-soninke-fr-base.csv";
const MANIFEST_URL = "data/source/manifest-577-review.csv";
const AUDIO_AUDIT_URL = "reports/audio-transfer-audit.csv";
const STORAGE_KEY = "soninkegpt_conversations";
const THEME_KEY = "soninkegpt_theme";
const MAX_DISPLAY = 80;

// ── State ──
const state = {
  entries: [],
  audioByWord: new Map(),
  conversations: [],
  activeConversationId: null,
  direction: "all",
  isGenerating: false,
};

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
  return String(value || "").normalize("NFC").trim().toLocaleLowerCase("fr");
}

function parseCSV(text, delimiter = ";") {
  const rows = text.replace(/^\uFEFF/, "").split(/\r?\n/).filter(Boolean);
  if (!rows.length) return [];
  const parseLine = (line) => {
    const cells = []; let cell = "", quoted = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (ch === '"') {
        if (quoted && line[i + 1] === '"') { cell += '"'; i++; }
        else quoted = !quoted;
      } else if (ch === delimiter && !quoted) { cells.push(cell); cell = ""; }
      else cell += ch;
    }
    cells.push(cell);
    return cells;
  };
  const headers = parseLine(rows[0]).map(h => h.trim());
  return rows.slice(1).map(line => {
    const values = parseLine(line);
    return Object.fromEntries(headers.map((h, i) => [h, values[i] || ""]));
  });
}

// ── Local Storage ──
function loadConversations() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    state.conversations = data ? JSON.parse(data) : [];
  } catch { state.conversations = []; }
}

function saveConversations() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state.conversations));
  } catch {}
}

function getConversation(id) {
  return state.conversations.find(c => c.id === id);
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
  state.conversations = state.conversations.filter(c => c.id !== id);
  saveConversations();
}

// ── Theme ──
function initTheme() {
  const saved = localStorage.getItem(THEME_KEY) || "light";
  applyTheme(saved);
}

function applyTheme(theme) {
  if (theme === "auto") {
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    document.documentElement.setAttribute("data-theme", prefersDark ? "dark" : "light");
  } else {
    document.documentElement.setAttribute("data-theme", theme);
  }
  localStorage.setItem(THEME_KEY, theme);
  updateThemeButtons(theme);
}

function updateThemeButtons(theme) {
  $$(".theme-option").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.theme === theme);
  });
}

function toggleTheme() {
  const current = localStorage.getItem(THEME_KEY) || "light";
  const next = current === "light" ? "dark" : "light";
  applyTheme(next);
}

// ── Dictionary Response Engine ──
function findDictionaryMatches(query) {
  const normalized = normalizeWord(query);
  if (!normalized) return [];

  // Exact match
  const exact = state.entries.filter(e =>
    normalizeWord(e.soninke) === normalized ||
    normalizeWord(e.francais) === normalized
  );
  if (exact.length) return exact.slice(0, 10);

  // Starts with
  const startsWith = state.entries.filter(e =>
    normalizeWord(e.soninke).startsWith(normalized) ||
    normalizeWord(e.francais).startsWith(normalized)
  );
  if (startsWith.length) return startsWith.slice(0, 10);

  // Contains
  const contains = state.entries.filter(e =>
    normalizeWord(e.soninke).includes(normalized) ||
    normalizeWord(e.francais).includes(normalized)
  );
  return contains.slice(0, 10);
}

function extractSearchTerms(message) {
  // Prioritize explicit translation questions so the whole phrase is not
  // mistaken for a dictionary term (e.g. "Comment dit-on « merci » en soninké ?").
  const translationPatterns = [
    /comment\\s+dit(?:-on)?\\s+[«"“]?(.+?)[»"”]?\\s+en\\s+sonink[ée]\\s*[?!.]*$/i,
    /(?:traduis|traduire|traduit|traduction de)\\s+[«"“]?(.+?)[»"”]?\\s+en\\s+sonink[ée]\\s*[?!.]*$/i,
    /(?:comment\\s+dit-on|comment\\s+dire)\\s+[«"“]?(.+?)[»"”]?\\s*[?!.]*$/i,
  ];
  for (const pattern of translationPatterns) {
    const match = message.match(pattern);
    if (match && match[1]) {
      const term = match[1].replace(/[»"”?.!]+$/, "").trim();
      if (term) return [term];
    }
  }

  // Try to extract meaningful words from the message
  const lower = message.toLowerCase();

  // Common question patterns
  const patterns = [
    /(?:tradui[sst]?|dis|comment dit-?on|en sonink[ée])\s*[«""]?(.+?)[»""]?\s*$/i,
    /(?:que signifie|veut dire|signification de)\s*[«""]?(.+?)[»""]?\s*$/i,
    /(?:cherche|recherche|trouve)\s*[«""]?(.+?)[»""]?\s*$/i,
    /(?:mot|terme|expression)\s*[«""]?(.+?)[»""]?\s*$/i,
  ];

  for (const pattern of patterns) {
    const match = message.match(pattern);
    if (match && match[1]) {
      const term = match[1].replace(/[?.!]+$/, "").trim();
      if (term && term.length > 1) return [term];
    }
  }

  // Extract quoted terms
  const quoted = message.match(/[«""](.+?)[»""]/g);
  if (quoted) return quoted.map(q => q.replace(/[«»""]/g, "").trim());

  // Extract individual words (2+ chars, skip common words)
  const stopWords = new Set(["le","la","les","un","une","des","de","du","en","au","aux","et","ou","est","sont","a","à","pour","dans","sur","avec","son","sa","ses","ce","cette","mon","ton","notre","votre","je","tu","il","elle","nous","vous","ils","elles","me","te","se","que","qui","quoi","comment","bonjour","merci","aide","peux","veux","sais","dire","traduire","apprendre","expliquer","mot","phrase","veut","signifie","traduis","dis","fait","donne","cherche","trouve","soninké","soninke","français","française"]);

  const words = lower
    .replace(/[?.!,;:()\-/]/g, " ")
    .split(/\s+/)
    .filter(w => w.length > 1 && !stopWords.has(w));

  return [...new Set(words)];
}

function generateResponse(message) {
  const lower = message.toLowerCase().trim();

  // Greetings
  if (/^(bonjour|hello|hi|salut|hey|a jaara|coucou)/i.test(lower)) {
    return `A jaara ! 👋\n\nBienvenue dans SoninkeGPT. Je suis votre assistant pour la langue soninké.\n\nJe peux vous aider à :\n- **Traduire** des mots entre le soninké et le français\n- **Apprendre** le vocabulaire de base\n- **Explorer** la culture soninké\n- **Rechercher** des mots dans le lexique de référence\n\nComment puis-je vous aider aujourd'hui ?`;
  }

  // Thanks
  if (/^(merci|thank|diakara|a jaara)/i.test(lower) && lower.length < 30) {
    return `I ma siyaaxanbare ! 🙏\n\nC'est un plaisir de vous aider. N'hésitez pas si vous avez d'autres questions sur la langue soninké.`;
  }

  // How are you
  if (/^(comment (vas|allez)|ça va|njoxo na)/i.test(lower) && lower.length < 40) {
    return `A si ngiine ! (Tout va bien !)\n\nJe suis là pour vous aider avec la langue soninké. Que souhaitez-vous savoir ?`;
  }

  // Basic words
  if (/mot[s]? de base|vocabulaire de base|quelques mots|premiers mots/i.test(lower)) {
    const basics = state.entries.slice(0, 15);
    let response = `Voici quelques mots essentiels en soninké :\n\n`;
    for (const entry of basics) {
      const audio = state.audioByWord.get(normalizeWord(entry.soninke));
      const audioTag = audio ? " 🔊" : "";
      response += `- **${entry.soninke}** → ${entry.francais}${audioTag}\n`;
    }
    response += `\nVous pouvez cliquer sur une suggestion ci-dessous pour explorer davantage, ou me demander la traduction d'un mot spécifique.`;
    return response;
  }

  // Culture: keep this intent specific. Matching every occurrence of "soninké"
  // used to intercept translation questions before the dictionary search.
  if (/culture|histoire|peuple sonink|empire du ghana|ghana|wagadu|tradition orale|griot|geseru|cérémonie|castes traditionnelles/i.test(lower)) {
    return `**La culture soninké** ✺\n\nLe peuple soninké (aussi appelé Sarakolé, Marka ou Wakore) possède une riche histoire et une langue fascinante.\n\n**Points clés :**\n- Les Soninké sont historiquement liés à l'Empire du Ghana (Wagadu)\n- Leur langue fait partie de la famille mandé\n- La tradition orale est centrale dans la transmission du savoir\n- Le soninké est parlé au Mali, Sénégal, Mauritanie, Gambie et dans la diaspora\n\n**Traditions importantes :**\n- Le système de castes traditionnels\n- Les griots (geseru) et la transmission orale\n- Les cérémonies (mariages, baptêmes, etc.)\n\nCe lexique contient **${state.entries.length} entrées** collectées auprès de référents linguistiques. N'hésitez pas à me demander la traduction de mots spécifiques !`;
  }

  // Help / what can you do
  if (/aide|help|que peux-tu|que pouvez-vous|capacit[ée]s|fonctionnalit[ée]s/i.test(lower)) {
    return `**Voici ce que je peux faire :**\n\n🔤 **Traduction**\n- Demandez la traduction d'un mot en soninké ou en français\n- Ex : « Comment dit-on *partir* en soninké ? »\n\n📖 **Lexique**\n- Recherchez des mots dans le dictionnaire de référence\n- Découvrez les catégories et statuts de validation\n\n🔊 **Prononciation**\n- Certains mots disposent d'enregistrements audio de référence\n\n✺ **Culture**\n- Apprenez sur la culture soninké et son histoire\n\n💡 **Suggestions :**\n- « Traduis *bonjour* en soninké »\n- « Apprends-moi quelques mots de base »\n- « Explique-moi la culture soninké »`;
  }

  // Pronunciation / audio
  if (/prononciation|audio|écouter|entendre|dire.*audio/i.test(lower)) {
    const audioCount = state.audioByWord.size;
    return `**Prononciation audio** 🔊\n\nLe corpus contient **${audioCount} enregistrements** de référence reliés aux mots du lexique.\n\nLes enregistrements sont validés par audit et correspondent uniquement aux mots dont la correspondance est confirmée.\n\nPour écouter un mot :\n1. Ouvrez le **Lexique** depuis la barre latérale\n2. Ou demandez-moi un mot spécifique — s'il dispose d'un audio, je vous l'indiquerai\n\nLes validations linguistiques sont distinctes des contrôles techniques.`;
  }

  // Dictionary search
  const terms = extractSearchTerms(message);
  let allResults = [];

  // Search with extracted terms
  for (const term of terms) {
    const matches = findDictionaryMatches(term);
    allResults.push(...matches);
  }

  // Deduplicate
  const seen = new Set();
  allResults = allResults.filter(e => {
    const key = e.id || `${e.soninke}-${e.francais}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });

  if (allResults.length > 0) {
    let response = "";
    if (allResults.length === 1) {
      const e = allResults[0];
      const audio = state.audioByWord.get(normalizeWord(e.soninke));
      response = `**${e.soninke}** → ${e.francais}`;
      if (e.categorie) response += `\n\n*Catégorie :* ${e.categorie}`;
      if (e.statut) response += `\n*Statut :* ${e.statut.replace(/_/g, " ")}`;
      if (e.source) response += `\n*Source :* ${e.source}`;
      if (audio) response += `\n\n🔊 Un enregistrement audio de référence est disponible pour ce mot.`;
      response += `\n\n*Identifiant : ${e.id}*`;
    } else {
      response = `J'ai trouvé **${allResults.length} résultat${allResults.length > 1 ? "s" : ""}** :\n\n`;
      for (const e of allResults.slice(0, 12)) {
        const audio = state.audioByWord.get(normalizeWord(e.soninke));
        const audioTag = audio ? " 🔊" : "";
        const category = e.categorie ? ` *(${e.categorie})*` : "";
        response += `- **${e.soninke}** → ${e.francais}${category}${audioTag}\n`;
      }
      if (allResults.length > 12) {
        response += `\n*Et ${allResults.length - 12} autre${allResults.length - 12 > 1 ? "s" : ""} résultat${allResults.length - 12 > 1 ? "s" : ""}… Ouvrez le Lexique complet pour tout voir.*`;
      }
    }
    return response;
  }

  // No match — provide helpful response
  if (terms.length > 0) {
    return `Je n'ai pas trouvé de correspondance exacte pour « **${terms.join("**, **")}** » dans le lexique actuel.\n\nLe dictionnaire contient **${state.entries.length} entrées**. Quelques suggestions :\n\n- Vérifiez l'orthographe du mot\n- Essayez un synonyme\n- Ouvrez le **Lexique** complet depuis la barre latérale pour parcourir toutes les entrées\n- Demandez-moi un mot en français ou en soninké\n\nN'hésitez pas à reformuler votre question !`;
  }

  // Generic fallback
  return `Je suis SoninkeGPT, votre assistant pour la langue soninké.\n\nJe peux vous aider avec :\n- La **traduction** de mots (soninké ↔ français)\n- L'**apprentissage** du vocabulaire\n- La **culture** soninké\n- La **recherche** dans le lexique de référence\n\nEssayez par exemple :\n- « Traduis *bonjour* en soninké »\n- « Apprends-moi quelques mots de base »\n- « Explique-moi la culture soninké »`;
}

// ── Markdown-like rendering ──
function renderMarkdown(text) {
  let html = esc(text);

  // Code blocks
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
    return `<pre><code class="language-${lang}">${code.trim()}</code></pre>`;
  });

  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Bold
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

  // Italic
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

  // Lists
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, (match) => `<ul>${match}</ul>`);

  // Paragraphs (split by double newlines)
  html = html.split(/\n\n+/).map(block => {
    block = block.trim();
    if (!block) return '';
    if (block.startsWith('<ul>') || block.startsWith('<ol>') || block.startsWith('<pre>')) return block;
    return `<p>${block.replace(/\n/g, '<br>')}</p>`;
  }).join('\n');

  return html;
}

// ── Render Messages ──
function renderMessages() {
  const conv = getConversation(state.activeConversationId);
  const messagesArea = $("#messages-area");
  const welcomeScreen = $("#welcome-screen");

  if (!conv || conv.messages.length === 0) {
    messagesArea.classList.remove("has-messages");
    welcomeScreen.style.display = "flex";
    return;
  }

  welcomeScreen.style.display = "none";
  messagesArea.classList.add("has-messages");

  let html = "";
  for (const msg of conv.messages) {
    if (msg.role === "user") {
      html += `<div class="message message-user">
        <div class="message-content">${esc(msg.content)}</div>
      </div>`;
    } else {
      html += `<div class="message message-assistant">
        <div class="message-avatar">S</div>
        <div class="message-body">
          <div class="message-text">${renderMarkdown(msg.content)}</div>
          <div class="message-actions">
            <button class="msg-action-btn" data-copy="${esc(msg.content)}" title="Copier" aria-label="Copier la réponse">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            </button>
          </div>
        </div>
      </div>`;
    }
  }

  messagesArea.innerHTML = html;
  scrollToBottom();
}

function scrollToBottom() {
  const container = $("#chat-container");
  requestAnimationFrame(() => {
    container.scrollTop = container.scrollHeight;
  });
}

function showTypingIndicator() {
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

// ── Stream Message (typewriter effect) ──
function streamMessage(conv, fullText) {
  const messagesArea = $("#messages-area");
  const lastMsg = messagesArea.querySelector(".message-assistant:last-child .message-text");
  if (!lastMsg) {
    conv.messages[conv.messages.length - 1].content = fullText;
    conv.updatedAt = Date.now();
    saveConversations();
    state.isGenerating = false;
    updateSendButton();
    renderMessages();
    return;
  }

  let index = 0;
  const chunkSize = 3; // characters per frame
  const frameDelay = 12; // ms between frames

  function typeNext() {
    if (index >= fullText.length) {
      // Done typing
      conv.messages[conv.messages.length - 1].content = fullText;
      conv.updatedAt = Date.now();
      saveConversations();
      state.isGenerating = false;
      updateSendButton();
      // Re-render with full markdown
      renderMessages();
      return;
    }

    index = Math.min(index + chunkSize, fullText.length);
    const partial = fullText.slice(0, index);
    lastMsg.innerHTML = renderMarkdown(partial);
    scrollToBottom();

    setTimeout(typeNext, frameDelay);
  }

  typeNext();
}

// ── Send Message ──
async function sendMessage(text) {
  if (!text.trim() || state.isGenerating) return;

  // Create conversation if needed
  if (!state.activeConversationId) {
    const conv = createConversation(text.trim().slice(0, 40));
    state.activeConversationId = conv.id;
    updateTopbarTitle();
  }

  const conv = getConversation(state.activeConversationId);
  if (!conv) return;

  // Add user message
  conv.messages.push({ role: "user", content: text.trim() });

  // Update title if first message
  if (conv.messages.length === 1) {
    conv.title = text.trim().slice(0, 40) + (text.length > 40 ? "…" : "");
  }
  conv.updatedAt = Date.now();
  saveConversations();

  // Render
  renderMessages();
  renderConversationList();
  clearInput();

  // Show typing
  state.isGenerating = true;
  updateSendButton();
  showTypingIndicator();

  // Generate response with typing effect
  const response = generateResponse(text);
  const delay = Math.min(300 + response.length * 1.5, 1200);

  setTimeout(() => {
    removeTypingIndicator();

    // Add message with empty content, then stream it
    conv.messages.push({ role: "assistant", content: "" });
    renderMessages();
    streamMessage(conv, response);
  }, delay);
}

// ── Conversation List ──
function renderConversationList() {
  const list = $("#conversation-list");
  const searchQuery = $("#search-conversations").value.toLowerCase();

  let filtered = state.conversations;
  if (searchQuery) {
    filtered = filtered.filter(c =>
      c.title.toLowerCase().includes(searchQuery) ||
      c.messages.some(m => m.content.toLowerCase().includes(searchQuery))
    );
  }

  if (filtered.length === 0) {
    list.innerHTML = `<div style="padding: 20px 12px; text-align: center; color: var(--text-sidebar-muted); font-size: 12px;">
      ${searchQuery ? "Aucune conversation trouvée" : "Aucune conversation"}
    </div>`;
    return;
  }

  // Group by date
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
    if (convs.length === 0) continue;
    html += `<div class="conv-group-label">${label}</div>`;
    for (const conv of convs) {
      const isActive = conv.id === state.activeConversationId;
      html += `<div class="conv-item${isActive ? " active" : ""}" data-conv-id="${conv.id}">
        <span class="conv-item-title">${esc(conv.title)}</span>
        <button class="conv-item-menu" data-menu-id="${conv.id}" aria-label="Options">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="5" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="12" cy="19" r="1"/></svg>
        </button>
      </div>`;
    }
  }

  list.innerHTML = html;

  // Add click handlers
  list.querySelectorAll(".conv-item").forEach(item => {
    item.addEventListener("click", (e) => {
      if (e.target.closest(".conv-item-menu")) return;
      openConversation(item.dataset.convId);
    });
  });

  list.querySelectorAll(".conv-item-menu").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      showContextMenu(btn, btn.dataset.menuId);
    });
  });
}

function openConversation(id) {
  state.activeConversationId = id;
  renderConversationList();
  renderMessages();
  updateTopbarTitle();
  closeSidebar();
}

function startNewChat() {
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

// ── Context Menu ──
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
  const menu = $("#context-menu");
  menu.classList.remove("visible");

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

// ── Delete Modal ──
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

// ── Dictionary Panel ──
let dictDirection = "all";

function openDictionaryPanel() {
  $("#dictionary-modal").classList.add("visible");
  renderDictResults();
  $("#dict-search").focus();
}

function renderDictResults() {
  const query = normalizeWord($("#dict-search").value);
  const results = state.entries.filter(entry => {
    const snk = normalizeWord(entry.soninke);
    const fr = normalizeWord(entry.francais);
    if (dictDirection === "snk") return snk.includes(query);
    if (dictDirection === "fr") return fr.includes(query);
    return !query || snk.includes(query) || fr.includes(query);
  }).slice(0, MAX_DISPLAY);

  const container = $("#dict-results");
  if (results.length === 0) {
    container.innerHTML = `<div class="dict-empty">Aucun résultat</div>`;
    return;
  }

  container.innerHTML = results.map(e => {
    const audio = state.audioByWord.get(normalizeWord(e.soninke));
    return `<div class="dict-card">
      <h4>${esc(e.soninke)}${audio ? " 🔊" : ""}</h4>
      <div class="dict-translation">${esc(e.francais)}</div>
      <div class="dict-meta">${e.categorie ? esc(e.categorie) : ""}${e.statut ? " · " + esc(e.statut.replace(/_/g, " ")) : ""}</div>
    </div>`;
  }).join("");
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

// ── Input Handling ──
function clearInput() {
  const input = $("#message-input");
  input.value = "";
  autoResize(input);
  updateSendButton();
}

function autoResize(textarea) {
  textarea.style.height = "auto";
  textarea.style.height = Math.min(textarea.scrollHeight, 200) + "px";
}

function updateSendButton() {
  const input = $("#message-input");
  const btn = $("#send-btn");
  const hasText = input.value.trim().length > 0;

  if (state.isGenerating) {
    btn.classList.remove("enabled");
    btn.classList.add("loading");
  } else if (hasText) {
    btn.classList.add("enabled");
    btn.classList.remove("loading");
  } else {
    btn.classList.remove("enabled", "loading");
  }
}

// ── Copy to clipboard ──
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Fallback
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
      return true;
    } catch { return false; }
    finally { document.body.removeChild(textarea); }
  }
}

// ── Load Data ──
async function loadDictionary() {
  try {
    const response = await fetch(DATA_URL);
    if (!response.ok) throw new Error("HTTP " + response.status);
    const csv = await response.text();
    state.entries = parseCSV(csv, ";").filter(row => row.soninke || row.francais);
    $("#lexicon-count").textContent = state.entries.length;
    $("#about-count").textContent = state.entries.length;
    updateCorpusStatus();
  } catch {
    $("#corpus-status").textContent = "Données non chargées";
    $("#lexicon-count").textContent = "—";
  }
}

async function loadAudioIndex() {
  try {
    const [manifestResponse, auditResponse] = await Promise.all([
      fetch(MANIFEST_URL), fetch(AUDIO_AUDIT_URL)
    ]);
    if (!manifestResponse.ok || !auditResponse.ok) return;
    const [manifestText, auditText] = await Promise.all([
      manifestResponse.text(), auditResponse.text()
    ]);
    const manifest = parseCSV(manifestText, ",");
    const audit = parseCSV(auditText, ",");
    const successful = new Set(
      audit.filter(row => ["copied_from_source", "already_present"].includes(row.status)).map(row => row.id)
    );
    const byId = new Map(manifest.map(row => [row.id, row]));
    for (const id of successful) {
      const row = byId.get(id);
      if (!row || !row.text) continue;
      const key = normalizeWord(row.text);
      if (!state.audioByWord.has(key)) {
        state.audioByWord.set(key, { id, url: `audio/${encodeURIComponent(id)}.wav` });
      }
    }
    updateCorpusStatus();
  } catch {}
}

function updateCorpusStatus() {
  const count = state.entries.length;
  const audioCount = state.audioByWord.size;
  let status = count + " entrées";
  if (audioCount) status += " · " + audioCount + " audios";
  $("#corpus-status").textContent = status;
}

// ── Event Listeners ──
function initEvents() {
  // Input
  const input = $("#message-input");
  input.addEventListener("input", () => {
    autoResize(input);
    updateSendButton();
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (input.value.trim() && !state.isGenerating) {
        sendMessage(input.value);
      }
    }
  });

  // Send button
  $("#send-btn").addEventListener("click", () => {
    if (input.value.trim() && !state.isGenerating) {
      sendMessage(input.value);
    }
  });

  // New chat buttons
  $("#new-chat-btn").addEventListener("click", startNewChat);
  $("#new-chat-btn-top").addEventListener("click", startNewChat);

  // Menu button (mobile)
  $("#menu-btn").addEventListener("click", openSidebar);
  $("#sidebar-close").addEventListener("click", closeSidebar);
  $("#sidebar-overlay").addEventListener("click", closeSidebar);

  // Theme
  $("#theme-toggle").addEventListener("click", toggleTheme);

  $$(".theme-option").forEach(btn => {
    btn.addEventListener("click", () => {
      applyTheme(btn.dataset.theme);
    });
  });

  // Settings
  $("#settings-btn").addEventListener("click", () => {
    $("#settings-modal").classList.add("visible");
  });

  $("#settings-close").addEventListener("click", () => {
    $("#settings-modal").classList.remove("visible");
  });

  // Dictionary
  $("#dictionary-btn").addEventListener("click", () => {
    openDictionaryPanel();
    closeSidebar();
  });

  $("#dictionary-close").addEventListener("click", () => {
    $("#dictionary-modal").classList.remove("visible");
  });

  $("#dict-search").addEventListener("input", renderDictResults);

  $$(".dict-filter").forEach(btn => {
    btn.addEventListener("click", () => {
      dictDirection = btn.dataset.dir;
      $$(".dict-filter").forEach(b => b.classList.toggle("active", b === btn));
      renderDictResults();
    });
  });

  // Search conversations
  $("#search-conversations").addEventListener("input", renderConversationList);

  // Context menu
  $$("#context-menu .context-item").forEach(item => {
    item.addEventListener("click", () => handleContextAction(item.dataset.action));
  });

  // Delete modal
  $("#delete-cancel").addEventListener("click", () => {
    deleteTargetId = null;
    $("#delete-modal").classList.remove("visible");
  });

  $("#delete-confirm").addEventListener("click", confirmDelete);

  // Clear all data
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

  // Copy buttons
  document.addEventListener("click", async (e) => {
    const btn = e.target.closest(".msg-action-btn[data-copy]");
    if (btn) {
      const success = await copyToClipboard(btn.dataset.copy);
      if (success) {
        btn.classList.add("copied");
        setTimeout(() => btn.classList.remove("copied"), 2000);
      }
    }
  });

  // Suggestions
  $$(".suggestion-card").forEach(card => {
    card.addEventListener("click", () => {
      const prompt = card.dataset.prompt;
      if (prompt) {
        input.value = prompt;
        autoResize(input);
        updateSendButton();
        sendMessage(prompt);
      }
    });
  });

  // Close modals on overlay click
  $$(".modal-overlay").forEach(overlay => {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        overlay.classList.remove("visible");
      }
    });
  });

  // Close modals on Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      $$(".modal-overlay.visible").forEach(m => m.classList.remove("visible"));
      $("#context-menu").classList.remove("visible");
      closeSidebar();
    }
  });

  // System theme change
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    if (localStorage.getItem(THEME_KEY) === "auto") {
      applyTheme("auto");
    }
  });
}

// ── Initialize ──
async function init() {
  initTheme();
  loadConversations();
  initEvents();
  renderConversationList();
  renderMessages();

  // Load data
  await Promise.all([
    loadDictionary(),
    loadAudioIndex().catch(() => {})
  ]);
}

init();
