/* Verifies exact bundle bytes before executing any scientific factory. */
'use strict';
(() => {
const IDs=Object.freeze(['./vendor/reference-excerpt.cjs','./vendor/anchor-kernel.cjs','./vendor/lean-anchor.cjs','./vendor/kernel.cjs','./vendor/controls.cjs','./native-load.cjs','./native-controls.cjs']);
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
 check(pin&&pin.path==='research/m31-native-load-baseline-2026-10-17/source/browser-bundle.js'&&Number.isSafeInteger(pin.bytes)&&pin.bytes>0&&pin.bytes<=MAX_BUNDLE_BYTES&&/^[a-f0-9]{64}$/.test(pin.sha256),'frozen source bundle pin');
 check(Array.isArray(pin.sources)&&pin.sources.length===7&&pin.sources.every((p,i)=>p.id===IDs[i]),'frozen module allowlist');
 const response=await fetch('/'+pin.path,{cache:'no-store',credentials:'same-origin'});check(response.ok,'bundle fetch');
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
 await window.__appendNativeRecord('source-verified',window.__m31SourceReceipt);
 check(window.__m31SourceReceipt.adapterControls.pass,'fixed Buffer adapter controls');
 // The actual Blob contains the verified bytes, not a separately fetched script.
 let factories=null;
 window.__M31_BUNDLE_INSTALL__=value=>{check(factories===null&&Object.keys(value).length===IDs.length&&IDs.every(id=>typeof value[id]==='function'),'bundle factory installation');factories=value;};
 const blobURL=URL.createObjectURL(new Blob([raw],{type:'text/javascript'})),script=document.createElement('script');
 try{await new Promise((resolve,reject)=>{script.onload=resolve;script.onerror=()=>reject(Error('checkpoint: verified script load'));script.src=blobURL;document.head.appendChild(script);});check(factories,'bundle installation missing');}
 finally{script.remove();URL.revokeObjectURL(blobURL);delete window.__M31_BUNDLE_INSTALL__;}
 const cache=Object.create(null);
 function resolve(from,requested){check(requested.startsWith('./'),'relative dependency');const base=from.split('/').slice(0,-1);const id=base.join('/')+'/'+requested.slice(2);check(IDs.includes(id),'dependency allowlist');return id;}
 function require(id){check(IDs.includes(id),'CommonJS dependency allowlist');if(Object.hasOwn(cache,id))return cache[id].exports;const module={exports:{}};cache[id]=module;window.__m31SourceReceipt.factoryExecutionIds.push(id);factories[id](module,module.exports,requested=>require(resolve(id,requested)),BufferCompat);return module.exports;}
 return {kernel:require('./vendor/kernel.cjs'),controls:require('./vendor/controls.cjs'),native:require('./native-load.cjs'),additional:require('./native-controls.cjs')};
};
})();


