const BINDING_SHA='20f3cad0f7c0d1b6e35417436e0880bd2663885d312a09868b022fea0dde8db6';
const $=id=>document.getElementById(id),root=new URL('../../../',location.href);
let observer,deadline,failed=false;
async function bytes(url){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error('Missing pinned record');return new Uint8Array(await r.arrayBuffer());}
async function sha(b){return [...new Uint8Array(await crypto.subtle.digest('SHA-256',b))].map(x=>x.toString(16).padStart(2,'0')).join('');}
async function verify(p){if(!p||typeof p.path!=='string'||p.path.includes('..')||p.path.startsWith('/'))throw Error('Invalid pin');const b=await bytes(new URL(p.path,root));if(b.length!==p.bytes||await sha(b)!==p.sha256)throw Error('Evidence pin mismatch');return b;}
function fail(e){if(failed)return;failed=true;clearTimeout(deadline);observer?.disconnect();$('replay').removeAttribute('src');$('replay').hidden=true;$('content').hidden=true;$('focus-scene').disabled=true;document.body.dataset.binding='failed';document.querySelector('h1').textContent='Evidence display stopped.';document.querySelector('.lead').textContent='The design and historical replay could not be verified.';$('status').textContent='Display stopped: '+e.message;}
function focus(){const d=$('replay').contentDocument;d?.getElementById('scene')?.scrollIntoView({block:'center'});}
async function main(){
 const raw=await bytes(new URL('./binding.json',location.href));if(await sha(raw)!==BINDING_SHA)throw Error('Binding identity mismatch');const b=JSON.parse(new TextDecoder().decode(raw));
 if(b.kind!=='design-only-replay-binding')throw Error('Wrong design binding');
 const historical=JSON.parse(new TextDecoder().decode(await verify(b.historicalManifest)));
 const inventory=new Map(historical.files.map(p=>[p.path,p]));
 for(const p of b.historicalAssets){const x=inventory.get(p.path);if(!x||x.sha256!==p.sha256||x.bytes!==p.bytes)throw Error('Replay asset outside published inventory');}
 await Promise.all([...b.historicalAssets,...b.designRecords].map(verify));
 $('content').hidden=false;$('status').textContent='Design records verified. Loading the unchanged historical 3D replay…';
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
    clearTimeout(deadline);frame.hidden=false;$('focus-scene').disabled=false;document.body.dataset.binding='verified';$('status').textContent='Design records verified · Historical replay verified · No new simulation';focus();
   }
  }
  observer?.disconnect();observer=new MutationObserver(inspect);observer.observe(d.body,{attributes:true,attributeFilter:['data-binding']});inspect();
 });
 frame.src=new URL(b.replayPath,root).href;
 $('focus-scene').addEventListener('click',focus);
}
main().catch(fail);
