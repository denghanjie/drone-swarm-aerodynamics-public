'use strict';
const fs=require('node:fs');
const {pairTerm}=require('./reference-excerpt.cjs');
const mg=.027*9.81,arm=.028,radius=.023,rho=1.225,A=Math.PI*radius*radius,R=Math.sqrt(2)*arm;
const c={D:2*R,decay:10.11,spread:.07668,origin:-5.817,minDown:2.5,neighbor:3,nearRad:.15,downFade:2,downCut:2.5,radFade:2,radCut:3,induced:Math.sqrt(mg/(8*rho*A)),sqrt2minus1:Math.sqrt(2)-1};
const dot=(a,b)=>a.reduce((s,v,k)=>s+v*b[k],0),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],norm=a=>Math.hypot(...a),unit=a=>a.map(v=>v/norm(a));
function vehicle(id,q,axis,corner=null){
  let u=norm(cross([0,0,1],axis))>1e-12?unit(cross([0,0,1],axis)):[1,0,0],v=cross(axis,u);
  if(corner){ // Make the first (-u-v) corner equal to the prescribed direction.
    const e=unit(corner),f=cross(axis,e);u=e.map((x,k)=>(-x+f[k])/Math.sqrt(2));v=cross(axis,u);
  }
  const offsets=[[-1,-1],[1,-1],[1,1],[-1,1]].map(([s,t])=>u.map((x,k)=>arm*(s*x+t*v[k])));
  const f0=Array.from({length:4},(_,r)=>(mg/4)*(.8+.1*((id+2*r)%5)));
  return {id,q,axis,offsets,f0,S0:f0.reduce((s,x)=>s+x,0)};
}
function fixtures(){
  const level=Array.from({length:8},(_,i)=>vehicle(i,[0,0,.4*i],[0,0,1]));
  const tilted=Array.from({length:8},(_,i)=>{const b=(-1)**i*Math.PI/12;return vehicle(i,[.035*(-1)**i,.02*(i%3),.4*i],[Math.sin(b),0,Math.cos(b)]);});
  const L=2*Math.sqrt(10)*R,q=Array.from({length:6},(_,i)=>[L*Math.cos(i*Math.PI/3),L*Math.sin(i*Math.PI/3),0]);
  const hex=q.map((p,i)=>vehicle(i,p,p.map((x,k)=>3/Math.sqrt(10)*(x-q[(i+5)%6][k])/L+(k===2?1/Math.sqrt(10):0))));
  const e=Math.PI/12,near=[vehicle(0,[0,0,0],[-Math.sin(e),0,Math.cos(e)],[-Math.cos(e),0,-Math.sin(e)]),vehicle(1,[R,0,0],[Math.sin(e),0,Math.cos(e)],[Math.cos(e),0,-Math.sin(e)])];
  return [['level-ladder',level],['tilted-ladder',tilted],['hexagon-cycle',hex],['near-rejection',near]];
}
const emptyWork=()=>({rootClosures:0,bisectionIterations:0,positiveTermMultiplications:0});
function root(alpha,w){
  if(!(alpha>=0&&Number.isFinite(alpha)))throw new Error('invalid alpha');
  w.rootClosures++;
  if(alpha===0)return 1;
  let lo=0,hi=1;
  for(let k=0;k<56;k++){const x=(lo+hi)/2;if(x*x*x+alpha*x-1>0)hi=x;else lo=x;w.bisectionIterations++;}
  return (lo+hi)/2;
}
function nodeMap(i,y,vehicles,a,w){
  const rotors=a[i].map((row,r)=>{let alpha=0;for(let j=0;j<row.length;j++)if(row[j]>0){alpha+=row[j]*y[j];w.positiveTermMultiplications++;}const x=root(alpha,w);return {alpha,x,T:vehicles[i].f0[r]*x};});
  return {y:Math.sqrt(rotors.reduce((s,t)=>s+t.T,0)/vehicles[i].S0),rotors};
}
function map(y,vehicles,a,w){const rows=vehicles.map((_,i)=>nodeMap(i,y,vehicles,a,w));return {y:rows.map(v=>v.y),rotors:rows.map(v=>v.rotors)};}
const logDistance=(a,b)=>Math.max(...a.map((x,i)=>Math.abs(Math.log(x)-Math.log(b[i]))));
function runCase(id,vehicles){
  const n=vehicles.length,p=new Float64Array(28*n),errors=[];
  for(const v of vehicles){p.set(v.q,28*v.id);p.set(v.axis,28*v.id+4);for(let r=0;r<4;r++)p.set(v.offsets[r],28*v.id+8+4*r);
    if(Math.abs(norm(v.axis)-1)>1e-12||v.offsets.some(o=>Math.abs(dot(o,v.axis))>1e-12||Math.abs(norm(o)-R)>1e-12)||v.f0.some(x=>!(x>0&&Number.isFinite(x))))errors.push({kind:'input-contract',i:v.id});}
  const pairs=[],a=vehicles.map(()=>Array.from({length:4},()=>Array(n).fill(0))),edgeSet=new Set();let capMax=0;
  for(let i=0;i<n;i++)for(let r=0;r<4;r++)for(let j=0;j<n;j++)if(i!==j){
    const f=pairTerm(p,i,j,r,c);pairs.push({i,r,j,K:f.term,...f});
    if(f.symbol===4||f.symbol===11)errors.push({kind:'unsupported-pair',i,r,j,symbol:f.symbol});
    const scaled=f.term*Math.sqrt(vehicles[j].S0/mg);capMax=Math.max(capMax,scaled);
    if(!(scaled<=128&&Number.isFinite(scaled)))errors.push({kind:'scaled-cap',i,r,j});
    a[i][r][j]=scaled/Math.sqrt(vehicles[i].f0[r]/(2*rho*A));
    if(f.term>0)edgeSet.add(`${j},${i}`);
  }
  const edges=[...edgeSet].map(s=>s.split(',').map(Number)).sort((x,y)=>x[0]-y[0]||x[1]-y[1]);
  const order=vehicles.map(v=>v.id).sort((i,j)=>vehicles[j].q[2]-vehicles[i].q[2]||i-j),position=Array(n);order.forEach((i,k)=>position[i]=k);
  const descendingEligible=edges.every(([j,i])=>position[j]<position[i]);
  const ordinaryLmax=Math.max(...a.flat().map(row=>row.reduce((s,x)=>s+x,0)))/(4*Math.sqrt(2));
  const out={id,vehicles,pairs,a,admission:{admitted:errors.length===0,errors,scaledCapMax:capMax},graph:{edges,order,descendingEligible,prescribedCyclePresent:id==='hexagon-cycle'?Array.from({length:6},(_,j)=>edgeSet.has(`${j},${(j+5)%6}`)).every(Boolean):null},geometryWork:{pairCalls:pairs.length,positiveRotorTerms:pairs.filter(x=>x.K>0).length},ordinaryLmax,solutions:null};
  if(errors.length)return out;
  let direct=null;
  if(descendingEligible){const y=Array(n).fill(1),w=emptyWork(),rotors=Array(n);for(const i of order){const z=nodeMap(i,y,vehicles,a,w);y[i]=z.y;rotors[i]=z.rotors;}
    const rw=emptyWork(),residualMap=map(y,vehicles,a,rw);direct={y,rotors,work:w,residualMap,residualWork:rw,residualLog:logDistance(y,residualMap.y)};}
  let y=Array(n).fill(1),iterates=[y.slice()],work=emptyWork(),uncoupled=null,converged=false;
  for(let k=0;k<64;k++){const before={...work},z=map(y,vehicles,a,work);if(k===0)uncoupled={map:z,work:Object.fromEntries(Object.keys(work).map(s=>[s,work[s]-before[s]]))};
    const change=logDistance(y,z.y);y=z.y;iterates.push(y.slice());if(change<=1e-11){converged=true;break;}}
  const rw=emptyWork(),residualMap=map(y,vehicles,a,rw),picard={y,iterates,iterations:iterates.length-1,converged,work,residualMap,residualWork:rw,residualLog:logDistance(y,residualMap.y)};
  out.solutions={direct,picard,uncoupled};return out;
}
function main(){const output=process.argv[2];if(!output)throw new Error('output path required');
  const out={kind:'four-rotor-static-coupling-development-verification',constants:{mg,arm,radius,rho,A,R,c},runtime:{node:process.version},cases:fixtures().map(([id,v])=>runCase(id,v))};
  out.candidatePass=out.cases.every(x=>x.id==='near-rejection'?!x.admission.admitted&&x.pairs.some(p=>p.symbol===4)&&x.solutions===null:x.admission.admitted&&x.graph.edges.length>0&&x.solutions.picard.converged&&(x.id==='hexagon-cycle'?x.graph.prescribedCyclePresent&&!x.graph.descendingEligible:x.graph.descendingEligible));
  fs.writeFileSync(output,JSON.stringify(out,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify({candidatePass:out.candidatePass,cases:out.cases.map(c=>({id:c.id,admitted:c.admission.admitted,edges:c.graph.edges.length,iterations:c.solutions?.picard.iterations??null}))}));if(!out.candidatePass)process.exitCode=1;
}
if(require.main===module)main();
