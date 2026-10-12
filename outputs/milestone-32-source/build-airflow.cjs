'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const A=require('../milestone-28-source/aero.cjs'),W=require('../step03a-source/wake.cjs'),F=require('../step02c-source/physics.cjs');
const dir=__dirname,source=path.join(dir,'../milestone-28-source'),nominal=F.P.m*F.P.g/4;
const pose=(p)=>[...p,0,0,0,0,0,0,1,0,0,0,...Array(4).fill(nominal)];
const mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
let checks=[];function check(name,pass){assert(pass,name);checks.push({name,pass});}
const demo=[];
for(let di=1;di<=28;di++)for(let xi=-30;xi<=30;xi++){
 const down=di/10,x=xi/50,states=[pose([0,0,3]),pose([x,0,3-down])];
 try{const f=A.fields(states,'sum-rotor');demo.push({down,x,winds:f.winds[1],sourceWinds:f.winds[0],liftFraction:mean(f.winds[1].map(u=>A.effectiveThrust(nominal,u)/nominal))});}
 catch(e){if(!(e instanceof A.DomainError))throw e;demo.push({down,x,domain:e.message});}
}
const self=A.fields([pose([0,0,3])],'sum-rotor');check('No self inflow',self.maximumInflow===0);
check('Receiver above source has no downward-wake inflow',A.fields([pose([0,0,2]),pose([0,0,3])],'sum-rotor').winds[1].every(u=>u===0));
check('Zero inflow leaves thrust unchanged',A.effectiveThrust(nominal,0)===nominal);
check('Beyond cutoff yields zero',A.fields([pose([0,0,3]),pose([0,0,.4])],'sum-rotor').maximumInflow===0);
const center=demo.find(x=>x.down===1&&x.x===0),side=demo.find(x=>x.down===1&&x.x===.6);
check('Centered receiver has more inflow than offset receiver',mean(center.winds)>mean(side.winds));
check('Near wake is explicitly unsupported',!!demo.find(x=>x.down===.1&&x.x===0).domain);
let residual=0;for(const d of demo)if(d.winds)for(const u of d.winds){const f=A.effectiveThrust(nominal,u);residual=Math.max(residual,Math.abs(A.idealPower(f,u)-A.idealPower(nominal,0)));}
check('Receiver power identity residual below 1e-12 W',residual<1e-12);
const plume=[];for(let i=0;i<=46;i++){const down=.2+i*.05,r=W.hoverWake({downstream:down,radial:0,mass:F.P.m,propRadius:A.P.rotorRadius,motorDistance:A.P.motorDistance});plume.push({down,halfWidth:r.halfWidthM,centerSpeed:r.speedMS});}
check('Half-width contour gives half centerline speed',Math.abs(W.normalizedWake(12,W.parameters.spread*(12-W.parameters.origin)).speed/W.normalizedWake(12,0).speed-.5)<1e-14);
const cases=[];
for(const mode of ['off','sum-force','sum-rotor','rss-rotor']){
 const id='primary-1601-50-wide-'+mode+'-0.0025-0.01',record=JSON.parse(fs.readFileSync(path.join(source,id+'.json'))),raw=fs.readFileSync(path.join(source,record.replay.file)),frames=[];
 check(mode+' binary frame length',raw.length===record.replay.frames*record.replay.valuesPerFrame*8);
 for(let k=0;k<record.replay.frames;k++){
  const values=Array.from({length:record.replay.valuesPerFrame},(_,i)=>raw.readDoubleLE((k*record.replay.valuesPerFrame+i)*8)),t=values[0];
  const poses=Array.from({length:50},(_,i)=>values.slice(1+7*i,1+7*(i+1))),states=poses.map(p=>[...p.slice(0,3),0,0,0,...p.slice(3),0,0,0,...Array(4).fill(nominal)]);
  let field,links=[],domain=null;
  try{field=A.fields(states,mode);if(mode!=='off')for(let i=0;i<50;i++){const contributions=[];let total=[0,0,0,0];for(let j=0;j<50;j++)if(i!==j){const w=A.fields([states[i],states[j]],'sum-rotor').winds[0];for(let r=0;r<4;r++)total[r]+=mode==='rss-rotor'?w[r]*w[r]:w[r];if(mean(w)>.03)contributions.push({source:j,receiver:i,inflow:mean(w)});}for(let r=0;r<4;r++)assert(Math.abs((mode==='rss-rotor'?Math.sqrt(total[r]):total[r])-field.winds[i][r])<1e-12);links.push(...contributions.sort((a,b)=>b.inflow-a.inflow).slice(0,2));}}
  catch(e){if(!(e instanceof A.DomainError))throw e;domain=e.message;field=null;links=[];}
  frames.push({t,poses,winds:field?.winds||null,maximumInflow:field?.maximumInflow??null,links,domain});
 }
 cases.push({id,mode,frames,crossings:record.crossings,metrics:record.metrics,provenance:'Historical milestone 28; baseline controller; not milestone 31 wall-priority',file:'../milestone-28-source/'+id+'.json'});
}
check('Pair decomposition matches all valid reconstructed field frames',true);
const data={parameters:A.P,rotors:F.rotors,nominalRotorThrustN:nominal,demo,plume,cases,geometry:JSON.parse(fs.readFileSync(path.join(source,'factory-wide.json'))),semantics:'Snapshot field reconstructed only at saved exact Float64 poses. Pose-only state sufficient because source strength prescribed from isolated hover; not historical held field or actual rotor loads.'};
fs.writeFileSync(path.join(dir,'airflow.json'),JSON.stringify(data));fs.writeFileSync(path.join(dir,'../milestone-32-airflow-checks.json'),JSON.stringify({checks,powerResidualW:residual,counts:{demo:demo.length,cases:cases.length,frames:cases.map(c=>({mode:c.mode,total:c.frames.length,domainFailures:c.frames.filter(f=>f.domain).length}))}},null,2));
console.log('Airflow data and',checks.length,'checks saved');
