'use strict';
// Standalone retained-record contract. No project modules are imported.
const crypto = require('node:crypto');
const MAX = BigInt(Number.MAX_SAFE_INTEGER);
class ContractError extends Error {
  constructor(code, detail={}) { super(code); this.name='ContractError'; this.code=code; this.detail=detail; }
}
function fail(code, detail) { throw new ContractError(code, detail); }
function requireThat(ok, code, detail={}) { if (!ok) fail(code, detail); }
function gcd(a,b) { a=a<0n?-a:a; b=b<0n?-b:b; while(b) [a,b]=[b,a%b]; return a; }
function rational(n,d=1n) {
  requireThat(typeof n==='bigint'&&typeof d==='bigint'&&d!==0n,'INVALID_RATIONAL');
  if(d<0n){n=-n;d=-d;} const g=gcd(n,d);return {n:n/g,d:d/g};
}
function decimal(token) {
  requireThat(typeof token==='string'&&token.length<=256,'INVALID_RATIONAL');
  const m=/^(-?)(0|[1-9][0-9]*)(?:\.([0-9]+))?(?:[eE]([+-]?[0-9]+))?$/.exec(token);
  requireThat(!!m,'INVALID_RATIONAL',{token});
  const exponent=m[4]===undefined?0:Number(m[4]);
  requireThat(Number.isSafeInteger(exponent)&&Math.abs(exponent)<=1024,'INVALID_RATIONAL',{token});
  const fractional=m[3]||''; let n=BigInt(m[2]+fractional)*(m[1]?-1n:1n),d=1n;
  const power=exponent-fractional.length;
  if(power>=0)n*=10n**BigInt(power);else d=10n**BigInt(-power);
  return rational(n,d);
}
function fromPair(q) {
  requireThat(q&&typeof q==='object'&&typeof q.numerator==='string'&&typeof q.denominator==='string','INVALID_TIMEBASE');
  requireThat(/^-?[0-9]+$/.test(q.numerator)&&/^[0-9]+$/.test(q.denominator)&&q.numerator.length<=256&&q.denominator.length<=256,'INVALID_TIMEBASE');
  const n=BigInt(q.numerator),d=BigInt(q.denominator);
  requireThat(n>0n&&d>0n,'INVALID_TIMEBASE');return rational(n,d);
}
const mul=(a,b)=>rational(a.n*b.n,a.d*b.d);
const div=(a,b)=>{requireThat(b.n!==0n,'INVALID_RATIONAL');return rational(a.n*b.d,a.d*b.n);};
const sub=(a,b)=>rational(a.n*b.d-b.n*a.d,a.d*b.d);
const equal=(a,b)=>a.n===b.n&&a.d===b.d;
const pair=q=>({numerator:String(q.n),denominator:String(q.d)});
function signedPair(q) {
  requireThat(q&&typeof q.numerator==='string'&&typeof q.denominator==='string'&&/^-?[0-9]+$/.test(q.numerator)&&/^[0-9]+$/.test(q.denominator),'INVALID_RATIONAL');
  return rational(BigInt(q.numerator),BigInt(q.denominator));
}
function integer(value, code='INVALID_TICK') {
  requireThat(typeof value==='number'||typeof value==='string',code);
  if(typeof value==='number')requireThat(Number.isSafeInteger(value),code);
  let q;try{q=decimal(String(value));}catch(e){fail(code,{value});}
  requireThat(q.d===1n&&q.n>=0n&&q.n<=MAX,code,{value});return q.n;
}
function index(q,code) { requireThat(q.d===1n&&q.n>=0n&&q.n<=MAX,code,{value:pair(q)});return Number(q.n); }
function pointerEscape(s){return s.replace(/~/g,'~0').replace(/\//g,'~1');}

// Complete JSON reader with RFC 6901 numeric-token indexing. It rejects duplicates,
// depth/length excess, trailing data and invalid strings/numbers. It never finds a
// nested timebase by a global regular expression or by float re-serialization.
function parseJSONNumbers(text) {
  requireThat(typeof text==='string'&&Buffer.byteLength(text)<=4194304,'JSON_SIZE');
  let at=0;const tokens=new Map();
  function ws(){while(at<text.length&&/[\x20\t\r\n]/.test(text[at]))at++;}
  function string(){const start=at;requireThat(text[at++]==='"','JSON_SYNTAX');let escaped=false;
    for(;at<text.length;at++){const c=text[at];if(c==='"'&&!escaped){at++;try{return JSON.parse(text.slice(start,at));}catch(e){fail('JSON_SYNTAX');}}if(c==='\\'&&!escaped)escaped=true;else escaped=false;}fail('JSON_SYNTAX');}
  function value(ptr,depth){requireThat(depth<=64,'JSON_DEPTH');ws();const c=text[at];
    if(c==='"')return string();
    if(c==='['){at++;ws();const a=[];if(text[at]===']'){at++;return a;}for(;;){a.push(value(ptr+'/'+a.length,depth+1));ws();if(text[at]===']'){at++;return a;}requireThat(text[at++ ]===',','JSON_SYNTAX');}}
    if(c==='{'){at++;ws();const o=Object.create(null);if(text[at]==='}'){at++;return o;}for(;;){ws();requireThat(text[at]==='"','JSON_SYNTAX');const key=string();requireThat(!Object.hasOwn(o,key),'JSON_DUPLICATE_KEY',{pointer:ptr,key});ws();requireThat(text[at++ ]===':','JSON_SYNTAX');o[key]=value(ptr+'/'+pointerEscape(key),depth+1);ws();if(text[at]==='}'){at++;return o;}requireThat(text[at++ ]===',','JSON_SYNTAX');}}
    for(const [literal,result]of [['true',true],['false',false],['null',null]])if(text.startsWith(literal,at)){at+=literal.length;return result;}
    const match=/-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/y;match.lastIndex=at;const found=match.exec(text);
    requireThat(!!found,'JSON_SYNTAX',{offset:at});at=match.lastIndex;tokens.set(ptr,found[0]);const number=Number(found[0]);requireThat(Number.isFinite(number),'JSON_NONFINITE',{pointer:ptr});return number;
  }
  const data=value('',0);ws();requireThat(at===text.length,'JSON_TRAILING_DATA',{offset:at});return {data,tokens};
}
function tokenRational(parsed,ptr,code='MISSING_TIMEBASE') {requireThat(parsed.tokens.has(ptr),code,{pointer:ptr});return decimal(parsed.tokens.get(ptr));}
function tokenInteger(parsed,ptr,code='MISSING_TICK'){requireThat(parsed.tokens.has(ptr),code,{pointer:ptr});return Number(integer(parsed.tokens.get(ptr)));}
function jsonEqual(a,b){return JSON.stringify(a)===JSON.stringify(b);}
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function stateBytes(state){requireThat(Array.isArray(state)&&state.length===16,'STATE_SHAPE');const b=Buffer.alloc(2176);let offset=0;
  for(let i=0;i<16;i++){requireThat(Array.isArray(state[i])&&state[i].length===17,'STATE_SHAPE',{drone:i});for(let j=0;j<17;j++){const x=state[i][j];requireThat(typeof x==='number'&&Number.isFinite(x),'STATE_SHAPE',{drone:i,field:j});b.writeDoubleLE(x,offset);offset+=8;}}return b;}
function verifyStateBytes(actual,witnesses){requireThat(Buffer.isBuffer(actual)&&actual.length===2176,'STATE_SHAPE');requireThat(Array.isArray(witnesses)&&witnesses.length>0,'STATE_IDENTITY');const out=[];for(const w of witnesses){requireThat(Buffer.isBuffer(w.bytes)&&w.bytes.length===2176,'STATE_SHAPE');requireThat(actual.equals(w.bytes),'STATE_IDENTITY',{source:sha(actual),witness:sha(w.bytes),identity:w.identity});out.push({identity:w.identity,sha256:sha(w.bytes),direct_equal:true});}return {state_sha256:sha(actual),bytes:actual.length,witnesses:out};}

// readJSON(path) is supplied by the harness's bounded, verified read adapter.
function normalize(selector,registration,readJSON,identityByPath,canonicalPair) {
  const source=readJSON(registration.run_path),run=source.data,own=readJSON(selector.path),ownData=own.data;
  const side=readJSON(registration.raw.sidecar_path),raw=registration.raw.sidecar_wrapper?side.data.originalSidecar:side.data;
  const prefix=registration.raw.sidecar_wrapper?'/originalSidecar':'';
  const audit=readJSON(registration.anchor.metadata_path).data;
  requireThat(run.runId===registration.run_id&&run.config.seed===registration.seed,'SOURCE_IDENTITY_CONFLICT');
  requireThat(run.config.count===16&&typeof run.complete==='boolean','SOURCE_IDENTITY_CONFLICT');
  requireThat(raw&&raw.runId===run.runId&&jsonEqual(raw,run[registration.raw.run_member]),'SOURCE_IDENTITY_CONFLICT');
  requireThat(jsonEqual(raw.shape,registration.raw.shape)&&raw.shape[1]===16&&raw.shape[2]===17,'STATE_SHAPE');
  const rawBytesDeclared=registration.raw.sidecar_wrapper?raw.uncompressedBytes:raw.bytes;
  const rawHashDeclared=registration.raw.sidecar_wrapper?raw.uncompressedSha256:raw.sha256;
  const rawIdentity=identityByPath.get(registration.raw.path);
  requireThat(rawIdentity&&rawBytesDeclared===rawIdentity.bytes&&rawHashDeclared===rawIdentity.sha256&&raw.shape[0]*2176===rawBytesDeclared,'SOURCE_FILE_IDENTITY');
  requireThat(audit.id===registration.anchor.audit_id&&audit.samples===registration.anchor.entry_count,'SOURCE_IDENTITY_CONFLICT');
  const streamIdentity=identityByPath.get(registration.anchor.stream_path);
  requireThat(streamIdentity&&audit.signatureStream.bytes===streamIdentity.bytes&&audit.signatureStream.sha256===streamIdentity.sha256&&audit.samples*32===streamIdentity.bytes,'STREAM_IDENTITY');
  requireThat('research-next/implementation/'+audit.signatureStream.path===registration.anchor.stream_path,'SOURCE_IDENTITY_CONFLICT');
  const q=tokenRational(source,'/config/baseTickSeconds'),cq=fromPair(canonicalPair),dt=tokenRational(side,prefix+'/dt');
  requireThat(equal(q,fromPair(registration.source_clock.quantum_seconds)),'CLOCK_METADATA_CONFLICT');
  const first=selector.state_pointer==='/initial',isStop=selector.state_pointer==='/state';
  const sourceTick=first?selector.initial_tick_literal:tokenInteger(own,selector.source_tick_pointer);
  const requested=tokenRational(source,'/config/duration','TIME_CONFLICT');
  const historical=registration.raw.sidecar_wrapper;
  const rawClock=historical?q:tokenRational(side,'/baseTickSeconds');
  const step=tokenInteger(source,'/config/stepTicks');
  const physicsDt=tokenRational(source,'/config/physicsDt','CLOCK_METADATA_CONFLICT');
  requireThat(equal(physicsDt,mul(q,rational(BigInt(step)))),'CLOCK_METADATA_CONFLICT');
  if(historical){requireThat(side.data.encoding==='little-endian Float64 bytes; no values interpreted'&&raw.encoding==='gzip / little-endian Float64','SOURCE_IDENTITY_CONFLICT');
    const preflight=readJSON(registration.anchor.schedule_record_path),p=preflight.data;
    requireThat(p.id===registration.anchor.audit_id&&p.seed===registration.seed&&p.passed===true&&p.visitedEndpoints===raw.shape[0]&&p.expectedEndpoints===raw.shape[0]&&jsonEqual(p.input,raw),'SOURCE_IDENTITY_CONFLICT');
    requireThat(p.sampleSchedule===registration.anchor.schedule_literal&&equal(tokenRational(preflight,'/baseTickSeconds'),cq),'CLOCK_METADATA_CONFLICT');
    requireThat(equal(tokenRational(side,prefix+'/startTime'),rational(0n))&&equal(tokenRational(side,prefix+'/endTime'),mul(dt,rational(BigInt(raw.shape[0]-1)))),'TIME_CONFLICT');
    requireThat(equal(dt,mul(q,rational(BigInt(step)))),'CLOCK_METADATA_CONFLICT');
  }else{
    requireThat(raw.encoding==='little-endian Float64, uncompressed'&&raw.count===16,'SOURCE_IDENTITY_CONFLICT');
    requireThat(run.signatureSchedule===registration.anchor.schedule_literal,'ROLE_SCHEDULE_CONFLICT');
    requireThat(equal(rawClock,q)&&raw.cadenceTicks===registration.raw.cadence_current_ticks&&equal(dt,mul(q,rational(BigInt(raw.cadenceTicks)))),'CLOCK_METADATA_CONFLICT');
  }
  requireThat(equal(dt,mul(cq,rational(BigInt(registration.raw.cadence_current_ticks)))),'CLOCK_METADATA_CONFLICT');
  const partial=!first&&!run.complete;
  const stop=run.stop;
  let state=ownData[selector.state_pointer.slice(1)];
  const metadata={selectorId:selector.id,selectorSide:selector.state_pointer.slice(1),sourcePath:selector.path,sourceSha256:identityByPath.get(selector.path).sha256,sourceIdentity:identityByPath.get(selector.path),sourceRunId:run.runId,runId:ownData.runId,seed:run.config.seed,sourceClock:pair(q),clockReference:pair(q),canonicalClock:canonicalPair,sourceTick,sourceEndTick:tokenInteger(source,'/endTick'),declaredEndTime:!first&&source.tokens.has('/endTime')?pair(tokenRational(source,'/endTime')):null,requestedDuration:pair(requested),complete:run.complete,partialFinal:partial,role:'endpoint',schedule:registration.anchor.schedule,expectedSchedule:registration.anchor.schedule,anchorAuditId:registration.anchor.audit_id,expectedAnchorAuditId:registration.anchor.audit_id,stepCurrentTicks:registration.anchor.step_current_ticks,sourceStepTicks:step,signatureCount:audit.samples,signaturePath:registration.anchor.stream_path,signatureIdentity:streamIdentity,rawPath:registration.raw.path,rawRows:raw.shape[0],rawDt:pair(dt),rawStartTime:{numerator:'0',denominator:'1'},rawBaseTickSeconds:pair(rawClock),rawClockReference:pair(rawClock),allowPeerWitness:selector.id==='json-5-final'||selector.id==='json-exact-P1-stop',state,peerStates:[],exactStoppedState:partial?stop&&stop.exactStoppedState:undefined,phase:partial?stop&&stop.phase:undefined,stopTick:partial?stop&&stop.tick:undefined,stopRunId:partial?stop&&stop.runId:undefined};
  if(partial){
    const failurePath='research-next/implementation/results/failures/s840131-P1.json';const failure=readJSON(failurePath).data;
    requireThat(stop&&failure.runId===run.runId&&stop.runId===run.runId&&failure.tick===run.endTick&&stop.tick===run.endTick,'SOURCE_IDENTITY_CONFLICT');
    requireThat(stop.exactStoppedState===true&&failure.exactStoppedState===true,'NOT_EXACT_STOP');
    requireThat(stop.phase==='accepted-endpoint'&&failure.phase==='accepted-endpoint','ROLE_SCHEDULE_CONFLICT');
    metadata.peerStates=[{identity:registration.run_path+'#/final',path:registration.run_path,pointer:'/final',state:run.final},{identity:registration.run_path+'#/stop/state',path:registration.run_path,pointer:'/stop/state',state:stop.state},{identity:failurePath+'#/state',path:failurePath,pointer:'/state',state:failure.state}];
    metadata.peerPrimary=isStop?{path:registration.run_path,pointer:'/final'}:{path:failurePath,pointer:'/state'};
    if(isStop){metadata.exactStoppedState=ownData.exactStoppedState;metadata.phase=ownData.phase;metadata.stopTick=ownData.tick;metadata.stopRunId=ownData.runId;}
  }
  return metadata;
}
function rationalKernel(sourceTick,sourceClock,canonicalClock){const n=integer(sourceTick),t=mul(rational(n),fromPair(sourceClock));return {physicalTime:pair(t),canonicalTick:index(div(t,fromPair(canonicalClock)),'NONINTEGER_CANONICAL_TICK')};}
function anchorIndex(canonicalTick,stepCurrentTicks,schedule){requireThat(['preflight-row','accepted-endpoint','joint-5'].includes(schedule),'UNSUPPORTED_SCHEDULE');const n=integer(canonicalTick),step=integer(stepCurrentTicks);requireThat(step>0n,'NONINTEGER_ANCHOR');const base=div(rational(n),rational(step));index(base,'NONINTEGER_ANCHOR');return index(mul(base,rational(schedule==='joint-5'?5n:1n)),'NONINTEGER_ANCHOR');}
function resolve(metadata){const m=metadata;
  requireThat(Object.hasOwn(m,'sourceClock')&&m.sourceClock!==null,'MISSING_TIMEBASE');const q=fromPair(m.sourceClock);
  requireThat(equal(q,fromPair(m.clockReference))&&equal(fromPair(m.rawBaseTickSeconds),fromPair(m.rawClockReference)),'CLOCK_METADATA_CONFLICT');
  requireThat(m.runId===m.sourceRunId&&m.anchorAuditId===m.expectedAnchorAuditId,'SOURCE_IDENTITY_CONFLICT');
  requireThat(['preflight-row','accepted-endpoint','joint-5'].includes(m.schedule),'UNSUPPORTED_SCHEDULE');
  requireThat(m.schedule===m.expectedSchedule&&m.role==='endpoint','ROLE_SCHEDULE_CONFLICT');
  requireThat(Object.hasOwn(m,'sourceTick')&&m.sourceTick!==null,'MISSING_TICK');
  const n=integer(m.sourceTick),t=mul(rational(n),q);
  if(m.declaredEndTime!==null)requireThat(equal(t,signedPair(m.declaredEndTime)),'TIME_CONFLICT');
  if(m.selectorSide!=='initial'&&m.complete)requireThat(equal(t,signedPair(m.requestedDuration)),'TIME_CONFLICT');
  if(m.partialFinal){requireThat(m.allowPeerWitness&&m.stopRunId===m.sourceRunId&&m.stopTick===Number(n)&&m.sourceEndTick===Number(n),'SOURCE_IDENTITY_CONFLICT');requireThat(m.exactStoppedState===true,'NOT_EXACT_STOP');requireThat(m.phase==='accepted-endpoint','ROLE_SCHEDULE_CONFLICT');}
  const current=index(div(t,fromPair(m.canonicalClock)),'NONINTEGER_CANONICAL_TICK');
  const rr=div(sub(t,signedPair(m.rawStartTime)),fromPair(m.rawDt));let rawRow=null;
  if(rr.d===1n){rawRow=index(rr,'RAW_RANGE');requireThat(rawRow<m.rawRows,'RAW_RANGE');}
  else requireThat(m.allowPeerWitness&&m.partialFinal,'UNAVAILABLE_EXACT_RAW_ROW');
  const entry=anchorIndex(current,m.stepCurrentTicks,m.schedule);
  requireThat(entry<m.signatureCount,'ANCHOR_RANGE');
  if(m.schedule==='preflight-row')requireThat(rawRow===entry,'EVENT_IDENTITY_CONFLICT');
  return {sourcePath:m.sourcePath,sourceSha256:m.sourceSha256,sourceRunId:m.sourceRunId,seed:m.seed,sourceTick:Number(n),sourceClock:pair(q),canonicalClock:m.canonicalClock,physicalTime:pair(t),canonicalTick:current,role:m.role,schedule:m.schedule,anchorAuditId:m.anchorAuditId,rawRow,rawOffsetBytes:rawRow===null?null:rawRow*2176,rawWitness:rawRow===null?'unavailable':'retained-raw-row',identityWitness:rawRow===null?{kind:'peer-json',sourceKind:m.selectorSide==='state'?'peer-final-and-embedded-stop-json':'peer-exact-stop-json',primary:m.peerPrimary,records:m.peerStates.map(p=>({path:p.path,pointer:p.pointer})),limitation:'Correlated retained JSON representations; no exact sparse raw row and no independent proof of signature/state association.'}:{kind:'retained-raw-row',sourceKind:'retained-raw-row',primary:{path:m.rawPath,pointer:null,row:rawRow,offsetBytes:rawRow*2176},records:[{path:m.rawPath,pointer:null,row:rawRow,offsetBytes:rawRow*2176}],limitation:null},anchorEntry:entry,anchorOffsetBytes:entry*32,signaturePath:m.signaturePath,phase:m.partialFinal?m.phase:null};
}
function validateDescriptor(d,oracle,m,registration,canonicalPair){const e=oracle.expected;
  requireThat(registration&&canonicalPair,'MISSING_PROVENANCE');
  requireThat(d.sourcePath===oracle.path&&d.sourceSha256===m.sourceIdentity.sha256&&d.sourceRunId===registration.run_id&&d.seed===registration.seed&&d.anchorAuditId===registration.anchor.audit_id&&d.signaturePath===registration.anchor.stream_path,'SOURCE_IDENTITY_CONFLICT');
  requireThat(equal(fromPair(d.sourceClock),fromPair(registration.source_clock.quantum_seconds))&&equal(fromPair(d.canonicalClock),fromPair(canonicalPair)),'CLOCK_METADATA_CONFLICT');
  const expectedPhase=oracle.required_phase||(!registration.complete&&oracle.state_pointer!=='/initial'?'accepted-endpoint':null);
  requireThat(d.phase===expectedPhase,'ROLE_SCHEDULE_CONFLICT');
  requireThat(d.sourceTick===e.source_tick&&d.canonicalTick===e.canonical_tick&&equal(signedPair(d.physicalTime),signedPair(e.physical_time_seconds)),'EVENT_IDENTITY_CONFLICT');
  requireThat(d.role===oracle.role&&d.schedule===registration.anchor.schedule,'ROLE_SCHEDULE_CONFLICT');
  requireThat(Number.isSafeInteger(d.anchorEntry)&&d.anchorEntry>=0&&d.anchorEntry<m.signatureCount,'ANCHOR_RANGE');
  if(m.schedule==='joint-5')requireThat(d.anchorEntry%5===0,'ROLE_SCHEDULE_CONFLICT');
  requireThat(d.anchorEntry===e.anchor_entry,'EVENT_IDENTITY_CONFLICT');
  if(e.raw_row===null)requireThat(d.rawRow===null&&d.rawWitness==='unavailable','UNAVAILABLE_EXACT_RAW_ROW');
  else requireThat(d.rawRow===e.raw_row&&d.rawWitness==='retained-raw-row','EVENT_IDENTITY_CONFLICT');
  requireThat(d.rawOffsetBytes===e.raw_offset_bytes&&d.anchorOffsetBytes===e.anchor_offset_bytes,'OFFSET_CONFLICT');
  validateWitnessProvenance(d,oracle,registration);
  return true;
}
function validateWitnessProvenance(d,oracle,registration){
  const e=oracle.expected,w=d.identityWitness;requireThat(w&&w.primary&&Array.isArray(w.records),'MISSING_PROVENANCE');
  requireThat(w.sourceKind===e.identity_witness_kind&&w.primary.path===e.identity_witness_path&&w.primary.pointer===e.identity_witness_pointer,'WITNESS_PROVENANCE');
  if(e.raw_row!==null){
    const expected={path:e.identity_witness_path,pointer:null,row:e.raw_row,offsetBytes:e.raw_offset_bytes};
    requireThat(w.kind==='retained-raw-row'&&w.limitation===null&&jsonEqual(w.primary,expected)&&jsonEqual(w.records,[expected]),'WITNESS_PROVENANCE');
  }else{
    requireThat(w.kind==='peer-json'&&w.limitation==='Correlated retained JSON representations; no exact sparse raw row and no independent proof of signature/state association.','WITNESS_PROVENANCE');
    const failurePath=e.identity_witness_kind==='peer-exact-stop-json'?e.identity_witness_path:oracle.path;
    const expected=[{path:registration.run_path,pointer:'/final'},{path:registration.run_path,pointer:'/stop/state'},{path:failurePath,pointer:'/state'}];
    requireThat(jsonEqual(w.records,expected)&&w.records.some(p=>p.path===w.primary.path&&p.pointer===w.primary.pointer),'WITNESS_PROVENANCE');
    if(e.additional_witness_pointer)requireThat(w.records.some(p=>p.path===e.identity_witness_path&&p.pointer===e.additional_witness_pointer),'WITNESS_PROVENANCE');
  }
  return true;
}
function verifyOpaqueStream(bytes,identity){requireThat(Buffer.isBuffer(bytes)&&bytes.length===identity.bytes&&sha(bytes)===identity.sha256,'STREAM_IDENTITY');return true;}
function verifySourceIdentity(actual,expected){requireThat(actual.bytes===expected.bytes&&actual.sha256===expected.sha256,'SOURCE_FILE_IDENTITY');return true;}
module.exports={validateWitnessProvenance,verifyOpaqueStream,verifySourceIdentity,ContractError,fail,requireThat,rational,decimal,fromPair,signedPair,mul,div,sub,equal,pair,integer,index,parseJSONNumbers,tokenRational,tokenInteger,sha,stateBytes,verifyStateBytes,normalize,rationalKernel,anchorIndex,resolve,validateDescriptor};
