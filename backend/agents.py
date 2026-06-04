"""
LLM agent definitions for LaunchPad AI.

Contains the verbatim system prompts, Pydantic handoff schemas, the
JSONStreamExtractor state machine, and a streaming wrapper around litellm that
gracefully degrades to cached mock data on any failure.
"""
from __future__ import annotations

import json
import re
import os
from typing import AsyncGenerator, List, Optional

from pydantic import BaseModel, ValidationError

from .mock_data import MOCK_OUTPUTS

# ==========================================================================
# 1. Verbatim system prompts
# ==========================================================================
RESEARCHER_PROMPT = """You are an elite Market Researcher AI. Your task is to analyze a new product idea and provide actionable, deep market intelligence.

Given a single-sentence product idea, produce a detailed markdown report containing:
1. TARGET AUDIENCE PROFILE: Define the primary and secondary buyer personas, their demographics, and core psychographics.
2. PAIN POINT ANALYSIS: Detail the 3 biggest pain points this audience experiences that this product solves.
3. COMPETITIVE ANALYSIS: Identify 2-3 existing competitors or alternatives and explain how this product can differentiate.
4. UNIQUE VALUE PROPOSITION (UVP): Brainstorm three key angles for a UVP.

At the very end of your response, output a raw JSON block wrapped in ```json ... ``` containing:
{
  "target_audience": "Short description of core persona",
  "pain_points": ["Pain point 1", "Pain point 2", "Pain point 3"],
  "competitors": ["Competitor A", "Competitor B"],
  "uvp_angles": ["Angle 1", "Angle 2", "Angle 3"]
}
Ensure your analysis is highly specific and realistic. Avoid vague buzzwords."""

STRATEGIST_PROMPT = """You are a world-class Brand Strategist AI. You translate raw market research into a cohesive brand identity and positioning framework.

You will receive Research Notes. Review the target audience, pain points, and UVP angles. Establish:
1. BRAND NAME: Create 3 strong, catchy, and relevant brand name suggestions with rationale. Pick ONE as the recommended name.
2. POSITIONING STATEMENT: A clear, memorable one-liner of what the brand does, for whom, and why it matters.
3. TONE OF VOICE Guidelines: Select 3 adjectives (e.g., Bold, Friendly, Tech-forward) with instructions on how to write for this brand.
4. VISUAL IDENTITY DIRECTION:
   - Recommended Color Palette: A primary color, secondary color, dark background color, and accent color (hex codes).
   - Typography Vibe: Font recommendations (e.g., sans-serif, serif, modern tech) using Google Fonts imports.

At the very end of your response, output a raw JSON block wrapped in ```json ... ``` containing:
{
  "selected_brand_name": "Recommended Brand Name",
  "positioning": "Core brand positioning statement",
  "tone": ["Tone adjective 1", "Tone adjective 2", "Tone adjective 3"],
  "visuals": {
    "primary_color": "#HEX",
    "secondary_color": "#HEX",
    "bg_color": "#HEX",
    "accent_color": "#HEX",
    "font_family": "FontName"
  }
}
Ensure the hex codes are harmonized, high-contrast, and modern (avoid basic black, white, red, green)."""

COPYWRITER_PROMPT = """You are an expert Direct Response Copywriter AI. Your job is to take a brand strategy and translate it into high-converting website copy.

You will receive a Brand Strategy Brief. Write copy for the following sections:
1. HERO SECTION: A compelling Headline, Subheadline, CTA Button text, and input placeholder (e.g. for newsletter/beta).
2. BENEFITS SECTION: 3 distinct features or benefit cards. Each must have: a Title, a 2-sentence description, and an SVG icon concept (e.g., "Shield", "Zap", "Layers").
3. SOCIAL PROOF / TESTIMONIAL: One highly realistic testimonial with an author name, title, and quote.
4. ACCORDION FAQ: 3 frequently asked questions with highly reassuring, concise answers.
5. FINAL CALL TO ACTION: A short headline and CTA text.

At the very end of your response, output a raw JSON block wrapped in ```json ... ``` containing:
{
  "hero": {
    "headline": "...",
    "subheadline": "...",
    "cta_text": "...",
    "input_placeholder": "..."
  },
  "features": [
    {"title": "...", "description": "...", "icon": "..."}
  ],
  "testimonial": {
    "quote": "...",
    "author": "...",
    "role": "..."
  },
  "faqs": [
    {"question": "...", "answer": "..."}
  ],
  "footer": {
    "copyright": "..."
  }
}
The copywriting should match the tone guidelines exactly. Write copy that feels alive, benefits-driven, and punchy."""

