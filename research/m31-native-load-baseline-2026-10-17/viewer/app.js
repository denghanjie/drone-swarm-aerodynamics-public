// Saved output display. This file imports no native/exact model or numerical solver.
const BINDING_SHA='55257067b0877c42d0b5f91af755f5ee0af5c496fdf66761200706d722984b6b';
const PACKAGE='research/m31-native-load-baseline-2026-10-17',AUDIT_PACKAGE='research/m31-native-saved-audit-2026-10-17';
const SOURCE='e6f99b140c70887fa0ed05c14574221eb5db12da',MANIFEST='8bae9d039d2fbfd40a34085b1bc00f3c76725c57675ea2a681121add083f4019';
const BROWSER_SHA='2f1a599000e782f1ac50163cf05fd046b7fb3c20e9ed350c7566b8c9fce900fe',ATTEMPT_SHA='2d9db1aa6db0f61118ab735a7db6d2dca919a0a48d94b0a1cf49a4f5e9ad2c33';
const AUDIT_SOURCE='eb049deb66c4c7aee78826b2eecde8281d02a1b9',AUDIT_MANIFEST='7ca777cfe98e6498d8cc789244f3f3d14223a45f807c60c7e8a99913d64ac3c1';
const AUDIT_REPORT_SHA='e4b93e1b5d03f378b2d7ac254256fcb7deb2e3371dc4dd70136ec6c376974080';
const PLAN=['run-a','run-b'].flatMap(runId=>[0,5,10].map(t=>({id:runId+'-t'+t,runId,t})));
const SCHEDULE=PLAN.flatMap((p,i)=>(i%2?['L','F']:['F','L']).map(method=>({caseId:p.id,method})));
const CATEGORIES=['rotor','collective','worldForce','worldMoment'];
const FIXTURES=['one-word','signed-zero','minimum-subnormal','halfway-even-down','halfway-even-up','subnormal-half-to-zero','negative-halfway-even','scalar-inside-box','euclidean-3-4-5','strict-threshold-inclusive','strict-threshold-fail','reference-overlap-unresolved','rational-square-root-enclosure','signed-moment-cancellation'];
const CORRUPTIONS=['load-word','squared-force-law','body-frame-force','load-id-association'];
const LABELS={rotor:'Rotor thrust / (mg/4)',collective:'Collective thrust / mg',worldForce:'World force norm / mg',worldMoment:'World moment norm / (mg R)'};
const $=id=>document.getElementById(id),same=(a,b)=>JSON.stringify(a)===JSON.stringify(b),need=(ok,label)=>{if(!ok)throw Error(label);};
const sha=async value=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',typeof value==='string'?new TextEncoder().encode(value):value))].map(v=>v.toString(16).padStart(2,'0')).join('');
function canonical(value){if(Array.isArray(value))return '['+value.map(canonical).join(',')+']';if(value&&typeof value==='object')return '{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+canonical(value[k])).join(',')+'}';return JSON.stringify(value);}
function el(tag,text,cls){const node=document.createElement(tag);if(text!==undefined)node.textContent=text;if(cls)node.className=cls;return node;}
function hash(value){return typeof value==='string'&&/^[a-f0-9]{64}$/.test(value);}
function word(value){return typeof value==='string'&&/^[a-f0-9]{16}$/.test(value);}
const scratch=new DataView(new ArrayBuffer(8));
function number(value){need(word(value),'Malformed native binary64 word');scratch.setBigUint64(0,BigInt('0x'+value),false);const n=scratch.getFloat64(0,false);need(Number.isFinite(n),'Nonfinite saved word');return n;}
const fmt=n=>Object.is(n,-0)?'-0':n===0?'0':n.toExponential(6);
function rational(q){return q&&typeof q.n==='string'&&typeof q.d==='string'&&q.n.length<=4096&&q.d.length<=4096&&/^(0|[1-9][0-9]*)$/.test(q.n)&&/^[1-9][0-9]*$/.test(q.d);}
function interval(box){return box&&rational(box.l)&&rational(box.u)&&BigInt(box.l.n)*BigInt(box.u.d)<=BigInt(box.u.n)*BigInt(box.l.d);}
function decimal(q){if(q.n==='0')return '0';return(Number(q.n.slice(0,16))/Number(q.d.slice(0,16))*10**(q.n.length-Math.min(q.n.length,16)-q.d.length+Math.min(q.d.length,16))).toExponential(3);}
function pinEqual(a,b){return a&&b&&a.path===b.path&&a.bytes===b.bytes&&a.sha256===b.sha256;}
let binding=null,data=null,audit=null,auditFailure=null,scene=null,lastScene=null,stateId=PLAN[0].id,method='F',droneId=0;
function knownPin(path){return binding.pins.find(pin=>pin.path===path);}
async function readPin(pin,cap=16*1024*1024){
 need(pin&&typeof pin.path==='string'&&!pin.path.startsWith('/')&&!pin.path.split('/').includes('..')&&Number.isSafeInteger(pin.bytes)&&pin.bytes>0&&pin.bytes<=cap&&hash(pin.sha256),'Invalid evidence pin');
 const response=await fetch('../../../'+pin.path,{cache:'no-store'});need(response.ok,'Pinned record unavailable');const bytes=await response.arrayBuffer();need(bytes.byteLength===pin.bytes&&await sha(bytes)===pin.sha256,'Pinned record digest differs');return JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes));
}
async function validateData(model){
 need(model.schema==='m31-native-load-display-v1'&&model.package===PACKAGE&&model.sourceCommit===SOURCE&&model.sourceManifestSha256===MANIFEST,'Native display identity');
 need(same(model.states.map(s=>({id:s.id,runId:s.runId,t:s.t})),PLAN),'Six-state schedule');
 need(model.nativeBrowser.internalComplete===true&&model.nativeBrowser.returnedCalls===12&&model.nativeBrowser.browserOutputSha256===BROWSER_SHA,'Saved browser completion');
 const attempt=model.originalAttempt;need(attempt.status==='failed'&&attempt.exitCode===1&&attempt.childExitCode===0&&attempt.cleanupError===true&&attempt.firstFailure.type==='PermissionError','Original failed supervision must remain visible');
 for(const state of model.states){
  need(state.ids.length===64&&new Set(state.ids).size===64&&state.ids.every((id,i)=>Number.isSafeInteger(id)&&id>=0&&(i===0||id>state.ids[i-1])),'Stable ID order');
  need(state.poseWords.length===64&&state.poseWords.every(words=>words.length===7&&words.every(word)),'Saved pose shape');state.poseWords.flat().forEach(number);
  need(same(Object.keys(state.methods),['F','L']),'Two native methods');
  for(const m of ['F','L']){
   const call=state.methods[m];need(call.status==='native-success'&&call.reason===null&&hash(call.inputFileSha256)&&hash(call.semanticInputSha256),'Saved native call');
   need(SCHEDULE[call.sequence]?.caseId===state.id&&SCHEDULE[call.sequence]?.method===m&&call.fieldPath==='calls['+call.sequence+'].evidence','Native output field address');
   need(call.loads.length===64&&same(call.loads.map(load=>load.id),state.ids),'Delivered-load ID order');
   for(const load of call.loads){need(load.rotor.length===4&&load.worldForce.length===3&&load.worldMoment.length===3,'Delivered load shape');[...load.rotor,load.collective,...load.worldForce,...load.worldMoment].forEach(number);}
   need(await sha(canonical({ids:state.ids,loads:call.loads}))===call.loadWordsSha256,'Delivered-word projection digest');
  }
 }
}
function strictCall(row){
 if(row.nativeStatus!=='native-success'||row.referenceStatus!=='admitted'||row.qualified!==true||row.decision!=='qualified')return false;
 if(!row.identity||!['raw','constants','prepared'].every(key=>row.identity[key]===true)||row.support?.matches!==true||row.support.missingCount!==0||row.support.extraCount!==0||row.support.nativePositiveCount!==row.support.exactPositiveCount||row.consumptionMatches!==true||row.loadArithmetic?.passed!==true||row.loadArithmetic.failureCount!==0)return false;
 return CATEGORIES.every(category=>{const e=row.errors?.[category];return e?.decision==='pass'&&interval(e.normalizedError)&&interval(e.normalizedSquaredError)&&BigInt(e.normalizedSquaredError.u.n)*10000000000000000n<=BigInt(e.normalizedSquaredError.u.d);});
}
async function loadAudit(){
 if(binding.audit===null)return;
 const link=binding.audit;need(link.schema==='m31-native-saved-audit-view-link-v1'&&link.package===AUDIT_PACKAGE&&link.sourceCommit===AUDIT_SOURCE&&link.manifest.sha256===AUDIT_MANIFEST&&link.report.sha256===AUDIT_REPORT_SHA,'Audit source binding');
 for(const name of ['manifest','publication','attempt','report'])need(pinEqual(link[name],knownPin(link[name].path))&&link[name].path.startsWith(AUDIT_PACKAGE+'/'),'Audit evidence pin');
 const [manifest,publication,attempt,report]=await Promise.all(['manifest','publication','attempt','report'].map(name=>readPin(link[name])));
 need(Array.isArray(manifest.files)&&manifest.files.length>0,'Audit source inventory');
 need(publication.commit===link.sourceCommit&&publication.manifestSha256===link.manifest.sha256&&publication.manifestBytes===link.manifest.bytes&&publication.manifestPath===link.manifest.path&&publication.verifiedFilePins===manifest.files.length&&publication.remoteBytesEqualLocal===true&&publication.committedBytesEqualLocal===true,'Audit published source identity');
 need(attempt.schema==='m31-native-saved-audit-attempt-v1'&&attempt.stage==='saved-check'&&attempt.status==='completed'&&attempt.exitCode===0&&attempt.childExitCode===0&&attempt.childReaped===true&&attempt.preservationPassed===true&&attempt.sourceCommit===link.sourceCommit&&attempt.sourceManifestSha256===link.manifest.sha256&&attempt.outputBytes===link.report.bytes&&attempt.outputSha256===link.report.sha256,'Audit supervised completion');
 need(report.schema==='m31-native-load-check-v1'&&report.passed===true&&['qualified','unqualified'].includes(report.decision)&&report.sourceCommit===SOURCE&&report.sourceManifestSha256===MANIFEST&&report.browserOutputSha256===BROWSER_SHA,'Audit result native binding');
 const provenance=report.savedEvidenceAudit;need(provenance?.schema==='m31-native-saved-evidence-audit-provenance-v1'&&provenance.auditSourceCommit===link.sourceCommit&&provenance.auditSourceManifestSha256===link.manifest.sha256,'Saved audit source identity');
 const originals={originalSourceManifest:PACKAGE+'/source-manifest.json',originalChecker:PACKAGE+'/source/check.py',originalBrowserOutput:PACKAGE+'/results/browser.json',originalFailedAttempt:PACKAGE+'/results/browser-attempt.json',originalJournal:PACKAGE+'/results/browser-journal.jsonl'};
 for(const [key,path]of Object.entries(originals))need(pinEqual(provenance[key],knownPin(path)),'Audit original evidence binding');
 need(provenance.originalSourceCommit===SOURCE&&provenance.originalSupervisorStatus==='failed'&&provenance.originalSupervisorFailure?.type==='PermissionError'&&provenance.originalSupervisorRepaired===false&&provenance.originalCheckerMainUsedUnchanged===true&&provenance.fixtureAssertionsPassed===true&&provenance.corruptionAssertionsPassed===true&&provenance.launchCleanupComplianceClaim===false&&provenance.newBrowserCalls===0&&provenance.performanceClaim===false&&provenance.onlineCertificationClaim===false,'Audit scope and failure preservation');
 need(report.performanceClaim===false&&report.onlineCertificationClaim===false&&report.attemptedTargetCalls===12&&report.calls.length===12&&same(report.calls.map(row=>({caseId:row.caseId,method:row.method})),SCHEDULE),'Audit fixed denominator');
 need(report.normalization?.tolerance?.n==='1'&&report.normalization.tolerance.d==='100000000'&&report.normalization.comparison==='exact squared normalized error bounds','Strict audit threshold');
 need(report.browserControls?.passed===true&&report.browserControls.inheritedCount===48&&report.browserControls.wrapperCount===24&&report.browserProvenance?.passed===true&&report.browserProvenance.bundleAndSevenSlicesMatchPinnedStandaloneSources===true,'Audit controls and source gates');
 need(same(report.arithmeticFixtures?.map(row=>row.id),FIXTURES)&&report.arithmeticFixtures.every(row=>row.passed===true)&&same(report.corruptionChecks?.map(row=>row.id),CORRUPTIONS)&&report.corruptionChecks.every(row=>row.passed===true),'Audit independent validation gates');
 need(report.nativeParity?.length===6&&same(report.nativeParity.map(row=>row.caseId),PLAN.map(p=>p.id)),'Audit parity denominator');
 for(const row of report.calls){need(typeof row.qualified==='boolean'&&['qualified','unqualified'].includes(row.decision)&&(row.decision==='qualified')===row.qualified,'Saved audit decision');if(row.errors)for(const category of CATEGORIES)need(['pass','fail','unresolved'].includes(row.errors[category]?.decision)&&interval(row.errors[category].normalizedError)&&interval(row.errors[category].normalizedSquaredError),'Saved audit error enclosure');need(row.qualified===strictCall(row),'Audit call gate consistency');}
 need(report.nativeParity.every(row=>typeof row.matches==='boolean'&&Array.isArray(row.differentFields)&&row.matches===(row.differentFields.length===0)),'Audit parity gate consistency');
 const qualified=report.calls.filter(strictCall).length;need(report.qualifiedTargetCalls===qualified,'Audit qualified count');
 const all=qualified===12&&report.nativeParity.every(row=>row.matches===true);need((report.decision==='qualified')===all,'Audit overall gate consistency');
 audit=report;
}
function auditRow(id,m){return audit?.calls.find(row=>row.caseId===id&&row.method===m);}
function badge(cell,text,cls){cell.append(el('strong',text,cls));}
function renderOverview(){
 $('all-results').replaceChildren();
 for(const p of PLAN){const state=data?.states.find(s=>s.id===p.id),row=el('tr'),first=el('td'),button=el('button',(p.runId==='run-a'?'A':'B')+' · '+p.t+' s','state-link'+(p.id===stateId?' current':''));button.disabled=!state;button.type='button';button.addEventListener('click',()=>{stateId=p.id;$('state').value=p.id;renderSelection(true);});first.append(button);row.append(first);row.dataset.state=p.id;
  for(const m of ['F','L']){const native=el('td'),checked=el('td');badge(native,state?'Returned':'Not bound',state?'neutral':'muted');const ar=auditRow(p.id,m);badge(checked,ar?(ar.qualified?'Qualified':'Not qualified'):'Pending',ar?(ar.qualified?'pass':'bad'):'pending');row.append(native,checked);}
  const parity=el('td'),match=audit?.nativeParity.find(x=>x.caseId===p.id);badge(parity,match?(match.matches?'Same outputs':'Different outputs'):'Pending',match?(match.matches?'pass':'bad'):'pending');row.append(parity);$('all-results').append(row);
 }
 $('denominator').textContent=(data?'6 / 6':'0 / 6')+' recorded states bound · both methods remain visible · '+(audit?audit.qualifiedTargetCalls+' / 12 independently qualified calls.':'12 scheduled calls await an accepted independent audit.');
}
function renderAudit(){
 const row=auditRow(stateId,method);$('audit-results').replaceChildren();
 for(const category of CATEGORIES){const tr=el('tr'),error=row?.errors?.[category];tr.append(el('th',LABELS[category]));const status=el('td'),bounds=el('td');badge(status,error?({pass:'Pass',fail:'Fail',unresolved:'Unresolved'}[error.decision]):'Pending',error?(error.decision==='pass'?'pass':error.decision==='fail'?'bad':'pending'):'pending');bounds.textContent=error?'≈ ['+decimal(error.normalizedError.l)+', '+decimal(error.normalizedError.u)+']':'No accepted independent error bound';tr.append(status,bounds);$('audit-results').append(tr);}
 $('audit-caption').textContent=row?stateId+' · '+method+' · '+(row.qualified?'All saved identity, support, arithmetic, consumption and strict accuracy gates passed.':'This native call did not qualify; see the preserved gates below.'):'Pending. Native success does not establish exact-model compatibility.';
 $('exact-audit').textContent=row?JSON.stringify(row,null,2):auditFailure?'Audit unavailable or inconsistent: '+auditFailure:'No accepted independent audit.';
}
function renderSelection(resetCamera=false){
 renderOverview();renderAudit();if(!data)return;
 const state=data.states.find(s=>s.id===stateId),call=state.methods[method],index=state.ids.indexOf(droneId);need(index>=0,'Selected stable ID');const load=call.loads[index];
 $('load-results').replaceChildren();
 const fields=[...load.rotor.map((value,r)=>['Rotor '+r+' thrust (N)',[value]]),['Collective thrust (N)',[load.collective]],['World force [x, y, z] (N)',load.worldForce],['World moment [x, y, z] (N·m)',load.worldMoment]];
 for(const [label,values]of fields){const row=el('tr'),words=el('td');values.forEach(value=>words.append(el('code',value)));row.append(el('th',label),el('td',values.map(value=>fmt(number(value))).join(', ')),words);$('load-results').append(row);}
 $('selection-summary').textContent=stateId+' · method '+method+' · stable drone ID '+droneId+' · actual returned values.';
 $('exact-record').textContent=JSON.stringify({stateId,method,droneId,poseWords:state.poseWords[index],load,field:call.fieldPath+'.loads['+index+']'},null,2);
 $('output-identity').textContent='Native browser SHA-256 '+BROWSER_SHA+' · '+call.fieldPath+'.loads['+index+'] · all 64 delivered loads SHA-256 '+call.loadWordsSha256+' · input file '+call.inputFileSha256+' · semantic input '+call.semanticInputSha256+'.';
 const scale=Number($('scale').value),arrows=$('arrows').checked;
 if(scene){scene.style({scale,visible:arrows,selectedId:droneId});scene.setSnapshot({id:stateId,method,ids:state.ids,poses:state.poseWords.map(words=>({position:words.slice(0,3).map(number),quaternion:words.slice(3).map(number)})),worldForces:call.loads.map(item=>item.worldForce.map(number))},resetCamera);}
 $('frame-status').textContent='Recorded '+state.runId+' · '+state.t+' s · method '+method+' · 64 saved poses · '+(scene?(arrows?'returned world-force arrows shown.':'force arrows hidden.'):'3D unavailable; exact values remain below.');
 $('scale-caption').textContent='Drone glyphs enlarged 3×. Arrow endpoint = recorded center + returned force × '+scale+' scene m/N. This display scale does not change a load or audit threshold.';
 window.__viewState={...(lastScene||{}),validEvidence:true,stateId,method,droneId,independentAudit:audit?.decision??'pending',originalSupervisorStatus:'failed',nativeBrowserSha256:BROWSER_SHA};
 window.__evidenceState={bound:true,stateIds:PLAN.map(p=>p.id),methods:['F','L'],originalSupervisorStatus:'failed',nativeReturnedCalls:12,auditDecision:audit?.decision??'pending',auditFailure,selectedLoad:load,loadWordsSha256:call.loadWordsSha256,selectedAudit:auditRow(stateId,method)??null};
}
function renderStatus(){
 $('native-count').textContent='12 / 12 returned';$('supervisor-status').textContent='Failed · cleanup';$('supervisor-detail').textContent='Child exit 0; supervisor exit 1. EPERM prevented successful outer cleanup.';$('original-failure').hidden=false;
 if(audit){const pass=audit.decision==='qualified';$('audit-status').textContent=pass?'Retained audit passed':'Did not qualify';$('audit-status').className=pass?'pass':'bad';$('audit-detail').textContent=audit.qualifiedTargetCalls+' / 12 calls qualified at 1e-8. The original supervisor failure is unchanged.';$('notice').textContent=pass?'Saved-record accuracy audit passed for all twelve retained calls. Original launch supervision remains failed; this is a separate, bounded evidence result.':'The independent saved-record audit did not qualify every required call. All saved outcomes and the original supervisor failure remain visible.';}
 else{$('audit-status').textContent=auditFailure?'Unavailable':'Pending';$('audit-status').className='pending';$('audit-detail').textContent=auditFailure?'The independent audit record failed its binding or gate checks.':'No independently verified audit result has been accepted by this page.';$('notice').textContent='Qualification pending. Chrome returned all twelve native outputs; the original supervisor failed during cleanup. '+(auditFailure?'The later audit is unavailable or inconsistent.':'A separate saved-record audit is still required.');}
}
function reject(error){data=null;audit=null;lastScene=null;scene?.clear();for(const id of ['state','method','drone','scale','reset','arrows'])$(id).disabled=true;$('scene-empty').hidden=false;$('scene-empty').textContent='No accepted recorded scene.';$('notice').classList.add('error');$('notice').textContent='Saved evidence unavailable or inconsistent. No load visualization or qualification result is accepted.';$('native-count').textContent='Not bound';$('audit-status').textContent='Pending';$('audit-status').className='pending';$('audit-detail').textContent='No independent qualification is accepted.';$('supervisor-status').textContent='Failed · cleanup';$('supervisor-detail').textContent='The original supervisor failed with EPERM. This display binding is unavailable.';$('original-failure').hidden=false;$('pins').replaceChildren();$('load-results').replaceChildren();$('selection-summary').textContent='No accepted selection.';$('exact-record').textContent='No accepted record.';$('output-identity').textContent='';$('identity').textContent='No accepted display binding.';$('frame-status').textContent='No accepted recorded scene.';renderOverview();renderAudit();window.__viewState={validEvidence:false,originalSupervisorStatus:'failed',error:String(error.message)};window.__evidenceState={bound:false,originalSupervisorStatus:'failed',auditDecision:'pending'};}
async function main(){
 for(const p of PLAN){const option=el('option',(p.runId==='run-a'?'Run A':'Run B')+' · '+p.t+' s');option.value=p.id;$('state').append(option);}renderOverview();renderAudit();
 need(hash(BINDING_SHA),'Unbuilt source draft');const response=await fetch('binding.json',{cache:'no-store'});need(response.ok,'Display binding unavailable');const raw=await response.arrayBuffer();need(raw.byteLength<256*1024&&await sha(raw)===BINDING_SHA,'Display binding digest');binding=JSON.parse(new TextDecoder().decode(raw));
 need(binding.schema==='m31-native-load-view-binding-v1'&&binding.package===PACKAGE&&binding.sourceCommit===SOURCE&&binding.sourceManifestSha256===MANIFEST&&same(binding.schedule,PLAN)&&binding.display.path==='display-data.json','Display binding identity');
 need(Array.isArray(binding.pins)&&new Set(binding.pins.map(pin=>pin.path)).size===binding.pins.length&&binding.pins.every(pin=>hash(pin.sha256)&&Number.isSafeInteger(pin.bytes)&&pin.bytes>0&&!pin.path.includes('..')),'Evidence inventory');
 need(knownPin(PACKAGE+'/results/browser.json')?.sha256===BROWSER_SHA&&knownPin(PACKAGE+'/results/browser-attempt.json')?.sha256===ATTEMPT_SHA,'Original output and failure pins');
 const dr=await fetch(binding.display.path,{cache:'no-store'});need(dr.ok,'Display projection unavailable');const bytes=await dr.arrayBuffer();need(bytes.byteLength===binding.display.bytes&&bytes.byteLength<4*1024*1024&&await sha(bytes)===binding.display.sha256,'Projection digest');data=JSON.parse(new TextDecoder().decode(bytes));await validateData(data);
 try{await loadAudit();}catch(error){audit=null;auditFailure=String(error.message);}
 renderStatus();for(const id of data.states[0].ids){const option=el('option',String(id));option.value=String(id);$('drone').append(option);}droneId=data.states[0].ids[0];
 $('identity').textContent='Native source '+SOURCE+' · manifest '+MANIFEST+' · recorded output '+BROWSER_SHA+'. The compact display contains actual saved pose and load words.';
 for(const pin of binding.pins){const item=el('li'),link=el('a',pin.path);link.href='../../../'+pin.path;item.append(link,document.createTextNode(' · '+pin.bytes+' bytes · SHA-256 '+pin.sha256));$('pins').append(item);}
 try{const mod=await import('./scene.js');scene=mod.createRecordedScene($('scene'),state=>{lastScene=state;if(window.__viewState?.validEvidence)Object.assign(window.__viewState,state);});$('scene-empty').hidden=true;}catch(error){$('scene-empty').textContent='3D could not initialize. Recorded load words and evidence remain available below.';window.__sceneError=String(error.message);}
 for(const id of ['state','method','drone'])$(id).disabled=false;for(const id of ['scale','arrows','reset'])$(id).disabled=!scene;
 for(const id of ['state','method','drone','scale','arrows'])$(id).addEventListener('change',()=>{try{stateId=$('state').value;method=$('method').value;droneId=Number($('drone').value);renderSelection(id==='state');}catch(error){reject(error);}});
 $('reset').addEventListener('click',()=>scene?.reset());renderSelection(true);
}
main().catch(reject);
