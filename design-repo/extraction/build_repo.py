#!/usr/bin/env python3
"""Builder for this design-repo. Regenerates every data file from the real source.

    python3 extraction/build_repo.py

Needs the source project next to design-repo/ (../src, ../public). Every citation is located by a
needle (a literal string that must exist in the cited file), so line numbers are re-derived whenever
the clone moves (BASELINE R16); a needle that disappears makes the build fail loudly instead of
producing a stale citation. Copy budgets, the leakage registry, counts and the CSS excerpt are all
computed here, never hand-typed. Hand-written files (validators, tests, gate, docs) are not touched,
except that registry.manifest.json and policy/design-policy.json receive recomputed counts and the
policy content hash at the end.
"""
import hashlib
import json
import math
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.dirname(REPO)
sys.path.insert(0, os.path.join(REPO, "extraction"))

VERSION = "1.0.0"
PAGESPEC_VERSION = "1.0.0"
ALLOWLIST_VERSION = "1.0.0"

C272 = "src/engine/chunks/272.js"
C924 = "src/engine/chunks/924.js"
CLAY = "src/engine/chunks/layout.js"
C404 = "src/engine/chunks/notfound.js"
NFJSX = "src/components/NotFound.jsx"
APP = "src/App.jsx"
PROJ = "src/data/projects.json"
CSS = "src/styles/site.css"
EXCERPT = "extraction/evidence/site.pretty.css"

_lines = {}


def lines_of(root, rel):
    key = (root, rel)
    if key not in _lines:
        base = PROJECT if root == "project" else REPO
        with open(os.path.join(base, rel), encoding="utf-8") as f:
            _lines[key] = f.read().split("\n")
    return _lines[key]


def find(rel, needle, nth=1, root="project", after=0):
    seen = 0
    for i, line in enumerate(lines_of(root, rel), 1):
        if i <= after:
            continue
        if needle in line:
            seen += 1
            if seen == nth:
                return i
    raise SystemExit(f"needle not found: {rel} :: {needle!r} (nth={nth})")


def cite(rel, needle, span=0, nth=1, root="project", note=None, after=0):
    a = find(rel, needle, nth, root, after)
    n = len(lines_of(root, rel))
    b = min(a + span, n)
    c = {"root": root, "file": rel, "lines": f"{a}-{b}" if b != a else str(a), "tag": needle}
    if note:
        c["note"] = note
    return c


def cite_range(rel, start, end, root="project", note=None, nth=1):
    a = find(rel, start, nth, root)
    b = find(rel, end, 1, root, after=a - 1)
    c = {"root": root, "file": rel, "lines": f"{a}-{b}", "tag": start}
    if note:
        c["note"] = note
    return c


def css(needle, note=None):
    return cite(EXCERPT, needle, root="repo", note=note)


