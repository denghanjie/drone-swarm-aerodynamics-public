// Final display contract v2: byte-bound records can be inspected after a failed
// terminal review, with prominent unqualified status. This never upgrades it.
export const ADAPTER_READY = true;
const equal = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const samePin = (a, b) => a?.bytes === b?.bytes && a?.sha256 === b?.sha256;
const requireState = (ok, message) => {if (!ok) throw Error(message);};
export function verifyPublishedEvidence({meta, documents}) {
  const {result, budget, freeze, review, reviewClosure: closure, reviewInputIndex: index, reviewPrepared: prepared} = documents;
  requireState(result.terminal === true && result.invocationComplete === true && budget.terminal === true && budget.active === false && budget.status === 'closed' && budget.attempts === 1 && budget.retryPermitted === false, 'Science is not terminal');
  requireState(budget.processGroupCleanup?.confirmedAbsent === true && budget.timeout === false && budget.outputCapExceeded === false, 'Science resource closure unavailable');
  requireState(closure.terminal === true && closure.active !== true && closure.attempts === 1 && closure.retryPermitted === false && closure.childProcessGroupConfirmedAbsent === true && closure.preparedArtifactsUnchanged === true && closure.timeout === false && closure.outputCapExceeded === false && closure.error === null, 'Review external resource closure unavailable');
  requireState(closure.externalWallSeconds < 90 && closure.subprocessWallSeconds <= 89 && closure.totalOutputBytes <= 33554432 && closure.totalOutputCapBytes === 33554432, 'Review outside frozen resource contract');
  requireState(review.terminal === true && review.completed === true && review.fatal === null && closure.reviewCompleted === true, 'Review did not finish its checks');
  requireState(review.evidenceIntegrityPass === closure.evidenceIntegrityPass && closure.reportSHA256 === meta.files.review.sha256 && closure.reportBytes === meta.files.review.bytes, 'Review report/closure mismatch');
  requireState(closure.preparedManifestSHA256 === meta.files.reviewPrepared.sha256 && closure.bindings['input-index.public.json'] === meta.files.reviewInputIndex.sha256 && closure.bindings['checker.py'] === meta.files.reviewChecker.sha256, 'Review source/index chain mismatch');
  requireState(index.transformation?.privateOriginalSHA256 === closure.bindings['input-index.private.json'], 'Public/private input-index chain mismatch');
  for (const obj of [closure, index]) requireState(obj.sourceCommit === meta.sourceCommit && obj.sourceCommit === result.sourceCommit && obj.freezeSHA256 === meta.files.freeze.sha256, 'Review source/freeze mismatch');
  requireState(meta.reviewContract.version === 2 && meta.reviewContract.checkerSHA256 === meta.files.reviewChecker.sha256 && meta.reviewContract.publicInputIndexSHA256 === meta.files.reviewInputIndex.sha256 && meta.reviewContract.closureSHA256 === meta.files.reviewClosure.sha256, 'Display review contract mismatch');
  const reviewPassed = review.evidenceIntegrityPass === true;
  if (reviewPassed) requireState(closure.completed === true && closure.exitCode === 0 && meta.bindingState === 'bound-terminal-evidence', 'Passing review closure mismatch');
  else requireState(closure.completed === false && closure.exitCode !== 0 && meta.bindingState === 'bound-unqualified-records' && meta.reviewContract.displayMode === 'terminal-review-failed', 'Failed review must remain visibly unqualified');
  const indexed = (group, label) => {const rows = index.files.filter(x => x.group === group && x.label === label);requireState(rows.length === 1, 'Missing or duplicate input-index entry');return rows[0];};
  const sourcePins = freeze.files;
  requireState(sourcePins.length === 53 && sourcePins.every(e => samePin(e, indexed('source', e.path))), 'Frozen source pins differ from reviewed inputs');
  requireState(samePin(meta.files.freeze, indexed('freeze', 'freeze.json')), 'Freeze input pin mismatch');
  requireState(samePin(meta.files.result, indexed('result', 'result.json')) && samePin(meta.files.result, indexed('raw', 'result.json')) && samePin(meta.files.budget, indexed('result', 'budget.json')), 'Terminal result/budget input mismatch');
  for (const e of closure.scientificTerminalPins) requireState(samePin(e,indexed(e.group,e.label)), 'External science pin mismatch');
  for (const [key,name] of [['reviewInputIndex','input-index.public.json'],['reviewChecker','checker.py']]) requireState(samePin(meta.files[key],prepared.files.find(x=>x.name===name)), 'Prepared artifact pin mismatch');
  requireState(equal(meta.receiverIds,result.config.receiverIds) && equal(meta.origins.map(x=>x.offset),result.config.origins) && meta.nSources === result.config.nSources, 'Cohort/configuration mismatch');
  const boundFiles = {};
  const anchors={freeze:indexed('freeze','freeze.json'),result:indexed('result','result.json'),budget:indexed('result','budget.json'),review:{bytes:closure.reportBytes,sha256:closure.reportSHA256},reviewClosure:{bytes:meta.files.reviewClosure.bytes,sha256:meta.reviewContract.closureSHA256},reviewInputIndex:prepared.files.find(x=>x.name==='input-index.public.json'),reviewPrepared:{bytes:meta.files.reviewPrepared.bytes,sha256:closure.preparedManifestSHA256},reviewChecker:prepared.files.find(x=>x.name==='checker.py')};
  for (const [key,spec] of Object.entries(meta.files)) {
    const pin = anchors[key] ?? (spec.rawName ? indexed('raw',spec.rawName) : spec.repoPath ? indexed('source',spec.repoPath) : null);
    requireState(pin && samePin(pin,spec),'File is not bound to original evidence: '+key);
    boundFiles[key]={bytes:pin.bytes,sha256:pin.sha256};
  }
  return {byteBindingsVerified:true,integrityVerified:reviewPassed,reviewPassed,boundFiles,reviewNotice:reviewPassed?'Independent saved-evidence integrity review passed.':'Independent review FAILED two control-stage bookkeeping checks; no complete integrity qualification is claimed. These are hash-bound recorded results for inspection. The unchanged review, source diagnosis and terminal failure remain linked below.'};
}

