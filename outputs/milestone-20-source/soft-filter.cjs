'use strict';
// Unique minimum of a strongly convex, soft half-space objective.
// This is a continuous command preference, not a flight safety certificate.
const P=Object.freeze({gateWeight:80,neighborWeight:40,sphereWeight:40,margin:.25,neighborMargin:.38,horizon:1.2,speedLimit:.9,tolerance:1e-8,maxIterations:40});
const norm=v=>Math.hypot(...v),dot=(a,b)=>a.reduce((s,v,k)=>s+v*b[k],0),clamp=(x,l,h)=>Math.max(l,Math.min(h,x));
function smooth(l,h,x){const q=clamp((x-l)/(h-l),0,1);return q*q*(3-2*q);}
function objective(v,base,cs){let value=.5*v.reduce((a,x,k)=>a+(x-base[k])**2,0);for(const c of cs){const r=Math.max(0,c.b-dot(c.n,v));value+=.5*c.w*r*r;}return value;}
function derivatives(v,base,cs){const g=v.map((x,k)=>x-base[k]),H=[[1,0,0],[0,1,0],[0,0,1]];for(const c of cs){const r=c.b-dot(c.n,v);if(r<=0)continue;for(let i=0;i<3;i++){g[i]-=c.w*r*c.n[i];for(let j=0;j<3;j++)H[i][j]+=c.w*c.n[i]*c.n[j];}}return {g,H};}
function solveSPD(A,b){const L=Array.from({length:3},()=>[0,0,0]);for(let i=0;i<3;i++)for(let j=0;j<=i;j++){let x=A[i][j];for(let k=0;k<j;k++)x-=L[i][k]*L[j][k];L[i][j]=i===j?Math.sqrt(x):x/L[j][j];}const y=[0,0,0],x=[0,0,0];for(let i=0;i<3;i++){let q=b[i];for(let k=0;k<i;k++)q-=L[i][k]*y[k];y[i]=q/L[i][i];}for(let i=2;i>=0;i--){let q=y[i];for(let k=i+1;k<3;k++)q-=L[k][i]*x[k];x[i]=q/L[i][i];}return x;}
function optimize(base,cs){let v=base.slice(),iterations=0;for(;iterations<P.maxIterations;iterations++){const {g,H}=derivatives(v,base,cs);if(norm(g)<P.tolerance)break;const d=solveSPD(H,g.map(x=>-x)),value=objective(v,base,cs),slope=dot(g,d);let alpha=1,trial;for(let j=0;j<24;j++){trial=v.map((x,k)=>x+alpha*d[k]);if(objective(trial,base,cs)<=value+1e-4*alpha*slope+1e-15)break;alpha*=.5;}v=trial;}return {solution:v,residual:norm(derivatives(v,base,cs).g),iterations,objective:objective(v,base,cs)};}
function constraints(i,states,course){const s=states[i],cs=[],add=(n,b,w,kind)=>{if(w>0)cs.push({n,b,w,kind});};
 if(course.gates)for(const gate of course.gates){const x=s[0]-gate.center[0],w=smooth(-2.6,-1.8,x)*(1-smooth(.5,1,x));if(w<=0)continue;const edge=gate.width/2-P.margin,arrival=clamp(-x/Math.max(.15,s[3]),.3,2);let risk=0;
  for(const k of [1,2]){const q=s[k]-gate.center[k],n=[0,0,0];n[k]=1;add(n,-(edge+q)/P.horizon,P.gateWeight*w,'wall');add(n.map(x=>-x),-(edge-q)/P.horizon,P.gateWeight*w,'wall');risk=Math.max(risk,smooth(-.18,.05,Math.max(Math.abs(q+arrival*s[3+k]),Math.abs(q))-edge));}
  add([-1,0,0],-Math.max(0,-x-.35)/P.horizon,P.gateWeight*w*risk*(1-smooth(-.1,.15,x)),'gate-forward');
 }
 if(course.spheres)for(const sphere of course.spheres){const d=s.slice(0,3).map((v,k)=>v-sphere.center[k]),distance=norm(d),clear=distance-sphere.radius-.075;add(d.map(x=>x/Math.max(distance,1e-9)),-(clear-P.margin)/P.horizon,P.sphereWeight*(1-smooth(.9,1.2,clear)),'sphere');}
 for(let j=0;j<states.length;j++){if(i===j)continue;const q=states[j],d=s.slice(0,3).map((v,k)=>v-q[k]),distance=norm(d),w=1-smooth(1.1,1.5,distance);if(w<=0||distance<1e-9)continue;const n=d.map(x=>x/distance);add(n,dot(q.slice(3,6),n)-(distance-P.neighborMargin)/P.horizon,P.neighborWeight*w,'neighbor');}
 return cs;
}
function filter(i,states,base,course){const cs=constraints(i,states,course),result=optimize(base,cs),length=norm(result.solution),velocity=result.solution.map(x=>x*Math.min(1,P.speedLimit/Math.max(length,1e-9)));return {...result,velocity,constraintCount:cs.length,maxViolation:Math.max(0,...cs.map(c=>c.b-dot(c.n,velocity)))};}
module.exports={P,objective,derivatives,solveSPD,optimize,constraints,filter,smooth};
