# 🚀 LaunchPad AI — Real-Time Agentic Product Incubator

Turn **one sentence** into a **launch-ready, custom-designed landing page** — live,
on stage, in ~60 seconds. A team of four specialized AI agents collaborates in
real time, and you watch every handoff happen inside a cinematic dashboard.

> **Researcher → Strategist → Copywriter → Web Builder**

![pipeline](https://img.shields.io/badge/agents-4-6366F1) ![offline](https://img.shields.io/badge/replay%20mode-100%25%20offline-10B981) ![stack](https://img.shields.io/badge/FastAPI%20%2B%20Vanilla%20JS-0B0F19)

---

## ✨ Why it's built this way

The primary goal is the **visual "wow" factor** and **bulletproof stage
resilience**. If the venue Wi-Fi dies or an API times out, a high-fidelity
**Stage-Safe Replay Mode** takes over instantly — fully offline, with zero
external resources.

- **Live token streaming** with a cinematic 40 char/sec pacing queue.
- **Animated SVG handoff pulses** between agent cards.
- **Glassmorphic cyber-dark UI** with a reveal-moment confetti burst.
- **Structured JSON handoffs** validated with Pydantic between every stage.
- **Graceful degradation** — per-agent fallback badge: *"API Offline – Using Cached Backup"*.

---

## 🏃 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Configure a live LLM provider in .env — NOT needed for Replay Mode

# 3. Run the server
uvicorn backend.main:app --host 0.0.0.0 --port 8000
#    or:  python -m backend.main

# 4. Open the dashboard
open http://localhost:8000
```

**For the demo:** leave the toggle on **Stage-Safe Replay** and hit
**Launch Project**. No keys, no network required.

---

## 🔌 Live Mode (optional)

Set a key + model in `.env`. Supported via [LiteLLM](https://github.com/BerriAI/litellm):

| Provider | Env var | `LLM_MODEL` |
|---|---|---|
| Anthropic (default) | `ANTHROPIC_API_KEY` | `anthropic/claude-3-5-sonnet-20241022` |
| Groq (fastest) | `GROQ_API_KEY` | `groq/llama-3.3-70b-versatile` |
| Google Gemini (free tier) | `GEMINI_API_KEY` | `gemini/gemini-1.5-flash` or `gemini/gemini-2.0-flash-lite` |
| Ollama (local) | — | `ollama/qwen2.5:7b` |

Flip the toggle to **Live API**. If any agent's call fails, that card shows the
warning badge and the pipeline silently continues from cached data.

---

## 🧱 Architecture

```
frontend/                 Vanilla HTML/CSS/JS dashboard (no build step)
  index.html              Cinematic split-panel UI
  style.css               Glassmorphic cyber-dark theme
  app.js                  WebSocket client, pacing queue, SVG pulses, confetti
backend/
  main.py                 FastAPI + WebSocket orchestrator + static serving
  agents.py               System prompts, Pydantic schemas, JSON stream extractor
  mock_data.py            Cached cinematic outputs for offline Replay Mode
```

### Data flow
1. Browser opens `/ws` and sends `{idea, mode}`.
2. Server runs the pipeline, streaming `token` events per agent.
3. Each agent's trailing ` ```json ` block is extracted by a state machine and
   validated against its Pydantic schema, then fed into the next agent's prompt.
4. The Web Builder emits raw HTML → `render` event → iframe reveal + confetti.

---

## 🛡️ Offline Verification

1. Disable your network / enable airplane mode.
2. Load `http://localhost:8000`, keep **Replay Mode** on, hit **Launch**.
3. The full pipeline streams and the BarkSpeak landing page renders with **zero
   network requests** — the generated page uses only system fonts and inline SVG.

---

See [`DEMO_SCRIPT.md`](./DEMO_SCRIPT.md) for the timed stage walkthrough.
