// Saved-byte decoding only. This module never evaluates a field, profile or root.
export const QUERY = ['unwritten','running','valid','domain invalid','input invalid','arithmetic invalid','sum limit','root invalid','body invalid'];
export const POLICY = ['unwritten','self / outside','nonpositive down','down cut','near invalid','near skip','radial cut','zero projection','positive term','numerically zero term','malformed','arithmetic invalid','reserved','reserved','reserved','reserved'];
const HEADER = ['receiverID','N','queryStatus','failureStage','writtenFullPairWords','writtenRotorSymbols','firstFailureSlot','payloadValidity'];
const GPU_FIELDS = ['Uraw','nominalRaw','vi','coefficient','x','force','shaderResidual','signedLastUpdate'];
const R_FIELDS = ['Uordinary','Ucompensated','nominal','vi','alpha','x','force','lower','upper','residual'];
export const fetched = new Set();
export function assert(ok, message) {if (!ok) throw Error(message);}
export function validateDescriptor(d) {
  assert(d && /^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(d.name), 'Invalid evidence name');
  assert(d.url === './evidence/' + d.name, 'Evidence must use the local evidence directory');
  assert(Number.isSafeInteger(d.bytes) && d.bytes >= 0 && d.bytes <= 16 * 1024 * 1024, 'Selected evidence size is invalid');
  assert(/^[0-9a-f]{64}$/.test(d.sha256), 'Missing evidence SHA-256');
}
export async function fetchVerified(d, signal) {
  validateDescriptor(d);
  const response = await fetch(d.url, {cache:'no-store', signal});
  assert(response.ok, 'Cannot fetch ' + d.name);
  const bytes = await response.arrayBuffer();
  assert(bytes.byteLength === d.bytes, 'Byte length mismatch: ' + d.name);
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  const hash = Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2,'0')).join('');
  assert(hash === d.sha256, 'SHA-256 mismatch: ' + d.name);
  fetched.add(d.name); return bytes;
}
export async function fetchJSON(d, signal) {return JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(await fetchVerified(d, signal)));}
export function view(bytes, expected, name) {assert(bytes.byteLength === expected, 'Unexpected layout: ' + name);return new DataView(bytes);}
export function header(v, offset) {return Object.fromEntries(HEADER.map((name,k) => [name,v.getUint32(offset + 4*k,true)]));}
function scalar(v, offset, wide, valid) {
  const value = wide ? v.getFloat64(offset,true) : v.getFloat32(offset,true);
  const bits = wide ? '0x' + v.getBigUint64(offset,true).toString(16).padStart(16,'0') : '0x' + v.getUint32(offset,true).toString(16).padStart(8,'0');
  return {value, valid:!!valid, bits};
}
export function gpuRoot(v, offset) {
  const mask=v.getUint32(offset+36,true), meta=v.getUint32(offset+32,true);
  return {...Object.fromEntries(GPU_FIELDS.map((key,k)=>[key,scalar(v,offset+4*k,false,mask&(1<<k))])), mask, meta,
    status:(meta>>>7)&7, branch:meta&7, iterations:(meta>>>3)&15, flags:(meta>>>10)&65535, positiveTerms:v.getUint32(offset+40,true)};
}
export function referenceRoot(v, offset) {
  const flagsValidity=v.getUint32(offset+88,true), mask=flagsValidity&1023;
  return {...Object.fromEntries(R_FIELDS.map((key,k)=>[key,scalar(v,offset+8*k,true,mask&(1<<k))])), mask, flagsValidity,
    status:v.getUint32(offset+80,true), iterations:v.getUint32(offset+84,true), positiveTerms:v.getUint32(offset+92,true)};
}
export function receiverRecord(v, id, N, kind) {
  if (!v) return null;
  const stride=kind==='GPU'?256:480, offset=id*stride, h=header(v,offset);
  const identityOK=h.receiverID===id && h.N===N;
  const roots=Array.from({length:4},(_,r)=>kind==='GPU'?gpuRoot(v,offset+32+48*r):referenceRoot(v,offset+32+96*r));
  const body=Array.from({length:8},(_,k)=>scalar(v,offset+(kind==='GPU'?224+4*k:416+8*k),kind!=='GPU',identityOK&&(h.payloadValidity&(k<4?8:16))));
  return {header:h,identityOK,roots,body};
}
export function decodePoses(bytes,N) {
  const v=view(bytes,N*17*8,'originalStates.f64');
  return Array.from({length:N},(_,id)=>({id,position:Array.from({length:3},(_,k)=>v.getFloat64((17*id+k)*8,true)),quaternion:Array.from({length:4},(_,k)=>v.getFloat64((17*id+6+k)*8,true))}));
}
export function decodePairPoses(bytes,count) {
  const v=view(bytes,count*16*8,'controls-pairs-original.f64');
  const vec=(id,k)=>[0,1,2].map(j=>v.getFloat64((id*16+k+j)*8,true));
  return Array.from({length:count},(_,id)=>({id,receiver:vec(id,0),receiverAxis:vec(id,3),source:vec(id,6),sourceAxis:vec(id,9),offset:vec(id,12)}));
}
export function pairRecord(v,id) {
  if(!v)return null; const b=256*id, h=header(v,b), mask=v.getUint32(b+56,true);
  return {header:h,identityOK:h.receiverID===id&&h.N===2,symbol:v.getUint32(b+32,true),mask,
    ...Object.fromEntries(['term','down','radial','projection','centerNorm'].map((key,k)=>[key,scalar(v,b+36+4*k,false,mask&(1<<k))]))};
}
export function value(s) {return s?.valid && Number.isFinite(s.value) ? s.value : null;}
export function difference(a,b) {const av=value(a),bv=value(b);return av===null||bv===null?null:av-bv;}
export function format(n) {if(n===null||n===undefined)return 'Unavailable';if(Object.is(n,-0))return '−0';if(!Number.isFinite(n))return String(n);if(n===0)return '0';return Math.abs(n)<.0001||Math.abs(n)>=100000?n.toExponential(6):Number(n.toPrecision(8)).toString();}
export function formatScalar(s) {return !s?.valid?'Unavailable':format(s.value);}
export function pointer(root,path) {
  if(path==='')return root;
  assert(typeof path==='string'&&path.startsWith('/'),'Review pointer must be a JSON pointer');
  return path.slice(1).split('/').reduce((obj,key)=>obj?.[key.replace(/~1/g,'/').replace(/~0/g,'~')],root);
}
