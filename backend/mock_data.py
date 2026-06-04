"""
Cinematic, fully-cached agent outputs for Stage-Safe Replay Mode.

These outputs are pre-written so the entire 4-agent pipeline can run with
ZERO network dependency. The generated landing page (BUILDER_OUTPUT) uses
ONLY system fonts and inline SVGs — no Google Fonts, no external CSS, no
external image URLs — so it renders perfectly offline.
"""

# --------------------------------------------------------------------------
# Agent 1 — Researcher
# --------------------------------------------------------------------------
RESEARCHER_OUTPUT = """# Market Intelligence Report

## 1. TARGET AUDIENCE PROFILE
**Primary persona — "The Devoted Dog Parent"**: Urban & suburban millennials and
Gen-Z (ages 26-42), dual-income, no kids or empty-nesters who treat their dog as
a family member. They spend $1,200+/year on premium pet care and are early
adopters of smart-home and wearable tech.

**Secondary persona — "The Anxious First-Timer"**: New dog owners overwhelmed by
behavioral cues who crave reassurance that they are reading their pet correctly.

Psychographics: emotionally invested, status-aware, gadget-curious, highly active
on Instagram/TikTok pet communities.

## 2. PAIN POINT ANALYSIS
1. **The Communication Gap** — Owners constantly guess what their dog needs
   (hungry? anxious? in pain?) and feel guilty when they get it wrong.
2. **Separation Anxiety Blindspot** — No visibility into how the dog feels while
   home alone, leading to stress for both pet and owner.
3. **Health Signals Missed Early** — Subtle distress vocalizations that hint at
   illness go unnoticed until symptoms are severe.

## 3. COMPETITIVE ANALYSIS
- **Fi Smart Collar** — strong on GPS/activity but offers zero emotional
  translation. We win on personality & communication.
- **Petpuls (bark-emotion analyzer)** — clunky, clinical app with no humor and
  no messaging. We differentiate with delightful, shareable SMS-style output.
- **Generic GPS trackers** — purely logistical; ignore the emotional bond
  entirely.

## 4. UNIQUE VALUE PROPOSITION (UVP)
- **Angle A:** "Finally understand exactly what your dog is saying — in real time."
- **Angle B:** "Turn every bark into a text you'll actually want to screenshot."
- **Angle C:** "AI that closes the emotional gap between you and your best friend."

```json
{
  "target_audience": "Devoted millennial & Gen-Z dog parents who treat their pet as family and adopt smart wearable tech early",
  "pain_points": ["Constantly guessing what their dog needs and feeling guilty when wrong", "No visibility into the dog's emotional state during alone-time", "Missing subtle distress vocalizations that signal early illness"],
  "competitors": ["Fi Smart Collar", "Petpuls bark analyzer"],
  "uvp_angles": ["Understand exactly what your dog is saying in real time", "Turn every bark into a screenshot-worthy text", "AI that closes the emotional gap with your best friend"]
}
```"""

# --------------------------------------------------------------------------
# Agent 2 — Strategist
# --------------------------------------------------------------------------
STRATEGIST_OUTPUT = """# Brand Strategy & Identity Framework

## 1. BRAND NAME
1. **BarkSpeak** — instantly communicates the core function: giving voice to barks.
   Friendly, memorable, app-store friendly. ★ RECOMMENDED
2. **Woofly** — playful and cute, leans heavily into the fun factor.
3. **Tailk** — clever "tail + talk" portmanteau, but harder to say aloud.

**Recommended: BarkSpeak** — the clearest, most trademarkable, and most scalable.

## 2. POSITIONING STATEMENT
*BarkSpeak is the AI-powered smart collar that translates your dog's barks into
real, funny text messages — so devoted dog parents never have to guess what
their best friend is feeling again.*

## 3. TONE OF VOICE
- **Playful** — witty, warm, never clinical.
- **Reassuring** — confident and caring; we reduce owner anxiety.
- **Tech-forward** — smart and credible without jargon.
Write like a clever friend who happens to be a dog-behavior expert.

## 4. VISUAL IDENTITY DIRECTION
- **Color Palette:** Primary indigo, secondary warm coral, deep navy background,
  electric mint accent — modern, high-contrast, and friendly.
- **Typography Vibe:** Clean geometric sans-serif (Outfit / Poppins family).

```json
{
  "selected_brand_name": "BarkSpeak",
  "positioning": "The AI smart collar that translates your dog's barks into real, funny text messages so you never guess what your best friend feels again",
  "tone": ["Playful", "Reassuring", "Tech-forward"],
  "visuals": {
    "primary_color": "#6366F1",
    "secondary_color": "#FB7185",
    "bg_color": "#0F1729",
    "accent_color": "#2DD4BF",
    "font_family": "Outfit"
  }
}
```"""

