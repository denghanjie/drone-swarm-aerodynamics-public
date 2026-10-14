'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const M=require('./exact-aero.cjs'),{ROOT,sha,reserve,save}=require('./io.cjs');
const categories=['downstreamZero','farStart','downstreamFade','downstreamCutoff','nearRadius','radialFade','radialCutoff','neighborRadius','tilt'];
const outerAtFar=M.P.radialCutoff*M.W.parameters.spread*(M.W.parameters.minDownstream-M.W.parameters.origin)*M.P.motorDistance;
function sample(states,location){
 const {axes,points}=M.prepare(states),n=states.length,pairs=[],signature=Buffer.alloc(n*(n-1)*4*2+n),closest=categories.map(()=>null),minimum=categories.map(()=>null),maximum=categories.map(()=>null),distances=new Array(n*n);let offset=0;
 function margin(k,value,i,r,j){const near=!closest[k]||Math.abs(value)<Math.abs(closest[k].margin),low=!minimum[k]||value<minimum[k].margin,high=!maximum[k]||value>maximum[k].margin;if(near||low||high){const v=k===8?{margin:value,drone:i}:{margin:value,receiver:i,rotor:r,source:j};if(near)closest[k]=v;if(low)minimum[k]=v;if(high)maximum[k]=v;}}
 for(let i=0;i<n;i++)for(let r=0;r<4;r++)for(let j=0;j<n;j++)if(i!==j){
  const a=3*j,p=12*i+3*r,x=states[j][0]-points[p],y=states[j][1]-points[p+1],z=states[j][2]-points[p+2];
  const down=((0+x*axes[a])+y*axes[a+1])+z*axes[a+2],radial=Math.hypot(x-down*axes[a],y-down*axes[a+1],z-down*axes[a+2]);
  const half=M.W.parameters.spread*(down/M.P.motorDistance-M.W.parameters.origin)*M.P.motorDistance;
  const distance=r===0?(distances[i*n+j]=Math.hypot(...[0,1,2].map(k=>states[j][k]-states[i][k]))):distances[i*n+j];
  const margins=[down,down-M.farStart,down-M.P.downstreamFade,down-M.P.downstreamCutoff,radial-M.P.nearFieldRadius,radial-M.P.radialFade*half,radial-M.P.radialCutoff*half,distance-M.P.neighborRadius];
  let bits=0;for(let k=0;k<margins.length;k++){if(k===0?margins[k]>0:margins[k]>=0)bits|=1<<k;margin(k,margins[k],i,r,j);}
  signature.writeUInt16LE(bits,offset);offset+=2;
  const identity={receiver:i,rotor:r,source:j};pairs.push({down,radial,bits,margins,...identity});
  if(distance<M.P.neighborRadius&&down>0&&down<M.farStart&&radial<M.P.nearFieldRadius)throw Object.assign(new M.DomainError('Receiver enters unmodeled near wake', {...identity,downstream:down,radial}),{auditLocation:location});
 }
 for(let i=0;i<n;i++){const m=axes[3*i+2]-Math.cos(M.P.maxTiltDegrees*Math.PI/180);margin(8,m,i);signature[offset++]=m>=0?1:0;}
 return {states,location,pairs,closest,minimum,maximum,signatureSha256:sha(signature)};
}
function jumpRisk(samples){
 const flagged=[];
 for(let k=0;k<samples[0].pairs.length;k++){
  const p=samples.map(s=>s.pairs[k]),lo=Math.min(...p.map(x=>x.down)),hi=Math.max(...p.map(x=>x.down)),rlo=Math.min(...p.map(x=>x.radial)),rhi=Math.max(...p.map(x=>x.radial));
  if(lo<=M.farStart&&hi>=M.farStart&&rlo<outerAtFar&&rhi>=M.P.nearFieldRadius)flagged.push({receiver:p[0].receiver,rotor:p[0].rotor,source:p[0].source,downstreamRange:[lo,hi],radialRange:[rlo,rhi]});
 }
 return flagged;
}
class BranchAudit {
 constructor(id,{persist=true}={}){this.id=id;this.persist=persist;this.samples=0;this.pairSamples=0;this.signatureChanges=0;this.extrema=categories.map(()=>({nearest:null,minimum:null,maximum:null}));this.brackets={};this.hash=crypto.createHash('sha256');this.pending=[];this.written=0;this.path=`results/audit/${id}.signatures.bin`;this.previous=null;this.risks=[];this.stepRiskChecks=0;this.endpointRiskChecks=0;this.fullTrialRiskChecks=0;}
 observe(states,location,{comparePrevious=true,raw=null}={}){
  const s=sample(states,location);s.raw=raw||states;this.samples++;this.pairSamples+=s.pairs.length;
  const b=Buffer.from(s.signatureSha256,'hex');this.hash.update(b);if(this.persist)this.pending.push(b);
  for(let k=0;k<categories.length;k++){const e=this.extrema[k];for(const [key,entry]of [['nearest',s.closest[k]],['minimum',s.minimum[k]],['maximum',s.maximum[k]]]){const value=entry===null?undefined:entry.margin;if(!e[key]||(key==='nearest'?Math.abs(value)<Math.abs(e[key].margin):key==='minimum'?value<e[key].margin:value>e[key].margin))e[key]={...entry,location};}}
  if(comparePrevious&&this.previous)this.compare(this.previous,s);
  this.previous=s;if(this.pending.length>=1024)this.flush();return s;
 }
 compare(a,b){
  if(a.signatureSha256===b.signatureSha256)return;
  this.signatureChanges++;
  const changes=new Map();
  for(let i=0;i<a.pairs.length;i++){const x=a.pairs[i],y=b.pairs[i],xor=x.bits^y.bits;if(!xor)continue;for(let k=0;k<8;k++)if(xor&(1<<k)){const severity=Math.abs(x.margins[k]-y.margins[k]),old=changes.get(k);if(!old||severity>old.severity)changes.set(k,{severity,receiver:x.receiver,rotor:x.rotor,source:x.source,fromMargin:x.margins[k],toMargin:y.margins[k]});}}
  for(const [k,detail]of changes){const bracket={category:categories[k],...detail,from:{location:a.location,state:a.states,raw:a.raw},to:{location:b.location,state:b.states,raw:b.raw},meaning:'Sample bracket only; equal-time RK trial states are not ordered physical observations'};const saved=this.brackets[categories[k]];if(!saved)this.brackets[categories[k]]={first:bracket,worst:bracket,count:1};else{saved.count++;if(detail.severity>saved.worst.severity)saved.worst=bracket;}}
 }
 checkStep(samples){
  this.stepRiskChecks++;if(samples.some(s=>s.location.role==='stage'))this.fullTrialRiskChecks++;if(samples.filter(s=>s.location.role==='endpoint').length>=2)this.endpointRiskChecks++;
  const flagged=jumpRisk(samples);if(flagged.length){const endpointSamples=samples.filter(s=>s.location.role==='endpoint');const evidence={reason:'Unresolved finite-jump sampled-range risk',flagged,endpointFlaggedPairs:endpointSamples.length>=2?jumpRisk(endpointSamples):[],endpointBracketFlag:endpointSamples.length>=2&&jumpRisk(endpointSamples).length>0,fullTrialFlag:samples.some(s=>s.location.role==='stage'),farStart:M.farStart,nearRadius:M.P.nearFieldRadius,outerSupportAtFarStart:outerAtFar,samples:samples.map(s=>({location:s.location,state:s.states,raw:s.raw,signatureSha256:s.signatureSha256})),meaning:'Conservative possible crossing; no event localization or interpolation'};this.risks.push(evidence);throw Object.assign(Error(evidence.reason),{detail:evidence,unresolvedJump:true});}
 }
 flush(){if(!this.pending.length)return;const b=Buffer.concat(this.pending),p=reserve(this.path,this.written+b.length);fs.mkdirSync(path.dirname(p),{recursive:true});const fd=fs.openSync(p,'a');try{fs.writeFileSync(fd,b);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}this.written+=b.length;this.pending=[];}
 finish(){this.flush();let bracketBytes=0;const bracketChunks=[];const brackets={};for(const [category,entry] of Object.entries(this.brackets)){brackets[category]={count:entry.count};for(const key of ['first','worst']){const v=entry[key];const copy={...v};for(const side of ['from','to']){const raw=require('./io.cjs').rawBytes(v[side].state);bracketChunks.push(raw);copy[side]={location:v[side].location,geometryOffsetBytes:bracketBytes,geometryBytes:raw.length,geometrySha256:sha(raw)};bracketBytes+=raw.length;if(v[side].raw!==v[side].state){const actual=require('./io.cjs').rawBytes(v[side].raw);bracketChunks.push(actual);copy[side].rawStageOffsetBytes=bracketBytes;copy[side].rawStageBytes=actual.length;copy[side].rawStageSha256=sha(actual);bracketBytes+=actual.length;}}brackets[category][key]=copy;}}let bracketRaw=null;if(this.persist&&bracketBytes){require('./io.cjs').atomicWrite(`results/audit/${this.id}.brackets.f64`,Buffer.concat(bracketChunks));bracketRaw={path:`results/audit/${this.id}.brackets.f64`,bytes:bracketBytes,sha256:sha(Buffer.concat(bracketChunks)),encoding:'little-endian Float64; whole swarm full17 states; offsets in bracket entries'};}const result={id:this.id,samples:this.samples,pairSamples:this.pairSamples,signatureChanges:this.signatureChanges,stepRiskChecks:this.stepRiskChecks,endpointRiskChecks:this.endpointRiskChecks,fullTrialRiskChecks:this.fullTrialRiskChecks,worstBracketDefinition:'Largest absolute signed-margin change among sampled category transitions; signature changes are not physical discontinuity claims',extrema:Object.fromEntries(categories.map((k,i)=>[k,this.extrema[i]])),brackets,bracketRaw,risks:this.risks,signatureStream:{path:this.persist?this.path:null,bytes:this.samples*32,sha256:this.hash.digest('hex'),encoding:'32 raw SHA256 bytes per observation; sample schedule specified by run/preflight record',inputEncoding:'receiver-major, rotor-major, source-major excluding self; UInt16LE predicate bits: bit0 downstream>0; bits1-7 signed margin>=0 in category order; then one tilt>=0 byte per drone. Inactive pairs included; signature changes need not change field',categories},coverage:'All ordered receiver-rotor/source pairs including those outside field neighbor support; domain guard applies only to production eligible pairs. Full per-pair margins are evaluated, not serialized.'};if(this.persist)save(`results/audit/${this.id}.json`,result);return result;}
}
module.exports={sample,jumpRisk,BranchAudit,categories,outerAtFar};
