"""Static source editing only; never compile a shader or evaluate a model."""
import argparse, hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);args=p.parse_args()
source=args.baseline.read_text()
expected='ba780bc60e68bf66d29d3170c74abfd648568ddc835f7aebc7edee13dde2b108'
if hashlib.sha256(args.baseline.read_bytes()).hexdigest()!=expected:raise SystemExit('Baseline source hash mismatch')
def replace(old,new):
 global source
 if source.count(old)!=1:raise SystemExit('Static source edit anchor mismatch: '+old[:60])
 source=source.replace(old,new)
def block(start,end,new):
 global source
 a=source.index(start);b=source.index(end,a);source=source[:a]+new+'\n\n'+source[b:]
replace('// STATIC DRAFT ONLY. Not compiled or executed.\n// Explicit prepared-geometry port of independent-I grouping and factored fade.\n// Global original/packed tilt admission belongs to the host.\n// See API.md and controls.json for exact layouts and synthetic-control scope.', '''// STATIC COORDINATE-ORIGIN DRAFT. Not compiled or executed.
// Derived from the published wake slice; policies/profile/constants unchanged.
// A/B share exact input bytes. C appends position residuals only.
// Returned vectors expose values, not a guarantee about backend operation order.
// Host owns global original/packed tilt and semantic high+low admission.
// See KERNEL-CONTRACT.md, schema.json and controls.json.''')
replace('const CONTROL_COUNT: u32 = 16u;', '''const CONTROL_COUNT: u32 = 20u;
const ARM_A: u32 = 0u;
const ARM_B: u32 = 1u;
const ARM_C: u32 = 2u;''')
replace('const V_TERM: u32 = 2048u;', '''const V_TERM: u32 = 2048u;
const V_CENTER_DELTA: u32 = 0x7000u;
const V_ROTOR_DELTA: u32 = 0x38000u;''')
replace('  pad0: u32, pad1: u32,\n}', '''  pad0: u32, pad1: u32,
  lx: u32, ly: u32, lz: u32, pad2: u32,
}''')
replace('struct Control { words: array<u32, 32>, }','struct Control { words: array<u32, 40>, }')
replace('// Scalar u32 members: 80-byte stride, no implicit vec3 padding.','// Scalar u32 members: 104-byte stride, no implicit vec3 padding.')
replace('  fadeDownBits: u32, fadeRadialBits: u32, termBits: u32,\n}', '''  fadeDownBits: u32, fadeRadialBits: u32, termBits: u32,
  centerDeltaXBits: u32, centerDeltaYBits: u32, centerDeltaZBits: u32,
  rotorDeltaXBits: u32, rotorDeltaYBits: u32, rotorDeltaZBits: u32,
}''')
replace('@group(0) @binding(1) var<storage, read> nodes: array<Node>;', '''// A/B: 5000*8 words. C: 5000*12 words. Shape is checked before loads.
@group(0) @binding(1) var<storage, read> nodes: array<u32>;''')
replace('         n.pad0 == 0u && n.pad1 == 0u;', '''         finiteBits(n.lx) && finiteBits(n.ly) && finiteBits(n.lz) &&
         n.pad0 == 0u && n.pad1 == 0u && n.pad2 == 0u;''')
replace('fn axis(n: Node) -> vec3<f32> {', '''fn lowPosition(n: Node) -> vec3<f32> {
  return vec3<f32>(bitcast<f32>(n.lx), bitcast<f32>(n.ly), bitcast<f32>(n.lz));
}
fn nodeStride(armKind: u32) -> u32 { return select(8u, 12u, armKind == ARM_C); }
fn loadNode(index: u32, armKind: u32) -> Node {
  let base = index * nodeStride(armKind);
  var result = Node(nodes[base], nodes[base + 1u], nodes[base + 2u],
                    nodes[base + 3u], nodes[base + 4u], nodes[base + 5u],
                    nodes[base + 6u], nodes[base + 7u], 0u, 0u, 0u, 0u);
  if (armKind == ARM_C) {
    result.lx = nodes[base + 8u]; result.ly = nodes[base + 9u];
    result.lz = nodes[base + 10u]; result.pad2 = nodes[base + 11u];
  }
  return result;
}
fn rotorDisplacement(armKind: u32, sourcePosition: vec3<f32>,
                     receiverPosition: vec3<f32>, offset: vec3<f32>,
                     centerDelta: vec3<f32>) -> vec3<f32> {
  if (armKind == ARM_A) {
    let point = receiverPosition + offset;
    return sourcePosition - point;
  }
  return centerDelta - offset;
}
fn axis(n: Node) -> vec3<f32> {''')
replace('                    0u, 0u, 0u, 0u, 0u, 0u);', '''                    0u, 0u, 0u, 0u, 0u, 0u,
                    0u, 0u, 0u, 0u, 0u, 0u);''')
