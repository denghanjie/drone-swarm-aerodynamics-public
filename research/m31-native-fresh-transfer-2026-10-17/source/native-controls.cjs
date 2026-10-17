'use strict';
// Source-only prospective controls. No kernel import or execution here.
// Every additional input below is a literal with at most two drones.
// Expectations are authored requirements, not observed results.
const inherited = require('./vendor/controls.cjs');
const additionalControlIds = Object.freeze([
  'isolated-linear-nominal',
  'reverse-stable-id-order',
  'duplicate-id',
  'unsafe-id',
  'negative-zero-id',
  'short-state',
  'sparse-state',
  'active-unequal-pair',
  'subnormal-coupled-output',
  'nominal-zero',
  'nominal-negative',
  'normalizer-overflow',
  'subnormal-isolated',
  'quaternion-domain',
  'unsupported-near-pair',
  'neighbor-exact-three',
  'downcut-exact',
  'downcut-below',
  'projection-zero-farfield',
  'equal-z-order-refusal',
  'tilted-unequal-linear-loads',
  'tilted-symmetric-cancellation',
  'nonfinite-unused-velocity',
  'empty-input',
]);
function additionalControls() {
  return [
    {id: 'isolated-linear-nominal', method: 'F', expectedStatus: 'native-success',
      purpose: 'Zero contraction retains each nominal force and materializes all four native loads.',
      input: {drones: [{id: 7, state: [0,0,0, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}]}},
    {id: 'reverse-stable-id-order', method: 'F', expectedStatus: 'native-success',
      purpose: 'Canonical output IDs must be [2,9]; input rows remain owned by the caller.',
      input: {drones: [{id: 9, state: [4,0,0, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}, {id: 2, state: [0,0,0, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}]}},
    {id: 'duplicate-id', method: 'F', expectedStatus: 'input-refused',
      purpose: 'Duplicate stable IDs are refused.',
      input: {drones: [{id: 2, state: [0,0,0, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}, {id: 2, state: [4,0,0, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}]}},
    {id: 'unsafe-id', method: 'F', expectedStatus: 'input-refused',
      purpose: 'Unsafe integer IDs are refused.',
      input: {drones: [{id: 9007199254740992, state: [0,0,0, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}]}},
    {id: 'negative-zero-id', method: 'F', expectedStatus: 'input-refused',
      purpose: 'Negative-zero IDs are refused; state signed zeros are permitted.',
      input: {drones: [{id: -0, state: [0,0,0, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}]}},
    {id: 'short-state', method: 'F', expectedStatus: 'input-refused',
      purpose: 'The row must have exactly17 dense entries.',
      input: {drones: [{id: 1, state: [0,0,0,0,0,0,0,0,0,1,0,0,0,.03,.04,.05]}]}},
    {id: 'sparse-state', method: 'F', expectedStatus: 'input-refused',
      purpose: 'A literal hole is refused rather than inherited or skipped.',
      input: {drones: [{id: 1, state: [0,,0,0,0,0,0,0,0,1,0,0,0,.03,.04,.05,.06]}]}},
    {id: 'active-unequal-pair', method: 'F', expectedStatus: 'native-success',
      purpose: 'A substantial positive wake checks linear f*x delivered forces and complete support.',
      input: {drones: [{id: 1, state: [0,0,0,0,0,0,0,0,0,1,0,0,0,.03,.04,.05,.06]}, {id: 2, state: [0,0,.6,0,0,0,0,0,0,1,0,0,0,.03,.04,.05,.06]}]}},
    {id: 'subnormal-coupled-output', method: 'F', expectedStatus: 'numerical-failure',
      purpose: 'Native finite bisection with a tiny receiver force must not return zero loads as success.',
      input: {drones: [{id: 1, state: [0,0,0, 0,0,0, 0,0,0,1, 0,0,0, 5e-324,5e-324,5e-324,5e-324]}, {id: 2, state: [0,0,.6, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}]}},
    {id: 'nominal-zero', method: 'F', expectedStatus: 'input-refused',
      purpose: 'Zero nominal force is refused.',
      input: {drones: [{id: 1, state: [0,0,0,0,0,0,0,0,0,1,0,0,0,0,.04,.05,.06]}]}},
    {id: 'nominal-negative', method: 'F', expectedStatus: 'input-refused',
      purpose: 'Negative nominal force is refused.',
      input: {drones: [{id: 1, state: [0,0,0,0,0,0,0,0,0,1,0,0,0,-.03,.04,.05,.06]}]}},
    {id: 'normalizer-overflow', method: 'F', expectedStatus: 'numerical-failure',
      purpose: 'Finite positive force with overflowing native normalizer is unsuccessful.',
      input: {drones: [{id: 1, state: [0,0,0,0,0,0,0,0,0,1,0,0,0,1.7976931348623157e308,.04,.05,.06]}]}},
    {id: 'subnormal-isolated', method: 'F', expectedStatus: 'native-success',
      purpose: 'Positive subnormal forces in a zero-contraction scene retain their delivered force words.',
      input: {drones: [{id: 1, state: [0,0,0, 0,0,0, 0,0,0,1, 0,0,0, 5e-324,5e-324,5e-324,5e-324]}]}},
    {id: 'quaternion-domain', method: 'F', expectedStatus: 'domain-refused',
      purpose: 'Native quaternion/axis/offset admission is retained.',
      input: {drones: [{id: 1, state: [0,0,0,0,0,0,0,0,0,2,0,0,0,.03,.04,.05,.06]}]}},
    {id: 'unsupported-near-pair', method: 'F', expectedStatus: 'domain-refused',
      purpose: 'Unsupported near field is refused before projection or solve.',
      input: {drones: [{id: 1, state: [0,0,0, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}, {id: 2, state: [0,0,.02,0,0,0,0,0,0,1,0,0,0,.03,.04,.05,.06]}]}},
    {id: 'neighbor-exact-three', method: 'F', expectedStatus: 'native-success',
      purpose: 'Exact neighbor cutoff produces no positive term.',
      input: {drones: [{id: 1, state: [0,0,0, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}, {id: 2, state: [0,0,3,0,0,0,0,0,0,1,0,0,0,.03,.04,.05,.06]}]}},
    {id: 'downcut-exact', method: 'F', expectedStatus: 'native-success',
      purpose: 'Exact down cutoff produces no positive term.',
      input: {drones: [{id: 1, state: [0,0,0, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}, {id: 2, state: [0,0,2.5,0,0,0,0,0,0,1,0,0,0,.03,.04,.05,.06]}]}},
    {id: 'downcut-below', method: 'F', expectedStatus: 'native-success',
      purpose: 'Fixed adjacent down-cut word exercises the active fade side without tuning.',
      input: {drones: [{id: 1, state: [0,0,0, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}, {id: 2, state: [0,0,2.4999999999999996,0,0,0,0,0,0,1,0,0,0,.03,.04,.05,.06]}]}},
    {id: 'projection-zero-farfield', method: 'F', expectedStatus: 'native-success',
      purpose: 'An admitted far-field geometry can have zero native receiver projection.',
      input: {drones: [{id: 1, state: [0,0,0, 0,0,0, 0,.7071067811865476,0,.7071067811865476, 0,0,0, .03,.04,.05,.06]}, {id: 2, state: [0,0,.6, 0,0,0, 0,0,0,1, 0,0,0, .03,.04,.05,.06]}]}},
    {id: 'equal-z-order-refusal', method: 'F', expectedStatus: 'domain-refused',
      purpose: 'Positive tilted wake with equal z and wrong stable-ID direction is refused.',
      input: {drones: [{id: 1, state: [0,0,0, 0,0,0, 0,.7071067811865476,0,.7071067811865476, 0,0,0, .03,.04,.05,.06]}, {id: 2, state: [.6,0,0,0,0,0,0,.7071067811865476,0,.7071067811865476,0,0,0,.03,.04,.05,.06]}]}},
    {id: 'tilted-unequal-linear-loads', method: 'F', expectedStatus: 'native-success',
      purpose: 'Tilted unequal rotor forces check native world-force and signed moment construction.',
      input: {drones: [{id: 5, state: [0,0,0, 0,0,0, 0,.7071067811865476,0,.7071067811865476, 0,0,0, .03,.04,.05,.06]}]}},
    {id: 'tilted-symmetric-cancellation', method: 'F', expectedStatus: 'native-success',
      purpose: 'Symmetric rotor forces exercise signed world-moment cancellation.',
      input: {drones: [{id: 5, state: [0,0,0,0,0,0,0,.3826834323650898,0,.9238795325112867,0,0,0,.05,.05,.05,.05]}]}},
    {id: 'nonfinite-unused-velocity', method: 'F', expectedStatus: 'input-refused',
      purpose: 'Unused raw velocity fields are still required finite.',
      input: {drones: [{id: 1, state: [0,0,0,Infinity,0,0,0,0,0,1,0,0,0,.03,.04,.05,.06]}]}},
    {id: 'empty-input', method: 'F', expectedStatus: 'input-refused',
      purpose: 'Empty input is explicitly unsupported.',
      input: {drones: []}},
  ];
}
function evaluateControl(spec, result) {
  const checks = [];
  const check = (id, pass) => checks.push({id, pass: pass === true});
  check('expected-status', result.status === spec.expectedStatus);
  if (spec.expectedReason !== undefined) check('expected-reason', result.reason === spec.expectedReason);
  if (result.status === 'native-success') {
    check('canonical-ids', result.ids.every((id, i) => i === 0 || result.ids[i - 1] < id));
    check('all-load-words-consumed', result.consumption.loadWords === 11 * result.ids.length);
    check('all-ids-and-status-consumed', result.consumption.identityWords === result.ids.length &&
      result.consumption.status === 'native-success' && result.consumption.statusCharacters === 14);
    check('delivered-linear-forces', result.loads.every((load, i) =>
      load.rotor.every((value, r) => Object.is(value, result.raw[i].state[13 + r] * result.solution[i].rotors[r].x) &&
        Object.is(value, result.solution[i].rotors[r].T))));
    if (spec.id === 'active-unequal-pair') {
      check('all-four-positive-receiver-terms', result.coefficients.K.length === 4 &&
        Array.from(result.coefficients.offsets).every((v, i) => v === Math.min(i, 4)));
      check('nontrivial-rotor-ratios', result.solution[0].rotors.every(rotor => rotor.x > 0 && rotor.x < 1));
      check('source-ratios-one', result.solution[1].rotors.every(rotor => rotor.x === 1));
    }
    if (['neighbor-exact-three', 'downcut-exact', 'projection-zero-farfield'].includes(spec.id)) {
      check('zero-positive-support', result.coefficients.K.length === 0);
    }
    if (spec.id === 'downcut-below') check('positive-fade-side', result.coefficients.K.length === 4);
    if (spec.id === 'reverse-stable-id-order') {
      check('stable-id-association', result.ids[0] === 2 && result.ids[1] === 9 &&
        result.raw[0].state[0] === 0 && result.raw[1].state[0] === 4);
    }
    if (spec.id === 'subnormal-isolated') {
      check('subnormal-force-words', result.loads[0].rotor.every(value => Object.is(value, 5e-324)) &&
        Object.is(result.loads[0].collective, 2e-323));
    }
    // These analytic nominal-load expectations use an a priori absolute 1e-14
    // control tolerance, separate from the four primary offline 1e-8 gates.
    const expected = {
      'isolated-linear-nominal': {collective: .18, force: [0, 0, .18], moment: [-.00112, 0, 0]},
      'tilted-unequal-linear-loads': {collective: .18, force: [.18, 0, 0], moment: [0, 0, .00112]},
      'tilted-symmetric-cancellation': {collective: .2,
        force: [.1414213562373095, 0, .1414213562373095], moment: [0, 0, 0]}
    }[spec.id];
    if (expected) {
      const load = result.loads[0], close = (a, b) => Number.isFinite(a) && Math.abs(a - b) <= 1e-14;
      check('nominal-ratios-one', result.solution[0].rotors.every(rotor => rotor.x === 1));
      check('analytic-collective', close(load.collective, expected.collective));
      check('analytic-world-force', load.worldForce.every((v, k) => close(v, expected.force[k])));
      check('analytic-world-moment', load.worldMoment.every((v, k) => close(v, expected.moment[k])));
    }
  }
  return {schema: 'm31-native-microcontrol-check-v1', id: spec.id, checks,
    pass: checks.length > 0 && checks.every(item => item.pass)};
}
module.exports = {additionalControlIds, additionalControls, evaluateControl,
  inheritedControlIds: inherited.controlIds, inheritedControls: inherited.controls,
  ownershipSequence: inherited.ownershipSequence};
