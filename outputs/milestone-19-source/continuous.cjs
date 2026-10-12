'use strict';
const P=Object.freeze({neighborRadius:1.8,neighborFade:1.3,sepRadius:.85,alignment:2,cohesion:.22,cruise:.65,maxSpeed:.9,horizon:.4,margin:.25,filterHorizon:1.2,iterations:6,neighborMargin:.38});
const norm=a=>Math.hypot(...a),clamp=(x,l,h)=>Math.max(l,Math.min(h,x)),smooth=(l,h,x)=>{const t=clamp((x-l)/(h-l),0,1);return t*t*(3-2*t)},limit=v=>{const n=norm(v);return v.map(x=>x*Math.min(1,P.maxSpeed/Math.max(n,1e-9)))};
function base(i,states,course,retain=false,inset=false){const s=states[i],v=s.slice(3,6),speed=norm(v),a=v.map(x=>1.2*(P.cruise-speed)*x/Math.max(speed,.01)),social=[0,0,0],sep=[0,0,0];let weight=0,behind=0;
 for(let j=0;j<states.length;j++){if(i===j)continue;const q=states[j],delta=q.slice(0,3).map((x,k)=>x-s[k]),d=norm(delta),w=1-smooth(P.neighborFade,P.neighborRadius,d);if(!w)continue;weight+=w;behind+=w*Math.max(0,-delta[0]);for(let k=0;k<3;k++){social[k]+=w*(P.alignment*(q[3+k]-v[k])+(retain?.34:P.cohesion)*delta[k]);if(d<P.sepRadius&&d>1e-9)sep[k]-=1.5*(1/d-1/P.sepRadius)*delta[k]/d;}}
 for(let k=0;k<3;k++)a[k]+=sep[k]+social[k]/Math.max(1,weight);
 let desired=[.55,0,0];
 if(course.spheres){let target=course.route[0].slice();for(let j=0;j<course.route.length-1;j++){const p=course.route[j],q=course.route[j+1],w=smooth(p[0]-.5,p[0]+.5,s[0]);for(let k=1;k<3;k++)target[k]=target[k]*(1-w)+q[k]*w;}desired[1]=clamp(.7*(target[1]-s[1]),-.55,.55);desired[2]=clamp(.7*(target[2]-s[2]),-.55,.55);for(const o of course.spheres){const d=s.slice(0,3).map((x,k)=>x-o.center[k]),n=norm(d),clear=n-o.radius-.075;if(clear<1.2){const closing=Math.max(0,-v.reduce((a,x,k)=>a+x*d[k]/Math.max(n,1e-9),0));const fade=1-smooth(1,1.2,clear);for(let k=0;k<3;k++)a[k]+=fade*(2*Math.max(0,1.2-clear)+2*closing)*d[k]/Math.max(n,1e-9);}}}
 else{
  // Smooth partition of map guidance between successive gates; no per-drone state machine.
  let remaining=1,forward=0;desired[1]=desired[2]=0;
  for(const g of course.gates){const x=s[0]-g.center[0],passed=smooth(.4,1.1,x),w=remaining*(1-passed),edge=g.width/2-(inset?.35:.25),y=s[1]-g.center[1],z=s[2]-g.center[2],ey=clamp(y,-edge,edge)-y,ez=clamp(z,-edge,edge)-z,approach=smooth(-3,-1.5,x),slow=1/(1+(ey/.35)**2+(ez/.35)**2);forward+=w*.55*(1-approach+approach*slow);desired[1]+=w*clamp(ey,-.6,.6);desired[2]+=w*clamp(ez,-.6,.6);remaining*=passed;}
  desired[0]=forward+remaining*.55;
 }
 // Local retention slows a leading drone when its visible neighborhood trails behind.
 if(retain&&weight>0)desired[0]*=1-.85*smooth(.35,.85,behind/Math.max(1,weight));
 for(let k=0;k<3;k++)a[k]+=1.3*(desired[k]-v[k]);if(s[2]<1.5)a[2]+=3*(1.5-s[2])+2*Math.max(0,-v[2]);return limit(v.map((x,k)=>x+P.horizon*a[k]));
}
function obstacle(s,input,course){let out=input.slice();if(course.gates)for(const g of course.gates){const x=s[0]-g.center[0],w=smooth(-2.6,-1.8,x)*(1-smooth(.5,1,x));if(w<=0)continue;const edge=g.width/2-P.margin,arrival=clamp(-x/Math.max(.15,s[3]),.3,2);let risk=0;
 for(const k of [1,2]){const q=s[k]-g.center[k],bounded=clamp(out[k],-(edge+q)/P.filterHorizon,(edge-q)/P.filterHorizon);out[k]+=(bounded-out[k])*w;risk=Math.max(risk,smooth(-.18,.05,Math.max(Math.abs(q+arrival*s[3+k]),Math.abs(q))-edge));}
 const front=1-smooth(-.1,.15,x),upper=Math.max(0,-x-.35)/P.filterHorizon;out[0]+=w*risk*front*(Math.min(out[0],upper)-out[0]);}
 if(course.spheres)for(const o of course.spheres){const d=s.slice(0,3).map((v,k)=>v-o.center[k]),n=norm(d),normal=d.map(v=>v/Math.max(n,1e-9)),clear=n-o.radius-.075,w=1-smooth(.9,1.2,clear),radial=out.reduce((a,v,k)=>a+v*normal[k],0),lower=-(clear-.25)/P.filterHorizon;if(radial<lower)for(let k=0;k<3;k++)out[k]+=w*(lower-radial)*normal[k];}return limit(out);}
function filter(i,states,input,course){let out=input.slice();const s=states[i];for(let it=0;it<P.iterations;it++){out=obstacle(s,out,course);for(let j=0;j<states.length;j++){if(i===j)continue;const q=states[j],delta=s.slice(0,3).map((v,k)=>v-q[k]),d=norm(delta),w=1-smooth(1.1,1.5,d);if(w<=0||d<1e-9)continue;const n=delta.map(v=>v/d),lower=q.slice(3,6).reduce((a,v,k)=>a+v*n[k],0)-(d-P.neighborMargin)/P.filterHorizon,radial=out.reduce((a,v,k)=>a+v*n[k],0);if(radial<lower)for(let k=0;k<3;k++)out[k]+=w*(lower-radial)*n[k];}out=limit(out);}return obstacle(s,out,course);}
module.exports={P,base,filter,obstacle,smooth};
