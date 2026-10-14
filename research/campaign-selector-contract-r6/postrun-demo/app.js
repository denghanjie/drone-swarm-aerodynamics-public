"use strict";
const $=id=>document.getElementById(id),publicLayout=location.pathname.includes('/campaign-selector-contract-r6/');
if(!publicLayout)$('semantic').href='../../audit-r6-semantic-review/postrun/PUBLIC-SUMMARY.md';
async function read(url){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error('Unavailable selected derivative: '+url);return r.text();}
(async()=>{try{
const [summaryText,indexText]=await Promise.all([read('../postrun-report/EVIDENCE.json'),read('../postrun-report/CASE-DECISIONS.json')]);const e=JSON.parse(summaryText),index=JSON.parse(indexText);
if(e.schema!=='selector-r6-sanitized-postrun-summary/v1'||index.schema!=='selector-r6-public-case-decision-index/v1'||e.isOriginalReceipt!==false||index.isOriginalReceipt!==false||index.rawReceiptsPublic!==false)throw Error('Unexpected derivative schema or scope.');
const rows=index.rows;if(rows.length!==100||rows.some((r,i)=>r.length!==6||r[0]!==i+1||r[3]!==r[4]||!/^[0-9a-f]{64}$/.test(r[5])))throw Error('Case-index decision or identity mismatch.');
const count=kind=>rows.filter(r=>r[2]===kind).length;if(count('nominal')!==23||count('negative')!==73||count('positive-control')!==4||e.coverage.matchedExpectedDecisions!==100)throw Error('Case counts differ from summary.');
let digestStatus='Browser digest verification unavailable; counts/decisions only checked.';
if(globalThis.crypto&&crypto.subtle){const bytes=new TextEncoder().encode(indexText),digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),b=>b.toString(16).padStart(2,'0')).join('');if(digest!==e.caseDecisionIndex.sha256||bytes.length!==e.caseDecisionIndex.bytes)throw Error('Decision-index byte identity differs from summary.');digestStatus='The decision-index bytes match the summary SHA-256.';}
for(const row of rows){const tr=document.createElement('tr');for(const value of [row[0]+': '+row[1],...row.slice(2)]){const td=document.createElement('td');td.textContent=value;tr.append(td);}$('cases').append(tr);}
$('acceptance').textContent=e.coordinatorAcceptance.accepted?'Accepted for the fixed retained-record selector/timebase contract':'Final reviewed coordinator acceptance pending';
$('checks').textContent='Loaded sanitized derivatives: all 100 recorded decisions match their expected outcomes. '+digestStatus+' No raw receipt, selector, model or experiment was executed by this page.';
}catch(error){$('checks').className='error';$('checks').textContent='Derivative loading/checking incomplete: '+error.message+' The saved text is not a live verification. Serve via static HTTP or inspect the linked selected files.';}})();
$('load-replay').addEventListener('click',()=>{const frame=document.createElement('iframe');frame.title='Unchanged earlier historical swarm replay; no R6 flight';frame.src=publicLayout?'../../campaign-joint-stage-reference/postrun-display/joint-stages-partial-offline.html':'../../research-next/postrun-display/joint-stages-partial-offline.html';$('replay-host').replaceChildren(frame);$('load-replay').hidden=true;$('replay-status').textContent='Earlier viewer requested. Its trajectories and P1 partial-pose hold predate R6.';});
