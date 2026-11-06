// LED view: draws the live picture as glowing LEDs on a canvas.
// Taken over from the old browser preview.

const led = (() => {
  const defaults = { fit: true, scale: 8, dot: 0.8, glow: 0.55, shape: "round", unlit: true };
  const cfg = { ...defaults };
  try { Object.assign(cfg, JSON.parse(localStorage.getItem("ledmatrix-led") || "{}")); } catch {}
  const save = () => { try { localStorage.setItem("ledmatrix-led", JSON.stringify(cfg)); } catch {} };

  const screen = document.getElementById("screen");
  const ctx = screen.getContext("2d");
  const src = document.createElement("canvas");    // 1 pixel per LED
  const srcCtx = src.getContext("2d");
  const lit = document.createElement("canvas");    // lit LEDs, scaled up
  const litCtx = lit.getContext("2d");
  const mask = document.createElement("canvas");   // LED shapes
  const unlit = document.createElement("canvas");  // dark, unlit LEDs
  let W = 0, H = 0, S = 1, image = null, frames = 0;

  function currentScale() {
    if (!cfg.fit) return cfg.scale;
    const wrap = document.getElementById("screen-wrap");
    const room = Math.min((wrap.clientWidth - 40) / W, (innerHeight * 0.5) / H);
    return Math.max(2, Math.floor(room));
  }

  function drawShapes(target, color) {
    const c = target.getContext("2d");
    c.clearRect(0, 0, target.width, target.height);
    c.fillStyle = color;
    const d = S * cfg.dot, off = (S - d) / 2;
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        if (cfg.shape === "round") {
          c.beginPath();
          c.arc(x * S + S / 2, y * S + S / 2, d / 2, 0, Math.PI * 2);
          c.fill();
        } else {
          c.fillRect(x * S + off, y * S + off, d, d);
        }
      }
    }
  }

  function layout() {
    if (!W) return;
    S = currentScale();
    for (const c of [screen, lit, mask, unlit]) { c.width = W * S; c.height = H * S; }
    drawShapes(mask, "#fff");
    drawShapes(unlit, "rgba(255,255,255,0.055)");
    draw();
  }

  function draw() {
    if (!W) return;
    // 1) lit LEDs: scale the frame up without smoothing, then cut out the LED shapes
    litCtx.globalCompositeOperation = "source-over";
    litCtx.clearRect(0, 0, lit.width, lit.height);
    litCtx.imageSmoothingEnabled = false;
    litCtx.drawImage(src, 0, 0, lit.width, lit.height);
    litCtx.globalCompositeOperation = "destination-in";
    litCtx.drawImage(mask, 0, 0);

    // 2) compose: background, unlit LEDs, lit LEDs, glow
    ctx.globalCompositeOperation = "source-over";
    ctx.filter = "none";
    ctx.globalAlpha = 1;
    ctx.fillStyle = "#040506";
    ctx.fillRect(0, 0, screen.width, screen.height);
    if (cfg.unlit) ctx.drawImage(unlit, 0, 0);
    ctx.drawImage(lit, 0, 0);
    if (cfg.glow > 0) {
      ctx.globalCompositeOperation = "lighter";
      ctx.globalAlpha = cfg.glow;
      ctx.filter = `blur(${Math.max(1, S * 0.8)}px)`;
      ctx.drawImage(lit, 0, 0);
      ctx.filter = "none";
      ctx.globalAlpha = 1;
      ctx.globalCompositeOperation = "source-over";
    }
  }

  // one message = "WxH:" + base64 of the raw RGB bytes
  function onFrame(msg) {
    const sep = msg.indexOf(":");
    const [w, h] = msg.slice(0, sep).split("x").map(Number);
    if (w !== W || h !== H) {
      W = w; H = h;
      src.width = W; src.height = H;
      image = srcCtx.createImageData(W, H);
      layout();
    }
    const bin = atob(msg.slice(sep + 1));
    const px = image.data;
    for (let i = 0, j = 0; i < bin.length; i += 3, j += 4) {
      px[j] = bin.charCodeAt(i);
      px[j + 1] = bin.charCodeAt(i + 1);
      px[j + 2] = bin.charCodeAt(i + 2);
      px[j + 3] = 255;
    }
    srcCtx.putImageData(image, 0, 0);
    draw();
    frames++;
  }

  function connect(onState) {
    const es = new EventSource("/api/stream");
    es.onopen = () => onState(true);
    es.onmessage = (e) => onFrame(e.data);
    es.onerror = () => onState(false);
  }

  // ---------- controls ----------
  function bindRange(id, key) {
    const el = document.getElementById(id);
    el.value = cfg[key];
    el.oninput = () => {
      cfg[key] = Number(el.value);
      if (key === "scale") { cfg.fit = false; syncSegs(); }
      save(); layout();
    };
  }
  function syncSegs() {
    for (const b of document.querySelectorAll("#fit button")) b.classList.toggle("on", (b.dataset.v === "fit") === cfg.fit);
    for (const b of document.querySelectorAll("#shape button")) b.classList.toggle("on", b.dataset.v === cfg.shape);
    document.querySelector("#unlit button").classList.toggle("on", cfg.unlit);
  }
  bindRange("scale", "scale");
  bindRange("dot_size", "dot");
  bindRange("glow", "glow");
  document.getElementById("fit").onclick = (e) => {
    if (!e.target.dataset.v) return;
    cfg.fit = e.target.dataset.v === "fit"; save(); syncSegs(); layout();
  };
  document.getElementById("shape").onclick = (e) => {
    if (!e.target.dataset.v) return;
    cfg.shape = e.target.dataset.v; save(); syncSegs(); layout();
  };
  document.getElementById("unlit").onclick = () => { cfg.unlit = !cfg.unlit; save(); syncSegs(); draw(); };
  syncSegs();

  const wrap = document.getElementById("screen-wrap");
  const toggleFull = () => document.fullscreenElement ? document.exitFullscreen() : wrap.requestFullscreen();
  document.getElementById("full").onclick = toggleFull;
  document.addEventListener("fullscreenchange", layout);

  document.getElementById("snap").onclick = () => {
    screen.toBlob((blob) => {
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `ledmatrix-${new Date().toISOString().replace(/[:.]/g, "-")}.png`;
      a.click();
      URL.revokeObjectURL(a.href);
    });
  };

  addEventListener("resize", () => { if (cfg.fit) layout(); });

  // show the pixel under the mouse, handy when building modules
  screen.addEventListener("mousemove", (e) => {
    document.getElementById("pos").textContent = `x ${Math.floor(e.offsetX / S)} · y ${Math.floor(e.offsetY / S)}`;
  });
  screen.addEventListener("mouseleave", () => { document.getElementById("pos").textContent = ""; });

  return {
    connect, layout, toggleFull,
    takeFrames() { const f = frames; frames = 0; return f; },
  };
})();