/* Verifies exact bundle bytes before executing any scientific factory. */
'use strict';
(() => {
const IDS=Object.freeze([{"id":"./research/m31-native-fresh-transfer-2026-10-17/source/vendor/reference-excerpt.cjs","path":"research/m31-native-fresh-transfer-2026-10-17/source/vendor/reference-excerpt.cjs"},{"id":"./research/m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs","path":"research/m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs"},{"id":"./research/m31-native-fresh-transfer-2026-10-17/source/vendor/lean-anchor.cjs","path":"research/m31-native-fresh-transfer-2026-10-17/source/vendor/lean-anchor.cjs"},{"id":"./research/m31-native-fresh-transfer-2026-10-17/source/vendor/kernel.cjs","path":"research/m31-native-fresh-transfer-2026-10-17/source/vendor/kernel.cjs"},{"id":"./research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs","path":"research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs"},{"id":"./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/step02c-source/physics.cjs","path":"research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/step02c-source/physics.cjs"},{"id":"./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/sim.cjs","path":"research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/sim.cjs"},{"id":"./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/grid.cjs","path":"research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/grid.cjs"},{"id":"./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/geometry.cjs","path":"research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/geometry.cjs"},{"id":"./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/factory.cjs","path":"research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/factory.cjs"},{"id":"./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/factory-wide.cjs","path":"research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/factory-wide.cjs"},{"id":"./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/wall-filter.cjs","path":"research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/wall-filter.cjs"},{"id":"./research/m31-native-tree-state1000-2026-10-17/source/transport.cjs","path":"research/m31-native-tree-state1000-2026-10-17/source/transport.cjs"},{"id":"./research/m31-native-tree-state1000-2026-10-17/source/compact-codec.cjs","path":"research/m31-native-tree-state1000-2026-10-17/source/compact-codec.cjs"},{"id":"./research/m31-native-tree-state1000-2026-10-17/source/tree.cjs","path":"research/m31-native-tree-state1000-2026-10-17/source/tree.cjs"},{"id":"./research/m31-native-tree-state1000-2026-10-17/source/native-tree.cjs","path":"research/m31-native-tree-state1000-2026-10-17/source/native-tree.cjs"},{"id":"./research/m31-native-tree-state1000-2026-10-17/source/layout.cjs","path":"research/m31-native-tree-state1000-2026-10-17/source/layout.cjs"},{"id":"./research/m31-native-tree-state1000-2026-10-17/source/browser-adapter.cjs","path":"research/m31-native-tree-state1000-2026-10-17/source/browser-adapter.cjs"},{"id":"./research/m31-native-tree-state1000-2026-10-17/source/browser-driver.cjs","path":"research/m31-native-tree-state1000-2026-10-17/source/browser-driver.cjs"}]);
const IDs=Object.freeze(IDS.map(x=>x.id));
const MAX_BUNDLE_BYTES=2*1024*1024;
function check(ok,label){if(!ok)throw Error('checkpoint: '+label);}
async function digest(b){return [...new Uint8Array(await crypto.subtle.digest('SHA-256',b))].map(v=>v.toString(16).padStart(2,'0')).join('');}
function bufferAlloc(size,fill=0){
 check(Number.isSafeInteger(size)&&size>=0&&size<=100000000,'supported Buffer allocation size');
 check(fill===0||fill===1,'supported Buffer allocation fill');
 const out=new Uint8Array(size).fill(fill),view=new DataView(out.buffer);
 const offset=(at)=>{check(Number.isInteger(at)&&at>=0&&at+8<=out.byteLength,'supported Buffer offset');return at;};
 Object.defineProperties(out,{
  writeDoubleLE:{value(value,at=0){check(typeof value==='number','Buffer float64 value');at=offset(at);view.setFloat64(at,value,true);return at+8;}},
  readDoubleLE:{value(at=0){return view.getFloat64(offset(at),true);}},
  writeBigUInt64LE:{value(value,at=0){check(typeof value==='bigint'&&value>=0n&&value<=0xffffffffffffffffn,'Buffer uint64 value');at=offset(at);view.setBigUint64(at,value,true);return at+8;}},
  readBigUInt64LE:{value(at=0){return view.getBigUint64(offset(at),true);}}
 });
 return out;
}
const BufferCompat=Object.freeze({alloc:bufferAlloc});
// Fixed adapter-only controls. These definitions are not evaluated at load time.
// The nine groups contain 56 named assertions and never call scientific code.
const BUFFER_CONTROL_SPECS=Object.freeze([
 {id:'zero-allocation',checks:['length-8','uint8array-instance','all-zero','empty-supported']},
 {id:'one-fill',checks:['length-7','all-one']},
 {id:'fresh-storage',checks:['distinct-buffers','dedicated-views','mutation-isolated','methods-own-nonenumerable']},
 {id:'float64-le',checks:['one-write-return8','one-bytes','one-read','negative-zero-write-return16','negative-zero-bytes','negative-zero-read']},
 {id:'float64-special',checks:['nan-return8','nan-roundtrip','positive-infinity-return8','positive-infinity-roundtrip','negative-infinity-return8','negative-infinity-roundtrip']},
 {id:'uint64-le',checks:['zero-return8','zero-bytes','zero-read','pattern-return16','pattern-bytes','pattern-read','maximum-return24','maximum-bytes','maximum-read']},
 {id:'offset-rejection',checks:['read-f64-negative','read-f64-fractional','read-f64-overrun','write-f64-negative','write-f64-fractional','write-f64-overrun','read-u64-negative','read-u64-fractional','read-u64-overrun','write-u64-negative','write-u64-fractional','write-u64-overrun','empty-read-f64','empty-read-u64']},
 {id:'value-rejection',checks:['uint64-negative','uint64-overflow','uint64-number','float64-string']},
 {id:'allocation-rejection',checks:['negative-size','fractional-size','nan-size','infinite-size','over-limit-size','unsupported-fill2','string-fill']}
]);
function runBufferAdapterControls(){
 const groups=[],same=(a,b)=>a.length===b.length&&a.every((value,index)=>value===b[index]);
 const rejects=fn=>{try{fn();return false;}catch{return true;}};
 function group(index,run){
  const spec=BUFFER_CONTROL_SPECS[index],record={id:spec.id,expectedChecks:spec.checks.length,checks:[],errorClass:null,pass:false};
  const test=value=>{check(record.checks.length<spec.checks.length,'adapter assertion count');record.checks.push({id:spec.checks[record.checks.length],pass:value===true});};
  try{run(test);}catch(error){record.errorClass=error.constructor?.name??'Error';}
  record.pass=record.errorClass===null&&record.checks.length===spec.checks.length&&record.checks.every(item=>item.pass);groups.push(record);
 }
 group(0,test=>{const b=BufferCompat.alloc(8);test(b.length===8);test(b instanceof Uint8Array&&b.constructor===Uint8Array);test(same(b,[0,0,0,0,0,0,0,0]));test(BufferCompat.alloc(0).length===0);});
 group(1,test=>{const b=BufferCompat.alloc(7,1);test(b.length===7);test(same(b,[1,1,1,1,1,1,1]));});
 group(2,test=>{const a=BufferCompat.alloc(8),b=BufferCompat.alloc(8);test(a.buffer!==b.buffer);test(a.byteOffset===0&&b.byteOffset===0&&a.byteLength===a.buffer.byteLength&&b.byteLength===b.buffer.byteLength);a[0]=7;test(b[0]===0);test(['readDoubleLE','writeDoubleLE','readBigUInt64LE','writeBigUInt64LE'].every(name=>Object.hasOwn(a,name)&&typeof a[name]==='function'&&Object.getOwnPropertyDescriptor(a,name).enumerable===false));});
 group(3,test=>{const b=BufferCompat.alloc(16);test(b.writeDoubleLE(1)===8);test(same(b.subarray(0,8),[0,0,0,0,0,0,240,63]));test(Object.is(b.readDoubleLE(),1));test(b.writeDoubleLE(-0,8)===16);test(same(b.subarray(8,16),[0,0,0,0,0,0,0,128]));test(Object.is(b.readDoubleLE(8),-0));});
 group(4,test=>{const b=BufferCompat.alloc(8);test(b.writeDoubleLE(NaN)===8);test(Number.isNaN(b.readDoubleLE()));test(b.writeDoubleLE(Infinity)===8);test(b.readDoubleLE()===Infinity);test(b.writeDoubleLE(-Infinity)===8);test(b.readDoubleLE()===-Infinity);});
 group(5,test=>{const b=BufferCompat.alloc(24);test(b.writeBigUInt64LE(0n)===8);test(same(b.subarray(0,8),[0,0,0,0,0,0,0,0]));test(b.readBigUInt64LE()===0n);test(b.writeBigUInt64LE(0x0123456789abcdefn,8)===16);test(same(b.subarray(8,16),[239,205,171,137,103,69,35,1]));test(b.readBigUInt64LE(8)===0x0123456789abcdefn);test(b.writeBigUInt64LE(0xffffffffffffffffn,16)===24);test(same(b.subarray(16,24),[255,255,255,255,255,255,255,255]));test(b.readBigUInt64LE(16)===0xffffffffffffffffn);});
 group(6,test=>{const b=BufferCompat.alloc(8);for(const method of ['readDoubleLE','writeDoubleLE','readBigUInt64LE','writeBigUInt64LE'])for(const offset of [-1,.5,1])test(rejects(()=>method==='writeDoubleLE'?b[method](1,offset):method==='writeBigUInt64LE'?b[method](1n,offset):b[method](offset)));const empty=BufferCompat.alloc(0);test(rejects(()=>empty.readDoubleLE()));test(rejects(()=>empty.readBigUInt64LE()));});
 group(7,test=>{const b=BufferCompat.alloc(8);test(rejects(()=>b.writeBigUInt64LE(-1n)));test(rejects(()=>b.writeBigUInt64LE(0x10000000000000000n)));test(rejects(()=>b.writeBigUInt64LE(1)));test(rejects(()=>b.writeDoubleLE('1')));});
 group(8,test=>{for(const size of [-1,.5,NaN,Infinity,100000001])test(rejects(()=>BufferCompat.alloc(size)));test(rejects(()=>BufferCompat.alloc(8,2)));test(rejects(()=>BufferCompat.alloc(8,'1')));});
 return {schema:'m31-browser-buffer-controls-v1',expectedGroups:9,expectedChecks:56,groupIds:BUFFER_CONTROL_SPECS.map(spec=>spec.id),groups,executedGroups:groups.length,executedChecks:groups.reduce((sum,item)=>sum+item.checks.length,0),beforeScientificFactories:true,pass:groups.length===9&&groups.every(item=>item.pass)&&groups.reduce((sum,item)=>sum+item.checks.length,0)===56,scope:'fixed adapter compatibility cases only; NaN payload bits and general Node Buffer API equivalence are not claimed'};
}

let used=false;
window.runNativeTreeProbe=async function(payload){
 check(!used,'single-page-invocation');used=true;
 const {config,bundle,provenance,authorization,remainingMs}=payload;
 check(authorization?.executionAllowed===true&&typeof authorization.runTokenSha256==='string'&&/^[a-f0-9]{64}$/.test(authorization.runTokenSha256),'supervised-authorization');
 check(Number.isFinite(Date.parse(authorization.launchCutoffUtc))&&Date.now()<Date.parse(authorization.launchCutoffUtc),'page-launch-cutoff');
 check(Number.isFinite(remainingMs)&&remainingMs>0&&remainingMs<=120000,'page-budget');
 const deadline=performance.now()+remainingMs;
 const guard=()=>check(performance.now()<deadline,'page-cooperative-deadline');
 let transport=null;
 const append=async(kind,body)=>{guard();check(transport,'transport-installed');let transferMilliseconds=0,persistMilliseconds=0;const start=performance.now();
  const descriptor=await transport.encodeRecord(body,async bytes=>{const hash=await digest(bytes);let raw='';for(let i=0;i<bytes.length;i+=32768)raw+=String.fromCharCode(...bytes.subarray(i,i+32768));const base64=btoa(raw),sent=performance.now();const receipt=await window.__storeTreeShard({bytes:bytes.length,sha256:hash,base64});transferMilliseconds+=performance.now()-sent;persistMilliseconds+=receipt.persistMilliseconds;check(receipt.pin?.sha256===hash&&receipt.pin.bytes===bytes.length,'shard-ack');return receipt.pin;},guard);
  const serializationMilliseconds=performance.now()-start-transferMilliseconds,sent=performance.now();const receipt=await window.__appendTreeRecord(kind,descriptor,{serializationMilliseconds,transferMilliseconds,persistMilliseconds});transferMilliseconds+=performance.now()-sent;check(receipt?.durable===true,'durable-journal-ack');return {...receipt,serializationMilliseconds,transferMilliseconds,persistMilliseconds:persistMilliseconds+receipt.persistMilliseconds};};
 guard();check(isSecureContext&&crypto.subtle,'secure-browser-context');
 check(bundle?.path==='research/m31-native-tree-state1000-2026-10-17/source/browser-bundle.js'&&bundle.bytes>0&&bundle.bytes<=MAX_BUNDLE_BYTES&&/^[a-f0-9]{64}$/.test(bundle.sha256),'bundle-pin');
 check(Array.isArray(bundle.sources)&&bundle.sources.length===IDS.length&&bundle.sources.every((p,i)=>p.id===IDS[i].id&&p.path===IDS[i].path),'bundle-source-allowlist');
 const response=await fetch('/'+bundle.path,{cache:'no-store',credentials:'same-origin'});check(response.ok,'bundle-fetch');
 const reader=response.body.getReader(),parts=[];let length=0;
 try{for(;;){guard();const {done,value}=await reader.read();if(done)break;length+=value.length;check(length<=bundle.bytes,'bundle-byte-growth');parts.push(value);}}catch(error){await reader.cancel().catch(()=>{});throw error;}finally{reader.releaseLock();}
 check(length===bundle.bytes,'bundle-byte-length');const raw=new Uint8Array(length);let at=0;for(const p of parts){raw.set(p,at);at+=p.length;}
 check(await digest(raw)===bundle.sha256,'bundle-digest');let previousEnd=0;
 for(const source of bundle.sources){guard();check(Number.isSafeInteger(source.offset)&&Number.isSafeInteger(source.bytes)&&source.bytes>0&&source.offset>=previousEnd&&source.offset+source.bytes<=raw.length,'source-slice-bounds');check(await digest(raw.subarray(source.offset,source.offset+source.bytes))===source.sha256,'source-slice-digest');previousEnd=source.offset+source.bytes;}
 const adapterControls=runBufferAdapterControls();
 const sourceRecord={bundle:{path:bundle.path,bytes:bundle.bytes,sha256:bundle.sha256},sources:bundle.sources,verifiedBeforeFactoryExecution:true,adapterControls,localFactoryProcessShim:{module:'./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/factory.cjs',env:{FLOCK_FACTORY_VARIANT:'wide'}},nativeArithmetic:true};
 check(adapterControls.pass,'buffer-compatibility-controls');
 let factories=null;window.__M31_BUNDLE_INSTALL__=value=>{check(factories===null&&Object.keys(value).length===IDs.length&&IDs.every(id=>typeof value[id]==='function'),'factory-install');factories=value;};
 const url=URL.createObjectURL(new Blob([raw],{type:'text/javascript'})),script=document.createElement('script');
 try{await new Promise((resolve,reject)=>{script.onload=resolve;script.onerror=()=>reject(Error('verified-bundle-load'));script.src=url;document.head.appendChild(script);});check(factories!==null,'factory-install-missing');}
 finally{script.remove();URL.revokeObjectURL(url);delete window.__M31_BUNDLE_INSTALL__;}
 const cache=Object.create(null),executed=[];
 function resolve(from,request){check(typeof request==='string'&&(request.startsWith('./')||request.startsWith('../')),'relative-require');const stack=from.split('/').slice(0,-1);for(const p of request.split('/')){if(p==='.')continue;if(p==='..'){check(stack.length>1,'module-traversal');stack.pop();}else stack.push(p);}const id=stack.join('/');check(IDs.includes(id),'module-allowlist');return id;}
 function load(id){guard();check(IDs.includes(id),'module-id');if(Object.hasOwn(cache,id))return cache[id].exports;const module={exports:{}};cache[id]=module;executed.push(id);const localProcess=id==='./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/factory.cjs'?Object.freeze({env:Object.freeze({FLOCK_FACTORY_VARIANT:'wide'})}):undefined;factories[id](module,module.exports,request=>load(resolve(id,request)),BufferCompat,localProcess);return module.exports;}
 transport=load('./research/m31-native-tree-state1000-2026-10-17/source/transport.cjs');await append('source',sourceRecord);
 const driver=load('./research/m31-native-tree-state1000-2026-10-17/source/browser-driver.cjs').createDriver({physics:load('./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/step02c-source/physics.cjs'),swarm:load('./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/sim.cjs'),Grid:load('./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/grid.cjs').Grid,geometry:load('./research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/geometry.cjs'),nativeF:load('./research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs'),nativeTree:load('./research/m31-native-tree-state1000-2026-10-17/source/native-tree.cjs')});
 await append('factories',{ids:executed,globalProcessModified:false,globalBufferModified:false});
 const answer=await driver.run({config,append,guard,sha:async bytes=>digest(typeof bytes==='string'?new TextEncoder().encode(bytes):bytes),provenance});guard();
 return answer;
};
})();
