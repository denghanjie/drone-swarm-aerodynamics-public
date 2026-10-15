'use strict';
// Independent bracketed scalar reference. No production/GPU imports.
// Evaluates the real polynomial in host binary64; brackets are numerical diagnostics,
// not directed-rounding interval certificates. No physical validation follows.
function solveAlpha(alpha){
 if(!Number.isFinite(alpha)||alpha<0)throw Error('Invalid alpha');
 if(alpha===0)return {alpha,x:1,lo:1,hi:1,iterations:0,residual:0};
 let lo=0,hi=1,iterations=0;
 for(;iterations<96&&hi-lo>2e-15;iterations++){
  const mid=(lo+hi)/2,value=mid*mid*mid+alpha*mid-1;
  if(value>0)hi=mid;else lo=mid;
 }
 const x=(lo+hi)/2;
 return {alpha,x,lo,hi,iterations,residual:x*x*x+alpha*x-1};
}
function powerRatio(f,f0,alpha){const x=f/f0;return x*(alpha/2+Math.sqrt(alpha*alpha/4+x));}
module.exports={solveAlpha,powerRatio};
