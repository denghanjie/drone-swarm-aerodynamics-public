'use strict';
// Exact historical function text; fresh source-accounting diagnostic only.
function fade(start,end,value){if(value<=start)return 1;if(value>=end)return 0;const t=(value-start)/(end-start);return (1-t)*(1-t)*(1+2*t);}

function pairTerm(p,i,j,r,c,centerAlreadyEligible=false) {
  const ib=28*i,jb=28*j,ob=ib+8+4*r;
  const out={symbol:0,term:0,down:0,radial:0,projection:0,center:0,validity:0,stage:0};
  if(i===j){out.symbol=1;out.validity=1;return out;}
  if(!centerAlreadyEligible){const dx=p[jb]-p[ib],dy=p[jb+1]-p[ib+1],dz=p[jb+2]-p[ib+2];out.center=Math.hypot(dx,dy,dz);out.validity|=16;
    if(!Number.isFinite(out.center)||out.center>512||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>257){out.symbol=11;out.stage=3;return out;}
    if(out.center>=c.neighbor){out.symbol=1;out.validity|=1;return out;}}
  const px=p[ib]+p[ob],py=p[ib+1]+p[ob+1],pz=p[ib+2]+p[ob+2];
  const dx=p[jb]-px,dy=p[jb+1]-py,dz=p[jb+2]-pz;
  if(![dx,dy,dz].every(Number.isFinite)||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>258){out.symbol=11;out.stage=4;return out;}
  const ax=p[jb+4],ay=p[jb+5],az=p[jb+6];
  const down=dx*ax+dy*ay+dz*az;out.down=down;
  if(!Number.isFinite(down)||Math.abs(down)>1024){out.symbol=11;out.stage=4;return out;}out.validity|=2;
  if(down<=0){out.symbol=2;out.validity|=1;return out;}
  if(down>=c.downCut){out.symbol=3;out.validity|=1;return out;}
  const radial=Math.hypot(dx-down*ax,dy-down*ay,dz-down*az);out.radial=radial;
  if(!Number.isFinite(radial)||radial>2048){out.symbol=11;out.stage=4;return out;}out.validity|=4;
  if(down<c.minDown*c.D){out.symbol=radial<c.nearRad?4:5;out.stage=out.symbol===4?4:0;if(out.symbol===5)out.validity|=1;return out;}
  const normalizedDown=down/c.D;
  const halfWidth=c.spread*(normalizedDown-c.origin)*c.D;
  if(!(halfWidth>0)||!Number.isFinite(halfWidth)){out.symbol=11;out.stage=4;return out;}
  if(radial>=c.radCut*halfWidth){out.symbol=6;out.validity|=1;return out;}
  const receiverProjection=Math.max(0,p[ib+4]*ax+p[ib+5]*ay+p[ib+6]*az);out.projection=receiverProjection;out.validity|=8;
  const xi=(radial/c.D)/(c.spread*(normalizedDown-c.origin));
  const denominator=1+c.sqrt2minus1*xi*xi;
  const normalizedSpeed=(c.decay/(normalizedDown-c.origin))/(denominator*denominator);
  const speed=normalizedSpeed*c.induced*fade(c.downFade,c.downCut,down)*fade(c.radFade,c.radCut,radial/halfWidth)*receiverProjection;
  if(!termAdmitted(speed)||!Number.isFinite(receiverProjection)){out.symbol=11;out.stage=4;return out;}
  out.term=speed;out.validity|=1;out.symbol=receiverProjection<=0?7:(speed>0?8:9);return out;
}

function termAdmitted(value){return Number.isFinite(value)&&value>=0&&value<=128;}

module.exports={fade,pairTerm,termAdmitted};
