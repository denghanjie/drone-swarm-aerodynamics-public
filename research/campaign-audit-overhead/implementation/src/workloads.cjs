'use strict';
const path=require('path'),v8=require('v8'),crypto=require('crypto');
const {sourceArray}=require('./corpus.cjs'),{loadAudit,STUDY}=require('./load-audit.cjs'),{digest,digestDetails,capture}=require('./exact.cjs');
const EXPECTED={'W-ENDPOINT':{observations:257,pairSamples:246720,comparisons:256,riskCalls:256},'W-STAGE-FIXTURE':{observations:161,pairSamples:154560,comparisons:160,riskCalls:32}};
function prepareWorkload(workload,seed){
 if(!Object.hasOwn(EXPECTED,workload)||![840131,840137].includes(seed))throw Error('Unfrozen workload');
 const {row}=sourceArray(seed===840131?4:8),end=workload==='W-ENDPOINT'?256:32,states=Array.from({length:end+1},(_,i)=>row(i));
 const endpoints=states.map((s,i)=>({states:s,location:{tick:8*i,time:8*i*(1/51200),role:'endpoint'}}));
 const stages=workload==='W-STAGE-FIXTURE'?Array.from({length:32},(_,i)=>[0,0.5,0.5,1].map((fraction,k)=>{const geometry=states[i].map(s=>s.slice()),raw=geometry.map(s=>s.map((v,j)=>j>=6&&j<=9?v*(1+2**-20):v));return {states:geometry,raw,location:{tick:8*i+fraction*8,time:(8*i+fraction*8)*(1/51200),role:'stage',stage:k+1}};})):null;
 return {workload,seed,endpoints,stages};
}
function runWorkload(prepared,driver,tick,onObservation=()=>{}){
 const {workload,endpoints,stages}=prepared,samples=[];const counts={observations:0,pairSamples:0,comparisons:0,riskCalls:0,riskExceptions:0};
 function obs(e,options){onObservation({operation:'observe',completedObservations:counts.observations,index:counts.observations,input:{states:e.states,location:e.location,options},sample:null});tick();const s=driver.observe(e.states,e.location,options);onObservation({operation:'last-completed-observation',completedObservations:counts.observations+1,index:counts.observations,input:{states:e.states,location:e.location,options},sample:s});samples.push(s);counts.observations++;counts.pairSamples+=(s.B||s).pairs.length;return s;}
 function rawInput(s){const x=s.B||s;return {states:x.states,location:x.location,raw:x.raw};}
 function compare(a,b){onObservation({operation:'compare',completedObservations:counts.observations,input:[rawInput(a),rawInput(b)],sample:null});driver.compare(a,b);counts.comparisons++;}
 function risk(samples){onObservation({operation:'checkStep',completedObservations:counts.observations,input:samples.map(rawInput),sample:null});counts.riskCalls++;if(driver.checkStep(samples)===false)counts.riskExceptions++;}
 let previous=obs(endpoints[0],{comparePrevious:workload==='W-ENDPOINT'});
 if(workload==='W-ENDPOINT')for(let i=1;i<endpoints.length;i++){const s=obs(endpoints[i],{comparePrevious:true});counts.comparisons++;risk([previous,s]);previous=s;}
 else for(let i=0;i<32;i++){
  const ss=stages[i].map(e=>obs(e,{comparePrevious:false,raw:e.raw})),accepted=obs(endpoints[i+1],{comparePrevious:false});
  compare(previous,accepted);
  for(let k=1;k<4;k++){compare(ss[k-1],ss[k]);}
  compare(ss[3],accepted);risk([previous,...ss,accepted]);previous=accepted;
 }
 onObservation({operation:'finish',completedObservations:counts.observations,input:null,lastCompletedSample:samples.at(-1),sample:null});return {result:driver.finish(),samples,counts};
}
function components(result,samples){const out=samples.map((value,i)=>({path:'samples['+i+']',value}));for(const [key,value]of Object.entries(result)){if(key==='id')continue;if(key==='risks')value.forEach((v,i)=>out.push({path:'finish.risks['+i+']',value:v}));else if(key==='extrema'||key==='brackets')for(const [k,v]of Object.entries(value))out.push({path:'finish.'+key+'.'+k,value:v});else out.push({path:'finish.'+key,value});}return out;}
function componentDigests(result,samples){return components(result,samples).map(({path,value})=>{return {path,...digestDetails(value)};});}
function aliasEdges(result,samples){const first=new Map(),edges=[];function walk(v,p,component){if(v===null||typeof v!=='object')return;if(first.has(v)){const previous=first.get(v);if(previous.component!==component)edges.push([p,previous.path]);return;}first.set(v,{path:p,component});for(const k of Object.keys(v))walk(v[k],p+'.'+k,component);}for(const item of components(result,samples))walk(item.value,item.path,item.path);return edges;}
function semanticDigest(result,samples){return digest({samples,finish:{...result,id:'<logical-id>'}});}
function driverFactory(variant,jobId){const {audit}=loadAudit(variant,path.join(STUDY,'implementation/results/unused',jobId));return id=>{const a=new audit.BranchAudit(id,{persist:false});return {observe:(s,l,o)=>a.observe(s,l,o),compare:(x,y)=>a.compare(x,y),checkStep:s=>{const r=capture(()=>a.checkStep(s));if(!r.ok&&!r.error.unresolvedJump)throw r.error;return r.ok;},finish:()=>a.finish()};};}
function correctnessWorkload(ctx,workload,seed){const prepared=prepareWorkload(workload,seed);ctx.case(`workload-${workload}-${seed}`,'exact-benchmark-workload-contract',()=>{const p=ctx.pair({id:`contract-${workload}-${seed}`});const driver={observe:(s,l,o)=>{const v=p.observe(s,l,o);ctx.assert(!v.errorB,'Workload geometry domain error');return v;},compare:(a,b)=>p.compare(a,b),checkStep:s=>{const r=p.checkStep(s);if(!r.B.ok)ctx.assert(r.B.error.unresolvedJump===true&&r.B.error.message==='Unresolved finite-jump sampled-range risk','Unexpected workload range error');return r.B.ok;},finish:()=>p.finish()};const {result,samples,counts}=runWorkload(prepared,driver,ctx.tick);ctx.assert(!result.errorB,'Workload finish failed');
 ctx.setCurrent({operation:'completeWorkloadGraph',input:{workload,seed,manifestIndex:seed===840131?4:8,rows:workload==='W-ENDPOINT'?[0,256]:[0,32],sampleCount:samples.length},pairedOutput:{B:{ok:true,wholeAggregate:'Available in memory but not serialized by design; paired minimal counterexample retained on failure'},C1:{ok:true,wholeAggregate:'Available in memory but not serialized by design; paired minimal counterexample retained on failure'}}},p.audits);
 ctx.setAggregateFailureResolver(error=>{
  const paths=[error.detail?.path,error.detail?.baseline?.firstSeenPath,error.detail?.candidate?.firstSeenPath],sampleIndices=new Set(),riskIndices=new Set();
  for(const witnessPath of paths){if(typeof witnessPath!=='string')continue;const sample=witnessPath.match(/^completeWorkloadGraph\.samples\.(\d+)(?:\.|$)/),risk=witnessPath.match(/^completeWorkloadGraph\.finish\.risks\.(\d+)(?:\.|$)/);if(sample)sampleIndices.add(Number(sample[1]));if(risk)riskIndices.add(Number(risk[1]));}
  if(error.detail?.path==='completeWorkloadGraph.finish.risks')riskIndices.add(Math.min(result.B.risks.length,result.C1.risks.length));
  return {wholeHistories:'Available in memory but not serialized by design',counterexample:error.detail||null,pairedSampleInputs:[...sampleIndices].map(index=>({observationIndex:index,sourceRow:workload==='W-ENDPOINT'?index:index===0?0:Math.floor((index-1)/5)+((index-1)%5===4?1:0),B:ctx.failureSampleInput(samples[index]?.B),C1:ctx.failureSampleInput(samples[index]?.C1)})),pairedRiskInputs:[...riskIndices].map(index=>({index,B:ctx.failureRiskInput(result.B.risks[index]),C1:ctx.failureRiskInput(result.C1.risks[index])}))};
 });
 ctx.exact(counts.observations,EXPECTED[workload].observations,'workload.observations');ctx.exact({samples:samples.map(s=>s.B),finish:result.B},{samples:samples.map(s=>s.C1),finish:result.C1},'completeWorkloadGraph');ctx.outputDigests.push({workload,seed,semanticDigest:semanticDigest(result.B,samples.map(s=>s.B)),expectedCounts:EXPECTED[workload],actualCounts:counts,consumesAllPublicSamples:true,componentDigests:componentDigests(result.B,samples.map(s=>s.B)),aliasEdges:aliasEdges(result.B,samples.map(s=>s.B)),normalization:'Only logical id normalized; all public samples, result fields and aliases consumed by deterministic own-key/Float64/descriptor/reference graph encoding'});},{workload,seed,rows:workload==='W-ENDPOINT'?[0,256]:[0,32]},['exact-benchmark-workload','all-public-samples','exact-joint-schedule','finish-inside-workload','full-finish-equality','raw-stage-distinct-references']);}
module.exports={components,componentDigests,aliasEdges,prepareWorkload,runWorkload,semanticDigest,driverFactory,correctnessWorkload,EXPECTED};
