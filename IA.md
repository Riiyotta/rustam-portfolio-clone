# https://www.kerimovdesigns.com/ (local replica in this project, verified against the live site with Playwright)

Source: https://www.kerimovdesigns.com/ (local replica in this project, verified against the live site with Playwright)
Status: **measured-from-clone-source** · production approved: **false**
13 routes · 4 templates · 28 unique sections

> Generated from `ia.json` by `build.mjs`. Edit the JSON, not this file.

## Shape of the site

The largest 3 templates (Project detail (overlay), Home (work index), About (profile overlay)) account for 12 of 13 routes (92%). The remaining 1 routes span 1 template.

| template | routes | share |
|---|---:|---:|
| Project detail (overlay) | 10 | 77% |
| Home (work index) | 1 | 8% |
| About (profile overlay) | 1 | 8% |
| Not found (404) | 1 | 8% |

## Page chrome

**12 routes carry chrome = `full`** — Home (work index), About (profile overlay), Project detail (overlay).

**1 routes carry chrome = `nav-only`** — Not found (404).

## Sections by reuse

How widely a section is shared determines whether it belongs in a shared
component library or stays local to its page.

| section | category | templates | routes | implementation | scope |
|---|---|---:|---:|---|---|
| `shell.navbar` | SHELL | 4 | 13 | `src/engine/chunks/layout.js > module 5883 (Navbar)` | Present on all 13 routes, both breakpoints. |
| `utility.page-transition` | UTILITY | 4 | 13 | `src/engine/chunks/layout.js > module 7689 (ClientPageTransitionWrapper)` | Mounted around every route by the root layout; active only during client-side navigation between the 12 portfolio routes. |
| `utility.toast` | UTILITY | 4 | 13 | `src/App.jsx > Toaster (react-hot-toast)` | Mounted once in the root layout on all 13 routes. |
| `utility.preloader` | UTILITY | 3 | 12 | `src/engine/chunks/924.js > module 4760 (Preloader)` | Shown once on first load of the 12 portfolio routes (home, about, project); not on the not-found route. |
| `work.strip-webgl` | WORK | 3 | 12 | `src/engine/chunks/272.js > f (gallery planes, shaders)` | Desktop breakpoint on the 12 portfolio routes: interactive on home, and kept mounted (blurred behind the backdrop) under the about and project overlays. |
| `shell.footer-mobile` | SHELL | 3 | 12 | `src/engine/chunks/924.js > h (mobile footer)` | Mobile breakpoint on the 12 portfolio routes; there is no footer on desktop. |
| `utility.overlay-backdrop` | UTILITY | 2 | 11 | `src/engine/chunks/272.js > g (backdrop) + clip-path polygon builder` | Desktop breakpoint on the 11 overlay routes (about plus every project). |
| `utility.kinetic-cursor` | UTILITY | 2 | 11 | `src/engine/chunks/272.js > I (kinetic cursor)` | Desktop pointer devices on the 11 overlay routes (about plus every project). |
| `project.header` | PROJECT | 1 | 10 | `src/engine/chunks/272.js > N (project details, title + description)` | Project detail routes (10), desktop breakpoint. |
| `project.media-stage` | PROJECT | 1 | 10 | `src/engine/chunks/272.js > f (selected plane morph, fragment shader)` | Project detail routes (10), desktop breakpoint. |
| `project.meta` | PROJECT | 1 | 10 | `src/engine/chunks/272.js > N (Year/Tools block)` | Project detail routes (10), desktop breakpoint. |
| `project.footer-bar` | PROJECT | 1 | 10 | `src/engine/chunks/272.js > N (footer grid + media nav)` | Project detail routes (10), desktop breakpoint. |
| `project.mobile-header` | PROJECT | 1 | 10 | `src/engine/chunks/924.js > v (header)` | Project detail routes (10), mobile breakpoint. |
| `project.mobile-media` | PROJECT | 1 | 10 | `src/engine/chunks/924.js > v (media column)` | Project detail routes (10), mobile breakpoint. |
| `project.mobile-details` | PROJECT | 1 | 10 | `src/engine/chunks/924.js > v (details)` | Project detail routes (10), mobile breakpoint. |
| `intro.headline` | INTRO | 1 | 1 | `src/engine/chunks/272.js (desktop hero overlay ~L2400) + src/engine/chunks/924.js > b (mobile home)` | Homepage only (1 route), both breakpoints. |
| `intro.portrait-link` | INTRO | 1 | 1 | `src/engine/chunks/272.js > B (profile plane) + src/engine/chunks/924.js > b (mobile)` | Homepage only (1 route), both breakpoints. |
| `intro.statement` | INTRO | 1 | 1 | `src/engine/chunks/272.js (~L2527)` | Homepage only (1 route), desktop breakpoint only. |
| `utility.hover-title` | UTILITY | 1 | 1 | `src/engine/chunks/272.js > w (title overlay) + v (projection)` | Homepage only (1 route), desktop breakpoint only. |
| `work.grid` | WORK | 1 | 1 | `src/engine/chunks/924.js > g (mobile work grid)` | Homepage only (1 route), mobile breakpoint only. |
| `profile.header` | PROFILE | 1 | 1 | `src/engine/chunks/272.js (~L1900 profile items) + About overlay` | About route (1), desktop breakpoint. |
| `profile.media-stage` | PROFILE | 1 | 1 | `src/engine/chunks/272.js > B (profile plane, media list E)` | About route (1), desktop breakpoint. |
| `profile.discipline-list` | PROFILE | 1 | 1 | `src/engine/chunks/272.js (About menu)` | About route (1), desktop breakpoint. |
| `profile.footer-bar` | PROFILE | 1 | 1 | `src/engine/chunks/272.js (~L2217–2242)` | About route (1), desktop breakpoint. |
| `profile.mobile-intro` | PROFILE | 1 | 1 | `src/engine/chunks/924.js > j (intro section)` | About route (1), mobile breakpoint. |
| `profile.services-mobile` | PROFILE | 1 | 1 | `src/engine/chunks/924.js > j (services section, data m)` | About route (1), mobile breakpoint. |
| `error.digits-scene` | ERROR | 1 | 1 | `src/engine/chunks/notfound.js > module 9812` | Not-found route only (1). |
| `error.message` | ERROR | 1 | 1 | `src/components/NotFound.jsx` | Not-found route only (1). |

