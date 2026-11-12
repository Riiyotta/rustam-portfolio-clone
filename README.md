# kerimovdesigns.com — local replica

```bash
npm install
npm run dev      # http://localhost:5190
npm run build && npm run preview
```

## How it's put together

- `src/engine/chunks/*.js` — the original site's application modules (gallery WebGL scene,
  shaders, preloader, nav, About/project overlays, mobile list, 404 scene), de-minified and kept
  verbatim so motion and timing match exactly.
- `src/engine/runtime.js` — a tiny webpack-compatible loader that maps the modules' numeric
  vendor imports to npm packages (three r176, @react-three/fiber, drei, gsap, framer-motion,
  lenis, zustand, react-hot-toast). Unknown exports throw a clear error instead of failing silently.
- `src/engine/navigation.js` — stand-in for `next/navigation` (`usePathname`, `useRouter`).
- `src/App.jsx` — reproduces the Next.js layout/page tree; `src/components/NotFound.jsx` is the 404 route.
- `src/styles/site.css` — the original compiled stylesheet (Tailwind v4 output, Satoshi @font-face).
- `src/data/projects.json` — project content, with every image/video URL pointed at `public/`.
- `public/` — all fonts, images and videos, downloaded locally (no external asset URLs).

Routes: `/`, `/about`, `/project/:id`; anything else renders the 404 page.

## Information architecture (`ia.json`)

`ia.json` is the only IA file to hand-edit. `IA.md` and `matrix.csv` are **generated** from it — don't edit them.

```bash
node validate.mjs   # hard invariants: route sum, template count, section references, categories
node build.mjs      # regenerates IA.md + matrix.csv
```

What the data shows (13 routes, 4 templates, 28 sections):

- 10 of 13 routes (77%) are project-detail overlays from one template, fed by `src/data/projects.json`. The rest of the build effort is the home gallery, the About overlay and the 404 page.
- Only 8 sections are shared across templates, and every one is chrome or runtime UI: navbar, mobile footer, preloader, page transition, toast, backdrop, kinetic cursor, and the WebGL strip that stays mounted behind the overlays. All 20 content sections are single-use, so keep them page-local.
- Desktop and mobile are different compositions of the same templates (WebGL overlays vs. stacked mobile articles), so 20 of the 28 sections are breakpoint-specific (13 desktop-only, 7 mobile-only); each section's `scope` says which.
- The validator's one remaining note is intentional: `utility.page-transition` is *mounted* on all 13 routes but only *animates* between the 12 portfolio routes. Both numbers are true, so don't "fix" one to match the other.
