'use strict';
// Prepared UI-only QA. The coordinator runs it once after independent saved
// review, integration and browser-QA authorization. It never imports a model,
// host reference, shader, scientific runner or review checker.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const {chromium} = require('playwright');
const args = {};
for (let i = 2; i < process.argv.length; i += 2) {
  const key = process.argv[i];
  if (!key?.startsWith('--') || process.argv[i + 1] === undefined) throw Error('Arguments must be --name value pairs');
  args[key.slice(2)] = process.argv[i + 1];
}
for (const key of ['base-url', 'repo', 'report', 'screenshots']) if (!args[key]) throw Error('Missing --' + key);
const repo = path.resolve(args.repo), campaignRelative = 'research/m31-browser-wake-slice-2026-10-16', campaign = path.join(repo, campaignRelative), raw = path.join(campaign, 'raw');
const screenshotDirectory = path.resolve(args.screenshots), reportPath = path.resolve(args.report);
const baseURL = new URL(args['base-url']), intendedURL = new URL('/' + campaignRelative + '/viewer/', baseURL).href;
const IDS = [27, 445, 4500, 988], N = 5000, statusNames = ['unwritten', 'malformed', 'domain invalid', 'early zero', 'evaluated zero', 'positive profile', 'arithmetic invalid'];
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const readJSON = name => JSON.parse(fs.readFileSync(path.join(campaign, name)));
const result = readJSON('results/result.json'), review = readJSON('results/independent-review.json'), termReport = readJSON('raw/terms-assessment.json');
const terminalBudget = readJSON('results/budget.json'), viewerManifest = readJSON('viewer/data.json');
const closurePath = path.resolve(campaign, 'viewer', viewerManifest.files.reviewClosure.url);
if (!closurePath.startsWith(repo + path.sep)) throw Error('Review closure path must remain in repository');
const closureBytes = fs.readFileSync(closurePath), reviewClosure = JSON.parse(closureBytes);
if (sha(closureBytes) !== viewerManifest.files.reviewClosure.sha256 || closureBytes.length !== viewerManifest.files.reviewClosure.bytes) throw Error('Review closure manifest mismatch');
if (!result.terminal || !terminalBudget.terminal || terminalBudget.active || !review.terminal || !review.reviewPass || !reviewClosure.terminal || reviewClosure.active || !reviewClosure.qualifiedReviewClosure) throw Error('UI QA requires terminal science and independently verified saved-evidence integrity');
const evidence = {
  T: fs.readFileSync(path.join(raw, 'terms-gpu.u32')),
  R: {metadata: fs.readFileSync(path.join(raw, 'R-metadata.u32')), terms: fs.readFileSync(path.join(raw, 'R-terms.f64')), sums: fs.readFileSync(path.join(raw, 'R-ordinarySums.f64')), validity: fs.readFileSync(path.join(raw, 'R-sumValidity.u8'))},
  Q: {metadata: fs.readFileSync(path.join(raw, 'Q-metadata.u32')), terms: fs.readFileSync(path.join(raw, 'Q-terms.f64')), sums: fs.readFileSync(path.join(raw, 'Q-ordinarySums.f64')), validity: fs.readFileSync(path.join(raw, 'Q-sumValidity.u8'))}
};
const report = {kind: 'saved-wake-viewer-ui-qa', terminal: false, pass: false, scientificEvaluation: false, scope: 'UI rendering and read-only comparisons against saved words/reports; no new scientific gate', intendedURL, sourceCommit: result.sourceCommit, node: process.version, qaSourceSha256: sha(fs.readFileSync(__filename)), checks: 0, pairChecks: 0, sourceCases: 0, testedRotors: [], screenshots: [], errors: [], evidenceHashes: {gpuTerms: sha(evidence.T), result: sha(fs.readFileSync(path.join(campaign, 'results/result.json'))), review: sha(fs.readFileSync(path.join(campaign, 'results/independent-review.json')))}};
let browser;
function assert(ok, label, detail) {report.checks++;if (!ok) {const error = Error(label);error.detail = detail;throw error;}}
function display(value) {return value === null || value === undefined || !Number.isFinite(value) ? 'Unavailable' : value === 0 ? '0' : Math.abs(value) < .001 ? value.toExponential(6) : value.toPrecision(9);}
function originalRecord(stage, selection, source, rotor) {
  const ordinal = (selection * N + source) * 4 + rotor, gpu = stage === 'T', buffer = gpu ? evidence.T : evidence[stage].metadata, base = ordinal * (gpu ? 80 : 32);
  const status = buffer.readUInt32LE(base + 16), mask = buffer.readUInt32LE(base + 24), idValid = buffer.readUInt32LE(base) === ordinal && buffer.readUInt32LE(base + 4) === IDS[selection] && buffer.readUInt32LE(base + 8) === source && buffer.readUInt32LE(base + 12) === rotor;
  const term = gpu ? buffer.readFloatLE(base + 76) : evidence[stage].terms.readDoubleLE(ordinal * 8), valid = idValid && [3, 4, 5].includes(status) && !!(mask & 2048) && Number.isFinite(term) && term >= 0;
  return {term: valid ? term : null, status};
}
function largestSavedError(selection, rotor) {
  let chosen = 0, maximum = -1;
  for (let source = 0; source < N; source++) {const t = originalRecord('T', selection, source, rotor), r = originalRecord('R', selection, source, rotor);if (t.term !== null && r.term !== null) {const difference = Math.abs(t.term - r.term);if (difference > maximum) {maximum = difference;chosen = source;}}}
  return chosen;
}
async function selected(page, selection, rotor) {
  await page.locator('#receiver').selectOption(String(selection));await page.locator('#rotor').selectOption(String(rotor));
  assert(await page.locator('body').getAttribute('data-receiver') === String(IDS[selection]), 'Selected receiver identity');
  assert(await page.locator('body').getAttribute('data-rotor') === String(rotor), 'Selected rotor identity');
}
async function sourceCheck(page, selection, rotor, source) {
  await page.locator('#source').fill(String(source));await page.locator('#source').dispatchEvent('change');
  assert(await page.locator('body').getAttribute('data-source') === String(source), 'Inspected source identity');
  for (const [index, stage] of ['R','Q','T'].entries()) {
    const expected = originalRecord(stage, selection, source, rotor), cells = await page.locator('#pair-table tr').nth(index).locator('td').allTextContents();
    assert(cells[0] === stage && cells[1] === display(expected.term) && cells[2] === (statusNames[expected.status] ?? `Unknown status ${expected.status}`), 'Displayed term/status matches original words', {selection, rotor, source, stage, expected: [display(expected.term), statusNames[expected.status]], actual: cells});report.pairChecks++;
  }
  report.sourceCases++;
}
async function snapshot(page, name) {await page.screenshot({path: path.join(screenshotDirectory, name), fullPage: true});report.screenshots.push({file: name, viewport: page.viewportSize(), view: await page.locator('body').getAttribute('data-view')});}
function monitor(page, expectedCorruption = false) {
  const errors = [], prohibited = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => {if (message.type() === 'error' && !(expectedCorruption && message.text().includes('Evidence checksum mismatch'))) errors.push(message.text());});
  page.on('request', request => {const url = new URL(request.url());if (/\/source\/(browser\.(html|js)|experiment\.cjs|wake\.wgsl)$/.test(url.pathname)) prohibited.push(url.pathname);});
  return {errors, prohibited};
}
async function ready(page) {
  await page.goto(intendedURL, {waitUntil: 'networkidle'});await page.waitForSelector('body[data-ready="true"]', {timeout: 20000});
  assert(new URL(page.url()).pathname === '/' + campaignRelative + '/viewer/', 'Intended page pathname');
  assert((await page.title()) === 'M31 · Saved wake-slice evidence', 'Page title identity');
  assert((await page.locator('h1').innerText()).replace(/\s+/g, ' ').trim() === 'One saved scene. Four wake receivers.', 'Visible heading identity');
  assert(await page.locator('body').getAttribute('data-integrity') === 'verified', 'Saved integrity unlocked');
}
(async () => {
  fs.mkdirSync(screenshotDirectory, {recursive: true});fs.mkdirSync(path.dirname(reportPath), {recursive: true});
  browser = await chromium.launch({channel: args['browser-channel'] || 'chrome', headless: true});report.browser = await browser.version();
  const desktop = await browser.newContext({viewport: {width: 1440, height: 1080}, deviceScaleFactor: 1}), page = await desktop.newPage(), desktopMonitor = monitor(page);
  await ready(page);
  assert(await page.locator('body').getAttribute('data-receiver') === '988' && await page.locator('body').getAttribute('data-rotor') === '3', 'Default failed receiver/rotor');
  assert(await page.locator('body').getAttribute('data-color') === 'error-TR' && await page.locator('body').getAttribute('data-view') === 'focused', 'Default error color and focused view');
  assert(await page.locator('body').getAttribute('data-source') === String(largestSavedError(3, 3)), 'Default source is largest saved absolute T−R error');
  assert((await page.locator('#outcome').innerText()).includes('Term-error gate failed'), 'Recorded negative result visible');
  assert((await page.locator('#status').innerText()).includes('Serial reduction was not dispatched'), 'No invented serial result');
  assert(await page.locator('#sum-table tr').count() === 16 && await page.locator('#gate-table tr').count() === 16, 'All16sum and gate rows');
  assert(!fs.existsSync(path.join(raw, 'reduce-gpu.u32')), 'Current scientific evidence contains no serial output');
  for (let index = 0; index < 16; index++) {
    const sums = await page.locator('#sum-table tr').nth(index).locator('td').allTextContents(), gates = await page.locator('#gate-table tr').nth(index).locator('td').allTextContents(), t = termReport.rotors.find(item => item.index === index);
    for (const [column, stage] of [[1,'R'],[2,'Q']]) {const value = evidence[stage].sums.readDoubleLE(index * 8), suffix = evidence[stage].validity[index] === 1 ? '' : ' · partial';assert(sums[column] === display(value) + suffix, 'Displayed reference sum matches retained bytes', {index, stage});}
    assert(sums[3] === display(t.exactStoredTermSum.approximateDisplay), 'Displayed T exact-sum certificate');
    assert(sums[4] === 'Unavailable' && sums[5] === 'Not dispatched', 'Serial sum unavailable for every rotor');
    const expectedGate = [display(t.l1QR.approximateDisplay), display(t.l1TQ.approximateDisplay), display(t.l1TR.approximateDisplay), display(t.l1PlusAllowance.approximateDisplay), 'Unavailable', display(termReport.threshold.referenceSumAllowance.approximateDisplay), 'Unavailable', display(termReport.threshold.epsilon.approximateDisplay), `${t.pass ? 'Term passed' : 'Term FAILED'} · final unavailable`];
    assert(JSON.stringify(gates.slice(1)) === JSON.stringify(expectedGate), 'Displayed gate components match retained report; no new gate arithmetic', {index});
  }
  assert((await page.locator('#gate-table tr').nth(15).innerText()).includes('Term FAILED'), 'Failed conservative row15 visible');
  for (let selection = 0; selection < 4; selection++) for (let rotor = 0; rotor < 4; rotor++) {
    await selected(page, selection, rotor);await page.locator('#color').selectOption('error-TR');
    const largest = largestSavedError(selection, rotor);
    for (const source of [0, IDS[selection], 4999, largest]) await sourceCheck(page, selection, rotor, source);
    await page.locator('#largest').click();assert(await page.locator('body').getAttribute('data-source') === String(largest), 'Largest-error control matches saved words');
    report.testedRotors.push({receiver: IDS[selection], rotor, largestErrorSource: largest});
  }
  await selected(page, 3, 3);await page.locator('#color').selectOption('error-TR');await page.locator('#largest').click();
  for (const color of ['contribution-T','status-T','error-TR']) {await page.locator('#color').selectOption(color);assert(await page.locator('body').getAttribute('data-color') === color, 'Color mode updates');assert((await page.locator('#legend').innerText()).length > 50, 'Legend updates with meaningful content');}
  await page.locator('#links').uncheck();await page.locator('#links').check();assert(await page.locator('#links').isChecked(), 'Contribution links toggle');
  await page.locator('#focus').click();assert(await page.locator('body').getAttribute('data-view') === 'focused', 'Focused camera');assert(Number(await page.locator('body').getAttribute('data-visible-bodies')) < 5000, 'Focused display filters non-contributors');await snapshot(page, 'desktop-focused.png');
  await page.locator('#whole').click();assert(await page.locator('body').getAttribute('data-view') === 'whole', 'Whole-cloud camera');assert(await page.locator('body').getAttribute('data-visible-bodies') === '5000', 'Whole view restores every saved pose');await snapshot(page, 'desktop-whole.png');
  const anchors = await page.locator('a[href]').evaluateAll(elements => elements.map(element => ({url: element.href, text: element.textContent.trim()})));
  assert(anchors.some(item => new URL(item.url).pathname === '/outputs/milestone-31-lab.html'), 'Original M31 local3DBoids replay link');
  for (const url of new Set(anchors.map(item => item.url))) {assert(new URL(url).origin === new URL(intendedURL).origin, 'Evidence link remains on published host');const response = await desktop.request.get(url);assert(response.ok(), 'Evidence/navigation link responds', {path: new URL(url).pathname, status: response.status()});}
  assert(desktopMonitor.errors.length === 0, 'Desktop console/page errors absent', desktopMonitor.errors);assert(desktopMonitor.prohibited.length === 0, 'No scientific runner requests', desktopMonitor.prohibited);
  const mobile = await browser.newContext({viewport: {width: 390, height: 844}, deviceScaleFactor: 1, isMobile: true, hasTouch: true}), mobilePage = await mobile.newPage(), mobileMonitor = monitor(mobilePage);
  await ready(mobilePage);await selected(mobilePage, 3, 3);await sourceCheck(mobilePage, 3, 3, largestSavedError(3, 3));
  assert(await mobilePage.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'No page-level mobile horizontal overflow');
  await mobilePage.locator('#whole').click();await mobilePage.locator('#focus').click();await snapshot(mobilePage, 'mobile-focused.png');
  assert(mobileMonitor.errors.length === 0, 'Mobile console/page errors absent', mobileMonitor.errors);assert(mobileMonitor.prohibited.length === 0, 'Mobile has no scientific runner requests', mobileMonitor.prohibited);
  const corruptContext = await browser.newContext({viewport: {width: 1280, height: 900}}), corruptPage = await corruptContext.newPage(), corruptMonitor = monitor(corruptPage, true), corrupted = Buffer.from(evidence.T);corrupted[0] ^= 1;
  await corruptPage.route('**/' + campaignRelative + '/raw/terms-gpu.u32', route => route.fulfill({status: 200, contentType: 'application/octet-stream', body: corrupted}));
  await corruptPage.goto(intendedURL, {waitUntil: 'networkidle'});await corruptPage.waitForSelector('body[data-integrity="failed"]');
  assert(await corruptPage.locator('body').getAttribute('data-ready') === 'false', 'Corrupt term bytes cannot unlock viewer');
  assert((await corruptPage.locator('#status').innerText()).includes('Evidence checksum mismatch'), 'Corruption rejection is explicit');
  assert(await corruptPage.locator('#scene canvas').count() === 0, 'No scientific scene rendered after integrity rejection');
  assert(corruptMonitor.prohibited.length === 0 && corruptMonitor.errors.length === 0, 'Integrity test introduces no unexpected execution/errors', corruptMonitor);
  report.pass = true;
})().catch(error => {
  let message = String(error.message);for (const replacement of [[repo,'<repository>'],[screenshotDirectory,'<screenshots>'],[reportPath,'<report>']]) message = message.split(replacement[0]).join(replacement[1]);
  report.errors.push({message, detail: error.detail ?? null});process.exitCode = 1;
}).finally(async () => {
  if (browser) await browser.close();report.terminal = true;
  fs.mkdirSync(path.dirname(reportPath), {recursive: true});fs.writeFileSync(reportPath, JSON.stringify(report, null, 2)+'\n');
  console.log(JSON.stringify({pass: report.pass, checks: report.checks, pairChecks: report.pairChecks, sourceCases: report.sourceCases, testedRotors: report.testedRotors.length, screenshots: report.screenshots.map(item => item.file), errors: report.errors}));
});
