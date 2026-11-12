# Portfolio design-repo (graphic designer portfolio replica)

A machine-validated description of how this portfolio site looks and behaves: tokens, section
contracts, page templates, a PageSpec schema and the validators that keep them honest. A generator
(human or model) composes PageSpecs from it; the validators reject anything the source does not
support, and in `generated` mode anything that would reproduce the source's identity or content.

Status: **design-review-pending**, `productionApproved: false`. The category/policy binding and every
exception are proposals awaiting the owner's review; nothing here is self-approved.

## What the source is

A local replica of the live portfolio of a real graphic designer (a person, not a company). Its
copy, photographs of the owner, wordmark and project imagery are his. Consequences built in here:

- `reference` PageSpecs may carry the real content as evidence; `generated` PageSpecs may not
  (rules `GENERATED_MODE_*` in `schema/semantic_validate.py`, patterns in `policy/source-brand.json`).
- Photos of the owner are `blocked-for-generation`; project and discipline media are
  `reference-only`; both point at generation-safe substitutes (`assets/asset-roles.json`). The
  availability is pinned in code (`PINNED_AVAILABILITY` in `extraction/verify_all.py` and
  `schema/semantic_validate.py`), so editing the registry alone cannot loosen it.
- No media is copied into this folder.

Category: `portfolio`, bound to the generic `n0-design-constraints-common` 0.1.0 policy with a local
extension (`policy/design-policy.json`). Approval: `defined-pending-architecture-review`.

## Shape of the site (what the contracts encode)

- **Desktop (>= 1024px)** is one 100svh stage with no document scroll. A WebGL strip of project
  planes runs along the bottom; the wheel moves it. Every "section" is a layer of that stage. The
  project detail and the profile open as overlays over the stage (backdrop 97% ink + 24px blur).
- **Mobile (< 1024px)** is an ordinary scrolling list: opener, selected-work grid, contact footer;
  the project and profile pages become articles. These are responsive variants of the same
  templates, recorded in each contract's structured `responsive` field.
- **Templates (4):** `home` (/), `about` (/about), `project-detail` (/project/:id, 10 real ids),
  `not-found` (every other path). Every served route is mapped exactly once (`templates/routes.json`).
- **Runtime UI** (preloader, kinetic cursor, page transition, overlay backdrop, hover title, toast)
  has contracts with `retrievalEligible: false` and is never a node; templates list it under
  `runtimeLayers`.
- **Theme:** dark only. There is no light theme or toggle in the source.

## Layout

```
tokens/00-foundation   colour, opacity, typography, spacing, radius, effect, breakpoint, motion, motion-patterns
tokens/10-semantic     text.*, surface.*, border.*, focus.*
tokens/20-component    navbar / overlay / cursor overrides
tokens/30-layout       gutters, columns, stage, gallery geometry, grids
tokens/themes/dark.json   resolves every semantic/component token
tokens/llm/            token-catalog.json, token-policy.json, component-allowlist.json
primitives/ components/ sections/   contracts (sections: closed source{} + semantic{} split)
templates/             templates.json (structured nodes), routes.json
compatibility/graph.json   rhythm/structure/leakage rules with severities (== validator RULES)
assets/asset-roles.json    closed availability + generation-safe substitutes
policy/                design-policy.json, source-brand.json (leakage registry)
schema/                pagespec.schema.json (Draft-07), section-contract.schema.json,
                       semantic_validate.py, examples/ (reference + generated per template), tests/
extraction/            build_repo.py, verify_all.py, wrapper_gate.py, prove_drift.py, policy_hash.py,
                       counts.py, measure_sections.mjs, section-finders.json, measured-values.json,
                       measurements/ (geometry JSON), evidence/site.pretty.css, parity/ (harness + results)
```

## Counts (recomputed by `extraction/build_repo.py`; `verify_all.py` fails if they drift)

<!-- counts:start -->
| key | value |
|---|---|
| tokens | 173 |
| tokenFiles | 13 |
| primitives | 9 |
| components | 6 |
| sections | 21 |
| sectionsRetrievalIneligible | 6 |
| templates | 4 |
| routes | 13 |
| assetRoles | 18 |
| motionPatterns | 13 |
| graphRules | 26 |
| examples | 8 |
| referenceExamples | 4 |
| generatedExamples | 4 |
| adversarialCases | 89 |
| driftCases | 36 |
<!-- counts:end -->

## Run the checks

Python 3.9+ with `jsonschema` (Draft-07). From this folder:

```bash
python3 extraction/verify_all.py              # everything; exit 1 on any FAIL
python3 schema/semantic_validate.py           # all examples (or pass spec paths)
python3 schema/tests/adversarial_test.py      # mutations must be rejected, controls must pass
python3 extraction/prove_drift.py             # every check fails on injected drift (needs the source project next to this folder for the citation/CSS cases)
python3 extraction/wrapper_gate.py            # measured-height gate alone
python3 extraction/policy_hash.py --check     # policy content hash
```

Used alone (without the source project beside it), citations into `../src` and the stylesheet hash
degrade to WARN; everything else still runs.

Re-measuring needs Node with the `playwright` package resolvable (e.g. via `NODE_PATH`) and the
clone's dev server running:

```bash
BASE_URL=http://localhost:5190 node extraction/measure_sections.mjs > extraction/measurements/clone-sections.json
OUT_DIR=<scratch dir outside this repo> RUN_LABEL=run1 node extraction/parity/parity.mjs > extraction/parity/results-run1.json
python3 extraction/build_repo.py              # rebuild data files, measured values, counts, policy hash
```
`PLAYWRIGHT_CHROMIUM_PATH` optionally selects a browser. Captures stay outside the repo; only
numeric results are tracked.

## Measurements and parity

- Section heights at 1440x900 (and 390x844, 1024x768) are measured in a headless browser with
  WebGL (`extraction/measurements/*.json`, summarised in `extraction/measured-values.json`). At
  1440px every page is one 900px stage, so no page has 3+ in-flow sections and the share rule is
  skipped; no HERO exceeds 1800px. The live site, measured with the same finders, gives identical
  heights.
- Parity: `extraction/parity/results-run1.json` and `results-run2.json` (12 scenarios, per-section
  region scores and averages, run twice). See CHANGELOG for the numbers.

## Known limits

- **Fresh-clone verification is pending**: the project is not under version control, so a fresh
  `git clone` cannot be made. A clean copy (without `node_modules`, `dist`, the saved reference copy
  and this folder) was installed with `npm ci` and built with `npm run build` instead, and this
  folder was verified alone in an empty directory.
- Reduced motion: the source implements a reduced-motion branch for word reveals, the cursor and the
  page transition only. For the WebGL strip, hover blur, focus stage, preloader, 404 digits and
  backdrop the fallback is a requirement for generated pages (`sourceImplementsFallback: false`).
- The source has no reviews, ratings or testimonials; the schema has no field for them.
- No IR exists and none was generated.