**8 shared sections** appear in more than one template and belong in a component library.

**20 single-use sections** appear in exactly one template. Building these
as "reusable" components up front would be speculative — keep them page-local
until a second caller actually appears.

## Templates

### Home (work index) — `template.home`

1 route · `/` · chrome: **full**

| # | category | section | |
|---:|---|---|---|
| 1 | UTILITY | `utility.preloader` | shared ×3 |
| 2 | UTILITY | `utility.page-transition` | shared ×4 |
| 3 | SHELL | `shell.navbar` | shared ×4 |
| 4 | INTRO | `intro.headline` | page-local |
| 5 | INTRO | `intro.portrait-link` | page-local |
| 6 | INTRO | `intro.statement` | page-local |
| 7 | WORK | `work.strip-webgl` | shared ×3 |
| 8 | UTILITY | `utility.hover-title` | page-local |
| 9 | WORK | `work.grid` | page-local |
| 10 | SHELL | `shell.footer-mobile` | shared ×3 |
| 11 | UTILITY | `utility.toast` | shared ×4 |

### About (profile overlay) — `template.about`

1 route · `/about` · chrome: **full**

| # | category | section | |
|---:|---|---|---|
| 1 | UTILITY | `utility.preloader` | shared ×3 |
| 2 | UTILITY | `utility.page-transition` | shared ×4 |
| 3 | SHELL | `shell.navbar` | shared ×4 |
| 4 | WORK | `work.strip-webgl` | shared ×3 |
| 5 | UTILITY | `utility.overlay-backdrop` | shared ×2 |
| 6 | PROFILE | `profile.header` | page-local |
| 7 | PROFILE | `profile.media-stage` | page-local |
| 8 | PROFILE | `profile.discipline-list` | page-local |
| 9 | PROFILE | `profile.footer-bar` | page-local |
| 10 | UTILITY | `utility.kinetic-cursor` | shared ×2 |
| 11 | PROFILE | `profile.mobile-intro` | page-local |
| 12 | PROFILE | `profile.services-mobile` | page-local |
| 13 | SHELL | `shell.footer-mobile` | shared ×3 |
| 14 | UTILITY | `utility.toast` | shared ×4 |

