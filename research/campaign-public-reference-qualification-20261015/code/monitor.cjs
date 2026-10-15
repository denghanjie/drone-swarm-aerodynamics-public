'use strict';
// Compact numerical monitor; no model imports or output side effects.
module.exports=function makeMonitor(M,B,G){
 const categories=['downZero','farStart','downFade','downCut','nearRadius','radialFade','radialCut','neighborRadius','tilt'];
 const outer=M.P.radialCutoff*M.W.parameters.spread*(M.W.parameters.minDownstream-M.W.parameters.origin)*M.P.motorDistance;
 const x={samples:0,pairSamples:0,changedPairSignatures:0,jumpChecks:0,minimumPairClearance:null,minimumObstacleClearance:null,extrema:categories.map(()=>({min:null,max:null,nearest:null})),controls:0,wallConstraints:0,pairConstraints:0,neighborChanges:0,tiltClips:0,motorBounds:0,speedLimits:0,maxRepairIterations:0,maxWallResidual:0,maxPairResidual:0,maxProjection:0,maxRawNormDefect:0};
 let prevBits=null,prevNeighbors=null;
 function fail(message,detail){throw Object.assign(Error(message),{detail});}
 function margin(k,v,id,location){if(!Number.isFinite(v))fail('Nonfinite monitor margin',{k,id});const a=x.extrema[k];if(a.min===null||v<a.min)a.min=v;if(a.max===null||v>a.max)a.max=v;if(a.nearest===null||Math.abs(v)<Math.abs(a.nearest.value))a.nearest={value:v,id,location};}
 function sample(Y,location){
  const {axes,points}=M.prepare(Y),n=Y.length,down=new Float64Array(n*(n-1)*4),radial=new Float64Array(down.length),bits=new Uint16Array(down.length);let k=0;
  for(let i=0;i<n;i++)for(let r=0;r<4;r++)for(let j=0;j<n;j++)if(i!==j){
   const a=3*j,p=12*i+3*r,dx=Y[j][0]-points[p],dy=Y[j][1]-points[p+1],dz=Y[j][2]-points[p+2];
   const d=((0+dx*axes[a])+dy*axes[a+1])+dz*axes[a+2],v=Math.hypot(dx-d*axes[a],dy-d*axes[a+1],dz-d*axes[a+2]);
   const half=M.W.parameters.spread*(d/M.P.motorDistance-M.W.parameters.origin)*M.P.motorDistance;
   const dist=Math.hypot(Y[j][0]-Y[i][0],Y[j][1]-Y[i][1],Y[j][2]-Y[i][2]);
   const m=[d,d-M.farStart,d-M.P.downstreamFade,d-M.P.downstreamCutoff,v-M.P.nearFieldRadius,v-M.P.radialFade*half,v-M.P.radialCutoff*half,dist-M.P.neighborRadius];
   for(let c=0;c<8;c++){margin(c,m[c],k,location);if(c===0?m[c]>0:m[c]>=0)bits[k]|=1<<c;}
   if(dist<M.P.neighborRadius&&d>0&&d<M.farStart&&v<M.P.nearFieldRadius)fail('Near-wake domain',{receiver:i,rotor:r,source:j,downstream:d,radial:v,location});
   down[k]=d;radial[k]=v;if(prevBits&&bits[k]!==prevBits[k])x.changedPairSignatures++;k++;
  }
  for(let i=0;i<n;i++)margin(8,axes[3*i+2]-Math.cos(M.P.maxTiltDegrees*Math.PI/180),i,location);
  prevBits=bits;x.samples++;x.pairSamples+=k;return {down,radial};
 }
 function jump(samples){x.jumpChecks++;for(let k=0;k<samples[0].down.length;k++){
  let lo=Infinity,hi=-Infinity,rl=Infinity,rh=-Infinity;for(const s of samples){lo=Math.min(lo,s.down[k]);hi=Math.max(hi,s.down[k]);rl=Math.min(rl,s.radial[k]);rh=Math.max(rh,s.radial[k]);}
  if(lo<=M.farStart&&hi>=M.farStart&&rl<outer&&rh>=M.P.nearFieldRadius)fail('Unresolved sampled finite-jump risk',{pairIndex:k,downstreamRange:[lo,hi],radialRange:[rl,rh],farStart:M.farStart,outerAtFar:outer});
 }}
 function safe(old,Y){for(let i=0;i<Y.length;i++){
  const s=Y[i];if(s.length!==17||!s.every(Number.isFinite)||Math.abs(Math.hypot(...s.slice(6,10))-1)>1e-10||s[2]<B.P.bodyRadius||s.slice(13).some(f=>f<0))fail('Accepted state domain',{drone:i});
  const hits=B.obstacleContacts(old[i],s);if(hits.length)fail('Obstacle contact envelope',{drone:i,hits});
 }for(const [i,j]of B.contactCandidates(old,Y)){const d=G.segmentPair(old[i],Y[i],old[j],Y[j]);if(d<2*B.P.bodyRadius)fail('Drone contact envelope',{i,j,distance:d});}}
 function controls(c){x.controls++;const neighbors=c.event.rows.map(r=>r.signature.neighbors);
  c.event.rows.forEach((r,i)=>{if(r.converged===false)fail('Wall repair unconverged',{drone:i,tick:c.event.tick});x.wallConstraints+=r.walls.length;x.pairConstraints+=r.pairs.length;x.tiltClips+=+r.signature.tiltClipped;x.motorBounds+=r.signature.motorBounds.filter(v=>v!==0).length;x.speedLimits+=+r.signature.speedAtLimit;x.maxRepairIterations=Math.max(x.maxRepairIterations,r.iterations);x.maxWallResidual=Math.max(x.maxWallResidual,r.wallResidual);x.maxPairResidual=Math.max(x.maxPairResidual,r.pairResidual);if(prevNeighbors&&JSON.stringify(neighbors[i])!==JSON.stringify(prevNeighbors[i]))x.neighborChanges++;});prevNeighbors=neighbors;
 }
 function clearance(Y){for(let i=0;i<Y.length;i++){for(const box of B.course.boxes){const v=G.boxDistance(Y[i],box).distance-B.P.bodyRadius;x.minimumObstacleClearance=x.minimumObstacleClearance===null?v:Math.min(x.minimumObstacleClearance,v);}for(let j=i+1;j<Y.length;j++){const v=Math.hypot(...[0,1,2].map(k=>Y[i][k]-Y[j][k]))-2*B.P.bodyRadius;x.minimumPairClearance=x.minimumPairClearance===null?v:Math.min(x.minimumPairClearance,v);}}}
 return {x,sample,jump,safe,controls,clearance,categories};
};
