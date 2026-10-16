const BINDING_SHA='d680c3107107185895d2ce65285142658d8ee9fa0281fcc071d8a1afc6538110';
const $=id=>document.getElementById(id),root=new URL('../../../',location.href);
let observer,deadline,failed=false;
async function bytes(url){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error('Missing pinned record');return new Uint8Array(await r.arrayBuffer());}
async function sha(b){return [...new Uint8Array(await crypto.subtle.digest('SHA-256',b))].map(x=>x.toString(16).padStart(2,'0')).join('');}
async function verify(p){if(!p||typeof p.path!=='string'||p.path.includes('..')||p.path.startsWith('/'))throw Error('Invalid pin');const b=await bytes(new URL(p.path,root));if(b.length!==p.bytes||await sha(b)!==p.sha256)throw Error('Evidence pin mismatch');return b;}
function fail(e){if(failed)return;failed=true;clearTimeout(deadline);observer?.disconnect();$('replay').removeAttribute('src');$('replay').hidden=true;$('content').hidden=true;$('focus-scene').disabled=true;document.body.dataset.binding='failed';document.querySelector('h1').textContent='Evidence display stopped.';document.querySelector('.lead').textContent='The arithmetic evidence and historical replay could not be verified.';$('status').textContent='Display stopped: '+e.message;}
function focus(){const d=$('replay').contentDocument;d?.getElementById('scene')?.scrollIntoView({block:'center'});}
async function main(){
 const raw=await bytes(new URL('./binding.json',location.href));if(await sha(raw)!==BINDING_SHA)throw Error('Binding identity mismatch');const b=JSON.parse(new TextDecoder().decode(raw));
 if(b.kind!=='primitive-result-replay-binding')throw Error('Wrong result binding');
 const historical=JSON.parse(new TextDecoder().decode(await verify(b.historicalManifest)));
 const inventory=new Map(historical.files.map(p=>[p.path,p]));
 for(const p of b.historicalAssets){const x=inventory.get(p.path);if(!x||x.sha256!==p.sha256||x.bytes!==p.bytes)throw Error('Replay asset outside published inventory');}
 await Promise.all([...b.historicalAssets,...b.designRecords].map(verify));
 const records=Object.fromEntries(await Promise.all(Object.entries(b.resultRecords).map(async([key,p])=>[key,JSON.parse(new TextDecoder().decode(await verify(p)))])));
 const {kernel,checker,audit,publication,sourceManifest}=records;
 if(![kernel,checker].every(x=>x.success===true&&x.closed===true&&x.childGroupAbsent===true&&x.sourceAndRuntimeRechecked===true)||publication.remoteBytesEqualLocal!==true||audit.passed!==true||audit.baselineErrorCount!==0||audit.totalRecords!==1488||audit.journal?.passed!==true)throw Error('Arithmetic qualification incomplete');
 if(!audit.faultControls||audit.faultControls.length!==5||audit.faultControls.flatMap(c=>c.probes).length!==6||!audit.faultControls.every(c=>c.executed&&c.passed&&c.probes.every(p=>p.rejected)))throw Error('Fault controls incomplete');
 const expected={ok:1032,'unresolved-domain':215,'unresolved-range':236,'invalid-nonfinite':5,'invalid-bits':0,'invalid-interval':0,'unresolved-iteration':0,'unresolved-sqrt-check':0};
 for(const [key,n] of Object.entries(expected))if(audit.expectedStatusCounts[key]!==n||audit.observedStatusCounts[key]!==n)throw Error('Displayed counts differ from audited record');
 for(const stage of [kernel,checker])if(stage.sourceCommit!==publication.commit||stage.sourceManifestSha256!==publication.manifestSha256)throw Error('Source identity mismatch');
 if(publication.manifestSha256!==b.resultRecords.sourceManifest.sha256||audit.sourceManifest.sha256!==publication.manifestSha256||checker.output.sha256!==b.resultRecords.audit.sha256||audit.input.sha256!==kernel.output.sha256||audit.journal.sha256!==kernel.journal.sha256||sourceManifest.allocation.primitiveRecords!==1488)throw Error('Result chain mismatch');

 $('content').hidden=false;$('status').textContent='Arithmetic records verified. Loading the unchanged historical 3D replay…';
 const frame=$('replay');
 deadline=setTimeout(()=>fail(Error('Historical replay did not finish verification')),45000);
 frame.addEventListener('load',()=>{
  if(failed)return;
  const d=frame.contentDocument;
  if(!d?.body){fail(Error('Replay document unavailable'));return;}
  function inspect(){
   if(failed)return;
   const state=d.body.dataset.binding;
   if(state==='failed'){fail(Error('Historical replay failed its own evidence checks'));return;}
   if(state==='verified'){
    clearTimeout(deadline);frame.hidden=false;$('focus-scene').disabled=false;document.body.dataset.binding='verified';$('status').textContent='Arithmetic records verified · Historical replay verified · No new drone simulation';focus();
   }
  }
  observer?.disconnect();observer=new MutationObserver(inspect);observer.observe(d.body,{attributes:true,attributeFilter:['data-binding']});inspect();
 });
 frame.src=new URL(b.replayPath,root).href;
 $('focus-scene').addEventListener('click',focus);
}
main().catch(fail);