replace('                routing: u32) -> TermRecord {\n  var out = blank', '                routing: u32, armKind: u32) -> TermRecord {\n  var out = blank')
replace('  let sa = axis(source);\n  let arm', '''  let sa = axis(source);
  let receiverLow = lowPosition(receiver);
  let sourceLow = lowPosition(source);
  // 2^-17 is an exact residual guard. Validate before any geometric operation.
  if (any(abs(receiverLow) > vec3<f32>(0.00000762939453125f)) ||
      any(abs(sourceLow) > vec3<f32>(0.00000762939453125f))) { return out; }
  if (armKind != ARM_C && (receiver.lx != 0u || receiver.ly != 0u ||
      receiver.lz != 0u || source.lx != 0u || source.ly != 0u || source.lz != 0u)) {
    return out;
  }
  let arm''')
replace('  let center = length(sp - rp);', '''  // Written expressions describe the intervention, not a backend order promise.
  let highDifference = sp - rp;
  var centerDelta = highDifference;
  if (armKind == ARM_C) {
    let lowDifference = sourceLow - receiverLow;
    centerDelta = highDifference + lowDifference;
  }
  if (!finiteFloat(centerDelta.x) || !finiteFloat(centerDelta.y) ||
      !finiteFloat(centerDelta.z) || any(abs(centerDelta) > vec3<f32>(257.0f))) {
    return invalidArithmetic(out);
  }
  out.centerDeltaXBits = bitcast<u32>(centerDelta.x);
  out.centerDeltaYBits = bitcast<u32>(centerDelta.y);
  out.centerDeltaZBits = bitcast<u32>(centerDelta.z);
  out.validityMask = out.validityMask | V_CENTER_DELTA;
  let center = length(centerDelta);''')
replace('  let point = rp + arm;\n  let displacement = sp - point;', '''  let displacement = rotorDisplacement(armKind, sp, rp, arm, centerDelta);
  if (!finiteFloat(displacement.x) || !finiteFloat(displacement.y) ||
      !finiteFloat(displacement.z) || any(abs(displacement) > vec3<f32>(258.0f))) {
    return invalidArithmetic(out);
  }
  out.rotorDeltaXBits = bitcast<u32>(displacement.x);
  out.rotorDeltaYBits = bitcast<u32>(displacement.y);
  out.rotorDeltaZBits = bitcast<u32>(displacement.z);
  out.validityMask = out.validityMask | V_ROTOR_DELTA;''')