### Project detail (overlay) — `template.project-detail`

10 routes · `/project/{id}` · chrome: **full**

| # | category | section | |
|---:|---|---|---|
| 1 | UTILITY | `utility.preloader` | shared ×3 |
| 2 | UTILITY | `utility.page-transition` | shared ×4 |
| 3 | SHELL | `shell.navbar` | shared ×4 |
| 4 | WORK | `work.strip-webgl` | shared ×3 |
| 5 | UTILITY | `utility.overlay-backdrop` | shared ×2 |
| 6 | PROJECT | `project.header` | page-local |
| 7 | PROJECT | `project.media-stage` | page-local |
| 8 | PROJECT | `project.meta` | page-local |
| 9 | PROJECT | `project.footer-bar` | page-local |
| 10 | UTILITY | `utility.kinetic-cursor` | shared ×2 |
| 11 | PROJECT | `project.mobile-header` | page-local |
| 12 | PROJECT | `project.mobile-media` | page-local |
| 13 | PROJECT | `project.mobile-details` | page-local |
| 14 | SHELL | `shell.footer-mobile` | shared ×3 |
| 15 | UTILITY | `utility.toast` | shared ×4 |

### Not found (404) — `template.not-found`

1 route · `/* (any unmatched path)` · chrome: **nav-only**

| # | category | section | |
|---:|---|---|---|
| 1 | UTILITY | `utility.page-transition` | shared ×4 |
| 2 | SHELL | `shell.navbar` | shared ×4 |
| 3 | ERROR | `error.digits-scene` | page-local |
| 4 | ERROR | `error.message` | page-local |
| 5 | UTILITY | `utility.toast` | shared ×4 |

## Section reference

### SHELL

_Persistent site chrome: the fixed meta navigation and the mobile footer._

**`shell.navbar`** — Fixed top navigation. Desktop: five label/value columns (Name, occupation, Location, Connect with Copy Email / Instagram / LinkedIn, Profile with About me) with staggered fade-up entrance. Mobile: collapses to the name on the left and an 'About me' toggle on the right.

· Present on all 13 routes, both breakpoints. · appears on 13 routes · implemented by `src/engine/chunks/layout.js > module 5883 (Navbar)`

**`shell.footer-mobile`** — Mobile page footer listing Services (the five disciplines), Connect (Instagram, LinkedIn) and the design/development credit.

· Mobile breakpoint on the 12 portfolio routes; there is no footer on desktop. · appears on 12 routes · implemented by `src/engine/chunks/924.js > h (mobile footer)`

### UTILITY

_Runtime UI layered over the page (preloader, transitions, cursor, overlays, toasts); not content._

**`utility.preloader`** — Full-screen loading cover with the 'KERIMOV DESIGNS' wordmark revealed left-to-right by a clip-path tied to asset-loading progress, then slid up out of view.

· Shown once on first load of the 12 portfolio routes (home, about, project); not on the not-found route. · appears on 12 routes · implemented by `src/engine/chunks/924.js > module 4760 (Preloader)`

**`utility.page-transition`** — Route-change transition layer with its own WebGL canvas that covers the viewport while client-side navigation swaps the view.

