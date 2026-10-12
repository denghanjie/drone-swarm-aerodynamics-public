'use strict';
const dot=(a,b)=>a.reduce((z,x,k)=>z+x*b[k],0);
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
