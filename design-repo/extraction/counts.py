#!/usr/bin/env python3
"""Recompute the manifest's counts from the files on disk (shared by build_repo.py and verify_all.py)."""
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _j(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return json.load(f)


def _count(script):
    out = subprocess.run([sys.executable, os.path.join(REPO, script), "--count"], capture_output=True, text=True)
    s = out.stdout.strip()
    return int(s) if out.returncode == 0 and s.isdigit() else -1


def compute_counts():
    secs = [_j(f"sections/{f}") for f in sorted(os.listdir(os.path.join(REPO, "sections"))) if f.endswith(".json")]
    ex = sorted(f for f in os.listdir(os.path.join(REPO, "schema/examples")) if f.endswith(".json"))
    token_files = []
    for d, _, fs in os.walk(os.path.join(REPO, "tokens")):
        if os.path.basename(d) == "llm":
            continue
        token_files += [f for f in fs if f.endswith(".json")]
    return {
        "tokens": len(_j("tokens/llm/token-catalog.json")["tokens"]),
        "tokenFiles": len(token_files),
        "primitives": len([f for f in os.listdir(os.path.join(REPO, "primitives")) if f.endswith(".json")]),
        "components": len([f for f in os.listdir(os.path.join(REPO, "components")) if f.endswith(".json")]),
        "sections": len(secs),
        "sectionsRetrievalIneligible": sum(1 for s in secs if s.get("retrievalEligible") is False),
        "templates": len(_j("templates/templates.json")["templates"]),
        "routes": len(_j("templates/routes.json")["routes"]),
        "assetRoles": len(_j("assets/asset-roles.json")["roles"]),
        "motionPatterns": len(_j("tokens/00-foundation/motion-patterns.json")["patterns"]),
        "graphRules": len(_j("compatibility/graph.json")["rules"]),
        "examples": len(ex),
        "referenceExamples": sum(1 for e in ex if e.startswith("reference.")),
        "generatedExamples": sum(1 for e in ex if e.startswith("generated.")),
        "adversarialCases": _count("schema/tests/adversarial_test.py"),
        "driftCases": _count("extraction/prove_drift.py"),
    }


if __name__ == "__main__":
    print(json.dumps(compute_counts(), indent=1))
