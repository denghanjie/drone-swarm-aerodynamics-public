'use strict';
window.__M31_BUNDLE_INSTALL__({
"./reference-excerpt.cjs":function(module,exports,require,Buffer){
'use strict';
// Exact historical function text; fresh source-accounting diagnostic only.
function fade(start,end,value){if(value<=start)return 1;if(value>=end)return 0;const t=(value-start)/(end-start);return (1-t)*(1-t)*(1+2*t);}

function pairTerm(p,i,j,r,c,centerAlreadyEligible=false) {
  const ib=28*i,jb=28*j,ob=ib+8+4*r;
  const out={symbol:0,term:0,down:0,radial:0,projection:0,center:0,validity:0,stage:0};
  if(i===j){out.symbol=1;out.validity=1;return out;}
  if(!centerAlreadyEligible){const dx=p[jb]-p[ib],dy=p[jb+1]-p[ib+1],dz=p[jb+2]-p[ib+2];out.center=Math.hypot(dx,dy,dz);out.validity|=16;
    if(!Number.isFinite(out.center)||out.center>512||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>257){out.symbol=11;out.stage=3;return out;}
    if(out.center>=c.neighbor){out.symbol=1;out.validity|=1;return out;}}
  const px=p[ib]+p[ob],py=p[ib+1]+p[ob+1],pz=p[ib+2]+p[ob+2];
  const dx=p[jb]-px,dy=p[jb+1]-py,dz=p[jb+2]-pz;
  if(![dx,dy,dz].every(Number.isFinite)||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>258){out.symbol=11;out.stage=4;return out;}
  const ax=p[jb+4],ay=p[jb+5],az=p[jb+6];
  const down=dx*ax+dy*ay+dz*az;out.down=down;
  if(!Number.isFinite(down)||Math.abs(down)>1024){out.symbol=11;out.stage=4;return out;}out.validity|=2;
  if(down<=0){out.symbol=2;out.validity|=1;return out;}
  if(down>=c.downCut){out.symbol=3;out.validity|=1;return out;}
  const radial=Math.hypot(dx-down*ax,dy-down*ay,dz-down*az);out.radial=radial;
  if(!Number.isFinite(radial)||radial>2048){out.symbol=11;out.stage=4;return out;}out.validity|=4;
  if(down<c.minDown*c.D){out.symbol=radial<c.nearRad?4:5;out.stage=out.symbol===4?4:0;if(out.symbol===5)out.validity|=1;return out;}
  const normalizedDown=down/c.D;
  const halfWidth=c.spread*(normalizedDown-c.origin)*c.D;
  if(!(halfWidth>0)||!Number.isFinite(halfWidth)){out.symbol=11;out.stage=4;return out;}
  if(radial>=c.radCut*halfWidth){out.symbol=6;out.validity|=1;return out;}
  const receiverProjection=Math.max(0,p[ib+4]*ax+p[ib+5]*ay+p[ib+6]*az);out.projection=receiverProjection;out.validity|=8;
  const xi=(radial/c.D)/(c.spread*(normalizedDown-c.origin));
  const denominator=1+c.sqrt2minus1*xi*xi;
  const normalizedSpeed=(c.decay/(normalizedDown-c.origin))/(denominator*denominator);
  const speed=normalizedSpeed*c.induced*fade(c.downFade,c.downCut,down)*fade(c.radFade,c.radCut,radial/halfWidth)*receiverProjection;
  if(!termAdmitted(speed)||!Number.isFinite(receiverProjection)){out.symbol=11;out.stage=4;return out;}
  out.term=speed;out.validity|=1;out.symbol=receiverProjection<=0?7:(speed>0?8:9);return out;
}

function termAdmitted(value){return Number.isFinite(value)&&value>=0&&value<=128;}

module.exports={fade,pairTerm,termAdmitted};

},
"./anchor-kernel.cjs":function(module,exports,require,Buffer){
'use strict';
const {pairTerm}=require('./reference-excerpt.cjs');
const mg=.027*9.81,arm=.028,radius=.023,rho=1.225,A=Math.PI*radius*radius,R=Math.sqrt(2)*arm;
const c={D:2*R,decay:10.11,spread:.07668,origin:-5.817,minDown:2.5,neighbor:3,nearRad:.15,downFade:2,downCut:2.5,radFade:2,radCut:3,induced:Math.sqrt(mg/(8*rho*A)),sqrt2minus1:Math.sqrt(2)-1};
const constants={mg,arm,radius,rho,A,R,c};
function cross(a,b){return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];}
function rotate(q,v){const t=cross(q,v).map(x=>2*x),u=cross(q,t);return v.map((x,k)=>x+(q[3]*t[k]+u[k]));}
const emptyWork=()=>({rootClosures:0,bisectionIterations:0,positiveTermMultiplications:0});
function root(alpha,w){if(!(alpha>=0&&Number.isFinite(alpha)))throw new Error('invalid alpha');w.rootClosures++;if(alpha===0)return 1;let lo=0,hi=1;for(let k=0;k<56;k++){let x=(lo+hi)/2;if(x*x*x+alpha*x-1>0)hi=x;else lo=x;w.bisectionIterations++;}return (lo+hi)/2;}
function logDistance(a,b){let v=0;for(let i=0;i<a.length;i++)v=Math.max(v,Math.abs(Math.log(a[i])-Math.log(b[i])));return v;}

function prepare(states){
 const n=states.length;
 const p=new Float64Array(28*n),nominal=states.map(s=>s.slice(13,17)),S0=nominal.map(a=>a.reduce((s,x)=>s+x,0));
 const input={finite:true,quaternionNormMaxError:0,quaternionBadCount:0,axisNormMaxError:0,axisBadCount:0,offsetNormMaxError:0,offsetDotMaxAbs:0,offsetBadCount:0,nominalZeroCount:0,nominalNegativeCount:0,nominalPositive:true,nominalTotalFinite:S0.every(Number.isFinite),geometryValid:false,maxTiltDegrees:0,tiltWithin45Count:0};
 const corners=[[arm,arm,0],[-arm,arm,0],[-arm,-arm,0],[arm,-arm,0]];
 for(let i=0;i<n;i++){
   const s=states[i],q=s.slice(6,10),axis=rotate(q,[0,0,1]);input.finite&&=s.every(Number.isFinite);
   const qe=Math.abs(Math.hypot(...q)-1),ae=Math.abs(Math.hypot(...axis)-1);input.quaternionNormMaxError=Math.max(input.quaternionNormMaxError,qe);input.axisNormMaxError=Math.max(input.axisNormMaxError,ae);if(qe>1e-10||!Number.isFinite(qe))input.quaternionBadCount++;if(ae>1e-9||!Number.isFinite(ae))input.axisBadCount++;
   p.set(s.slice(0,3),28*i);p.set(axis,28*i+4);
   const tilt=Math.acos(Math.max(-1,Math.min(1,axis[2]/Math.hypot(...axis))))*180/Math.PI;input.maxTiltDegrees=Math.max(input.maxTiltDegrees,tilt);if(tilt<=45)input.tiltWithin45Count++;
   for(let r=0;r<4;r++){const o=rotate(q,corners[r]);p.set(o,28*i+8+4*r);const ne=Math.abs(Math.hypot(...o)-R),de=Math.abs(o[0]*axis[0]+o[1]*axis[1]+o[2]*axis[2]);input.offsetNormMaxError=Math.max(input.offsetNormMaxError,ne);input.offsetDotMaxAbs=Math.max(input.offsetDotMaxAbs,de);if(ne>1e-9||de>1e-9||!Number.isFinite(ne+de))input.offsetBadCount++;if(nominal[i][r]===0)input.nominalZeroCount++;if(nominal[i][r]<0)input.nominalNegativeCount++;}
 }
 input.nominalPositive=input.finite&&nominal.every(a=>a.every(x=>x>0));input.geometryValid=input.finite&&input.quaternionBadCount===0&&input.axisBadCount===0&&input.offsetBadCount===0;
 const nominalOK=input.nominalPositive&&input.nominalTotalFinite;

 return {n,states,p,nominal,S0,input,nominalOK};
}
// Index coordinates only. World arithmetic in the exact kernel is untouched.
function indexScene(q,mode){
 if(mode==='all')return {certificate:{finite:null,min:null,max:null,spans:null,certified:null,useGrid:false,fallback:false,reason:'all-pairs-selected'},local:null,grid:null};
 const {n,states}=q,min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity];
 let finite=true;
 for(const s of states)for(let k=0;k<3;k++){finite&&=Number.isFinite(s[k]);min[k]=Math.min(min[k],s[k]);max[k]=Math.max(max[k],s[k]);}
 const spans=max.map((x,k)=>x-min[k]);
 const certified=finite&&spans.every(x=>Number.isFinite(x)&&x>=0&&x<=256);
 const useGrid=mode==='grid'&&certified,local=useGrid?states.map(s=>s.slice(0,3).map((x,k)=>x-min[k])):null,grid=new Map();
 if(useGrid)for(let j=0;j<n;j++){const key=local[j].map(x=>Math.floor(x/4)).join(',');if(!grid.has(key))grid.set(key,[]);grid.get(key).push(j);}
 return {certificate:{finite,min,max,spans,certified,useGrid,fallback:mode==='grid'&&!certified},local,grid};
}
function candidates(index,i,n){
 if(!index.certificate.useGrid)throw new Error('grid enumeration requires certificate');
 const u=index.local[i],lo=u.map(x=>Math.floor((x-3)/4)-1),hi=u.map(x=>Math.floor((x+3)/4)+1),out=[];
 for(let x=lo[0];x<=hi[0];x++)for(let y=lo[1];y<=hi[1];y++)for(let z=lo[2];z<=hi[2];z++){
  const row=index.grid.get(`${x},${y},${z}`);if(row)for(const j of row)out.push(j);
 }
 return out.sort((a,b)=>a-b);
}
function build(states,mode,fullSymbols,guard=()=>{}){
 const t0=performance.now(),q=prepare(states),{n,p,nominal,S0,input,nominalOK}=q,t1=performance.now();
 const index=indexScene(q,mode),t2=performance.now();
 const symbols=fullSymbols?Buffer.alloc(n*n*4,1):null,symbolCounts=Array(12).fill(0);symbolCounts[1]=n*n*4;
 const offsets=new Uint32Array(4*n+1),sources=[],K=[],deps=Array.from({length:n},()=>[]);
 const geometryWork={logicalDirectedPairs:n*(n-1),gatheredNonselfCandidates:0,directedCenterTests:0,certifiedSkippedPairs:0,centerEligiblePairs:0,centerGuardRejectedPairs:0,pairCalls:0,positiveRotorTerms:0};
 let scaledCapMax=nominalOK?0:null,scaledCapViolationCount=nominalOK?0:null,uniqueVehicleEdges=0,heightViolationEdges=0,orderViolationEdges=0;
 function classify(base,r,s){if(symbols)symbols[base+r]=s;if(s!==1){symbolCounts[1]--;symbolCounts[s]++;}}
 for(let i=0;i<n;i++){
  guard();const rows=[[],[],[],[]],incoming=new Set(),js=index.certificate.useGrid?candidates(index,i,n):null;let previous=-1;
  for(let jj=0;jj<(js?js.length:n);jj++){const j=js?js[jj]:jj;if(j<=previous)throw new Error('candidate order/uniqueness failure');previous=j;if(i===j)continue;
   geometryWork.gatheredNonselfCandidates++;geometryWork.directedCenterTests++;
   const dx=p[28*j]-p[28*i],dy=p[28*j+1]-p[28*i+1],dz=p[28*j+2]-p[28*i+2],center=Math.hypot(dx,dy,dz),base=4*(i*n+j);
   if(!Number.isFinite(center)||center>512||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>257){for(let r=0;r<4;r++)classify(base,r,11);geometryWork.centerGuardRejectedPairs++;continue;}
   if(center>=c.neighbor)continue;geometryWork.centerEligiblePairs++;
   for(let r=0;r<4;r++){const f=pairTerm(p,i,j,r,c,true);geometryWork.pairCalls++;classify(base,r,f.symbol);
    if(f.term>0){rows[r].push([j,f.term]);incoming.add(j);geometryWork.positiveRotorTerms++;if(geometryWork.positiveRotorTerms>2000000)throw new Error('positive coefficient guard exceeded');
     if(nominalOK){const v=f.term*Math.sqrt(S0[j]/mg);scaledCapMax=Math.max(scaledCapMax,v);if(!Number.isFinite(v)||v>128)scaledCapViolationCount++;}
    }
   }
  }
  for(let r=0;r<4;r++){for(const [j,k] of rows[r]){sources.push(j);K.push(k);}offsets[4*i+r+1]=sources.length;}
  deps[i]=[...incoming].sort((a,b)=>a-b);uniqueVehicleEdges+=deps[i].length;
  // Compare the same descending-z, ascending-ID key without constructing a schedule.
  for(const j of deps[i]){if(states[j][2]<=states[i][2])heightViolationEdges++;if(!(states[j][2]>states[i][2]||(states[j][2]===states[i][2]&&j<i)))orderViolationEdges++;}
 }
 geometryWork.certifiedSkippedPairs=geometryWork.logicalDirectedPairs-geometryWork.directedCenterTests;
 const src=Uint32Array.from(sources),kv=Float64Array.from(K),t3=performance.now(),incomingDegree=deps.map(a=>a.length);
 const graph={uniqueVehicleEdges,incomingDegree,maxIncomingDegree:Math.max(...incomingDegree),heightViolationEdges,orderViolationEdges,descendingEligible:orderViolationEdges===0};
 const reasons=[];if(!input.geometryValid)reasons.push('geometry');if(!nominalOK)reasons.push('nominal');if(symbolCounts[4])reasons.push('near-field');if(symbolCounts[11])reasons.push('invalid-term');if(scaledCapViolationCount)reasons.push('scaled-cap');
 const admission={admitted:reasons.length===0,reasons,unsupportedNearCount:symbolCounts[4],invalidTermCount:symbolCounts[11],scaledCapMax,scaledCapViolationCount};
 let ordinaryLmax=null,aa=null;
 if(nominalOK){aa=new Float64Array(K.length);let maxSum=0;for(let row=0;row<4*n;row++){let sum=0;for(let z=offsets[row];z<offsets[row+1];z++){aa[z]=kv[z]*Math.sqrt(S0[src[z]]/mg)/Math.sqrt(nominal[Math.floor(row/4)][row%4]/(2*rho*A));sum+=aa[z];}maxSum=Math.max(maxSum,sum);}ordinaryLmax=maxSum/(4*Math.sqrt(2));}
 const t4=performance.now();
 return {...q,src,kv,offsets,aa,symbols,symbolCounts,geometryWork,graph,admission,ordinaryLmax,deps,certificate:index.certificate,phasesMs:{input:t1-t0,index:t2-t1,geometry:t3-t2,admission:t4-t3}};
}
function schedule(q){return Array.from({length:q.n},(_,i)=>i).sort((i,j)=>q.states[j][2]-q.states[i][2]||i-j);}
function fullGraph(q){const order=schedule(q);let depth=null;if(q.graph.descendingEligible){depth=Array(q.n).fill(0);for(const i of order)for(const j of q.deps[i])depth[i]=Math.max(depth[i],depth[j]+1);}return {...q.graph,order,dependencyDepth:depth,maxDependencyDepth:depth?Math.max(...depth):null};}
function nodeMap(q,i,y,w){
 const {nominal,S0,offsets,aa,src}=q,rotors=[];let total=0;
 for(let r=0;r<4;r++){const row=4*i+r;let alpha=0;for(let z=offsets[row];z<offsets[row+1];z++){alpha+=aa[z]*y[src[z]];w.positiveTermMultiplications++;}const x=root(alpha,w),T=nominal[i][r]*x;rotors.push({alpha,x,T});total+=T;}
 return {y:Math.sqrt(total/S0[i]),rotors};
}
function map(q,y,w,guard){const rows=[];for(let i=0;i<q.n;i++){guard();rows.push(nodeMap(q,i,y,w));}return {y:rows.map(x=>x.y),rotors:rows.map(x=>x.rotors)};}
function solve(q,method,order,trace,guard=()=>{}){
 if(!q.admission.admitted||!q.graph.descendingEligible)throw new Error('solve domain rejected');
 const {n}=q,work=emptyWork();let y=Array(n).fill(1),rotors,extra={};
 if(method==='O'){rotors=Array(n);for(const i of order){guard();const z=nodeMap(q,i,y,work);y[i]=z.y;rotors[i]=z.rotors;}}
 else{let converged=false,lastChange=null,iterations=0,iterates=trace?[y.slice()]:null;
  for(let k=0;k<64;k++){guard();const z=map(q,y,work,guard);lastChange=logDistance(y,z.y);y=z.y;rotors=z.rotors;iterations++;if(iterates)iterates.push(y.slice());if(lastChange<=1e-11){converged=true;break;}}
  extra={iterations,converged,lastChange};if(iterates)extra.iterates=iterates;
 }
 return {y,rotors,work,...extra};
}
function residual(q,solution,guard=()=>{}){
 const residualWork=emptyWork(),residualMap=map(q,solution.y,residualWork,guard);let sourceReceiverMismatch=0;
 for(let i=0;i<q.n;i++)sourceReceiverMismatch=Math.max(sourceReceiverMismatch,Math.abs(q.S0[i]*solution.y[i]*solution.y[i]-residualMap.rotors[i].reduce((s,x)=>s+x.T,0))/q.S0[i]);
 return {residualWork,residualMap,residualLog:logDistance(solution.y,residualMap.y),sourceReceiverMismatch};
}
// Shared small output consumption is timed; full SHA and comparisons are not.
function checksum(q,s){let v=0;for(let i=0;i<q.n;i++)v+=s.y[i]*(i+1)+s.rotors[i].reduce((a,r)=>a+r.T,0);return v+(q.kv[0]||0)+(q.kv[q.kv.length-1]||0);}
function query(states,label,guard){const begin=performance.now(),q=build(states,label==='A'?'all':'grid',false,guard),t0=performance.now(),order=label==='C'?null:schedule(q),t1=performance.now(),s=solve(q,label==='C'?'P':'O',order,false,guard),t2=performance.now();Object.assign(s,residual(q,s,guard));const t3=performance.now(),check=checksum(q,s),end=performance.now(),phasesMs={...q.phasesMs,setup:t1-t0,solve:t2-t1,residual:t3-t2,checksum:end-t3};phasesMs.remainder=end-begin-Object.values(phasesMs).reduce((a,b)=>a+b,0);return {q,s,check,totalMs:end-begin,phasesMs};}
function cached(q,method,order,guard){const begin=performance.now(),s=solve(q,method,order,false,guard),t1=performance.now();Object.assign(s,residual(q,s,guard));const t2=performance.now(),check=checksum(q,s),end=performance.now();return {q,s,check,totalMs:end-begin,phasesMs:{solve:t1-begin,residual:t2-t1,checksum:end-t2}};}
module.exports={constants,build,schedule,fullGraph,solve,residual,query,cached,checksum};

},
"./lean-anchor.cjs":function(module,exports,require,Buffer){
'use strict';

// A and the numerical solver are the unchanged, separately pinned anchor.
// This file is a source-only candidate; numerical qualification is pending.
const anchor=require('./anchor-kernel.cjs');
const {fade}=require('./reference-excerpt.cjs');
const {constants}=anchor;
const {mg,arm,radius,rho,A,R,c}=constants;
const CHUNK_CAPACITY=4096;

// Preparation is copied verbatim from the frozen anchor: do not regroup rotation.
function cross(a,b){return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];}
function rotate(q,v){const t=cross(q,v).map(x=>2*x),u=cross(q,t);return v.map((x,k)=>x+(q[3]*t[k]+u[k]));}
function prepare(states){
 const n=states.length;
 const p=new Float64Array(28*n),nominal=states.map(s=>s.slice(13,17)),S0=nominal.map(a=>a.reduce((s,x)=>s+x,0));
 const input={finite:true,quaternionNormMaxError:0,quaternionBadCount:0,axisNormMaxError:0,axisBadCount:0,offsetNormMaxError:0,offsetDotMaxAbs:0,offsetBadCount:0,nominalZeroCount:0,nominalNegativeCount:0,nominalPositive:true,nominalTotalFinite:S0.every(Number.isFinite),geometryValid:false,maxTiltDegrees:0,tiltWithin45Count:0};
 const corners=[[arm,arm,0],[-arm,arm,0],[-arm,-arm,0],[arm,-arm,0]];
 for(let i=0;i<n;i++){
   const s=states[i],q=s.slice(6,10),axis=rotate(q,[0,0,1]);input.finite&&=s.every(Number.isFinite);
   const qe=Math.abs(Math.hypot(...q)-1),ae=Math.abs(Math.hypot(...axis)-1);input.quaternionNormMaxError=Math.max(input.quaternionNormMaxError,qe);input.axisNormMaxError=Math.max(input.axisNormMaxError,ae);if(qe>1e-10||!Number.isFinite(qe))input.quaternionBadCount++;if(ae>1e-9||!Number.isFinite(ae))input.axisBadCount++;
   p.set(s.slice(0,3),28*i);p.set(axis,28*i+4);
   const tilt=Math.acos(Math.max(-1,Math.min(1,axis[2]/Math.hypot(...axis))))*180/Math.PI;input.maxTiltDegrees=Math.max(input.maxTiltDegrees,tilt);if(tilt<=45)input.tiltWithin45Count++;
   for(let r=0;r<4;r++){const o=rotate(q,corners[r]);p.set(o,28*i+8+4*r);const ne=Math.abs(Math.hypot(...o)-R),de=Math.abs(o[0]*axis[0]+o[1]*axis[1]+o[2]*axis[2]);input.offsetNormMaxError=Math.max(input.offsetNormMaxError,ne);input.offsetDotMaxAbs=Math.max(input.offsetDotMaxAbs,de);if(ne>1e-9||de>1e-9||!Number.isFinite(ne+de))input.offsetBadCount++;if(nominal[i][r]===0)input.nominalZeroCount++;if(nominal[i][r]<0)input.nominalNegativeCount++;}
 }
 input.nominalPositive=input.finite&&nominal.every(a=>a.every(x=>x>0));input.geometryValid=input.finite&&input.quaternionBadCount===0&&input.axisBadCount===0&&input.offsetBadCount===0;
 const nominalOK=input.nominalPositive&&input.nominalTotalFinite;

 return {n,states,p,nominal,S0,input,nominalOK};
}

