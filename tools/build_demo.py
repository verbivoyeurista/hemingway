#!/usr/bin/env python3
"""Build the Hemingway compositional demo surface.

Reads ~/hemingway/library/generated_demo.json and emits a single self-contained
HTML at ~/hemingway/tools/demo.html (works over file://).

The demo is a CONTROLLED ABLATION, not a live competitor: same facts, three
stacked layers — Neutral (no knowledge base) -> +Voice (who Venmo is, HELD across
audiences) -> +Tone (how Venmo flexes, DIVERGES). The +voice row being identical
while the +tone row splits is the entire visual argument: voice held, tone flexed.
"""
import json, os, html

HOME = os.path.expanduser("~")
IN = f"{HOME}/hemingway/library/generated_demo.json"
OUT = f"{HOME}/hemingway/tools/demo.html"

D = json.load(open(IN))


def esc(s):
    return html.escape(s or "")


def variant_html(v):
    tells = "".join(f"<li>{esc(t)}</li>" for t in v.get("tells", []))
    star = " star" if "★" in v.get("label", "") else ""
    return f"""<div class="var{star}">
      <div class="vhd"><span class="vlab">{esc(v['label'])}</span><span class="badge tone-{esc(v['tone'])}">{esc(v['tone'])}</span></div>
      <div class="copy">{esc(v['copy'])}</div>
      <ul class="tells">{tells}</ul>
    </div>"""


def event_html(ev):
    hero = " hero" if ev.get("hero") else ""
    axis = ev.get("flex_axis", "")
    axis_lab = "flexes by audience" if axis == "audience" else "flexes by framing"
    variants = "".join(variant_html(v) for v in ev["variants"])
    return f"""<section class="ev{hero}">
  <div class="evhd">
    <span class="name">{esc(ev['label'])}</span>
    <span class="axis">{esc(axis_lab)}</span>
  </div>
  <div class="facts"><span class="k">the facts</span>{esc(ev['facts'])}</div>

  <div class="stage neutral">
    <div class="stagelab">neutral <span class="tag">no knowledge base</span></div>
    <div class="copy">{esc(ev['neutral'])}</div>
  </div>
  <div class="down">+ voice</div>
  <div class="stage voice">
    <div class="stagelab">+ voice <span class="tag held">held — identical for both</span></div>
    <div class="copy">{esc(ev['voice'])}</div>
  </div>
  <div class="down">+ tone</div>
  <div class="stage tone">
    <div class="stagelab">+ tone <span class="tag flexed">flexed — diverges</span></div>
    <div class="variants">{variants}</div>
  </div>

  <div class="flexnote">{esc(ev['flex_note'])}</div>
</section>"""


BODY = "\n".join(event_html(e) for e in D["events"])
meta = D["meta"]

