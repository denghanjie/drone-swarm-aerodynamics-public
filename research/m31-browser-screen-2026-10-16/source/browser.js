/* Verifies exact bundle bytes before executing any scientific factory. */
'use strict';
(() => {
const IDs=Object.freeze(['./reference-excerpt.cjs','./anchor-kernel.cjs','./lean-anchor.cjs','./kernel.cjs','./controls.cjs']);
const MAX_BUNDLE_BYTES=1024*1024;
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
window.__loadM31Sources=async function loadM31Sources(pin){
 check(!used,'one module-loader invocation');used=true;
 check(pin&&/^\/source\/[A-Za-z0-9._-]+\.js$/.test(pin.path)&&Number.isSafeInteger(pin.bytes)&&pin.bytes>0&&pin.bytes<=MAX_BUNDLE_BYTES&&/^[a-f0-9]{64}$/.test(pin.sha256),'frozen source bundle pin');
 check(Array.isArray(pin.sources)&&pin.sources.length===5&&pin.sources.every((p,i)=>p.id===IDs[i]),'frozen module allowlist');
 const response=await fetch(pin.path,{cache:'no-store',credentials:'same-origin'});check(response.ok,'bundle fetch');
 const reader=response.body.getReader(),parts=[];let length=0;
 try{for(;;){const {done,value}=await reader.read();if(done)break;length+=value.length;check(length<=pin.bytes,'bundle byte growth');parts.push(value);}}catch(error){await reader.cancel().catch(()=>{});throw error;}finally{reader.releaseLock();}
 check(length===pin.bytes,'bundle byte length');const raw=new Uint8Array(length);let at=0;for(const part of parts){raw.set(part,at);at+=part.length;}
 check(await digest(raw)===pin.sha256,'executed bundle digest');
 const verified=[];let previousEnd=0;
 for(const source of pin.sources){
  check(Number.isSafeInteger(source.offset)&&Number.isSafeInteger(source.bytes)&&source.bytes>0&&source.offset>=previousEnd&&source.offset+source.bytes<=raw.length&&/^[a-f0-9]{64}$/.test(source.sha256),'source slice bounds');
  check(await digest(raw.subarray(source.offset,source.offset+source.bytes))===source.sha256,'source slice digest');previousEnd=source.offset+source.bytes;verified.push({...source});
 }
 window.__m31SourceReceipt={bundle:{path:pin.path,bytes:pin.bytes,sha256:pin.sha256},sources:verified,verifiedBeforeFactoryExecution:true,bufferCompatibility:'local Uint8Array allocation; zero/one fill; LE float64 and uint64 DataView methods; no global Buffer or native prototype changes',nativeArithmetic:true,adapterControls:null,factoryExecutionIds:[]};
 window.__m31SourceReceipt.adapterControls=runBufferAdapterControls();
 check(window.__m31SourceReceipt.adapterControls.pass,'fixed Buffer adapter controls');
 // The actual Blob contains the verified bytes, not a separately fetched script.
 let factories=null;
 window.__M31_BUNDLE_INSTALL__=value=>{check(factories===null&&Object.keys(value).length===IDs.length&&IDs.every(id=>typeof value[id]==='function'),'bundle factory installation');factories=value;};
 const blobURL=URL.createObjectURL(new Blob([raw],{type:'text/javascript'})),script=document.createElement('script');
 try{await new Promise((resolve,reject)=>{script.onload=resolve;script.onerror=()=>reject(Error('checkpoint: verified script load'));script.src=blobURL;document.head.appendChild(script);});check(factories,'bundle installation missing');}
 finally{script.remove();URL.revokeObjectURL(blobURL);delete window.__M31_BUNDLE_INSTALL__;}
 const cache=Object.create(null);
 function require(id){check(IDs.includes(id),'CommonJS dependency allowlist');if(Object.hasOwn(cache,id))return cache[id].exports;const module={exports:{}};cache[id]=module;window.__m31SourceReceipt.factoryExecutionIds.push(id);factories[id](module,module.exports,require,BufferCompat);return module.exports;}
 return {kernel:require('./kernel.cjs'),controls:require('./controls.cjs')};
};
})();

