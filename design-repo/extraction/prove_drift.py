#!/usr/bin/env python3
"""Prove every verify_all.py check (and the pins/gates) actually fails on injected drift.

    python3 extraction/prove_drift.py            # run all drift cases
    python3 extraction/prove_drift.py --count    # number of cases (manifest counts)

For each case: copy design-repo (plus the cited source files, when the project is present) into a
fresh scratch directory, inject one drift, run that copy's own extraction/verify_all.py and require
it to exit 1 with the expected check FAILing. Finally the untouched real repo must still pass.
Scratch location: $PROVE_DRIFT_DIR if set, else the OS temp directory; each case cleans up after itself.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.dirname(REPO)
SOURCE_PARTS = ["src", "index.html", "ia.json"]


def jload(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def jsave(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write("\n")


def edit_text(p, old, new, count=1):
    s = open(p, encoding="utf-8").read()
    if old not in s:
        raise RuntimeError(f"drift anchor not found in {p}: {old[:60]!r}")
    open(p, "w", encoding="utf-8").write(s.replace(old, new, count))


CASES = []


def case(name, expect):
    def deco(fn):
        CASES.append((name, expect, fn))
        return fn
    return deco


@case("phantom allowlist entry", "ALLOWLIST_PARITY")
def _(r, p):
    f = f"{r}/tokens/llm/component-allowlist.json"; d = jload(f)
    d["entries"].append({"id": "section.phantom", "kind": "section", "file": "sections/section.phantom.json"}); jsave(f, d)


@case("contract without allowlist entry", "ALLOWLIST_PARITY")
def _(r, p):
    f = f"{r}/tokens/llm/component-allowlist.json"; d = jload(f)
    d["entries"] = [e for e in d["entries"] if e["id"] != "project.meta"]; jsave(f, d)


@case("out-of-range citation", "CITATIONS")
def _(r, p):
    f = f"{r}/sections/project.header.json"; d = jload(f)
    d["source"]["lines"] = "99990-99999"; jsave(f, d)


@case("in-range citation describing the wrong code (tag not at the lines)", "CITATIONS")
def _(r, p):
    f = f"{r}/sections/hero.intro.json"; d = jload(f)
    d["source"]["lines"] = "100-120"; jsave(f, d)


@case("cited source line moved under the design-repo (src edit)", "CITATIONS")
def _(r, p):
    f = f"{p}/src/engine/chunks/272.js"
    s = open(f, encoding="utf-8").read().split("\n")
    s.insert(10, "// inserted line shifts every later citation")
    open(f, "w", encoding="utf-8").write("\n".join(s))


@case("manifest count hand-edited", "COUNTS")
def _(r, p):
    f = f"{r}/registry.manifest.json"; d = jload(f); d["counts"]["sections"] += 1; jsave(f, d)


@case("README count hand-edited", "README_COUNTS")
def _(r, p):
    f = f"{r}/README.md"; s = open(f, encoding="utf-8").read()
    s = re.sub(r"(\|\s*templates\s*\|\s*)(\d+)", lambda m: m.group(1) + str(int(m.group(2)) + 3), s, count=1)
    open(f, "w", encoding="utf-8").write(s)


@case("allowlistVersion drift", "VERSION_PARITY")
def _(r, p):
    f = f"{r}/tokens/llm/component-allowlist.json"; d = jload(f); d["version"] = "9.9.9"; jsave(f, d)


@case("registry availability loosened (real portrait made generation-safe)", "ASSET_PINS")
def _(r, p):
    f = f"{r}/assets/asset-roles.json"; d = jload(f); d["roles"]["person.portrait-source"]["availability"] = "generation-safe"; jsave(f, d)


@case("pin removed from verify_all.py", "ASSET_PINS")
def _(r, p):
    edit_text(f"{r}/extraction/verify_all.py", '    "brand.favicon-source": "blocked-for-generation",\n', "", 1)


@case("pin changed in semantic_validate.py only", "ASSET_PINS")
def _(r, p):
    edit_text(f"{r}/schema/semantic_validate.py", '"project.video-source": "reference-only"', '"project.video-source": "generation-safe"')


@case("wordmark generationPolicy changed to a different valid value", "ASSET_PINS")
def _(r, p):
    f = f"{r}/assets/asset-roles.json"; d = jload(f); d["roles"]["brand.wordmark-source"]["generationPolicy"] = "must-reuse-exact"; jsave(f, d)


@case("schema assetRole enum gains an unregistered role", "ASSET_PINS")
def _(r, p):
    f = f"{r}/schema/pagespec.schema.json"; d = jload(f); d["definitions"]["assetRole"]["enum"].append("logo.real"); jsave(f, d)


@case("contract + allowlist flipped together (preloader retrievable)", "RETRIEVAL_PIN")
def _(r, p):
    f = f"{r}/sections/utility.preloader.json"; d = jload(f); d["retrievalEligible"] = True; d.pop("retrievalIneligibleReason", None); jsave(f, d)
    f = f"{r}/tokens/llm/component-allowlist.json"; d = jload(f)
    for e in d["entries"]:
        if e["id"] == "utility.preloader":
            e["retrievalEligible"] = True
    jsave(f, d)


@case("retrieval pin entry removed from verify_all.py", "RETRIEVAL_PIN")
def _(r, p):
    edit_text(f"{r}/extraction/verify_all.py", '"utility.overlay-backdrop", "utility.hover-title", "utility.toast",\n}', '"utility.overlay-backdrop", "utility.hover-title",\n}')


@case("token catalog value edited without the token file", "TOKEN_CATALOG")
def _(r, p):
    f = f"{r}/tokens/llm/token-catalog.json"; d = jload(f); d["tokens"]["color.ink.900"]["value"] = "#111111"; jsave(f, d)


@case("token file edited without the catalog", "TOKEN_CATALOG")
def _(r, p):
    f = f"{r}/tokens/00-foundation/color.json"; d = jload(f); d["color"]["paper"]["100"]["$value"] = "#ffffff"; jsave(f, d)


@case("policy category name that is not a catalog key", "TOKEN_POLICY_FILE")
def _(r, p):
    f = f"{r}/tokens/llm/token-policy.json"; d = jload(f); d["catalogCategories"].append("shadow"); jsave(f, d)


@case("policy-enforcing file edited (hash drift)", "POLICY_HASH")
def _(r, p):
    f = f"{r}/compatibility/graph.json"; d = jload(f); d["rules"][0]["rule"] += " (edited)"; jsave(f, d)


@case("graph severity flipped (graph vs validator)", "GRAPH_VALIDATOR_AGREEMENT")
def _(r, p):
    f = f"{r}/compatibility/graph.json"; d = jload(f)
    for x in d["rules"]:
        if x["id"] == "MOTION_BUDGET_WEBGL":
            x["severity"] = "error"
    jsave(f, d)


@case("template references a section with no contract", "TEMPLATES_ROUTES")
def _(r, p):
    f = f"{r}/templates/templates.json"; d = jload(f)
    d["templates"]["home"]["nodes"].insert(2, {"section": "content.ghost", "required": False, "repeatable": False}); jsave(f, d)


@case("route mapped twice", "TEMPLATES_ROUTES")
def _(r, p):
    f = f"{r}/templates/routes.json"; d = jload(f); d["routes"].append(dict(d["routes"][1])); jsave(f, d)


@case("project route missing for a real project id", "TEMPLATES_ROUTES")
def _(r, p):
    f = f"{r}/templates/routes.json"; d = jload(f); d["routes"] = [x for x in d["routes"] if not x["route"].startswith("/project/6aef")]; jsave(f, d)


@case("measured height missing for a template node", "WRAPPER_GATE")
def _(r, p):
    f = f"{r}/extraction/measured-values.json"; d = jload(f)
    del d["sectionHeights"]["1440x900"]["templates"]["home"]["sections"]["hero.intro"]; jsave(f, d)


@case("heights measured at the wrong viewport", "WRAPPER_GATE")
def _(r, p):
    f = f"{r}/extraction/measured-values.json"; d = jload(f); d["sectionHeights"]["1440x900"]["viewport"] = "1280x720"; jsave(f, d)


@case("HERO grows past 3000px without a whitelist", "WRAPPER_GATE")
def _(r, p):
    f = f"{r}/extraction/measured-values.json"; d = jload(f)
    d["sectionHeights"]["1440x900"]["templates"]["home"]["sections"]["hero.intro"]["heightPx"] = 3200; jsave(f, d)


@case("gate threshold edited in code", "WRAPPER_GATE")
def _(r, p):
    edit_text(f"{r}/extraction/wrapper_gate.py", "HERO_ERROR_PX = 3000", "HERO_ERROR_PX = 100")


@case("CSS excerpt edited", "CSS_PIN")
def _(r, p):
    f = f"{r}/extraction/evidence/site.pretty.css"
    edit_text(f, "background-color:#0e100c;", "background-color:#000000;")


@case("source stylesheet changed under the pin", "CSS_PIN")
def _(r, p):
    f = f"{p}/src/styles/site.css"
    s = open(f, encoding="utf-8").read().replace(".text-color{color:#ebe8e4}", ".text-color{color:#ffffff}")
    open(f, "w", encoding="utf-8").write(s)


@case("motion fallback changed in motion-patterns.json", "MOTION_PINS")
def _(r, p):
    f = f"{r}/tokens/00-foundation/motion-patterns.json"; d = jload(f); d["patterns"]["word-reveal"]["reducedMotionFallback"] = "none"; jsave(f, d)


@case("section semantic.id differs from contract id", "SECTION_CONTRACTS")
def _(r, p):
    f = f"{r}/sections/project.meta.json"; d = jload(f); d["semantic"]["id"] = "project.facts"; jsave(f, d)


@case("generated example leaks the owner's name", "EXAMPLES")
def _(r, p):
    f = f"{r}/schema/examples/generated.home.json"; d = jload(f); d["nodes"][0]["content"]["ownerName"] = "Rustam Kerimov"; jsave(f, d)


@case("parity score below the gate without an exception", "PARITY")
def _(r, p):
    f = f"{r}/extraction/parity/results-run1.json"; d = jload(f)
    sc = next(iter(d["scenarios"].values())); sid = next(iter(sc["sections"])); sc["sections"][sid]["score"] = 0.5; jsave(f, d)


@case("agent self-approved a parity exception", "PARITY")
def _(r, p):
    f = f"{r}/extraction/measured-values.json"; d = jload(f)
    d["parity"]["exceptions"] = [{"scenario": "home", "section": "hero.intro", "status": "approved", "approvedBy": "claude agent"}]; jsave(f, d)


@case("entryPoint pointing outside the package", "MANIFEST_ENTRYPOINTS")
def _(r, p):
    f = f"{r}/registry.manifest.json"; d = jload(f); d["entryPoints"]["sourceCss"] = "../src/styles/site.css"; jsave(f, d)


@case("absolute machine path in a doc", "HYGIENE")
def _(r, p):
    with open(f"{r}/CHANGELOG.md", "a", encoding="utf-8") as fh:
        fh.write("\nbuilt in " + "/" + "Users/someone/work/design-repo\n")


def run_verify(repo):
    out = subprocess.run([sys.executable, os.path.join(repo, "extraction", "verify_all.py")], capture_output=True, text=True, cwd=repo, timeout=600)
    return out.returncode, out.stdout + out.stderr


def make_scratch(base):
    root = tempfile.mkdtemp(prefix="prove-drift-", dir=base)
    r = os.path.join(root, "design-repo")
    shutil.copytree(REPO, r, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
    if os.path.isdir(os.path.join(PROJECT, "src")):
        for part in SOURCE_PARTS:
            s = os.path.join(PROJECT, part)
            if os.path.isdir(s):
                shutil.copytree(s, os.path.join(root, part))
            elif os.path.isfile(s):
                shutil.copy2(s, os.path.join(root, part))
    return root, r


def main(argv):
    if "--count" in argv:
        print(len(CASES))
        return 0
    base = os.environ.get("PROVE_DRIFT_DIR") or None
    if base:
        os.makedirs(base, exist_ok=True)
    has_src = os.path.isdir(os.path.join(PROJECT, "src"))
    fails = 0
    # precondition: an untouched scratch copy must pass, so every case below fails for its own reason
    root, r = make_scratch(base)
    try:
        code, out = run_verify(r)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print(f"{'PASS' if code == 0 else 'FAIL'}  untouched scratch copy passes verify_all (baseline for every case)")
    if code != 0:
        print("\n".join(l for l in out.splitlines() if l.startswith("FAIL")))
        return 1
    for name, expect, fn in CASES:
        root, r = make_scratch(base)
        try:
            if not has_src and expect in ("CITATIONS", "CSS_PIN") or (not has_src and "real project id" in name):
                print(f"SKIP  {name}: needs the source project next to design-repo")
                continue
            fn(r, root)
            code, out = run_verify(r)
            line = next((l for l in out.splitlines() if l.startswith("FAIL") and expect in l), None)
            ok = code == 1 and line is not None
            fails += not ok
            print(f"{'CAUGHT' if ok else 'MISSED'}  {name}  -> {expect}" + (f"\n        {line.strip()[:150]}" if line else f"\n        exit={code}; FAIL lines: {[l[:90] for l in out.splitlines() if l.startswith('FAIL')][:3]}"))
        finally:
            shutil.rmtree(root, ignore_errors=True)
    code, out = run_verify(REPO)
    print(f"{'PASS' if code == 0 else 'FAIL'}  untouched real repo: verify_all exit {code}")
    print(f"\nprove_drift: {len(CASES) - fails}/{len(CASES)} drift cases caught; real repo {'passes' if code == 0 else 'FAILS'}")
    return 1 if fails or code else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