PAGE = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hemingway · compositional demo</title>
<style>
  :root{{--bg:#0f1117;--panel:#171a23;--panel2:#1d212c;--line:#2a2f3d;--ink:#e7e9ee;--dim:#9aa1b1;
        --teen:#7c5cff;--parent:#2bb3a3;--gold:#f4c04d;--muted:#6b7280;--accent:#7c5cff;}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
  header{{padding:34px 26px 10px;max-width:1040px;margin:0 auto}}
  header h1{{font-size:23px;margin:0 0 8px;letter-spacing:.2px}}
  header .thesis{{color:var(--dim);font-size:14.5px;max-width:800px}}
  header .thesis b{{color:var(--ink)}}
  .legend{{max-width:1040px;margin:14px auto 0;padding:0 26px;display:flex;gap:10px;flex-wrap:wrap;font-size:12px;color:var(--dim)}}
  .legend span{{border:1px solid var(--line);border-radius:20px;padding:4px 11px}}
  .legend .held{{border-color:#3a4a6b;color:#9db4e0}}
  .legend .flexed{{border-color:#6b4b1f;color:var(--gold)}}
  main{{max-width:1040px;margin:0 auto;padding:18px 26px 100px}}
  .ev{{background:var(--panel);border:1px solid var(--line);border-radius:16px;margin:20px 0;padding:20px 22px}}
  .ev.hero{{border-color:#4a3f7a;box-shadow:0 0 0 1px #4a3f7a, 0 8px 40px -18px #7c5cff88}}
  .evhd{{display:flex;align-items:baseline;gap:12px;margin-bottom:6px}}
  .evhd .name{{font-size:17px;font-weight:650}}
  .evhd .axis{{font-size:11.5px;color:var(--dim);text-transform:uppercase;letter-spacing:.5px}}
  .facts{{color:#cbd0dc;font-size:13.5px;margin:6px 0 16px;padding:10px 12px;background:#12141c;border-radius:9px;border:1px solid var(--line)}}
  .facts .k{{display:block;font-size:10px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);margin-bottom:3px}}
  .stage{{border-radius:11px;padding:13px 15px;border:1px solid var(--line)}}
  .stage.neutral{{background:#14161d;opacity:.82}}
  .stage.neutral .copy{{color:#aab; font-style:italic}}
  .stage.voice{{background:#161a26;border-color:#33406b}}
  .stage.tone{{background:#161a26;border-color:#5a4a2a}}
  .stagelab{{font-size:11px;text-transform:uppercase;letter-spacing:.6px;color:var(--dim);margin-bottom:7px;display:flex;align-items:center;gap:8px}}
  .tag{{font-size:10px;letter-spacing:.3px;padding:2px 7px;border-radius:20px;border:1px solid var(--line);color:var(--muted);text-transform:none}}
  .tag.held{{border-color:#3a4a6b;color:#9db4e0}}
  .tag.flexed{{border-color:#6b4b1f;color:var(--gold)}}
  .copy{{font-size:15px;line-height:1.5}}
  .down{{text-align:center;color:var(--muted);font-size:11px;letter-spacing:.5px;padding:7px 0;text-transform:uppercase}}
  .variants{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:4px}}
  .var{{background:#12141c;border:1px solid var(--line);border-radius:9px;padding:12px 13px}}
  .var.star{{border-color:var(--gold)}}
  .vhd{{display:flex;align-items:center;justify-content:space-between;margin-bottom:7px}}
  .vlab{{font-size:12px;font-weight:600;color:var(--dim)}}
  .badge{{font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;padding:2px 8px;border-radius:20px}}
  .tone-calm{{background:#123330;color:#7fe0d3;border:1px solid #1d5a52}}
  .tone-playful{{background:#241d43;color:#b9a7ff;border:1px solid #3a2f6b}}
  .var .copy{{font-size:14px}}
  .tells{{margin:9px 0 0;padding-left:16px;color:var(--dim);font-size:11.5px;line-height:1.5}}
  .tells li{{margin:1px 0}}
  .flexnote{{margin-top:15px;padding:11px 14px;background:#12141c;border-left:3px solid var(--accent);border-radius:0 8px 8px 0;font-size:13px;color:#cdd3e0}}
  footer{{max-width:1040px;margin:0 auto;padding:0 26px 60px;color:var(--muted);font-size:11.5px}}
  @media(max-width:720px){{.variants{{grid-template-columns:1fr}}}}
</style></head><body>
<header>
  <h1>Hemingway — same facts, watch what the knowledge adds</h1>
  <p class="thesis">{esc(meta['thesis'])}</p>
</header>
<div class="legend">
  <span>neutral = knowledge base <b>out of the room</b></span>
  <span class="held">+ voice = who Venmo is · <b>held</b></span>
  <span class="flexed">+ tone = how Venmo flexes · <b>diverges</b></span>
</div>
<main>
{BODY}
</main>
<footer>
  voice: {esc(meta['voice_source'])} · tone: {esc(meta['tone_source'])} — controlled ablation, not a live competitor.
</footer>
</body></html>"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write(PAGE)
print(f"wrote {OUT}  ({len(PAGE)} bytes)  events: {len(D['events'])}")
