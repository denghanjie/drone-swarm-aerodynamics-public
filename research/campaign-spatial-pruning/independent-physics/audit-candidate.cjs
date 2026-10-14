'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const file=path.resolve(process.argv[2]||path.join(__dirname,'../implementation/src/pruned-aero.cjs')),M=require(file),F=M.F;
let seed=93017;const random=()=>((seed=(1664525*seed+1013904223)>>>0)/4294967296);
const pose=(x,y,z,tilt=0,az=0)=>[x,y,z,0,0,0,Math.cos(az)*Math.sin(tilt/2),Math.sin(az)*Math.sin(tilt/2),0,Math.cos(tilt/2),0,0,0,...Array(4).fill(F.P.m*F.P.g/4)];
let cases=0,domain=0,omitted=0,maxReferenceDifference=0,maxError=0,maxForceError=0,maxMomentError=0,boundViolation=0;
for(let k=0;k<1200;k++){
 const down=[.1979898987,.2,.5,1,1.999999,2,2.25,2.49,2.5,2.51][k%10]+(random()-.5)*.03;
 const states=[pose(0,0,0,random()*.348,random()*Math.PI*2),pose((random()-.5)*1.4,(random()-.5)*1.4,down,random()*.348,random()*Math.PI*2)];
 for(const s of states)for(let r=13;r<17;r++)s[r]*=.1+2.15*random();
 let reference,exact,approx,referenceError,candidateError;
 try{reference=M.A.fields(states,'sum-rotor');}catch(e){referenceError=e;}
 try{exact=M.fields(states,{epsilon:0});approx=M.fields(states,{epsilon:.04});}catch(e){candidateError=e;}
 if(referenceError||candidateError){assert(referenceError instanceof M.DomainError&&candidateError instanceof M.DomainError);domain++;continue;}
 for(let i=0;i<states.length;i++){
  const b=M.loadBounds(states[i],approx.winds[i],approx.omittedBounds[i]),x=M.loads(states[i],reference.winds[i]),y=M.loads(states[i],approx.winds[i]);
  for(let r=0;r<4;r++){maxReferenceDifference=Math.max(maxReferenceDifference,Math.abs(reference.winds[i][r]-exact.winds[i][r]));const e=reference.winds[i][r]-approx.winds[i][r];maxError=Math.max(maxError,e);boundViolation=Math.max(boundViolation,e-approx.omittedBounds[i]);assert(e>=-1e-12&&e<=approx.omittedBounds[i]+1e-12);}
  const ef=Math.hypot(...x.force.map((v,k)=>v-y.force[k])),em=Math.hypot(...x.moment.map((v,k)=>v-y.moment[k]));maxForceError=Math.max(maxForceError,ef);maxMomentError=Math.max(maxMomentError,em);assert(ef<=b.force+1e-12);assert(em<=b.moment+1e-13);assert(ef<=.005*F.P.m*F.P.g);assert(em<=.0075*F.P.m*F.P.g*F.P.a);
 }
 omitted+=approx.omittedPairs;cases++;
}
assert(maxReferenceDifference<=1e-12);
const out={scope:'Independent finite candidate sweep, no timing or physical claims',sourceSha256:crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),seed:93017,cases,matchingDomainExits:domain,omittedPairs:omitted,maxReferenceDifference,maxError,maxForceError,maxMomentError,maxBoundViolation:boundViolation,pass:true};
fs.writeFileSync(path.join(__dirname,'candidate-audit-checks.json'),JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(out,null,2));