BUILDER_PROMPT = """You are a Senior Frontend Engineer and UI/UX Designer AI. Your task is to write a single-file, highly-responsive landing page using the provided copy, branding colors, typography, and strategy brief.

STRICT OUTPUT GUIDELINE:
- You must output ONLY valid, raw, complete HTML code.
- Do NOT wrap your output in ```html ... ``` or any other markdown wrappers.
- Do NOT include any conversational introduction, explanation, or notes.
- Start immediately with `<!DOCTYPE html>` and end with `</html>`.

DESIGN GUIDELINES (To ensure a premium "wow-factor" design):
- Headings/Fonts: Import the recommended font family from Google Fonts inside the `<head>`.
- Color Palette: Map the selected brand colors to CSS custom properties (variables) like `--primary`, `--secondary`, `--bg`, `--accent`, `--text`. Use them consistently.
- Layout: Create a clean, modern grid/flexbox layout. Use generous spacing (padding/margins) to let elements breathe.
- Aesthetic Details: Include modern design cues:
  - Glassmorphism effects (e.g., `backdrop-filter: blur(10px); background: rgba(255,255,255,0.05);` for headers or cards).
  - Subtle gradients and background shapes.
  - Smooth hover transitions on all buttons and cards (e.g., scale up, shadow glow).
  - Dark mode styling using the Strategist's background color as the body background.
- Components to Implement:
  - Sticky navigation bar with Logo (the selected brand name) and CTA.
  - Hero Section: Large typography, input field + CTA button with glow, mock interactive email capture.
  - Feature Grid: 3 cards utilizing SVG icons (inline SVG or modern system fonts, do not use external image links that can fail).
  - Testimonial Section: Centered, elegant layout with quote styling and author image placeholder (using a beautiful geometric SVG pattern instead of broken image URLs).
  - FAQ Accordion: Working interactive accordion using pure HTML `<details>` and `<summary>` styled beautifully.
  - Final CTA Section: Centered, high-conversion section.
  - Footer: Navigation links and copyright.

Ensure the HTML runs completely standalone. All CSS must be inline in a `<style>` block. All interactivity (like active states, FAQ transitions, or submission feedback) must be styled or handled with a tiny inline `<script>` at the bottom of the page."""

AGENT_PROMPTS = {
    "researcher": RESEARCHER_PROMPT,
    "strategist": STRATEGIST_PROMPT,
    "copywriter": COPYWRITER_PROMPT,
    "builder": BUILDER_PROMPT,
}

# Ordered pipeline definition (id, display name, accent).
PIPELINE = [
    {"id": "researcher", "name": "Researcher", "accent": "#06B6D4"},
    {"id": "strategist", "name": "Strategist", "accent": "#8B5CF6"},
    {"id": "copywriter", "name": "Copywriter", "accent": "#EC4899"},
    {"id": "builder", "name": "Web Builder", "accent": "#10B981"},
]


# ==========================================================================
# 2. Pydantic handoff schemas
# ==========================================================================
class ResearchData(BaseModel):
    target_audience: str
    pain_points: List[str]
    competitors: List[str]
    uvp_angles: List[str]


class VisualData(BaseModel):
    primary_color: str
    secondary_color: str
    bg_color: str
    accent_color: str
    font_family: str


class StrategyData(BaseModel):
    selected_brand_name: str
    positioning: str
    tone: List[str]
    visuals: VisualData


class FeatureItem(BaseModel):
    title: str
    description: str
    icon: str


class TestimonialData(BaseModel):
    quote: str
    author: str
    role: str


class FaqItem(BaseModel):
    question: str
    answer: str


class CopyData(BaseModel):
    hero: dict
    features: List[FeatureItem]
    testimonial: TestimonialData
    faqs: List[FaqItem]
    footer: dict


SCHEMA_BY_AGENT = {
    "researcher": ResearchData,
    "strategist": StrategyData,
    "copywriter": CopyData,
    "builder": None,  # builder returns raw HTML, no JSON handoff
}


