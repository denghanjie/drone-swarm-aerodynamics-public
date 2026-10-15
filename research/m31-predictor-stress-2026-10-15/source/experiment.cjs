'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{performance}=require('perf_hooks');
const base=path.resolve(__dirname,'..'),root=path.resolve(base,'../..'),raw=path.join(base,'raw'),C=require('../config.json'),cases=require('./cases.cjs');
const A=require(path.join(root,'outputs/milestone-28-source/aero.cjs')),F=require(path.join(root,'outputs/step02c-source/physics.cjs')),O=require('./independent.cjs');
const start=performance.now(),weight=F.P.m*F.P.g,budgets=[C.forceBudgetMgFraction*weight,...Array(2).fill(C.momentBudgetMgDFraction*weight*A.P.motorDistance)];
let fieldCalls=0,oracleCalls=0,rawBytes=0,stream=null,lastComplete=null,current=null,failureContext=null;
fs.mkdirSync(raw,{recursive:true});const marker=Buffer.from(JSON.stringify({sourceCommit:process.env.RESEARCH_SOURCE_COMMIT||null,config:C,runtime:process.version})+'\n');fs.writeFileSync(path.join(raw,'started.json'),marker,{flag:'wx'});rawBytes+=marker.length;
function guard(){if(performance.now()-start>C.wallCapSeconds*1000-2000)throw Error('cooperative wall cap');}
function field(s,oracle=false){guard();if(fieldCalls>=C.fieldCallCap)throw Error('field call cap');fieldCalls++;if(oracle)oracleCalls++;return (oracle?O:A).fields(s,'sum-rotor');}
function write(name,data,failure=false){const buf=Buffer.from(JSON.stringify(data)+'\n');if(rawBytes+buf.length>C.rawByteCap-(failure?0:C.failureReserveBytes))throw Error('raw byte cap');fs.writeFileSync(path.join(raw,name),buf,{flag:'wx'});rawBytes+=buf.length;}
function loads(s,w){const v=F.wrench(w.map((u,k)=>A.effectiveThrust(s[13+k],u)));return [v.T,v.t[0],v.t[1]];}
function fail(message,context){failureContext=context;throw Error(message);}
function near(a,b,detail){if(!Number.isFinite(a)||!Number.isFinite(b)||Math.abs(a-b)>C.arithmeticAgreementTolerance)fail('independent arithmetic mismatch',{...detail,production:a,independent:b,difference:a-b,tolerance:C.arithmeticAgreementTolerance});}
function cache(id){return {id,last:-1,priorTick:null,wind:null,prior:null};}
function estimate(c,tick){if(c.id!=='predict-5ms'||c.prior===null)return c.wind;const ratio=(tick-c.last)/(c.last-c.priorTick);return c.wind.map((u,k)=>Math.max(0,u+(u-c.prior[k])*ratio));}
function advance(c,tick,s,ref){if(c.id==='instant'){const w=ref||field(s).winds[0];return {id:c.id,winds:w,loads:loads(s[0],w),left:null,refresh:true};}
 const period=C.periodTicks[c.id];let left=null;
 if(tick%period===0){if(c.wind){const w=estimate(c,tick);left={winds:w,loads:loads(s[0],w)};}c.prior=c.wind;c.priorTick=c.last;c.wind=field(s).winds[0];c.last=tick;}
 const w=estimate(c,tick);return {id:c.id,winds:w,loads:loads(s[0],w),left,refresh:c.last===tick};}
function metrics(rows){return C.variants.map((id,vi)=>{function grid(stride){return [0,1,2].map(k=>{let peak=0,worstTick=0,worstSide='sample',integral=0,overTarget=0;
 for(let tick=0;tick<=C.finalTick;tick+=stride){const row=rows[tick],v=row.values[vi],reference=row.values[0].loads[k],error=v.loads[k]-reference;
 for(const [side,e] of [['sample',error],...(v.left?[['left',v.left.loads[k]-reference]]:[])]){if(Math.abs(e)>peak){peak=Math.abs(e);worstTick=tick;worstSide=side;}if(Math.abs(e)>budgets[k]+C.arithmeticAgreementTolerance)overTarget++;}
 if(tick){const p=rows[tick-stride],e0=p.values[vi].loads[k]-p.values[0].loads[k],e1=(v.left||v).loads[k]-reference;integral+=(e0*e0+e1*e1)*.5*stride*C.tickSeconds;}}
 return {observable:['thrust','roll','pitch'][k],peak,rms:Math.sqrt(integral/(C.finalTick*C.tickSeconds)),worstTick,worstSide,budget:budgets[k],peakWithinBudget:peak<=budgets[k]+C.arithmeticAgreementTolerance,queryExceedances:overTarget};});}
 const primary=grid(C.primaryStride),refined=grid(C.fineStride),sampling=primary.map((p,k)=>{const q=refined[k],floor=k?C.momentSamplingFloor:C.forceSamplingFloor;return {observable:p.observable,peakStable:Math.abs(p.peak-q.peak)<=Math.max(C.samplingRelativeTolerance*q.peak,floor),rmsStable:Math.abs(p.rms-q.rms)<=Math.max(C.samplingRelativeTolerance*q.rms,floor),peakDifference:Math.abs(p.peak-q.peak),rmsDifference:Math.abs(p.rms-q.rms)};});return {id,primary,refined,sampling};});}
