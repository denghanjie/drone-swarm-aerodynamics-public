'use strict';
// Exact-zero controls: E is eager; L delays radial geometry past downstream-zero exits.
// Category mask: 0 self/outside, 1 zero, 2 near fallback, 3 remaining retained.
// No positive omission or stored-reference input; all query geometry is rebuilt.
const F=require('../../../outputs/step02c-source/physics.cjs'),A=require('../../../outputs/milestone-28-source/aero.cjs'),W=require('../../../outputs/step03a-source/wake.cjs'),{Grid}=require('../../../outputs/milestone-26-source/grid.cjs');
const f0=F.P.m*F.P.g/4,D=A.P.motorDistance,area=Math.PI*A.P.rotorRadius**2,vi0=Math.sqrt(f0/(2*A.P.rho*area)),a=F.P.a;
const allowances=Object.freeze({geometry:1e-12});
const recordSemantics='source-screen-category-v1';
const maskCodes=Object.freeze({outside:0,zero:1,fallback:2,remainingRetained:3});
const dot=(x,y)=>x[0]*y[0]+x[1]*y[1]+x[2]*y[2];
function fade(start,end,x){const t=Math.max(0,Math.min(1,(x-start)/(end-start)));return 1-t*t*(3-2*t);}
function sourceScreenE(c,axis,axisNorm,radialNorm,receiverRadius,projection,counts){
 const d0=dot(c,axis),r0=Math.hypot(c[0]-d0*axis[0],c[1]-d0*axis[1],c[2]-d0*axis[2]);
 const lo=d0-axisNorm*receiverRadius-allowances.geometry,hi=d0+axisNorm*receiverRadius+allowances.geometry,rlo=Math.max(0,r0-radialNorm*receiverRadius-allowances.geometry);
 if(hi<=0||lo>=A.P.downstreamCutoff){counts.downstreamZeroExits++;return {kind:'zero',bound:0};}
 // Domain is checked before projection or radial pruning, even for weak wakes.
 if(hi>0&&lo<W.parameters.minDownstream*D&&rlo<A.P.nearFieldRadius)return {kind:'fallback',bound:null};
 if(hi<W.parameters.minDownstream*D)return {kind:'zero',bound:0};
 const dH=Math.min(hi,A.P.downstreamCutoff),half=W.parameters.spread*(dH-W.parameters.origin*D),qlo=rlo/half;
 if(qlo>=A.P.radialCutoff||projection===0)return {kind:'zero',bound:0};
 // Keep the original two-property result shape without computing a positive bound.
 return {kind:'retained',bound:null};
}
function sourceScreenL(c,axis,axisNorm,radialNorm,receiverRadius,projection,counts){
 const d0=dot(c,axis);
 const lo=d0-axisNorm*receiverRadius-allowances.geometry,hi=d0+axisNorm*receiverRadius+allowances.geometry;
 if(hi<=0||lo>=A.P.downstreamCutoff){counts.downstreamZeroExits++;return {kind:'zero',bound:0};}
 const r0=Math.hypot(c[0]-d0*axis[0],c[1]-d0*axis[1],c[2]-d0*axis[2]),rlo=Math.max(0,r0-radialNorm*receiverRadius-allowances.geometry);
 // Domain is checked before projection or radial pruning, even for weak wakes.
 if(hi>0&&lo<W.parameters.minDownstream*D&&rlo<A.P.nearFieldRadius)return {kind:'fallback',bound:null};
 if(hi<W.parameters.minDownstream*D)return {kind:'zero',bound:0};
 const dH=Math.min(hi,A.P.downstreamCutoff),half=W.parameters.spread*(dH-W.parameters.origin*D),qlo=rlo/half;
 if(qlo>=A.P.radialCutoff||projection===0)return {kind:'zero',bound:0};
 // Keep the original two-property result shape without computing a positive bound.
 return {kind:'retained',bound:null};
}
function exactTerm(states,i,j,k,points,axes,counts){
 counts.rotorVisits++;
 const d=[states[j][0]-points[i][k][0],states[j][1]-points[i][k][1],states[j][2]-points[i][k][2]],axis=axes[j],down=dot(d,axis);
 if(down<=0||down>=A.P.downstreamCutoff)return 0;
 const radial=Math.hypot(d[0]-down*axis[0],d[1]-down*axis[1],d[2]-down*axis[2]);
 if(down<W.parameters.minDownstream*D){if(radial<A.P.nearFieldRadius)throw new A.DomainError('Receiver enters unmodeled near wake',{receiver:i,source:j,rotor:k,downstream:down,radial});return 0;}
 const nd=down/D,half=W.parameters.spread*(nd-W.parameters.origin)*D;
 if(radial>=A.P.radialCutoff*half)return 0;
 counts.profileEvaluations++;
 return W.normalizedWake(nd,radial/D).speed*vi0*fade(A.P.downstreamFade,A.P.downstreamCutoff,down)*fade(A.P.radialFade,A.P.radialCutoff,radial/half)*Math.max(0,dot(axes[i],axis));
}
function fields(states,method='E',options={}){
 if(method!=='E'&&method!=='L')throw Error('Unknown zero-screen method');
 const screen=method==='E'?sourceScreenE:sourceScreenL;
 const n=states.length,axes=states.map(s=>F.rotate(s.slice(6,10),[0,0,1]));
 for(let i=0;i<n;i++)if(axes[i][2]<Math.cos(A.P.maxTiltDegrees*Math.PI/180))throw new A.DomainError('Source/receiver tilt exceeds exploratory20-degree limit',{drone:i,axis:axes[i]});
 const offsets=states.map(s=>F.rotors.map(r=>F.rotate(s.slice(6,10),[r[0],r[1],0]))),points=offsets.map((rr,i)=>rr.map(r=>r.map((v,k)=>v+states[i][k])));
 const radii=offsets.map(rr=>Math.max(...rr.map(r=>Math.hypot(...r))));
 const axisNorms=axes.map(v=>Math.hypot(...v)),radialNorms=axisNorms.map(s=>Math.max(1,Math.abs(1-s*s)));
 const grid=new Grid(states,1.5),winds=[],records=[];
 const counts={candidates:0,screenCalls:0,zeroCulls:0,positiveOmissions:0,actualPositiveOmissions:0,retained:0,nearFallbacks:0,remainingRetained:0,downstreamZeroExits:0,centerRadialHypotCalls:0,rotorVisits:0,profileEvaluations:0};
 for(let i=0;i<n;i++){
  if(options.guard)options.guard(counts);
  const ids=grid.neighbors(i,A.P.neighborRadius),wind=[0,0,0,0],mask=new Uint8Array(Math.ceil(n/4)),downstreamBefore=counts.downstreamZeroExits;
  let zero=0,retained=0,fallback=0,remaining=0;
  const put=(j,code)=>{mask[j>>2]|=code<<((j&3)*2);};
  for(const j of ids){
   counts.candidates++;counts.screenCalls++;
   // Projection stays eager for both E and L, including downstream-zero sources.
   const decision=screen([states[j][0]-states[i][0],states[j][1]-states[i][1],states[j][2]-states[i][2]],axes[j],axisNorms[j],radialNorms[j],radii[i],Math.max(0,dot(axes[i],axes[j])),counts);
   if(decision.kind==='zero'){put(j,1);counts.zeroCulls++;zero++;continue;}
   if(decision.kind==='fallback'){put(j,2);counts.nearFallbacks++;fallback++;}
   else {put(j,3);counts.remainingRetained++;remaining++;}
   counts.retained++;retained++;
   for(let k=0;k<4;k++)wind[k]+=exactTerm(states,i,j,k,points,axes,counts);
  }
  winds.push(wind);
  const downstreamZeroExits=counts.downstreamZeroExits-downstreamBefore;
  // Counts of this source-center norm follow the shared call/branch counters.
  const centerRadialHypotCalls=ids.length-(method==='L'?downstreamZeroExits:0);
  counts.centerRadialHypotCalls+=centerRadialHypotCalls;
  const row={receiver:i,mask,candidates:ids.length,screenCalls:ids.length,zeroCulls:zero,retained,nearFallbacks:fallback,remainingRetained:remaining,downstreamZeroExits,centerRadialHypotCalls,semantics:recordSemantics,actualPositiveOmissions:0,actualOmittedInflowBound:0};
  records.push(row);if(options.onReceiver)options.onReceiver(row);
 }
 return {winds,counts,records,method,recordSemantics,maskCodes,actualOmittedInflowBound:0};
}
function loadRows(states,winds){return states.map((s,i)=>{const f=winds[i].map(U=>A.effectiveThrust(f0,U)),w=F.wrench(f),torque=[w.t[0],w.t[1],0];return [...winds[i],...f,w.T,torque[0],torque[1],...F.rotate(s.slice(6,10),[0,0,w.T]),...F.rotate(s.slice(6,10),torque)];});}
function query(states,method='E',options={}){
 const field=fields(states,method,options);
 const rows=loadRows(states,field.winds);let checksum=0;for(const row of rows)for(const x of row)checksum+=x;
 return {rows,checksum,counts:field.counts,records:field.records,method,recordSemantics,maskCodes,actualOmittedInflowBound:0};
}
module.exports={f0,D,vi0,a,allowances,recordSemantics,maskCodes,fields,query};
