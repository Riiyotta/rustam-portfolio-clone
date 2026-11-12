#!/usr/bin/env node
/**
 * Live-vs-clone parity harness (BASELINE R12).
 *
 *   OUT_DIR=<scratch dir outside the repo> RUN_LABEL=run1 \
 *     node extraction/parity/parity.mjs > extraction/parity/results-run1.json
 *
 * Environment (no machine paths in the repo):
 *   LIVE_URL   original site   (default https://www.kerimovdesigns.com)
 *   CLONE_URL  clone dev server (default http://localhost:5190)
 *   OUT_DIR    where PNG captures go; NEVER inside design-repo (captures carry the source's copy and imagery)
 *   PLAYWRIGHT_CHROMIUM_PATH  optional browser executable
 *
 * Determinism (applied identically on both sides):
 *   - HTMLMediaElement.play is replaced by a no-op that leaves every video paused on frame 0
 *     (this also freezes the WebGL video textures, which read from detached <video> elements);
 *   - captures wait for document fonts, for the fixed preloader to leave, then a fixed settle time;
 *   - interactions (wheel, hover, click) use the same coordinates and waits on both sides.
 * Scoring: a pixel mismatches when any RGB channel differs by more than THRESHOLD; a region's score is
 * 1 - mismatched/total. Section regions come from the clone's DOM via extraction/section-finders.json;
 * the per-section gate is 0.80 (verify_all.py re-checks it). Output is numbers only: no copy, no images.
 */
import { chromium } from 'playwright';
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { tmpdir } from 'node:os';

const LIVE = (process.env.LIVE_URL || 'https://www.kerimovdesigns.com').replace(/\/$/, '');
const CLONE = (process.env.CLONE_URL || 'http://localhost:5190').replace(/\/$/, '');
const OUT = resolve(process.env.OUT_DIR || join(tmpdir(), 'parity-captures'));
const REPO = resolve(new URL('../..', import.meta.url).pathname);
if (OUT.startsWith(REPO)) throw new Error('OUT_DIR must be outside design-repo (captures are not tracked)');
mkdirSync(OUT, { recursive: true });
const THRESHOLD = 24;
const GATE = 0.8;
const FINDERS = JSON.parse(readFileSync(new URL('../section-finders.json', import.meta.url), 'utf8')).finders;
const PROJECT = '/project/6aefb39eda2cd8ea85237d26';
// the gallery strip sits in the lower part of the 1440x900 stage (planes ~y 720-880), so hover/click target (1050, 800)