'use strict';
(() => {
const assert=(value,label)=>{if(!value)throw Error('checkpoint: '+label);};
const equalBytes=(a,b)=>a.byteLength===b.byteLength&&a.every((v,i)=>v===b[i]);
const bytes=x=>new Uint8Array(x.buffer,x.byteOffset,x.byteLength);
const sha=async value=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',typeof value==='string'?new TextEncoder().encode(value):value))].map(v=>v.toString(16).padStart(2,'0')).join('');
let consumed=false;
window.runNativeQualification=async function({config,bundle}){
 assert(!consumed,'single qualification invocation');consumed=true;
 const start=performance.now(),mode={L:'lean',F:'screen'};
 let kernel,controlModule,progress={phase:'source-verification'};
 const evidence={controls:[],ownership:null},emit=async(kind,body)=>{
   const receipt=await window.__appendNativeRecord(kind,body);assert(receipt?.durable===true,'durable journal acknowledgement');return receipt;
 };
 function guard(){assert(performance.now()-start<85000,'page cooperative deadline');}
 config.screen={componentThreshold:4,spanLimit:256};
 try{
 assert(isSecureContext&&crypto.subtle,'secure browser context');
 assert(new Uint8Array(new Uint16Array([1]).buffer)[0]===1,'little endian browser');
 const loaded=await window.__loadM31Sources(bundle);kernel=loaded.kernel;controlModule=loaded.controls;
 await emit('source',window.__m31SourceReceipt);
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
 assert(exact(controlModule.controlIds,config.controls.inheritedIds),'exported literal control IDs');const fixedControls=controlModule.controls();assert(exact(fixedControls.map(c=>c.id),config.controls.inheritedIds),'literal control IDs');
 let retained=null;
 for(const ctl of fixedControls){
  progress={phase:'control',id:ctl.id};await emit('intent',progress);guard();const states=statesFor(ctl.positions);
  for(const patch of ctl.statePatches??[]){assert(Number.isInteger(patch.vehicle)&&patch.vehicle>=0&&patch.vehicle<states.length&&Number.isInteger(patch.index)&&patch.index>=0&&patch.index<17,'control patch');states[patch.vehicle][patch.index]=patch.value;}
  const before=stateBuffer(states),beforeTokens=states.map(a=>a.map(token)),built={},solutions={L:null,F:null},mutationChecks={build:{},solve:{L:null,F:null}};for(const label of ['L','F']){built[label]=kernel.build(states,mode[label],true,guard);mutationChecks.build[label]=equalBytes(before,stateBuffer(states));}
  const buildComparison=compare(built.F,null,{q:built.L,s:null},true),audit=omissionAudit(states,built.L,built.F);
  const rec={id:ctl.id,n:states.length,inputBeforeTokens:beforeTokens,stateTokens:states.map(a=>a.map(token)),positionTokens:ctl.positions.map(a=>a.map(token)),statePatches:(ctl.statePatches??[]).map(x=>({...x,value:token(x.value)})),expectedScreenEligible:ctl.expectedScreenEligible,expectedFallbackReason:ctl.expectedFallbackReason,solvePolicy:'admitted-and-descending-only',noSolveReason:null,L:literal(built.L),F:literal(built.F),solutions,comparison:buildComparison,omissionAudit:audit,mutationChecks};
  rec.screenExpectation=Object.is(built.F.screen.eligible,ctl.expectedScreenEligible)&&Object.is(built.F.screen.fallbackReason,ctl.expectedFallbackReason);
  if(buildComparison.pass&&built.L.admission.admitted&&built.L.graph.descendingEligible){for(const label of ['L','F']){const q=built[label],s=kernel.solve(q,'O',kernel.schedule(q),false,guard);Object.assign(s,kernel.residual(q,s,guard));solutions[label]=s;mutationChecks.solve[label]=equalBytes(before,stateBuffer(states));}}else rec.noSolveReason=!buildComparison.pass?'model-mismatch':!built.L.admission.admitted?'admission':'ordering';
  rec.solutionComparison=solveCompare(solutions.F,solutions.L);rec.stateTokens=states.map(a=>a.map(token));rec.inputBeforeSha256=await sha(before);rec.inputAfterSha256=await sha(stateBuffer(states));rec.inputUnchanged=equalBytes(before,stateBuffer(states))&&Object.values(mutationChecks.build).every(x=>x===true)&&Object.values(mutationChecks.solve).every(x=>x===null||x===true);rec.pass=buildComparison.pass&&audit.pass&&rec.screenExpectation&&rec.solutionComparison.pass&&rec.inputUnchanged;
  await emit('inherited-control',encode(rec));evidence.controls.push({id:ctl.id,pass:rec.pass,solved:solutions.L!==null});assert(rec.pass,'control mismatch');
  if(ctl.id==='planes-66')retained={states,before,beforeTokens,built,literals:{L:rec.L,F:rec.F}};
 }
 assert(evidence.controls.length===48&&retained,'control schedule mismatch');
 progress={phase:'ownership'};await emit('intent',progress);const extraBuilds=[],seen=[],seenArrays=[];let disjoint=true,unchanged=true;
 function checkStorage(q){for(const a of [q.p,q.offsets,q.src,q.kv,q.aa,q.symbols].filter(Boolean)){disjoint&&=a.byteOffset===0&&a.byteLength===a.buffer.byteLength&&!seen.some(b=>b.buffer===a.buffer);seen.push(a);}for(const a of [q.S0,...q.nominal,...q.deps,...(q.screen?[q.screen.min,q.screen.max,q.screen.spans]:[])]){disjoint&&=!seenArrays.includes(a)&&!q.states.some(b=>a===b);seenArrays.push(a);}}
 for(const q of Object.values(retained.built))checkStorage(q);
 assert(exact(controlModule.ownershipSequence,['L:sparse2','F:sparse2','L:planes62','F:planes62','L:fallback258','F:fallback258'])&&exact(controlModule.ownershipSequence,config.controls.ownershipSequence)&&controlModule.ownershipSequence.length===6,'ownership schedule');
 for(const spec of controlModule.ownershipSequence){await emit('intent',{phase:'ownership-build',sequence:extraBuilds.length,id:spec});const [label,which]=spec.split(':'),positions=which==='sparse2'?[[0,0,0],[4,0,0]]:which==='fallback258'?[[0,0,0],[258,0,0]]:Array.from({length:62},(_,i)=>[0,0,i<31?0:.6]),states=statesFor(positions),before=stateBuffer(states),beforeTokens=states.map(a=>a.map(token)),q=kernel.build(states,mode[label],true,guard);checkStorage(q);const inputUnchanged=equalBytes(before,stateBuffer(states));unchanged&&=inputUnchanged;extraBuilds.push({label,id:which,n:states.length,inputBeforeTokens:beforeTokens,stateTokens:states.map(a=>a.map(token)),inputBeforeSha256:await sha(before),inputAfterSha256:await sha(stateBuffer(states)),inputUnchanged,positionTokens:positions.map(a=>a.map(token)),bundle:literal(q)});await emit('ownership-build',encode(extraBuilds.at(-1)));}
 unchanged&&=equalBytes(retained.before,stateBuffer(retained.states));const ownership={sequence:controlModule.ownershipSequence,extraBuilds,retained:{L:{before:retained.literals.L,after:literal(retained.built.L)},F:{before:retained.literals.F,after:literal(retained.built.F)}},retainedInputBeforeTokens:retained.beforeTokens,retainedInputAfterTokens:retained.states.map(a=>a.map(token)),retainedInputBeforeSha256:await sha(retained.before),retainedInputAfterSha256:await sha(stateBuffer(retained.states)),inputUnchanged:unchanged,returnedStorageDisjoint:disjoint};
 ownership.pass=unchanged&&disjoint&&exact(ownership.retained.L.before,ownership.retained.L.after)&&exact(ownership.retained.F.before,ownership.retained.F.after);evidence.ownership=await emit('ownership',encode(ownership));assert(ownership.pass,'ownership control mismatch');retained=null;

 const specs=loaded.additional.additionalControls();
 assert(specs.length<=24&&specs.length===config.controls.wrapper.length,'wrapper control count');
 assert(exact(loaded.additional.additionalControlIds,config.controls.wrapper.map(x=>x.id)),'wrapper control IDs');
 function inputSnapshot(value){
  if(typeof value==='number')return {number:word(value)};
  if(value===null||typeof value!=='object')return value;
  return {array:Array.isArray(value),properties:Reflect.ownKeys(value).map(key=>{
   const descriptor=Object.getOwnPropertyDescriptor(value,key);assert(Object.hasOwn(descriptor,'value'),'literal data property');
   return [key,inputSnapshot(descriptor.value)];
  })};
 }
 let heldSuccessful=null;
 function storageObjects(value,found=new Set(),seen=new Set()){
  if(value===null||typeof value!=='object'||seen.has(value))return found;seen.add(value);
  if(Array.isArray(value)||ArrayBuffer.isView(value)||value instanceof ArrayBuffer)found.add(value);
  if(ArrayBuffer.isView(value)){found.add(value.buffer);return found;}
  if(value instanceof ArrayBuffer)return found;
  for(const key of Reflect.ownKeys(value)){const d=Object.getOwnPropertyDescriptor(value,key);if(Object.hasOwn(d,'value'))storageObjects(d.value,found,seen);}
  return found;
 }
 function ownershipCheck(input,answer,id){
  const caller=storageObjects(input),current=storageObjects(answer);
  const inputStorageDisjoint=[...current].every(object=>!caller.has(object));
  const previousResultId=heldSuccessful?.id??null;
  const previousResultUnchanged=heldSuccessful===null||JSON.stringify(loaded.native.encodeEvidence(heldSuccessful.answer))===heldSuccessful.encoded;
  const previousStorageDisjoint=heldSuccessful===null||[...current].every(object=>!heldSuccessful.storage.has(object));
  const check={inputStorageDisjoint,previousResultId,previousResultUnchanged,previousStorageDisjoint,
   pass:inputStorageDisjoint&&previousResultUnchanged&&previousStorageDisjoint};
  if(answer.status==='native-success')heldSuccessful={id,answer,storage:current,encoded:JSON.stringify(loaded.native.encodeEvidence(answer))};
  return check;
 }
 for(let i=0;i<specs.length;i++){
  const spec=specs[i],expected=config.controls.wrapper[i];
  assert(spec.id===expected.id&&spec.method===expected.method&&spec.expectedStatus===expected.expectedStatus&&spec.expectedReason===expected.expectedReason,'frozen wrapper expectation');
  assert(Array.isArray(spec.input.drones)&&spec.input.drones.length<=4,'microcontrol size');
  progress={phase:'wrapper-control',id:spec.id};await emit('intent',progress);guard();
  const before=inputSnapshot(spec.input),queryStart=performance.now(),answer=loaded.native.query(spec.input,spec.method,guard),diagnosticCallMs=performance.now()-queryStart;
  const inputUnchanged=exact(before,inputSnapshot(spec.input)),ownership=ownershipCheck(spec.input,answer,'control:'+spec.id);
  let checks;try{checks=loaded.additional.evaluateControl(spec,answer);}catch(error){checks={pass:false,checks:[],errorClass:error.constructor?.name??'Error'};}
  const wire=loaded.native.encodeEvidence(answer),record={id:spec.id,method:spec.method,expectedStatus:spec.expectedStatus,
   expectedReason:spec.expectedReason??null,input:before,inputUnchanged,ownership,diagnosticCallMs,checks,evidence:wire,pass:checks.pass&&inputUnchanged&&ownership.pass};
  await emit('wrapper-control',record);assert(record.pass,'wrapper control failure');
 }
 let targetCalls=0;
 for(const item of config.cases){
  progress={phase:'raw-input',id:item.id};guard();
  const response=await fetch('/'+item.input.path,{cache:'no-store',credentials:'same-origin'});assert(response.ok,'raw input response');
  const raw=new Uint8Array(await response.arrayBuffer());assert(raw.length===item.input.bytes&&await sha(raw)===item.input.sha256,'raw input pin');
  const saved=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(raw));
  assert(Object.keys(saved).length===1&&Array.isArray(saved.drones)&&saved.drones.length===64,'raw input shape');
  const semanticInputSha256=await sha(canonical({domain:'m31-moving-admission/input/v1',id:item.id,input:saved}));assert(semanticInputSha256===item.semanticInputSha256,'semantic raw input digest');
  for(const method of item.methods){
   progress={phase:'target',sequence:targetCalls,caseId:item.id,method};await emit('intent',progress);guard();
   // Every target obtains a fresh owned decode from the same immutable raw-word file.
   const input={drones:saved.drones.map(row=>({id:row.id,state:row.state.map(fromWord)}))},before=inputSnapshot(input);
   const queryStart=performance.now(),answer=loaded.native.query(input,method,guard),diagnosticCallMs=performance.now()-queryStart;
   const wire=loaded.native.encodeEvidence(answer);wire.caseId=item.id;wire.inputFileSha256=item.input.sha256;wire.semanticInputSha256=semanticInputSha256;
   const inputUnchanged=exact(before,inputSnapshot(input)),ownership=ownershipCheck(input,answer,'target:'+item.id+':'+method);
   const call={sequence:targetCalls,caseId:item.id,method,semanticInputSha256,inputFileSha256:item.input.sha256,inputUnchanged,ownership,diagnosticCallMs,evidence:wire};
   await emit('target',call);targetCalls++;
   assert(inputUnchanged,'target input mutation');assert(ownership.pass,'target result ownership failure');
   assert(answer.status!=='resource-failure'&&answer.status!=='internal-failure','target safety failure');
   assert(['native-success','input-refused','domain-refused','numerical-failure'].includes(answer.status),'unknown native status');
   // Scientific refusals remain in the twelve-call denominator; no replacement or retry.
  }
 }
 assert(targetCalls===12,'twelve target calls');return {complete:true,targetCalls};
 }catch(error){
  await emit('failure',{...progress,id:progress.id??progress.caseId??null,
   code:String(error.message||'browser exception').startsWith('checkpoint: ')?String(error.message).slice(12):'browser exception',errorClass:error.constructor?.name??'Error'});
  return {complete:false};
 }
};
function canonical(value){if(Array.isArray(value))return '['+value.map(canonical).join(',')+']';if(value&&typeof value==='object')return '{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+canonical(value[k])).join(',')+'}';return JSON.stringify(value);}
const scratch=new DataView(new ArrayBuffer(8));
function word(value){scratch.setFloat64(0,value,false);return scratch.getBigUint64(0,false).toString(16).padStart(16,'0');}
function fromWord(value){assert(typeof value==='string'&&/^[a-f0-9]{16}$/.test(value),'raw binary64 word');scratch.setBigUint64(0,BigInt('0x'+value),false);return scratch.getFloat64(0,false);}
})();
