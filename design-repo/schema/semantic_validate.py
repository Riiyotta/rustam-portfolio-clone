#!/usr/bin/env python3
"""Semantic validator for PageSpecs: everything JSON Schema cannot express.

    python3 schema/semantic_validate.py                     # every file in schema/examples
    python3 schema/semantic_validate.py path/to/spec.json   # one or more specs
    python3 schema/semantic_validate.py --json ...           # machine-readable findings

Layers: (1) Draft-07 schema (schema/pagespec.schema.json); (2) the rules below, whose ids and
severities equal compatibility/graph.json (verify_all.py checks the agreement). Exit 1 on any error.

Pins (independent of the registries, so editing a JSON file alone cannot loosen them):
  PINNED_AVAILABILITY  asset role -> availability (also in extraction/verify_all.py)
  PINNED_POLICY        weighty roles -> generationPolicy
  RETRIEVAL_INELIGIBLE runtime/utility sections (also in extraction/verify_all.py)
  MOTION_FALLBACKS     motion pattern -> reduced-motion fallback
Generated-mode leakage patterns come from one registry, policy/source-brand.json, harvested from
the real source by extraction/build_repo.py.
"""
import json
import os
import re
import sys

sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RULES = {
    "TEMPLATE_NODE_SEQUENCE": "error", "ROUTE_TEMPLATE_MATCH": "error", "NAVBAR_FIRST": "error", "FOOTER_LAST": "error",
    "ONE_HERO": "error", "HERO_HOME_ONLY": "error", "NO_ADJACENT_DUPLICATE": "error", "UTILITY_NOT_A_NODE": "error",
    "RUNTIME_LAYER_ALLOWED": "error", "MOTION_PATTERN_ALLOWED": "error", "MOTION_FALLBACK_PINNED": "error",
    "MOTION_BUDGET_WEBGL": "warn", "MAX_WORDS": "error", "ASSET_ROLE_ALLOWED": "error", "TOKEN_POLICY": "error",
    "GENERATED_MODE_BRAND": "error", "GENERATED_MODE_PERSON": "error", "GENERATED_MODE_PROJECT": "error",
    "GENERATED_MODE_COPY": "error", "GENERATED_MODE_CTA": "error", "GENERATED_MODE_URL": "error",
    "GENERATED_MODE_ASSET": "error", "GENERATED_MODE_LOGO": "error", "RETRIEVAL_PIN": "error",
    "ASSET_AVAILABILITY_PIN": "error", "REFERENCE_ASSET_SOURCE": "error",
}

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
PINNED_POLICY = {
    "person.portrait-source": "must-not-reuse",
    "brand.wordmark-source": "must-not-reuse",
    "brand.favicon-source": "must-not-reuse",
}
LOGO_ROLES = {"brand.wordmark-source", "brand.favicon-source"}
RETRIEVAL_INELIGIBLE = {
    "utility.preloader", "utility.kinetic-cursor", "utility.page-transition",
    "utility.overlay-backdrop", "utility.hover-title", "utility.toast",
}
RUNTIME_UI_WORDS = re.compile(r"preloader|loader|cursor|transition|backdrop|toast|modal|dialog|drawer|overlay|tooltip|hover-title|banner|consent|lightbox|popup|utility\.", re.I)
MOTION_FALLBACKS = {
    "word-reveal": "opacity-fade", "staggered-fade-up": "opacity-fade", "gallery-strip-scroll": "static-strip",
    "hover-focus-blur": "no-blur-highlight", "plane-focus-stage": "crossfade-stage", "kinetic-cursor": "snap-follow",
    "page-transition-wipe": "instant-route-change", "preloader-wipe": "instant-hide", "opacity-hover": "opacity-hover",
    "content-crossfade": "opacity-fade", "floating-digits": "static-digits", "backdrop-fade": "instant-show", "none": "none",
}
GENERATED_SCHEMES = ("placeholder://", "generated://", "user-supplied://")
RESERVED_HOSTS = (".example", ".invalid")
RESERVED_EXACT = ("example.com", "example.org", "example.net")
RAW_VALUE = re.compile(r"^\s*(#[0-9a-f]{3,8}|rgba?\(|hsla?\(|oklch\(|[0-9.]+\s*(px|rem|em|%|vw|vh|svh|ms|s)\b|var\(|calc\(|clamp\()", re.I)
NAMED_COLOR = re.compile(r"^(white|black|red|blue|green|gray|grey|transparent|currentcolor)$", re.I)


