'use strict';
// Endpoints denote exact integer / 2^96 values. No native transcendental premise.
const SHIFT=96n,S=1n<<SHIFT,MAX=1n<<352n;
class Unqualified extends Error{constructor(code){super(code);this.code=code;}}
function interval(l,u){
 if(typeof l!=='bigint'||typeof u!=='bigint'||l>u)throw new Unqualified('invalid-interval');
 if(l< -MAX||u>MAX)throw new Unqualified('unresolved-range');
 return Object.freeze({l,u});
}
function check(a){return interval(a?.l,a?.u);}
function floorDiv(n,d){if(d===0n)throw new Unqualified('unresolved-domain');if(d<0n){n=-n;d=-d;}let q=n/d;if(n<0n&&n%d!==0n)q--;return q;}
const ceilDiv=(n,d)=>-floorDiv(-n,d);
function fromBits(bits){
 if(typeof bits!=='string'||! /^[0-9a-f]{16}$/.test(bits))throw new Unqualified('invalid-bits');
 const v=BigInt('0x'+bits),negative=(v>>63n)!==0n,exp=(v>>52n)&2047n,frac=v&((1n<<52n)-1n);
 if(exp===2047n)throw new Unqualified('invalid-nonfinite');
 let n=exp===0n?frac:(1n<<52n)+frac;
 if(negative)n=-n;
 const e=(exp===0n?-1074n:exp-1075n)+SHIFT;
 if(e>=0n)return interval(n<<e,n<<e);
 const d=1n<<(-e);return interval(floorDiv(n,d),ceilDiv(n,d));
}
function add(a,b){a=check(a);b=check(b);return interval(a.l+b.l,a.u+b.u);}
function sub(a,b){a=check(a);b=check(b);return interval(a.l-b.u,a.u-b.l);}
function min(xs){return xs.reduce((a,b)=>a<b?a:b);}
function max(xs){return xs.reduce((a,b)=>a>b?a:b);}
function mul(a,b){a=check(a);b=check(b);const p=[a.l*b.l,a.l*b.u,a.u*b.l,a.u*b.u];return interval(floorDiv(min(p),S),ceilDiv(max(p),S));}
function div(a,b){a=check(a);b=check(b);if(b.l<=0n&&b.u>=0n)throw new Unqualified('unresolved-domain');const p=[[a.l,b.l],[a.l,b.u],[a.u,b.l],[a.u,b.u]];return interval(min(p.map(([n,d])=>floorDiv(n*S,d))),max(p.map(([n,d])=>ceilDiv(n*S,d))));}
function square(a){a=check(a);const l=a.l<=0n&&a.u>=0n?0n:min([a.l*a.l,a.u*a.u]),u=max([a.l*a.l,a.u*a.u]);return interval(floorDiv(l,S),ceilDiv(u,S));}
function isqrt(n){
 if(n<0n)throw new Unqualified('unresolved-domain');if(n<2n)return n;
 let x=1n<<BigInt(Math.ceil(n.toString(2).length/2));
 for(let i=0;i<512;i++){
  const y=(x+n/x)>>1n;
  if(y>=x){if(x*x>n||(x+1n)*(x+1n)<=n)throw new Unqualified('unresolved-sqrt-check');return x;}
  x=y;
 }
 throw new Unqualified('unresolved-iteration');
}
function sqrt(a){a=check(a);if(a.l<0n)throw new Unqualified('unresolved-domain');const low=isqrt(a.l*S),high=isqrt(a.u*S);return interval(low,high*high===a.u*S?high:high+1n);}
const encode=a=>({l:a.l.toString(),u:a.u.toString()});
function decode(a){
 const valid=x=>typeof x==='string'&&/^-?(0|[1-9][0-9]{0,106})$/.test(x);
 if(!a||!valid(a.l)||!valid(a.u))throw new Unqualified('invalid-interval');
 return interval(BigInt(a.l),BigInt(a.u));
}
module.exports={SHIFT,S,MAX,interval,fromBits,add,sub,mul,div,square,sqrt,encode,decode,Unqualified};
