#!/usr/bin/env python3
"""Build the Hemingway golden-set marking UI.

Loads the teen corpus (furlough Figma extract) + the parent corpus (Downloads
parent_emails_v3), pairs them by event, pre-seeds Atlas's candidate golden picks
and tone-facet tags, and emits a single self-contained HTML marking surface at
~/hemingway/tools/golden_marker.html (works over file://, marks persist to
localStorage, export to golden_set.json).

The marking is Brittney's editorial call -- the filter IS the authorship
(Wren 2026-07-16). Pre-seed is a starting draft to react to, not a decision.
"""
import json, os, glob, html

HOME = os.path.expanduser("~")
FURLOUGH = f"{HOME}/hemingway/library/furlough_emails_extracted.json"
PARENT_DIR = f"{HOME}/Downloads/parent_emails_v3"
OUT = f"{HOME}/hemingway/tools/golden_marker.html"

# --- load teen (furlough) ---
teen = {e["event"]: e for e in json.load(open(FURLOUGH))["emails"] if e["audience"] == "teen"}
# parent-facing frames that live in furlough (account_restricted parent, backup stub)
teen_parent_frames = {e["event"]: e for e in json.load(open(FURLOUGH))["emails"] if e["audience"] == "parent"}

# --- load parent (Downloads) ---
parent = {}
for f in sorted(glob.glob(f"{PARENT_DIR}/*.json")):
    d = json.load(open(f))
    parent[d["id"]] = d

# --- event pairing: teen_event -> parent_id (Downloads) or furlough parent frame ---
PAIRS = [
    # (event_key, label, teen_event, parent_source)  parent_source: ("dl", id) or ("furlough", event)
    ("card_locked",       "Card locked",            "card_locked",       ("dl", "debit_card_locked")),
    ("card_unlocked",     "Card unlocked",          "card_unlocked",     ("dl", "debit_card_unlocked")),
    ("account_restricted","Account restricted",     "account_restricted",("furlough", "account_restricted")),
    ("card_canceled",     "Card canceled",          "card_canceled",     ("dl", "debit_card_canceled")),
    ("pin_changed",       "PIN changed",            "pin_changed",       ("dl", "debit_card_pin_changed")),
    ("card_shipped",      "Card shipped",           "card_shipped",      ("dl", "debit_card_sent")),
    ("card_activated",    "Card activated",         "card_activated",    ("dl", "debit_card_active")),
    ("card_replaced",     "Card replaced / reissued","card_replaced",    ("dl", "debit_card_reissued")),
    ("backup_fi_added",   "Backup FI added",        "backup_fi_added",   ("dl", "venmo_teen_fi_added")),
]

# --- Atlas candidate pre-seed. golden: True/False/None(undecided). facets: chips. why/closer notes. ---
# recipient chip is implied by column; kept off the palette.
PALETTE = {
    "intent":   ["inform", "reassure", "celebrate", "instruct", "alert", "request"],
    "role":     ["teen-user", "parent-overseer", "direct-address", "about-the-teen"],
    "tone":     ["playful", "calm", "neutral"],
    "stakes":   ["high-stakes", "routine"],
    "signal":   ["milestone", "update", "needs-action"],
}

