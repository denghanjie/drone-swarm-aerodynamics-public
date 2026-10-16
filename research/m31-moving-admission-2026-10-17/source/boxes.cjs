'use strict';
// Exact rational interval arithmetic: no native-rounded geometry bounds.
const R=require('./rational.cjs');
const min=xs=>xs.reduce((a,b)=>R.cmp(a,b)<=0?a:b),max=xs=>xs.reduce((a,b)=>R.cmp(a,b)>=0?a:b);
const point=q=>[q,q],add=(a,b)=>[R.add(a[0],b[0]),R.add(a[1],b[1])],sub=(a,b)=>[R.sub(a[0],b[1]),R.sub(a[1],b[0])];
function mul(a,b){const p=[R.mul(a[0],b[0]),R.mul(a[0],b[1]),R.mul(a[1],b[0]),R.mul(a[1],b[1])];return [min(p),max(p)];}
const scale=(a,b)=>mul(a,point(b)),dividePositive=(a,b)=>{if(R.cmp(b,R.zero)<=0)throw Error('nonpositive box divisor');return [R.div(a[0],b),R.div(a[1],b)];};
const sum=xs=>xs.reduce(add,point(R.zero)),dot=(a,b)=>sum(a.map((v,k)=>mul(v,b[k]))),difference=(a,b)=>a.map((v,k)=>sub(v,b[k]));
const absMax=a=>max(a.map(R.abs)),absMin=a=>R.cmp(a[0],R.zero)<=0&&R.cmp(a[1],R.zero)>=0?R.zero:min(a.map(R.abs));
const normUpper2=a=>R.sum(a.map(v=>R.sq(absMax(v)))),normLower2=a=>R.sum(a.map(v=>R.sq(absMin(v))));
const bounds=points=>[0,1,2].map(k=>[min(points.map(p=>p[k])),max(points.map(p=>p[k]))]);
const wireQ=q=>({n:String(q.n),d:String(q.d)}),wire=a=>a.map(v=>v.map(wireQ));
module.exports={point,add,sub,mul,scale,dividePositive,sum,dot,difference,absMax,absMin,normUpper2,normLower2,bounds,wire};
