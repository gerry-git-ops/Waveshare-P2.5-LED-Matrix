// Dashboard: menu, design, translations and the data from the API.

// ---------- translations (UI follows "language" in config.yaml) ----------
const TEXTS = {
  en: {
    design: "Design", system: "System", light: "Light", dark: "Dark",
    live: "Live", modules: "Modules", hardware: "Hardware", now: "On screen now",
    size: "Size", unlit: "Unlit LEDs", screenshot: "Screenshot", fullscreen: "Fullscreen",
    panels: "Panels", preview: "Preview", connected: "live", reconnecting: "reconnecting…",
    on: "on", off: "off", running: "running", left: "left", duration: "Duration",
    auto: "set by the module", seconds: "s",
    display: "Display", wiring: "Wiring", general: "General", brightness: "Brightness",
    pixels: "Pixels", panel: "Panel", chains: "Chains", per_chain: "Panels per chain",
    mapping: "GPIO mapping", slowdown: "GPIO slowdown", colors: "Color order",
    fps: "Frames per second", language: "Language",
    matrix: "Matrix", host: "Host", cpu: "CPU", temperature: "Temperature", memory: "Memory",
    disk: "Storage", uptime: "Uptime", system: "System", cores: "Cores", frequency: "Clock",
    load: "Load (1/5/15 min)", hostname: "Hostname", ip: "IP address", os: "Operating system",
    python: "Python", not_available: "not reported by this system", of: "of",
    d: "d", h: "h", min: "min",
  },
  de: {
    design: "Design", system: "System", light: "Hell", dark: "Dunkel",
    live: "Live", modules: "Module", hardware: "Hardware", now: "Gerade zu sehen",
    size: "Größe", unlit: "Dunkle LEDs", screenshot: "Screenshot", fullscreen: "Vollbild",
    panels: "Panels", preview: "Vorschau", connected: "live", reconnecting: "verbinde neu…",
    on: "an", off: "aus", running: "läuft", left: "übrig", duration: "Dauer",
    auto: "legt das Modul fest", seconds: "s",
    display: "Anzeige", wiring: "Anschluss", general: "Allgemein", brightness: "Helligkeit",
    pixels: "Pixel", panel: "Panel", chains: "Ketten", per_chain: "Panels pro Kette",
    mapping: "GPIO-Belegung", slowdown: "GPIO-Bremse", colors: "Farbreihenfolge",
    fps: "Bilder pro Sekunde", language: "Sprache",
    matrix: "Matrix", host: "Host", cpu: "CPU", temperature: "Temperatur", memory: "Arbeitsspeicher",
    disk: "Speicherplatz", uptime: "Laufzeit", system: "System", cores: "Kerne", frequency: "Takt",
    load: "Last (1/5/15 min)", hostname: "Hostname", ip: "IP-Adresse", os: "Betriebssystem",
    python: "Python", not_available: "wird von diesem System nicht gemeldet", of: "von",
    d: "T", h: "Std", min: "Min",
  },
    fr: {
    design: "Thème", system: "Système", light: "Clair", dark: "Sombre",
    live: "Direct", modules: "Modules", hardware: "Matériel", now: "À l'écran",
    size: "Taille", unlit: "LED éteintes", screenshot: "Capture", fullscreen: "Plein écran",
    panels: "Panneaux", preview: "Aperçu", connected: "en direct", reconnecting: "reconnexion…",
    on: "activé", off: "désactivé", running: "en cours", left: "restant", duration: "Durée",
    auto: "défini par le module", seconds: "s",
    display: "Affichage", wiring: "Câblage", general: "Général", brightness: "Luminosité",
    pixels: "Pixels", panel: "Panneau", chains: "Chaînes", per_chain: "Panneaux par chaîne",
    mapping: "Brochage GPIO", slowdown: "Ralentissement GPIO", colors: "Ordre des couleurs",
    fps: "Images par seconde", language: "Langue",
    matrix: "Matrice", host: "Hôte", cpu: "CPU", temperature: "Température", memory: "Mémoire",
    disk: "Stockage", uptime: "En marche depuis", system: "Système", cores: "Cœurs", frequency: "Fréquence",
    load: "Charge (1/5/15 min)", hostname: "Nom d'hôte", ip: "Adresse IP", os: "Système d'exploitation",
    python: "Python", not_available: "non fourni par ce système", of: "sur",
    d: "j", h: "h", min: "min",
  },
  es: {
    design: "Diseño", system: "Sistema", light: "Claro", dark: "Oscuro",
    live: "En vivo", modules: "Módulos", hardware: "Hardware", now: "En pantalla",
    size: "Tamaño", unlit: "LED apagados", screenshot: "Captura", fullscreen: "Pantalla completa",
    panels: "Paneles", preview: "Vista previa", connected: "en vivo", reconnecting: "reconectando…",
    on: "activo", off: "inactivo", running: "en curso", left: "restante", duration: "Duración",
    auto: "lo define el módulo", seconds: "s",
    display: "Pantalla", wiring: "Conexión", general: "General", brightness: "Brillo",
    pixels: "Píxeles", panel: "Panel", chains: "Cadenas", per_chain: "Paneles por cadena",
    mapping: "Asignación GPIO", slowdown: "Ralentización GPIO", colors: "Orden de colores",
    fps: "Imágenes por segundo", language: "Idioma",
    matrix: "Matriz", host: "Host", cpu: "CPU", temperature: "Temperatura", memory: "Memoria",
    disk: "Almacenamiento", uptime: "Tiempo activo", system: "Sistema", cores: "Núcleos", frequency: "Frecuencia",
    load: "Carga (1/5/15 min)", hostname: "Nombre del equipo", ip: "Dirección IP", os: "Sistema operativo",
    python: "Python", not_available: "este sistema no lo informa", of: "de",
    d: "d", h: "h", min: "min",
  },
};
let T = TEXTS.en;
const t = (key) => T[key] ?? TEXTS.en[key] ?? key;
function translatePage() {
  for (const el of document.querySelectorAll("[data-t]")) el.textContent = t(el.dataset.t);
}

