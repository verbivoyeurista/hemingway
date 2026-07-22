#!/usr/bin/env python3
"""
analyze_tone_residual.py  --  Wren's test for the trust_calibration chip.

Question (from the facet-vocab ruling): does the golden set need a
trust_calibration chip, or do signal + recipient + actor already explain the
tone it measures?

Method (Wren, 2026-07-18): predict tone with signal + recipient + actor.
Group golden strings by that predictor triple. WITHIN each group, look at
residual tone variance:
  - flat within group  -> signal+recipient+actor is enough; no trust chip;
                          reassure retires from the marker (lives in canon).
  - splits within group -> a predictor is missing. Inspect the split:
                          build-vs-repair (first-time vs after-incident) => trust earns its chip.
                          gain-vs-lose access => event/state_transition, not trust.

Reads the CURRENT (pre-ruling) vocab in golden_set.json. Self-contained.
"""
import json, re, os
from collections import defaultdict

HOME = os.path.expanduser("~")
IN = os.path.join(HOME, "hemingway/library/golden_set.json")

TONE = {"playful", "calm", "neutral"}
SIGNAL = {"milestone", "update", "needs-action", "onboarding"}
INTENT = {"inform", "reassure", "celebrate", "instruct", "alert", "request"}
STAKES = {"high-stakes", "routine"}


def actor_of(side):
    """Who acted -- scanned across all copy fields (subject carries it sometimes)."""
    c = side.get("copy", {}) or {}
    txt = " ".join(c.get(k, "") for k in ("subject", "preheader", "hero", "body"))
    if re.search(r"\bYou (locked|unlocked|canceled|changed|added|activated)\b", txt):
        return "reader"            # reader is the actor -- check first ("You" is not a name)
    if re.search(r"\b(?!You\b)[A-Z][a-z]+ (locked|unlocked|changed|canceled|activated)\b", txt):
        return "guardian"          # a named guardian acted on the teen
    return "system"                # passive / system-initiated


def recipient_of(facets):
    if "teen-user" in facets: return "teen"
    if "parent-overseer" in facets: return "parent"
    return "?"


def pick(facets, vocab):
    return sorted(set(facets) & vocab)


def main():
    data = json.load(open(IN))
    rows = []
    for ev in data["events"]:
        for side in ("teen", "parent"):
            s = ev.get(side)
            if not (s and s.get("golden") and not s.get("excluded")):
                continue
            f = s.get("facets", [])
            rows.append({
                "event": ev["event"], "side": side,
                "signal": " ".join(pick(f, SIGNAL)) or "-",
                "recipient": recipient_of(f),
                "actor": actor_of(s),
                "tone": " ".join(pick(f, TONE)) or "-",
                "intent": " ".join(pick(f, INTENT)) or "-",
                "stakes": " ".join(pick(f, STAKES)) or "-",
                "why": s.get("why", ""), "closer": s.get("closer", ""),
                "hero": (s.get("copy", {}) or {}).get("hero", ""),
            })

    groups = defaultdict(list)
    for r in rows:
        groups[(r["signal"], r["recipient"], r["actor"])].append(r)

    print(f"\n=== tone residual test  (predictors: signal + recipient + actor,  n={len(rows)}) ===\n")
    residual_cells = []
    for key in sorted(groups):
        g = groups[key]
        tones = sorted({r["tone"] for r in g})
        flat = len(tones) == 1
        tag = "FLAT " if flat else "RESID"
        print(f"[{tag}] signal={key[0]!r}  recipient={key[1]}  actor={key[2]}   -> tone {{{', '.join(tones)}}}")
        for r in g:
            print(f"         {r['event']:18} {r['side']:6} tone={r['tone']:14} intent={r['intent']:20} stakes={r['stakes']}")
        if not flat:
            residual_cells.append((key, g))
        print()

    if not residual_cells:
        print(">>> VERDICT: tone is FLAT within signal+recipient+actor everywhere.")
        print("    No trust chip. reassure retires from the marker; lives in canon for the generator.\n")
        return

    print(">>> RESIDUAL found -- inspecting the latent axis in each split cell:\n")
    for key, g in residual_cells:
        print(f"  cell signal={key[0]!r} recipient={key[1]} actor={key[2]}:")
        for r in sorted(g, key=lambda x: x["tone"]):
            print(f"    - {r['event']:16} tone={r['tone']:8} | hero: {r['hero'][:60]!r}")
            print(f"      why: {r['why']}")
        print()


if __name__ == "__main__":
    main()
