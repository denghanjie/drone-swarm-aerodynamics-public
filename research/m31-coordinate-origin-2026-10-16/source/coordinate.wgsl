// STATIC COORDINATE-ORIGIN DRAFT. Not compiled or executed.
// Derived from the published wake slice; policies/profile/constants unchanged.
// A/B share exact input bytes. C appends position residuals only.
// Returned vectors expose values, not a guarantee about backend operation order.
// Host owns global original/packed tilt and semantic high+low admission.
// See KERNEL-CONTRACT.md, schema.json and controls.json.

const SOURCE_COUNT: u32 = 5000u;
const SELECTION_COUNT: u32 = 4u;
const TERM_COUNT: u32 = 80000u;
const CONTROL_COUNT: u32 = 20u;
const ARM_A: u32 = 0u;
const ARM_B: u32 = 1u;
const ARM_C: u32 = 2u;
const UNSET: u32 = 0xffffffffu;
const CONTINUE_POLICY: u32 = 8u;

const MALFORMED: u32 = 1u;
const DOMAIN_INVALID: u32 = 2u;
const VALID_ZERO: u32 = 3u;
const PROFILE_ZERO: u32 = 4u;
const PROFILE_POSITIVE: u32 = 5u;
const ARITHMETIC_INVALID: u32 = 6u;

const V_CENTER: u32 = 1u;
const V_DOWN: u32 = 2u;
const V_RADIAL: u32 = 4u;
const V_HALF: u32 = 8u;
const V_DOT: u32 = 16u;
const V_PROJECTION: u32 = 32u;
const V_NORMALIZED_DOWN: u32 = 64u;
const V_XI: u32 = 128u;
const V_SPEED: u32 = 256u;
const V_FADE_DOWN: u32 = 512u;
const V_FADE_RADIAL: u32 = 1024u;
const V_TERM: u32 = 2048u;
const V_CENTER_DELTA: u32 = 0x7000u;
const V_ROTOR_DELTA: u32 = 0x38000u;

const F_SELF: u32 = 1u;
const F_OUTSIDE: u32 = 2u;
const F_DOWN_FADE: u32 = 4u;
const F_RADIAL_FADE: u32 = 8u;
const F_CONTROL: u32 = 16u;
const F_PREPARED_CONTROL: u32 = 32u;

struct Constants { words: array<u32, 16>, }
struct Node {
  px: u32, py: u32, pz: u32,
  ax: u32, ay: u32, az: u32,
  pad0: u32, pad1: u32,
  lx: u32, ly: u32, lz: u32, pad2: u32,
}
struct Offset { x: u32, y: u32, z: u32, pad: u32, }
struct Control { words: array<u32, 40>, }

// Scalar u32 members: 104-byte stride, no implicit vec3 padding.
struct TermRecord {
  ordinal: u32, receiverID: u32, sourceID: u32, rotor: u32,
  status: u32, policyCode: u32, validityMask: u32, routingFlags: u32,
  centerNormBits: u32, downBits: u32, radialBits: u32,
  halfWidthBits: u32, axisDotBits: u32, projectionBits: u32,
  normalizedDownBits: u32, xiBits: u32, normalizedSpeedBits: u32,
  fadeDownBits: u32, fadeRadialBits: u32, termBits: u32,
  centerDeltaXBits: u32, centerDeltaYBits: u32, centerDeltaZBits: u32,
  rotorDeltaXBits: u32, rotorDeltaYBits: u32, rotorDeltaZBits: u32,
}
struct SumRecord {
  selectionIndex: u32, receiverID: u32, rotor: u32,
  status: u32, validityMask: u32, termCount: u32,
  sumBits: u32, firstBadSlot: u32,
}

@group(0) @binding(0) var<storage, read> constants: Constants;
// A/B: 5000*8 words. C: 5000*12 words. Shape is checked before loads.
@group(0) @binding(1) var<storage, read> nodes: array<u32>;
@group(0) @binding(2) var<storage, read> offsets: array<Offset>;
@group(0) @binding(3) var<storage, read> selectedIDs: array<u32>;
@group(0) @binding(4) var<storage, read_write> terms: array<TermRecord>;
@group(0) @binding(5) var<storage, read> controls: array<Control>;
@group(0) @binding(6) var<storage, read_write> controlOutputs: array<TermRecord>;
@group(0) @binding(7) var<storage, read_write> sums: array<SumRecord>;

