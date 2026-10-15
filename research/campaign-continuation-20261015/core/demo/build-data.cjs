'use strict';
// Authorized postprocessing: deterministic coordinates and saved records only.
// No aerodynamic module is imported; no model or trajectory is evaluated.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),out=__dirname,results=path.join(root,'results');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function check(x,m){if(!x)throw Error(m);}
function read(name){const b=fs.readFileSync(path.join(results,name));return {value:JSON.parse(b),sha256:sha(b)};}
function hashCoords(coords){const b=Buffer.alloc(coords.length*24);coords.forEach((v,i)=>v.forEach((x,j)=>b.writeDoubleLE(x,24*i+8*j)));return sha(b);}
const summary=read('summary.json'),metadata=read('metadata.json'),supervisor=JSON.parse(fs.readFileSync(path.join(root,'SUPERVISOR.json')));
check(summary.value.status==='complete'&&summary.value.completeFixtures===6&&supervisor.exit_code===0&&!supervisor.timed_out,'Incomplete experiment');
const m=metadata.value,g=m.geometry,{k,s,r0,vi}=m.constants;
check(m.experimentId==='CORE-EXTENT-CERTIFICATE-20261015'&&g.delta===.25&&JSON.stringify(g.extents)==='[2,4,8]'&&JSON.stringify(g.phases)==='[0,0.125]','Frozen geometry mismatch');
const full=[],fixtures=[];
for(const rec of summary.value.fixtureRecords){
 const raw=fs.readFileSync(path.join(results,rec.path));check(sha(raw)===rec.sha256,'Fixture record hash mismatch');const f=JSON.parse(raw),coords=[];
 for(let j=0;j<=(f.extentMeters-.5)/g.delta;j++){
  const d=.5+j*g.delta,b=k*(d+s),R=2*b-r0,phase=f.phaseMeters[0],lim=Math.ceil((R+phase)/g.delta)+1;let count=0;
  check(f.phaseMeters[1]===phase,'Unequal phase');
  for(let iy=-lim;iy<=lim;iy++)for(let ix=-lim;ix<=lim;ix++){const x=ix*g.delta+phase,y=iy*g.delta+phase;if(x*x+y*y<=R*R){coords.push([x,y,d]);count++;}}
  const layer=f.layers[j];check(layer.downstream===d&&layer.sourceRadius===R&&layer.count===count,'Regenerated layer mismatch');
 }
 check(coords.length===f.sourceCount&&hashCoords(coords)===f.coordinates.sha256,'Regenerated coordinate hash mismatch');
 full.push(coords);fixtures.push({id:f.fixture,phase:f.phaseMeters[0],extent:f.extentMeters,count:f.sourceCount,coordinateSha256:f.coordinates.sha256,recordSha256:rec.sha256,record:'../results/'+rec.path,rotors:f.rotors,boundsMS:f.boundsMS,maxXi:f.checks.maxXi,counts:{full:coords.filter(v=>v[2]<=2).length,partial:coords.filter(v=>v[2]>2&&v[2]<2.5).length,omitted:coords.filter(v=>v[2]>=2.5).length}});
}
check(fixtures.length===6,'Missing fixture');
const clouds=[full[2],full[5]];
fixtures.forEach((f,i)=>{f.cloud=Math.floor(i/3);check(hashCoords(clouds[f.cloud].slice(0,f.count))===f.coordinateSha256,'Compact prefix mismatch');});
const data={experiment:m.experimentId,kind:'Static synthetic point clouds; not Boids flight or measured flow',postprocess:'Coordinates regenerated after the run; all six ordered Float64 hashes verified before this JSON write. No model evaluation.',summarySha256:summary.sha256,metadataSha256:metadata.sha256,vi,receiver:g.receiver,rotors:g.rotors,axialFadeStart:2,axialCutoff:2.5,coordinateStorage:'Two largest clouds; each fixture is its verified ordered prefix',clouds,fixtures};
const buffer=Buffer.from(JSON.stringify(data)+'\n');check(buffer.length<=50000,'Viewer data cap');
check(!fs.existsSync(path.join(out,'data.json')),'Exclusive viewer build; output exists');
fs.writeFileSync(path.join(out,'data.json'),buffer,{flag:'wx'});
const receipt={kind:'Postprocess only; no kernel calls',experiment:m.experimentId,coordinateHashChecks:fixtures.map(f=>({fixture:f.id,sha256:f.coordinateSha256,verified:true})),data:{file:'data.json',bytes:buffer.length,sha256:sha(buffer)},scriptSha256:sha(fs.readFileSync(__filename)),renderingVerified:false};
fs.writeFileSync(path.join(out,'POSTPROCESS.json'),JSON.stringify(receipt,null,2)+'\n',{flag:'wx'});
process.stdout.write(JSON.stringify({status:'complete',fixtures:fixtures.length,dataBytes:buffer.length,modelCalls:0})+'\n');
