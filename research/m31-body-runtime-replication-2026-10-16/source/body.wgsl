// SOURCE-ONLY DRAFT. Never compiled/dispatched during preparation.
// Ordinary f32 primitive A: source - (receiver + offset).
// Same finite-support policy/profile; prescribed source strength.
// Input preparation and actual original/packed global admissions are host-owned.
// ABI is coordinated with m31_evidence_audit; no world-load outputs.

const NONE: u32 = 0xffffffffu;
const ROW_RUNNING: u32 = 1u;
const ROW_VALID: u32 = 2u;
const ROW_DOMAIN: u32 = 3u;
const ROW_INPUT: u32 = 4u;
const ROW_ARITHMETIC: u32 = 5u;
const ROW_SUM: u32 = 6u;
const ROW_ROOT: u32 = 7u;
const ROW_BODY: u32 = 8u;
const ST_LAYOUT: u32 = 1u;
const ST_ADMISSION: u32 = 2u;
const ST_CENTER: u32 = 3u;
const ST_PAIR: u32 = 4u;
const ST_SUM: u32 = 5u;
const ST_COEFFICIENT: u32 = 6u;
const ST_NEWTON: u32 = 7u;
const ST_PRODUCT: u32 = 8u;
const ST_BODY: u32 = 9u;
const ROOT_VALID: u32 = 1u;
const ROOT_INPUT: u32 = 2u;
const ROOT_ARITHMETIC: u32 = 3u;
const BR_NZERO: u32 = 1u;
const BR_UZERO: u32 = 2u;
const BR_LOW: u32 = 3u;
const BR_HIGH: u32 = 4u;
const F_N_SUB: u32 = 1u;
const F_U_SUB: u32 = 2u;
const F_N_ZERO: u32 = 4u;
const F_U_ZERO: u32 = 8u;
const F_N_NEGZERO: u32 = 16u;
const F_U_NEGZERO: u32 = 32u;
const F_ALPHA_ZERO: u32 = 64u;
const F_ALPHA_SUB: u32 = 128u;
const F_PRODUCT_ZERO: u32 = 256u;
const F_INTERMEDIATE_ZERO: u32 = 512u;
const F_FORCE_SUB: u32 = 1024u;

struct Constants { words: array<u32, 32>, }
struct Node {
  px: u32, py: u32, pz: u32,
  ax: u32, ay: u32, az: u32, pad0: u32, pad1: u32,
}
struct Offset { x: u32, y: u32, z: u32, pad: u32, }
struct PairResult {
  symbol: u32, term: f32, down: f32, radial: f32,
  projection: f32, center: f32, numericValidity: u32, failureStage: u32,
}
struct RootResult { words: array<u32, 12>, failureStage: u32, }
struct Polynomial { value: f32, derivative: f32, lostProduct: u32, }

@group(0) @binding(0) var<storage, read> constants: Constants;
@group(0) @binding(1) var<storage, read> nodes: array<u32>;
@group(0) @binding(2) var<storage, read> offsets: array<Offset>;
@group(0) @binding(3) var<storage, read> nominals: array<u32>;
@group(0) @binding(4) var<storage, read_write> policies: array<u32>;
@group(0) @binding(5) var<storage, read_write> outputs: array<u32>;
@group(0) @binding(6) var<storage, read> controlInputs: array<u32>;
@group(0) @binding(7) var<storage, read_write> controlOutputs: array<u32>;

