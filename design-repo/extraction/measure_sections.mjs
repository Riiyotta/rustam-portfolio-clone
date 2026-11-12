#!/usr/bin/env node
/**
 * Re-measure section boxes (and a text-free colour/typography histogram) per template.
 *
 *   BASE_URL=http://localhost:5190 node extraction/measure_sections.mjs > out.json
 *
 * Environment (no machine paths live in this repo):
 *   BASE_URL                  site to measure (default http://localhost:5190, the clone's dev server)
 *   PLAYWRIGHT_CHROMIUM_PATH  optional Chromium/Chrome executable; otherwise Playwright's bundled browser
 *   VIEWPORTS                 optional, e.g. "1440x900,390x844" (default both)
 *   NODE_PATH                 must resolve the `playwright` package (global or local install)
 *
 * Output is geometry + computed-style histograms only: no copy, no screenshots.
 * WebGL needs a GPU or SwiftShader in headless mode, hence the launch args below.
 */
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';

const BASE = (process.env.BASE_URL || 'http://localhost:5190').replace(/\/$/, '');
const VIEWPORTS = (process.env.VIEWPORTS || '1440x900,390x844')
  .split(',')
  .map((s) => s.trim().split('x').map(Number));
const PROJECT_ROUTE = '/project/6aefb39eda2cd8ea85237d26'; // first project id in src/data/projects.json

// Finders (extraction/section-finders.json) run in the page and return the elements whose union box is the section.
const FINDERS = JSON.parse(readFileSync(new URL('./section-finders.json', import.meta.url), 'utf8')).finders;

const PAGES = [
  { template: 'home', route: '/', sections: ['shell.navbar', 'hero.intro', 'content.intro-note', 'portfolio.work-index', 'shell.footer-contact', 'utility.overlay-backdrop', 'utility.hover-title'] },
  { template: 'about', route: '/about', sections: ['shell.navbar', 'about.profile-header', 'about.media-stage', 'about.discipline-list', 'about.footer-meta', 'shell.footer-contact', 'utility.overlay-backdrop', 'utility.kinetic-cursor'] },
  { template: 'project-detail', route: PROJECT_ROUTE, sections: ['shell.navbar', 'project.header', 'project.media-stage', 'project.meta', 'project.footer-bar', 'shell.footer-contact', 'utility.overlay-backdrop', 'utility.kinetic-cursor'] },
  { template: 'not-found', route: '/this-route-does-not-exist', sections: ['shell.navbar', 'notfound.digits-scene', 'notfound.message'] },
];

async function settle(page) {
  await page.evaluate(() => document.fonts.ready);
  // preloader (fixed, z-index 9999) must be gone before measuring
  await page.waitForFunction(() => ![...document.querySelectorAll('div')].some((d) => getComputedStyle(d).zIndex === '9999' && d.getBoundingClientRect().height > 0), null, { timeout: 20000 }).catch(() => {});
  await page.waitForTimeout(2500);
}

const launch = { args: ['--use-gl=angle', '--enable-unsafe-swiftshader'] };
if (process.env.PLAYWRIGHT_CHROMIUM_PATH) launch.executablePath = process.env.PLAYWRIGHT_CHROMIUM_PATH;
const browser = await chromium.launch(launch);
const result = { tool: 'extraction/measure_sections.mjs', baseUrl: BASE, measuredAt: new Date().toISOString().slice(0, 10), viewports: {} };

for (const [w, h] of VIEWPORTS) {
  const key = `${w}x${h}`;
  result.viewports[key] = {};
  for (const pg of PAGES) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.goto(BASE + pg.route, { waitUntil: 'networkidle', timeout: 60000 });
    await settle(page);
    const data = await page.evaluate(({ finders, ids }) => {
      const sections = {};
      for (const id of ids) {
        let els = [];
        try { els = eval(finders[id]) || []; } catch (e) { els = []; }
        els = els.filter((e) => e && e.getBoundingClientRect().height > 0 && getComputedStyle(e).display !== 'none');
        if (!els.length) { sections[id] = { present: false }; continue; }
        const rs = els.map((e) => e.getBoundingClientRect());
        const top = Math.min(...rs.map((r) => r.top)) + window.scrollY, bottom = Math.max(...rs.map((r) => r.bottom)) + window.scrollY;
        const left = Math.min(...rs.map((r) => r.left)), right = Math.max(...rs.map((r) => r.right));
        // in-flow = no fixed/absolute ancestor up to <body>
        let inFlow = true;
        for (let n = els[0]; n && n !== document.body; n = n.parentElement) {
          const p = getComputedStyle(n).position; if (p === 'fixed' || p === 'absolute' || p === 'sticky') { inFlow = false; break; }
        }
        sections[id] = { present: true, x: Math.round(left), y: Math.round(top), width: Math.round(right - left), height: Math.round(bottom - top), position: getComputedStyle(els[0]).position, inFlow };
      }
      // text-free computed-style histogram of visible elements
      const color = {}, bg = {}, fam = {}, size = {}, weight = {};
      const bump = (o, k) => (o[k] = (o[k] || 0) + 1);
      for (const el of document.querySelectorAll('body *')) {
        const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
        const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || cs.display === 'none') continue;
        const hasText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
        if (hasText) { bump(color, cs.color); bump(fam, cs.fontFamily); bump(size, cs.fontSize); bump(weight, cs.fontWeight); }
        if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)') bump(bg, cs.backgroundColor);
      }
      return { sections, documentHeight: document.documentElement.scrollHeight, histogram: { textColor: color, background: bg, fontFamily: fam, fontSize: size, fontWeight: weight } };
    }, { finders: FINDERS, ids: pg.sections });
    result.viewports[key][pg.template] = { route: pg.route, ...data };
    await page.close();
  }
}
await browser.close();
process.stdout.write(JSON.stringify(result, null, 1) + '\n');
