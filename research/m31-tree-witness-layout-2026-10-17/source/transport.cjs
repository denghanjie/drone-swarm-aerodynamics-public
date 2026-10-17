'use strict';
// Lossless JSON-value transport only. No science, filesystem, hashing or compression.
const LIMITS=Object.freeze({chunkBytes:1048576,binaryBytes:100663296,jsonBytes:268435456,elements:16000000,depth:64,descriptorBytes:2097152});
const utf8=new TextEncoder(), text=new TextDecoder('utf-8',{fatal:true});
const need=(v,c)=>{if(!v)throw Error('transport-'+c);};
function exactKeys(o,keys){need(o&&typeof o==='object'&&!Array.isArray(o)&&Object.keys(o).length===keys.length&&keys.every(k=>Object.hasOwn(o,k)),'descriptor-keys');}
function validateDescriptor(record){
 exactKeys(record,['schema','fields','binaryBytes','jsonBytes','elements']);need(record.schema==='m31-lossless-record-v1'&&Array.isArray(record.fields)&&record.fields.length<=128,'record-schema');
 let bytes=0,jsonBytes=2,elements=1;const keys=new Set();
 for(const f of record.fields){
  exactKeys(f,['key','stream']);need(typeof f.key==='string'&&utf8.encode(f.key).length<=4096&&!keys.has(f.key),'field-key');keys.add(f.key);const s=f.stream;
  exactKeys(s,['schema','binaryBytes','jsonBytes','elements','chunks']);need(s.schema==='m31-value-stream-v1'&&Array.isArray(s.chunks)&&s.chunks.length>0,'stream-schema');
  for(const k of ['binaryBytes','jsonBytes','elements'])need(Number.isSafeInteger(s[k])&&s[k]>0&&s[k]<=LIMITS[k],'stream-bound');
  let n=0;for(let i=0;i<s.chunks.length;i++){const p=s.chunks[i];exactKeys(p,['path','bytes','sha256']);need(/^[0-9a-f]{64}$/.test(p.sha256)&&p.path==='research/m31-tree-witness-layout-2026-10-17/results/shards/'+p.sha256+'.bin'&&Number.isInteger(p.bytes)&&p.bytes>0&&p.bytes<=LIMITS.chunkBytes&&(i===s.chunks.length-1||p.bytes===LIMITS.chunkBytes),'chunk-descriptor');n+=p.bytes;}
  need(n===s.binaryBytes,'stream-bytes');bytes+=n;elements+=1+s.elements;jsonBytes+=utf8.encode(JSON.stringify(f.key)).length+1+s.jsonBytes+(keys.size>1?1:0);
 }
 need(bytes===record.binaryBytes&&jsonBytes===record.jsonBytes&&elements===record.elements&&bytes<=LIMITS.binaryBytes&&jsonBytes<=LIMITS.jsonBytes&&elements<=LIMITS.elements,'descriptor-totals');
 need(utf8.encode(JSON.stringify(record)).length<=LIMITS.descriptorBytes,'descriptor-size');return record;
}
function packValue(value,guard=()=>{}) {
 let binaryBytes=0,elements=0,current=null,used=0,view=null;const chunks=[];
 function fresh(){if(current&&used)chunks.push(current.subarray(0,used));guard();current=new Uint8Array(LIMITS.chunkBytes);view=new DataView(current.buffer);used=0;}
 function room(n){need(n<=LIMITS.chunkBytes&&binaryBytes+n<=LIMITS.binaryBytes,'binary-cap');if(!current||used===current.length)fresh();need(used+n<=current.length,'contiguous-internal');binaryBytes+=n;}
 function raw(bytes){need(binaryBytes+bytes.length<=LIMITS.binaryBytes,'binary-cap');let at=0;while(at<bytes.length){if(!current||used===current.length)fresh();const n=Math.min(bytes.length-at,current.length-used);current.set(bytes.subarray(at,at+n),used);used+=n;at+=n;binaryBytes+=n;}}
 function byte(n){room(1);current[used++]=n;}
 function u32(n){need(Number.isSafeInteger(n)&&n>=0&&n<=0xffffffff,'u32');if(current&&used+4>current.length){const b=new Uint8Array(4);new DataView(b.buffer).setUint32(0,n,false);raw(b);}else{room(4);view.setUint32(used,n,false);used+=4;}}
 function word(s){need(/^[0-9a-f]{16}$/.test(s),'word');if(current&&used+8>current.length){const b=new Uint8Array(8);for(let i=0;i<8;i++)b[i]=parseInt(s.slice(2*i,2*i+2),16);raw(b);}else{room(8);for(let i=0;i<8;i++)current[used+i]=parseInt(s.slice(2*i,2*i+2),16);used+=8;}}
 function number(x){need(Number.isFinite(x),'finite-number');if(current&&used+8>current.length){const b=new Uint8Array(8);new DataView(b.buffer).setFloat64(0,x,false);raw(b);}else{room(8);view.setFloat64(used,x,false);used+=8;}}
 function visit(v,depth){
  need(depth<=LIMITS.depth&&++elements<=LIMITS.elements,'shape-cap');if((elements&65535)===0)guard();
  if(v===null){byte(0);return 4;}if(v===false){byte(1);return 5;}if(v===true){byte(2);return 4;}
  if(typeof v==='number'){byte(3);number(v);return utf8.encode(JSON.stringify(v)).length;}
  if(typeof v==='string'){if(/^[0-9a-f]{16}$/.test(v)){byte(7);word(v);return 18;}const b=utf8.encode(v);need(text.decode(b)===v,'noncanonical-utf8-string');byte(4);u32(b.length);raw(b);return utf8.encode(JSON.stringify(v)).length;}
  if(Array.isArray(v)){
   need(Reflect.ownKeys(v).length===v.length+1,'dense-array');let size=2+Math.max(0,v.length-1);
   const words=v.length>0&&v.every(x=>typeof x==='string'&&/^[0-9a-f]{16}$/.test(x));
   const ints=!words&&v.length>0&&v.every(x=>Number.isInteger(x)&&x>=0&&x<=0xffffffff&&!Object.is(x,-0));
   const nums=!words&&!ints&&v.length>0&&v.every(x=>typeof x==='number'&&Number.isFinite(x));
   byte(words?8:ints?9:nums?10:5);u32(v.length);
   if(words||ints||nums){need(depth+1<=LIMITS.depth,'depth-cap');need(elements+v.length<=LIMITS.elements,'elements-cap');elements+=v.length;for(let i=0;i<v.length;i++){if((i&65535)===0)guard();if(words){word(v[i]);size+=18;}else{if(ints)u32(v[i]);else number(v[i]);size+=utf8.encode(JSON.stringify(v[i])).length;}}}
   else for(const item of v)size+=visit(item,depth+1);
   need(size<=LIMITS.jsonBytes,'json-cap');return size;
  }
  need(v&&typeof v==='object'&&(Object.getPrototypeOf(v)===Object.prototype||Object.getPrototypeOf(v)===null),'object-type');
  const keys=Object.keys(v);need(Reflect.ownKeys(v).length===keys.length,'object-own-keys');byte(6);u32(keys.length);let size=2+Math.max(0,keys.length-1);
  for(const key of keys){const d=Object.getOwnPropertyDescriptor(v,key);need(d&&Object.hasOwn(d,'value'),'data-property');size+=visit(key,depth+1)+1+visit(d.value,depth+1);need(size<=LIMITS.jsonBytes,'json-cap');}return size;
 }
 const jsonBytes=visit(value,0);if(current&&used)chunks.push(current.subarray(0,used));need(jsonBytes<=LIMITS.jsonBytes,'json-cap');return {chunks,binaryBytes,jsonBytes,elements};
}
function unpackValue(chunks,expected){
 const length=chunks.reduce((n,c)=>n+c.length,0);need(length<=LIMITS.binaryBytes&&length===expected.binaryBytes,'decode-size');
 const all=new Uint8Array(length);let offset=0;for(let i=0;i<chunks.length;i++){const c=chunks[i];need(c.length>0&&c.length<=LIMITS.chunkBytes&&(i===chunks.length-1||c.length===LIMITS.chunkBytes),'chunk-size');all.set(c,offset);offset+=c.length;}
 const view=new DataView(all.buffer);let at=0,elements=0;
 function take(n){need(Number.isSafeInteger(n)&&n>=0&&at+n<=all.length,'truncated');const begin=at;at+=n;return begin;}
 function u32(){return view.getUint32(take(4),false);}function word(){let s='';const begin=take(8);for(let i=0;i<8;i++)s+=all[begin+i].toString(16).padStart(2,'0');return s;}
 function num(){const x=view.getFloat64(take(8),false);need(Number.isFinite(x),'nonfinite');return x;}
 function visit(depth){
  need(depth<=LIMITS.depth&&++elements<=LIMITS.elements,'decode-shape');const tag=all[take(1)];
  if(tag===0)return null;if(tag===1)return false;if(tag===2)return true;if(tag===3)return num();if(tag===7)return word();
  if(tag===4){const n=u32();need(n<=LIMITS.jsonBytes,'string-cap');const begin=take(n);return text.decode(all.subarray(begin,begin+n));}
  need([5,6,8,9,10].includes(tag),'unknown-tag');const n=u32();need(n<=LIMITS.elements-elements,'container-elements');
  if(tag===6){const o={};for(let i=0;i<n;i++){const key=visit(depth+1);need(typeof key==='string'&&!Object.hasOwn(o,key),'object-key');Object.defineProperty(o,key,{value:visit(depth+1),enumerable:true,writable:true,configurable:true});}return o;}
  if(tag!==5)need(n>0&&depth+1<=LIMITS.depth,'optimized-array-shape');const out=new Array(n);if(tag===5){for(let i=0;i<n;i++)out[i]=visit(depth+1);}else{elements+=n;for(let i=0;i<n;i++)out[i]=tag===8?word():tag===9?u32():num();}return out;
 }
 const result=visit(0);need(at===all.length&&elements===expected.elements,'trailing-or-element-count');return result;
}
async function encodeRecord(body,put,guard=()=>{}){
 need(body&&typeof body==='object'&&!Array.isArray(body)&&(Object.getPrototypeOf(body)===Object.prototype||Object.getPrototypeOf(body)===null),'record-object');
 need(Reflect.ownKeys(body).length===Object.keys(body).length,'record-own-fields');const fields=[];let binaryBytes=0,jsonBytes=2,elements=1;
 for(const key of Object.keys(body)){
  guard();const d=Object.getOwnPropertyDescriptor(body,key);need(d&&Object.hasOwn(d,'value'),'record-data-field');const packed=packValue(d.value,guard);binaryBytes+=packed.binaryBytes;jsonBytes+=utf8.encode(JSON.stringify(key)).length+1+packed.jsonBytes+(fields.length?1:0);elements+=1+packed.elements;
  need(binaryBytes<=LIMITS.binaryBytes&&jsonBytes<=LIMITS.jsonBytes&&elements<=LIMITS.elements,'record-cap');const refs=[];
  for(const bytes of packed.chunks){guard();const p=await put(bytes);need(p.bytes===bytes.length&&/^[0-9a-f]{64}$/.test(p.sha256),'put-receipt');refs.push(p);}
  fields.push({key,stream:{schema:'m31-value-stream-v1',binaryBytes:packed.binaryBytes,jsonBytes:packed.jsonBytes,elements:packed.elements,chunks:refs}});
 }
 return validateDescriptor({schema:'m31-lossless-record-v1',fields,binaryBytes,jsonBytes,elements});
}
async function decodeRecord(record,get){
 validateDescriptor(record);
 const body={};let bytes=0,elements=1;
 for(const field of record.fields){need(typeof field.key==='string'&&!Object.hasOwn(body,field.key)&&field.stream.schema==='m31-value-stream-v1','field-descriptor');const chunks=[];for(const p of field.stream.chunks)chunks.push(await get(p));const value=unpackValue(chunks,field.stream);Object.defineProperty(body,field.key,{value,enumerable:true,writable:true,configurable:true});bytes+=field.stream.binaryBytes;elements+=1+field.stream.elements;}
 need(bytes===record.binaryBytes&&elements===record.elements,'record-totals');return body;
}
module.exports={LIMITS,packValue,unpackValue,encodeRecord,decodeRecord,validateDescriptor};
