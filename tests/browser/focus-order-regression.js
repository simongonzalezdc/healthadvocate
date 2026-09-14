/* Focus-order regression battery — WCAG 2.1 SC 2.4.3 (Level A).
 *
 * Encodes the two findings from the 2026-09-13 machine a11y pass
 * (HA-MACHINE-A11Y-PASS-RESULT.md): SPA view switches and the coverage
 * form→panel re-render orphaned keyboard focus on document.body, leaving the
 * revealed content unannounced. Asserts document.activeElement lands INSIDE
 * the revealed content after:
 *   1. home entry-card activation via Enter
 *   2. home entry-card activation via Space
 *   3. coverage case creation via keyboard only (Tab to Create, Enter)
 *
 * Not part of the python CI (no node/playwright there). Run locally:
 *   env HEALTHADVOCATE_MODEL_ENABLED=0 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
 *     .venv/bin/uvicorn healthadvocate.app:app --host 127.0.0.1 --port 8080 &
 *   .venv/bin/python tests/browser/serve-coverage.py 8081 &
 *   NODE_PATH=/opt/homebrew/lib/node_modules \
 *     node tests/browser/focus-order-regression.js
 * Loopback only; synthetic data only. Exit 0 = every case passed.
 */
const { chromium } = require('playwright');

const BASE = process.env.FOCUS_BASE || 'http://127.0.0.1:8080';
const COV = process.env.FOCUS_COV || 'http://127.0.0.1:8081';
const settle = (p, ms = 450) => p.waitForTimeout(ms);
const results = [];

async function newCtx(browser) {
  const ctx = await browser.newContext();
  await ctx.route('**/*', route =>
    route.request().url().startsWith('http://127.0.0.1') ? route.continue() : route.abort());
  return ctx;
}

function focusState() {
  const el = document.activeElement;
  return {
    focus: el === document.body ? 'BODY' : el.tagName.toLowerCase() + (el.id ? '#' + el.id : ''),
    focusInView: !!(el.closest && el.closest('.view.active')),
  };
}

(async () => {
  const browser = await chromium.launch();

  for (const key of ['Enter', 'Space']) {
    const ctx = await newCtx(browser);
    const page = await ctx.newPage();
    await page.goto(BASE, { waitUntil: 'domcontentloaded' });
    await settle(page);
    await page.focus('.entry-card[data-goto="symptoms"]');
    await page.keyboard.press(key);
    await settle(page);
    const state = await page.evaluate(focusState);
    const detail = await page.evaluate(() => ({
      view: document.getElementById('view-symptoms').className,
      insideSymptoms: !!document.activeElement.closest('#view-symptoms'),
    }));
    Object.assign(detail, state);
    const ok = /active/.test(detail.view) && detail.focus !== 'BODY'
      && detail.focusInView && detail.insideSymptoms;
    results.push({ name: `entry-card ${key} activation`, ok, detail });
    await ctx.close();
  }

  {
    const ctx = await newCtx(browser);
    const page = await ctx.newPage();
    await page.goto(COV, { waitUntil: 'domcontentloaded' });
    await page.click('.nav-btn[data-view="coverage"]');
    await settle(page, 600);
    await page.focus('#coverage-title');
    await page.fill('#coverage-title', 'Synthetic focus-order regression case');
    await page.keyboard.press('Tab');
    const createFocused = await page.evaluate(() =>
      (document.activeElement.dataset && document.activeElement.dataset.action)
      || document.activeElement.tagName.toLowerCase());
    await page.keyboard.press('Enter');
    await page.waitForFunction(() =>
      /created \(synthetic only\)/i.test(document.getElementById('coverage-status').textContent),
      null, { timeout: 8000 });
    await settle(page);
    const state = await page.evaluate(focusState);
    const detail = await page.evaluate(() => ({
      status: document.getElementById('coverage-status').textContent.trim(),
      insidePanel: !!document.activeElement.closest('#coverage-panel')
        && !document.getElementById('coverage-panel').hidden,
    }));
    Object.assign(detail, state, { createFocused });
    const ok = createFocused === 'coverage-create' && detail.focus !== 'BODY'
      && detail.focusInView && detail.insidePanel;
    results.push({ name: 'coverage keyboard create', ok, detail });
    await ctx.close();
  }

  await browser.close();
  for (const r of results)
    console.log(`${r.ok ? 'PASS' : 'FAIL'}  ${r.name}  ${JSON.stringify(r.detail)}`);
  const failed = results.filter(r => !r.ok).length;
  console.log(failed ? `${failed}/${results.length} FAILED` : `${results.length}/${results.length} PASSED`);
  process.exit(failed ? 1 : 0);
})().catch(e => { for (const r of results) console.log(`${r.ok ? 'PASS' : 'FAIL'}  ${r.name}  ${JSON.stringify(r.detail)}`); console.error(e); process.exit(1); });
