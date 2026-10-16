// Display saved evidence only; never imports or invokes scientific code.
const BINDING_SHA='1319efa4a1546e767b74b93a7db5d2bb465ee95c7ef41ad27333baca8a679884';
const $=id=>document.getElementById(id);
const sha=async b=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b)),x=>x.toString(16).padStart(2,'0')).join('');
async function checked(url,pin){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error('Missing evidence');const b=await r.arrayBuffer();if(await sha(b)!==pin.sha256||(pin.bytes!==undefined&&b.byteLength!==pin.bytes))throw Error('Evidence digest mismatch');return new TextDecoder().decode(b);}
try{
 const b=JSON.parse(await checked('binding.json',{sha256:BINDING_SHA}));if(b.schema!=='m31-normalizer-failed-launch-view-v1'||b.pins.length!==7)throw Error('Binding mismatch');
 const e={};for(const p of b.pins)e[p.path]=await checked('../../../'+p.path,p);
 const prefix='research/m31-normalizer-ablation-2026-10-17/';const s=JSON.parse(e[prefix+'results/kernel-supervision.json']),a=JSON.parse(e[prefix+'results/kernel-attempt.json']),pub=JSON.parse(e[prefix+'source-publication.json']);
 if(s.success!==false||s.closed!==true||s.childGroupAbsent!==true||s.samples!==0||s.scientificEvidence.length!==0||s.terminationReason!=='incomplete-stage-evidence'||s.sourceCommit!==b.sourceCommit||a.sourceCommit!==b.sourceCommit||pub.commit!==b.sourceCommit||pub.manifestSha256!==s.sourceManifestSha256||pub.verifiedFilePins!==88||pub.remoteBytesEqualLocal!==true||pub.committedBytesEqualLocal!==true)throw Error('Outcome mismatch');
 $('notice').textContent='Closed failed launch · all scientific outcomes remain untested.';
 $('detail').textContent='The supervised attempt ended after '+s.wallSeconds.toFixed(3)+' seconds. This is failed-launch elapsed time, not a method benchmark. Zero memory samples were recorded, so reported zero RSS is not a memory-use measurement.';
 $('facts').hidden=false;$('historical').src=b.historicalUrl;$('historical').hidden=false;
 window.__failureView={validEvidence:true,launchPassed:false,scientificStatus:'untested',historicalOnly:true,sourceCommit:b.sourceCommit};
}catch(e){$('notice').classList.add('error');$('notice').textContent='Evidence unavailable or inconsistent. Research details and historical replay are hidden.';$('facts').hidden=true;$('historical').removeAttribute('src');$('historical').hidden=true;window.__failureView={validEvidence:false,error:e.message};}