# --------------------------------------------------------------------------
# Agent 3 — Copywriter
# --------------------------------------------------------------------------
COPYWRITER_OUTPUT = """# BarkSpeak — Website Copy

## 1. HERO SECTION
**Headline:** Your dog has a lot to say. Now you'll actually get the message.
**Subheadline:** BarkSpeak's AI collar translates every bark, whine, and happy
yip into real text messages — delivered straight to your phone.
**CTA:** Reserve Your Collar
**Placeholder:** Enter your email for early access

## 2. BENEFITS
1. **Real-Time Translation** — Hear a bark, read a text. BarkSpeak decodes your
   dog's vocalizations the instant they happen. No more guessing games.
2. **Mood & Wellness Insights** — Spot anxiety, excitement, or early signs of
   discomfort. BarkSpeak watches the patterns so you can act early.
3. **Screenshot-Worthy Moments** — Every translated message is delightfully
   on-brand for your dog. Your group chat will never be the same.

## 3. SOCIAL PROOF
"I got a text that said 'the mailman is BACK and I have concerns.' I've never
felt closer to my dog. BarkSpeak is pure magic." — *Jordan Mills, Golden
Retriever parent*

## 4. FAQ
- Is it comfortable for my dog? Absolutely — lightweight, water-resistant, and
  vet-approved for all-day wear.
- How accurate is the translation? Our AI is trained on millions of canine
  vocalizations and improves the more it learns your dog.
- Do I need a subscription? The collar works out of the box; premium wellness
  insights are an optional add-on.

## 5. FINAL CTA
**Headline:** Start the conversation you've waited your whole life to have.
**CTA:** Reserve Your Collar

```json
{
  "hero": {
    "headline": "Your dog has a lot to say. Now you'll actually get the message.",
    "subheadline": "BarkSpeak's AI collar translates every bark, whine, and happy yip into real text messages — delivered straight to your phone.",
    "cta_text": "Reserve Your Collar",
    "input_placeholder": "Enter your email for early access"
  },
  "features": [
    {"title": "Real-Time Translation", "description": "Hear a bark, read a text. BarkSpeak decodes your dog's vocalizations the instant they happen. No more guessing games.", "icon": "Zap"},
    {"title": "Mood & Wellness Insights", "description": "Spot anxiety, excitement, or early signs of discomfort. BarkSpeak watches the patterns so you can act early.", "icon": "Activity"},
    {"title": "Screenshot-Worthy Moments", "description": "Every translated message is delightfully on-brand for your dog. Your group chat will never be the same.", "icon": "MessageCircle"}
  ],
  "testimonial": {
    "quote": "I got a text that said 'the mailman is BACK and I have concerns.' I've never felt closer to my dog. BarkSpeak is pure magic.",
    "author": "Jordan Mills",
    "role": "Golden Retriever parent"
  },
  "faqs": [
    {"question": "Is it comfortable for my dog?", "answer": "Absolutely — lightweight, water-resistant, and vet-approved for all-day wear."},
    {"question": "How accurate is the translation?", "answer": "Our AI is trained on millions of canine vocalizations and gets sharper the more it learns your dog."},
    {"question": "Do I need a subscription?", "answer": "The collar works out of the box; premium wellness insights are an optional add-on."}
  ],
  "footer": {
    "copyright": "© 2026 BarkSpeak. Made with love for good dogs everywhere."
  }
}
```"""

