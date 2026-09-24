/* Honesty matrix (lane B — glass honesty, audits E1/E2/D5/D3/B3,
 * 2026-09-24). Browser-level proof that the safety truth reaches the
 * person's screen.
 *
 * Boots its OWN loopback app from THIS checkout on an ephemeral port
 * (model off: HEALTHADVOCATE_MODEL_ENABLED=0, HF/transformers offline),
 * never touches the long-running :8080 instance, and tears the server
 * down on exit. Chromium only. Synthetic inputs only.
 *
 * Run:
 *   PLAYWRIGHT_BROWSERS_PATH=$HOME/workspaces/.cache/playwright \
 *   NODE_PATH=/opt/homebrew/lib/node_modules \
 *   node tools/browserframe/honesty_matrix.mjs
 *
 * Checks:
 *   H0 Help view carries the two named US crisis lines + link-only resources
 *   H1 fallback-shaped symptoms response renders the NEEDS_HUMAN banner
 *      (allowed next steps + named humans)
 *   H4 model-off MILD input never surfaces a HIGH urgency verdict,
 *      end-to-end (API payload + rendered view) — the no-judgment case
 *   H3 no "verified"/"confirmed" claims in rendered home/symptoms views;
 *      old badge strings ("Validation", "Reliability") absent
 *   H2 urgency "unavailable" renders as an honest model-unavailable state
 *      with NO high-urgency styling (synthetic payload injected, so the
 *      check passes whichever order the backend value lands in)
 *   H5 a NEEDS_HUMAN wrapper without a usable allowed_next_steps key
 *      still renders the banner + named humans (no silent disappearance)
 *   H6 missing/null/unknown urgency never renders a MEDIUM badge —
 *      absence is not a verdict
 *
 * Results JSON + screenshots: /tmp/ha-honesty-matrix/
 */

process.env.PLAYWRIGHT_BROWSERS_PATH ||= '/Users/simongonzalezdecruz/workspaces/.cache/playwright';

import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import net from 'node:net';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url); // ESM ignores NODE_PATH; require honors it
const { chromium } = require('playwright');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
/* Interpreter carrying the pinned app deps (the same venv the loopback
 * app runs on). The `healthadvocate` package itself resolves to THIS
 * checkout via cwd, not to the venv's worktree. */
const PY = '/Users/simongonzalezdecruz/workspaces/.worktrees/healthadvocate-pm-verify-20260917/.venv/bin/python';
const OUT = '/tmp/ha-honesty-matrix';
fs.mkdirSync(OUT, { recursive: true });

const results = [];
function row(id, intent, pass, evidence) {
  results.push({ id, intent, result: pass ? 'pass' : 'fail', evidence });
  console.log(`[${pass ? 'PASS' : 'FAIL'}] ${id} — ${evidence.slice(0, 200)}`);
  fs.writeFileSync(path.join(OUT, 'results.json'), JSON.stringify(results, null, 2));
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

function freePort() {
  return new Promise((resolve, reject) => {
    const probe = net.createServer();
    probe.listen(0, '127.0.0.1', () => {
      const { port } = probe.address();
      probe.close(() => resolve(port));
    });
    probe.on('error', reject);
  });
}

async function waitHealthy(base, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const r = await fetch(`${base}/api/health`);
      if (r.ok) return true;
    } catch { /* not up yet */ }
    await sleep(1000);
  }
  return false;
}

/* Synthetic, shape-faithful symptoms payload with urgency "unavailable"
 * (lane A value) AND the NEEDS_HUMAN wrapper — exercises both landing
 * orders without depending on the backend change having landed. */
const UNAVAILABLE_PAYLOAD = {
  conditions: [],
  urgency: 'unavailable',
  explanation: 'Synthetic probe payload: the model is unavailable.',
  action_items: [],
  red_flags: [],
  possible_conditions: [],
  structured_output: { _model_blocked: true, _block_reason: 'probe' },
  validation: {
    confirmed: [], ner_only: [], llm_only: [],
    reliability: 'high', urgency_disagreement: false,
  },
  pii_scrubbed: false,
  pii_found_and_masked: false,
  urgency_decision: {
    outcome: 'NEEDS_HUMAN',
    reason_kind: 'below-threshold',
    question_id: 'symptom-triage-urgency',
    question_class: 'score',
    runner: 'code',
    answer: null,
    threshold_applied: 0.5,
    reason: 'Synthetic probe: placeholder candidate.',
    allowed_next_steps: [
      'Review the attached calibrated numbers',
      'Make the decision as a human',
    ],
    validation_errors: [],
    gate_state: 'REVIEW_REQUIRED',
  },
};

/* Launch chromium from the shared browser cache. The cached build can
 * drift from the playwright package's pinned revision (no installs are
 * allowed here), so fall back to the cached executables explicitly. */