SEED = {
    # event: { teen:{golden,facets,closer,why}, parent:{...} }
    "card_locked": {
        "teen":   {"golden": True,  "facets": ["inform","teen-user","direct-address","calm","update"],
                   "closer": "Card transactions will be declined until Judy unlocks it.",
                   "why": "Names the parent as the actor ('Judy locked'); calm, no blame. Clean teen register."},
        "parent": {"golden": True,  "facets": ["inform","parent-overseer","about-the-teen","calm","update"],
                   "closer": "In the meantime, [teen_name] can still send and receive payments in the Venmo app.",
                   "why": "Same event, overseer frame ('You locked [teen_name]'s'); reassures the parent the teen isn't cut off."},
    },
    "card_unlocked": {
        "teen":   {"golden": True,  "facets": ["reassure","celebrate","teen-user","playful","update"],
                   "closer": "You can use your debit card again. 🤘🙌🖖",
                   "why": "Emoji closer is the compact tone tell -- voice held (warm), teen register (playful)."},
        "parent": {"golden": True,  "facets": ["inform","parent-overseer","about-the-teen","calm","update"],
                   "closer": "", "why": "Overseer-side of the same relief. Pairs cleanly against teen."},
    },
    "account_restricted": {
        "teen":   {"golden": True,  "facets": ["reassure","alert","teen-user","direct-address","calm","high-stakes","needs-action"],
                   "closer": "For help getting up and running again, ask your parent or guardian to contact us.",
                   "why": "Highest-stakes flex: alarming event, calm reassuring voice, routes teen to guardian. Best demo pair."},
        "parent": {"golden": True,  "facets": ["inform","alert","parent-overseer","about-the-teen","calm","high-stakes","needs-action"],
                   "closer": "For help unlocking your accounts, give us a call.",
                   "why": "Same alert, authority-to-adult register. (NB source typo 'been been restricted' -- fix if used verbatim.)"},
    },
    "card_canceled": {
        "teen":   {"golden": True,  "facets": ["inform","teen-user","calm","high-stakes","needs-action"],
                   "closer": "Not sure why? Your parent or guardian might have more info.",
                   "why": "Soft close that defers authority to the guardian without alarm -- textbook teen register."},
        "parent": {"golden": True,  "facets": ["inform","parent-overseer","about-the-teen","calm","needs-action"],
                   "closer": "If you didn't request this or have questions, contact us.",
                   "why": "Overseer confirmation; the actor is 'you'."},
    },
    "pin_changed": {
        "teen":   {"golden": True,  "facets": ["inform","teen-user","direct-address","playful","update"],
                   "closer": "Already have it? You rock and can ignore this email.",
                   "why": "'You rock' closer = sparing, earned delight in teen register. Strong voice-held tell."},
        "parent": {"golden": None,  "facets": ["inform","parent-overseer","update"],
                   "closer": "", "why": "Check parent copy is not thinner than teen before promoting."},
    },
    "card_shipped": {
        "teen":   {"golden": None,  "facets": ["celebrate","teen-user","playful","milestone"],
                   "closer": "Where will you use it first?",
                   "why": "Nice milestone energy but carries placeholder address block -- clean before use."},
        "parent": {"golden": None,  "facets": ["inform","parent-overseer","milestone"],
                   "closer": "", "why": ""},
    },
    "card_activated": {
        "teen":   {"golden": None,  "facets": ["celebrate","teen-user","milestone"],
                   "closer": "Remember—even though the card is yours, Judy can still see your transactions and lock your card.",
                   "why": "Good 'yours-but-supervised' line; candidate if a milestone pair is wanted."},
        "parent": {"golden": None,  "facets": ["inform","parent-overseer","milestone"],
                   "closer": "", "why": ""},
    },
    "card_replaced": {
        "teen":   {"golden": None,  "facets": ["inform","teen-user","update"],
                   "closer": "", "why": "Placeholder address block; lower demo value than locked/unlocked."},
        "parent": {"golden": None,  "facets": ["inform","parent-overseer","update"],
                   "closer": "", "why": ""},
    },
    "backup_fi_added": {
        "teen":   {"golden": None,  "facets": ["inform","teen-user","update"],
                   "closer": "Go to the app to view or edit this change.",
                   "why": "Teen copy is fine but generic."},
        "parent": {"golden": False, "facets": [],
                   "closer": "", "why": "OUT: furlough parent version is an empty STUB (body never written). Shipped != good. Downloads venmo_teen_fi_added shown instead."},
    },
}

def teen_cell(ev):
    e = teen.get(ev, {})
    return {
        "subject": e.get("subject",""), "preheader": e.get("preheader",""),
        "hero": e.get("hero",""), "body": e.get("body",""),
        "src": e.get("template_id",""),
    }

def parent_cell(source):
    kind, key = source
    if kind == "dl":
        d = parent.get(key, {})
        return {"subject": d.get("subject",""), "preheader": d.get("preheader",""),
                "hero": "", "body": d.get("body",""),
                "signal": d.get("signal",""), "src": f"Downloads/{key}.json"}
    else:  # furlough parent frame
        d = teen_parent_frames.get(key, {})
        return {"subject": d.get("subject",""), "preheader": d.get("preheader",""),
                "hero": d.get("hero",""), "body": d.get("body",""),
                "signal": "", "src": d.get("template_id","")}

data = []
for ev_key, label, teen_ev, psource in PAIRS:
    seed = SEED.get(ev_key, {})
    data.append({
        "event": ev_key, "label": label,
        "teen": {**teen_cell(teen_ev), **{"seed": seed.get("teen", {})}},
        "parent": {**parent_cell(psource), **{"seed": seed.get("parent", {})}},
    })

payload = {"palette": PALETTE, "events": data,
           "meta": {"teen_source": "furlough (Figma)", "parent_source": "parent_emails_v3 (Downloads)",
                    "note": "Pre-seed = Atlas candidate. Your marks are the authorship."}}

# ---------------- HTML ----------------
TPL = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hemingway · Golden-set marker</title>
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
  .intro{color:var(--dim);font-size:13px;margin:6px 0 20px;max-width:760px}
  .intro b{color:var(--ink)}
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
  label.fld{display:block;margin-top:10px}
  label.fld .lab{font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim);margin-bottom:3px;display:block}
  input.txt,textarea.txt{width:100%;background:var(--panel2);border:1px solid var(--line);color:var(--ink);
       border-radius:8px;padding:7px 9px;font:13px inherit;resize:vertical}
  textarea.txt{min-height:44px}
  .col.golden{box-shadow:inset 0 0 0 2px var(--gold)}
  .col.out{opacity:.55}
  .seedhint{font-size:11px;color:var(--out);margin-top:6px;font-style:italic}
  footer.bar{position:fixed;bottom:0;left:0;right:0;background:#0d0f16f2;border-top:1px solid var(--line);
       padding:10px 22px;display:flex;align-items:center;gap:16px;backdrop-filter:blur(6px)}
