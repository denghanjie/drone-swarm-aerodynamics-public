"use strict";
const $=id=>document.getElementById(id);
const publicLayout=location.pathname.includes('/campaign-census-checkpoint-r5/');
const recordRoot='../results/attempt-001/';
const ids=Array.from({length:21},(_,i)=>'R5-'+String(i+1).padStart(2,'0'));
const injected=new Set(['R5-12','R5-16','R5-17','R5-18']);
for(const id of ids){const li=document.createElement('li'),a=document.createElement('a');a.href=recordRoot+id+'.json';a.textContent=id+(injected.has(id)?' · injected metadata':' · real filesystem');li.append(a);$('cases').append(li);}
if(!publicLayout){$('semantic').href='../../audit-r5-semantic-review/postrun/PUBLIC-SUMMARY.md';$('literature').href='../../audit-r5-semantic-review/postrun/literature/README.md';}
async function read(url){const response=await fetch(url,{cache:'no-store'});if(!response.ok)throw Error('Record unavailable: '+url);return response.json();}
(async()=>{try{
const [summary,result,parent,...cases]=await Promise.all([read('../postrun-report/EVIDENCE.json'),read(recordRoot+'result.json'),read(recordRoot+'PARENT-OBSERVATION.json'),...ids.map(id=>read(recordRoot+id+'.json'))]);
if(summary.schema!=='census-r5-sanitized-postrun-summary/v1'||summary.isOriginalReceipt!==false||summary.coordinatorAccepted!==true)throw Error('Expected reviewed sanitized acceptance was not found.');
if(result.completed!==21||result.unrun!==0||result.error!==null||parent.exit_code!==0||parent.timeout!==false||!parent.payload_accounting_complete)throw Error('Terminal record facts differ from the stated result.');
if(cases.some((r,i)=>r.id!==ids[i]||r.expected!==r.observed))throw Error('A prescribed case identity/outcome did not match.');
const accepts=cases.filter(r=>r.observed==='accept').length;
if(accepts!==10||cases.length-accepts!==11||summary.coverage.matchedExpected!==21||summary.coverage.unexpectedOutcomes!==0)throw Error('Aggregate result mismatch.');
if(cases.some(r=>(r.evidence==='injected-metadata')!==injected.has(r.id)))throw Error('Metadata-injection labels differ from the records.');
if(parent.payload_read_upper!==summary.resourceObservations.instrumentedPayloadReadUpperBytes||parent.payload_write_upper!==summary.resourceObservations.instrumentedPayloadWriteUpperBytes)throw Error('Resource aggregate mismatch.');
$('load-status').textContent='Loaded the sanitized later acceptance, original child/parent records and all 21 receipts: 21/21 prescribed decisions match, with 10 accepts and 11 intended control errors. This page checks recorded metadata only; it does not rerun the protocol.';
}catch(error){$('load-status').className='error';$('load-status').textContent='Record loading/checking incomplete: '+error.message+' The saved summary is not a live verification. Serve this page over static HTTP or inspect the linked originals.';}})();
$('replay-button').addEventListener('click',()=>{const frame=document.createElement('iframe');frame.title='Earlier unqualified historical swarm replay; no R5 flight';frame.src=publicLayout?'../../campaign-joint-stage-reference/postrun-display/joint-stages-partial-offline.html':'../../research-next/postrun-display/joint-stages-partial-offline.html';$('replay-host').replaceChildren(frame);$('replay-button').hidden=true;$('replay-status').textContent='Earlier viewer requested. All trajectories are historical, including P1 partial-pose hold.';});
