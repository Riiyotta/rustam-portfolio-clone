#!/usr/bin/env python3
"""Adversarial suite: every rule must reject a mutated instance; every control must pass.

    python3 schema/tests/adversarial_test.py          # run all, exit 1 on any miss
    python3 schema/tests/adversarial_test.py --count  # number of mutation cases (used for manifest counts)

Covers BUILD-GUIDE 2.8 (schema, structural, maxWords), BASELINE R1-R5 (mode + generated-mode leakage:
brand, store mark/URL, rating, person, URL, copy, CTA, proprietary media, logo), R8 (retrieval
eligibility at node / contract / allowlist level and a content section marked ineligible), R9 (wrapper
gate) and R10 (unknown token, raw colour, arbitrary spacing, unsupported font, restricted token, slot
and theme combinations). A case passes only when the expected rule id (and sub-code) is reported as an
error (or, for warn rules, as a warning that does not fail the page).
"""
import copy
import json
import os
import sys

sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "schema"))
sys.path.insert(0, os.path.join(REPO, "extraction"))
import semantic_validate as sv  # noqa: E402
import wrapper_gate as wg  # noqa: E402

EX = os.path.join(REPO, "schema", "examples")


def ex(name):
    with open(os.path.join(EX, name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def nodeidx(spec, sid):
    return [n["section"] for n in spec["nodes"]].index(sid)


def c(spec, sid):
    return spec["nodes"][nodeidx(spec, sid)]["content"]


CASES = []


def case(name, base, expect, sub=None, layer="all", severity="error", ctx_mut=None):
    def deco(fn):
        CASES.append({"name": name, "base": base, "mutate": fn, "expect": expect, "sub": sub, "layer": layer, "severity": severity, "ctx_mut": ctx_mut})
        return fn
    return deco


# ---------------- schema layer (R1 + BUILD-GUIDE 2.8) ----------------
@case("schema: unknown template", "generated.home", "SCHEMA")
def _(s): s["template"] = "landing"
@case("schema: mode missing (R1)", "generated.home", "SCHEMA")
def _(s): del s["mode"]
@case("schema: mode outside closed enum (R1)", "generated.home", "SCHEMA")
def _(s): s["mode"] = "draft"
@case("schema: wrong pageSpecVersion", "generated.home", "SCHEMA")
def _(s): s["pageSpecVersion"] = "0.9.0"
@case("schema: missing reducedMotionFallback", "generated.home", "SCHEMA")
def _(s): del s["nodes"][1]["motion"]["reducedMotionFallback"]
@case("schema: invented motion field", "generated.home", "SCHEMA")
def _(s): s["nodes"][1]["motion"]["inventedAnimation"] = "spin"
@case("schema: invented section type alias", "generated.home", "SCHEMA")
def _(s): s["nodes"][1]["section"] = "hero.marketing"
@case("schema: extra node property", "generated.home", "SCHEMA")
def _(s): s["nodes"][1]["className"] = "big"
@case("schema: extra content field", "generated.home", "SCHEMA")
def _(s): c(s, "content.intro-note")["subtitle"] = "extra"
@case("schema: invented asset role", "generated.home", "SCHEMA")
def _(s): c(s, "hero.intro")["portrait"]["assetRole"] = "logo.real"
@case("schema: rating field cannot be expressed (R2 rating leakage)", "generated.home", "SCHEMA")
def _(s): c(s, "content.intro-note")["rating"] = "4.9/5 from 120 clients"
@case("schema: theme outside enum", "generated.home", "SCHEMA")
def _(s): s["theme"] = "light"
@case("schema: malformed year", "generated.project-detail", "SCHEMA")
def _(s): c(s, "project.meta")["year"] = "twenty24"
@case("schema: required content field missing", "generated.project-detail", "SCHEMA")
def _(s): del c(s, "project.header")["description"]
@case("schema: unknown token slot", "generated.home", "SCHEMA")
def _(s): s["nodes"][0]["tokens"]["shadow"] = "effect.backdrop-blur"
@case("schema: utility section as node", "generated.home", "SCHEMA")
def _(s): s["nodes"].insert(1, {"section": "utility.preloader", "content": {}, "motion": {"pattern": "preloader-wipe", "reducedMotionFallback": "instant-hide"}})

# ---------------- structural / template cross-reference ----------------
@case("structure: duplicate navbar", "generated.home", "TEMPLATE_NODE_SEQUENCE", layer="semantic")
def _(s): s["nodes"].insert(1, copy.deepcopy(s["nodes"][0]))
@case("structure: required hero removed", "generated.home", "TEMPLATE_NODE_SEQUENCE", layer="semantic")
def _(s): s["nodes"].pop(nodeidx(s, "hero.intro"))
@case("structure: navbar moved after hero", "generated.home", "NAVBAR_FIRST", layer="semantic")
def _(s): s["nodes"][0], s["nodes"][1] = s["nodes"][1], s["nodes"][0]
@case("structure: template/node-sequence mismatch (about nodes declared as home)", "generated.about", "TEMPLATE_NODE_SEQUENCE", layer="semantic")
def _(s): s["template"] = "home"; s["route"] = "/"
@case("structure: home template on /about", "generated.home", "ROUTE_TEMPLATE_MATCH", layer="semantic")
def _(s): s["route"] = "/about"
@case("structure: 404 template on a real route", "generated.not-found", "ROUTE_TEMPLATE_MATCH", layer="semantic")
def _(s): s["route"] = "/about"
@case("structure: footer not last", "generated.home", "FOOTER_LAST", layer="semantic")
def _(s): f = s["nodes"].pop(); s["nodes"].insert(2, f)
@case("structure: hero on a project page", "generated.project-detail", "HERO_HOME_ONLY", layer="semantic")
def _(s): s["nodes"].insert(1, copy.deepcopy(ex("generated.home")["nodes"][1]))
@case("structure: two heroes", "generated.home", "ONE_HERO", layer="semantic")
def _(s): s["nodes"].insert(2, copy.deepcopy(s["nodes"][1]))
@case("structure: adjacent duplicate", "generated.home", "NO_ADJACENT_DUPLICATE", layer="semantic")
def _(s): s["nodes"].insert(3, copy.deepcopy(s["nodes"][3]))
@case("structure: runtime layer not allowed on template", "generated.not-found", "RUNTIME_LAYER_ALLOWED", layer="semantic")
def _(s): s["runtimeLayers"] = ["utility.page-transition", "utility.hover-title"]

# ---------------- R8 retrieval eligibility ----------------
@case("R8 node level: utility section used as a node (semantic layer)", "generated.home", "UTILITY_NOT_A_NODE", layer="semantic")
def _(s): s["nodes"].insert(1, {"section": "utility.kinetic-cursor", "content": {}, "motion": {"pattern": "kinetic-cursor", "reducedMotionFallback": "snap-follow"}})


def _flip_contract(ctx):
    ctx["sections"]["utility.preloader"]["retrievalEligible"] = True


def _flip_allowlist(ctx):
    for e in ctx["allowlist"]["entries"]:
        if e["id"] == "utility.toast":
            e["retrievalEligible"] = True


def _content_ineligible(ctx):
    ctx["sections"]["portfolio.work-index"]["retrievalEligible"] = False


def _both(ctx):
    _flip_contract(ctx)
    for e in ctx["allowlist"]["entries"]:
        if e["id"] == "utility.preloader":
            e["retrievalEligible"] = True


@case("R8 contract level: preloader flipped to eligible", "generated.home", "RETRIEVAL_PIN", layer="semantic", ctx_mut=_flip_contract)
def _(s): pass
@case("R8 allowlist level: toast flipped to eligible", "generated.home", "RETRIEVAL_PIN", layer="semantic", ctx_mut=_flip_allowlist)
def _(s): pass
@case("R8 contract+allowlist flipped together", "generated.home", "RETRIEVAL_PIN", layer="semantic", ctx_mut=_both)
def _(s): pass
@case("R8 content section marked ineligible", "generated.home", "RETRIEVAL_PIN", layer="semantic", ctx_mut=_content_ineligible)
def _(s): pass

# ---------------- motion ----------------
@case("motion: pattern not allowed for section", "generated.home", "MOTION_PATTERN_ALLOWED", layer="semantic")
def _(s): s["nodes"][1]["motion"] = {"pattern": "floating-digits", "reducedMotionFallback": "static-digits"}
@case("motion: fallback not the pinned one", "generated.home", "MOTION_FALLBACK_PINNED", layer="semantic")
def _(s): s["nodes"][1]["motion"]["reducedMotionFallback"] = "none"
def _scene_budget(ctx):
    # treat the word-reveal pattern as a scene so a valid home page carries 3 "scenes"
    ctx["graph"]["webglScenePatterns"] = list(ctx["graph"]["webglScenePatterns"]) + ["word-reveal"]


@case("motion: scene budget exceeded is warned, not fatal", "generated.home", "MOTION_BUDGET_WEBGL", layer="semantic", severity="warn", ctx_mut=_scene_budget)
def _(s): pass

# ---------------- maxWords ----------------
@case("maxWords: intro note overflow", "generated.home", "MAX_WORDS")
def _(s): c(s, "content.intro-note")["text"] = " ".join(["word"] * 60)
@case("maxWords: project description overflow", "generated.project-detail", "MAX_WORDS")
def _(s): c(s, "project.header")["description"] = " ".join(["line"] * 90)
@case("maxWords: hero line overflow", "generated.home", "MAX_WORDS")
def _(s): c(s, "hero.intro")["headingLines"][0] = "ONE TWO THREE FOUR FIVE SIX"
@case("maxWords: work item title overflow (nested list object)", "generated.home", "MAX_WORDS")
def _(s): c(s, "portfolio.work-index")["items"][0]["title"] = "a very long project title here"

# ---------------- R10 token policy ----------------
@case("R10 unknown token", "generated.home", "TOKEN_POLICY", sub="unknown-token")
def _(s): s["nodes"][0]["tokens"]["textColor"] = "text.brand-accent"
@case("R10 raw hex colour", "generated.home", "TOKEN_POLICY", sub="raw-value")
def _(s): s["nodes"][0]["tokens"]["textColor"] = "#ff0066"
@case("R10 raw rgb colour", "generated.home", "TOKEN_POLICY", sub="raw-value")
def _(s): s["nodes"][0]["tokens"]["surface"] = "rgb(14, 16, 12)"
@case("R10 arbitrary spacing", "generated.home", "TOKEN_POLICY", sub="raw-value")
def _(s): s["nodes"][1]["tokens"]["spacing"] = "13px"
@case("R10 unsupported font", "generated.home", "TOKEN_POLICY", sub="unsupported-font")
def _(s): s["nodes"][0]["tokens"]["fontFamily"] = "Comic Sans MS"
@case("R10 restricted shader token", "generated.home", "TOKEN_POLICY", sub="restricted")
def _(s): s["nodes"][0]["tokens"]["surface"] = "color.gl.transition-a"
@case("R10 token in the wrong slot", "generated.home", "TOKEN_POLICY", sub="slot")
def _(s): s["nodes"][0]["tokens"]["textColor"] = "surface.page"
@case("R10 invalid theme/token combination (semantic layer)", "generated.home", "TOKEN_POLICY", sub="theme", layer="semantic")
def _(s): s["theme"] = "light"

# ---------------- R2/R5 generated-mode leakage ----------------
@case("R5 brand: source wordmark in meta title", "generated.home", "GENERATED_MODE_BRAND")
def _(s): s["meta"]["title"] = "Kerimov Designs portfolio"
@case("R5 brand: source domain spelling", "generated.home", "GENERATED_MODE_BRAND")
def _(s): c(s, "content.intro-note")["text"] = "Visit kerimovdesigns for more drawings and posters."
@case("R5 logo: source wordmark role", "generated.home", "GENERATED_MODE_LOGO")
def _(s): c(s, "hero.intro")["portrait"] = {"assetRole": "brand.wordmark-source", "src": "generated://wordmark", "alt": ""}
@case("R5 store mark/URL leakage", "generated.home", "GENERATED_MODE_URL")
def _(s): c(s, "shell.navbar")["contactLinks"].append({"label": "App Store", "href": "https://apps.apple.com/app/id123", "kind": "external"})
@case("R5 review/rating leakage via copy", "generated.home", "GENERATED_MODE_PERSON")
def _(s): c(s, "content.intro-note")["text"] = "Rated five stars by Jonas Nygaard and many happy clients across the region."
@case("R5 person: owner name", "generated.home", "GENERATED_MODE_PERSON")
def _(s): c(s, "shell.navbar")["ownerName"] = "Rustam Kerimov"
@case("R5 person: real contact email", "generated.home", "GENERATED_MODE_PERSON")
def _(s): c(s, "shell.navbar")["contactLinks"][0]["href"] = "mailto:rustam-98@hotmail.com"
@case("R5 person: real location", "generated.home", "GENERATED_MODE_PERSON")
def _(s): c(s, "shell.navbar")["location"] = "Oslo, Norway"
@case("R5 person: real age fact", "generated.about", "GENERATED_MODE_PERSON")
def _(s): c(s, "about.footer-meta")["facts"] = ["Harbor City", "Age: 27"]
@case("R5 source URL: social profile", "generated.home", "GENERATED_MODE_URL")
def _(s): c(s, "shell.navbar")["contactLinks"][1]["href"] = "https://www.instagram.com/kerimov.designs/"
@case("R5 source URL: credit link", "generated.home", "GENERATED_MODE_URL")
def _(s): c(s, "shell.footer-contact")["credit"]["href"] = "https://www.jonasnygaard.com"
@case("R5 URL: non-placeholder domain", "generated.home", "GENERATED_MODE_URL")
def _(s): c(s, "shell.footer-contact")["credit"]["href"] = "https://northwind-web.com"
@case("R5 URL: media host of the source", "generated.home", "GENERATED_MODE_URL")
def _(s): c(s, "hero.intro")["portrait"]["src"] = "generated://x?from=https://utfs.io/f/abc"
@case("R5 source copy: hero heading", "generated.home", "GENERATED_MODE_COPY")
def _(s): c(s, "hero.intro")["headingLines"] = ["GRAPHIC DESIGNER", "CRAFTING VISUAL IDENTITIES,", "TYPOGRAPHY AND MOTION."]
@case("R5 source copy: intro note paraphrase keeps a 5-word run", "generated.home", "GENERATED_MODE_COPY")
def _(s): c(s, "content.intro-note")["text"] = "Browse freely. I'm always open to new projects, fresh ideas and more."
@case("R5 source copy: About discipline text", "generated.about", "GENERATED_MODE_COPY")
def _(s): c(s, "about.profile-header")["intro"] = "Building distinctive visual systems that give brands a clear voice."
@case("R5 source copy: 404 text", "generated.not-found", "GENERATED_MODE_COPY")
def _(s): c(s, "notfound.message")["heading"] = "This page got lost."
@case("R5 source CTA: copy-email label", "generated.home", "GENERATED_MODE_CTA")
def _(s): c(s, "shell.navbar")["contactLinks"][0]["label"] = "Copy Email"
@case("R5 source CTA: 404 back link", "generated.not-found", "GENERATED_MODE_CTA")
def _(s): c(s, "notfound.message")["backLinkLabel"] = "Back to portfolio"
@case("R5 source CTA: interaction hint", "generated.project-detail", "GENERATED_MODE_CTA")
def _(s): c(s, "project.footer-bar")["hint"] = "Scroll or click to explore"
@case("R5 project: real project title", "generated.home", "GENERATED_MODE_PROJECT")
def _(s): c(s, "portfolio.work-index")["items"][0]["title"] = "Kistefos museum"
@case("R5 project: generic real title by equality", "generated.home", "GENERATED_MODE_PROJECT")
def _(s): c(s, "portfolio.work-index")["items"][1]["title"] = "Art Exhibition"
@case("R5 project: real project id in a link", "generated.home", "GENERATED_MODE_PROJECT")
def _(s): c(s, "portfolio.work-index")["items"][0]["href"] = "/project/6aefb39eda2cd8ea85237d26"
@case("R5 media: owner portrait file under a safe role", "generated.home", "GENERATED_MODE_ASSET")
def _(s): c(s, "hero.intro")["portrait"]["src"] = "/rk-portrait.jpg"
@case("R5 media: owner portrait role", "generated.about", "GENERATED_MODE_ASSET")
def _(s): c(s, "about.media-stage")["media"][0]["asset"] = {"assetRole": "person.portrait-source", "src": "generated://p", "alt": ""}
@case("R5 media: real project cover role", "generated.project-detail", "GENERATED_MODE_ASSET")
def _(s): c(s, "project.media-stage")["media"][0]["asset"]["assetRole"] = "project.cover-source"
@case("R5 media: real project video path", "generated.project-detail", "GENERATED_MODE_ASSET")
def _(s): c(s, "project.media-stage")["media"][2]["asset"]["src"] = "/projects/videos/hhEReYBoKW7ERrThgMtwlh6JCLoKVqaQF7GDNYjf824cSO5z.mp4"
@case("R5 media: discipline video file name", "generated.about", "GENERATED_MODE_ASSET")
def _(s): c(s, "about.media-stage")["media"][2]["asset"]["src"] = "generated://bylarm-new.mp4"
@case("asset: section-disallowed role in work index", "generated.home", "ASSET_ROLE_ALLOWED", layer="semantic")
def _(s): c(s, "portfolio.work-index")["items"][0]["cover"]["assetRole"] = "scene.procedural-digits"
@case("reference: source role pointed at a placeholder", "reference.home", "REFERENCE_ASSET_SOURCE", layer="semantic")
def _(s): c(s, "hero.intro")["portrait"]["src"] = "placeholder://portrait"


# ---------------- R3 pins (registry edit cannot loosen) ----------------
def _loosen_registry(ctx):
    ctx["roles"]["person.portrait-source"]["availability"] = "generation-safe"


def _policy_value(ctx):
    ctx["roles"]["brand.wordmark-source"]["generationPolicy"] = "must-reuse-exact"


@case("R3 registry loosened: portrait made generation-safe (pin still blocks)", "generated.about", "ASSET_AVAILABILITY_PIN", layer="semantic", ctx_mut=_loosen_registry)
def _(s): c(s, "about.media-stage")["media"][0]["asset"] = {"assetRole": "person.portrait-source", "src": "generated://p", "alt": ""}
@case("R3 wordmark policy changed to a different valid value", "generated.home", "ASSET_AVAILABILITY_PIN", layer="semantic", ctx_mut=_policy_value)
def _(s): pass

# ---------------- R9 wrapper gate ----------------
GATE_CASES = []


def gate_case(name, expect):
    def deco(fn):
        GATE_CASES.append({"name": name, "mutate": fn, "expect": expect})
        return fn
    return deco


def _gate_inputs():
    mv, wl, tpl, cats = wg.load_inputs()
    return copy.deepcopy(mv), copy.deepcopy(wl), copy.deepcopy(tpl), dict(cats)


def _home(mv):
    return mv["sectionHeights"]["1440x900"]["templates"]["home"]


def _inflow_home(mv, hero, work, footer, doc):
    h = _home(mv)
    h["documentHeightPx"] = doc
    h["sections"]["hero.intro"].update({"heightPx": hero, "inFlow": True})
    h["sections"]["content.intro-note"].update({"heightPx": 100, "inFlow": True})
    h["sections"]["portfolio.work-index"].update({"heightPx": work, "inFlow": True})
    h["sections"]["shell.footer-contact"] = {"heightPx": footer, "inFlow": True, "position": "static", "category": "SHELL"}


@gate_case("R9 HERO 1900px warns", "warn")
def _(mv, wl, tpl, cats): _home(mv)["sections"]["hero.intro"]["heightPx"] = 1900
@gate_case("R9 HERO 3100px fails", "error")
def _(mv, wl, tpl, cats): _home(mv)["sections"]["hero.intro"]["heightPx"] = 3100
@gate_case("R9 one in-flow section holds 70% of the page fails", "error")
def _(mv, wl, tpl, cats): _inflow_home(mv, 300, 2800, 300, 4000)
@gate_case("R9 one in-flow section holds 55% of the page warns", "warn")
def _(mv, wl, tpl, cats): _inflow_home(mv, 900, 2200, 300, 4000)
@gate_case("R9 whitelist without justification fails", "error")
def _(mv, wl, tpl, cats):
    _home(mv)["sections"]["hero.intro"]["heightPx"] = 3100
    wl["entries"] = [{"template": "home", "section": "hero.intro", "reviewedBy": "design lead", "justification": "ok", "maxHeightPx": 3200}]
@gate_case("R9 agent reviewer without attestation fails", "error")
def _(mv, wl, tpl, cats):
    _home(mv)["sections"]["hero.intro"]["heightPx"] = 3100
    wl["entries"] = [{"template": "home", "section": "hero.intro", "reviewedBy": "claude agent", "justification": "a long enough justification for the test case", "maxHeightPx": 3200}]
@gate_case("R9 stale whitelist cap fails", "error")
def _(mv, wl, tpl, cats):
    _home(mv)["sections"]["hero.intro"]["heightPx"] = 3100
    wl["entries"] = [{"template": "home", "section": "hero.intro", "reviewedBy": "design lead", "justification": "a long enough justification for the test case", "maxHeightPx": 3000}]
@gate_case("R9 missing measurement fails", "error")
def _(mv, wl, tpl, cats): del _home(mv)["sections"]["portfolio.work-index"]
@gate_case("R9 measured at the wrong viewport fails", "error")
def _(mv, wl, tpl, cats): mv["sectionHeights"]["1440x900"]["viewport"] = "1280x800"
@gate_case("R9 no 1440 block at all fails", "error")
def _(mv, wl, tpl, cats): mv["sectionHeights"] = {"1280x800": mv["sectionHeights"]["1440x900"]}


def run_case(k, ctx0):
    spec = ex(k["base"])
    k["mutate"](spec)
    ctx = copy.deepcopy(ctx0)
    if k["ctx_mut"]:
        k["ctx_mut"](ctx)
    fs = sv.validate(spec, ctx, schema_layer=(k["layer"] != "semantic"))
    if k["layer"] == "schema":
        fs = [f for f in fs if f["rule"] == "SCHEMA"]
    hits = [f for f in fs if f["rule"] == k["expect"] and (k["sub"] is None or f"[{k['sub']}]" in f["message"])]
    if k["severity"] == "warn":
        ok = any(f["severity"] == "warn" for f in hits) and not sv.errors_of(fs)
    else:
        ok = any(f["severity"] == "error" for f in hits)
    return ok, hits, fs


def main(argv):
    if "--count" in argv:
        print(len(CASES) + len(GATE_CASES))
        return 0
    ctx0 = sv.load_context()
    control_fail, misses = 0, 0
    n_controls = len([f for f in os.listdir(EX) if f.endswith(".json")]) + 1
    print("controls (must produce zero errors):")
    for f in sorted(os.listdir(EX)):
        if f.endswith(".json"):
            fs = sv.validate(ex(f[:-5]), ctx0)
            e = sv.errors_of(fs)
            control_fail += bool(e)
            print(f"  {'PASS' if not e else 'FAIL'}  control {f}" + ("" if not e else f"  -> {e[:2]}"))
    errs, warns, _ = wg.check(*_gate_inputs())
    control_fail += bool(errs)
    print(f"  {'PASS' if not errs else 'FAIL'}  control wrapper gate on the real measurements ({len(errs)} errors, {len(warns)} warnings)")
    print("mutations (each must be rejected by the named rule):")
    for k in CASES:
        ok, hits, fs = run_case(k, ctx0)
        misses += not ok
        tag = k["expect"] + (f"[{k['sub']}]" if k["sub"] else "")
        print(f"  {'PASS' if ok else 'MISS'}  {k['name']}  -> {tag}" + ("" if ok else f"  got {[(f['rule'], f['message'][:60]) for f in fs][:4]}"))
    for g in GATE_CASES:
        mv, wl, tpl, cats = _gate_inputs()
        g["mutate"](mv, wl, tpl, cats)
        e, w, _ = wg.check(mv, wl, tpl, cats)
        ok = bool(e) if g["expect"] == "error" else (bool(w) and not e)
        misses += not ok
        print(f"  {'PASS' if ok else 'MISS'}  {g['name']}  -> wrapper gate {g['expect']}" + ("" if ok else f"  got errors={e[:2]} warnings={w[:2]}"))
    total = len(CASES) + len(GATE_CASES)
    print(f"\nadversarial: {total - misses}/{total} mutations rejected as expected; controls {n_controls - control_fail}/{n_controls} pass")
    return 1 if (misses or control_fail) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
