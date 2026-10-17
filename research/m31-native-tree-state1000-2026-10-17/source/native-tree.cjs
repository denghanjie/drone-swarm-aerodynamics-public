'use strict';

// Source-only draft. Loading/executing this module requires the parent's
// separately frozen source approval and execution allocation.
const K = (() => {
'use strict';

// SOURCE ONLY: H/H0 fork of F; numerical qualification is pending.
// Original production F and all shared numerical dependencies stay immutable.
const anchor=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs');
const lean=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/lean-anchor.cjs');
const {fade}=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/reference-excerpt.cjs');
const tree=require('./tree.cjs');
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

function buildAssembly(states,mode,fullSymbols,guard=()=>{},options=null){
 const typed=mode==='typed';
 const t0=performance.now(),q=prepare(states),{n,p,nominal,S0,input,nominalOK}=q,t1=performance.now();
 // Retain the F eligibility predicate; coverage is separate finite-runtime evidence.
 const screen=screenPredicate(p,n);
 const certificate={finite:null,min:null,max:null,spans:null,certified:null,useGrid:false,fallback:false,reason:'center-tree-selected'},t2=performance.now();
 const treeEvidence=options&&options.evidence?tree.coverage(mode,n,screen):null;
 if(treeEvidence&&options.onEvidence)options.onEvidence(treeEvidence);
 if(!screen.eligible){
  // Full unchanged-L evaluation, including its preparation and original guards.
  // The preceding current preparation/predicate is intentionally paid in F.
  const delegatedStart=performance.now(),fallback=lean.build(states,'lean',fullSymbols,guard);
  if(treeEvidence)treeEvidence.complete=true;
  return {...fallback,screen:finishScreen(screen,fallback.geometryWork),
   phasesMs:{...fallback.phasesMs,screenPreflight:delegatedStart-t0}};
 }
 const centerTree=tree.build(p,n,treeEvidence);
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
  const candidates=tree.gather(centerTree,p,i,mode,treeEvidence);
  let previous=-1;
  for(const j of candidates){
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
  if(treeEvidence)treeEvidence.counters.completedReceivers++;
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
 const assemblyStats={schema:'m31-receiver-row-assembly-v1',mode:'lean',inputN:n,positiveEntries:entries,dependencyEntries:uniqueVehicleEdges,
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
 if(treeEvidence)treeEvidence.complete=true;
 return {...q,src,kv,offsets,aa,symbols,symbolCounts,geometryWork,graph,admission,ordinaryLmax,deps,certificate,assemblyStats,screen:finishScreen(screen,geometryWork),phasesMs:{input:t1-t0,index:t2-t1,geometry:t3-t2,admission:t4-t3}};
}

function build(states,mode,fullSymbols,guard,options){
 if(mode==='H'||mode==='H0')return buildAssembly(states,mode,fullSymbols,guard,options);
 throw new TypeError('tree build method must be H or H0');
}
return {constants,build,schedule:anchor.schedule,fullGraph:anchor.fullGraph,solve:anchor.solve,residual:anchor.residual,cached:anchor.cached,checksum:anchor.checksum};

})();
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
function query(input, method = 'H', guard = () => {}, options = null) {
  const begin = performance.now(), phasesMs = {}; let phaseStart = begin;
  let raw = null, q = null, prepared = null, solution = null, output = null, stage = 'input';
  let treeEvidence = null;
  function phase(name) { const now = performance.now(); phasesMs[name] = now - phaseStart; phaseStart = now; }
  function poll() {
    try { guard(); } catch (_) { throw new Refusal('resource-failure', 'cooperative-guard'); }
  }
  const base = {schema: 'm31-native-load-result-v1',
    model: 'ordinary-binary64-full-contribution', method: typeof method === 'string' ? method : null,
    status: null, reason: null, constants: CONSTANTS};
  try {
    need(method === 'H' || method === 'H0', 'input-refused', 'method');
    need(typeof guard === 'function', 'input-refused', 'guard-type'); poll();
    raw = captureInput(input, poll); phase('input'); stage = 'build';
    const states = raw.map(item => item.state);
    q = K.build(states, method, false, poll, {
      evidence: options !== null && typeof options === 'object' && options.treeEvidence === true,
      onEvidence(value) { treeEvidence = value; value.canonicalIds = raw.map(item => item.id); }
    });
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
  // The sink retains explicitly requested partial coverage even if build throws.
  // No tree certificate or traversal counters are saved by the default query.
  output.tree = treeEvidence;
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
  out.tree = result.tree ? {...result.tree,
    canonicalIds: result.tree.canonicalIds === null ? null : result.tree.canonicalIds.slice(),
    leafDictionary: result.tree.leafDictionary.map(leaves => leaves.slice()),
    nodes: result.tree.nodes.map(node => ({...node, min: vector(node.min), max: vector(node.max),
      ...(node.members ? {members: node.members.slice()} : {})})),
    receivers: result.tree.receivers.map(receiver => ({...receiver,
      culled: receiver.culled.map(cull => ({...cull, difference: word(cull.difference)})),
      leavesRef: receiver.leavesRef,
      gathered: receiver.gathered === null ? null : {kind: receiver.gathered.kind, data: receiver.gathered.data.slice()}})),
    counters: {...result.tree.counters}} : null;
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