function typedChunks(){
 const sourceChunks=[],KChunks=[];
 let length=0,used=0,chunkCount=0,rowCopySegments=0;
 return {
  appendRow(ids,values,rowLength){
   let at=0;
   while(at<rowLength){
    if(chunkCount===0||used===CHUNK_CAPACITY){
     sourceChunks.push(new Uint32Array(CHUNK_CAPACITY));
     KChunks.push(new Float64Array(CHUNK_CAPACITY));
     chunkCount++;used=0;
    }
    const take=Math.min(rowLength-at,CHUNK_CAPACITY-used);
    sourceChunks[chunkCount-1].set(ids.subarray(at,at+take),used);
    KChunks[chunkCount-1].set(values.subarray(at,at+take),used);
    at+=take;used+=take;length+=take;rowCopySegments++;
   }
  },
  get length(){return length;},
  finish(){
   // These allocations own the outputs; neither scratch nor chunk views escape.
   const src=new Uint32Array(length),kv=new Float64Array(length);
   let at=0;
   for(let k=0;k<chunkCount;k++){
    const take=Math.min(CHUNK_CAPACITY,length-at);
    src.set(sourceChunks[k].subarray(0,take),at);
    kv.set(KChunks[k].subarray(0,take),at);
    at+=take;
   }
   const stats={chunkCount,
    chunkGrowthCount:Math.max(0,chunkCount-1),chunkTypedArrayAllocations:2*chunkCount,
    chunkCapacityEntries:chunkCount*CHUNK_CAPACITY,
    chunkUsedEntries:length,chunkSpareEntries:chunkCount*CHUNK_CAPACITY-length,
    chunkAllocatedPayloadBytes:chunkCount*CHUNK_CAPACITY*12,
    rowToChunkCopySegments:rowCopySegments,chunkToFinalCopySegments:chunkCount,
    rowToChunkCopiedEntries:length,chunkToFinalCopiedEntries:length,
    rowToChunkCopiedBytes:12*length,chunkToFinalCopiedBytes:12*length};
   // Release references, without claiming when garbage collection occurs.
   sourceChunks.length=0;KChunks.length=0;
   return {src,kv,stats};
  }
 };
}

