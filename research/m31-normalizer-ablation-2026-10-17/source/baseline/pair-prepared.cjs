'use strict';
const I=require('./interval.cjs'),R=require('./rational.cjs'),A=require('./adapter.cjs');
const C=A.exact,iq=q=>R.toInterval(q,I),ic=n=>iq(R.q(BigInt(n))),Z=ic(0),ONE=ic(1);
const bounds=xs=>Object.fromEntries(Object.entries(xs).map(([k,v])=>[k,I.encode(v)]));
const zero=branch=>({status:'zero',branch,intervals:bounds({K:Z,coefficient:Z})});
const rejected=branch=>({status:'rejected',branch});
const le=(x,y)=>R.cmp(x,y)<=0,ge=(x,y)=>R.cmp(x,y)>=0,gt=(x,y)=>R.cmp(x,y)>0,lt=(x,y)=>R.cmp(x,y)<0;
function maxAbs(v,n){return v.some(x=>gt(R.abs(x),R.q(BigInt(n))));}
// Fade is monotone on the entire real line. Evaluate endpoint values with
// directed intervals; exact endpoint branch choices avoid crossing errors.
function fadePoint(v,start,end){if(v<=start.l)return ONE;if(v>=end.u)return Z;const t=I.div(I.sub(I.interval(v,v),start),I.sub(end,start));return I.mul(I.square(I.sub(ONE,t)),I.add(ONE,I.mul(ic(2),t)));}
function fade(v,start,end){const lo=fadePoint(v.u,start,end),hi=fadePoint(v.l,start,end);return I.interval(lo.l,hi.u);}
// Prepared exact dyadic geometry is validated/cached once per method before queries.
function query(p,s,rotor){const out=result=>result;const rc=p.center,sc=s.center,dc=R.vecSub(sc,rc);if(maxAbs(dc,257)||gt(R.dot(dc,dc),R.q(512n*512n)))return out(rejected('center-guard'));if(ge(R.dot(dc,dc),R.sq(C.neighbor)))return out(zero('neighbor'));
 const d=R.vecSub(sc,p.points[rotor]),axis=s.axis;if(maxAbs(d,258))return out(rejected('rotor-guard'));const down=R.dot(d,axis);if(gt(R.abs(down),R.q(1024n)))return out(rejected('down-guard'));if(le(down,R.zero))return out(zero('upstream'));if(ge(down,C.downCut))return out(zero('down-cut'));
 const e=d.map((x,i)=>R.sub(x,R.mul(down,axis[i]))),r2=R.dot(e,e);if(gt(r2,R.q(2048n*2048n)))return out(rejected('radial-guard'));if(lt(down,R.mul(C.minDown,C.D)))return out(lt(r2,R.sq(C.nearRad))?rejected('near'):zero('near-outside'));
 const nd=R.div(down,C.D),base=R.sub(nd,C.origin),width=R.mul(R.mul(C.spread,base),C.D);if(le(width,R.zero))return out(rejected('width'));if(ge(r2,R.sq(R.mul(C.radCut,width))))return out(zero('radial'));
 const rawProjection=R.dot(p.axis,axis),projection=gt(rawProjection,R.zero)?rawProjection:R.zero;if(le(projection,R.zero))return out(zero('projection'));
 try{
  // xi^2 = radial^2 / width^2 exactly, retaining actual near-unit axes.
  const xi2=R.div(r2,R.sq(width)),den=R.add(R.one,R.mul(C.kappa,xi2));
  const profile=R.mul(R.div(R.div(C.decay,base),R.sq(den)),R.mul(C.induced,projection));
  const radial=I.sqrt(iq(r2));
  const K=I.mul(I.mul(iq(profile),fade(iq(down),iq(C.downFade),iq(C.downCut))),fade(I.div(radial,iq(width)),iq(C.radFade),iq(C.radCut)));
  const nominal=R.sum(s.forces),beta=I.sqrt(iq(R.div(nominal,C.mg))),nu=I.sqrt(iq(R.div(p.forces[rotor],R.mul(R.mul(R.q(2n),C.rho),C.A))));
  const scaledK=I.mul(K,beta),cap=ic(128);
  if(K.l>cap.u||scaledK.l>cap.u)return out(rejected('cap'));
  if(K.l<0n||K.u>cap.l||scaledK.u>cap.l)return out({status:'unresolved',branch:'cap'});
  if(nu.l<=0n)return out({status:'unresolved',branch:'normalizer'});
  return out({status:'positive',branch:'active',intervals:bounds({K,scaledK,beta,nu,coefficient:I.div(scaledK,nu)})});
 }catch(error){if(!(error instanceof I.Unqualified))throw error;return out({status:'unresolved',branch:error.code});}
}
module.exports={query};
