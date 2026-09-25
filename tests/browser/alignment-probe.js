/* G001 probe: sibling cards equal width; containers on the measure. Boots its own
 * loopback server like ax-audit (env ALGN_BASE to override). */
const { chromium } = require('playwright');

(async () => {
  const BASE = process.env.ALGN_BASE || 'http://127.0.0.1:8080';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await p.goto(BASE + '/', { waitUntil: 'networkidle' });
  await p.waitForTimeout(800);
  await p.evaluate(() => document.querySelectorAll('.reveal').forEach((el) => el.setAttribute('data-reveal', 'revealed')));
  const facts = await p.evaluate(() => {
    const cards = [...document.querySelectorAll('.entry-grid .entry-card:not(.entry-card-primary)')];
    const ws = cards.map(c => c.getBoundingClientRect().width);
    const grid = getComputedStyle(document.querySelector('.entry-grid') || document.body);
    const shell = document.querySelector('header .container, header > div, #main-nav') || document.body;
    const shellW = shell.getBoundingClientRect().width;
    return {
      siblingCount: ws.length,
      widthDelta: ws.length >= 2 ? Math.max(...ws) - Math.min(...ws) : 0,
      gap: grid.gap,
      shellW: Math.round(shellW),
    };
  });
  await b.close();
  console.log(JSON.stringify(facts));
  if (facts.widthDelta > 2) { console.error('FAIL: sibling width delta > 2px'); process.exit(1); }
  console.log('PASS');
})().catch(e => { console.error(e); process.exit(1); });