# --------------------------------------------------------------------------
# Agent 4 — Web Builder (standalone HTML, system fonts + inline SVG only)
# --------------------------------------------------------------------------
BUILDER_OUTPUT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BarkSpeak — Finally Understand Your Dog</title>
<style>
  :root{
    --primary:#6366F1; --secondary:#FB7185; --bg:#0F1729;
    --accent:#2DD4BF; --text:#E5E7EB; --muted:#94A3B8;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    background:var(--bg);color:var(--text);line-height:1.6;overflow-x:hidden}
  .wrap{max-width:1140px;margin:0 auto;padding:0 24px}
  a{color:inherit;text-decoration:none}
  .glow{position:fixed;border-radius:50%;filter:blur(120px);opacity:.4;z-index:0;pointer-events:none}
  .g1{width:500px;height:500px;background:var(--primary);top:-150px;left:-100px}
  .g2{width:500px;height:500px;background:var(--secondary);bottom:-150px;right:-120px}

  nav{position:sticky;top:0;z-index:50;display:flex;align-items:center;justify-content:space-between;
    padding:16px 24px;backdrop-filter:blur(14px);background:rgba(15,23,41,.6);
    border-bottom:1px solid rgba(255,255,255,.08)}
  .logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;letter-spacing:-.02em}
  .logo-badge{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;
    background:linear-gradient(135deg,var(--primary),var(--secondary));color:#fff}
  .nav-cta{padding:9px 18px;border-radius:999px;font-weight:600;font-size:14px;
    background:linear-gradient(135deg,var(--primary),var(--secondary));color:#fff;
    box-shadow:0 4px 18px rgba(99,102,241,.45);transition:transform .15s}
  .nav-cta:hover{transform:translateY(-2px)}

  section{position:relative;z-index:1}
  .hero{text-align:center;padding:96px 0 80px}
  .pill{display:inline-flex;align-items:center;gap:8px;padding:6px 16px;border-radius:999px;
    background:rgba(45,212,191,.12);border:1px solid rgba(45,212,191,.35);
    color:var(--accent);font-size:13px;font-weight:600;margin-bottom:24px}
  .hero h1{font-size:clamp(34px,5.5vw,60px);font-weight:800;line-height:1.08;letter-spacing:-.03em;
    max-width:900px;margin:0 auto 20px;background:linear-gradient(120deg,#fff,#c7d2fe);
    -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
  .hero p{font-size:19px;color:var(--muted);max-width:620px;margin:0 auto 36px}
  .capture{display:flex;gap:10px;max-width:480px;margin:0 auto;flex-wrap:wrap;justify-content:center}
  .capture input{flex:1;min-width:220px;padding:15px 18px;border-radius:14px;
    background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);color:#fff;font-size:15px}
  .capture input::placeholder{color:var(--muted)}
  .capture input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(45,212,191,.2)}
  .btn-primary{padding:15px 28px;border:none;border-radius:14px;font-weight:700;font-size:15px;cursor:pointer;
    color:#fff;background:linear-gradient(135deg,var(--primary),var(--secondary));
    box-shadow:0 8px 26px rgba(99,102,241,.5);transition:transform .15s,box-shadow .25s}
  .btn-primary:hover{transform:translateY(-2px);box-shadow:0 12px 34px rgba(251,113,133,.55)}
  .hint{margin-top:14px;font-size:13px;color:var(--muted)}

  .section-head{text-align:center;margin-bottom:54px}
  .section-head h2{font-size:clamp(28px,4vw,42px);font-weight:800;letter-spacing:-.02em;margin-bottom:12px}
  .section-head p{color:var(--muted);font-size:17px}

  .features{padding:60px 0}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px}
  .card{padding:30px;border-radius:20px;background:rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.08);backdrop-filter:blur(10px);transition:transform .25s,box-shadow .25s}
  .card:hover{transform:translateY(-6px);box-shadow:0 18px 40px rgba(0,0,0,.4);border-color:rgba(99,102,241,.4)}
  .ficon{width:52px;height:52px;border-radius:14px;display:grid;place-items:center;margin-bottom:18px;
    background:linear-gradient(135deg,rgba(99,102,241,.25),rgba(45,212,191,.2));color:var(--accent)}
  .card h3{font-size:20px;font-weight:700;margin-bottom:10px}
  .card p{color:var(--muted);font-size:15px}

  .testimonial{padding:80px 0}
  .quote-card{max-width:760px;margin:0 auto;text-align:center;padding:48px 40px;border-radius:24px;
    background:linear-gradient(135deg,rgba(99,102,241,.12),rgba(251,113,133,.1));
    border:1px solid rgba(255,255,255,.1)}
  .quote-card .q{font-size:24px;font-weight:600;line-height:1.45;margin-bottom:28px;letter-spacing:-.01em}
  .author{display:flex;align-items:center;justify-content:center;gap:14px}
  .avatar{width:54px;height:54px;border-radius:50%;overflow:hidden;flex-shrink:0;
    box-shadow:0 0 0 2px rgba(255,255,255,.15)}
  .author-name{font-weight:700;text-align:left}
  .author-role{color:var(--muted);font-size:14px;text-align:left}

  .faq{padding:60px 0 80px;max-width:760px;margin:0 auto}
  details{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
    border-radius:14px;margin-bottom:14px;padding:4px 4px;overflow:hidden;transition:background .2s}
  details[open]{background:rgba(99,102,241,.08);border-color:rgba(99,102,241,.35)}
  summary{cursor:pointer;list-style:none;padding:18px 22px;font-weight:600;font-size:17px;
    display:flex;justify-content:space-between;align-items:center}
  summary::-webkit-details-marker{display:none}
  summary .chev{transition:transform .25s;color:var(--accent)}
  details[open] summary .chev{transform:rotate(180deg)}
  details p{padding:0 22px 20px;color:var(--muted)}

  .final{text-align:center;padding:90px 0;position:relative}
  .final-card{max-width:820px;margin:0 auto;padding:64px 40px;border-radius:28px;
    background:linear-gradient(135deg,var(--primary),var(--secondary));position:relative;overflow:hidden}
  .final-card h2{font-size:clamp(28px,4vw,44px);font-weight:800;color:#fff;margin-bottom:14px;letter-spacing:-.02em}
  .final-card p{color:rgba(255,255,255,.85);font-size:18px;margin-bottom:30px}
  .final-card .btn-primary{background:#fff;color:var(--primary)}

  footer{border-top:1px solid rgba(255,255,255,.08);padding:40px 0;text-align:center}
  .footer-links{display:flex;gap:26px;justify-content:center;flex-wrap:wrap;margin-bottom:18px}
  .footer-links a{color:var(--muted);font-size:14px;transition:color .2s}
  .footer-links a:hover{color:var(--text)}
  .copyright{color:var(--muted);font-size:13px}

  .toast{position:fixed;bottom:24px;left:50%;transform:translate(-50%,80px);z-index:100;
    background:var(--accent);color:#062925;font-weight:700;padding:14px 26px;border-radius:999px;
    box-shadow:0 10px 30px rgba(45,212,191,.5);opacity:0;transition:transform .4s,opacity .4s}
  .toast.show{transform:translate(-50%,0);opacity:1}
</style>
</head>
<body>
<div class="glow g1"></div><div class="glow g2"></div>

<nav>
  <div class="logo">
    <span class="logo-badge">
      <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91 0z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/></svg>
    </span>
    BarkSpeak
  </div>
  <a href="#reserve" class="nav-cta">Reserve Your Collar</a>
</nav>

<section class="hero wrap">
  <span class="pill">🐾 Now in early access</span>
  <h1>Your dog has a lot to say. Now you'll actually get the message.</h1>
  <p>BarkSpeak's AI collar translates every bark, whine, and happy yip into real text messages — delivered straight to your phone.</p>
  <form class="capture" onsubmit="reserve(event)">
    <input type="email" placeholder="Enter your email for early access" required>
    <button class="btn-primary" type="submit">Reserve Your Collar</button>
  </form>
  <p class="hint">Join 12,000+ dog parents already on the waitlist.</p>
</section>

<section class="features wrap">
  <div class="section-head">
    <h2>Built to close the communication gap</h2>
    <p>Smart hardware, delightful software, and an AI that truly knows your dog.</p>
  </div>
  <div class="grid">
    <div class="card">
      <div class="ficon"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg></div>
      <h3>Real-Time Translation</h3>
      <p>Hear a bark, read a text. BarkSpeak decodes your dog's vocalizations the instant they happen. No more guessing games.</p>
    </div>
    <div class="card">
      <div class="ficon"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div>
      <h3>Mood &amp; Wellness Insights</h3>
      <p>Spot anxiety, excitement, or early signs of discomfort. BarkSpeak watches the patterns so you can act early.</p>
    </div>
    <div class="card">
      <div class="ficon"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg></div>
      <h3>Screenshot-Worthy Moments</h3>
      <p>Every translated message is delightfully on-brand for your dog. Your group chat will never be the same.</p>
    </div>
  </div>
</section>

<section class="testimonial wrap">
  <div class="quote-card">
    <p class="q">"I got a text that said 'the mailman is BACK and I have concerns.' I've never felt closer to my dog. BarkSpeak is pure magic."</p>
    <div class="author">
      <div class="avatar">
        <svg viewBox="0 0 54 54" width="54" height="54"><defs><linearGradient id="av" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6366F1"/><stop offset="1" stop-color="#FB7185"/></linearGradient></defs><rect width="54" height="54" fill="url(#av)"/><circle cx="27" cy="21" r="9" fill="rgba(255,255,255,.85)"/><path d="M9 50c0-10 8-16 18-16s18 6 18 16z" fill="rgba(255,255,255,.85)"/></svg>
      </div>
      <div>
        <div class="author-name">Jordan Mills</div>
        <div class="author-role">Golden Retriever parent</div>
      </div>
    </div>
  </div>
</section>

<section class="faq wrap">
  <div class="section-head">
    <h2>Questions, answered</h2>
    <p>Everything you need to know before your dog starts texting.</p>
  </div>
  <details open>
    <summary>Is it comfortable for my dog?<span class="chev">▾</span></summary>
    <p>Absolutely — lightweight, water-resistant, and vet-approved for all-day wear.</p>
  </details>
  <details>
    <summary>How accurate is the translation?<span class="chev">▾</span></summary>
    <p>Our AI is trained on millions of canine vocalizations and gets sharper the more it learns your dog.</p>
  </details>
  <details>
    <summary>Do I need a subscription?<span class="chev">▾</span></summary>
    <p>The collar works out of the box; premium wellness insights are an optional add-on.</p>
  </details>
</section>

<section class="final wrap" id="reserve">
  <div class="final-card">
    <h2>Start the conversation you've waited your whole life to have.</h2>
    <p>Reserve your BarkSpeak collar today and be first in line when we ship.</p>
    <button class="btn-primary" onclick="reserve(event)">Reserve Your Collar</button>
  </div>
</section>

<footer>
  <div class="footer-links">
    <a href="#">Product</a><a href="#">How it works</a><a href="#">Support</a><a href="#">Privacy</a>
  </div>
  <p class="copyright">© 2026 BarkSpeak. Made with love for good dogs everywhere.</p>
</footer>

<div class="toast" id="toast">🎉 You're on the list! Check your inbox.</div>
<script>
  function reserve(e){e.preventDefault();var t=document.getElementById('toast');
    t.classList.add('show');setTimeout(function(){t.classList.remove('show')},3200);}
</script>
</body>
</html>"""


# Convenience map consumed by the orchestrator during Replay Mode.
MOCK_OUTPUTS = {
    "researcher": RESEARCHER_OUTPUT,
    "strategist": STRATEGIST_OUTPUT,
    "copywriter": COPYWRITER_OUTPUT,
    "builder": BUILDER_OUTPUT,
}
