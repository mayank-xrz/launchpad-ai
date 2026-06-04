"""
LaunchPad AI — FastAPI server.

Serves the static cinematic frontend and exposes a WebSocket that orchestrates
the 4-agent pipeline (Researcher → Strategist → Copywriter → Web Builder),
streaming tokens and lifecycle events to the browser.

WebSocket protocol (server → client):
  {"type": "pipeline_start"}
  {"type": "agent_start",  "agent": "researcher"}
  {"type": "token",        "agent": "researcher", "text": "..."}
  {"type": "fallback",     "agent": "researcher"}            # API failed, using cache
  {"type": "agent_done",   "agent": "researcher", "data": {...}, "valid": true}
  {"type": "handoff",      "from": "researcher", "to": "strategist"}
  {"type": "render",       "html": "<!DOCTYPE html>..."}     # builder result
  {"type": "pipeline_done"}
  {"type": "error",        "message": "..."}

Client → server:
  {"idea": "...", "mode": "replay" | "live", "model": "optional/model"}
"""
from __future__ import annotations

import asyncio
import os
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .agents import (
    PIPELINE,
    JSONStreamExtractor,
    stream_agent,
    validate_handoff,
)
from .mock_data import MOCK_OUTPUTS

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(title="LaunchPad AI")


@app.get("/")
async def index():
    return FileResponse(FRONTEND_DIR / "index.html")


# ---- Replay-mode pacing (server-side artificial delay) -------------------
REPLAY_CHUNK = 6           # characters per emitted chunk
REPLAY_DELAY = 0.020       # seconds between chunks; tuned so the full 4-agent
                           # run lands in the ~60-75s stage window


async def run_replay(ws: WebSocket, idea: str):
    """Stream the cached outputs token-by-token, fully offline."""
    await ws.send_json({"type": "pipeline_start"})
    context: dict = {}

    for idx, agent in enumerate(PIPELINE):
        aid = agent["id"]
        await ws.send_json({"type": "agent_start", "agent": aid})
        await asyncio.sleep(0.4)  # brief "thinking" beat

        extractor = JSONStreamExtractor()
        text = MOCK_OUTPUTS[aid]
        for i in range(0, len(text), REPLAY_CHUNK):
            chunk = text[i : i + REPLAY_CHUNK]
            extractor.process_chunk(chunk)
            await ws.send_json({"type": "token", "agent": aid, "text": chunk})
            await asyncio.sleep(REPLAY_DELAY)

        await _finish_agent(ws, aid, extractor, context)

        if idx < len(PIPELINE) - 1:
            await ws.send_json(
                {"type": "handoff", "from": aid, "to": PIPELINE[idx + 1]["id"]}
            )
            await asyncio.sleep(0.6)

    await ws.send_json({"type": "render", "html": MOCK_OUTPUTS["builder"]})
    await ws.send_json({"type": "pipeline_done"})


async def run_live(ws: WebSocket, idea: str, model: str | None):
    """Stream live LLM output, falling back to cache per-agent on failure."""
    await ws.send_json({"type": "pipeline_start"})
    context: dict = {}
    kwargs = {"model": model} if model else {}

    for idx, agent in enumerate(PIPELINE):
        aid = agent["id"]
        await ws.send_json({"type": "agent_start", "agent": aid})

        extractor = JSONStreamExtractor()
        async for event in stream_agent(aid, idea, context, **kwargs):
            if event["type"] == "fallback":
                await ws.send_json({"type": "fallback", "agent": aid})
            elif event["type"] == "token":
                extractor.process_chunk(event["text"])
                await ws.send_json(
                    {"type": "token", "agent": aid, "text": event["text"]}
                )

        await _finish_agent(ws, aid, extractor, context)

        if idx < len(PIPELINE) - 1:
            await ws.send_json(
                {"type": "handoff", "from": aid, "to": PIPELINE[idx + 1]["id"]}
            )

    html = context.get("builder_html") or MOCK_OUTPUTS["builder"]
    await ws.send_json({"type": "render", "html": html})
    await ws.send_json({"type": "pipeline_done"})


async def _finish_agent(ws, aid, extractor, context):
    """Common completion logic: extract/validate JSON handoff (or capture HTML)."""
    if aid == "builder":
        html = extractor.get_text().strip()
        # Strip accidental markdown fences if the model added them.
        if html.startswith("```"):
            html = html.split("```", 2)[-1] if "```" in html else html
            html = html.replace("html", "", 1).strip("` \n")
        context["builder_html"] = html
        await ws.send_json({"type": "agent_done", "agent": aid, "valid": True})
        return

    raw = extractor.extract_json()
    data, err = validate_handoff(aid, raw)
    context[aid] = data or {}
    await ws.send_json(
        {"type": "agent_done", "agent": aid, "data": data, "valid": err is None}
    )


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        payload = await ws.receive_json()
        idea = (payload.get("idea") or "").strip()
        mode = payload.get("mode", "replay")
        model = payload.get("model")

        if not idea:
            idea = "A smart dog collar that translates barks into funny text messages using AI."

        if mode == "live":
            await run_live(ws, idea, model)
        else:
            await run_replay(ws, idea)

    except WebSocketDisconnect:
        return
    except Exception as exc:  # noqa: BLE001
        try:
            await ws.send_json({"type": "error", "message": str(exc)})
        except Exception:
            pass


# Mount static assets LAST so "/" and "/ws" take precedence.
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=bool(os.getenv("DEV")),
    )