// ---------- design: system / light / dark ----------
const themeSelect = document.getElementById("theme");
themeSelect.value = localStorage.getItem("ledmatrix-theme") || "system";
function applyTheme() {
  const mode = themeSelect.value;
  const dark = mode === "dark" || (mode === "system" && matchMedia("(prefers-color-scheme: dark)").matches);
  document.documentElement.className = dark ? "dark" : "light";
}
themeSelect.onchange = () => { localStorage.setItem("ledmatrix-theme", themeSelect.value); applyTheme(); };
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", applyTheme);

// ---------- menu ----------
document.getElementById("tabs").onclick = (e) => {
  const tab = e.target.closest(".tab");
  if (!tab) return;
  for (const b of document.querySelectorAll(".tab")) b.classList.toggle("active", b === tab);
  for (const p of document.querySelectorAll(".page")) p.classList.toggle("active", p.id === "page-" + tab.dataset.tab);
  if (tab.dataset.tab === "live") led.layout();
};

// ---------- helpers ----------
const el = (html) => { const d = document.createElement("div"); d.innerHTML = html.trim(); return d.firstChild; };
const esc = (v) => String(v).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const isColor = (v) => Array.isArray(v) && v.length === 3 && v.every((n) => Number.isInteger(n) && n >= 0 && n <= 255);
function show(v) {
  // option values: colors as a little swatch, lists short and readable
  if (isColor(v)) return `<span class="swatch" style="background:rgb(${v})"></span>${v.join(", ")}`;
  if (Array.isArray(v)) {
    if (v.every(isColor)) return v.map(show).join("<br>");
    return v.map((x) => (x && typeof x === "object" ? esc(x.file ?? JSON.stringify(x)) : esc(x))).join("<br>");
  }
  if (v && typeof v === "object") return esc(JSON.stringify(v));
  return esc(v);
}
const api = (path) => fetch(path).then((r) => r.json());

// ---------- modules ----------
let modules = [];
function renderModules(status) {
  const list = document.getElementById("module-list");
  list.replaceChildren(...modules.map((m) => {
    const running = status && m.index === status.config_index;
    const options = Object.entries(m.options)
      .map(([k, v]) => `<div class="row"><span>${esc(k)}</span><span>${show(v)}</span></div>`).join("");
    const duration = m.duration ? `${m.duration} ${t("seconds")}` : t("auto");
    return el(`
      <div class="tile ${running ? "running" : ""} ${m.enabled ? "" : "disabled"}">
        <div class="tile-head">
          <span class="badge number">#${m.index + 1}</span>
          <span class="tile-name">${esc(m.type)}</span>
          ${running ? `<span class="badge">▶ ${t("running")}</span>` : ""}
          <span class="badge ${m.enabled ? "" : "off"}">${m.enabled ? t("on") : t("off")}</span>
        </div>
        <div class="rows">
          <div class="row"><span>${t("duration")}</span><span>${duration}</span></div>
          ${options}
        </div>
      </div>`);
  }));
}

