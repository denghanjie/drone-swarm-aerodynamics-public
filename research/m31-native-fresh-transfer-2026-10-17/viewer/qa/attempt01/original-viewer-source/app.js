// Saved-record display only. No simulator, reference, native query or checker imports.
const BINDING_SHA='efe52b55952a948246574bf024d949f3a39897b741de65caf231d960ae5b4be3';
const PACKAGE='research/m31-native-fresh-transfer-2026-10-17';
const PLAN=[{id:'fresh-a-t5',seed:26171711,methods:['F','L']},{id:'fresh-b-t5',seed:26171712,methods:['L','F']}];
const MOVING=['positive','distant-zero','raw-force','order-incompatible'];
const STAGES=['generation','reference','browser','check'];
const SCHEDULE=PLAN.flatMap(p=>p.methods.map(method=>({caseId:p.id,method})));
const CATEGORIES=['rotor','collective','worldForce','worldMoment'];
const $=id=>document.getElementById(id),same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const need=(ok,label)=>{if(!ok)throw Error(label);};
const hash=x=>typeof x==='string'&&/^[a-f0-9]{64}$/.test(x);
const word=x=>typeof x==='string'&&/^[a-f0-9]{16}$/.test(x);
const sha=async b=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',b))].map(x=>x.toString(16).padStart(2,'0')).join('');
const canonical=x=>Array.isArray(x)?'['+x.map(canonical).join(',')+']':x&&typeof x==='object'?'{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}':JSON.stringify(x);
const pinEqual=(a,b)=>a&&b&&a.path===b.path&&a.bytes===b.bytes&&a.sha256===b.sha256;
function el(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
const scratch=new DataView(new ArrayBuffer(8));
function number(w){need(word(w),'Malformed saved binary64 word');scratch.setBigUint64(0,BigInt('0x'+w),false);const n=scratch.getFloat64(0,false);need(Number.isFinite(n),'Nonfinite saved display word');return n;}
const fmt=x=>Object.is(x,-0)?'-0':x===0?'0':x.toExponential(6);
let binding=null,records=new Map(),runs=new Map(),scene=null,lastScene=null,runId=PLAN[0].id,method='F',frameIndex=0,droneId=0,playing=false,timer=null,integrityFailure=null;
const output=name=>binding?.stages[name]?.output?records.get(binding.stages[name].output.path):null;
const attempt=name=>binding?.stages[name]?.attempt?records.get(binding.stages[name].attempt.path):null;
const knownPin=p=>binding?.pins.find(x=>x.path===p);
function boundRecord(pin){need(pinEqual(pin,knownPin(pin?.path)),'Unbound record association');const value=records.get(pin.path);need(value,'Pinned JSON unavailable');return value;}
function sourceBound(value){need(value&&value.sourceCommit===binding.sourceCommit&&value.sourceManifestSha256===binding.sourceManifestSha256,'Saved source identity mismatch');}
function closed(name){const a=attempt(name),p=binding?.stages[name]?.output;return !!(a&&p&&a.status==='completed'&&a.exitCode===0&&a.childExitCode===0&&a.childReaped===true&&a.preservationPassed===true&&a.outputBytes===p.bytes&&a.outputSha256===p.sha256);}
async function readPin(pin){
 need(pin&&typeof pin.path==='string'&&!pin.path.startsWith('/')&&!pin.path.split('/').includes('..')&&Number.isSafeInteger(pin.bytes)&&pin.bytes>0&&pin.bytes<=33554432&&hash(pin.sha256),'Invalid saved pin');
 const response=await fetch('../../../'+pin.path,{cache:'no-store',credentials:'same-origin'});need(response.ok,'Pinned record unavailable: '+pin.path);
 const raw=await response.arrayBuffer();need(raw.byteLength===pin.bytes&&await sha(raw)===pin.sha256,'Pinned record changed: '+pin.path);
 return pin.path.endsWith('.json')?JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(raw)):null;
}
function validateRaw(raw){
 need(raw&&same(Object.keys(raw),['drones'])&&Array.isArray(raw.drones)&&raw.drones.length===64,'Saved raw shape');
 const ids=raw.drones.map(x=>x.id);need(ids.every((x,i)=>Number.isSafeInteger(x)&&x>=0&&(i===0||x>ids[i-1])),'Saved stable ID order');
 for(const row of raw.drones){need(row.state?.length===17&&row.state.every(word),'Saved state words');row.state.forEach(number);}return ids;
}
const poses=raw=>raw.drones.flatMap(x=>x.state.slice(0,3).concat(x.state.slice(6,10)));
async function validateRecords(){
 const manifest=boundRecord(binding.manifest),publication=boundRecord(binding.publication);
 need(binding.manifest.path===PACKAGE+'/source-manifest.json'&&binding.manifest.sha256===binding.sourceManifestSha256,'Source manifest binding');
 need(publication.commit===binding.sourceCommit&&publication.manifestSha256===binding.sourceManifestSha256&&publication.manifestBytes===binding.manifest.bytes&&publication.verifiedFilePins===manifest.files.length&&publication.remoteBytesEqualLocal===true&&publication.committedBytesEqualLocal===true,'Published source receipt');
 const science=boundRecord(binding.science);need(pinEqual(binding.science,manifest.files.find(p=>p.path===binding.science.path))&&science.schema==='m31-native-fresh-science-config-v1','Frozen science configuration');
 need(same(science.slots.map(x=>({id:x.id,seed:x.seed,methods:x.methods})),PLAN)&&science.slots.every(x=>x.n===64&&x.t===5),'Fixed fresh slots');
 need(science.generation.mode==='boids'&&science.generation.airflow==='off'&&science.generation.duration===5&&science.generation.frameEvery===.2,'Recorded flight configuration');
 for(const name of STAGES){const a=attempt(name),o=output(name);if(a){sourceBound(a);need(a.schema==='m31-native-fresh-attempt-v1'&&a.stage===name,'Stage receipt identity');if(a.status==='completed')need(closed(name),'Completed receipt does not bind its output');}if(o)sourceBound(o);}
 const g=output('generation'),r=output('reference'),b=output('browser'),c=output('check');
 if(g){need(g.schema==='m31-native-fresh-generation-v1'&&same(g.slots.map(x=>x.id),PLAN.map(x=>x.id)),'Two generation slots');
  for(const [i,p]of PLAN.entries()){
   const row=g.slots[i];need(row.seed===p.seed&&row.t===5&&row.n===64&&same(row.methods,p.methods),'Generation slot identity');
   if(!row.generation){runs.set(p.id,{row,record:null,ids:[],frames:[]});continue;}
   const rec=boundRecord(row.generation);sourceBound(rec);need(rec.schema==='m31-native-fresh-generation-record-v1'&&rec.id===p.id&&rec.seed===p.seed,'Generation record identity');
   need(rec.requested.mode==='boids'&&rec.requested.airflow==='off'&&rec.requested.duration===5,'Recorded mode identity');
   const ids=rec.initial?validateRaw(rec.initial):[];
   need(Array.isArray(rec.frames)&&rec.frames.length<=26,'Saved frame count');
   rec.frames.forEach((f,j)=>{need(Number.isFinite(f.t)&&f.t>=0&&f.t<=5&&(j===0||f.t>rec.frames[j-1].t)&&f.words?.length===448&&f.words.every(word),'Saved frame shape/time');f.words.forEach(number);});
   if(rec.frames.length){need(ids.length===64&&rec.frames[0].t===0&&same(rec.frames[0].words,poses(rec.initial)),'Initial pose association');}
   let raw=null;
   if(row.input){raw=boundRecord(row.input);need(same(validateRaw(raw),ids),'Final ID association');need(same(raw,rec.snapshot)&&same(raw,rec.final)&&same(rec.frames.at(-1)?.words,poses(raw))&&rec.frames.at(-1)?.t===5,'Final raw/pose association');const semantic=await sha(new TextEncoder().encode(canonical({domain:science.semanticInputDomain,id:p.id,input:raw})));need(semantic===row.semanticInputSha256,'Final raw semantic identity');}
   if(row.status==='captured')need(rec.status==='captured'&&raw&&same(rec.frames.map(x=>x.t),Array.from({length:26},(_,j)=>Number((j*.2).toFixed(6))))&&same(rec.initial,rec.returnedInitial),'Complete saved sequence');
   runs.set(p.id,{row,record:rec,ids,frames:rec.frames,raw});
  }
 }
 if(r){need(r.schema==='m31-native-fresh-reference-index-v1','Reference schema');if(r.generationIndex)need(pinEqual(r.generationIndex,binding.stages.generation.output),'Reference generation binding');}
 if(b){need(b.schema==='m31-native-browser-qualification-v1','Browser schema');if(b.generationIndex)need(pinEqual(b.generationIndex,binding.stages.generation.output),'Browser generation binding');if(b.referenceIndex)need(pinEqual(b.referenceIndex,binding.stages.reference.output),'Browser reference binding');validateCalls(b.calls??[],SCHEDULE);validateCalls(b.movingControlCalls??[],MOVING.flatMap(caseId=>['F','L'].map(method=>({caseId,method}))));}
 if(c){need(c.schema==='m31-native-fresh-load-check-v1','Checker schema');if(c.passed===true){need(pinEqual(c.generationIndex,binding.stages.generation.output)&&pinEqual(c.referenceIndex,binding.stages.reference.output)&&c.browserOutputSha256===binding.stages.browser.output?.sha256,'Checker output association');need(c.attemptedTargetCalls===4&&c.calls?.length===4&&same(c.calls.map(x=>({caseId:x.caseId,method:x.method})),SCHEDULE),'Checker target denominator');need(c.attemptedMovingControlCalls===8&&c.movingControls?.length===8,'Checker moving denominator');need(c.originalSupervisorRepaired===false&&c.performanceClaim===false&&c.onlineCertificationClaim===false,'Checker claim scope');}}
}
function validateCalls(calls,schedule){
 need(Array.isArray(calls)&&calls.length<=schedule.length,'Native schedule bound');
 calls.forEach((call,i)=>{need(call.sequence===i&&call.caseId===schedule[i].caseId&&call.method===schedule[i].method,'Native saved schedule');need(call.evidence?.schema==='m31-native-load-evidence-v1'&&call.evidence.caseId===call.caseId&&call.evidence.method===call.method,'Native evidence association');});
}
const nativeCall=(id,m)=>output('browser')?.calls?.find(x=>x.caseId===id&&x.method===m);
const checkedCall=(id,m)=>output('check')?.calls?.find(x=>x.caseId===id&&x.method===m);
function qualifiedGlobal(){
 const g=output('generation'),r=output('reference'),b=output('browser'),c=output('check');
 return !!(STAGES.every(closed)&&g?.complete&&g.inputsAndSourcesPreserved&&r?.complete&&r.qualified&&r.inputsAndSourcesPreserved&&b?.complete&&b.inputsAndSourcesPreserved&&b.browserClosed&&b.browserRootExitConfirmed&&b.browserRootCloseConfirmed&&b.browserRoot?.exit?.code===0&&b.browserRoot.exit.signal===null&&b.browserRoot.close?.code===0&&b.browserRoot.close.signal===null&&b.browserRoot.error===null&&c?.passed&&c.decision==='qualified'&&c.inputsAndSourcesPreserved&&c.qualifiedTargetCalls===4&&c.qualifiedMovingControlCalls===8);
}
function eligible(id,m){
 const run=runs.get(id),call=nativeCall(id,m),check=checkedCall(id,m),ref=output('reference')?.targets?.find(x=>x.id===id);
 return !!(qualifiedGlobal()&&run?.raw&&run.row.status==='captured'&&run.row.motion?.passed&&run.row.novelAgainstRetained?.passed&&ref?.qualified&&ref.referenceStatus==='admitted'&&ref.branch==='loads'&&ref.graphStatus==='acyclic-compatible'&&ref.positiveRotorPairs>0&&call?.evidence.status==='native-success'&&check?.qualified&&check.decision==='qualified'&&CATEGORIES.every(k=>check.errors?.[k]?.decision==='pass'));
}
function actualLoads(id,m){
 const run=runs.get(id),call=nativeCall(id,m),e=call.evidence,raw=run.raw;
 need(call.inputUnchanged===true&&call.ownership?.pass===true&&call.inputFileSha256===run.row.input.sha256&&call.semanticInputSha256===run.row.semanticInputSha256,'Native final input association');
 need(e.inputFileSha256===call.inputFileSha256&&e.semanticInputSha256===call.semanticInputSha256&&same(e.raw,raw.drones)&&same(e.ids,run.ids),'Native raw words/IDs');
 need(e.loads?.length===64&&same(e.loads.map(x=>x.id),run.ids),'Native load ID association');
 for(const load of e.loads){need(load.rotor?.length===4&&load.worldForce?.length===3&&load.worldMoment?.length===3,'Saved load shape');[...load.rotor,load.collective,...load.worldForce,...load.worldMoment].forEach(number);}return e.loads;
}
function stateText(name){const a=attempt(name),o=output(name);return integrityFailure?'Integrity failure':!a?'Not bound':a.status==='completed'?(name==='check'?o?.decision??'Completed':name==='reference'&&o?.qualified===true?'Qualified':'Completed'):a.status;}
function renderSummary(){
 for(const name of STAGES){const a=attempt(name),o=output(name),passed=closed(name)&&(name!=='check'||o?.decision==='qualified')&&(name!=='reference'||o?.qualified===true);$(name+'-status').textContent=stateText(name);$(name+'-status').className=passed?'pass':a?'bad':'pending';$(name+'-detail').textContent=a?('Child '+String(a.childExitCode??'—')+' · supervisor '+String(a.exitCode??'—')+(o?.reason?' · '+o.reason:'')):'No saved stage receipt bound.';}
 const g=output('generation'),b=output('browser'),c=output('check');
 $('summary').textContent=integrityFailure?'Integrity failure: no replay or loads are shown. All fixed outcome slots remain below.':`${g?.slots?.filter(x=>x.status==='captured').length??0} / 2 complete captures · ${b?.calls?.length??0} / 4 returned target calls · ${c?.qualifiedTargetCalls??0} / 4 saved qualified calls. ${qualifiedGlobal()?'Final arrows are available at the recorded 5 s endpoints.':'Final arrows are withheld until every saved gate qualifies.'}`;
 $('all-results').replaceChildren();
 for(const [i,p]of PLAN.entries()){const run=runs.get(p.id),tr=el('tr'),cell=el('td'),button=el('button',(i===0?'A':'B')+' · '+p.seed,'state-link'+(runId===p.id?' current':''));button.disabled=!binding||!!integrityFailure;button.addEventListener('click',()=>chooseRun(p.id));cell.append(button);tr.append(cell,el('td',integrityFailure?'Not accepted':(run?.row.status??'Not available')+' · '+(run?.frames.length??0)+' frames'));
  for(const m of ['F','L']){const call=nativeCall(p.id,m),check=checkedCall(p.id,m);tr.append(el('td',integrityFailure?'Not accepted':call?call.evidence.status+(call.evidence.reason?' · '+call.evidence.reason:''):'Not returned'),el('td',integrityFailure?'Not accepted':check?.decision??'Not available',check?.qualified?'pass':'pending'));}
  const parity=output('check')?.nativeParity?.find(x=>x.caseId===p.id);tr.append(el('td',parity?(parity.matches?'Same saved outputs':'Different outputs'):'Not available'));$('all-results').append(tr);
 }
 $('moving-results').replaceChildren();for(const id of MOVING)for(const m of ['F','L']){const call=output('browser')?.movingControlCalls?.find(x=>x.caseId===id&&x.method===m),check=output('check')?.movingControls?.find(x=>x.caseId===id&&x.method===m),tr=el('tr');tr.append(el('td',id),el('td',m),el('td',integrityFailure?'Not accepted':call?call.evidence.status+(call.evidence.reason?' · '+call.evidence.reason:''):'Not returned'),el('td',integrityFailure?'Not accepted':check?.decision??'Not available'));$('moving-results').append(tr);}
}
function stop(){playing=false;if(timer!==null)clearTimeout(timer);timer=null;$('play').textContent='Play';expose();}
function expose(){window.__freshViewerState={bound:!!binding&&!integrityFailure,integrityFailure,runId,method,frameIndex,frameTime:runs.get(runId)?.frames[frameIndex]?.t??null,playing,qualified:!integrityFailure&&eligible(runId,method),render:lastScene};}
function fail(error){stop();integrityFailure=error.message||'Saved-record validation failed';runs.clear();records.clear();scene?.clear();lastScene=null;for(const node of document.querySelectorAll('.controls select,.controls button,.controls input,.timeline button,.timeline input'))node.disabled=true;$('scene-empty').hidden=false;$('scene-empty').textContent='Replay cleared: saved records did not pass integrity checks.';$('load-results').replaceChildren();$('exact-record').textContent='No accepted saved call.';$('selection-summary').textContent='No qualified final selection.';$('frame-status').textContent='No accepted frame.';$('time').textContent='—';$('notice').textContent=integrityFailure;$('notice').className='error';renderSummary();expose();}
function renderSelection(resetCamera=false){
 try{
  need(PLAN.some(p=>p.id===runId)&&['F','L'].includes(method),'Unknown fixed selection');
  const run=runs.get(runId),frame=run?.frames[frameIndex];$('load-results').replaceChildren();lastScene=null;
  const check=checkedCall(runId,method),call=nativeCall(runId,method);$('exact-record').textContent=JSON.stringify({caseId:runId,method,nativeStatus:call?.evidence.status??null,nativeReason:call?.evidence.reason??null,check:check??null},null,2);
  if(!frame){scene?.clear();$('scene-empty').hidden=false;$('scene-empty').textContent='No recorded frames are available for this fixed run slot.';$('frame-status').textContent=(run?.row.status??'Not available')+' · no pose inferred.';$('selection-summary').textContent='No qualified final selection.';$('time').textContent='—';for(const id of ['initial','previous','play','next','final','frame','drone','reset','method','arrows','scale'])$(id).disabled=true;renderSummary();expose();return;}
  const final=frame.t===5&&frameIndex===run.frames.length-1,can=eligible(runId,method),loads=final&&can?actualLoads(runId,method):null;
  const decoded=Array.from({length:64},(_,i)=>{const w=frame.words.slice(i*7,i*7+7);return{position:w.slice(0,3).map(number),quaternion:w.slice(3).map(number)};});
  scene.style({scale:Number($('scale').value),visible:$('arrows').checked&&!!loads,selectedId:droneId});
  scene.setSnapshot({id:runId,method,ids:run.ids,poses:decoded,worldForces:loads?loads.map(x=>x.worldForce.map(number)):null},resetCamera);
  $('scene-empty').hidden=true;$('frame').max=String(run.frames.length-1);$('frame').value=String(frameIndex);$('time').textContent=frame.t.toFixed(1)+' s · '+(frameIndex+1)+'/'+run.frames.length;
  $('frame-status').textContent=`Recorded frame ${frameIndex+1} of ${run.frames.length} at ${frame.t.toFixed(1)} s. ${run.row.status==='captured'?'Complete 5 s capture.':'Incomplete saved capture: '+run.row.status+'.'} ${loads?'Qualified posthoc '+method+' forces at the final pose.':'Recorded Boids poses only; no aerodynamic forces at this selection.'}`;
  for(const id of ['initial','final','frame','drone','reset'])$(id).disabled=false;$('previous').disabled=frameIndex===0;$('next').disabled=frameIndex===run.frames.length-1;$('play').disabled=run.frames.length<2;
  $('method').disabled=!['F','L'].some(m=>eligible(runId,m));$('arrows').disabled=!loads;$('scale').disabled=!loads;
  $('selection-summary').textContent=loads?`Run ${runId} · 5.0 s · ${method} · drone ${droneId}. Exact saved native words; qualified by the bound checker.`:final?'Final state selected; scientific qualification is unavailable or failed. Native arrows and load display are withheld.':'Select the final frame to inspect qualified posthoc loads.';
  if(loads){const load=loads.find(x=>x.id===droneId);for(const [key,label]of [['rotor','Rotor thrust (N)'],['collective','Collective thrust (N)'],['worldForce','World force (N)'],['worldMoment','World moment (N·m)']]){const values=Array.isArray(load[key])?load[key]:[load[key]],tr=el('tr'),exact=el('td');exact.append(el('code',values.join(' ')));tr.append(el('th',label),el('td',values.map(x=>fmt(number(x))).join(', ')),exact);$('load-results').append(tr);}$('exact-record').textContent=JSON.stringify({caseId:runId,method,frameIndex,frameTime:frame.t,input:run.row.input,fieldPath:'calls['+call.sequence+'].evidence.loads',load,check},null,2);}
  renderSummary();expose();
 }catch(error){fail(error);}
}
function seek(index){stop();frameIndex=index;renderSelection();}
function chooseRun(id){stop();runId=id;frameIndex=0;$('run').value=id;const ids=runs.get(id)?.ids??[];droneId=ids[0]??0;$('drone').replaceChildren(...ids.map(id=>{const o=el('option',String(id));o.value=String(id);return o;}));renderSelection(true);}
function tick(){const frames=runs.get(runId)?.frames??[];if(!playing||frameIndex>=frames.length-1){stop();return;}frameIndex++;renderSelection();if(playing&&frameIndex<frames.length-1){const gap=Math.max(1,(frames[frameIndex+1].t-frames[frameIndex].t)*1000);timer=setTimeout(tick,gap);}else stop();}
$('run').addEventListener('change',()=>chooseRun($('run').value));$('method').addEventListener('change',()=>{stop();method=$('method').value;renderSelection();});$('drone').addEventListener('change',()=>{droneId=Number($('drone').value);renderSelection();});
$('frame').addEventListener('input',()=>seek(Number($('frame').value)));$('initial').addEventListener('click',()=>seek(0));$('final').addEventListener('click',()=>seek((runs.get(runId)?.frames.length??1)-1));$('previous').addEventListener('click',()=>seek(Math.max(0,frameIndex-1)));$('next').addEventListener('click',()=>seek(Math.min((runs.get(runId)?.frames.length??1)-1,frameIndex+1)));
$('play').addEventListener('click',()=>{if(playing){stop();return;}const frames=runs.get(runId)?.frames??[];if(frameIndex>=frames.length-1){frameIndex=0;renderSelection();}playing=true;$('play').textContent='Pause';timer=setTimeout(tick,Math.max(1,((frames[frameIndex+1]?.t??frames[frameIndex].t)-frames[frameIndex].t)*1000));expose();});
for(const id of ['scale','arrows'])$(id).addEventListener('change',()=>renderSelection());$('reset').addEventListener('click',()=>scene?.reset());document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
async function main(){
 need(hash(BINDING_SHA),'Source-only draft: saved result identities have not been bound.');
 const response=await fetch('binding.json',{cache:'no-store'});need(response.ok,'Viewer binding unavailable');const bytes=await response.arrayBuffer();need(bytes.byteLength<=131072&&await sha(bytes)===BINDING_SHA,'Viewer binding identity differs');
 binding=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes));need(binding.schema==='m31-native-fresh-view-binding-v1'&&binding.package===PACKAGE&&/^[a-f0-9]{40}$/.test(binding.sourceCommit)&&hash(binding.sourceManifestSha256),'Viewer source identity');need(Array.isArray(binding.pins)&&new Set(binding.pins.map(p=>p.path)).size===binding.pins.length&&binding.pins.length<=40,'Bound record inventory');
 need(same(Object.keys(binding.stages),STAGES),'Four explicit stage slots');
 need(same(binding.dependencies?.map(p=>p.path),['outputs/step02b-source/vendor/three.module.js','outputs/step02b-source/vendor/three.core.js','outputs/step02b-source/vendor/OrbitControls.js'])&&binding.dependencies.every(p=>pinEqual(p,knownPin(p.path))),'Pinned scene dependency closure');
 for(const pin of binding.pins)records.set(pin.path,await readPin(pin));
 await validateRecords();for(const p of PLAN)for(const m of ['F','L'])if(eligible(p.id,m))actualLoads(p.id,m);
 const module=await import('./scene.js');scene=module.createRecordedScene($('scene'),state=>{lastScene=state;expose();});
 $('run').disabled=false;$('notice').textContent='Pinned saved records accepted. Replay and posthoc qualification are shown separately.';$('notice').className='';
 $('identity').textContent='Source '+binding.sourceCommit+' · manifest '+binding.sourceManifestSha256;
 $('summary-detail').textContent='The viewer reads saved decisions and words. It does not execute the scientific checker or repair earlier outcomes.';
 $('pins').replaceChildren();for(const pin of binding.pins.filter(p=>p.path.endsWith('.json'))){const li=el('li'),a=el('a',pin.path);a.href='../../../'+pin.path;li.append(a,el('small',' · '+pin.bytes+' bytes · '+pin.sha256));$('pins').append(li);}
 chooseRun(runId);
}
renderSummary();main().catch(fail);
