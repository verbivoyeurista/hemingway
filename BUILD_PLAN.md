# Hemingway — Build Plan (v2)

_Owner: Brittney (Meoweth) · drafted with Atlas 2026-07-16 · **v2 folds in Wren's independent CD
review** (`projects/hemingway/REVIEW_RESPONSE_FROM_WREN_2026_07_16_build_plan.md`) + the committed
three-layer content model. The tracking doc; check against it to stay on plan._

**Two load-bearing calls promoted to canonical (Wren + Meoweth):**
1. **Voice held, tone flexed** — not "voice-flex." Voice is constant (who Venmo is); tone flexes by
   situation/audience. Precision here is the expertise being sold.
2. **The score_card separates measured from judged** — or it rebuilds the flat, confidence-hiding
   score CFE exists to critique.

## What Hemingway is
The **portable Content Brain** — a content-design evaluation + production system on Claude API,
outside Meta. The instantiation of `research/content_brain_architecture_spec.md`. Sibling of Lode on
the same spine (**composition over assertion**): *"Nothing asserted. Everything composed. The
judgment is in the system."*

**Goal now:** a demo-able Venmo showcase that readies Brittney for agency contract work. The block
was never quality — it's a *demo problem* (legible in 30 seconds). **Foreground the METHOD over the
artifact:** the pitch isn't "here's Venmo's guide," it's *"point it at any brand's shipped strings."*

## Governing discipline
- **Lode-1.0 discipline:** Phase 0 is the only commitment; later phases wait for their build-when
  trigger (`decomposition_emerges_from_use`).
- **Carry the POV:** the "who authors the model / ideas→biases" thesis is the lens. Hemingway =
  *human support over human replacement.*

---

## Architecture — two three-layer models, nested
- **System architecture** (Content Brain spec): **Knowledge → Agents → Orchestrator.**
- **The Knowledge layer is structured as the committed content model: facets → patterns → profiles.**
  - **Facets** (bottom, upstream) — orthogonal primitives of meaning that compose into patterns.
    v0 (stabilizing, 9): `semantic_intent` · `event` · `risk_posture` · `state_transition` ·
    `trust_calibration` · `user_state` · `stakes` · `delivery_context` · `recipient`.
  - **Patterns** (middle) — channel-specific structures (email_alert, push, in-app status). A pattern
    declares which facets matter and *composes* rules from facet intersections (doesn't enumerate).
  - **Profiles** (top) — who's written for/to. Audience calibration (parent, teen, business, primary).
    **This is the layer the demo's parent-vs-teen split exercises.**
- **Voice** sits across all of it as the *constant* (the extracted `venmo_voice`). **Tone** is
  *composed from the facets* for a given moment + profile. Voice held; tone flexed.

Principles: knowledge-first · deterministic where possible, LLM where necessary · **observable**
(every finding traces to a `source_rule`) · portable · layered.

## Database rules
- **Two DB types:** a **rules library** (facets/patterns/profiles/voice — *what should be true*) and
  a **string corpus** (all shipped strings — *what is*). Different jobs: rules *evaluate*; corpus is
  what you *extract voice from* and *baseline against*.
- **Baseline ≠ target.** The broad corpus gives a **baseline** (descriptive — Venmo on average) with
  representativeness *and* noise in the same purchase. `good_examples` must be a **curated golden
  subset** (prescriptive), never the whole corpus. Shipped ≠ good.
- **Curated extraction, said straight.** The moment you pick which strings count as voice, you've
  made the editorial call — *that filter IS the authorship*. Sell the curation as the CD judgment;
  don't hide behind "we just extracted it."
- **Content full-state; links are provenance only.** (Verso's full-state files rotted; live links
  need walled-garden infra.) The LODE §3B idea-shape applied to knowledge: `content` + `provenance`
  + `why_held` + `last_reviewed`. **Extracted rules carry LOWER confidence** than authored ones
  (`why_held: observed/derived`, not `consensus` — nobody agreed to them).
- **Build only the delta the model can't do.** Skip grammar (the model powers AP; forcing rules is
  worse). Invest in Venmo voice / terminology / audience.