def _load(rel, root=REPO):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return json.load(f)


def load_context(root=REPO):
    sections = {}
    for f in sorted(os.listdir(os.path.join(root, "sections"))):
        if f.endswith(".json"):
            d = _load(f"sections/{f}", root)
            sections[d["id"]] = d
    return {
        "schema": _load("schema/pagespec.schema.json", root),
        "templates": _load("templates/templates.json", root)["templates"],
        "sections": sections,
        "graph": _load("compatibility/graph.json", root),
        "roles": _load("assets/asset-roles.json", root)["roles"],
        "catalog": _load("tokens/llm/token-catalog.json", root),
        "policy": _load("tokens/llm/token-policy.json", root),
        "brand": _load("policy/source-brand.json", root),
        "allowlist": _load("tokens/llm/component-allowlist.json", root),
    }


class Findings(list):
    def add(self, rule, msg, path=""):
        self.append({"rule": rule, "severity": RULES[rule], "path": path, "message": msg})


# ------------------------------------------------------------------ repo-level pins
def check_pins(ctx, out):
    for role, d in ctx["roles"].items():
        pin = PINNED_AVAILABILITY.get(role)
        if pin is None:
            out.add("ASSET_AVAILABILITY_PIN", f"role {role} has no pinned availability")
        elif d.get("availability") != pin:
            out.add("ASSET_AVAILABILITY_PIN", f"role {role}: registry says {d.get('availability')!r}, pin says {pin!r}")
        if role in PINNED_POLICY and d.get("generationPolicy") != PINNED_POLICY[role]:
            out.add("ASSET_AVAILABILITY_PIN", f"role {role}: generationPolicy {d.get('generationPolicy')!r} != pinned {PINNED_POLICY[role]!r}")
    for role in PINNED_AVAILABILITY:
        if role not in ctx["roles"]:
            out.add("ASSET_AVAILABILITY_PIN", f"pinned role {role} missing from the registry")
    allow = {e["id"]: e for e in ctx["allowlist"]["entries"] if e.get("kind") == "section"}
    for sid, s in ctx["sections"].items():
        pinned_false = sid in RETRIEVAL_INELIGIBLE
        if s.get("retrievalEligible") is pinned_false:
            out.add("RETRIEVAL_PIN", f"section {sid}: contract retrievalEligible={s.get('retrievalEligible')} contradicts the pin")
        a = allow.get(sid)
        if a is not None and a.get("retrievalEligible") is pinned_false:
            out.add("RETRIEVAL_PIN", f"section {sid}: allowlist retrievalEligible={a.get('retrievalEligible')} contradicts the pin")
        looks_runtime = bool(RUNTIME_UI_WORDS.search(sid) or RUNTIME_UI_WORDS.search(s.get("title", "")))
        if looks_runtime and not pinned_false:
            out.add("RETRIEVAL_PIN", f"section {sid} looks like runtime UI but is not in RETRIEVAL_INELIGIBLE")
    for sid in RETRIEVAL_INELIGIBLE:
        if sid not in ctx["sections"]:
            out.add("RETRIEVAL_PIN", f"pinned section {sid} has no contract")


# ------------------------------------------------------------------ helpers
def words(s):
    return len(re.findall(r"\S+", s or ""))


def norm_tokens(s):
    return re.findall(r"[a-z0-9æøå']+", (s or "").lower().replace("’", "'"))


def iter_strings(obj, path=""):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_strings(v, f"{path}[{i}]")


