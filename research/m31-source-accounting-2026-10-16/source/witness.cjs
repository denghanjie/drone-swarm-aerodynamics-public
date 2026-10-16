'use strict';
// New finite static witness. Imports only the reviewed three-function excerpt.
const {pairTerm}=require('./reference-excerpt.cjs');
const mg=.027*9.81, arm=.028, radius=.023, rho=1.225;
const area=Math.PI*radius*radius;
const c={D:2*Math.sqrt(2)*arm,decay:10.11,spread:.07668,origin:-5.817,
 minDown:2.5,neighbor:3,nearRad:.15,downFade:2,downCut:2.5,radFade:2,radCut:3,
 induced:Math.sqrt(mg/(8*rho*area)),sqrt2minus1:Math.sqrt(2)-1};
const cases=[['off',[0,0,0,0]],['quarter-hover',Array(4).fill(mg/16)],
 ['hover',Array(4).fill(mg/4)],['twice-hover',Array(4).fill(mg/2)],
 ['unequal-same-total',[.4*mg,.1*mg,.4*mg,.1*mg]]];
const arms=[[-arm,-arm,0],[arm,-arm,0],[arm,arm,0],[-arm,arm,0]];
const out={nodeVersion:process.version,scope:'20 static numerical field calls; no physical measurements or flight dynamics',calls:0,cases:[]};
for(const [id,motors] of cases){
 const p=new Float64Array(56);p.set([0,0,0],0);p.set([0,0,1],4);
 p.set([0,0,.6],28);p.set([0,0,1],32);
 for(let k=0;k<4;k++){p.set(arms[k],8+4*k);p.set(arms[k],36+4*k);p[24+k]=mg/4;p[52+k]=motors[k];}
 const fields=[];
 for(let r=0;r<4;r++){fields.push(pairTerm(p,0,1,r,c));out.calls++;}
 out.cases.push({id,sourceNominalRotorsN:motors,sourceTotalNominalN:motors.reduce((a,b)=>a+b,0),fields});
}
out.stimulusAdmitted=out.cases.every(x=>x.fields.every(f=>f.symbol===8&&f.term>0&&Number.isFinite(f.term)));
out.sourceIndependentInTheseCases=out.cases.every(x=>x.fields.every((f,k)=>Object.is(f.term,out.cases[2].fields[k].term)&&f.symbol===out.cases[2].fields[k].symbol));
process.stdout.write(JSON.stringify(out,null,2)+'\n');
if(!out.stimulusAdmitted||!out.sourceIndependentInTheseCases||out.calls!==20)process.exitCode=1;