def wjson(rel, data):
    path = os.path.join(REPO, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def words(s):
    return len(re.findall(r"\S+", s or ""))


def budget(n, step=5):
    """maxWords budget = measured max rounded up to the next multiple of `step` (min 1)."""
    return max(1, int(math.ceil(n / float(step)) * step)) if n > step else max(1, n)


# ---------------------------------------------------------------------------------------------
# 0. CSS excerpt (site.css is one minified line, so line citations into it are useless)
# ---------------------------------------------------------------------------------------------
CSS_RULE_PATTERNS = [
    r"@font-face\{[^}]*\}",
    r"html\{scrollbar-width:none[^}]*\}",
    r"\.bg-dark\{[^}]*\}",
    r"\.text-color\{[^}]*\}",
    r"\.font-sans\{[^}]*\}",
    r"\.text-white\\/60\{color:#fff9\}",
]
CSS_DECL_PATTERNS = [
    r"--font-sans:[^;}]*",
    r"--text-(?:xs|sm|base|lg|xl|2xl|3xl|5xl|7xl):[^;}]*",
    r"--font-weight-(?:medium|semibold|bold|black):[^;}]*",
    r"--ease-(?:out|in-out):[^;}]*",
    r"--default-transition-(?:duration|timing-function):[^;}]*",
    r"--spacing:[^;}]*",
]
CSS_MEDIA_PATTERNS = [r"@media \(min-width:(?:40rem|48rem|64rem|80rem|96rem|390px)\)",
                      r"@media \(max-height:(?:800px|650px)\)", r"@media \(min-width:1024px\) and \(max-height:680px\)",
                      r"@media \(hover:hover\)"]


def pretty_rule(rule):
    sel, body = rule.split("{", 1)
    body = body.rstrip("}")
    decls = [d for d in re.split(r";(?![^(]*\))", body) if d]
    return sel + " {\n" + "".join(f"  {d};\n" for d in decls) + "}"


def build_css_excerpt():
    src = os.path.join(PROJECT, CSS)
    raw = open(src, encoding="utf-8").read()
    digest = sha256_file(src)
    rules, decls, medias = [], [], []
    for p in CSS_RULE_PATTERNS:
        for m in re.findall(p, raw):
            if m not in rules:
                rules.append(m)
    for p in CSS_DECL_PATTERNS:
        for m in re.findall(p, raw):
            if m not in decls:
                decls.append(m)
    for p in CSS_MEDIA_PATTERNS:
        for m in re.findall(p, raw):
            if m not in medias:
                medias.append(m)
    out = [
        "/* Prettified excerpt of src/styles/site.css (the original compiled stylesheet, one minified line).",
        f"   sha256 of the full source file: {digest}",
        "   Generated by extraction/build_repo.py. Every rule/declaration below occurs verbatim (minified)",
        "   in the source; verify_all.py re-checks that and re-hashes the source when it is present. */",
        "",
        "/* ---- rules ---- */",
    ]
    for r in rules:
        out.append(pretty_rule(r))
    out += ["", "/* ---- theme declarations (from :root / @layer theme) ---- */", ":root {"]
    out += [f"  {d};" for d in decls]
    out += ["}", "", "/* ---- media queries present in the source (headers only) ---- */"]
    out += [f"{m} {{ /* ... */ }}" for m in medias]
    path = os.path.join(REPO, EXCERPT)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    _lines.pop(("repo", EXCERPT), None)
    return digest, rules, decls, medias


# ---------------------------------------------------------------------------------------------
# 1. Source data
# ---------------------------------------------------------------------------------------------
PROJECTS = json.load(open(os.path.join(PROJECT, PROJ), encoding="utf-8"))

ABOUT_ITEMS = []  # parsed from 272.js `D` array (desktop About copy)


def parse_about_items():
    src = "\n".join(lines_of("project", C272))
    m = re.search(r"let D = \[(.*?)\n        \],\n        H = ", src, re.S)
    block = m.group(1)
    for obj in re.finditer(r"\{(.*?)\n          \}", block, re.S):
        body = obj.group(1)
        item = {}
        for key in ("label", "title", "intro", "description", "mobile"):
            mm = re.search(key + r':\s*"((?:[^"\\]|\\.)*)"', body)
            item[key] = mm.group(1) if mm else None
        ABOUT_ITEMS.append(item)


parse_about_items()


def mobile_services():
    src = "\n".join(lines_of("project", C924))
    out = []
    for m in re.finditer(r'title: "([^"]+)",\s*src: "([^"]+)",\s*type: "(\w+)",\s*description:\s*"([^"]+)"', src):
        out.append({"title": m.group(1), "src": m.group(2), "type": m.group(3), "description": m.group(4)})
    return out


MOBILE_SERVICES = mobile_services()

HERO_LINES = ["GRAPHIC DESIGNER", "CRAFTING VISUAL IDENTITIES,", "TYPOGRAPHY AND MOTION."]
INTRO_NOTE = ("Take a look at my selected projects below to see what I've been working on. I'm always open to new "
              "projects, fresh ideas and creative collaborations, so feel free to get in touch.")
NOTFOUND_HEADING = "This page got lost."
NOTFOUND_BODY = "The page you’re looking for doesn’t exist, but my portfolio is still right where it should be."
MOBILE_ABOUT_TITLE = "Behind\nThe Work."

# ---------------------------------------------------------------------------------------------
# 2. Tokens
# ---------------------------------------------------------------------------------------------


def tok(t, v, desc, ev, **extra):
    d = {"$type": t, "$value": v, "$description": desc, "evidence": ev}
    d.update(extra)
    return d


def build_tokens():
    color = {
        "ink": {
            "950": tok("color", "#0b0c09", "Mobile page surface and the loading cover shown while the desktop scene loads.",
                       [cite(C924, "bg-[#0b0c09] text-[#e7e3dd]"), cite(C924, "fixed inset-0 z-[9999] bg-[#0b0c09]")]),
            "900": tok("color", "#0e100c", "Page surface (desktop) and preloader surface.",
                       [css(".bg-dark {"), cite(C924, "bg-[#0e100c] text-[#e7e3dd]")]),
            "850": tok("color", "#0e0d0c", "Overlay backdrop behind project/about overlays (used at 97% opacity).",
                       [cite(C272, "bg-[#0e0d0c]/97 backdrop-blur-[24px]")]),
            "800": tok("color", "#1e211b", "Media placeholder surface behind images/videos while loading (mobile).",
                       [cite(C924, "relative aspect-[4/3] w-full overflow-hidden bg-[#1e211b]")]),
        },
        "paper": {
            "100": tok("color", "#ebe8e4", "Primary text on the page surface (navbar, hero, intro note).",
                       [css(".text-color {")]),
            "200": tok("color", "#e7e3dd", "Text inside overlays, preloader and mobile layout; focus outline colour.",
                       [cite(C272, "pointer-events-none absolute inset-0 z-20 text-[#e7e3dd]"), cite(C924, "bg-[#0e100c] text-[#e7e3dd]")]),
        },
        "neutral": {
            "white": tok("color", "#ffffff", "Hover-title follower (blended with difference), cursor label, 404 copy.",
                         [cite(C272, "tracking-[0.005em] text-white mix-blend-difference"), cite(NFJSX, "text-white transition-opacity")]),
            "black": tok("color", "#000000", "Letterbox behind inline video (mobile project media).",
                         [cite(C924, "pointer-events-none block h-auto w-full bg-black")]),
        },
        "toast": {
            "surface": tok("color", "#ecebeb", "Toast surface (copy-email confirmation).", [cite(APP, "background: '#ecebeb'")]),
            "text": tok("color", "#1c1a17", "Toast text.", [cite(APP, "color: '#1c1a17'")]),
        },
        "gl": {
            "transition-a": tok("color", "#2f302d", "WebGL page-transition shader mix colour A (lerped 52% into a supplied colour).",
                                [cite(CLAY, 'e = new c.Q1f("#2f302d")')], restricted="internal-shader-only"),
            "transition-b": tok("color", "#4a4944", "WebGL page-transition shader mix colour B (lerped 38%).",
                                [cite(CLAY, 'r = new c.Q1f("#4a4944")')], restricted="internal-shader-only"),
            "transition-detail-a": tok("color", "#11130f", "Transition colour A when entering a project detail.",
                                       [cite(CLAY, '{ a: new c.Q1f("#11130f"), b: new c.Q1f("#1e211c") }')], restricted="internal-shader-only"),
            "transition-detail-b": tok("color", "#1e211c", "Transition colour B when entering a project detail.",
                                       [cite(CLAY, '{ a: new c.Q1f("#11130f"), b: new c.Q1f("#1e211c") }')], restricted="internal-shader-only"),
            "transition-default-a": tok("color", "#31362f", "Transition colour A for other destinations.",
                                        [cite(CLAY, '{ a: new c.Q1f("#31362f"), b: new c.Q1f("#545c51") }')], restricted="internal-shader-only"),
            "transition-default-b": tok("color", "#545c51", "Transition colour B for other destinations.",
                                        [cite(CLAY, '{ a: new c.Q1f("#31362f"), b: new c.Q1f("#545c51") }')], restricted="internal-shader-only"),
            "plane-alpha-background": tok("color", "vec3(0.88, 0.871, 0.871)",
                                          "Shader constant ALPHA_BACKGROUND that transparent texels of gallery planes are mixed toward. Written as-is it is #e0dede; read as linear and encoded to sRGB it is #f1f0f0. Kept as the raw shader value.",
                                          [cite(C272, "uniform sampler2D uTexture;", note="fragment shader string (single long line); contains ALPHA_BACKGROUND = vec3(0.88, 0.871, 0.871)")],
                                          restricted="internal-shader-only"),
        },
    }
    opacity = {
        "100": tok("number", 1, "Active item / full emphasis.", [cite(C272, '"text-[#e7e3dd] opacity-100"')]),
        "97": tok("number", 0.97, "Overlay backdrop opacity.", [cite(C272, "bg-[#0e0d0c]/97")]),
        "90": tok("number", 0.9, "Meta values (year/tools), mobile body text.", [cite(C272, "font-medium leading-[1.3] text-[#e7e3dd]/90")]),
        "85": tok("number", 0.85, "Mobile project description.", [cite(C924, "text-[17px] leading-[1.45] text-[#e7e3dd]/85")]),
        "80": tok("number", 0.8, "Overlay intro/body copy and micro labels.", [cite(C272, "leading-[1.55] text-[#e7e3dd]/80 lg:block")]),
        "78": tok("number", 0.78, "Project description on desktop.", [cite(C272, "leading-[1.55] text-[#e7e3dd]/78")]),
        "65": tok("number", 0.65, "Mobile about discipline label.", [cite(C272, "tracking-[0.08em] text-[#e7e3dd]/65")]),
        "60": tok("number", 0.6, "404 body copy (white at 60%).", [css(".text-white\\/60 {"), cite(NFJSX, "text-white/60")]),
        "55": tok("number", 0.55, "Overlay mobile meta labels.", [cite(C272, "tracking-[0.2em] text-[#e7e3dd]/55")]),
        "50": tok("number", 0.5, "Link hover opacity (navbar, footer links).", [cite(CLAY, "transition-opacity duration-300 hover:opacity-50")]),
        "45": tok("number", 0.45, "Overlay mobile description label.", [cite(C272, "tracking-[0.2em] text-[#e7e3dd]/45")]),
        "40": tok("number", 0.4, "Separator slash in about footer meta.", [cite(C272, '"hidden opacity-40 md:inline"')]),
        "30": tok("number", 0.3, "Inactive pagination number / inactive discipline menu item.", [cite(C272, "opacity-30 hover:opacity-100"), cite(C272, "style: { opacity: l === t ? 1 : 0.3 }")]),
        "20": tok("number", 0.2, "Hairline border above mobile project meta; preloader ghost wordmark.", [cite(C924, "border-t border-[#e7e3dd]/20"), cite(C924, 'className: "text-[#e7e3dd]/20"')]),
    }
    typography = {
        "family": {
            "display": tok("fontFamily", ["Satoshi", "Arial", "Helvetica", "sans-serif"],
                           "Page font for everything not explicitly set to the UI stack. Elements tagged with the source's `font-bueno` class resolve here too: that class is not defined in the stylesheet, so they inherit the html family.",
                           [css("html {"), css("font-family:Satoshi,Arial")]),
            "ui": tok("fontFamily", ["ui-sans-serif", "system-ui", "sans-serif", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"],
                      "System UI stack for micro labels, tags, year/tools labels and the cursor label.",
                      [css("--font-sans:"), css(".font-sans {")]),
            "digits": tok("fontFamily", ["Arial", "Helvetica", "sans-serif"], "Canvas font of the 404 floating digits (weight 900, 380px texture).",
                          [cite(C404, '(n.font = "900 380px Arial, Helvetica, sans-serif")')]),
        },
        "weight": {
            "regular": tok("fontWeight", 400, "Body copy.", [css("font-weight:400")]),
            "medium": tok("fontWeight", 500, "Navbar, meta values, menus, preloader wordmark.", [css("--font-weight-medium:500")]),
            "semibold": tok("fontWeight", 600, "Cursor label, 404 heading.", [css("--font-weight-semibold:600"), cite(C272, "text-[14px] font-semibold uppercase leading-none tracking-[0.11em]")]),
            "bold": tok("fontWeight", 700, "Display headings (hero, project and about titles).", [css("--font-weight-bold:700")]),
            "black": tok("fontWeight", 900, "404 back link; 404 digits.", [css("--font-weight-black:900"), cite(NFJSX, "font-black uppercase")]),
        },
        "size": {
            "hero-display": tok("fontSize", "clamp(25px, 2.15vw, 38px)", "Hero heading, desktop (>=1024px). Below 1024px the overlay uses clamp(22px, 4.2vw, 32px).",
                                [cite(C272, "text-[clamp(22px,4.2vw,32px)] font-bold leading-[1.1] tracking-[-0.035em] lg:text-[clamp(25px,2.15vw,38px)]")]),
            "hero-display-mobile": tok("fontSize", "clamp(28px, 7.3vw, 46px)", "Hero heading in the mobile list layout (<1024px).",
                                       [cite(C924, "max-w-[560px] font-bueno text-[clamp(28px,7.3vw,46px)]")]),
            "project-title": tok("fontSize", "clamp(22px, 1.45vw, 27px)", "Project title in the detail overlay (>=768px); clamp(21px, 4.5vw, 28px) below.",
                                 [cite(C272, "md:text-[clamp(22px,1.45vw,27px)]")]),
            "project-title-mobile": tok("fontSize", "clamp(31px, 8vw, 54px)", "Project title in the mobile article layout.",
                                        [cite(C924, "max-w-[580px] font-bueno text-[clamp(31px,8vw,54px)]")]),
            "about-title": tok("fontSize", "clamp(20px, 1.7vw, 32px)", "About discipline title (titles longer than 15 characters use clamp(15px, 1.35vw, 24px)).",
                               [cite(C272, '"text-[clamp(15px,1.35vw,24px)]"', span=1)]),
            "body-overlay": tok("fontSize", "clamp(15px, 1.05vw, 18px)", "Project description in the overlay (15px below 800px viewport height, 14px below 650px).",
                                [cite(C272, "break-words font-bueno text-[clamp(15px,1.05vw,18px)]")]),
            "body-about": tok("fontSize", "clamp(15px, 1.08vw, 19px)", "About intro/description in the overlay.",
                              [cite(C272, "mt-5 hidden font-bueno text-[clamp(15px,1.08vw,19px)]")]),
            "nav-value": tok("fontSize", "clamp(15px, 1.1vw, 20px)", "Navbar values (15px below 1024px).",
                             [cite(CLAY, "font-bueno text-[15px] font-medium leading-[1.18] tracking-[-0.025em] lg:text-[clamp(15px,1.1vw,20px)]")]),
            "menu-item": tok("fontSize", "clamp(16px, 1.1vw, 19px)", "About discipline menu items and meta values.",
                             [cite(C272, "flex flex-col items-end font-bueno text-[clamp(16px,1.1vw,19px)]")]),
            "pagination": tok("fontSize", "clamp(15px, 1.15vw, 19px)", "Project media pagination numbers.",
                              [cite(C272, "font-bueno text-[clamp(15px,1.15vw,19px)] font-medium tabular-nums")]),
            "intro-note": tok("fontSize", "17px", "Intro note paragraph on the home page (14px below 1024px).",
                              [cite(C272, "text-[14px] leading-[1.45] tracking-[-0.025em] text-color lg:text-[17px]")]),
            "nav-label": tok("fontSize", "0.875rem", "Navbar column labels (text-sm, 14px).", [css("--text-sm:.875rem"), cite(CLAY, 'className: "text-sm",')]),
            "cursor-label": tok("fontSize", "14px", "Kinetic cursor label.", [cite(C272, "whitespace-nowrap font-sans text-[14px] font-semibold uppercase")]),
            "micro": tok("fontSize", "10px", "Micro labels (scroll hint, year/tools labels, tags) at >=768px; 9px below (tags 8px).",
                         [cite(C272, "text-[9px] font-medium uppercase leading-[1.4] tracking-[0.16em] text-[#e7e3dd]/80 md:text-[10px]")]),
            "preloader-wordmark": tok("fontSize", "1.25rem", "Preloader wordmark (text-xl, 20px).", [css("--text-xl:1.25rem"), cite(C924, "font-bueno text-xl font-medium uppercase leading-none tracking-[0.22em]")]),
            "notfound-heading": tok("fontSize", "3rem", "404 heading at >=768px (text-5xl); 1.875rem below.", [css("--text-5xl:3rem"), cite(NFJSX, "md:text-5xl")]),
            "notfound-body": tok("fontSize", "1.25rem", "404 body at >=768px (text-xl); 1.125rem below.", [css("--text-lg:1.125rem"), cite(NFJSX, "md:text-xl")]),
            "hover-title": tok("fontSize", "clamp(11px, 0.048 * plane-width, 16px)", "Hover-title follower size, computed per frame from the projected plane width.",
                               [cite(C272, "p = c.cj9.clamp(0.048 * d, 11, 16);")]),
            "mobile-body": tok("fontSize", "17px", "Mobile project description and mobile footer-adjacent body copy.", [cite(C924, "whitespace-pre-line font-bueno text-[17px] leading-[1.45]")]),
            "mobile-about-body": tok("fontSize", "clamp(19px, 5vw, 24px)", "Mobile about bio.", [cite(C924, "max-w-[500px] space-y-7  text-[clamp(19px,5vw,24px)]")]),
            "mobile-card-title": tok("fontSize", "12px", "Mobile work card title (14px from 640px).", [cite(C924, "mt-2.5 font-bueno text-[12px] font-medium uppercase leading-[1.25] sm:text-[14px]")]),
            "mobile-footer": tok("fontSize", "15px", "Mobile footer columns.", [cite(C924, "grid grid-cols-2 gap-x-6 text-[15px] font-medium leading-[1.25]")]),
        },
        "lineHeight": {
            "tight-085": tok("lineHeight", 0.85, "Mobile about display heading.", [cite(C924, "leading-[0.85] tracking-[-0.045em]")]),
            "display-102": tok("lineHeight", 1.02, "Hover title; mobile project title.", [cite(C272, "uppercase leading-[1.02] tracking-[0.005em]")]),
            "display-104": tok("lineHeight", 1.04, "Mobile hero heading.", [cite(C924, "font-bold uppercase leading-[1.04] tracking-[-0.035em]")]),
            "display-105": tok("lineHeight", 1.05, "About title.", [cite(C272, "font-bold uppercase leading-[1.05] tracking-[-0.025em]")]),
            "display-108": tok("lineHeight", 1.08, "Project title.", [cite(C272, "font-bold uppercase leading-[1.08] tracking-[-0.012em]")]),
            "display-110": tok("lineHeight", 1.1, "Hero heading.", [cite(C272, "font-bold leading-[1.1] tracking-[-0.035em]")]),
            "ui-118": tok("lineHeight", 1.18, "Navbar.", [cite(CLAY, "leading-[1.18]")]),
            "ui-130": tok("lineHeight", 1.3, "Meta values.", [cite(C272, "font-medium leading-[1.3]")]),
            "ui-140": tok("lineHeight", 1.4, "Micro labels; discipline menu.", [cite(C272, "font-medium leading-[1.4]\",")]),
            "body-145": tok("lineHeight", 1.45, "Intro note; mobile body.", [cite(C272, "text-[14px] leading-[1.45]")]),
            "body-155": tok("lineHeight", 1.55, "Overlay body copy.", [cite(C272, "leading-[1.55] text-[#e7e3dd]/78")]),
        },
        "tracking": {
            "display-tight": tok("letterSpacing", "-0.035em", "Hero and mobile display headings.", [cite(C272, "leading-[1.1] tracking-[-0.035em]")]),
            "ui-tight": tok("letterSpacing", "-0.025em", "Navbar, intro note, about title.", [cite(CLAY, "tracking-[-0.025em]")]),
            "title-tight": tok("letterSpacing", "-0.012em", "Project title.", [cite(C272, "tracking-[-0.012em]")]),
            "hover-title": tok("letterSpacing", "0.005em", "Hover-title follower.", [cite(C272, "tracking-[0.005em]")]),
            "label-wide": tok("letterSpacing", "0.16em", "Micro labels (scroll hint, tags).", [cite(C272, "leading-[1.4] tracking-[0.16em]")]),
            "label-wider": tok("letterSpacing", "0.18em", "Year/Tools labels.", [cite(C272, "font-medium  tracking-[0.18em]")]),
            "cursor": tok("letterSpacing", "0.11em", "Cursor label.", [cite(C272, "leading-none tracking-[0.11em]")]),
            "wordmark": tok("letterSpacing", "0.22em", "Preloader wordmark.", [cite(C924, "tracking-[0.22em]")]),
        },
    }
    spacing = {
        "base": tok("dimension", "0.25rem", "Spacing unit; all utility spacing is a multiple of it.", [css("--spacing:.25rem")]),
        "1": tok("dimension", "4px", "Media nav button horizontal padding; tight gaps.", [cite(C272, "shrink-0 border-0 bg-transparent px-1 py-2")]),
        "2": tok("dimension", "8px", "Footer grid gap (mobile), pagination vertical padding.", [cite(C272, "grid-cols-[minmax(0,1fr)_minmax(0,1fr)_minmax(0,1fr)] items-end gap-2")]),
        "3": tok("dimension", "12px", "Label-to-value gap; mobile card grid column gap; media stack gap.", [cite(C272, '"mb-3 font-sans text-[10px] font-medium  tracking-[0.18em]')]),
        "5": tok("dimension", "20px", "About title to body; mobile grid gaps.", [cite(C272, "mt-5 hidden font-bueno")]),
        "6": tok("dimension", "24px", "Meta column gap; paragraph gap in about body.", [cite(C272, "hidden w-[18.5%] flex-col items-start gap-6 md:flex")]),
        "7": tok("dimension", "28px", "About footer gap (desktop).", [cite(C272, "lg:flex lg:items-end lg:gap-7")]),
        "8": tok("dimension", "32px", "Title to description (>=768px); mobile card row gap.", [cite(C272, "mt-8 hidden md:block lg:mt-11")]),
        "11": tok("dimension", "44px", "Title to description at >=1024px.", [cite(C272, "lg:mt-11")]),
        "12": tok("dimension", "48px", "Mobile meta block top margin.", [cite(C924, "mt-12 grid grid-cols-2 gap-x-5 gap-y-9")]),
        "16": tok("dimension", "64px", "Mobile section spacing (hero top, work list top, footer top).", [cite(C924, 'className: "mt-16 sm:mt-20"')]),
        "20": tok("dimension", "80px", "Mobile discipline stack gap.", [cite(C924, 'className: "space-y-20"')]),
        "24": tok("dimension", "96px", "Mobile services block top margin.", [cite(C924, 'className: "mt-24"')]),
        "nav-offset-mobile": tok("dimension", "72px", "Top padding of the mobile layout under the fixed navbar.", [cite(C924, 'pt-[72px]')]),
    }
    radius = {"none": tok("dimension", "0px", "No rounded corners anywhere in the rendered UI (images, planes, buttons are square). The stylesheet's only radius utility (rounded-full) is not used by any rendered element.",
                          [cite(C924, "aspect-[4/5] w-full object-cover")])}
    effect = {
        "backdrop-blur": tok("dimension", "24px", "Backdrop blur behind overlays.", [cite(C272, "backdrop-blur-[24px]")]),
        "reveal-blur": tok("dimension", "3px", "Initial blur of words in the word-reveal pattern.", [cite(C272, 'hidden: { y: "115%", opacity: 0, filter: "blur(3px)" },')]),
        "unfocused-plane-darken": tok("number", 0.6, "Non-hovered gallery planes blur and darken by 60% while one plane is hovered.", [cite(C272, "let x = l || R || !ep || s ? 0 : 1;", span=4)]),
    }
    breakpoint = {
        "xs": tok("dimension", "390px", "Custom min-width query present in the stylesheet.", [css("@media (min-width:390px)")]),
        "sm": tok("dimension", "640px", "40rem.", [css("@media (min-width:40rem)")]),
        "md": tok("dimension", "768px", "48rem: overlay detail switches from stacked mobile meta to side columns.", [css("@media (min-width:48rem)")]),
        "lg": tok("dimension", "1024px", "64rem: the layout switch. Below it (matchMedia max-width 1023px) the page renders the scrolling list layout; at and above it the single-viewport WebGL scene.",
                  [css("@media (min-width:64rem)"), cite(C924, 'window.matchMedia("(max-width: 1023px)")')]),
        "xl": tok("dimension", "1280px", "80rem.", [css("@media (min-width:80rem)")]),
        "2xl": tok("dimension", "1536px", "96rem.", [css("@media (min-width:96rem)")]),
        "short-800": tok("dimension", "800px", "max-height query: overlay description shrinks to 15px.", [css("@media (max-height:800px)")]),
        "short-650": tok("dimension", "650px", "max-height query: overlay description shrinks to 14px.", [css("@media (max-height:650px)")]),
        "short-desktop-680": tok("dimension", "680px", "(min-width:1024px) and (max-height:680px): intro note hidden.", [css("@media (min-width:1024px) and (max-height:680px)")]),
    }
    motion = {
        "easing": {
            "reveal": tok("cubicBezier", [0.16, 1, 0.3, 1], "Primary reveal/entrance curve (words, navbar, overlays, 404 arrow).", [cite(C272, "let ee = [0.16, 1, 0.3, 1],"), cite(CLAY, "let s = [0.16, 1, 0.3, 1],")]),
            "preloader-exit": tok("cubicBezier", [0.76, 0, 0.24, 1], "Preloader slide-out.", [cite(C924, "let p = [0.76, 0, 0.24, 1];")]),
            "standard": tok("cubicBezier", [0.4, 0, 0.2, 1], "Default CSS transition curve (opacity hovers).", [css("--ease-in-out:cubic-bezier(.4,0,.2,1)")]),
            "expo-out": tok("string", "expo.out", "Cursor entry/press tween curve.", [cite(C272, 'ease: "expo.out",')]),
            "cosine-in-out": tok("string", "-(cos(pi*t)-1)/2", "Page-transition progress curve.", [cite(CLAY, "f = -(Math.cos(Math.PI * d) - 1) / 2,")]),
        },
        "duration": {
            "instant": tok("duration", "150ms", "Reduced-motion exit.", [cite(C272, "exit: { opacity: 0, transition: { duration: 0.15 } },")]),
            "fast": tok("duration", "200ms", "Reduced-motion fades; hover-title container fade.", [cite(C272, "visible: { opacity: 1, transition: { duration: 0.2 } },")]),
            "hover": tok("duration", "300ms", "Link/pagination opacity transitions.", [cite(C272, "transition-opacity duration-300 ease-in-out")]),
            "exit": tok("duration", "350ms", "Hero intro exit.", [cite(C272, "exit: { opacity: 0, transition: { duration: 0.35, ease: ee } },")]),
            "cursor-entry": tok("duration", "420ms", "Cursor entry tween.", [cite(C272, "duration: 0.42,")]),
            "menu": tok("duration", "500ms", "About discipline menu opacity transition.", [cite(C272, "transition-opacity duration-500 ease-in-out")]),
            "transition-leave": tok("duration", "680ms", "WebGL page transition, leaving phase.", [cite(CLAY, 'let s = "entering" === e ? 0.82 : 0.68,')]),
            "word": tok("duration", "700ms", "Word reveal in overlays.", [cite(C272, "transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] },")]),
            "about-swap": tok("duration", "750ms", "About content cross-fade.", [cite(C272, "transition: { opacity: { duration: 0.75, ease: H } },")]),
            "transition-enter": tok("duration", "820ms", "WebGL page transition, entering phase.", [cite(CLAY, 'let s = "entering" === e ? 0.82 : 0.68,')]),
            "entrance": tok("duration", "850ms", "Navbar entrance; hero word reveal; preloader slide-out.", [cite(CLAY, "transition: { duration: 0.85, delay: t, ease: s },")]),
            "digits-loop": tok("duration", "6.5s", "404 digits float loop.", [cite(C404, "r = (t % 6.5) / 6.5,")]),
        },
        "stagger": {
            "letters-menu": tok("duration", "12ms", "About menu label words.", [cite(C272, "stagger: 0.012,")]),
            "body": tok("duration", "15ms", "Overlay body words (default).", [cite(C272, "stagger: l = 0.015,")]),
            "intro-note": tok("duration", "18ms", "Intro note words.", [cite(C272, "stagger: 0.018,")]),
            "title": tok("duration", "25ms", "Overlay titles.", [cite(C272, "stagger: 0.025,")]),
            "overlay-groups": tok("duration", "35ms", "Overlay group stagger.", [cite(C272, "visible: { transition: { delayChildren: 0, staggerChildren: 0.035 } },")]),
            "hero-words": tok("duration", "45ms", "Hero heading words.", [cite(C272, "stagger: 0.045,")]),
            "hero-first-line": tok("duration", "60ms", "Hero first line words.", [cite(C272, "stagger: 0.06,")]),
            "navbar-columns": tok("duration", "80ms", "Navbar column entrance delays step (0, 0.08 ... 0.32s).", [cite(CLAY, "delay: 0.08,")]),
            "hero-lines": tok("duration", "120ms", "Hero heading lines.", [cite(C272, "visible: { transition: { staggerChildren: 0.12 } },")]),
        },
        "damping": {
            "scroll": tok("number", 9, "Wheel-driven strip scroll damping factor.", [cite(C272, "(D.current = c.cj9.damp(D.current, n.current, 9, el))));")]),
            "hover": tok("number", 5.5, "Plane hover damping.", [cite(C272, "d = c.cj9.damp(", span=6)]),
            "blur": tok("number", 7, "Unfocused-plane blur damping.", [cite(C272, ": c.cj9.damp(h.uBlur.value, x, 7, el)),")]),
            "cursor-follow": tok("number", 10, "Cursor follow: 1 - exp(-10 dt).", [cite(C272, "a = o ? 1 : 1 - Math.exp(-10 * l),")]),
        },
    }
    layout = {
        "gutter": {
            "mobile": tok("dimension", "5%", "Page side gutter below 1024px (navbar, mobile layout, overlay left edge).", [cite(C924, 'className: "w-full px-[5%] ".concat(')]),
            "desktop-nav": tok("dimension", "3.1%", "Navbar side gutter and hero left edge at >=1024px.", [cite(CLAY, "lg:px-[3.1%]")]),
            "desktop-overlay": tok("dimension", "3.5%", "Overlay text column left edge at >=768/1024px.", [cite(C272, "md:left-[3.5%] md:top-[27%] md:w-[20.5%]")]),
            "desktop-footer": tok("dimension", "5.3%", "Overlay footer bar left edge.", [cite(C272, "md:bottom-[5%] md:left-[5.3%] md:right-[4%]")]),
        },
        "column": {
            "overlay-text": tok("dimension", "20.5%", "Project overlay text column width (about: 21%).", [cite(C272, "md:w-[20.5%]")]),
            "overlay-meta": tok("dimension", "18.5%", "Project meta column width (right, bottom 26%).", [cite(C272, "bottom-[26%] right-[3.8%] hidden w-[18.5%]")]),
            "hero-heading": tok("dimension", "70%", "Hero heading block width at >=1024px (top 32%).", [cite(C272, "lg:left-[3.1%] lg:top-[32%] lg:w-[70%]")]),
            "portrait-thumb": tok("dimension", "clamp(150px, 12vw, 210px)", "Portrait thumbnail width (4:5) at >=1024px, top 150px.", [cite(C272, "lg:top-[150px] lg:w-[clamp(150px,12vw,210px)]")]),
        },
        "viewport": {
            "stage": tok("dimension", "100svh", "Desktop page is one 100svh stage with no document scroll; the wheel drives the gallery.", [cite(C272, '"relative h-svh w-full touch-none overflow-hidden bg-transparent "')]),
        },
        "gallery": {
            "plane-heights": tok("list", [0.14, 0.18, 0.13, 0.16, 0.15, 0.19], "Plane heights as fractions of viewport height, cycled per project.", [cite(C272, "let h = [0.14, 0.18, 0.13, 0.16, 0.15, 0.19],")]),
            "plane-gap": tok("list", {"desktop": "1.2vw", "touch": "3.5vw"}, "Gap between planes as a fraction of viewport width.", [cite(C272, "let e = N.width * (R ? 0.035 : 0.012),")]),
        },
        "grid": {
            "mobile-work": tok("string", "2 columns, 12px column gap, 32px row gap, 4:3 covers", "Mobile 'selected work' grid.", [cite(C924, "grid grid-cols-2 items-start gap-x-3 gap-y-8")]),
            "navbar": tok("string", "5 columns justified space-between (name, occupation, location, connect, profile); 2 below 1024px", "Navbar columns.", [cite(CLAY, '"flex w-full items-start justify-between gap-x-5 ".concat(')]),
            "footer-bar": tok("string", "3 equal columns: hint | tags | pagination", "Project footer bar.", [cite(C272, "grid-cols-[minmax(0,1fr)_minmax(0,1fr)_minmax(0,1fr)]")]),
        },
    }
    semantic = {
        "text": {
            "primary": {"$type": "color", "$value": "{color.paper.100}", "$description": "Text on the page surface.", "evidence": [css(".text-color {")]},
            "overlay": {"$type": "color", "$value": "{color.paper.200}", "$description": "Text inside overlays and the mobile layout.", "evidence": [cite(C272, "pointer-events-none absolute inset-0 z-20 text-[#e7e3dd]")]},
            "overlay-muted": {"$type": "color", "$value": "{color.paper.200}", "opacity": "{opacity.80}", "$description": "Overlay body copy and micro labels.", "evidence": [cite(C272, "leading-[1.55] text-[#e7e3dd]/80 lg:block")]},
            "overlay-subtle": {"$type": "color", "$value": "{color.paper.200}", "opacity": "{opacity.55}", "$description": "Quiet labels.", "evidence": [cite(C272, "tracking-[0.2em] text-[#e7e3dd]/55")]},
            "inverse-blend": {"$type": "color", "$value": "{color.neutral.white}", "$description": "White text rendered with difference blending over imagery (hover title).", "evidence": [cite(C272, "text-white mix-blend-difference")]},
            "on-toast": {"$type": "color", "$value": "{color.toast.text}", "$description": "Toast text.", "evidence": [cite(APP, "color: '#1c1a17'")]},
        },
        "surface": {
            "page": {"$type": "color", "$value": "{color.ink.900}", "$description": "Desktop page / preloader.", "evidence": [css(".bg-dark {")]},
            "page-mobile": {"$type": "color", "$value": "{color.ink.950}", "$description": "Mobile layout surface; loading cover.", "evidence": [cite(C924, "bg-[#0b0c09] text-[#e7e3dd]")]},
            "backdrop": {"$type": "color", "$value": "{color.ink.850}", "opacity": "{opacity.97}", "$description": "Overlay backdrop (with 24px blur).", "evidence": [cite(C272, "bg-[#0e0d0c]/97")]},
            "media-placeholder": {"$type": "color", "$value": "{color.ink.800}", "$description": "Behind media while loading.", "evidence": [cite(C924, "overflow-hidden bg-[#1e211b]")]},
            "toast": {"$type": "color", "$value": "{color.toast.surface}", "$description": "Toast surface.", "evidence": [cite(APP, "background: '#ecebeb'")]},
        },
        "border": {
            "hairline": {"$type": "color", "$value": "{color.paper.200}", "opacity": "{opacity.20}", "$description": "Divider above mobile project meta.", "evidence": [cite(C924, "border-t border-[#e7e3dd]/20")]},
        },
        "focus": {
            "outline": {"$type": "color", "$value": "{color.paper.200}", "$description": "1px focus-visible outline on overlay buttons.", "evidence": [cite(C272, "focus-visible:outline-[#e7e3dd]")]},
        },
    }
    component = {
        "navbar": {
            "label-size": {"$type": "fontSize", "$value": "{typography.size.nav-label}", "$description": "Column label.", "evidence": [cite(CLAY, 'className: "text-sm",')]},
            "value-size": {"$type": "fontSize", "$value": "{typography.size.nav-value}", "$description": "Column value.", "evidence": [cite(CLAY, "lg:text-[clamp(15px,1.1vw,20px)]")]},
            "link-hover-opacity": {"$type": "number", "$value": "{opacity.50}", "$description": "Link hover.", "evidence": [cite(CLAY, "hover:opacity-50")]},
        },
        "overlay": {
            "title-size": {"$type": "fontSize", "$value": "{typography.size.project-title}", "$description": "Overlay title.", "evidence": [cite(C272, "md:text-[clamp(22px,1.45vw,27px)]")]},
            "body-size": {"$type": "fontSize", "$value": "{typography.size.body-overlay}", "$description": "Overlay body.", "evidence": [cite(C272, "text-[clamp(15px,1.05vw,18px)]")]},
            "pagination-inactive-opacity": {"$type": "number", "$value": "{opacity.30}", "$description": "Inactive media number.", "evidence": [cite(C272, "opacity-30 hover:opacity-100")]},
        },
        "cursor": {
            "label-size": {"$type": "fontSize", "$value": "{typography.size.cursor-label}", "$description": "Cursor label.", "evidence": [cite(C272, "text-[14px] font-semibold uppercase leading-none tracking-[0.11em]")]},
            "press-scale": {"$type": "number", "$value": 0.82, "$description": "Scale while pressed.", "evidence": [cite(C272, "scale: 0.82,")]},
            "max-tilt": {"$type": "number", "$value": 2.5, "$description": "Velocity tilt limit (degrees).", "evidence": [cite(C272, "Math.max(-2.5, Math.min(2.5, 0.22 * c + 0.04 * d)),")]},
        },
    }
    dark = {"theme": "dark", "$description": "The site is dark-only: there is no light theme, no theme toggle and no prefers-color-scheme rule in the source. Every semantic token resolves here.",
            "evidence": [css(".bg-dark {"), css(".text-color {")], "resolves": {}}
    files = {
        "tokens/00-foundation/color.json": {"color": color},
        "tokens/00-foundation/opacity.json": {"opacity": opacity},
        "tokens/00-foundation/typography.json": {"typography": typography},
        "tokens/00-foundation/spacing.json": {"spacing": spacing},
        "tokens/00-foundation/radius.json": {"radius": radius},
        "tokens/00-foundation/effect.json": {"effect": effect},
        "tokens/00-foundation/breakpoint.json": {"breakpoint": breakpoint},
        "tokens/00-foundation/motion.json": {"motion": motion},
        "tokens/10-semantic/semantic.json": semantic,
        "tokens/20-component/component.json": component,
        "tokens/30-layout/layout.json": {"layout": layout},
    }
    flat = {}

    def walk(prefix, node, layer, path):
        if isinstance(node, dict) and "$value" in node:
            flat[prefix] = {"layer": layer, "file": path, "type": node["$type"], "value": node["$value"], "description": node["$description"],
                            "restricted": node.get("restricted"), "opacity": node.get("opacity")}
            return
        if isinstance(node, dict):
            for k, v in node.items():
                if k.startswith("$") or k == "evidence":
                    continue
                walk(f"{prefix}.{k}" if prefix else k, v, layer, path)

    for path, data in files.items():
        layer = path.split("/")[1]
        prefix = {"10-semantic": "", "20-component": "component"}.get(layer, "")
        walk(prefix, data, layer, path)
        wjson(path, data)
    # resolve references for the theme
    def resolve(v):
        if isinstance(v, str) and v.startswith("{") and v.endswith("}"):
            ref = v[1:-1]
            if ref not in flat:
                raise SystemExit(f"unresolved token reference {v}")
            return resolve(flat[ref]["value"])
        return v
    for tid, t in sorted(flat.items()):
        if t["layer"] in ("10-semantic", "20-component"):
            r = {"value": resolve(t["value"])}
            if t.get("opacity"):
                r["opacity"] = resolve(t["opacity"])
            dark["resolves"][tid] = r
    wjson("tokens/themes/dark.json", dark)
    return flat


# ---------------------------------------------------------------------------------------------
# 3. Motion patterns (fallbacks pinned again in schema/semantic_validate.py)
# ---------------------------------------------------------------------------------------------
MOTION_PATTERNS = {
    "word-reveal": {"description": "Each word rises from 115% below its own clipped line box while fading in and un-blurring 3px to 0, staggered per word.",
                    "timing": {"duration": "{motion.duration.word}", "easing": "{motion.easing.reveal}", "stagger": "{motion.stagger.body}"},
                    "reducedMotionFallback": "opacity-fade", "sourceImplementsFallback": True,
                    "evidence": [cite_range(C272, "function k(e) {", "      function S(e) {"), cite(C272, "variants: a ? C : P,")]},
    "staggered-fade-up": {"description": "Navbar columns fade in from 14px below, 0.85s reveal curve, delays 0/0.08/0.16/0.24/0.32s.",
                          "timing": {"duration": "{motion.duration.entrance}", "easing": "{motion.easing.reveal}", "stagger": "{motion.stagger.navbar-columns}"},
                          "reducedMotionFallback": "opacity-fade", "sourceImplementsFallback": False,
                          "evidence": [cite(CLAY, "initial: { opacity: 0, y: 14 },", span=3)]},
    "gallery-strip-scroll": {"description": "Infinite horizontal strip of textured planes; the wheel moves a damped target (damping 9); planes bend toward the pointer and at the viewport edges.",
                             "timing": {"damping": "{motion.damping.scroll}"},
                             "reducedMotionFallback": "static-strip", "sourceImplementsFallback": False,
                             "evidence": [cite(C272, "(D.current = c.cj9.damp(D.current, n.current, 9, el))));"), cite(C272, "uniform float uTime, uHover, uWorldScale, uEdgeBend")]},
    "hover-focus-blur": {"description": "Hovering a plane focuses it; the other planes blur and darken by 60% (damping 5.5 hover, 7 blur) and the hover-title follows the plane.",
                         "timing": {"damping": "{motion.damping.hover}"},
                         "reducedMotionFallback": "no-blur-highlight", "sourceImplementsFallback": False,
                         "evidence": [cite(C272, ": c.cj9.damp(h.uBlur.value, x, 7, el)),"), cite(C272, "d = c.cj9.damp(", span=6)]},
    "plane-focus-stage": {"description": "Opening a project morphs the chosen plane into a centred stage with backdrop fade; clicks/wheel step through media; pagination jumps.",
                          "timing": {"easing": "{motion.easing.reveal}"},
                          "reducedMotionFallback": "crossfade-stage", "sourceImplementsFallback": False,
                          "evidence": [cite(C272, "uTransitionBend, uMorph"), cite_range(C272, "function N(e) {", "      function I(e) {")]},
    "kinetic-cursor": {"description": "Custom cursor label (RETURN / NEXT) follows the pointer with 1-exp(-10dt) lerp, tilts with velocity up to 2.5deg, enters with a 0.42s expo-out tween and scales to 0.82 when pressed. Only on hover-capable fine pointers.",
                       "timing": {"duration": "{motion.duration.cursor-entry}", "easing": "{motion.easing.expo-out}", "damping": "{motion.damping.cursor-follow}"},
                       "reducedMotionFallback": "snap-follow", "sourceImplementsFallback": True,
                       "evidence": [cite(C272, "a = o ? 1 : 1 - Math.exp(-10 * l),"), cite(C272, '"(prefers-reduced-motion: reduce)",')]},
    "page-transition-wipe": {"description": "Full-screen WebGL wipe between routes: entering 0.82s, leaving 0.68s, cosine ease-in-out; colours depend on destination.",
                             "timing": {"duration": "{motion.duration.transition-enter}", "easing": "{motion.easing.cosine-in-out}"},
                             "reducedMotionFallback": "instant-route-change", "sourceImplementsFallback": True,
                             "evidence": [cite(CLAY, 'let s = "entering" === e ? 0.82 : 0.68,'), cite(CLAY, "if (l) return void t.push(n);")]},
    "preloader-wipe": {"description": "Wordmark shown as a 20% ghost with a clip-path reveal driven by load progress, then the cover slides up 100% over 0.85s on the exit curve.",
                       "timing": {"duration": "{motion.duration.entrance}", "easing": "{motion.easing.preloader-exit}"},
                       "reducedMotionFallback": "instant-hide", "sourceImplementsFallback": False,
                       "evidence": [cite(C924, "let p = [0.76, 0, 0.24, 1];"), cite(C924, '(h.current.style.clipPath = "inset(0 ".concat(')]},
    "opacity-hover": {"description": "Links and buttons drop to 50% opacity (300ms) on hover; pagination numbers rise from 30% to 100%.",
                      "timing": {"duration": "{motion.duration.hover}", "easing": "{motion.easing.standard}"},
                      "reducedMotionFallback": "opacity-hover", "sourceImplementsFallback": True,
                      "evidence": [cite(CLAY, "transition-opacity duration-300 hover:opacity-50")]},
    "content-crossfade": {"description": "About content swaps with a 0.75s opacity cross-fade (0.45s out) when the discipline changes.",
                          "timing": {"duration": "{motion.duration.about-swap}", "easing": "{motion.easing.reveal}"},
                          "reducedMotionFallback": "opacity-fade", "sourceImplementsFallback": True,
                          "evidence": [cite(C272, "transition: { opacity: { duration: 0.75, ease: H } },"), cite(C272, "d = u ? _ : G;")]},
    "floating-digits": {"description": "Three canvas-textured digits float and sway on a 6.5s loop behind the 404 message.",
                        "timing": {"duration": "{motion.duration.digits-loop}"},
                        "reducedMotionFallback": "static-digits", "sourceImplementsFallback": False,
                        "evidence": [cite(C404, "r = (t % 6.5) / 6.5,")]},
    "backdrop-fade": {"description": "Overlay backdrop (97% ink, 24px blur) fades in under project/about overlays.",
                      "timing": {"duration": "{motion.duration.word}"},
                      "reducedMotionFallback": "instant-show", "sourceImplementsFallback": False,
                      "evidence": [cite(C272, "pointer-events-none fixed inset-0 z-[15] bg-[#0e0d0c]/97 backdrop-blur-[24px] opacity-0")]},
    "none": {"description": "No motion.", "timing": {}, "reducedMotionFallback": "none", "sourceImplementsFallback": True, "evidence": [cite(NFJSX, '<h1 className="sr-only">404</h1>')]},
}
FALLBACKS = sorted(set(p["reducedMotionFallback"] for p in MOTION_PATTERNS.values()))


# ---------------------------------------------------------------------------------------------
# 4. Asset roles (availability also pinned in verify_all.py and semantic_validate.py)
# ---------------------------------------------------------------------------------------------
def build_asset_roles():
    roles = {
        "person.portrait-source": {"availability": "blocked-for-generation", "generationPolicy": "must-not-reuse",
                                   "description": "Photographs of the site owner (a real person). Reference evidence only; never reproduced, altered or imitated in generated output.",
                                   "sourceExamples": ["/rk-portrait.jpg", "/rk-about.jpg"], "generationSafeSubstitutes": ["person.portrait-fictional", "media.placeholder"],
                                   "licensing": "A real person's likeness: no reuse, no look-alike generation.",
                                   "evidence": [cite(C272, '{ src: "/rk-portrait.jpg", discipline: null },'), cite(C924, 'src: "/rk-about.jpg",')]},
        "brand.wordmark-source": {"availability": "blocked-for-generation", "generationPolicy": "must-not-reuse",
                                  "description": "The owner's studio wordmark as set in the preloader. Never must-reuse-exact in generated mode.",
                                  "sourceExamples": ["preloader wordmark text"], "generationSafeSubstitutes": ["brand.wordmark-placeholder"],
                                  "licensing": "Personal brand identity of a real designer.", "evidence": [cite(C924, 'children: "KERIMOV DESIGNS",')]},
        "brand.favicon-source": {"availability": "blocked-for-generation", "generationPolicy": "must-not-reuse",
                                 "description": "Site favicon.", "sourceExamples": ["/favicon.ico"], "generationSafeSubstitutes": ["brand.wordmark-placeholder"],
                                 "licensing": "Personal brand identity.", "evidence": [cite("index.html", 'href="/favicon.ico" type="image/x-icon"')]},
        "project.cover-source": {"availability": "reference-only", "generationPolicy": "must-not-reuse",
                                 "description": "Cover image of a real portfolio project (gallery plane texture / mobile card).",
                                 "sourceExamples": ["/projects/<hash> (10 covers)"], "generationSafeSubstitutes": ["project.cover-generated", "media.placeholder"],
                                 "licensing": "Proprietary client and personal work of the designer.", "evidence": [cite(PROJ, '"src": "/projects/', nth=1)]},
        "project.gallery-source": {"availability": "reference-only", "generationPolicy": "must-not-reuse",
                                   "description": "Additional images of a real project shown in the media stage.",
                                   "sourceExamples": ["/projects/<hash> (53 gallery images)"], "generationSafeSubstitutes": ["project.gallery-generated", "media.placeholder"],
                                   "licensing": "Proprietary work.", "evidence": [cite(PROJ, '"images": [', nth=1)]},
        "project.video-source": {"availability": "reference-only", "generationPolicy": "must-not-reuse",
                                 "description": "Motion piece of a real project (looped, muted).",
                                 "sourceExamples": ["/projects/videos/<hash>.mp4 (8 files)"], "generationSafeSubstitutes": ["project.video-generated", "media.placeholder"],
                                 "licensing": "Proprietary work.", "evidence": [cite(PROJ, '"srcVideo": "/projects/videos/', nth=1)]},
        "discipline.media-source": {"availability": "reference-only", "generationPolicy": "must-not-reuse",
                                    "description": "Images/video illustrating each discipline on the About page (taken from the designer's own projects).",
                                    "sourceExamples": ["/visual-identity.jpg", "/logo-design.jpg", "/art-direction.jpg", "/editorial-design.jpg", "/bylarm-new.mp4"],
                                    "generationSafeSubstitutes": ["discipline.media-generated", "media.placeholder"], "licensing": "Proprietary work.",
                                    "evidence": [cite(C272, '{ src: "/bylarm-new.mp4", discipline: "Motion & Animation" },')]},
        "scene.procedural-digits": {"availability": "generation-safe", "generationPolicy": "may-generate-new",
                                    "description": "Digits drawn at runtime onto a canvas texture (404 scene). Procedural, no source imagery.",
                                    "sourceExamples": ["canvas texture, Arial 900"], "licensing": "Procedural.", "evidence": [cite(C404, 'let a = ["4", "0", "4"];')]},
        "brand.wordmark-placeholder": {"availability": "generation-safe", "generationPolicy": "may-generate-new",
                                       "description": "Placeholder, user-supplied or newly generated wordmark text for a fictional or client brand.",
                                       "licensing": "Must be original to the requesting party.", "evidence": [cite(C924, 'children: "KERIMOV DESIGNS",', note="the slot this role fills")]},
        "person.portrait-fictional": {"availability": "generation-safe", "generationPolicy": "may-generate-new",
                                      "description": "Portrait of a fictional person or one supplied by the page's real owner (user-supplied://).",
                                      "licensing": "Generated people must not resemble the source owner.", "evidence": [cite(C924, 'alt: "Portrait of Rustam Kerimov",', note="the slot this role fills")]},
        "project.cover-generated": {"availability": "generation-safe", "generationPolicy": "may-generate-new",
                                    "description": "Generated or user-supplied cover for a fictional/new project.", "licensing": "Original work only.", "evidence": [cite(C924, "src: e.src,", note="the slot this role fills")]},
        "project.gallery-generated": {"availability": "generation-safe", "generationPolicy": "may-generate-new",
                                      "description": "Generated or user-supplied gallery image.", "licensing": "Original work only.", "evidence": [cite(C924, 'alt: "".concat(m.title, " — work ").concat(t + 1),', note="the slot this role fills")]},
        "project.video-generated": {"availability": "generation-safe", "generationPolicy": "may-generate-new",
                                    "description": "Generated or user-supplied looping muted video.", "licensing": "Original work only.", "evidence": [cite(C924, 'children: (0, r.jsx)("source", { src: m.srcVideo }),', note="the slot this role fills")]},
        "discipline.media-generated": {"availability": "generation-safe", "generationPolicy": "may-generate-new",
                                       "description": "Generated or user-supplied media illustrating a discipline.", "licensing": "Original work only.", "evidence": [cite(C924, 'src: "/visual-identity.jpg",', note="the slot this role fills")]},
        "media.placeholder": {"availability": "generation-safe", "generationPolicy": "may-generate-new",
                              "description": "Neutral placeholder media (solid surface.media-placeholder fill) for any image/video slot.",
                              "licensing": "None needed.", "evidence": [cite(C924, "relative aspect-[4/3] w-full overflow-hidden bg-[#1e211b]")]},
        "link.placeholder-url": {"availability": "generation-safe", "generationPolicy": "may-generate-new",
                                 "description": "Placeholder links on reserved domains only (*.example, *.invalid, example.com/.net/.org) or site-relative paths.",
                                 "licensing": "Reserved for documentation (RFC 2606).", "evidence": [cite(CLAY, 'href: "https://www.instagram.com/kerimov.designs/",', note="the slot this role fills")]},
        "copy.original": {"availability": "generation-safe", "generationPolicy": "may-generate-new",
                          "description": "Newly written copy. Must not reuse source phrasing (checked by 5-word shingles).", "licensing": "Original.",
                          "evidence": [cite(C272, 'text: "CRAFTING VISUAL IDENTITIES,",', note="the slot this role fills")]},
        "rating.placeholder": {"availability": "generation-safe", "generationPolicy": "may-generate-new",
                               "description": "Placeholder rating. The source has no reviews, ratings or testimonials and the PageSpec schema has no rating field, so no section uses this role; it exists so a generator has a declared safe target.",
                               "licensing": "Fictional only.", "evidence": [cite(APP, "const isKnownRoute", note="route table: no review/testimonial page exists")]},
    }
    doc = {"version": VERSION,
           "availabilityEnum": ["reference-only", "generation-safe", "blocked-for-generation"],
           "generationPolicyEnum": ["may-generate-new", "must-reuse-exact", "must-not-fabricate", "must-not-reuse"],
           "srcSchemes": {"reference": "site-relative path into the source's public/ folder (evidence only)",
                          "generated": ["placeholder://", "generated://", "user-supplied://"]},
           "note": "The source is the live portfolio of a real designer: his photographs, studio wordmark and project media are blocked or reference-only. Availability is pinned in code (PINNED_AVAILABILITY in extraction/verify_all.py and schema/semantic_validate.py), so editing this registry alone cannot loosen it.",
           "roles": roles}
    wjson("assets/asset-roles.json", doc)
    return roles


# ---------------------------------------------------------------------------------------------
# 5. Primitives and components
# ---------------------------------------------------------------------------------------------
def build_primitives_components():
    prims = {
        "primitive.word-reveal-text": ("Text split into words, each in an overflow-clipped inline box so it can rise into place.", ["text", "stagger", "delay"],
                                        [cite_range(C272, "function k(e) {", "      function S(e) {")], ["word-reveal"]),
        "primitive.micro-label": ("Small uppercase label in the UI stack, wide tracking (scroll hint, tags, Year/Tools labels).", ["text"],
                                  [cite(C272, '"mb-3 font-sans text-[10px] font-medium  tracking-[0.18em] text-[#e7e3dd]",')], ["none"]),
        "primitive.text-link": ("Plain text link/button that drops to 50% opacity on hover (300ms).", ["label", "href"],
                                [cite(CLAY, '"whitespace-nowrap transition-opacity duration-300 hover:opacity-50",')], ["opacity-hover"]),
        "primitive.copy-button": ("Button that copies a contact string to the clipboard and swaps its label for idle / copied / failed states (resets after 2.2s).", ["label", "copiedLabel", "failedLabel"],
                                  [cite(C924, "await navigator.clipboard.writeText(", span=10)], ["opacity-hover"]),
        "primitive.media-plane": ("Textured WebGL plane (image or video texture) with hover, blur, bend and morph uniforms.", ["assetRole", "src"],
                                  [cite(C272, "uniform float uTime, uHover, uWorldScale, uEdgeBend")], ["gallery-strip-scroll", "hover-focus-blur"]),
        "primitive.image-frame": ("Image block with the media-placeholder surface behind it, no radius.", ["assetRole", "src", "alt", "aspectRatio"],
                                  [cite(C924, 'className: "block h-auto w-full bg-[#1e211b]",')], ["none"]),
        "primitive.video-frame": ("Muted, looping, inline, non-interactive video with black letterbox.", ["assetRole", "src", "label"],
                                  [cite(C924, "pointer-events-none block h-auto w-full bg-black")], ["none"]),
        "primitive.pagination-number": ("Numeric button, 30% opacity unless current; 300ms opacity transition; 1px focus outline.", ["index", "current"],
                                        [cite(C272, '"aria-label": "Show project media ".concat(t + 1),')], ["opacity-hover"]),
        "primitive.arrow-link": ("Heavy uppercase link with a drawn arrow whose head scales in on hover (0.5s reveal curve).", ["label", "href"],
                                 [cite(NFJSX, 'className="origin-[14px_12px] scale-0 transition-transform duration-500')], ["opacity-hover"]),
    }
    comps = {
        "component.label-value": ("A small label above a value (navbar columns, Year/Tools).", ["primitive.micro-label", "primitive.word-reveal-text"], ["label", "value"],
                                  [cite_range(C272, "function S(e) {", "      function N(e) {")]),
        "component.nav-column": ("One navbar column: label + value or a stack of links, entering with a staggered fade-up.", ["component.label-value", "primitive.text-link", "primitive.copy-button"], ["label", "value", "links"],
                                 [cite(CLAY, 'children: "occupation:",', span=4)]),
        "component.work-card": ("Mobile work card: 4:3 cover + uppercase title, whole card is a link.", ["primitive.image-frame"], ["title", "href", "cover"],
                                [cite(C924, 'ariaLabel: "View ".concat(e.title),', span=24)]),
        "component.discipline-menu": ("Vertical list of discipline buttons, right-aligned, inactive at 30% opacity, 500ms transition.", ["primitive.word-reveal-text"], ["items", "current"],
                                      [cite(C272, "children: D.map((e, t) =>", span=26)]),
        "component.media-pagination": ("Row of pagination numbers for the media stage.", ["primitive.pagination-number"], ["count", "current"],
                                       [cite(C272, '"aria-label": "Project media navigation",', span=40)]),
        "component.split-heading": ("Multi-line display heading built from word-reveal lines.", ["primitive.word-reveal-text"], ["lines"],
                                    [cite(C272, 'text: "GRAPHIC DESIGNER",', span=2)]),
    }
    out = {}
    for pid, (desc, props, ev, motion) in prims.items():
        d = {"id": pid, "kind": "primitive", "version": VERSION, "description": desc, "props": props, "motionPatterns": motion, "evidence": ev}
        wjson(f"primitives/{pid}.json", d)
        out[pid] = d
    for cid, (desc, uses, props, ev) in comps.items():
        d = {"id": cid, "kind": "component", "version": VERSION, "description": desc, "composes": uses, "props": props, "evidence": ev}
        wjson(f"components/{cid}.json", d)
        out[cid] = d
    return out


# ---------------------------------------------------------------------------------------------
# 6. Sections
# ---------------------------------------------------------------------------------------------
def project_media(p):
    seen = []
    for s in [p["src"]] + p.get("images", []):
        if s and s.strip() and s not in seen:
            seen.append(s)
    vid = 1 if (p.get("srcVideo") or "").strip() else 0
    return seen, vid


def compute_budgets():
    b = {}
    b["project.title"] = max(words(p["title"]) for p in PROJECTS)
    b["project.description"] = max(words(p["description"]) for p in PROJECTS)
    b["project.tools"] = max(words(p["tools"]) for p in PROJECTS)
    b["project.tag"] = max(words(t.replace("-", " ")) for p in PROJECTS for t in p["tags"])
    b["project.tags"] = max(len(p["tags"]) for p in PROJECTS)
    b["project.media"] = max(len(project_media(p)[0]) + project_media(p)[1] for p in PROJECTS)
    b["about.title"] = max(words(i["title"]) for i in ABOUT_ITEMS)
    b["about.intro"] = max(words(i["intro"]) for i in ABOUT_ITEMS)
    b["about.description"] = max(words(i["description"]) for i in ABOUT_ITEMS)
    b["about.mobile"] = max(words(i["mobile"]) for i in ABOUT_ITEMS)
    b["about.label"] = max(words(i["label"]) for i in ABOUT_ITEMS)
    b["about.items"] = len(ABOUT_ITEMS)
    b["hero.line"] = max(words(l) for l in HERO_LINES)
    b["intro.note"] = words(INTRO_NOTE)
    b["notfound.heading"] = words(NOTFOUND_HEADING)
    b["notfound.body"] = words(NOTFOUND_BODY)
    b["mobile.service.description"] = max(words(s["description"]) for s in MOBILE_SERVICES) if MOBILE_SERVICES else 0
    return b


def build_sections(measure, budgets):
    m1440 = measure["viewports"]["1440x900"]
    m390 = measure["viewports"]["390x844"]

    def heights(template, sid):
        out = {}
        for vp, mm in (("1440x900", m1440), ("390x844", m390)):
            s = mm.get(template, {}).get("sections", {}).get(sid)
            if s and s.get("present"):
                out[vp] = {"heightPx": s["height"], "widthPx": s["width"], "inFlow": s["inFlow"], "position": s["position"]}
            else:
                out[vp] = {"present": False}
        return out

    MW = budget
    S = []

    def sec(sid, title, category, purpose, source, content, motion, responsive, retrieval=True, reason=None, constraints=None,
            gen_roles=None, ref_roles=None, tokens=None, measured=None, evidence=None, components=None, notes=None):
        d = {"id": sid, "version": VERSION, "title": title,
             "source": source, "semantic": {"id": sid, "category": category, "purpose": purpose},
             "retrievalEligible": retrieval}
        if not retrieval:
            d["retrievalIneligibleReason"] = reason
        d.update({"content": content, "constraints": constraints or {}, "responsive": responsive,
                  "motion": motion, "generatedAssetRoles": gen_roles or [], "referenceAssetRoles": ref_roles or [],
                  "tokens": tokens or [], "composes": components or [], "evidence": evidence or [], "measured": measured or {}})
        if notes:
            d["notes"] = notes
        S.append(d)

    def mot(patterns, default=None):
        default = default or patterns[0]
        return {"patterns": patterns, "default": default, "reducedMotionFallback": MOTION_PATTERNS[default]["reducedMotionFallback"],
                "sourceImplementsFallback": MOTION_PATTERNS[default]["sourceImplementsFallback"]}

    def src(sid, rel, start, end=None, span=0):
        c = cite_range(rel, start, end) if end else cite(rel, start, span=span)
        c = {"id": sid, **c}
        return c

    link_fields = {"label": {"type": "text", "maxWords": 2}, "href": {"type": "link"}, "kind": {"type": "enum", "values": ["copy-email", "social", "external", "internal"]}}

    sec("shell.navbar", "Site navbar", "SHELL", "Fixed identity bar: owner name, occupation, location, contact links and the profile toggle.",
        src("module-5883:navbar", CLAY, '"aria-label": "Main navigation",', "    6411: (n, e, t) => {"),
        {"fields": {"ownerName": {"type": "text", "maxWords": 3, "required": True}, "occupation": {"type": "text", "maxWords": 3, "required": True},
                    "location": {"type": "text", "maxWords": 3, "required": True}, "contactLinks": {"type": "list", "of": link_fields, "maxItems": 3},
                    "profileLinkLabel": {"type": "text", "maxWords": 2, "required": True}}},
        mot(["staggered-fade-up", "opacity-hover"]),
        {"desktop": "Fixed, transparent, 5 columns (Name:/occupation:/Location:/Connect:/Profile:) justified across the width, side gutter 3.1%, top 18px; labels 14px, values clamp(15px,1.1vw,20px) medium.",
         "mobile": "Below 1024px only the name (left) and an 'About me' / 'Back' toggle (right) remain; gutter 5%, top 24px.",
         "breakpoint": "{breakpoint.lg}"},
        constraints={"onePerPage": True, "mustBeFirst": True},
        gen_roles=["link.placeholder-url", "copy.original"],
        tokens=["text.primary", "component.navbar.label-size", "component.navbar.value-size", "typography.family.display", "motion.easing.reveal"],
        measured=heights("home", "shell.navbar"), components=["component.nav-column", "primitive.copy-button", "primitive.text-link"],
        evidence=[cite(CLAY, "fixed inset-x-0 top-0 z-[100] w-full bg-transparent px-[5%] pb-4 pt-6")])

    sec("hero.intro", "Home opener", "HERO", "Page-opening statement of who the designer is, with the portrait thumbnail that opens the profile.",
        src("module-5272:fn-ei", C272, "function ei(e) {", "      let el = [0.16, 1, 0.3, 1],"),
        {"fields": {"headingLines": {"type": "list", "of": {"type": "text", "maxWords": budgets["hero.line"] + 1}, "minItems": 1, "maxItems": 3, "required": True},
                    "portrait": {"type": "asset", "required": True, "aspectRatio": "4:5"},
                    "profileHref": {"type": "link", "required": True}}},
        mot(["word-reveal"]),
        {"desktop": "Heading at left 3.1%, top 32%, width 70%, one line per row (no wrap), clamp(25px,2.15vw,38px) bold, leading 1.1; portrait thumbnail at right 3.1%, top 150px, width clamp(150px,12vw,210px), 4:5; both overlay the gallery.",
         "mobile": "In-flow block: heading clamp(28px,7.3vw,46px) bold uppercase leading 1.04, portrait below right-aligned at 48% width (max 240px) linking to /about.",
         "breakpoint": "{breakpoint.lg}"},
        constraints={"onePerPage": True, "homeOnly": True},
        gen_roles=["person.portrait-fictional", "media.placeholder", "copy.original"], ref_roles=["person.portrait-source"],
        tokens=["typography.size.hero-display", "typography.weight.bold", "typography.lineHeight.display-110", "typography.tracking.display-tight", "text.primary"],
        measured=heights("home", "hero.intro"), components=["component.split-heading"],
        evidence=[cite(C924, 'text: "Graphic Designer\\nCrafting Visual Identities,\\nTypography and Motion.",'), cite(C272, '"aria-label": "Open Rustam Kerimov profile",')])

    sec("content.intro-note", "Intro note", "CONTENT", "Short first-person invitation to browse the work and get in touch.",
        src("module-5272:fn-es", C272, "function es(e) {", "      let ec = (e) =>"),
        {"fields": {"text": {"type": "text", "maxWords": MW(budgets["intro.note"]), "required": True}}},
        mot(["word-reveal"]),
        {"desktop": "Paragraph anchored to the portrait column (bottom calc(21svh + 32px), shifted 55% left), width clamp(360px,29vw,500px), 17px, leading 1.45. Hidden when the viewport is >=1024px wide and <=680px tall.",
         "mobile": "Not rendered in the mobile list layout.", "breakpoint": "{breakpoint.lg}"},
        constraints={"onePerPage": True, "homeOnly": True},
        gen_roles=["copy.original"], tokens=["typography.size.intro-note", "typography.lineHeight.body-145", "text.primary"],
        measured=heights("home", "content.intro-note"), components=["primitive.word-reveal-text"],
        evidence=[cite(C272, "lg:top-auto lg:bottom-[calc(21svh+32px)]")])

    sec("portfolio.work-index", "Work index", "PORTFOLIO", "Index of all projects; each item opens that project's detail.",
        src("module-5272:fn-f-gallery", C272, "function f(e) {", "      function x() {"),
        {"fields": {"heading": {"type": "text", "maxWords": 3},
                    "items": {"type": "list", "minItems": 1, "maxItems": 12, "required": True,
                              "of": {"title": {"type": "text", "maxWords": budgets["project.title"] + 1}, "href": {"type": "link"}, "cover": {"type": "asset"}}}}},
        mot(["gallery-strip-scroll", "hover-focus-blur"]),
        {"desktop": "Full-viewport WebGL strip behind everything: one textured plane per project, heights cycled [0.14,0.18,0.13,0.16,0.15,0.19] x viewport height, gap 1.2vw, repeated infinitely, wheel-driven; hover focuses one plane and shows its title next to the cursor.",
         "mobile": "In-flow 'Selected Work:' section: 2-column grid, 12px/32px gaps, 4:3 cover + 12px uppercase title per card.",
         "breakpoint": "{breakpoint.lg}"},
        constraints={"onePerPage": True},
        gen_roles=["project.cover-generated", "media.placeholder", "copy.original"], ref_roles=["project.cover-source"],
        tokens=["layout.gallery.plane-heights", "layout.gallery.plane-gap", "layout.grid.mobile-work", "typography.size.mobile-card-title"],
        measured=heights("home", "portfolio.work-index"), components=["primitive.media-plane", "component.work-card"],
        evidence=[cite(C272, "let h = [0.14, 0.18, 0.13, 0.16, 0.15, 0.19],"), cite(C924, 'children: "Selected Work:",')],
        notes="Desktop height equals the viewport because the strip is a full-viewport canvas layer; the planes themselves are 13-19% of viewport height.")

    sec("shell.footer-contact", "Contact footer (mobile)", "SHELL", "Closing contact block: services list, contact links and the design/development credit.",
        src("module-4656:fn-h-footer", C924, "      function h() {", "      function g(e) {"),
        {"fields": {"servicesHeading": {"type": "text", "maxWords": 2}, "services": {"type": "list", "of": {"type": "text", "maxWords": 3}, "maxItems": 6},
                    "connectHeading": {"type": "text", "maxWords": 2}, "contactLinks": {"type": "list", "of": link_fields, "maxItems": 3},
                    "creditLabel": {"type": "text", "maxWords": 3}, "credit": {"type": "object", "of": {"label": {"type": "text", "maxWords": 3}, "href": {"type": "link"}}}}},
        mot(["opacity-hover"]),
        {"desktop": "Not rendered at >=1024px (the navbar carries the contact links).", "mobile": "In-flow footer after the page content: 2-column grid (services | connect), 15px medium, credit line below.", "breakpoint": "{breakpoint.lg}"},
        constraints={"onePerPage": True, "mustBeLast": True},
        gen_roles=["link.placeholder-url", "copy.original"], tokens=["typography.size.mobile-footer", "text.overlay"],
        measured=heights("home", "shell.footer-contact"), components=["primitive.copy-button", "primitive.text-link"],
        evidence=[cite(C924, 'children: "Design / Development:",')])

    sec("project.header", "Project header", "PROJECT_DETAIL", "Project title and its descriptive text.",
        src("module-5272:fn-N-header", C272, '"absolute left-[5%] top-[7%] z-30 w-[88%] md:left-[3.5%] md:top-[27%] md:w-[20.5%]",', span=40),
        {"fields": {"title": {"type": "text", "maxWords": budgets["project.title"] + 1, "required": True},
                    "description": {"type": "text", "maxWords": MW(budgets["project.description"], 10), "required": True},
                    "tags": {"type": "list", "of": {"type": "text", "maxWords": budgets["project.tag"]}, "maxItems": budgets["project.tags"] + 1}}},
        mot(["word-reveal"]),
        {"desktop": "Left text column (left 3.5%, top 27%, width 20.5%): title clamp(22px,1.45vw,27px) bold uppercase, description clamp(15px,1.05vw,18px) leading 1.55 at 78% (smaller under 800/650px tall viewports).",
         "mobile": "In-flow article header: title clamp(31px,8vw,54px) bold uppercase, tags joined with ' / ' below in 10px UI-stack caps.",
         "breakpoint": "{breakpoint.lg}"},
        constraints={"onePerPage": True},
        gen_roles=["copy.original"], tokens=["typography.size.project-title", "typography.size.body-overlay", "text.overlay", "text.overlay-muted"],
        measured=heights("project-detail", "project.header"), components=["primitive.word-reveal-text"],
        evidence=[cite(C924, 'children: f.join(" / "),')])

    sec("project.media-stage", "Project media stage", "MEDIA", "The project's images and video, viewed one at a time (desktop) or stacked (mobile).",
        src("module-5272:gallery-vertex-shader-morph", C272, "uTransitionBend, uMorph"),
        {"fields": {"media": {"type": "list", "minItems": 1, "maxItems": budgets["project.media"] + 2, "required": True,
                              "of": {"asset": {"type": "asset"}, "kind": {"type": "enum", "values": ["image", "video"]}}}}},
        mot(["plane-focus-stage"]),
        {"desktop": "The clicked gallery plane morphs into a centred stage over the backdrop; wheel/click advances media, pagination jumps; cursor shows NEXT/RETURN.",
         "mobile": "In-flow stack of full-width images (12px apart, placeholder surface) followed by the looping muted video.",
         "breakpoint": "{breakpoint.lg}"},
        constraints={"onePerPage": True},
        gen_roles=["project.cover-generated", "project.gallery-generated", "project.video-generated", "media.placeholder"],
        ref_roles=["project.cover-source", "project.gallery-source", "project.video-source"],
        tokens=["surface.media-placeholder", "surface.backdrop"], measured=heights("project-detail", "project.media-stage"),
        components=["primitive.media-plane", "primitive.image-frame", "primitive.video-frame"],
        evidence=[cite(C924, 'className: "space-y-3",'), cite(C924, 'alt: "".concat(m.title, " — work ").concat(t + 1),')])

    sec("project.meta", "Project facts", "PROJECT_DETAIL", "Year and tools of the project (mobile also repeats the description here).",
        src("module-5272:fn-N-meta", C272, '"absolute bottom-[26%] right-[3.8%] hidden w-[18.5%] flex-col items-start gap-6 md:flex",', span=24),
        {"fields": {"yearLabel": {"type": "text", "maxWords": 1}, "year": {"type": "year", "required": True},
                    "toolsLabel": {"type": "text", "maxWords": 1}, "tools": {"type": "text", "maxWords": budgets["project.tools"] + 2, "required": True}}},
        mot(["word-reveal"]),
        {"desktop": "Right column (right 3.8%, bottom 26%, width 18.5%): 10px UI-stack labels with 0.18em tracking above clamp(16px,1.1vw,19px) medium values at 90%.",
         "mobile": "Grid below the media after a 20%-opacity hairline: 'About the project:' description spanning both columns, then Year and Tools.",
         "breakpoint": "{breakpoint.md}"},
        constraints={"onePerPage": True},
        gen_roles=["copy.original"], tokens=["typography.size.micro", "typography.size.menu-item", "typography.tracking.label-wider", "border.hairline"],
        measured=heights("project-detail", "project.meta"), components=["component.label-value"],
        evidence=[cite(C924, 'children: "About the project:",')])

    sec("project.footer-bar", "Project footer bar", "NAVIGATION", "Bottom bar of the detail view: interaction hint, tags, and media pagination.",
        src("module-5272:fn-N-footer", C272, '"absolute bottom-[3.5%] left-[5%] right-[5%] grid', span=60),
        {"fields": {"hint": {"type": "text", "maxWords": 5, "required": True},
                    "tags": {"type": "list", "of": {"type": "text", "maxWords": budgets["project.tag"]}, "maxItems": budgets["project.tags"] + 1},
                    "mediaCount": {"type": "integer", "min": 1, "max": budgets["project.media"] + 2, "required": True}}},
        mot(["opacity-hover"]),
        {"desktop": "3 equal columns at bottom 5%: hint (10px caps, 80%), tags joined ' / ' centred (truncated), numbered media buttons right-aligned (30% -> 100%).",
         "mobile": "Not rendered in the mobile article layout (tags move into the header; media is stacked, so no pagination).", "breakpoint": "{breakpoint.lg}"},
        constraints={"onePerPage": True},
        gen_roles=["copy.original"], tokens=["typography.size.micro", "typography.size.pagination", "typography.tracking.label-wide", "component.overlay.pagination-inactive-opacity"],
        measured=heights("project-detail", "project.footer-bar"), components=["component.media-pagination", "primitive.micro-label"],
        evidence=[cite(C272, 'children: "Scroll or click to explore",', nth=1)])

    sec("about.profile-header", "Profile header", "PROFILE", "Who the designer is (Profile entry) or what the selected discipline is: title, intro and description.",
        src("module-5272:fn-V-header", C272, '"absolute left-[5%] top-[10%] w-[90%] lg:left-[3.5%] lg:top-[27%] lg:w-[21%]",', span=50),
        {"fields": {"title": {"type": "text", "maxWords": budgets["about.title"] + 1, "required": True},
                    "intro": {"type": "text", "maxWords": MW(budgets["about.intro"]), "required": True},
                    "description": {"type": "text", "maxWords": MW(budgets["about.description"]), "required": True}}},
        mot(["word-reveal", "content-crossfade"]),
        {"desktop": "Left column (left 3.5%, top 27%, width 21%): title clamp(20px,1.7vw,32px) bold uppercase (smaller when >15 chars), intro + description clamp(15px,1.08vw,19px) at 80%.",
         "mobile": "Full-bleed portrait 75svh (min 430px, max 820px) with a 2-line display title overlapping its bottom edge, then the bio paragraphs and a location line.",
         "breakpoint": "{breakpoint.lg}"},
        constraints={"onePerPage": True},
        gen_roles=["person.portrait-fictional", "media.placeholder", "copy.original"], ref_roles=["person.portrait-source"],
        tokens=["typography.size.about-title", "typography.size.body-about", "text.overlay", "text.overlay-muted"],
        measured=heights("about", "about.profile-header"), components=["primitive.word-reveal-text"],
        evidence=[cite(C924, 'text: "Behind\\nThe Work.",')])

    sec("about.media-stage", "Profile media stage", "MEDIA", "Large media for the profile and each discipline, switched by the discipline list or by clicking.",
        src("module-5272:fn-B-about-scene", C272, "      function B(e) {", span=40),
        {"fields": {"media": {"type": "list", "minItems": 1, "maxItems": budgets["about.items"] + 2, "required": True,
                              "of": {"asset": {"type": "asset"}, "kind": {"type": "enum", "values": ["image", "video"]}}}}},
        mot(["plane-focus-stage"]),
        {"desktop": "WebGL stage over the backdrop; the portrait thumbnail morphs into it on open; clicking over the image advances, elsewhere closes.",
         "mobile": "No separate stage: each discipline's media sits inside the discipline list.", "breakpoint": "{breakpoint.lg}"},
        constraints={"onePerPage": True},
        gen_roles=["person.portrait-fictional", "discipline.media-generated", "media.placeholder"], ref_roles=["person.portrait-source", "discipline.media-source"],
        tokens=["surface.backdrop"], measured=heights("about", "about.media-stage"), components=["primitive.media-plane"],
        evidence=[cite(C272, '{ src: "/rk-portrait.jpg", discipline: null },', span=6)])

    sec("about.discipline-list", "Discipline list", "PROFILE", "The designer's disciplines/services; selecting one swaps header and media.",
        src("module-5272:fn-V-menu", C272, '"pointer-events-auto absolute bottom-[5%] right-[3.1%] hidden w-[22%] text-right lg:block",', span=30),
        {"fields": {"items": {"type": "list", "minItems": 2, "maxItems": budgets["about.items"] + 2, "required": True,
                              "of": {"label": {"type": "text", "maxWords": budgets["about.label"] + 1},
                                     "summary": {"type": "text", "maxWords": MW(max(budgets["about.mobile"], budgets["mobile.service.description"]))},
                                     "media": {"type": "asset"}}}}},
        mot(["opacity-hover"]),
        {"desktop": "Right-aligned menu at bottom 5%, right 3.1%: clamp(16px,1.1vw,19px) medium, inactive items at 30%.",
         "mobile": "'Services:' heading, then one block per discipline (title, media, description) 80px apart.", "breakpoint": "{breakpoint.lg}"},
        constraints={"onePerPage": True},
        gen_roles=["discipline.media-generated", "person.portrait-fictional", "media.placeholder", "copy.original"], ref_roles=["discipline.media-source", "person.portrait-source"],
        tokens=["typography.size.menu-item", "text.overlay"], measured=heights("about", "about.discipline-list"), components=["component.discipline-menu"],
        evidence=[cite(C924, 'className: "space-y-20",')],
        notes="On mobile this list holds 64.5% of the measured 390px page (6 stacked discipline blocks). The wrapper gate is pinned to 1440px, where the list is an absolutely positioned menu; the mobile share is recorded as information in extraction/measured-values.json.")

    sec("about.footer-meta", "Profile footer meta", "PROFILE", "Interaction hint plus short personal facts (location, age).",
        src("module-5272:fn-V-footer", C272, '"absolute bottom-[4%] left-[5%] right-[5%] grid grid-cols-2 items-end gap-2', span=50),
        {"fields": {"hint": {"type": "text", "maxWords": 5, "required": True}, "facts": {"type": "list", "of": {"type": "text", "maxWords": 3}, "maxItems": 3}}},
        mot(["word-reveal"]),
        {"desktop": "Bottom-left row (left 5.3%, bottom 5%): hint and facts in 10px UI-stack caps at 80%, facts separated by a 40% slash.",
         "mobile": "Facts become one line under the mobile bio (11px caps).", "breakpoint": "{breakpoint.lg}"},
        constraints={"onePerPage": True},
        gen_roles=["copy.original"], tokens=["typography.size.micro", "typography.tracking.label-wide"], measured=heights("about", "about.footer-meta"),
        components=["primitive.micro-label"], evidence=[cite(C924, 'mt-12 font-sans text-[11px] uppercase tracking-[0.1em]')])

    sec("notfound.digits-scene", "404 digits scene", "MEDIA", "Decorative full-viewport scene of floating status-code digits.",
        src("module-9812:floating-digits", C404, "    9812: (e, t, n) => {", span=40),
        {"fields": {"digits": {"type": "digits", "required": True}}},
        mot(["floating-digits"]),
        {"desktop": "Full-viewport canvas behind the message.", "mobile": "Same, scaled to the viewport.", "breakpoint": None},
        constraints={"onePerPage": True},
        gen_roles=["scene.procedural-digits"], tokens=["typography.family.digits", "motion.duration.digits-loop"],
        measured=heights("not-found", "notfound.digits-scene"), evidence=[cite(NFJSX, "<FloatingDigits />")])

    sec("notfound.message", "404 message", "NOTICE", "Tells the visitor the page does not exist and links back to the portfolio.",
        src("component-NotFound:message", NFJSX, '<section className=" absolute left-10 bottom-6 z-10 max-w-3xl text-left">', span=31),
        {"fields": {"heading": {"type": "text", "maxWords": budgets["notfound.heading"] + 2, "required": True},
                    "body": {"type": "text", "maxWords": MW(budgets["notfound.body"]), "required": True},
                    "backLinkLabel": {"type": "text", "maxWords": 4, "required": True}, "backHref": {"type": "link", "required": True}}},
        mot(["opacity-hover"]),
        {"desktop": "Bottom-left block (left 40px, bottom 24px, max 48rem): 48px semibold heading, 20px body at 60% white, heavy uppercase arrow link.",
         "mobile": "Same block; heading 30px, body 18px.", "breakpoint": "{breakpoint.md}"},
        constraints={"onePerPage": True, "mustBeLast": True},
        gen_roles=["copy.original"], tokens=["typography.size.notfound-heading", "typography.size.notfound-body", "typography.weight.black"],
        measured=heights("not-found", "notfound.message"), components=["primitive.arrow-link"],
        evidence=[cite(APP, "const isKnownRoute")])

    # runtime / utility UI: never retrievable
    U = "Runtime UI that exists only during interaction or loading; it carries no page content and must never be retrieved as a section to compose."
    sec("utility.preloader", "Preloader", "UTILITY", "Load-progress cover with the wordmark reveal.",
        src("module-4760:preloader", C924, "    4760: (e, t, n) => {", "    5744: (e, t, n) => {"),
        {"fields": {}}, mot(["preloader-wipe"]),
        {"desktop": "Fixed full-screen cover until WebGL textures are ready, then slides up.", "mobile": "Shown once with threeReady=true (no textures to wait for).", "breakpoint": None},
        retrieval=False, reason="Loading cover shown only until assets are ready; " + U,
        ref_roles=["brand.wordmark-source"], gen_roles=["brand.wordmark-placeholder"], tokens=["surface.page", "typography.size.preloader-wordmark", "motion.easing.preloader-exit"],
        measured={"note": "Transient: removed before measurement settles; full viewport while visible."}, evidence=[cite(C924, 'className: "fixed inset-0 z-[9999] bg-[#0b0c09]",')])
    sec("utility.kinetic-cursor", "Kinetic cursor", "UTILITY", "Pointer-following label (RETURN / NEXT) inside open overlays.",
        src("module-5272:fn-I-cursor", C272, "      function I(e) {", "      let R = d"),
        {"fields": {}}, mot(["kinetic-cursor"]),
        {"desktop": "Only with hover-capable fine pointers; replaces the system cursor over overlays.", "mobile": "Not rendered.", "breakpoint": None},
        retrieval=False, reason="Interaction affordance that follows the pointer; " + U, tokens=["component.cursor.label-size", "component.cursor.press-scale"],
        measured=heights("about", "utility.kinetic-cursor"), evidence=[cite(C272, 'useState)("RETURN")')])
    sec("utility.page-transition", "Page transition", "UTILITY", "Full-screen WebGL wipe between routes.",
        src("module-7689:transition-canvas", CLAY, "    7689: (n, e, t) => {", span=30),
        {"fields": {}}, mot(["page-transition-wipe"]),
        {"desktop": "Covers the viewport during route changes.", "mobile": "Same.", "breakpoint": None},
        retrieval=False, reason="Route-change overlay visible for under a second; " + U, tokens=["color.gl.transition-a", "color.gl.transition-b"],
        measured={"note": "Transient overlay (fixed, full viewport) during navigation only."}, evidence=[cite(CLAY, '" pointer-events-none fixed inset-0 z-[99999] overflow-hidden ",')])
    sec("utility.overlay-backdrop", "Overlay backdrop", "UTILITY", "Blurred dark layer behind project/about overlays.",
        src("module-5272:fn-g-backdrop", C272, "      function g(e) {", "      function w(e) {"),
        {"fields": {}}, mot(["backdrop-fade"]),
        {"desktop": "Fixed full viewport, opacity driven by the scene.", "mobile": "Not rendered (no overlays on mobile).", "breakpoint": None},
        retrieval=False, reason="Decorative layer whose opacity is animated by the scene; " + U, tokens=["surface.backdrop", "effect.backdrop-blur"],
        measured=heights("project-detail", "utility.overlay-backdrop"), evidence=[cite(C272, "bg-[#0e0d0c]/97 backdrop-blur-[24px] opacity-0")])
    sec("utility.hover-title", "Hover title follower", "UTILITY", "Project title that follows the hovered gallery plane.",
        src("module-5272:fn-w-title", C272, "      function w(e) {", "      var y = n(6799),"),
        {"fields": {}}, mot(["hover-focus-blur"]),
        {"desktop": "Absolutely positioned per frame from the plane's projected corner; 11-16px.", "mobile": "Not rendered.", "breakpoint": None},
        retrieval=False, reason="Hover-only label duplicating the project title; " + U, tokens=["typography.size.hover-title", "text.inverse-blend"],
        measured={"note": "Hidden (opacity 0) until a plane is hovered; no box at rest."}, evidence=[cite(C272, "function v(e, t, n, r, i) {")])
    sec("utility.toast", "Toast", "UTILITY", "Confirmation toast host (copy-email feedback).",
        src("app:toaster", APP, '<Toaster position="top-center" toastOptions={toastOptions} />'),
        {"fields": {}}, mot(["none"]),
        {"desktop": "Top-centre fixed host.", "mobile": "Same.", "breakpoint": None},
        retrieval=False, reason="Success/error feedback that appears for a moment after copying; " + U, tokens=["surface.toast", "text.on-toast"],
        measured={"note": "Fixed host with no content at rest."}, evidence=[cite(APP, "const toastOptions = {")])

    for d in S:
        wjson(f"sections/{d['id']}.json", d)
    return S


# ---------------------------------------------------------------------------------------------
# 7. Templates, routes
# ---------------------------------------------------------------------------------------------
RUNTIME = ["utility.preloader", "utility.page-transition", "utility.toast"]


def build_templates():
    t = {
        "home": {"family": "home", "routePattern": "^/$", "homeRouteOnly": True,
                 "description": "Landing view: identity opener plus the full work index.",
                 "nodes": [{"section": "shell.navbar", "required": True, "repeatable": False},
                           {"section": "hero.intro", "required": True, "repeatable": False},
                           {"section": "content.intro-note", "required": False, "repeatable": False},
                           {"section": "portfolio.work-index", "required": True, "repeatable": False},
                           {"section": "shell.footer-contact", "required": False, "repeatable": False}],
                 "runtimeLayers": RUNTIME + ["utility.overlay-backdrop", "utility.hover-title"],
                 "composition": "Desktop (>=1024px): one 100svh stage with no document scroll; every section is a layer over the WebGL work strip. Mobile: in-flow list (opener, selected work grid, contact footer).",
                 "evidence": [cite(C272, "            (0, r.jsx)(ei, { visible: J && !ek && !eL && !P }),"), cite(C924, "(0, r.jsx)(b, { projects: n, navigate: c }),")]},
        "about": {"family": "profile", "routePattern": "^/about$", "homeRouteOnly": False,
                  "description": "The designer's profile and disciplines.",
                  "nodes": [{"section": "shell.navbar", "required": True, "repeatable": False},
                            {"section": "about.profile-header", "required": True, "repeatable": False},
                            {"section": "about.media-stage", "required": True, "repeatable": False},
                            {"section": "about.discipline-list", "required": True, "repeatable": False},
                            {"section": "about.footer-meta", "required": False, "repeatable": False},
                            {"section": "shell.footer-contact", "required": False, "repeatable": False}],
                  "runtimeLayers": RUNTIME + ["utility.overlay-backdrop", "utility.kinetic-cursor"],
                  "composition": "Desktop: an overlay opened over the home stage (the work strip stays underneath, blurred by the backdrop); /about loaded directly opens it after the preloader. Mobile: its own scrolling article.",
                  "underlay": "home",
                  "evidence": [cite(C272, "(0, r.jsx)(V, {", nth=1), cite(C924, "u = \"/about\" === i,")]},
        "project-detail": {"family": "content-detail", "routePattern": "^/project/[^/]+$", "homeRouteOnly": False,
                           "description": "One project: header, media, facts and the media pagination bar.",
                           "nodes": [{"section": "shell.navbar", "required": True, "repeatable": False},
                                     {"section": "project.header", "required": True, "repeatable": False},
                                     {"section": "project.media-stage", "required": True, "repeatable": False},
                                     {"section": "project.meta", "required": True, "repeatable": False},
                                     {"section": "project.footer-bar", "required": False, "repeatable": False},
                                     {"section": "shell.footer-contact", "required": False, "repeatable": False}],
                           "runtimeLayers": RUNTIME + ["utility.overlay-backdrop", "utility.kinetic-cursor"],
                           "composition": "Desktop: overlay over the home stage, the clicked plane becomes the media stage. Mobile: scrolling article (header, stacked media, facts, footer).",
                           "underlay": "home",
                           "stateVariants": {"unknownId": "An id not in the project list renders a 'not found' notice with a link back to the index (mobile layout); the route itself still answers 200 on the live site."},
                           "evidence": [cite(C272, "function ed(e) {", span=3), cite(C924, 'children: "Project not found",')]},
        "not-found": {"family": "utility-page", "routePattern": "*", "homeRouteOnly": False,
                      "description": "Fallback for every unknown path.",
                      "nodes": [{"section": "shell.navbar", "required": True, "repeatable": False},
                                {"section": "notfound.digits-scene", "required": True, "repeatable": False},
                                {"section": "notfound.message", "required": True, "repeatable": False}],
                      "runtimeLayers": ["utility.page-transition", "utility.toast"],
                      "composition": "Full-viewport digits scene with the message anchored bottom-left; same at every width.",
                      "evidence": [cite(APP, ") : (", span=2), cite(NFJSX, "export default function NotFound() {")]},
    }
    doc = {"version": VERSION, "note": "One template per page shape. Desktop and mobile are responsive variants of the same templates (the clone switches layout at 1024px), not separate templates. Node order is the reading order; on desktop the sections are layers of one viewport.", "templates": t}
    wjson("templates/templates.json", doc)
    routes = [{"route": "/", "template": "home", "evidence": cite(APP, "path === '/'")},
              {"route": "/about", "template": "about", "evidence": cite(APP, "path === '/about'")}]
    for p in PROJECTS:
        routes.append({"route": f"/project/{p['id']}", "template": "project-detail", "evidence": cite(PROJ, f'"id": "{p["id"]}"')})
    routes.append({"route": "*", "template": "not-found", "evidence": cite(APP, ") : (", note="every path other than /, /about, /project/:id renders NotFound (live site answers 404)")})
    wjson("templates/routes.json", {"version": VERSION, "note": "Every route the clone serves, each mapped exactly once. '*' is the fallback for unknown paths.", "routes": routes})
    return t, routes


# ---------------------------------------------------------------------------------------------
# 8. Compatibility graph (rule ids/severities must equal RULES in schema/semantic_validate.py)
# ---------------------------------------------------------------------------------------------
GRAPH_RULES = [
    ("TEMPLATE_NODE_SEQUENCE", "error", "A PageSpec's nodes must be exactly its declared template's node list in order: every required node present, optional nodes only where the template lists them, no others."),
    ("ROUTE_TEMPLATE_MATCH", "error", "The route must match the template's routePattern; the home template only on '/'."),
    ("NAVBAR_FIRST", "error", "shell.navbar is the first node on every template."),
    ("FOOTER_LAST", "error", "shell.footer-contact, when present, is the last node."),
    ("ONE_HERO", "error", "At most one HERO node. Exceptions: about, project-detail and not-found have no HERO at all (none required)."),
    ("HERO_HOME_ONLY", "error", "hero.intro and content.intro-note appear only on the home template."),
    ("NO_ADJACENT_DUPLICATE", "error", "The same section id never appears twice in a row (no template repeats a section)."),
    ("UTILITY_NOT_A_NODE", "error", "Sections with retrievalEligible=false (runtime UI) are never nodes; they may only be listed in runtimeLayers allowed by the template."),
    ("RUNTIME_LAYER_ALLOWED", "error", "Every runtimeLayers entry must be allowed by the template."),
    ("MOTION_PATTERN_ALLOWED", "error", "A node's motion.pattern must be one of its section contract's patterns."),
    ("MOTION_FALLBACK_PINNED", "error", "motion.reducedMotionFallback must equal the pinned fallback of the chosen pattern."),
    ("MOTION_BUDGET_WEBGL", "warn", "At most one WebGL scene pattern (gallery-strip-scroll, plane-focus-stage, floating-digits) per page; more is allowed but warned."),
    ("MAX_WORDS", "error", "Every text field respects its section contract's maxWords budget."),
    ("ASSET_ROLE_ALLOWED", "error", "An asset's role must be a generatedAssetRoles entry of its section in generated mode, or a reference/generated role of the section in reference mode."),
    ("TOKEN_POLICY", "error", "Node token references must exist in the catalog, fit their slot, resolve in the page theme and never be raw values or restricted tokens."),
    ("GENERATED_MODE_BRAND", "error", "Generated pages contain no source brand/wordmark/domain spelling."),
    ("GENERATED_MODE_PERSON", "error", "Generated pages name no real person from the source (owner, credited developer, artists, contact email, age)."),
    ("GENERATED_MODE_PROJECT", "error", "Generated pages reuse no real project title, client name or project id."),
    ("GENERATED_MODE_COPY", "error", "Generated pages reuse no source copy (5-word shingle overlap or equality with any registry string of 3+ words)."),
    ("GENERATED_MODE_CTA", "error", "Generated pages reuse no source call-to-action / interaction label."),
    ("GENERATED_MODE_URL", "error", "Generated pages link only to site-relative paths or reserved placeholder domains; no source domain, social profile, email or store link."),
    ("GENERATED_MODE_ASSET", "error", "Generated pages use only generation-safe asset roles with placeholder://, generated:// or user-supplied:// sources and no source file names."),
    ("GENERATED_MODE_LOGO", "error", "Generated pages never use the source wordmark/favicon roles."),
    ("RETRIEVAL_PIN", "error", "Section contracts and the allowlist must agree with the retrieval pin in code: runtime UI is never retrievable, content sections always are."),
    ("ASSET_AVAILABILITY_PIN", "error", "assets/asset-roles.json availability must equal PINNED_AVAILABILITY in code; validation always uses the pinned value."),
    ("REFERENCE_ASSET_SOURCE", "error", "Reference pages may use reference-only/blocked roles only with site-relative source paths (evidence), never placeholder schemes for source roles."),
]


def build_graph():
    rules = [{"id": i, "severity": s, "rule": r, "enforcedBy": f"schema/semantic_validate.py::{i}"} for i, s, r in GRAPH_RULES]
    doc = {"version": VERSION, "note": "Rules a JSON Schema cannot express. The validator's RULES table must list exactly these ids with these severities (verify_all.py checks it).",
           "webglScenePatterns": ["gallery-strip-scroll", "plane-focus-stage", "floating-digits"], "rules": rules}
    wjson("compatibility/graph.json", doc)
    return rules


# ---------------------------------------------------------------------------------------------
# 9. Source-brand leakage registry (patterns harvested from the real source)
# ---------------------------------------------------------------------------------------------
def build_source_brand():
    nav_src = "\n".join(lines_of("project", CLAY))
    s924 = "\n".join(lines_of("project", C924))
    email = re.search(r'writeText\("([^"]+@[^"]+)"\)', s924).group(1)
    socials = sorted(set(re.findall(r'href: "(https://[^"]+)"', nav_src + s924)))
    copy = []
    copy += HERO_LINES + [" ".join(HERO_LINES), INTRO_NOTE, NOTFOUND_HEADING, NOTFOUND_BODY, MOBILE_ABOUT_TITLE.replace("\n", " ")]
    for it in ABOUT_ITEMS:
        copy += [it["intro"], it["description"], it["mobile"]]
    for sv in MOBILE_SERVICES:
        copy.append(sv["description"])
    for p in PROJECTS:
        copy += [para for para in p["description"].split("\n\n") if para.strip()]
    copy = [c for c in dict.fromkeys(copy) if c]
    doc = {
        "version": VERSION,
        "note": "Single registry of source-identity patterns, harvested by extraction/build_repo.py from the real source (navbar, preloader, About copy, project data, 404 page). Used by schema/semantic_validate.py in generated mode only; reference mode may contain all of it.",
        "brand": {"patterns": [r"\brustam\b", r"\bkerimov\b", r"kerimov\s*designs", r"kerimovdesigns", r"kerimov\.designs", r"rustam-kerimov"],
                  "evidence": [cite(C924, 'children: "KERIMOV DESIGNS",'), cite("index.html", "<title>Rustam Kerimov | Portfolio</title>")]},
        "person": {"patterns": [r"rustam\s+kerimov", r"jonas\s*nygaard", r"\bcaiman\b", r"yayoi\s+kusama", r"dana\s+schutz", r"cory\s+arcangel", r"cipe\s+pineles", r"keith\s+haring",
                                re.escape(email), r"rustam-98", r"age:\s*27"],
                   "evidence": [cite(C924, 'children: "Jonas Nygaard",'), cite(C924, "await navigator.clipboard.writeText("), cite(C272, 'text: "Age: 27",')]},
        "project": {"titles": [p["title"] for p in PROJECTS], "ids": [p["id"] for p in PROJECTS],
                    "patterns": [r"\bmori\b", r"kistefos", r"aurelis", r"posters\s+bundle", r"dr[øo]mmenes\s+melodi", r"echo\s+festival", r"breens?\s+bygg", r"\bi-d\s+magazine\b",
                                 r"maltesers", r"bylarm", r"by:larm"],
                    "evidence": [cite(PROJ, '"title": "MORI",'), cite(C272, '{ src: "/bylarm-new.mp4", discipline: "Motion & Animation" },')]},
        "location": {"patterns": [r"oslo,?\s*norway"], "evidence": [cite(CLAY, '"Oslo, Norway",')]},
        "url": {"domains": ["kerimovdesigns.com", "instagram.com/kerimov.designs", "linkedin.com/in/rustam-kerimov-75bb5a331", "jonasnygaard.com", "hotmail.com", "ufs.sh", "utfs.io"],
                "observedLinks": socials,
                "reservedPlaceholderDomains": [".example", ".invalid", "example.com", "example.org", "example.net"],
                "evidence": [cite(CLAY, 'href: "https://www.linkedin.com/in/rustam-kerimov-75bb5a331/",'), cite(C924, 'href: "https://www.jonasnygaard.com",')]},
        "cta": {"strings": ["Copy Email", "Copy email address", "Copied!", "Copy failed", "Back to portfolio", "Back to work", "Scroll or click to explore", "About me",
                            "Selected Work:", "About the project:", "Design / Development:", "RETURN", "NEXT"],
                "evidence": [cite(CLAY, ': "Copy Email",'), cite(NFJSX, "<span>Back to portfolio</span>"), cite(C272, '[h, m] = (0, o.useState)("RETURN"),')]},
        "assetFilenames": {"patterns": [r"rk-portrait", r"rk-about", r"bylarm-new", r"visual-identity\.jpg", r"logo-design\.jpg", r"art-direction\.jpg", r"editorial-design\.jpg",
                                        r"/projects/", r"hhEReYBoKW7E", r"favicon\.ico"],
                           "evidence": [cite(C272, '{ src: "/visual-identity.jpg", discipline: "Visual Identities" },')]},
        "copy": {"shingleSize": 5, "equalityMinWords": 3, "strings": copy,
                 "evidence": [cite(C272, 'text: "Take a look at my selected projects below'), cite_range(C272, "      let D = [", "        H = [0.16, 1, 0.3, 1],"), cite(PROJ, '"description": "MORI is a fictional')]},
    }
    wjson("policy/source-brand.json", doc)
    return doc


# ---------------------------------------------------------------------------------------------
# 10. Token catalog + policy + allowlist
# ---------------------------------------------------------------------------------------------
SLOT_RULES = {
    "textColor": {"prefixes": ["text."], "type": "color"},
    "surface": {"prefixes": ["surface."], "type": "color"},
    "border": {"prefixes": ["border.", "focus."], "type": "color"},
    "fontFamily": {"prefixes": ["typography.family."], "type": "fontFamily"},
    "typeScale": {"prefixes": ["typography.size.", "component.navbar.", "component.overlay.", "component.cursor."], "type": "fontSize"},
    "fontWeight": {"prefixes": ["typography.weight."], "type": "fontWeight"},
    "spacing": {"prefixes": ["spacing."], "type": "dimension"},
    "motionEasing": {"prefixes": ["motion.easing."], "type": None},
}


def build_llm(flat, sections, comps):
    catalog = {"version": VERSION, "note": "Flattened from tokens/** by extraction/build_repo.py (verify_all.py re-flattens and compares). PageSpecs reference tokens by id.",
               "themes": ["dark"], "tokens": {}}
    for tid, t in sorted(flat.items()):
        e = {"layer": t["layer"], "type": t["type"], "value": t["value"], "file": t["file"], "themes": [] if t.get("restricted") else ["dark"]}
        if t.get("restricted"):
            e["restricted"] = t["restricted"]
        if t.get("opacity"):
            e["opacity"] = t["opacity"]
        catalog["tokens"][tid] = e
    wjson("tokens/llm/token-catalog.json", catalog)
    categories = sorted(set(t.split(".")[0] for t in flat))
    policy = {"version": VERSION,
              "approvedThemes": ["dark"],
              "slots": SLOT_RULES,
              "restrictedTokens": {"rule": "Tokens marked restricted (internal shader constants) are never valid in a PageSpec.", "prefixes": ["color.gl."]},
              "rawValueRestrictions": {"color": "no #hex, rgb(), hsl(), oklch() or named colours in token slots", "spacing": "no px/rem/em/% literals: use spacing.* tokens",
                                       "fontFamily": "only typography.family.* tokens (Satoshi stack, UI stack, digits stack)"},
              "catalogCategories": categories,
              "approvedFontFamilies": [str(flat[k]["value"][0]) for k in sorted(flat) if k.startswith("typography.family.")],
              "overrides": "PageSpec nodes may carry an optional `tokens` object (slot -> token id). There is no other style override mechanism; section contracts own all other styling.",
              "enforcedBy": "schema/semantic_validate.py::TOKEN_POLICY"}
    wjson("tokens/llm/token-policy.json", policy)
    allow = {"version": ALLOWLIST_VERSION,
             "note": "Closed list of every contract an AI may compose or configure. verify_all.py checks parity with the contract files both ways and that retrievalEligible matches the contracts and the pin.",
             "nodeSettableProperties": ["section", "variant", "content", "motion", "tokens"],
             "entries": []}
    for s in sections:
        allow["entries"].append({"id": s["id"], "kind": "section", "file": f"sections/{s['id']}.json", "retrievalEligible": s["retrievalEligible"],
                                 "contentFields": sorted(s["content"]["fields"].keys()), "motionPatterns": s["motion"]["patterns"], "generatedAssetRoles": s["generatedAssetRoles"]})
    for cid, c in sorted(comps.items()):
        allow["entries"].append({"id": cid, "kind": c["kind"], "file": f"{c['kind']}s/{cid}.json", "props": c["props"]})
    wjson("tokens/llm/component-allowlist.json", allow)
    mp = {"version": VERSION, "note": "Motion patterns observed in the source. reducedMotionFallback is pinned in schema/semantic_validate.py (MOTION_FALLBACKS). sourceImplementsFallback=false means the source itself has no reduced-motion branch for that pattern; the fallback is then a requirement for generated pages, not a description of the source.",
          "fallbacks": FALLBACKS, "patterns": MOTION_PATTERNS}
    wjson("tokens/00-foundation/motion-patterns.json", mp)
    return catalog, policy, allow


# ---------------------------------------------------------------------------------------------
# 11. PageSpec schema
# ---------------------------------------------------------------------------------------------
def field_schema(f, roles):
    t = f.get("type")
    if t == "text":
        return {"type": "string", "minLength": 1}
    if t == "link":
        return {"type": "string", "minLength": 1}
    if t == "year":
        return {"type": "string", "pattern": "^[0-9]{4}$"}
    if t == "digits":
        return {"type": "string", "pattern": "^[0-9]{3}$"}
    if t == "integer":
        return {"type": "integer", "minimum": f.get("min", 0), "maximum": f.get("max", 99)}
    if t == "enum":
        return {"type": "string", "enum": f["values"]}
    if t == "asset":
        return {"$ref": "#/definitions/asset"}
    if t == "object":
        props = {k: field_schema(v, roles) for k, v in f["of"].items()}
        return {"type": "object", "additionalProperties": False, "properties": props, "required": sorted(props)}
    if t == "list":
        of = f["of"]
        if "type" in of and isinstance(of["type"], str):
            item = field_schema(of, roles)
        else:
            props = {k: field_schema(v, roles) for k, v in of.items()}
            req = [k for k, v in of.items() if k != "media" and k != "kind" or k == "kind"]
            item = {"type": "object", "additionalProperties": False, "properties": props, "required": sorted(k for k in props if k not in ("media",))}
        d = {"type": "array", "items": item}
        if "minItems" in f:
            d["minItems"] = f["minItems"]
        if "maxItems" in f:
            d["maxItems"] = f["maxItems"]
        return d
    raise SystemExit(f"unknown field type {t}")


def build_schema(sections, templates, roles):
    retrievable = [s for s in sections if s["retrievalEligible"]]
    utilities = [s["id"] for s in sections if not s["retrievalEligible"]]
    branches = []
    for s in retrievable:
        props = {k: field_schema(v, roles) for k, v in s["content"]["fields"].items()}
        req = sorted(k for k, v in s["content"]["fields"].items() if v.get("required"))
        content = {"type": "object", "additionalProperties": False, "properties": props}
        if req:
            content["required"] = req
        branches.append({"if": {"properties": {"section": {"const": s["id"]}}, "required": ["section"]},
                         "then": {"properties": {"content": content, "motion": {"properties": {"pattern": {"enum": s["motion"]["patterns"]}}}}}})
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "pagespec.schema.json",
        "title": "PageSpec (portfolio design-repo)",
        "type": "object",
        "additionalProperties": False,
        "required": ["pageSpecVersion", "mode", "template", "route", "theme", "meta", "nodes"],
        "properties": {
            "pageSpecVersion": {"const": PAGESPEC_VERSION},
            "mode": {"type": "string", "enum": ["reference", "generated"], "description": "reference = faithful reconstruction of the source (evidence); generated = a new page for someone else, carrying no source identity or content."},
            "template": {"type": "string", "enum": sorted(templates)},
            "route": {"type": "string", "minLength": 1},
            "theme": {"type": "string", "enum": ["dark"]},
            "meta": {"type": "object", "additionalProperties": False, "required": ["title", "description"],
                     "properties": {"title": {"type": "string", "minLength": 1, "maxLength": 70}, "description": {"type": "string", "minLength": 1, "maxLength": 160}}},
            "runtimeLayers": {"type": "array", "uniqueItems": True, "items": {"type": "string", "enum": utilities}},
            "nodes": {"type": "array", "minItems": 1, "items": {"$ref": "#/definitions/node"}},
        },
        "definitions": {
            "assetRole": {"type": "string", "enum": sorted(roles)},
            "asset": {"type": "object", "additionalProperties": False, "required": ["assetRole", "src", "alt"],
                      "properties": {"assetRole": {"$ref": "#/definitions/assetRole"}, "src": {"type": "string", "minLength": 1}, "alt": {"type": "string"}}},
            "motion": {"type": "object", "additionalProperties": False, "required": ["pattern", "reducedMotionFallback"],
                       "properties": {"pattern": {"type": "string", "enum": sorted(MOTION_PATTERNS)},
                                      "reducedMotionFallback": {"type": "string", "enum": FALLBACKS},
                                      "trigger": {"type": "string", "enum": ["load", "hover", "wheel", "click", "route-change", "loop"]}}},
            "tokens": {"type": "object", "additionalProperties": False, "properties": {k: {"type": "string", "minLength": 1} for k in SLOT_RULES}},
            "node": {"type": "object", "additionalProperties": False, "required": ["section", "content", "motion"],
                     "properties": {"section": {"type": "string", "enum": [s["id"] for s in retrievable]},
                                    "variant": {"type": "string", "enum": ["default"]},
                                    "content": {"type": "object"},
                                    "motion": {"$ref": "#/definitions/motion"},
                                    "tokens": {"$ref": "#/definitions/tokens"}},
                     "allOf": branches},
        },
    }
    wjson("schema/pagespec.schema.json", schema)
    sc = {
        "$schema": "http://json-schema.org/draft-07/schema#", "$id": "section-contract.schema.json", "title": "Section contract", "type": "object",
        "additionalProperties": False,
        "required": ["id", "version", "title", "source", "semantic", "retrievalEligible", "content", "constraints", "responsive", "motion", "generatedAssetRoles", "referenceAssetRoles", "tokens", "composes", "evidence", "measured"],
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z]+\\.[a-z0-9-]+$"}, "version": {"type": "string"}, "title": {"type": "string"},
            "source": {"type": "object", "additionalProperties": False, "required": ["id", "root", "file", "lines", "tag"],
                       "properties": {"id": {"type": "string"}, "root": {"enum": ["project", "repo"]}, "file": {"type": "string"}, "lines": {"type": "string", "pattern": "^[0-9]+(-[0-9]+)?$"}, "tag": {"type": "string", "minLength": 3}, "note": {"type": "string"}}},
            "semantic": {"type": "object", "additionalProperties": False, "required": ["id", "category", "purpose"],
                         "properties": {"id": {"type": "string"}, "category": {"enum": ["SHELL", "HERO", "CONTENT", "PORTFOLIO", "PROJECT_DETAIL", "MEDIA", "PROFILE", "NAVIGATION", "NOTICE", "UTILITY"]}, "purpose": {"type": "string", "minLength": 10}}},
            "retrievalEligible": {"type": "boolean"},
            "retrievalIneligibleReason": {"type": "string", "minLength": 30},
            "content": {"type": "object", "additionalProperties": False, "required": ["fields"], "properties": {"fields": {"type": "object"}}},
            "constraints": {"type": "object", "additionalProperties": False, "properties": {k: {"type": "boolean"} for k in ("onePerPage", "mustBeFirst", "mustBeLast", "homeOnly")}},
            "responsive": {"type": "object", "additionalProperties": False, "required": ["desktop", "mobile", "breakpoint"],
                           "properties": {"desktop": {"type": "string"}, "mobile": {"type": "string"}, "breakpoint": {"type": ["string", "null"]}}},
            "motion": {"type": "object", "additionalProperties": False, "required": ["patterns", "default", "reducedMotionFallback", "sourceImplementsFallback"],
                       "properties": {"patterns": {"type": "array", "minItems": 1, "items": {"enum": sorted(MOTION_PATTERNS)}}, "default": {"enum": sorted(MOTION_PATTERNS)},
                                      "reducedMotionFallback": {"enum": FALLBACKS}, "sourceImplementsFallback": {"type": "boolean"}}},
            "generatedAssetRoles": {"type": "array", "items": {"enum": sorted(roles)}}, "referenceAssetRoles": {"type": "array", "items": {"enum": sorted(roles)}},
            "tokens": {"type": "array", "items": {"type": "string"}}, "composes": {"type": "array", "items": {"type": "string"}},
            "evidence": {"type": "array", "items": {"$ref": "#/definitions/citation"}}, "measured": {"type": "object"}, "notes": {"type": "string"},
        },
        "allOf": [{"if": {"properties": {"retrievalEligible": {"const": False}}}, "then": {"required": ["retrievalIneligibleReason"]}}],
        "definitions": {"citation": {"type": "object", "additionalProperties": False, "required": ["root", "file", "lines", "tag"],
                                     "properties": {"root": {"enum": ["project", "repo"]}, "file": {"type": "string"}, "lines": {"type": "string", "pattern": "^[0-9]+(-[0-9]+)?$"}, "tag": {"type": "string"}, "note": {"type": "string"}}}},
    }
    wjson("schema/section-contract.schema.json", sc)
    return schema


