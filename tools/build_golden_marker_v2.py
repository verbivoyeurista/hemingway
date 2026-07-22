#!/usr/bin/env python3
"""Rebuild the golden-set marker as the RECONCILED view (post 2026-07-18 ruling).

Reseeds from the existing marks in ~/hemingway/library/golden_set.json (NOT the
raw corpora) so Brittney's authorship carries over, then migrates each side to the
ruled 5-handle palette:

    intent (scrubbed) · signal (6) · recipient · actor · severity

Changes vs v1:
  - `tone` (playful/calm/neutral) is no longer an input chip -> shown read-only as
    the MEASURED OUTPUT (the dependent variable the golden set exists to measure).
  - `role` split into `recipient` (from column) + `actor` (derived from copy).
  - `stakes` -> `severity` (coarse). `signal` expanded to the canonical 6.
  - intent values scrubbed: inform->confirm/alert, request->invite, reassure DROPPED.
  - `reassure` was misfiled; where present, an in-cell note flags it relocating to
    trust_calibration (tracked-missing, not wired).
  - `trust_calibration` + `state_transition` rendered as greyed PENDING groups so the
    gaps are visible in place, but non-interactive (not part of the palette).

New localStorage key + new output file so v1 marks/state are untouched.
"""
import json, os, re, html

HOME = os.path.expanduser("~")
IN = f"{HOME}/hemingway/library/golden_set.json"
OUT = f"{HOME}/hemingway/tools/golden_marker_v2.html"

PALETTE = {
    "intent":    ["confirm", "alert", "celebrate", "instruct", "invite", "warn", "protect"],
    "signal":    ["milestone", "update", "needs_action", "urgent", "onboarding", "monitoring"],
    "recipient": ["teen", "parent"],
    "actor":     ["parent", "teen", "system"],
    "priority":  ["low", "medium", "high"],
}
# NOTE: recipient is teen/parent for THIS set. Deferred hierarchical model:
# a parent IS an account_holder, a teen account is a sub-account; observer = later.
PENDING = {
    "trust_calibration · pending — not wired": ["build", "reassure", "repair", "protect", "mark_milestone"],
    "state_transition · pending — earned by data": ["gain", "neutral", "lose"],
}


def derive_actor(copy, side):
    txt = " ".join((copy.get(k) or "") for k in ("subject", "preheader", "hero", "body"))
    if re.search(r"\bYou (locked|unlocked|canceled|changed|added|activated)\b", txt):
        return side                # "you" = the reader = this email's recipient (parent or teen)
    if re.search(r"\b(?!You\b)[A-Z][a-z]+ (locked|unlocked|changed|canceled|activated)\b", txt):
        return "parent"            # a named guardian acted -- the guardian IS the parent
    return "system"                # no user acted (age restriction, system ship, etc.)


def migrate(side_key, facets, copy, event):
    f = set(facets)
    out = [side_key, derive_actor(copy, side_key)]  # recipient (column), actor (who acted)
    if "celebrate" in f: out.append("celebrate")
    if "instruct" in f: out.append("instruct")
    if "alert" in f: out.append("alert")
    if "request" in f: out.append("invite")
    if "inform" in f and "alert" not in f: out.append("confirm")
    if "milestone" in f: out.append("milestone")
    if "update" in f: out.append("update")
    if "onboarding" in f: out.append("onboarding")
    if "needs-action" in f: out.append("urgent" if event == "account_restricted" else "needs_action")
    out.append("high" if "high-stakes" in f else "low")   # priority (coarse; medium reserved)
    return out


def tone_out(facets):
    for t in ("playful", "calm", "neutral"):
        if t in facets:
            return t
    return ""


src = json.load(open(IN))
events = []
for ev in src["events"]:
    row = {"event": ev["event"], "label": ev.get("label", ev["event"])}
    for side in ("teen", "parent"):
        s = ev.get(side, {}) or {}
        copy = s.get("copy", {}) or {}
        facets = s.get("facets", [])
        golden = True if s.get("golden") else (False if s.get("excluded") else None)
        row[side] = {
            "subject": copy.get("subject", ""), "preheader": copy.get("preheader", ""),
            "hero": copy.get("hero", ""), "body": copy.get("body", ""),
            "src": s.get("source", ""),
            "tone": tone_out(facets),
            "mignote": "‘reassure’ → trust_calibration (tracked, pending)" if "reassure" in facets else "",
            "seed": {"golden": golden, "facets": migrate(side, facets, copy, ev["event"]),
                     "closer": s.get("closer", ""), "why": s.get("why", "")},
        }
    events.append(row)

