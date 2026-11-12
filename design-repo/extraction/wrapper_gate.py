#!/usr/bin/env python3
"""Whole-page-wrapper quality gate (BASELINE R9). Called by verify_all.py; also runnable alone.

    python3 extraction/wrapper_gate.py

Inputs: extraction/measured-values.json -> sectionHeights["1440x900"] (measured by
extraction/measure_sections.mjs in a headless browser), extraction/wrapper-whitelist.json,
templates/templates.json and the section contracts (for categories).

Thresholds are pinned here in code, not read from JSON:
  HERO > 1800px: warn; HERO > 3000px: error unless whitelisted.
  one in-flow non-SHELL section > 50% of its page: warn; > 60%: error unless whitelisted
  (skipped for pages with fewer than 3 in-flow content sections; fixed/absolute/sticky
  elements take no page height and are not in-flow).
  Missing measurement for a template node that renders at 1440: error. Wrong viewport: error.
  Whitelist entries need reviewedBy, justification >= 30 chars and maxHeightPx above the
  measured height; stale/over-cap entries fail; a whitelisted hit still warns; an agent
  reviewer must say "agent attestation, not a human sign-off".
"""
import json
import os
import sys

sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VIEWPORT = "1440x900"
HERO_WARN_PX = 1800
HERO_ERROR_PX = 3000
SHARE_WARN = 0.50
SHARE_ERROR = 0.60
MIN_INFLOW_FOR_SHARE = 3
MIN_JUSTIFICATION = 30
AGENT_ATTESTATION = "agent attestation, not a human sign-off"
AGENT_WORDS = ("agent", "claude", "assistant", "automated")


def _load(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return json.load(f)


def load_inputs():
    mv = _load("extraction/measured-values.json")
    wl = _load("extraction/wrapper-whitelist.json")
    tpl = _load("templates/templates.json")["templates"]
    cats = {}
    for f in os.listdir(os.path.join(REPO, "sections")):
        if f.endswith(".json"):
            d = _load(f"sections/{f}")
            cats[d["id"]] = d["semantic"]["category"]
    return mv, wl, tpl, cats


def check(mv, whitelist, templates, categories):
    errors, warnings, info = [], [], []
    sh = (mv.get("sectionHeights") or {})
    if VIEWPORT not in sh:
        errors.append(f"sectionHeights has no {VIEWPORT} measurement (found {sorted(sh)})")
        return errors, warnings, info
    block = sh[VIEWPORT]
    if block.get("viewport") != VIEWPORT:
        errors.append(f"sectionHeights[{VIEWPORT}] was measured at viewport {block.get('viewport')!r}, not {VIEWPORT}")
    entries = {(e.get("template"), e.get("section")): e for e in whitelist.get("entries", [])}
    used = set()

    def whitelisted(tname, sid, height):
        e = entries.get((tname, sid))
        if not e:
            return False
        used.add((tname, sid))
        ok = True
        rb = str(e.get("reviewedBy") or "")
        if not rb:
            errors.append(f"whitelist {tname}/{sid}: missing reviewedBy"); ok = False
        elif any(w in rb.lower() for w in AGENT_WORDS) and AGENT_ATTESTATION not in rb:
            errors.append(f"whitelist {tname}/{sid}: agent reviewer must state '{AGENT_ATTESTATION}'"); ok = False
        if len(str(e.get("justification") or "")) < MIN_JUSTIFICATION:
            errors.append(f"whitelist {tname}/{sid}: justification shorter than {MIN_JUSTIFICATION} chars"); ok = False
        cap = e.get("maxHeightPx")
        if not isinstance(cap, (int, float)) or cap <= height:
            errors.append(f"whitelist {tname}/{sid}: maxHeightPx {cap} is not above the measured {height}px (stale or over-cap)"); ok = False
        return ok

    for tname, tdef in templates.items():
        page = block.get("templates", {}).get(tname)
        if page is None:
            errors.append(f"{tname}: no 1440px measurement")
            continue
        secs = page.get("sections", {})
        doc_h = page.get("documentHeightPx")
        if not isinstance(doc_h, (int, float)) or doc_h <= 0:
            errors.append(f"{tname}: documentHeightPx missing")
            continue
        inflow = []
        for n in tdef["nodes"]:
            sid = n["section"]
            m = secs.get(sid)
            if m is None:
                errors.append(f"{tname}/{sid}: missing measurement")
                continue
            if m.get("present") is False:
                if n.get("required"):
                    errors.append(f"{tname}/{sid}: required node not rendered at {VIEWPORT}")
                elif not m.get("reason"):
                    errors.append(f"{tname}/{sid}: absent at {VIEWPORT} without a recorded reason")
                continue
            h = m.get("heightPx")
            if not isinstance(h, (int, float)):
                errors.append(f"{tname}/{sid}: heightPx missing")
                continue
            cat = categories.get(sid, m.get("category"))
            if cat == "HERO":
                if h > HERO_ERROR_PX:
                    if whitelisted(tname, sid, h):
                        warnings.append(f"{tname}/{sid}: HERO {h}px > {HERO_ERROR_PX}px (whitelisted)")
                    else:
                        errors.append(f"{tname}/{sid}: HERO {h}px > {HERO_ERROR_PX}px")
                elif h > HERO_WARN_PX:
                    warnings.append(f"{tname}/{sid}: HERO {h}px > {HERO_WARN_PX}px")
            if m.get("inFlow") and cat != "SHELL":
                inflow.append((sid, h))
        if len(inflow) < MIN_INFLOW_FOR_SHARE:
            info.append(f"{tname}: {len(inflow)} in-flow content section(s) at {VIEWPORT}; share rule skipped")
            continue
        for sid, h in inflow:
            share = h / float(doc_h)
            if share > SHARE_ERROR:
                if whitelisted(tname, sid, h):
                    warnings.append(f"{tname}/{sid}: holds {share:.0%} of the page (whitelisted)")
                else:
                    errors.append(f"{tname}/{sid}: holds {share:.0%} of the page (> {SHARE_ERROR:.0%})")
            elif share > SHARE_WARN:
                warnings.append(f"{tname}/{sid}: holds {share:.0%} of the page (> {SHARE_WARN:.0%})")
    for key in entries:
        if key not in used:
            errors.append(f"whitelist entry {key[0]}/{key[1]} matches no gated hit (stale)")
    return errors, warnings, info


def main():
    errors, warnings, info = check(*load_inputs())
    for i in info:
        print(f"INFO  {i}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}")
    print(f"wrapper gate: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
