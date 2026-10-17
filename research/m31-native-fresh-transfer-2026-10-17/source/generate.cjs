'use strict';
// Explicit supervised generation allocation only. No aerodynamic module is loaded.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const NAME='research/m31-native-fresh-transfer-2026-10-17',CAP=32*1024*1024;
const [rootArg,expected,commit]=process.argv.slice(2),root=path.resolve(rootArg||'.');
const pkg=path.join(root,NAME),results=path.join(pkg,'results');
const need=(v,c)=>{if(!v)throw Error(c);},sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function canonical(v){if(Array.isArray(v))return '['+v.map(canonical).join(',')+']';if(v&&typeof v==='object')return '{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}';return JSON.stringify(v);}
function identity(file){const b=fs.readFileSync(file);return {bytes:b.length,sha256:sha(b)};}
function pin(file){return {path:path.relative(root,file).split(path.sep).join('/'),...identity(file)};}
function checked(p){need(typeof p.path==='string'&&!path.isAbsolute(p.path)&&p.path.split('/').every(s=>s&&s!=='.'&&s!=='..'),'pin-path');const f=path.join(root,p.path);need(fs.realpathSync(f)===f&&fs.lstatSync(f).isFile(),'pin-file');const v=identity(f);need(v.bytes===p.bytes&&v.sha256===p.sha256,'pin-identity');return f;}
function load(f){need(fs.statSync(f).size<=CAP,'json-cap');return JSON.parse(fs.readFileSync(f,'utf8'));}
function create(file,value,limit=CAP){const bytes=Buffer.from(JSON.stringify(value)+'\n');need(bytes.length<=limit,'file-cap');const fd=fs.openSync(file,'wx',0o600);try{fs.writeFileSync(fd,bytes);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}const dd=fs.openSync(path.dirname(file),'r');try{fs.fsyncSync(dd);}finally{fs.closeSync(dd);}return pin(file);}
const bits=v=>{const b=Buffer.alloc(8);b.writeDoubleLE(v);return b.readBigUInt64LE().toString(16).padStart(16,'0');};
function capture(states){need(Array.isArray(states)&&states.length===64,'capture-count');return {drones:states.map((s,id)=>{need(Array.isArray(s)&&s.length===17&&s.every(v=>typeof v==='number'),'capture-shape');return {id,state:s.map(bits)};})};}
const pose=v=>v.drones.flatMap(d=>[...d.state.slice(0,3),...d.state.slice(6,10)]);
function diagnostic(v){if(v===undefined)return {undefined:true};if(typeof v==='number')return Number.isFinite(v)&&!Object.is(v,-0)?v:{binary64:bits(v)};if(Array.isArray(v))return v.map(diagnostic);if(v&&typeof v==='object')return Object.fromEntries(Object.entries(v).map(([k,x])=>[k,diagnostic(x)]));return v;}
function dyadic(w){const b=BigInt('0x'+w),e=Number((b>>52n)&2047n),m=b&((1n<<52n)-1n);need(e!==2047,'nonfinite-motion-word');return {n:(b>>63n?-1n:1n)*(e?m+(1n<<52n):m),s:e?e-1023-52:-1074};}
function motion(a,b){let witness=null;const changed=!same(a,b);for(let i=1;i<64;i++)for(let k=0;k<3;k++){const xs=[b.drones[i].state[k],b.drones[0].state[k],a.drones[i].state[k],a.drones[0].state[k]].map(dyadic),s=Math.min(...xs.map(x=>x.s)),sign=[1n,-1n,-1n,1n];const sum=xs.reduce((z,x,j)=>z+sign[j]*(x.n<<BigInt(x.s-s)),0n);if(sum!==0n&&witness===null)witness={id:i,axis:k};}return {stateChanged:changed,relativeGeometryChanged:witness!==null,witness,passed:changed&&witness!==null};}
let manifest,science,attempt,manifestPin,publicationPin,journalFd=null,journalBytes=0,sequence=0,activeSlot=null;
const fixedSlots=[{id:'fresh-a-t5',seed:26171711,t:5,n:64,methods:['F','L']},{id:'fresh-b-t5',seed:26171712,t:5,n:64,methods:['L','F']}];
const index={schema:'m31-native-fresh-generation-v1',sourceCommit:commit,sourceManifestSha256:expected,complete:false,slots:fixedSlots.map(s=>({...s,status:'not-attempted',generation:null,input:null,semanticInputSha256:null,motion:null})),controls:[],errors:[]};
function event(kind,body){const b=Buffer.from(JSON.stringify({sequence:sequence++,kind,body})+'\n');need(b.length<=128*1024&&journalBytes+b.length<=4*1024*1024,'journal-cap');fs.writeFileSync(journalFd,b);fs.fsyncSync(journalFd);journalBytes+=b.length;}
function preflight(){
 need(process.argv.length===5&&/^[a-f0-9]{64}$/.test(expected)&&/^[a-f0-9]{40}$/.test(commit),'arguments');
 need(__filename===path.join(pkg,'source/generate.cjs')&&process.env.RESEARCH_EXECUTION_CONTEXT==='tool-require-escalated','entry-dispatch');
 need(process.platform==='darwin'&&!process.env.NODE_OPTIONS&&!process.env.NODE_PATH,'node-context');
 need(Date.now()<Date.parse('2026-10-17T03:00:00+00:00'),'cutoff');
 const mf=path.join(pkg,'source-manifest.json');manifestPin=pin(mf);need(manifestPin.sha256===expected,'manifest-sha');manifest=load(mf);
 need(new Set(manifest.files.map(p=>p.path)).size===manifest.files.length,'duplicate-pin');manifest.files.forEach(checked);
 for(const n of ['generate.cjs','science-config.json','vendor/generation/milestone-31-source/sim.cjs','vendor/generation/milestone-31-source/grid.cjs','vendor/generation/milestone-31-source/geometry.cjs','vendor/generation/milestone-31-source/factory.cjs','vendor/generation/milestone-31-source/factory-wide.cjs','vendor/generation/milestone-31-source/wall-filter.cjs','vendor/generation/step02c-source/physics.cjs'])need(manifest.files.some(p=>p.path===NAME+'/source/'+n),'source-closure');
 const node=identity(fs.realpathSync(process.execPath));need(node.bytes===manifest.runtime.node.bytes&&node.sha256===manifest.runtime.node.sha256,'node-pin');
 science=load(path.join(pkg,'source/science-config.json'));need(science.schema==='m31-native-fresh-science-config-v1','science-config');
 need(same(science.slots,[{id:'fresh-a-t5',seed:26171711,t:5,n:64,methods:['F','L']},{id:'fresh-b-t5',seed:26171712,t:5,n:64,methods:['L','F']}]),'fixed-slots');
 need(same(science.generation,{count:64,duration:5,dt:0.0025,mode:'boids',search:'grid',filter:'wall-priority',record:true,frameEvery:0.2,factoryVariant:'wide',airflow:'off',observation:'ideal'}),'fixed-generation');
 need(Array.isArray(science.retainedInputs)&&same(science.retainedInputs.map(r=>r.id),['run-a-t0','run-a-t5','run-a-t10','run-b-t0','run-b-t5','run-b-t10']),'six-retained-inputs');
 for(const retained of science.retainedInputs){const p=manifest.files.find(x=>x.path===retained.input.path);need(p&&p.bytes===retained.input.bytes&&p.sha256===retained.input.sha256,'retained-input-source-pin');const f=checked(retained.input);need(sha(Buffer.from(canonical(load(f))))===retained.rawContentSha256,'retained-content-hash');}
 const receipt=load(path.join(pkg,'source-publication.json'));publicationPin=pin(path.join(pkg,'source-publication.json'));attempt=load(path.join(results,'generation-attempt.json'));
 need(attempt.stage==='generation'&&attempt.status==='started'&&attempt.sourceCommit===commit&&attempt.sourceManifestSha256===expected,'attempt-binding');
 need(receipt.commit===commit&&receipt.manifestSha256===expected&&receipt.manifestBytes===manifestPin.bytes&&receipt.manifestPath===manifestPin.path&&receipt.verifiedFilePins===manifest.files.length&&receipt.remoteBytesEqualLocal===true&&receipt.committedBytesEqualLocal===true&&Date.parse(receipt.verifiedUtc)<=Date.parse(attempt.startedUtc),'publication-binding');
 need(!fs.existsSync(path.join(results,'generation.json'))&&!fs.existsSync(path.join(results,'generation-journal.jsonl')),'exclusive-stage');
 for(const d of ['generation','inputs'])fs.mkdirSync(path.join(results,d),{recursive:false});
 journalFd=fs.openSync(path.join(results,'generation-journal.jsonl'),'wx',0o600);
 index.slots=science.slots.map(s=>({...s,status:'not-attempted',generation:null,input:null,semanticInputSha256:null,motion:null}));
}
function semantic(id,input){return sha(Buffer.from(canonical({domain:science.semanticInputDomain,id,input})));}
function runOne(slot,simulator){
 const g=science.generation,options={seed:slot.seed,count:64,duration:5,dt:g.dt,mode:g.mode,search:g.search,filter:g.filter,record:true,frameEvery:g.frameEvery};
 const rec={schema:'m31-native-fresh-generation-record-v1',sourceCommit:commit,sourceManifestSha256:expected,id:slot.id,seed:slot.seed,requested:g,generatorOptions:options,initial:null,returnedInitial:null,final:null,snapshot:null,frames:[],callbacks:[],returnedSummary:null,error:null,status:'started',motion:null,novelAgainstRetained:null};
 event('generation-start',{id:slot.id,seed:slot.seed,options});
 try{
  const returned=simulator.run({...options,frameSink(frame){need(Array.isArray(frame)&&frame.length===449,'pose-shape');const t=frame[0];need(Number.isFinite(t)&&t>=0&&t<=5&&(!rec.frames.length||t>rec.frames.at(-1).t)&&rec.frames.length<27,'pose-time');const saved={t,words:frame.slice(1).map(bits)};rec.frames.push(saved);event('pose',{id:slot.id,...saved});},progress(meta,states){const input=capture(states),t=meta.t;need((t===0||t===5||meta.stopReason!==null)&&(!rec.callbacks.length||t>rec.callbacks.at(-1).t),'callback-time');need(rec.frames.at(-1)?.t===t&&same(pose(input),rec.frames.at(-1).words),'callback-pose-binding');if(t===0){need(rec.initial===null,'initial-once');rec.initial=input;}if(t===5){need(rec.snapshot===null,'snapshot-once');rec.snapshot=input;}rec.callbacks.push(diagnostic(meta));event('full-state',{id:slot.id,t,stopReason:meta.stopReason,input});}});
  rec.returnedInitial=capture(returned.initial);rec.final=capture(returned.final);const {initial,final,frames,...summary}=returned;need(frames===undefined,'no-duplicate-frames');rec.returnedSummary=diagnostic(summary);
  need(same(rec.initial,rec.returnedInitial),'initial-return-binding');need(returned.metrics.end===5&&returned.metrics.stopReason===null,'scheduled-terminal-unavailable');
  need(rec.snapshot&&same(rec.snapshot,rec.final)&&same(pose(rec.final),rec.frames.at(-1).words)&&rec.frames.at(-1).t===5,'terminal-pose-binding');
  need(same(rec.frames.map(f=>f.t),Array.from({length:26},(_,i)=>Number((i*.2).toFixed(6)))),'pose-cadence');
  need(same(rec.callbacks.map(c=>c.t),[0,5])&&rec.callbacks.every(c=>c.stopReason===null),'callback-completion');
  need(same(returned.config,{filter:g.filter,seed:slot.seed,count:64,mode:g.mode,dt:g.dt,duration:5,search:g.search,course:'factory-v1',airflow:'off',observation:'ideal'})&&same(returned.recording,{cadence:.2,streamed:true}),'returned-config');
  rec.motion=motion(rec.initial,rec.snapshot);need(rec.motion.passed,'unchanged-relative-geometry');
  const rawContentSha256=sha(Buffer.from(canonical(rec.snapshot))),matches=science.retainedInputs.filter(r=>r.rawContentSha256===rawContentSha256).map(r=>r.id);
  rec.novelAgainstRetained={comparedCount:6,matches,passed:matches.length===0,rawContentSha256,retained:science.retainedInputs};need(rec.novelAgainstRetained.passed,'target-repeats-retained-input');rec.status='captured';
 }catch(error){rec.error={type:error.constructor?.name||'Error',code:/^[a-z0-9-]+$/.test(error.message||'')?error.message:'generator-exception'};rec.status='unavailable';}
 const generation=create(path.join(results,'generation',slot.id+'.json'),rec,8*1024*1024);let input=null,digest=null;
 Object.assign(index.slots[activeSlot],{status:'incomplete-persistence',generation,motion:rec.motion,novelAgainstRetained:rec.novelAgainstRetained});
 // A failed slot's partial capture stays in its generation record and journal.
 if(rec.status==='captured'){input=create(path.join(results,'inputs',slot.id+'.json'),rec.snapshot,128*1024);digest=semantic(slot.id,rec.snapshot);Object.assign(index.slots[activeSlot],{input,semanticInputSha256:digest});}
 const result={...slot,status:rec.status,generation,input,semanticInputSha256:digest,motion:rec.motion,novelAgainstRetained:rec.novelAgainstRetained};event('generation-complete',result);return result;
}
try{
 preflight();process.env.FLOCK_FACTORY_VARIANT='wide';
 // This is the first scientific import, after all source/runtime/publication gates.
 const simulator=require('./vendor/generation/milestone-31-source/sim.cjs');
 for(let i=0;i<science.slots.length;i++){activeSlot=i;index.slots[i].status='started';index.slots[i]=runOne(science.slots[i],simulator);activeSlot=null;}
 for(let i=0;i<science.movingControls.length;i++){const c=science.movingControls[i];const input={drones:c.drones.map(d=>({id:d.id,state:d.state.map(v=>bits(Number(v)))}))};const inputPin=create(path.join(results,'inputs',c.id+'.json'),input,128*1024);index.controls.push({id:c.id,n:c.drones.length,input:inputPin,semanticInputSha256:semantic(c.id,input),methods:['F','L'],expectedReference:science.expectedReference[i],expectedNative:science.expectedNative[i]});}
 index.complete=index.slots.length===2&&index.slots.every(s=>s.status==='captured'&&s.motion?.passed&&s.novelAgainstRetained?.passed)&&index.controls.length===4;
}catch(error){index.errors.push({type:error.constructor?.name||'Error',code:/^[a-z0-9-]+$/.test(error.message||'')?error.message:'generation-entry-exception'});}
finally{
 try{if(manifest){manifest.files.forEach(checked);checked(manifestPin);checked(publicationPin);need(same(load(path.join(results,'generation-attempt.json')),attempt),'attempt-preserved');for(const row of index.slots)for(const key of ['generation','input'])if(row[key])checked(row[key]);for(const row of index.controls)checked(row.input);index.inputsAndSourcesPreserved=true;}}catch(_){index.complete=false;index.errors.push({type:'PreservationError',code:'postrun-preservation'});}
 if(journalFd!==null){fs.fsyncSync(journalFd);fs.closeSync(journalFd);index.journal=pin(path.join(results,'generation-journal.jsonl'));}
 try{create(path.join(results,'generation.json'),index,2*1024*1024);}catch(_){process.exitCode=1;}
 if(!index.complete||index.errors.length||index.inputsAndSourcesPreserved!==true)process.exitCode=1;
}