/* Source-only browser adaptation; scientific factories execute only in the explicit entry point. */
'use strict';
(() => {
const utf8 = new TextEncoder();
const CHUNK_BYTES = 3 * 1024 * 1024; // At most 4 MiB of base64, one awaited call in flight.
const HASH_BYTES = 128 * 1024 * 1024;
const MAX_JSON_BYTES = 16 * 1024 * 1024;
function equalBytes(a,b){if(a.byteLength!==b.byteLength)return false;for(let i=0;i<a.byteLength;i++)if(a[i]!==b[i])return false;return true;}
const bytes = x => new Uint8Array(x.buffer,x.byteOffset,x.byteLength);
function assert(v,label){if(!v)throw Error('checkpoint: '+label);}
function toBytes(x){return typeof x === 'string' ? utf8.encode(x) : x instanceof Uint8Array ? x : bytes(x);}
let activeAccounting=null;
async function sha(x){const t=performance.now(),b=toBytes(x);assert(b.byteLength<=HASH_BYTES,'hash input byte cap');const result=[...new Uint8Array(await crypto.subtle.digest('SHA-256',b))].map(v=>v.toString(16).padStart(2,'0')).join('');if(activeAccounting){activeAccounting.hashMs+=performance.now()-t;activeAccounting.hashBytes+=b.length;activeAccounting.hashCalls++;}return result;}
function concat(parts,cap=HASH_BYTES){const length=parts.reduce((n,a)=>n+a.byteLength,0);assert(Number.isSafeInteger(length)&&length<=cap,'concatenation byte cap');const out=new Uint8Array(length);let at=0;for(const part of parts){out.set(part,at);at+=part.byteLength;}return out;}
function base64(b){let s='';for(let i=0;i<b.length;i+=8192)s+=String.fromCharCode(...b.subarray(i,i+8192));return btoa(s);}
async function eventLoopTurn(){const t=performance.now();await new Promise(resolve=>setTimeout(resolve,0));if(activeAccounting){activeAccounting.eventLoopYieldMs+=performance.now()-t;activeAccounting.eventLoopYields++;}}
let consumed=false;
window.runBrowserExperiment=async function runBrowserExperiment(config,inputIndex){
 assert(!consumed,'one browser invocation only');consumed=true;
 const start=performance.now(),mode={L:'lean',F:'screen'};
 let kernel,controlModule,outputBytes=0,progress={phase:'source-gate'},clockSample=null;
 const transport={chunkBytes:CHUNK_BYTES,maxBase64Characters:4*1024*1024,maxInFlight:1,acknowledgedBytes:0,acknowledgedChunks:0,completedArtifacts:0,durableExclusiveAckRequired:true};
 const stageAccounting={sourceLoadMs:0,inputFetchDecodeMs:0,artifactEncodingMs:0,base64EncodingMs:0,hashMs:0,hashBytes:0,hashCalls:0,gzipMs:0,gzipInputBytes:0,gzipOutputBytes:0,transportAckMs:0,eventLoopYieldMs:0,eventLoopYields:0,notes:'Query timers exclude loader, controls, qualification, input generation/transfer/decode, comparisons, encoding, hashes, gzip, transport, durable persistence and event-loop turns. Inclusive phase totals overlap detailed counters; do not sum them as disjoint components.'};activeAccounting=stageAccounting;
 const artifactPaths=new Set();
 function guard(){assert(performance.now()-start<=config.limits.candidateCooperativeSeconds*1000,'internal wall guard exceeded');}
 async function write(rel,payload,emergency=false){
  const b=toBytes(payload);assert(/^results\/[A-Za-z0-9._-]+$/.test(rel),'artifact path');assert(!artifactPaths.has(rel),'exclusive page artifact');artifactPaths.add(rel);
  const cap=emergency?config.limits.scientificBytes:config.limits.normalScientificBytes;
  assert(Number.isSafeInteger(cap)&&cap>0&&outputBytes+b.length<=cap,'output guard exceeded');
  const digest=await sha(b);let receipt=null;
  for(let at=0;at<b.length||at===0;at+=CHUNK_BYTES){
   const end=Math.min(b.length,at+CHUNK_BYTES),final=end===b.length,part=b.subarray(at,end);
   const encodeStart=performance.now(),encoded=base64(part);stageAccounting.base64EncodingMs+=performance.now()-encodeStart;
   const sendStart=performance.now();receipt=await window.__saveChunk(rel,encoded,final,emergency);stageAccounting.transportAckMs+=performance.now()-sendStart;
   transport.acknowledgedBytes+=part.length;transport.acknowledgedChunks++;outputBytes+=part.length;
   if(final)break;
  }
  assert(receipt&&receipt.path===rel&&receipt.bytes===b.length&&receipt.sha256===digest&&receipt.durable===true&&receipt.exclusive===true&&receipt.fsync===true&&receipt.directoryFsync===true,'durable exclusive artifact receipt');transport.completedArtifacts++;
  return {path:rel,bytes:b.length,sha256:digest};
 }
 async function json(rel,o,emergency=false){const t=performance.now(),b=utf8.encode(JSON.stringify(encode(o))+'\n');stageAccounting.artifactEncodingMs+=performance.now()-t;assert(b.length<=MAX_JSON_BYTES,'JSON artifact byte cap');return await write(rel,b,emergency);}
 async function gzip(raw){
  const gzipStart=performance.now();let offset=0,total=0;const parts=[];
  const stream=new ReadableStream({pull(controller){if(offset===raw.length){controller.close();return;}const end=Math.min(raw.length,offset+CHUNK_BYTES);controller.enqueue(raw.subarray(offset,end));offset=end;}}).pipeThrough(new CompressionStream('gzip'));
  const reader=stream.getReader();
  try{for(;;){guard();const {done,value}=await reader.read();if(done)break;total+=value.length;assert(total<=config.limits.compressedSymbolsBytesPerBundle,'compressed symbol guard exceeded');parts.push(value);}}catch(error){await reader.cancel().catch(()=>{});throw error;}finally{reader.releaseLock();}
  const out=concat(parts,config.limits.compressedSymbolsBytesPerBundle);stageAccounting.gzipMs+=performance.now()-gzipStart;stageAccounting.gzipInputBytes+=raw.length;stageAccounting.gzipOutputBytes+=out.length;return out;
 }
 async function fetchPin(pin){
  assert(pin&&/^(inputs|generation)\/[A-Za-z0-9._-]+$/.test(pin.path)&&Number.isSafeInteger(pin.bytes)&&pin.bytes>=0&&pin.bytes<=HASH_BYTES&&/^[a-f0-9]{64}$/.test(pin.sha256),'input pin');
  const response=await fetch('/'+pin.path,{cache:'no-store',credentials:'same-origin'});assert(response.ok,'input fetch');const reader=response.body.getReader(),parts=[];let count=0;
  try{for(;;){guard();const {done,value}=await reader.read();if(done)break;count+=value.length;assert(count<=pin.bytes,'input length growth');parts.push(value);}}catch(error){await reader.cancel().catch(()=>{});throw error;}finally{reader.releaseLock();}
  const b=concat(parts);assert(b.length===pin.bytes&&await sha(b)===pin.sha256,'input pin verification');return b;
 }
 function decodeStates(raw,n){assert(raw.byteLength===n*17*8,'state input shape');const view=new DataView(raw.buffer,raw.byteOffset,raw.byteLength),out=[];for(let i=0;i<n;i++){const row=[];for(let k=0;k<17;k++)row.push(view.getFloat64((17*i+k)*8,true));out.push(row);}return out;}
 function environment(){return {browserProcessId:config.browserProcessId,pageUserAgent:navigator.userAgent,platform:navigator.platform,hardwareConcurrency:navigator.hardwareConcurrency,deviceMemoryGiB:navigator.deviceMemory??null,language:navigator.language,visibility:document.visibilityState,documentHidden:document.hidden,isSecureContext:window.isSecureContext,crossOriginIsolated:window.crossOriginIsolated,performanceTimeOrigin:performance.timeOrigin,clock:'native window.performance.now monotonic milliseconds',clockSample,threads:'one page main JavaScript thread; browser helper threads/processes externally observed',renderingDuringMatchedTimings:false,queryTimerScope:'unchanged kernel.query totalMs/phasesMs',sourceLoad:window.__m31SourceReceipt??null,externalRuntimeEvidence:config.runtimeEvidence??null,rssScope:'no page RSS claim; owned Chrome-tree sampled RSS is the external supervisor responsibility'};}
const token=x=>Object.is(x,-0)?'-0':String(x);
function encode(x){if(typeof x==='number'&&(!Number.isFinite(x)||Object.is(x,-0)))return token(x);if(Array.isArray(x))return x.map(encode);if(x&&typeof x==='object')return Object.fromEntries(Object.entries(x).map(([k,v])=>[k,encode(v)]));return x;}
function clone(x){if(Array.isArray(x))return x.map(clone);if(x&&typeof x==='object')return Object.fromEntries(Object.entries(x).map(([k,v])=>[k,clone(v)]));return x;}
function exact(a,b){if(Object.is(a,b))return true;if(!a||!b||typeof a!=='object'||typeof b!=='object'||Array.isArray(a)!==Array.isArray(b))return false;const ka=Object.keys(a),kb=Object.keys(b);return ka.length===kb.length&&ka.every(k=>Object.hasOwn(b,k)&&exact(a[k],b[k]));}
const statesFor=positions=>positions.map(v=>[...v,0,0,0,0,0,0,1,0,0,0,...Array(4).fill(kernel.constants.mg/4)]);
const stateBuffer=states=>bytes(Float64Array.from(states.flat()));
function numeric(a,b){
 if(a===null||b===null)return {length:0,bad:a===b?0:1,pass:a===b,firstMismatch:a===b?null:{nullMismatch:true}};
 if(a.length!==b.length)return {length:a.length,bad:1,pass:false,firstMismatch:{lengthA:a.length,lengthB:b.length}};
 let maxAbs=0,maxRel=0,bad=0,nonfinitePairs=0,firstMismatch=null;
 for(let i=0;i<a.length;i++){if(Number.isFinite(a[i])&&Number.isFinite(b[i])){const d=Math.abs(a[i]-b[i]);maxAbs=Math.max(maxAbs,d);maxRel=Math.max(maxRel,d/Math.max(Math.abs(b[i]),Number.MIN_VALUE));}else nonfinitePairs++;if(!Object.is(a[i],b[i])){bad++;if(firstMismatch===null)firstMismatch={index:i,actual:token(a[i]),reference:token(b[i])};}}
 return {length:a.length,maxAbs,maxRel,nonfinitePairs,bad,firstMismatch,pass:bad===0};
}
function literal(q){return clone({n:q.n,symbols:q.symbols?[...q.symbols]:null,offsets:[...q.offsets],sources:[...q.src],K:[...q.kv],a:q.aa?[...q.aa]:null,input:q.input,admission:q.admission,graph:kernel.fullGraph(q),certificate:q.certificate,symbolCounts:q.symbolCounts,geometryWork:q.geometryWork,ordinaryLmax:q.ordinaryLmax,assemblyStats:q.assemblyStats??null,screen:q.screen??null});}
function modelGeometry(q){const {directedCenterTests,certifiedSkippedPairs,...rest}=q.geometryWork;return rest;}
function comparableAssembly(q){if(!q.assemblyStats)return null;const {commonSymbolBytes,...rest}=q.assemblyStats;return rest;}
function solutionValues(s){return [...s.y,...s.rotors.flatMap(a=>a.flatMap(r=>[r.alpha,r.x,r.T])),...s.residualMap.y,...s.residualMap.rotors.flatMap(a=>a.flatMap(r=>[r.alpha,r.x,r.T]))];}
function solutionRecord(s){return {values:solutionValues(s),work:s.work,residualWork:s.residualWork,residualLog:s.residualLog,sourceReceiverMismatch:s.sourceReceiverMismatch,iterations:s.iterations??1,converged:s.converged??true,lastChange:s.lastChange??null};}
const solHash=async s=>await sha(JSON.stringify(encode(solutionRecord(s))));
async function matrixHash(q){const parts=[];for(const a of [q.offsets,q.src,q.kv,q.aa])if(a)parts.push(bytes(a));parts.push(utf8.encode(JSON.stringify(encode({input:q.input,admission:q.admission,graph:kernel.fullGraph(q),symbolCounts:q.symbolCounts,ordinaryLmax:q.ordinaryLmax}))));return await sha(concat(parts));}
function solveCompare(s,ref){if(s===null||ref===null)return {pass:s===ref,notSolved:true};const values=numeric(solutionValues(s),solutionValues(ref)),work=exact(s.work,ref.work)&&exact(s.residualWork,ref.residualWork),termination=(s.iterations??1)===(ref.iterations??1)&&(s.converged??true)===(ref.converged??true)&&Object.is(s.lastChange??null,ref.lastChange??null),residual=Number.isFinite(s.residualLog)&&s.residualLog<=1e-9&&Number.isFinite(s.sourceReceiverMismatch)&&s.sourceReceiverMismatch<=2e-9,exactResidual=Object.is(s.residualLog,ref.residualLog)&&Object.is(s.sourceReceiverMismatch,ref.sourceReceiverMismatch),completeSolution=exact(s,ref);return {values,work,termination,residual,exactResidual,completeSolution,pass:values.pass&&work&&termination&&residual&&exactResidual&&completeSolution};}
function compare(q,s,ref,withSymbols,ownMethod=false){
 const c={symbols:!withSymbols||(q.symbols!==null&&ref.q.symbols!==null&&equalBytes(q.symbols,ref.q.symbols)),offsets:equalBytes(bytes(q.offsets),bytes(ref.q.offsets)),sources:equalBytes(bytes(q.src),bytes(ref.q.src)),K:numeric(q.kv,ref.q.kv),a:numeric(q.aa,ref.q.aa),prepared:equalBytes(bytes(q.p),bytes(ref.q.p))&&exact(q.nominal,ref.q.nominal)&&exact(q.S0,ref.q.S0),input:exact(q.input,ref.q.input),admission:exact(q.admission,ref.q.admission),graph:exact(kernel.fullGraph(q),kernel.fullGraph(ref.q)),dependencies:exact(q.deps,ref.q.deps),certificate:exact(q.certificate,ref.q.certificate),symbolCounts:exact(q.symbolCounts,ref.q.symbolCounts),modelGeometry:exact(modelGeometry(q),modelGeometry(ref.q)),ordinaryLmax:Object.is(q.ordinaryLmax,ref.q.ordinaryLmax),assembly:exact(comparableAssembly(q),comparableAssembly(ref.q)),symbolAllocation:q.assemblyStats.commonSymbolBytes===(withSymbols?q.n*q.n*4:0),solution:solveCompare(s,ref.s)};
 if(ownMethod){c.screen=exact(q.screen??null,ref.q.screen??null);c.allGeometryWork=exact(q.geometryWork,ref.q.geometryWork);}
 c.pass=Object.values(c).every(v=>typeof v==='boolean'?v:v.pass);return c;
}
function omissionAudit(states,L,F){
 const n=states.length,screen=F.screen,rec={eligible:screen.eligible,orderedPairs:0,omittedPairs:0,checkedRotorSymbols:0,exactOutsideSymbols:true,firstMismatch:null};
 assert(L.symbols&&F.symbols,'omission tensor missing');
 for(let i=0;i<n;i++){guard();for(let j=0;j<n;j++){if(i===j)continue;rec.orderedPairs++;const dx=states[j][0]-states[i][0],dy=states[j][1]-states[i][1],dz=states[j][2]-states[i][2];if(!screen.eligible||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))<config.screen.componentThreshold)continue;rec.omittedPairs++;for(let r=0;r<4;r++){rec.checkedRotorSymbols++;const at=4*(i*n+j)+r;if(L.symbols[at]!==1||F.symbols[at]!==1){rec.exactOutsideSymbols=false;if(rec.firstMismatch===null)rec.firstMismatch={receiver:i,source:j,rotor:r,L:L.symbols[at],F:F.symbols[at]};}}}}
 rec.screenCounts=rec.orderedPairs===screen.orderedPairVisits&&rec.omittedPairs===screen.skippedCenterNormCalls&&screen.actualCenterNormCalls===rec.orderedPairs-rec.omittedPairs&&screen.componentTests===(screen.eligible?rec.orderedPairs:0);
 rec.pass=rec.exactOutsideSymbols&&rec.screenCounts;return rec;
}
async function persist(id,label,q,s){
 const t0=performance.now(),base=`results/${id}-${label}`,artifacts={};
 if(q.symbols){const gz=await gzip(q.symbols);assert(gz.length<=config.limits.compressedSymbolsBytesPerBundle,'compressed symbol guard exceeded');artifacts.symbols={...await write(base+'-symbols.u8.gz',gz),rawSha256:await sha(q.symbols),rawBytes:q.symbols.length};}
 for(const [k,v] of Object.entries({offsets:q.offsets,sources:q.src,K:q.kv,a:q.aa}))if(v)artifacts[k]=await write(base+'-'+k+'.bin',bytes(v));
 const doc={id,label,n:q.n,input:q.input,admission:q.admission,graph:kernel.fullGraph(q),certificate:q.certificate,symbolCounts:q.symbolCounts,geometryWork:q.geometryWork,ordinaryLmax:q.ordinaryLmax,assemblyStats:q.assemblyStats??null,screen:q.screen??null,artifacts,solutions:{O:s},matrixHash:await matrixHash(q),solutionHash:s?await solHash(s):null};
 const meta=await json(base+'.json',doc);return {meta,totalPersistenceMs:performance.now()-t0,fsync:true,directoryFsync:true,fsyncScope:'file content and parent directory after exclusive link/unlink publication',durableExclusiveCollector:true,compression:'native CompressionStream gzip; compression level implementation-defined'};
}
const evidence={kind:'fresh-boids-center-screen',runtimeKind:'actual-chrome-javascript',browserProcessId:config.browserProcessId,constants:null,complete:false,controls:[],ownership:null,generation:[],qualification:[],timings:[],environmentStart:null};
async function recordTiming(item,method,block,warmup){
 const sequence=evidence.timings.length;progress={phase:'timing',id:item.id,method,block,warmup,sequence};await eventLoopTurn();guard();let result;const attemptStart=performance.now();
 try{result=kernel.query(item.states,method,guard);}catch(e){await json(`results/call-${String(sequence).padStart(3,'0')}-raw.json`,{sequence,id:item.id,method,block,warmup,status:'query-threw',observedElapsedMs:performance.now()-attemptStart},true);throw e;}
 const qualified=item.builders[method],rec={sequence,workload:'full',id:item.id,method,block,warmup,status:'returned',totalMs:result.totalMs,phasesMs:result.phasesMs,checksum:result.check,geometryWork:result.q.geometryWork,screen:result.q.screen??null,certificate:result.q.certificate,work:result.s.work,residualWork:result.s.residualWork,iterations:result.s.iterations??1,converged:result.s.converged??true,lastChange:result.s.lastChange??null,residualLog:result.s.residualLog,sourceReceiverMismatch:result.s.sourceReceiverMismatch,assemblyStats:result.q.assemblyStats??null};
 progress.currentTiming=clone(rec);rec.raw=await json(`results/call-${String(sequence).padStart(3,'0')}-raw.json`,rec);evidence.timings.push(rec);guard();
 const comparison=compare(result.q,result.s,qualified,false,true),mh=await matrixHash(result.q),sh=await solHash(result.s),checksum=Object.is(result.check,kernel.checksum(qualified.q,qualified.s)),inputUnchanged=equalBytes(item.inputBytes,stateBuffer(item.states));
 const finiteTiming=Number.isFinite(rec.totalMs)&&rec.totalMs>0&&Object.values(rec.phasesMs).every(Number.isFinite);
 rec.validation={...comparison,inputUnchanged,inputBeforeSha256:await sha(item.inputBytes),inputAfterSha256:await sha(stateBuffer(item.states)),checksum,finiteTiming,matrixHash:mh,solutionHash:sh,hashesMatch:mh===qualified.matrixHash&&sh===qualified.solutionHash,pass:comparison.pass&&inputUnchanged&&checksum&&finiteTiming&&mh===qualified.matrixHash&&sh===qualified.solutionHash};
 await json(`results/call-${String(sequence).padStart(3,'0')}.json`,rec);
 if(!rec.validation.pass){await persist(item.id,'repeat-failure-'+sequence,result.q,result.s);throw Error('checkpoint: repeat output mismatch');}
}
try{
 assert(typeof window.__saveChunk==='function','collector binding required');
 assert(config.schema==='m31-browser-screen-v1'&&exact(config.methods,['L','F'])&&exact(config.permutations,['LF','FL'])&&config.blocks===6&&config.warmupCalls===6&&config.measuredCalls===36&&config.totalCalls===42,'frozen schedule');
 assert(config.controls===48&&Array.isArray(config.controlIds)&&config.controlIds.length===48&&config.ownershipExtraBuilds===6&&config.qualificationBuilds===6&&config.qualificationSolves===6,'frozen control counts');
 assert(config.controlSolvePolicy==='untimed solve+residual iff admitted and descendingEligible; otherwise explicit no-solve reason','frozen control solve policy');
 assert(config.screen.componentThreshold===4&&config.screen.spanLimit===256,'frozen screen thresholds');
 assert(config.generation.duration===5&&config.generation.dt===.0025&&config.generation.frameEvery===.2,'frozen generation time rules');
 assert(Number.isFinite(config.limits.candidateCooperativeSeconds)&&config.limits.candidateCooperativeSeconds>0&&config.limits.candidateCooperativeSeconds<=895,'cooperative budget');
 assert(config.limits.normalScientificBytes===512*1024*1024&&config.limits.scientificBytes===528*1024*1024,'artifact byte budgets');
 assert(config.limits.compressedSymbolsBytesPerBundle===64*1024*1024,'compressed symbol cap');
 assert(typeof config.browserProcessId==='string'&&/^[A-Za-z0-9_-]{1,64}$/.test(config.browserProcessId),'process identity');
 assert(new Uint8Array(new Uint16Array([1]).buffer)[0]===1,'little endian runtime required');
 assert(config.cases.length===3&&config.cases.every((c,i)=>c.n===[1000,5000,5000][i]&&c.seed===261701+i&&c.t===5&&/^[A-Za-z0-9._-]+$/.test(c.id)),'frozen cases');
 assert(new Set(config.cases.map(c=>c.id)).size===3,'distinct case IDs');
 assert(window.isSecureContext&&crypto.subtle&&typeof CompressionStream==='function','native browser APIs required');
 const clockValues=[];for(let i=0;i<128;i++)clockValues.push(performance.now());
 assert(clockValues.every(Number.isFinite)&&clockValues.every((v,i)=>i===0||v>=clockValues[i-1]),'monotonic finite page clock');
 const deltas=clockValues.slice(1).map((v,i)=>v-clockValues[i]).filter(v=>v>0);clockSample={reads:128,minObservedPositiveDeltaMs:deltas.length?Math.min(...deltas):null,method:'fixed 128 metadata reads; no clock calibration loop'};
 const sourceStart=performance.now();const loaded=await window.__loadM31Sources(config.sourceBundle);guard();stageAccounting.sourceLoadMs=performance.now()-sourceStart;
 kernel=loaded.kernel;controlModule=loaded.controls;
 evidence.executionConfigSha256=await sha(JSON.stringify(encode(config)));evidence.inputIndexSha256=await sha(JSON.stringify(encode(inputIndex)));evidence.manifestHashScope='SHA-256 UTF-8 JSON.stringify(encode(object)), no trailing newline; controller separately retains original index file pin.';
 evidence.constants=kernel.constants;evidence.environmentStart=environment();
 assert(exact(controlModule.controlIds,config.controlIds),'exported literal control IDs');const fixedControls=controlModule.controls();assert(exact(fixedControls.map(c=>c.id),config.controlIds),'literal control IDs');
 let retained=null;
 for(const ctl of fixedControls){
  progress={phase:'control',id:ctl.id};guard();const states=statesFor(ctl.positions);
  for(const patch of ctl.statePatches??[]){assert(Number.isInteger(patch.vehicle)&&patch.vehicle>=0&&patch.vehicle<states.length&&Number.isInteger(patch.index)&&patch.index>=0&&patch.index<17,'control patch');states[patch.vehicle][patch.index]=patch.value;}
  const before=stateBuffer(states),beforeTokens=states.map(a=>a.map(token)),built={},solutions={L:null,F:null},mutationChecks={build:{},solve:{L:null,F:null}};for(const label of config.methods){built[label]=kernel.build(states,mode[label],true,guard);mutationChecks.build[label]=equalBytes(before,stateBuffer(states));}
  const buildComparison=compare(built.F,null,{q:built.L,s:null},true),audit=omissionAudit(states,built.L,built.F);
  const rec={id:ctl.id,n:states.length,inputBeforeTokens:beforeTokens,stateTokens:states.map(a=>a.map(token)),positionTokens:ctl.positions.map(a=>a.map(token)),statePatches:(ctl.statePatches??[]).map(x=>({...x,value:token(x.value)})),expectedScreenEligible:ctl.expectedScreenEligible,expectedFallbackReason:ctl.expectedFallbackReason,solvePolicy:'admitted-and-descending-only',noSolveReason:null,L:literal(built.L),F:literal(built.F),solutions,comparison:buildComparison,omissionAudit:audit,mutationChecks};
  rec.screenExpectation=Object.is(built.F.screen.eligible,ctl.expectedScreenEligible)&&Object.is(built.F.screen.fallbackReason,ctl.expectedFallbackReason);
  if(buildComparison.pass&&built.L.admission.admitted&&built.L.graph.descendingEligible){for(const label of config.methods){const q=built[label],s=kernel.solve(q,'O',kernel.schedule(q),false,guard);Object.assign(s,kernel.residual(q,s,guard));solutions[label]=s;mutationChecks.solve[label]=equalBytes(before,stateBuffer(states));}}else rec.noSolveReason=!buildComparison.pass?'model-mismatch':!built.L.admission.admitted?'admission':'ordering';
  rec.solutionComparison=solveCompare(solutions.F,solutions.L);rec.stateTokens=states.map(a=>a.map(token));rec.inputBeforeSha256=await sha(before);rec.inputAfterSha256=await sha(stateBuffer(states));rec.inputUnchanged=equalBytes(before,stateBuffer(states))&&Object.values(mutationChecks.build).every(x=>x===true)&&Object.values(mutationChecks.solve).every(x=>x===null||x===true);rec.pass=buildComparison.pass&&audit.pass&&rec.screenExpectation&&rec.solutionComparison.pass&&rec.inputUnchanged;
  const saved=await json(`results/control-${ctl.id}.json`,rec);evidence.controls.push({id:ctl.id,pass:rec.pass,pin:saved,solved:solutions.L!==null});assert(rec.pass,'control mismatch');
  if(ctl.id==='planes-66')retained={states,before,beforeTokens,built,literals:{L:rec.L,F:rec.F}};
 }
 assert(evidence.controls.length===config.controls&&retained,'control schedule mismatch');
 progress={phase:'ownership'};const extraBuilds=[],seen=[],seenArrays=[];let disjoint=true,unchanged=true;
 function checkStorage(q){for(const a of [q.p,q.offsets,q.src,q.kv,q.aa,q.symbols].filter(Boolean)){disjoint&&=a.byteOffset===0&&a.byteLength===a.buffer.byteLength&&!seen.some(b=>b.buffer===a.buffer);seen.push(a);}for(const a of [q.S0,...q.nominal,...q.deps,...(q.screen?[q.screen.min,q.screen.max,q.screen.spans]:[])]){disjoint&&=!seenArrays.includes(a)&&!q.states.some(b=>a===b);seenArrays.push(a);}}
 for(const q of Object.values(retained.built))checkStorage(q);
 assert(exact(controlModule.ownershipSequence,['L:sparse2','F:sparse2','L:planes62','F:planes62','L:fallback258','F:fallback258'])&&exact(controlModule.ownershipSequence,config.ownershipSequence)&&controlModule.ownershipSequence.length===config.ownershipExtraBuilds,'ownership schedule');
 for(const spec of controlModule.ownershipSequence){const [label,which]=spec.split(':'),positions=which==='sparse2'?[[0,0,0],[4,0,0]]:which==='fallback258'?[[0,0,0],[258,0,0]]:Array.from({length:62},(_,i)=>[0,0,i<31?0:.6]),states=statesFor(positions),before=stateBuffer(states),beforeTokens=states.map(a=>a.map(token)),q=kernel.build(states,mode[label],true,guard);checkStorage(q);const inputUnchanged=equalBytes(before,stateBuffer(states));unchanged&&=inputUnchanged;extraBuilds.push({label,id:which,n:states.length,inputBeforeTokens:beforeTokens,stateTokens:states.map(a=>a.map(token)),inputBeforeSha256:await sha(before),inputAfterSha256:await sha(stateBuffer(states)),inputUnchanged,positionTokens:positions.map(a=>a.map(token)),bundle:literal(q)});}
 unchanged&&=equalBytes(retained.before,stateBuffer(retained.states));const ownership={sequence:controlModule.ownershipSequence,extraBuilds,retained:{L:{before:retained.literals.L,after:literal(retained.built.L)},F:{before:retained.literals.F,after:literal(retained.built.F)}},retainedInputBeforeTokens:retained.beforeTokens,retainedInputAfterTokens:retained.states.map(a=>a.map(token)),retainedInputBeforeSha256:await sha(retained.before),retainedInputAfterSha256:await sha(stateBuffer(retained.states)),inputUnchanged:unchanged,returnedStorageDisjoint:disjoint};
 ownership.pass=unchanged&&disjoint&&exact(ownership.retained.L.before,ownership.retained.L.after)&&exact(ownership.retained.F.before,ownership.retained.F.after);evidence.ownership=await json('results/ownership.json',ownership);assert(ownership.pass,'ownership control mismatch');retained=null;
 const inputStart=performance.now(),cases=[];
 assert(inputIndex.kind==='fresh-airflow-off-boids-states'&&exact(inputIndex.shape,['vehicle',17])&&inputIndex.dtype==='float64le'&&inputIndex.cases.length===3,'input index schema');
 for(let caseIndex=0;caseIndex<config.cases.length;caseIndex++){
  const info=config.cases[caseIndex],entry=inputIndex.cases[caseIndex];progress={phase:'input-fetch',id:info.id};guard();
  assert(entry.id===info.id&&entry.n===info.n&&entry.seed===info.seed&&entry.t===info.t&&entry.path===`inputs/${info.id}.f64`,'input case binding');
  assert(entry.generationPin&&entry.generationPin.path===`generation/${info.id}.json`&&entry.generationPath===entry.generationPin.path,'generation metadata pin');
  const raw=await fetchPin(entry),metaRaw=await fetchPin(entry.generationPin),record=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(metaRaw));
  const expectedConfig={filter:config.generation.filter,seed:info.seed,count:info.n,mode:config.generation.mode,dt:config.generation.dt,duration:info.t,search:config.generation.search,course:config.generation.expectedCourse,airflow:'off',observation:'ideal'};
  assert(record.id===info.id&&record.n===info.n&&record.seed===info.seed&&record.complete===true&&record.initialMatches===true&&exact(record.config,expectedConfig),'generation metadata identity');
  assert(record.metrics.end===5&&record.metrics.stopReason===null&&record.metrics.failure===null&&exact(record.recording,{cadence:.2,streamed:true}),'generation completion');
  assert(record.final.path===entry.path&&record.final.bytes===entry.bytes&&record.final.sha256===entry.sha256,'generation final pin');
  const initial=await fetchPin(record.initial);assert(initial.length===info.n*17*8,'initial full state shape');
  assert(record.frames.length===26&&record.poses.frames===26&&record.poses.width===1+7*info.n,'pose frame count');
  const poses=await fetchPin(record.poses),width=(1+7*info.n)*8;assert(poses.length===26*width,'poses byte length');
  for(let frameIndex=0;frameIndex<26;frameIndex++){
   const pin=record.frames[frameIndex],frame=await fetchPin(pin);assert(pin.t===frameIndex/5&&frame.length===width,'frame metadata');
   const frameView=new DataView(frame.buffer,frame.byteOffset,frame.byteLength);assert(frameView.getFloat64(0,true)===frameIndex/5&&equalBytes(frame,poses.subarray(frameIndex*width,(frameIndex+1)*width)),'pose/frame byte agreement');
  }
  const states=decodeStates(raw,info.n),finalPose=bytes(Float64Array.from([info.t,...states.flatMap(row=>[...row.slice(0,3),...row.slice(6,10)])]));
  assert(equalBytes(finalPose,poses.subarray(25*width)),'final pose/full state agreement');
  assert(equalBytes(raw,stateBuffer(states)),'decoded full state exact bytes');
  cases.push({...info,states,inputBytes:raw,builders:{}});evidence.generation.push({id:info.id,pin:entry.generationPin,complete:true,generationMs:record.generationMs,externalGeneration:true,finalPin:{path:entry.path,bytes:entry.bytes,sha256:entry.sha256},generationEvidenceVerified:true});
  await eventLoopTurn();
 }
 stageAccounting.inputFetchDecodeMs=performance.now()-inputStart;
 for(const item of cases){
  for(const label of config.methods){
   progress={phase:'qualification',id:item.id,label};guard();const t=performance.now(),q=kernel.build(item.states,mode[label],true,guard);
   q.diagnosticGraph=kernel.fullGraph(q);
   if(!q.admission.admitted||!q.graph.descendingEligible){await persist(item.id,label,q,null);throw Error('checkpoint: qualification domain rejected');}
   const s=kernel.solve(q,'O',kernel.schedule(q),false,guard);Object.assign(s,kernel.residual(q,s,guard));
   const qualificationComputeMs=performance.now()-t,saved=await persist(item.id,label,q,s),qualified={q,s,matrixHash:await matrixHash(q),solutionHash:await solHash(s)};
   item.builders[label]=qualified;const comparison=compare(q,s,item.builders.L,true);
   comparison.inputUnchanged=equalBytes(item.inputBytes,stateBuffer(item.states));comparison.pass&&=comparison.inputUnchanged;
   const audit=label==='F'?omissionAudit(item.states,item.builders.L.q,q):null;
   const record={id:item.id,label,qualificationComputeMs,persistence:saved,comparison,omissionAudit:audit,inputBeforeSha256:await sha(item.inputBytes),inputAfterSha256:await sha(stateBuffer(item.states)),matrixHash:qualified.matrixHash,solutionHash:qualified.solutionHash};
   record.pass=comparison.pass&&(!audit||audit.pass);evidence.qualification.push(record);
   await json(`results/qualification-${item.id}-${label}.json`,record);assert(record.pass,'qualification anchor mismatch');
  }
  // Both complete tensors were persisted and element-compared before release.
  for(const label of config.methods)item.builders[label].q.symbols=null;
 }
 for(const item of cases)for(const method of config.methods)await recordTiming(item,method,-1,true);
 for(let block=0;block<config.blocks;block++)for(let j=0;j<cases.length;j++){const c=(j+block)%cases.length,item=cases[c];for(const method of config.permutations[(block+c)%2])await recordTiming(item,method,block,false);}
 assert(evidence.qualification.length===config.qualificationBuilds&&evidence.timings.length===config.totalCalls&&evidence.timings.filter(x=>x.warmup).length===config.warmupCalls&&evidence.timings.filter(x=>!x.warmup).length===config.measuredCalls&&evidence.generation.length===3,'completed schedule mismatch');
 evidence.complete=true;evidence.environmentEnd=environment();evidence.memory={pageRSSMeasured:false,externalOwnedChromeRSSRequired:true};evidence.transport=transport;evidence.stageAccounting=stageAccounting;evidence.wallMsBeforeEvidence=performance.now()-start;
 evidence.newScientificBytesBeforeEvidence=outputBytes;evidence.controlSolvePolicy='admitted-and-descending-only';evidence.actualControlSolves=2*evidence.controls.filter(x=>x.solved).length;
 const evidencePin=await json('results/evidence.json',evidence);guard();
 return {complete:true,browserProcessId:config.browserProcessId,evidencePin,controls:evidence.controls.length,generation:evidence.generation.length,qualifications:evidence.qualification.length,timingCalls:evidence.timings.length,outputBytes,elapsedMs:performance.now()-start,sourceReceipt:window.__m31SourceReceipt,accountingAtCompletion:{transport,stageAccounting}};
}catch(e){
 evidence.complete=false;
 const known=['positive coefficient guard exceeded','candidate order/uniqueness failure','invalid alpha','solve domain rejected'];
 const message=e.message?.startsWith('checkpoint: ')?e.message:known.includes(e.message)?e.message:'unexpected execution exception';
 evidence.sourceReceipt=window.__m31SourceReceipt??null;const failure={message,exceptionClass:e.constructor.name,sourceReceipt:evidence.sourceReceipt,progress,completedControls:evidence.controls.length,completedGeneration:evidence.generation.length,completedQualifications:evidence.qualification.length,completedTimings:evidence.timings.length};
 try{failure.failurePin=await json('results/failure.json',failure,true);}catch{failure.failurePersistenceFailed=true;}
 try{failure.partialEvidencePin=await json('results/partial-evidence.json',evidence,true);}catch{failure.partialEvidencePersistenceFailed=true;}
 return {complete:false,browserProcessId:config.browserProcessId,failure:encode(failure),outputBytes,elapsedMs:performance.now()-start};
}

};
})();
