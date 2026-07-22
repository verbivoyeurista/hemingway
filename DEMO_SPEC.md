# Hemingway demo — interactive composition stack

**One belief to install:** this isn't a style prompt. It's a knowledge system — you can toggle each
layer off and watch the email lose exactly what that layer contributed. The moat (voice fingerprinted
from a corpus, tone hand-marked as a golden set, facets composing) becomes *visible and interactive*.

## The surface
A sample email on the left. On the right, a stack of composition **layer cards**. Tapping a
toggleable layer recomposes the email live. The stack = the ontology's scope ladder.

## The layers (bottom = universal/locked → top = variable/toggleable)

🔒 **LOCKED substrate** (always on — you can't turn these off):
1. **Mechanics** — universal house style (em-dash sparingly + unspaced; sentence case). Engine-scope, all brands.
2. **Compliance** — legal / regulatory (disclaimers, consent). Can't turn off the law.
3. **UX / content style guide** — needs-stack, required/prohibited content, accessibility, reading level. Can't turn off "be clear + accessible."
4. **Brand profile** — strategic identity (mission, values, personality) that voice is derived from.

🔘 **TOGGLEABLE spotlight** (tap to see each layer's contribution):
5. **Voice** — brand linguistic fingerprint. OFF → generic, brand-anonymous English.
6. **Tone** — the moment's register (composed from signal). OFF → flat, register-less.
7. **User** — audience. Switch teen ⇄ parent → reframes actor, closer, warmth ceiling.
8. **Situation** (signal/event) — preset, OR typed by the user in "generate your own."

Split logic: locked = constraints you can't violate; toggleable = compositional choices whose
contribution we want visible. Brand-profile is *choosable*-locked (spotlight is voice/tone/user).

## Interactions
- **Tap Voice / Tone** → on/off. Watch the email go generic / flat.
- **Tap User** → switch teen/parent. Watch it reframe (voice held, tone flexed).
- **Clear + generate your own** → user describes an event (e.g. "account graduates at 18"); system
  composes it through the full stack. Proves it generalizes to unseen events.

## Build note (robustness for Monday)
- Toggle states are **pre-composed** controlled ablations — swap between baked versions, no live model.
  This is the hero = controlled ablation principle (never a live competitor).
- Only "generate your own" wants live (or a few pre-baked) generation.

## Status
- Design: Brittney mocks in Figma (her lane).
- Build: Atlas → self-contained HTML (marker/demo discipline), reads pre-composed states.
- Inputs ready: `venmo_voice_extracted.json`, `tone_profiles.json`, `golden_set.json`, `element_facets.md`.
