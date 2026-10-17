'use strict';
// UNADOPTED draft alternative; prefer extending the prior motion-feedback adapter.
// Retained for design provenance only; not an executable experiment allocation.
// UNEXECUTED source candidate. This module defines a new projected-attitude
// numerical adapter; it does not alter any qualified model or old integrator.
// No execution is authorized by its presence. See DESIGN.md.
const PARAMS = Object.freeze({m: .027, g: 9.81,
  inertia: Object.freeze([1.4e-5, 1.4e-5, 2.17e-5]),
  motorTau: .04, yawRatio: 7.94e-12 / 3.16e-10});
const spin = Object.freeze([1, -1, 1, -1]);
function need(value, reason) { if (!value) throw new Error(reason); }
function vector(value, n, reason) {
  need(Array.isArray(value) && value.length === n &&
    value.every(Number.isFinite), reason);
}
function cross(a, b) { return [a[1]*b[2]-a[2]*b[1],
  a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]; }
function rotate(q, v) {
  const t = cross(q, v).map(x => 2*x), u = cross(q, t);
  return v.map((x, k) => x + q[3]*t[k] + u[k]);
}
function projectState(state) {
  vector(state, 17, 'state-shape-or-nonfinite');
  need(state.slice(13).every(x => x > 0), 'nominal-force-domain');
  const out = state.slice(), q = out.slice(6, 10), n = Math.hypot(...q);
  need(Number.isFinite(n) && n > 0, 'quaternion-norm');
  out.splice(6, 4, ...q.map(x => x/n));
  return out;
}
function derivativeFromTotalLoad(projectedState, command, load) {
  // Caller MUST query native loads on exactly projectedState and prove that
  // binding independently. This low-level function cannot establish it itself.
  vector(projectedState, 17, 'state-shape-or-nonfinite');
  vector(command, 4, 'command-shape-or-nonfinite');
  need(command.every(x => x >= 0), 'negative-command');
  need(projectedState.slice(13).every(x => x > 0), 'nominal-force-domain');
  need(load && typeof load === 'object', 'load-shape');
  vector(load.worldForce, 3, 'force-shape-or-nonfinite');
  vector(load.worldMoment, 3, 'moment-shape-or-nonfinite');
  const q = projectedState.slice(6, 10), w = projectedState.slice(10, 13);
  need(Math.abs(Math.hypot(...q)-1) <= 1e-10, 'projected-quaternion-required');
  // Model total force replaces nominal collective; gravity is separate.
  const acceleration = load.worldForce.map(x => x/PARAMS.m);
  acceleration[2] -= PARAMS.g;
  // Lever-arm moment is delivered in world coordinates. Convert once to body.
  // Nominal roll/pitch is REPLACED, never added. Retaining nominal reaction yaw
  // is an explicit provisional actuator assumption, not measured aerodynamics.
  const torque = rotate([-q[0], -q[1], -q[2], q[3]], load.worldMoment);
  torque[2] += projectedState.slice(13).reduce(
    (sum, force, r) => sum + spin[r]*PARAMS.yawRatio*force, 0);
  const gyro = cross(w, w.map((x, k) => x*PARAMS.inertia[k]));
  const angularAcceleration = torque.map((x, k) => (x-gyro[k])/PARAMS.inertia[k]);
  const qv = q.slice(0,3), qw = cross(qv,w);
  const dq = [...w.map((x,k) => .5*(q[3]*x+qw[k])),
    -.5*qv.reduce((sum,x,k) => sum+x*w[k],0)];
  // The state retains nominal motor thrust, not downwash-modified thrust.
  const motor = command.map((x,r) => (x-projectedState[13+r])/PARAMS.motorTau);
  const result = [...projectedState.slice(3,6), ...acceleration,
    ...dq, ...angularAcceleration, ...motor];
  need(result.every(Number.isFinite), 'derivative-nonfinite');
  return result;
}
module.exports = {PARAMS, projectState, derivativeFromTotalLoad};