function windowMetrics(cid,rows){return (cases.reportingWindows[cid]||[]).map(window=>({...window,methods:C.variants.map((id,vi)=>{const signedLoadMin=[Infinity,Infinity,Infinity],signedLoadMax=[-Infinity,-Infinity,-Infinity];let signedWindMin=Infinity,signedWindMax=-Infinity;
 for(let tick=window.startTick;tick<=window.endTick;tick++){const row=rows[tick],v=row.values[vi],ref=row.values[0];for(const side of [v,...(v.left?[v.left]:[])]){for(let k=0;k<3;k++){const e=side.loads[k]-ref.loads[k];signedLoadMin[k]=Math.min(signedLoadMin[k],e);signedLoadMax[k]=Math.max(signedLoadMax[k],e);}for(let k=0;k<4;k++){const e=side.winds[k]-ref.winds[k];signedWindMin=Math.min(signedWindMin,e);signedWindMax=Math.max(signedWindMax,e);}}}
 return {id,signedLoadMin,signedLoadMax,signedWindMin,signedWindMax};})}));}
const summaries=[],timings=[];
try{
 assert.deepEqual(cases.ids,C.cases);assert.equal(C.warmupPasses,1);assert.equal(C.recordedTimingPasses,5);assert.equal(C.primaryStride,2);assert.equal(C.fineStride,1);
 for(const cid of C.cases){
  const rows=[],caches=C.variants.map(cache),oracleMax={wind:0,loads:[0,0,0]},refRange=[Infinity,-Infinity],expected={};let maxSources=0;const f0=fieldCalls,o0=oracleCalls;
  stream=fs.openSync(path.join(raw,cid+'.ndjson'),'wx');
  for(let tick=0;tick<=C.finalTick;tick++){
   current={phase:'science',case:cid,tick};const s=cases.poses(cid,tick*C.tickSeconds);current.states=s;const a=field(s),o=field(s,true);current.production=a;current.independent=o;
   for(let i=0;i<s.length;i++)for(let k=0;k<4;k++){const d=Math.abs(a.winds[i][k]-o.winds[i][k]);oracleMax.wind=Math.max(oracleMax.wind,d);near(a.winds[i][k],o.winds[i][k],{case:cid,tick,vehicle:i,rotor:k,observable:'wind'});}
   const r=loads(s[0],a.winds[0]),ow=O.receiverWrench(s[0].slice(13),o.winds[0]),ol=[ow.T,ow.t[0],ow.t[1]];current.productionLoads=r;current.independentLoads=ol;
   for(let k=0;k<3;k++){oracleMax.loads[k]=Math.max(oracleMax.loads[k],Math.abs(r[k]-ol[k]));near(r[k],ol[k],{case:cid,tick,observable:['thrust','roll','pitch'][k]});}
   const values=caches.map(c=>advance(c,tick,s,a.winds[0])),row={tick,states:s,referenceAllWinds:a.winds,independentAllWinds:o.winds,independentReceiverLoads:ol,fieldDiagnostics:{contributions:a.contributions,candidates:a.candidates},values};
   refRange[0]=Math.min(refRange[0],...a.winds[0]);refRange[1]=Math.max(refRange[1],...a.winds[0]);maxSources=Math.max(maxSources,s.length-1);
   const buf=Buffer.from(JSON.stringify(row)+'\n');if(rawBytes+buf.length>C.rawByteCap-C.failureReserveBytes)throw Error('raw byte cap');fs.writeSync(stream,buf);rawBytes+=buf.length;rows.push(row);lastComplete={case:cid,tick};
  }
  fs.closeSync(stream);stream=null;
  for(let vi=0;vi<C.variants.length;vi++){let sum=0;for(let tick=0;tick<=C.finalTick;tick+=C.primaryStride){const x=rows[tick].values[vi].loads;sum+=x[0]+x[1]+x[2];}expected[C.variants[vi]]=sum;}
  const out={id:cid,description:cases.descriptions[cid],vehicleCount:maxSources+1,metrics:metrics(rows),reportingWindows:windowMetrics(cid,rows),oracleMaximumDifference:oracleMax,receiverInflowRange:refRange,scienceFieldCalls:fieldCalls-f0,oracleCalls:oracleCalls-o0,expectedPrimaryChecksums:expected};
  write(cid+'-accuracy.json',out);summaries.push(out);
 }
 // Rotate both case and method order; no saved-data access inside timed query loop.
 for(let pass=0;pass<C.warmupPasses+C.recordedTimingPasses;pass++)for(let ci=0;ci<C.cases.length;ci++)for(let j=0;j<C.variants.length;j++){
  const cid=C.cases[(ci+pass)%C.cases.length],id=C.variants[(j+pass)%C.variants.length],c=cache(id),before=fieldCalls,ts=performance.now();let checksum=0;
  for(let tick=0;tick<=C.finalTick;tick+=C.primaryStride){current={phase:'timing',case:cid,id,pass,tick};const s=cases.poses(cid,tick*C.tickSeconds);current.states=s;const v=advance(c,tick,s);checksum+=v.loads[0]+v.loads[1]+v.loads[2];}
  const totalMs=performance.now()-ts,expected=summaries.find(x=>x.id===cid).expectedPrimaryChecksums[id];if(checksum!==expected)fail('timed checksum differs',{case:cid,id,pass,checksum,expected});
  const record={case:cid,id,pass,warmup:pass<C.warmupPasses,totalMs,fieldCalls:fieldCalls-before,checksum};timings.push(record);write(`timing-${pass}-${ci}-${j}.json`,record);
 }
 for(const summary of summaries){summary.timingSummary=C.variants.map(id=>{const data=timings.filter(t=>t.case===summary.id&&t.id===id&&!t.warmup),v=data.map(t=>t.totalMs).sort((a,b)=>a-b);assert.equal(data.length,5);assert(data.every(t=>t.fieldCalls===data[0].fieldCalls));return {id,totalMs:{minimum:v[0],median:v[2],maximum:v[4]},fieldCalls:data[0].fieldCalls};});}
 const comparisons=summaries.flatMap(c=>{const h=c.metrics.find(m=>m.id==='hold-5ms'),p=c.metrics.find(m=>m.id==='predict-5ms');return [0,1,2].map(k=>{const floor=k?C.momentSamplingFloor:C.forceSamplingFloor;return {case:c.id,observable:p.refined[k].observable,floor,peakNoWorse:p.refined[k].peak<=h.refined[k].peak+floor,peakStrictlyBetter:p.refined[k].peak<h.refined[k].peak-floor,peakScreensPass:p.sampling[k].peakStable&&h.sampling[k].peakStable,rmsNoWorse:p.refined[k].rms<=h.refined[k].rms+floor,rmsStrictlyBetter:p.refined[k].rms<h.refined[k].rms-floor,rmsScreensPass:p.sampling[k].rmsStable&&h.sampling[k].rmsStable};});});
 const suiteDecision={comparisons,allTestedPeaksImproved:comparisons.every(x=>x.peakNoWorse&&x.peakScreensPass)&&comparisons.some(x=>x.peakStrictlyBetter),allTestedRmsImproved:comparisons.every(x=>x.rmsNoWorse&&x.rmsScreensPass)&&comparisons.some(x=>x.rmsStrictlyBetter),scope:'Finite selected suite only, not universal superiority or physical validation'};
 const result={status:'complete prospective prescribed-input stress challenge',sourceCommit:process.env.RESEARCH_SOURCE_COMMIT||null,config:C,budgets,cases:summaries,suiteDecision,fieldCalls,oracleCalls,elapsedSeconds:(performance.now()-start)/1000,noveltyEstablished:false,physicalValidation:false,scope:'Prescribed 2–4 vehicle inputs; quasi-static field evaluated for every vehicle, loads only for receiver0. No integrated dynamics, Boids, obstacles, GPU or rendering.'};
 write('result.json',result);fs.writeFileSync(path.join(base,'results/result.json'),JSON.stringify(result,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify({status:result.status,fieldCalls,oracleCalls,rawBytes}));
}catch(e){if(stream!==null)fs.closeSync(stream);const failure={status:'failed or incomplete; no retry',name:e.name,message:e.message,detail:e.detail||null,failureContext,current,lastComplete,fieldCalls,oracleCalls,elapsedSeconds:(performance.now()-start)/1000};try{write('failure.json',failure,true);write('partial-summaries.json',summaries,true);}catch(_){}console.error(JSON.stringify(failure));process.exitCode=1;}
