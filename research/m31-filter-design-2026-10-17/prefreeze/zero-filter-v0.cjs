'use strict';
const F=require('./binary64-interval.cjs');
// Call only after the unchanged adapter has admitted the complete raw input.
// Inputs are prepared binary64 words, not rounded conversions of exact rationals.
function prepare(value){return {center:value.center.map(F.fromBits),axis:value.axis.map(F.fromBits),points:value.points.map(p=>p.map(F.fromBits))};}
function constants(words){return Object.fromEntries(Object.entries(words).map(([k,v])=>[k,F.fromBits(v)]));}
function classify(receiver,source,rotor,C){
 const Z=F.point(0),stop=reason=>({kind:'fallback',reason});
 const decide=(predicate,reason)=>{if(predicate===null)throw new F.Uncertain(reason);return predicate;};
 // Deliberately catch only this module's refusal classes; programming errors fail.
 try {
  const dc=F.difference(source.center,receiver.center);
  if(!dc.every(v=>F.boundedAbs(v,257)))return stop('center-component');
  const dc2=F.norm2(dc);
  if(F.le(dc2,F.point(512*512))!==true)return stop('center-norm');
  const neighbor=F.ge(dc2,F.square(C.neighbor));
  if(neighbor===true)return {kind:'zero',branch:'neighbor'};
  if(neighbor===null)return stop('neighbor-uncertain');
  const d=F.difference(source.center,receiver.points[rotor]);
  if(!d.every(v=>F.boundedAbs(v,258)))return stop('rotor-component');
  const down=F.dot(d,source.axis);
  if(!F.boundedAbs(down,1024))return stop('down-guard');
  const upstream=F.le(down,Z);
  if(upstream===true)return {kind:'zero',branch:'upstream'};
  if(upstream===null)return stop('upstream-uncertain');
  const cut=F.ge(down,C.downCut);
  if(cut===true)return {kind:'zero',branch:'down-cut'};
  if(cut===null)return stop('down-cut-uncertain');
  const e=d.map((v,k)=>F.sub(v,F.mul(down,source.axis[k]))),r2=F.norm2(e);
  if(F.le(r2,F.point(2048*2048))!==true)return stop('radial-guard');
  const near=F.lt(down,F.mul(C.minDown,C.D));
  if(near===null)return stop('near-uncertain');
  if(near===true){if(F.ge(r2,F.square(C.nearRad))===true)return {kind:'zero',branch:'near-outside'};return stop('near-exact');}
  const base=F.sub(F.div(down,C.D),C.origin),width=F.mul(F.mul(C.spread,base),C.D);
  if(F.gt(width,Z)!==true)return stop('width');
  const radial=F.ge(r2,F.square(F.mul(C.radCut,width)));
  if(radial===true)return {kind:'zero',branch:'radial'};
  if(radial===null)return stop('radial-uncertain');
  const projection=F.le(F.dot(receiver.axis,source.axis),Z);
  if(projection===true)return {kind:'zero',branch:'projection'};
  return stop(projection===null?'projection-uncertain':'active-exact');
 }catch(e){if(e instanceof F.Fallback)return stop('arithmetic-'+e.reason);throw e;}
}
// The exact query remains the only producer of positive/rejected/unresolved data.
function query(exactQuery,exactReceiver,exactSource,fastReceiver,fastSource,rotor,C){
 const decision=classify(fastReceiver,fastSource,rotor,C);
 const result=decision.kind==='zero'?{status:'zero',branch:decision.branch,intervals:{K:{l:'0',u:'0'},coefficient:{l:'0',u:'0'}}}:exactQuery(exactReceiver,exactSource,rotor);
 return {decision,result};
}
module.exports={prepare,constants,classify,query};