function buildAssembly(states,mode,fullSymbols,guard=()=>{}){
 const typed=mode==='typed';
 const t0=performance.now(),q=prepare(states),{n,p,nominal,S0,input,nominalOK}=q,t1=performance.now();
 // Exactly the original all-pairs certificate; assembly is separate metadata.
 const certificate={finite:null,min:null,max:null,spans:null,certified:null,useGrid:false,fallback:false,reason:'all-pairs-selected'},t2=performance.now();
 const symbols=fullSymbols?Buffer.alloc(n*n*4,1):null,symbolCounts=Array(12).fill(0);symbolCounts[1]=n*n*4;
 const offsets=new Uint32Array(4*n+1),deps=Array.from({length:n},()=>[]);
 const sourceRows=typed?Array.from({length:4},()=>new Uint32Array(n)):null;
 const KRows=typed?Array.from({length:4},()=>new Float64Array(n)):null;
 const rowLengths=[0,0,0,0],points=new Float64Array(12);
 const writer=typed?typedChunks():null,sources=typed?null:[],K=typed?null:[];
 const geometryWork={logicalDirectedPairs:n*(n-1),gatheredNonselfCandidates:0,directedCenterTests:0,certifiedSkippedPairs:0,centerEligiblePairs:0,centerGuardRejectedPairs:0,pairCalls:0,positiveRotorTerms:0};
 let scaledCapMax=nominalOK?0:null,scaledCapViolationCount=nominalOK?0:null,uniqueVehicleEdges=0,heightViolationEdges=0,orderViolationEdges=0,maxRowLength=0;
 function classify(base,r,s){if(symbols)symbols[base+r]=s;if(s!==1){symbolCounts[1]--;symbolCounts[s]++;}}
 for(let i=0;i<n;i++){
  guard();
  const ib=28*i,receiverAx=p[ib+4],receiverAy=p[ib+5],receiverAz=p[ib+6];
  // Same point sums as pairTerm, including binary64 rounding and signed zero.
  for(let r=0;r<4;r++){
   const ob=ib+8+4*r;
   points[3*r]=p[ib]+p[ob];points[3*r+1]=p[ib+1]+p[ob+1];points[3*r+2]=p[ib+2]+p[ob+2];
  }
  const rows=typed?null:[[],[],[],[]],incoming=typed?null:new Set();
  rowLengths.fill(0);
  let previous=-1;
  for(let j=0;j<n;j++){
   if(j<=previous)throw new Error('candidate order/uniqueness failure');previous=j;if(i===j)continue;
   geometryWork.gatheredNonselfCandidates++;geometryWork.directedCenterTests++;
   const jb=28*j,sx=p[jb],sy=p[jb+1],sz=p[jb+2];
   const dx=sx-p[ib],dy=sy-p[ib+1],dz=sz-p[ib+2],center=Math.hypot(dx,dy,dz),base=4*(i*n+j);
   if(!Number.isFinite(center)||center>512||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>257){for(let r=0;r<4;r++)classify(base,r,11);geometryWork.centerGuardRejectedPairs++;continue;}
   if(center>=c.neighbor)continue;geometryWork.centerEligiblePairs++;
   const ax=p[jb+4],ay=p[jb+5],az=p[jb+6];
   let projectionReady=false,receiverProjection=0,sourcePositive=false;
   // Shared scalar classifier for L and T. Consume each rotor immediately:
   // computing all four first would move a positive-cap failure past later work.
   for(let r=0;r<4;r++){
    let symbol=0,term=0;
    rotor: {
     const dx=sx-points[3*r],dy=sy-points[3*r+1],dz=sz-points[3*r+2];
     if(!Number.isFinite(dx)||!Number.isFinite(dy)||!Number.isFinite(dz)||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>258){symbol=11;break rotor;}
     const down=dx*ax+dy*ay+dz*az;
     if(!Number.isFinite(down)||Math.abs(down)>1024){symbol=11;break rotor;}
     if(down<=0){symbol=2;break rotor;}
     if(down>=c.downCut){symbol=3;break rotor;}
     const radial=Math.hypot(dx-down*ax,dy-down*ay,dz-down*az);
     if(!Number.isFinite(radial)||radial>2048){symbol=11;break rotor;}
     if(down<c.minDown*c.D){symbol=radial<c.nearRad?4:5;break rotor;}
     const normalizedDown=down/c.D;
     const halfWidth=c.spread*(normalizedDown-c.origin)*c.D;
     if(!(halfWidth>0)||!Number.isFinite(halfWidth)){symbol=11;break rotor;}
     if(radial>=c.radCut*halfWidth){symbol=6;break rotor;}
     if(!projectionReady){
      receiverProjection=Math.max(0,receiverAx*ax+receiverAy*ay+receiverAz*az);
      projectionReady=true;
     }
     const xi=(radial/c.D)/(c.spread*(normalizedDown-c.origin));
     const denominator=1+c.sqrt2minus1*xi*xi;
     const normalizedSpeed=(c.decay/(normalizedDown-c.origin))/(denominator*denominator);
     const speed=normalizedSpeed*c.induced*fade(c.downFade,c.downCut,down)*fade(c.radFade,c.radCut,radial/halfWidth)*receiverProjection;
     if(!(Number.isFinite(speed)&&speed>=0&&speed<=128)||!Number.isFinite(receiverProjection)){symbol=11;break rotor;}
     term=speed;symbol=receiverProjection<=0?7:(speed>0?8:9);
    }
    geometryWork.pairCalls++;classify(base,r,symbol);
    if(term>0){
     if(typed){
      const at=rowLengths[r];
      // Capacity N is structural, not a pruning budget. Never truncate a row.
      if(at>=n)throw new Error('typed row capacity invariant failure');
      sourceRows[r][at]=j;KRows[r][at]=term;rowLengths[r]=at+1;
     }else{
      rows[r].push([j,term]);incoming.add(j);rowLengths[r]++;
     }
     sourcePositive=true;
     geometryWork.positiveRotorTerms++;if(geometryWork.positiveRotorTerms>2000000)throw new Error('positive coefficient guard exceeded');
     if(nominalOK){const v=term*Math.sqrt(S0[j]/mg);scaledCapMax=Math.max(scaledCapMax,v);if(!Number.isFinite(v)||v>128)scaledCapViolationCount++;}
    }
   }
   // Ascending j, once per source, gives the same unique sorted dependencies.
   if(typed&&sourcePositive)deps[i].push(j);
  }
  for(let r=0;r<4;r++){
   maxRowLength=Math.max(maxRowLength,rowLengths[r]);
   if(typed){writer.appendRow(sourceRows[r],KRows[r],rowLengths[r]);offsets[4*i+r+1]=writer.length;}
   else{for(const [j,k] of rows[r]){sources.push(j);K.push(k);}offsets[4*i+r+1]=sources.length;}
  }
  if(!typed)deps[i]=[...incoming].sort((a,b)=>a-b);
  uniqueVehicleEdges+=deps[i].length;
  for(const j of deps[i]){if(states[j][2]<=states[i][2])heightViolationEdges++;if(!(states[j][2]>states[i][2]||(states[j][2]===states[i][2]&&j<i)))orderViolationEdges++;}
 }
 geometryWork.certifiedSkippedPairs=geometryWork.logicalDirectedPairs-geometryWork.directedCenterTests;
 const packed=typed?writer.finish():null;
 const src=typed?packed.src:Uint32Array.from(sources),kv=typed?packed.kv:Float64Array.from(K),t3=performance.now(),incomingDegree=deps.map(a=>a.length);
 const graph={uniqueVehicleEdges,incomingDegree,maxIncomingDegree:Math.max(...incomingDegree),heightViolationEdges,orderViolationEdges,descendingEligible:orderViolationEdges===0};
 const reasons=[];if(!input.geometryValid)reasons.push('geometry');if(!nominalOK)reasons.push('nominal');if(symbolCounts[4])reasons.push('near-field');if(symbolCounts[11])reasons.push('invalid-term');if(scaledCapViolationCount)reasons.push('scaled-cap');
 const admission={admitted:reasons.length===0,reasons,unsupportedNearCount:symbolCounts[4],invalidTermCount:symbolCounts[11],scaledCapMax,scaledCapViolationCount};
 let ordinaryLmax=null,aa=null;
 if(nominalOK){aa=new Float64Array(kv.length);let maxSum=0;for(let row=0;row<4*n;row++){let sum=0;for(let z=offsets[row];z<offsets[row+1];z++){aa[z]=kv[z]*Math.sqrt(S0[src[z]]/mg)/Math.sqrt(nominal[Math.floor(row/4)][row%4]/(2*rho*A));sum+=aa[z];}maxSum=Math.max(maxSum,sum);}ordinaryLmax=maxSum/(4*Math.sqrt(2));}
 const t4=performance.now();
 const entries=kv.length,rowScratchBytes=typed?48*n:0;
 const assemblyStats={schema:'m31-receiver-row-assembly-v1',mode,inputN:n,positiveEntries:entries,dependencyEntries:uniqueVehicleEdges,
  rowCapacityEntries:typed?n:null,rowLengthsAtLastReceiver:rowLengths.slice(),maxRowLengthEntries:maxRowLength,
  rowGrowthCount:typed?0:null,rowScratchTypedArrayAllocations:typed?8:0,
  rowScratchIdBytes:typed?16*n:0,rowScratchKBytes:typed?32*n:0,rowScratchBytes,
  rotorPointScratchBytes:points.byteLength,rotorPointTypedArrayAllocations:1,
  chunkPolicyCapacityEntries:CHUNK_CAPACITY,
  ...(typed?packed.stats:{chunkCount:0,chunkGrowthCount:0,chunkTypedArrayAllocations:0,chunkCapacityEntries:0,chunkUsedEntries:0,chunkSpareEntries:0,chunkAllocatedPayloadBytes:0,rowToChunkCopySegments:0,chunkToFinalCopySegments:0,rowToChunkCopiedEntries:0,chunkToFinalCopiedEntries:0,rowToChunkCopiedBytes:0,chunkToFinalCopiedBytes:0}),
  ordinaryPositiveTupleCount:typed?0:entries,ordinarySetAddCalls:typed?0:entries,ordinaryDependencySetCount:typed?0:n,
  ordinaryGlobalSourceEntries:typed?0:entries,ordinaryGlobalKEntries:typed?0:entries,
  ordinaryRowToGlobalCopiedEntries:typed?0:entries,ordinaryGlobalToFinalCopiedEntries:typed?0:entries,
  dependencyOutputRepresentation:'independent ordinary arrays; ascending unique IDs',
  dependencyOutputArrays:n,finalSourceBytes:src.byteLength,finalKBytes:kv.byteLength,offsetBytes:offsets.byteLength,scalingBytes:aa?aa.byteLength:0,
  outputTypedArraysOwnBuffers:true,scratchViewsReturned:false,
  jsHeapBytesMeasured:false,garbageCollectionMeasured:false};
 // Payload accounting only, not an observed process/JS heap peak. Symbols and
 // prepared input geometry are common and are listed separately below.
 assemblyStats.finalizationOverlapKnownPayloadBytes=rowScratchBytes+points.byteLength+offsets.byteLength+assemblyStats.chunkAllocatedPayloadBytes+src.byteLength+kv.byteLength;
 assemblyStats.allocatedAssemblyTypedPayloadBytes=assemblyStats.finalizationOverlapKnownPayloadBytes+assemblyStats.scalingBytes;
 assemblyStats.commonPreparedGeometryBytes=p.byteLength;
 assemblyStats.commonSymbolBytes=symbols?symbols.byteLength:0;
 return {...q,src,kv,offsets,aa,symbols,symbolCounts,geometryWork,graph,admission,ordinaryLmax,deps,certificate,assemblyStats,phasesMs:{input:t1-t0,index:t2-t1,geometry:t3-t2,admission:t4-t3}};
}

