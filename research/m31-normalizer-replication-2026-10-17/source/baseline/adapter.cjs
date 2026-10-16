'use strict';
const spec=require('./spec.json'),R=require('./rational.cjs');
function bits(v){const b=Buffer.alloc(8);b.writeDoubleBE(v);return b.toString('hex');}
function number(b){return Buffer.from(b,'hex').readDoubleBE();}
const c=Object.fromEntries(Object.entries(spec.constants).map(([k,v])=>[k,Number(v)]));
c.PI=number(spec.PIBits);c.mg=c.mg0*c.g;c.A=(c.PI*c.radius)*c.radius;c.rt2=Math.sqrt(2);c.R=c.rt2*c.arm;c.D=2*c.R;c.induced=Math.sqrt(c.mg/((8*c.rho)*c.A));c.kappa=c.rt2-1;
const constantBits=Object.fromEntries(Object.entries(c).map(([k,v])=>[k,bits(v)]));
const exact=Object.fromEntries(Object.entries(constantBits).map(([k,v])=>[k,R.fromBits(v)]));
function cross(a,b){return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];}
function rotate(q,v){const t=cross(q,v).map(x=>2*x),u=cross(q,t);return v.map((x,k)=>x+(q[3]*t[k]+u[k]));}
function prep(s){const center=s.slice(0,3),axis=rotate(s.slice(6,10),[0,0,1]);const offsets=spec.corners.map(a=>rotate(s.slice(6,10),a.map(x=>x*c.arm)));const points=offsets.map(o=>center.map((v,i)=>v+o[i]));return {center:center.map(bits),axis:axis.map(bits),offsets:offsets.map(a=>a.map(bits)),points:points.map(a=>a.map(bits)),forces:s.slice(13,17).map(bits)};}
function normWithin(v,base,t){const n=R.dot(v,v);return R.cmp(n,R.sq(R.sub(base,t)))>=0&&R.cmp(n,R.sq(R.add(base,t)))<=0;}
function valid(s,p){if([...p.center,...p.axis,...p.offsets.flat(),...p.points.flat(),...p.forces].some(b=>!Number.isFinite(number(b))))return false;const axis=p.axis.map(R.fromBits);if(!normWithin(s.slice(6,10).map(x=>R.fromBits(bits(x))),R.one,exact.qTolerance))return false;if(!normWithin(axis,R.one,exact.geometryTolerance))return false;for(const v of p.offsets.map(a=>a.map(R.fromBits))){if(!normWithin(v,exact.R,exact.geometryTolerance)||R.cmp(R.abs(R.dot(v,axis)),exact.geometryTolerance)>0)return false;}return true;}
function prepare(input){const a=input.receiver.map(number),b=input.source.map(number);if([...a,...b].some(v=>!Number.isFinite(v)))return {prepared:null,rejection:'raw-nonfinite'};if([...a.slice(13,17),...b.slice(13,17)].some(v=>v<=0))return {prepared:null,rejection:'raw-force'};const prepared={receiver:prep(a),source:prep(b)};if(!valid(a,prepared.receiver)||!valid(b,prepared.source))return {prepared,rejection:'preparation'};return {prepared,rejection:null};}
module.exports={bits,number,c,constantBits,exact,prepare};
