/*
 * Frontend battery for feature wave F1 (D119, 2026-09-24).
 *
 * Same harness as tests/test_frontend_model_off_honesty.js: the REAL
 * healthadvocate/static/app.js loads in a node:vm sandbox with a stub DOM
 * (DOMContentLoaded never fires; init stays inert) and the real renderers
 * run against synthetic payloads. i18n is stubbed with the English catalog
 * keys the renderers consume, so assertions match shipped copy.
 *
 * Run: node tests/test_frontend_features_f1.js   (exit 0 = pass)
 */
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const STATIC = path.join(__dirname, '..', 'healthadvocate', 'static');

function loadHA() {
  const source = fs.readFileSync(path.join(STATIC, 'app.js'), 'utf8');
  const element = () => ({
    innerHTML: '',
    textContent: '',
    classList: { add() {}, remove() {}, toggle() {} },
    focus() {},
    querySelector() { return null; },
    addEventListener() {},
    setAttribute() {},
  });
  /* per-id element store: renderers that fetch their own container
     (renderLibrary) write into the same object the test holds */
  const els = {};
  const sandbox = {
    document: {
      addEventListener() {},
      getElementById(id) { return els[id] || (els[id] = element()); },
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
  sandbox.__els = els;
  const context = vm.createContext(sandbox);
  vm.runInContext(source + '\n;globalThis.HA = HA;', context, { filename: 'app.js' });
  return sandbox;
}

/* English catalog loaded from the shipped en.js (HA is lexical in that
 * file's scope too — same trick: evaluate and export). */
function loadEnCatalog() {
  const stub = {};
  const sandbox = {
    HA: { i18n: { register(code, cat) { stub[code] = cat; } } },
  };
  sandbox.globalThis = sandbox;
  const src = fs.readFileSync(path.join(STATIC, 'i18n', 'en.js'), 'utf8');
  vm.runInContext(src, vm.createContext(sandbox), { filename: 'en.js' });
  return stub.en || {};
}

const sandbox = loadHA();
const HA = sandbox.HA;
const en = loadEnCatalog();
HA.i18n = { t: (key) => en[key] || key };

let failures = 0;
function check(name, cond) {
  if (cond) console.log(`PASS ${name}`);
  else { failures += 1; console.error(`FAIL ${name}`); }
}
const fakeEl = () => ({ innerHTML: '' });

/* ── F1a: appeal letter render ─────────────────────────────────────────── */

const appealModelPayload = {
  letter: 'Subject: Formal appeal\n\nTo the Appeals Department:\n\nI am writing to appeal.',
  model_generated: true,
  needs_human: false,
  note: '',
  citations: [
    { fact: 'amount: $1,200.00', source: 'denial letter' },
    { fact: 'the user\'s own words', source: 'your words' },
  ],
};

{
  const el = fakeEl();
  HA.renderAppealLetter(appealModelPayload, el);
  const html = el.innerHTML;
  check('F1a model letter wears INFERRED',
    html.includes('prov-inferred') && /INFERRED/i.test(html));
  check('F1a letter is editable in place',
    html.includes('<textarea') && html.includes('appeal-letter-text'));
  check('F1a download + print actions present',
    html.includes('data-action="appeal-letter-download"')
      && html.includes('data-action="appeal-letter-print"'));
  check('F1a citations list traces to sources',
    html.includes('$1,200.00') && html.includes('denial letter'));
  check('F1a no needs-human banner when reason classified',
    !html.includes('appeal-needs-human'));
}

{
  const el = fakeEl();
  HA.renderAppealLetter(
    Object.assign({}, appealModelPayload, {
      model_generated: false,
      note: 'The optional local model is off, so this letter was assembled on this device from the facts you provided.',
      needs_human: true,
    }), el);
  const html = el.innerHTML;
  check('F1a model-off letter shows the assembled honesty note',
    /assembled on this device/.test(html));
  check('F1a unclassifiable reason raises needs-human banner',
    html.includes('appeal-needs-human') && /needs a human|could not be classified/i.test(html));
  check('F1a model-off letter is NOT labeled INFERRED model-drafted',
    !/INFERRED — model-drafted/.test(html));
}

{
  const el = fakeEl();
  HA.renderAppealLetter(
    Object.assign({}, appealModelPayload, {
      letter: '<script>alert(1)</script>\nSubject: Formal appeal',
    }), el);
  check('F1a hostile letter text escaped',
    !el.innerHTML.includes('<script>alert(1)') && el.innerHTML.includes('&lt;script&gt;'));
}

{
  const el = fakeEl();
  HA.renderBill({ explanation: 'line check', suspicious_charges: [], red_flags: [] }, el);
  check('F1a bill result carries the appeal-studio cross-link',
    el.innerHTML.includes('data-action="appeal-from-bill"'));
}

{
  HA._libFilter = 'all';
  HA._libQuery = '';
  HA.renderLibrary();
  const lib = sandbox.__els['lib-list'];
  check('F1a denial-tagged library items get the appeal chip',
    lib.innerHTML.includes('data-action="appeal-from-library"'));
  check('F1a non-denial library items do not',
    (lib.innerHTML.match(/appeal-from-library/g) || []).length
      === HA.CATALOG.filter(it => (it.tags || []).includes('denial')).length);
}

/* ── i18n frame ────────────────────────────────────────────────────────── */
{
  const esSrc = fs.readFileSync(path.join(STATIC, 'i18n', 'es.js'), 'utf8');
  const need = ['appeal.studio_head', 'appeal.generate', 'appeal.inferred_label',
    'appeal.assembled_note', 'appeal.needs_human_body', 'appeal.from_bill'];
  for (const key of need) check(`i18n es catalog carries ${key}`, esSrc.includes(`'${key}'`));
}

if (failures) {
  console.error(`\n${failures} check(s) FAILED`);
  process.exit(1);
}
console.log('\nall checks passed');
