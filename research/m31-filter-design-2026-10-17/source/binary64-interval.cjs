'use strict';
// Prospective implementation; no numerical allocation is authorized by this file.
// Correctness assumes ECMAScript binary64 basic-operation semantics, gradual
// underflow, and no reassociation/fusion of this explicit expression graph.
class Fallback extends Error { constructor(reason) { super(reason); this.reason=reason; } }
const memory=new DataView(new ArrayBuffer(8));
function finite(x) { if(typeof x!=='number'||!Number.isFinite(x))throw new Fallback('nonfinite');return x; }
function nextUp(x) {
 finite(x); if(x===0)return Number.MIN_VALUE;
 memory.setFloat64(0,x,false);
 let hi=memory.getUint32(0,false),lo=memory.getUint32(4,false);
 if(x>0){ if(lo===0xffffffff){lo=0;hi++;}else lo++; }
 else { if(lo===0){lo=0xffffffff;hi--;}else lo--; }
 memory.setUint32(0,hi,false);memory.setUint32(4,lo,false);
 return memory.getFloat64(0,false);
}
const nextDown=x=>-nextUp(-finite(x));
function interval(l,u){finite(l);finite(u);if(l>u)throw new Fallback('invalid-interval');return {l,u};}
const point=x=>interval(x,x);
function check(a){if(!a||typeof a!=='object')throw new Fallback('invalid-interval');return interval(a.l,a.u);}
const lower=x=>finite(nextDown(finite(x))),upper=x=>finite(nextUp(finite(x)));
function add(a,b){a=check(a);b=check(b);return interval(lower(a.l+b.l),upper(a.u+b.u));}
function sub(a,b){a=check(a);b=check(b);return interval(lower(a.l-b.u),upper(a.u-b.l));}
function mul(a,b){a=check(a);b=check(b);const p=[a.l*b.l,a.l*b.u,a.u*b.l,a.u*b.u];p.forEach(finite);return interval(lower(Math.min(...p)),upper(Math.max(...p)));}
function div(a,b){a=check(a);b=check(b);if(b.l<=0&&b.u>=0)throw new Fallback('zero-denominator');const p=[a.l/b.l,a.l/b.u,a.u/b.l,a.u/b.u];p.forEach(finite);return interval(lower(Math.min(...p)),upper(Math.max(...p)));}
function square(a){a=check(a);const p=[a.l*a.l,a.u*a.u];p.forEach(finite);return interval(a.l<=0&&a.u>=0?0:lower(Math.min(...p)),upper(Math.max(...p)));}
const sum=xs=>xs.reduce(add,point(0)),dot=(a,b)=>sum(a.map((v,k)=>mul(v,b[k]))),norm2=a=>sum(a.map(square)),difference=(a,b)=>a.map((v,k)=>sub(v,b[k]));
function ge(a,b){a=check(a);b=check(b);return a.l>=b.u?true:a.u<b.l?false:null;}
function gt(a,b){a=check(a);b=check(b);return a.l>b.u?true:a.u<=b.l?false:null;}
const le=(a,b)=>ge(b,a),lt=(a,b)=>gt(b,a);
function boundedAbs(a,n){a=check(a);finite(n);if(n<0)throw new Fallback('invalid-absolute-bound');return a.l>=-n&&a.u<=n;}
function fromBits(word){if(typeof word!=='string'||!/^[0-9a-f]{16}$/.test(word))throw new Fallback('invalid-word');memory.setUint32(0,parseInt(word.slice(0,8),16),false);memory.setUint32(4,parseInt(word.slice(8),16),false);return point(memory.getFloat64(0,false));}
module.exports={Fallback,nextUp,nextDown,interval,point,fromBits,add,sub,mul,div,square,sum,dot,norm2,difference,ge,gt,le,lt,boundedAbs};
