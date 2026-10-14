'use strict';
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
function boxDistance(p,b){const d=p.map((x,k)=>x< b.min[k]?x-b.min[k]:x>b.max[k]?x-b.max[k]:0),n=Math.hypot(...d);if(n>0)return {distance:n,normal:d.map(x=>x/n)};
 let best=Infinity,normal=[0,0,0];for(let k=0;k<3;k++)for(const sign of [-1,1]){const distance=sign<0?p[k]-b.min[k]:b.max[k]-p[k];if(distance<best){best=distance;normal=[0,0,0];normal[k]=sign;}}return {distance:-best,normal};}
// Exact Euclidean distance from a straight segment to an axis-aligned solid box.
function segmentBoxDistance(a,b,box){const d=b.map((x,k)=>x-a[k]),cuts=[0,1];for(let k=0;k<3;k++)if(d[k])for(const face of [box.min[k],box.max[k]]){const t=(face-a[k])/d[k];if(t>0&&t<1)cuts.push(t);}cuts.sort((a,b)=>a-b);let best=Infinity;
 for(let j=0;j<cuts.length-1;j++){const lo=cuts[j],hi=cuts[j+1],mid=(lo+hi)/2;let aa=0,ab=0;for(let k=0;k<3;k++){const x=a[k]+mid*d[k];if(x<box.min[k]||x>box.max[k]){const face=x<box.min[k]?box.min[k]:box.max[k],q=a[k]-face;aa+=d[k]*d[k];ab+=q*d[k];}}const t=clamp(aa?-ab/aa:mid,lo,hi),p=a.map((x,k)=>x+t*d[k]);best=Math.min(best,Math.max(0,boxDistance(p,box).distance));}return best;}
function segmentPair(a,b,c,d){const r=a.slice(0,3).map((x,k)=>x-c[k]),v=b.slice(0,3).map((x,k)=>x-a[k]-d[k]+c[k]),vv=v.reduce((s,x)=>s+x*x,0),t=clamp(vv?-r.reduce((s,x,k)=>s+x*v[k],0)/vv:0,0,1);return Math.hypot(...r.map((x,k)=>x+t*v[k]));}
module.exports={boxDistance,segmentBoxDistance,segmentPair};