block('@compute @workgroup_size(64)\nfn termsMain', 'fn rawControlValid', '''fn termsForArm(ordinal: u32, armKind: u32) {
  if (ordinal >= arrayLength(&terms)) { return; }
  let selection = ordinal / (SOURCE_COUNT * 4u);
  let source = (ordinal / 4u) % SOURCE_COUNT;
  let rotor = ordinal % 4u;
  terms[ordinal] = blank(ordinal, UNSET, source, rotor, 0u);
  if (ordinal >= TERM_COUNT || arrayLength(&terms) != TERM_COUNT ||
      arrayLength(&nodes) != SOURCE_COUNT * nodeStride(armKind) ||
      arrayLength(&offsets) != 16u || !selectedValid() || !constantsValid()) { return; }
  let receiver = selectedIDs[selection];
  terms[ordinal] = preparedTerm(ordinal, receiver, source, rotor,
                               loadNode(receiver, armKind), loadNode(source, armKind),
                               offsets[selection * 4u + rotor], 0u, armKind);
}
@compute @workgroup_size(64)
fn termsA(@builtin(global_invocation_id) invocation: vec3<u32>) { termsForArm(invocation.x, ARM_A); }
@compute @workgroup_size(64)
fn termsB(@builtin(global_invocation_id) invocation: vec3<u32>) { termsForArm(invocation.x, ARM_B); }
@compute @workgroup_size(64)
fn termsC(@builtin(global_invocation_id) invocation: vec3<u32>) { termsForArm(invocation.x, ARM_C); }''')
block('fn rawControlValid', 'fn scalarControl', '''fn rawControlValid(input: Control, ordinal: u32, armKind: u32) -> bool {
  if (input.words[0] != ordinal || input.words[1] > 1u || input.words[2] > 1u ||
      input.words[3] != 0u || input.words[15] != 0u || input.words[19] != 0u ||
      input.words[23] != 0u || input.words[27] != 0u || input.words[31] != 0u ||
      input.words[35] != 0u || input.words[39] != 0u) { return false; }
  // Check every scalar/high/low raw exponent before any reinterpretation.
  for (var i = 4u; i < 40u; i = i + 1u) {
    if (!finiteBits(input.words[i])) { return false; }
  }
  if (input.words[1] == 0u) {
    for (var i = 12u; i < 40u; i = i + 1u) {
      if (input.words[i] != 0u) { return false; }
    }
  } else {
    for (var i = 4u; i < 12u; i = i + 1u) {
      if (input.words[i] != 0u) { return false; }
    }
  }
  if (armKind != ARM_C) {
    for (var i = 32u; i < 40u; i = i + 1u) {
      if (input.words[i] != 0u) { return false; }
    }
  }
  return true;
}''')
block('@compute @workgroup_size(64)\nfn controlsMain', 'fn acceptedTerm', '''fn controlsForArm(ordinal: u32, armKind: u32) {
  if (ordinal >= arrayLength(&controlOutputs)) { return; }
  controlOutputs[ordinal] = blank(ordinal, 0u, 1u, 0u, F_CONTROL);
  if (ordinal >= CONTROL_COUNT || arrayLength(&controlOutputs) != CONTROL_COUNT ||
      arrayLength(&controls) != CONTROL_COUNT) { return; }
  let input = controls[ordinal];
  let sourceID = select(1u, 0u, input.words[2] == 1u);
  var routing = F_CONTROL;
  if (input.words[1] == 1u) { routing = routing | F_PREPARED_CONTROL; }
  let base = blank(ordinal, 0u, sourceID, 0u, routing);
  controlOutputs[ordinal] = base;
  if (!rawControlValid(input, ordinal, armKind) || !constantsValid()) { return; }
  if (input.words[1] == 0u) {
    controlOutputs[ordinal] = scalarControl(input, base);
    return;
  }
  let source = Node(input.words[12], input.words[13], input.words[14],
                    input.words[20], input.words[21], input.words[22], 0u, 0u,
                    input.words[32], input.words[33], input.words[34], 0u);
  let receiver = Node(input.words[16], input.words[17], input.words[18],
                      input.words[24], input.words[25], input.words[26], 0u, 0u,
                      input.words[36], input.words[37], input.words[38], 0u);
  let offset = Offset(input.words[28], input.words[29], input.words[30], 0u);
  controlOutputs[ordinal] = preparedTerm(ordinal, 0u, sourceID, 0u,
                                        receiver, source, offset, routing, armKind);
}
@compute @workgroup_size(64)
fn controlsA(@builtin(global_invocation_id) invocation: vec3<u32>) { controlsForArm(invocation.x, ARM_A); }
@compute @workgroup_size(64)
fn controlsB(@builtin(global_invocation_id) invocation: vec3<u32>) { controlsForArm(invocation.x, ARM_B); }
@compute @workgroup_size(64)
fn controlsC(@builtin(global_invocation_id) invocation: vec3<u32>) { controlsForArm(invocation.x, ARM_C); }

fn vectorPayloadValid(record: TermRecord) -> bool {
  let centerMask = record.validityMask & V_CENTER_DELTA;
  let rotorMask = record.validityMask & V_ROTOR_DELTA;
  if (centerMask == 0u) {
    if (record.centerDeltaXBits != 0u || record.centerDeltaYBits != 0u ||
        record.centerDeltaZBits != 0u) { return false; }
  } else {
    if (centerMask != V_CENTER_DELTA || !finiteBits(record.centerDeltaXBits) ||
        !finiteBits(record.centerDeltaYBits) || !finiteBits(record.centerDeltaZBits)) { return false; }
    let delta = vec3<f32>(bitcast<f32>(record.centerDeltaXBits),
                          bitcast<f32>(record.centerDeltaYBits), bitcast<f32>(record.centerDeltaZBits));
    if (any(abs(delta) > vec3<f32>(257.0f))) { return false; }
  }
  if (rotorMask == 0u) {
    if (record.rotorDeltaXBits != 0u || record.rotorDeltaYBits != 0u ||
        record.rotorDeltaZBits != 0u) { return false; }
  } else {
    if (rotorMask != V_ROTOR_DELTA || !finiteBits(record.rotorDeltaXBits) ||
        !finiteBits(record.rotorDeltaYBits) || !finiteBits(record.rotorDeltaZBits)) { return false; }
    let delta = vec3<f32>(bitcast<f32>(record.rotorDeltaXBits),
                          bitcast<f32>(record.rotorDeltaYBits), bitcast<f32>(record.rotorDeltaZBits));
    if (any(abs(delta) > vec3<f32>(258.0f))) { return false; }
  }
  return true;
}''')
replace('      record.routingFlags >= F_CONTROL || !finiteBits(record.termBits))', '      record.routingFlags >= F_CONTROL || !finiteBits(record.termBits) ||\n      !vectorPayloadValid(record))')
# Only the main-buffer reducer requires vector-augmented masks; scalar controls
# intentionally keep the old reached masks.
replace('return record.validityMask == 2049u && record.routingFlags == F_OUTSIDE;', 'return record.validityMask == 30721u && record.routingFlags == F_OUTSIDE;')
replace('return record.validityMask == 2051u;', 'return record.validityMask == 260099u;')
replace('return record.validityMask == 2055u;', 'return record.validityMask == 260103u;')
replace('return record.validityMask == 2127u;', 'return record.validityMask == 260175u;')
replace('if (record.validityMask != 4095u ||', 'if (record.validityMask != 262143u ||')
root=Path(__file__).resolve().parent
(root/'coordinate.wgsl').write_text(source)
print('Static shader source written; no parser/compiler or numerical evaluation.')
