'use strict';
const keys=['positionM','velocityMps','attitudeRad','angularVelocityRadps'];
function compare(a,b){
 if(!a.result.complete||!b.result.complete||a.common.length!==b.common.length||a.result.config.seed!==b.result.config.seed)throw Error('Incomplete or mismatched comparison');
 for(const d of [a,b])if(d.result.endTick!==51200||d.result.config.count!==16||d.result.config.commonTicks!==32||d.common.length!==1601)throw Error('Incomplete canonical common-grid contract');
 const maximum=Object.fromEntries([...keys,'nominalMotorN','attitudeAtan2Rad'].map(k=>[k,0])),worst={};
 function set(key,value,n,i){if(!Number.isFinite(value))throw Error('Nonfinite comparison');if(!worst[key]||value>maximum[key]){maximum[key]=value;worst[key]={record:n,tick:n*32,time:n/1600,drone:i};}}
 for(let n=0;n<a.common.length;n++)for(let i=0;i<16;i++){
  const x=a.common[n],y=b.common[n],o=17*i;if(x.length!==272||y.length!==272)throw Error('Bad common row');
  for(const [key,k]of [['positionM',0],['velocityMps',3],['angularVelocityRadps',10]])set(key,Math.hypot(...[0,1,2].map(j=>x[o+k+j]-y[o+k+j])),n,i);
  let d=0,nx=0,ny=0;for(let k=6;k<10;k++){d+=x[o+k]*y[o+k];nx+=x[o+k]**2;ny+=y[o+k]**2;}
  if(!(nx>0&&ny>0))throw Error('Invalid comparison quaternion');
  set('attitudeRad',2*Math.acos(Math.min(1,Math.abs(d/Math.sqrt(nx*ny)))),n,i);
  const q=x.slice(o+6,o+10).map(v=>v/Math.sqrt(nx)),r=y.slice(o+6,o+10).map(v=>v/Math.sqrt(ny));
  const vx=q[3]*r[0]-q[0]*r[3]-q[1]*r[2]+q[2]*r[1],vy=q[3]*r[1]-q[1]*r[3]-q[2]*r[0]+q[0]*r[2],vz=q[3]*r[2]-q[2]*r[3]-q[0]*r[1]+q[1]*r[0];
  set('attitudeAtan2Rad',2*Math.atan2(Math.hypot(vx,vy,vz),Math.abs(d/Math.sqrt(nx*ny))),n,i);
  for(let k=13;k<17;k++)set('nominalMotorN',Math.abs(x[o+k]-y[o+k]),n,i);
 }
 return {a:a.result.runId,b:b.result.runId,records:a.common.length,maximum,worst};
}
function gate(fine,caps,{coarse=null,floors=null,reduction=null}={}){const rows=keys.map(key=>({key,value:fine.maximum[key],cap:caps[key],absolutePassed:Number.isFinite(fine.maximum[key])&&fine.maximum[key]<=caps[key],reductionPassed:!coarse||fine.maximum[key]<=Math.max(floors[key],reduction*coarse.maximum[key]),coarse:coarse?.maximum[key]??null,floor:floors?.[key]??null}));return {passed:rows.every(r=>r.absolutePassed&&r.reductionPassed),rows,fine,coarse,reduction};}
function compareControllers(a,b){if(a.controlEvents.length!==b.controlEvents.length)throw Error('Mismatched controller counts');let maximumCommandDifference=0,worst=null;const branchDifferences=[];for(let n=0;n<a.controlEvents.length;n++){const x=a.controlEvents[n],y=b.controlEvents[n];if(x.tick!==y.tick)throw Error('Mismatched controller tick');if(x.branchSignatureSha256!==y.branchSignatureSha256)branchDifferences.push({tick:x.tick,a:x.branchSignatureSha256,b:y.branchSignatureSha256});for(let i=0;i<16;i++)for(let r=0;r<4;r++){const d=Math.abs(x.commands[i][r]-y.commands[i][r]);if(!Number.isFinite(d))throw Error('Nonfinite controller comparison');if(d>maximumCommandDifference){maximumCommandDifference=d;worst={tick:x.tick,drone:i,rotor:r,a:x.commands[i][r],b:y.commands[i][r]};}}}return {a:a.result.runId,b:b.result.runId,events:a.controlEvents.length,maximumCommandDifference,worst,branchDifferences,meaning:'Branch signature changes are not themselves physical controller discontinuities; actual command differences retained'};}
function skippedRows(config,completed,reason){return config.seeds.flatMap(seed=>config.rows.map(row=>({runId:`s${seed}-${row.arm}`,seed,...row,status:completed.includes(`s${seed}-${row.arm}`)?'attempted':'skipped',reason:completed.includes(`s${seed}-${row.arm}`)?null:reason})));}
module.exports={keys,compare,gate,compareControllers,skippedRows};
