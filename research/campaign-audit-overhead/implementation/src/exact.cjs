'use strict';
const crypto=require('crypto');
function mismatch(path,a,b,kind){throw Object.assign(Error(`Exact mismatch at ${path}: ${kind}`),{equivalenceFailed:true,detail:{path,kind,baseline:a,candidate:b}});}
function valueWitness(v){if(v===null||typeof v!=='object')return {type:typeof v,value:v};return {type:'object',constructor:v.constructor.name,array:Array.isArray(v),...(Array.isArray(v)?{length:v.length}:{}),...(Buffer.isBuffer(v)||ArrayBuffer.isView(v)?{byteLength:v.byteLength}:{})};}
function descriptorWitness(d){return {enumerable:d.enumerable,configurable:d.configurable,kind:'value'in d?'data':'accessor',...('writable'in d?{writable:d.writable}:{}),getterPresent:'get'in d,setterPresent:'set'in d};}
function aliasWitness(entry,path,nextId,extra={}){return {referenceId:entry?entry.id:nextId,firstSeenPath:entry?entry.path:path,previouslySeen:!!entry,currentPath:path,...extra};}
function exact(a,b,path='$',seenA=new Map(),seenB=new Map()){
 if(typeof a!==typeof b)mismatch(path,valueWitness(a),valueWitness(b),'type');
 if(a===null||b===null||typeof a!=='object'){if(!Object.is(a,b))mismatch(path,typeof a==='object'&&a!==null?valueWitness(a):a,typeof b==='object'&&b!==null?valueWitness(b):b,'Object.is');return;}
 const priorA=seenA.get(a),priorB=seenB.get(b);
 if(priorA||priorB){if(priorA?.peer!==b||priorB?.peer!==a)mismatch(path,aliasWitness(priorA,path,seenA.size),aliasWitness(priorB,path,seenB.size),'reference alias');return;}
 seenA.set(a,{peer:b,path,id:seenA.size});seenB.set(b,{peer:a,path,id:seenB.size});
 if(a.constructor.name!==b.constructor.name||Array.isArray(a)!==Array.isArray(b))mismatch(path,a.constructor.name,b.constructor.name,'constructor');
 if(Buffer.isBuffer(a)||ArrayBuffer.isView(a)){if(!Buffer.from(a.buffer,a.byteOffset,a.byteLength).equals(Buffer.from(b.buffer,b.byteOffset,b.byteLength)))mismatch(path,a,b,'binary bytes');return;}
 const ak=Reflect.ownKeys(a),bk=Reflect.ownKeys(b);if(ak.length!==bk.length){let i=0;while(i<ak.length&&i<bk.length&&ak[i]===bk[i])i++;mismatch(path,{ownKeyCount:ak.length,firstDifferenceIndex:i,keyPresent:i<ak.length,key:ak[i]},{ownKeyCount:bk.length,firstDifferenceIndex:i,keyPresent:i<bk.length,key:bk[i]},'key length');}
 for(let i=0;i<ak.length;i++){
  const k=ak[i];if(k!==bk[i])mismatch(path,{index:i,key:k},{index:i,key:bk[i]},'property insertion order');
  if(k==='stack'&&a instanceof Error)continue;
  const ad=Object.getOwnPropertyDescriptor(a,k),bd=Object.getOwnPropertyDescriptor(b,k);
  for(const p of ['enumerable','configurable','writable'])if(ad[p]!==bd[p])mismatch(path+'.'+String(k),descriptorWitness(ad),descriptorWitness(bd),'descriptor');
  if('get'in ad||'get'in bd)throw Error('Getter input outside frozen data-only corpus');
  exact(ad.value,bd.value,path+'.'+String(k),seenA,seenB);
 }
 if(a instanceof Error&&a.message!==b.message)mismatch(path,a.message,b.message,'error message');
}
function exactSample(a,b){
 // Pair records are public data; this specialization preserves every key/value/order check
 // without constructing two huge reference Maps for independent pair/margin records.
 const keys=['states','location','pairs','closest','minimum','maximum','signatureSha256','raw'];
 exact(Reflect.ownKeys(a),Reflect.ownKeys(b),'sample.keys');
 for(const k of keys)if(k!=='pairs'&&Object.hasOwn(a,k))exact(a[k],b[k],'sample.'+k);
 if(a.pairs.length!==b.pairs.length)mismatch('sample.pairs.length',a.pairs.length,b.pairs.length,'length');
 const pairRefsA=new Map(),pairRefsB=new Map();
 for(let i=0;i<a.pairs.length;i++){
  const x=a.pairs[i],y=b.pairs[i];for(const [left,right,label]of [[x,y,'record'],[x.margins,y.margins,'margins']]){const ai=pairRefsA.get(left),bi=pairRefsB.get(right),refPath='pair['+i+'].'+label;if(!!ai!==!!bi||ai?.id!==bi?.id)mismatch(refPath,aliasWitness(ai,refPath,pairRefsA.size,{firstSeenPairIndex:ai?ai.pairIndex:i,firstSeenRole:ai?ai.role:label,currentPairIndex:i,currentRole:label}),aliasWitness(bi,refPath,pairRefsB.size,{firstSeenPairIndex:bi?bi.pairIndex:i,firstSeenRole:bi?bi.role:label,currentPairIndex:i,currentRole:label}),'pair reference alias');if(!ai){pairRefsA.set(left,{id:pairRefsA.size,path:refPath,pairIndex:i,role:label});pairRefsB.set(right,{id:pairRefsB.size,path:refPath,pairIndex:i,role:label});}}exact(Reflect.ownKeys(x),Reflect.ownKeys(y),'pair.keys');
  for(const k of ['down','radial','bits','receiver','rotor','source'])if(!Object.is(x[k],y[k]))mismatch(`pair[${i}].${k}`,x[k],y[k],'Object.is');
  if(!Array.isArray(x.margins)||!Array.isArray(y.margins)||Reflect.ownKeys(x.margins).length!==9||Reflect.ownKeys(y.margins).length!==9||x.margins.length!==8||y.margins.length!==8)mismatch(`pair[${i}].margins`,x.margins,y.margins,'length');
  for(let k=0;k<8;k++)if(!Object.is(x.margins[k],y.margins[k]))mismatch(`pair[${i}].margin[${k}]`,x.margins[k],y.margins[k],'Object.is');
 }
 // Cross-category winner sharing is observable and deliberately checked together.
 exact([a.closest,a.minimum,a.maximum],[b.closest,b.minimum,b.maximum],'sample.reductionAliases');
 for(const s of [a,b])if(s.raw===undefined&&Object.hasOwn(s,'raw'))throw Error('Unexpected raw field');
}
function capture(fn){try{return {ok:true,value:fn()};}catch(error){return {ok:false,error};}}
function classView(a){return Object.fromEntries(Object.keys(a).filter(k=>k!=='hash').map(k=>[k,a[k]]));}
function digestDetails(value){
 const h=crypto.createHash('sha256'),seen=new Map(),buf=Buffer.allocUnsafe(65536),strings=new Map();let offset=0,total=0;
 function flush(){if(offset){h.update(buf.subarray(0,offset));total+=offset;offset=0;}}
 function ensure(n){if(offset+n>buf.length)flush();}
 function byte(x){ensure(1);buf[offset++]=x;}
 function uint(x){ensure(4);buf.writeUInt32LE(x,offset);offset+=4;}
 function bytes(b){if(b.length>buf.length){flush();h.update(b);total+=b.length;}else{ensure(b.length);b.copy(buf,offset);offset+=b.length;}}
 function str(x){let b=strings.get(x);if(!b){b=Buffer.from(x);if(strings.size<4096)strings.set(x,b);}uint(b.length);bytes(b);}
 function walk(v){
  if(v===null){byte(0);return;}const t=typeof v;
  if(t==='undefined'){byte(1);return;}if(t==='boolean'){byte(v?3:2);return;}
  if(t==='number'){byte(4);ensure(8);buf.writeDoubleLE(v,offset);offset+=8;return;}
  if(t==='string'){byte(5);str(v);return;}
  if(t!=='object')throw Error('Unsupported frozen digest value '+t);
  if(seen.has(v)){byte(6);uint(seen.get(v));return;}seen.set(v,seen.size);
  if(Buffer.isBuffer(v)){byte(7);uint(v.length);bytes(v);return;}
  byte(Array.isArray(v)?8:9);str(v.constructor.name);const keys=Reflect.ownKeys(v);uint(keys.length);
  for(const k of keys){if(typeof k!=='string')throw Error('Symbol in frozen digest graph');str(k);const d=Object.getOwnPropertyDescriptor(v,k);if(!('value'in d))throw Error('Accessor in frozen digest graph');byte((d.enumerable?1:0)|(d.configurable?2:0)|(d.writable?4:0));walk(d.value);}
 }
 walk(value);flush();return {sha256:h.digest('hex'),bytes:total};
}
function digest(value){return digestDetails(value).sha256;}