const D = { width: 1440, height: 900 };
const SCENARIOS = [
  { name: 'home', viewport: D, route: '/', sections: ['shell.navbar', 'hero.intro', 'content.intro-note', 'portfolio.work-index'] },
  { name: 'home-wheel', viewport: D, route: '/', act: async (p) => { await p.mouse.move(720, 450); await p.mouse.wheel(0, 700); }, settle: 3500, sections: ['shell.navbar', 'portfolio.work-index'] },
  { name: 'home-hover', viewport: D, route: '/', act: async (p) => { await p.mouse.move(1050, 800, { steps: 8 }); }, settle: 2500, sections: ['shell.navbar', 'portfolio.work-index'] },
  { name: 'open-project', viewport: D, route: '/', act: async (p) => { await p.mouse.move(1050, 800, { steps: 5 }); await p.waitForTimeout(800); await p.mouse.click(1050, 800); }, settle: 5000, sections: ['shell.navbar', 'project.header', 'project.media-stage', 'project.meta', 'project.footer-bar'] },
  { name: 'about-click', viewport: D, route: '/', act: async (p) => { await p.locator('nav[aria-label="Main navigation"] button').last().click(); }, settle: 5000, sections: ['shell.navbar', 'about.profile-header', 'about.media-stage', 'about.discipline-list', 'about.footer-meta'] },
  { name: 'about-direct', viewport: D, route: '/about', sections: ['shell.navbar', 'about.profile-header', 'about.media-stage', 'about.discipline-list', 'about.footer-meta'] },
  { name: 'project-deeplink', viewport: D, route: PROJECT, sections: ['shell.navbar', 'project.header', 'project.media-stage', 'project.meta', 'project.footer-bar'] },
  { name: 'project-media-next', viewport: D, route: PROJECT, act: async (p) => { await p.locator('nav[aria-label="Project media navigation"] button').nth(1).click(); }, settle: 3500, sections: ['shell.navbar', 'project.header', 'project.media-stage', 'project.meta', 'project.footer-bar'] },
  { name: 'tablet-1024-home', viewport: { width: 1024, height: 768 }, route: '/', sections: ['shell.navbar', 'hero.intro', 'content.intro-note', 'portfolio.work-index'] },
  { name: 'mobile-390-home', viewport: { width: 390, height: 844 }, route: '/', sections: ['shell.navbar', 'hero.intro', 'portfolio.work-index'] },
  { name: 'mobile-390-project', viewport: { width: 390, height: 844 }, route: PROJECT, sections: ['shell.navbar', 'project.header', 'project.media-stage'] },
  { name: 'not-found', viewport: D, route: '/this-route-does-not-exist', sections: ['shell.navbar', 'notfound.digits-scene', 'notfound.message'] },
];

const FREEZE = () => {
  const noop = function () { try { this.pause(); this.currentTime = 0; } catch (e) {} return Promise.resolve(); };
  Object.defineProperty(HTMLMediaElement.prototype, 'play', { value: noop, configurable: true, writable: true });
  Object.defineProperty(HTMLMediaElement.prototype, 'autoplay', { get: () => false, set: () => {}, configurable: true });
};

async function settle(page, ms) {
  await page.evaluate(() => document.fonts.ready);
  await page.waitForFunction(() => ![...document.querySelectorAll('div')].some((d) => getComputedStyle(d).zIndex === '9999' && d.getBoundingClientRect().height > 0), null, { timeout: 20000 }).catch(() => {});
  await page.waitForTimeout(ms);
}

async function capture(browser, base, sc) {
  const ctx = await browser.newContext({ viewport: sc.viewport, deviceScaleFactor: 1, reducedMotion: 'no-preference' });
  await ctx.addInitScript(FREEZE);
  const page = await ctx.newPage();
  await page.goto(base + sc.route, { waitUntil: 'networkidle', timeout: 60000 });
  await settle(page, 3000);
  if (sc.act) { await sc.act(page); await page.waitForTimeout(sc.settle || 3000); }
  const png = await page.screenshot({ type: 'png' });
  const boxes = await page.evaluate(({ finders, ids }) => {
    const out = {};
    for (const id of ids) {
      let els = []; try { els = eval(finders[id]) || []; } catch (e) {}
      els = els.filter((e) => e && e.getBoundingClientRect().height > 0);
      if (!els.length) { out[id] = null; continue; }
      const rs = els.map((e) => e.getBoundingClientRect());
      const x = Math.max(0, Math.min(...rs.map((r) => r.left))), y = Math.max(0, Math.min(...rs.map((r) => r.top)));
      const r = Math.min(innerWidth, Math.max(...rs.map((r) => r.right))), b = Math.min(innerHeight, Math.max(...rs.map((r) => r.bottom)));
      out[id] = r > x && b > y ? { x: Math.round(x), y: Math.round(y), w: Math.round(r - x), h: Math.round(b - y) } : null;
    }
    return out;
  }, { finders: FINDERS, ids: sc.sections });
  await ctx.close();
  return { png, boxes };
}

