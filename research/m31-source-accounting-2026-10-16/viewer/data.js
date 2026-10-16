const FILES = ['results/result.json', 'results/witness-stdout.json'];
const finite = value => typeof value === 'number' && Number.isFinite(value);
function require(condition, message) { if (!condition) throw new Error(message); }
function numbers(object, keys, label) { require(object && keys.every(key => finite(object[key])), `Invalid numeric ${label}`); }
function validateResult(r) {
  require(r?.kind === 'finite-source-accounting-result', 'Unexpected result kind');
  require(typeof r.numericalGatePass === 'boolean' && r.JIsMeasuredThrust === false && r.newPhysicalMeasurements === 0 && r.fieldPlaneExcludesReceiverCenterGate === true, 'Unexpected result scope');
  numbers(r.constants, ['D', 'rotorRadius', 'nominalWeightN'], 'constants');
  require(r.constants.D > 0 && r.constants.rotorRadius > 0, 'Invalid display dimensions');
  numbers(r, ['untruncatedJOverWeight', 'radialSquaredProfileRetention'], 'summary');
  numbers(r.convergence512To1024, ['untruncatedAbsoluteDifference', 'radialFadedAbsoluteDifference'], 'convergence');
  require(Array.isArray(r.planes) && r.planes.length === 10, 'Expected ten saved planes');
  let previous = -Infinity;
  for (const p of r.planes) {
    numbers(p, ['downstreamM', 'halfWidthM', 'nominalRadialCutoffM', 'centerlineUntruncatedMps', 'downstreamFade', 'JUntruncatedN', 'JRadialOnlyN', 'JBothFadesN', 'JBothOverNominalWeight'], 'plane');
    require(p.downstreamM > previous && p.halfWidthM > 0 && typeof p.fadedFieldIdenticallyZero === 'boolean', 'Invalid plane metadata');
    previous = p.downstreamM;
    require(Array.isArray(p.profile) && p.profile.length === 41, 'Expected 41 saved profile samples');
    let radius = -Infinity;
    for (const point of p.profile) {
      numbers(point, ['xi', 'radiusM', 'untruncatedMps', 'radialOnlyMps', 'bothFadesMps'], 'profile sample');
      require(point.radiusM > radius && point.radiusM >= 0 && point.xi >= 0 && ['untruncatedMps', 'radialOnlyMps', 'bothFadesMps'].every(k => point[k] >= 0), 'Invalid profile ordering or speed');
      radius = point.radiusM;
    }
  }
}
function validateWitness(w) {
  require(w && w.calls === 20 && Array.isArray(w.cases) && w.cases.length === 5, 'Expected five cases and twenty saved pair calls');
  require(typeof w.sourceIndependentInTheseCases === 'boolean' && typeof w.stimulusAdmitted === 'boolean' && typeof w.scope === 'string', 'Invalid witness status');
  const ids = new Set();
  for (const c of w.cases) {
    require(typeof c.id === 'string' && c.id.length > 0 && !ids.has(c.id), 'Invalid witness case ID'); ids.add(c.id);
    require(Array.isArray(c.sourceNominalRotorsN) && c.sourceNominalRotorsN.length === 4 && c.sourceNominalRotorsN.every(finite) && finite(c.sourceTotalNominalN), 'Invalid saved motor values');
    require(Array.isArray(c.fields) && c.fields.length === 4, 'Expected four saved fields per case');
    c.fields.forEach(f => numbers(f, ['symbol', 'term', 'down', 'radial', 'projection', 'center', 'validity', 'stage'], 'witness field'));
  }
}
async function fetchBytes(url) {
  const response = await fetch(url, { cache: 'no-store', credentials: 'same-origin' });
  require(response.ok, `Evidence unavailable (${response.status}): ${url}`);
  const bytes = await response.arrayBuffer();
  require(bytes.byteLength <= 2 * 1024 * 1024, 'Evidence exceeds the display input limit');
  return bytes;
}
function parse(bytes, label) {
  try { return JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)); }
  catch { throw new Error(`Invalid UTF-8 JSON: ${label}`); }
}
export async function loadEvidence() {
  require(globalThis.crypto?.subtle, 'SHA-256 verification requires HTTPS or localhost');
  const binding = parse(await fetchBytes('./binding.json'), 'binding.json');
  require(binding?.version === 1 && Array.isArray(binding.files) && binding.files.length === 2, 'Invalid binding manifest');
  require(new Set(binding.files.map(x => x.path)).size === 2 && binding.files.every(x => FILES.includes(x.path)), 'Binding must contain exactly the two declared result paths');
  const records = await Promise.all(FILES.map(async path => {
    const pin = binding.files.find(x => x.path === path);
    require(Number.isSafeInteger(pin.bytes) && pin.bytes > 0 && pin.bytes <= 2 * 1024 * 1024 && /^[a-f0-9]{64}$/.test(pin.sha256), `Invalid binding entry: ${path}`);
    const bytes = await fetchBytes(`../${path}`);
    require(bytes.byteLength === pin.bytes, `Byte-count mismatch: ${path}`);
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    const hash = Array.from(new Uint8Array(digest), x => x.toString(16).padStart(2, '0')).join('');
    require(hash === pin.sha256, `SHA-256 mismatch: ${path}`);
    return { path, bytes: bytes.byteLength, sha256: hash, value: parse(bytes, path) };
  }));
  validateResult(records[0].value); validateWitness(records[1].value);
  return { result: records[0].value, witness: records[1].value, receipts: records.map(({ value, ...pin }) => pin) };
}
