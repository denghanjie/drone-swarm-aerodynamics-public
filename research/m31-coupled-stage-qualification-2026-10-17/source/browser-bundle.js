'use strict';
window.__M31_BUNDLE_INSTALL__({
"./vendor/reference-excerpt.cjs":function(module,exports,require,Buffer,process){
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
"./vendor/anchor-kernel.cjs":function(module,exports,require,Buffer,process){
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
"./vendor/lean-anchor.cjs":function(module,exports,require,Buffer,process){
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
"./vendor/kernel.cjs":function(module,exports,require,Buffer,process){
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
"./native-load.cjs":function(module,exports,require,Buffer,process){
'use strict';

// Source-only draft. Loading/executing this module requires the parent's
// separately frozen source approval and execution allocation.
const K = require('./vendor/kernel.cjs');
const MAX_N = 5000;
const POSITIVE_TERM_CAP = 2000000;
const RESIDUAL_LOG_LIMIT = 1e-9;
const SOURCE_RECEIVER_LIMIT = 2e-9;
const {mg, arm, radius, rho, A, R, c} = K.constants;
const CONSTANTS = Object.freeze({mg, arm, radius, rho, A, R,
  D: c.D, decay: c.decay, spread: c.spread, origin: c.origin,
  minDown: c.minDown, neighbor: c.neighbor, nearRad: c.nearRad,
  downFade: c.downFade, downCut: c.downCut, radFade: c.radFade,
  radCut: c.radCut, induced: c.induced, kappa: c.sqrt2minus1});

class Refusal extends Error {
  constructor(status, reason) { super(reason); this.status = status; this.reason = reason; }
}
function need(ok, status, reason) { if (!ok) throw new Refusal(status, reason); }
function finite(value) { return typeof value === 'number' && Number.isFinite(value); }
function positive(value) { return finite(value) && value > 0; }
function dataProperty(object, name) {
  const property = Object.getOwnPropertyDescriptor(object, name);
  need(property && Object.hasOwn(property, 'value'), 'input-refused', 'accessor-or-missing-property');
  return property.value;
}
function record(object, names) {
  need(object !== null && typeof object === 'object' && !Array.isArray(object),
    'input-refused', 'record-shape');
  const prototype = Object.getPrototypeOf(object);
  need(prototype === Object.prototype || prototype === null, 'input-refused', 'record-prototype');
  const keys = Reflect.ownKeys(object);
  need(keys.length === names.length && names.every(name => keys.includes(name)),
    'input-refused', 'record-fields');
  for (const name of names) dataProperty(object, name);
}
function dense(array, expected, limit) {
  need(Array.isArray(array) && Object.getPrototypeOf(array) === Array.prototype,
    'input-refused', 'array-type');
  const length = dataProperty(array, 'length');
  need(Number.isSafeInteger(length) && length >= 0,
    'input-refused', 'array-length');
  if (limit !== undefined) need(length <= limit, 'resource-failure', 'drone-count-limit');
  if (expected !== undefined) need(length === expected, 'input-refused', 'array-length');
  need(Reflect.ownKeys(array).length === length + 1, 'input-refused', 'array-extra-or-missing-property');
  for (let i = 0; i < length; i++) dataProperty(array, String(i));
  return length;
}
function captureInput(input, poll) {
  record(input, ['drones']);
  const drones = dataProperty(input, 'drones');
  const n = dense(drones, undefined, MAX_N);
  need(n > 0, 'input-refused', 'empty-input');
  const copied = [], seen = new Set();
  for (let i = 0; i < n; i++) {
    poll();
    const item = dataProperty(drones, String(i)); record(item, ['id', 'state']);
    const id = dataProperty(item, 'id'), state = dataProperty(item, 'state');
    need(Number.isSafeInteger(id) && id >= 0 && !Object.is(id, -0),
      'input-refused', 'id-domain');
    need(!seen.has(id), 'input-refused', 'duplicate-id'); seen.add(id);
    dense(state, 17);
    const owned = new Array(17);
    for (let k = 0; k < 17; k++) {
      const value = dataProperty(state, String(k));
      need(finite(value), 'input-refused', 'raw-nonfinite'); owned[k] = value;
    }
    let total = 0;
    for (let r = 0; r < 4; r++) {
      const force = owned[13 + r];
      need(force > 0, 'input-refused', 'nominal-nonpositive'); total += force;
      const denominator = force / (2 * rho * A), nu = Math.sqrt(denominator);
      need(positive(denominator) && positive(nu), 'numerical-failure', 'normalizer-range');
    }
    need(positive(total), 'numerical-failure', 'nominal-total-range');
    const beta = Math.sqrt(total / mg);
    need(positive(beta), 'numerical-failure', 'source-scale-range');
    copied.push({id, state: owned});
  }
  copied.sort((a, b) => a.id - b.id);
  return copied;
}
function validateBuild(q, n, poll) {
  need(q.n === n && q.S0.length === n && q.nominal.length === n,
    'internal-failure', 'builder-shape');
  need(q.offsets.length === 4 * n + 1 && q.src.length === q.kv.length &&
    q.aa !== null && q.aa.length === q.kv.length,
    'internal-failure', 'coefficient-shape');
  need(q.kv.length <= POSITIVE_TERM_CAP, 'resource-failure', 'positive-term-limit');
  need(q.offsets[0] === 0 && q.offsets[4 * n] === q.kv.length,
    'internal-failure', 'coefficient-offsets');
  for (let i = 0; i < n; i++) {
    need(positive(q.S0[i]), 'numerical-failure', 'prepared-total-range');
    need(q.nominal[i].length === 4 && q.nominal[i].every(positive),
      'numerical-failure', 'prepared-force-range');
  }
  for (let row = 0; row < 4 * n; row++) {
    poll();
    const start = q.offsets[row], end = q.offsets[row + 1];
    need(start <= end && end <= q.kv.length, 'internal-failure', 'coefficient-offsets');
    let previous = -1;
    for (let z = start; z < end; z++) {
      const source = q.src[z];
      need(source < n && source !== Math.floor(row / 4) && source > previous,
        'internal-failure', 'source-order'); previous = source;
      need(positive(q.kv[z]) && positive(q.aa[z]),
        'numerical-failure', 'coefficient-range');
    }
  }
  need(q.admission.admitted, 'domain-refused', 'native-admission');
  need(q.graph.descendingEligible, 'domain-refused', 'native-graph-order');
}
function validateMap(value, q, label, poll) {
  const n = q.n;
  need(value.y.length === n && value.rotors.length === n,
    'internal-failure', label + '-shape');
  for (let i = 0; i < n; i++) {
    poll();
    need(positive(value.y[i]) && value.y[i] <= 1,
      'numerical-failure', label + '-y-range');
    need(value.rotors[i].length === 4, 'internal-failure', label + '-rotor-shape');
    for (let r = 0; r < 4; r++) {
      const rotor = value.rotors[i][r];
      need(finite(rotor.alpha) && rotor.alpha >= 0,
        'numerical-failure', label + '-alpha-range');
      need(positive(rotor.x) && rotor.x <= 1,
        'numerical-failure', label + '-x-range');
      need(positive(rotor.T) && rotor.T <= q.nominal[i][r],
        'numerical-failure', label + '-force-range');
    }
  }
}
function cross(a, b) {
  return [a[1] * b[2] - a[2] * b[1],
    a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
}
function prepareEvidence(raw, q, poll) {
  const prepared = [];
  for (let i = 0; i < raw.length; i++) {
    poll();
    const id = raw[i].id, base = 28 * i;
    const center = Array.from(q.p.subarray(base, base + 3));
    const axis = Array.from(q.p.subarray(base + 4, base + 7));
    const offsets = [], points = [], nu = [];
    for (let r = 0; r < 4; r++) {
      const start = base + 8 + 4 * r;
      const offset = Array.from(q.p.subarray(start, start + 3)); offsets.push(offset);
      points.push(center.map((value, k) => value + offset[k]));
      nu.push(Math.sqrt(q.nominal[i][r] / (2 * rho * A)));
    }
    prepared.push({id, center, axis, offsets, points, forces: q.nominal[i].slice(),
      nativeTotal: q.S0[i], nativeBeta: Math.sqrt(q.S0[i] / mg), nativeNu: nu});
  }
  return prepared;
}
function materializeLoads(raw, prepared, solution, poll) {
  const loads = [], solved = [];
  for (let i = 0; i < raw.length; i++) {
    poll();
    const {id, center, axis, offsets, points, nativeNu} = prepared[i];
    const rotor = []; let collective = 0; const worldMoment = [0, 0, 0];
    for (let r = 0; r < 4; r++) {
      // T is the actual native product produced by the unchanged nodeMap.
      const force = solution.rotors[i][r].T; rotor.push(force); collective += force;
      const lever = cross(offsets[r], axis);
      for (let k = 0; k < 3; k++) worldMoment[k] += lever[k] * force;
    }
    const worldForce = axis.map(value => value * collective);
    need([...center, ...axis, ...offsets.flat(), ...points.flat()].every(finite),
      'numerical-failure', 'prepared-geometry-range');
    need(nativeNu.every(positive) && positive(collective) &&
      [...rotor, ...worldForce, ...worldMoment].every(finite),
      'numerical-failure', 'delivered-load-range');
    loads.push({id, rotor, collective, worldForce, worldMoment});
    solved.push({id, y: solution.y[i], rotors: solution.rotors[i]});
  }
  return {loads, solution: solved};
}
function consumeLoads(loads, poll) {
  // Consume every delivered output word without a floating sum that could
  // overflow on otherwise finite loads. This is a checksum, not an audit hash.
  const scratch = new DataView(new ArrayBuffer(8));
  let hash = 2166136261, loadWords = 0, identityWords = 0;
  const status = 'native-success';
  for (let i = 0; i < status.length; i++) hash = Math.imul(hash ^ status.charCodeAt(i), 16777619) >>> 0;
  function word(value) {
    scratch.setFloat64(0, value, false);
    hash = Math.imul(hash ^ scratch.getUint32(0, false), 16777619) >>> 0;
    hash = Math.imul(hash ^ scratch.getUint32(4, false), 16777619) >>> 0;
  }
  for (const load of loads) {
    poll();
    // Every safe-integer ID has an exact binary64 encoding. Mix it before its
    // associated load words so changing the ID association changes this input.
    word(load.id); identityWords++;
    const values = [...load.rotor, load.collective, ...load.worldForce, ...load.worldMoment];
    for (const value of values) {
      word(value); loadWords++;
    }
  }
  return {kind: 'native-load-id-status-fnv32', status, loadWords, identityWords,
    statusCharacters: status.length, value: hash};
}
function query(input, method = 'F', guard = () => {}) {
  const begin = performance.now(), phasesMs = {}; let phaseStart = begin;
  let raw = null, q = null, prepared = null, solution = null, output = null, stage = 'input';
  function phase(name) { const now = performance.now(); phasesMs[name] = now - phaseStart; phaseStart = now; }
  function poll() {
    try { guard(); } catch (_) { throw new Refusal('resource-failure', 'cooperative-guard'); }
  }
  const base = {schema: 'm31-native-load-result-v1',
    model: 'ordinary-binary64-full-contribution', method: typeof method === 'string' ? method : null,
    status: null, reason: null, constants: CONSTANTS};
  try {
    need(method === 'F' || method === 'L', 'input-refused', 'method');
    need(typeof guard === 'function', 'input-refused', 'guard-type'); poll();
    raw = captureInput(input, poll); phase('input'); stage = 'build';
    const states = raw.map(item => item.state);
    q = K.build(states, method === 'F' ? 'screen' : 'lean', false, poll);
    prepared = prepareEvidence(raw, q, poll);
    validateBuild(q, raw.length, poll); phase('buildAndAdmission'); stage = 'schedule';
    const order = K.schedule(q); phase('schedule'); stage = 'solve';
    solution = K.solve(q, 'O', order, false, poll); validateMap(solution, q, 'solution', poll);
    phase('solve'); stage = 'residual';
    const residual = K.residual(q, solution, poll);
    validateMap(residual.residualMap, q, 'residual', poll);
    need(finite(residual.residualLog) && residual.residualLog >= 0 &&
      finite(residual.sourceReceiverMismatch) && residual.sourceReceiverMismatch >= 0,
      'numerical-failure', 'residual-range');
    need(residual.residualLog <= RESIDUAL_LOG_LIMIT &&
      residual.sourceReceiverMismatch <= SOURCE_RECEIVER_LIMIT,
      'numerical-failure', 'residual-limit');
    phase('residual'); stage = 'loads';
    const delivered = materializeLoads(raw, prepared, solution, poll); phase('loads');
    stage = 'consumption'; const consumption = consumeLoads(delivered.loads, poll); phase('consumption');
    output = {...base, status: 'native-success', raw, ids: raw.map(item => item.id),
      prepared, ...delivered, coefficients: {offsets: q.offsets, sourceIndices: q.src, K: q.kv, a: q.aa},
      diagnostics: {admission: q.admission, input: q.input, graph: q.graph,
        symbolCounts: q.symbolCounts, screen: q.screen ?? null,
        geometryWork: q.geometryWork, buildPhasesMs: q.phasesMs,
        ordinaryLmax: q.ordinaryLmax, scheduleIndices: order,
        solveWork: solution.work, residualWork: residual.residualWork,
        residualLog: residual.residualLog, sourceReceiverMismatch: residual.sourceReceiverMismatch},
      consumption};
  } catch (error) {
    let status = 'internal-failure', reason = 'unexpected-exception';
    if (error instanceof Refusal) { status = error.status; reason = error.reason; }
    else if (error instanceof Error && error.message === 'positive coefficient guard exceeded') {
      status = 'resource-failure'; reason = 'positive-term-limit';
    } else if (error instanceof Error && error.message === 'invalid alpha') {
      status = 'numerical-failure'; reason = 'native-alpha-range';
    } else if (error instanceof RangeError) { status = 'resource-failure'; reason = 'native-range-error'; }
    output = {...base, status, reason, stage, raw, prepared,
      coefficients: q ? {offsets: q.offsets, sourceIndices: q.src, K: q.kv, a: q.aa} : null,
      ids: raw ? raw.map(item => item.id) : null,
      diagnostics: q ? {admission: q.admission, input: q.input, graph: q.graph,
        symbolCounts: q.symbolCounts, screen: q.screen ?? null, geometryWork: q.geometryWork} : null};
  }
  // This timestamp follows final result assembly and all required output work.
  const end = performance.now();
  phasesMs.finalization = end - phaseStart;
  output.timing = {clock: 'performance.now', totalMs: end - begin, phasesMs,
    boundary: 'raw current input through validation, copying, canonical ID order, native build/admission, ordered solve, residual, four loads, evidence fields and complete load-word/ID/status consumption'};
  return output;
}

function encodeEvidence(result) {
  // Explicitly outside query timing. No reference/oracle input is accepted.
  const scratch = new DataView(new ArrayBuffer(8));
  function word(value) {
    if (typeof value !== 'number') throw new TypeError('word requires number');
    scratch.setFloat64(0, value, false);
    return scratch.getUint32(0, false).toString(16).padStart(8, '0') +
      scratch.getUint32(4, false).toString(16).padStart(8, '0');
  }
  const vector = values => Array.from(values, word);
  function safe(value) {
    if (typeof value === 'number') return Number.isFinite(value) ? value : {nonfiniteWord: word(value)};
    if (Array.isArray(value)) return value.map(safe);
    if (value !== null && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, safe(item)]));
    return value;
  }
  const out = {schema: 'm31-native-load-evidence-v1', model: result.model,
    status: result.status, reason: result.reason, method: result.method, ids: result.ids,
    constants: Object.fromEntries(Object.entries(result.constants).map(([key, value]) => [key, word(value)])),
    raw: result.raw ? result.raw.map(item => ({id: item.id, state: vector(item.state)})) : null,
    diagnostics: safe(result.diagnostics), timing: safe(result.timing)};
  out.prepared = result.prepared ? result.prepared.map(item => ({id: item.id, center: vector(item.center),
    axis: vector(item.axis), offsets: item.offsets.map(vector), points: item.points.map(vector),
    forces: vector(item.forces), nativeTotal: word(item.nativeTotal),
    nativeBeta: word(item.nativeBeta), nativeNu: vector(item.nativeNu)})) : null;
  out.coefficients = result.coefficients ? {offsets: Array.from(result.coefficients.offsets),
    sourceIndices: Array.from(result.coefficients.sourceIndices),
    K: vector(result.coefficients.K), a: result.coefficients.a ? vector(result.coefficients.a) : null} : null;
  if (result.status !== 'native-success') { out.stage = result.stage; return out; }
  out.solution = result.solution.map(item => ({id: item.id, y: word(item.y),
    rotors: item.rotors.map(rotor => ({alpha: word(rotor.alpha), x: word(rotor.x), T: word(rotor.T)}))}));
  out.loads = result.loads.map(item => ({id: item.id, rotor: vector(item.rotor),
    collective: word(item.collective), worldForce: vector(item.worldForce), worldMoment: vector(item.worldMoment)}));
  out.consumption = result.consumption;
  return out;
}

module.exports = {query, encodeEvidence, limits: Object.freeze({maxN: MAX_N,
  positiveTermCap: POSITIVE_TERM_CAP, residualLogLimit: RESIDUAL_LOG_LIMIT,
  sourceReceiverLimit: SOURCE_RECEIVER_LIMIT})};

},
"./vendor/generation/step02c-source/physics.cjs":function(module,exports,require,Buffer,process){
/* Original 6-DOF rigid-body simulator. World/body +z up, quaternion [x,y,z,w]. */
(function(root){'use strict';
const P=Object.freeze({m:.027,g:9.81,I:[1.4e-5,1.4e-5,2.17e-5],a:.028,kf:3.16e-10,km:7.94e-12,motorTau:.04,controlDt:.01,tiltMax:Math.PI/12,duration:16});
const rotors=[[P.a,P.a,1],[-P.a,P.a,-1],[-P.a,-P.a,1],[P.a,-P.a,-1]];
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x)),add=(a,b)=>a.map((x,i)=>x+b[i]),scale=(a,k)=>a.map(x=>x*k),dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],norm=a=>Math.hypot(...a),unit=a=>scale(a,1/norm(a));
function qmul(a,b){const v=add(add(scale(b.slice(0,3),a[3]),scale(a.slice(0,3),b[3])),cross(a,b));return [...v,a[3]*b[3]-dot(a.slice(0,3),b.slice(0,3))];}
function rotate(q,v){const t=scale(cross(q,v),2);return add(v,add(scale(t,q[3]),cross(q,t)));}
function quaternionFromBasis(x,y,z){const m=[x[0],y[0],z[0],x[1],y[1],z[1],x[2],y[2],z[2]],tr=m[0]+m[4]+m[8];let q;
 if(tr>0){const s=Math.sqrt(tr+1)*2;q=[(m[7]-m[5])/s,(m[2]-m[6])/s,(m[3]-m[1])/s,s/4];}
 else if(m[0]>m[4]&&m[0]>m[8]){const s=Math.sqrt(1+m[0]-m[4]-m[8])*2;q=[s/4,(m[1]+m[3])/s,(m[2]+m[6])/s,(m[7]-m[5])/s];}
 else if(m[4]>m[8]){const s=Math.sqrt(1+m[4]-m[0]-m[8])*2;q=[(m[1]+m[3])/s,s/4,(m[5]+m[7])/s,(m[2]-m[6])/s];}
 else{const s=Math.sqrt(1+m[8]-m[0]-m[4])*2;q=[(m[2]+m[6])/s,(m[5]+m[7])/s,s/4,(m[3]-m[1])/s];}return unit(q);
}
function euler(q){const [x,y,z,w]=q;return [Math.atan2(2*(w*x+y*z),1-2*(x*x+y*y)),Math.asin(clamp(2*(w*y-z*x),-1,1)),Math.atan2(2*(w*z+x*y),1-2*(y*y+z*z))];}
function wrench(f){let T=0,t=[0,0,0];f.forEach((v,i)=>{const [x,y,s]=rotors[i];T+=v;t[0]+=y*v;t[1]-=x*v;t[2]+=s*P.km/P.kf*v;});return {T,t};}
function mix(T,t,ratio){const k=P.km/P.kf,raw=rotors.map(([x,y,s])=>T/4+y*t[0]/(4*P.a**2)-x*t[1]/(4*P.a**2)+s*t[2]/(4*k)),max=ratio*P.m*P.g/4;return {u:raw.map(f=>clamp(f,0,max)),saturated:raw.some(f=>f<0||f>max)};}
// State p[0:3], v[3:6], q[6:10], body omega[10:13], motor thrusts[13:17].
function derivative(y,u,external=[0,0,0]){const q=y.slice(6,10),w=y.slice(10,13),{T,t}=wrench(y.slice(13)),F=rotate(q,[0,0,T/P.m]),gyro=cross(w,w.map((v,i)=>v*P.I[i])),dq=scale(qmul(q,[...w,0]),.5);return [...y.slice(3,6),F[0]+external[0]/P.m,F[1]+external[1]/P.m,F[2]-P.g+external[2]/P.m,...dq,...t.map((v,i)=>(v-gyro[i])/P.I[i]),...u.map((v,i)=>(v-y[13+i])/P.motorTau)];}
function integrate(y,u,h,external=[0,0,0]){const next=(k,s)=>y.map((v,i)=>v+s*k[i]),k1=derivative(y,u,external),k2=derivative(next(k1,h/2),u,external),k3=derivative(next(k2,h/2),u,external),k4=derivative(next(k3,h),u,external);const out=y.map((v,i)=>v+h*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6),q=unit(out.slice(6,10));out.splice(6,4,...q);return out;}
function target(t,scenario){let vx=0,vy=0,z=1,yaw=0,phase='Hover';
 if(scenario==='move'){if(t>=2&&t<6){vx=.5;phase='Move along X';}else if(t>=6)phase='Brake and hold';}
 if(scenario==='climb'&&t>=2){z=3;phase='Climb request';}
 if(scenario==='yaw'&&t>=2){yaw=Math.PI/2;phase='Turn 90°';}
 if(scenario==='flight'){if(t>=2&&t<5){vx=.5;phase='Move along X';}else if(t>=5&&t<8){vy=.5;phase='Move along Y';}else if(t>=8){z=1.8;phase=t<11?'Climb and brake':'Turn 90°';if(t>=11)yaw=Math.PI/2;}}
 return {vx,vy,z,yaw,phase};}
function control(y,r,ratio){const a=[2.5*(r.vx-y[3]),2.5*(r.vy-y[4]),P.g+clamp(6*(r.z-y[2])-4*y[5],-4,5)];const xy=Math.hypot(a[0],a[1]),limit=a[2]*Math.tan(P.tiltMax);if(xy>limit){a[0]*=limit/xy;a[1]*=limit/xy;}
 const bz=unit(a),heading=[Math.cos(r.yaw),Math.sin(r.yaw),0],by=unit(cross(bz,heading)),bx=cross(by,bz),qd=quaternionFromBasis(bx,by,bz),q=y.slice(6,10),err=qmul([-q[0],-q[1],-q[2],q[3]],qd),sign=err[3]<0?-1:1,w=y.slice(10,13),gyro=cross(w,w.map((v,i)=>v*P.I[i]));
 const torque=w.map((v,i)=>P.I[i]*(100*2*sign*err[i]-20*v)+gyro[i]);
 const axis=rotate(q,[0,0,1]),T=P.m*a[2]/Math.max(.5,axis[2]);return {...mix(T,torque,ratio),qd};}
class Simulation{constructor({scenario='flight',ratio=2.25,dt=.005,load=0}={}){if(!Number.isFinite(load)||load<0||load>.3)throw Error('Invalid load');if(!['flight','move','climb','hover','yaw'].includes(scenario)||ratio<1.1||ratio>2.25||dt<=0||Math.abs(P.controlDt/dt-Math.round(P.controlDt/dt))>1e-8)throw Error('Invalid configuration');this.load=load;this.scenario=scenario;this.ratio=ratio;this.dt=dt;this.n=0;this.t=0;this.y=[0,0,1,0,0,0,0,0,0,1,0,0,0,...Array(4).fill(P.m*P.g/4)];this.c=control(this.y,target(0,scenario),ratio);this.satTime=0;this.history=[this.sample()];}
 force(){return this.t>=4&&this.t<8?[0,0,-this.load*P.m*P.g]:[0,0,0];}
 sample(){const r=target(this.t,this.scenario),e=euler(this.y.slice(6,10));return {externalFz:this.force()[2],t:this.t,x:this.y[0],y:this.y[1],z:this.y[2],vx:this.y[3],vy:this.y[4],vz:this.y[5],qx:this.y[6],qy:this.y[7],qz:this.y[8],qw:this.y[9],roll:e[0],pitch:e[1],yaw:e[2],wx:this.y[10],wy:this.y[11],wz:this.y[12],f1:this.y[13],f2:this.y[14],f3:this.y[15],f4:this.y[16],thrust:this.y.slice(13).reduce((a,b)=>a+b,0),targetVx:r.vx,targetVy:r.vy,targetZ:r.z,targetYaw:r.yaw,phase:this.load>0?(this.t<4?'Before the push':this.t<8?'Downward push':'Recovery'):r.phase,saturated:this.c.saturated};}
 step(){if(this.t>=P.duration-1e-9)return false;if(this.n%Math.round(P.controlDt/this.dt)===0)this.c=control(this.y,target(this.t,this.scenario),this.ratio);if(this.c.saturated)this.satTime+=this.dt;this.y=integrate(this.y,this.c.u,this.dt,this.force());this.n++;this.t=this.n*this.dt;this.history.push(this.sample());return true;}
 run(){while(this.step());return this;}
 metrics(){const h=this.history;return {finalPosition:this.y.slice(0,3),finalSpeed:norm(this.y.slice(3,6)),finalEulerDeg:euler(this.y.slice(6,10)).map(x=>x*180/Math.PI),maxThrustWeight:Math.max(...h.map(s=>s.thrust/(P.m*P.g))),saturationFraction:this.satTime/P.duration,maxQuaternionNormError:Math.max(...h.map(s=>Math.abs(Math.hypot(s.qx,s.qy,s.qz,s.qw)-1)))};}
}
const api={P,rotors,Simulation,derivative,integrate,control,mix,wrench,target,qmul,rotate,euler,quaternionFromBasis};if(typeof module!=='undefined')module.exports=api;else root.Drone3D=api;
})(typeof globalThis!=='undefined'?globalThis:this);

},
"./vendor/generation/milestone-31-source/sim.cjs":function(module,exports,require,Buffer,process){
'use strict';
const F=require('../step02c-source/physics.cjs'),{Grid}=require('./grid.cjs'),G=require('./geometry.cjs'),course=require('./factory.cjs');
const {repair,residual}=require('./wall-filter.cjs');
const P=Object.freeze({neighbor:1.8,fade:1.3,separationRadius:.85,separation:1.5,alignment:2,cohesion:.22,cruise:.65,forward:.55,maxSpeed:.9,steeringHorizon:.4,bodyRadius:.075,margin:.3,pairMargin:.38,filterHorizon:1.2,iterations:6,spacing:.75,jitter:.08,controlDt:.01});
const norm=a=>Math.hypot(...a),cap=(x,l,h)=>Math.max(l,Math.min(h,x)),smooth=(a,b,x)=>{const t=cap((x-a)/(b-a),0,1);return t*t*(3-2*t)},limit=v=>{const n=norm(v);return v.map(x=>x*Math.min(1,P.maxSpeed/Math.max(n,1e-12)))};
function rng(seed){let x=seed>>>0;return()=>((x=(1664525*x+1013904223)>>>0)/4294967296);}
function initial(seed,count){const random=rng(seed),side=Math.ceil(Math.cbrt(count)),ny=Math.min(16,side),nz=Math.min(9,side),nx=Math.ceil(count/(ny*nz)),sites=[];for(let x=0;x<nx;x++)for(let y=0;y<ny;y++)for(let z=0;z<nz;z++)sites.push([-6-x*P.spacing,(y-(ny-1)/2)*P.spacing,4.5+(z-(nz-1)/2)*P.spacing]);for(let i=sites.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[sites[i],sites[j]]=[sites[j],sites[i]];}return sites.slice(0,count).map(p=>{const pos=p.map(x=>x+(random()*2-1)*P.jitter),v=[random()-.5,random()-.5,random()-.5],n=norm(v),vel=v.map(x=>.2*x/n),yaw=Math.atan2(vel[1],vel[0]);return [...pos,...vel,0,0,Math.sin(yaw/2),Math.cos(yaw/2),0,0,0,...Array(4).fill(F.P.m*F.P.g/4)];});}
function routeTarget(x){const r=course.route;if(x<=r[0][0])return r[0].slice();for(let i=0;i<r.length-1;i++){const a=r[i],b=r[i+1];if(x<=b[0]){const w=smooth(a[0],b[0],x);return [x,a[1]+w*(b[1]-a[1]),a[2]+w*(b[2]-a[2])];}}return [x,0,4];}
function steer(i,states,ids,mode='boids',filter='baseline',diagnostic=null){
 const s=states[i],v=s.slice(3,6),speed=norm(v),a=v.map(x=>1.2*(P.cruise-speed)*x/Math.max(speed,.01)),sep=[0,0,0],social=[0,0,0];let weight=0;
 for(const j of ids){const q=states[j],dvec=q.slice(0,3).map((x,k)=>x-s[k]),d=norm(dvec),w=1-smooth(P.fade,P.neighbor,d);weight+=w;for(let k=0;k<3;k++){social[k]+=w*(P.alignment*(q[3+k]-v[k])+P.cohesion*dvec[k]);if(d<P.separationRadius&&d>1e-9)sep[k]-=P.separation*(1/d-1/P.separationRadius)*dvec[k]/d;}}
 if(mode!=='goal-only')for(let k=0;k<3;k++)a[k]+=sep[k];if(mode==='boids')for(let k=0;k<3;k++)a[k]+=social[k]/Math.max(1,weight);
 const target=routeTarget(s[0]+.8),errors=[target[1]-s[1],target[2]-s[2]],outside=errors.map(e=>Math.sign(e)*Math.max(0,Math.abs(e)-.55)),desired=[P.forward,cap(.8*outside[0],-.6,.6),cap(.8*outside[1],-.6,.6)];
 // Shared broad route field. No per-drone waypoint assignments, slots or leader.
 desired[0]*=1/(1+.15*(outside[0]**2+outside[1]**2));
 for(let k=0;k<3;k++)a[k]+=1.3*(desired[k]-v[k]);let out=limit(v.map((x,k)=>x+P.steeringHorizon*a[k]));
 const constraints=[];for(const box of course.boxes){const reach=1.6+P.bodyRadius+1e-10;if(s[0]<box.min[0]-reach||s[0]>box.max[0]+reach||s[1]<box.min[1]-reach||s[1]>box.max[1]+reach||s[2]<box.min[2]-reach||s[2]>box.max[2]+reach)continue;const q=G.boxDistance(s,box),clear=q.distance-P.bodyRadius;if(clear<1.6)constraints.push({obstacle:box.id,n:q.normal,lower:-(clear-P.margin)/P.filterHorizon});}
 const walls=constraints.slice();
 // Same pair-avoidance filter in every social ablation: comparisons isolate Boids forces.
 for(const j of ids){const q=states[j],delta=s.slice(0,3).map((x,k)=>x-q[k]),d=norm(delta);if(d<1.5&&d>1e-9){const n=delta.map(x=>x/d);constraints.push({neighbor:j,n,lower:q.slice(3,6).reduce((z,x,k)=>z+x*n[k],0)-(d-P.pairMargin)/P.filterHorizon});}}
 for(let it=0;it<P.iterations;it++){for(const c of constraints){const radial=out.reduce((z,x,k)=>z+x*c.n[k],0);if(radial<c.lower)out=out.map((x,k)=>x+(c.lower-radial)*c.n[k]);}out=limit(out);}
 const before=out.slice(),repaired=filter==='wall-priority'?repair(out,walls,P.maxSpeed):null;
 if(repaired)out=repaired.velocity;
 if(diagnostic)diagnostic({velocity:out.slice(),actual:v,walls,pairs:constraints.slice(walls.length),beforeWallResidual:residual(before,walls,P.maxSpeed),wallResidual:residual(out,walls,P.maxSpeed),pairResidual:residual(out,constraints.slice(walls.length),P.maxSpeed),iterations:repaired?.iterations||0,converged:repaired?.converged??null});
 return out;
}
function measure(states){const n=states.length,grid=new Grid(states,P.neighbor),parent=Array.from({length:n},(_,i)=>i),size=Array(n).fill(1),find=i=>{while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i];}return i;};let minSep=P.neighbor,largest=1,edges=0;
 for(let i=0;i<n;i++)for(const j of grid.neighbors(i,P.neighbor)){if(j<=i)continue;edges++;minSep=Math.min(minSep,norm(states[i].slice(0,3).map((x,k)=>x-states[j][k])));const a=find(i),b=find(j);if(a!==b){parent[b]=a;size[a]+=size[b];largest=Math.max(largest,size[a]);}}
 const center=[0,1,2].map(k=>states.reduce((z,s)=>z+s[k],0)/n),order=norm([0,1,2].map(k=>states.reduce((z,s)=>z+s[k+3]/Math.max(1e-9,norm(s.slice(3,6))),0)/n)),heights=states.map(s=>s[2]);let minObstacle=Infinity;for(const s of states)for(const b of course.boxes)minObstacle=Math.min(minObstacle,G.boxDistance(s,b).distance-P.bodyRadius);
 return {center,order,largestFraction:largest/n,components:new Set(parent.map((_,i)=>find(i))).size,heightSpan:Math.max(...heights)-Math.min(...heights),rmsRadius:Math.sqrt(states.reduce((z,s)=>z+norm(s.slice(0,3).map((x,k)=>x-center[k]))**2,0)/n),minimumSeparationCappedAtRadius:minSep,minimumObstacleClearance:minObstacle,meanNeighborCount:2*edges/n};
}
function contactCandidates(old,next){const maxMove=Math.max(...old.map((s,i)=>norm(s.slice(0,3).map((x,k)=>x-next[i][k])))),radius=2*P.bodyRadius+2*maxMove+1e-10,grid=new Grid(old,.4),out=[];for(let i=0;i<old.length;i++)for(const j of grid.neighbors(i,radius))if(j>i)out.push([i,j]);return out;}
function obstacleContacts(a,b){const lo=[0,1,2].map(k=>Math.min(a[k],b[k])-P.bodyRadius),hi=[0,1,2].map(k=>Math.max(a[k],b[k])+P.bodyRadius),out=[];for(const box of course.boxes){if([0,1,2].some(k=>hi[k]<box.min[k]||lo[k]>box.max[k]))continue;const clearance=G.segmentBoxDistance(a.slice(0,3),b.slice(0,3),box)-P.bodyRadius;if(clearance<0)out.push({id:box.id,clearance});}return out;}
function run({seed=1301,count=50,mode='boids',dt=.005,duration=120,record=true,search='grid',frameEvery=1,frameSink=null,progress=null,filter='baseline'}={}){
 if(!['baseline','wall-priority'].includes(filter))throw Error('Invalid filter');
 if(!Number.isInteger(count)||count<2||count>5000||!['boids','separation-only','goal-only'].includes(mode)||!['grid','brute'].includes(search)||![.005,.0025,.00125].includes(dt)||!(duration>0))throw Error('Invalid configuration');
 if(!(frameEvery>=.1)||Math.abs(frameEvery/.1-Math.round(frameEvery/.1))>1e-8)throw Error('Frame cadence must be a positive multiple of0.1s');
 const started=performance.now(),timing={steering:0,physics:0,safety:0,measurement:0};let states=initial(seed,count),start=states.map(s=>s.slice()),controls,frames=[],samples=[],end=0,stopReason=null,failure=null,crossings=Array(count).fill(null),maxTilt=0,saturation=0,neighborChecks=0;
 const diagnostics={updates:0,wallViolationsBefore:0,wallViolationsAfter:0,pairViolationsAfter:0,maxWallBefore:0,maxWallAfter:0,maxPairAfter:0,unconverged:0,maxIterations:0};let lastCommands=[],lastControlTime=0;
 timing.initialization=performance.now()-started;
 function sample(t){const at=performance.now();samples.push({t,passed:crossings.filter(x=>x!==null).length,...measure(states)});if(record&&(Math.abs(t/frameEvery-Math.round(t/frameEvery))<1e-8||stopReason||Math.abs(t-duration)<1e-8)){const frame=[t,...states.flatMap(s=>[...s.slice(0,3),...s.slice(6,10)])];if(frameSink)frameSink(frame);else frames.push(frame);}if(progress&&(Math.abs(t/5-Math.round(t/5))<1e-8||stopReason))progress({t,passed:crossings.filter(x=>x!==null).length,stopReason,wallMs:performance.now()-started},states);timing.measurement+=performance.now()-at;}sample(0);
 for(let step=0;step<Math.round(duration/dt);step++){
  if(step%Math.round(P.controlDt/dt)===0){const at=performance.now(),grid=search==='grid'?new Grid(states,P.neighbor):null;controls=states.map((s,i)=>{const ids=grid?grid.neighbors(i,P.neighbor):states.map((_,j)=>j).filter(j=>j!==i&&norm(s.slice(0,3).map((x,k)=>x-states[j][k]))<P.neighbor);neighborChecks+=ids.length;const v=steer(i,states,ids,mode,filter,d=>{lastCommands[i]={...d,state:s};diagnostics.updates++;diagnostics.wallViolationsBefore+=d.beforeWallResidual>1e-7;diagnostics.wallViolationsAfter+=d.wallResidual>1e-7;diagnostics.pairViolationsAfter+=d.pairResidual>1e-7;diagnostics.maxWallBefore=Math.max(diagnostics.maxWallBefore,d.beforeWallResidual);diagnostics.maxWallAfter=Math.max(diagnostics.maxWallAfter,d.wallResidual);diagnostics.maxPairAfter=Math.max(diagnostics.maxPairAfter,d.pairResidual);diagnostics.unconverged+=d.converged===false;diagnostics.maxIterations=Math.max(diagnostics.maxIterations,d.iterations);});lastControlTime=step*dt;return F.control(s,{vx:v[0],vy:v[1],z:s[2]+(2.5*v[2]+1.5*s[5])/6,yaw:Math.atan2(v[1],v[0])},2.25);});timing.steering+=performance.now()-at;}
  const old=states,at=performance.now();states=states.map((s,i)=>{if(controls[i].saturated)saturation+=dt;return F.integrate(s,controls[i].u,dt);});timing.physics+=performance.now()-at;end=(step+1)*dt;const st=performance.now();
  for(let i=0;i<count;i++){const s=states[i];if(!s.every(Number.isFinite)||s[2]<P.bodyRadius){stopReason='vehicle model limit';failure={drone:i};break;}maxTilt=Math.max(maxTilt,...F.euler(s.slice(6,10)).slice(0,2).map(Math.abs));const hits=obstacleContacts(old[i],s);if(hits.length){stopReason='obstacle contact envelope';failure={drone:i,hits};break;}if(crossings[i]===null&&old[i][0]<course.finish&&s[0]>=course.finish)crossings[i]=end;}
  if(!stopReason)for(const [i,j] of contactCandidates(old,states)){const d=G.segmentPair(old[i],states[i],old[j],states[j]);if(d<2*P.bodyRadius){stopReason='drone contact envelope';failure={pair:[i,j],distance:d};break;}}
  timing.safety+=performance.now()-st;if(stopReason||(step+1)%Math.round(.1/dt)===0)sample(+end.toFixed(6));if(stopReason)break;
 }
 if(samples.at(-1).t!==+end.toFixed(6))sample(+end.toFixed(6));
 return {diagnostics,lastControl:{t:lastControlTime,affected:(failure?.pair||[failure?.drone]).filter(i=>i!==undefined).map(i=>({drone:i,...lastCommands[i],actuator:controls[i]}))},config:{filter,seed,count,mode,dt,duration,search,course:course.id,airflow:'off',observation:'ideal'},initial:start,final:states,crossings,metrics:{passed:crossings.filter(x=>x!==null).length,end,stopReason,failure,minimumSampledSeparation:Math.min(...samples.map(s=>s.minimumSeparationCappedAtRadius)),minimumSampledObstacleClearance:Math.min(...samples.map(s=>s.minimumObstacleClearance)),minimumConnectedFraction:Math.min(...samples.map(s=>s.largestFraction)),final:samples.at(-1),maxTiltDegrees:maxTilt*180/Math.PI,saturationFraction:saturation/(count*end)},timing:{...timing,total:performance.now()-started,unit:'ms',scope:'Node wall time, includes sampling/recording and initialization; excludes external JSON serialization and rendering; no deliberate UI yields.'},neighborVisits:neighborChecks,samples,...(record&&!frameSink?{frames}:{}),recording:{cadence:frameEvery,streamed:!!frameSink}};
}
module.exports={P,initial,routeTarget,steer,measure,contactCandidates,obstacleContacts,run,course};if(require.main===module)console.log(JSON.stringify(run(JSON.parse(process.argv[2]||'{}'))));

},
"./vendor/generation/milestone-31-source/grid.cjs":function(module,exports,require,Buffer,process){
'use strict';
class Grid{
 constructor(states,cell=1.8){if(!(cell>0))throw Error('Positive cell size required');this.states=states;this.cell=cell;this.cells=new Map();for(let i=0;i<states.length;i++){const p=states[i],key=this.key(...p.slice(0,3).map(x=>Math.floor(x/cell)));if(!this.cells.has(key))this.cells.set(key,[]);this.cells.get(key).push(i);}}
 key(x,y,z){return x+','+y+','+z;}
 candidates(p,r){const c=this.cell,lo=p.slice(0,3).map(x=>Math.floor((x-r)/c)),hi=p.slice(0,3).map(x=>Math.floor((x+r)/c)),out=[];for(let x=lo[0];x<=hi[0];x++)for(let y=lo[1];y<=hi[1];y++)for(let z=lo[2];z<=hi[2];z++){const ids=this.cells.get(this.key(x,y,z));if(ids)out.push(...ids);}return out.sort((a,b)=>a-b);}
 neighbors(i,r){const p=this.states[i];return this.candidates(p,r).filter(j=>j!==i&&Math.hypot(p[0]-this.states[j][0],p[1]-this.states[j][1],p[2]-this.states[j][2])<r);}
}
module.exports={Grid};

},
"./vendor/generation/milestone-31-source/geometry.cjs":function(module,exports,require,Buffer,process){
'use strict';
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
function boxDistance(p,b){const d=p.map((x,k)=>x< b.min[k]?x-b.min[k]:x>b.max[k]?x-b.max[k]:0),n=Math.hypot(...d);if(n>0)return {distance:n,normal:d.map(x=>x/n)};
 let best=Infinity,normal=[0,0,0];for(let k=0;k<3;k++)for(const sign of [-1,1]){const distance=sign<0?p[k]-b.min[k]:b.max[k]-p[k];if(distance<best){best=distance;normal=[0,0,0];normal[k]=sign;}}return {distance:-best,normal};}
// Exact Euclidean distance from a straight segment to an axis-aligned solid box.
function segmentBoxDistance(a,b,box){const d=b.map((x,k)=>x-a[k]),cuts=[0,1];for(let k=0;k<3;k++)if(d[k])for(const face of [box.min[k],box.max[k]]){const t=(face-a[k])/d[k];if(t>0&&t<1)cuts.push(t);}cuts.sort((a,b)=>a-b);let best=Infinity;
 for(let j=0;j<cuts.length-1;j++){const lo=cuts[j],hi=cuts[j+1],mid=(lo+hi)/2;let aa=0,ab=0;for(let k=0;k<3;k++){const x=a[k]+mid*d[k];if(x<box.min[k]||x>box.max[k]){const face=x<box.min[k]?box.min[k]:box.max[k],q=a[k]-face;aa+=d[k]*d[k];ab+=q*d[k];}}const t=clamp(aa?-ab/aa:mid,lo,hi),p=a.map((x,k)=>x+t*d[k]);best=Math.min(best,Math.max(0,boxDistance(p,box).distance));}return best;}
function segmentPair(a,b,c,d){const r=a.slice(0,3).map((x,k)=>x-c[k]),v=b.slice(0,3).map((x,k)=>x-a[k]-d[k]+c[k]),vv=v.reduce((s,x)=>s+x*x,0),t=clamp(vv?-r.reduce((s,x,k)=>s+x*v[k],0)/vv:0,0,1);return Math.hypot(...r.map((x,k)=>x+t*v[k]));}
module.exports={boxDistance,segmentBoxDistance,segmentPair};

},
"./vendor/generation/milestone-31-source/factory.cjs":function(module,exports,require,Buffer,process){
'use strict';
const base=require('./factory-wide.cjs');
const variant=process.env.FLOCK_FACTORY_VARIANT||'wide';
if(!['wide','narrow'].includes(variant))throw Error('Unknown factory variant');
if(variant==='wide')module.exports=base;
else {
 const c=JSON.parse(JSON.stringify(base));c.id='factory-narrow-v1';c.name='Three factory halls — narrower openings';
 for(const [i,g] of c.gates.entries()){
  g.width=3;g.height=2.5;const y0=g.y-1.5,y1=g.y+1.5,z0=g.z-1.25,z1=g.z+1.25;
  for(const b of c.boxes.filter(b=>b.id.startsWith('partition-'+i+'-'))){
   if(b.id.endsWith('-left'))b.max[1]=y0;
   if(b.id.endsWith('-right'))b.min[1]=y1;
   if(b.id.endsWith('-below')){b.min[1]=y0;b.max[1]=y1;b.max[2]=z0;}
   if(b.id.endsWith('-above')){b.min[1]=y0;b.max[1]=y1;b.min[2]=z1;}
  }
 }
 c.description+=' Narrow variant changes only the three doorways to3×2.5m.';module.exports=c;
}

},
"./vendor/generation/milestone-31-source/factory-wide.cjs":function(module,exports,require,Buffer,process){
'use strict';
const boxes=[];function box(id,min,max,kind='equipment'){boxes.push({id,min,max,kind});}
box('floor',[-60,-10,-.4],[42,10,0],'shell');box('ceiling',[-14,-10,10],[42,10,10.4],'shell');box('north-wall',[-14,10,0],[42,10.4,10],'shell');box('south-wall',[-14,-10.4,0],[42,-10,10],'shell');
const gates=[{x:0,y:-2,z:4,width:5,height:4},{x:12,y:2,z:5.8,width:5,height:4},{x:24,y:-1,z:3.2,width:5,height:4}];
for(const [i,g] of gates.entries()){const y0=g.y-g.width/2,y1=g.y+g.width/2,z0=g.z-g.height/2,z1=g.z+g.height/2;box('partition-'+i+'-left',[g.x-.18,-10,0],[g.x+.18,y0,10],'partition');box('partition-'+i+'-right',[g.x-.18,y1,0],[g.x+.18,10,10],'partition');box('partition-'+i+'-below',[g.x-.18,y0,0],[g.x+.18,y1,z0],'partition');box('partition-'+i+'-above',[g.x-.18,y0,z1],[g.x+.18,y1,10],'partition');}
for(const x of [3.5,7,15.5,19,27.5,31])for(const side of [-1,1]){const y=side*7;box('rack-'+x+'-'+side,[x-.6,y-1.2,0],[x+.6,y+1.2,7],'rack');}
box('press-A',[4,-.2,0],[6,2.5,4.5]);box('press-B',[16,-4.8,0],[18,-1.8,6]);box('press-C',[28,1.5,0],[30,4.5,5.5]);
box('overhead-A',[6,-5,7.8],[9,5,8.4],'overhead');box('overhead-B',[18,-5,8.3],[21,5,8.9],'overhead');box('loading-platform',[32,-5,0],[34,0,1.2]);
const route=[[-7,-2,4],[1,-2,4],[6,-2.5,5.7],[10,2,5.8],[13,2,5.8],[18,2.5,5.8],[22,-1,3.2],[25,-1,3.2],[30,-1,3.7],[36,0,4]];
module.exports={id:'factory-v1',name:'Three factory halls',units:'metres',boxes,gates,route,finish:36,duration:120,description:'Synthetic factory: thick offset partitions, changing-height doorways, racks, presses and overhead structures. All shown solid boxes are checked. The ceiling and side shell can be visually hidden; their collisions remain active.'};

},
"./vendor/generation/milestone-31-source/wall-filter.cjs":function(module,exports,require,Buffer,process){
'use strict';
const dot=(a,b)=>a.slice(0,3).reduce((z,x,k)=>z+x*b[k],0);
function residual(v,cs,speed){return Math.max(0,Math.hypot(...v)-speed,...cs.map(c=>c.lower-dot(c.n,v)));}
// Dykstra projection onto obstacle halfspaces AND the speed ball. Pair requests
// are deliberately left soft: wall repair can violate them and this is measured.
function repair(preferred,cs,speed=.9,maxIterations=512){
 let x=preferred.slice();const corrections=Array.from({length:cs.length+1},()=>[0,0,0]);
 if(residual(x,cs,speed)<=1e-10)return {velocity:x,iterations:0,converged:true};
 for(let it=1;it<=maxIterations;it++){
  const old=x.slice();
  for(let i=0;i<=cs.length;i++){
   const y=x.map((v,k)=>v+corrections[i][k]);
   if(i===cs.length){const f=Math.min(1,speed/Math.max(1e-30,Math.hypot(...y)));x=y.map(v=>v*f);}
   else {const c=cs[i],d=Math.max(0,c.lower-dot(c.n,y))/dot(c.n,c.n);x=y.map((v,k)=>v+d*c.n[k]);}
   corrections[i]=y.map((v,k)=>v-x[k]);
  }
  if(residual(x,cs,speed)<=1e-9&&Math.hypot(...x.map((v,k)=>v-old[k]))<=1e-10)return {velocity:x,iterations:it,converged:true};
 }
 return {velocity:x,iterations:maxIterations,converged:false};
}
module.exports={repair,residual};

},
"./adapter.cjs":function(module,exports,require,Buffer,process){
'use strict';

// SOURCE ONLY. Dependency injection performs no work until the caller invokes it.
const scratch = new DataView(new ArrayBuffer(8));
function word(value) {
  if (typeof value !== 'number') throw new TypeError('binary64 number required');
  scratch.setFloat64(0, value, false);
  return scratch.getUint32(0, false).toString(16).padStart(8, '0') +
    scratch.getUint32(4, false).toString(16).padStart(8, '0');
}
function number(hex) {
  if (typeof hex !== 'string' || !/^[0-9a-f]{16}$/.test(hex)) throw Error('invalid binary64 word');
  scratch.setUint32(0, parseInt(hex.slice(0, 8), 16), false);
  scratch.setUint32(4, parseInt(hex.slice(8), 16), false);
  return scratch.getFloat64(0, false);
}
const words = values => Array.from(values, word);
const cross = (a, b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
function need(ok, message) { if (!ok) throw Error(message); }
function finiteVector(value, n) {
  return Array.isArray(value) && value.length === n && value.every(Number.isFinite);
}
function copyDrones(drones) { return drones.map(({id, state}) => ({id, state: state.slice()})); }
function inputWords(drones) { return {drones: drones.map(({id, state}) => ({id, state: words(state)}))}; }
function freeze(value) {
  if (value && typeof value === 'object' && !Object.isFrozen(value)) {
    for (const item of Object.values(value)) freeze(item);
    Object.freeze(value);
  }
  return value;
}
// Retains malformed native responses without requiring their success schema.
// Numeric values, including NaN and signed zero, retain their exact words.
function snapshot(value, seen = new Map()) {
  if (typeof value === 'number') return {binary64Word: word(value)};
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return value;
  if (typeof value !== 'object') return {unserializableType: typeof value, text: String(value)};
  if (seen.has(value)) return {reference: seen.get(value)};
  seen.set(value, seen.size);
  if (value instanceof ArrayBuffer) return {arrayBufferBytes: Array.from(new Uint8Array(value))};
  if (ArrayBuffer.isView(value)) return {viewType: value.constructor.name,
    viewBytes: Array.from(new Uint8Array(value.buffer, value.byteOffset, value.byteLength))};
  const isArray = Array.isArray(value), keys = Reflect.ownKeys(value);
  const denseArray = isArray && keys.length === value.length+1 &&
    Array.from({length: value.length}, (_, i) => Object.hasOwn(value, i)).every(Boolean);
  const out = denseArray ? [] : Object.create(null);
  if (isArray && !denseArray) out.arrayLength = value.length;
  for (const key of keys) {
    if (isArray && key === 'length') continue;
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    out[String(key)] = Object.hasOwn(descriptor, 'value') ? snapshot(descriptor.value, seen) : {accessor: true};
  }
  return out;
}
function project(drones) {
  const seen = new Set();
  return drones.map(({id, state}) => {
    need(Number.isSafeInteger(id) && id >= 0 && !Object.is(id, -0) && !seen.has(id), 'projection-id');
    seen.add(id); need(finiteVector(state, 17), 'projection-state');
    const q = state.slice(6, 10);
    const normSquare = ((q[0]*q[0] + q[1]*q[1]) + q[2]*q[2]) + q[3]*q[3];
    const norm = Math.sqrt(normSquare);
    need(norm > 0 && Number.isFinite(norm), 'projection-quaternion');
    const next = state.slice();
    for (let k = 0; k < 4; k++) next[6+k] = q[k]/norm;
    need(next.every(Number.isFinite), 'projection-nonfinite');
    return {id, state: next, rawStateWords: words(state), normSquareWord: word(normSquare), normWord: word(norm)};
  });
}
async function semanticHash(input) {
  need(globalThis.crypto && globalThis.crypto.subtle, 'sha256-unavailable');
  const digest = await globalThis.crypto.subtle.digest('SHA-256', new TextEncoder().encode(JSON.stringify(input)));
  return Array.from(new Uint8Array(digest), x => x.toString(16).padStart(2, '0')).join('');
}

function createAdapter({physics: F, native}) {
  need(F && native && typeof native.query === 'function', 'dependencies');
  function nominalLoad({id, state}) {
    const rotor = state.slice(13, 17), q = state.slice(6, 10), axis = F.rotate(q, [0, 0, 1]);
    let collective = 0; const worldMoment = [0, 0, 0];
    for (let r = 0; r < 4; r++) {
      collective += rotor[r];
      const offset = F.rotate(q, [F.rotors[r][0], F.rotors[r][1], 0]);
      const lever = cross(offset, axis);
      for (let k = 0; k < 3; k++) worldMoment[k] += lever[k]*rotor[r];
    }
    return {id, rotor, collective, worldForce: axis.map(x => x*collective), worldMoment};
  }
  function bind(contextToken, projected, envelope) {
    need(envelope && envelope.contextToken === contextToken, 'stale-stage-token');
    const expected = inputWords(projected);
    need(JSON.stringify(envelope.inputWords) === JSON.stringify(expected), 'stale-input-words');
    const result = envelope.result;
    need(result && result.status === 'native-success', 'native-non-success');
    need(Array.isArray(result.raw) && result.raw.length === projected.length, 'native-raw-shape');
    need(JSON.stringify(inputWords(result.raw)) === JSON.stringify(expected), 'native-raw-binding');
    need(Array.isArray(result.loads) && result.loads.length === projected.length, 'native-load-count');
    const byId = new Map();
    for (const load of result.loads) {
      need(load && Number.isSafeInteger(load.id) && !byId.has(load.id), 'native-load-id');
      need(finiteVector(load.rotor, 4) && Number.isFinite(load.collective) &&
        finiteVector(load.worldForce, 3) && finiteVector(load.worldMoment, 3), 'native-load-shape');
      byId.set(load.id, load);
    }
    need(projected.every(item => byId.has(item.id)), 'native-load-missing-id');
    return projected.map(item => byId.get(item.id));
  }
  function consume(item, command, load) {
    need(finiteVector(command, 4), 'command-shape');
    const state = item.state, q = state.slice(6, 10), w = state.slice(10, 13);
    const derivative = F.derivative(state, command);
    for (let k = 0; k < 3; k++) derivative[3+k] = load.worldForce[k]/F.P.m;
    derivative[5] -= F.P.g;
    const bodyArm = F.rotate([-q[0], -q[1], -q[2], q[3]], load.worldMoment);
    const nominalYaw = F.wrench(state.slice(13, 17)).t[2];
    const totalBody = [bodyArm[0], bodyArm[1], bodyArm[2] + nominalYaw];
    const gyro = cross(w, w.map((value, k) => value*F.P.I[k]));
    for (let k = 0; k < 3; k++) derivative[10+k] = (totalBody[k]-gyro[k])/F.P.I[k];
    need(finiteVector(derivative, 17), 'derivative-nonfinite');
    return {derivative, record: {id: item.id, rawStateWords: item.rawStateWords,
      stateWords: words(state), normSquareWord: item.normSquareWord, normWord: item.normWord,
      commandsWords: words(command), nominalMotorWords: words(state.slice(13, 17)),
      consumed: {rotorWords: words(load.rotor), collectiveWord: word(load.collective),
        worldForceWords: words(load.worldForce), worldMomentWords: words(load.worldMoment)},
      bodyArmWords: words(bodyArm), totalBodyWords: words(totalBody), nominalYawWord: word(nominalYaw),
      gyroWords: words(gyro), derivativeWords: words(derivative)}};
  }
  async function evaluate({raw, commands, context, append, guard, loadProvider}) {
    const {arm, stepIndex, stageIndex, relativeTime, originalTime, dt} = context;
    const stageId = `${arm}-step${stepIndex}-k${stageIndex}`;
    const record = {schema: 'm31-coupled-stage-v1', stageId, arm, stepIndex, stageIndex,
      relativeTimeWord: word(relativeTime), originalTimeWord: word(originalTime), dtWord: word(dt),
      status: 'pending', nativeInput: null, native: null, records: [], reason: null,
      nativeCalls: 0, rawBeforeProjection: inputWords(raw), commandsBeforeEvaluation: commands.map(words)};
    let projected, returned, scientificError = null;
    try {
      guard(); projected = project(raw);
      need(commands.length === projected.length && commands.every(u => finiteVector(u, 4)), 'commands-count');
      record.nativeInput = inputWords(projected);
      let loads;
      if (loadProvider) {
        loads = loadProvider(projected, context);
        loads = bind(stageId, projected, {contextToken: stageId, inputWords: record.nativeInput,
          result: {status: 'native-success', raw: copyDrones(projected), loads}});
      } else if (arm === 'off') {
        loads = projected.map(nominalLoad);
      } else {
        need(arm === 'coupled', 'unknown-arm');
        const hash = await semanticHash(record.nativeInput);
        record.nativeCalls = 1;
        let result;
        try { result = native.query(copyDronesAsInput(projected), 'F', guard); }
        catch (error) { record.nativeThrown = {message: String(error && error.message || error), detail: snapshot(error)}; throw error; }
        // Preserve the response before binding or trusting any success field.
        try { record.native = native.encodeEvidence(result); }
        catch (error) {
          record.nativeMalformed = {encodingError: String(error && error.message || error), response: snapshot(result)};
          throw Error('native-evidence-schema');
        }
        record.native.caseId = stageId;
        record.native.semanticInputSha256 = hash;
        record.native.inlineInputCanonicalSha256 = hash;
        try { loads = bind(stageId, projected, {contextToken: stageId, inputWords: record.nativeInput, result}); }
        catch (error) {
          if (result && result.status === 'native-success') record.nativeMalformed = {
            bindingError: String(error && error.message || error), response: snapshot(result)};
          throw error;
        }
      }
      const evaluated = projected.map((item, i) => consume(item, commands[i], loads[i]));
      record.records = evaluated.map(item => item.record); record.status = 'completed';
      returned = {derivatives: evaluated.map(item => item.derivative), stageId, projected};
    } catch (error) {
      record.status = 'failed'; record.reason = String(error && error.message || error);
      if (projected) record.projectedOnFailure = inputWords(projected);
      scientificError = error;
    }
    // Exactly one durable append. Persistence failures propagate untouched;
    // they are not reclassified as a scientific result or retried here.
    await append('stage', freeze(record));
    if (scientificError) throw scientificError;
    return returned;
  }
  function copyDronesAsInput(drones) { return {drones: copyDrones(drones)}; }
  async function step({drones, commands, arm, stepIndex, dt, timeOrigin, append, guard, loadProvider, onRawK2}) {
    const base = copyDrones(drones), t = stepIndex*dt, stageIds = [];
    const stage = async (raw, stageIndex, relativeTime) => {
      const evaluated = await evaluate({raw, commands, append, guard, loadProvider,
        context: {arm, stepIndex, stageIndex, relativeTime, originalTime: timeOrigin+relativeTime, dt}});
      stageIds.push(evaluated.stageId); return evaluated.derivatives;
    };
    const add = (k, scale) => base.map((item, i) => ({id: item.id,
      state: item.state.map((value, j) => value+scale*k[i][j])}));
    const k1 = await stage(base, 1, t), rawK2 = add(k1, dt/2);
    if (onRawK2) await onRawK2(copyDrones(rawK2));
    const k2 = await stage(rawK2, 2, t+dt/2);
    const k3 = await stage(add(k2, dt/2), 3, t+dt/2);
    const k4 = await stage(add(k3, dt), 4, t+dt);
    const rawFinal = base.map((item, i) => ({id: item.id, state: item.state.map((value, j) =>
      value+dt*(((k1[i][j]+2*k2[i][j])+2*k3[i][j])+k4[i][j])/6)}));
    let final = null, projectionError = null;
    try { final = project(rawFinal); } catch (error) { projectionError = error; }
    await append('step', freeze({schema: 'm31-coupled-step-v1', stepId: `${arm}-step${stepIndex}`,
      arm, stepIndex, relativeTimeWord: word(t+dt), originalTimeWord: word(timeOrigin+(t+dt)), dtWord: word(dt),
      status: projectionError ? 'failed' : 'completed', reason: projectionError ? String(projectionError.message || projectionError) : null,
      start: base.map(item => ({id: item.id, stateWords: words(item.state)})), stageIds,
      rawFinal: rawFinal.map(item => ({id: item.id, stateWords: words(item.state)})),
      final: final && final.map(item => ({id: item.id, stateWords: words(item.state),
        normSquareWord: item.normSquareWord, normWord: item.normWord}))}));
    if (projectionError) throw projectionError;
    return copyDrones(final);
  }
  return {nominalLoad, bind, consume, evaluate, step};
}

module.exports = {createAdapter, word, number, words, project, snapshot, freeze, inputWords, copyDrones, cross};

},
"./browser-driver.cjs":function(module,exports,require,Buffer,process){
'use strict';

const A = require('./adapter.cjs');
const {word, number, words, project, snapshot, freeze, inputWords, copyDrones} = A;
function need(ok, message) { if (!ok) throw Error(message); }
const distance = (a, b) => Math.hypot(...a.map((x, i) => x-b[i]));
function errors(actual, exact, hover) {
  const q = actual.slice(6, 10), target = exact.slice(6, 10);
  return {position: distance(actual.slice(0, 3), exact.slice(0, 3)),
    velocity: distance(actual.slice(3, 6), exact.slice(3, 6)),
    attitude: 2*Math.min(distance(q, target), distance(q, target.map(x => -x))),
    omega: distance(actual.slice(10, 13), exact.slice(10, 13)),
    motor: Math.max(...actual.slice(13, 17).map((x, i) => Math.abs(x-exact[13+i])/hover))};
}
function basicState() { return [0, 0, 1, .2, -.1, .05, 0, 0, 0, 1, 0, 0, 0, .06, .06, .06, .06]; }

function createDriver({physics: F, swarm: S, Grid, geometry: G, native}) {
  const adapter = A.createAdapter({physics: F, native});
  let used = false;

  async function wiringControls(config, emit, guard) {
    const declared = config.wiringControls.ids, reports = [];
    for (const id of declared) {
      guard(); const tilted = ['tilted-unequal', 'nominal-yaw', 'motor-lag'].includes(id);
      const state = tilted ? config.wiringControls.tilted.rawState.slice() : basicState();
      let raw = [{id: 11, state}];
      if (['reversed-load-ids', 'duplicate-load-id', 'missing-load-id'].includes(id)) {
        const second = basicState(); second[0] = 2; second[13] = .05;
        raw.push({id: 29, state: second});
      }
      if (id === 'zero-quaternion') raw[0].state.splice(6, 4, 0, 0, 0, 0);
      if (id === 'nonfinite-quaternion') raw[0].state[6] = Infinity;
      const commands = raw.map(() => tilted ? config.wiringControls.tilted.commands.slice() : [.07, .08, .09, .10]);
      const expected = config.wiringControls.rejectedIds.includes(id) ? 'rejected' : 'accepted';
      const record = {schema: 'm31-wiring-control-v1', id, expected, observed: null,
        reason: null, nativeCalls: 0, fixture: {rawInput: inputWords(raw), commandsWords: commands.map(words),
          contextToken: `control-${id}`, envelope: null}, records: [], pass: false};
      try {
        const projected = project(raw);
        const loads = projected.map(item => tilted ? {id: item.id,
          rotor: config.wiringControls.tilted.rotor.slice(), collective: config.wiringControls.tilted.collective,
          worldForce: config.wiringControls.tilted.worldForce.slice(), worldMoment: config.wiringControls.tilted.worldMoment.slice()} : adapter.nominalLoad(item));
        const envelope = {contextToken: record.fixture.contextToken, inputWords: inputWords(projected),
          result: {status: 'native-success', raw: copyDrones(projected), loads}};
        if (id === 'reversed-load-ids') envelope.result.loads.reverse();
        if (id === 'duplicate-load-id') envelope.result.loads[1].id = envelope.result.loads[0].id;
        if (id === 'missing-load-id') envelope.result.loads[1].id = 99;
        if (id === 'stale-stage-token') envelope.contextToken = 'control-previous-stage';
        if (id === 'stale-raw-input') envelope.result.raw[0].state[0] += 1;
        if (id === 'nonfinite-load') envelope.result.loads[0].worldForce[0] = NaN;
        record.fixture.envelope = snapshot(envelope);
        const bound = adapter.bind(record.fixture.contextToken, projected, envelope);
        const evaluated = projected.map((item, i) => adapter.consume(item, commands[i], bound[i]));
        record.records = evaluated.map(item => item.record);
        if (id === 'null-load') {
          record.baselineDerivativeWords = projected.map((item, i) => words(F.derivative(item.state, commands[i])));
          need(evaluated.every((item, i) => distance(item.derivative, F.derivative(projected[i].state, commands[i])) <= config.wiringControls.algebraTolerance), 'null-load-algebra');
        }
        if (id === 'tilted-unequal') {
          const body = record.records[0].bodyArmWords.map(number);
          need(distance(body, config.wiringControls.tilted.expectedBodyArm) <= config.wiringControls.algebraTolerance, 'frame-transform-algebra');
        }
        if (id === 'nominal-yaw') {
          const expectedYaw = F.wrench(projected[0].state.slice(13, 17)).t[2];
          need(record.records[0].nominalYawWord === word(expectedYaw), 'nominal-yaw-policy');
          need(word(expectedYaw) !== word(F.wrench(bound[0].rotor).t[2]), 'yaw-control-degenerate');
        }
        if (id === 'motor-lag') {
          need(evaluated[0].derivative.slice(13, 17).every((v, r) => word(v) === word((commands[0][r]-projected[0].state[13+r])/F.P.motorTau)), 'motor-lag-algebra');
        }
        if (id === 'reversed-load-ids') {
          need(record.records.every((item, i) => item.id === projected[i].id &&
            JSON.stringify(item.consumed.rotorWords) === JSON.stringify(words(projected[i].state.slice(13, 17)))), 'stable-id-algebra');
        }
        record.observed = 'accepted'; record.pass = expected === 'accepted';
      } catch (error) {
        record.observed = 'rejected'; record.reason = String(error && error.message || error);
        record.pass = expected === 'rejected' && record.reason === config.wiringControls.expectedReasons[id];
      }
      await emit('wiring-control', record); reports.push({id, pass: record.pass, observed: record.observed});
    }
    return reports;
  }

  async function manufacturedControls(config, emit, guard) {
    const reports = [], hover = F.P.m*F.P.g/4, T = config.manufactured.duration;
    for (const caseId of config.manufactured.cases) {
      const runs = [];
      for (let level = 0; level < config.manufactured.timesteps.length; level++) {
        guard(); const dt = config.manufactured.timesteps[level], count = Math.round(T/dt);
        const id = `${caseId}-h${level}`, initial = basicState();
        if (caseId !== 'translation') initial.splice(3, 3, 0, 0, 0);
        if (caseId === 'principal-spin') initial[12] = 1;
        if (caseId === 'motor-relaxation') initial.splice(13, 4, .04, .04, .04, .04);
        const command = Array(4).fill(caseId === 'motor-relaxation' ? .08 : .06), exact = initial.slice();
        if (caseId === 'translation') for (let k = 0; k < 3; k++) exact[k] += T*initial[3+k];
        if (caseId === 'principal-spin') { exact[8] = Math.sin(T/2); exact[9] = Math.cos(T/2); }
        if (caseId === 'motor-relaxation') for (let r = 0; r < 4; r++) exact[13+r] = .08+(.04-.08)*Math.exp(-T/F.P.motorTau);
        const record = {schema: 'm31-manufactured-run-v1', id, caseId, dtWord: word(dt), durationWord: word(T),
          steps: count, initial: [{id: 11, stateWords: words(initial)}], commandsWords: [words(command)],
          events: [], final: null, exactFinal: [{id: 11, stateWords: words(exact)}], errors: null,
          nativeCalls: 0, complete: false, reason: null,
          law: 'prescribed-world-force-mg-and-zero-world-arm-moment; nominal actuator yaw retained'};
        let drones = [{id: 11, state: initial.slice()}];
        try {
          for (let stepIndex = 0; stepIndex < count; stepIndex++) {
            drones = await adapter.step({drones, commands: [command], arm: id, stepIndex, dt, timeOrigin: 0,
              append: async (kind, item) => { record.events.push({kind, record: item}); }, guard,
              loadProvider: projected => projected.map(item => ({id: item.id, rotor: item.state.slice(13, 17),
                collective: item.state.slice(13, 17).reduce((a, b) => a+b, 0),
                worldForce: [0, 0, F.P.m*F.P.g], worldMoment: [0, 0, 0]}))});
          }
          record.final = drones.map(item => ({id: item.id, stateWords: words(item.state)}));
          record.errors = errors(drones[0].state, exact, hover);
          record.complete = Object.values(record.errors).every(Number.isFinite);
        } catch (error) { record.reason = String(error && error.message || error); }
        await emit('manufactured-run', record); runs.push(record);
      }
      const gates = {};
      for (const [component, tolerance] of Object.entries(config.manufactured.tolerances)) {
        const e = runs.map(run => run.errors && run.errors[component]);
        const floor = config.manufactured.roundoffFloor, ratio = config.manufactured.refinementRatio;
        const available = runs.every(run => run.complete) && e.every(x => typeof x === 'number' && Number.isFinite(x));
        gates[component] = {errors: e, tolerance, roundoffFloor: floor,
          pass: available && e[2] <= tolerance && e[1] <= Math.max(floor, ratio*e[0]) && e[2] <= Math.max(floor, ratio*e[1])};
      }
      const report = {schema: 'm31-manufactured-summary-v1', caseId,
        runIds: runs.map(run => run.id), gates, pass: Object.values(gates).every(gate => gate.pass),
        observedOrder: null, interpretation: 'analytic endpoint and contraction checks only; no convergence-order claim'};
      await emit('manufactured-summary', report); reports.push(report);
    }
    return reports;
  }

  function control(drones, arm, stepIndex, config) {
    const states = drones.map(item => item.state), grid = new Grid(states, S.P.neighbor), commands = [], records = [];
    for (let i = 0; i < states.length; i++) {
      const state = states[i], neighbors = grid.neighbors(i, S.P.neighbor);
      const velocity = S.steer(i, states, neighbors, 'boids', 'wall-priority');
      const target = {vx: velocity[0], vy: velocity[1], z: state[2]+(2.5*velocity[2]+1.5*state[5])/6,
        yaw: Math.atan2(velocity[1], velocity[0])};
      const actuator = F.control(state, target, 2.25); commands.push(actuator.u.slice());
      records.push({id: drones[i].id, stateWords: words(state), neighborIds: neighbors.map(j => drones[j].id),
        desiredVelocityWords: words(velocity), target: {vxWord: word(target.vx), vyWord: word(target.vy),
          zWord: word(target.z), yawWord: word(target.yaw)}, commandsWords: words(actuator.u),
        saturated: actuator.saturated, desiredQuaternionWords: words(actuator.qd)});
    }
    const time = stepIndex*config.integration.dt;
    return {commands, record: {schema: 'm31-coupled-controller-v1', arm,
      controlIndex: stepIndex/config.integration.stepsPerControl, stepIndex,
      relativeTimeWord: word(time), originalTimeWord: word(config.integration.timeOrigin+time), records}};
  }
  function safety(old, next) {
    const issues = [], a = old.map(item => item.state), b = next.map(item => item.state);
    for (let i = 0; i < b.length; i++) {
      if (!b[i].every(Number.isFinite) || b[i][2] < S.P.bodyRadius) issues.push({kind: 'vehicle-model-limit', id: next[i].id});
      const hits = S.obstacleContacts(a[i], b[i]);
      if (hits.length) issues.push({kind: 'obstacle-contact', id: next[i].id, hits});
    }
    for (const [i, j] of S.contactCandidates(a, b)) {
      const separation = G.segmentPair(a[i], b[i], a[j], b[j]);
      if (separation < 2*S.P.bodyRadius) issues.push({kind: 'drone-contact', ids: [next[i].id, next[j].id], distanceWord: word(separation)});
    }
    return issues;
  }

  async function run({config, initialInput, append, guard}) {
    need(!used, 'driver-single-use'); used = true;
    need(typeof append === 'function' && typeof guard === 'function', 'driver-callbacks');
    const counts = {coupledStages: 0, coupledCompleted: 0, primaryNativeCalls: 0, offStages: 0,
      offCompleted: 0, offNativeCalls: 0, steps: 0, controllers: 0, rawDiagnostics: 0,
      wiringControls: 0, manufacturedRuns: 0, manufacturedSummaries: 0, manufacturedStages: 0};
    async function emit(kind, record) {
      await append(kind, freeze(record));
      if (kind === 'stage') {
        const prefix = record.arm === 'coupled' ? 'coupled' : 'off'; counts[prefix+'Stages']++;
        if (record.status === 'completed') counts[prefix+'Completed']++;
        if (prefix === 'coupled') counts.primaryNativeCalls += record.nativeCalls;
        else counts.offNativeCalls += record.nativeCalls;
      }
      if (kind === 'step') counts.steps++;
      if (kind === 'controller') counts.controllers++;
      if (kind === 'raw-diagnostic') counts.rawDiagnostics++;
      if (kind === 'wiring-control') counts.wiringControls++;
      if (kind === 'manufactured-run') { counts.manufacturedRuns++; counts.manufacturedStages += record.events.filter(event => event.kind === 'stage').length; }
      if (kind === 'manufactured-summary') counts.manufacturedSummaries++;
    }
    const arms = [], failures = [];
    try {
      guard();
      need(config.schema === 'm31-coupled-science-config-v1' && config.integration.dt === .0025 &&
        config.integration.steps === 8 && config.integration.duration === .02 && config.integration.timeOrigin === 5 &&
        config.integration.controlDt === .01 && config.integration.stepsPerControl === 4, 'fixed-integration-config');
      need(F.P.controlDt === .01 && S.P.controlDt === .01 && S.course.id === 'factory-v1', 'frozen-physics-course');
      need(initialInput && Array.isArray(initialInput.drones) && initialInput.drones.length === 64, 'saved-initial-count');
      const initial = initialInput.drones.map(item => ({id: item.id, state: item.state.map(number)}));
      need(initial.every((item, i) => item.id === i && item.state.length === 17 && item.state.every(Number.isFinite)), 'saved-initial-layout');
      await emit('initial', {schema: 'm31-coupled-initial-v1', source: config.initialInput,
        originalTimeWord: word(5), relativeTimeWord: word(0), input: inputWords(initial)});
      const wiring = await wiringControls(config, emit, guard);
      const manufactured = await manufacturedControls(config, emit, guard);
      need(wiring.every(item => item.pass) && manufactured.every(item => item.pass), 'fixed-control-failure');
      for (const arm of ['coupled', 'off']) {
        let drones = copyDrones(initial), commands = null, completedSteps = 0;
        try {
          for (let stepIndex = 0; stepIndex < config.integration.steps; stepIndex++) {
            guard();
            if (stepIndex%config.integration.stepsPerControl === 0) {
              const update = control(drones, arm, stepIndex, config); commands = update.commands;
              await emit('controller', update.record);
            }
            const old = drones;
            drones = await adapter.step({drones, commands, arm, stepIndex, dt: config.integration.dt,
              timeOrigin: config.integration.timeOrigin, append: emit, guard,
              onRawK2: arm === 'coupled' && stepIndex === 0 ? async raw => {
                const records = raw.map(({id, state}) => {
                  const q = state.slice(6, 10), sum = ((q[0]*q[0]+q[1]*q[1])+q[2]*q[2])+q[3]*q[3];
                  const norm = Math.sqrt(sum), defect = Math.abs(norm-1);
                  return {id, rawStateWords: words(state), normSquareWord: word(sum), normWord: word(norm),
                    defectWord: word(defect), passesNormPrerequisite: Number.isFinite(norm) && defect <= config.projection.qTolerance};
                });
                await emit('raw-diagnostic', {schema: 'm31-raw-quaternion-prerequisite-v1',
                  stageId: 'coupled-step0-k2', qToleranceWord: word(config.projection.qTolerance), records,
                  nativeCalls: 0, referenceCalls: 0, fullPreparationAttempted: false, admissionConclusion: null,
                  interpretation: 'quaternion norm prerequisite only; passing implies neither complete geometry nor modeled-domain admission'});
              } : null});
            completedSteps++;
            const issues = safety(old, drones);
            await emit('safety', {schema: 'm31-coupled-safety-v1', arm, stepIndex, issues, pass: issues.length === 0});
            need(issues.length === 0, 'continuation-safety-failure');
          }
          const report = {arm, complete: true, completedSteps, final: inputWords(drones)};
          arms.push(report); await emit('arm-summary', report);
        } catch (error) {
          const report = {arm, complete: false, completedSteps, reason: String(error && error.message || error), final: inputWords(drones)};
          arms.push(report); failures.push(report); await emit('arm-summary', report);
        }
      }
      const exactCounts = Object.entries(config.expectedRuntimeCounts).every(([key, value]) => counts[key] === value);
      const complete = exactCounts && arms.length === 2 && arms.every(arm => arm.complete);
      const summary = {schema: 'm31-coupled-driver-summary-v1', complete, counts, exactCounts,
        arms: arms.map(({arm, complete: ok, completedSteps, reason}) => ({arm, complete: ok, completedSteps, reason: reason || null})),
        failures, independentReferenceAcceptance: 'pending-external-checker', qualification: 'not-established-by-producer'};
      await emit('driver-summary', summary); return summary;
    } catch (error) {
      const summary = {schema: 'm31-coupled-driver-summary-v1', complete: false, counts,
        reason: String(error && error.message || error), failures, qualification: 'not-established'};
      await emit('driver-failure', summary); return summary;
    }
  }
  return {run};
}

module.exports = {createDriver};

},
});