fn finiteBits(bits: u32) -> bool {
  return (bits & 0x7f800000u) != 0x7f800000u;
}
fn finiteFloat(value: f32) -> bool { return finiteBits(bitcast<u32>(value)); }
fn c(index: u32) -> f32 { return bitcast<f32>(constants.words[index]); }
fn dot3(a: vec3<f32>, b: vec3<f32>) -> f32 {
  return a.x * b.x + a.y * b.y + a.z * b.z;
}

fn constantsValid() -> bool {
  // Complete raw validation precedes all constant reinterpretation.
  for (var i = 0u; i < 14u; i = i + 1u) {
    if (!finiteBits(constants.words[i])) { return false; }
  }
  if (constants.words[14] != 0u || constants.words[15] != 0u) { return false; }
  // The host separately requires exact identity with every frozen word.
  if (c(0u) < 0.05f || c(0u) > 0.1f ||
      c(1u) < 10.0f || c(1u) > 11.0f ||
      c(2u) < 0.07f || c(2u) > 0.08f ||
      c(3u) < -6.0f || c(3u) > -5.0f ||
      c(11u) < 0.9f || c(11u) > 1.0f ||
      c(12u) < 1.0f || c(12u) > 10.0f ||
      c(13u) < 0.4f || c(13u) > 0.5f) { return false; }
  // Fixed policy constants and fixed fade denominators (0.5 and 1).
  return constants.words[4] == 0x40200000u &&
         constants.words[5] == 0x40400000u &&
         constants.words[6] == 0x3e19999au &&
         constants.words[7] == 0x40000000u &&
         constants.words[8] == 0x40200000u &&
         constants.words[9] == 0x40000000u &&
         constants.words[10] == 0x40400000u;
}

