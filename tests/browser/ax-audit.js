/* Machine announcement-equivalent AX audit for HealthAdvocate — repo-owned.
 * Per checked journey (home, symptoms, coverage): capture the Chromium full
 * accessibility tree (the tree exposed to assistive tech) per step and audit:
 *  - 4.1.2 name/role/value on every interactive AX node; visible focusables
 *    missing from the AX tree; value/state on value-bearing controls
 *  - 2.4.3 focus order vs DOM order (forward+backward combined coverage),
 *    traps, focus position after SPA view switches
 *  - 4.1.3 live-region exposure + dynamic announcement text in the AX subtree
 *  - 2.4.7 :focus-visible + author indicator on every walked element
 *  - 1.3.1 landmarks + heading outline (DOM-ordered, visible-only)
 *  - 2.4.1 skip-link bypass; 2.4.2 title; 3.1.1 lang
 *
 * NOT covered: the human listening pass (actual VoiceOver speech, rotor
 * behaviour, comprehension) — machine evidence only, no full WCAG audit,
 * no NVDA/JAWS, no mobile VO.
 *
 * Run (boots both loopback servers itself and tears them down):
 *   make a11y-ax
 * or against already-running loopback servers:
 *   NODE_PATH=/opt/homebrew/lib/node_modules node tests/browser/ax-audit.js
 * Env: AX_BASE (default http://127.0.0.1:8080), AX_COV (default :8081),
 *      AX_OUT (result JSON path, default /tmp/ha-ax-audit-result.json),
 *      AX_HEAD (label recorded in meta.app_head; default: git HEAD).
 * Exit 0 = every journey PASS (advisories allowed); exit 1 = mapped findings
 * or harness error. Loopback only; synthetic data only.
 *
 * Checker-artifact elimination log — candidate "findings" withdrawn during
 * the original 2026-09-13 audit (HA-MACHINE-A11Y-PASS-RESULT.md), kept here
 * so the screen-reader-half gate re-runs without re-deriving the CDP pits:
 *  1. "Live-region text not announced": reading only the region node's
 *     name/value + strict subtree misses the text — Chromium re-parents
 *     live-region text nodes and populated text lives in child StaticText
 *     nodes. Assert instead: region exposes role=status + live=polite +
 *     atomic, AND the updated text exists as StaticText somewhere in the
 *     tree (axTreeContainsText).
 *  2. "focusables never reached by Tab": Chromium's sequential-focus start
 *     follows the previously focused element across page.reload() (focus
 *     restoration), so walks began mid-document. Walk a FRESH page per
 *     state and combine forward + backward coverage.
 *  3. "all chrome focusables absent from the AX tree": the cross-check
 *     snapshotted the DOM before tagging data-axprobe attributes, so every
 *     backend-node lookup missed. Tag first, then snapshot, then look up.
 *  4. "backward walk never reaches the skip link": descriptors lacked DOM
 *     indices, so two adjacent identical tags read as a stuck loop. Use
 *     indexed descriptors (idx:tag#id).
 *  5. "skip link (index 0) never reached": visited but not recorded before
 *     the loop break. Record before breaking.
 *  6. "heading outline skips h1->h4": v1 ordered headings from the CDP
 *     response array, not DOM order. Build the outline from a DOM query in
 *     document order, visible-only.
 *  Trap semantics: consecutive-same-focus at the LAST/FIRST DOM focusable
 *  is a document boundary, not a trap.
 *  CDP pitfall: nodeId values are strings in some responses and numbers in
 *  others — always String() them before Map lookups (see byId/collect).
 */
const { chromium } = require('playwright');

const BASE = process.env.AX_BASE || 'http://127.0.0.1:8080';
const COV = process.env.AX_COV || 'http://127.0.0.1:8081';

const findings = [];
const advisories = [];
const journeys = {};
const log = (...a) => console.log(...a);
const finding = (journey, step, sc, level, desc, evidence) =>
  findings.push({ journey, step, sc, level, desc, evidence: String(evidence).slice(0, 400) });
const advisory = (journey, step, sc, desc, evidence) =>
  advisories.push({ journey, step, sc, desc, evidence: String(evidence).slice(0, 400) });

const INTERACTIVE_ROLES = new Set(['button', 'link', 'textBox', 'searchBox', 'checkBox',
  'radioButton', 'comboBox', 'listBox', 'option', 'menuItem', 'menuBarItem', 'menu',
  'menuButton', 'tab', 'switch', 'spinButton', 'slider', 'treeItem', 'popUpButton',
  'dateTime', 'gridCell', 'details', 'disclosureTriangle']);
