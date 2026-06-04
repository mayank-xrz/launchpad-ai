/* ============================================================
   LaunchPad AI — Frontend controller
   WebSocket client · token pacing queue · SVG handoff pulses ·
   reveal animation · confetti burst.
   ============================================================ */

const EXAMPLE_IDEA =
  "A smart dog collar that translates barks into funny text messages using AI.";

const AGENTS = ["researcher", "strategist", "copywriter", "builder"];
const CARD_ID = {
  researcher: "agent-researcher",
  strategist: "agent-strategist",
  copywriter: "agent-copywriter",
  builder: "agent-builder",
};
const OUT_ID = {
  researcher: "output-researcher",
  strategist: "output-strategist",
  copywriter: "output-copywriter",
  builder: "output-builder",
};

// ---- DOM ----
const $ = (id) => document.getElementById(id);
const ideaInput = $("idea-input");
const exampleBtn = $("example-btn");
const launchBtn = $("launch-btn");
const replayToggle = $("replay-toggle");
const statusChip = $("connection-status");
const statusLabel = statusChip.querySelector(".status-label");
const placeholder = $("placeholder");
const frame = $("sandbox-frame");
const connectorsSvg = $("pipeline-connectors");

let ws = null;
let running = false;

/* ============================================================
   Token pacing queue — max ~40 chars/sec, cinematic readability.
   Each agent gets its own queue; tokens drain at a steady rate.
   ============================================================ */
class Pacer {
  constructor(targetEl, charsPerSec = 40) {
    this.el = targetEl;
    this.buffer = "";
    this.interval = null;
    this.charsPerTick = Math.max(1, Math.round(charsPerSec / 10)); // 10 ticks/sec
    this.cursor = document.createElement("span");
    this.cursor.className = "cursor";
    this.onDrain = null;
  }
  push(text) {
    this.buffer += text;
    this.start();
  }
  start() {
    if (this.interval) return;
    this.el.appendChild(this.cursor);
    this.interval = setInterval(() => this.tick(), 100);
  }
  tick() {
    if (this.buffer.length === 0) {
      clearInterval(this.interval);
      this.interval = null;
      if (this.onDrain) this.onDrain();
      return;
    }
    const slice = this.buffer.slice(0, this.charsPerTick);
    this.buffer = this.buffer.slice(this.charsPerTick);
    this.cursor.insertAdjacentText("beforebegin", slice);
    this.el.scrollTop = this.el.scrollHeight;
  }
  finish(cb) {
    // Resolve when the buffer is fully drained.
    if (this.buffer.length === 0 && !this.interval) {
      this.cursor.remove();
      cb && cb();
    } else {
      this.onDrain = () => {
        this.cursor.remove();
        cb && cb();
      };
    }
  }
}

const pacers = {};

/* ============================================================
   Card state helpers
   ============================================================ */
function setCardState(agent, state) {
  const card = $(CARD_ID[agent]);
  card.classList.remove("idle", "thinking", "streaming", "done", "warn");
  card.classList.add(state);
  // expose accent as CSS var for color-mix
  card.style.setProperty("--accent", card.dataset.accent);
}

function resetAll() {
  AGENTS.forEach((a) => {
    setCardState(a, "idle");
    $(OUT_ID[a]).textContent = "";
    pacers[a] = new Pacer($(OUT_ID[a]));
  });
  frame.classList.remove("revealed");
  frame.removeAttribute("srcdoc");
  placeholder.classList.remove("hidden");
  clearConnectors();
}

function setStatus(label, cls) {
  statusLabel.textContent = label;
  statusChip.classList.remove("running", "error");
  if (cls) statusChip.classList.add(cls);
}

/* ============================================================
   SVG connectors — draw lines card→card, pulse on handoff
   ============================================================ */
function drawConnectors() {
  const pipeRect = $("pipeline").getBoundingClientRect();
  for (let i = 0; i < AGENTS.length - 1; i++) {
    const a = $(CARD_ID[AGENTS[i]]).getBoundingClientRect();
    const b = $(CARD_ID[AGENTS[i + 1]]).getBoundingClientRect();
    const x = 18; // sits in the left gutter of the pipeline
    const y1 = a.bottom - pipeRect.top + $("pipeline").scrollTop;
    const y2 = b.top - pipeRect.top + $("pipeline").scrollTop;
    const path = $(`path-${i}`);
    path.setAttribute("d", `M ${x} ${y1 - 6} C ${x} ${y1 + 10}, ${x} ${y2 - 16}, ${x} ${y2 + 6}`);
  }
}

function clearConnectors() {
  for (let i = 0; i < 3; i++) {
    const p = $(`path-${i}`);
    p.classList.remove("active-handoff");
    p.style.stroke = "";
  }
}

function pulseConnector(fromIdx, toAgent) {
  const p = $(`path-${fromIdx}`);
  if (!p) return;
  const accent = $(CARD_ID[toAgent]).dataset.accent;
  p.style.stroke = accent;
  p.style.color = accent;
  p.classList.remove("active-handoff");
  void p.getBBox(); // reflow to restart animation
  p.classList.add("active-handoff");
}

window.addEventListener("resize", () => { if (running) drawConnectors(); });

/* ============================================================
   Reveal moment — scale-in iframe, confetti, auto-scroll tour
   ============================================================ */
