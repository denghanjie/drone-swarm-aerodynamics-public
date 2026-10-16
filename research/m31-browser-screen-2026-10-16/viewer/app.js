let stopReplay=()=>{};
const $=id=>document.getElementById(id),fmt=n=>n.toLocaleString('en-US'),ms=n=>n.toFixed(2);
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
async function bound(pin){
 const r=await fetch('../'+pin.path,{cache:'no-store'});if(!r.ok)throw Error('Missing saved record');
 const b=await r.arrayBuffer(),h=[...new Uint8Array(await crypto.subtle.digest('SHA-256',b))].map(x=>x.toString(16).padStart(2,'0')).join('');
 if(h!==pin.sha256||b.byteLength!==pin.bytes)throw Error('Evidence pin mismatch');return b;
}
async function jsonPin(pin){return JSON.parse(new TextDecoder().decode(await bound(pin)));}
async function main(){
 const binding=await(await fetch('./binding.json',{cache:'no-store'})).json();
 const records=Object.fromEntries(await Promise.all(Object.entries(binding.records).map(async([k,p])=>[k,await jsonPin(p)])));
 const {display:data,analysis={},review={},qualification={},sourcePublication}=records;
 if(!data||!sourcePublication)throw Error('Missing source or display record');
 const closed=['generationRun','run','reviewRun'].every(k=>records[k]?.supervisorSuccess===true&&records[k]?.closed===true&&records[k]?.childGroupAbsent===true);
 const slots=['p0','p1','p2'].every(s=>records[s+'Closure']?.complete===true&&records[s+'Closure']?.closureConfirmed===true);
 const verified=closed&&slots&&review.pass===true&&review.complete===true&&analysis.independentAuditPass===true&&qualification.sealSuccess===true&&qualification.evidenceQualified===true;
 if(qualification.evidenceQualified===true&&!verified)throw Error('Qualified seal lacks complete closure and audit');
 for(const k of ['generationRun','run','reviewRun','qualification'])if(records[k]&&records[k].sourceCommit!==sourcePublication.commit)throw Error('Source identity mismatch');
 if(data.sourceCommit!==sourcePublication.commit||data.verified!==verified||data.practicalPass!==(verified&&qualification.practicalRulePass===true))throw Error('Display result mismatch');
 const calls=['p0','p1','p2'].reduce((n,s)=>n+(records[s+'Evidence']?.timings?.length??0),0);
 if(data.timingCalls!==calls)throw Error('Displayed call count mismatch');
 if(verified&&(!eq(analysis.processes?.map(x=>x.processId),['p0','p1','p2'])||calls!==126))throw Error('Incomplete qualified campaign');
 const samePin=(a,b)=>a&&b&&a.bytes===b.bytes&&a.sha256===b.sha256;
 let inventory=new Map();
 function inInventory(pin){if(verified&&!samePin(pin,inventory.get(pin.path)))throw Error('Display record is outside sealed inventory');}
 if(verified){
  for(const k of ['generationRun','run','reviewRun','review','analysis','sourcePublication','sourceManifest','p0Closure','p1Closure','p2Closure']){
   const pin=binding.records[k];if(!pin||!samePin(pin,qualification.inputs?.[pin.path]))throw Error('Display evidence differs from seal input');
  }
  const entries=records.reviewRun.artifacts;
  if(!Array.isArray(entries)||new Set(entries.map(x=>x.path)).size!==entries.length)throw Error('Invalid sealed inventory');
  inventory=new Map(entries.map(x=>[x.path,x]));
  for(const s of ['p0','p1','p2'])inInventory(binding.records[s+'Evidence']);
  const configPath='research/m31-browser-screen-2026-10-16/config.json';
  if(!samePin(binding.records.configuration,records.sourceManifest.files.find(x=>x.path===configPath)))throw Error('Configuration differs from frozen source');
 }
 const ids=data.cases.map(x=>x.id),expectedIds=records.configuration.cases.map(x=>x.id);
 if(new Set(ids).size!==ids.length||(verified&&!eq(ids,expectedIds)))throw Error('Missing or duplicate displayed case');
 $('content').hidden=false;$('headline').replaceChildren(...data.headline.split('\n').flatMap((t,i)=>i?[document.createElement('br'),document.createTextNode(t)]:[document.createTextNode(t)]));
 $('lead').textContent=data.lead;$('finding').textContent=data.finding;$('timings').textContent=calls+' / 126';$('checks').textContent=fmt(review.checkCount??0)+' checked · '+(verified?'passed':'incomplete / failed');$('rule').textContent=verified?(data.practicalPass?'Passed':'Not met'):'Unresolved';
 for(const c of data.cases){
  const configCase=records.configuration?.cases.find(x=>x.id===c.id);
  if(!configCase||configCase.n!==c.n||configCase.seed!==c.seed)throw Error('Display input identity mismatch');
  if(c.y&&!verified)throw Error('Unqualified displayed loads');
  if(verified&&(c.loadProcess!=='p0'||c.loadPin?.path!==`runs/p0/results/${c.id}-L.json`||!Array.isArray(c.y)||c.y.length!==c.n))throw Error('Qualified load requires exact case source');
  if(!verified&&c.processes.length)throw Error('Unqualified displayed timing');
  if(verified&&!eq(c.processes.map(x=>x.processId),['p0','p1','p2']))throw Error('Missing or duplicate process display');
  inInventory(c.generationPin);inInventory(c.poses);if(c.loadPin)inInventory(c.loadPin);
  for(const t of c.processes){const a=analysis.processes.find(x=>x.processId===t.processId)?.cases.find(x=>x.id===c.id);if(!a||!eq(t.methods,Object.fromEntries(Object.entries(a.methods).map(([m,v])=>[m,v.totalMs])))||!eq(t.pairs,a.pairs)||t.performanceRulePass!==a.performanceRulePass)throw Error('Displayed timing or pairing mismatch');}
  const o=document.createElement('option');o.value=c.id;o.textContent=fmt(c.n)+' drones · seed '+c.seed;$('case').append(o);
 }
 if(!data.cases.length)throw Error('No complete pose record in this attempt');
 const {createScene}=await import('./scene.js'),scene=createScene($('scene')),cache=new Map();let request=0,selected=null,timer=null;
 function pause(){if(timer!==null)clearInterval(timer);timer=null;$('play').textContent='Play recorded flight';document.body.dataset.playing='false';}stopReplay=pause;
 function showFrame(ix){$('frame').value=String(ix);scene.frame(ix);const t=cache.get(selected.id)[ix*(1+7*selected.n)];$('time').textContent=t.toFixed(1)+' s';$('scene-state').textContent=fmt(selected.n)+' recorded poses · '+t.toFixed(1)+' s · airflow off';$('colors').textContent=ix===selected.frames-1&&selected.y?'Final pose only: blue → amber indicates lower modeled total load relative to nominal. Loads from process p0 match the qualified outputs of all three processes. These are predictions, not measured thrust loss.':'Recorded poses use uniform blue. No airflow loads were integrated into these playback frames.';}
 function costs(){
  const c=selected,t=c.processes.find(x=>x.processId===$('process').value);$('bars').replaceChildren();$('process-table').replaceChildren();
  for(const s of ['p0','p1','p2']){const a=c.processes.find(x=>x.processId===s),tr=document.createElement('tr');tr.dataset.selected=String(s===$('process').value);for(const text of [s,a?a.pairs['F/L'].medianPairedRatio.toFixed(4):'Unavailable',a?a.pairs['F/L'].strictWins+'/6':'—',a?(a.performanceRulePass?'Met':'Missed'):'Unqualified']){const td=document.createElement('td');td.textContent=text;tr.append(td);}$('process-table').append(tr);}
  if(!t){$('comparison').textContent='No qualified timing conclusion is available for this case and process.';$('decision').textContent='An incomplete attempt cannot establish a speedup or a slowdown.';return;}
  const names={L:'L · Unchanged lean all-pairs',F:'F · Current-position far screen'},max=Math.max(...Object.values(t.methods).map(x=>x.max));
  for(const m of 'LF'){const v=t.methods[m],row=document.createElement('div');row.className='bar-row';const label=document.createElement('span');label.textContent=names[m];const track=document.createElement('div');track.className='bar-track';const bar=document.createElement('div');bar.className='bar bar-'+m;bar.style.width=(100*v.median/max)+'%';track.append(bar);const value=document.createElement('span');value.className='bar-value';value.textContent=ms(v.median)+' ms ['+ms(v.min)+'–'+ms(v.max)+']';row.append(label,track,value);$('bars').append(row);}
  const v=t.pairs['F/L'];$('comparison').textContent=t.processId+' · Paired median F/L: '+v.medianPairedRatio.toFixed(4)+' · '+v.strictWins+'/6 strict F wins. Bars show median [min–max] from six calls; ranges describe observed variability, not confidence intervals.';
  $('decision').textContent=c.n===5000?(t.performanceRulePass?'This case × process cell met the fixed rule. All six primary cells must pass.':'This case × process cell missed the fixed rule. No pooled result can rescue it.'):'This 1,000-drone case is contextual. The primary decision uses all six 5,000-drone cells.';
 }
 async function select(){
  pause();const token=++request,c=data.cases.find(x=>x.id===$('case').value);$('status').textContent='Checking saved flight and load bytes…';
  const g=await jsonPin(c.generationPin);if(g.id!==c.id||g.n!==c.n||!eq(g.poses,c.poses)||c.frames!==g.poses.frames)throw Error('Displayed pose metadata mismatch');
  if(!cache.has(c.id))cache.set(c.id,new Float64Array(await bound(c.poses)));
  if(c.loadPin){const q=await jsonPin(c.loadPin);if(q.id!==c.id||q.n!==c.n||q.label!=='L'||!eq(q.solutions.O.y,c.y))throw Error('Displayed load mismatch');}
  if(token!==request)return;selected=c;const poses=cache.get(c.id);if(poses.length!==c.frames*(1+7*c.n))throw Error('Recorded pose shape mismatch');
  scene.load(c,poses);$('frame').max=String(c.frames-1);showFrame(c.frames-1);$('case-title').textContent=fmt(c.n)+' drones · seed '+c.seed;$('case-detail').textContent=c.description;costs();
  $('status').textContent='Saved records and selected pose/load bytes verified by SHA-256. '+(verified?'Independent numerical audit passed.':'Scientific audit incomplete or failed; see the retained records.');document.body.dataset.binding='verified';
 }
 $('case').value=data.cases.find(c=>c.n===5000)?.id??data.cases[0].id;
 $('case').addEventListener('change',()=>select().catch(fail));$('process').addEventListener('change',costs);
 $('frame').addEventListener('input',()=>{pause();showFrame(Number($('frame').value));});
 $('play').addEventListener('click',()=>{if(timer!==null){pause();return;}if(Number($('frame').value)>=selected.frames-1)showFrame(0);$('play').textContent='Pause replay';document.body.dataset.playing='true';timer=setInterval(()=>{const ix=Number($('frame').value)+1;showFrame(ix);if(ix>=selected.frames-1)pause();},400);});
 $('size').addEventListener('change',()=>scene.size(Number($('size').value)));$('reset').addEventListener('click',scene.reset);document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
 $('pins').textContent=Object.values(binding.records).map(p=>p.path+': '+p.sha256).join(' · ');await select();
}
function fail(e){stopReplay();$('content').hidden=true;$('headline').textContent='Evidence display stopped.';$('lead').textContent='A saved-record consistency check failed. No scientific claim is shown by this page.';document.body.dataset.binding='failed';$('status').className='error';$('status').textContent='Display stopped: '+e.message;}main().catch(fail);