- **Terminology is the most rigorous Phase 0 DB piece** — the do/don't-say list. "wallet" when Venmo
  never says wallet is the cheapest, most legible, most embarrassing demo failure.

---

## The demo (Phase 0 output) — "voice held, tone flexed"
Show the **compositional stack**, not a competition with live. Order: **neutral → +voice → +tone**,
with the audience split landing at **tone**:

```
          neutral        + voice             + tone
parent    [flat facts]   [sounds Venmo]      [Venmo · parent register]
teen      [flat facts]   [sounds Venmo]      [Venmo · teen register]
                         ↑ identical rows      ↑ rows diverge
                         VOICE HELD            TONE FLEXED
```
- The **+voice** column is *identical* across parent/teen (voice held); the **+tone** column
  *diverges* (tone flexed). "Voice holds steady as Venmo while tone adapts to the reader" — made
  visually undeniable, no expertise required.
- **`live` is never a column to beat.** The hero contrast is **no-voice → +voice/+tone**, framed as a
  **controlled ablation**: *"same model, same task — the only change is whether the DB is in the
  room."* (CFE information-separation as a demo.) If `live` appears, it's neutral context, curated
  for *representativeness*, never rigged weak.
- **REQUIREMENT (not nice-to-have): one visible knowledge thread per Venmo-voice/tone cell** — e.g.
  *"teen tone = `semantic_intent:reassure` + `user_state:stress` + `stakes:trust` + `profile[teen]:
  no financial jargon`."* Without it the demo only proves "a model can adopt a voice"; *with* it,
  the thesis (**the judgment is in the system**) is on screen. Comp-over-assertion, rendered.
- **Fingerprint delta: optional** — text contrast is the proof for everyone; numbers corroborate for
  technical viewers. Never blocks "done."

---

## Gated build sequence

### Phase 0 — MVP: "voice held, tone flexed"
1. ✅ Brand source resolved (all Venmo). Filter vendor strings (Ingo) + isolate voice-bearing strings.
2. Assemble the **Venmo DB slice**: **voice** (constant — extracted ✅ `venmo_voice_extracted.json`),
   **tone** composed from the relevant facets, **2 profiles** (parent + teen — extract from the
   parent-vs-teen email diff), **terminology** (rigorous do/don't-say), the corpus (baseline +
   curated `good_examples`).
3. Make the generator **knowledge-driven** (kill GRC + the generic terse-rewrite; load the DB slice).
4. **Curate 3–5 demo inputs** where the compositional flex is unambiguous *(its own task)*.
5. Surface: the neutral → +voice → +tone stack × parent/teen, **with the visible knowledge thread**.
6. Optional: light fingerprint delta.
- **Done when:** you pull it up and a non-CD gets "voice held, tone flexed" in 30 seconds.

### Later phases (build-when triggers)
012's thesis = **one bar, two modes, no routing UI** ("the left-nav everyone copies and nobody
reads"). **Grade and Draft are *modes of the one bar*, not nav destinations.** Manage is the only
genuinely new *surface* (a list). Keep that line or the phases drift into four tabs.

| Phase | What | Trigger |
|---|---|---|
| **1 — Home** | 012 bar (Ask/Draft *modes*) + transparent **DB cards** (plain-language glosses, not schema dumps) | MVP lands; need becomes "let me understand it myself" |
| **2 — Grade** | grade the user's own content (see rubric) — a *mode of the bar* | people draft and want feedback on *their* drafts |
| **3 — Draft** | generative: draft-from-brief + draft-from-input; output follows the content type (**don't hardcode subject/preheader/body — the corpus is app strings**) | people want to *make*, not just see |
| **4 — Manage** | all items + owners — the one genuinely new surface | enough items/people that "where is it / who owns it" is real |

### Grade — the rubric (spec'd; Grade & surface designed TOGETHER)
- **Verb system, minus Verdict** — five *action* verbs for findings: `Fix / Change / Consider /
  Notice / Question`. **Retire `Verdict`** (a doc-level pass/fail masquerading as a finding action —
  the composed overall *is* the verdict now).
- **The four axes = the four knowledge layers, scored** (comp-over-assertion applied to grading):
  `pattern conformance` (pattern layer) · `principle conformance` (facets) · `voice match` (profile/
  voice) · `signal/tone fit` (signal series). The score is *composed from the same components the
  system classifies with* — that's why these four.
- **Separate MEASURED from JUDGED.** `voice match` + `signal fit` = real fingerprint deltas off a
  baseline (**numbers**). `principle` + `pattern` conformance = **LLM judgments** (carry a
  confidence). Never print "principle 3/5" beside "voice 72" as if equally objective.
- **Compose the overall, don't assert it.** No averaging four axes where two are false-precise —
  compose from axis states + verbs (e.g. any `Fix` caps the overall at WARN regardless of numbers).
- **Return `positive_signals`** — what to *keep*, not only what to fix (good CD practice + good demo).
- **Grade ↔ surface coupling:** the thick rubric breaks 012's thin PASS/FAIL/WARN response layout.
  Use **progressive disclosure** — thin composed overall + top findings, expand for the full
  score_card. Design the rubric and the response-state together.

### Agent architecture
Knowledge in the **DB**, agents crawl it (never split by knowledge domain). Split by **cognitive
mode** (Fix vs Notice vs Question); **grade separate from write** (the eyes can't be the hands);
writer ↔ evaluator **revision loop**, explicit stop (max 2).

## Guardrails (from scanning the other agents' bites)
- **CD Brain** conflated knowledge + agent behavior → keep knowledge in the DB.
- **Verso** had no revision-termination + a 1,644-line agent → explicit stop criteria, small agents.
- **Central Products** shipped 0 evals at maturity → ship with a golden set from day one.

## Roadmap (deferred — the engine, not the demo)
Full 6-agent orchestra · planner · full 8-dim fingerprint · session memory · live info + the
outward-Lode eye (parked) · editable DB · **multi-brand (the commercial payoff — the method is the
product)** · **prohibition knowledge as a first-class type** ("what you must NOT say" — regulatory /
teen-safety / fraud-sensitive; agencies want to see you know the guardrails) · Figma/CMS · Lode-as-skills.

## Content model open questions (Meoweth/Wren, stabilizing)
- Is `delivery_context` a facet or a pattern attribute?
- Does `recipient` roll into `user_state`?

## Assets on disk
- **Strings:** `~/hemingway/library/venmo_strings.txt` (Venmo corpus, 6,894 entries; source
  `~/Desktop/MARKs.txt`) · `~/conversation_insights/venmo-onboarding-content/`
- **Extracted:** `~/hemingway/library/venmo_voice_extracted.json` (the constant VOICE — baseline)
- **Emails:** `~/Downloads/venmo_emails/`, `~/Downloads/parent_emails_v3/` (→ parent/teen tone split)
- **Brand:** `~/Downloads/pattern_stack/brand_venmo.json`
- **Research:** `content_brain_architecture_spec.md`, `verso-deep-dive.md`,
  `cd-brain-landscape-research.md` (all `~/Rhys/projects/hemingway/research/`)
- **Review:** `~/Rhys/projects/hemingway/REVIEW_RESPONSE_FROM_WREN_2026_07_16_build_plan.md`
- **Build:** `~/hemingway/` (v0 app + client grader), `~/hemingway-api/` (Cloudflare Worker)
- **Design:** vault `~/Rhys/projects/hemingway/notes/` (012 surface, 014 voice-vs-tone, 004/005/006)

## OPEN QUESTIONS
1. ~~Brand source~~ **RESOLVED:** all CashyApp = Venmo (de-ID find-replace); corpus reverted; Ingo
   filtered.
2. **Confirm with Wren:** the demo order **neutral → voice → tone** (split-at-tone) — Atlas argues
   putting the audience split at the *last* step is what makes "held vs flexed" pop; Wren's note
   phrased it loosely as tone→voice.
