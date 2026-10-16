'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const F=require('./binary64-interval.cjs'),Q=require('./zero-filter.cjs');
const A=require('../../m31-screening-cost-2026-10-17/source/adapter.cjs');
const R=require('../../m31-screening-cost-2026-10-17/source/rational.cjs');
const P=require('../../m31-screening-cost-2026-10-17/source/pair-prepared.cjs');
const specPath=path.join(__dirname,'spec.json'),specBytes=fs.readFileSync(specPath),spec=JSON.parse(specBytes);
const contract=require('./result-contract.json');
const output=process.env.RESEARCH_RESULT_PATH,manifest=process.env.RESEARCH_SOURCE_MANIFEST_PATH;
if(!output||!manifest)throw Error('Result and manifest paths required');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const sourceManifestSha256=sha(fs.readFileSync(manifest)),specSha256=sha(specBytes);
function durableDirectory(p){const f=fs.openSync(p,'r');try{fs.fsyncSync(f);}finally{fs.closeSync(f);}}
const journal=fs.openSync(output+'.jsonl','wx');durableDirectory(path.dirname(output));
let journalEvents=0;
function append(event){const line=JSON.stringify(event)+'\n';if(Buffer.byteLength(line)>128*1024)throw Error('Journal event budget exceeded');fs.writeSync(journal,line);fs.fsyncSync(journal);journalEvents++;}
append({kind:'header',schema:contract.journalSchema,specId:spec.id,sourceManifestSha256,specSha256});
const constantIntervals=Q.constants(A.constantBits),records=[];
function exact(value){return {center:value.center.map(R.fromBits),axis:value.axis.map(R.fromBits),points:value.points.map(v=>v.map(R.fromBits)),forces:value.forces.map(R.fromBits)};}
function primitive(c){
 let outcome;
 try{
  if(['nextUp','nextDown'].includes(c.op)){
   const a=F.fromBits(c.word);outcome={kind:'word',word:A.bits(F[c.op](a.l))};
  }else{
   if(!['add','sub','mul','div','square'].includes(c.op))throw Error('Unknown primitive');
   const args=c.args.map(a=>F.interval(F.fromBits(a.l).l,F.fromBits(a.u).u));
   if(args.length!==(c.op==='square'?1:2))throw Error('Wrong primitive arity');
   const result=F[c.op](...args);outcome={kind:'interval',l:A.bits(result.l),u:A.bits(result.u)};
  }
 }catch(e){if(e instanceof F.Fallback)outcome={kind:'fallback',reason:e.reason};else throw e;}
 return {kind:'primitive',id:c.id,op:c.op,...(['nextUp','nextDown'].includes(c.op)?{word:c.word}:{args:c.args}),outcome};
}
function pair(c){
 const input={receiver:c.receiver.slice(),source:c.source.slice(),rotor:c.rotor};
 if(!Number.isInteger(input.rotor)||input.rotor<0||input.rotor>3||[input.receiver,input.source].some(v=>v.length!==17||v.some(w=>typeof w!=='string'||!/^[0-9a-f]{16}$/.test(w))))throw Error('Invalid frozen pair fixture');
 const prepared=A.prepare(input);let baseline,candidate;
 if(prepared.rejection){baseline={status:'rejected',branch:prepared.rejection};candidate={decision:{kind:'preparation'},result:{...baseline}};}
 else{
  // Both representations are local to this invocation and derive from these
  // identical admitted words. Neither is supplied by a separate caller/cache.
  const pr=prepared.prepared.receiver,ps=prepared.prepared.source;
  const er=exact(pr),es=exact(ps),fr=Q.prepare(pr),fsrc=Q.prepare(ps);
  baseline=P.query(er,es,input.rotor);
  candidate=Q.query(P.query,er,es,fr,fsrc,input.rotor,constantIntervals);
 }
 return {kind:'pair',id:c.id,input,prepared,baseline,candidate};
}
for(const c of spec.records){const row=c.kind==='primitive'?primitive(c):c.kind==='pair'?pair(c):(()=>{throw Error('Unknown record kind');})();records.push(row);append({kind:'record',row});}
if(records.length!==spec.expectedRecords)throw Error('Allocation count mismatch');
append({kind:'complete',records:records.length});fs.closeSync(journal);
const doc={schema:contract.schema,specId:spec.id,sourceManifestSha256,specSha256,constants:A.constantBits,runtime:{node:process.version,v8:process.versions.v8,platform:process.platform,arch:process.arch},records};
const serialized=JSON.stringify(doc)+'\n';if(Buffer.byteLength(serialized)>16*1024*1024)throw Error('Result budget exceeded');
const fd=fs.openSync(output,'wx');try{fs.writeFileSync(fd,serialized);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}durableDirectory(path.dirname(output));
console.log(JSON.stringify({records:records.length,journalEvents}));