const VALUE_ROLES = new Set(['textBox', 'searchBox', 'spinButton', 'comboBox', 'slider', 'dateTime']);
const LIVE_ROLES = new Set(['status', 'alert', 'log', 'marquee', 'timer', 'statusBar', 'alertDialog']);
const LANDMARK_ROLES = ['banner', 'main', 'navigation', 'contentinfo', 'complementary', 'form', 'region'];
const settle = (p, ms = 450) => p.waitForTimeout(ms);

/* ---------- CDP helpers ---------- */
async function cdpFor(page) {
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('DOM.enable');
  await cdp.send('Accessibility.enable');
  return cdp;
}
const prop = (node, name) => {
  const p = (node.properties || []).find(x => x.name === name);
  if (!p) return undefined;
  return p.value ? p.value.value : undefined;
};
async function getAx(cdp) {
  const { nodes } = await cdp.send('Accessibility.getFullAXTree');
  return nodes;
}

/* AX representation of a DOM id, including its announced subtree text. */
async function axNodeForDomId(cdp, page, id) {
  const { root } = await cdp.send('DOM.getDocument', { depth: -1 });
  let backend = null;
  (function walk(n) {
    if (!n || backend !== null) return;
    const attrs = n.attributes || [];
    for (let i = 0; i < attrs.length; i += 2)
      if (attrs[i] === 'id' && attrs[i + 1] === id) { backend = n.backendNodeId; return; }
    (n.children || []).some(walk);
    if (backend === null && n.shadowRoots) n.shadowRoots.some(walk);
  })(root);
  const nodes = await getAx(cdp);
  const byId = new Map(nodes.map(n => [String(n.nodeId), n]));
  const target = nodes.find(n => n.backendDOMNodeId === backend);
  if (!target) return null;
  // collect announced text from the subtree (staticText/inlineTextBox nodes)
  const texts = [];
  (function collect(n) {
    const node = byId.get(n);
    if (!node) return;
    const role = node.role && node.role.value || '';
    if (role === 'staticText' || role === 'inlineTextBox') {
      const t = (node.name && node.name.value) || (node.value && node.value.value) || '';
      if (t) texts.push(t);
    }
    (node.childIds || []).forEach(cid => collect(String(cid)));
  })(String(target.nodeId));
  return { role: target.role && target.role.value, name: (target.name && target.name.value) || '',
    value: target.value && target.value.value !== undefined ? String(target.value.value) : '',
    live: prop(target, 'live'), relevant: prop(target, 'relevant'),
    atomic: prop(target, 'atomic'), busy: prop(target, 'busy'),
    subtreeText: texts.join(' ').replace(/\s+/g, ' ').trim() };
}


/* the updated text must exist as an AX StaticText node somewhere in the tree
 * (Chrome re-parents live-region text; subtree walking alone is not evidence) */
async function axTreeContainsText(cdp, needle) {
  if (!needle) return false;
  const nodes = await getAx(cdp);
  const n = needle.replace(/\s+/g, ' ').trim().slice(0, 60);
  return nodes.some(x => {
    const t = ((x.name && x.name.value) || '').replace(/\s+/g, ' ').trim();
    return t.includes(n);
  });
}