def iter_assets(obj, path=""):
    if isinstance(obj, dict):
        if "assetRole" in obj:
            yield path, obj
        for k, v in obj.items():
            yield from iter_assets(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_assets(v, f"{path}[{i}]")


def is_link_path(path, value):
    leaf = re.sub(r"\[\d+\]", "", path.split(".")[-1])
    return leaf in ("href", "profileHref", "backHref") or bool(re.match(r"^(https?:|mailto:|www\.)", value, re.I))


NON_COPY_KEYS = {"section", "variant", "assetRole", "kind", "pattern", "reducedMotionFallback", "trigger", "src", "year", "digits"}


def text_fields(spec):
    """(path, text) for copy-bearing strings: content + meta, excluding ids/enums/urls/sources."""
    out = []
    for p, v in iter_strings(spec.get("meta", {}), "meta"):
        out.append((p, v))
    for i, n in enumerate(spec.get("nodes", [])):
        for p, v in iter_strings(n.get("content", {}), f"nodes[{i}].content"):
            leaf = re.sub(r"\[\d+\]", "", p.split(".")[-1])
            if leaf in NON_COPY_KEYS or is_link_path(p, v):
                continue
            out.append((p, v))
    return out


def host_ok(url):
    m = re.match(r"^(?:https?://)?([^/?#:]+)", url.strip(), re.I)
    if not m:
        return False
    host = m.group(1).lower()
    return host.endswith(RESERVED_HOSTS) or host in RESERVED_EXACT or any(host.endswith("." + h) for h in RESERVED_EXACT)


# ------------------------------------------------------------------ main validation
def validate(spec, ctx=None, schema_layer=True, pins=True):
    ctx = ctx or load_context()
    out = Findings()
    if schema_layer:
        try:
            import jsonschema
            v = jsonschema.Draft7Validator(ctx["schema"])
            for e in sorted(v.iter_errors(spec), key=lambda e: list(e.absolute_path)):
                out.append({"rule": "SCHEMA", "severity": "error", "path": "/".join(str(p) for p in e.absolute_path), "message": e.message[:300]})
        except ImportError:
            out.append({"rule": "SCHEMA", "severity": "warn", "path": "", "message": "jsonschema not installed; schema layer skipped"})
    if pins:
        check_pins(ctx, out)
    if not isinstance(spec, dict):
        return out
    sections, templates = ctx["sections"], ctx["templates"]
    nodes = [n for n in spec.get("nodes", []) if isinstance(n, dict)]
    ids = [n.get("section") for n in nodes]
    tname = spec.get("template")
    tpl = templates.get(tname)
    mode = spec.get("mode")

    # template cross-reference (not nodes[] in isolation)
    if tpl is None:
        out.add("TEMPLATE_NODE_SEQUENCE", f"unknown template {tname!r}")
    else:
        i = 0
        for tn in tpl["nodes"]:
            if i < len(ids) and ids[i] == tn["section"]:
                i += 1
                while tn.get("repeatable") and i < len(ids) and ids[i] == tn["section"]:
                    i += 1
            elif tn.get("required"):
                out.add("TEMPLATE_NODE_SEQUENCE", f"required node {tn['section']} missing or out of order for template {tname}")
        if i < len(ids):
            out.add("TEMPLATE_NODE_SEQUENCE", f"node(s) {ids[i:]} not allowed at this position by template {tname} (expected order {[t['section'] for t in tpl['nodes']]})")
        route = spec.get("route", "")
        pat = tpl.get("routePattern")
        if pat == "*":
            for on, ot in templates.items():
                if ot.get("routePattern") not in (None, "*") and re.match(ot["routePattern"], route or ""):
                    out.add("ROUTE_TEMPLATE_MATCH", f"route {route!r} belongs to template {on}, not the fallback")
        elif not re.match(pat, route or ""):
            out.add("ROUTE_TEMPLATE_MATCH", f"route {route!r} does not match {tname} pattern {pat}")
        allowed_layers = set(tpl.get("runtimeLayers", []))
        for l in spec.get("runtimeLayers", []) or []:
            if l not in allowed_layers:
                out.add("RUNTIME_LAYER_ALLOWED", f"runtime layer {l} is not allowed on template {tname}")
    if ids and ids[0] != "shell.navbar":
        out.add("NAVBAR_FIRST", f"first node is {ids[0]}, expected shell.navbar")
    if "shell.footer-contact" in ids and ids[-1] != "shell.footer-contact":
        out.add("FOOTER_LAST", "shell.footer-contact is not the last node")
    for a, b in zip(ids, ids[1:]):
        if a == b:
            out.add("NO_ADJACENT_DUPLICATE", f"{a} appears twice in a row")
    heroes = [s for s in ids if sections.get(s, {}).get("semantic", {}).get("category") == "HERO"]
    if len(heroes) > 1:
        out.add("ONE_HERO", f"{len(heroes)} HERO nodes")
    for s in ids:
        if sections.get(s, {}).get("constraints", {}).get("homeOnly") and tname != "home":
            out.add("HERO_HOME_ONLY", f"{s} is home-only but template is {tname}")

    webgl = set(ctx["graph"].get("webglScenePatterns", []))
    scene_count = 0
    for i, n in enumerate(nodes):
        sid = n.get("section")
        s = sections.get(sid)
        p = f"nodes[{i}]"
        if s is None:
            continue
        if sid in RETRIEVAL_INELIGIBLE or s.get("retrievalEligible") is False:
            out.add("UTILITY_NOT_A_NODE", f"{sid} is runtime UI (retrievalEligible=false) and cannot be a node", p)
        m = n.get("motion") or {}
        pat = m.get("pattern")
        if pat is not None:
            if pat not in s["motion"]["patterns"]:
                out.add("MOTION_PATTERN_ALLOWED", f"{sid}: pattern {pat!r} not in {s['motion']['patterns']}", p + ".motion")
            if pat in MOTION_FALLBACKS and m.get("reducedMotionFallback") != MOTION_FALLBACKS[pat]:
                out.add("MOTION_FALLBACK_PINNED", f"{sid}: fallback {m.get('reducedMotionFallback')!r} != pinned {MOTION_FALLBACKS[pat]!r} for {pat}", p + ".motion")
            if pat in webgl:
                scene_count += 1
        check_words(s["content"]["fields"], n.get("content") or {}, out, p + ".content", sid)
        # asset roles per section
        allowed_gen = set(s.get("generatedAssetRoles", []))
        allowed_ref = allowed_gen | set(s.get("referenceAssetRoles", []))
        for ap, a in iter_assets(n.get("content") or {}, p + ".content"):
            role = a.get("assetRole")
            if role not in (allowed_gen if mode == "generated" else allowed_ref):
                out.add("ASSET_ROLE_ALLOWED", f"{sid}: role {role!r} not allowed in {mode} mode here", ap)
        check_tokens(n.get("tokens") or {}, spec.get("theme"), ctx, out, p + ".tokens")
    if spec.get("theme") not in ctx["policy"].get("approvedThemes", []):
        out.add("TOKEN_POLICY", f"TOKEN_POLICY[theme] theme {spec.get('theme')!r} is not an approved theme {ctx['policy'].get('approvedThemes')}")
    if scene_count > 1:
        out.add("MOTION_BUDGET_WEBGL", f"{scene_count} WebGL scene patterns on one page")

    if mode == "generated":
        check_generated(spec, ctx, out)
    elif mode == "reference":
        for ap, a in iter_assets(spec.get("nodes", [])):
            av = PINNED_AVAILABILITY.get(a.get("assetRole"))
            if av in ("reference-only", "blocked-for-generation") and str(a.get("src", "")).startswith(GENERATED_SCHEMES):
                out.add("REFERENCE_ASSET_SOURCE", f"source role {a.get('assetRole')} must point at the real source file, not {a.get('src')!r}", ap)
    return out


def check_words(fields, content, out, path, sid):
    for name, f in fields.items():
        if name not in content:
            continue
        v = content[name]
        t = f.get("type")
        if t == "text" and isinstance(v, str) and "maxWords" in f and words(v) > f["maxWords"]:
            out.add("MAX_WORDS", f"{sid}.{name}: {words(v)} words > {f['maxWords']}", f"{path}.{name}")
        elif t == "list" and isinstance(v, list):
            of = f.get("of", {})
            for i, item in enumerate(v):
                if isinstance(of.get("type"), str):
                    if of["type"] == "text" and isinstance(item, str) and "maxWords" in of and words(item) > of["maxWords"]:
                        out.add("MAX_WORDS", f"{sid}.{name}[{i}]: {words(item)} words > {of['maxWords']}", f"{path}.{name}[{i}]")
                elif isinstance(item, dict):
                    check_words(of, item, out, f"{path}.{name}[{i}]", sid)
        elif t == "object" and isinstance(v, dict):
            check_words(f.get("of", {}), v, out, f"{path}.{name}", sid)


def check_tokens(tokens, theme, ctx, out, path):
    cat = ctx["catalog"]["tokens"]
    pol = ctx["policy"]
    restricted = tuple(pol.get("restrictedTokens", {}).get("prefixes", []))
    for slot, ref in tokens.items():
        p = f"{path}.{slot}"
        rule = pol["slots"].get(slot)
        if not isinstance(ref, str):
            continue
        if RAW_VALUE.search(ref) or NAMED_COLOR.match(ref.strip()):
            kind = "spacing" if slot == "spacing" else ("color" if slot in ("textColor", "surface", "border") else "value")
            out.add("TOKEN_POLICY", f"TOKEN_POLICY[raw-value] {slot}={ref!r}: raw {kind} value; use a catalog token", p)
            continue
        if slot == "fontFamily" and ref not in cat:
            out.add("TOKEN_POLICY", f"TOKEN_POLICY[unsupported-font] {ref!r} is not an approved font family token {sorted(k for k in cat if k.startswith('typography.family.'))}", p)
            continue
        if ref not in cat:
            out.add("TOKEN_POLICY", f"TOKEN_POLICY[unknown-token] {ref!r} is not in tokens/llm/token-catalog.json", p)
            continue
        t = cat[ref]
        if ref.startswith(restricted) or t.get("restricted"):
            out.add("TOKEN_POLICY", f"TOKEN_POLICY[restricted] {ref!r} is restricted ({t.get('restricted')})", p)
        if rule is None:
            out.add("TOKEN_POLICY", f"TOKEN_POLICY[slot] unknown slot {slot!r}", p)
        elif not ref.startswith(tuple(rule["prefixes"])):
            out.add("TOKEN_POLICY", f"TOKEN_POLICY[slot] {ref!r} cannot fill slot {slot} (allowed prefixes {rule['prefixes']})", p)
        if theme not in t.get("themes", []):
            out.add("TOKEN_POLICY", f"TOKEN_POLICY[theme] {ref!r} does not resolve in theme {theme!r}", p)


def shingles(tokens, n):
    return {" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}


def check_generated(spec, ctx, out):
    b = ctx["brand"]
    allstr = [(p, v) for p, v in iter_strings({"meta": spec.get("meta", {}), "nodes": spec.get("nodes", []), "route": spec.get("route", "")})
              if not re.sub(r"\[\d+\]", "", p.split(".")[-1]) in ("section", "assetRole", "kind", "pattern", "reducedMotionFallback", "trigger")]
    texts = text_fields(spec)

    def scan(rule, patterns, label):
        for p, v in allstr:
            for pat in patterns:
                if re.search(pat, v, re.I):
                    out.add(rule, f"{label} pattern /{pat}/ matched {v[:60]!r}", p)
                    break

    scan("GENERATED_MODE_BRAND", b["brand"]["patterns"], "source brand")
    scan("GENERATED_MODE_PERSON", b["person"]["patterns"] + b["location"]["patterns"], "source person/contact/location")
    scan("GENERATED_MODE_PROJECT", b["project"]["patterns"] + [re.escape(i) for i in b["project"]["ids"]], "source project/client")
    titles = {t.strip().lower() for t in b["project"]["titles"]}
    for p, v in texts:
        if v.strip().lower() in titles:
            out.add("GENERATED_MODE_PROJECT", f"source project title {v!r}", p)
    # CTA / interaction labels
    ctas = [c.strip().lower() for c in b["cta"]["strings"]]
    for p, v in texts:
        lv = v.strip().lower()
        for c in ctas:
            if lv == c or (len(c.split()) >= 3 and c in lv):
                out.add("GENERATED_MODE_CTA", f"source label {c!r} reused", p)
                break
    # copy: shingles + equality
    n = int(b["copy"].get("shingleSize", 5))
    mineq = int(b["copy"].get("equalityMinWords", 3))
    src_sh, src_eq = set(), set()
    for s in b["copy"]["strings"]:
        t = norm_tokens(s)
        src_sh |= shingles(t, n)
        if len(t) >= mineq:
            src_eq.add(" ".join(t))
    joined = []
    for p, v in texts:
        t = norm_tokens(v)
        joined += t
        hit = shingles(t, n) & src_sh
        if hit:
            out.add("GENERATED_MODE_COPY", f"shares source phrasing {sorted(hit)[0]!r}", p)
        elif " ".join(t) in src_eq:
            out.add("GENERATED_MODE_COPY", f"equals a source string {v[:60]!r}", p)
    # heading lines split across list items: check the concatenation too
    for i, nd in enumerate(spec.get("nodes", [])):
        lines = (nd.get("content") or {}).get("headingLines")
        if isinstance(lines, list) and len(lines) > 1:
            t = norm_tokens(" ".join(x for x in lines if isinstance(x, str)))
            hit = shingles(t, n) & src_sh
            if hit or " ".join(t) in src_eq:
                out.add("GENERATED_MODE_COPY", f"heading lines together reproduce source copy {sorted(hit)[0] if hit else ' '.join(t)!r}", f"nodes[{i}].content.headingLines")
    # URLs
    domains = [d.lower() for d in b["url"]["domains"]]
    for p, v in allstr:
        lv = v.lower()
        if any(d in lv for d in domains):
            out.add("GENERATED_MODE_URL", f"source domain/profile in {v[:80]!r}", p)
            continue
        if is_link_path(p, v):
            if v.startswith("/") or v.startswith("#"):
                continue
            if v.lower().startswith("mailto:"):
                if not host_ok(v.split("@")[-1]):
                    out.add("GENERATED_MODE_URL", f"email {v!r} is not on a reserved placeholder domain", p)
                continue
            if not host_ok(re.sub(r"^https?://", "", v, flags=re.I)):
                out.add("GENERATED_MODE_URL", f"external link {v!r} is not on a reserved placeholder domain (.example/.invalid/example.com)", p)
        elif re.search(r"https?://|www\.", v, re.I):
            for u in re.findall(r"(?:https?://|www\.)[^\s\"')]+", v, re.I):
                if not host_ok(re.sub(r"^https?://", "", u, flags=re.I)):
                    out.add("GENERATED_MODE_URL", f"inline URL {u!r} is not on a reserved placeholder domain", p)
    # assets
    fn = b["assetFilenames"]["patterns"]
    for ap, a in iter_assets(spec.get("nodes", []), "nodes"):
        role, src = a.get("assetRole"), str(a.get("src", ""))
        av = PINNED_AVAILABILITY.get(role)
        if role in LOGO_ROLES:
            out.add("GENERATED_MODE_LOGO", f"source wordmark/favicon role {role} in a generated page", ap)
        if av != "generation-safe":
            out.add("GENERATED_MODE_ASSET", f"role {role} is {av or 'unknown'} (pinned); generated pages use generation-safe roles only", ap)
        if not src.startswith(GENERATED_SCHEMES):
            out.add("GENERATED_MODE_ASSET", f"src {src!r} must use placeholder://, generated:// or user-supplied://", ap)
        if any(re.search(pt, src, re.I) for pt in fn):
            out.add("GENERATED_MODE_ASSET", f"src {src!r} names a source asset file", ap)


def errors_of(findings):
    return [f for f in findings if f["severity"] == "error"]


def main(argv):
    as_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        d = os.path.join(REPO, "schema", "examples")
        paths = [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".json")]
    ctx = load_context()
    total_err = 0
    report = {}
    for p in paths:
        with open(p, encoding="utf-8") as f:
            spec = json.load(f)
        fs = validate(spec, ctx)
        e = errors_of(fs)
        total_err += len(e)
        report[os.path.basename(p)] = fs
        if not as_json:
            print(f"{'PASS' if not e else 'FAIL'}  {os.path.basename(p)}  ({len(e)} error(s), {len(fs) - len(e)} warning(s))")
            for x in fs:
                print(f"      {x['severity'].upper():5} {x['rule']}: {x['message']} @ {x['path']}")
    if as_json:
        print(json.dumps(report, indent=1))
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