# ---------------------------------------------------------------------------------------------
# 12. Examples
# ---------------------------------------------------------------------------------------------
def node(section, content, pattern=None, sections_by_id=None, tokens=None):
    s = sections_by_id[section]
    pattern = pattern or s["motion"]["default"]
    n = {"section": section, "content": content, "motion": {"pattern": pattern, "reducedMotionFallback": MOTION_PATTERNS[pattern]["reducedMotionFallback"]}}
    if tokens:
        n["tokens"] = tokens
    return n


def build_examples(sections):
    by = {s["id"]: s for s in sections}
    p0 = PROJECTS[0]
    media0, vid0 = project_media(p0)
    nav_ref = {"ownerName": "Rustam Kerimov", "occupation": "Graphic Designer", "location": "Oslo, Norway",
               "contactLinks": [{"label": "Copy Email", "href": "mailto:rustam-98@hotmail.com", "kind": "copy-email"},
                                {"label": "Instagram", "href": "https://www.instagram.com/kerimov.designs/", "kind": "social"},
                                {"label": "LinkedIn", "href": "https://www.linkedin.com/in/rustam-kerimov-75bb5a331/", "kind": "social"}],
               "profileLinkLabel": "About me"}
    footer_ref = {"servicesHeading": "Services:", "services": [s["title"] for s in MOBILE_SERVICES], "connectHeading": "Connect:",
                  "contactLinks": nav_ref["contactLinks"], "creditLabel": "Design / Development:", "credit": {"label": "Jonas Nygaard", "href": "https://www.jonasnygaard.com"}}
    ex = {}
    ex["reference.home"] = {
        "pageSpecVersion": PAGESPEC_VERSION, "mode": "reference", "template": "home", "route": "/", "theme": "dark",
        "meta": {"title": "Rustam Kerimov | Portfolio", "description": "Graphic designer, Rustam Kerimov's portfolio"},
        "runtimeLayers": ["utility.preloader", "utility.page-transition", "utility.overlay-backdrop", "utility.hover-title", "utility.toast"],
        "nodes": [node("shell.navbar", nav_ref, sections_by_id=by, tokens={"textColor": "text.primary", "fontFamily": "typography.family.display", "typeScale": "component.navbar.value-size"}),
                  node("hero.intro", {"headingLines": HERO_LINES, "portrait": {"assetRole": "person.portrait-source", "src": "/rk-portrait.jpg", "alt": "Portrait of Rustam Kerimov"}, "profileHref": "/about"}, sections_by_id=by,
                       tokens={"typeScale": "typography.size.hero-display", "fontWeight": "typography.weight.bold"}),
                  node("content.intro-note", {"text": INTRO_NOTE}, sections_by_id=by),
                  node("portfolio.work-index", {"heading": "Selected Work:", "items": [{"title": p["title"], "href": f"/project/{p['id']}", "cover": {"assetRole": "project.cover-source", "src": p["src"], "alt": p["title"]}} for p in PROJECTS]}, sections_by_id=by),
                  node("shell.footer-contact", footer_ref, sections_by_id=by)]}
    disc = ABOUT_ITEMS
    about_media = [{"asset": {"assetRole": "person.portrait-source", "src": "/rk-portrait.jpg", "alt": "Profile"}, "kind": "image"}]
    for s in MOBILE_SERVICES:
        about_media.append({"asset": {"assetRole": "discipline.media-source", "src": s["src"], "alt": s["title"]}, "kind": s["type"]})
    ex["reference.about"] = {
        "pageSpecVersion": PAGESPEC_VERSION, "mode": "reference", "template": "about", "route": "/about", "theme": "dark",
        "meta": {"title": "Rustam Kerimov | Portfolio", "description": "Graphic designer, Rustam Kerimov's portfolio"},
        "runtimeLayers": ["utility.preloader", "utility.page-transition", "utility.overlay-backdrop", "utility.kinetic-cursor", "utility.toast"],
        "nodes": [node("shell.navbar", nav_ref, sections_by_id=by),
                  node("about.profile-header", {"title": disc[0]["title"], "intro": disc[0]["intro"], "description": disc[0]["description"]}, sections_by_id=by),
                  node("about.media-stage", {"media": about_media}, sections_by_id=by),
                  node("about.discipline-list", {"items": [{"label": d["label"], "summary": d["mobile"], "media": m["asset"]} for d, m in zip(disc, about_media)]}, sections_by_id=by),
                  node("about.footer-meta", {"hint": "Scroll or click to explore", "facts": ["Oslo, Norway", "Age: 27"]}, sections_by_id=by),
                  node("shell.footer-contact", footer_ref, sections_by_id=by)]}
    pm = [{"asset": {"assetRole": "project.cover-source" if i == 0 else "project.gallery-source", "src": s, "alt": f"{p0['title']} — work {i + 1}"}, "kind": "image"} for i, s in enumerate(media0)]
    if vid0:
        pm.append({"asset": {"assetRole": "project.video-source", "src": p0["srcVideo"], "alt": f"{p0['title']} video"}, "kind": "video"})
    ex["reference.project-detail"] = {
        "pageSpecVersion": PAGESPEC_VERSION, "mode": "reference", "template": "project-detail", "route": f"/project/{p0['id']}", "theme": "dark",
        "meta": {"title": "Rustam Kerimov | Portfolio", "description": "Graphic designer, Rustam Kerimov's portfolio"},
        "runtimeLayers": ["utility.preloader", "utility.page-transition", "utility.overlay-backdrop", "utility.kinetic-cursor", "utility.toast"],
        "nodes": [node("shell.navbar", nav_ref, sections_by_id=by),
                  node("project.header", {"title": p0["title"], "description": p0["description"], "tags": p0["tags"]}, sections_by_id=by,
                       tokens={"textColor": "text.overlay", "typeScale": "typography.size.project-title"}),
                  node("project.media-stage", {"media": pm}, sections_by_id=by),
                  node("project.meta", {"yearLabel": "Year:", "year": p0["type"], "toolsLabel": "Tools:", "tools": p0["tools"]}, sections_by_id=by),
                  node("project.footer-bar", {"hint": "Scroll or click to explore", "tags": p0["tags"], "mediaCount": len(pm)}, sections_by_id=by),
                  node("shell.footer-contact", footer_ref, sections_by_id=by)]}
    ex["reference.not-found"] = {
        "pageSpecVersion": PAGESPEC_VERSION, "mode": "reference", "template": "not-found", "route": "/this-route-does-not-exist", "theme": "dark",
        "meta": {"title": "Rustam Kerimov | Portfolio", "description": "Graphic designer, Rustam Kerimov's portfolio"},
        "runtimeLayers": ["utility.page-transition", "utility.toast"],
        "nodes": [node("shell.navbar", nav_ref, sections_by_id=by),
                  node("notfound.digits-scene", {"digits": "404"}, sections_by_id=by),
                  node("notfound.message", {"heading": NOTFOUND_HEADING, "body": NOTFOUND_BODY, "backLinkLabel": "Back to portfolio", "backHref": "/"}, sections_by_id=by)]}

    # ---- generated (fictional illustrator "Mara Lindqvist", original copy, placeholder media/URLs) ----
    nav_gen = {"ownerName": "Mara Lindqvist", "occupation": "Type Illustrator", "location": "Harbor City",
               "contactLinks": [{"label": "Email me", "href": "mailto:hello@studio.example", "kind": "copy-email"},
                                {"label": "Sketchbook", "href": "https://sketchbook.example/mara", "kind": "social"}],
               "profileLinkLabel": "Profile"}
    footer_gen = {"servicesHeading": "Practice", "services": ["Lettering", "Book covers", "Signage"], "connectHeading": "Reach", "contactLinks": nav_gen["contactLinks"],
                  "creditLabel": "Site by", "credit": {"label": "Northwind Web", "href": "https://northwind.example"}}
    gen_projects = [("Saltmarsh Almanac", "almanac"), ("Lantern Market", "lantern"), ("Quiet Ferry", "ferry"), ("Paper Orchard", "orchard")]
    ex["generated.home"] = {
        "pageSpecVersion": PAGESPEC_VERSION, "mode": "generated", "template": "home", "route": "/", "theme": "dark",
        "meta": {"title": "Mara Lindqvist, type illustrator", "description": "Lettering, book covers and wayfinding drawn by hand and set in motion."},
        "runtimeLayers": ["utility.preloader", "utility.page-transition", "utility.hover-title"],
        "nodes": [node("shell.navbar", nav_gen, sections_by_id=by, tokens={"textColor": "text.primary", "fontFamily": "typography.family.display"}),
                  node("hero.intro", {"headingLines": ["LETTERS DRAWN SLOWLY,", "SET IN MOTION."], "portrait": {"assetRole": "person.portrait-fictional", "src": "generated://portrait/fictional-illustrator-4x5", "alt": "Illustrated self-portrait of a fictional illustrator"}, "profileHref": "/about"}, sections_by_id=by,
                       tokens={"typeScale": "typography.size.hero-display", "spacing": "spacing.8"}),
                  node("content.intro-note", {"text": "Browse the drawings and commissions below. New lettering briefs are welcome from spring onward; a short note with your timeline is the best start."}, sections_by_id=by),
                  node("portfolio.work-index", {"heading": "Recent work", "items": [{"title": t, "href": f"/project/{slug}", "cover": {"assetRole": "project.cover-generated", "src": f"generated://cover/{slug}", "alt": f"{t} cover"}} for t, slug in gen_projects]}, sections_by_id=by),
                  node("shell.footer-contact", footer_gen, sections_by_id=by)]}
    ex["generated.about"] = {
        "pageSpecVersion": PAGESPEC_VERSION, "mode": "generated", "template": "about", "route": "/about", "theme": "dark",
        "meta": {"title": "About Mara Lindqvist", "description": "Practice, process and the kinds of lettering commissions taken on."},
        "runtimeLayers": ["utility.preloader", "utility.kinetic-cursor"],
        "nodes": [node("shell.navbar", nav_gen, sections_by_id=by),
                  node("about.profile-header", {"title": "MARA LINDQVIST", "intro": "An illustrator who draws letters before setting them.", "description": "Most commissions start as pencil roughs and end as vector marks, animated titles or painted signs."}, sections_by_id=by),
                  node("about.media-stage", {"media": [{"asset": {"assetRole": "person.portrait-fictional", "src": "generated://portrait/fictional-illustrator-4x5", "alt": "Fictional illustrator at a drawing desk"}, "kind": "image"},
                                                       {"asset": {"assetRole": "discipline.media-generated", "src": "generated://discipline/lettering", "alt": "Hand lettering sample"}, "kind": "image"},
                                                       {"asset": {"assetRole": "media.placeholder", "src": "placeholder://media/16x9", "alt": "Placeholder"}, "kind": "video"}]}, sections_by_id=by),
                  node("about.discipline-list", {"items": [{"label": "Lettering", "summary": "Custom letterforms for covers, labels and titles.", "media": {"assetRole": "discipline.media-generated", "src": "generated://discipline/lettering", "alt": "Lettering"}},
                                                           {"label": "Signage", "summary": "Painted and printed signs for small shops.", "media": {"assetRole": "media.placeholder", "src": "placeholder://media/4x3", "alt": "Signage placeholder"}}]}, sections_by_id=by),
                  node("about.footer-meta", {"hint": "Click the image to continue", "facts": ["Harbor City", "Since 2015"]}, sections_by_id=by)]}
    ex["generated.project-detail"] = {
        "pageSpecVersion": PAGESPEC_VERSION, "mode": "generated", "template": "project-detail", "route": "/project/almanac", "theme": "dark",
        "meta": {"title": "Saltmarsh Almanac, lettering", "description": "Cover lettering and chapter marks for a fictional nature almanac."},
        "runtimeLayers": ["utility.page-transition", "utility.overlay-backdrop", "utility.kinetic-cursor"],
        "nodes": [node("shell.navbar", nav_gen, sections_by_id=by),
                  node("project.header", {"title": "Saltmarsh Almanac", "description": "A fictional almanac needed a title that felt hand-cut from reeds.\n\nEach chapter mark reuses the same three strokes, so the set reads as one family from spine to index.", "tags": ["lettering", "book cover"]}, sections_by_id=by,
                       tokens={"textColor": "text.overlay", "typeScale": "typography.size.project-title"}),
                  node("project.media-stage", {"media": [{"asset": {"assetRole": "project.cover-generated", "src": "generated://cover/almanac", "alt": "Almanac cover"}, "kind": "image"},
                                                         {"asset": {"assetRole": "project.gallery-generated", "src": "generated://gallery/almanac-1", "alt": "Chapter marks"}, "kind": "image"},
                                                         {"asset": {"assetRole": "project.video-generated", "src": "generated://video/almanac-loop", "alt": "Animated title"}, "kind": "video"}]}, sections_by_id=by),
                  node("project.meta", {"yearLabel": "Year", "year": "2024", "toolsLabel": "Media", "tools": "Pencil, vector"}, sections_by_id=by),
                  node("project.footer-bar", {"hint": "Wheel to browse", "tags": ["lettering", "book cover"], "mediaCount": 3}, sections_by_id=by)]}
    ex["generated.not-found"] = {
        "pageSpecVersion": PAGESPEC_VERSION, "mode": "generated", "template": "not-found", "route": "/missing-page", "theme": "dark",
        "meta": {"title": "Nothing drawn here", "description": "This address has no page."},
        "runtimeLayers": ["utility.page-transition"],
        "nodes": [node("shell.navbar", nav_gen, sections_by_id=by),
                  node("notfound.digits-scene", {"digits": "404"}, sections_by_id=by),
                  node("notfound.message", {"heading": "No sketch at this address.", "body": "The link may be old. Every finished drawing is still on the front page.", "backLinkLabel": "Return home", "backHref": "/"}, sections_by_id=by)]}
    for k, v in ex.items():
        wjson(f"schema/examples/{k}.json", v)
    return ex


