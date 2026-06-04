# 🎬 LaunchPad AI — Live Pitch Demo Script

> Keep **Stage-Safe Replay** ON for the live demo. It is flawless, paced, and
> 100% offline. Switch to **Live API** only if you want to prove live calls and
> have a reliable connection + key configured.

---

## A. Hook & Closing Line

**Hook (say before launching):**
> "Most AI projects operate inside a silent black box. Today, we are opening the
> engine cover to show you how a team of autonomous AI agents collaborates in
> real time to take a product from a raw sentence to a launch-ready,
> custom-designed landing page."

**Closing Line (after the reveal):**
> "No templates, no drag-and-drop editors, no manual code—just a sentence, a
> collaborative team of agents, and a fully polished, launch-ready web app in
> 60 seconds."

---

## B. Timed Demo Script (≈60–75s)

| Time | Visual cue | What to say |
|------|-----------|-------------|
| **0:00–0:15** | Click "Load example idea", then **Launch Project** | *"I have a raw product idea here: a collar that translates dog barks to SMS. I'll hit 'Launch Project'. We're running in stage-safe mode, so performance is smooth and latency is locked down."* |
| **0:15–0:35** | Researcher card lights cyan, text streams, dots pulse | *"First, the Researcher lights up — analyzing the market, identifying competitors, defining personas. It structures its findings and passes them down the pipeline."* |
| **0:35–0:50** | Violet handoff pulse → Strategist → pink Copywriter | *"As the handoff line pulses, the Strategist names our product 'BarkSpeak', picks a modern dark palette and font. Instantly the Copywriter drafts persuasive headlines and an interactive FAQ."* |
| **0:50–1:05** | Emerald Web Builder streams HTML in monospace | *"Now the Web Builder assembles the layout, maps our strategic colors to CSS variables, and builds the grid. Watch the live code stream into the terminal."* |
| **1:05–1:20** | Iframe scales in, confetti bursts, auto-scroll tour | *"And there it is! The sandbox scales into view — a responsive, professional landing page. Brand colors applied, the FAQ accordion works, ready to collect emails."* |

---

## C. Technical Depth to Emphasize to Judges

1. **Asynchronous Pacing Pipe** — the frontend feeds streamed tokens into a
   queue that drains at ~40 chars/sec, so the UI never locks up during fast
   bursts and stays at a cinematic, readable speed.
2. **Structured JSON Handoffs** — agents don't pass loose prose. A backend
   state-machine extracts a strict ` ```json ` payload from each stage and
   validates it with Pydantic, guaranteeing the next agent receives a perfect
   programmatic state representation.
3. **Dynamic CSS Generation** — the Web Builder styles the page from scratch,
   writing CSS custom properties from the Strategist's hex output, so the
   visual result is uniquely branded on every run.
4. **Bulletproof Fallback** — any live API failure flips the affected card to a
   glowing *"API Offline – Using Cached Backup"* badge and the pipeline
   continues seamlessly from cached data. The show never stops.

---

## D. Pre-Flight Checklist

- [ ] `pip install -r requirements.txt`
- [ ] Server running: `uvicorn backend.main:app --port 8000`
- [ ] Browser open at `http://localhost:8000`, zoomed for the room
- [ ] Toggle set to **Stage-Safe Replay**
- [ ] (Optional offline test) airplane mode ON → launch → page still renders
- [ ] Example idea pre-loaded in the input box