// ---------- hardware ----------
function renderHardware(c) {
  const hw = c.hardware;
  const tile = (title, body) => `<div class="tile"><div class="tile-head"><span class="tile-name">${title}</span></div>${body}</div>`;
  const row = (k, v) => `<div class="row"><span>${t(k)}</span><span>${esc(v)}</span></div>`;
  document.getElementById("hardware-list").replaceChildren(
    el(tile(t("display"), `<div class="big">${hw.width} × ${hw.height}</div><div class="rows">
      ${row("panel", `${hw.cols} × ${hw.rows}`)}${row("per_chain", hw.chain_length)}${row("chains", hw.parallel)}</div>`)),
    el(tile(t("brightness"), `<div class="big">${hw.brightness} %</div><div class="bar"><div style="width:${hw.brightness}%"></div></div>`)),
    el(tile(t("wiring"), `<div class="rows">${row("mapping", hw.hardware_mapping)}${row("slowdown", hw.gpio_slowdown)}${row("colors", hw.rgb_sequence)}</div>`)),
    el(tile(t("general"), `<div class="rows">${row("fps", c.fps)}${row("language", c.language)}</div>`)),
  );
}

// ---------- host: the computer the matrix runs on ----------
const size = (bytes) => bytes >= 1e9 ? (bytes / 1e9).toFixed(1) + " GB" : Math.round(bytes / 1e6) + " MB";
function duration(seconds) {
  const d = Math.floor(seconds / 86400), h = Math.floor(seconds % 86400 / 3600), m = Math.floor(seconds % 3600 / 60);
  return (d ? `${d} ${t("d")} ` : "") + (d || h ? `${h} ${t("h")} ` : "") + `${m} ${t("min")}`;
}
function bar(percent, warn = 70, hot = 85) {
  const level = percent >= hot ? "hot" : percent >= warn ? "warn" : "";
  return `<div class="bar ${level}"><div style="width:${Math.min(100, percent)}%"></div></div>`;
}
function renderHost(h) {
  document.getElementById("host-model").textContent = `(${h.model})`;
  const tile = (title, body) => `<div class="tile"><div class="tile-head"><span class="tile-name">${t(title)}</span></div>${body}</div>`;
  const row = (k, v) => `<div class="row"><span>${t(k)}</span><span>${esc(v)}</span></div>`;
  const temp = h.temperature === null
    ? `<div class="big">–</div><div class="rows"><div class="row"><span>${t("not_available")}</span><span></span></div></div>`
    : `<div class="big">${h.temperature} °C</div>${bar(h.temperature, 65, 80)}`;
  document.getElementById("host-list").replaceChildren(
    el(tile("cpu", `<div class="big">${h.cpu.percent} %</div>${bar(h.cpu.percent)}<div class="rows" style="margin-top:10px">
      ${row("cores", h.cpu.cores)}${h.cpu.mhz ? row("frequency", h.cpu.mhz + " MHz") : ""}${row("load", h.cpu.load.join(" · "))}</div>`)),
    el(tile("temperature", temp)),
    el(tile("memory", `<div class="big">${h.memory.percent} %</div>${bar(h.memory.percent)}
      <div class="rows" style="margin-top:10px"><div class="row"><span>${size(h.memory.used)} ${t("of")} ${size(h.memory.total)}</span><span></span></div></div>`)),
    el(tile("disk", `<div class="big">${h.disk.percent} %</div>${bar(h.disk.percent, 80, 90)}
      <div class="rows" style="margin-top:10px"><div class="row"><span>${size(h.disk.used)} ${t("of")} ${size(h.disk.total)}</span><span></span></div></div>`)),
    el(tile("uptime", `<div class="big">${duration(h.uptime)}</div>`)),
    el(tile("system", `<div class="rows">${row("hostname", h.hostname)}${row("ip", h.ip)}${row("os", h.os)}${row("python", h.python)}</div>`)),
  );
}
async function updateHost() {
  try { renderHost(await api("/api/host")); } catch {}
}

// ---------- status, polled every second ----------
async function updateStatus() {
  try {
    const s = await api("/api/status");
    document.getElementById("now-name").textContent = s.module;
    const done = s.duration ? (s.elapsed / s.duration) * 100 : 0;
    document.getElementById("progress").style.width = Math.min(100, done) + "%";
    const mode = document.getElementById("mode");
    mode.textContent = s.preview ? t("preview") : t("panels");
    mode.classList.toggle("off", s.preview);
    renderModules(s);
  } catch {}
  document.getElementById("fps").textContent = `${led.takeFrames()} fps`;
}

// ---------- start ----------
(async () => {
  const config = await api("/api/config");
  T = TEXTS[config.language] || TEXTS.en;
  document.documentElement.lang = config.language;
  translatePage();
  renderHardware(config);
  modules = await api("/api/modules");
  led.connect((ok) => {
    document.getElementById("dot").classList.toggle("live", ok);
    document.getElementById("conn").textContent = ok ? t("connected") : t("reconnecting");
  });
  updateStatus();
  setInterval(updateStatus, 1000);
  updateHost();
  setInterval(updateHost, 3000);
})();