const D=require('./pair.cjs');
// Minimal 16-coordinate chart: position, velocity, quaternion vector (positive scalar), body rates, motors.
function pack(y){return [...y.slice(0,9),...y.slice(10)];}
function unpack(x){const qv=x.slice(6,9),v=1-qv.reduce((a,b)=>a+b*b,0);if(v<=0)throw Error('Invalid chart');return [...x.slice(0,9),Math.sqrt(v),...x.slice(9)];}
function map(x,c,gains,dt=.005){const s=new D.Simulation({...c,gains,dt});s.y=unpack(x);const u=s.command().u;let y=s.y;for(let i=0;i<Math.round(.01/dt);i++)y=D.pairIntegrate(y,u,dt,s);return pack(y);}
function jac(f,x,h=1e-5){const a=Array.from({length:x.length},()=>[]);for(let j=0;j<x.length;j++){let xp=x.slice(),xm=x.slice();xp[j]+=h;xm[j]-=h;const p=f(xp),m=f(xm);for(let i=0;i<x.length;i++)a[i][j]=(p[i]-m[i])/(2*h);}return a;}
function solve(a,b){a=a.map((r,i)=>[...r,b[i]]);const n=b.length;for(let j=0;j<n;j++){let k=j;for(let i=j+1;i<n;i++)if(Math.abs(a[i][j])>Math.abs(a[k][j]))k=i;[a[k],a[j]]=[a[j],a[k]];if(Math.abs(a[j][j])<1e-14)throw Error('Singular');const v=a[j][j];for(let c=j;c<=n;c++)a[j][c]/=v;for(let i=0;i<n;i++)if(i!==j){const v=a[i][j];for(let c=j;c<=n;c++)a[i][c]-=v*a[j][c];}}return a.map(r=>r[n]);}

function root(c,gains,start){const f=x=>map(x,c,gains),res=x=>f(x).map((v,i)=>v-x[i]);let x=start||pack(new D.Simulation({...c,gains}).y);for(let it=0;it<80;it++){const r=res(x);if(Math.max(...r.map(Math.abs))<1e-11)return x;const dx=solve(jac(res,x),r.map(v=>-v));let alpha=1,found=false;while(alpha>1e-8){try{const next=x.map((v,i)=>v+alpha*dx[i]);if(Math.hypot(...res(next))<Math.hypot(...r)){x=next;found=true;break;}}catch{}alpha/=2;}if(!found)break;}throw Error('Equilibrium did not converge');}
module.exports={pack,unpack,map,jac,solve,root};