payload = {"palette": PALETTE, "pending": PENDING, "events": events,
           "meta": {"teen_source": src.get("teen_source", ""), "parent_source": src.get("parent_source", ""),
                    "note": "Reconciled view. Reseeded from your marks + migrated to the ruled palette."}}

TPL = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hemingway · Golden-set marker (reconciled)</title>
<style>
  :root{--bg:#0f1117;--panel:#171a23;--panel2:#1d212c;--line:#2a2f3d;--ink:#e7e9ee;--dim:#9aa1b1;
        --teen:#7c5cff;--parent:#2bb3a3;--gold:#f4c04d;--out:#4b5163;--accent:#7c5cff;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
  header{position:sticky;top:0;z-index:10;background:linear-gradient(180deg,#12141c,#12141cf2);
         border-bottom:1px solid var(--line);padding:14px 22px;display:flex;align-items:center;gap:18px}
  header h1{font-size:16px;margin:0;font-weight:650;letter-spacing:.2px}
  header .sub{color:var(--dim);font-size:12.5px}
  header .spacer{flex:1}
  .btn{background:var(--panel2);border:1px solid var(--line);color:var(--ink);padding:7px 13px;border-radius:8px;
       cursor:pointer;font-size:13px}
  .btn:hover{border-color:var(--accent)}
  .btn.primary{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
  .counts{font-size:12.5px;color:var(--dim)}
  .counts b{color:var(--gold)}
  main{max-width:1180px;margin:0 auto;padding:20px 22px 120px}
  .intro{color:var(--dim);font-size:13px;margin:6px 0 20px;max-width:820px}
  .intro b{color:var(--ink)}
  .intro code{background:var(--panel2);padding:1px 5px;border-radius:4px;font-size:12px}
  .ev{background:var(--panel);border:1px solid var(--line);border-radius:14px;margin:0 0 18px;overflow:hidden}
  .ev>.hd{display:flex;align-items:center;gap:12px;padding:12px 16px;background:#141824;border-bottom:1px solid var(--line)}
  .ev>.hd .name{font-weight:650}
  .ev>.hd .ek{color:var(--dim);font-size:12px;font-family:ui-monospace,Menlo,monospace}
  .cols{display:grid;grid-template-columns:1fr 1fr;gap:0}
  .col{padding:16px}
  .col.teen{border-right:1px solid var(--line)}
  .tag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.4px;padding:2px 8px;border-radius:20px;text-transform:uppercase}
  .tag.teen{background:#241d43;color:#b9a7ff;border:1px solid #3a2f6b}
  .tag.parent{background:#123330;color:#7fe0d3;border:1px solid #1d5a52}
  .copy{margin:12px 0}
  .copy .k{font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim);margin-top:8px}
  .copy .subj{font-weight:650;font-size:15px}
  .copy .pre{color:var(--dim);font-size:13px}
  .copy .hero{font-weight:600;margin-top:4px}
  .copy .body{white-space:pre-wrap;font-size:13.5px;color:#cbd0dc;margin-top:2px}
  .src{font-family:ui-monospace,Menlo,monospace;font-size:10.5px;color:var(--out);margin-top:8px}
  .toneout{margin-top:10px;font-size:12px;color:var(--dim)}
  .toneout b{color:var(--gold);text-transform:lowercase}
  .toneout .tag2{font-size:9.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--out);border:1px solid var(--line);border-radius:5px;padding:1px 5px;margin-left:6px}
  .ctrl{margin-top:14px;border-top:1px dashed var(--line);padding-top:12px}
  .goldrow{display:flex;align-items:center;gap:10px;margin-bottom:10px}
  .toggle{display:flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}
  .toggle button{background:transparent;border:0;color:var(--dim);padding:6px 12px;cursor:pointer;font-size:12.5px}
  .toggle button.on-gold{background:var(--gold);color:#241a00;font-weight:700}
  .toggle button.on-out{background:var(--out);color:#fff;font-weight:600}
  .grp{margin:8px 0}
  .grp .lab{font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim);margin-bottom:4px}
  .chips{display:flex;flex-wrap:wrap;gap:6px}
  .chip{font-size:12px;padding:4px 10px;border-radius:16px;border:1px solid var(--line);color:var(--dim);cursor:pointer;user-select:none}
  .chip.on{background:var(--accent);border-color:var(--accent);color:#fff}
  .grp.pending{opacity:.55}
  .grp.pending .lab{color:#c08a4d}
  .chip.pending{border-style:dashed;cursor:not-allowed;color:var(--out);background:transparent}
  label.fld{display:block;margin-top:10px}
  label.fld .lab{font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim);margin-bottom:3px;display:block}
  input.txt,textarea.txt{width:100%;background:var(--panel2);border:1px solid var(--line);color:var(--ink);
       border-radius:8px;padding:7px 9px;font:13px inherit;resize:vertical}
  textarea.txt{min-height:44px}
  .col.golden{box-shadow:inset 0 0 0 2px var(--gold)}
  .col.out{opacity:.55}
  .seedhint{font-size:11px;color:var(--out);margin-top:6px;font-style:italic}
  .mignote{font-size:11px;color:#c08a4d;margin-top:6px;font-style:italic}
  footer.bar{position:fixed;bottom:0;left:0;right:0;background:#0d0f16f2;border-top:1px solid var(--line);
       padding:10px 22px;display:flex;align-items:center;gap:16px;backdrop-filter:blur(6px)}
</style></head><body>
<header>
  <h1>Hemingway · Golden-set marker <span style="color:var(--dim);font-weight:400">· reconciled</span></h1>
  <span class="sub">ruled palette: intent · signal · recipient · actor · priority</span>
  <span class="spacer"></span>
  <span class="counts" id="counts"></span>
  <button class="btn" id="reseed">Reset to migrated</button>
  <button class="btn primary" id="export">Export golden_set.json</button>
</header>
<main>
  <p class="intro">This is your golden set <b>reseeded from your own marks</b> and migrated to the ruled vocabulary.
  What changed: <b>tone</b> is no longer a chip — it's shown as the <b>measured output</b> (the thing the golden set
  exists to measure). <code>role</code> split into <b>recipient</b> (column) + <b>actor</b> (derived from the copy).
  <code>stakes</code>→<b>priority</b> (low/med/high); <code>signal</code> expanded to the canonical 6; intent values scrubbed to canon.
  The greyed <b>pending</b> groups (trust_calibration, state_transition) are the tracked gaps — visible in place, not wired.
  Where <code>reassure</code> was misfiled, an amber note flags where it relocates. Marks autosave (new key, v1 untouched).</p>
  <div id="root"></div>
</main>
<footer class="bar">
  <span class="counts" id="counts2"></span>
  <span class="spacer" style="flex:1"></span>
  <button class="btn primary" id="export2">Export golden_set.json</button>
</footer>
<script>
const DATA = __PAYLOAD__;
const LS = "hemingway_golden_v3";
let state = load();

function load(){
  try{ const s = JSON.parse(localStorage.getItem(LS)); if(s) return s; }catch(e){}
  return seedState();
}
function seedState(){
  const st = {};
  for(const ev of DATA.events){
    st[ev.event] = {};
    for(const side of ["teen","parent"]){
      const sd = ev[side].seed || {};
      st[ev.event][side] = {
        golden: (sd.golden===true?"gold":sd.golden===false?"out":null),
        facets: (sd.facets||[]).slice(),
        closer: sd.closer||"",
        why: sd.why||"",
      };
    }
  }
  return st;
}
function save(){ localStorage.setItem(LS, JSON.stringify(state)); render(); }
function esc(s){ return (s||"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c])); }

function chipGroups(evk, side){
  let h="";
  for(const [grp,opts] of Object.entries(DATA.palette)){
    h+=`<div class="grp"><div class="lab">${grp}</div><div class="chips">`;
    for(const o of opts){
      const on = state[evk][side].facets.includes(o);
      h+=`<span class="chip ${on?'on':''}" data-ev="${evk}" data-side="${side}" data-facet="${o}">${o}</span>`;
    }
    h+=`</div></div>`;
  }
  for(const [grp,opts] of Object.entries(DATA.pending||{})){
    h+=`<div class="grp pending"><div class="lab">${grp}</div><div class="chips">`;
    for(const o of opts){ h+=`<span class="chip pending">${o}</span>`; }
    h+=`</div></div>`;
  }
  return h;
}

function copyBlock(c){
  let h="";
  if(c.subject!==undefined && c.subject!=="") h+=`<div class="k">subject</div><div class="subj">${esc(c.subject)}</div>`;
  if(c.preheader) h+=`<div class="pre">${esc(c.preheader)}</div>`;
  if(c.hero) h+=`<div class="k">hero</div><div class="hero">${esc(c.hero)}</div>`;
  if(c.body) h+=`<div class="k">body</div><div class="body">${esc(c.body)}</div>`;
  return h;
}

function sideCol(ev, side){
  const c = ev[side]; const s = state[ev.event][side];
  const cls = s.golden==="gold"?"golden":s.golden==="out"?"out":"";
  const tone = c.tone ? `<div class="toneout">measured tone <span class="tag2">output</span> <b>${esc(c.tone)}</b></div>` : "";
  const mig = c.mignote ? `<div class="mignote">migrated: ${esc(c.mignote)}</div>` : "";
  return `<div class="col ${side} ${cls}">
    <span class="tag ${side}">${side}</span>
    <div class="copy">${copyBlock(c)}</div>
    <div class="src">${esc(c.src)}</div>
    ${tone}
    <div class="ctrl">
      <div class="goldrow">
        <div class="toggle" data-ev="${ev.event}" data-side="${side}">
          <button data-v="gold" class="${s.golden==='gold'?'on-gold':''}">★ Golden</button>
          <button data-v="out"  class="${s.golden==='out'?'on-out':''}">✖ Out</button>
        </div>
      </div>
      ${chipGroups(ev.event, side)}
      <label class="fld"><span class="lab">closer / sign-off (tone tell)</span>
        <input class="txt" data-ev="${ev.event}" data-side="${side}" data-f="closer" value="${esc(s.closer).replace(/"/g,'&quot;')}"></label>
      <label class="fld"><span class="lab">why golden (the judgment)</span>
        <textarea class="txt" data-ev="${ev.event}" data-side="${side}" data-f="why">${esc(s.why)}</textarea></label>
      ${mig}
    </div></div>`;
}

function render(){
  const root = document.getElementById("root");
  root.innerHTML = DATA.events.map(ev=>`
    <div class="ev"><div class="hd"><span class="name">${esc(ev.label)}</span><span class="ek">${ev.event}</span></div>
      <div class="cols">${sideCol(ev,"teen")}${sideCol(ev,"parent")}</div></div>`).join("");
  let g=0,o=0,tot=0;
  for(const ev of DATA.events) for(const side of ["teen","parent"]){ tot++; const v=state[ev.event][side].golden; if(v==="gold")g++; if(v==="out")o++; }
  const txt = `<b>${g}</b> golden · ${o} out · ${tot-g-o} undecided / ${tot} cells`;
  document.getElementById("counts").innerHTML=txt;
  document.getElementById("counts2").innerHTML=txt;
}

document.addEventListener("click",e=>{
  const t=e.target;
  if(t.matches(".toggle button")){
    const w=t.closest(".toggle"); const ev=w.dataset.ev, side=w.dataset.side, v=t.dataset.v;
    const cur=state[ev][side].golden;
    state[ev][side].golden = (cur===v?null:v); save();
  }
  if(t.matches(".chip")){
    if(!t.dataset.ev) return;   // pending chips are non-interactive
    const {ev,side,facet}=t.dataset; const arr=state[ev][side].facets;
    const i=arr.indexOf(facet); if(i>=0)arr.splice(i,1); else arr.push(facet); save();
  }
});
document.addEventListener("input",e=>{
  const t=e.target; if(!t.matches(".txt"))return;
  const {ev,side,f}=t.dataset; state[ev][side][f]=t.value;
  localStorage.setItem(LS, JSON.stringify(state));
});
document.getElementById("reseed").onclick=()=>{ if(confirm("Reset all marks to the migrated seed?")){ state=seedState(); save(); } };

function exportJSON(){
  const out={ generated_note:"Golden set (reconciled palette). golden=in the prescriptive subset. Marks are Brittney's authorship.",
              teen_source:DATA.meta.teen_source, parent_source:DATA.meta.parent_source, events:[] };
  for(const ev of DATA.events){
    const row={event:ev.event,label:ev.label};
    for(const side of ["teen","parent"]){
      const s=state[ev.event][side];
      row[side]={ golden: s.golden==="gold", excluded: s.golden==="out",
                  facets:s.facets, closer:s.closer, why:s.why, tone:ev[side].tone,
                  copy:{subject:ev[side].subject,preheader:ev[side].preheader,hero:ev[side].hero,body:ev[side].body},
                  source:ev[side].src };
    }
    out.events.push(row);
  }
  const blob=new Blob([JSON.stringify(out,null,2)],{type:"application/json"});
  const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download="golden_set.json"; a.click();
}
document.getElementById("export").onclick=exportJSON;
document.getElementById("export2").onclick=exportJSON;
render();
</script></body></html>
"""

htmlout = TPL.replace("__PAYLOAD__", json.dumps(payload))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write(htmlout)
print(f"wrote {OUT}  ({len(htmlout)} bytes)")
print(f"events: {len(events)}")
for ev in events:
    for side in ("teen", "parent"):
        s = ev[side]
        g = "GOLD" if s["seed"]["golden"] else ("out" if s["seed"]["golden"] is False else "  ?")
        print(f"  {g:4} {ev['event']:18} {side:6} tone={s['tone']:8} :: {' '.join(s['seed']['facets'])}")