function build(states,mode,fullSymbols,guard){
 if(mode==='all'||mode==='grid')return anchor.build(states,mode,fullSymbols,guard);
 if(mode==='lean'||mode==='typed')return buildAssembly(states,mode,fullSymbols,guard);
 throw new Error('unknown builder mode');
}
function query(states,label,guard){
 if(label==='A'||label==='B'||label==='C')return anchor.query(states,label,guard);
 if(label!=='L'&&label!=='T')throw new Error('unknown query label');
 const begin=performance.now(),q=build(states,label==='L'?'lean':'typed',false,guard),t0=performance.now(),order=anchor.schedule(q),t1=performance.now(),s=anchor.solve(q,'O',order,false,guard),t2=performance.now();Object.assign(s,anchor.residual(q,s,guard));const t3=performance.now(),check=anchor.checksum(q,s),end=performance.now(),phasesMs={...q.phasesMs,setup:t1-t0,solve:t2-t1,residual:t3-t2,checksum:end-t3};phasesMs.remainder=end-begin-Object.values(phasesMs).reduce((a,b)=>a+b,0);return {q,s,check,totalMs:end-begin,phasesMs};
}
module.exports={constants,build,schedule:anchor.schedule,fullGraph:anchor.fullGraph,solve:anchor.solve,residual:anchor.residual,query,cached:anchor.cached,checksum:anchor.checksum};

},
"./kernel.cjs":function(module,exports,require,Buffer){
'use strict';

// Finite pinned-runtime experiment only; no portable Math.hypot equivalence claim.
// L delegates the byte-pinned original; F changes only the center-screen path.
const anchor=require('./anchor-kernel.cjs');
const lean=require('./lean-anchor.cjs');
const {fade}=require('./reference-excerpt.cjs');
const {constants}=anchor;
const {mg,arm,radius,rho,A,R,c}=constants;
const CHUNK_CAPACITY=4096;

// Preparation is copied verbatim from the frozen anchor: do not regroup rotation.
function cross(a,b){return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];}
function rotate(q,v){const t=cross(q,v).map(x=>2*x),u=cross(q,t);return v.map((x,k)=>x+(q[3]*t[k]+u[k]));}
function prepare(states){
 const n=states.length;
 const p=new Float64Array(28*n),nominal=states.map(s=>s.slice(13,17)),S0=nominal.map(a=>a.reduce((s,x)=>s+x,0));
 const input={finite:true,quaternionNormMaxError:0,quaternionBadCount:0,axisNormMaxError:0,axisBadCount:0,offsetNormMaxError:0,offsetDotMaxAbs:0,offsetBadCount:0,nominalZeroCount:0,nominalNegativeCount:0,nominalPositive:true,nominalTotalFinite:S0.every(Number.isFinite),geometryValid:false,maxTiltDegrees:0,tiltWithin45Count:0};
 const corners=[[arm,arm,0],[-arm,arm,0],[-arm,-arm,0],[arm,-arm,0]];
 for(let i=0;i<n;i++){
   const s=states[i],q=s.slice(6,10),axis=rotate(q,[0,0,1]);input.finite&&=s.every(Number.isFinite);
   const qe=Math.abs(Math.hypot(...q)-1),ae=Math.abs(Math.hypot(...axis)-1);input.quaternionNormMaxError=Math.max(input.quaternionNormMaxError,qe);input.axisNormMaxError=Math.max(input.axisNormMaxError,ae);if(qe>1e-10||!Number.isFinite(qe))input.quaternionBadCount++;if(ae>1e-9||!Number.isFinite(ae))input.axisBadCount++;
   p.set(s.slice(0,3),28*i);p.set(axis,28*i+4);
   const tilt=Math.acos(Math.max(-1,Math.min(1,axis[2]/Math.hypot(...axis))))*180/Math.PI;input.maxTiltDegrees=Math.max(input.maxTiltDegrees,tilt);if(tilt<=45)input.tiltWithin45Count++;
   for(let r=0;r<4;r++){const o=rotate(q,corners[r]);p.set(o,28*i+8+4*r);const ne=Math.abs(Math.hypot(...o)-R),de=Math.abs(o[0]*axis[0]+o[1]*axis[1]+o[2]*axis[2]);input.offsetNormMaxError=Math.max(input.offsetNormMaxError,ne);input.offsetDotMaxAbs=Math.max(input.offsetDotMaxAbs,de);if(ne>1e-9||de>1e-9||!Number.isFinite(ne+de))input.offsetBadCount++;if(nominal[i][r]===0)input.nominalZeroCount++;if(nominal[i][r]<0)input.nominalNegativeCount++;}
 }
 input.nominalPositive=input.finite&&nominal.every(a=>a.every(x=>x>0));input.geometryValid=input.finite&&input.quaternionBadCount===0&&input.axisBadCount===0&&input.offsetBadCount===0;
 const nominalOK=input.nominalPositive&&input.nominalTotalFinite;

 return {n,states,p,nominal,S0,input,nominalOK};
}

