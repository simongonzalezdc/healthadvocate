/*
 * Frontend model-off honesty + escaping pins (Lane C fix, 2026-09-24
 * findings 2/3 + the two XSS findings).
 *
 * Loads the REAL healthadvocate/static/app.js in a node:vm sandbox with a
 * stub DOM (DOMContentLoaded never fires, so the init block stays inert)
 * and drives the real renderers with synthetic payloads.
 *
 * Run: node tests/test_frontend_model_off_honesty.js   (exit 0 = pass)
 */

'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const APP_JS = path.join(__dirname, '..', 'healthadvocate', 'static', 'app.js');

function loadHA() {
  const source = fs.readFileSync(APP_JS, 'utf8');
  const element = () => ({
    innerHTML: '',
    textContent: '',
    classList: { add() {}, remove() {}, toggle() {} },
    focus() {},
    querySelector() { return null; },
    addEventListener() {},
    setAttribute() {},
  });
  const sandbox = {
    document: {
      addEventListener() {},           // DOMContentLoaded never fires
      getElementById() { return element(); },
      querySelectorAll() { return []; },
      createElement() { return element(); },
      documentElement: element(),
      body: element(),
    },
    window: { addEventListener() {} },
    fetch: () => Promise.reject(new Error('no network in test')),
    console,
    setTimeout, clearTimeout, setInterval, clearInterval,
  };
  sandbox.globalThis = sandbox;
  const context = vm.createContext(sandbox);
  // Same-script scope: expose the top-level `const HA` to the sandbox.
  vm.runInContext(source + '\n;globalThis.HA = HA;', context, {
    filename: 'app.js',
  });
  return sandbox.HA;
}

function fakeEl() {
  const el = { innerHTML: '' };
  return el;
}

let failures = 0;
function check(name, cond) {
  if (cond) {
    console.log(`PASS ${name}`);
  } else {
    failures += 1;
    console.error(`FAIL ${name}`);
  }
}

const HA = loadHA();

/* ── Finding 2: safeUrgency must pass the honest state through ── */
check("safeUrgency('unavailable') === 'unavailable'",
  HA.safeUrgency('unavailable') === 'unavailable');
check("safeUrgency still whitelists low/medium/high",
  HA.safeUrgency('high') === 'high' && HA.safeUrgency('low') === 'low');

/* ── Findings 2+3: model-off symptom render ── */
const modelOffPayload = {
  urgency: 'unavailable',
  explanation:
    'The optional local model is unavailable or blocked by the privacy boundary. '
    + 'Deterministic preparation steps remain available.',
  conditions: [{ name: 'headache', confidence: 0.95, label: 'DISEASE' }],
  action_items: [
    'Continue with the manual Coverage workflow or local checklists.',
    'Enable a loopback-only model runtime only if you need generative drafts.',
  ],
  red_flags: [],
  validation: { reliability: 'high', urgency_disagreement: false },
  urgency_decision: {
    outcome: 'NEEDS_HUMAN',
    reason_kind: 'invalid-answer',
    reason: 'Calibrated confidence is below the measured threshold for this '
      + 'question class; the numbers are attached for a human decision.',
    gate_state: 'review_required',
    allowed_next_steps: [
      'Review the attached calibrated numbers',
      'Make the decision as a human',
      'Record the human decision against this question id',
    ],
  },
};

{
  const el = fakeEl();
  HA.renderSymptoms(modelOffPayload, el);
  const html = el.innerHTML;
  check('model-off badge is the neutral UNAVAILABLE state',
    html.includes('urgency-unavailable') && html.includes('UNAVAILABLE'));
  check('model-off badge is NOT the coral alarm',
    !html.includes('urgency-high'));
  check('NEEDS_HUMAN banner rendered', html.includes('NEEDS_HUMAN'));
  check('wrapper reason rendered',
    html.includes('below the measured threshold'));
  check('gate state rendered', html.includes('review_required'));
  check('all allowed_next_steps rendered',
    modelOffPayload.urgency_decision.allowed_next_steps
      .every((s) => html.includes(s)));
  check('emergency guidance rendered with the unavailable state',
    /emergency/i.test(html));
}

/* Real emergency styling must be untouched for a genuine 'high'. */
{
  const el = fakeEl();
  HA.renderSymptoms(
    Object.assign({}, modelOffPayload, { urgency: 'high' }), el);
  check("genuine 'high' keeps the alarm badge",
    el.innerHTML.includes('urgency-high') && el.innerHTML.includes('HIGH'));
}

/* ── XSS finding: renderCommunity credibility must be escaped ── */
{
  const el = fakeEl();
  HA.renderCommunity({
    urgency: 'low',
    explanation: 'benign',
    credibility: '<IMG SRC=X ONERROR=ALERT(1)>',
  }, el);
  const html = el.innerHTML;
  check('hostile credibility escaped (no live markup)',
    !/<img[^>]*src=["']?x/i.test(html) && html.includes('&lt;IMG'));
}

/* ── XSS finding: track dashboard counters must be escaped ── */
{
  const el = fakeEl();
  HA.renderTrackDashboard({
    active: '<b>1</b>',
    monitoring: '<img src=y>',
    resolved: '0',
    tracks: [{ id: 't-1', concern: 'sleep', category: 'general', status: 'active' }],
  }, el);
  const html = el.innerHTML;
  check('hostile track counters escaped',
    !/<b>1<\/b>/.test(html) && !/<img[^>]*src=["']?y/i.test(html)
      && html.includes('&lt;b&gt;1&lt;/b&gt;'));
}

if (failures) {
  console.error(`\n${failures} check(s) FAILED`);
  process.exit(1);
}
console.log('\nall checks passed');
