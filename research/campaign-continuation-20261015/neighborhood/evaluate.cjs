'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert');
const P=__dirname,OLD=path.join(P,'../research-velocity-ratio-screen');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=n=>fs.readFileSync(path.join(P,n));
const json=n=>JSON.parse(read(n));
const M='b3c14e51a256f161df96f5f1df96c1b42d3c3cb2abed7869272a58b4fe1a01de';
const K='fb6d5a1d632a0023818041ef6bc39316ff8ed950f318da1a6649e2515b9fd8bc';
const rel=json('EVALUATION-RELEASE.json'),self=sha(fs.readFileSync(__filename));
assert(rel.approved===true&&rel.input_manifest_sha256===M&&rel.evaluator_sha256===self);
assert(!fs.existsSync(path.join(P,'RESULT.json'))&&!fs.existsSync(path.join(P,'EVALUATION-STARTED.json')));
assert(sha(read('evidence-freeze.json'))===M);
const mf=json('evidence-freeze.json');
for(const [n,v] of Object.entries(mf.files)){const b=read(n);assert(b.length===v.bytes&&sha(b)===v.sha256,n);}
const old=fs.readFileSync(path.join(OLD,'evidence-freeze.json'));
assert(sha(old)===mf.pilot_manifest_sha256);
for(const [n,v] of Object.entries(JSON.parse(old).files)){const b=fs.readFileSync(path.join(OLD,n));assert(b.length===v.bytes&&sha(b)===v.sha256,n);}
const source=path.resolve(P,'../research-recovery-r8/public-baseline/research/campaign-joint-stage-reference/implementation/snapshot/outputs/step03a-source/wake.cjs');
assert(sha(fs.readFileSync(source))===K);
const data=json('measurements.json'),rows=[data.anchor,...data.responses];
assert(rows.length===12&&data.responses.length===11&&new Set(rows.map(r=>r.id)).size===12);
const lambda=2*Math.sqrt(2),floor=2.5*lambda,A=(Math.sqrt(2)-1)/(.07668**2);
const margin=(floor+5.817*lambda)**2-3*A;
assert(margin>0);
for(const r of rows){
 const v=[r.zeta,...r.zeta_bounds,r.v,...r.v_bounds];assert(v.every(Number.isFinite));
 assert(r.zeta_bounds[0]>=floor&&r.zeta_bounds[0]<=r.zeta&&r.zeta<=r.zeta_bounds[1]);
 assert(r.v_bounds[0]>=0&&r.v_bounds[0]<=r.v&&r.v<=r.v_bounds[1]);
}
assert(data.anchor.v_bounds[0]>0);
for(const t of [11,14,17,20])assert(data.responses.filter(r=>r.neighborhood===t).length===(t===20?2:3));
const bytes=d=>fs.readdirSync(d,{withFileTypes:true}).reduce((s,e)=>s+(e.isDirectory()?bytes(path.join(d,e.name)):fs.statSync(path.join(d,e.name)).size),0);
assert(bytes(P)+bytes(OLD)+20000<1000000);
const started={started_at_utc:new Date().toISOString(),input_manifest_sha256:M,evaluator_sha256:self};
fs.writeFileSync(path.join(P,'EVALUATION-STARTED.json'),JSON.stringify(started)+'\n',{flag:'wx'});
const W=require(source);
assert([W.parameters.decay,W.parameters.spread,W.parameters.origin,W.parameters.minDownstream].join(',')==='10.11,0.07668,-5.817,2.5');
let calls=0;
function q(z){calls++;const v=W.normalizedWake(z/lambda,1/lambda).speed;assert(Number.isFinite(v)&&v>0);return v;}
const qs=new Map();
for(const r of rows){const c=q(r.zeta),hi=q(r.zeta_bounds[0]),lo=q(r.zeta_bounds[1]);assert(lo<=c&&c<=hi);qs.set(r.id,{center:c,low:lo,high:hi});}
assert(calls===36);
const a=data.anchor,aq=qs.get(a.id);
const results=data.responses.map(r=>{
 const p=qs.get(r.id),R=r.v/a.v,Q=p.center/aq.center;
 const Rb=[r.v_bounds[0]/a.v_bounds[1],r.v_bounds[1]/a.v_bounds[0]];
 const Qb=[p.low/aq.high,p.high/aq.low];
 return {id:r.id,neighborhood:r.neighborhood,zeta:r.zeta,partial_eligibility:r.partial_eligibility,observed_ratio:R,model_ratio:Q,observed_interval:Rb,model_interval:Qb,paired_difference:R-Q,paired_difference_interval:[Rb[0]-Qb[1],Rb[1]-Qb[0]],q:p};
});
function union(xs){const out=[];for(const b of xs.map(x=>x.slice()).sort((a,b)=>a[0]-b[0])){const last=out[out.length-1];if(last&&b[0]<=last[1])last[1]=Math.max(last[1],b[1]);else out.push(b);}return out;}
const groups=[11,14,17,20].map(t=>{const rr=results.filter(r=>r.neighborhood===t),u=union(rr.map(r=>r.paired_difference_interval));return {target:t,ids:rr.map(r=>r.id),paired_difference_union:u,paired_difference_hull:[u[0][0],u[u.length-1][1]],truncated_at_20:t===20};});
const output={status:'conditional-shape-screen-no-physical-pass-fail',input_manifest_sha256:M,evaluator_sha256:self,release_sha256:sha(read('EVALUATION-RELEASE.json')),kernel_sha256:K,public_commit:'1336f5c416875a9651f92b58b2ed06649f25b04e',model_version:'arXiv:2403.13321v3',measurement_version:'arXiv:2507.09463v1 Fig.9',scalar_calls:calls,geometry:{lambda,eta:1,floor},monotonicity:{formula:'q=C*lambda*t^3/(t^2+A)^2; derivative sign=3A-t^2',A,domain_margin:margin},anchor:{id:a.id,q:aq},results,neighborhoods:groups,limitations:'Unknown experimental/plane error; shared anchor/calibration; no confidence level or amplitude validation. Hull overlap is not joint agreement. Target20 ends at20.'};
const out=JSON.stringify(output,null,2)+'\n';
assert(Buffer.byteLength(out)+fs.statSync(path.join(P,'EVALUATION-STARTED.json')).size<20000);
fs.writeFileSync(path.join(P,'RESULT.json'),out,{flag:'wx'});
process.stdout.write(JSON.stringify({calls,bytes:Buffer.byteLength(out),sha256:sha(out)})+'\n');
