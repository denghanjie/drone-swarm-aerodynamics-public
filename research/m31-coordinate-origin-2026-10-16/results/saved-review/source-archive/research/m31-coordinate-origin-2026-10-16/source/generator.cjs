'use strict';
// STATIC SOURCE ONLY. No seed, input, trigonometry, or reference value is evaluated on import.
const SHAPE=Object.freeze([20,25,10]);
const SHIFT=Object.freeze([64,-32,16]);
const RECEIVER_IDS=Object.freeze([749,500,2250,4750]);
function chargeWork(charge,name,n=1){if(charge)charge(name,n);}
function requireThat(ok,message){if(!ok)throw Error(message);}
function units64(value){const b=Buffer.alloc(8);b.writeDoubleLE(value);const u=b.readBigUInt64LE(),e=Number(u>>52n&2047n),f=u&((1n<<52n)-1n);requireThat(e!==2047,'Finite dyadic required');const m=e===0?f:((1n<<52n)|f)<<BigInt(e-1);return u>>63n?-m:m;}
function quaternion(roll,pitch,yaw){const cr=Math.cos(roll/2),sr=Math.sin(roll/2),cp=Math.cos(pitch/2),sp=Math.sin(pitch/2),cy=Math.cos(yaw/2),sy=Math.sin(yaw/2);return [sr*cp*cy-cr*sp*sy,cr*sp*cy+sr*cp*sy,cr*cp*sy-sr*sp*cy,cr*cp*cy+sr*sp*sy];}
function generateFresh(sourceCommit,charge){
  requireThat(typeof sourceCommit==='string'&&/^[0-9a-f]{40}$/.test(sourceCommit),'Published source commit must be exactly 40 lowercase hex digits');
  chargeWork(charge,'generationSeedHashes');
  const digest=require('node:crypto').createHash('sha256').update('m31-coordinate-origin-v1\n'+sourceCommit+'\n','utf8').digest();
  const seed=digest.readUInt32LE(0);requireThat(seed!==608897,'Historical seed forbidden: stop this frozen campaign without redraw or replacement commit');let rng=seed,draws=0;
  function next(){chargeWork(charge,'generationRandomWords');draws++;rng=(rng+0x6d2b79f5)>>>0;let t=rng;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return (t^(t>>>14))>>>0;}
  const canonical=[],translated=[],canonicalNumerators=new Int32Array(15000),translatedNumerators=new Int32Array(15000),angleTicks=new Int32Array(15000),angles=new Float64Array(15000),translationResiduals=new Float64Array(15000);
  let exactTranslationCount=0,canonicalF32ExactCount=0;const f0=.027*9.81/4;
  for(let z=0;z<10;z++)for(let y=0;y<25;y++)for(let x=0;x<20;x++){
    chargeWork(charge,'generationStates');const node=canonical.length,indices=[x,y,z],p=[],tp=[];
    for(let axis=0;axis<3;axis++){
      const jitter=(next()%16385)-8192,num=131072*(2*indices[axis]-(SHAPE[axis]-1))+jitter,tnum=num+SHIFT[axis]*1048576,k=3*node+axis;
      chargeWork(charge,'generationCoordinateCertificates');
      requireThat(Number.isSafeInteger(num)&&Number.isSafeInteger(tnum)&&Math.abs(num)<4194304&&Math.abs(tnum)<134217728,'Frozen numerator bound');
      canonicalNumerators[k]=num;translatedNumerators[k]=tnum;p[axis]=num/1048576;tp[axis]=tnum/1048576;
      const residual=units64(tp[axis])-units64(p[axis])-units64(SHIFT[axis]);
      translationResiduals[k]=tp[axis]-p[axis]-SHIFT[axis];
      requireThat(residual===0n&&translationResiduals[k]===0,'Exact translation certificate');exactTranslationCount++;
      requireThat(Math.fround(p[axis])===p[axis],'Canonical exact binary32 certificate');canonicalF32ExactCount++;
    }
    for(let axis=0;axis<3;axis++){
      const word=next(),sign=(word&0x80000000)?-1:1,min=axis<2?131072:65536,span=axis<2?262145:11665409,k=3*node+axis;
      angleTicks[k]=sign*(min+((word&0x7fffffff)%span));angles[k]=(angleTicks[k]/65536)*Math.PI/180;
    }
    chargeWork(charge,'generationQuaternions');const q=quaternion(angles[3*node],angles[3*node+1],angles[3*node+2]);
    const s=[...p,0,0,0,...q,0,0,0,f0,f0,f0,f0],t=s.slice();t.splice(0,3,...tp);canonical.push(s);translated.push(t);
  }
  return {statesByOrigin:[canonical,translated],receiverIds:Uint32Array.from(RECEIVER_IDS),canonicalNumerators,translatedNumerators,angleTicks,angles,translationResiduals,audit:{sourceCommit,seedDomain:'m31-coordinate-origin-v1\n',seedDigestHex:digest.toString('hex'),seedWordLE:seed,randomAlgorithm:'Mulberry32 uint32; zero seed accepted; fixed modulo mapping; historical seed608897 stops campaign without redraw',randomWords:draws,shape:[...SHAPE],order:'z then y then x; ID=(z*25+y)*20+x',positionDenominator:1048576,jitterNumeratorMin:-8192,jitterNumeratorMax:8192,origins:[[0,0,0],[...SHIFT]],receiverIds:[...RECEIVER_IDS],receiverStrata:[[9,12,1],[0,0,1],[10,12,4],[10,12,9]],exactTranslationCount,canonicalF32ExactCount,angleTickDenominator:65536,rollPitchMagnitudeTicks:[131072,393216],yawMagnitudeTicks:[65536,11730944],noRejectionOrReplacement:true}};
}
module.exports={generateFresh};
