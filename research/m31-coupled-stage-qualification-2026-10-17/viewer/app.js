// Display saved words only. No simulation, native load, reference or checker import.
const PACKAGE='research/m31-coupled-stage-qualification-2026-10-17';
const INITIAL={path:'research/m31-native-fresh-transfer-2026-10-17/results/inputs/fresh-a-t5.json',bytes:21955,sha256:'48dc63da80d4400a948a102143e872a49645b37b08eac73f932959653a16fa7c'};
const CAP=32*1024*1024,ARMS=['coupled','off'],SHA=/^[0-9a-f]{64}$/;
const $=id=>document.getElementById(id),need=(v,c)=>{if(!v)throw Error(c);},same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const sha=async bytes=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(v=>v.toString(16).padStart(2,'0')).join('');
const decoder=new TextDecoder('utf-8',{fatal:true}),scratch=new DataView(new ArrayBuffer(8));
function number(w){need(typeof w==='string'&&/^[0-9a-f]{16}$/.test(w),'Invalid saved binary64 word');scratch.setBigUint64(0,BigInt('0x'+w),false);const n=scratch.getFloat64(0,false);need(Number.isFinite(n),'Nonfinite display word');return n;}
function url(relative){need(typeof relative==='string'&&relative&&!relative.startsWith('/')&&!relative.split('/').includes('..'),'Invalid record path');return '../../../'+relative;}
async function read(relative,optional=false){
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);let reader;
 try{const response=await fetch(url(relative),{cache:'no-store',credentials:'same-origin',signal:controller.signal});
  if(optional&&response.status===404)return null;need(response.ok,'Record unavailable: '+relative);
  const size=response.headers.get('content-length');if(size!==null)need(Number(size)<=CAP,'Record exceeds byte cap');
  reader=response.body.getReader();const parts=[];let count=0;
  for(;;){const {value,done}=await reader.read();if(done)break;count+=value.length;need(count<=CAP,'Record exceeds byte cap');parts.push(value);}
  const raw=new Uint8Array(count);let offset=0;for(const p of parts){raw.set(p,offset);offset+=p.length;}
  return {path:relative,raw,bytes:count,sha256:await sha(raw)};
 }catch(error){if(reader)await reader.cancel().catch(()=>{});throw error;}finally{if(reader)reader.releaseLock();clearTimeout(timer);}
}
function json(record){return record===null?null:JSON.parse(decoder.decode(record.raw));}
function pinMatch(record,pin){return record&&pin&&record.bytes===pin.bytes&&record.sha256===pin.sha256;}
function parseState(raw){
 need(raw&&Array.isArray(raw.drones)&&raw.drones.length===64,'Expected 64 saved drone states');
 const ids=[],poses=[],words=[];
 raw.drones.forEach((row,i)=>{need(row.id===i&&Array.isArray(row.state)&&row.state.length===17,'Stable ID/state association');const values=row.state.map(number);need(Math.hypot(...values.slice(6,10))>0,'Zero display quaternion');ids.push(row.id);poses.push({position:values.slice(0,3),quaternion:values.slice(6,10)});words.push(row.state.slice());});
 return {ids,poses,words};
}
function frame(id,arm,kind,t,raw,extra={}){const decoded=parseState(raw);need(Number.isFinite(t)&&t>=0&&t<=.020000000001,'Saved time outside continuation');return {id,arm,kind,t,...decoded,worldForces:null,status:'saved',...extra};}
const fmt=n=>Object.is(n,-0)?'-0':Math.abs(n)<1e-6&&n!==0?n.toExponential(4):n.toFixed(5);
let scene=null,sceneFailure=null,data=null,arm='coupled',stageMode=false,frameIndex=0,selectedId=0,playing=false,timer=null,loading=false;
let framesByArm={coupled:{endpoints:[],stages:[]},off:{endpoints:[],stages:[]}};
let lastScene=null,integrityFailure=null;
window.__M31_COUPLED_VIEW__={ready:false,playing:false,recordOnly:true};
function expose(){window.__M31_COUPLED_VIEW__={ready:!!data,recordOnly:true,playing,arm,stageMode,frameIndex,selectedId,integrityFailure,status:$('status-title').textContent,counts:ARMS.map(a=>({arm:a,endpoints:Math.max(0,framesByArm[a].endpoints.length-1),stages:framesByArm[a].stages.length})),scene:lastScene};}
function stop(){playing=false;if(timer!==null)clearInterval(timer);timer=null;$('play').textContent='Play';$('play').setAttribute('aria-pressed','false');expose();}
function chosen(){return framesByArm[arm][stageMode?'stages':'endpoints'];}
function rawLink(parent,label,relative){parent.replaceChildren();if(!relative)return;const a=document.createElement('a');a.textContent=label;a.href=url(relative);parent.appendChild(a);}
function updateSelection(){
 const current=chosen()[frameIndex];if(!current)return;
 $('position').textContent=current.poses[selectedId].position.map(fmt).join(' / ');
 $('force').textContent=current.worldForces?current.worldForces[selectedId].map(fmt).join(' / '):current.kind==='endpoint'?'Not recorded at endpoints':'No complete consumed-load record';
 $('record-status').textContent=current.status;
 scene?.style({scale:2,visible:$('forces').checked&&current.worldForces!==null,selectedId});expose();
}
function render(){
 const list=chosen();frameIndex=Math.max(0,Math.min(frameIndex,list.length-1));const current=list[frameIndex];
 $('scrub').max=String(Math.max(0,list.length-1));$('scrub').value=String(frameIndex);$('scrub').disabled=list.length<2;
 $('play').disabled=stageMode||list.length<2;const stageAvailable=framesByArm[arm].stages.length>0;
 $('stages').disabled=!stageAvailable;$('stages').checked=stageMode;
 $('forces').disabled=!framesByArm[arm].stages.some(f=>f.worldForces!==null);
 if(!current){scene?.clear();$('scene-empty').hidden=false;$('scene-empty').textContent='No renderable saved stage for this branch.';return;}
 $('scene-empty').hidden=!!scene;if(sceneFailure)$('scene-empty').textContent=sceneFailure;
 $('time').textContent='+'+current.t.toFixed(5)+' s';
 const branch=arm==='coupled'?'Coupled':'Airflow off';
 $('frame-label').textContent=current.kind==='stage'?`${branch} · step ${current.stepIndex+1}, k${current.stageIndex} · ${current.status}`:`${branch} · ${current.initial?'saved initial state':`saved endpoint ${current.stepIndex+1} of 8`} · ${64} drones`;
 $('selection-title').textContent=current.kind==='stage'?`Step ${current.stepIndex+1} / stage k${current.stageIndex}`:current.initial?'Saved initial state':`Endpoint ${current.stepIndex+1}`;
 $('selection-note').textContent=current.kind==='stage'?'Intermediate projected stage input. It is not an accepted endpoint or an extra trajectory sample.':current.initial?(framesByArm[arm].endpoints.length===1?'No completed motion endpoint is available for this branch. Only its saved initial state is shown.':'Pinned initial state at original time 5 s. Both branches start from these same 64 saved states.'):'Accepted endpoint read directly from the saved step record. No intermediate motion has been generated.';
 $('playback-note').textContent=stageMode?'Stage inspection: k2 and k3 share a time but have distinct saved inputs. Use the scrubber; stage playback is disabled.':'Slow replay: each recorded 2.5 ms endpoint is held for 0.5 s (200× slower). No interpolated motion.';
 rawLink($('selected-raw-link'),current.sidecar?'Exact saved stage input →':current.initial?'Pinned initial state →':current.kind==='stage'?'Read this stage in the journal →':'Read this endpoint in the journal →',current.sidecar??(current.initial?INITIAL.path:PACKAGE+'/results/browser-journal.jsonl'));
 scene?.setSnapshot(current,false);updateSelection();expose();
}
function fitEnvelope(){
 const min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity],include=p=>p.forEach((v,k)=>{min[k]=Math.min(min[k],v);max[k]=Math.max(max[k],v);});
 for(const a of ARMS)for(const f of [...framesByArm[a].endpoints,...framesByArm[a].stages])f.poses.forEach((p,i)=>{include(p.position);if(f.worldForces)include(p.position.map((x,k)=>x+2*f.worldForces[i][k]));});
 return {min,max};
}
function prepareFrames(initial,events,index,warnings){
 const result={coupled:{endpoints:[],stages:[]},off:{endpoints:[],stages:[]}};
 for(const a of ARMS)result[a].endpoints.push(frame('initial',a,'endpoint',0,initial,{initial:true,status:'Pinned initial state'}));
 const journalInitial=events.find(e=>e.kind==='initial');if(journalInitial)need(same(journalInitial.body.input,initial),'Journal initial state differs from pinned input');
 const seenStage=new Set(),seenStep=new Set();
 for(const event of events){
  const b=event.body;if(!b||!ARMS.includes(b.arm))continue;
  if(event.kind==='stage'){
   need(Number.isInteger(b.stepIndex)&&b.stepIndex>=0&&b.stepIndex<8&&Number.isInteger(b.stageIndex)&&b.stageIndex>=1&&b.stageIndex<=4&&b.stageId===`${b.arm}-step${b.stepIndex}-k${b.stageIndex}`&&!seenStage.has(b.stageId),'Duplicate or invalid stage identity');seenStage.add(b.stageId);
   if(b.status!=='completed')warnings.push(`${b.stageId}: producer recorded a failed stage.`);
   if(b.nativeInput===null){warnings.push(`${b.stageId}: no projected input was recorded.`);continue;}
   try{
    const f=frame(b.stageId,b.arm,'stage',number(b.relativeTimeWord),b.nativeInput,{stepIndex:b.stepIndex,stageIndex:b.stageIndex,status:b.status==='completed'?'Recorded stage · producer completed':'Recorded stage · failed',sidecar:index?.inputs?.[b.stageId]?.path??null});
    if(b.status==='completed'){
     need(Array.isArray(b.records)&&b.records.length===64,'Stage consumed record count');
     f.worldForces=b.records.map((r,i)=>{need(r.id===i&&same(r.stateWords,b.nativeInput.drones[i].state)&&Array.isArray(r.consumed?.worldForceWords)&&r.consumed.worldForceWords.length===3,'Stage force/state association');return r.consumed.worldForceWords.map(number);});
    }
    result[b.arm].stages.push(f);
   }catch(error){warnings.push(`${b.stageId}: display withheld (${error.message}).`);}
  }else if(event.kind==='step'){
   need(Number.isInteger(b.stepIndex)&&b.stepIndex>=0&&b.stepIndex<8&&b.stepId===`${b.arm}-step${b.stepIndex}`&&!seenStep.has(b.stepId),'Duplicate or invalid endpoint identity');seenStep.add(b.stepId);
   if(b.status!=='completed'||!Array.isArray(b.final)){warnings.push(`${b.stepId}: no completed endpoint.`);continue;}
   try{
    need(b.stepIndex===result[b.arm].endpoints.length-1,'Endpoint sequence has a gap');
    const t=number(b.relativeTimeWord);need(t>result[b.arm].endpoints.at(-1).t,'Endpoint time order');
    result[b.arm].endpoints.push(frame(b.stepId,b.arm,'endpoint',t,{drones:b.final.map(r=>({id:r.id,state:r.stateWords}))},{stepIndex:b.stepIndex,status:'Recorded endpoint · producer completed'}));
   }catch(error){warnings.push(`${b.stepId}: endpoint withheld (${error.message}).`);}
  }
 }
 return result;
}
function parseJournal(record,index,warnings){
 const text=decoder.decode(record.raw),lines=text.split('\n');
 if(lines.at(-1)==='')lines.pop();else{lines.pop();warnings.push('An unfinished final journal line was excluded.');}
 need(lines.length<=4096,'Journal record limit');const events=[];
 for(let i=0;i<lines.length;i++){
  try{const e=JSON.parse(lines[i]);need(e.sequence===i&&typeof e.kind==='string'&&e.body&&typeof e.body==='object','Journal sequence/shape');events.push(e);}
  catch(error){warnings.push(`Journal reading stopped at record ${i}: ${error.message}.`);break;}
 }
 if(index?.journal&&events.length!==index.journal.records)warnings.push('Journal parsed count differs from its saved index.');
 return events;
}
function reason(value){if(!value)return null;const e=value.firstFailure??value.errors?.[0]??value.finalizationFailure;return e?String(e.code??e.reason??e.type??'Saved failure'):null;}
function summary(view){
 const {attempt,browser,check,warnings,journalBound,browserBound,checkBound}=view;
 const on=framesByArm.coupled.endpoints.length-1,off=framesByArm.off.endpoints.length-1;
 $('on-count').textContent=on+' / 8';$('off-count').textContent=off+' / 8';
 $('check-status').textContent=check?.complete&&check.passed?'Passed · saved':check?'Failed / incomplete':'Not available';
 const complete=attempt?.status==='completed'&&['browser','reference','check'].every(s=>attempt.stages?.[s]?.status==='completed')&&browser?.complete===true&&browser.browserClosed===true&&browser.browserRootExitConfirmed===true&&browser.browserRootCloseConfirmed===true&&check?.complete===true&&check.passed===true&&journalBound&&browserBound&&checkBound&&warnings.length===0&&on===8&&off===8&&ARMS.every(a=>framesByArm[a].stages.length===32&&framesByArm[a].stages.every(s=>s.status==='Recorded stage · producer completed'));
 let title,detail,state='pending';
 if(complete){title='Saved checks passed';detail='All saved stages completed and the supervisor binds the browser/check outputs. This is numerical interface qualification for this continuation.';state='passed';}
 else if(attempt?.status==='failed'||check?.passed===false||browser?.complete===false){title='Failed or incomplete run';detail='Available saved states remain inspectable. Missing or refused stages have not been replaced.';state='failed';}
 else if(on===0&&off===0){title='No motion evidence yet';detail='Only the pinned 64-drone initial state is available. No coupled trajectory is being implied.';}
 else if(attempt?.status==='running'){title='Saved snapshot of a run in progress';detail='This page does not poll. Reload after the run closes to read its final status.';}
 else{title='Partial evidence — qualification unconfirmed';detail='Saved records are displayed, but complete bound checker and supervisor evidence is unavailable.';}
 $('status-title').textContent=title;$('status-detail').textContent=detail;$('notice').dataset.state=state;
 $('integrity').textContent=`Initial input SHA-256 verified. ${journalBound?'Journal bytes match the saved browser index.':view.events.length?'Partial journal is not bound to a completed saved index.':'No readable browser journal yet.'} ${browserBound&&checkBound?'Browser and checker bytes match supervisor output identities.':'Final supervisor output bindings are incomplete.'}`;
 const why=reason(attempt)||reason(check)||reason(browser);$('failure-note').hidden=!why;$('failure-note').textContent=why?'Saved failure: '+why:'';
 $('record-warnings').hidden=warnings.length===0;$('record-warnings').textContent=warnings.slice(0,4).join(' ')+(warnings.length>4?` ${warnings.length-4} more record notices.`:'');
}
async function ensureScene(){
 if(!scene&&!sceneFailure){try{const {createRecordedScene}=await import('./scene.js');scene=createRecordedScene($('scene'),state=>{lastScene=state;expose();});}catch(error){sceneFailure='3D rendering unavailable. Saved record details remain readable.';$('scene-empty').textContent=sceneFailure;}}
 if(!$('drone').options.length)for(let id=0;id<64;id++){const option=document.createElement('option');option.value=String(id);option.textContent='ID '+id;$('drone').appendChild(option);}
}
async function load(){
 if(loading)return;loading=true;stop();$('reload').disabled=true;integrityFailure=null;let verifiedInitial=null;
 try{
  const initialRecord=await read(INITIAL.path);need(pinMatch(initialRecord,INITIAL),'Pinned initial input hash mismatch');const initial=json(initialRecord);parseState(initial);verifiedInitial=initial;
  const [attemptRecord,browserRecord,checkRecord,journalRecord]=await Promise.all([read(PACKAGE+'/results/run-attempt.json',true),read(PACKAGE+'/results/browser.json',true),read(PACKAGE+'/results/check.json',true),read(PACKAGE+'/results/browser-journal.jsonl',true)]);
  const attempt=json(attemptRecord),browser=json(browserRecord),check=json(checkRecord),warnings=[];
  const identities=[attempt,browser,check].filter(Boolean);if(identities.length){need(identities.every(x=>SHA.test(x.sourceManifestSha256)&&/^[0-9a-f]{40}$/.test(x.sourceCommit)),'Saved source identity missing');need(identities.every(x=>x.sourceManifestSha256===identities[0].sourceManifestSha256&&x.sourceCommit===identities[0].sourceCommit),'Saved files refer to different source runs');}
  if(attempt)need(attempt.schema==='m31-coupled-stage-attempt-v1','Unexpected supervisor schema');
  if(browser)need(browser.schema==='m31-coupled-stage-browser-v1','Unexpected browser schema');
  if(check)need(check.schema==='m31-coupled-stage-check-v1','Unexpected checker schema');
  let journalBound=false,browserBound=false,checkBound=false;
  if(browser?.journal){need(browser.journal.path===PACKAGE+'/results/browser-journal.jsonl','Unexpected journal path');need(pinMatch(journalRecord,browser.journal),'Journal hash differs from saved index');journalBound=true;}
  if(attempt?.stages?.browser?.output){need(pinMatch(browserRecord,attempt.stages.browser.output),'Browser hash differs from supervisor');browserBound=true;}
  if(attempt?.stages?.check?.output){need(pinMatch(checkRecord,attempt.stages.check.output),'Checker hash differs from supervisor');checkBound=true;}
  const events=journalRecord?parseJournal(journalRecord,browser,warnings):[];
  const next=prepareFrames(initial,events,browser,warnings);framesByArm=next;data={initial,attempt,browser,check,events,warnings,journalBound,browserBound,checkBound};
  await ensureScene();$('arm').disabled=false;$('drone').disabled=false;$('reset').disabled=!scene;
  frameIndex=0;stageMode=false;$('forces').checked=false;summary(data);scene?.setFitEnvelope(fitEnvelope());render();scene?.reset();
 }catch(error){
  integrityFailure=error.message;data=null;scene?.clear();lastScene=null;stageMode=false;frameIndex=0;$('forces').checked=false;
  framesByArm={coupled:{endpoints:[],stages:[]},off:{endpoints:[],stages:[]}};
  if(verifiedInitial){framesByArm=prepareFrames(verifiedInitial,[],null,[]);data={initial:verifiedInitial,baseOnly:true};await ensureScene();scene?.setFitEnvelope(fitEnvelope());render();scene?.reset();}
  $('notice').dataset.state='integrity';$('status-title').textContent='Evidence could not be verified';$('status-detail').textContent=error.message;
  $('on-count').textContent='0 / 8';$('off-count').textContent='0 / 8';$('check-status').textContent='Unverified';
  if(!verifiedInitial){$('scene-empty').hidden=false;$('scene-empty').textContent='No unverified motion is shown.';}
  for(const id of ['arm','stages','forces','play','scrub'])$(id).disabled=true;
  $('drone').disabled=!verifiedInitial;$('reset').disabled=!verifiedInitial||!scene;
  $('integrity').textContent=verifiedInitial?'The pinned initial state is verified and remains visible. Motion/loads are withheld; inspect the raw files and reload when complete.':'Record loading stopped. Inspect the raw files and reload when complete.';
  $('failure-note').hidden=true;$('record-warnings').hidden=true;
 }finally{loading=false;$('reload').disabled=false;expose();}
}
$('arm').addEventListener('change',()=>{stop();arm=$('arm').value;frameIndex=0;if(!framesByArm[arm].stages.length)stageMode=false;if(!stageMode)$('forces').checked=false;render();});
$('stages').addEventListener('change',()=>{stop();stageMode=$('stages').checked;frameIndex=0;if(!stageMode)$('forces').checked=false;render();});
$('forces').addEventListener('change',()=>{stop();if($('forces').checked&&!stageMode){stageMode=true;frameIndex=0;}render();});
$('scrub').addEventListener('input',()=>{stop();frameIndex=Number($('scrub').value);render();});
$('drone').addEventListener('change',()=>{selectedId=Number($('drone').value);updateSelection();});
$('reset').addEventListener('click',()=>scene?.reset());$('reload').addEventListener('click',load);
$('play').addEventListener('click',()=>{if(playing){stop();return;}if(stageMode||chosen().length<2)return;if(frameIndex===chosen().length-1)frameIndex=0;playing=true;$('play').textContent='Pause';$('play').setAttribute('aria-pressed','true');render();timer=setInterval(()=>{if(frameIndex>=chosen().length-1){stop();return;}frameIndex++;render();if(frameIndex===chosen().length-1)stop();},500);expose();});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
load();
