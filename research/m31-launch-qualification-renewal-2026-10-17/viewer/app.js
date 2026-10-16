// Saved-evidence presentation only. No harness or scientific imports.
const BINDING_SHA='ac2981fe48928a60ba755d75074e24e7001ed53c07ee4c8f203eceb47cda6b2c';
const PREFIX='research/m31-launch-qualification-renewal-2026-10-17/';
const CASES=['capability','normal','child-exit7','sampler-nonzero','sampler-malformed','delayed-ready','child-timeout','early-guardian-exit'];
const FIRST=[null,null,'child-exit','sampler-nonzero','sampler-malformed',null,'child-timeout','guardian-exit-before-release'];
const $=id=>document.getElementById(id);
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const requireEvidence=(ok)=>{if(!ok)throw Error('Saved evidence is inconsistent');};
const sha=async b=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b)),x=>x.toString(16).padStart(2,'0')).join('');
async function checked(url,pin){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error('Evidence file unavailable');const bytes=await r.arrayBuffer();requireEvidence(await sha(bytes)===pin.sha256&&(pin.bytes===undefined||bytes.byteLength===pin.bytes));return new TextDecoder().decode(bytes);}
try{
 const binding=JSON.parse(await checked('binding.json',{sha256:BINDING_SHA}));
 requireEvidence(binding.schema==='m31-renewal-result-view-v1'&&binding.pins.length===7);
 const evidence={};for(const pin of binding.pins)evidence[pin.path]=await checked('../../../'+pin.path,pin);
 const result=JSON.parse(evidence[PREFIX+'results/check.json']),publication=JSON.parse(evidence[PREFIX+'source-publication.json']),config=JSON.parse(evidence[PREFIX+'source/config.json']);
 requireEvidence(result.passed===true&&same(result.errors,[])&&same(result.cases.map(c=>c.case),CASES)&&result.cases.every(c=>c.passed===true)&&same(config.cases,CASES));
 requireEvidence(result.scientificQualification===false&&result.historicalRootCauseEstablished===false&&result.scientificRerunAuthorized===false);
 requireEvidence(publication.commit===result.sourceCommit&&publication.manifestSha256===result.sourceManifestSha256&&publication.verifiedFilePins===16&&publication.remoteBytesEqualLocal===true&&publication.committedBytesEqualLocal===true&&result.executionContext==='tool-require-escalated');
 requireEvidence(result.savedEvidencePins.length===39&&new Set(result.savedEvidencePins.map(p=>p.path)).size===39);
 for(const pin of result.savedEvidencePins){requireEvidence(pin.path.startsWith(PREFIX+'results/')&&!pin.path.includes('..'));evidence[pin.path]=await checked('../../../'+pin.path,pin);}
 const index=JSON.parse(evidence[PREFIX+'results/index.json']),attempt=JSON.parse(evidence[PREFIX+'results/attempt.json']);
 requireEvidence(index.fatalFailure===null&&same(index.cases,CASES)&&attempt.soleAttempt===true&&Date.parse(publication.verifiedUtc)<=Date.parse(attempt.startedUtc)&&Date.parse(attempt.startedUtc)<Date.parse(config.cutoffUtc));
 for(const saved of [index,attempt])for(const key of ['sourceCommit','sourceManifestSha256','configSha256','executionContext','supervisorPid','supervisorPgid'])requireEvidence(saved[key]===result[key]);
 requireEvidence(same(index.runtime,config.runtime)&&same(attempt.runtime,config.runtime)&&index.wallSeconds<=60&&result.wallSeconds<=15);
 const records=CASES.map((id,i)=>{const r=JSON.parse(evidence[PREFIX+'results/'+id+'/report.json']);requireEvidence(r.case===id&&r.closed===true&&(r.firstFailure?.kind??null)===FIRST[i]&&same(r.secondaryFailures,FIRST[i]?[{kind:'missing-inert-output'}]:[]));if(id!=='capability')requireEvidence(r.closureProbes.length===2&&r.closureProbes.every(p=>p.absent===true)&&Number.isInteger(r.guardianExitCode));for(const event of r.events)if(event.event==='child-start')requireEvidence(r.authorization&&r.authorization.monotonicNs<event.monotonicNs);return r;});
 const labels={'capability':'Real process inspection','normal':'Normal child','child-exit7':'Child exits 7','sampler-nonzero':'Injected sampler exit','sampler-malformed':'Injected malformed row','delayed-ready':'Delayed readiness','child-timeout':'Child timeout','early-guardian-exit':'Guardian exits early'};
 function render(){const filter=$('case-filter').value;const selected=records.filter(r=>filter==='all'||(filter==='negative'?r.firstFailure!==null:r.firstFailure===null));$('cases').replaceChildren();for(const r of selected){const tr=document.createElement('tr');for(const text of [labels[r.case],r.firstFailure?'Expected failure handled':'Passed',r.firstFailure?.kind??'No failure',r.case==='capability'?'No child group':'2 absent probes']){const td=document.createElement('td');td.textContent=text;tr.appendChild(td);}$('cases').appendChild(tr);}$('visible-count').textContent=selected.length+' of 8 cases shown';}
 $('case-filter').addEventListener('change',render);render();
 $('headline').textContent='Eight launch checks passed.';
 $('notice').textContent='Saved checker: 8 / 8 passed · 39 evidence pins verified · no new scientific result.';
 $('timing').textContent='The harmless run took '+index.wallSeconds.toFixed(3)+' s; the saved-file check took '+result.wallSeconds.toFixed(4)+' s. These are operational test durations, not aerodynamic performance measurements.';
 $('binding-summary').textContent='Source '+result.sourceCommit.slice(0,12)+' · 16 source pins reported by the publication receipt. This page verified the saved checker and its 39 evidence pins; it does not rerun that checker.';
 $('facts').hidden=false;$('historical').src=binding.historicalUrl;$('historical').hidden=false;
 window.__statusView={validEvidence:true,execution:'passed',passedCases:8,checkerPins:39,closedGroups:7,historicalOnly:true,scientificQualification:false,cases:CASES};
}catch(error){$('headline').textContent='Evidence could not be verified.';$('notice').classList.add('error');$('notice').textContent='Evidence unavailable or inconsistent. Results and replay are hidden.';$('facts').hidden=true;$('historical').removeAttribute('src');$('historical').hidden=true;window.__statusView={validEvidence:false,error:error.message};}
