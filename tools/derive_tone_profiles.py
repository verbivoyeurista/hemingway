#!/usr/bin/env python3
"""
derive_tone_profiles.py  --  Hemingway Phase 0, last piece.

Reads the hand-marked golden set and DERIVES two tone profiles (teen, parent)
plus the held-vs-flexed split -- the demo spine "voice held, tone flexed".

Philosophy (composition over assertion): this script does NOT assert tone.
It COMPOSES each profile from Brittney's marks -- the golden picks are the
authorship, the facet chips are the primitives, the closers are the tone tells.
Everything printed is grounded in a count or a pulled example from the corpus.

Provenance inversion vs voice: venmo_voice is a BASELINE (descriptive,
fingerprinted over 6,838 strings, why_held=observed, LOWER confidence). These
tone profiles are a GOLDEN SUBSET (prescriptive, MARKED not fingerprinted,
why_held=authored, HIGHER confidence -- a human decided which strings count).

Single self-contained file (Lode-1.0 discipline). No deps beyond stdlib.

  in : ~/hemingway/library/golden_set.json
  out: ~/hemingway/library/tone_profiles.json  (+ readable stdout summary)
"""
import json, re, os, sys
from collections import Counter, defaultdict

HOME = os.path.expanduser("~")
IN   = os.path.join(HOME, "hemingway/library/golden_set.json")
OUT  = os.path.join(HOME, "hemingway/library/tone_profiles.json")

# Sanctioned facet -> category map (from build_golden_marker.py FACETS).
# NB (Wren term-pass, open since 2026-05-31): 'signal' + 'stakes' are canonical
# (Layer 6 / Layer 4); 'intent' = shortened semantic_intent; 'role' carries the
# actor-vs-observer distinction. The affective axis was renamed 'warmth' -> 'tone'
# and 'plain' -> 'neutral' (Brittney, 2026-07-18): 'warmth' biased the axis toward
# warm=good; 'plain' smuggled in lesser/boring. 'neutral' is the unmarked zero-point.
# ('plain' kept mapped for back-compat with any legacy marks; canonical value = neutral.)
CATEGORY = {
    "inform": "intent", "reassure": "intent", "celebrate": "intent",
    "instruct": "intent", "alert": "intent", "request": "intent",
    "teen-user": "role", "parent-overseer": "role",
    "direct-address": "role", "about-the-teen": "role",
    "playful": "tone", "calm": "tone", "neutral": "tone", "plain": "tone",
    "high-stakes": "stakes", "routine": "stakes",
    "milestone": "signal", "update": "signal", "needs-action": "signal",
}
CATS = ["intent", "role", "tone", "stakes", "signal"]

EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿\U0001F1E6-\U0001F1FF❤]")
DELIGHT = re.compile(r"\b(you rock|hooray|woohoo|nice|congrats|congratulations)\b", re.I)
GUARDIAN = re.compile(r"parent or guardian", re.I)
CONTRACTION = re.compile(r"\b\w+'(ll|re|ve|s|t|d|m)\b", re.I)


def load():
    with open(IN) as f:
        return json.load(f)


def golden_sides(data, audience):
    """Return list of (event, side_dict) that are golden & not excluded for an audience."""
    out = []
    for ev in data["events"]:
        s = ev.get(audience)
        if s and s.get("golden") and not s.get("excluded"):
            out.append((ev["event"], s))
    return out


def joined_copy(side):
    c = side.get("copy", {}) or {}
    return "\n".join(v for v in [c.get("hero", ""), c.get("body", "")] if v)


def actor_framing(sides):
    """Detect who the second person is and who acts -- the role axis, mechanically."""
    named_actor = 0     # a guardian name acts on the teen ("Judy locked ...")
    you_is_actor = 0    # "You <verb>ed [teen_name]'s ..." -- reader is the actor
    defers_up = 0       # routes reader to a guardian
    for _, s in sides:
        txt = joined_copy(s)
        if re.search(r"\b(You|you) (locked|unlocked|canceled|changed|added|requested)\b", txt):
            you_is_actor += 1
        if re.search(r"\b[A-Z][a-z]+ (locked|unlocked|changed|canceled)\b", txt):
            named_actor += 1
        if GUARDIAN.search(txt) or "ask your parent" in txt.lower():
            defers_up += 1
    return {"named_guardian_acts": named_actor,
            "reader_is_actor": you_is_actor,
            "defers_to_guardian": defers_up}


def closer_tells(sides):
    closers = [(e, s.get("closer", "")) for e, s in sides]
    nonempty = [(e, c) for e, c in closers if c.strip()]
    emoji = [(e, c) for e, c in nonempty if EMOJI.search(c)]
    delight = [(e, c) for e, c in nonempty if DELIGHT.search(c)]
    guardian = [(e, c) for e, c in nonempty if GUARDIAN.search(c)]
    words = [len(c.split()) for _, c in nonempty]
    return {
        "n_closers": len(nonempty),
        "n_empty": len(closers) - len(nonempty),
        "emoji_closers": [c for _, c in emoji],
        "delight_closers": [c for _, c in delight],
        "guardian_deferral_closers": [c for _, c in guardian],
        "avg_closer_words": round(sum(words) / len(words), 1) if words else 0,
        "all_closers": {e: c for e, c in nonempty},
    }


