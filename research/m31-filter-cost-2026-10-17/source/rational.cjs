'use strict';
// Exact rational branch predicates over the supplied dyadic model operands.
function gcd(a,b){if(a<0n)a=-a;while(b){const t=a%b;a=b;b=t;}return a;}
function q(n,d=1n){if(d===0n)throw Error('zero rational denominator');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return {n:n/g,d:d/g};}
const add=(a,b)=>q(a.n*b.d+b.n*a.d,a.d*b.d),sub=(a,b)=>q(a.n*b.d-b.n*a.d,a.d*b.d),mul=(a,b)=>q(a.n*b.n,a.d*b.d),div=(a,b)=>q(a.n*b.d,a.d*b.n);
const cmp=(a,b)=>{const v=a.n*b.d-b.n*a.d;return v<0n?-1:v>0n?1:0;};
const sq=a=>mul(a,a),abs=a=>q(a.n<0n?-a.n:a.n,a.d),zero=q(0n),one=q(1n);
function fromBits(bits){const b=BigInt('0x'+bits),e=Number((b>>52n)&2047n),f=b&((1n<<52n)-1n);if(e===2047)throw Error('nonfinite rational');let n=e===0?f:(1n<<52n)+f;if(b>>63n)n=-n;const power=e===0?-1074:e-1075;return power>=0?q(n<<BigInt(power)):q(n,1n<<BigInt(-power));}
const sum=xs=>xs.reduce(add,zero),dot=(a,b)=>sum(a.map((v,i)=>mul(v,b[i]))),vecSub=(a,b)=>a.map((x,i)=>sub(x,b[i]));
function toInterval(a,k){const n=a.n*k.S;let l=n/a.d;if(n<0n&&n%a.d)l--;let u=n/a.d;if(n>0n&&n%a.d)u++;return k.interval(l,u);}
module.exports={q,add,sub,mul,div,cmp,sq,abs,zero,one,fromBits,sum,dot,vecSub,toInterval};