# ---------------------------------------------------------------------------------------------
# 13. Measured values
# ---------------------------------------------------------------------------------------------
def build_measured(css_digest, measure, budgets, sections, templates):
    def load_opt(rel):
        p = os.path.join(REPO, rel)
        return json.load(open(p)) if os.path.exists(p) else None
    live = load_opt("extraction/measurements/live-sections.json")
    tablet = load_opt("extraction/measurements/clone-sections-1024.json")
    cat = {s["id"]: s["semantic"]["category"] for s in sections}
    sh = {"viewport": "1440x900", "tool": "extraction/measure_sections.mjs", "source": "extraction/measurements/clone-sections.json",
          "measuredAt": measure["measuredAt"], "target": "clone (local dev server); live site re-measured for reconciliation, see reconciliation", "templates": {}}
    mobile = {"viewport": "390x844", "templates": {}}
    for tname, tdef in templates.items():
        for key, holder in (("1440x900", sh), ("390x844", mobile)):
            m = measure["viewports"][key][tname]
            entry = {"route": m["route"], "documentHeightPx": m["documentHeight"], "sections": {}}
            inflow_total = 0
            for n in tdef["nodes"]:
                s = m["sections"].get(n["section"], {"present": False})
                if s.get("present"):
                    entry["sections"][n["section"]] = {"heightPx": s["height"], "inFlow": s["inFlow"], "position": s["position"], "category": cat[n["section"]]}
                    if s["inFlow"] and cat[n["section"]] != "SHELL":
                        inflow_total += 1
                else:
                    entry["sections"][n["section"]] = {"present": False, "category": cat[n["section"]],
                                                       "reason": "not rendered at this width (responsive variant)"}
            entry["inFlowContentSections"] = inflow_total
            if key == "390x844":
                entry["shares"] = {k: round(v["heightPx"] / float(m["documentHeight"]), 3) for k, v in entry["sections"].items() if v.get("inFlow") and v.get("category") != "SHELL"}
            holder["templates"][tname] = entry
    sh["inFlowNote"] = ("At 1440px every section is an absolutely/fixed positioned layer of one 100svh stage (documentHeight = 900), so each page has 0 in-flow content sections "
                        "and the >50%/>60% share rule is skipped (fewer than 3 in-flow sections). HERO thresholds still apply.")
    mobile["note"] = "Informational only: the wrapper gate is pinned to 1440px. At 390px the layout is an in-flow list; shares above 0.6 come from repeated-item lists (6 discipline blocks, stacked project media), not from a whole-page section."
    recon = {}
    if live:
        for key in live["viewports"]:
            for tname in live["viewports"][key]:
                lv = live["viewports"][key][tname]["sections"]
                cl = measure["viewports"].get(key, {}).get(tname, {}).get("sections", {})
                rows = {}
                for sid, b in lv.items():
                    c = cl.get(sid, {})
                    if b.get("present") or c.get("present"):
                        rows[sid] = {"liveHeightPx": b.get("height"), "cloneHeightPx": c.get("height"), "deltaPx": (None if not (b.get("present") and c.get("present")) else c["height"] - b["height"])}
                recon[f"{key}:{tname}"] = rows
    histo = {}
    for tname, m in measure["viewports"]["1440x900"].items():
        for k, v in m["histogram"].items():
            agg = histo.setdefault(k, {})
            for val, n in v.items():
                agg[val] = agg.get(val, 0) + n
    mv = {
        "version": VERSION,
        "note": "Citation trail for every decision. Paths with root=project resolve against the project folder that contains design-repo/ (src/, public/, index.html); verify_all.py checks them when that folder is present and warns (does not fail) when design-repo is used alone.",
        "sourceProject": {"kind": "local replica of a live personal portfolio (Vite + React app running the original's application modules)", "routesServed": ["/", "/about", "/project/:id", "* (404)"],
                          "projects": len(PROJECTS), "projectImages": sum(len(project_media(p)[0]) for p in PROJECTS), "projectVideos": sum(project_media(p)[1] for p in PROJECTS),
                          "nonProjectVideos": 1, "fonts": ["Satoshi Regular 400", "Medium 500", "Bold 700", "Black 900 (self-hosted woff2)"],
                          "groundwork": "No IA/CLONE_SPEC/QA/asset-manifest groundwork existed when this build started; an ia.json/IA.md appeared in the project root during the build (concurrent pass) and was cross-checked, see iaCrossCheck. Everything here was derived from src/ and fresh browser measurement."},
        "sourceFiles": {rel: {"lines": len(lines_of("project", rel)), "sha256": sha256_file(os.path.join(PROJECT, rel))} for rel in [C272, C924, CLAY, C404, NFJSX, APP, PROJ, "index.html"]},
        "cssExcerpt": {"source": CSS, "sourceSha256": css_digest, "excerpt": EXCERPT, "excerptSha256": sha256_file(os.path.join(REPO, EXCERPT)),
                       "why": "src/styles/site.css is a single minified line; citations point at the tracked prettified excerpt instead, and the source is pinned by hash."},
        "copyBudgets": {"method": "maxWords = measured maximum in the source rounded up (extraction/build_repo.py: budget())", "measuredMaxWords": budgets},
        "sectionHeights": {"1440x900": sh},
        "sectionHeightsMobile": {"390x844": mobile},
        "tabletCheck": ({"viewport": "1024x768", "source": "extraction/measurements/clone-sections-1024.json",
                         "result": "1024px renders the desktop stage (the layout switch is max-width 1023px)",
                         "templates": {t: {"documentHeightPx": v["documentHeight"], "sections": {k: s.get("height") for k, s in v["sections"].items() if s.get("present")}} for t, v in tablet["viewports"]["1024x768"].items()}} if tablet else None),
        "reconciliation": {"source": "extraction/measurements/live-sections.json", "method": "same finders, live site vs clone", "rows": recon} if live else None,
        "computedStyleHistogram1440": {"source": "extraction/measurements/clone-sections.json", "note": "Visible-element counts across the 4 templates; tokens were cross-checked against these.", "histogram": histo},
        "parity": {"harness": "extraction/parity/parity.mjs", "results": ["extraction/parity/results-run1.json", "extraction/parity/results-run2.json"], "gate": 0.8,
                   "exceptions": [],
                   "diagnosis": {
                       "mobile-390-home/portfolio.work-index": "lowest region score (about 0.90): live and clone captures are visually identical (same layout, crop and order); the residual is per-pixel noise inside the project photographs, i.e. the live site serves differently encoded image files than the local copies. Not a layout difference; above the 0.80 gate, no exception needed.",
                       "not-found/notfound.digits-scene": "about 0.98: the digits float on a continuous 6.5s loop driven by elapsed time, so two captures land on slightly different phases.",
                       "method": "captures were inspected side by side; videos frozen on frame 0 on both sides; interaction coordinates target the gallery strip (y 800 of 900) so hover and open-project reach the real states"}},
        "iaCrossCheck": ({
            "source": "ia.json / IA.md / matrix.csv in the project root (written by a concurrent ia-builder pass while this repo was being built; read-only here)",
            "evidence": [cite("ia.json", '"totalRoutes": 13'), cite("ia.json", '"totalTemplates": 4')],
            "agrees": ["13 routes, 4 templates (home, about, project-detail, not-found)", "desktop overlays render over the still-mounted, blurred work strip",
                       "runtime UI set: preloader, page transition, toast, overlay backdrop, kinetic cursor, hover title", "footer exists only below 1024px"],
            "differsOnPurpose": ["the IA lists mobile-only DOM variants as their own sections (work.grid, project.mobile-*, profile.mobile-*); here they are the responsive variants of one semantic section each, because they serve the same purpose (BASELINE R6: different DOM is not a different purpose)",
                                 "the IA splits the home opener into headline / portrait link / statement; here headline + portrait form the HERO and the statement is content.intro-note (it renders separately, desktop-only, with its own timing)"],
        } if os.path.isfile(os.path.join(PROJECT, "ia.json")) else None),
        "decisions": {
            "category": "portfolio (one person's work index, project pages, profile; no pricing, sign-up, accounts or checkout)",
            "templates": "4 page shapes; desktop and mobile are responsive variants of the same templates",
            "darkOnly": "single dark theme; no light theme or theme toggle exists",
            "fontBueno": "the source tags display text with a font class that the stylesheet never defines, so it inherits html's Satoshi stack; recorded as typography.family.display",
        },
    }
    wjson("extraction/measured-values.json", mv)
    return mv


