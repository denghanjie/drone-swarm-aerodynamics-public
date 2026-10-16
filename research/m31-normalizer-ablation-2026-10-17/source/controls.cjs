'use strict';
// Frozen synthetic probes. This module is imported only in the supervised kernel.
const R=require('./baseline/rational.cjs'),I=require('./baseline/interval.cjs'),M=require('./baseline/methods.cjs');
const rq=(n,d=1)=>R.q(BigInt(n),BigInt(d));
function lifetimeInputs(){
 const {a,b}=require('./lifetime-config.json');return [M.makeInput(a),M.makeInput(b)];
}
function run(arm){
 if(!['baseline','candidate'].includes(arm))throw Error('Unknown arm');
 const P=require('./'+arm+'/pair-prepared.cjs'),rows=[];let access=[];
 const fresh=()=>arm==='candidate'?P.createQuery():P.query;
 function object(label,z,forces){
  const o={center:[rq(0),rq(0),rq(z,100)],axis:[rq(0),rq(0),rq(1)],points:Array.from({length:4},()=>[rq(0),rq(0),rq(z,100)])};
  Object.defineProperty(o,'forces',{get(){access.push(label);return typeof forces==='function'?forces():forces;}});return o;
 }
 const f0=[5,6,7,8].map(n=>rq(n,100)),f1=[9,10,11,12].map(n=>rq(n,100)),p0f=[6,7,8,9].map(n=>rq(n,100)),p1f=[10,11,12,13].map(n=>rq(n,100));
 function call(group,k,q,p,s,r){
  access=[];let result=null,error=null;
  try{result=q(p,s,r);}catch(e){error={name:e.name,message:e.message};}
  rows.push({name:group+'-'+k,group,ordinal:rows.length+1,result,error,access:[...access]});
 }
 {
  const q=fresh(),p=object('n:p0',100,p0f),ss=[object('b:s0',150,f0),object('b:s1',150,f1)];
  for(let k=0;k<6;k++)call('source-key',k,q,p,ss[k%2],0);
 }
 {
  const q=fresh(),s=object('b:s0',150,f0),ps=[object('n:p0',100,p0f),object('n:p1',100,p1f)];
  for(const [k,a] of [[0,0],[0,1],[1,0],[1,1],[0,0],[0,1]].entries())call('receiver-rotor-key',k,q,ps[a[0]],s,a[1]);
 }
 {
  const q=fresh(),bomb=()=>{throw Error('early-normalizer-access');};
  const p=object('n:early',100,bomb);
  for(let k=0;k<4;k++){
   const s=object('b:early',k===1?50:k===3?105:150,bomb);
   if(k===0)s.center[0]=rq(4);if(k===2)s.center[0]=rq(258);
   call('early',k,q,p,s,0);
  }
 }
 {
  const q=fresh();let attempts=0;
  const s=object('b:retry',150,()=>{if(attempts++<2)throw new I.Unqualified('fixture-beta');return f0;}),p=object('n:p0',100,p0f);
  for(let k=0;k<4;k++)call('beta-retry',k,q,p,s,0);
 }
 {
  const q=fresh();let attempts=0;
  const s=object('b:s0',150,f0),p=object('n:retry',100,()=>{if(attempts++<2)throw new I.Unqualified('fixture-nu');return p0f;});
  for(let k=0;k<4;k++)call('nu-retry',k,q,p,s,0);
 }
 {
  const q=fresh();let phase=0;
  const s=object('b:unexpected',150,()=>{if(phase<2)throw Error('fixture-beta');return f0;}),p=object('n:unexpected',100,()=>{throw Error('fixture-nu');});
  for(;phase<4;phase++)call('unexpected',phase,q,p,s,0);
 }
 {
  const q=fresh(),p=object('n:p0',100,p0f),huge=object('b:huge',150,Array.from({length:4},()=>rq('10000000000000000000000000000000000000000')));
  const tiny=object('n:tiny',100,Array.from({length:4},()=>rq(1,'1'+'0'.repeat(300)))),s=object('b:s0',150,f0);
  call('later-refusal',0,q,p,huge,0);call('later-refusal',1,q,p,huge,0);
  call('later-refusal',2,q,tiny,s,0);call('later-refusal',3,q,tiny,s,0);
 }
 if(rows.length!==32)throw Error('Direct query allocation mismatch');return {schema:'m31-normalizer-direct-v1',arm,synthetic:true,rows};
}
module.exports={run,lifetimeInputs};
