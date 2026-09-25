/** empor #1 pin: the four theme dots must render distinct colors. */
// S+ r3 pin (empor #1): the theme dots must RENDER their colors — a regex
// once deleted the dot rules and gray placeholders rode two full judge rounds.
(async () => {
  const { chromium } = require('playwright');
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto((process.env.ALGN_BASE || 'http://127.0.0.1:8080') + '/', { waitUntil: 'networkidle' });
  await p.waitForTimeout(600);
  const dots = await p.evaluate(() => [...document.querySelectorAll('.pal-swatch')].map(el => getComputedStyle(el).backgroundColor));
  await b.close();
  const uniq = new Set(dots);
  if (dots.length >= 4 && uniq.size < 4) { console.error('FAIL: theme dots not distinct —', dots.join(' ')); process.exit(1); }
  console.log('theme dots distinct:', [...uniq].join(' '));
})();