fn c(index: u32) -> f32 { return bitcast<f32>(constants.words[index]); }
fn finiteBits(bits: u32) -> bool { return (bits & 0x7f800000u) != 0x7f800000u; }
fn finiteFloat(value: f32) -> bool { return finiteBits(bitcast<u32>(value)); }
fn rawZero(bits: u32) -> bool { return (bits & 0x7fffffffu) == 0u; }
fn rawSubnormal(bits: u32) -> bool {
  return (bits & 0x7f800000u) == 0u && (bits & 0x007fffffu) != 0u;
}
fn rawNormal(bits: u32) -> bool {
  let exponent = bits & 0x7f800000u;
  return exponent != 0u && exponent != 0x7f800000u;
}
fn nonnegativeBits(bits: u32) -> bool {
  return finiteBits(bits) && ((bits & 0x80000000u) == 0u || rawZero(bits));
}
fn positiveOperand(value: f32) -> bool {
  let bits = bitcast<u32>(value);
  return nonnegativeBits(bits) && !rawZero(bits);
}
fn lostMultiply(left: f32, right: f32, product: f32) -> bool {
  return positiveOperand(left) && positiveOperand(right) && rawZero(bitcast<u32>(product));
}
fn canonicalNonnegative(bits: u32) -> f32 {
  if (rawZero(bits) || rawSubnormal(bits)) { return 0.0f; }
  return bitcast<f32>(bits);
}
fn dot3(a: vec3<f32>, b: vec3<f32>) -> f32 {
  return a.x * b.x + a.y * b.y + a.z * b.z;
}
fn finiteVec(a: vec3<f32>) -> bool {
  return finiteFloat(a.x) && finiteFloat(a.y) && finiteFloat(a.z);
}
fn constantsValid() -> bool {
  for (var index = 0u; index < 20u; index = index + 1u) {
    if (!finiteBits(constants.words[index])) { return false; }
  }
  for (var index = 21u; index < 32u; index = index + 1u) {
    if (constants.words[index] != 0u) { return false; }
  }
  if (c(0u) < 0.05f || c(0u) > 0.1f || c(1u) < 10.0f || c(1u) > 11.0f ||
      c(2u) < 0.07f || c(2u) > 0.08f || c(3u) < -6.0f || c(3u) > -5.0f ||
      c(11u) < 0.9f || c(11u) > 1.0f || c(12u) < 1.0f || c(12u) > 10.0f ||
      c(13u) < 0.4f || c(13u) > 0.5f || c(14u) < 1.0f || c(14u) > 2.0f ||
      c(15u) < 0.001f || c(15u) > 0.002f || c(16u) < 0.02f || c(16u) > 0.04f ||
      c(17u) < 0.02f || c(17u) > 0.03f || c(18u) < 0.1f || c(18u) > 0.2f) { return false; }
  // The host also checks exact identity of every frozen constant word.
  return constants.words[4] == 0x40200000u && constants.words[5] == 0x40400000u &&
    constants.words[6] == 0x3e19999au && constants.words[7] == 0x40000000u &&
    constants.words[8] == 0x40200000u && constants.words[9] == 0x40000000u &&
    constants.words[10] == 0x40400000u && constants.words[19] == 0x49800000u;
}
fn nodePosition(n: Node) -> vec3<f32> {
  return vec3<f32>(bitcast<f32>(n.px), bitcast<f32>(n.py), bitcast<f32>(n.pz));
}
fn nodeAxis(n: Node) -> vec3<f32> {
  return vec3<f32>(bitcast<f32>(n.ax), bitcast<f32>(n.ay), bitcast<f32>(n.az));
}
fn loadNode(index: u32) -> Node {
  let b = 8u * index;
  return Node(nodes[b],nodes[b+1u],nodes[b+2u],nodes[b+4u],nodes[b+5u],nodes[b+6u],nodes[b+3u],nodes[b+7u]);
}
fn nodeValid(n: Node, allowPreparedTilt: bool) -> bool {
  if (!finiteBits(n.px) || !finiteBits(n.py) || !finiteBits(n.pz) ||
      !finiteBits(n.ax) || !finiteBits(n.ay) || !finiteBits(n.az) || n.pad0 != 0u || n.pad1 != 0u) { return false; }
  let p = nodePosition(n);
  let a = nodeAxis(n);
  if (any(abs(p) > vec3<f32>(128.0f)) || any(abs(a) > vec3<f32>(1.01f))) { return false; }
  return allowPreparedTilt || a.z >= c(11u);
}
fn offsetValid(o: Offset) -> bool {
  if (!finiteBits(o.x) || !finiteBits(o.y) || !finiteBits(o.z) || o.pad != 0u) { return false; }
  return all(abs(vec3<f32>(bitcast<f32>(o.x),bitcast<f32>(o.y),bitcast<f32>(o.z))) <= vec3<f32>(0.1f));
}
fn nominalValid(bits: u32) -> bool {
  if (!nonnegativeBits(bits)) { return false; }
  return bitcast<f32>(bits) <= c(18u);
}
fn blankPair(stage: u32) -> PairResult {
  return PairResult(10u,0.0f,0.0f,0.0f,0.0f,0.0f,0u,stage);
}
fn arithmeticPair(input: PairResult, stage: u32) -> PairResult {
  var out = input;
  out.symbol = 11u;
  out.numericValidity = out.numericValidity & ~1u;
  out.failureStage = stage;
  return out;
}
fn zeroPair(input: PairResult, symbol: u32) -> PairResult {
  var out = input;
  out.symbol = symbol;
  out.term = 0.0f;
  out.numericValidity = out.numericValidity | 1u;
  out.failureStage = 0u;
  return out;
}
fn factoredFade(start: f32, end: f32, value: f32) -> f32 {
  if (value <= start) { return 1.0f; }
  if (value >= end) { return 0.0f; }
  let t = (value - start) / (end - start);
  return (1.0f-t) * (1.0f-t) * (1.0f+2.0f*t);
}