def facet_profile(sides):
    by_cat = defaultdict(Counter)
    for _, s in sides:
        for f in s.get("facets", []):
            cat = CATEGORY.get(f)
            if cat:
                by_cat[cat][f] += 1
    out = {}
    for cat in CATS:
        c = by_cat.get(cat, Counter())
        out[cat] = {"counts": dict(c), "dominant": [f for f, _ in c.most_common()]}
    return out


def build_profile(data, audience):
    sides = golden_sides(data, audience)
    fp = facet_profile(sides)
    return {
        "audience": audience,
        "n_golden": len(sides),
        "events": [e for e, _ in sides],
        "facet_profile": fp,
        "actor_framing": actor_framing(sides),
        "closer_tells": closer_tells(sides),
    }


def held_vs_flexed(teen, parent):
    """Per category: same dominant facet across audiences = HELD (voice);
    different = FLEXED (tone). Computed only from the marks, not asserted."""
    held, flexed = {}, {}
    for cat in CATS:
        t = set(teen["facet_profile"][cat]["dominant"])
        p = set(parent["facet_profile"][cat]["dominant"])
        shared = sorted(t & p)
        teen_only = sorted(t - p)
        parent_only = sorted(p - t)
        if shared and not teen_only and not parent_only:
            held[cat] = shared
        else:
            flexed[cat] = {"shared": shared, "teen_adds": teen_only, "parent_adds": parent_only}
    return {"held": held, "flexed": flexed}


def main():
    if not os.path.exists(IN):
        sys.exit(f"missing {IN} -- export the golden set first")
    data = load()
    teen = build_profile(data, "teen")
    parent = build_profile(data, "parent")
    split = held_vs_flexed(teen, parent)

    out = {
        "name": "venmo_tone_profiles",
        "brand": "Venmo",
        "kind": "derived_tone_profile",
        "_provenance": {
            "method": "COMPOSED from the hand-marked golden set. The golden picks "
                      "are the authorship (Brittney's editorial call); facet chips "
                      "are the primitives; closers are the tone tells. Nothing "
                      "asserted -- every field is a count or a pulled example.",
            "source": os.path.relpath(IN, HOME),
            "reading": "This is TONE (flexes by audience/situation), overlaid on the "
                       "constant VOICE (venmo_voice_extracted.json). MARKED not "
                       "fingerprinted: tone can't be extracted statistically, it is "
                       "decided. That is why a small golden set is the honest method.",
            "why_held": "authored -- a human marked which strings count. Carries "
                        "HIGHER confidence than the voice baseline (observed/derived).",
            "confidence_vs_voice": "voice = descriptive baseline (low); tone = "
                                   "prescriptive golden subset (higher, because authored).",
        },
        "teen": teen,
        "parent": parent,
        "voice_held_tone_flexed": split,
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    # ---- readable summary ----
    def line(x=""):
        print(x)
    line(f"\n=== tone profiles derived  ({teen['n_golden']} teen golden, {parent['n_golden']} parent golden) ===")
    for prof in (teen, parent):
        line(f"\n[{prof['audience'].upper()}]  events: {', '.join(prof['events'])}")
        for cat in CATS:
            dom = prof["facet_profile"][cat]["dominant"]
            if dom:
                line(f"    {cat:8} : {', '.join(dom)}")
        af = prof["actor_framing"]
        line(f"    framing  : guardian-acts={af['named_guardian_acts']}  reader-acts={af['reader_is_actor']}  defers-up={af['defers_to_guardian']}")
        ct = prof["closer_tells"]
        line(f"    closers  : {ct['n_closers']} written / {ct['n_empty']} empty, avg {ct['avg_closer_words']} words")
        if ct["emoji_closers"]:
            line(f"      emoji  : {ct['emoji_closers']}")
        if ct["delight_closers"]:
            line(f"      delight: {ct['delight_closers']}")
        if ct["guardian_deferral_closers"]:
            line(f"      defers : {ct['guardian_deferral_closers']}")

    line("\n=== VOICE HELD (same across teen & parent = the constant) ===")
    for cat, v in split["held"].items():
        line(f"    {cat:8} : {', '.join(v)}")
    line("\n=== TONE FLEXED (diverges by audience = the variable) ===")
    for cat, v in split["flexed"].items():
        bits = []
        if v["shared"]: bits.append(f"shared[{', '.join(v['shared'])}]")
        if v["teen_adds"]: bits.append(f"teen+[{', '.join(v['teen_adds'])}]")
        if v["parent_adds"]: bits.append(f"parent+[{', '.join(v['parent_adds'])}]")
        line(f"    {cat:8} : {'  '.join(bits)}")
    line(f"\nwrote {os.path.relpath(OUT, HOME)}\n")


if __name__ == "__main__":
    main()
