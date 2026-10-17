// Saved-data display only. Never imports a scientific module or recomputes a candidate.
const BINDING_SHA='286d6b3d49acf01cdd594f6a42f46961ad0dd4258682b1e23e7c2ee045d2f970';
const PACKAGE='research/m31-direct-load-diagnostic-2026-10-17';
const PRIOR='research/m31-normalizer-replication-2026-10-17';
const SOURCE='ee342fe5cdd824cbd68e4c1c85bae9f83bf688bf';
const MANIFEST='93d26849dcd0a86d18b254f8eb5babc3d13e0f46d08efc92dfc2bc5cef79635b';
const TIERS=['1e-8','1e-4','1e-2'];
const CATEGORIES=['rotor','collective','worldForce','worldMoment'];
const LABELS={rotor:'Rotor thrust / (mg/4)',collective:'Collective thrust / mg',worldForce:'World force norm / mg',worldMoment:'World moment norm / (mg R)'};
const PLAN=['run-a','run-b'].flatMap(runId=>[0,5,10].map(t=>({id:runId+'-t'+t,runId,t})));
const $=id=>document.getElementById(id),same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const sha=async b=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b)),v=>v.toString(16).padStart(2,'0')).join('');
const fmt=n=>n.toLocaleString('en-US'),count=n=>Number.isSafeInteger(n)&&n>=0,word=w=>typeof w==='string'&&/^[0-9a-f]{16}$/.test(w);
function need(ok,message){if(!ok)throw Error(message);}
function el(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
const dv=new DataView(new ArrayBuffer(8));
function number(w){need(word(w),'Invalid coordinate word');dv.setUint32(0,parseInt(w.slice(0,8),16),false);dv.setUint32(4,parseInt(w.slice(8),16),false);const v=dv.getFloat64(0,false);need(Number.isFinite(v),'Nonfinite saved coordinate');return v;}
function rational(q){return q&&typeof q.n==='string'&&typeof q.d==='string'&&/^(0|[1-9][0-9]*)$/.test(q.n)&&/^[1-9][0-9]*$/.test(q.d);}
// Decimal formatting only; exact saved status strings make every threshold decision.
function decimal(q){if(q.n==='0')return '0';const n=q.n,d=q.d;const a=Number(n.slice(0,16)),b=Number(d.slice(0,16));return ((a/b)*10**((n.length-Math.min(16,n.length))-(d.length-Math.min(16,d.length)))).toExponential(3);}
function errorText(audit,box){return audit==='A'?'≈ ['+decimal(box.l)+', '+decimal(box.u)+']':'Upper ≈ '+decimal(box.u);}
function savedTier(audit){return audit.tiers.find(t=>t.tier===tier);}
const statusLabel=(s,audit)=>s==='pass'?(audit==='A'?'Pass':'Certified'):s==='definite-fail'?'Definite fail':s==='not-certified'?'Not certified':'Unresolved';
const statusClass=s=>s==='pass'?'pass':s==='definite-fail'?'bad':'pending';
let binding=null,data=null,replay=null,lastSceneState=null,stateId=PLAN[0].id,proposal='omit10',tier=TIERS[0],category='rotor';
function validate(model){
 need(model.schema==='m31-direct-load-display-v1'&&model.package===PACKAGE&&model.checkerPassed===true&&same(model.tiers,TIERS),'Wrong display schema');
 need(model.sourceCommit===SOURCE&&model.sourceManifestSha256===MANIFEST,'Display source identity mismatch');
 need(Array.isArray(model.states)&&same(model.states.map(s=>({id:s.id,runId:s.runId,t:s.t})),PLAN),'Six-state schedule mismatch');
 need(typeof model.fullControlStrictPass==='boolean'&&typeof model.allSixStrictHeadroom==='boolean'&&typeof model.decision==='string','Saved decision missing');
 for(const s of model.states){
  need(/^[0-9a-f]{64}$/.test(s.inputSha256)&&binding.pins.find(p=>p.path===PRIOR+'/results/inputs/'+s.id+'.json')?.sha256===s.inputFileSha256&&binding.pins.find(p=>p.path===PRIOR+'/results/reference/'+s.id+'.json')?.sha256===s.referenceFileSha256,'Input/reference identity differs');
  need(Array.isArray(s.ids)&&s.ids.length===64&&new Set(s.ids).size===64&&s.ids.every(n=>Number.isInteger(n)&&n>=0&&n<=65535),'Invalid saved stable IDs');
  need(Array.isArray(s.poseWords)&&s.poseWords.length===448&&s.poseWords.every(word),'Invalid saved pose words');s.poseWords.forEach(number);
  need(Array.isArray(s.geometry)&&same(s.geometry.map(g=>g.id),s.ids),'Geometry stable-ID order mismatch');
  for(const [i,g]of s.geometry.entries()){need(same(g.center,s.poseWords.slice(7*i,7*i+3))&&g.points.length===4&&g.points.every(p=>p.length===3&&p.every(word)),'Prepared endpoints differ');g.points.flat().forEach(number);}
  const ids=new Set(s.ids);need(count(s.positiveTerms)&&s.positiveTerms<=16128&&Array.isArray(s.omittedLinks)&&s.omittedLinks.length===Math.ceil(s.positiveTerms/10),'Invalid saved positive/mask count');
  need(new Set(s.omittedLinks.map(a=>a.join(':'))).size===s.omittedLinks.length&&s.omittedLinks.every(a=>a.length===3&&ids.has(a[0])&&ids.has(a[2])&&a[0]!==a[2]&&Number.isInteger(a[1])&&a[1]>=0&&a[1]<4),'Invalid omitted stable-ID link');
  need(same(Object.keys(s.proposals),['full','omit10']),'Candidate schedule mismatch');
  for(const name of ['full','omit10']){
   const p=s.proposals[name];need(p.omittedCount===(name==='full'?0:s.omittedLinks.length)&&same(Object.keys(p.audits),name==='full'?['A','B']:['A','B','C']),'Candidate count/audits mismatch');
   for(const [audit,a]of Object.entries(p.audits)){
    const allowed=audit==='A'?['pass','definite-fail','unresolved']:['pass','not-certified'];
    need(same(Object.keys(a.maxErrors),CATEGORIES)&&same(a.tiers.map(t=>t.tier),TIERS),'Audit categories/tiers differ');
    for(const box of Object.values(a.maxErrors))need(rational(box.l)&&rational(box.u)&&BigInt(box.l.n)*BigInt(box.u.d)<=BigInt(box.u.n)*BigInt(box.l.d),'Malformed error interval');
    for(const t of a.tiers)need(allowed.includes(t.overall)&&same(Object.keys(t.categories),CATEGORIES)&&Object.values(t.categories).every(v=>allowed.includes(v)),'Wrong A or B/C saved status');
   }
  }
 }
}
function appendAuditCell(row,auditName,audit,metric,overall=true){
 const cell=el('td');if(!audit){cell.append(el('span','Not applicable','muted'),el('small','Full control has no omission audit.'));row.append(cell);return;}
 const t=savedTier(audit),status=overall?t.overall:t.categories[metric],box=audit.maxErrors[metric];
 cell.append(el('strong',statusLabel(status,auditName),statusClass(status)),el('small',errorText(auditName,box)));cell.dataset.status=status;cell.dataset.audit=auditName;cell.dataset.category=metric;cell.title='Exact saved error interval: ['+box.l.n+'/'+box.l.d+', '+box.u.n+'/'+box.u.d+']';row.append(cell);
}
function renderTable(){
 const body=$('all-results');body.replaceChildren();
 for(const p of PLAN){
  const s=data?.states.find(v=>v.id===p.id),row=el('tr'),first=el('td'),button=el('button',(p.runId==='run-a'?'A':'B')+' · '+p.t+' s','state-link'+(stateId===p.id?' current':''));button.type='button';button.disabled=!s;button.addEventListener('click',()=>{try{stateId=p.id;$('state').value=p.id;renderSelection(true);}catch(e){reject(e);}});first.append(button);row.append(first);row.dataset.state=p.id;
  if(!s){for(let i=0;i<6;i++)row.append(el('td','Not bound'));body.append(row);continue;}
  row.append(el('td',s.omittedLinks.length+' / '+s.positiveTerms));appendAuditCell(row,'A',s.proposals.full.audits.A,category);appendAuditCell(row,'B',s.proposals.full.audits.B,category);
  for(const a of ['A','B','C'])appendAuditCell(row,a,s.proposals.omit10.audits[a],category);body.append(row);
 }
 $('denominator').textContent=(data?'6':'0')+' / 6 states bound. Every scheduled state remains visible, including failures and uncertified outcomes.';
 if(data){const counts=['A','B','C'].map(a=>data.states.filter(s=>savedTier(s.proposals.omit10.audits[a]).overall==='pass').length);$('tier-summary').textContent=tier+' · omission A: '+counts[0]+'/6 pass · B: '+counts[1]+'/6 certified · C: '+counts[2]+'/6 certified. '+(tier==='1e-8'?'Strict contract.':tier==='1e-2'?'Stress only; no physical 1% claim.':'Looser diagnostic only.');}
}
function renderDetail(s){
 const body=$('detail-results');body.replaceChildren();
 const audits=s?.proposals[proposal].audits;
 for(const metric of CATEGORIES){const row=el('tr');const heading=el('th',LABELS[metric]);heading.scope='row';row.append(heading);row.dataset.category=metric;for(const a of ['A','B','C']){if(s)appendAuditCell(row,a,audits[a],metric,false);else row.append(el('td','Not bound'));}body.append(row);}
 $('detail-caption').textContent=s?s.id+' · '+(proposal==='full'?'Full control':'Delete weakest 10%')+' · '+tier+' · same saved candidate across A/B/C.':'No accepted candidate.';
 $('exact-errors').textContent=s?JSON.stringify(audits,null,2):'No evidence bound.';
}
function renderSelection(reloadPose=false){
 renderTable();const s=data?.states.find(v=>v.id===stateId);renderDetail(s);if(!s)return;
 const links=proposal==='omit10'?s.omittedLinks:[],geometry=new Map(s.geometry.map(g=>[g.id,g]));
 const segments=links.map(([i,r,j])=>[...geometry.get(j).center,...geometry.get(i).points[r]].map(number));
 if(replay){if(reloadPose)replay.setFrames(s.runId,[{t:s.t,words:s.poseWords}]);replay.setOverlays($('overlays').checked?segments:[]);}
 const visible=replay&&$('overlays').checked;
 $('frame-status').textContent='Saved '+s.runId+' · '+s.t+' s · 64 recorded poses · '+(visible?(links.length?links.length+' omitted links shown.':'Full control: no coefficients deleted.'):(replay?'Omitted links hidden; all saved outcomes remain visible.':'3D unavailable; saved evidence remains below.'));
 $('selection-summary').textContent=(proposal==='full'?'Full control deletes 0':('Fixed omission deletes '+links.length))+' of '+s.positiveTerms+' positive terms. Tolerance selection changes only the displayed decisions; it never changes a candidate or mask.';
 window.__viewState={...(lastSceneState||{}),validEvidence:true,stateId:s.id,tier,proposal,category,renderedBodyCount:replay?64:0,selectedLinkCount:links.length,renderedLinkCount:replay?replay.overlayCount():0,overlayCount:replay?replay.overlayCount():0,overlaysEnabled:$('overlays').checked,ids:s.ids,edgeSamples:links.map((e,i)=>({receiver:e[0],rotor:e[1],source:e[2],endpoints:segments[i]})),sourceCommit:SOURCE};
 window.__evidenceState={bound:true,denominator:6,tier,proposal,category,checkerPassed:true,stateIds:PLAN.map(p=>p.id),rows:data.states.map(v=>({id:v.id,positiveTerms:v.positiveTerms,omittedCount:v.omittedLinks.length,full:v.proposals.full.audits,omit10:v.proposals.omit10.audits})),selectedAudits:s.proposals[proposal].audits};
}
function reject(error){
 binding=null;data=null;replay?.setOverlays([]);$('scene').querySelectorAll('canvas').forEach(c=>c.hidden=true);
 for(const id of ['state','tier','proposal','category','reset','overlays'])$(id).disabled=true;
 $('notice').classList.add('error');$('notice').textContent='Evidence unavailable or inconsistent. No saved pose, mask or numerical claim is accepted.';$('scene-empty').hidden=false;$('scene-empty').textContent='No accepted evidence is displayed.';$('check-status').textContent='Not bound';$('full-count').textContent='— / 6';$('omit-count').textContent='— / 6';$('strict-detail').textContent='No accepted accuracy result.';$('frame-status').textContent='Evidence validation failed.';$('selection-summary').textContent='No accepted selection.';$('tier-summary').textContent='No accepted tier summary.';$('identity').textContent='No accepted source identity.';$('pose-provenance').textContent='No accepted pose provenance.';$('pins').replaceChildren();renderTable();renderDetail(null);window.__viewState={validEvidence:false,error:String(error.message)};window.__evidenceState={bound:false,denominator:6,stateIds:PLAN.map(p=>p.id)};
}
async function main(){
 for(const p of PLAN){const option=el('option',(p.runId==='run-a'?'Run A':'Run B')+' · '+p.t+' s');option.value=p.id;$('state').append(option);}renderTable();renderDetail(null);
 need(/^[0-9a-f]{64}$/.test(BINDING_SHA),'Source draft has no accepted binding');
 const response=await fetch('binding.json',{cache:'no-store'});need(response.ok,'Binding unavailable');const bytes=await response.arrayBuffer();need(bytes.byteLength<=128*1024&&await sha(bytes)===BINDING_SHA,'Binding digest differs');binding=JSON.parse(new TextDecoder().decode(bytes));
 need(binding.schema==='m31-direct-load-view-binding-v1'&&binding.package===PACKAGE&&binding.sourceCommit===SOURCE&&binding.sourceManifestSha256===MANIFEST&&same(binding.schedule,PLAN)&&binding.display.path==='display-data.json'&&binding.immutableSourcePinCount===159&&binding.resultFileCount===4,'Wrong accepted allocation binding');
 need(Array.isArray(binding.pins)&&binding.pins.length>0&&new Set(binding.pins.map(p=>p.path)).size===binding.pins.length,'Missing or duplicate evidence pins');
 for(const p of binding.pins)need((p.path.startsWith(PACKAGE+'/')||p.path.startsWith(PRIOR+'/'))&&!p.path.includes('..')&&count(p.bytes)&&/^[0-9a-f]{64}$/.test(p.sha256),'Invalid evidence pin');
 const response2=await fetch(binding.display.path,{cache:'no-store'});need(response2.ok,'Display data unavailable');const db=await response2.arrayBuffer();need(db.byteLength<=16*1024*1024&&db.byteLength===binding.display.bytes&&await sha(db)===binding.display.sha256,'Display digest differs');data=JSON.parse(new TextDecoder().decode(db));validate(data);
 $('notice').textContent='Saved-data integrity check passed. The omission candidate fails the strict numerical accuracy threshold in all six states.';$('check-status').textContent='Passed';$('check-status').className='pass';
 const strict=a=>a.tiers.find(t=>t.tier==='1e-8').overall==='pass';const full=data.states.filter(s=>strict(s.proposals.full.audits.A)).length,omit=data.states.filter(s=>strict(s.proposals.omit10.audits.A)).length;
 $('full-count').textContent=full+' / 6 pass';$('full-count').className=full===6?'pass':'bad';$('omit-count').textContent=omit+' / 6 pass';$('omit-count').className=omit===6?'pass':'bad';$('strict-detail').textContent='All six states have a definite A failure at 1e-8. Stress-tier successes do not replace this result.';
 $('identity').textContent='Source '+SOURCE+' · manifest '+MANIFEST+' · 159 frozen source/input pins · four accepted result files · display '+binding.display.sha256+'.';
 $('pose-provenance').textContent='Poses: prior normalizer replication, airflow off, recorded at 0 / 5 / 10 s. Input pose words match the saved generation frames. Omitted links use the exact saved stable-ID mask and prepared source-center/receiver-rotor words.';
 for(const p of binding.pins){const item=el('li'),a=el('a',p.path);a.href='../../../'+p.path;item.append(a,document.createTextNode(' · '+p.bytes+' bytes · SHA-256 '+p.sha256));$('pins').append(item);}
 try{const module=await import('./scene.js');replay=module.createReplay($('scene'),s=>{lastSceneState=s;});$('scene-empty').hidden=true;}catch(error){$('scene-empty').textContent='3D could not initialize. The saved six-state evidence remains available below.';window.__replayError=String(error.message);}
 for(const id of ['state','tier','proposal','category'])$(id).disabled=false;$('reset').disabled=!replay;$('overlays').disabled=!replay;
 for(const id of ['state','tier','proposal','category'])$(id).addEventListener('change',()=>{try{stateId=$('state').value;tier=$('tier').value;proposal=$('proposal').value;category=$('category').value;renderSelection(id==='state');}catch(e){reject(e);}});
 $('overlays').addEventListener('change',()=>{try{renderSelection();}catch(e){reject(e);}});$('reset').addEventListener('click',()=>replay?.reset());renderSelection(true);
}
main().catch(reject);
