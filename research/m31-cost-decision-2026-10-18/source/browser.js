'use strict';
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


const canonical=v=>JSON.stringify(sort(v));
function sort(v){return Array.isArray(v)?v.map(sort):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,sort(v[k])])):v;}
const scratch=new DataView(new ArrayBuffer(8));
function word(v){scratch.setFloat64(0,v,false);return scratch.getBigUint64(0,false).toString(16).padStart(16,'0');}
function number(w){check(/^[0-9a-f]{16}$/.test(w),'word');scratch.setBigUint64(0,BigInt('0x'+w),false);const v=scratch.getFloat64(0,false);check(Number.isFinite(v),'finite');return v;}
const ignored=new Set(['diagnostics.buildPhasesMs','diagnostics.geometryWork.gatheredNonselfCandidates','diagnostics.screen.orderedPairVisits','diagnostics.screen.componentTests']);
function normalize(v,path=''){
 if(typeof v==='number')return word(v);
 if(Array.isArray(v))return v.map(x=>normalize(x,path+'[]'));
 if(v&&typeof v==='object')return Object.fromEntries(Object.entries(v).filter(([k])=>!ignored.has(path?path+'.'+k:k)).map(([k,x])=>[k,normalize(x,path?path+'.'+k:k)]));
 return v;
}
let used=false;
window.runCost=async function(payload){
 check(!used,'one-attempt');used=true;const {inputWords,expected,bundleText,deadlineUtc}=payload;
 const end=performance.now()+170000;const guard=()=>check(performance.now()<end&&Date.now()<Date.parse(deadlineUtc),'deadline');
 const controls=runBufferAdapterControls();check(controls.pass,'buffer-controls');
 let factories;window.__M31_BUNDLE_INSTALL__=v=>{check(!factories,'install-once');factories=v;};
 const script=document.createElement('script');script.textContent=bundleText;document.head.appendChild(script);script.remove();delete window.__M31_BUNDLE_INSTALL__;
 const cache={};function load(id){guard();check(Object.hasOwn(factories,id),'factory');if(cache[id])return cache[id].exports;
  const module={exports:{}};cache[id]=module;factories[id](module,module.exports,request=>{const parts=id.split('/').slice(0,-1);for(const x of request.split('/')){if(x==='.')continue;if(x==='..')parts.pop();else parts.push(x);}return load(parts.join('/'));},BufferCompat,undefined);return module.exports;}
 const base='./research/m31-native-tree-state1000-2026-10-17/source/';
 const F=load('./research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs'),H=load(base+'native-tree.cjs'),tree=load(base+'tree.cjs');
 const expectedText=canonical(expected),inputText=JSON.stringify(inputWords);check(inputWords.drones.length===1000,'N');
 const keys=['diagnostics','status','reason','constants','raw','ids','prepared','coefficients','solution','loads','consumption'];
 const orders=[['F','H','H0','HC'],['H','HC','F','H0'],['HC','H0','H','F'],['H0','F','HC','H']];
 let calls=0;
 async function run(arm,block,position,kind,diagnostic=null){
  guard();const outer=performance.now();const input={drones:inputWords.drones.map(x=>({id:x.id,state:x.state.map(number)}))};
  const native=arm==='F'?F:H;const result=native.query(input,arm==='F'?'F':arm==='H0'?'H0':'H',guard,{treeEvidence:arm==='HC'});calls++;
  const unchanged=JSON.stringify({drones:input.drones.map(x=>({id:x.id,state:x.state.map(word)}))})===inputText;
  const queryMs=performance.now()-outer;
  const encodeStart=performance.now();let encoded;try{encoded=native.encodeEvidence(result);}catch(e){encoded={encodingFailure:String(e.message),result};}const encodeMs=performance.now()-encodeStart;
  const compareStart=performance.now();const semantic=canonical(normalize(Object.fromEntries(keys.filter(k=>Object.hasOwn(encoded,k)).map(k=>[k,encoded[k]]))));
  const equal=keys.every(k=>Object.hasOwn(encoded,k))&&semantic===expectedText;const compareMs=performance.now()-compareStart;
  const row={call:calls,kind,block,position,arm,queryMs,nativeMs:result.timing?.totalMs??null,phases:result.timing?.phasesMs??null,buildPhases:result.diagnostics?.buildPhasesMs??null,work:result.diagnostics?.geometryWork??null,encodeMs,compareMs,inputUnchanged:unchanged,semanticEqual:equal,status:result.status,diagnostic};
  const transferStart=performance.now();const receipt=await window.saveActual({row,semantic,failureBody:equal?null:encoded});
  const transferAndPersistMs=performance.now()-transferStart;await window.saveTiming({call:calls,transferAndPersistMs,persistMs:receipt.persistMs});
  check(equal&&unchanged&&result.status==='native-success','correctness');guard();
 }
 for(let block=0;block<28;block++){const order=orders[block%4];for(let position=0;position<4;position++)await run(order[position],block<4?block:block-4,position,block<4?'warm':'measured');}
 for(const [position,arm]of ['F','H','HC','H0'].entries()){
  const diagnostic={buildMs:0,gatherMs:0,buildCalls:0,gatherCalls:0};const build=tree.build,gather=tree.gather;
  tree.build=function(...args){const t=performance.now();try{return build(...args);}finally{diagnostic.buildMs+=performance.now()-t;diagnostic.buildCalls++;}};
  tree.gather=function(...args){const t=performance.now();try{return gather(...args);}finally{diagnostic.gatherMs+=performance.now()-t;diagnostic.gatherCalls++;}};
  try{await run(arm,0,position,'diagnostic',diagnostic);}finally{tree.build=build;tree.gather=gather;}
 }
 check(calls===116,'count');return {complete:true,calls,controls,orders,userAgent:navigator.userAgent};
};