function screenPredicate(p,n){
 const min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity];
 let coordinateFinite=true;
 for(let i=0;i<n;i++)for(let k=0;k<3;k++){
  const value=p[28*i+k];
  coordinateFinite=Number.isFinite(value)&&coordinateFinite;
  min[k]=Math.min(min[k],value);max[k]=Math.max(max[k],value);
 }
 const spans=max.map((value,k)=>value-min[k]),spanFinite=spans.every(Number.isFinite);
 const eligible=coordinateFinite&&spanFinite&&spans.every(value=>value>=0&&value<=256);
 return {schema:'m31-center-screen-work-v1',finiteRuntimeOnly:true,runtimeGeneralEquivalenceProven:false,
  spanLimit:256,componentThreshold:4,coordinateFinite,spanFinite,min,max,spans,eligible,fallback:!eligible,
  fallbackReason:eligible?null:!coordinateFinite?'coordinate-nonfinite':!spanFinite?'span-nonfinite':'span-out-of-range',
  omissionEvidence:'reconstruct-from-saved-current-positions-and-frozen-predicate',
  historicalCertifiedSkippedPairsIsFormalProof:false};
}
function finishScreen(screen,work){
 return {...screen,orderedPairVisits:work.gatheredNonselfCandidates,
  componentTests:screen.eligible?work.gatheredNonselfCandidates:0,
  skippedCenterNormCalls:work.certifiedSkippedPairs,actualCenterNormCalls:work.directedCenterTests};
}

