'use strict';

// Source-only temporal broad phase. No coefficient, geometry preparation,
// admission result or solver value is retained. Do not execute before freeze.
const HALF_WIDTH = 0.125;
const ABS_COORDINATE_LIMIT = 2 ** 20;
const MAX_CANDIDATE_ENTRIES = 2000000;
const SCREEN_THRESHOLD = 4;
const word = new DataView(new ArrayBuffer(8));

function nextUp(value) {
  if (value === Infinity) return value;
  if (value === 0) return Number.MIN_VALUE;
  word.setFloat64(0, value, false);
  const bits = word.getBigUint64(0, false);
  word.setBigUint64(0, value > 0 ? bits + 1n : bits - 1n, false);
  return word.getFloat64(0, false);
}
function nextDown(value) { return -nextUp(-value); }

let cached = null;
let totals;
let last;
function reset() {
  cached = null;
  totals = {queries: 0, builds: 0, reuses: 0, fallbacks: 0,
    invalidations: 0, identityRebuilds: 0, boxExitRebuilds: 0,
    buildOrderedPairs: 0, buildAxisIntervalTests: 0,
    containmentCoordinateTests: 0};
  last = {action: 'reset', reason: null, n: null, candidateEntries: 0};
  return stats();
}
function stats() {
  return {...totals, cached: cached !== null,
    cachedN: cached ? cached.ids.length : 0,
    cachedCandidateEntries: cached ? cached.entries : 0,
    last: {...last}, limits: {halfWidth: HALF_WIDTH,
      absoluteCoordinateLimit: ABS_COORDINATE_LIMIT,
      maxCandidateEntries: MAX_CANDIDATE_ENTRIES,
      screenThreshold: SCREEN_THRESHOLD, outwardEndpointUlps: 1}};
}
function witness() {
  // Explicitly outside query timing. Copies only existing cache state; it does
  // not rebuild, classify a pair, evaluate geometry or mutate the cache.
  if (!cached) return {schema: 'm31-buffered-candidate-witness-v1', cached: false,
    ids: [], boxes: [], rows: [], entries: 0, last: {...last}};
  return {schema: 'm31-buffered-candidate-witness-v1', cached: true,
    ids: cached.ids.slice(), boxes: Array.from(cached.boxes),
    boxLayout: 'six words per canonical ID: xLo,xHi,yLo,yHi,zLo,zHi',
    rows: cached.rows.map(row => row.map(index => cached.ids[index])), entries: cached.entries,
    last: {...last}};
}
function invalidate() {
  if (cached) totals.invalidations++;
  cached = null;
}
function bypass(reason, n) {
  totals.queries++;
  totals.fallbacks++;
  invalidate();
  last = {action: 'fallback', reason, n, candidateEntries: 0};
  return null;
}

// Caller must freshly evaluate the unchanged global screen before calling.
// Null means enumerate all current sources; never truncate a candidate row.
function rowsFor(p, n, ids, guard = () => {}) {
  totals.queries++;
  function fallback(reason) {
    totals.fallbacks++;
    invalidate();
    last = {action: 'fallback', reason, n, candidateEntries: 0};
    return null;
  }
  if (!Array.isArray(ids) || ids.length !== n ||
      !Number.isSafeInteger(n) || n < 1 || p.length !== 28 * n) {
    return fallback('identity-or-prepared-shape');
  }
  for (let i = 0; i < n; i++) {
    guard();
    if (!Number.isSafeInteger(ids[i]) || ids[i] < 0 || Object.is(ids[i], -0) ||
        (i > 0 && ids[i] <= ids[i - 1])) return fallback('identity-domain-or-order');
    for (let k = 0; k < 3; k++) {
      const value = p[28 * i + k];
      if (!Number.isFinite(value) || Math.abs(value) > ABS_COORDINATE_LIMIT) {
        return fallback('absolute-coordinate-bound');
      }
    }
  }

  let reason = 'cold';
  if (cached) {
    reason = cached.ids.length !== n ? 'count-change' : null;
    if (!reason) for (let i = 0; i < n; i++) {
      if (cached.ids[i] !== ids[i]) { reason = 'id-change'; break; }
    }
    if (reason) totals.identityRebuilds++;
    if (!reason) {
      for (let i = 0; i < n && !reason; i++) {
        guard();
        for (let k = 0; k < 3; k++) {
          const value = p[28 * i + k], at = 6 * i + 2 * k;
          totals.containmentCoordinateTests++;
          if (value < cached.boxes[at] || value > cached.boxes[at + 1]) {
            reason = 'box-exit'; totals.boxExitRebuilds++; break;
          }
        }
      }
    }
    if (!reason) {
      totals.reuses++;
      last = {action: 'reuse', reason: 'all-current-centers-inside-stored-boxes',
        n, candidateEntries: cached.entries};
      return cached.rows;
    }
  }

  // Publish no partially rebuilt cache, including on a cooperative-guard throw.
  invalidate();
  last = {action: 'building', reason, n, candidateEntries: 0};
  const boxes = new Float64Array(6 * n);
  for (let i = 0; i < n; i++) {
    guard();
    for (let k = 0; k < 3; k++) {
      const value = p[28 * i + k];
      const lo = nextDown(value - HALF_WIDTH), hi = nextUp(value + HALF_WIDTH);
      if (!Number.isFinite(lo) || !Number.isFinite(hi) || lo > value || hi < value) {
        return fallback('nonfinite-or-invalid-box');
      }
      boxes[6 * i + 2 * k] = lo;
      boxes[6 * i + 2 * k + 1] = hi;
    }
  }
  const rows = Array.from({length: n}, () => []);
  let entries = 0;
  for (let i = 0; i < n; i++) {
    guard();
    for (let j = 0; j < n; j++) {
      if ((j & 1023) === 0) guard();
      if (i === j) continue;
      totals.buildOrderedPairs++;
      let excluded = false;
      for (let k = 0; k < 3; k++) {
        const receiverAt = 6 * i + 2 * k, sourceAt = 6 * j + 2 * k;
        // Monotonic binary64 subtraction encloses the exact current *rounded*
        // subtraction for any pair of stored-box members. Equality screens out.
        const lowDifference = boxes[sourceAt] - boxes[receiverAt + 1];
        const highDifference = boxes[sourceAt + 1] - boxes[receiverAt];
        totals.buildAxisIntervalTests++;
        if (lowDifference >= SCREEN_THRESHOLD || highDifference <= -SCREEN_THRESHOLD) {
          excluded = true; break;
        }
      }
      if (!excluded) {
        if (entries >= MAX_CANDIDATE_ENTRIES) return fallback('candidate-entry-cap');
        // Canonical indices are valid only with the exact stored ID vector.
        // witness() resolves them to public source IDs outside query timing.
        rows[i].push(j); entries++;
      }
    }
  }
  cached = {ids: ids.slice(), boxes, rows, entries};
  totals.builds++;
  last = {action: 'build', reason, n, candidateEntries: entries};
  return rows;
}

reset();
module.exports = {rowsFor, bypass, reset, stats, witness,
  limits: Object.freeze({halfWidth: HALF_WIDTH,
    absoluteCoordinateLimit: ABS_COORDINATE_LIMIT,
    maxCandidateEntries: MAX_CANDIDATE_ENTRIES,
    screenThreshold: SCREEN_THRESHOLD, outwardEndpointUlps: 1})};