function immutableSnapshot(value){
 const refs=[],snapshotRefs=new Map(),replacementRefs=new Map();
 function take(v,path){if(!v||typeof v!=='object'||snapshotRefs.has(v))return;const ds=Object.getOwnPropertyDescriptors(v),entry={id:refs.length,path};snapshotRefs.set(v,entry);refs.push([v,ds,entry]);for(const [key,d]of Object.entries(ds))if('value'in d)take(d.value,path+'.'+key);}
 function witness(v,path){if(v===null||typeof v!=='object')return valueWitness(v);let entry=snapshotRefs.get(v)||replacementRefs.get(v);if(!entry){entry={id:refs.length+replacementRefs.size,path};replacementRefs.set(v,entry);}return {...valueWitness(v),referenceId:entry.id,firstSeenPath:entry.path,presentAtSnapshot:snapshotRefs.has(v),currentPath:path};}
 take(value,'nonmutation');return ()=>{for(const [ref,ds,entry]of refs){const now=Object.getOwnPropertyDescriptors(ref);exact(Object.keys(ds),Object.keys(now),entry.path+'.keys');for(const k of Object.keys(ds)){const a=ds[k],b=now[k],valuePath=entry.path+'.'+k;for(const p of ['enumerable','configurable','writable','get','set'])if(!Object.is(a[p],b[p]))mismatch(valuePath,{...descriptorWitness(a),differingField:p},{...descriptorWitness(b),differingField:p},'descriptor');if(!Object.is(a.value,b.value))mismatch(valuePath,witness(a.value,valuePath),witness(b.value,valuePath),'value/reference changed; Object.is is false');}}};
}
function rawBytes(states){const b=Buffer.alloc(states.reduce((n,r)=>n+r.length*8,0));let p=0;for(const s of states)for(const x of s){b.writeDoubleLE(x,p);p+=8;}return b;}
module.exports={exact,exactSample,capture,classView,digest,digestDetails,immutableSnapshot,rawBytes,mismatch};
