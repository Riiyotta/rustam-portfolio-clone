#!/usr/bin/env python3
"""One-shot verification of this design-repo. Exit 1 on any FAIL; WARNs do not fail.

    python3 extraction/verify_all.py
    python3 extraction/verify_all.py --quiet     # only the summary and non-PASS lines

The repo root is derived from this file's location. Evidence citations with root=project resolve
against the folder that contains design-repo/ (src/, public/, index.html); when that folder is absent
(design-repo used alone) those checks degrade to WARN, everything else still runs.
Every check below is proven to fail on injected drift by extraction/prove_drift.py.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.dirname(REPO)
sys.path.insert(0, os.path.join(REPO, "extraction"))
sys.path.insert(0, os.path.join(REPO, "schema"))

# ---- pins (independent of the registries; must equal schema/semantic_validate.py) ----
PINNED_AVAILABILITY = {
    "person.portrait-source": "blocked-for-generation",
    "brand.wordmark-source": "blocked-for-generation",
    "brand.favicon-source": "blocked-for-generation",
    "project.cover-source": "reference-only",
    "project.gallery-source": "reference-only",
    "project.video-source": "reference-only",
    "discipline.media-source": "reference-only",
    "scene.procedural-digits": "generation-safe",
    "brand.wordmark-placeholder": "generation-safe",
    "person.portrait-fictional": "generation-safe",
    "project.cover-generated": "generation-safe",
    "project.gallery-generated": "generation-safe",
    "project.video-generated": "generation-safe",
    "discipline.media-generated": "generation-safe",
    "media.placeholder": "generation-safe",
    "link.placeholder-url": "generation-safe",
    "copy.original": "generation-safe",
    "rating.placeholder": "generation-safe",
}
RETRIEVAL_INELIGIBLE = {
    "utility.preloader", "utility.kinetic-cursor", "utility.page-transition",
    "utility.overlay-backdrop", "utility.hover-title", "utility.toast",
}
RUNTIME_UI_WORDS = re.compile(r"preloader|loader|cursor|transition|backdrop|toast|modal|dialog|drawer|overlay|tooltip|hover-title|banner|consent|lightbox|popup|utility\.", re.I)
PARITY_GATE = 0.80
PARITY_RUN_TOLERANCE = 0.02

RESULTS = []
QUIET = "--quiet" in sys.argv


def rec(check, status, msg):
    RESULTS.append((check, status, msg))


def J(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return json.load(f)


def project_present():
    return os.path.isfile(os.path.join(PROJECT, "src", "engine", "chunks", "272.js"))


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def all_json():
    out = []
    for d, dirs, fs in os.walk(REPO):
        dirs[:] = [x for x in dirs if x not in ("__pycache__",)]
        for f in fs:
            if f.endswith(".json"):
                out.append(os.path.relpath(os.path.join(d, f), REPO))
    return sorted(out)


def sections():
    return {J(f"sections/{f}")["id"]: J(f"sections/{f}") for f in sorted(os.listdir(os.path.join(REPO, "sections"))) if f.endswith(".json")}


# ------------------------------------------------------------------------------------------
def check_json_parse():
    bad = []
    for rel in all_json():
        try:
            J(rel)
        except Exception as e:  # noqa
            bad.append(f"{rel}: {e}")
    rec("JSON_PARSE", "FAIL" if bad else "PASS", bad[:3] if bad else f"{len(all_json())} JSON files parse")


def check_section_contracts():
    import jsonschema
    sch = J("schema/section-contract.schema.json")
    jsonschema.Draft7Validator.check_schema(sch)
    v = jsonschema.Draft7Validator(sch)
    probs = []
    for sid, s in sections().items():
        for e in v.iter_errors(s):
            probs.append(f"{sid}: {e.message[:120]}")
        if s["semantic"]["id"] != sid:
            probs.append(f"{sid}: semantic.id {s['semantic']['id']} != id")
        if s["source"]["id"] == sid:
            probs.append(f"{sid}: source.id must differ from the semantic id")
        if s["retrievalEligible"] is False and len(s.get("retrievalIneligibleReason", "")) < 30:
            probs.append(f"{sid}: retrievalIneligibleReason < 30 chars")
        if s["semantic"]["category"] == "HERO" and not s["constraints"].get("onePerPage"):
            probs.append(f"{sid}: HERO must be onePerPage")
    rec("SECTION_CONTRACTS", "FAIL" if probs else "PASS", probs[:4] if probs else f"{len(sections())} contracts valid against schema/section-contract.schema.json; source/semantic split holds")


def check_allowlist_parity():
    allow = J("tokens/llm/component-allowlist.json")
    files = {}
    for kind, d in (("section", "sections"), ("primitive", "primitives"), ("component", "components")):
        for f in os.listdir(os.path.join(REPO, d)):
            if f.endswith(".json"):
                files[J(f"{d}/{f}")["id"]] = (kind, f"{d}/{f}")
    ids = {e["id"]: e for e in allow["entries"]}
    probs = [f"phantom allowlist entry {i}" for i in ids if i not in files]
    probs += [f"contract {i} has no allowlist entry" for i in files if i not in ids]
    secs = sections()
    for i, e in ids.items():
        if i in files:
            if e.get("kind") != files[i][0] or e.get("file") != files[i][1]:
                probs.append(f"{i}: allowlist kind/file {e.get('kind')}/{e.get('file')} != {files[i]}")
        if i in secs:
            s = secs[i]
            if sorted(e.get("contentFields", [])) != sorted(s["content"]["fields"]):
                probs.append(f"{i}: allowlist contentFields drifted from the contract")
            if e.get("motionPatterns") != s["motion"]["patterns"]:
                probs.append(f"{i}: allowlist motionPatterns drifted")
            if e.get("generatedAssetRoles") != s["generatedAssetRoles"]:
                probs.append(f"{i}: allowlist generatedAssetRoles drifted")
    sch = J("schema/pagespec.schema.json")
    node_props = sorted(sch["definitions"]["node"]["properties"])
    if node_props != sorted(allow["nodeSettableProperties"]):
        probs.append(f"nodeSettableProperties {allow['nodeSettableProperties']} != schema node properties {node_props}")
    rec("ALLOWLIST_PARITY", "FAIL" if probs else "PASS", probs[:4] if probs else f"{len(ids)} allowlist entries == {len(files)} contract files; node settable properties match the schema")


def check_retrieval_pin():
    import semantic_validate as sv
    probs = []
    if set(sv.RETRIEVAL_INELIGIBLE) != RETRIEVAL_INELIGIBLE:
        probs.append("RETRIEVAL_INELIGIBLE differs between verify_all.py and semantic_validate.py")
    secs = sections()
    allow = {e["id"]: e for e in J("tokens/llm/component-allowlist.json")["entries"]}
    for sid, s in secs.items():
        pinned_false = sid in RETRIEVAL_INELIGIBLE
        if s["retrievalEligible"] is pinned_false:
            probs.append(f"{sid}: contract retrievalEligible={s['retrievalEligible']} contradicts the pin")
        if sid in allow and allow[sid].get("retrievalEligible") is pinned_false:
            probs.append(f"{sid}: allowlist retrievalEligible contradicts the pin")
        if (RUNTIME_UI_WORDS.search(sid) or RUNTIME_UI_WORDS.search(s.get("title", ""))) and not pinned_false:
            probs.append(f"{sid}: looks like runtime UI but is not pinned retrieval-ineligible")
    for sid in RETRIEVAL_INELIGIBLE:
        if sid not in secs:
            probs.append(f"pinned {sid} has no contract")
    sch_nodes = set(J("schema/pagespec.schema.json")["definitions"]["node"]["properties"]["section"]["enum"])
    if sch_nodes & RETRIEVAL_INELIGIBLE:
        probs.append(f"schema node enum admits runtime UI {sorted(sch_nodes & RETRIEVAL_INELIGIBLE)}")
    if sch_nodes != {s for s in secs if s not in RETRIEVAL_INELIGIBLE}:
        probs.append("schema node section enum != retrievable contracts")
    rec("RETRIEVAL_PIN", "FAIL" if probs else "PASS", probs[:4] if probs else f"{len(RETRIEVAL_INELIGIBLE)} runtime sections pinned ineligible in both scripts; contracts, allowlist and schema agree")


def check_asset_pins():
    import semantic_validate as sv
    reg = J("assets/asset-roles.json")
    roles = reg["roles"]
    probs = []
    if sv.PINNED_AVAILABILITY != PINNED_AVAILABILITY:
        probs.append("PINNED_AVAILABILITY differs between verify_all.py and semantic_validate.py")
    for r, d in roles.items():
        if r not in PINNED_AVAILABILITY:
            probs.append(f"role {r} not pinned")
        elif d.get("availability") != PINNED_AVAILABILITY[r]:
            probs.append(f"role {r}: registry {d.get('availability')} != pin {PINNED_AVAILABILITY[r]}")
        if d.get("availability") not in reg["availabilityEnum"]:
            probs.append(f"role {r}: availability outside the closed enum")
        if d.get("availability") in ("reference-only", "blocked-for-generation"):
            subs = d.get("generationSafeSubstitutes") or []
            if not subs:
                probs.append(f"role {r}: no generationSafeSubstitutes")
            for x in subs:
                if PINNED_AVAILABILITY.get(x) != "generation-safe":
                    probs.append(f"role {r}: substitute {x} is not generation-safe")
            if d.get("generationPolicy") == "must-reuse-exact":
                probs.append(f"role {r}: a source role is must-reuse-exact")
        if r in sv.PINNED_POLICY and d.get("generationPolicy") != sv.PINNED_POLICY[r]:
            probs.append(f"role {r}: generationPolicy {d.get('generationPolicy')} != pinned {sv.PINNED_POLICY[r]}")
    for r in PINNED_AVAILABILITY:
        if r not in roles:
            probs.append(f"pinned role {r} missing from registry")
    enum = J("schema/pagespec.schema.json")["definitions"]["assetRole"]["enum"]
    if sorted(enum) != sorted(roles):
        probs.append("schema assetRole enum != registry roles")
    for sid, s in sections().items():
        for r in s["generatedAssetRoles"]:
            if PINNED_AVAILABILITY.get(r) != "generation-safe":
                probs.append(f"{sid}: generatedAssetRoles lists non-generation-safe {r}")
    rec("ASSET_PINS", "FAIL" if probs else "PASS", probs[:4] if probs else f"{len(roles)} roles match PINNED_AVAILABILITY in both scripts; substitutes generation-safe; schema enum in sync")


def iter_citations(obj):
    if isinstance(obj, dict):
        if {"root", "file", "lines", "tag"} <= set(obj) and all(isinstance(obj[k], str) for k in ("root", "file", "lines", "tag")):
            yield obj
        for v in obj.values():
            yield from iter_citations(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from iter_citations(v)


def check_citations():
    probs, checked, skipped = [], 0, 0
    cache = {}
    have_project = project_present()
    for rel in all_json():
        for c in iter_citations(J(rel)):
            base = PROJECT if c["root"] == "project" else REPO
            if c["root"] == "project" and not have_project:
                skipped += 1
                continue
            path = os.path.join(base, c["file"])
            if not os.path.isfile(path):
                probs.append(f"{rel}: cited file missing {c['file']}")
                continue
            if path not in cache:
                with open(path, encoding="utf-8") as f:
                    cache[path] = f.read().split("\n")
            lines = cache[path]
            m = re.match(r"^(\d+)(?:-(\d+))?$", c["lines"])
            if not m:
                probs.append(f"{rel}: bad range {c['lines']}")
                continue
            a, b = int(m.group(1)), int(m.group(2) or m.group(1))
            if a < 1 or b < a or b > len(lines):
                probs.append(f"{rel}: {c['file']}:{c['lines']} outside 1-{len(lines)}")
                continue
            if not any(c["tag"] in l for l in lines[a - 1:b]):
                probs.append(f"{rel}: tag {c['tag'][:50]!r} not found in {c['file']}:{c['lines']}")
                continue
            checked += 1
    if probs:
        rec("CITATIONS", "FAIL", probs[:4] + [f"... {len(probs)} total"])
    elif skipped:
        rec("CITATIONS", "WARN", f"{checked} repo citations verified; {skipped} citations into the source project skipped (design-repo used alone: no ../src)")
    else:
        rec("CITATIONS", "PASS", f"{checked} citations re-read: every range exists and contains its tag")


def check_css_pin():
    mv = J("extraction/measured-values.json")["cssExcerpt"]
    ex_path = os.path.join(REPO, mv["excerpt"])
    probs = []
    if sha(ex_path) != mv["excerptSha256"]:
        probs.append("excerpt sha256 != measured-values.cssExcerpt.excerptSha256")
    src = os.path.join(PROJECT, mv["source"])
    if not os.path.isfile(src):
        rec("CSS_PIN", "FAIL" if probs else "WARN", probs or f"{mv['source']} not present (design-repo alone): source hash not re-checked; excerpt hash OK")
        return
    if sha(src) != mv["sourceSha256"]:
        probs.append(f"{mv['source']} sha256 {sha(src)[:12]} != pinned {mv['sourceSha256'][:12]} (source moved: rebuild)")
    raw = open(src, encoding="utf-8").read()
    text = open(ex_path, encoding="utf-8").read()
    n = 0
    for sel, body in re.findall(r"^([^\s/:][^{\n]*?) \{\n((?:  [^\n]*;\n)+)\}", text, re.M):
        decls = [d.strip()[:-1] for d in body.strip().split("\n")]
        if sel == ":root":
            for d in decls:
                n += 1
                if d not in raw:
                    probs.append(f"excerpt declaration not in source: {d[:60]}")
        else:
            mini = sel + "{" + ";".join(decls) + "}"
            n += 1
            if mini not in raw:
                probs.append(f"excerpt rule not in source: {sel}")
    for media in re.findall(r"^(@media [^{]+) \{ /\* \.\.\. \*/ \}", text, re.M):
        n += 1
        if media not in raw:
            probs.append(f"media query not in source: {media}")
    rec("CSS_PIN", "FAIL" if probs else "PASS", probs[:4] if probs else f"source sha256 pinned; {n} excerpt rules/declarations/queries found verbatim in the minified source")


def flatten_tokens():
    flat = {}

    def walk(prefix, node, layer, path):
        if isinstance(node, dict) and "$value" in node:
            flat[prefix] = {"layer": layer, "type": node["$type"], "value": node["$value"], "file": path, "restricted": node.get("restricted")}
            return
        if isinstance(node, dict):
            for k, v in node.items():
                if k.startswith("$") or k == "evidence":
                    continue
                walk(f"{prefix}.{k}" if prefix else k, v, layer, path)
    for layer in ("00-foundation", "10-semantic", "20-component", "30-layout"):
        d = os.path.join(REPO, "tokens", layer)
        for f in sorted(os.listdir(d)):
            if f.endswith(".json") and f != "motion-patterns.json":
                rel = f"tokens/{layer}/{f}"
                walk({"20-component": "component"}.get(layer, ""), J(rel), layer, rel)
    return flat


def check_token_catalog():
    flat = flatten_tokens()
    cat = J("tokens/llm/token-catalog.json")["tokens"]
    probs = [f"catalog missing {k}" for k in flat if k not in cat] + [f"catalog has phantom {k}" for k in cat if k not in flat]
    for k, t in flat.items():
        if k in cat and (cat[k]["value"] != t["value"] or cat[k]["type"] != t["type"] or cat[k].get("restricted") != t["restricted"]):
            probs.append(f"catalog {k} drifted from {t['file']}")
    # every semantic/component reference resolves; theme resolves them all
    dark = J("tokens/themes/dark.json")["resolves"]

    def resolve(v):
        if isinstance(v, str) and v.startswith("{") and v.endswith("}"):
            return resolve(flat[v[1:-1]]["value"]) if v[1:-1] in flat else None
        return v
    for k, t in flat.items():
        if t["layer"] in ("10-semantic", "20-component"):
            r = resolve(t["value"])
            if r is None:
                probs.append(f"{k}: unresolved reference {t['value']}")
            elif k not in dark or dark[k]["value"] != r:
                probs.append(f"theme dark does not resolve {k} to {r}")
    rec("TOKEN_CATALOG", "FAIL" if probs else "PASS", probs[:4] if probs else f"{len(cat)} catalog tokens == re-flattened token files; dark theme resolves every semantic/component token")


def check_token_policy_file():
    pol = J("tokens/llm/token-policy.json")
    cat = J("tokens/llm/token-catalog.json")
    keys = set(cat["tokens"])
    cats = {k.split(".")[0] for k in keys}
    probs = [f"policy category {c!r} is not a catalog category" for c in pol["catalogCategories"] if c not in cats]
    for slot, r in pol["slots"].items():
        if not any(k.startswith(p) for p in r["prefixes"] for k in keys):
            probs.append(f"slot {slot}: no catalog token matches {r['prefixes']}")
    for p in pol["restrictedTokens"]["prefixes"]:
        if not any(k.startswith(p) for k in keys):
            probs.append(f"restricted prefix {p} matches nothing")
    fams = [str(cat["tokens"][k]["value"][0]) for k in sorted(keys) if k.startswith("typography.family.")]
    if fams != pol["approvedFontFamilies"]:
        probs.append(f"approvedFontFamilies {pol['approvedFontFamilies']} != catalog {fams}")
    if pol["approvedThemes"] != cat["themes"]:
        probs.append("approvedThemes != catalog themes")
    import semantic_validate as sv
    if set(pol["slots"]) != set(J("schema/pagespec.schema.json")["definitions"]["tokens"]["properties"]):
        probs.append("policy slots != schema token slots")
    rec("TOKEN_POLICY_FILE", "FAIL" if probs else "PASS", probs[:4] if probs else "policy categories, slots, restricted prefixes and font families resolve against the real catalog")


def check_motion_pins():
    import semantic_validate as sv
    mp = J("tokens/00-foundation/motion-patterns.json")
    probs = []
    pats = {k: v["reducedMotionFallback"] for k, v in mp["patterns"].items()}
    if pats != sv.MOTION_FALLBACKS:
        probs.append("motion-patterns.json fallbacks != MOTION_FALLBACKS pinned in semantic_validate.py")
    sch = J("schema/pagespec.schema.json")["definitions"]["motion"]
    if sorted(sch["properties"]["pattern"]["enum"]) != sorted(pats):
        probs.append("schema motion pattern enum != motion-patterns.json")
    if sch.get("additionalProperties") is not False:
        probs.append("schema motion object is not closed")
    for sid, s in sections().items():
        for p in s["motion"]["patterns"]:
            if p not in pats:
                probs.append(f"{sid}: unknown motion pattern {p}")
        if s["motion"]["reducedMotionFallback"] != pats.get(s["motion"]["default"]):
            probs.append(f"{sid}: reducedMotionFallback != its default pattern's pinned fallback")
        if s["motion"]["sourceImplementsFallback"] != mp["patterns"].get(s["motion"]["default"], {}).get("sourceImplementsFallback"):
            probs.append(f"{sid}: sourceImplementsFallback disagrees with motion-patterns.json")
    rec("MOTION_PINS", "FAIL" if probs else "PASS", probs[:4] if probs else f"{len(pats)} patterns; fallbacks pinned and identical in tokens, schema, contracts and validator")


def check_templates_routes():
    tdoc = J("templates/templates.json")["templates"]
    routes = J("templates/routes.json")["routes"]
    secs = sections()
    probs = []
    sch_t = J("schema/pagespec.schema.json")["properties"]["template"]["enum"]
    if sorted(sch_t) != sorted(tdoc):
        probs.append("schema template enum != templates.json")
    for tn, t in tdoc.items():
        for n in t["nodes"]:
            if not isinstance(n, dict) or set(n) != {"section", "required", "repeatable"}:
                probs.append(f"{tn}: node {n} is not a structured {{section, required, repeatable}} object")
                continue
            if n["section"] not in secs:
                probs.append(f"{tn}: node section {n['section']} has no contract")
            elif not secs[n["section"]]["retrievalEligible"]:
                probs.append(f"{tn}: runtime section {n['section']} used as a node")
        for l in t.get("runtimeLayers", []):
            if l not in RETRIEVAL_INELIGIBLE:
                probs.append(f"{tn}: runtimeLayer {l} is not runtime UI")
        if t["nodes"][0]["section"] != "shell.navbar":
            probs.append(f"{tn}: first node is not shell.navbar")
    seen = {}
    for r in routes:
        seen[r["route"]] = seen.get(r["route"], 0) + 1
        if r["template"] not in tdoc:
            probs.append(f"route {r['route']}: unknown template {r['template']}")
            continue
        pat = tdoc[r["template"]]["routePattern"]
        if pat != "*" and not re.match(pat, r["route"]):
            probs.append(f"route {r['route']} does not match {r['template']} pattern {pat}")
    probs += [f"route {k} mapped {v} times" for k, v in seen.items() if v != 1]
    for tn in tdoc:
        if not any(r["template"] == tn for r in routes):
            probs.append(f"template {tn} has no route")
    if project_present():
        with open(os.path.join(PROJECT, "src/data/projects.json"), encoding="utf-8") as f:
            ids = [p["id"] for p in json.load(f)]
        want = {f"/project/{i}" for i in ids}
        have = {r["route"] for r in routes if r["template"] == "project-detail"}
        if want != have:
            probs.append(f"project routes {sorted(have ^ want)[:3]} differ from src/data/projects.json")
        app = open(os.path.join(PROJECT, "src/App.jsx"), encoding="utf-8").read()
        for needle in ("path === '/'", "path === '/about'", "/^\\/project\\/[^/]+$/"):
            if needle not in app:
                probs.append(f"route table in src/App.jsx changed (missing {needle}); re-map routes")
    status = "FAIL" if probs else "PASS"
    rec("TEMPLATES_ROUTES", status, probs[:4] if probs else f"{len(tdoc)} templates with structured nodes; {len(routes)} routes each mapped exactly once" + ("" if project_present() else " (project ids not re-read: source absent)"))


def check_graph_agreement():
    import semantic_validate as sv
    g = {r["id"]: r["severity"] for r in J("compatibility/graph.json")["rules"]}
    probs = []
    if g != sv.RULES:
        probs.append(f"graph vs validator: only-in-graph {sorted(set(g) - set(sv.RULES))}, only-in-validator {sorted(set(sv.RULES) - set(g))}, severity diffs {sorted(k for k in g if k in sv.RULES and g[k] != sv.RULES[k])}")
    src = open(os.path.join(REPO, "schema/semantic_validate.py"), encoding="utf-8").read()
    for rid in g:
        if src.count(f'"{rid}"') < 2:
            probs.append(f"rule {rid} is declared but never raised in semantic_validate.py")
    rec("GRAPH_VALIDATOR_AGREEMENT", "FAIL" if probs else "PASS", probs[:3] if probs else f"{len(g)} rules: ids and severities identical in compatibility/graph.json and semantic_validate.py; each is raised in code")


def check_schema_and_examples():
    import jsonschema
    import semantic_validate as sv
    sch = J("schema/pagespec.schema.json")
    probs = []
    jsonschema.Draft7Validator.check_schema(sch)
    if sch.get("$schema") != "http://json-schema.org/draft-07/schema#":
        probs.append("schema is not Draft-07")
    if "mode" not in sch["required"] or sch["properties"]["mode"].get("enum") != ["reference", "generated"]:
        probs.append("mode is not a required closed enum")
    secs = sections()
    for br in sch["definitions"]["node"]["allOf"]:
        sid = br["if"]["properties"]["section"]["const"]
        fields = sorted(br["then"]["properties"]["content"]["properties"])
        if sid not in secs or fields != sorted(secs[sid]["content"]["fields"]):
            probs.append(f"schema content branch for {sid} drifted from its contract")
    ctx = sv.load_context()
    d = os.path.join(REPO, "schema/examples")
    by_t = {}
    n = 0
    for f in sorted(os.listdir(d)):
        if not f.endswith(".json"):
            continue
        spec = J(f"schema/examples/{f}")
        n += 1
        want_mode = f.split(".")[0]
        if spec.get("mode") != want_mode:
            probs.append(f"{f}: mode {spec.get('mode')} does not match its file name")
        by_t.setdefault(spec.get("template"), set()).add(spec.get("mode"))
        e = sv.errors_of(sv.validate(spec, ctx))
        if e:
            probs.append(f"{f}: {len(e)} error(s): {e[0]['rule']} {e[0]['message'][:60]}")
    for t in J("templates/templates.json")["templates"]:
        if by_t.get(t) != {"reference", "generated"}:
            probs.append(f"template {t}: needs a reference and a generated example (has {sorted(by_t.get(t, []))})")
    rec("EXAMPLES", "FAIL" if probs else "PASS", probs[:4] if probs else f"Draft-07 schema valid; {n} examples pass schema + semantic validation; every template has a reference and a generated example")


def check_versions():
    man = J("registry.manifest.json")
    probs = []
    if man["allowlistVersion"] != J("tokens/llm/component-allowlist.json")["version"]:
        probs.append(f"manifest allowlistVersion {man['allowlistVersion']} != allowlist {J('tokens/llm/component-allowlist.json')['version']}")
    if man["pageSpecVersion"] != J("schema/pagespec.schema.json")["properties"]["pageSpecVersion"]["const"]:
        probs.append("manifest pageSpecVersion != schema const")
    if man.get("status") != "design-review-pending" or man.get("productionApproved") is not False:
        probs.append("status/productionApproved changed: approval is a human sign-off")
    rec("VERSION_PARITY", "FAIL" if probs else "PASS", probs or f"allowlistVersion {man['allowlistVersion']} and pageSpecVersion {man['pageSpecVersion']} match; repositoryVersion is documentation-only")


def check_counts():
    from counts import compute_counts
    want = compute_counts()
    man = J("registry.manifest.json")["counts"]
    diff = {k: (man.get(k), v) for k, v in want.items() if man.get(k) != v}
    diff.update({k: (man[k], None) for k in man if k not in want})
    bad_scripts = [k for k, v in want.items() if v == -1]
    probs = [f"{k}: manifest {a} != recomputed {b}" for k, (a, b) in diff.items()] + [f"{k}: counting script failed" for k in bad_scripts]
    rec("COUNTS", "FAIL" if probs else "PASS", probs[:4] if probs else f"manifest counts recomputed from disk: {want}")
    return want


def check_readme_counts(want):
    text = open(os.path.join(REPO, "README.md"), encoding="utf-8").read()
    m = re.search(r"<!-- counts:start -->(.*?)<!-- counts:end -->", text, re.S)
    if not m:
        rec("README_COUNTS", "FAIL", "README.md has no <!-- counts:start --> block")
        return
    got = dict(re.findall(r"\|\s*([A-Za-z]+)\s*\|\s*(-?\d+)\s*\|", m.group(1)))
    probs = [f"README {k}={got.get(k)} != {v}" for k, v in want.items() if got.get(k) != str(v)]
    rec("README_COUNTS", "FAIL" if probs else "PASS", probs[:4] if probs else "README counts table equals the recomputed counts")


def check_policy_hash():
    import policy_hash
    hv = policy_hash.content_hash()
    man = J("registry.manifest.json")["designPolicy"]
    pol = J("policy/design-policy.json")
    probs = []
    if man["contentHash"] != hv:
        probs.append(f"manifest contentHash {man['contentHash'][:20]} != recomputed {hv[:20]}")
    if pol["enforcedBy"]["contentHash"] != hv:
        probs.append("policy/design-policy.json contentHash != recomputed")
    if sorted(man["contentHashOf"]) != sorted(policy_hash.POLICY_FILES) or sorted(pol["enforcedBy"]["files"]) != sorted(policy_hash.POLICY_FILES):
        probs.append("policy file list drifted")
    appr = pol["classification"]["approval"]
    if appr["status"] != "defined-pending-architecture-review" or appr["architectureDecisionRecorded"] or man.get("architectureDecisionRecorded"):
        probs.append("policy approval changed without a recorded owner decision")
    if J("registry.manifest.json")["category"] != pol["classification"]["category"]:
        probs.append("manifest category != policy classification")
    txt = (open(os.path.join(REPO, "README.md"), encoding="utf-8").read() + json.dumps(pol) + json.dumps(J("registry.manifest.json"))).lower()
    if J("registry.manifest.json")["category"] != "saas" and "saas" in txt:
        probs.append("SaaS wording in a non-SaaS repo")
    rec("POLICY_HASH", "FAIL" if probs else "PASS", probs or f"policy contentHash {hv[:23]}... recomputed and matches manifest + policy; approval pending")


def check_wrapper_gate():
    import wrapper_gate
    e, w, i = wrapper_gate.check(*wrapper_gate.load_inputs())
    if e:
        rec("WRAPPER_GATE", "FAIL", e[:4])
    elif w:
        rec("WRAPPER_GATE", "WARN", w[:4])
    else:
        rec("WRAPPER_GATE", "PASS", f"heights at 1440x900 measured for every template node; no HERO > 1800px; share rule skipped on {len(i)} single-viewport page(s) (0 in-flow content sections)")


def check_parity():
    probs, warns = [], []
    mv = J("extraction/measured-values.json")["parity"]
    runs = []
    for rel in mv["results"]:
        p = os.path.join(REPO, rel)
        if not os.path.isfile(p):
            probs.append(f"parity results missing: {rel}")
            continue
        runs.append(J(rel))
    exc = {(e.get("scenario"), e.get("section")): e for e in mv.get("exceptions", [])}
    for e in exc.values():
        if e.get("status") != "pending human approval" or e.get("approvedBy") is not None:
            probs.append(f"parity exception {e.get('scenario')}/{e.get('section')} must be 'pending human approval' with approvedBy null")
    for r in runs:
        for sn, s in r["scenarios"].items():
            for sid, x in s["sections"].items():
                if x["score"] is None:
                    warns.append(f"{r['run']}:{sn}/{sid}: region not found")
                elif x["score"] < PARITY_GATE and (sn, sid) not in exc:
                    probs.append(f"{r['run']}:{sn}/{sid}: {x['score']:.3f} < gate {PARITY_GATE} and no exception")
    if len(runs) == 2:
        a, b = runs
        for sn, s in a["scenarios"].items():
            for sid, x in s["sections"].items():
                y = b["scenarios"].get(sn, {}).get("sections", {}).get(sid, {})
                if x.get("score") is not None and y.get("score") is not None and abs(x["score"] - y["score"]) > PARITY_RUN_TOLERANCE:
                    probs.append(f"{sn}/{sid}: runs disagree {x['score']:.3f} vs {y['score']:.3f}")
    pngs = [os.path.relpath(os.path.join(d, f), REPO) for d, _, fs in os.walk(REPO) for f in fs if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".mp4"))]
    if pngs:
        probs.append(f"captures/media tracked in the repo: {pngs[:3]}")
    if probs:
        rec("PARITY", "FAIL", probs[:4])
    else:
        mins = [min(x["score"] for s in r["scenarios"].values() for x in s["sections"].values() if x["score"] is not None) for r in runs]
        rec("PARITY", "WARN" if warns else "PASS", (warns[:3] if warns else []) + [f"{len(runs)} runs, every section >= {PARITY_GATE} (min per run {[round(m, 4) for m in mins]}), runs agree within {PARITY_RUN_TOLERANCE}; no captures tracked"])


def check_manifest_hygiene():
    man = J("registry.manifest.json")
    probs = []
    for k, v in man["entryPoints"].items():
        if v.startswith("..") or os.path.isabs(v):
            probs.append(f"entryPoint {k} points outside: {v}")
        elif not os.path.exists(os.path.join(REPO, v)):
            probs.append(f"entryPoint {k} missing: {v}")
    for k in ("repositoryId", "category", "designPolicy", "sourceStack", "versionFieldNote", "defaultTheme", "schemaValidatedThemes", "counts"):
        if k not in man:
            probs.append(f"manifest lacks {k}")
    if not man.get("sourceStack", {}).get("documentationOnly"):
        probs.append("sourceStack must be documentationOnly")
    for ep in ("tokenCatalog", "tokenPolicy", "componentAllowlist", "motionPatterns"):
        if ep not in man["entryPoints"]:
            probs.append(f"{ep} not registered")
    rec("MANIFEST_ENTRYPOINTS", "FAIL" if probs else "PASS", probs[:4] if probs else f"{len(man['entryPoints'])} entryPoints, all inside design-repo and present")


def check_hygiene():
    junk, paths = [], []
    pat = re.compile(r"/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|/private/(tmp|var)/|C:\\\\Users\\\\")
    for d, dirs, fs in os.walk(REPO):
        for f in fs:
            p = os.path.join(d, f)
            rel = os.path.relpath(p, REPO)
            if f in (".DS_Store", "Thumbs.db", "desktop.ini") or "__MACOSX" in rel or "__pycache__" in rel or f.endswith(".pyc"):
                junk.append(rel)
                continue
            if f.endswith((".json", ".md", ".py", ".mjs", ".css", ".txt")):
                if pat.search(open(p, encoding="utf-8", errors="ignore").read()):
                    paths.append(rel)
    probs = [f"junk file {j}" for j in junk[:3]] + [f"absolute machine path in {p}" for p in paths[:3]]
    rec("HYGIENE", "FAIL" if probs else "PASS", probs or "no absolute machine paths, no junk files")


def check_source_snapshot():
    if not project_present():
        rec("SOURCE_SNAPSHOT", "WARN", "source project absent: snapshot hashes not compared")
        return
    snap = J("extraction/measured-values.json")["sourceFiles"]
    moved = [rel for rel, v in snap.items() if not os.path.isfile(os.path.join(PROJECT, rel)) or sha(os.path.join(PROJECT, rel)) != v["sha256"]]
    if moved:
        rec("SOURCE_SNAPSHOT", "WARN", f"source moved since the build: {moved} (citations re-verified individually above; re-run extraction/build_repo.py and re-measure, BASELINE R16)")
    else:
        rec("SOURCE_SNAPSHOT", "PASS", f"{len(snap)} cited source files unchanged since the build (sha256)")


def main():
    checks = [check_json_parse, check_section_contracts, check_allowlist_parity, check_retrieval_pin, check_asset_pins, check_citations,
              check_css_pin, check_token_catalog, check_token_policy_file, check_motion_pins, check_templates_routes, check_graph_agreement,
              check_schema_and_examples, check_versions, check_policy_hash, check_wrapper_gate, check_parity, check_manifest_hygiene,
              check_hygiene, check_source_snapshot]
    for c in checks:
        try:
            c()
        except Exception as e:  # a crashing check is a failing check
            rec(c.__name__.replace("check_", "").upper(), "FAIL", f"check crashed: {type(e).__name__}: {e}")
    try:
        want = check_counts()
        check_readme_counts(want)
    except Exception as e:
        rec("COUNTS", "FAIL", f"check crashed: {type(e).__name__}: {e}")
    for name, st, msg in RESULTS:
        if QUIET and st == "PASS":
            continue
        print(f"{st:4}  {name:26} {msg}")
    f = sum(1 for r in RESULTS if r[1] == "FAIL")
    w = sum(1 for r in RESULTS if r[1] == "WARN")
    print(f"\nverify_all: {len(RESULTS) - f - w} pass, {w} warn, {f} fail  (project sources {'present' if project_present() else 'absent'})")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
