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
