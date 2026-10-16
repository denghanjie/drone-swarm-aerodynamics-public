'use strict';
const spec=require('./spec.json'),A=require('./adapter.cjs'),P=require('./pair.cjs'),R=require('./rational.cjs'),I=require('./interval.cjs');
const iq=q=>R.toInterval(q,I), ONE=iq(R.one), Z=iq(R.zero);
const sum=xs=>xs.reduce(I.add,Z), enc=I.encode;
const rational=q=>({n:q.n.toString(),d:q.d.toString()});
const cross=(a,b)=>[R.sub(R.mul(a[1],b[2]),R.mul(a[2],b[1])),R.sub(R.mul(a[2],b[0]),R.mul(a[0],b[2])),R.sub(R.mul(a[0],b[1]),R.mul(a[1],b[0]))];
function maxError(box,candidate,scale){
 const difference=I.sub(box,iq(candidate));
 const absMax=(-difference.l)>difference.u?-difference.l:difference.u;
 return I.div(I.interval(0n,absMax),iq(scale)).u;
}
function normError(box,candidate,scale){
 return I.div(I.sqrt(sum(box.map((b,k)=>I.square(I.sub(b,iq(candidate[k])))))),iq(scale)).u;
}
function solve(scene){
 const input={drones:scene.drones.map(d=>({id:d.id,state:d.state.map(s=>A.bits(Number(s)))}))};
 if(input.drones.length<1||input.drones.length>spec.maxDrones||new Set(input.drones.map(d=>d.id)).size!==input.drones.length||input.drones.some(d=>!Number.isInteger(d.id)||d.id<spec.stableIdMin||d.id>spec.stableIdMax||d.state.length!==17))throw Error('Invalid declared identity/domain');
 const prepared=input.drones.map(d=>{const p=A.prepare({receiver:d.state,source:d.state});return {id:d.id,value:p.prepared?.receiver??null,rejection:p.rejection};});
 const pairs=[],coverage={plannedPairs:4*input.drones.length*(input.drones.length-1),observedPairs:0,positiveTerms:0,stopReason:null};
 const record={id:scene.id,input,prepared,coverage,pairs,result:null,solve:null,certificate:null};
 const refuse=(status,branch,witness=null)=>{record.result={status,branch,witness,toleranceAchieved:null};return record;};
 const invalid=prepared.find(d=>d.rejection);
 if(invalid){coverage.stopReason='global-preparation';return refuse('rejected',invalid.rejection,{id:invalid.id});}
 const ordered=prepared.slice().sort((a,b)=>-R.cmp(R.fromBits(a.value.center[2]),R.fromBits(b.value.center[2]))||a.id-b.id),rank=new Map(ordered.map((d,k)=>[d.id,k]));
 const byId=new Map(prepared.map((d,k)=>[d.id,k]));
 for(const receiver of input.drones)for(let r=0;r<4;r++)for(const source of input.drones){
  if(receiver.id===source.id)continue;
  const result=P.query({receiver:receiver.state,source:source.state,rotor:r,self:false}).result;
  pairs.push({i:receiver.id,r,j:source.id,result});
  if(result.status==='positive')coverage.positiveTerms++;
 }
 coverage.observedPairs=pairs.length;
 if(coverage.observedPairs!==coverage.plannedPairs)throw Error('Incomplete pair coverage');
 const witness=p=>({i:p.i,r:p.r,j:p.j});
 const rejection=pairs.find(p=>p.result.status==='rejected');
 if(rejection)return refuse('rejected','pair-'+rejection.result.branch,witness(rejection));
 const unresolved=pairs.find(p=>p.result.status==='unresolved');
 if(unresolved)return refuse('unresolved','pair-'+unresolved.result.branch,witness(unresolved));
 const backwards=pairs.find(p=>p.result.status==='positive'&&rank.get(p.j)>=rank.get(p.i));
 if(backwards)return refuse('rejected','ordering',witness(backwards));
 if(coverage.positiveTerms>spec.positiveTermCap)return refuse('resource','positive-term-budget');
 const rows=prepared.map(()=>Array.from({length:4},()=>[]));
 for(const p of pairs)if(p.result.status==='positive')rows[byId.get(p.i)][p.r].push({j:byId.get(p.j),a:I.decode(p.result.intervals.coefficient)});
 const f=prepared.map(d=>d.value.forces.map(R.fromBits));
 const weights=f.map(v=>{const total=R.sum(v);return v.map(x=>R.div(x,total));});
 // Native proposal only: never used as a mathematical accuracy premise.
 const fnative=prepared.map(d=>d.value.forces.map(A.number));
 const wnative=fnative.map(v=>{const total=v.reduce((a,b)=>a+b,0);return v.map(x=>x/total);});
 let x=prepared.map(()=>[1,1,1,1]);
 for(let iteration=0;iteration<spec.candidateIterations;iteration++){
  const y=x.map((v,i)=>Math.sqrt(v.reduce((s,q,r)=>s+wnative[i][r]*q,0)));
  x=rows.map(row=>row.map(terms=>{
   const alpha=terms.reduce((s,t)=>s+(Number(t.a.l+t.a.u)/Number(2n*I.S))*y[t.j],0);
   let lo=0,hi=1;
   for(let k=0;k<spec.rootBisections;k++){const mid=(lo+hi)/2;if(mid*mid*mid+alpha*mid>1)hi=mid;else lo=mid;}
   return (lo+hi)/2;
  }));
 }
 record.solve={iterations:spec.candidateIterations,bisections:spec.rootBisections,candidate:x.map((v,i)=>({id:prepared[i].id,x:v.map(A.bits)}))};
 if(x.some(v=>v.some(q=>!Number.isFinite(q)||q<=0||q>1)))return refuse('unresolved','candidate-domain');
 try{
  const xq=record.solve.candidate.map(d=>d.x.map(R.fromBits));
  const xi=xq.map(v=>v.map(iq));
  const y=xq.map((v,i)=>I.sqrt(iq(R.sum(v.map((q,r)=>R.mul(weights[i][r],q))))));
  const proof=[];let Kbar=I.S;
  for(let i=0;i<rows.length;i++)for(let r=0;r<4;r++){
   const s=sum(rows[i][r].map(t=>I.mul(t.a,y[t.j])));
   const p=I.add(I.mul(I.square(xi[i][r]),xi[i][r]),I.mul(xi[i][r],s));
   if(p.l<=0n)return refuse('unresolved','certificate-defect');
   const inverse=I.div(ONE,I.interval(p.l,p.l)).u;
   const kbar=[I.S,p.u,inverse].reduce((a,b)=>a>b?a:b);
   if(kbar>Kbar)Kbar=kbar;
   proof.push({id:prepared[i].id,r,s,p,kbar});
  }
  const boxes=prepared.map(()=>[]);
  for(const row of proof){
   const factor=I.mul(I.interval(row.kbar,row.kbar),I.interval(Kbar,Kbar));
   const i=byId.get(row.id),l=I.div(xi[i][row.r],factor).l,u=I.mul(xi[i][row.r],factor).u;
   row.xstar=I.interval(l,u<I.S?u:I.S);boxes[i][row.r]=row.xstar;
  }
  const maxima={rotor:0n,collective:0n,worldForce:0n,worldMoment:0n};
  const loads=prepared.map((d,i)=>{
   const axis=d.value.axis.map(R.fromBits),levers=d.value.offsets.map(o=>cross(o.map(R.fromBits),axis));
   const rotor=xq[i].map((q,r)=>R.mul(f[i][r],q)),collective=R.sum(rotor),force=axis.map(a=>R.mul(a,collective));
   const moment=[0,1,2].map(k=>R.sum(rotor.map((q,r)=>R.mul(levers[r][k],q))));
   const rb=boxes[i].map((b,r)=>I.mul(iq(f[i][r]),b)),cb=sum(rb),fb=axis.map(a=>I.mul(iq(a),cb));
   const mb=[0,1,2].map(k=>sum(rb.map((b,r)=>I.mul(iq(levers[r][k]),b))));
   const errors={rotor:rb.map((b,r)=>maxError(b,rotor[r],R.div(A.exact.mg,R.q(4n)))),collective:maxError(cb,collective,A.exact.mg),worldForce:normError(fb,force,A.exact.mg),worldMoment:normError(mb,moment,R.mul(A.exact.mg,A.exact.R))};
   for(const category of Object.keys(maxima))for(const v of category==='rotor'?errors.rotor:[errors[category]])if(v>maxima[category])maxima[category]=v;
   return {id:d.id,candidate:{rotor:rotor.map(rational),collective:rational(collective),force:force.map(rational),moment:moment.map(rational)},bounds:{rotor:rb.map(enc),collective:enc(cb),force:fb.map(enc),moment:mb.map(enc)},error:{rotor:errors.rotor.map(String),collective:String(errors.collective),worldForce:String(errors.worldForce),worldMoment:String(errors.worldMoment)}};
  });
  record.certificate={rows:proof.map(p=>({id:p.id,r:p.r,s:enc(p.s),p:enc(p.p),kbar:String(p.kbar),xstar:enc(p.xstar)})),Kbar:String(Kbar),loads,maxErrors:Object.fromEntries(Object.entries(maxima).map(([k,v])=>[k,String(v)]))};
  const toleranceAchieved=Object.values(maxima).every(v=>v*BigInt(spec.tolerance.denominator)<=I.S*BigInt(spec.tolerance.numerator));
  record.result={status:toleranceAchieved?'certified':'tolerance-failed',branch:'loads',witness:null,toleranceAchieved};return record;
 }catch(e){if(!(e instanceof I.Unqualified))throw e;return refuse('unresolved','certificate-'+e.code);}
}
module.exports={solve};
