'use strict';
/* SOURCE-ONLY DRAFT. No generation or numerical initialization at import.
 * All hash, geometry, input-audit and state work occurs inside generateFamily.
 * Runtime Math.sqrt is implementation-approximated: pin Node/V8 and retain
 * actual admissions. This generator does not evaluate wake terms or roots.
 * Protocol: design/INDEPENDENT-INPUT-DESIGN.md. No old seed/data is read.
 */

function specification() {
  return {
    version: 1,
    namespace: 'm31.body-load.input.v1/2026-10-16\0',
    hash: 'SHA-256; namespace || u32be(family) || u32be(ell) || u8(stream) || u8(component)',
    streams: { permutation: 0, jitter: 1, tilt: 2, yaw: 3, motorScale: 4, velocity: 5, omega: 6 },
    origin: [.123456789, -.234567891, 1.345678912],
    families: [
      { id: 1, name: 'paired-columns', dimensions: [5, 5, 2], spacing: [.731, .763, .611], tNumerator: 0, tDenominator: 1, hNumerator: 0, hDenominator: 1, bDenominator: 64, componentBound: 5, expectedDesignated: 25, expectedCoreDesignated: 17, expectedThreeNormalDesignated: 23 },
      { id: 2, name: 'tilted-layers', dimensions: [10, 10, 5], spacing: [.731, .763, .611], tNumerator: 21, tDenominator: 200, hNumerator: 1, hDenominator: 3, bDenominator: 96, componentBound: 10, expectedDesignated: 400, expectedCoreDesignated: 298, expectedThreeNormalDesignated: 382 },
      { id: 3, name: 'dense-volume', dimensions: [20, 25, 10], spacing: [.731, .763, .611], tNumerator: 7, tDenominator: 100, hNumerator: 1, hDenominator: 5, bDenominator: 64, componentBound: 22, expectedDesignated: 4500, expectedCoreDesignated: 3370, expectedThreeNormalDesignated: 4281 },
      { id: 4, name: 'broad-sparse-pairs', dimensions: [50, 50, 2], spacing: [3.211, 3.211, .611], tNumerator: 0, tDenominator: 1, hNumerator: 3, hDenominator: 20, bDenominator: 64, componentBound: 112, expectedDesignated: 2500, expectedCoreDesignated: 1872, expectedThreeNormalDesignated: 2343 }
    ],
    geometryAdmission: { quaternionNormError: 1e-10, frameGramError: 1e-10, position: 128, axisComponent: 1.01, offsetComponent: .1, axisZMinimum: .97, designatedDownMinimum: .56, designatedDownMaximum: .66, designatedRadialMaximum: .075, designatedProjectionMinimum: .99, designatedCenterMaximum: .614, nonF32CoordinateFraction: .99 },
    exposureGateR: .25,
    invocation: 'Explicit generateFamily only; no top-level numerical work.'
  };
}