/* ---------- structure audit ---------- */
async function auditStructure(cdp, page, journey, step) {
  const nodes = await getAx(cdp);
  const counts = { axNodes: nodes.length, interactive: 0, named: 0, unnamed: [],
    headings: [], landmarks: {}, liveRegions: [], valueIssues: [] };
  for (const node of nodes) {
    const role = node.role && node.role.value || '';
    const name = node.name && node.name.value || '';
    if (INTERACTIVE_ROLES.has(role)) {
      counts.interactive++;
      if (!name.trim()) counts.unnamed.push(`${role}#b${node.backendDOMNodeId}`);
      else counts.named++;
      if (VALUE_ROLES.has(role) && (node.value === undefined || node.value === null))
        counts.valueIssues.push(`${role} ${JSON.stringify(name)}`);
      if (role === 'checkBox' && prop(node, 'checked') === undefined)
        counts.valueIssues.push(`checkBox ${JSON.stringify(name)} no checked state`);
    }
    if (role === 'heading') counts.headings.push({ level: prop(node, 'level'), name: name.slice(0, 60), backend: node.backendDOMNodeId });
    if (LANDMARK_ROLES.includes(role)) counts.landmarks[role] = (counts.landmarks[role] || 0) + 1;
    if (LIVE_ROLES.has(role) || ['polite', 'assertive'].includes(prop(node, 'live')))
      counts.liveRegions.push({ role, live: prop(node, 'live') || '(implicit)', name: name.slice(0, 40) });
  }
  // heading outline in DOM order (visible only), levels from the AX nodes
  const outline = await page.evaluate(() => {
    return [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(el => {
      const v = el.closest('.view'); if (v && !v.classList.contains('active')) return false;
      return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    }).map(el => ({ tag: el.tagName.toLowerCase(), text: el.textContent.trim().slice(0, 60) }));
  });
  counts.headingOutlineDomOrder = outline.map(h => `${h.tag} "${h.text}"`);
  let prev = 0;
  for (const h of outline) {
    const lvl = parseInt(h.tag[1]);
    if (prev && lvl > prev + 1)
      advisory(journey, step, '1.3.1',
        `heading outline skips levels (h${prev} -> h${lvl} "${h.text}"); screen-reader heading navigation works but the outline implies missing subsection levels`,
        counts.headingOutlineDomOrder.join(' | '));
    prev = lvl || prev;
  }
  if (counts.unnamed.length) finding(journey, step, '4.1.2', 'A',
    `${counts.unnamed.length} interactive AX node(s) expose an empty accessible name`, counts.unnamed.join(', '));
  if (counts.valueIssues.length) finding(journey, step, '4.1.2', 'A',
    'value/state not exposed on value-bearing control(s)', counts.valueIssues.join('; '));
  return counts;
}

/* visible focusables in DOM order, with global DOM index */
async function domFocusables(page) {
  return page.evaluate(() => {
    const sel = 'a[href], button, input, select, textarea, summary, [tabindex]:not([tabindex="-1"])';
    const all = [...document.querySelectorAll(sel)];
    return all.filter(el => {
      if (el.disabled) return false;
      const v = el.closest('.view');
      if (v && !v.classList.contains('active')) return false;
      const style = getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden') return false;
      return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    }).map(el => ({ idx: all.indexOf(el), tag: el.tagName.toLowerCase(), id: el.id,
      name: el.getAttribute('aria-label') || el.textContent.trim().slice(0, 32) || el.name || '' }));
  });
}

/* every visible focusable must be present (focusable) in the AX tree */
async function crossCheckFocusablesInAx(page, cdp, journey, step) {
  const probes = await page.evaluate(() => {
    const sel = 'a[href], button, input, select, textarea, summary, [tabindex]:not([tabindex="-1"])';
    const all = [...document.querySelectorAll(sel)];
    return all.filter(el => {
      if (el.disabled) return false;
      const v = el.closest('.view');
      if (v && !v.classList.contains('active')) return false;
      const style = getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden') return false;
      return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    }).map(el => {
      const idx = all.indexOf(el);
      el.setAttribute('data-axprobe', String(idx));
      return { idx, tag: el.tagName.toLowerCase(), id: el.id,
        name: el.getAttribute('aria-label') || el.textContent.trim().slice(0, 28) || '' };
    });
  });
  const { root } = await cdp.send('DOM.getDocument', { depth: -1 });
  const backendByDomIdx = {};
  (function walk(n) {
    if (!n) return;
    const attrs = n.attributes || [];
    for (let i = 0; i < attrs.length; i += 2)
      if (attrs[i] === 'data-axprobe') backendByDomIdx[attrs[i + 1]] = n.backendNodeId;
    (n.children || []).forEach(walk);
  })(root);
  const nodes = await getAx(cdp);
  const axFocusable = new Set(nodes.filter(n => prop(n, 'focusable')).map(n => n.backendDOMNodeId));
  const missing = probes.filter(p => !axFocusable.has(backendByDomIdx[String(p.idx)]));
  await page.evaluate(() => document.querySelectorAll('[data-axprobe]').forEach(el => el.removeAttribute('data-axprobe')));
  if (missing.length) finding(journey, step, '2.4.3', 'A',
    'visible focusable element(s) absent from the accessibility tree (screen readers cannot reach them)',
    JSON.stringify(missing));
  return { visibleFocusables: probes.length, missingFromAx: missing.length, missing };
}

const focusState = () => {
  const el = document.activeElement;
  if (!el || el === document.body) return { body: true };
  const cs = getComputedStyle(el);
  const sel = 'a[href], button, input, select, textarea, summary, [tabindex]:not([tabindex="-1"])';
  const all = [...document.querySelectorAll(sel)];
  return { body: false, idx: all.indexOf(el), tag: el.tagName.toLowerCase(), id: el.id,
    name: (el.getAttribute('aria-label') || el.textContent.trim().slice(0, 32) || ''),
    fv: el.matches(':focus-visible'),
    ow: cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0,
    bs: cs.boxShadow !== 'none' };
};

/* Combined forward+backward walk from current focus. Full-coverage check:
 * forward visits idx..end in increasing DOM order, backward covers ..idx-1. */
async function tabWalk(page, journey, step, maxSteps = 70) {
  const dom = await domFocusables(page);
  const domSet = dom.map(f => f.idx);
  const fSeq = [], bSeq = [];
  let fvMiss = [], indMiss = [];
  const startState = await page.evaluate(focusState);
  // forward until BODY (document end)
  for (let i = 0; i < maxSteps; i++) {
    await page.keyboard.press('Tab'); await settle(page);
    const st = await page.evaluate(focusState);
    if (st.body) break;
    const d = `${st.idx}:${st.tag}${st.id ? '#' + st.id : ''}`;
    if (fSeq.length && fSeq[fSeq.length - 1] === d) {
      // stuck on the same element: trap unless it is the last DOM focusable
      const lastIdx = Math.max(...domSet);
      if (st.idx !== lastIdx) finding(journey, step, '2.4.3', 'A', 'focus trap: Tab stops advancing mid-document', fSeq.join(' ') + ' STUCK@' + d);
      break;
    }
    fSeq.push(d);
    if (!st.fv) fvMiss.push(d);
    if (!(st.ow || st.bs)) indMiss.push(d);
  }
  // backward from body -> last element -> down to 0
  for (let i = 0; i < maxSteps; i++) {
    await page.keyboard.press('Shift+Tab'); await settle(page);
    const st = await page.evaluate(focusState);
    if (st.body) { if (bSeq.length) break; else continue; }
    const d = `${st.idx}:${st.tag}${st.id ? '#' + st.id : ''}`;
    if (bSeq.length && bSeq[bSeq.length - 1] === d) {
      const firstIdx = Math.min(...domSet);
      if (st.idx !== firstIdx) finding(journey, step, '2.4.3', 'A', 'focus trap: Shift+Tab stops advancing mid-document', bSeq.join(' ') + ' STUCK@' + d);
      break;
    }
    if (parseInt(d) === 0) { bSeq.push(d); break; }
    if (bSeq.includes(d)) break;
    bSeq.push(d);
    if (!st.fv) fvMiss.push('b:' + d);
    if (!(st.ow || st.bs)) indMiss.push('b:' + d);
  }
  const covered = new Set([...fSeq, ...bSeq].map(s => parseInt(s)));
  const missed = domSet.filter(i => !covered.has(i));
  const fIdx = fSeq.map(s => parseInt(s)), bIdx = bSeq.map(s => parseInt(s));
  let monoF = true, monoB = true;
  for (let i = 1; i < fIdx.length; i++) if (fIdx[i] <= fIdx[i - 1]) monoF = false;
  for (let i = 1; i < bIdx.length; i++) if (bIdx[i] >= bIdx[i - 1]) monoB = false;
  if (missed.length) finding(journey, step, '2.4.3', 'A',
    `${missed.length} visible focusable element(s) never reached by combined Tab/Shift+Tab walk`, JSON.stringify(missed));
  if (!monoF) finding(journey, step, '2.4.3', 'A', 'forward Tab order deviates from DOM order', fSeq.join(' '));
  if (!monoB && bIdx.length > 1) finding(journey, step, '2.4.3', 'A', 'backward Shift+Tab order deviates from DOM order', bSeq.join(' '));
  if (fvMiss.length) finding(journey, step, '2.4.7', 'AA', 'focused element(s) never match :focus-visible', fvMiss.join(', '));
  if (indMiss.length) finding(journey, step, '2.4.7', 'AA', 'focused element(s) show no author focus indicator (outline/box-shadow)', indMiss.join(', '));
  return { startFocus: startState.body ? 'BODY' : `${startState.idx}:${startState.tag}${startState.id ? '#' + startState.id : ''}`,
    visibleFocusables: dom.length, forwardSteps: fSeq.length, backwardSteps: bSeq.length,
    covered: covered.size, missed, forward: fSeq, backward: bSeq, monoF, monoB, fvMiss, indMiss };
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  log(`# HealthAdvocate machine announcement-equivalent AX audit v2`);
  log(`# chromium ${browser.version()} | playwright ${require('playwright/package.json').version}`);
  log(`# A=${BASE} B=${COV}`);
  const newJourneyCtx = async () => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.abort());
    return ctx;
  };

  /* ============ JOURNEY 1: HOME ============ */
  {
    const J = 'home'; journeys[J] = { steps: [] };
    const ctx = await newJourneyCtx();
    const page = await ctx.newPage();
    const cdp = await cdpFor(page);
    await page.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
    await settle(page, 900);
    const counts = await auditStructure(cdp, page, J, 'load');
    journeys[J].steps.push({ step: 'load', counts });
    const title = await page.title(), lang = await page.getAttribute('html', 'lang');
    if (!/HealthAdvocate/.test(title)) finding(J, 'load', '2.4.2', 'A', 'document title does not identify the app', title);
    if (lang !== 'en') finding(J, 'load', '3.1.1', 'A', 'html lang missing/not en', String(lang));
    if (!counts.landmarks.main) finding(J, 'load', '1.3.1', 'A', 'no main landmark in AX tree', JSON.stringify(counts.landmarks));
    if (!counts.landmarks.banner) finding(J, 'load', '1.3.1', 'A', 'no banner landmark in AX tree', JSON.stringify(counts.landmarks));
    if (counts.headings.filter(h => h.level === 1).length !== 1) finding(J, 'load', '1.3.1', 'A', 'expected exactly one h1', JSON.stringify(counts.headings.map(h => 'h' + h.level)));

    // skip link (2.4.1)
    await page.keyboard.press('Tab'); await settle(page);
    const skipName = await page.evaluate(() => document.activeElement.classList.contains('skip-link') ? document.activeElement.textContent.trim() : null);
    await page.keyboard.press('Enter'); await settle(page);
    await page.keyboard.press('Tab'); await settle(page);
    const afterSkip = await page.evaluate(() => ({ inMain: !!document.activeElement.closest('main'),
      el: document.activeElement.tagName + (document.activeElement.id ? '#' + document.activeElement.id : '') }));
    if (!skipName) finding(J, 'skip-link', '2.4.1', 'A', 'first Tab does not land on the skip link', skipName);
    if (!afterSkip.inMain) finding(J, 'skip-link', '2.4.1', 'A', 'skip-link activation does not bring sequential focus into main', JSON.stringify(afterSkip));
    journeys[J].steps.push({ step: 'skip-link', firstTab: skipName, afterEnterNextTab: afterSkip });

    // tab walk on a FRESH page (deterministic body start)
    const p2 = await ctx.newPage();
    const cdp2 = await cdpFor(p2);
    await p2.goto(BASE + '/', { waitUntil: 'domcontentloaded' }); await settle(p2, 900);
    const walk = await tabWalk(p2, J, 'tab-walk');
    journeys[J].steps.push({ step: 'tab-walk', ...walk, forward: walk.forward.slice(0, 30), backward: walk.backward.slice(0, 30) });
    const xcheck = await crossCheckFocusablesInAx(p2, cdp2, J, 'tab-walk');
    journeys[J].steps.push({ step: 'focusables-in-ax', ...xcheck });

    // entry-card activation: where does focus go after the view switch?
    await p2.focus('.entry-card[data-goto="symptoms"]');
    await p2.keyboard.press('Enter'); await settle(p2);
    const afterEnter = await p2.evaluate(() => ({
      view: document.querySelector('.view.active')?.id,
      focus: document.activeElement === document.body ? 'BODY' : document.activeElement.tagName + (document.activeElement.id ? '#' + document.activeElement.id : ''),
      focusInView: !!(document.activeElement.closest && document.activeElement.closest('.view.active')),
    }));
    journeys[J].steps.push({ step: 'entry-activation-enter', ...afterEnter });
    if (afterEnter.focus === 'BODY' || !afterEnter.focusInView)
      finding(J, 'entry-activation', '2.4.3', 'A',
        `SPA view switch on entry-card activation leaves focus on document.body (focused control was hidden with the home view); the new view is not announced and sequential focus restarts from the document start`,
        JSON.stringify(afterEnter));
    // same check via Space
    await p2.keyboard.press('Shift+Tab'); await settle(p2); // back to body -> last focusable
    await p2.evaluate(() => HA.showView('home')); await settle(p2);
    await p2.focus('.entry-card[data-goto="symptoms"]');
    await p2.keyboard.press(' '); await settle(p2);
    const afterSpace = await p2.evaluate(() => ({
      view: document.querySelector('.view.active')?.id,
      focus: document.activeElement === document.body ? 'BODY' : document.activeElement.tagName + (document.activeElement.id ? '#' + document.activeElement.id : ''),
    }));
    journeys[J].steps.push({ step: 'entry-activation-space', ...afterSpace });
    if (afterSpace.focus === 'BODY' || afterSpace.view !== 'view-symptoms')
      finding(J, 'entry-activation-space', '2.4.3', 'A',
        `SPA view switch on entry-card Space activation leaves focus on document.body`,
        JSON.stringify(afterSpace));
    // nav-button activation for contrast (focus stays on the control)
    await p2.evaluate(() => HA.showView('home')); await settle(p2);
    await p2.click('.nav-btn[data-view="symptoms"]'); await settle(p2);
    const afterNav = await p2.evaluate(() => ({
      view: document.querySelector('.view.active')?.id,
      focus: document.activeElement === document.body ? 'BODY' : document.activeElement.tagName + (document.activeElement.id ? '#' + document.activeElement.id : '') + '.' + (document.activeElement.className || '').split(' ')[0],
    }));
    journeys[J].steps.push({ step: 'nav-activation', ...afterNav });
    // theme toggle state exposure observation
    const themeBtn = await axNodeForDomId(cdp2, p2, 'btn-theme');
    journeys[J].steps.push({ step: 'theme-toggle-ax', node: themeBtn });
    if (themeBtn && themeBtn.role === 'button' && !/pressed|theme state|dark|light/i.test(themeBtn.name))
      advisory(J, 'theme-toggle', '4.1.2',
        'theme toggle is a stateless button (no aria-pressed / no state in name) and the theme change is not announced; VO users press it blind',
        JSON.stringify(themeBtn));
    await ctx.close();
  }

  /* ============ JOURNEY 2: SYMPTOMS ============ */
  {
    const J = 'symptoms'; journeys[J] = { steps: [] };
    const ctx = await newJourneyCtx();
    const page = await ctx.newPage();
    const cdp = await cdpFor(page);
    await page.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
    await settle(page, 900);
    await page.evaluate(() => HA.showView('symptoms'));
    await settle(page);

    const counts = await auditStructure(cdp, page, J, 'open');
    journeys[J].steps.push({ step: 'open', counts });
    if (counts.headingOutlineDomOrder.length === 0)
      advisory(J, 'open', '1.3.1',
        'symptoms view exposes zero headings while active; its visual title "Symptom Assessment" is a styled span (panel-eyebrow), not a programmatic heading — VO heading navigation finds nothing to orient on in this view',
        'coverage view, by contrast, is labelled by an h2 (Coverage Continuity)');
    const liveBefore = await axNodeForDomId(cdp, page, 'symptom-results');
    journeys[J].steps.push({ step: 'live-region-empty-state', node: liveBefore,
      note: 'empty live region may be pruned from the AX tree until content arrives; liveness is asserted post-update below' });

    // dynamic update: model-unavailable guidance (announcement capture)
    await page.fill('#symptom-input', 'Synthetic AX probe: mild headache for two days, no fever');
    await page.click('#view-symptoms [data-action="assess-symptoms"]');
    await page.waitForFunction(() => {
      const t = document.getElementById('symptom-results').textContent.trim();
      return t.length > 0 && !/loading|analyzing/i.test(t.slice(0, 24));
    }, null, { timeout: 20000 });
    await settle(page);
    const ann = await axNodeForDomId(cdp, page, 'symptom-results');
    const annText = await page.evaluate(() => document.getElementById('symptom-results').textContent.trim());
    const annInAx = await axTreeContainsText(cdp, 'Model processing was blocked'); // single StaticText node; full domText spans nodes
    journeys[J].steps.push({ step: 'announce-assess', node: ann, domText: annText.slice(0, 240), textPresentInAxTree: annInAx });
    if (!ann || !ann.live || ann.live === 'off')
      finding(J, 'announce-assess', '4.1.3', 'AA', 'symptom results region not exposed as live in the AX tree after update', JSON.stringify(ann));
    else if (!annInAx || !/model|privacy|blocked|unable|offline/i.test(annText))
      finding(J, 'announce-assess', '4.1.3', 'AA', 'dynamic symptom result text not present in the AX tree', JSON.stringify({ ann, annText: annText.slice(0, 120), annInAx }));
    // structure after results render (heading outline of the populated view)
    const countsAfter = await auditStructure(cdp, page, J, 'after-assess');
    journeys[J].steps.push({ step: 'after-assess-structure', headingOutline: countsAfter.headingOutlineDomOrder });

    // error path: 422 oversize announced through the same region
    await page.fill('#symptom-input', 'x'.repeat(50001));
    await page.click('#view-symptoms [data-action="assess-symptoms"]');
    await page.waitForFunction(() => /exceeds maximum length|error/i.test(document.getElementById('symptom-results').textContent), null, { timeout: 20000 });
    await settle(page);
    const err = await axNodeForDomId(cdp, page, 'symptom-results');
    const errText = await page.evaluate(() => document.getElementById('symptom-results').textContent.trim());
    const errInAx = await axTreeContainsText(cdp, errText);
    journeys[J].steps.push({ step: 'announce-422-oversize', node: err, domText: errText.slice(0, 240), textPresentInAxTree: errInAx });
    if (!/exceeds maximum length/i.test(errText) || !errInAx)
      finding(J, 'announce-422-oversize', '4.1.3', 'AA', '422 oversize error text not exposed in the AX tree', JSON.stringify({ err, errText: errText.slice(0, 120), errInAx }));

    // tab walk on fresh page in the symptoms state
    const p2 = await ctx.newPage();
    const cdp2 = await cdpFor(p2);
    await p2.goto(BASE + '/', { waitUntil: 'domcontentloaded' }); await settle(p2, 900);
    await p2.evaluate(() => HA.showView('symptoms')); await settle(p2);
    const walk = await tabWalk(p2, J, 'tab-walk');
    journeys[J].steps.push({ step: 'tab-walk', ...walk, forward: walk.forward.slice(0, 30), backward: walk.backward.slice(0, 30) });
    const xcheck = await crossCheckFocusablesInAx(p2, cdp2, J, 'tab-walk');
    journeys[J].steps.push({ step: 'focusables-in-ax', ...xcheck });
    await ctx.close();
  }

  /* ============ JOURNEY 3: COVERAGE ============ */
  {
    const J = 'coverage'; journeys[J] = { steps: [] };
    const ctx = await newJourneyCtx();
    const page = await ctx.newPage();
    const cdp = await cdpFor(page);
    await page.goto(COV + '/', { waitUntil: 'domcontentloaded' });
    await settle(page, 900);
    await page.evaluate(() => HA.showView('coverage'));
    await settle(page);

    const counts = await auditStructure(cdp, page, J, 'open');
    journeys[J].steps.push({ step: 'open', counts });
    const region = await axNodeForDomId(cdp, page, 'view-coverage');
    journeys[J].steps.push({ step: 'region-ax', node: region });
    if (!region || !/coverage continuity/i.test((region.name || '') + (region.subtreeText || '').slice(0, 40)))
      finding(J, 'open', '1.3.1', 'A', 'coverage view region not named by its heading in the AX tree', JSON.stringify(region));

    // create synthetic case -> panel + announced status
    await page.fill('#coverage-title', 'Synthetic a11y AX probe case');
    await page.click('[data-action="coverage-create"]');
    await page.waitForFunction(() => !document.getElementById('coverage-panel').hidden, null, { timeout: 30000 });
    await settle(page);
    const created = await axNodeForDomId(cdp, page, 'coverage-status');
    const createdText = await page.evaluate(() => document.getElementById('coverage-status').textContent.trim());
    const createdInAx = await axTreeContainsText(cdp, createdText);
    journeys[J].steps.push({ step: 'announce-create', node: created, domText: createdText.slice(0, 200), textPresentInAxTree: createdInAx });
    if (!created || !created.live || created.live === 'off')
      finding(J, 'announce-create', '4.1.3', 'AA', 'coverage status region not live in AX tree after update', JSON.stringify(created));
    else if (!createdInAx || !/created \(synthetic only\)/i.test(createdText))
      finding(J, 'announce-create', '4.1.3', 'AA', 'case-created status not exposed in the AX tree', JSON.stringify({ created, createdText: createdText.slice(0, 120), createdInAx }));
    const panelCounts = await auditStructure(cdp, page, J, 'panel-state');
    journeys[J].steps.push({ step: 'panel-structure', counts: panelCounts });

    // keyboard-driven create: where does focus land when the form is replaced by the panel?
    await page.reload({ waitUntil: 'domcontentloaded' }); await settle(page, 900);
    await page.evaluate(() => HA.showView('coverage')); await settle(page);
    await page.focus('#coverage-title');
    await page.fill('#coverage-title', 'Synthetic a11y AX probe case 3');
    // keyboard: Tab from the title input to the create button, then Enter
    await page.keyboard.press('Tab'); await settle(page);
    const createFocused = await page.evaluate(() => document.activeElement.dataset?.action || document.activeElement.tagName);
    await page.keyboard.press('Enter');
    await page.waitForFunction(() => !document.getElementById('coverage-panel').hidden, null, { timeout: 30000 });
    await settle(page);
    const afterKbCreate = await page.evaluate(() => ({
      view: document.querySelector('.view.active')?.id,
      focus: document.activeElement === document.body ? 'BODY' : document.activeElement.tagName + (document.activeElement.id ? '#' + document.activeElement.id : ''),
      focusInView: !!(document.activeElement.closest && document.activeElement.closest('.view.active')),
      status: document.getElementById('coverage-status').textContent.trim(),
    }));
    journeys[J].steps.push({ step: 'keyboard-create-focus', createFocused, ...afterKbCreate });
    if (afterKbCreate.focus === 'BODY' || !afterKbCreate.focusInView)
      finding(J, 'keyboard-create-focus', '2.4.3', 'A',
        'SPA form-to-panel replacement on keyboard case creation leaves focus on document.body (create form is hidden with the focused button); the new panel is not announced and sequential focus restarts from the document start',
        JSON.stringify({ createFocused, ...afterKbCreate }));

    // combined walk across the panel document state
    const walk = await tabWalk(page, J, 'tab-walk-panel');
    journeys[J].steps.push({ step: 'tab-walk-panel', ...walk, forward: walk.forward.slice(0, 40), backward: walk.backward.slice(0, 40) });
    const xcheck = await crossCheckFocusablesInAx(page, cdp, J, 'tab-walk-panel');
    journeys[J].steps.push({ step: 'focusables-in-ax', ...xcheck });

    // commitment gate by keyboard alone -> designed fail-closed answer announced
    await page.reload({ waitUntil: 'domcontentloaded' }); await settle(page, 900);
    await page.evaluate(() => HA.showView('coverage')); await settle(page);
    await page.fill('#coverage-title', 'Synthetic a11y AX probe case 2');
    await page.click('[data-action="coverage-create"]');
    await page.waitForFunction(() => !document.getElementById('coverage-panel').hidden, null, { timeout: 30000 });
    await settle(page);
    await page.focus('#coverage-intent');
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('Tab'); await settle(page);
    const gateFocused = await page.evaluate(() => document.activeElement.dataset?.action || document.activeElement.tagName);
    await page.keyboard.press('Enter');
    await page.waitForFunction(() => document.getElementById('coverage-gate-result').textContent.trim().length > 0, null, { timeout: 30000 });
    await settle(page);
    const gate = await axNodeForDomId(cdp, page, 'coverage-gate-result');
    const gateText = await page.evaluate(() => document.getElementById('coverage-gate-result').textContent.trim());
    const gateInAx = await axTreeContainsText(cdp, gateText);
    journeys[J].steps.push({ step: 'announce-commitment-gate', gateFocused, node: gate, domText: gateText.slice(0, 260), textPresentInAxTree: gateInAx });
    if (gateFocused !== 'coverage-gate')
      finding(J, 'announce-commitment-gate', '2.4.3', 'A', 'commitment-gate button not reached by keyboard from the intent select', gateFocused);
    if (!gate || !gate.live || gate.live === 'off')
      finding(J, 'announce-commitment-gate', '4.1.3', 'AA', 'gate result region not live in AX tree after update', JSON.stringify(gate));
    else if (!gateInAx || !/blocked: HealthAdvocate will not perform this action/i.test(gateText))
      finding(J, 'announce-commitment-gate', '4.1.3', 'AA', 'fail-closed gate answer not exposed in the AX tree', JSON.stringify({ gate, gateText: gateText.slice(0, 120), gateInAx }));

    // fresh-page create-form state walk
    const p2 = await ctx.newPage();
    const cdp2 = await cdpFor(p2);
    await p2.goto(COV + '/', { waitUntil: 'domcontentloaded' }); await settle(p2, 900);
    await p2.evaluate(() => HA.showView('coverage')); await settle(p2);
    const walkForm = await tabWalk(p2, J, 'tab-walk-form');
    journeys[J].steps.push({ step: 'tab-walk-form', ...walkForm, forward: walkForm.forward.slice(0, 30), backward: walkForm.backward.slice(0, 30) });
    const xcheck2 = await crossCheckFocusablesInAx(p2, cdp2, J, 'tab-walk-form');
    journeys[J].steps.push({ step: 'focusables-in-ax-form', ...xcheck2 });
    await ctx.close();
  }

  for (const j of Object.keys(journeys)) {
    const jf = findings.filter(f => f.journey === j);
    journeys[j].mappedFailures = jf.length;
    journeys[j].advisories = advisories.filter(f => f.journey === j).length;
    journeys[j].verdict = jf.length === 0 ? 'PASS' : 'FAIL';
  }
  const head = process.env.AX_HEAD || (() => {
    try {
      return require('child_process').execSync('git rev-parse HEAD').toString().trim();
    } catch (e) {
      return 'unknown';
    }
  })();
  const out = {
    meta: { app_head: head, chromium: browser.version(),
      playwright: require('playwright/package.json').version, base: BASE, covBase: COV,
      generated: new Date().toISOString(),
      scope: 'machine announcement-equivalent AX-tree audit; human VoiceOver listening pass NOT covered' },
    journeys, findings, advisories,
  };
  const outPath = process.env.AX_OUT || '/tmp/ha-ax-audit-result.json';
  require('fs').writeFileSync(outPath, JSON.stringify(out, null, 2));
  log('\n# SUMMARY');
  for (const [j, d] of Object.entries(journeys)) log(`${j}: ${d.verdict} failures=${d.mappedFailures} advisories=${d.advisories}`);
  log(`\nmapped findings: ${findings.length}`);
  findings.forEach(f => log(`- [${f.journey}/${f.step}] SC ${f.sc} (${f.level}): ${f.desc} :: ${f.evidence.slice(0, 150)}`));
  log(`\nadvisories: ${advisories.length}`);
  advisories.forEach(f => log(`- [${f.journey}/${f.step}] SC ${f.sc}: ${f.desc}`));
  log(`\nresult json: ${outPath}`);
  await browser.close();
  process.exit(findings.length ? 1 : 0);
})().catch(e => { console.error('HARNESS ERROR', e); process.exit(1); });