</style></head><body>
<header>
  <h1>Hemingway · Golden-set marker</h1>
  <span class="sub">teen (furlough) × parent (Downloads) — mark the tone exemplars</span>
  <span class="spacer"></span>
  <span class="counts" id="counts"></span>
  <button class="btn" id="reseed">Reset to pre-seed</button>
  <button class="btn primary" id="export">Export golden_set.json</button>
</header>
<main>
  <p class="intro">Voice is done (the constant, extracted from the corpus). <b>Tone can't be extracted — it's marked.</b>
  Shipped ≠ good: the corpus is a baseline, the golden set is the prescriptive subset of what <i>good</i> looks like.
  Choosing which strings count <b>is the authorship</b> (Wren, 2026-07-16). The gold picks + facet chips below are my
  candidate draft — <b>strike, promote, retag</b>. Closers are captured separately (Wren: sign-offs are their own tone tell).
  Your marks autosave; Export writes <code>golden_set.json</code> → feeds the two tone profiles.</p>
  <div id="root"></div>
</main>
<footer class="bar">
  <span class="counts" id="counts2"></span>
  <span class="spacer" style="flex:1"></span>
  <button class="btn primary" id="export2">Export golden_set.json</button>
</footer>
<script>
const DATA = __PAYLOAD__;
const LS = "hemingway_golden_v1";
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
  return h;
}

function copyBlock(c){
  let h="";
  if(c.subject!==undefined && c.subject!=="") h+=`<div class="k">subject</div><div class="subj">${esc(c.subject)}</div>`;
  if(c.preheader) h+=`<div class="pre">${esc(c.preheader)}</div>`;
  if(c.hero) h+=`<div class="k">hero</div><div class="hero">${esc(c.hero)}</div>`;
  if(c.body) h+=`<div class="k">body</div><div class="body">${esc(c.body)}</div>`;
  if(c.signal) h+=`<div class="k">signal (source)</div><div class="body">${esc(c.signal)}</div>`;
  return h;
}

function sideCol(ev, side){
  const c = ev[side]; const s = state[ev.event][side];
  const cls = s.golden==="gold"?"golden":s.golden==="out"?"out":"";
  const seedNote = (ev[side].seed && ev[side].seed.why) ? `<div class="seedhint">seed: ${esc(ev[side].seed.why)}</div>`:"";
  return `<div class="col ${side} ${cls}">
    <span class="tag ${side}">${side}</span>
    <div class="copy">${copyBlock(c)}</div>
    <div class="src">${esc(c.src)}</div>
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
      ${seedNote}
    </div></div>`;
}

function render(){
  const root = document.getElementById("root");
  root.innerHTML = DATA.events.map(ev=>`
    <div class="ev"><div class="hd"><span class="name">${esc(ev.label)}</span><span class="ek">${ev.event}</span></div>
      <div class="cols">${sideCol(ev,"teen")}${sideCol(ev,"parent")}</div></div>`).join("");
  // counts
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
    const {ev,side,facet}=t.dataset; const arr=state[ev][side].facets;
    const i=arr.indexOf(facet); if(i>=0)arr.splice(i,1); else arr.push(facet); save();
  }
});
document.addEventListener("input",e=>{
  const t=e.target; if(!t.matches(".txt"))return;
  const {ev,side,f}=t.dataset; state[ev][side][f]=t.value;
  localStorage.setItem(LS, JSON.stringify(state)); // save w/o full re-render (keep focus)
  let g=0,o=0,tot=0;
  for(const x of DATA.events) for(const s of ["teen","parent"]){ tot++; const v=state[x.event][s].golden; if(v==="gold")g++; if(v==="out")o++; }
});
document.getElementById("reseed").onclick=()=>{ if(confirm("Reset all marks to the pre-seed draft?")){ state=seedState(); save(); } };

function exportJSON(){
  const out={ generated_note:"Golden set for Hemingway tone profiles. golden=in the prescriptive subset. The marks are Brittney's editorial call (the authorship).",
              teen_source:DATA.meta.teen_source, parent_source:DATA.meta.parent_source, events:[] };
  for(const ev of DATA.events){
    const row={event:ev.event,label:ev.label};
    for(const side of ["teen","parent"]){
      const s=state[ev.event][side];
      row[side]={ golden: s.golden==="gold", excluded: s.golden==="out",
                  facets:s.facets, closer:s.closer, why:s.why,
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
print(f"events: {len(data)}  teen loaded: {len(teen)}  parent loaded: {len(parent)}")
