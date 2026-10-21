const DATA_URL = "data/source/lexique-soninke-fr-base.csv";
const state = { entries: [], direction: "all" };
const $ = (selector) => document.querySelector(selector);
const parseCSV = (text) => {
  const rows = text.replace(/^\uFEFF/, "").split(/\r?\n/).filter(Boolean);
  if (!rows.length) return [];
  const parseLine = (line) => {
    const cells = []; let cell = "", quoted = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (ch === '"') { if (quoted && line[i + 1] === '"') { cell += '"'; i++; } else quoted = !quoted; }
      else if (ch === ";" && !quoted) { cells.push(cell); cell = ""; }
      else cell += ch;
    }
    cells.push(cell); return cells;
  };
  const headers = parseLine(rows[0]);
  return rows.slice(1).map(line => {
    const values = parseLine(line); return Object.fromEntries(headers.map((h,i) => [h, values[i] || ""]));
  }).filter(row => row.soninke || row.francais);
};
const esc = (value) => String(value || "").replace(/[&<>"']/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]));
function render() {
  const q = $("#search").value.trim().toLocaleLowerCase("fr");
  const found = state.entries.filter(entry => {
    const snk = (entry.soninke || "").toLocaleLowerCase("fr");
    const fr = (entry.francais || "").toLocaleLowerCase("fr");
    if (state.direction === "snk" && !snk.includes(q)) return false;
    if (state.direction === "fr" && !fr.includes(q)) return false;
    return !q || (state.direction === "snk" ? snk.includes(q) : state.direction === "fr" ? fr.includes(q) : snk.includes(q) || fr.includes(q) || (entry.categorie || "").toLocaleLowerCase("fr").includes(q));
  }).slice(0, 100);
  $("#result-count").textContent = found.length + (found.length > 1 ? " entrées affichées" : " entrée affichée") + (state.entries.length > 100 && !q ? " · aperçu limité à 100" : "");
  $("#results").innerHTML = found.length ? found.map(entry => `<article class="word-card"><h3>${esc(entry.soninke)}</h3><div class="translation">${esc(entry.francais)}</div><div class="meta">${entry.categorie ? `<span class="pill">${esc(entry.categorie)}</span>` : ""}${entry.statut ? `<span class="pill">${esc(entry.statut.replaceAll("_"," "))}</span>` : ""}${entry.source ? `<span class="pill">Source : ${esc(entry.source)}</span>` : ""}</div></article>`).join("") : '<div class="empty">Aucun résultat. Essayez une autre graphie ou un mot en français.</div>';
}
$("#search").addEventListener("input", render);
$("#clear").addEventListener("click", () => { $("#search").value = ""; render(); $("#search").focus(); });
document.querySelectorAll("[data-direction]").forEach(button => button.addEventListener("click", () => {
  state.direction = button.dataset.direction;
  document.querySelectorAll("[data-direction]").forEach(item => item.classList.toggle("active", item === button));
  render();
}));
fetch(DATA_URL).then(response => { if (!response.ok) throw new Error("HTTP " + response.status); return response.text(); })
  .then(csv => {
    state.entries = parseCSV(csv);
    $("#corpus-status").textContent = state.entries.length + " entrées chargées";
    render();
  })
  .catch(() => {
    $("#corpus-status").textContent = "Données non chargées";
    $("#results").innerHTML = '<div class="empty">Le fichier du lexique est inaccessible depuis cette prévisualisation. Ouvrez le projet depuis le dépôt GitHub ou réessayez après le déploiement.</div>';
    $("#result-count").textContent = "—";
  });
