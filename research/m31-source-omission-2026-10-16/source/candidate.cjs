'use strict';
// No stored-reference input: every query rebuilds all geometry, neighbors and decisions.
const F=require('../../../outputs/step02c-source/physics.cjs'),A=require('../../../outputs/milestone-28-source/aero.cjs'),W=require('../../../outputs/step03a-source/wake.cjs'),{Grid}=require('../../../outputs/milestone-26-source/grid.cjs');
const f0=F.P.m*F.P.g/4,D=A.P.motorDistance,area=Math.PI*A.P.rotorRadius**2,vi0=Math.sqrt(f0/(2*A.P.rho*area)),L=f0/(3*vi0),a=F.P.a;
const targets=Object.freeze({thrust:.005*F.P.m*F.P.g,roll:.0005*F.P.m*F.P.g*D,pitch:.0005*F.P.m*F.P.g*D});
const allowances=Object.freeze({geometry:1e-12,boundRelative:1e-12,boundAbsolute:1e-12,rotor:1e-12,inflowAudit:1e-11});
const Bcap=Math.min((targets.thrust-4*allowances.rotor)/(4*L),(targets.roll-4*a*allowances.rotor)/(2*a*L),(targets.pitch-4*a*allowances.rotor)/(2*a*L));
const bits=new DataView(new ArrayBuffer(8));
function nextUp(x){if(!Number.isFinite(x)||x<0)throw Error('nextUp accepts finite nonnegative inputs');if(x===0)return Number.MIN_VALUE;bits.setFloat64(0,x,false);bits.setBigUint64(0,bits.getBigUint64(0,false)+1n,false);return bits.getFloat64(0,false);}
const dot=(x,y)=>x[0]*y[0]+x[1]*y[1]+x[2]*y[2];
function fade(start,end,x){const t=Math.max(0,Math.min(1,(x-start)/(end-start)));return 1-t*t*(3-2*t);}
function sourceBound(c,axis,axisNorm,radialNorm,receiverRadius,projection){
 const d0=dot(c,axis),r0=Math.hypot(c[0]-d0*axis[0],c[1]-d0*axis[1],c[2]-d0*axis[2]);
 const lo=d0-axisNorm*receiverRadius-allowances.geometry,hi=d0+axisNorm*receiverRadius+allowances.geometry,rlo=Math.max(0,r0-radialNorm*receiverRadius-allowances.geometry);
 if(hi<=0||lo>=A.P.downstreamCutoff)return {kind:'zero',bound:0};
 // Domain is checked before projection or radial pruning, even for weak wakes.
 if(hi>0&&lo<W.parameters.minDownstream*D&&rlo<A.P.nearFieldRadius)return {kind:'fallback',bound:null};
 if(hi<W.parameters.minDownstream*D)return {kind:'zero',bound:0};
 const dL=Math.max(lo,W.parameters.minDownstream*D),dH=Math.min(hi,A.P.downstreamCutoff),half=W.parameters.spread*(dH-W.parameters.origin*D),qlo=rlo/half;
 if(qlo>=A.P.radialCutoff||projection===0)return {kind:'zero',bound:0};
 const denom=1+(Math.SQRT2-1)*qlo*qlo;
 const raw=projection*vi0*W.parameters.decay/(dL/D-W.parameters.origin)*fade(A.P.downstreamFade,A.P.downstreamCutoff,dL)*fade(A.P.radialFade,A.P.radialCutoff,qlo)/(denom*denom);
 return {kind:'positive',bound:nextUp(raw*(1+allowances.boundRelative)+allowances.boundAbsolute)};
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
function fields(states,omit,options={}){
 const n=states.length,axes=states.map(s=>F.rotate(s.slice(6,10),[0,0,1]));
 for(let i=0;i<n;i++)if(axes[i][2]<Math.cos(A.P.maxTiltDegrees*Math.PI/180))throw new A.DomainError('Source/receiver tilt exceeds exploratory20-degree limit',{drone:i,axis:axes[i]});
 const offsets=states.map(s=>F.rotors.map(r=>F.rotate(s.slice(6,10),[r[0],r[1],0]))),points=offsets.map((rr,i)=>rr.map(r=>r.map((v,k)=>v+states[i][k])));
 // Matched baseline shares geometry but does not pay unused bound preprocessing.
 const radii=omit?offsets.map(rr=>Math.max(...rr.map(r=>Math.hypot(...r)))):null;
 const axisNorms=omit?axes.map(v=>Math.hypot(...v)):null,radialNorms=omit?axisNorms.map(s=>Math.max(1,Math.abs(1-s*s))):null;
 const grid=new Grid(states,1.5),winds=[],records=[];
 const counts={candidates:0,boundAttempts:0,zeroCulls:0,positiveOmissions:0,retained:0,nearFallbacks:0,rotorVisits:0,profileEvaluations:0};
 for(let i=0;i<n;i++){
  if(options.guard)options.guard(counts);
  const ids=grid.neighbors(i,A.P.neighborRadius),wind=[0,0,0,0],mask=(omit||options.evidence)?new Uint8Array(Math.ceil(n/4)):null,omitted=[];
  let B=0,zero=0,retained=0,fallback=0;
  const put=(j,code)=>{if(mask)mask[j>>2]|=code<<((j&3)*2);};
  for(const j of ids){
   counts.candidates++;let decision;
   if(omit){counts.boundAttempts++;decision=sourceBound([states[j][0]-states[i][0],states[j][1]-states[i][1],states[j][2]-states[i][2]],axes[j],axisNorms[j],radialNorms[j],radii[i],Math.max(0,dot(axes[i],axes[j])));
    if(decision.kind==='zero'){put(j,1);counts.zeroCulls++;zero++;continue;}
    if(decision.kind==='fallback'){counts.nearFallbacks++;fallback++;}
    else {const next=nextUp(B+decision.bound);if(next<=Bcap){B=next;put(j,3);counts.positiveOmissions++;omitted.push([j,decision.bound]);continue;}}
   }
   put(j,2);counts.retained++;retained++;
   for(let k=0;k<4;k++)wind[k]+=exactTerm(states,i,j,k,points,axes,counts);
  }
  winds.push(wind);
  if(omit||options.evidence){const row={receiver:i,mask,omitted,B,candidates:ids.length,zeroCulls:zero,retained,nearFallbacks:fallback};records.push(row);if(options.onReceiver)options.onReceiver(row);}
 }
 return {winds,counts,records};
}
function loadRows(states,winds){return states.map((s,i)=>{const f=winds[i].map(U=>A.effectiveThrust(f0,U)),w=F.wrench(f),torque=[w.t[0],w.t[1],0];return [...winds[i],...f,w.T,torque[0],torque[1],...F.rotate(s.slice(6,10),[0,0,w.T]),...F.rotate(s.slice(6,10),torque)];});}
function query(states,method,options={}){
 const field=method==='B'?A.fields(states,'sum-rotor'):fields(states,method==='C',options);
 const rows=loadRows(states,field.winds);let checksum=0;for(const row of rows)for(const x of row)checksum+=x;
 return {rows,checksum,counts:field.counts||{candidates:field.candidates,rotorVisits:4*field.candidates,profileEvaluations:field.contributions},records:field.records||[]};
}
module.exports={f0,D,vi0,L,a,targets,allowances,Bcap,nextUp,sourceBound,fields,query};
