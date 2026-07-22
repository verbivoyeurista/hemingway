# Marker facet coverage — golden-set marker vs committed schedule

**What this is:** a ledger of what the golden-set marker covers, coarsens, or omits relative to
the committed 9-facet schedule (`Rhys/projects/hemingway/notes/facet_schedule_v0.md`). The marker
is a **declared lossy view** of canon, not a peer vocabulary. Canon is Wren's; this ledger is the
marker's (Atlas's) side, kept in sync when the vocabulary is ruled.

Last ruling: 2026-07-18 facet-vocabulary reconciliation (see
`Rhys/capture/2026-07/2026_07_18_facet_vocab_reconciliation.md` +
`Rhys/projects/hemingway/REVIEW_RESPONSE_FROM_WREN_2026_07_18_facet_vocab_reconciliation.md`).

## Marker palette (post-ruling) — 5 input handles + 1 measured output

| marker handle | canon facet | status |
|---|---|---|
| `intent` | semantic_intent (#1) | PRESENT — values scrubbed to canon (warn/confirm/invite/alert/celebrate/instruct/protect); dropped `inform`→confirm/alert, `reassure`→(trust, tracked-missing), `request`→invite |
| `signal` | signal (004/028, drives tone) | PRESENT — expanded to canonical 6 (milestone/update/needs_action/urgent/onboarding/monitoring); `account_restricted` ruled off access_risk |
| `recipient` | recipient (#9) | PRESENT — split from `role`; values **teen / parent** for this set. `account_holder` + `observer` deferred to the hierarchical model (a parent IS an account_holder; a teen account is a sub-account) |
| `actor` | event_actor (inside event, #2) | PRESENT — split from `role`; values **parent / teen / system** (the user who acted, or system when no user acted); derived from copy. Shares the parent/teen vocabulary with recipient — that's what makes `monitoring` (recipient=parent + actor=teen) expressible |
| `priority` | stakes (#7), coarsened | PRESENT — coarse ceiling-on-warmth flag; values **low / medium / high**. Renamed off "stakes" (claimed the 5-field term) and off "urgency" (would collide with the `urgent` signal value) |
| `tone` (calm/playful/neutral) | — | RECLASSIFIED: not an input facet. It is the **measured output** (dependent variable) the golden set exists to measure. |

`trust_calibration` is **NOT** a marker chip — see deferred #2. Held as a tracked gap, not wired.

## Still missing / deferred — tracked, priority order

1. **`state_transition` (#4) — HIGHEST PRIORITY, earned by data.** The residual test
   (`tools/analyze_tone_residual.py`) found tone splits on **gain-vs-lose access** within a fully
   specified `(signal, recipient, actor)` cell (card_locked=calm vs pin_changed=playful, both
   `inform`). That residual is `state_transition` direction, not trust. This is the next facet to
   earn a chip.
2. **`event_outcome` (#2 sub-field) — data-earned 2026-07-19.** `completed | failed | pending |
   reversed` (canon 022). Surfaced by Template G: an onboarding email whose outcome=failed. Warmth =
   `onboarding`; the 😅 apologetic softening = `outcome:failed`. Sits alongside `state_transition`
   as the second `event` sub-field the residuals keep pointing at.

3. **`trust_calibration` (#5) — TESTED, NOT wired.** Ran the residual test twice (2026-07-19). With
   Template G mis-classified as `needs_action`, a calm-vs-playful residual appeared and trust looked
   real. Once Brittney ruled the honest signal = `onboarding` (an onboarding *fail-state*), the
   residual **dissolved** — the warmth is `onboarding + outcome:failed` composing, not a trust dial.
   So trust is NOT a marker chip. It stays in canon for the generator (025). What looked like a
   missing facet was two existing facets composing — comp-over-assertion catching itself.
3. **`risk_posture` (#3) ⟂ `stakes.material_risk` orthogonality seam.** The two nearly duplicate in
   canon (financial/identity/privacy). Real cleanup, its own session — flagged in 025 review, not
   this one.
4. **`event` sub-fields (#2): event_class / event_trigger.** `event_actor` surfaced (as `actor`),
   `event_outcome` is now data-earned (see #2). Convergence worth naming: **every residual this
   golden set produces points at the `event` facet** — `state_transition` (gain/lose) and
   `event_outcome` (success/fail). The data's ask is unambiguous: the next facet is `event`, not
   trust.
5. **`user_state` (#6)** — compound (appraisal/stress/mental-model). Generator-side for now.
6. **`delivery_context` (#8)** — N/A while the marker is single-channel (email). Revisit if the
   corpus spans channels.

## Recurrence guard (durable fix — pending)

The drift happened because the palette is hand-authored in `build_golden_marker.py`, free to wander
from canon. Durable close: **generate the palette from a machine-readable canonical facet source**
(canon = single source, marker = declared lossy view). Requires Wren to stand up that structured
source in the vault; Atlas makes `build_golden_marker.py` + `derive_tone_profiles.py` consume it.
Open since 2026-05-31; this is what actually closes it.
