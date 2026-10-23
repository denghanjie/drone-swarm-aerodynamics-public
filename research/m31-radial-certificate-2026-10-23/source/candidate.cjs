'use strict';
// Experimental distance-stage cache. Conditional theorem; not a universal F certificate.
const dv=new DataView(new ArrayBuffer(8));
function up(x){if(x===Infinity)return x;if(x===0)return Number.MIN_VALUE;dv.setFloat64(0,x,false);let b=dv.getBigUint64(0,false);dv.setBigUint64(0,x>0?b+1n:b-1n,false);return dv.getFloat64(0,false);}
const down=x=>-up(-x),lower=x=>Math.max(0,down(x));
const threshold=3+2**-20,thresholdSquared=up(threshold*threshold);
let cache=null;
function reset(){cache=null;}
function eligible(p){return p.every(x=>x.every(Number.isFinite))&&[0,1,2].every(k=>{const a=p.map(x=>x[k]),s=Math.max(...a)-Math.min(...a);return Number.isFinite(s)&&s>=0&&s<=256;});}
function certificate(boxes,i,j){const sq=[];for(let k=0;k<3;k++){const lo=boxes[j][2*k]-boxes[i][2*k+1],hi=boxes[j][2*k+1]-boxes[i][2*k],a=Math.max(0,lo,-hi);sq.push(lower(a*a));}return lower(lower(sq[0]+sq[1])+sq[2])>=thresholdSquared;}
function step(ids,p){const n=ids.length,P=n*(n-1);if(!eligible(p)||p.some(v=>v.some(x=>Math.abs(x)>2**20))){cache=null;return{action:'fallback',reason:'coordinate-domain',omitted:new Uint8Array(P),witness:null};}
 let reason=cache?(cache.ids.length!==n?'count-change':cache.ids.some((x,i)=>x!==ids[i])?'id-change':null):'cold';
 if(cache&&!reason&&p.some((v,i)=>v.some((x,k)=>x<cache.boxes[i][2*k]||x>cache.boxes[i][2*k+1])))reason='box-exit';
 if(cache&&!reason)return{action:'reuse',reason:'contained',omitted:cache.omitted,witness:null};
 cache=null;const boxes=p.map(v=>v.flatMap(x=>[down(x-.125),up(x+.125)])),omitted=new Uint8Array(P);let at=0;
 for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j)omitted[at++]=Number(certificate(boxes,i,j));
 cache={ids:ids.slice(),boxes,omitted};return{action:'build',reason,omitted,witness:{ids:ids.slice(),reference:p.map(v=>v.slice()),boxes:boxes.map(v=>v.slice()),omitted:Array.from(omitted)}};
}
module.exports={up,down,eligible,step,reset,thresholdSquared};
