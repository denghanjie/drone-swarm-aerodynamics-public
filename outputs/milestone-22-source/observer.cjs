'use strict';
// Visibility is determined at measurement time, before prediction. No hidden neighbors
// are introduced by querying a globally extrapolated snapshot.
function localObservation(i,snapshot,age,estimator='raw'){
 if(!['raw','predict'].includes(estimator)||!Number.isFinite(age)||age<0)throw Error('Invalid observer');
 const own=snapshot[i],indices=[];for(let j=0;j<snapshot.length;j++)if(i===j||Math.hypot(...own.slice(0,3).map((x,k)=>x-snapshot[j][k]))<1.8)indices.push(j);
 const states=indices.map(j=>{const q=snapshot[j];if(estimator==='raw'||age===0)return q;const p=q.slice();for(let k=0;k<3;k++)p[k]+=age*q[k+3];return p;});
 return {states,index:indices.indexOf(i),indices};
}
module.exports={localObservation};
