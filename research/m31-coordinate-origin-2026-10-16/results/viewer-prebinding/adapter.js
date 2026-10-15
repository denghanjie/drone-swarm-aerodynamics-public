// Actual terminal report mapping, prepared from the retained JSON schema.
// Review verification remains locked until the real review receipt and closure exist.
export const ADAPTER_READY = false;
export function verifyPublishedEvidence() {
  throw Error('Coordinate campaign independent-review receipt and external closure are not yet bound');
}

// Read-only projection: no model, shader, checker, new scientific gate, candidate
// selection, missing vector or missing sum. See ADAPTER-CONTRACT.md.
export function projectPublishedReports({meta, documents}) {
  const result = documents.result;
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