function fail(message, detail) {
  const error = new Error(message);
  error.name = 'InputAdmissionError';
  error.detail = detail;
  throw error;
}
function requireThat(ok, message, detail) { if (!ok) fail(message, detail); }
function dot(a, b) { return (a[0] * b[0] + a[1] * b[1]) + a[2] * b[2]; }
function norm(a) { return Math.sqrt(dot(a, a)); }
function quaternionNorm(q) { return Math.sqrt(((q[0]*q[0] + q[1]*q[1]) + q[2]*q[2]) + q[3]*q[3]); }
function matrix(q) {
  const [x, y, z, w] = q;
  return [
    1 - 2 * (y*y + z*z), 2 * (x*y - z*w), 2 * (x*z + y*w),
    2 * (x*y + z*w), 1 - 2 * (x*x + z*z), 2 * (y*z - x*w),
    2 * (x*z - y*w), 2 * (y*z + x*w), 1 - 2 * (x*x + y*y)
  ];
}
function applyMatrix(m, v) {
  return [
    (m[0]*v[0] + m[1]*v[1]) + m[2]*v[2],
    (m[3]*v[0] + m[4]*v[1]) + m[5]*v[2],
    (m[6]*v[0] + m[7]*v[1]) + m[8]*v[2]
  ];
}
function hamilton(a, b) {
  return [
    ((a[3]*b[0] + b[3]*a[0]) + a[1]*b[2]) - a[2]*b[1],
    ((a[3]*b[1] + b[3]*a[1]) + a[2]*b[0]) - a[0]*b[2],
    ((a[3]*b[2] + b[3]*a[2]) + a[0]*b[1]) - a[1]*b[0],
    a[3]*b[3] - ((a[0]*b[0] + a[1]*b[1]) + a[2]*b[2])
  ];
}
function normalizedTangent(x, y, z) {
  const denominator = Math.sqrt(((1 + x*x) + y*y) + z*z);
  return [x/denominator, y/denominator, z/denominator, 1/denominator];
}
function adjacentPositive64(value, direction) {
  requireThat(Number.isFinite(value) && value > 0 && (direction === 1 || direction === -1), 'Adjacent-value definition', { value, direction });
  const bytes = new ArrayBuffer(8), view = new DataView(bytes);
  view.setFloat64(0, value, false);
  const bits = view.getBigUint64(0, false);
  view.setBigUint64(0, bits + BigInt(direction), false);
  return view.getFloat64(0, false);
}

function generateFamily(familyID, options = {}) {
  const partial = { kind: 'generation', buffers: {}, metadata: { complete: false, completedStates: 0, completedPermutationHashes: 0, completedInverseRows: 0, completedGeometryChecks: 0, lastStage: 'entry', failedFamily: familyID } };
  try { return generateFamilyImplementation(familyID, options, partial); }
  catch (error) {
    const failure = error instanceof Error ? error : new Error(String(error));
    failure.partial = partial; // references only: preserve actual data without recomputation/copy.
    throw failure;
  }
}