# ==========================================================================
# 3. JSON extraction state machine
# ==========================================================================
class JSONStreamExtractor:
    """Accumulates a streamed markdown response and pulls the trailing
    ```json ... ``` block once the full text is available. Designed to be fed
    chunks incrementally; it never raises while streaming."""

    def __init__(self):
        self.in_json_block = False
        self.full_text: List[str] = []

    def process_chunk(self, chunk: str) -> str:
        """Record a chunk and return it unchanged for pass-through display."""
        self.full_text.append(chunk)
        if not self.in_json_block and "```json" in "".join(self.full_text):
            self.in_json_block = True
        return chunk

    def get_text(self) -> str:
        return "".join(self.full_text)

    def extract_json(self) -> Optional[dict]:
        """Parse the last ```json fenced block from the accumulated text.
        Falls back to a brace-matching regex if the fence is malformed."""
        text = self.get_text()

        # Preferred: explicit ```json ... ``` fence (take the LAST one).
        matches = re.findall(r"```json\s*(.*?)```", text, re.DOTALL)
        candidates = list(matches)

        # Fallback: any ``` ... ``` fence.
        if not candidates:
            candidates = re.findall(r"```\s*(\{.*?\})\s*```", text, re.DOTALL)

        # Last-resort fallback: greedy outermost { ... }.
        if not candidates:
            brace = re.search(r"\{.*\}", text, re.DOTALL)
            if brace:
                candidates = [brace.group(0)]

        for raw in reversed(candidates):
            raw = raw.strip()
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                # Tolerate trailing commas, a common LLM artifact.
                cleaned = re.sub(r",(\s*[}\]])", r"\1", raw)
                try:
                    return json.loads(cleaned)
                except json.JSONDecodeError:
                    continue
        return None


def validate_handoff(agent_id: str, data: Optional[dict]):
    """Validate extracted JSON against the agent's Pydantic schema.
    Returns (validated_dict_or_None, error_str_or_None)."""
    schema = SCHEMA_BY_AGENT.get(agent_id)
    if schema is None or data is None:
        return data, None
    try:
        return schema(**data).model_dump(), None
    except ValidationError as exc:
        return data, str(exc)


# ==========================================================================
# 4. Prompt assembly — feed prior structured handoffs into each agent
# ==========================================================================
def build_user_message(agent_id: str, idea: str, context: dict) -> str:
    if agent_id == "researcher":
        return f"Product idea: {idea}"
    if agent_id == "strategist":
        return (
            f"Original product idea: {idea}\n\n"
            f"Research Notes (structured):\n"
            f"{json.dumps(context.get('researcher', {}), indent=2)}"
        )
    if agent_id == "copywriter":
        return (
            f"Original product idea: {idea}\n\n"
            f"Brand Strategy Brief (structured):\n"
            f"{json.dumps(context.get('strategist', {}), indent=2)}"
        )
    if agent_id == "builder":
        return (
            f"Original product idea: {idea}\n\n"
            f"Brand Strategy (colors, fonts, name):\n"
            f"{json.dumps(context.get('strategist', {}), indent=2)}\n\n"
            f"Website Copy:\n"
            f"{json.dumps(context.get('copywriter', {}), indent=2)}"
        )
    return idea


# ==========================================================================
# 5. Streaming LLM call (with graceful offline fallback)
# ==========================================================================
DEFAULT_MODEL = os.getenv("LLM_MODEL", "anthropic/claude-3-5-sonnet-20241022")


async def stream_agent(
    agent_id: str, idea: str, context: dict, model: str = DEFAULT_MODEL
) -> AsyncGenerator[dict, None]:
    """Yields dicts: {"type": "token", "text": ...} chunks, then either
    {"type": "fallback"} (if the API failed mid-flight) before tokens of the
    cached output, and always ends having accumulated full text in caller.

    The caller is responsible for pacing/queueing tokens to the UI.
    """
    system = AGENT_PROMPTS[agent_id]
    user = build_user_message(agent_id, idea, context)

    try:
        from litellm import acompletion

        response = await acompletion(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            stream=True,
            timeout=45,
        )
        got_any = False
        async for part in response:
            delta = part.choices[0].delta
            token = getattr(delta, "content", None)
            if token:
                got_any = True
                yield {"type": "token", "text": token}
        if not got_any:
            raise RuntimeError("Empty stream from LLM")
    except Exception as exc:  # noqa: BLE001 — any failure → graceful fallback
        # Signal the UI to show the warning badge, then replay cached output.
        yield {"type": "fallback", "error": str(exc)}
        for token in _chunk_text(MOCK_OUTPUTS[agent_id]):
            yield {"type": "token", "text": token}


def _chunk_text(text: str, size: int = 6):
    """Split cached text into small chunks to mimic token streaming."""
    for i in range(0, len(text), size):
        yield text[i : i + size]