// Nodes, offset and center are admitted by the caller. Center is shared across
// the four main-query rotors, preserving one ordered center check per pair.
fn preparedTerm(receiver: Node, source: Node, offset: Offset, isSelf: bool, center: f32) -> PairResult {
  var out = blankPair(ST_PAIR);
  out.center = center;
  if (!finiteFloat(center) || center < 0.0f || center > 512.0f) { return arithmeticPair(out,ST_CENTER); }
  out.numericValidity = 16u;
  if (isSelf || center >= c(5u)) { return zeroPair(out,1u); }
  let rp = nodePosition(receiver);
  let sp = nodePosition(source);
  let ra = nodeAxis(receiver);
  let sa = nodeAxis(source);
  let arm = vec3<f32>(bitcast<f32>(offset.x),bitcast<f32>(offset.y),bitcast<f32>(offset.z));
  // The fixed primitive-A operation: do not replace with (source-receiver)-arm.
  let point = rp + arm;
  let displacement = sp - point;
  if (!finiteVec(displacement) || any(abs(displacement) > vec3<f32>(258.0f))) { return arithmeticPair(out,ST_PAIR); }
  let down = dot3(displacement,sa);
  out.down = down;
  if (!finiteFloat(down) || abs(down) > 1024.0f) { return arithmeticPair(out,ST_PAIR); }
  out.numericValidity = out.numericValidity | 2u;
  if (down <= 0.0f) { return zeroPair(out,2u); }
  if (down >= c(8u)) { return zeroPair(out,3u); }
  let perpendicular = displacement - down * sa;
  let radial = length(perpendicular);
  out.radial = radial;
  if (!finiteFloat(radial) || radial < 0.0f || radial > 2048.0f) { return arithmeticPair(out,ST_PAIR); }
  out.numericValidity = out.numericValidity | 4u;
  if (down < c(4u) * c(0u)) {
    if (radial < c(6u)) { out.symbol = 4u; out.failureStage = ST_PAIR; return out; }
    return zeroPair(out,5u);
  }
  let normalizedDown = down / c(0u);
  let span = normalizedDown - c(3u);
  if (!finiteFloat(normalizedDown) || normalizedDown < 0.0f || normalizedDown > 64.0f ||
      !finiteFloat(span) || span < 4.0f || span > 71.0f) { return arithmeticPair(out,ST_PAIR); }
  let halfWidth = c(2u) * span * c(0u);
  if (!finiteFloat(halfWidth) || halfWidth < 0.01f || halfWidth > 8.0f) { return arithmeticPair(out,ST_PAIR); }
  if (radial >= c(10u) * halfWidth) { return zeroPair(out,6u); }
  let axisDot = dot3(ra,sa);
  if (!finiteFloat(axisDot) || abs(axisDot) > 4.0f) { return arithmeticPair(out,ST_PAIR); }
  let projection = max(0.0f,axisDot);
  out.projection = projection;
  out.numericValidity = out.numericValidity | 8u;
  let normalizedHalf = c(2u) * span;
  if (!finiteFloat(normalizedHalf) || normalizedHalf < 0.25f || normalizedHalf > 8.0f) { return arithmeticPair(out,ST_PAIR); }
  let xi = (radial / c(0u)) / normalizedHalf;
  let radialRatio = radial / halfWidth;
  if (!finiteFloat(xi) || xi < 0.0f || xi > 128.0f ||
      !finiteFloat(radialRatio) || radialRatio < 0.0f || radialRatio > 128.0f) { return arithmeticPair(out,ST_PAIR); }
  let denominator = 1.0f + c(13u) * xi * xi;
  if (!finiteFloat(denominator) || denominator < 1.0f || denominator > 8194.0f) { return arithmeticPair(out,ST_PAIR); }
  let normalizedSpeed = (c(1u) / span) / (denominator * denominator);
  let fadeDown = factoredFade(c(7u),c(8u),down);
  let fadeRadial = factoredFade(c(9u),c(10u),radialRatio);
  if (!finiteFloat(normalizedSpeed) || normalizedSpeed < 0.0f || normalizedSpeed > 3.0f ||
      !finiteFloat(fadeDown) || fadeDown < 0.0f || fadeDown > 1.001f ||
      !finiteFloat(fadeRadial) || fadeRadial < 0.0f || fadeRadial > 1.001f) { return arithmeticPair(out,ST_PAIR); }
  let term = normalizedSpeed * c(12u) * fadeDown * fadeRadial * projection;
  if (!finiteFloat(term) || term < 0.0f || term > 128.0f) { return arithmeticPair(out,ST_PAIR); }
  out.term = term;
  out.numericValidity = out.numericValidity | 1u;
  out.failureStage = 0u;
  if (projection <= 0.0f) { out.symbol = 7u; }
  else { out.symbol = select(9u,8u,term > 0.0f); }
  return out;
}
fn pairStatus(symbol: u32) -> u32 {
  if (symbol == 4u) { return ROW_DOMAIN; }
  if (symbol == 10u) { return ROW_INPUT; }
  if (symbol == 11u) { return ROW_ARITHMETIC; }
  return ROW_VALID;
}
fn rootMeta(branch: u32, iterations: u32, status: u32, flags: u32) -> u32 {
  return branch | (iterations << 3u) | (status << 7u) | (flags << 10u);
}
fn polynomial(x: f32, coefficient: f32, high: bool) -> Polynomial {
  let x2 = x*x;
  let x3 = x2*x;
  var lost = lostMultiply(x,x,x2) || lostMultiply(x2,x,x3);
  if (high) {
    let cubic = coefficient*x3;
    let derivativeTerm = (3.0f*coefficient)*x2;
    lost = lost || lostMultiply(coefficient,x3,cubic) || lostMultiply(3.0f*coefficient,x2,derivativeTerm);
    return Polynomial((cubic+x)-coefficient,derivativeTerm+1.0f,select(0u,1u,lost));
  }
  let linear = coefficient*x;
  lost = lost || lostMultiply(coefficient,x,linear);
  return Polynomial((x3+linear)-1.0f,3.0f*x2+coefficient,select(0u,1u,lost));
}
fn maskedRoot(input: RootResult) -> RootResult {
  var out = input;
  for (var word = 0u; word < 8u; word = word+1u) {
    if ((out.words[9] & (1u << word)) == 0u) { out.words[word] = 0u; }
  }
  return out;
}
fn solveReceiver(Ubits: u32, nbits: u32, positiveCount: u32) -> RootResult {
  var out: RootResult;
  out.words[0] = Ubits;
  out.words[1] = nbits;
  out.words[10] = positiveCount;
  out.failureStage = ST_ADMISSION;
  var valid = 0u;
  if (nonnegativeBits(Ubits)) {
    if (bitcast<f32>(Ubits) <= c(19u)) { valid = valid | 1u; }
  }
  if (nominalValid(nbits)) { valid = valid | 2u; }
  out.words[9] = valid;
  if (valid != 3u) { out.words[8] = rootMeta(0u,0u,ROOT_INPUT,0u); return maskedRoot(out); }
  var flags = 0u;
  if (rawSubnormal(nbits)) { flags = flags | F_N_SUB; }
  if (rawSubnormal(Ubits)) { flags = flags | F_U_SUB; }
  if (rawZero(nbits)) { flags = flags | F_N_ZERO; }
  if (rawZero(Ubits)) { flags = flags | F_U_ZERO; }
  if (nbits == 0x80000000u) { flags = flags | F_N_NEGZERO; }
  if (Ubits == 0x80000000u) { flags = flags | F_U_NEGZERO; }
  let nominal = canonicalNonnegative(nbits);
  let U = canonicalNonnegative(Ubits);
  if (nominal == 0.0f) {
    out.words[4] = 0u; out.words[5] = 0u;
    out.words[8] = rootMeta(BR_NZERO,0u,ROOT_VALID,flags);
    out.words[9] = 0x33u; out.failureStage = 0u; return maskedRoot(out);
  }
  if (U == 0.0f) {
    out.words[4] = bitcast<u32>(1.0f); out.words[5] = bitcast<u32>(nominal);
    out.words[8] = rootMeta(BR_UZERO,0u,ROOT_VALID,flags);
    out.words[9] = 0x33u; out.failureStage = 0u; return maskedRoot(out);
  }
  out.failureStage = ST_COEFFICIENT;
  let denominator = (2.0f*c(14u))*c(15u);
  let quotient = nominal/denominator;
  let vi = sqrt(quotient);
  out.words[2] = bitcast<u32>(vi);
  if (!finiteFloat(denominator) || denominator <= 0.0f || !finiteFloat(quotient) || quotient <= 0.0f ||
      !rawNormal(bitcast<u32>(vi)) || vi <= 0.0f) {
    out.words[8] = rootMeta(0u,0u,ROOT_ARITHMETIC,flags); return maskedRoot(out);
  }
  valid = valid | 4u;
  out.words[9] = valid;
  let high = U > vi;
  let branch = select(BR_LOW,BR_HIGH,high);
  var coefficient = 0.0f;
  if (high) { coefficient = vi/U; }
  else { coefficient = U/vi; }
  out.words[3] = bitcast<u32>(coefficient);
  if (!finiteFloat(coefficient) || coefficient < 0.0f || coefficient > 1.0f ||
      (high && (!rawNormal(bitcast<u32>(coefficient)) || coefficient <= 0.0f))) {
    out.words[8] = rootMeta(branch,0u,ROOT_ARITHMETIC,flags); return maskedRoot(out);
  }
  if (!high && rawZero(bitcast<u32>(coefficient))) { flags = flags | F_ALPHA_ZERO; }
  if (!high && rawSubnormal(bitcast<u32>(coefficient))) { flags = flags | F_ALPHA_SUB; }
  valid = valid | 8u;
  var x = 1.0f;
  if (high) { x = coefficient; }
  var iterations = 0u;
  var update = 0.0f;
  out.failureStage = ST_NEWTON;
  for (var iteration = 0u; iteration < 12u; iteration = iteration + 1u) {
    let p = polynomial(x,coefficient,high);
    if (p.lostProduct != 0u) { flags = flags | F_INTERMEDIATE_ZERO; }
    if (!finiteFloat(p.value) || !finiteFloat(p.derivative) || p.derivative <= 0.0f) {
      out.words[4] = bitcast<u32>(x); out.words[6] = bitcast<u32>(p.value);
      out.words[7] = bitcast<u32>(update); out.words[9] = valid;
      out.words[8] = rootMeta(branch,iterations,ROOT_ARITHMETIC,flags); return maskedRoot(out);
    }
    let next = x - p.value/p.derivative;
    update = next-x; // actual signed applied update, not F/F'.
    iterations = iterations + 1u;
    if (!finiteFloat(next) || next <= 0.0f || next > 1.0f || !finiteFloat(update)) {
      out.words[4] = bitcast<u32>(next); out.words[7] = bitcast<u32>(update); out.words[9] = valid;
      out.words[8] = rootMeta(branch,iterations,ROOT_ARITHMETIC,flags); return maskedRoot(out);
    }
    x = next;
  }
  let finalPolynomial = polynomial(x,coefficient,high);
  if (finalPolynomial.lostProduct != 0u) { flags = flags | F_INTERMEDIATE_ZERO; }
  out.words[4] = bitcast<u32>(x);
  out.words[6] = bitcast<u32>(finalPolynomial.value);
  out.words[7] = bitcast<u32>(update);
  if (!finiteFloat(finalPolynomial.value)) {
    out.words[9] = valid; out.words[8] = rootMeta(branch,iterations,ROOT_ARITHMETIC,flags); return maskedRoot(out);
  }
  valid = valid | 16u | 64u | 128u;
  out.failureStage = ST_PRODUCT;
  let force = nominal*x;
  out.words[5] = bitcast<u32>(force);
  if (lostMultiply(nominal,x,force)) { flags = flags | F_PRODUCT_ZERO; }
  if (rawSubnormal(bitcast<u32>(force))) { flags = flags | F_FORCE_SUB; }
  if (!finiteFloat(force) || force < 0.0f || force > nominal) {
    out.words[9] = valid; out.words[8] = rootMeta(branch,iterations,ROOT_ARITHMETIC,flags); return maskedRoot(out);
  }
  valid = valid | 32u;
  out.words[8] = rootMeta(branch,iterations,ROOT_VALID,flags);
  out.words[9] = valid;
  out.failureStage = 0u;
  return maskedRoot(out);
}
fn rootSucceeded(root: RootResult) -> bool { return ((root.words[8] >> 7u) & 7u) == ROOT_VALID; }
fn wrench(f: array<f32,4>) -> array<f32,4> {
  return array<f32,4>(
    ((f[0]+f[1])+f[2])+f[3],
    c(16u)*(((f[0]+f[1])-f[2])-f[3]),
    c(16u)*(((-f[0]+f[1])+f[2])-f[3]),
    c(17u)*(((f[0]-f[1])+f[2])-f[3])
  );
}
fn wrenchFirstBad(w: array<f32,4>) -> u32 {
  if (!finiteFloat(w[0]) || w[0] < 0.0f || w[0] > 4.0f*c(18u)*1.01f) { return 0u; }
  if (!finiteFloat(w[1]) || abs(w[1]) > 4.0f*c(16u)*c(18u)*1.01f) { return 1u; }
  if (!finiteFloat(w[2]) || abs(w[2]) > 4.0f*c(16u)*c(18u)*1.01f) { return 2u; }
  if (!finiteFloat(w[3]) || abs(w[3]) > 4.0f*c(17u)*c(18u)*1.01f) { return 3u; }
  return NONE;
}
fn failMain(base: u32, status: u32, stage: u32, slot: u32) {
  outputs[base+2u] = status; outputs[base+3u] = stage; outputs[base+6u] = slot;
}
@compute @workgroup_size(64)
fn mainBody(@builtin(global_invocation_id) invocation: vec3<u32>) {
  let receiverID = invocation.x;
  let N = constants.words[20];
  if (receiverID >= N || receiverID >= arrayLength(&outputs)/64u) { return; }
  let base = 64u*receiverID;
  for (var word = 0u; word < 64u; word = word+1u) { outputs[base+word] = 0u; }
  outputs[base] = receiverID; outputs[base+1u] = N; outputs[base+2u] = ROW_RUNNING; outputs[base+6u] = NONE;
  if (N < 2u || N > 5000u || !constantsValid() || arrayLength(&nodes) != 8u*N ||
      arrayLength(&offsets) != 4u*N || arrayLength(&nominals) != 4u*N ||
      arrayLength(&policies) != N*N || arrayLength(&outputs) != 64u*N) {
    failMain(base,ROW_INPUT,ST_LAYOUT,0u); return;
  }
  let receiver = loadNode(receiverID);
  if (!nodeValid(receiver,false)) { failMain(base,ROW_INPUT,ST_ADMISSION,0u); return; }
  var receiverOffsets: array<Offset,4>;
  var nominalWords: array<u32,4>;
  var nominalApplied: array<f32,4>;
  for (var rotor = 0u; rotor < 4u; rotor = rotor+1u) {
    receiverOffsets[rotor] = offsets[4u*receiverID+rotor];
    nominalWords[rotor] = nominals[4u*receiverID+rotor];
    if (!offsetValid(receiverOffsets[rotor]) || !nominalValid(nominalWords[rotor])) {
      failMain(base,ROW_INPUT,ST_ADMISSION,0u); return;
    }
    nominalApplied[rotor] = canonicalNonnegative(nominalWords[rotor]);
  }
  var sums: array<f32,4>;
  var positiveCounts: array<u32,4>;
  for (var sourceID = 0u; sourceID < N; sourceID = sourceID+1u) {
    let source = loadNode(sourceID);
    let pairIndex = receiverID*N+sourceID;
    var pairWord = 0u;
    var center = 0.0f;
    var commonFailure = 0u;
    var commonStage = ST_ADMISSION;
    if (!nodeValid(source,false)) { commonFailure = 10u; }
    else if (sourceID != receiverID) {
      let centerDelta = nodePosition(source)-nodePosition(receiver);
      center = length(centerDelta);
      if (!finiteVec(centerDelta) || any(abs(centerDelta) > vec3<f32>(257.0f)) ||
          !finiteFloat(center) || center < 0.0f || center > 512.0f) { commonFailure = 11u; commonStage = ST_CENTER; }
    }
    for (var rotor = 0u; rotor < 4u; rotor = rotor+1u) {
      var result = blankPair(commonStage);
      if (commonFailure != 0u) { result.symbol = commonFailure; }
      else { result = preparedTerm(receiver,source,receiverOffsets[rotor],receiverID==sourceID,center); }
      pairWord = pairWord | (result.symbol << (8u*rotor));
      outputs[base+5u] = 4u*sourceID+rotor+1u;
      outputs[base+7u] = 1u;
      let status = pairStatus(result.symbol);
      if (status != ROW_VALID) {
        policies[pairIndex] = pairWord; // sole write of this possibly partial word.
        outputs[base+4u] = sourceID + select(0u,1u,rotor==3u);
        failMain(base,status,result.failureStage,4u*sourceID+rotor); return;
      }
      let nextSum = sums[rotor]+result.term;
      sums[rotor] = nextSum;
      if (result.symbol == 8u) { positiveCounts[rotor] = positiveCounts[rotor]+1u; }
      if (!finiteFloat(nextSum) || nextSum < 0.0f || nextSum > c(19u)) {
        policies[pairIndex] = pairWord;
        outputs[base+4u] = sourceID + select(0u,1u,rotor==3u);
        failMain(base,ROW_SUM,ST_SUM,4u*sourceID+rotor); return;
      }
    }
    policies[pairIndex] = pairWord; // one writer and one completed word store.
    outputs[base+4u] = sourceID+1u;
  }
  outputs[base+7u] = 3u;
  var effectiveForces: array<f32,4>;
  var allRootsValid = true;
  var firstRootFailure = NONE;
  var rootFailureStage = 0u;
  for (var rotor = 0u; rotor < 4u; rotor = rotor+1u) {
    let root = solveReceiver(bitcast<u32>(sums[rotor]),nominalWords[rotor],positiveCounts[rotor]);
    for (var word = 0u; word < 12u; word = word+1u) { outputs[base+8u+12u*rotor+word] = root.words[word]; }
    if (!rootSucceeded(root)) {
      if (allRootsValid) { firstRootFailure = rotor; rootFailureStage = root.failureStage; }
      allRootsValid = false;
    } else { effectiveForces[rotor] = bitcast<f32>(root.words[5]); }
  }
  outputs[base+7u] = 7u;
  if (!allRootsValid) { failMain(base,ROW_ROOT,rootFailureStage,firstRootFailure); return; }
  let nominalBody = wrench(nominalApplied);
  var effectiveBody = wrench(effectiveForces);
  effectiveBody[3] = nominalBody[3];
  let firstBadBody = min(wrenchFirstBad(nominalBody),wrenchFirstBad(effectiveBody));
  if (firstBadBody != NONE) { failMain(base,ROW_BODY,ST_BODY,firstBadBody); return; }
  for (var component = 0u; component < 4u; component = component+1u) {
    outputs[base+56u+component] = bitcast<u32>(effectiveBody[component]);
    outputs[base+60u+component] = bitcast<u32>(nominalBody[component]);
  }
  outputs[base+7u] = 31u;
  outputs[base+2u] = ROW_VALID;
}

