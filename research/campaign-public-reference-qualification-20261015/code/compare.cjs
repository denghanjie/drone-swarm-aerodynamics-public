'use strict';
const keys=['positionM','velocityMps','attitudeRad','angularVelocityRadps'];
function compare(a,b,saveWitness){
 if(!a.complete||!b.complete||a.seed!==b.seed||a.common.length!==b.common.length||a.diag.length!==b.diag.length)throw Error('Incomplete comparison');
 const maximum={},worst={},terminalMaximum={},terminalWorst={};function set(k,v,w){if(w.tick===(a.common.length-1)*128&&(terminalMaximum[k]===undefined||v>terminalMaximum[k])){terminalMaximum[k]=v;terminalWorst[k]={tick:w.tick,drone:w.drone};}if(!Number.isFinite(v))throw Error('Nonfinite comparison');if(maximum[k]===undefined||v>maximum[k]){maximum[k]=v;worst[k]=w;}}
 for(let t=0;t<a.common.length;t++)for(let i=0;i<16;i++){
  const x=a.common[t].slice(i*17,i*17+17),y=b.common[t].slice(i*17,i*17+17),w={tick:t*128,drone:i,a:x,b:y};
  for(const [k,p]of [['positionM',0],['velocityMps',3],['angularVelocityRadps',10]])set(k,Math.hypot(x[p]-y[p],x[p+1]-y[p+1],x[p+2]-y[p+2]),w);
  const nx=Math.hypot(...x.slice(6,10)),ny=Math.hypot(...y.slice(6,10));if(!(nx>0&&ny>0))throw Error('Quaternion comparison');const q=x.slice(6,10).map(v=>v/nx),r=y.slice(6,10).map(v=>v/ny);
  const vx=q[3]*r[0]-q[0]*r[3]-q[1]*r[2]+q[2]*r[1],vy=q[3]*r[1]-q[1]*r[3]-q[2]*r[0]+q[0]*r[2],vz=q[3]*r[2]-q[2]*r[3]-q[0]*r[1]+q[1]*r[0],d=q.reduce((s,v,k)=>s+v*r[k],0);
  set('attitudeRad',2*Math.atan2(Math.hypot(vx,vy,vz),Math.abs(d)),w);set('nominalMotorN',Math.max(...[13,14,15,16].map(k=>Math.abs(x[k]-y[k]))),w);
 }
 const witnesses={},pairs=[];for(const k of Object.keys(worst)){const w=worst[k],row=pairs.length;pairs.push(w.a,w.b);witnesses[k]={tick:w.tick,drone:w.drone,rows:[row,row+1]};}const witnessData=saveWitness(pairs);
 if(a.controls.length!==b.controls.length)throw Error('Controller alignment');let command=0,commandWorst=null,branchMismatchCount=0;
 for(let t=0;t<a.controls.length;t++){const x=a.controls[t],y=b.controls[t];if(x.tick!==y.tick)throw Error('Controller clocks');branchMismatchCount+=+(x.signature!==y.signature);for(let i=0;i<16;i++)for(let r=0;r<4;r++){const d=Math.abs(x.commands[i][r]-y.commands[i][r]);if(d>command){command=d;commandWorst={tick:x.tick,drone:i,rotor:r,a:x.commands[i][r],b:y.commands[i][r]};}}}
 const field={},fieldWorst={};function fld(k,v,w){if(!Number.isFinite(v))throw Error('Nonfinite load comparison');if(field[k]===undefined||v>field[k]){field[k]=v;fieldWorst[k]=w;}}
 for(let t=0;t<a.diag.length;t++){const x=a.diag[t],y=b.diag[t];if(x.tick!==y.tick)throw Error('Diagnostic alignment');for(let i=0;i<16;i++){
  for(let r=0;r<4;r++){fld('incomingInflowMps',Math.abs(x.incoming[i][r]-y.incoming[i][r]),{tick:x.tick,drone:i,rotor:r,a:x.incoming[i][r],b:y.incoming[i][r],ages:[x.age,y.age]});fld('freshInflowMps',Math.abs(x.fresh[i][r]-y.fresh[i][r]),{tick:x.tick,drone:i,rotor:r,a:x.fresh[i][r],b:y.fresh[i][r]});}
  for(const [k,p,n]of [['forceN','force',3],['rollPitchMomentNm','moment',2]]){const u=x.loads[i][p].slice(0,n),v=y.loads[i][p].slice(0,n);fld(k,Math.hypot(...u.map((z,k)=>z-v[k])),{tick:x.tick,drone:i,a:u,b:v,ages:[x.age,y.age]});}
 }}
 return {a:a.id,b:b.id,records:a.common.length,maximum,terminalMaximum,terminalWorst,witnesses,witnessData,command,commandWorst,branchMismatchCount,field,fieldWorst};
}
function gate(fine,caps,coarse=null,floors=null,reduction=null){const rows=keys.map(k=>({key:k,value:fine.maximum[k],cap:caps[k],coarse:coarse?.maximum[k]??null,passed:fine.maximum[k]<=caps[k]&&(!coarse||fine.maximum[k]<=Math.max(floors[k],reduction*coarse.maximum[k]))}));return {passed:rows.every(r=>r.passed),rows};}
module.exports={keys,compare,gate};