async function launchChromium() {
  const cache = process.env.PLAYWRIGHT_BROWSERS_PATH;
  const candidates = [];
  if (cache) {
    candidates.push(
      `${cache}/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell`,
      `${cache}/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`,
    );
  }
  for (const executablePath of [null, ...candidates.filter(p => fs.existsSync(p))]) {
    try {
      return await chromium.launch(executablePath ? { executablePath } : undefined);
    } catch (e) {
      console.log(`launch attempt failed (${executablePath || 'default'}): ${String(e).split('\n')[0].slice(0, 120)}`);
    }
  }
  throw new Error('no launchable chromium found in the browser cache');
}

async function main() {
  const port = await freePort();
  const base = `http://127.0.0.1:${port}`;

  const server = spawn(
    PY,
    ['-m', 'uvicorn', 'healthadvocate.app:app', '--host', '127.0.0.1', '--port', String(port)],
    {
      cwd: ROOT,
      env: {
        ...process.env,
        HEALTHADVOCATE_MODEL_ENABLED: '0',
        HF_HUB_OFFLINE: '1',
        TRANSFORMERS_OFFLINE: '1',
      },
      stdio: ['ignore', 'pipe', 'pipe'],
    },
  );
  const logChunks = [];
  server.stdout.on('data', d => logChunks.push(d));
  server.stderr.on('data', d => logChunks.push(d));
  const shutdown = (signal = 'SIGTERM') => {
    try { server.kill(signal); } catch { /* already gone */ }
  };
  process.on('SIGINT', () => { shutdown(); process.exit(130); });
  process.on('exit', () => {
    fs.writeFileSync(path.join(OUT, 'server.log'), Buffer.concat(logChunks));
    try { server.kill('SIGKILL'); } catch { /* already gone */ }
  });

  let browser = null;
  try {
    if (!(await waitHealthy(base, 180_000))) {
      row('H-server-boot', 'loopback app boots model-off on an ephemeral port', false,
        `no /api/health on ${base} within 180s — see ${OUT}/server.log`);
      process.exit(1);
    }
    row('H-server-boot', 'loopback app boots model-off on an ephemeral port', true, `healthy on ${base} (pid ${server.pid})`);

    browser = await launchChromium();
    const page = await (await browser.newContext()).newPage();
    const pageErrors = [];
    page.on('pageerror', e => pageErrors.push(String(e).slice(0, 120)));

    /* H0 — Help view: exactly the two named US crisis lines + links. */
    await page.goto(base + '/', { waitUntil: 'domcontentloaded', timeout: 30_000 });
    await page.click('.nav-btn[data-view="help"]');
    const helpText = (await page.textContent('#view-help')) || '';
    const helpHrefs = await page.$$eval('#view-help a[href]', els => els.map(a => a.href));
    const h0 = /988 Suicide & Crisis Lifeline/.test(helpText)
      && /call or text 988/.test(helpText)
      && /1-800-985-5990/.test(helpText)
      && helpHrefs.some(h => h.startsWith('https://localhelp.healthcare.gov'))
      && helpHrefs.some(h => /^https:\/\/(www\.)?naic\.org/.test(h))
      && /Patient Advocate \/ Patient Relations/.test(helpText);
    row('H0-help-named-humans',
      'Help view shows the two named US crisis lines + link-only resources + patient-advocate line',
      h0,
      h0 ? '988 + 1-800-985-5990 + localhelp.healthcare.gov + naic.org + Patient Advocate line all present'
        : `missing content in #view-help (hrefs=[${helpHrefs.join(', ')}]): "${helpText.replace(/\s+/g, ' ').slice(0, 160)}"`);
    await page.screenshot({ path: `${OUT}/help-view.png` });

    /* H1 — real round-trip, model off: the fallback-shaped symptoms
     * response must render the NEEDS_HUMAN banner. */
    await page.click('.nav-btn[data-view="symptoms"]');
    const respPromise = page.waitForResponse(r => r.url().includes('/api/symptoms/assess'));
    await page.fill('#symptom-input', 'Synthetic probe input: sudden chest pain and shortness of breath for the past hour.');
    await page.click('[data-action="assess-symptoms"]');
    const resp = await respPromise;
    const payload = await resp.json();
    await page.waitForSelector('#symptom-results [data-testid="needs-human-banner"]', { timeout: 20_000 });
    const bannerText = (await page.textContent('[data-testid="needs-human-banner"]')) || '';
    const decision = payload.urgency_decision || {};
    const fallbackShaped = payload.structured_output?._model_blocked === true
      || decision.outcome === 'NEEDS_HUMAN';
    const stepsRendered = Array.isArray(decision.allowed_next_steps)
      && decision.allowed_next_steps.filter(s => bannerText.includes(s)).length;
    const humansNamed = /988/.test(bannerText) && /1-800-985-5990/.test(bannerText);
    const h1 = fallbackShaped
      && /This needs a human decision/.test(bannerText)
      && stepsRendered >= 1
      && humansNamed;
    row('H1-needs-human-banner',
      'fallback-shaped symptoms response renders the NEEDS_HUMAN banner with steps + named humans',
      h1,
      `outcome=${decision.outcome} reason_kind=${decision.reason_kind} _model_blocked=${payload.structured_output?._model_blocked} `
      + `steps_rendered=${stepsRendered}/${(decision.allowed_next_steps || []).length} humans_named=${humansNamed}`);
    await page.screenshot({ path: `${OUT}/symptoms-fallback.png` });

    /* H4 — model-off MILD input must NEVER surface a HIGH verdict,
     * end-to-end: real server, real round-trip, no interception.
     * (Verified finding: payload urgency "high" + red HIGH badge next
     * to the banner was the exact dishonesty.) */
    const mildRespPromise = page.waitForResponse(r => r.url().includes('/api/symptoms/assess'));
    await page.fill('#symptom-input', 'Synthetic probe input: I have had a mild headache and slight tiredness for a day. No fever, no other symptoms.');
    await page.click('[data-action="assess-symptoms"]');
    const mildResp = await mildRespPromise;
    const mildPayload = await mildResp.json();
    await page.waitForSelector('#symptom-results [data-testid="needs-human-banner"]', { timeout: 20_000 });
    const mildBadges = await page.locator('#symptom-results .urgency-badge').count();
    const mildHighs = await page.locator('#symptom-results .urgency-high').count();
    const mildUnavailable = await page.locator('#symptom-results [data-testid="urgency-unavailable"]').count();
    const h4 = mildPayload.urgency !== 'high' && mildBadges === 0 && mildHighs === 0
      && mildUnavailable >= 1 && mildPayload.structured_output?._model_blocked === true;
    row('H4-model-off-mild-never-high',
      'model-off mild input surfaces no HIGH verdict at API or glass level (no-judgment honesty)',
      h4,
      `payloadUrgency=${JSON.stringify(mildPayload.urgency)} badges=${mildBadges} highs=${mildHighs} `
      + `unavailableNotices=${mildUnavailable} _model_blocked=${mildPayload.structured_output?._model_blocked}`);
    await page.screenshot({ path: `${OUT}/symptoms-mild-model-off.png` });

    /* H3 — no "verified"/"confirmed" claims in rendered home/symptoms.
     * Run on the live-rendered symptoms view (post H1) + home view. */
    await page.click('#btn-home');
    const claims = await page.evaluate(() => {
      const out = {};
      for (const id of ['view-home', 'view-symptoms']) {
        out[id] = (document.getElementById(id)?.textContent || '').replace(/\s+/g, ' ');
      }
      return out;
    });
    const bad = [];
    for (const [id, text] of Object.entries(claims)) {
      for (const re of [/verif/i, /confirm/i, /Validation/, /Reliability/]) {
        const m = text.match(re);
        if (m) bad.push(`${id}: "${m[0]}"`);
      }
    }
    row('H3-no-verified-claims',
      'rendered home/symptoms views claim no "verified"/"confirmed"; old badge strings absent',
      bad.length === 0 && pageErrors.length === 0,
      bad.length === 0
        ? `clean (${Object.keys(claims).join(', ')} scanned; pageerrors=${pageErrors.length})`
        : `claim strings found: ${bad.join('; ')}`);

    /* H2 — urgency "unavailable" (synthetic payload injected at the
     * network layer): honest state, no badge, no high styling. */
    const page2 = await (await browser.newContext()).newPage();
    await page2.route('**/api/symptoms/assess', route => route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(UNAVAILABLE_PAYLOAD),
    }));
    await page2.goto(base + '/', { waitUntil: 'domcontentloaded', timeout: 30_000 });
    await page2.click('.nav-btn[data-view="symptoms"]');
    await page2.fill('#symptom-input', 'Synthetic probe input: anything at all.');
    await page2.click('[data-action="assess-symptoms"]');
    await page2.waitForSelector('#symptom-results [data-testid="urgency-unavailable"]', { timeout: 20_000 });
    const badges = await page2.locator('#symptom-results .urgency-badge').count();
    const highs = await page2.locator('#symptom-results .urgency-high').count();
    const banners = await page2.locator('#symptom-results [data-testid="needs-human-banner"]').count();
    const unavailText = (await page2.textContent('[data-testid="urgency-unavailable"]')) || '';
    const unavailClass = await page2.getAttribute('[data-testid="urgency-unavailable"]', 'class');
    const color = await page2.locator('[data-testid="urgency-unavailable"]')
      .evaluate(el => getComputedStyle(el).color);
    const h2 = badges === 0 && highs === 0 && banners === 1
      && /Model unavailable/i.test(unavailText)
      && /flag-info/.test(unavailClass || '');
    row('H2-urgency-unavailable',
      'urgency "unavailable" renders as honest model-unavailable state with no high-urgency styling',
      h2,
      `badges=${badges} highs=${highs} banners=${banners} class="${unavailClass}" color=${color} text="${unavailText.trim().slice(0, 60)}"`);
    await page2.screenshot({ path: `${OUT}/symptoms-unavailable.png` });
    await page2.close();

    /* H5 + H6 — drift-hole defenses on synthetic payloads (network-layer
     * injection; the live backend always attaches array steps, these pin
     * the glass against drift). */
    const renderSynthetic = async (label, mutate) => {
      const payload = JSON.parse(JSON.stringify(UNAVAILABLE_PAYLOAD));
      payload.urgency = 'medium';
      mutate(payload);
      const ctx = await browser.newContext();
      const p = await ctx.newPage();
      await p.route('**/api/symptoms/assess', route => route.fulfill({
        status: 200, contentType: 'application/json', body: JSON.stringify(payload),
      }));
      await p.goto(base + '/', { waitUntil: 'domcontentloaded', timeout: 30_000 });
      await p.click('.nav-btn[data-view="symptoms"]');
      await p.fill('#symptom-input', 'Synthetic probe input: anything at all.');
      await p.click('[data-action="assess-symptoms"]');
      await p.waitForSelector('#symptom-results', { timeout: 20_000 });
      await p.waitForTimeout(150);
      const out = {
        banners: await p.locator('#symptom-results [data-testid="needs-human-banner"]').count(),
        humans988: await p.locator('#symptom-results .needs-human-banner').textContent().then(t => /988/.test(t || '')).catch(() => false),
        badges: await p.locator('#symptom-results .urgency-badge').count(),
        mediums: await p.locator('#symptom-results .urgency-medium').count(),
        noVerdict: await p.locator('#symptom-results [data-testid="urgency-unavailable"]').count(),
        text: (await p.textContent('#symptom-results')) || '',
      };
      await ctx.close();
      return out;
    };

    // H5a: steps key absent entirely.
    const h5a = await renderSynthetic('no-steps-key', p => { delete p.urgency_decision.allowed_next_steps; });
    row('H5a-banner-without-steps-key',
      'NEEDS_HUMAN wrapper with NO allowed_next_steps key still renders banner + named humans',
      h5a.banners === 1 && h5a.humans988,
      `banners=${h5a.banners} humans_named=${h5a.humans988} stepsCopy=${/no allowed next steps were attached/.test(h5a.text)}`);

    // H5b: steps as a plain string.
    const h5b = await renderSynthetic('string-steps', p => { p.urgency_decision.allowed_next_steps = 'Decide as a human'; });
    row('H5b-banner-with-string-steps',
      'NEEDS_HUMAN wrapper with string allowed_next_steps renders banner + the step',
      h5b.banners === 1 && h5b.humans988 && /Decide as a human/.test(h5b.text),
      `banners=${h5b.banners} humans_named=${h5b.humans988} stepRendered=${/Decide as a human/.test(h5b.text)}`);

    // H6: urgency absent / null / unknown string next to a NEEDS_HUMAN
    // wrapper — never a confident MEDIUM badge.
    for (const [label, mutate] of [
      ['missing-urgency', p => { delete p.urgency; }],
      ['null-urgency', p => { p.urgency = null; }],
      ['unknown-string-urgency', p => { p.urgency = 'whenever'; }],
    ]) {
      const out = await renderSynthetic(label, mutate);
      row(`H6-${label}-never-medium`,
        `absent/unknown urgency (${label}) renders no verdict, never a MEDIUM badge`,
        out.badges === 0 && out.mediums === 0 && out.noVerdict >= 1 && out.banners === 1,
        `badges=${out.badges} mediums=${out.mediums} noVerdictNotices=${out.noVerdict} banners=${out.banners}`);
    }
  } finally {
    try { await browser?.close(); } catch { /* already closed */ }
    shutdown();
    await sleep(1500);
    try { server.kill('SIGKILL'); } catch { /* already gone */ }
  }

  const failed = results.filter(r => r.result === 'fail').length;
  console.log(`\nHONESTY MATRIX: ${results.length} rows, ${failed} failed — results: ${OUT}/results.json`);
  process.exit(failed ? 1 : 0);
}

main().catch(err => {
  console.error('probe crashed:', err);
  process.exit(1);
});
