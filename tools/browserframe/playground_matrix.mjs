import { chromium, webkit } from 'playwright';
import { execSync } from 'node:child_process';
import fs from 'node:fs';

const SHOTS = '/tmp/ha-ultraqa-qa/shots';
fs.mkdirSync(SHOTS, { recursive: true });
const results = [];
const row = (id, intent, pass, evidence) => {
  results.push({ id, intent, result: pass ? 'pass' : 'fail', evidence });
  console.log(`[${pass ? 'PASS' : 'FAIL'}] ${id} — ${evidence.slice(0, 170)}`);
  fs.writeFileSync('/tmp/ha-ultraqa-qa/results.json', JSON.stringify(results, null, 2));
};

async function restoreTunnel() {
  try {
    execSync('launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.kyanite.ha-crack-tunnel.plist 2>/dev/null || launchctl kickstart gui/$(id -u)/com.kyanite.ha-crack-tunnel', { shell: '/bin/bash' });
  } catch (e) { console.log('restore:', String(e).slice(0, 100)); }
}

async function openPage(launcher, engineName) {
  const browser = await launcher.launch();
  const page = await (await browser.newContext()).newPage();
  const logs = [];
  page.on('console', m => logs.push(`${m.type()}:${m.text().slice(0, 80)}`));
  page.on('pageerror', e => logs.push(`pageerror:${String(e).slice(0, 120)}`));
  return { browser, page, logs, tag: engineName.toUpperCase() };
}

async function runEngine(launcher, engineName) {
  const { browser, page, logs, tag } = await openPage(launcher, engineName);
  try {
    await page.goto('http://127.0.0.1:8936/', { timeout: 15000, waitUntil: 'domcontentloaded' });
    let badgeTxt = '';
    try {
      await page.waitForSelector('#badge.bad-live', { timeout: 20000 });
      badgeTxt = await page.textContent('#badge');
      row(`S1-${tag}-load`, 'page renders + LIVE badge', true, `badge="${badgeTxt}"`);
    } catch (e) {
      badgeTxt = await page.textContent('#badge').catch(() => '(no badge)');
      row(`S1-${tag}-load`, 'page renders + LIVE badge', false, `badge="${badgeTxt}"; console=[${logs.join(' | ').slice(0, 200)}]`);
      await browser.close(); return;
    }
    try {
      await page.fill('#q', `Reply with exactly: ENGINE-OK-${tag}`);
      await page.click('button');
      await page.waitForFunction(() => {
        const m = document.querySelectorAll('.msg.bot');
        const last = m[m.length - 1];
        return last && last.textContent.includes('ENGINE-OK-');
      }, { timeout: 90000 });
      row(`S2-${tag}-chat`, 'real chat round-trip via the UI', true, `marker received; ${await page.textContent('#status')}`);
      await page.screenshot({ path: `${SHOTS}/chat-${engineName}.png` });
    } catch (e) {
      const m = await page.$$eval('.msg.bot', els => els.map(x => x.textContent).join('||').slice(-200)).catch(() => '(none)');
      row(`S2-${tag}-chat`, 'real chat round-trip via the UI', false, `lastBot="${m}"; console=[${logs.join(' | ').slice(0, 160)}]`);
      await page.screenshot({ path: `${SHOTS}/chat-${engineName}-FAIL.png` });
    }
  } finally {
    try { await browser.close(); } catch {}
  }
}

for (const [l, n] of [[chromium, 'chromium'], [webkit, 'webkit']]) {
  try { await runEngine(l, n); } catch (e) { row(`S0-${n}-browser`, 'browser launches', false, String(e).slice(0, 150)); }
}

// S3 tunnel-down UX with guaranteed restore
{
  const { browser, page } = await openPage(webkit, 'tunneldown');
  try {
    execSync('launchctl bootout gui/$(id -u)/com.kyanite.ha-crack-tunnel 2>/dev/null || true', { shell: '/bin/bash' });
    await new Promise(r => setTimeout(r, 2500));
    await page.goto('http://127.0.0.1:8936/', { timeout: 15000, waitUntil: 'domcontentloaded' });
    await page.waitForSelector('#badge.bad-down', { timeout: 25000 });
    const badge = await page.textContent('#badge');
    await page.fill('#q', 'hello?');
    await page.click('button');
    await page.waitForFunction(() => {
      const m = document.querySelectorAll('.msg.bot');
      const last = m[m.length - 1];
      return last && (last.textContent.includes('⚠') || last.textContent.includes('failed'));
    }, { timeout: 20000 });
    await page.screenshot({ path: `${SHOTS}/tunnel-down.png` });
    row('S3-tunnel-down-ux', 'tunnel killed -> badge DOWN + explicit chat warning (no silent hang)', true, `badge="${badge}"; warning rendered`);
  } catch (e) {
    row('S3-tunnel-down-ux', 'tunnel killed -> badge DOWN + explicit chat warning (no silent hang)', false, String(e).slice(0, 170));
  } finally {
    try { await browser.close(); } catch {}
    await restoreTunnel();
    await new Promise(r => setTimeout(r, 3000));
  }
}

// S5 restored
{
  try {
    const { browser, page } = await openPage(chromium, 'restored');
    await page.goto('http://127.0.0.1:8936/', { timeout: 15000, waitUntil: 'domcontentloaded' });
    await page.waitForSelector('#badge.bad-live', { timeout: 25000 });
    row('S5-restored', 'after restore, badge LIVE again (self-heal verified)', true, 'badge LIVE');
    await browser.close();
  } catch (e) {
    row('S5-restored', 'after restore, badge LIVE again (self-heal verified)', false, String(e).slice(0, 150));
  }
}

const failed = results.filter(r => r.result === 'fail').length;
console.log(`\nMATRIX: ${results.length} rows, ${failed} failed`);
process.exit(failed ? 1 : 0);
