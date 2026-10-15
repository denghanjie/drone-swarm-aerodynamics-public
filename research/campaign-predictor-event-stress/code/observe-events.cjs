'use strict';
// Read-only observer. It consumes existing monitor geometry; no wake, controller,
// initializer or dynamics call. Its results never enter history or evolution.
module.exports=function makeObserver(M){
 const far=M.farStart,near=M.P.nearFieldRadius,cut=M.P.downstreamCutoff,neighbor=M.P.neighborRadius;
 const outer=M.P.radialCutoff*M.W.parameters.spread*(M.W.parameters.minDownstream-M.W.parameters.origin)*M.P.motorDistance;
 const x={work:{sampleAttempts:0,samples:0,pairVisits:0,centerDistanceEvaluations:0,endpointSamples:0,endpointPairComparisons:0,controllerCalls:0,controllerRows:0,wallRowsInspected:0,tupleCopies:0},
  outerAtFar:outer,nearestFarStart:null,nearestJumpAnnulus:null,
  walls:{listedVehicleTicks:0,listedConstraintRows:0,repairVehicleTicks:0,responseCount:0,significantBeforeCount:0,maximumBeforeResidual:0,maximumAfterResidual:0,firstListed:null,worstBefore:null,firstResponse:null,worstResponse:null},
  support:{radial:{count:0,entries:0,exits:0,first:null},axial:{count:0,entries:0,exits:0,first:null}},
  scope:'Sampled joint geometry and accepted-endpoint transitions only; unsigned annulus distance is not a continuous safety certificate'};
 let previous=null;
 const half=d=>M.W.parameters.spread*(d/M.P.motorDistance-M.W.parameters.origin)*M.P.motorDistance;
 function tuple(Y,location,i,r,j,d,v,dist){x.work.tupleCopies++;return {receiver:i,rotor:r,source:j,location:{...location},downstream:d,radial:v,halfWidth:half(d),neighborCenterDistance:dist,farStart:far,outerAtFar:outer,receiverState:Y[i].slice(),sourceState:Y[j].slice(),statesAreNormalizedGeometry:true};}
 function sample(Y,location,s){
  x.work.sampleAttempts++;const n=Y.length,dist=new Float64Array(n*n);let k=0;
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j){dist[i*n+j]=Math.hypot(Y[j][0]-Y[i][0],Y[j][1]-Y[i][1],Y[j][2]-Y[i][2]);x.work.centerDistanceEvaluations++;}
  for(let i=0;i<n;i++)for(let r=0;r<4;r++)for(let j=0;j<n;j++)if(i!==j){
   const d=s.down[k],v=s.radial[k],c=dist[i*n+j],b=half(d),gap=Math.abs(d-far),annulus=Math.hypot(d-far,Math.max(0,near-v,v-outer));
   if(x.nearestFarStart===null||gap<x.nearestFarStart.distance)x.nearestFarStart={distance:gap,...tuple(Y,location,i,r,j,d,v,c)};
   if(x.nearestJumpAnnulus===null||annulus<x.nearestJumpAnnulus.distance)x.nearestJumpAnnulus={distance:annulus,...tuple(Y,location,i,r,j,d,v,c)};
   if(location.role==='endpoint'&&previous){
    x.work.endpointPairComparisons++;
    const pd=previous.down[k],pv=previous.radial[k],pc=previous.dist[i*n+j],pb=half(pd);
    function transition(name,eligible,oldInside,newInside){if(!eligible||oldInside===newInside)return;const q=x.support[name];q.count++;newInside?q.entries++:q.exits++;if(q.first===null)q.first={direction:newInside?'entry':'exit',previous:tuple(previous.Y,previous.location,i,r,j,pd,pv,pc),current:tuple(Y,location,i,r,j,d,v,c),otherPredicatesSatisfiedAtBothEndpoints:true};}
    transition('radial',pd>=far&&d>=far&&pd<cut&&d<cut&&pc<neighbor&&c<neighbor,pv-M.P.radialCutoff*pb<0,v-M.P.radialCutoff*b<0);
    transition('axial',pd>=far&&d>=far&&pv<M.P.radialCutoff*pb&&v<M.P.radialCutoff*b&&pc<neighbor&&c<neighbor,pd-cut<0,d-cut<0);
   }
   x.work.pairVisits++;k++;
  }
  if(k!==s.down.length||k!==s.radial.length)throw Error('Observer/monitor pair ordering mismatch');
  if(location.role==='endpoint'){x.work.endpointSamples++;previous={down:s.down,radial:s.radial,dist,Y,location:{...location}};}
  x.work.samples++;
 }
 function controls(c,Y){
  x.work.controllerCalls++;
  for(const row of c.event.rows){
   x.work.controllerRows++;x.work.wallRowsInspected+=row.walls.length;
   const w=x.walls,listed=row.walls.length>0,response=row.beforeWallResidual>1e-8&&row.iterations>0&&row.wallResidual<=1e-9;
   w.listedVehicleTicks+=+listed;w.listedConstraintRows+=row.walls.length;w.repairVehicleTicks+=+(row.iterations>0);w.responseCount+=+response;w.significantBeforeCount+=+(row.beforeWallResidual>1e-8);
   w.maximumBeforeResidual=Math.max(w.maximumBeforeResidual,row.beforeWallResidual);w.maximumAfterResidual=Math.max(w.maximumAfterResidual,row.wallResidual);
   const firstListed=listed&&w.firstListed===null,worstBefore=listed&&(w.worstBefore===null||row.beforeWallResidual>w.worstBefore.beforeWallResidual),firstResponse=response&&w.firstResponse===null,worstResponse=response&&(w.worstResponse===null||row.beforeWallResidual>w.worstResponse.beforeWallResidual);
   if(firstListed||worstBefore||firstResponse||worstResponse){
    const z={tick:c.event.tick,vehicle:row.drone,state:Y[row.drone].slice(),walls:row.walls.map(a=>({obstacle:a.obstacle,n:a.n.slice(),lower:a.lower})),beforeWallResidual:row.beforeWallResidual,wallResidual:row.wallResidual,pairResidual:row.pairResidual,iterations:row.iterations,converged:row.converged,actual:row.actual.slice(),velocity:row.velocity.slice(),commands:row.commands.slice(),strictResponse:response,beforeRepairVelocityAvailable:false};
    if(firstListed)w.firstListed=z;if(worstBefore)w.worstBefore=z;if(firstResponse)w.firstResponse=z;if(worstResponse)w.worstResponse=z;
   }
  }
 }
 return {x,sample,controls};
};
