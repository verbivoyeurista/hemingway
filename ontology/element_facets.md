# Element — exhaustive facet draft (LIVING)

The **element** is the atomic authored content unit — surface-agnostic, the idea-analog.
This is the *exhaustion pass*: list every possible facet, then prune/derive together. Nothing
here is ruled — it's raw material. Each facet declares its **status**: DERIVED (computed from
evidence), AUTHORED (a human decides), COMPOSED (falls out of other facets), or CONSTANT (inherited).

Inward-out (Grain of the Web): the element is primary; the surface adapts to it, not the reverse.
Content-token model (Argyle): an element is a rich packet with **dependencies/siblings**, not a flat value.

---

## I. Payload — what it says
- **content** — the actual string(s). May be a **template** with slots (`[prefix] first name`, `Your $name`). — AUTHORED
- **content_slots** — the dynamic placeholders the copy exposes (teen_name, last_four, arrival_date). — DERIVED (from the copy)
- **length_budget** — character/word constraint (ties to the future "define header: how many chars"). — AUTHORED per surface-slot
- **required_content** — must-includes (canon: severity_cause_action, legitimacy_signal, single_clear_action). — COMPOSED (from stakes)
- **prohibited_patterns** — must-avoids (canon: no_alarm, no_celebration, no_warmth_cues). — COMPOSED (from stakes/trust)

## II. Semantics — what it's for & what prompted it
- **intent** (semantic_intent) — warn/confirm/invite/alert/celebrate/instruct/protect. — AUTHORED
- **event** — what happened in the system. Sub-fields: event_class, **actor**, **event_outcome** (completed/failed/…), event_trigger, **state_transition** (from→to). — DERIVED (from the trigger/copy). *The residuals keep pointing here.*
- **signal** — the moment: milestone/update/needs_action/urgent/onboarding/monitoring. Drives tone. — AUTHORED (the writer's framing choice)
- **trust_calibration** — build/reassure/repair/protect/mark_milestone. — AUTHORED (canon-for-generator; not a marker chip)

## III. Expression — how it's said
> **Scope ladder (which layer a rule impacts):** engine/universal (all brands) → brand/voice (one tenant) → moment/tone (composed) → audience/profile. A rule lives at the highest layer it's true for, so it can't be re-specified or forgotten downstream.
- **mechanics** — universal house-style / orthography. **ENGINE-SCOPE** (every tenant inherits it), the layer *below* voice; impacts ALL text regardless of brand/tone/audience. — CONSTANT (universal)
  - *em dash:* use **sparingly**; prefer **two sentences** over one em-dash clause; only when **earned** (drama, flair, a dramatic pause) — and then **no space on either side** (`word—word`, never `word — word`).
- **voice** — the brand constant (who's speaking). BRAND-SCOPE (one tenant). — CONSTANT (fingerprinted)
- **tone** — calm/playful/neutral. MOMENT-SCOPE. — COMPOSED (**depends on signal + profile** — worthless without its siblings)
- **profile** — the audience register it's composed for (teen/parent/…). AUDIENCE-SCOPE. — AUTHORED → drives tone composition

## IV. Stakes & reader
- **stakes / risk_posture** — material/access/trust/psychological risk if the comm fails. — AUTHORED (canon 025, 5-field)
- **priority** — coarse ceiling-on-warmth: low/med/high. — COMPOSED (from stakes)
- **user_state** — what the reader brings: appraisal, stress, mental_model, prior_context. — AUTHORED/estimated
- **accessibility** — reading_complexity, vulnerability_flags (protection triggers, not targeting). — AUTHORED (canon)

## V. Structure — relations (the content network)
- **prominence / role-in-message** — hero line vs body vs **closer** (closers are their own tone tell). — AUTHORED
- **relations** — dependencies & sequence to other elements (hero → CTA → closer). Siblings that don't work alone. — DERIVED/AUTHORED
- **actor** (also lives in II/event) — who acted, from the content semantics. — DERIVED (from copy)

## VI. Anatomy — element-as-idea (the meta / epistemic layer, inherited from Lode)
- **provenance** — golden / extracted-baseline / authored. — AUTHORED
- **status** — draft / shipped / golden / deprecated. (shipped ≠ good.) — AUTHORED
- **confidence** — measured (fingerprint numbers) vs judged (LLM + confidence); **why_held** (truth/consensus/inheritance). — DERIVED/AUTHORED
- **lineage** — version history of the copy. — DERIVED
- **localization / variants** — does it fork by locale/language? (federation: child forks parent, calls super). — AUTHORED

---

## Gemini pass — graded (comp-over-assertion filter: earn primitive status or compose)

**Accepted (real gaps):**
- I · `injection_schema` — typed slots WITH fallback primitives (`user_name [string, fallback:"there"]`). Pluralization = a case of this. — AUTHORED (schema) / DERIVED (slots)
- IV · `regulatory_governance` — GDPR/SEC/None. Composes into required/prohibited_content. Varies per client (agency). — AUTHORED
- IV · `reversibility` — irreversible/transient. Sub-field of event/state_transition. **Escalates priority** (dependency). — DERIVED
- V · `cardinality_constraint` — requires-sibling / stands-alone. Formalizes `relations` (Argyle's sibling dependency). — AUTHORED
- V · `semantic_weight` — H1-equivalent (NOT visual size). **Replaces `prominence`** — surface-agnostic, inward-out. — AUTHORED
- VI · `deprecation_strategy` — fallback-to-id / hard-fail for retired atoms. — AUTHORED
- VI · `licensing_or_copyright` — accepted but DEFERRED (rare for Venmo/agency now).

**Rejected (compose from existing — do NOT add as primitives):**
- II · `semantic_class` (Friction/Acceleration/Resolution) — a derived *lens* over intent+signal, not a facet.
- III · `formality_scale` — a set dial = the deleted `tone_register`. COMPOSED from voice+signal+audience. Measured output only, never an input knob.
- III · `rhetorical_device` — passive/active is voice; the rest is detectable from copy. DERIVED attribute, not authored facet.
- II · `actor_role` — already have it (`actor` / canon `event_actor`).

**Architecture decisions:**
- **Graph, not flat.** Relations/cardinality/content-network = first-class edges. Each atom = a structured record on a node. Instantiate in **Lode** (Hemingway is a Lode tenant; atom = idea, content-network = edges) — do NOT stand up a separate graph DB.
- Blueprint JSON shape = adopt as skeleton; VALUES must be derived, not asserted.

## Open threads for the pruning pass
- Which of these are **element** facets vs **surface** facets? (recipient / delivery_context / sender = surface, NOT here. profile is the tension — audience-register is element-ish, addressing is surface.)
- Dependencies to draw explicitly: tone←signal+profile; priority←stakes; required/prohibited←stakes+trust.
- Derive vs author is the through-line (Argyle: voice tokenizes, alt-text doesn't). Sort every facet.
- Is `signal` authored or DERIVED from `event`? (Today's Template G finding: signal is the *framing choice* — authored — but constrained by event/outcome.)
