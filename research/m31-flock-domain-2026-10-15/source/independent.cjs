'use strict';

/* Independent geometry-only M28 branch oracle.
 * No imports, field amplitude, receiver-force law, dynamics, or integration.
 * Input pose: [x,y,z,qx,qy,qz,qw]. Quaternions are never normalized here.
 * This module has been prepared by static reasoning; no poses were evaluated.
 *
 * prepare(poses) -> {positions,axes,worldrotors}
 * classifyReceiver(prepared,i) -> {
 *   receiver, codes: Uint8Array(4*N), counts: Array(8),
 *   centerChecks, eligible, nearEvents
 * }
 * Code at 4*j+k identifies source j / receiving rotor k. Self and excluded
 * source centers remain zero. Counts include all 4*N entries, including self.
 * Near events include every code 3 or 4, in source-then-rotor order.
 *
 * Tilt validity is a separate global gate for the caller. Classification here
 * remains hypothetical even when a source or receiver exceeds that gate.
 * For nonunit quaternions the same unnormalized matrix algebra is applied;
 * its output must not be interpreted as a validated rigid rotation.
 */

const a = 0.028;
const P = Object.freeze({
  a,
  D: 2 * Math.sqrt(2) * a,
  minDown: 2.5,
  nearRadius: 0.15,
  downCutoff: 2.5,
  radialCutoff: 3,
  spread: 0.07668,
  origin: -5.817,
  neighborRadius: 3
});

const CODES = Object.freeze({
  SELF_OR_OUTSIDE_CENTER: 0,
  NONPOSITIVE_DOWNSTREAM: 1,
  BEYOND_DOWNSTREAM_CUTOFF: 2,
  NEAR_INVALID: 3,
  NEAR_SKIPPED: 4,
  FAR_RADIAL_OUTSIDE: 5,
  RETAINED_ZERO_PROJECTION: 6,
  RETAINED_POSITIVE_SUPPORT: 7
});

const rotorOffsets = Object.freeze([
  Object.freeze([ a,  a]),
  Object.freeze([-a,  a]),
  Object.freeze([-a, -a]),
  Object.freeze([ a, -a])
]);

function prepare(poses) {
  if (!Array.isArray(poses)) throw new TypeError('poses must be an array');
  const positions = new Array(poses.length);
  const axes = new Array(poses.length);
  const worldrotors = new Array(poses.length);
  for (let i = 0; i < poses.length; i++) {
    const p = poses[i];
    if (!p || p.length !== 7 || !Array.from(p).every(Number.isFinite)) {
      throw new TypeError('pose ' + i + ' must contain seven finite numbers');
    }
    const [px, py, pz, x, y, z, w] = p;
    positions[i] = [px, py, pz];

    // Explicit quaternion matrix, independent of the production double-cross
    // rotation. No norm, normalization, Euler conversion, or model helper.
    const m00 = 1 - 2 * (y*y + z*z);
    const m01 = 2 * (x*y - z*w);
    const m02 = 2 * (x*z + y*w);
    const m10 = 2 * (x*y + z*w);
    const m11 = 1 - 2 * (x*x + z*z);
    const m12 = 2 * (y*z - x*w);
    const m20 = 2 * (x*z - y*w);
    const m21 = 2 * (y*z + x*w);
    const m22 = 1 - 2 * (x*x + y*y);
    axes[i] = [m02, m12, m22];
    worldrotors[i] = rotorOffsets.map(([rx, ry]) => [
      px + (m00*rx + m01*ry),
      py + (m10*rx + m11*ry),
      pz + (m20*rx + m21*ry)
    ]);
  }
  return {positions, axes, worldrotors};
}

function classifyReceiver(prepared, i) {
  const {positions, axes, worldrotors} = prepared;
  const n = positions.length;
  if (!Number.isInteger(i) || i < 0 || i >= n) {
    throw new RangeError('receiver index is outside the prepared pose array');
  }
  const codes = new Uint8Array(4*n);
  const counts = Array(8).fill(0);
  counts[0] = 4*n;
  const nearEvents = [];
  let centerChecks = 0;
  let eligible = 0;
  const receiverCenter = positions[i];
  const receiverAxis = axes[i];

  // Direct all-source loop: no spatial grid, candidate list, or original API.
  for (let j = 0; j < n; j++) {
    if (j === i) continue;
    centerChecks++;
    const source = positions[j];
    const distance = Math.hypot(
      receiverCenter[0] - source[0],
      receiverCenter[1] - source[1],
      receiverCenter[2] - source[2]
    );
    if (!(distance < P.neighborRadius)) continue;
    eligible++;
    const sourceAxis = axes[j];

    for (let k = 0; k < 4; k++) {
      const point = worldrotors[i][k];
      const dx = source[0] - point[0];
      const dy = source[1] - point[1];
      const dz = source[2] - point[2];
      const down = dx*sourceAxis[0] + dy*sourceAxis[1] + dz*sourceAxis[2];
      let code;

      if (down <= 0) {
        code = CODES.NONPOSITIVE_DOWNSTREAM;
      } else if (down >= P.downCutoff) {
        code = CODES.BEYOND_DOWNSTREAM_CUTOFF;
      } else {
        const radial = Math.hypot(
          dx - down*sourceAxis[0],
          dy - down*sourceAxis[1],
          dz - down*sourceAxis[2]
        );
        if (down < P.minDown * P.D) {
          code = radial < P.nearRadius ? CODES.NEAR_INVALID : CODES.NEAR_SKIPPED;
          nearEvents.push({source: j, rotor: k, down, radial, code});
        } else {
          const normalizedDown = down / P.D;
          const half = P.spread * (normalizedDown - P.origin) * P.D;
          if (radial >= P.radialCutoff * half) {
            code = CODES.FAR_RADIAL_OUTSIDE;
          } else {
            const cosine = Math.max(0,
              receiverAxis[0]*sourceAxis[0] +
              receiverAxis[1]*sourceAxis[1] +
              receiverAxis[2]*sourceAxis[2]
            );
            code = cosine <= 0 ? CODES.RETAINED_ZERO_PROJECTION : CODES.RETAINED_POSITIVE_SUPPORT;
          }
        }
      }
      codes[4*j + k] = code;
      counts[0]--;
      counts[code]++;
    }
  }
  return {receiver: i, codes, counts, centerChecks, eligible, nearEvents};
}

module.exports = {P, CODES, prepare, classifyReceiver};