· Mounted around every route by the root layout; active only during client-side navigation between the 12 portfolio routes. · appears on 13 routes · implemented by `src/engine/chunks/layout.js > module 7689 (ClientPageTransitionWrapper)`

**`utility.toast`** — Top-center toast host (light #ecebeb pill) available for transient confirmations.

· Mounted once in the root layout on all 13 routes. · appears on 13 routes · implemented by `src/App.jsx > Toaster (react-hot-toast)`

**`utility.hover-title`** — Uppercase project title that follows the hovered plane's projected corner with matching perspective tilt, drawn with mix-blend-difference.

· Homepage only (1 route), desktop breakpoint only. · appears on 1 routes · implemented by `src/engine/chunks/272.js > w (title overlay) + v (projection)`

**`utility.overlay-backdrop`** — Full-viewport dark (#0e0d0c at 97%) blurred backdrop that fades in behind an opened project or the About view, with a polygon cut-out tracking the active plane's bent outline.

· Desktop breakpoint on the 11 overlay routes (about plus every project). · appears on 11 routes · implemented by `src/engine/chunks/272.js > g (backdrop) + clip-path polygon builder`

**`utility.kinetic-cursor`** — Custom cursor label ('RETURN' / 'NEXT') that trails the pointer with velocity tilt and letter-spacing stretch, swapping to a small square over the media navigation; hides the native cursor.

· Desktop pointer devices on the 11 overlay routes (about plus every project). · appears on 11 routes · implemented by `src/engine/chunks/272.js > I (kinetic cursor)`

### INTRO

_The opening statement block of the homepage: headline, portrait entry point, invitation copy._

**`intro.headline`** — Three-line uppercase bold statement 'Graphic designer / crafting visual identities, / typography and motion.' with word-by-word blur-and-rise reveal.

· Homepage only (1 route), both breakpoints. · appears on 1 routes · implemented by `src/engine/chunks/272.js (desktop hero overlay ~L2400) + src/engine/chunks/924.js > b (mobile home)`

**`intro.portrait-link`** — Small 4:5 portrait of the designer at the top right that opens the About view. Desktop renders it as a WebGL plane; mobile as a linked image.

· Homepage only (1 route), both breakpoints. · appears on 1 routes · implemented by `src/engine/chunks/272.js > B (profile plane) + src/engine/chunks/924.js > b (mobile)`

**`intro.statement`** — Short invitation paragraph ('Take a look at my selected projects below…') pinned above the work strip at the right, revealed word by word.

· Homepage only (1 route), desktop breakpoint only. · appears on 1 routes · implemented by `src/engine/chunks/272.js (~L2527)`

### WORK

_The portfolio index of projects, as a WebGL strip (desktop) or an image grid (mobile)._

**`work.strip-webgl`** — Infinite horizontal strip of project cover planes along the bottom of the viewport, driven by wheel/drag with damped inertia; the hovered plane stays sharp while the others blur and darken, and clicking a plane morphs it into the project view.

· Desktop breakpoint on the 12 portfolio routes: interactive on home, and kept mounted (blurred behind the backdrop) under the about and project overlays. · appears on 12 routes · implemented by `src/engine/chunks/272.js > f (gallery planes, shaders)`

**`work.grid`** — 'Selected Work:' heading over a two-column grid of project cover images with uppercase titles, each linking to its project route.

· Homepage only (1 route), mobile breakpoint only. · appears on 1 routes · implemented by `src/engine/chunks/924.js > g (mobile work grid)`

### PROJECT

_Blocks of a single project's detail view: title, description, media, metadata, pagination._

**`project.header`** — Left-column project title (bold uppercase) and multi-paragraph description, revealed word by word.

· Project detail routes (10), desktop breakpoint. · appears on 10 routes · implemented by `src/engine/chunks/272.js > N (project details, title + description)`

**`project.media-stage`** — The selected cover plane enlarged to the center of the viewport; clicking or scrolling morphs through the project's images and finally its video with a noise-flow shader, then returns to the cover.

· Project detail routes (10), desktop breakpoint. · appears on 10 routes · implemented by `src/engine/chunks/272.js > f (selected plane morph, fragment shader)`

**`project.meta`** — Right-column 'Year:' and 'Tools:' label/value pairs.

· Project detail routes (10), desktop breakpoint. · appears on 10 routes · implemented by `src/engine/chunks/272.js > N (Year/Tools block)`

**`project.footer-bar`** — Bottom bar in three columns: 'Scroll or click to explore' hint, the project's tags joined with slashes, and numbered media pagination buttons.

· Project detail routes (10), desktop breakpoint. · appears on 10 routes · implemented by `src/engine/chunks/272.js > N (footer grid + media nav)`

**`project.mobile-header`** — Mobile article header with the project title revealed line by line.

· Project detail routes (10), mobile breakpoint. · appears on 10 routes · implemented by `src/engine/chunks/924.js > v (header)`

**`project.mobile-media`** — Stacked full-width project images with the project video (autoplaying, muted) inline.

· Project detail routes (10), mobile breakpoint. · appears on 10 routes · implemented by `src/engine/chunks/924.js > v (media column)`

**`project.mobile-details`** — 'About the project:' description plus 'Year:' and 'Tools:' pairs for the mobile article.

· Project detail routes (10), mobile breakpoint. · appears on 10 routes · implemented by `src/engine/chunks/924.js > v (details)`

### PROFILE

_Blocks of the About view: designer identity, disciplines/services and their media._

**`profile.header`** — Left-column heading and two short paragraphs; starts on 'RUSTAM KERIMOV' with the bio and switches to the active discipline's own title and copy as the media stage advances.

· About route (1), desktop breakpoint. · appears on 1 routes · implemented by `src/engine/chunks/272.js (~L1900 profile items) + About overlay`

**`profile.media-stage`** — The portrait plane enlarged to the center and morphed through one media item per discipline (portrait, four images and one video) on click/scroll.

· About route (1), desktop breakpoint. · appears on 1 routes · implemented by `src/engine/chunks/272.js > B (profile plane, media list E)`

**`profile.discipline-list`** — Right-aligned list of six entries (Profile, Visual Identities, Logo Design, Art Direction, Motion & Animation, Editorial Design) highlighting the active one and jumping the media stage on click.

· About route (1), desktop breakpoint. · appears on 1 routes · implemented by `src/engine/chunks/272.js (About menu)`

**`profile.footer-bar`** — Bottom-left meta line: 'Scroll or click to explore', location and age.

· About route (1), desktop breakpoint. · appears on 1 routes · implemented by `src/engine/chunks/272.js (~L2217–2242)`

**`profile.mobile-intro`** — Mobile About opener: large portrait (rk-about), 'Behind The Work.' heading, two bio paragraphs and the location/age line.

· About route (1), mobile breakpoint. · appears on 1 routes · implemented by `src/engine/chunks/924.js > j (intro section)`

**`profile.services-mobile`** — 'Services:' list of the five disciplines, each with a heading, its image or video, and a one-sentence description.

· About route (1), mobile breakpoint. · appears on 1 routes · implemented by `src/engine/chunks/924.js > j (services section, data m)`

### ERROR

_Not-found page content._

**`error.digits-scene`** — Full-viewport three.js scene where the digits 4-0-4 orbit and tumble, then snap into a row on a 6.5 s loop.

· Not-found route only (1). · appears on 1 routes · implemented by `src/engine/chunks/notfound.js > module 9812`

**`error.message`** — Bottom-left 'This page got lost.' heading, reassurance line, and a 'Back to portfolio' link with an animated arrow.

· Not-found route only (1). · appears on 1 routes · implemented by `src/components/NotFound.jsx`