fn rawNodeValid(n: Node) -> bool {
  return finiteBits(n.px) && finiteBits(n.py) && finiteBits(n.pz) &&
         finiteBits(n.ax) && finiteBits(n.ay) && finiteBits(n.az) &&
         finiteBits(n.lx) && finiteBits(n.ly) && finiteBits(n.lz) &&
         n.pad0 == 0u && n.pad1 == 0u && n.pad2 == 0u;
}
fn rawOffsetValid(o: Offset) -> bool {
  return finiteBits(o.x) && finiteBits(o.y) && finiteBits(o.z) && o.pad == 0u;
}
fn position(n: Node) -> vec3<f32> {
  return vec3<f32>(bitcast<f32>(n.px), bitcast<f32>(n.py), bitcast<f32>(n.pz));
}
fn lowPosition(n: Node) -> vec3<f32> {
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
fn axis(n: Node) -> vec3<f32> {
  return vec3<f32>(bitcast<f32>(n.ax), bitcast<f32>(n.ay), bitcast<f32>(n.az));
}

fn blank(ordinal: u32, receiver: u32, source: u32, rotor: u32,
         routing: u32) -> TermRecord {
  return TermRecord(ordinal, receiver, source, rotor,
                    MALFORMED, UNSET, 0u, routing,
                    0u, 0u, 0u, 0u, 0u, 0u,
                    0u, 0u, 0u, 0u, 0u, 0u,
                    0u, 0u, 0u, 0u, 0u, 0u);
}
fn invalidArithmetic(record: TermRecord) -> TermRecord {
  var out = record;
  out.status = ARITHMETIC_INVALID;
  out.validityMask = out.validityMask & ~V_TERM;
  out.termBits = 0u;
  return out;
}
fn finishEarly(record: TermRecord, code: u32) -> TermRecord {
  var out = record;
  out.policyCode = code;
  out.termBits = 0u;
  if (code == 3u) {
    out.status = DOMAIN_INVALID;
    out.validityMask = out.validityMask & ~V_TERM;
  } else {
    out.status = VALID_ZERO;
    out.validityMask = out.validityMask | V_TERM;
  }
  return out;
}

// Shared composite policy. stage bounds which scalars have been computed:
// 0=center, 1=down, 2=radial/near, 3=half-width/radial support, 4=projection.
// Earlier decisions always precede later conditions, including in controls.
fn policy(stage: u32, isSelf: bool, center: f32, down: f32,
          radial: f32, halfWidth: f32, projection: f32) -> u32 {
  if (isSelf || center >= c(5u)) { return 0u; }
  if (stage == 0u) { return CONTINUE_POLICY; }
  if (down <= 0.0f) { return 1u; }
  if (down >= c(8u)) { return 2u; }
  if (stage == 1u) { return CONTINUE_POLICY; }
  if (down < c(4u) * c(0u)) {
    if (radial < c(6u)) { return 3u; }
    return 4u;
  }
  if (stage == 2u) { return CONTINUE_POLICY; }
  if (radial >= c(10u) * halfWidth) { return 5u; }
  if (stage == 3u) { return CONTINUE_POLICY; }
  if (projection <= 0.0f) { return 6u; }
  return 7u;
}

fn factoredFade(start: f32, end: f32, value: f32) -> f32 {
  if (value <= start) { return 1.0f; }
  if (value >= end) { return 0.0f; }
  let t = (value - start) / (end - start);
  return (1.0f - t) * (1.0f - t) * (1.0f + 2.0f * t);
}

fn finishProfile(record: TermRecord, down: f32, normalizedDown: f32,
                 xi: f32, radialRatio: f32, axisDot: f32) -> TermRecord {
  var out = record;
  // Scalar controls use this same helper with explicit synthetic stage inputs.
  if (!finiteFloat(down) || !finiteFloat(normalizedDown) ||
      !finiteFloat(xi) || !finiteFloat(radialRatio) || !finiteFloat(axisDot) ||
      normalizedDown < 0.0f || normalizedDown > 64.0f ||
      xi < 0.0f || xi > 128.0f || radialRatio < 0.0f || radialRatio > 128.0f ||
      abs(axisDot) > 4.0f) { return invalidArithmetic(out); }
  let projection = max(0.0f, axisDot);
  out.axisDotBits = bitcast<u32>(axisDot);
  out.projectionBits = bitcast<u32>(projection);
  out.normalizedDownBits = bitcast<u32>(normalizedDown);
  out.xiBits = bitcast<u32>(xi);
  out.validityMask = out.validityMask | V_DOT | V_PROJECTION | V_NORMALIZED_DOWN | V_XI;

  let span = normalizedDown - c(3u);
  let denominator = 1.0f + c(13u) * xi * xi;
  if (!finiteFloat(span) || span < 4.0f || span > 71.0f ||
      !finiteFloat(denominator) || denominator < 1.0f || denominator > 8194.0f) {
    return invalidArithmetic(out);
  }
  let normalizedSpeed = (c(1u) / span) / (denominator * denominator);
  let fadeDown = factoredFade(c(7u), c(8u), down);
  let fadeRadial = factoredFade(c(9u), c(10u), radialRatio);
  if (!finiteFloat(normalizedSpeed) || !finiteFloat(fadeDown) ||
      !finiteFloat(fadeRadial) || normalizedSpeed < 0.0f || normalizedSpeed > 3.0f ||
      fadeDown < 0.0f || fadeDown > 1.001f ||
      fadeRadial < 0.0f || fadeRadial > 1.001f) { return invalidArithmetic(out); }
  out.normalizedSpeedBits = bitcast<u32>(normalizedSpeed);
  out.fadeDownBits = bitcast<u32>(fadeDown);
  out.fadeRadialBits = bitcast<u32>(fadeRadial);
  out.validityMask = out.validityMask | V_SPEED | V_FADE_DOWN | V_FADE_RADIAL;
  if (down > c(7u)) { out.routingFlags = out.routingFlags | F_DOWN_FADE; }
  if (radialRatio > c(9u)) { out.routingFlags = out.routingFlags | F_RADIAL_FADE; }

  // Independent-I multiplication grouping, no change to source strength.
  let term = normalizedSpeed * c(12u) * fadeDown * fadeRadial * projection;
  if (!finiteFloat(term) || term < 0.0f || term > 128.0f) {
    return invalidArithmetic(out);
  }
  out.termBits = bitcast<u32>(term);
  out.validityMask = out.validityMask | V_TERM;
  out.status = select(PROFILE_ZERO, PROFILE_POSITIVE, term > 0.0f);
  return out;
}

fn preparedTerm(ordinal: u32, receiverID: u32, sourceID: u32, rotor: u32,
                receiver: Node, source: Node, offset: Offset,
                routing: u32, armKind: u32) -> TermRecord {
  var out = blank(ordinal, receiverID, sourceID, rotor, routing);
  if (!rawNodeValid(receiver) || !rawNodeValid(source) || !rawOffsetValid(offset)) {
    return out;
  }
  // Every raw numeric word above is finite before any record reinterpretation.
  let rp = position(receiver);
  let sp = position(source);
  let ra = axis(receiver);
  let sa = axis(source);
  let receiverLow = lowPosition(receiver);
  let sourceLow = lowPosition(source);
  // 2^-17 is an exact residual guard. Validate before any geometric operation.
  if (any(abs(receiverLow) > vec3<f32>(0.00000762939453125f)) ||
      any(abs(sourceLow) > vec3<f32>(0.00000762939453125f))) { return out; }
  if (armKind != ARM_C && (receiver.lx != 0u || receiver.ly != 0u ||
      receiver.lz != 0u || source.lx != 0u || source.ly != 0u || source.lz != 0u)) {
    return out;
  }
  let arm = vec3<f32>(bitcast<f32>(offset.x), bitcast<f32>(offset.y), bitcast<f32>(offset.z));
  if (any(abs(rp) > vec3<f32>(128.0f)) || any(abs(sp) > vec3<f32>(128.0f)) ||
      any(abs(ra) > vec3<f32>(1.01f)) || any(abs(sa) > vec3<f32>(1.01f)) ||
      any(abs(arm) > vec3<f32>(0.1f))) { return out; }

  let isSelf = receiverID == sourceID;
  if (isSelf) {
    out.routingFlags = out.routingFlags | F_SELF;
    return finishEarly(out, policy(0u, true, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f));
  }
  // Written expressions describe the intervention, not a backend order promise.
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
  let center = length(centerDelta);
  if (!finiteFloat(center) || center < 0.0f || center > 512.0f) { return invalidArithmetic(out); }
  out.centerNormBits = bitcast<u32>(center);
  out.validityMask = out.validityMask | V_CENTER;
  var code = policy(0u, false, center, 0.0f, 0.0f, 0.0f, 0.0f);
  if (code != CONTINUE_POLICY) {
    out.routingFlags = out.routingFlags | F_OUTSIDE;
    return finishEarly(out, code);
  }

  let displacement = rotorDisplacement(armKind, sp, rp, arm, centerDelta);
  if (!finiteFloat(displacement.x) || !finiteFloat(displacement.y) ||
      !finiteFloat(displacement.z) || any(abs(displacement) > vec3<f32>(258.0f))) {
    return invalidArithmetic(out);
  }
  out.rotorDeltaXBits = bitcast<u32>(displacement.x);
  out.rotorDeltaYBits = bitcast<u32>(displacement.y);
  out.rotorDeltaZBits = bitcast<u32>(displacement.z);
  out.validityMask = out.validityMask | V_ROTOR_DELTA;
  let down = dot3(displacement, sa);
  if (!finiteFloat(down) || abs(down) > 1024.0f) { return invalidArithmetic(out); }
  out.downBits = bitcast<u32>(down);
  out.validityMask = out.validityMask | V_DOWN;
  code = policy(1u, false, center, down, 0.0f, 0.0f, 0.0f);
  if (code != CONTINUE_POLICY) { return finishEarly(out, code); }

  let perpendicular = displacement - down * sa;
  let radial = length(perpendicular);
  if (!finiteFloat(radial) || radial < 0.0f || radial > 2048.0f) { return invalidArithmetic(out); }
  out.radialBits = bitcast<u32>(radial);
  out.validityMask = out.validityMask | V_RADIAL;
  code = policy(2u, false, center, down, radial, 0.0f, 0.0f);
  if (code != CONTINUE_POLICY) { return finishEarly(out, code); }

  // Do not add a second normalizedDown>=minDownstream domain predicate.
  let normalizedDown = down / c(0u);
  let span = normalizedDown - c(3u);
  if (!finiteFloat(normalizedDown) || normalizedDown < 0.0f || normalizedDown > 64.0f ||
      !finiteFloat(span) || span < 4.0f || span > 71.0f) { return invalidArithmetic(out); }
  let halfWidth = c(2u) * span * c(0u);
  if (!finiteFloat(halfWidth) || halfWidth < 0.01f || halfWidth > 8.0f) { return invalidArithmetic(out); }
  out.normalizedDownBits = bitcast<u32>(normalizedDown);
  out.halfWidthBits = bitcast<u32>(halfWidth);
  out.validityMask = out.validityMask | V_NORMALIZED_DOWN | V_HALF;
  code = policy(3u, false, center, down, radial, halfWidth, 0.0f);
  if (code != CONTINUE_POLICY) { return finishEarly(out, code); }

  let axisDot = dot3(ra, sa);
  if (!finiteFloat(axisDot) || abs(axisDot) > 4.0f) { return invalidArithmetic(out); }
  code = policy(4u, false, center, down, radial, halfWidth, max(0.0f, axisDot));
  out.policyCode = code;
  let normalizedHalf = c(2u) * span;
  if (!finiteFloat(normalizedHalf) || normalizedHalf < 0.25f || normalizedHalf > 8.0f) {
    return invalidArithmetic(out);
  }
  let xi = (radial / c(0u)) / normalizedHalf;
  let radialRatio = radial / halfWidth;
  return finishProfile(out, down, normalizedDown, xi, radialRatio, axisDot);
}

fn selectedValid() -> bool {
  if (arrayLength(&selectedIDs) != SELECTION_COUNT) { return false; }
  for (var i = 0u; i < SELECTION_COUNT; i = i + 1u) {
    if (selectedIDs[i] >= SOURCE_COUNT) { return false; }
    for (var j = 0u; j < i; j = j + 1u) {
      if (selectedIDs[i] == selectedIDs[j]) { return false; }
    }
  }
  return true;
}

fn termsForArm(ordinal: u32, armKind: u32) {
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
fn termsC(@builtin(global_invocation_id) invocation: vec3<u32>) { termsForArm(invocation.x, ARM_C); }

fn rawControlValid(input: Control, ordinal: u32, armKind: u32) -> bool {
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
}

fn scalarControl(input: Control, base: TermRecord) -> TermRecord {
  var out = base;
  let center = bitcast<f32>(input.words[4]);
  let down = bitcast<f32>(input.words[5]);
  let radial = bitcast<f32>(input.words[6]);
  let halfWidth = bitcast<f32>(input.words[7]);
  let axisDot = bitcast<f32>(input.words[8]);
  let normalizedDown = bitcast<f32>(input.words[9]);
  let xi = bitcast<f32>(input.words[10]);
  let radialRatio = bitcast<f32>(input.words[11]);
  if (center < 0.0f || center > 512.0f || abs(down) > 1024.0f ||
      radial < 0.0f || radial > 2048.0f || halfWidth < 0.001f || halfWidth > 8.0f ||
      abs(axisDot) > 4.0f || normalizedDown < 0.0f || normalizedDown > 64.0f ||
      xi < 0.0f || xi > 128.0f || radialRatio < 0.0f || radialRatio > 128.0f) { return out; }
  if (input.words[2] == 1u) {
    out.routingFlags = out.routingFlags | F_SELF;
    return finishEarly(out, policy(0u, true, center, down, radial, halfWidth, axisDot));
  }
  out.centerNormBits = input.words[4];
  out.validityMask = out.validityMask | V_CENTER;
  var code = policy(0u, false, center, down, radial, halfWidth, axisDot);
  if (code != CONTINUE_POLICY) {
    out.routingFlags = out.routingFlags | F_OUTSIDE;
    return finishEarly(out, code);
  }
  out.downBits = input.words[5];
  out.validityMask = out.validityMask | V_DOWN;
  code = policy(1u, false, center, down, radial, halfWidth, axisDot);
  if (code != CONTINUE_POLICY) { return finishEarly(out, code); }
  out.radialBits = input.words[6];
  out.validityMask = out.validityMask | V_RADIAL;
  code = policy(2u, false, center, down, radial, halfWidth, axisDot);
  if (code != CONTINUE_POLICY) { return finishEarly(out, code); }
  out.halfWidthBits = input.words[7];
  out.normalizedDownBits = input.words[9];
  out.validityMask = out.validityMask | V_HALF | V_NORMALIZED_DOWN;
  code = policy(3u, false, center, down, radial, halfWidth, axisDot);
  if (code != CONTINUE_POLICY) { return finishEarly(out, code); }
  out.policyCode = policy(4u, false, center, down, radial, halfWidth, max(0.0f, axisDot));
  return finishProfile(out, down, normalizedDown, xi, radialRatio, axisDot);
}

fn controlsForArm(ordinal: u32, armKind: u32) {
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
}

fn acceptedTerm(record: TermRecord, ordinal: u32, receiver: u32,
                source: u32, rotor: u32) -> bool {
  if (record.ordinal != ordinal || record.receiverID != receiver ||
      record.sourceID != source || record.rotor != rotor ||
      record.routingFlags >= F_CONTROL || !finiteBits(record.termBits) ||
      !vectorPayloadValid(record)) { return false; }
  if (record.status != VALID_ZERO && record.status != PROFILE_ZERO &&
      record.status != PROFILE_POSITIVE) { return false; }
  if ((record.validityMask & V_TERM) == 0u) { return false; }
  let value = bitcast<f32>(record.termBits);
  if (value < 0.0f || value > 128.0f) { return false; }
  if (record.status == VALID_ZERO) {
    if (value != 0.0f) { return false; }
    if (record.policyCode == 0u) {
      if (source == receiver) {
        return record.validityMask == 2048u && record.routingFlags == F_SELF;
      }
      return record.validityMask == 30721u && record.routingFlags == F_OUTSIDE;
    }
    if (record.routingFlags != 0u) { return false; }
    if (record.policyCode == 1u || record.policyCode == 2u) { return record.validityMask == 260099u; }
    if (record.policyCode == 4u) { return record.validityMask == 260103u; }
    if (record.policyCode == 5u) { return record.validityMask == 260175u; }
    return false;
  }
  if (record.validityMask != 262143u || (record.routingFlags & (F_SELF | F_OUTSIDE)) != 0u) { return false; }
  if (record.status == PROFILE_ZERO) {
    return value == 0.0f && (record.policyCode == 6u || record.policyCode == 7u);
  }
  return value > 0.0f && record.policyCode == 7u;
}

@compute @workgroup_size(64)
fn reduceMain(@builtin(global_invocation_id) invocation: vec3<u32>) {
  let index = invocation.x;
  if (index >= arrayLength(&sums)) { return; }
  let selection = index / 4u;
  let rotor = index % 4u;
  var out = SumRecord(selection, UNSET, rotor, 1u, 0u, 0u, 0u, UNSET);
  sums[index] = out;
  if (index >= 16u || arrayLength(&sums) != 16u ||
      arrayLength(&terms) != TERM_COUNT || !selectedValid()) { return; }
  let receiver = selectedIDs[selection];
  out.receiverID = receiver;
  var total = 0.0f;
  for (var source = 0u; source < SOURCE_COUNT; source = source + 1u) {
    let ordinal = (selection * SOURCE_COUNT + source) * 4u + rotor;
    let record = terms[ordinal];
    if (!acceptedTerm(record, ordinal, receiver, source, rotor)) {
      out.firstBadSlot = ordinal;
      sums[index] = out;
      return;
    }
    // Read the exact materialized f32 word; never recompute a source term.
    let term = bitcast<f32>(record.termBits);
    let next = total + term;
    if (!finiteFloat(next) || next < 0.0f || next > 1000000.0f) {
      out.firstBadSlot = ordinal;
      sums[index] = out;
      return;
    }
    total = next;
    out.termCount = source + 1u;
  }
  out.status = 2u;
  out.validityMask = 1u;
  out.sumBits = bitcast<u32>(total);
  sums[index] = out;
}
