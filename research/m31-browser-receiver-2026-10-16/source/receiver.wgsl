// STATIC DRAFT ONLY: not compiled or executed.
// Scope: fixed uploaded f0/vi constants, U in [0, 128].
// Binding 0: ReceiverInput raw-u32 array, 16-byte stride.
// Binding 1: ReceiverOutput array, 32-byte stride; same record count.
// Host dispatch: ceil(inputCount / 64) workgroups in x, y=z=1.

struct ReceiverInput {
  uBits: u32,
  f0Bits: u32,
  viBits: u32,
  padBits: u32,
}

struct ReceiverOutput {
  alpha: f32,
  x: f32,
  f: f32,
  reportedResidual: f32,
  iterations: f32,
  stopCode: f32,
  finalAbsStep: f32,
  reserved: f32,
}

@group(0) @binding(0)
var<storage, read> inputs: array<ReceiverInput>;

@group(0) @binding(1)
var<storage, read_write> outputs: array<ReceiverOutput>;

fn finiteRawBits(bits: u32) -> bool {
  return (bits & 0x7f800000u) != 0x7f800000u;
}

fn finiteFloat(value: f32) -> bool {
  return finiteRawBits(bitcast<u32>(value));
}

fn invalidOutput() -> ReceiverOutput {
  return ReceiverOutput(0.0f, 0.0f, 0.0f, 0.0f,
                        0.0f, 3.0f, 0.0f, 0.0f);
}

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) invocation: vec3<u32>) {
  let index = invocation.x;
  if (index >= arrayLength(&inputs)) {
    return;
  }

  // Every in-range invocation writes a complete record, including rejection.
  outputs[index] = invalidOutput();
  let input = inputs[index];

  // Invalid controls remain integer data until these checks have passed.
  if (!finiteRawBits(input.uBits) || !finiteRawBits(input.f0Bits) ||
      !finiteRawBits(input.viBits) || input.padBits != 0u) {
    return;
  }
  let u = bitcast<f32>(input.uBits);
  let f0 = bitcast<f32>(input.f0Bits);
  let vi = bitcast<f32>(input.viBits);

  // These protect this fixed-constant experiment, not a general receiver API.
  if (u < 0.0f || u > 128.0f ||
      f0 < 0.01f || f0 > 0.1f ||
      vi < 1.0f || vi > 10.0f) {
    return;
  }

  // Identity relative to the uploaded f32 nominal thrust; no Newton step.
  if (u == 0.0f) {
    outputs[index] = ReceiverOutput(0.0f, 1.0f, f0, 0.0f,
                                    0.0f, 0.0f, 0.0f, 0.0f);
    return;
  }

  let alpha = u / vi;
  if (!finiteFloat(alpha) || alpha <= 0.0f) {
    return;
  }
  var x = min(1.0f, 1.0f / alpha);
  if (!finiteFloat(x) || x < 0.0f || x > 1.0f) {
    return;
  }

  var iterations = 0u;
  var stopCode = 2.0f;
  var finalAbsStep = 0.0f;

  for (var k = 0u; k < 12u; k = k + 1u) {
    // Same source grouping as M28: no pow, fma, clamp or alternate solver.
    let numerator = x * x * x + alpha * x - 1.0f;
    let denominator = 3.0f * x * x + alpha;
    if (!finiteFloat(numerator) || !finiteFloat(denominator) || denominator <= 0.0f) {
      return;
    }
    let next = x - numerator / denominator;
    if (!finiteFloat(next) || next < 0.0f || next > 1.0f) {
      return;
    }

    finalAbsStep = abs(next - x);
    iterations = k + 1u;
    if (finalAbsStep < 1e-15f) {
      x = next;
      stopCode = 1.0f;
      break;
    }
    x = next;
  }

  let f = f0 * x;
  let reportedResidual = x * x * x + alpha * x - 1.0f;
  if (!finiteFloat(f) || !finiteFloat(reportedResidual) || !finiteFloat(finalAbsStep) ||
      f < 0.0f || f > f0) {
    return;
  }

  outputs[index] = ReceiverOutput(alpha, x, f, reportedResidual,
                                  f32(iterations), stopCode, finalAbsStep, 0.0f);
}
