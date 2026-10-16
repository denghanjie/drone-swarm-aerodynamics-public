'use strict';
const spec=require('./spec.json'),A=require('./adapter.cjs'),R=require('./rational.cjs'),P=require('./pair-prepared.cjs'),T=require('./tree.cjs'),L=require('./loads.cjs'),F=require('./zero-filter.cjs');
const counters=()=>Object.fromEntries(['preparationCalls','globalProofs','treeNodes','nodeVisits','nodeRuleTests','zeroNodes','zeroPairs','leafVisits','scalarPairs','scalarZeroPairs','positiveTerms','rejectedPairs','unresolvedPairs','filterPrepared','filterAttempts','filterZeros','exactScalarCalls'].map(k=>[k,0]));
function method(input,name,onPhase){
 // This admission is deliberately paid inside every timed method call.
 if(!spec.methods.includes(name)||!Array.isArray(input.drones)||input.drones.length<1||input.drones.length>spec.maxDrones||new Set(input.drones.map(d=>d.id)).size!==input.drones.length||input.drones.some(d=>!Number.isInteger(d.id)||d.id<spec.stableIdMin||d.id>spec.stableIdMax||!Array.isArray(d.state)||d.state.length!==17||d.state.some(b=>typeof b!=='string'||!(/^[0-9a-f]{16}$/).test(b))))throw Error('Invalid raw-word identity/domain');
 const work=counters();
 const prepared=input.drones.map(d=>{work.preparationCalls++;const p=A.prepare({receiver:d.state,source:d.state});return {id:d.id,value:p.prepared?.receiver??null,rejection:p.rejection};});
 const assembly={mode:name,globalGuard:null,tree:null,queries:[],work};
 const record={name,prepared,assembly,result:null,solve:null,certificate:null};
 const refuse=(status,branch,witness=null)=>{record.result={status,branch,witness,toleranceAchieved:null};return record;};
 const invalid=prepared.find(d=>d.rejection);
 if(invalid){onPhase('prepared');assembly.mode='global-preparation';return refuse('rejected',invalid.rejection,{id:invalid.id});}
 const exact=new Map(prepared.map(d=>[d.id,{center:d.value.center.map(R.fromBits),axis:d.value.axis.map(R.fromBits),points:d.value.points.map(v=>v.map(R.fromBits)),forces:d.value.forces.map(R.fromBits)}]));
 // Build optional fast geometry from the same admitted prepared words inside every timed call.
 const fast=name==='filtered'?new Map(prepared.map(d=>{work.filterPrepared++;return [d.id,F.prepare(d.value)];})):null;
 const filterConstants=name==='filtered'?F.constants(A.constantBits):null;
 onPhase('prepared');
 const indices=new Map(input.drones.map((d,i)=>[d.id,i]));
 let tree=null;
 if(name==='hierarchy'||name==='filtered'){
  work.globalProofs++;assembly.globalGuard=T.globalGuard(exact);
  if(assembly.globalGuard.passed){tree=T.build(exact);work.treeNodes=tree.nodes.length;assembly.tree=T.wire(tree);}
  else assembly.mode='fallback';
 }
 onPhase('spatial');
 const pairQuery=P.createQuery();
 const nonzero=[];
 function scan(i,r,members){
  const entries=[],filterZeros=[];let zeroCount=0;
  for(const j of members.slice().sort((a,b)=>a-b)){
   if(i===j)continue;
   work.scalarPairs++;
   const receiverId=input.drones[i].id,sourceId=input.drones[j].id;
   let raw;
   if(name==='filtered'){
    work.filterAttempts++;
    const decision=F.classify(fast.get(receiverId),fast.get(sourceId),r,filterConstants);
    if(decision.kind==='zero'){work.filterZeros++;filterZeros.push({j,branch:decision.branch});raw={status:'zero',branch:decision.branch};}
    else {work.exactScalarCalls++;raw=pairQuery(exact.get(receiverId),exact.get(sourceId),r);}
   }else{work.exactScalarCalls++;raw=pairQuery(exact.get(receiverId),exact.get(sourceId),r);}
   if(raw.status==='zero'){work.scalarZeroPairs++;zeroCount++;continue;}
   let result;
   if(raw.status==='positive'){work.positiveTerms++;result={status:raw.status,branch:raw.branch,coefficient:raw.intervals.coefficient};}
   else if(raw.status==='rejected'){work.rejectedPairs++;result={status:raw.status,branch:raw.branch};}
   else if(raw.status==='unresolved'){work.unresolvedPairs++;result={status:raw.status,branch:raw.branch};}
   else throw Error('Unexpected scalar status');
   entries.push({j,result});nonzero.push({i,r,j,result});
  }
  return {entries,zeroCount,filterZeros};
 }
 for(let i=0;i<input.drones.length;i++)for(let r=0;r<4;r++){
  const query={i,r,terminals:[]};assembly.queries.push(query);
  if(!tree){query.terminals.push({kind:'scan',...scan(i,r,input.drones.map((_,j)=>j))});continue;}
  function visit(nodeId){
   work.nodeVisits++;const node=tree.nodes[nodeId];
   const rule=T.zeroRule(node,exact.get(input.drones[i].id),r,work);
   if(rule){const count=tree.permutation.slice(node.start,node.end).filter(id=>id!==input.drones[i].id).length;work.zeroNodes++;work.zeroPairs+=count;query.terminals.push({kind:'zero',node:nodeId,rule,count});return;}
   if(node.left===null){work.leafVisits++;query.terminals.push({kind:'leaf',node:nodeId,...scan(i,r,tree.permutation.slice(node.start,node.end).map(id=>indices.get(id)))});return;}
   visit(node.left);visit(node.right);
  }
  visit(0);
 }
 if(work.scalarPairs+work.zeroPairs!==4*input.drones.length*(input.drones.length-1))throw Error('Incomplete pair partition');
 nonzero.sort((a,b)=>a.i-b.i||a.r-b.r||a.j-b.j);
 const pairs=nonzero.map(p=>({...p,i:input.drones[p.i].id,j:input.drones[p.j].id}));
 onPhase('assembled');
 const witness=p=>({i:p.i,r:p.r,j:p.j});
 const rejection=pairs.find(p=>p.result.status==='rejected');
 if(rejection)return refuse('rejected','pair-'+rejection.result.branch,witness(rejection));
 const unresolved=pairs.find(p=>p.result.status==='unresolved');
 if(unresolved)return refuse('unresolved','pair-'+unresolved.result.branch,witness(unresolved));
 const ordered=prepared.slice().sort((a,b)=>-R.cmp(exact.get(a.id).center[2],exact.get(b.id).center[2])||a.id-b.id),rank=new Map(ordered.map((d,k)=>[d.id,k]));
 const backwards=pairs.find(p=>p.result.status==='positive'&&rank.get(p.j)>=rank.get(p.i));
 if(backwards)return refuse('rejected','ordering',witness(backwards));
 if(work.positiveTerms>spec.positiveTermCap)return refuse('resource','positive-term-budget');
 Object.assign(record,L.certify(prepared,pairs));return record;
}
// Shared immutable literal ingestion is outside the raw-word timing boundary.
function makeInput(scene){
 return Object.freeze({drones:Object.freeze(scene.drones.map(d=>Object.freeze({id:d.id,state:Object.freeze(d.state.map(s=>A.bits(Number(s))))})))});
}
module.exports={method,makeInput};