function typedChunks(){
 const sourceChunks=[],KChunks=[];
 let length=0,used=0,chunkCount=0,rowCopySegments=0;
 return {
  appendRow(ids,values,rowLength){
   let at=0;
   while(at<rowLength){
    if(chunkCount===0||used===CHUNK_CAPACITY){
     sourceChunks.push(new Uint32Array(CHUNK_CAPACITY));
     KChunks.push(new Float64Array(CHUNK_CAPACITY));
     chunkCount++;used=0;
    }
    const take=Math.min(rowLength-at,CHUNK_CAPACITY-used);
    sourceChunks[chunkCount-1].set(ids.subarray(at,at+take),used);
    KChunks[chunkCount-1].set(values.subarray(at,at+take),used);
    at+=take;used+=take;length+=take;rowCopySegments++;
   }
  },
  get length(){return length;},
  finish(){
   // These allocations own the outputs; neither scratch nor chunk views escape.
   const src=new Uint32Array(length),kv=new Float64Array(length);
   let at=0;
   for(let k=0;k<chunkCount;k++){
    const take=Math.min(CHUNK_CAPACITY,length-at);
    src.set(sourceChunks[k].subarray(0,take),at);
    kv.set(KChunks[k].subarray(0,take),at);
    at+=take;
   }
   const stats={chunkCount,
    chunkGrowthCount:Math.max(0,chunkCount-1),chunkTypedArrayAllocations:2*chunkCount,
    chunkCapacityEntries:chunkCount*CHUNK_CAPACITY,
    chunkUsedEntries:length,chunkSpareEntries:chunkCount*CHUNK_CAPACITY-length,
    chunkAllocatedPayloadBytes:chunkCount*CHUNK_CAPACITY*12,
    rowToChunkCopySegments:rowCopySegments,chunkToFinalCopySegments:chunkCount,
    rowToChunkCopiedEntries:length,chunkToFinalCopiedEntries:length,
    rowToChunkCopiedBytes:12*length,chunkToFinalCopiedBytes:12*length};
   // Release references, without claiming when garbage collection occurs.
   sourceChunks.length=0;KChunks.length=0;
   return {src,kv,stats};
  }
 };
}