function revealSite(html) {
  frame.srcdoc = html;
  frame.onload = () => {
    placeholder.classList.add("hidden");
    requestAnimationFrame(() => frame.classList.add("revealed"));
    fireConfetti(5000);
    setTimeout(autoScrollTour, 900);
  };
}

function autoScrollTour() {
  try {
    const doc = frame.contentWindow;
    if (!doc) return;
    const max = frame.contentDocument.body.scrollHeight;
    let pos = 0;
    const down = setInterval(() => {
      pos += max / 90;
      doc.scrollTo({ top: pos, behavior: "auto" });
      if (pos >= max - frame.clientHeight) {
        clearInterval(down);
        setTimeout(() => doc.scrollTo({ top: 0, behavior: "smooth" }), 1200);
      }
    }, 30);
  } catch (e) { /* cross-origin safe-guard, srcdoc is same-origin */ }
}

/* ---- lightweight canvas confetti (no dependencies) ---- */
function fireConfetti(duration) {
  const canvas = $("confetti-canvas");
  const ctx = canvas.getContext("2d");
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width;
  canvas.height = rect.height;
  canvas.classList.add("active");

  const colors = ["#6366F1", "#8B5CF6", "#EC4899", "#10B981", "#2DD4BF", "#FB7185", "#FBBF24"];
  const N = 160;
  const parts = Array.from({ length: N }, () => ({
    x: canvas.width / 2 + (Math.random() - 0.5) * 120,
    y: canvas.height / 2,
    vx: (Math.random() - 0.5) * 14,
    vy: Math.random() * -16 - 4,
    size: Math.random() * 7 + 3,
    color: colors[(Math.random() * colors.length) | 0],
    rot: Math.random() * Math.PI,
    vr: (Math.random() - 0.5) * 0.3,
  }));

  const start = performance.now();
  (function frameLoop(now) {
    const t = now - start;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    parts.forEach((p) => {
      p.vy += 0.4; // gravity
      p.x += p.vx; p.y += p.vy; p.rot += p.vr;
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rot);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = Math.max(0, 1 - t / duration);
      ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
      ctx.restore();
    });
    if (t < duration) requestAnimationFrame(frameLoop);
    else { ctx.clearRect(0, 0, canvas.width, canvas.height); canvas.classList.remove("active"); }
  })(start);
}

/* ============================================================
   WebSocket pipeline driver
   ============================================================ */
function launch() {
  if (running) return;
  running = true;
  launchBtn.disabled = true;
  launchBtn.querySelector(".launch-text").textContent = "Launching…";
  resetAll();
  drawConnectors();
  setStatus("Running", "running");

  const mode = replayToggle.checked ? "replay" : "live";
  const proto = location.protocol === "https:" ? "wss" : "ws";
  ws = new WebSocket(`${proto}://${location.host}/ws`);

  ws.onopen = () => {
    ws.send(JSON.stringify({
      idea: ideaInput.value.trim() || EXAMPLE_IDEA,
      mode,
    }));
  };

  ws.onmessage = (ev) => handleEvent(JSON.parse(ev.data));

  ws.onerror = () => setStatus("Connection error", "error");
  ws.onclose = () => { /* end handled by pipeline_done */ };
}

function handleEvent(msg) {
  switch (msg.type) {
    case "pipeline_start":
      drawConnectors();
      break;

    case "agent_start":
      setCardState(msg.agent, "thinking");
      // flip to streaming once first token arrives
      break;

    case "token":
      if ($(CARD_ID[msg.agent]).classList.contains("thinking")) {
        setCardState(msg.agent, "streaming");
      }
      pacers[msg.agent].push(msg.text);
      break;

    case "fallback":
      setCardState(msg.agent, "warn");
      break;

    case "agent_done": {
      const finishState = $(CARD_ID[msg.agent]).classList.contains("warn")
        ? "warn" : "done";
      // Wait for the pacer to drain before marking visually complete.
      pacers[msg.agent].finish(() => {
        if (finishState === "done") setCardState(msg.agent, "done");
      });
      break;
    }

    case "handoff": {
      const fromIdx = AGENTS.indexOf(msg.from);
      pulseConnector(fromIdx, msg.to);
      break;
    }

    case "render":
      // Defer reveal slightly so the builder's stream finishes draining.
      pacers.builder.finish(() => {
        setTimeout(() => revealSite(msg.html), 400);
      });
      break;

    case "pipeline_done":
      setStatus("Complete", null);
      running = false;
      launchBtn.disabled = false;
      launchBtn.querySelector(".launch-text").textContent = "Launch Project";
      break;

    case "error":
      setStatus("Error", "error");
      running = false;
      launchBtn.disabled = false;
      launchBtn.querySelector(".launch-text").textContent = "Launch Project";
      break;
  }
}

/* ============================================================
   Wiring
   ============================================================ */
exampleBtn.addEventListener("click", () => {
  ideaInput.value = EXAMPLE_IDEA;
  ideaInput.focus();
});
launchBtn.addEventListener("click", launch);
ideaInput.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === "Enter") launch();
});

replayToggle.addEventListener("change", () => {
  const labels = document.querySelectorAll(".toggle-label");
  labels[0].classList.toggle("toggle-active", !replayToggle.checked);
  labels[1].classList.toggle("toggle-active", replayToggle.checked);
});

// initialize idle state on load
resetAll();
