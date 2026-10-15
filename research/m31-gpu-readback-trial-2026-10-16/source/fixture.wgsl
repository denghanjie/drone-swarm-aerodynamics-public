@group(0) @binding(0)
var<storage, read_write> output: array<u32, 32>;

@compute @workgroup_size(8)
fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
  let i: u32 = gid.x;
  if (i >= 17u) { return; }
  output[4u + i] = ((0x9E3779B9u * (i + 1u)) ^ 0xA5A5A5A5u) + 0x7F4A7C15u;
}