// Read-only projection: no model, shader, checker, new scientific gate, candidate
// selection, missing vector or missing sum. See ADAPTER-CONTRACT.md.
export function projectPublishedReports({meta, documents}) {
  const result = documents.result;
  for (let o=0;o<2;o++) {for (const q of ['R','Q0','Q1']) requireState(equal(result.references[o][q],documents[`o${o}-${q}-assessment.json`]), 'Embedded reference/report mismatch');}
  for (const c of result.cells) requireState(equal(c,documents[`${c.key}-disposition.json`]), 'Embedded cell/disposition mismatch');
  if (result.terminal !== true || !Array.isArray(result.cells) || result.cells.length !== 6) throw Error('Unexpected coordinate terminal-report shape');
  const campaign = {
    sourceCommit: result.sourceCommit,
    qualified: result.pass,
    outcomeLabel: result.decision === 'no-candidate' ? 'No candidate qualified' : `Recorded decision: ${result.decision ?? result.status}`,
    summary: result.decision === 'no-candidate' ? 'The saved result selects no candidate. All three origin-0 cells qualified. At the translated origin, Q0 failed and A/B were skipped. C’s high/low input reconstruction passed Q1, but its retained GPU term-error gate failed; serial C was not dispatched there. This diagnostic does not establish a backend cause.' : `Recorded terminal status: ${result.status}. Candidate selection and gates are copied from retained reports.`
  };
  const cells = meta.cells.map(descriptor => {
    const saved = result.cells.find(item => item.origin === descriptor.origin && item.arm === descriptor.arm);
    if (!saved || saved.reference !== (descriptor.arm === 'C' ? 'Q1' : 'Q0')) throw Error('Saved cell identity/reference mismatch');
    const ref = result.references?.[descriptor.origin]?.[saved.reference], terms = saved.terms, serial = saved.serial;
    if (!ref) throw Error('Missing matched saved reference assessment');
    const expectedTerms = Boolean(terms), expectedSerial = Boolean(serial);
    if (Boolean(descriptor.terms) !== expectedTerms || Boolean(descriptor.serial) !== expectedSerial) throw Error(`Saved raw/report exposure mismatch: ${saved.key}`);
    const skipped = saved.status === 'skipped-interface-gate';
    const statusKind = saved.status === 'qualified' ? 'qualified' : skipped ? 'skipped' : saved.status?.startsWith('failed-') ? 'failed' : 'unavailable';
    const termLabel = expectedTerms ? terms.completeTermCoverage === true ? '80,000 retained slots' : 'Retained / partial coverage' : skipped ? `Skipped after ${saved.reference} failure` : 'No retained term buffer';
    const serialLabel = expectedSerial ? '16 retained output records' : skipped ? 'Not dispatched · interface gate' : saved.status === 'failed-term-gate' && saved.release?.reductionDispatched === false ? 'Not dispatched · term gate' : 'No retained serial output';
    let note = `Origin ${saved.origin} / arm ${saved.arm}: ${saved.status}. ${saved.reference} is the required matched interface. ${termLabel}; ${serialLabel}.`;
    if (skipped) note += ' No GPU terms or vectors exist for this cell; selecting it does not substitute another arm’s data.';
    if (saved.arm === 'C' && ref.pass === true && terms?.pass === false) note += ' Q1 passed the high/low decoded-input gate, while the GPU term gate failed. These results do not prove compiler reassociation or another backend cause.';
    const rows = Array.from({length: 16}, (_, index) => {
      const q = ref.rotors?.find(item => item.index === index), t = terms?.rotors?.find(item => item.index === index), s = serial?.rotors?.find(item => item.index === index);
      const threshold = serial?.threshold ?? terms?.threshold ?? ref.threshold;
      const gateLabel = s ? `Combined ${s.pass ? 'passed' : 'FAILED'}` : t ? `Term ${t.pass ? 'passed' : 'FAILED'} · combined unavailable` : q ? `${saved.reference} ${q.pass ? 'passed' : 'FAILED'} · GPU unavailable` : 'Not assessed';
      return {index, exactTermSum: t?.exactStoredTermSum ?? null, termSumLabel: t?.qualifiedTermCount === 5000 ? '' : t ? 'partial / unqualified' : '', l1QR: t?.l1QR ?? q?.l1QR ?? null, l1TQ: t?.l1TQ ?? null, l1TR: t?.l1TR ?? null, termPlusAllowance: t?.l1PlusAllowance ?? null, reductionError: s?.absoluteReductionError ?? null, allowance: threshold?.referenceSumAllowance ?? null, combined: s?.combinedConservativeError ?? null, epsilon: threshold?.epsilon ?? null, gateLabel, gatePass: s?.pass ?? t?.pass ?? q?.pass ?? null};
    });
    return {origin: saved.origin, arm: saved.arm, key: saved.key, matchedReference: saved.reference, status: saved.status, statusKind, qualified: saved.qualified, qualificationLabel: saved.qualified === true ? 'Qualified at this origin' : 'Not qualified at this origin', note, availability: {terms: {retained: expectedTerms, label: termLabel}, serial: {retained: expectedSerial, label: serialLabel}}, rows};
  });
  const vectorContrasts = [];
  for (let origin = 0; origin < 2; origin++) for (const comparison of ['B-A', 'C-B']) {
    const report = documents[`o${origin}-${comparison}-vectors-assessment.json`];
    vectorContrasts.push({origin, comparison, available: Boolean(report), label: report ? report.label : 'Not retained · required cell data absent', fields: report?.fields ?? [], diagnosticOnly: report?.diagnosticOnly === true});
  }
  return {campaign, cells, vectorContrasts};
}
