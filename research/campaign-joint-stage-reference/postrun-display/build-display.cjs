'use strict';
// Separately timed display/document preparation. No scientific solver imported.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),impl=path.join(root,'implementation'),started=performance.now(),cpu0=process.cpuUsage();
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>fs.readFileSync(path.join(impl,p));
function size(){let n=0;function walk(p){for(const e of fs.readdirSync(p,{withFileTypes:true})){const f=path.join(p,e.name);if(e.isDirectory())walk(f);else n+=fs.statSync(f).size;}}walk(root);return n;}
const beforeBytes=size(),inputs=[];
function identity(p){const b=fs.readFileSync(p);return {path:path.relative(root,p),bytes:b.length,sha256:hash(b)};}
const freeze=JSON.parse(read('FREEZE.json'));
for(const entry of freeze.source.files){const p=path.join(impl,entry.path);if(hash(fs.readFileSync(p))!==entry.sha256)throw Error('Frozen source mismatch before display: '+entry.path);}
const campaign=JSON.parse(read('results/campaign.json'));
for(const rel of ['src/build-viewer.cjs','src/io.cjs','FREEZE.json','results/campaign.json','results/execution-validity.json','demo/app.js','demo/index.html','demo/vendor/three.core.js','demo/vendor/three.module.js','demo/vendor/OrbitControls.js','demo/vendor/THREE-LICENSE.txt'])inputs.push(identity(path.join(impl,rel)));
for(const seed of [840131,840137]){inputs.push(identity(path.join(root,`inputs/arrays/s${seed}-p1-a4.dense.f64`)));inputs.push(identity(path.join(root,`inputs/metadata/s${seed}-p1-a4.dense.f64.json`)));}
for(const id of campaign.runIds){const r=JSON.parse(read(`results/runs/${id}.json`));inputs.push(identity(path.join(impl,`results/runs/${id}.json`)));for(const m of [r.commonStates,r.denseStates])if(m){inputs.push(identity(path.join(impl,m.path)));inputs.push(identity(path.join(impl,m.path+'.json')));}}
const extractionStart=performance.now(),builder=require(path.join(impl,'src/build-viewer.cjs')),summary=builder.build(),extractionWallMs=performance.now()-extractionStart;
const records=read('demo/records.json'),D=JSON.parse(records),linkReview=[];
for(const run of D.runs){const target=path.resolve(impl,'demo',run.recordLink);linkReview.push({runId:run.runId,recordLink:run.recordLink,target:path.relative(root,target),exists:fs.existsSync(target),complete:run.complete,label:run.label,frameCount:run.frames.length,lastDisplayFrameSeconds:run.frames.at(-1)?.t,sourceSha256:run.sourceSha256});if(!fs.existsSync(target))throw Error('Missing run link '+run.recordLink);if(!run.complete&&!run.label.includes('incomplete'))throw Error('Incomplete label missing');}
if(D.referenceAccepted!==false||D.status!=='stopped')throw Error('Partial/unqualified display contract mismatch');
const docs={};for(const run of D.runs)docs[run.recordLink]={mime:'application/json',bytes:fs.readFileSync(path.resolve(impl,'demo',run.recordLink)).toString('base64')};
for(const [key,p,mime]of [['../../PLAN.md',path.join(root,'PLAN.md'),'text/plain'],['../FREEZE.json',path.join(impl,'FREEZE.json'),'application/json'],['../results/campaign.json',path.join(impl,'results/campaign.json'),'application/json'],['vendor/THREE-LICENSE.txt',path.join(impl,'demo/vendor/THREE-LICENSE.txt'),'text/plain']])docs[key]={mime,bytes:fs.readFileSync(p).toString('base64')};
const bundle={records:records.toString('base64'),modules:Object.fromEntries(['three.core.js','three.module.js','OrbitControls.js'].map(f=>[f,read('demo/vendor/'+f).toString('base64')])),app:read('demo/app.js').toString('base64'),docs,sourceHashes:inputs.filter(x=>x.path.includes('/demo/')||x.path.endsWith('build-viewer.cjs')),status:'PARTIAL / UNQUALIFIED',noScientificRecomputation:true};
let html=read('demo/index.html').toString('utf8');html=html.replace(/<script type="importmap">[\s\S]*?<\/script>/,'');
html=html.replace('<main>','<div style="padding:14px 28px;background:#432c24;color:#ffd9b8;font-size:14px;line-height:1.6"><strong>PARTIAL CAMPAIGN · REFERENCE UNQUALIFIED</strong><br>Seven new runs completed. Seed840131 P1 stopped at0.9915625s on its per-job wall cap. Eight rows were skipped. Both joint self-consistency screens passed; required held-physics and cross-family screens remain unfinished.<br><span id="offline-range"></span></div><main>');
html=html.replace('<script type="module" src="app.js"></script>',`<script id="offline-bundle" type="application/json">${JSON.stringify(bundle)}</script><script type="module">
const bundle=JSON.parse(document.getElementById('offline-bundle').textContent);
const decode=b=>new TextDecoder().decode(Uint8Array.from(atob(b),c=>c.charCodeAt(0)));
const asBlob=(text,type='text/javascript')=>URL.createObjectURL(new Blob([text],{type}));
const core=asBlob(decode(bundle.modules['three.core.js']));
const moduleSource=decode(bundle.modules['three.module.js']);
const three=asBlob(moduleSource.replaceAll("'./three.core.js'",JSON.stringify(core)));
const orbit=asBlob(decode(bundle.modules['OrbitControls.js']).replaceAll("from 'three'",'from '+JSON.stringify(three)));
const links=Object.fromEntries(Object.entries(bundle.docs).map(([key,d])=>[key,asBlob(decode(d.bytes),d.mime)]));
const records=JSON.parse(decode(bundle.records));
for(const r of records.runs)r.recordLink=links[r.recordLink];
const originalFetch=globalThis.fetch.bind(globalThis);
globalThis.fetch=(url,init)=>String(url)==='./records.json'?Promise.resolve(new Response(JSON.stringify(records),{status:200,headers:{'Content-Type':'application/json'}})):originalFetch(url,init);
for(const a of document.querySelectorAll('a[href]')){const key=a.getAttribute('href');if(links[key])a.href=links[key];}
const appSource=decode(bundle.app).replaceAll("'./vendor/three.module.js'",JSON.stringify(three)).replaceAll("'./vendor/OrbitControls.js'",JSON.stringify(orbit));
await import(asBlob(appSource));
const range=document.getElementById('offline-range');
function showRange(){const run=records.runs.find(r=>r.runId===document.getElementById('run').value);if(!run)return;range.textContent=run.complete?'Selected record completed its one-second window.':('Selected record is INCOMPLETE. Last displayed saved pose: '+run.frames.at(-1).t.toFixed(3)+'s. Playback beyond this holds that pose visually; it is not additional simulated motion.');}
document.getElementById('run').addEventListener('change',showRange);showRange();
window.__offlineDisplay={loaded:true,status:records.status,referenceAccepted:records.referenceAccepted,runs:records.runs.length};
</script>`);
const output=path.join(__dirname,'joint-stages-partial-offline.html');if(size()+Buffer.byteLength(html)>198000000)throw Error('Display would breach retained-byte cap/reserve');fs.writeFileSync(output,html);
for(const entry of freeze.source.files)if(hash(fs.readFileSync(path.join(impl,entry.path)))!==entry.sha256)throw Error('Frozen source changed during display preparation: '+entry.path);
const cpu=process.cpuUsage(cpu0),receipt={kind:'post-run display/document preparation only',numericalWindowReopened:false,scientificCalculations:false,integrations:false,gatesRecomputed:false,startedAt:new Date(Date.now()-(performance.now()-started)).toISOString(),elapsedWallMs:performance.now()-started,cpuMs:(cpu.user+cpu.system)/1000,extractionWallMs,summary,inputs,outputs:[identity(path.join(impl,'demo/records.json')),identity(output)],linkReview,frozenSourceUnchanged:true,retainedBytesBefore:beforeBytes,retainedBytesBeforeReceipt:size(),hardRetainedCapBytes:200000000,offlinePackaging:'Exact unchanged source bytes embedded as base64. Bootstrap rewrites only module import URLs in memory to blob URLs, serves embedded actual records via a scoped fetch shim, and resolves evidence links to embedded document blobs. Frozen files unchanged.',browserRenderingVerified:false};
fs.writeFileSync(path.join(__dirname,'DISPLAY-PREPARATION.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify({elapsedWallMs:receipt.elapsedWallMs,cpuMs:receipt.cpuMs,runs:D.runs.length,recordsBytes:records.length,offlineHtmlBytes:Buffer.byteLength(html),retainedBytes:size()}));