fn controlNode(base: u32) -> Node {
  return Node(controlInputs[base],controlInputs[base+1u],controlInputs[base+2u],
    controlInputs[base+4u],controlInputs[base+5u],controlInputs[base+6u],controlInputs[base+3u],controlInputs[base+7u]);
}
fn initializeControl(index: u32, fixtureN: u32) {
  let base = 64u*index;
  for (var word = 0u; word < 64u; word = word+1u) { controlOutputs[base+word] = 0u; }
  controlOutputs[base] = index; controlOutputs[base+1u] = fixtureN;
  controlOutputs[base+2u] = ROW_RUNNING; controlOutputs[base+6u] = NONE; controlOutputs[base+7u] = 32u;
}
fn failControl(base: u32, status: u32, stage: u32) {
  controlOutputs[base+2u] = status; controlOutputs[base+3u] = stage; controlOutputs[base+6u] = 0u;
}
fn controlLayout(index: u32, kind: u32) -> bool {
  let count = constants.words[20];
  if (count == 0u || count > 4096u || !constantsValid() ||
      arrayLength(&controlInputs) != 64u*count || arrayLength(&controlOutputs) != 64u*count) { return false; }
  let base = 64u*index;
  if (controlInputs[base] != index || controlInputs[base+1u] != kind || controlInputs[base+3u] != 0u) { return false; }
  for (var word = 36u; word < 64u; word = word+1u) { if (controlInputs[base+word] != 0u) { return false; } }
  return true;
}
@compute @workgroup_size(64)
fn controlPairs(@builtin(global_invocation_id) invocation: vec3<u32>) {
  let index = invocation.x;
  let count = constants.words[20];
  if (index >= count || index >= arrayLength(&controlOutputs)/64u) { return; }
  let base = 64u*index;
  initializeControl(index,0u);
  if (!controlLayout(index,1u)) { failControl(base,ROW_INPUT,ST_LAYOUT); return; }
  let fixtureN = controlInputs[base+7u];
  controlOutputs[base+1u] = fixtureN;
  let receiverID = controlInputs[base+4u];
  let sourceID = controlInputs[base+5u];
  let rotor = controlInputs[base+6u];
  let flags = controlInputs[base+2u];
  if (fixtureN < 2u || fixtureN > 5000u || receiverID >= fixtureN || sourceID >= fixtureN || rotor >= 4u ||
      (flags != 0u && !(flags == 1u && index == 14u))) { failControl(base,ROW_INPUT,ST_ADMISSION); return; }
  for (var word = 28u; word < 36u; word = word+1u) {
    if (controlInputs[base+word] != 0u) { failControl(base,ROW_INPUT,ST_LAYOUT); return; }
  }
  let receiver = controlNode(base+8u);
  let source = controlNode(base+16u);
  let offset = Offset(controlInputs[base+24u],controlInputs[base+25u],controlInputs[base+26u],controlInputs[base+27u]);
  var result = blankPair(ST_ADMISSION);
  if (nodeValid(receiver,flags==1u) && nodeValid(source,flags==1u) && offsetValid(offset)) {
    var center = 0.0f;
    if (receiverID != sourceID) { center = length(nodePosition(source)-nodePosition(receiver)); }
    result = preparedTerm(receiver,source,offset,receiverID==sourceID,center);
  }
  controlOutputs[base+5u] = 1u;
  controlOutputs[base+7u] = 33u;
  controlOutputs[base+8u] = result.symbol;
  if ((result.numericValidity & 1u) != 0u) { controlOutputs[base+9u] = bitcast<u32>(result.term); }
  if ((result.numericValidity & 2u) != 0u) { controlOutputs[base+10u] = bitcast<u32>(result.down); }
  if ((result.numericValidity & 4u) != 0u) { controlOutputs[base+11u] = bitcast<u32>(result.radial); }
  if ((result.numericValidity & 8u) != 0u) { controlOutputs[base+12u] = bitcast<u32>(result.projection); }
  if ((result.numericValidity & 16u) != 0u) { controlOutputs[base+13u] = bitcast<u32>(result.center); }
  controlOutputs[base+14u] = result.numericValidity;
  controlOutputs[base+2u] = pairStatus(result.symbol);
  if (controlOutputs[base+2u] != ROW_VALID) { failControl(base,controlOutputs[base+2u],result.failureStage); }
}
@compute @workgroup_size(64)
fn controlRoots(@builtin(global_invocation_id) invocation: vec3<u32>) {
  let index = invocation.x;
  let count = constants.words[20];
  if (index >= count || index >= arrayLength(&controlOutputs)/64u) { return; }
  let base = 64u*index;
  initializeControl(index,1u);
  if (!controlLayout(index,2u)) { failControl(base,ROW_ROOT,ST_LAYOUT); return; }
  if (controlInputs[base+2u] != 0u || controlInputs[base+4u] != 0u || controlInputs[base+5u] != 0u ||
      controlInputs[base+6u] != 0u || controlInputs[base+7u] != 1u) { failControl(base,ROW_ROOT,ST_LAYOUT); return; }
  for (var word = 8u; word < 28u; word = word+1u) {
    if (controlInputs[base+word] != 0u) { failControl(base,ROW_ROOT,ST_LAYOUT); return; }
  }
  for (var word = 29u; word < 36u; word = word+1u) {
    if (word != 32u && controlInputs[base+word] != 0u) { failControl(base,ROW_ROOT,ST_LAYOUT); return; }
  }
  let root = solveReceiver(controlInputs[base+32u],controlInputs[base+28u],0u);
  for (var word = 0u; word < 12u; word = word+1u) { controlOutputs[base+8u+word] = root.words[word]; }
  if (rootSucceeded(root)) { controlOutputs[base+2u] = ROW_VALID; }
  else { failControl(base,ROW_ROOT,root.failureStage); }
}
