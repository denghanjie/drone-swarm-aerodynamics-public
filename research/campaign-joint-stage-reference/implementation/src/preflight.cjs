'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const {ROOT,load,save,sha,states,readRaw}=require('./io.cjs');
const {BranchAudit}=require('./branch-audit.cjs'),{controller,B}=require('./controller.cjs'),{writeControllers}=require('./controller-record.cjs');
const Q=1/51200;
function readInput(seed){
 const acquisition=load('../inputs/INPUT-ACQUISITION.json'),entry=acquisition.arrays.find(x=>x.seed===seed);if(!entry||!entry.allIdentitiesVerified)throw Error('Missing verified acquisition');
 const wrapper=load('../inputs/'+entry.metadataPath),meta=wrapper.originalSidecar,run=load(`inputs/runs/s${seed}-p1-a4.json`);
 if(JSON.stringify(meta)!==JSON.stringify(run.denseStates)||JSON.stringify(meta.shape)!=='[6401,16,17]'||meta.dt!==1/6400||meta.startTime!==0||meta.endTime!==1||meta.runId!==`s${seed}-p1-a4`||!run.complete||run.config.seed!==seed)throw Error('Historical raw sidecar/run contract mismatch');
 const hash=crypto.createHash('sha256');let compressedBytes=0;
 for(const part of acquisition.parts.filter(p=>p.localPath.includes(`s${seed}-`))){const b=fs.readFileSync(path.resolve(ROOT,'../inputs',part.localPath));if(sha(b)!==part.sha256||b.length!==part.bytes)throw Error('Transport part hash mismatch');hash.update(b);compressedBytes+=b.length;}
 if(hash.digest('hex')!==meta.sha256||compressedBytes!==meta.compressedBytes)throw Error('Original compressed hash mismatch');
 const raw=readRaw(path.resolve(ROOT,'../inputs',entry.localPath),{bytes:meta.uncompressedBytes,sha256:meta.uncompressedSha256,shape:meta.shape});
 const initial=states(raw.row(0));if(JSON.stringify(initial)!==JSON.stringify(run.initial)||JSON.stringify(states(raw.row(6400)))!==JSON.stringify(run.final)||JSON.stringify(initial)!==JSON.stringify(B.initial(seed,16)))throw Error('Historical initial/final/seed mismatch');
 return {raw,meta,run};
}
function preflight(seed,{budgetCheck=()=>{},checkpoint=()=>{}}={}){
 const id=`preflight-s${seed}`,audit=new BranchAudit(id),events=[];let current=null,last=null,stop=null,source=null;
 try {
  source=readInput(seed);const oldEvents=source.run.events.filter(e=>e.type==='controller');
  if(oldEvents.length!==100)throw Error('Historical controller event count mismatch');
  for(let n=0;n<6401;n++){
   budgetCheck();const Y=states(source.raw.row(n));current={runId:id,phase:'saved-path-endpoint',tick:n*8,time:n/6400,state:Y,exactStoppedState:true};
   if(Y.some(s=>!s.every(Number.isFinite)))throw Error('Nonfinite historical endpoint');
   const s=audit.observe(Y,{tick:n*8,time:n/6400,role:'endpoint'});if(last)audit.checkStep([last,s]);last=s;
   if(n<6400&&n%64===0){const c=controller(Y,n*8),prior=oldEvents[n/64];if(prior.tick!==n||prior.commandsSha256!==c.event.commandsSha256)throw Object.assign(Error('Saved-path controller command hash mismatch'),{detail:{tick:n*8,expected:prior,actual:c.event}});events.push(c.event);}
   if(n%128===0)checkpoint({...current,exactStoppedState:false,meaning:'Last durable checkpoint only'});
  }
 }catch(e){stop={...current,runId:id,type:e.constructor.name,message:e.message,detail:e.detail||null,exactStoppedState:!!current};save(`results/failures/${id}.json`,stop);}
 const report={id,seed,passed:!stop,stop,input:source?.meta||null,visitedEndpoints:audit.samples,expectedEndpoints:6401,controllerEvents:events.length,audit:audit.finish(),controllers:writeControllers(id,events),sampleSchedule:'Endpoints n=0..6400, base tick=8n, no interpolation; terminal has no controller event',baseTickSeconds:Q};
 save(`results/preflight/${id}.json`,report);Object.defineProperty(report,'controlEvents',{value:events,enumerable:false});return report;
}
module.exports={readInput,preflight};
