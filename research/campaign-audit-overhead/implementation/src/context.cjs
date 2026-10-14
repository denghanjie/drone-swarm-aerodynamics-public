'use strict';
const fs=require('fs'),path=require('path'),v8=require('v8');
const {loadAudit,sha,STUDY,storage}=require('./load-audit.cjs');
const E=require('./exact.cjs');
const COUNTS=['observationsPerVariant','pairsPerVariant','tiltMarginsPerVariant','marginsPerVariant','exactSampleComparisons','savedSignatureAnchors','compareCallsPerVariant','riskCallsPerVariant','expectedExceptionsPerVariant','finishedAuditComparisons','savedBracketSides','savedBracketPairs','savedJsonStates','completeOriginalPreflightAudits','directArtifactByteComparisons'];
const emptyCounts=()=>Object.fromEntries(COUNTS.map(k=>[k,0]));
function clone(x,seen=new Map()){if(x===null||typeof x!=='object')return x;if(seen.has(x))return seen.get(x);if(Buffer.isBuffer(x)){const b=Buffer.from(x);seen.set(x,b);return b;}const y=Array.isArray(x)?[]:Object.create(Object.getPrototypeOf(x));seen.set(x,y);for(const k of Reflect.ownKeys(x)){const d=Object.getOwnPropertyDescriptor(x,k);if('value'in d)d.value=clone(d.value,seen);Object.defineProperty(y,k,d);}if(!Object.isExtensible(x))Object.preventExtensions(y);return y;}
function files(root,prefix=''){if(!fs.existsSync(root))return [];let out=[];for(const e of fs.readdirSync(root,{withFileTypes:true})){const rel=path.join(prefix,e.name),p=path.join(root,e.name);if(e.isDirectory())out.push(...files(p,rel));else out.push(rel);}return out.sort();}
function publicState(a){return {id:a.id,persist:a.persist,samples:a.samples,pairSamples:a.pairSamples,signatureChanges:a.signatureChanges,extrema:a.extrema,brackets:a.brackets,pending:a.pending,written:a.written,path:a.path,previous:a.previous,risks:a.risks,stepRiskChecks:a.stepRiskChecks,endpointRiskChecks:a.endpointRiskChecks,fullTrialRiskChecks:a.fullTrialRiskChecks};}
function stateSummary(a){return {samples:a.samples,pairSamples:a.pairSamples,signatureChanges:a.signatureChanges,extrema:a.extrema,brackets:a.brackets,pending:a.pending,written:a.written,path:a.path,risksLength:a.risks.length,lastRisk:a.risks.at(-1),stepRiskChecks:a.stepRiskChecks,endpointRiskChecks:a.endpointRiskChecks,fullTrialRiskChecks:a.fullTrialRiskChecks,hash:a.hash.copy().digest('hex')};}
function inputOf(s){return s?{states:s.states,location:s.location,raw:s.raw,signatureSha256:s.signatureSha256}:null;}
function riskInput(r){return r?{reason:r.reason,flaggedPairCount:r.flagged?.length,endpointFlaggedPairCount:r.endpointFlaggedPairs?.length,endpointBracketFlag:r.endpointBracketFlag,fullTrialFlag:r.fullTrialFlag,farStart:r.farStart,nearRadius:r.nearRadius,outerSupportAtFarStart:r.outerSupportAtFarStart,samples:r.samples,retention:'Exact raw sample inputs retained; whole flagged-pair arrays omitted from aggregate-only capture; complete minimal mismatch retained separately'}:null;}
function failureClassState(a){return {id:a.id,persist:a.persist,samples:a.samples,pairSamples:a.pairSamples,signatureChanges:a.signatureChanges,extrema:a.extrema,brackets:a.brackets,pending:a.pending,written:a.written,path:a.path,previousInput:inputOf(a.previous),risksLength:a.risks.length,lastRisk:a.risks.at(-1),accumulatedRiskHistory:'Not duplicated in the bounded class-state capture',stepRiskChecks:a.stepRiskChecks,endpointRiskChecks:a.endpointRiskChecks,fullTrialRiskChecks:a.fullTrialRiskChecks,hashStatus:E.capture(()=>a.hash.copy().digest('hex'))};}
function createContext(jobId,tick){
 const counts=emptyCounts(),cases=[],artifacts=[],outputDigests=[];let active=null,current=null,currentAudits=null,finishOutcomes=null,aggregateFailureResolver=null,durable=null,serial=0;
 const add=(key,n=1)=>{counts[key]+=n;if(active)active.counts[key]+=n;};
 const ctx={counts,cases,artifacts,outputDigests,tick,exact:E.exact,clone,failureSampleInput:inputOf,failureRiskInput:riskInput,current:()=>current,lastDurableCheckpoint:()=>durable,assert:(c,m)=>{if(!c)throw Object.assign(Error(m),{integrityBlocked:true});},add,
  case(id,scenario,fn,sourceSelectors={},assertions=[]){tick();const c={id,scenario,status:'running',counts:emptyCounts(),assertions,sourceSelectors};cases.push(c);active=c;current={caseId:id,sourceSelectors};currentAudits=null;finishOutcomes=null;aggregateFailureResolver=null;try{fn();c.status='passed';durable={caseId:id,completedCases:cases.filter(x=>x.status==='passed').map(x=>x.id),exactStoppedState:false,meaning:'Last completed case; not exact interrupted input'};}finally{active=null;}return c;},
  setCurrent(x,audits=null){current={caseId:active?.id,sourceSelectors:active?.sourceSelectors,...(current?.sourceSelector===undefined?{}:{sourceSelector:current.sourceSelector}),...x};currentAudits=audits;finishOutcomes=null;aggregateFailureResolver=null;},
  setAggregateFailureResolver(resolver){aggregateFailureResolver=resolver;},
  failureState(error){
   if(!current)return null;
   const saved={...current,pairedClassState:currentAudits?{B:failureClassState(currentAudits.B),C1:failureClassState(currentAudits.C1)}:null};
   if(current.operation==='finish'&&finishOutcomes){
    saved.aggregateRetention={wholeHistories:'Available in memory but not serialized by design',counterexample:error.detail||null,rule:'Retain the complete paired first differing value/component or exact alias relationship; evidence overflow is terminal, never truncation'};
    const witnessPaths=[error.detail?.path,error.detail?.baseline?.firstSeenPath,error.detail?.candidate?.firstSeenPath],indices=new Set();
    for(const witnessPath of witnessPaths){const m=typeof witnessPath==='string'&&witnessPath.match(/^finish\.value\.risks\.(\d+)(?:\.|$)/);if(m)indices.add(Number(m[1]));}
    if(error.detail?.path==='finish.value.risks'&&finishOutcomes.B?.ok&&finishOutcomes.C1?.ok)indices.add(Math.min(finishOutcomes.B.value.risks.length,finishOutcomes.C1.value.risks.length));
    saved.pairedRelevantRiskInputs=[...indices].map(index=>({index,B:finishOutcomes.B?.ok?riskInput(finishOutcomes.B.value.risks[index]):undefined,C1:finishOutcomes.C1?.ok?riskInput(finishOutcomes.C1.value.risks[index]):undefined}));
   }
   if(aggregateFailureResolver)saved.aggregateWitness=aggregateFailureResolver(error);
   return saved;
  },
  pair({id=`${jobId}-${serial++}`,persist=false,prepare=null}={}){
   const roots=Object.fromEntries(['B','C1'].map(v=>[v,path.join(STUDY,'implementation/results/outputs',jobId,String(serial++),v)]));
   const loaded=Object.fromEntries(['B','C1'].map(v=>[v,loadAudit(v,roots[v],{prepare})]));ctx.M=loaded.B.M;
   const audits={B:new loaded.B.audit.BranchAudit(id,{persist}),C1:new loaded.C1.audit.BranchAudit(id,{persist})};
   const p={audits,modules:{B:loaded.B.audit,C1:loaded.C1.audit},roots,id,previous:null,
    observe(states,location,options={}){
     tick();const inputB=clone({states,location,options}),inputC=clone({states,location,options});
     const unchangedB=E.immutableSnapshot(inputB),unchangedC=E.immutableSnapshot(inputC);
     ctx.setCurrent({operation:'observe',input:clone({states,location,options}),callOrder:['B','C1'],pairedOutput:{}},audits);
     const B=E.capture(()=>audits.B.observe(inputB.states,inputB.location,inputB.options));current.pairedOutput.B=B;const C1=E.capture(()=>audits.C1.observe(inputC.states,inputC.location,inputC.options));current.pairedOutput.C1=C1;unchangedB();unchangedC();
     if(B.ok!==C1.ok)E.mismatch('observe.outcome',B,C1,'exception vs success');
     if(!B.ok){E.exact(B.error,C1.error,'observe.error');E.exact(publicState(audits.B),publicState(audits.C1),'observe.failedClassState');E.exact(audits.B.hash.copy().digest('hex'),audits.C1.hash.copy().digest('hex'),'observe.failedHashState');add('expectedExceptionsPerVariant');return {errorB:B.error,errorC:C1.error};}
     E.exactSample(B.value,C1.value);E.exact(stateSummary(audits.B),stateSummary(audits.C1),'observe.classState');
     for(const [v,inp]of [['B',inputB],['C1',inputC]]){const s=v==='B'?B.value:C1.value;ctx.assert(s.states===inp.states&&s.location===inp.location&&s.raw===(inp.options.raw||inp.states),'Public input alias contract');}
     if(!E.rawBytes(inputB.states).equals(E.rawBytes(inputC.states)))E.mismatch('input.rawBytes',null,null,'Float64 bytes');
     add('observationsPerVariant');add('pairsPerVariant',B.value.pairs.length);add('tiltMarginsPerVariant',states.length);add('marginsPerVariant',B.value.pairs.length*8+states.length);add('exactSampleComparisons');
     if(options.comparePrevious!==false&&p.previous)add('compareCallsPerVariant');
     const s={B:B.value,C1:C1.value};p.previous=s;return s;
    },
    compare(a,b){tick();ctx.setCurrent({operation:'compare',input:{a:{B:inputOf(a.B),C1:inputOf(a.C1)},b:{B:inputOf(b.B),C1:inputOf(b.C1)}},callOrder:['B','C1'],pairedOutput:{}},audits);const B=E.capture(()=>audits.B.compare(a.B,b.B));current.pairedOutput.B=B;const C1=E.capture(()=>audits.C1.compare(a.C1,b.C1));current.pairedOutput.C1=C1;E.exact(B,C1,'compare.result');E.exact(stateSummary(audits.B),stateSummary(audits.C1),'compare.classState');add('compareCallsPerVariant');return {B,C1};},
    checkStep(samples){tick();ctx.setCurrent({operation:'checkStep',input:samples.map(s=>({B:inputOf(s.B),C1:inputOf(s.C1)})),callOrder:['B','C1'],pairedOutput:{}},audits);const B=E.capture(()=>audits.B.checkStep(samples.map(s=>s.B)));current.pairedOutput.B=B;const C1=E.capture(()=>audits.C1.checkStep(samples.map(s=>s.C1)));current.pairedOutput.C1=C1;E.exact(B,C1,'checkStep.result');E.exact(stateSummary(audits.B),stateSummary(audits.C1),'checkStep.classState');add('riskCallsPerVariant');if(!B.ok)add('expectedExceptionsPerVariant');return {B,C1};},
    finish(){tick();ctx.setCurrent({operation:'finish',input:{id,persist,outputRoots:roots,previous:{B:inputOf(audits.B.previous),C1:inputOf(audits.C1.previous)}},callOrder:['B','C1'],pairedOutput:{}},audits);finishOutcomes={};const B=E.capture(()=>audits.B.finish());finishOutcomes.B=B;current.pairedOutput.B=B.ok?{ok:true,wholeAggregate:'Available in memory but not serialized by design; paired minimal counterexample retained on failure'}:B;const C1=E.capture(()=>audits.C1.finish());finishOutcomes.C1=C1;current.pairedOutput.C1=C1.ok?{ok:true,wholeAggregate:'Available in memory but not serialized by design; paired minimal counterexample retained on failure'}:C1;E.exact(B,C1,'finish');if(!B.ok){E.exact(publicState(audits.B),publicState(audits.C1),'finish.failedClassState');E.exact(E.capture(()=>audits.B.hash.copy().digest('hex')),E.capture(()=>audits.C1.hash.copy().digest('hex')),'finish.failedHashStatus');add('expectedExceptionsPerVariant');return {errorB:B.error,errorC:C1.error};}add('finishedAuditComparisons');outputDigests.push({id,digest:E.digest(B.value)});
     const bf=files(roots.B),cf=files(roots.C1);E.exact(bf,cf,'artifact.paths');for(const rel of bf){const bb=fs.readFileSync(path.join(roots.B,rel)),cb=fs.readFileSync(path.join(roots.C1,rel));if(!bb.equals(cb)){let offset=0;while(offset<bb.length&&offset<cb.length&&bb[offset]===cb[offset])offset++;E.mismatch('artifact.'+rel,{path:path.relative(STUDY,path.join(roots.B,rel)),bytes:bb.length,sha256:sha(bb),firstDifferingOffset:offset,bytePresent:offset<bb.length,byte:bb[offset]},{path:path.relative(STUDY,path.join(roots.C1,rel)),bytes:cb.length,sha256:sha(cb),firstDifferingOffset:offset,bytePresent:offset<cb.length,byte:cb[offset]},'direct bytes; complete files retained at paired paths');}artifacts.push({logicalPath:rel,baselinePath:path.relative(STUDY,path.join(roots.B,rel)),candidatePath:path.relative(STUDY,path.join(roots.C1,rel)),bytes:bb.length,directBytesEqual:true,sha256:sha(bb)});add('directArtifactByteComparisons');}return {B:B.value,C1:C1.value};},
    flush(){tick();ctx.setCurrent({operation:'flush',input:{B:{pending:audits.B.pending,written:audits.B.written,path:audits.B.path},C1:{pending:audits.C1.pending,written:audits.C1.written,path:audits.C1.path}},callOrder:['B','C1'],pairedOutput:{}},audits);const B=E.capture(()=>audits.B.flush());current.pairedOutput.B=B;const C1=E.capture(()=>audits.C1.flush());current.pairedOutput.C1=C1;E.exact(B,C1,'flush');E.exact(stateSummary(audits.B),stateSummary(audits.C1),'flush.classState');return {B,C1};}
   };return p;
  }
 };
 // Importing constants is permitted only because this context is constructed after release validation.
 ctx.M=require(path.resolve(STUDY,'../research-next/implementation/src/exact-aero.cjs'));
 return ctx;
}
module.exports={createContext,emptyCounts,COUNTS,clone,files,publicState};
