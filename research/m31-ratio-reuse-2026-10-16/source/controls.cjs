'use strict';
const A=require('./adapter.cjs'),F=require('../../../outputs/step02c-source/physics.cjs');
const inherited=require('../../m31-force-ablation-2026-10-16/source/controls.cjs');
function controls(config){
 const h=A.nominalHover,q=[Math.sin(.1),0,0,Math.cos(.1)],s=[0,0,4,0.1,-.2,.05,...q,.2,-.1,.3,h,.9*h,1.1*h,.95*h],u=[h,h,h,h],records=[];
 const cache=Object.freeze({index:0,t:0,ratios:Object.freeze([Object.freeze([1,1,1,1])])});
 const e=A.cached([s],[u],cache,.005,()=>{},config),d=F.derivative(s,u);
 records.push({id:'identity-ratios',states:[s],commands:[u],cache,t:.005,actual:e,nominalDerivative:d,pass:JSON.stringify(e.derivatives[0])===JSON.stringify(d)&&e.corrections[0].force.every(x=>x===0)&&e.corrections[0].torque.every(x=>x===0)});
 const mixed=Object.freeze({index:0,t:0,ratios:Object.freeze([Object.freeze([.8,.9,.85,.95])])}),a=A.cached([s],[u],mixed,.005,()=>{},config),s2=s.slice();for(let r=13;r<17;r++)s2[r]*=1.1;const b=A.cached([s2],[u],mixed,.005,()=>{},config);
 const error=Math.max(...b.forces[0].map((x,r)=>Math.abs(x-1.1*a.forces[0][r])));
 records.push({id:'current-nominal-scaling',states:[s],changedStates:[s2],commands:[u],cache:mixed,t:.005,actual:a,changed:b,maxScalingError:error,cacheUnchanged:JSON.stringify(mixed.ratios)==='[[0.8,0.9,0.85,0.95]]',pass:error<1e-14&&JSON.stringify(mixed.ratios)==='[[0.8,0.9,0.85,0.95]]'});
 const guards=[];for(const t of [-.001,.0101]){let rejected=false;try{A.cached([s],[u],mixed,t,()=>{},config);}catch(e){rejected=e.message==='cache age outside interval';}guards.push({t,rejected});}
 records.push({id:'cache-age-rejection',guards,pass:guards.every(x=>x.rejected)});
 const invalid=[];for(const key of ['time','cacheTime','index']){let rejected=false;try{A.cached([s],[u],key==='cacheTime'?{...mixed,t:NaN}:key==='index'?{...mixed,index:NaN}:mixed,key==='time'?NaN:.005,()=>{},config);}catch(e){rejected=e.message==='missing cache';}invalid.push({key,rejected});}records.push({id:'nonfinite-cache-rejection',guards:invalid,pass:invalid.every(x=>x.rejected)});
 const prior=inherited.controls();return {pass:prior.pass&&records.every(x=>x.pass),inherited:prior,records};
}
module.exports={controls};
