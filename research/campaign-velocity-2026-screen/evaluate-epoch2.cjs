// Public edition: source path only changed; original release does not authorize this edited hash.
'use strict';
// Code only until a separately hash-bound root release. Exactly 18 kernel calls.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert');
const P=__dirname,sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=n=>fs.readFileSync(path.join(P,n)),json=n=>JSON.parse(read(n));
const M='1f7d28e85096abf4f3e4c62633370437dd60bf8bb9bc74e635e4b7aa9614844e';
const K='fb6d5a1d632a0023818041ef6bc39316ff8ed950f318da1a6649e2515b9fd8bc';
const self=sha(fs.readFileSync(__filename)),rel=json('EPOCH2-EVALUATION-RELEASE.json');
assert(rel.approved===true&&rel.epoch===2&&rel.input_manifest_sha256===M&&rel.evaluator_sha256===self);
assert(!fs.existsSync(path.join(P,'EPOCH2-RESULT.json'))&&!fs.existsSync(path.join(P,'EPOCH2-EVALUATION-STARTED.json')));
assert(sha(read('EPOCH2-FREEZE.json'))===M);
const mf=json('EPOCH2-FREEZE.json');assert(mf.epoch===2&&mf.model_calls===0&&mf.selected_count===6);
for(const [n,h] of Object.entries(mf.inputs))assert(sha(read(n))===h,n);
for(const r of mf.outputs){const b=read(r.path);assert(b.length===r.bytes&&sha(b)===r.sha256,r.path);}
assert(sha(read('collect-epoch2.py'))===mf.collector_sha256);
const source=path.resolve(P,'../campaign-joint-stage-reference/implementation/snapshot/outputs/step03a-source/wake.cjs');
assert(sha(fs.readFileSync(source))===K);
const data=json('epoch2-measurements.json'),rows=data.points;
assert(data.epoch===2&&rows.length===6&&new Set(rows.map(r=>r.id)).size===6);
const Ui=4.36,UH=4.373329400265024,kappa=1.0030572018956476,pad=1e-12;
assert(Math.abs(Math.sqrt(.032*9.81/(8*1.29*Math.PI*.0225**2))-UH)<1e-14);
assert(Math.abs(UH/Ui-kappa)<1e-14&&data.frozen_kappa===kappa);
assert(data.nominal_geometry.D_opposite_motors_m===.092&&data.nominal_geometry.radial_offset_m===0);
for(const r of rows){
 const x=r.zeta,v=r.v_normalized;
 assert([x.center,x.lower,x.upper,v.center,v.lower,v.upper].every(Number.isFinite));
 assert(x.lower>=5&&x.lower<=x.center&&x.center<=x.upper);
 assert(v.lower>=0&&v.lower<=v.center&&v.center<=v.upper);
 assert([7,11,15].includes(r.target)&&x.upper>=r.target-.5&&x.lower<=r.target+.5);
}
for(const t of [7,11,15])assert(rows.filter(r=>r.target===t).length===2);
const bytes=d=>fs.readdirSync(d,{withFileTypes:true}).reduce((s,e)=>s+(e.isDirectory()?bytes(path.join(d,e.name)):fs.statSync(path.join(d,e.name)).size),0);
assert(bytes(P)+20000<500000);
fs.writeFileSync(path.join(P,'EPOCH2-EVALUATION-STARTED.json'),JSON.stringify({utc:new Date().toISOString(),epoch:2,input_manifest_sha256:M,evaluator_sha256:self})+'\n',{flag:'wx'});
const W=require(source);
assert([W.parameters.decay,W.parameters.spread,W.parameters.origin,W.parameters.minDownstream].join(',')==='10.11,0.07668,-5.817,2.5');
let calls=0;
function q(z){calls++;const v=W.normalizedWake(z/2,0).speed;assert(Number.isFinite(v)&&v>0);return v;}
const results=rows.map(r=>{
 const x=r.zeta,v=r.v_normalized,c=q(x.center),hi=q(x.lower),lo=q(x.upper);
 assert(lo<=c&&c<=hi);
 const diff=v.center-kappa*c,b=[v.lower-kappa*hi-pad,v.upper-kappa*lo+pad];
 return {id:r.id,target:r.target,stratum:r.target===15?'approximately-self-similar':'developing-profile',zeta:{center:x.center,interval:[x.lower,x.upper]},observed:{center:v.center,interval:[v.lower,v.upper]},q:{center:c,interval:[lo,hi]},predicted_on_reported_scale:{center:kappa*c,interval:[kappa*lo,kappa*hi]},paired_difference:{center:diff,interval:b},nominal_m_per_s:{observed:Ui*v.center,observed_interval:[Ui*v.lower,Ui*v.upper],predicted:UH*c,predicted_interval:[UH*lo,UH*hi],paired_difference:Ui*diff,paired_difference_interval:b.map(a=>Ui*a)}};
});
assert(calls===18);
function union(xs){const out=[];for(const b of xs.map(x=>x.slice()).sort((a,b)=>a[0]-b[0])){const last=out[out.length-1];if(last&&b[0]<=last[1])last[1]=Math.max(last[1],b[1]);else out.push(b);}return out;}
const groups=[7,11,15].map(t=>{const rr=results.filter(r=>r.target===t),u=union(rr.map(r=>r.paired_difference.interval));return {target:t,stratum:rr[0].stratum,ids:rr.map(r=>r.id),paired_difference_union:u,paired_difference_hull:[u[0][0],u[u.length-1][1]]};});
const output={epoch:2,status:'conditional-scale-retaining-screen-no-physical-pass-fail',input_manifest_sha256:M,evaluator_sha256:self,release_sha256:sha(read('EPOCH2-EVALUATION-RELEASE.json')),kernel_sha256:K,public_commit:'1336f5c416875a9651f92b58b2ed06649f25b04e',model_version:'arXiv:2403.13321v3',measurement_version:'arXiv:2608.30900v1 Fig.5(a), PREPRINT',scalar_calls:calls,normalization:{Ui_reported:Ui,UH_nominal:UH,kappa,formula:'UH=sqrt(m*g/(8*rho*pi*R^2)); primary predicted normalized velocity=kappa*q'},geometry:{l_m:.046,D_opposite_motors_m:.092,r_m:0,axial_argument:'zeta/2',lower_domain:5},monotonicity:'dq/dzeta=-10.11/[2*(zeta/2+5.817)^2]<0 on the accepted domain; coordinate-endpoint enclosure at fixed nominal parameters.',results,neighborhoods:groups,limitations:'Fixed +/-0.01 SVG-unit graphical envelope only. Historical export, symbol placement, experimental PIV and nominal-input uncertainty unbounded. Mean speed magnitude differs from mean axial velocity under fluctuations. Shared calibration remains dependent. No fitted parameters or physical/statistical pass. Original quantization-gate epoch remains stopped.'};
const out=JSON.stringify(output,null,2)+'\n';
assert(Buffer.byteLength(out)+fs.statSync(path.join(P,'EPOCH2-EVALUATION-STARTED.json')).size<20000);
fs.writeFileSync(path.join(P,'EPOCH2-RESULT.json'),out,{flag:'wx'});
process.stdout.write(JSON.stringify({epoch:2,calls,bytes:Buffer.byteLength(out),sha256:sha(out)})+'\n');
