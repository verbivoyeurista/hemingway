#!/usr/bin/env python3
"""Hemingway generator — knowledge-driven compositional copy.

Architecture (per BUILD_PLAN): Claude is the HANDS, the extracted profiles are the
KNOWLEDGE that makes the output Venmo-specific. We build only the delta the model
can't do on its own — we don't teach it grammar, we inject *this brand's* voice and
*this audience's* tone as retrieved knowledge, then let it compose.

Composition is a controlled ablation in three layers:
    neutral  -> facts only, no knowledge base (brand-agnostic)
    +voice   -> apply the voice profile (HELD — identical across audiences)
    +tone    -> apply the tone profile for the audience/framing (FLEXED — diverges)

This is what produced library/generated_demo.json. The demo content was composed by
running this method inline through the model (Claude Code's own model IS the Claude
call). Point COMPOSE at the Anthropic API to regenerate headlessly.

Usage:
    python3 generate.py                # print the composition prompt for each event
    ANTHROPIC_API_KEY=... python3 generate.py --live   # call the API, rewrite demo json
"""
import json, os, sys

HOME = os.path.expanduser("~")
LIB = f"{HOME}/hemingway/library"
VOICE = json.load(open(f"{LIB}/venmo_voice_extracted.json"))
TONE = json.load(open(f"{LIB}/tone_profiles.json"))
DEMO = json.load(open(f"{LIB}/generated_demo.json"))


def voice_knowledge():
    ps = "\n".join(f"- {p['principle']}" for p in VOICE["voice_principles"])
    avoid = "\n".join(f"- {a}" for a in VOICE["avoid"])
    fp = VOICE["fingerprint"]
    return (f"VENMO VOICE (constant — who the brand is; HELD across every audience):\n{ps}\n\n"
            f"Fingerprint: {fp['second_person_you_pct']}% second-person, ~{fp['avg_words']} words/line, "
            f"{fp['contraction_pct']}% contractions, exclamation only {fp['exclamation_pct']}%.\n\n"
            f"Avoid:\n{avoid}")


def tone_knowledge(audience):
    prof = TONE.get(audience)
    if not prof:
        return ""
    fp = prof["facet_profile"]
    tone_vals = ", ".join(fp["tone"]["dominant"])
    closers = list(prof["closer_tells"]["all_closers"].values())
    ex = "\n".join(f'  - "{c}"' for c in closers[:3])
    return (f"{audience.upper()} TONE (flexes — how the voice bends for this reader):\n"
            f"- register: {tone_vals}\n"
            f"- framing: {'guardian named as actor; speak TO the teen; may defer up to a guardian' if audience=='teen' else 'the reader is the actor (overseer); speak ABOUT the teen; adult-to-adult'}\n"
            f"- closer tells (sign-offs carry the tone):\n{ex}")


def compose_prompt(facts, audience):
    return (f"You are Hemingway, composing notification copy.\n\n"
            f"{voice_knowledge()}\n\n{tone_knowledge(audience)}\n\n"
            f"THE FACTS:\n{facts}\n\n"
            f"Write three versions of this message:\n"
            f"1. NEUTRAL — the facts only, plain, no brand voice, no warmth. Brand-agnostic.\n"
            f"2. +VOICE — apply the Venmo voice above, but keep tone flat (no audience flex).\n"
            f"3. +TONE — apply the voice AND the {audience} tone. This is the flexed version.\n"
            f"Keep each to 1-3 short sentences. Return JSON: {{neutral, voice, tone}}.")


def compose_live(facts, audience):
    """Call the Anthropic API. Requires `anthropic` + ANTHROPIC_API_KEY."""
    import anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=600,
        messages=[{"role": "user", "content": compose_prompt(facts, audience)}],
    )
    return msg.content[0].text


def main():
    live = "--live" in sys.argv
    for ev in DEMO["events"]:
        aud = ev["variants"][0]["key"] if ev["flex_axis"] == "framing" else "teen"
        print(f"\n===== {ev['label']}  (flex: {ev['flex_axis']}) =====")
        if live:
            print(compose_live(ev["facts"], aud))
        else:
            print(compose_prompt(ev["facts"], aud))
    if not live:
        print("\n(dry run — prints the composition prompt. The shipped generated_demo.json was "
              "composed via this method inline. Add --live + ANTHROPIC_API_KEY to call the API.)")


if __name__ == "__main__":
    main()