function buildAssembly(states,mode,fullSymbols,guard=()=>{}){
 const typed=mode==='typed';
 const t0=performance.now(),q=prepare(states),{n,p,nominal,S0,input,nominalOK}=q,t1=performance.now();
 // Original all-pairs certificate remains unchanged. screen is finite-runtime evidence.
 const screen=screenPredicate(p,n);
 const certificate={finite:null,min:null,max:null,spans:null,certified:null,useGrid:false,fallback:false,reason:'all-pairs-selected'},t2=performance.now();
 if(!screen.eligible){
  // Full unchanged-L evaluation, including its preparation and original guards.
  // The preceding current preparation/predicate is intentionally paid in F.
  const delegatedStart=performance.now(),fallback=lean.build(states,'lean',fullSymbols,guard);
  return {...fallback,screen:finishScreen(screen,fallback.geometryWork),
   phasesMs:{...fallback.phasesMs,screenPreflight:delegatedStart-t0}};
 }
 const symbols=fullSymbols?Buffer.alloc(n*n*4,1):null,symbolCounts=Array(12).fill(0);symbolCounts[1]=n*n*4;
 const offsets=new Uint32Array(4*n+1),deps=Array.from({length:n},()=>[]);
 const sourceRows=typed?Array.from({length:4},()=>new Uint32Array(n)):null;
 const KRows=typed?Array.from({length:4},()=>new Float64Array(n)):null;
 const rowLengths=[0,0,0,0],points=new Float64Array(12);
 const writer=typed?typedChunks():null,sources=typed?null:[],K=typed?null:[];
 const geometryWork={logicalDirectedPairs:n*(n-1),gatheredNonselfCandidates:0,directedCenterTests:0,certifiedSkippedPairs:0,centerEligiblePairs:0,centerGuardRejectedPairs:0,pairCalls:0,positiveRotorTerms:0};
 let scaledCapMax=nominalOK?0:null,scaledCapViolationCount=nominalOK?0:null,uniqueVehicleEdges=0,heightViolationEdges=0,orderViolationEdges=0,maxRowLength=0;
 function classify(base,r,s){if(symbols)symbols[base+r]=s;if(s!==1){symbolCounts[1]--;symbolCounts[s]++;}}
 for(let i=0;i<n;i++){
  guard();
  const ib=28*i,receiverAx=p[ib+4],receiverAy=p[ib+5],receiverAz=p[ib+6];
  // Same point sums as pairTerm, including binary64 rounding and signed zero.
  for(let r=0;r<4;r++){
   const ob=ib+8+4*r;
   points[3*r]=p[ib]+p[ob];points[3*r+1]=p[ib+1]+p[ob+1];points[3*r+2]=p[ib+2]+p[ob+2];
  }
  const rows=typed?null:[[],[],[],[]],incoming=typed?null:new Set();
  rowLengths.fill(0);
  let previous=-1;
  for(let j=0;j<n;j++){
   if(j<=previous)throw new Error('candidate order/uniqueness failure');previous=j;if(i===j)continue;
   geometryWork.gatheredNonselfCandidates++;
   const jb=28*j,sx=p[jb],sy=p[jb+1],sz=p[jb+2];
   const dx=sx-p[ib],dy=sy-p[ib+1],dz=sz-p[ib+2],base=4*(i*n+j);
   // Observed finite-runtime equivalence is required; this is not a library proof.
   if(Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>=screen.componentThreshold)continue;
   geometryWork.directedCenterTests++;
   const center=Math.hypot(dx,dy,dz);
   if(!Number.isFinite(center)||center>512||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>257){for(let r=0;r<4;r++)classify(base,r,11);geometryWork.centerGuardRejectedPairs++;continue;}
   if(center>=c.neighbor)continue;geometryWork.centerEligiblePairs++;
   const ax=p[jb+4],ay=p[jb+5],az=p[jb+6];
   let projectionReady=false,receiverProjection=0,sourcePositive=false;
   // Shared scalar classifier for L and T. Consume each rotor immediately:
   // computing all four first would move a positive-cap failure past later work.
   for(let r=0;r<4;r++){
    let symbol=0,term=0;
    rotor: {
     const dx=sx-points[3*r],dy=sy-points[3*r+1],dz=sz-points[3*r+2];
     if(!Number.isFinite(dx)||!Number.isFinite(dy)||!Number.isFinite(dz)||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>258){symbol=11;break rotor;}
     const down=dx*ax+dy*ay+dz*az;
     if(!Number.isFinite(down)||Math.abs(down)>1024){symbol=11;break rotor;}
     if(down<=0){symbol=2;break rotor;}
     if(down>=c.downCut){symbol=3;break rotor;}
     const radial=Math.hypot(dx-down*ax,dy-down*ay,dz-down*az);
     if(!Number.isFinite(radial)||radial>2048){symbol=11;break rotor;}
     if(down<c.minDown*c.D){symbol=radial<c.nearRad?4:5;break rotor;}
     const normalizedDown=down/c.D;
     const halfWidth=c.spread*(normalizedDown-c.origin)*c.D;
     if(!(halfWidth>0)||!Number.isFinite(halfWidth)){symbol=11;break rotor;}
     if(radial>=c.radCut*halfWidth){symbol=6;break rotor;}
     if(!projectionReady){
      receiverProjection=Math.max(0,receiverAx*ax+receiverAy*ay+receiverAz*az);
      projectionReady=true;
     }
     const xi=(radial/c.D)/(c.spread*(normalizedDown-c.origin));
     const denominator=1+c.sqrt2minus1*xi*xi;
     const normalizedSpeed=(c.decay/(normalizedDown-c.origin))/(denominator*denominator);
     const speed=normalizedSpeed*c.induced*fade(c.downFade,c.downCut,down)*fade(c.radFade,c.radCut,radial/halfWidth)*receiverProjection;
     if(!(Number.isFinite(speed)&&speed>=0&&speed<=128)||!Number.isFinite(receiverProjection)){symbol=11;break rotor;}
     term=speed;symbol=receiverProjection<=0?7:(speed>0?8:9);
    }
    geometryWork.pairCalls++;classify(base,r,symbol);
    if(term>0){
     if(typed){
      const at=rowLengths[r];
      // Capacity N is structural, not a pruning budget. Never truncate a row.
      if(at>=n)throw new Error('typed row capacity invariant failure');
      sourceRows[r][at]=j;KRows[r][at]=term;rowLengths[r]=at+1;
     }else{
      rows[r].push([j,term]);incoming.add(j);rowLengths[r]++;
     }
     sourcePositive=true;
     geometryWork.positiveRotorTerms++;if(geometryWork.positiveRotorTerms>2000000)throw new Error('positive coefficient guard exceeded');
     if(nominalOK){const v=term*Math.sqrt(S0[j]/mg);scaledCapMax=Math.max(scaledCapMax,v);if(!Number.isFinite(v)||v>128)scaledCapViolationCount++;}
    }
   }
   // Ascending j, once per source, gives the same unique sorted dependencies.
   if(typed&&sourcePositive)deps[i].push(j);
  }
  for(let r=0;r<4;r++){
   maxRowLength=Math.max(maxRowLength,rowLengths[r]);
   if(typed){writer.appendRow(sourceRows[r],KRows[r],rowLengths[r]);offsets[4*i+r+1]=writer.length;}
   else{for(const [j,k] of rows[r]){sources.push(j);K.push(k);}offsets[4*i+r+1]=sources.length;}
  }
  if(!typed)deps[i]=[...incoming].sort((a,b)=>a-b);
  uniqueVehicleEdges+=deps[i].length;
  for(const j of deps[i]){if(states[j][2]<=states[i][2])heightViolationEdges++;if(!(states[j][2]>states[i][2]||(states[j][2]===states[i][2]&&j<i)))orderViolationEdges++;}
 }
 geometryWork.certifiedSkippedPairs=geometryWork.logicalDirectedPairs-geometryWork.directedCenterTests;
 const packed=typed?writer.finish():null;
 const src=typed?packed.src:Uint32Array.from(sources),kv=typed?packed.kv:Float64Array.from(K),t3=performance.now(),incomingDegree=deps.map(a=>a.length);
 const graph={uniqueVehicleEdges,incomingDegree,maxIncomingDegree:Math.max(...incomingDegree),heightViolationEdges,orderViolationEdges,descendingEligible:orderViolationEdges===0};
 const reasons=[];if(!input.geometryValid)reasons.push('geometry');if(!nominalOK)reasons.push('nominal');if(symbolCounts[4])reasons.push('near-field');if(symbolCounts[11])reasons.push('invalid-term');if(scaledCapViolationCount)reasons.push('scaled-cap');
 const admission={admitted:reasons.length===0,reasons,unsupportedNearCount:symbolCounts[4],invalidTermCount:symbolCounts[11],scaledCapMax,scaledCapViolationCount};
 let ordinaryLmax=null,aa=null;
 if(nominalOK){aa=new Float64Array(kv.length);let maxSum=0;for(let row=0;row<4*n;row++){let sum=0;for(let z=offsets[row];z<offsets[row+1];z++){aa[z]=kv[z]*Math.sqrt(S0[src[z]]/mg)/Math.sqrt(nominal[Math.floor(row/4)][row%4]/(2*rho*A));sum+=aa[z];}maxSum=Math.max(maxSum,sum);}ordinaryLmax=maxSum/(4*Math.sqrt(2));}
 const t4=performance.now();
 const entries=kv.length,rowScratchBytes=typed?48*n:0;
 const assemblyStats={schema:'m31-receiver-row-assembly-v1',mode:mode==='screen'?'lean':mode,inputN:n,positiveEntries:entries,dependencyEntries:uniqueVehicleEdges,
  rowCapacityEntries:typed?n:null,rowLengthsAtLastReceiver:rowLengths.slice(),maxRowLengthEntries:maxRowLength,
  rowGrowthCount:typed?0:null,rowScratchTypedArrayAllocations:typed?8:0,
  rowScratchIdBytes:typed?16*n:0,rowScratchKBytes:typed?32*n:0,rowScratchBytes,
  rotorPointScratchBytes:points.byteLength,rotorPointTypedArrayAllocations:1,
  chunkPolicyCapacityEntries:CHUNK_CAPACITY,
  ...(typed?packed.stats:{chunkCount:0,chunkGrowthCount:0,chunkTypedArrayAllocations:0,chunkCapacityEntries:0,chunkUsedEntries:0,chunkSpareEntries:0,chunkAllocatedPayloadBytes:0,rowToChunkCopySegments:0,chunkToFinalCopySegments:0,rowToChunkCopiedEntries:0,chunkToFinalCopiedEntries:0,rowToChunkCopiedBytes:0,chunkToFinalCopiedBytes:0}),
  ordinaryPositiveTupleCount:typed?0:entries,ordinarySetAddCalls:typed?0:entries,ordinaryDependencySetCount:typed?0:n,
  ordinaryGlobalSourceEntries:typed?0:entries,ordinaryGlobalKEntries:typed?0:entries,
  ordinaryRowToGlobalCopiedEntries:typed?0:entries,ordinaryGlobalToFinalCopiedEntries:typed?0:entries,
  dependencyOutputRepresentation:'independent ordinary arrays; ascending unique IDs',
  dependencyOutputArrays:n,finalSourceBytes:src.byteLength,finalKBytes:kv.byteLength,offsetBytes:offsets.byteLength,scalingBytes:aa?aa.byteLength:0,
  outputTypedArraysOwnBuffers:true,scratchViewsReturned:false,
  jsHeapBytesMeasured:false,garbageCollectionMeasured:false};
 // Payload accounting only, not an observed process/JS heap peak. Symbols and
 // prepared input geometry are common and are listed separately below.
 assemblyStats.finalizationOverlapKnownPayloadBytes=rowScratchBytes+points.byteLength+offsets.byteLength+assemblyStats.chunkAllocatedPayloadBytes+src.byteLength+kv.byteLength;
 assemblyStats.allocatedAssemblyTypedPayloadBytes=assemblyStats.finalizationOverlapKnownPayloadBytes+assemblyStats.scalingBytes;
 assemblyStats.commonPreparedGeometryBytes=p.byteLength;
 assemblyStats.commonSymbolBytes=symbols?symbols.byteLength:0;
 return {...q,src,kv,offsets,aa,symbols,symbolCounts,geometryWork,graph,admission,ordinaryLmax,deps,certificate,assemblyStats,screen:finishScreen(screen,geometryWork),phasesMs:{input:t1-t0,index:t2-t1,geometry:t3-t2,admission:t4-t3}};
}