async function diff(browser, a, b, regions, vp) {
  const page = await browser.newPage();
  const res = await page.evaluate(async ({ a, b, regions, vp, T }) => {
    const load = (s) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.src = 'data:image/png;base64,' + s; });
    const [ia, ib] = await Promise.all([load(a), load(b)]);
    const data = (img) => { const c = document.createElement('canvas'); c.width = vp.width; c.height = vp.height; const x = c.getContext('2d'); x.drawImage(img, 0, 0); return x.getImageData(0, 0, vp.width, vp.height).data; };
    const da = data(ia), db = data(ib);
    const score = (r) => {
      let bad = 0, n = 0;
      for (let y = r.y; y < r.y + r.h; y++) for (let x = r.x; x < r.x + r.w; x++) {
        const k = (y * vp.width + x) * 4; n++;
        if (Math.abs(da[k] - db[k]) > T || Math.abs(da[k + 1] - db[k + 1]) > T || Math.abs(da[k + 2] - db[k + 2]) > T) bad++;
      }
      return n ? 1 - bad / n : null;
    };
    const out = { full: score({ x: 0, y: 0, w: vp.width, h: vp.height }), sections: {} };
    for (const [id, r] of Object.entries(regions)) out.sections[id] = r ? { box: r, score: score(r) } : { box: null, score: null };
    return out;
  }, { a: a.toString('base64'), b: b.toString('base64'), regions, vp, T: THRESHOLD });
  await page.close();
  return res;
}

const launch = { args: ['--use-gl=angle', '--enable-unsafe-swiftshader'] };
if (process.env.PLAYWRIGHT_CHROMIUM_PATH) launch.executablePath = process.env.PLAYWRIGHT_CHROMIUM_PATH;
const browser = await chromium.launch(launch);
const label = process.env.RUN_LABEL || 'run';
const results = { tool: 'extraction/parity/parity.mjs', run: label, date: new Date().toISOString().slice(0, 10), liveUrl: LIVE, cloneUrl: 'local clone dev server', thresholdPerChannel: THRESHOLD, sectionGate: GATE, captureState: 'videos frozen on frame 0 both sides; preloader gone; fonts ready; fixed settle; no consent banner exists on the live site', scenarios: {} };
for (const sc of SCENARIOS) {
  const live = await capture(browser, LIVE, sc);
  const clone = await capture(browser, CLONE, sc);
  writeFileSync(join(OUT, `${label}-${sc.name}-live.png`), live.png);
  writeFileSync(join(OUT, `${label}-${sc.name}-clone.png`), clone.png);
  const d = await diff(browser, live.png, clone.png, clone.boxes, sc.viewport);
  const scores = Object.values(d.sections).map((s) => s.score).filter((s) => s !== null);
  results.scenarios[sc.name] = {
    viewport: `${sc.viewport.width}x${sc.viewport.height}`,
    route: sc.route.startsWith('/project/') ? '/project/:id' : sc.route,
    fullViewportScore: +d.full.toFixed(5),
    fullViewportMismatchPct: +((1 - d.full) * 100).toFixed(3),
    sectionAverage: scores.length ? +(scores.reduce((x, y) => x + y, 0) / scores.length).toFixed(5) : null,
    sections: Object.fromEntries(Object.entries(d.sections).map(([k, v]) => [k, { box: v.box, score: v.score === null ? null : +v.score.toFixed(5), passesGate: v.score === null ? null : v.score >= GATE }])),
  };
  process.stderr.write(`${sc.name}: full ${(d.full * 100).toFixed(2)}%\n`);
}
await browser.close();
const all = Object.values(results.scenarios).flatMap((s) => Object.values(s.sections).map((x) => x.score)).filter((x) => x !== null);
results.summary = { scenarios: Object.keys(results.scenarios).length, sectionScores: all.length, minSectionScore: Math.min(...all), averageSectionScore: +(all.reduce((a, b) => a + b, 0) / all.length).toFixed(5), allSectionsPassGate: all.every((x) => x >= GATE) };
process.stdout.write(JSON.stringify(results, null, 1) + '\n');
