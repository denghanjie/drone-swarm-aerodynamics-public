'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{performance}=require('perf_hooks');
const base=path.resolve(__dirname,'..'),root=path.resolve(base,'../..'),raw=path.join(base,'raw'),C=require('../config.json');
const A=require(path.join(root,'outputs/milestone-28-source/aero.cjs')),F=require(path.join(root,'outputs/step02c-source/physics.cjs')),O=require('./independent.cjs'),B=require('./bound.cjs').createBound(O,{heldThrust:A.effectiveThrust,heldThrustLabel:'M28 production effectiveThrust'});
const start=performance.now(),weight=F.P.m*F.P.g,D=A.P.motorDistance,budgets=[C.forceBudgetMgFraction*weight,C.momentBudgetMgDFraction*weight*D,C.momentBudgetMgDFraction*weight*D],Vmax=Math.PI*Math.hypot(.34,.08),Amax=Math.PI**2*Math.hypot(.34,.08);
let fieldCalls=0,oracleCalls=0,boundCalls=0,rawBytes=0,lastCompleteTick=null,failureContext=null,currentScienceInputs=null;fs.mkdirSync(raw,{recursive:true});fs.writeFileSync(path.join(raw,'started.json'),JSON.stringify({sourceCommit:process.env.RESEARCH_SOURCE_COMMIT||null,config:C,runtime:process.version})+'\n',{flag:'wx'});rawBytes=fs.statSync(path.join(raw,'started.json')).size;
function guard(){if(performance.now()-start>118000)throw Error('cooperative wall cap');}
function field(s,oracle=false){guard();if(fieldCalls>=C.fieldCallCap)throw Error('field call cap');fieldCalls++;if(oracle)oracleCalls++;return (oracle?O:A).fields(s,'sum-rotor').winds;}
function bound(s,delta,w){guard();if(boundCalls>=C.boundCallCap)throw Error('bound call cap');boundCalls++;return B.bound({states:s,delta,heldWinds:w});}
function save(name,value){const b=Buffer.from(JSON.stringify(value)+'\n');if(rawBytes+b.length>C.rawByteCap)throw Error('raw byte cap');fs.writeFileSync(path.join(raw,name),b,{flag:'wx'});rawBytes+=b.length;}
const hover=(p,v=[0,0,0])=>[...p,...v,0,0,0,1,0,0,0,...Array(4).fill(weight/4)];
function poses(tick){const t=tick*C.tickSeconds,z=Math.PI*t,s=Math.sin(z),c=Math.cos(z);return [hover([.34*c,.04*s,1.15+.08*c],[-.34*Math.PI*s,.04*Math.PI*c,-.08*Math.PI*s]),hover(C.sourcePosition)];}
function loads(s,w){const v=F.wrench(w.map((u,k)=>A.effectiveThrust(s[13+k],u)));return [v.T,v.t[0],v.t[1]];}
function cache(id){return {id,last:-1,next:0,wind:null,prior:null,priorTick:null,decision:null,refreshes:0,attempts:0};}
function predicted(c,tick){if(c.id!=='predict-5ms'||c.prior===null)return c.wind;const a=(tick-c.last)/(c.last-c.priorTick);return c.wind.map((u,k)=>Math.max(0,u+(u-c.prior[k])*a));}
function advance(c,tick,s,reference=null,recordDecisions=null){let left=null;
 if(c.id==='instant'){const w=reference||field(s)[0];return {id:c.id,winds:w,loads:loads(s[0],w),left:null,bound:null,refresh:true};}
 if(tick===c.next){if(c.wind){const w=predicted(c,tick);left={winds:w,loads:loads(s[0],w),bound:c.decision?{anchor:c.decision.tick,intervals:c.decision.bound.intervals.loadDifferences}:null};}
  c.prior=c.wind;c.priorTick=c.last;c.wind=field(s)[0];c.last=tick;c.refreshes++;
  if(c.id==='envelope'){
   c.decision=null;c.next=Infinity;
   if(tick<C.finalTick){let accepted=null;const attempts=[];for(const hTick of C.horizonTicks){if(tick+hTick>C.finalTick)continue;const h=hTick*C.tickSeconds,delta=Math.min(Vmax*h,Math.hypot(...s[0].slice(3,6))*h+.5*Amax*h*h),b=bound(s,delta,c.wind);c.attempts++;attempts.push({hTick,delta,domainAccepted:b.accepted,maxAbsError:b.maxAbsError,rejection:b.rejection});if(b.accepted&&b.maxAbsError.every((e,k)=>e<=budgets[k])){accepted={tick,hTick,delta,bound:b,attempts};break;}}
    if(!accepted){if(recordDecisions)recordDecisions.push({tick,failed:true,attempts});violation('Envelope shortest admissible horizon failed',{kind:'horizon-failure',tick,states:s,heldWinds:c.wind,attempts,budgets});}
    c.decision=accepted;c.next=tick+accepted.hTick;if(recordDecisions)recordDecisions.push(accepted);
   }
  }else{const period={'hold-10ms':40,'hold-5ms':20,'hold-2.5ms':10,'predict-5ms':20}[c.id];assert(period);c.next=tick+period;}
 }
 assert(c.wind);const w=predicted(c,tick);return {id:c.id,winds:w,loads:loads(s[0],w),left,bound:c.decision?{anchor:c.decision.tick,intervals:c.decision.bound.intervals.loadDifferences}:null,refresh:c.last===tick};
}
function violation(message,detail){failureContext=detail;throw Error(message);}
function near(a,b,tol=1e-12,detail={}){if(!(Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=tol))violation('arithmetic mismatch',{kind:'oracle-comparison',...detail,production:a,independent:b,difference:a-b,tolerance:tol});}
const checks=[],rows=[],decisions=[];let referenceMaximumDifference=[0,0,0],coverage={samples:0,maxExcess:-Infinity,worst:null,targetViolations:0};
let stream;
try{
 // State-space fixtures do not read the challenge path.
 const pair=[hover([.08,.02,1]),hover([0,0,1.7])],winds=field(pair)[0],zero=bound(pair,0,winds);assert(zero.accepted&&zero.maxAbsError.every(x=>x<1e-10));checks.push('zero-displacement envelope contains held value');
 const moved=pair.map(s=>s.slice());moved[0][7]=Math.sin(.01);moved[0][9]=Math.cos(.01);assert.equal(bound(moved,0,winds).accepted,false);checks.push('nonidentity attitude rejected');
 assert.equal(bound(pair,.6,winds).accepted,false);checks.push('potential near-field interval rejected before support shortcuts');
 const altered=pair.map(s=>s.slice());altered[0][13]*=.9;assert.equal(bound(altered,0,winds).accepted,false);checks.push('changing nominal thrust rejected');
 const caches=C.variants.map(cache);stream=fs.openSync(path.join(raw,'samples.ndjson'),'wx');
 for(let tick=0;tick<=C.finalTick;tick++){
  const s=poses(tick),w=field(s),independent=field(s,true),ref=loads(s[0],w[0]),other=O.receiverWrench(s[0].slice(13),independent[0]);
  currentScienceInputs={tick,states:s,referenceWinds:w,independentWinds:independent,referenceLoads:ref,independentLoads:other};
  for(let i=0;i<2;i++)for(let k=0;k<4;k++)near(w[i][k],independent[i][k],C.arithmeticAgreementTolerance,{tick,vehicle:i,rotor:k,observable:'inflow'});
  const oi=[other.T,other.t[0],other.t[1]];for(let k=0;k<3;k++){referenceMaximumDifference[k]=Math.max(referenceMaximumDifference[k],Math.abs(ref[k]-oi[k]));near(ref[k],oi[k],C.arithmeticAgreementTolerance,{tick,vehicle:0,observable:['thrust','roll','pitch'][k]});}
  const values=caches.map(c=>advance(c,tick,s,w[0],c.id==='envelope'?decisions:null));
  const e=values.at(-1);for(const v of [e,...(e.left?[e.left]:[])]){for(let k=0;k<3;k++){const error=ref[k]-v.loads[k];if(Math.abs(error)>budgets[k]+C.containmentCheckTolerance)coverage.targetViolations++;if(v.bound){const [lo,hi]=v.bound.intervals[k],excess=Math.max(lo-error,error-hi);coverage.samples++;if(excess>coverage.maxExcess){coverage.maxExcess=excess;coverage.worst={tick,k,side:v===e?'sample':'left',error,interval:[lo,hi],anchor:v.bound.anchor};}if(excess>C.containmentCheckTolerance)violation('envelope containment violated',{kind:'containment',tick,observable:k,side:v===e?'sample':'left',referenceLoads:ref,treatment:v,error,interval:[lo,hi],excess,tolerance:C.containmentCheckTolerance});}}}
  if(coverage.targetViolations)violation('envelope numerical target violated',{kind:'target',tick,referenceLoads:ref,treatment:e,budgets,targetViolations:coverage.targetViolations});
  const row={tick,position:s[0].slice(0,3),velocity:s[0].slice(3,6),values};rows.push(row);const line=Buffer.from(JSON.stringify(row)+'\n');if(rawBytes+line.length>C.rawByteCap)throw Error('raw byte cap');fs.writeSync(stream,line);rawBytes+=line.length;lastCompleteTick=tick;
 }
 fs.closeSync(stream);stream=null;save('envelope-decisions.json',decisions);save('verification.json',{checks,referenceMaximumDifference,coverage,fieldCalls,boundCalls,oracleCalls});
 const metrics=C.variants.map((id,vi)=>{function grid(stride){return [0,1,2].map(k=>{let peak=0,worstTick=0,worstSide='sample',integral=0;for(let tick=0;tick<=C.finalTick;tick+=stride){const row=rows[tick],v=row.values[vi],ref=row.values[0].loads[k],error=v.loads[k]-ref;for(const [side,x] of [['sample',error],...(v.left?[['left',v.left.loads[k]-ref]]:[])])if(Math.abs(x)>peak){peak=Math.abs(x);worstTick=tick;worstSide=side;}
    if(tick){const prior=rows[tick-stride],startError=prior.values[vi].loads[k]-prior.values[0].loads[k],endError=(v.left?v.left.loads[k]:v.loads[k])-ref;integral+=(startError*startError+endError*endError)*.5*stride*C.tickSeconds;}}
   return {observable:['thrust','roll','pitch'][k],unit:k?'N m':'N',peak,rms:Math.sqrt(integral/(C.finalTick*C.tickSeconds)),worstTick,worstSide,budget:budgets[k],peakWithinBudget:peak<=budgets[k]+C.containmentCheckTolerance};});}
  const primary=grid(2),refined=grid(1),sampling=primary.map((p,k)=>{const q=refined[k],floor=k?C.momentSamplingFloor:C.forceSamplingFloor;return {observable:p.observable,peakStable:Math.abs(p.peak-q.peak)<=Math.max(.05*q.peak,floor),rmsStable:Math.abs(p.rms-q.rms)<=Math.max(.05*q.rms,floor),peakDifference:Math.abs(p.peak-q.peak),rmsDifference:Math.abs(p.rms-q.rms)};});return {id,primary,refined,sampling};});
 const expected=new Map();for(let vi=0;vi<C.variants.length;vi++){let sum=0;for(let t=0;t<=C.finalTick;t+=2){const a=rows[t].values[vi].loads;sum+=a[0]+a[1]+a[2];}expected.set(C.variants[vi],sum);}
 save('accuracy.json',{metrics,coverage,referenceMaximumDifference,expectedPrimaryChecksums:Object.fromEntries(expected),budgets,Vmax,Amax});
 const timings=[];
 for(let pass=0;pass<6;pass++)for(let j=0;j<C.variants.length;j++){
  const id=C.variants[(pass+j)%C.variants.length],c=cache(id),f0=fieldCalls,b0=boundCalls,ts=performance.now();let checksum=0;
  for(let tick=0;tick<=C.finalTick;tick+=2){const v=advance(c,tick,poses(tick));checksum+=v.loads[0]+v.loads[1]+v.loads[2];}
  const totalMs=performance.now()-ts;assert.equal(checksum,expected.get(id),'timing checksum differs from retained primary samples');const t={id,pass,warmup:pass===0,totalMs,fieldCalls:fieldCalls-f0,boundCalls:boundCalls-b0,checksum};timings.push(t);save(`timing-${pass}-${j}.json`,t);
 }
 const timingSummary=C.variants.map(id=>{const a=timings.filter(t=>t.id===id&&!t.warmup),v=a.map(t=>t.totalMs).sort((a,b)=>a-b);assert.equal(a.length,5);assert(a.every(t=>t.fieldCalls===a[0].fieldCalls&&t.boundCalls===a[0].boundCalls));return {id,totalMs:{minimum:v[0],median:v[2],maximum:v[4]},fieldCalls:a[0].fieldCalls,boundCalls:a[0].boundCalls};});
 const result={status:'complete restricted envelope challenge',sourceCommit:process.env.RESEARCH_SOURCE_COMMIT||null,config:C,budgets,Vmax,Amax,checks,referenceMaximumDifference,coverage,metrics,timingSummary,fieldCalls,oracleCalls,boundCalls,refreshCount:decisions.length+1,elapsedSeconds:(performance.now()-start)/1000,physicalValidation:false,formalFloatingPointCertificate:false,noveltyEstablished:false,scope:'Single prescribed pair encounter; full overhead counted in CPU query timings; no flight integration, local Boids, rendering or GPU.'};save('result.json',result);fs.writeFileSync(path.join(base,'results/result.json'),JSON.stringify(result,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify({status:result.status,fieldCalls,boundCalls,coverage,timingSummary}));
}catch(e){if(stream!==undefined&&stream!==null)fs.closeSync(stream);const f={status:'failed or incomplete',name:e.name,message:e.message,failureContext,currentScienceInputs,coverage,lastCompleteTick,fieldCalls,boundCalls,oracleCalls,elapsedSeconds:(performance.now()-start)/1000};try{save('failure.json',f);save('partial-decisions.json',decisions);}catch(_){}console.error(JSON.stringify(f));process.exitCode=1;}