function build(states,mode,fullSymbols,guard){
 if(mode==='screen')return buildAssembly(states,mode,fullSymbols,guard);
 return lean.build(states,mode,fullSymbols,guard);
}
function query(states,label,guard){
 if(label!=='F')return lean.query(states,label,guard);
 const begin=performance.now(),q=build(states,'screen',false,guard),t0=performance.now(),order=anchor.schedule(q),t1=performance.now(),s=anchor.solve(q,'O',order,false,guard),t2=performance.now();Object.assign(s,anchor.residual(q,s,guard));const t3=performance.now(),check=anchor.checksum(q,s),end=performance.now(),phasesMs={...q.phasesMs,setup:t1-t0,solve:t2-t1,residual:t3-t2,checksum:end-t3};phasesMs.remainder=end-begin-Object.values(phasesMs).reduce((a,b)=>a+b,0);return {q,s,check,totalMs:end-begin,phasesMs};
}
module.exports={constants,build,schedule:anchor.schedule,fullGraph:anchor.fullGraph,solve:anchor.solve,residual:anchor.residual,query,cached:anchor.cached,checksum:anchor.checksum};

},
"./controls.cjs":function(module,exports,require,Buffer){
'use strict';
// Fixed prospective definitions. No source import, fixture evaluation or tuning here.
function nextUp(x){if(x===0)return Number.MIN_VALUE;const b=Buffer.alloc(8);b.writeDoubleLE(x);let u=b.readBigUInt64LE();u+=x>0?1n:-1n;b.writeBigUInt64LE(u);return b.readDoubleLE();}
const nextDown=x=>-nextUp(-x);

const controlIds=Object.freeze([
 'radius-0-below','radius-0-exact','radius-0-above',
 'radius--6-below','radius--6-exact','radius--6-above',
 'cell-below','cell-exact','cell-above','signed-zero','coarse-origin','coarse-translated',
 'dense-16','span-256','span-nextUp256','far-invalid258','nonfinite-nan','nonfinite-infinity',
 'overflow-span','near-field','duplicates','planes-62','planes-64','planes-66',
 'component-x-below','component-x-exact','component-x-above',
 'component-y-below','component-y-exact','component-y-above',
 'component-z-below','component-z-exact','component-z-above',
 'span-diagonal-256','span-nextDown256','center-257-fallback','center-nextUp257-fallback',
 'mixed-near-far','mixed-positive-far','invalid-quaternion-far',
 'nominal-zero-positive-far','nominal-negative-positive-far','nominal-nan-positive-far',
 'scaled-cap-positive-far','invalid-quaternion-nan-far','nominal-infinity-positive-far',
 'nominal-total-overflow-positive-far','nominal-unequal-positive-far'
]);

function controls(){
 // The original 24 positional definitions are retained without arithmetic changes.
 const out=[],add=(id,positions,grid)=>out.push({id,positions,expectedGrid:grid});
 for(const x of [0,-6])for(const [name,fn] of [['below',nextDown],['exact',x=>x],['above',nextUp]])add(`radius-${x}-${name}`,[[x,0,0],[fn(x+3),0,0]],true);
 for(const [axis,name,fn] of [[0,'below',nextDown],[1,'exact',x=>x],[2,'above',nextUp]]){const rotate=v=>v.map((_,k)=>v[(k-axis+3)%3]);add(`cell-${name}`,[[0,0,0],rotate([fn(4),.25,.5]),rotate([4,0,1])],true);}
 add('signed-zero',[[-0,0,0],[0,-0,0]],true);
 const coarse=[[0,0,0],[1,.25,.5],[4,1,2]];add('coarse-origin',coarse,true);add('coarse-translated',coarse.map(a=>a.map(x=>x+2**40)),true);
 add('dense-16',Array.from({length:16},(_,i)=>[i*.05,0,.45*(i%3)]),true);
 add('span-256',[[0,0,0],[256,0,0]],true);add('span-nextUp256',[[0,0,0],[nextUp(256),0,0]],false);
 add('far-invalid258',[[0,0,0],[258,0,0]],false);add('nonfinite-nan',[[0,0,0],[NaN,0,0]],false);add('nonfinite-infinity',[[0,0,0],[Infinity,0,0]],false);add('overflow-span',[[-Number.MAX_VALUE,0,0],[Number.MAX_VALUE,0,0]],false);
 add('near-field',[[0,0,0],[0,0,.02]],true);add('duplicates',[[1,1,1],[1,1,1]],true);
 for(const n of [62,64,66])add(`planes-${n}`,Array.from({length:n},(_,i)=>[0,0,i<n/2?0:.6]),true);
 const originalFallback={
  'span-nextUp256':'span-out-of-range','far-invalid258':'span-out-of-range',
  'nonfinite-nan':'coordinate-nonfinite','nonfinite-infinity':'coordinate-nonfinite',
  'overflow-span':'span-nonfinite'
 };
 for(const item of out){item.expectedScreenEligible=item.expectedGrid;item.expectedFallbackReason=originalFallback[item.id]||null;}

 const addScreen=(id,positions,eligible=true,statePatches=[],fallbackReason=null)=>out.push({
  id,positions,expectedScreenEligible:eligible,expectedFallbackReason:fallbackReason,statePatches
 });
 for(const [axis,axisName] of [[0,'x'],[1,'y'],[2,'z']]){
  for(const [name,fn] of [['below',nextDown],['exact',x=>x],['above',nextUp]]){
   const position=[0,0,0];position[axis]=fn(4);
   addScreen(`component-${axisName}-${name}`,[[0,0,0],position]);
  }
 }
 addScreen('span-diagonal-256',[[0,0,0],[256,256,256]]);
 addScreen('span-nextDown256',[[0,0,0],[nextDown(256),0,0]]);
 addScreen('center-257-fallback',[[0,0,0],[257,0,0]],false,[],'span-out-of-range');
 addScreen('center-nextUp257-fallback',[[0,0,0],[nextUp(257),0,0]],false,[],'span-out-of-range');
 addScreen('mixed-near-far',[[0,0,0],[0,0,.02],[4,0,0]]);
 addScreen('mixed-positive-far',[[0,0,0],[0,0,.6],[4,0,0]]);
 addScreen('invalid-quaternion-far',[[0,0,0],[4,0,0]],true,[{vehicle:0,index:9,value:2}]);
 addScreen('nominal-zero-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[{vehicle:1,index:13,value:0}]);
 addScreen('nominal-negative-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[{vehicle:1,index:13,value:-.01}]);
 addScreen('nominal-nan-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[{vehicle:1,index:13,value:NaN}]);
 addScreen('scaled-cap-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[13,14,15,16].map(index=>({vehicle:1,index,value:1e12})));
 addScreen('invalid-quaternion-nan-far',[[0,0,0],[4,0,0]],true,[{vehicle:0,index:6,value:NaN}]);
 addScreen('nominal-infinity-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[{vehicle:1,index:13,value:Infinity}]);
 addScreen('nominal-total-overflow-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[13,14,15,16].map(index=>({vehicle:1,index,value:Number.MAX_VALUE})));
 addScreen('nominal-unequal-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[.03,.04,.05,.06].map((value,r)=>({vehicle:1,index:13+r,value})));
 return out;
}

// Six separately paid cross-call builds, while retaining planes-66 L/F outputs.
// sparse2=[[0,0,0],[4,0,0]], planes62 is the original planes-62 literal,
// fallback258=[[0,0,0],[258,0,0]]. Each call receives fresh state arrays.
const ownershipSequence=Object.freeze(['L:sparse2','F:sparse2','L:planes62','F:planes62','L:fallback258','F:fallback258']);
module.exports={controls,controlIds,ownershipSequence};

}
});
