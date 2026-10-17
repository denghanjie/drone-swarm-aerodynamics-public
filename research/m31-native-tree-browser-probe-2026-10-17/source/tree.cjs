'use strict';

// SOURCE ONLY: numerical qualification and execution approval are pending.
// This module never evaluates rotor geometry, coefficients, or positive mass.
const LEAF_CAPACITY = 8;
const codec = require('./compact-codec.cjs');
const dictionaries = new WeakMap();

function coverage(mode, n, screen) {
  const evidence = {schema: 'm31-native-center-tree-compact-v1', mode, leafCapacity: LEAF_CAPACITY,
    eligible: screen.eligible, fallback: screen.fallback,
    fallbackReason: screen.fallbackReason, complete: false, n,
    canonicalIds: null, nodes: [], leafDictionary: [], receivers: [],
    counters: {treeNodes: 0, treeLeaves: 0, receiverTraversals: 0,
      nodeVisits: 0, endpointComparisons: 0, culledNodes: 0,
      omittedNonselfCandidates: 0, visitedLeaves: 0, gatheredIndices: 0,
      gatheredNonselfCandidates: 0, completedReceivers: 0}};
  dictionaries.set(evidence, codec.createLeafDictionary(evidence.leafDictionary));
  return evidence;
}

function build(p, n, evidence) {
  // Called only after the unchanged whole-scene F predicate succeeds.
  // Canonical indices already follow strictly increasing stable input IDs.
  const nodes = [], sizes = [];
  function split(members) {
    const id = nodes.length;
    const min = [Infinity, Infinity, Infinity], max = [-Infinity, -Infinity, -Infinity];
    for (const j of members) for (let k = 0; k < 3; k++) {
      const value = p[28 * j + k];
      min[k] = Math.min(min[k], value); max[k] = Math.max(max[k], value);
    }
    const node = {id, min, max, left: null, right: null};
    nodes.push(node); sizes.push(members.length);
    if (evidence) evidence.counters.treeNodes++;
    if (members.length <= LEAF_CAPACITY) {
      node.members = members;
      if (evidence) evidence.counters.treeLeaves++;
      return id;
    }
    let axis = 0, width = max[0] - min[0];
    for (let k = 1; k < 3; k++) {
      const next = max[k] - min[k];
      // Strict greater-than resolves equal widths to the lowest axis.
      if (next > width) { axis = k; width = next; }
    }
    members.sort((a, b) => {
      const av = p[28 * a + axis], bv = p[28 * b + axis];
      return av < bv ? -1 : av > bv ? 1 : a - b;
    });
    const middle = Math.floor(members.length / 2);
    node.left = split(members.slice(0, middle));
    node.right = split(members.slice(middle));
    return id;
  }
  if (evidence) evidence.nodes = nodes;
  const root = split(Array.from({length: n}, (_, j) => j));
  return {nodes, sizes, root};
}

function firstCull(node, p, receiver, counters) {
  // JavaScript subtraction is the original ordinary binary64 RN operation.
  // With finite extrema, monotonicity transfers either endpoint comparison
  // to every member. Equality at +4/-4 is deliberately included.
  for (let axis = 0; axis < 3; axis++) {
    const r = p[28 * receiver + axis];
    const positive = node.min[axis] - r;
    if (counters) counters.endpointComparisons++;
    if (positive >= 4) return {node: node.id, axis, side: 'min-ge4', difference: positive};
    const negative = node.max[axis] - r;
    if (counters) counters.endpointComparisons++;
    if (negative <= -4) return {node: node.id, axis, side: 'max-le-neg4', difference: negative};
  }
  return null;
}

function gather(tree, p, receiver, mode, evidence) {
  const gathered = [], counters = evidence ? evidence.counters : null;
  const leaves = evidence ? [] : null;
  const record = evidence ? {receiver, culled: [], leavesRef: null, gathered: null} : null;
  if (record) { evidence.receivers.push(record); counters.receiverTraversals++; }
  function visit(id) {
    const node = tree.nodes[id];
    if (counters) counters.nodeVisits++;
    const cull = firstCull(node, p, receiver, counters);
    // H0 pays the same predicate and traversal machinery but always descends.
    if (mode === 'H' && cull !== null) {
      if (record) {
        record.culled.push(cull); counters.culledNodes++;
        counters.omittedNonselfCandidates += tree.sizes[id];
      }
      return;
    }
    if (node.left === null) {
      if (record) { leaves.push(id); counters.visitedLeaves++; }
      for (const source of node.members) gathered.push(source);
      return;
    }
    visit(node.left); visit(node.right);
  }
  visit(tree.root);
  // Preserve F's exact source and immediate rotor-consumption order.
  gathered.sort((a, b) => a - b);
  if (record) {
    // Encode the actual sorted array before returning that same array to the classifier.
    record.gathered = codec.encodeIndices(gathered);
    record.leavesRef = dictionaries.get(evidence)(leaves);
  }
  if (counters) {
    counters.gatheredIndices += gathered.length;
    for (const source of gathered) if (source !== receiver) counters.gatheredNonselfCandidates++;
  }
  return gathered;
}

module.exports = {coverage, build, gather, leafCapacity: LEAF_CAPACITY};
