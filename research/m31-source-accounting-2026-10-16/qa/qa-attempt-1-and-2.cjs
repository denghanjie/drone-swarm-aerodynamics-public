const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { chromium } = require('playwright');
const pkg = path.resolve(process.argv[2]);
const out = path.resolve(process.argv[3]);
fs.mkdirSync(out, { recursive: true });
const url = 'http://127.0.0.1:8876/research/m31-source-accounting-2026-10-16/viewer/';
const result = JSON.parse(fs.readFileSync(path.join(pkg, 'results/result.json')));
const witness = JSON.parse(fs.readFileSync(path.join(pkg, 'results/witness-stdout.json')));
const report = { kind: 'display-only-qa', browserPath: 'Browser plugin not available; existing Playwright and Chrome', url, deadlineSeconds: 45, startedUtc: new Date().toISOString(), checks: [], console: [], screenshots: [], scientificExecution: false };
let browser;
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
function check(name, pass, detail = '') { report.checks.push({ name, pass: !!pass, detail }); if (!pass) throw new Error(name + ': ' + detail); }
async function shot(page, name, target) {
  const b = await (target || page).screenshot({ path: path.join(out, name), timeout: 5000 });
  report.screenshots.push({ path: name, bytes: b.length, sha256: hash(b) });
  return hash(b);
}
async function run() {
  browser = await chromium.launch({ executablePath: process.env.RESEARCH_CHROME, headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  page.setDefaultTimeout(5000);
  page.on('pageerror', e => report.console.push({ type: 'pageerror', text: e.message }));
  page.on('console', m => { if (['error', 'warning'].includes(m.type())) report.console.push({ type: m.type(), text: m.text() }); });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => document.body.dataset.binding !== 'pending');
  check('identity', page.url() === url && (await page.title()).startsWith('Source accounting'));
  check('meaningful content', (await page.locator('h1').innerText()) === 'The wake ignores motor strength.');
  check('evidence binding', await page.locator('body').getAttribute('data-binding') === 'verified');
  await page.waitForFunction(() => !document.getElementById('reset-camera').disabled);
  check('3D canvas available', await page.locator('#scene canvas').count() === 1);
  check('no framework overlay', await page.locator('vite-error-overlay, nextjs-portal, #webpack-dev-server-client-overlay').count() === 0);
  check('saved row and selector counts', await page.locator('#plane option').count() === 10 && await page.locator('#mode option').count() === 3 && await page.locator('#witness option').count() === 5 && await page.locator('#witness-table tbody tr').count() === 20);
  await shot(page, 'desktop.png');
  await page.locator('#scene').scrollIntoViewIfNeeded();
  await shot(page, 'desktop-scene.png', page.locator('#scene'));
  const fmt = n => n === 0 ? '0' : Number(n.toPrecision(8)).toString();
  for (let i = 0; i < result.planes.length; i++) {
    const p = result.planes[i];
    await page.selectOption('#plane', String(i));
    const cells = await page.locator('#profile-table tbody tr').evaluateAll(rows => rows.map(r => [...r.cells].map(c => c.title)));
    check(`plane ${i} all 41 saved profile records`, JSON.stringify(cells) === JSON.stringify(p.profile.map(v => [v.xi, v.radiusM, v.untruncatedMps, v.radialOnlyMps, v.bothFadesMps].map(String))));
    for (const [mode, key] of Object.entries({ bothFades: 'JBothFadesN', radialOnly: 'JRadialOnlyN', untruncated: 'JUntruncatedN' })) {
      await page.selectOption('#mode', mode);
      const empty = mode === 'bothFades' && p.fadedFieldIdenticallyZero;
      check(`plane ${i} ${mode} state`, await page.locator('#plane-j').innerText() === fmt(p[key]) && await page.locator('#plane-title').innerText() === `s = ${p.downstreamM} m` && await page.locator('#plane-state').getAttribute('data-empty') === String(empty));
      check(`plane ${i} ${mode} scene label`, (await page.locator('#scene').getAttribute('aria-label')).includes(`Selected downstream plane ${p.downstreamM} metres`));
    }
  }
  await page.selectOption('#plane', '8');
  await page.selectOption('#mode', 'bothFades');
  await page.locator('#scene').scrollIntoViewIfNeeded();
  check('zero cutoff explicit', (await page.locator('#plane-state').innerText()).includes('identically zero'));
  await shot(page, 'zero-cutoff.png');
  await page.selectOption('#plane', '1');
  await page.locator('#scene').scrollIntoViewIfNeeded();
  const before = hash(await page.locator('#scene').screenshot());
  for (let i = 0; i < witness.cases.length; i++) {
    const c = witness.cases[i];
    await page.selectOption('#witness', String(i));
    check(`witness ${i} recorded outputs`, await page.locator('#witness-total').innerText() === String(c.sourceTotalNominalN) && await page.locator('#witness-inflows').innerText() === c.fields.map(f => String(f.term)).join(' · ') && await page.locator('#witness-motors').innerText() === c.sourceNominalRotorsN.map(String).join(' · ') && JSON.stringify(JSON.parse(await page.locator('#witness-json').innerText())) === JSON.stringify(c));
    check(`witness ${i} highlighted rows`, await page.locator(`#witness-table tr.selected[data-case-index="${i}"]`).count() === 4);
    await page.locator('#scene').scrollIntoViewIfNeeded();
    check(`witness ${i} scene unchanged`, hash(await page.locator('#scene').screenshot()) === before);
  }
  const bounds = await page.locator('#scene canvas').boundingBox();
  await page.mouse.move(bounds.x + bounds.width / 2, bounds.y + bounds.height / 2);
  await page.mouse.down(); await page.mouse.move(bounds.x + bounds.width / 2 + 90, bounds.y + bounds.height / 2 + 45, { steps: 6 }); await page.mouse.up();
  check('orbit changes displayed scene', hash(await page.locator('#scene').screenshot()) !== before);
  await page.click('#reset-camera'); await page.locator('#scene').scrollIntoViewIfNeeded();
  check('reset restores scene', hash(await page.locator('#scene').screenshot()) === before);
  await page.setViewportSize({ width: 390, height: 844 });
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  check('mobile no page overflow', await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
  await shot(page, 'mobile.png');
  await page.locator('#scene').scrollIntoViewIfNeeded();
  await shot(page, 'mobile-scene.png');
  check('mobile canvas visible', await page.locator('#scene canvas').isVisible());
  check('clean normal console', report.console.length === 0, JSON.stringify(report.console));
  await page.route('**/results/result.json', async route => {
    const original = fs.readFileSync(path.join(pkg, 'results/result.json'), 'utf8');
    const changed = original.replace('0.7167725102581919', '0.7167725102581918');
    check('corruption fixture changes same-length bytes', original !== changed && Buffer.byteLength(original) === Buffer.byteLength(changed));
    await route.fulfill({ status: 200, contentType: 'application/json', body: changed });
  });
  await page.reload({ waitUntil: 'networkidle' });
  await page.waitForFunction(() => document.body.dataset.binding === 'failed');
  check('corrupted evidence refuses display', await page.locator('#verified-content').isHidden() && (await page.locator('#status').innerText()).includes('SHA-256 mismatch') && await page.locator('#scene canvas').count() === 0);
  await shot(page, 'corruption-refused.png');
  report.pass = true;
}
(async () => {
  let timer;
  try { await Promise.race([run(), new Promise((_, reject) => { timer = setTimeout(() => reject(new Error('45-second display deadline')), 45000); })]); }
  catch (e) { report.pass = false; report.error = e.stack.replaceAll(pkg, '<checkpoint>').replaceAll(out, '<qa-output>'); }
  finally {
    clearTimeout(timer);
    if (browser) { await browser.close(); report.browserClosed = true; }
    report.finishedUtc = new Date().toISOString();
    fs.writeFileSync(path.join(out, 'qa.json'), JSON.stringify(report, null, 2) + '\n');
    process.stdout.write(JSON.stringify({ pass: report.pass, checks: report.checks.length, screenshots: report.screenshots.length, browserClosed: report.browserClosed, error: report.error || null }) + '\n');
    process.exitCode = report.pass ? 0 : 1;
  }
})();