function generateFamilyImplementation(familyID, options, partial) {
  const spec = specification();
  const family = spec.families.find(f => f.id === familyID);
  requireThat(family !== undefined, 'Unknown fixed family', { familyID });
  const outerGuard = typeof options.guard === 'function' ? options.guard : () => {};
  const guard = context => { partial.metadata.lastStage = context.stage; partial.metadata.context = context; outerGuard(context); };
  const charge = typeof options.charge === 'function' ? options.charge : () => {};
  guard({ stage: 'generation-start', familyID });
  const crypto = require('node:crypto');
  const [nx, ny, nz] = family.dimensions;
  const N = nx * ny * nz;
  partial.metadata.N = N;
  const namespace = Buffer.from(spec.namespace, 'ascii');
  const message = Buffer.alloc(namespace.length + 10);
  namespace.copy(message);
  message.writeUInt32BE(familyID, namespace.length);
  function digest(ell, stream, component = 0) {
    message.writeUInt32BE(ell, namespace.length + 4);
    message[namespace.length + 8] = stream;
    message[namespace.length + 9] = component;
    charge('generatorHash', 1);
    return crypto.createHash('sha256').update(message).digest();
  }
  function fraction(ell, stream, component = 0) {
    const value = digest(ell, stream, component).readBigUInt64BE(0) >> 11n;
    return Number(value) / 9007199254740992;
  }
  function signed(ell, stream, component = 0) { return 2 * fraction(ell, stream, component) - 1; }

  const permutationDigests = new Uint8Array(32 * N);
  partial.buffers.permutationDigests = permutationDigests;
  const sorted = Array.from({ length: N }, (_, ell) => ell);
  for (let ell = 0; ell < N; ell++) {
    if ((ell & 63) === 0) guard({ stage: 'permutation-hashes', familyID, ell });
    permutationDigests.set(digest(ell, 0), 32 * ell);
    partial.metadata.completedPermutationHashes = ell + 1;
  }
  sorted.sort((a, b) => {
    for (let k = 0; k < 32; k++) {
      const delta = permutationDigests[32*a + k] - permutationDigests[32*b + k];
      if (delta !== 0) return delta;
    }
    return a - b;
  });
  const permutation = Uint32Array.from(sorted);
  const inversePermutation = new Uint32Array(N);
  partial.buffers.permutation = permutation;
  partial.buffers.inversePermutation = inversePermutation;
  partial.metadata.permutationComplete = true;
  for (let id = 0; id < N; id++) { inversePermutation[permutation[id]] = id; partial.metadata.completedInverseRows = id + 1; }
  charge('permutationRows', N);

  guard({ stage: 'frame-construction', familyID });
  const t = family.tNumerator / family.tDenominator;
  const h = family.hNumerator / family.hDenominator;
  const qB = hamilton(normalizedTangent(0, 0, h), normalizedTangent(0, t, 0));
  const B = matrix(qB);
  const frameNormError = Math.abs(quaternionNorm(qB) - 1);
  requireThat(frameNormError <= spec.geometryAdmission.quaternionNormError, 'Frame quaternion norm', { familyID, frameNormError });
  let frameGramError = 0;
  for (let row = 0; row < 3; row++) for (let col = 0; col < 3; col++) {
    const v = ((B[row] * B[col] + B[3+row] * B[3+col]) + B[6+row] * B[6+col]);
    frameGramError = Math.max(frameGramError, Math.abs(v - (row === col ? 1 : 0)));
  }
  requireThat(frameGramError <= spec.geometryAdmission.frameGramError, 'Frame Gram matrix', { familyID, frameGramError });
  const b = 1 / family.bDenominator;
  const fmax = ((2.25 * .027) * 9.81) / 4;
  const normalMinimum = 2 ** -126, subnormalMinimum = 2 ** -149;
  const normalMidpoint = normalMinimum - subnormalMinimum / 2;
  const firstSpecial = [0, 0, 0, 2 ** -1074, 2 ** -151, 2 ** -150,
    adjacentPositive64(2 ** -150, 1), subnormalMinimum,
    normalMinimum - subnormalMinimum, normalMidpoint,
    adjacentPositive64(normalMidpoint, -1), normalMinimum,
    normalMinimum + subnormalMinimum, adjacentPositive64(fmax, -1)];
  const states = new Float64Array(17 * N);
  const coreFlags = new Uint8Array(N);
  const stateValidity = new Uint8Array(N);
  const designatedPairs = new Uint32Array(2 * family.expectedDesignated);
  partial.buffers.states = states;
  partial.buffers.stateValidity = stateValidity;
  partial.buffers.coreFlags = coreFlags;
  partial.buffers.designatedPairs = designatedPairs;
  partial.metadata.completedDesignatedPairs = 0;
  const arms = [[.028,.028,0],[-.028,.028,0],[-.028,-.028,0],[.028,-.028,0]];
  let nonF32Coordinates = 0, maximumQuaternionNormError = 0;
  let minimumAxisZ = Infinity, maximumPositionComponent = 0;
  let designatedCount = 0, coreDesignatedCount = 0, threeNormalDesignatedCount = 0;
  for (let ell = 0; ell < N; ell++) {
    if ((ell & 31) === 0) guard({ stage: 'state-generation', familyID, ell });
    const iz = ell % nz, iy = Math.floor(ell / nz) % ny, ix = Math.floor(ell / (ny * nz));
    const id = inversePermutation[ell];
    const local = [
      (ix - (nx - 1) / 2) * family.spacing[0],
      (iy - (ny - 1) / 2) * family.spacing[1],
      (iz - (nz - 1) / 2) * family.spacing[2]
    ];
    const rotated = applyMatrix(B, local);
    const position = rotated.map((value, k) => (spec.origin[k] + value) + (7 / 10000) * signed(ell, 1, k));
    const tx = b * signed(ell, 2, 0), ty = b * signed(ell, 2, 1);
    const yawTangent = (7 / 5) * signed(ell, 3, 0);
    const q = hamilton(hamilton(qB, normalizedTangent(tx, ty, 0)), normalizedTangent(0, 0, yawTangent));
    const qError = Math.abs(quaternionNorm(q) - 1);
    maximumQuaternionNormError = Math.max(maximumQuaternionNormError, qError);
    requireThat(qError <= spec.geometryAdmission.quaternionNormError, 'Original quaternion norm', { familyID, id, ell, qError });
    const m = matrix(q), axis = applyMatrix(m, [0,0,1]);
    minimumAxisZ = Math.min(minimumAxisZ, axis[2]);
    requireThat(axis.every(x => Number.isFinite(x) && Math.abs(x) <= 1.01) && axis[2] >= .97, 'Generated axis admission', { familyID, id, ell, axis });
    for (let rotor = 0; rotor < 4; rotor++) {
      const offset = applyMatrix(m, arms[rotor]);
      requireThat(offset.every(x => Number.isFinite(x) && Math.abs(x) <= .1), 'Generated offset admission', { familyID, id, ell, rotor, offset });
    }
    const scale = 3 / 4 + fraction(ell, 4) / 4;
    const core = [13/100,37/100,61/100,89/100].map(value => (fmax * scale) * value);
    const residue = ell % 64;
    let motors;
    if (residue >= 16) motors = core;
    else if (residue === 0) motors = [0,0,0,0];
    else if (residue === 1) motors = [fmax,fmax,fmax,fmax];
    else if (residue === 14) motors = [fmax,0,fmax,0];
    else if (residue === 15) motors = [0,fmax,0,fmax];
    else motors = [firstSpecial[residue],core[1],core[2],core[3]];
    const cyclic = ell % 4;
    motors = motors.map((_, k) => motors[(k + cyclic) % 4]);
    requireThat(motors.every(f => Number.isFinite(f) && f >= 0 && f <= fmax), 'Original actual-motor admission', { familyID, id, ell, motors });
    coreFlags[id] = residue >= 16 ? 1 : 0;
    const state = [...position,
      ...[0,1,2].map(k => (1/10) * signed(ell, 5, k)),
      ...q,
      ...[0,1,2].map(k => (1/5) * signed(ell, 6, k)),
      ...motors];
    requireThat(state.length === 17 && state.every(Number.isFinite), 'Finite 17-state admission', { familyID, id, ell });
    for (let k = 0; k < 3; k++) {
      const magnitude = Math.abs(position[k]);
      maximumPositionComponent = Math.max(maximumPositionComponent, magnitude);
      requireThat(magnitude < family.componentBound && magnitude <= 128, 'Position analytical-envelope admission', { familyID, id, ell, component: k, value: position[k] });
      if (Math.fround(position[k]) !== position[k]) nonF32Coordinates++;
    }
    states.set(state, 17 * id);
    stateValidity[id] = 1;
    partial.metadata.completedStates++;
    if (iz < nz - 1) {
      designatedPairs[2 * designatedCount] = id;
      designatedPairs[2 * designatedCount + 1] = inversePermutation[ell + 1];
      designatedCount++;
      partial.metadata.completedDesignatedPairs = designatedCount;
      if (residue >= 16) coreDesignatedCount++;
      if (residue >= 16 || (residue >= 2 && residue <= 13) || residue === 1) threeNormalDesignatedCount++;
    }
    charge('generatedStates', 1);
  }
  requireThat(nonF32Coordinates * 100 >= 99 * 3 * N, 'General non-f32 coordinate fraction', { familyID, N, nonF32Coordinates });
  requireThat(designatedCount === family.expectedDesignated && coreDesignatedCount === family.expectedCoreDesignated && threeNormalDesignatedCount === family.expectedThreeNormalDesignated, 'Fixed input schedule counts', { familyID, designatedCount, coreDesignatedCount, threeNormalDesignatedCount });
  requireThat(coreDesignatedCount * 3 >= designatedCount * 2, 'At least two-thirds designated core stimulus', { familyID, coreDesignatedCount, designatedCount });

  const geometricAudit = { minimumDown: Infinity, maximumDown: -Infinity, maximumRadial: 0, minimumProjection: Infinity, maximumCenter: 0, rotorChecks: 0 };
  for (let pair = 0; pair < designatedCount; pair++) {
    if ((pair & 31) === 0) guard({ stage: 'designated-geometry-audit', familyID, pair });
    const receiver = designatedPairs[2*pair], source = designatedPairs[2*pair+1];
    const rs = states.subarray(17*receiver, 17*receiver+17), ss = states.subarray(17*source, 17*source+17);
    const rm = matrix(rs.subarray(6,10)), sm = matrix(ss.subarray(6,10));
    const ra = applyMatrix(rm,[0,0,1]), sa = applyMatrix(sm,[0,0,1]);
    const center = norm([ss[0]-rs[0],ss[1]-rs[1],ss[2]-rs[2]]);
    const projection = dot(ra,sa);
    geometricAudit.maximumCenter = Math.max(geometricAudit.maximumCenter, center);
    geometricAudit.minimumProjection = Math.min(geometricAudit.minimumProjection, projection);
    requireThat(center < .614 && projection > .99, 'Designated center/projection admission', { familyID, receiver, source, center, projection });
    for (let rotor = 0; rotor < 4; rotor++) {
      const offset = applyMatrix(rm, arms[rotor]);
      const displacement = [0,1,2].map(k => ss[k] - (rs[k] + offset[k]));
      const down = dot(displacement,sa);
      const radial = norm(displacement.map((x,k) => x - down * sa[k]));
      requireThat(Number.isFinite(down) && Number.isFinite(radial) && down >= .56 && down <= .66 && radial < .075, 'Designated rotor geometry admission', { familyID, receiver, source, rotor, down, radial });
      geometricAudit.minimumDown = Math.min(geometricAudit.minimumDown, down);
      geometricAudit.maximumDown = Math.max(geometricAudit.maximumDown, down);
      geometricAudit.maximumRadial = Math.max(geometricAudit.maximumRadial, radial);
      geometricAudit.rotorChecks++;
      partial.metadata.completedGeometryChecks = geometricAudit.rotorChecks;
      charge('designatedGeometryChecks', 1);
    }
  }
  guard({ stage: 'row-materialization', familyID, N });
  const stateRows = Array.from({ length: N }, (_, id) => Array.from(states.subarray(17*id,17*id+17)));
  const designatedReceiverIds = new Uint32Array(designatedCount);
  const designatedSourceIds = new Uint32Array(designatedCount);
  for (let pair = 0; pair < designatedCount; pair++) {
    designatedReceiverIds[pair] = designatedPairs[2*pair];
    designatedSourceIds[pair] = designatedPairs[2*pair+1];
  }
  const audit = {
      version: spec.version, namespace: spec.namespace, hash: spec.hash, family,
      runtime: { node: process.version, v8: process.versions.v8, platform: process.platform, arch: process.arch },
      frameQuaternion: qB, frameMatrix: B, frameNormError, frameGramError,
      fmax, nonF32Coordinates, coordinateCount: 3*N,
      maximumQuaternionNormError, minimumAxisZ, maximumPositionComponent,
      designatedCount, coreDesignatedCount, threeNormalDesignatedCount,
      geometricAudit, exposureGateR: .25,
      scope: 'Generated inputs and fixed geometric admission only; no wake profile, root, load, trajectory or scientific output computed.'
  };
  charge('returnedStateRows', N);
  guard({ stage: 'generation-complete', familyID, N });
  return { familyID, N, states: stateRows, permutation, inverse: inversePermutation, inversePermutation, permutationDigests, designatedReceiverIds, designatedSourceIds, designatedPairs, coreFlags, audit, metadata: audit };
}

module.exports = { specification, generateFamily };
