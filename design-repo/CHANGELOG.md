# Changelog

## 1.0.0 — initial build

Built from scratch (Situation A) against the current clone `src/` and fresh browser measurement of
the clone and the live site. No IA, spec, QA or asset-manifest groundwork existed when the build started;
an `ia.json`/`IA.md` written by a concurrent pass appeared in the project root mid-build and was
cross-checked (agrees on routes/templates/runtime UI; differs on purpose in splitting mobile variants
into separate sections — see `extraction/measured-values.json#iaCrossCheck`).

- Tokens from the compiled stylesheet (pinned by sha256, cited through the tracked prettified excerpt
  `extraction/evidence/site.pretty.css`) and literal values in the application modules; checked
  against a computed-style histogram of the rendered pages. Dark theme only.
- 21 section contracts (15 retrievable, 6 runtime UI with `retrievalEligible: false`), each with a
  closed `source{}` / `semantic{}` split, structured `responsive`, motion with pinned
  `reducedMotionFallback`, measured `maxWords` budgets and `generatedAssetRoles`.
- 4 templates with structured nodes; 13 routes (/, /about, 10 project ids, `*` fallback) each mapped once.
- PageSpec schema with required closed `mode` (`reference` | `generated`); semantic validator with
  template cross-reference, rhythm, motion, maxWords, token policy, asset-role and `GENERATED_MODE_*`
  leakage rules; asset availability and retrieval eligibility pinned in code.
- Reference and generated example per template; adversarial suite; wrapper-height gate with
  measured heights; drift proofs; policy content hash.

### Verification state (see the final report for command output)

- Fresh `git clone` verification: **pending** — the project is not under version control. A
  clean-copy build (`npm ci` + `npm run build`) and a design-repo-alone empty-directory run were done instead.
- Parity (live vs clone, 12 scenarios, 46 section regions, run twice): every section >= 0.80;
  min section score 0.9016 in both runs (mobile 390 work grid: per-pixel noise from differently
  encoded live image files, layout identical); section average 0.9967 (run 1) / 0.9965 (run 2);
  largest run-to-run difference 0.011. Full-viewport mismatch 0.00-0.07% for the 10 desktop/tablet
  scenarios, 2.70% mobile home (same image-encoding cause), 1.9-2.0% 404 (time-based digit float loop).
- No exceptions were added; none are approved.
- IR: none exists, none generated.
