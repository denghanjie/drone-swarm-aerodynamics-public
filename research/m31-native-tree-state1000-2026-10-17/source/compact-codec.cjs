'use strict';

// Evidence-only helpers. This module imports and executes no numerical kernel.
function need(ok, message) { if (!ok) throw Error(message); }
function encodeIndices(actual) {
  need(Array.isArray(actual), 'compact-indices-array');
  const runs = [];
  let previous = -1;
  for (let i = 0; i < actual.length; i++) {
    const value = actual[i];
    need(Number.isSafeInteger(value) && value >= 0 && !Object.is(value, -0) && value > previous,
      'compact-indices-order');
    if (i > 0 && value === previous + 1) runs[runs.length - 1]++;
    else runs.push(value, 1);
    previous = value;
  }
  // Fixed-width nonnegative integer elements: two elements per run. Ties use literals.
  return runs.length < actual.length ? {kind: 'runs', data: runs} : {kind: 'literal', data: actual.slice()};
}
function equalSequence(a, b) {
  return a.length === b.length && a.every((value, i) => value === b[i]);
}
function createLeafDictionary(entries = []) {
  const buckets = new Map();
  function hash(sequence) {
    let value = 2166136261;
    for (const item of sequence) {
      need(Number.isSafeInteger(item) && item >= 0 && item <= 0xffffffff && !Object.is(item, -0), 'compact-leaf-id');
      value = Math.imul(value ^ item, 16777619) >>> 0;
    }
    return `${sequence.length}:${value}`;
  }
  for (let i = 0; i < entries.length; i++) {
    const key = hash(entries[i]);
    if (!buckets.has(key)) buckets.set(key, []);
    buckets.get(key).push(i);
  }
  return function intern(actual) {
    need(Array.isArray(actual), 'compact-leaves-array');
    const key = hash(actual), matches = buckets.get(key) || [];
    // Hashes select a bucket only. Every shared reference requires exact sequence equality.
    for (const index of matches) if (equalSequence(entries[index], actual)) return index;
    const index = entries.length;
    entries.push(actual.slice()); matches.push(index); buckets.set(key, matches);
    return index;
  };
}
function compactLegacyTree(tree) {
  if (tree === null) return null;
  need(tree && tree.schema === 'm31-native-center-tree-v1', 'compact-legacy-schema');
  const leafDictionary = [], intern = createLeafDictionary(leafDictionary);
  return {...tree, schema: 'm31-native-center-tree-compact-v1', leafDictionary,
    nodes: tree.nodes.map(node => ({...node, min: node.min.slice(), max: node.max.slice(),
      ...(node.members ? {members: node.members.slice()} : {})})),
    canonicalIds: tree.canonicalIds === null ? null : tree.canonicalIds.slice(),
    counters: {...tree.counters},
    receivers: tree.receivers.map(({leaves, gathered, ...record}) => ({...record,
      culled: record.culled.map(cull => ({...cull})),
      leavesRef: intern(leaves), gathered: encodeIndices(gathered)}))};
}
const ignoredSemanticPaths = new Set(['method', 'tree', 'timing', 'diagnostics.buildPhasesMs',
  'diagnostics.geometryWork.gatheredNonselfCandidates',
  'diagnostics.screen.orderedPairVisits', 'diagnostics.screen.componentTests']);
function semanticDifference(left, right, path = '') {
  if (ignoredSemanticPaths.has(path)) return null;
  if (Object.is(left, right)) return null;
  if (left === null || right === null || typeof left !== typeof right || typeof left !== 'object') return path || '<root>';
  if (Array.isArray(left) !== Array.isArray(right)) return path || '<root>';
  if (Array.isArray(left)) {
    if (left.length !== right.length) return `${path}.length`;
    for (let i = 0; i < left.length; i++) {
      const difference = semanticDifference(left[i], right[i], `${path}[${i}]`);
      if (difference !== null) return difference;
    }
    return null;
  }
  const keys = new Set([...Object.keys(left), ...Object.keys(right)]);
  for (const key of keys) {
    const next = path ? `${path}.${key}` : key;
    if (ignoredSemanticPaths.has(next)) continue;
    if (!Object.hasOwn(left, key) || !Object.hasOwn(right, key)) return next;
    const difference = semanticDifference(left[key], right[key], next);
    if (difference !== null) return difference;
  }
  return null;
}
module.exports = {encodeIndices, createLeafDictionary, compactLegacyTree, semanticDifference};
