const DATA_URL = "data/source/lexique-soninke-fr-base.csv";
const MANIFEST_URL = "data/source/manifest-577-review.csv";
const AUDIO_AUDIT_URL = "reports/audio-transfer-audit.csv";
const state = { entries: [], audioByWord: new Map(), direction: "all" };
const $ = (selector) => document.querySelector(selector);

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
const normalizeWord = (value) => String(value || "").normalize("NFC").trim().toLocaleLowerCase("fr");
const esc = (value) => String(value || "").replace(/[&<>"']/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]));

function render() {
  const q = normalizeWord($("#search").value);
  const found = state.entries.filter(entry => {
    const snk = normalizeWord(entry.soninke);
    const fr = normalizeWord(entry.francais);
    const category = normalizeWord(entry.categorie);
    if (state.direction === "snk") return snk.includes(q);
    if (state.direction === "fr") return fr.includes(q);
    return !q || snk.includes(q) || fr.includes(q) || category.includes(q);
  }).slice(0, 100);
  $("#result-count").textContent = found.length + (found.length > 1 ? " entrées affichées" : " entrée affichée") + (state.entries.length > 100 && !q ? " · aperçu limité à 100" : "");
  $("#results").innerHTML = found.length ? found.map(entry => {
    const audio = state.audioByWord.get(normalizeWord(entry.soninke));
    return `<article class="word-card">
      <h3>${esc(entry.soninke)}</h3>
      <div class="translation">${esc(entry.francais)}</div>
      <div class="meta">${entry.categorie ? `<span class="pill">${esc(entry.categorie)}</span>` : ""}${entry.statut ? `<span class="pill">${esc(entry.statut.replaceAll("_"," "))}</span>` : ""}${entry.source ? `<span class="pill">Source : ${esc(entry.source)}</span>` : ""}</div>
      ${audio ? `<div class="audio-row"><audio controls preload="none" src="${esc(audio.url)}" aria-label="Prononciation de ${esc(entry.soninke)}"></audio><span class="audio-note">Enregistrement de référence · ${esc(audio.id)}</span></div>` : ""}
    </article>`;
  }).join("") : '<div class="empty">Aucun résultat. Essayez une autre graphie ou un mot en français.</div>';
}

$("#search").addEventListener("input", render);
$("#clear").addEventListener("click", () => { $("#search").value = ""; render(); $("#search").focus(); });
document.querySelectorAll("[data-direction]").forEach(button => button.addEventListener("click", () => {
  state.direction = button.dataset.direction;
  document.querySelectorAll("[data-direction]").forEach(item => item.classList.toggle("active", item === button));
  render();
}));

async function loadAudioIndex() {
  const [manifestResponse, auditResponse] = await Promise.all([
    fetch(MANIFEST_URL), fetch(AUDIO_AUDIT_URL)
  ]);
  if (!manifestResponse.ok || !auditResponse.ok) return;
  const [manifestText, auditText] = await Promise.all([manifestResponse.text(), auditResponse.text()]);
  const manifest = parseCSV(manifestText, ",");
  const audit = parseCSV(auditText, ",");
  const successful = new Set(audit.filter(row => ["copied_from_source", "already_present"].includes(row.status)).map(row => row.id));
  const byId = new Map(manifest.map(row => [row.id, row]));
  for (const id of successful) {
    const row = byId.get(id);
    if (!row || !row.text) continue;
    const key = normalizeWord(row.text);
    if (!state.audioByWord.has(key)) state.audioByWord.set(key, { id, url: `audio/${encodeURIComponent(id)}.wav` });
  }
}

Promise.all([
  fetch(DATA_URL).then(response => { if (!response.ok) throw new Error("HTTP " + response.status); return response.text(); }),
  loadAudioIndex().catch(() => {})
]).then(([csv]) => {
  state.entries = parseCSV(csv, ";").filter(row => row.soninke || row.francais);
  const linkedAudioCount = state.entries.filter(entry => state.audioByWord.has(normalizeWord(entry.soninke))).length;
  $("#corpus-status").textContent = state.entries.length + " entrées chargées" + (linkedAudioCount ? " · " + linkedAudioCount + " prononciations reliées" : "");
  render();
}).catch(() => {
  $("#corpus-status").textContent = "Données non chargées";
  $("#results").innerHTML = '<div class="empty">Le fichier du lexique est inaccessible depuis cette prévisualisation. Ouvrez le projet depuis le dépôt GitHub ou réessayez après le déploiement.</div>';
  $("#result-count").textContent = "—";
});