# ---------------------------------------------------------------------------------------------
# 14. Manifest + policy (counts recomputed; hash from policy_hash.py)
# ---------------------------------------------------------------------------------------------
from counts import compute_counts  # shared with verify_all.py


def build_manifest():
    import policy_hash
    counts = compute_counts()
    pol_path = "policy/design-policy.json"
    policy = {
        "policyId": "n0-design-constraints-common", "policyVersion": "0.1.0", "commonIrVersion": "0.5", "enforcementMode": "hard-and-soft",
        "classification": {"category": "portfolio", "domain": "personal-graphic-design-portfolio",
                           "decidedFrom": ["three page shapes plus a 404: a work index (10 projects), one detail view per project and a profile of one graphic designer",
                                           "no pricing, plans, sign-up, trial, account, dashboard, checkout or integrations anywhere in src/",
                                           "the only conversion is contacting the designer (copy email, two social profiles)",
                                           "content is one person's projects, disciplines and biography"],
                           "evidence": [cite(APP, "const isKnownRoute"), cite(PROJ, '"title": "MORI",')],
                           "approval": {"status": "defined-pending-architecture-review", "architectureDecisionRecorded": False,
                                        "proposedBy": "agent (design-repo extraction); not ratified by the owner", "ratifiedBy": None, "ratifiedAt": None}},
        "generationRules": {"modes": "PageSpec.mode is reference (faithful reconstruction; evidence only) or generated (a new page for someone else).",
                            "generated": ["no source person, brand, project, client, location or contact detail (GENERATED_MODE_PERSON / BRAND / PROJECT)",
                                          "no source copy or interaction labels (GENERATED_MODE_COPY / CTA; registry policy/source-brand.json)",
                                          "no portrait of the owner, wordmark, favicon or project/discipline media; only generation-safe roles with placeholder://, generated:// or user-supplied:// sources (GENERATED_MODE_ASSET / LOGO)",
                                          "links only site-relative or on reserved placeholder domains (GENERATED_MODE_URL)"],
                            "always": ["node sequences match their template; copy within measured budgets; tokens from the catalog under the token policy",
                                       "runtime UI (preloader, cursor, transition, backdrop, hover title, toast) is never retrievable and never a node",
                                       "every motion pattern carries its pinned reduced-motion fallback"]},
        "localExtension": {"id": "portfolio-local-1", "rules": ["dark theme only", "desktop pages are single-viewport stages: sections are layers, not a scroll sequence; mobile is the scrolling variant of the same templates",
                                                                 "WebGL scene budget: one scene pattern per page (warn)", "a real person's photographs are blocked for generation, never only reference-only"]},
        "enforcedBy": {"files": policy_hash.POLICY_FILES, "contentHash": policy_hash.content_hash()},
    }
    wjson(pol_path, policy)
    man = {
        "repositoryId": "rustam-portfolio-design-repo",
        "repositoryVersion": VERSION, "pageSpecVersion": PAGESPEC_VERSION, "allowlistVersion": ALLOWLIST_VERSION,
        "versionFieldNote": "allowlistVersion is machine-checked (verify_all.py fails unless it equals tokens/llm/component-allowlist.json version). pageSpecVersion is machine-checked against the schema's const. repositoryVersion is documentation-only and hand-maintained; nothing checks it.",
        "status": "design-review-pending", "productionApproved": False,
        "approvalNote": "Production approval is a human sign-off; none has been recorded.",
        "category": "portfolio", "categoryEvidence": "policy/design-policy.json#classification.decidedFrom",
        "designPolicy": {"policyId": policy["policyId"], "policyVersion": policy["policyVersion"], "commonIrVersion": "0.5", "enforcementMode": "hard-and-soft",
                         "domain": "personal-graphic-design-portfolio", "localExtension": "policy/design-policy.json#localExtension",
                         "approval": "defined-pending-architecture-review", "architectureDecisionRecorded": False,
                         "contentHash": policy["enforcedBy"]["contentHash"], "contentHashOf": policy_hash.POLICY_FILES},
        "sourceStack": {"documentationOnly": True,
                        "original": "Next.js app router with client components; compiled Tailwind v4 CSS; three.js r176 through @react-three/fiber and drei; framer-motion; gsap; lenis smooth scroll; zustand; react-hot-toast",
                        "clone": "Vite 5 + React 18 app that runs the original's de-minified application modules verbatim through a small webpack-compatible module runtime",
                        "note": "Recorded for provenance only; no token name, section id, schema field or validator rule depends on it."},
        "defaultTheme": "dark", "schemaValidatedThemes": ["dark"],
        "counts": counts,
        "entryPoints": {"manifest": "registry.manifest.json", "readme": "README.md", "changelog": "CHANGELOG.md",
                        "pageSpecSchema": "schema/pagespec.schema.json", "sectionContractSchema": "schema/section-contract.schema.json",
                        "semanticValidator": "schema/semantic_validate.py", "adversarialTests": "schema/tests/adversarial_test.py", "examples": "schema/examples",
                        "templates": "templates/templates.json", "routes": "templates/routes.json", "sections": "sections", "primitives": "primitives", "components": "components",
                        "compatibilityGraph": "compatibility/graph.json", "assetRoles": "assets/asset-roles.json",
                        "tokenCatalog": "tokens/llm/token-catalog.json", "tokenPolicy": "tokens/llm/token-policy.json", "componentAllowlist": "tokens/llm/component-allowlist.json",
                        "motionPatterns": "tokens/00-foundation/motion-patterns.json", "themes": "tokens/themes",
                        "designPolicy": "policy/design-policy.json", "sourceBrandRegistry": "policy/source-brand.json",
                        "measuredValues": "extraction/measured-values.json", "cssExcerpt": EXCERPT, "verifyAll": "extraction/verify_all.py",
                        "wrapperGate": "extraction/wrapper_gate.py", "wrapperWhitelist": "extraction/wrapper-whitelist.json", "proveDrift": "extraction/prove_drift.py",
                        "policyHash": "extraction/policy_hash.py", "builder": "extraction/build_repo.py", "measureTool": "extraction/measure_sections.mjs",
                        "sectionFinders": "extraction/section-finders.json", "parityHarness": "extraction/parity/parity.mjs", "parityResults": "extraction/parity"},
        "ir": "No IR exists for this repo and none was generated (BASELINE R13).",
        "freshCloneVerification": "Pending: the project is not under version control, so a fresh git clone cannot be made. A clean-copy verification (copy without node_modules/dist/_reference/design-repo, npm ci, npm run build) and a design-repo-alone empty-directory run were performed instead.",
    }
    wjson("registry.manifest.json", man)
    rp = os.path.join(REPO, "README.md")
    if os.path.exists(rp):
        text = open(rp, encoding="utf-8").read()
        rows = "\n".join(f"| {k} | {v} |" for k, v in counts.items())
        text = re.sub(r"<!-- counts:start -->.*?<!-- counts:end -->", lambda m: "<!-- counts:start -->\n| key | value |\n|---|---|\n" + rows + "\n<!-- counts:end -->", text, flags=re.S)
        open(rp, "w", encoding="utf-8").write(text)
    return man


def main():
    digest, *_ = build_css_excerpt()
    measure = json.load(open(os.path.join(REPO, "extraction/measurements/clone-sections.json")))
    flat = build_tokens()
    roles = build_asset_roles()
    comps = build_primitives_components()
    budgets = compute_budgets()
    sections = build_sections(measure, budgets)
    templates, routes = build_templates()
    build_graph()
    build_source_brand()
    build_llm(flat, sections, comps)
    build_schema(sections, templates, roles)
    build_examples(sections)
    build_measured(digest, measure, budgets, sections, templates)
    if os.path.exists(os.path.join(REPO, "schema/semantic_validate.py")):
        build_manifest()
    print(f"built: {len(flat)} tokens, {len(sections)} sections, {len(templates)} templates, {len(routes)} routes, {len(roles)} asset roles")


if __name__ == "__main__":
    main()
