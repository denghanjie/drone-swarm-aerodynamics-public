'use strict';
// Browser-only saved-data QA. No scientific source imports, reruns or mutations.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {chromium}=require('playwright');
const root=process.env.RESEARCH_ROOT,attempt=Number(process.env.RESEARCH_QA_ATTEMPT);
if(!root||!Number.isInteger(attempt)||attempt<1||attempt>3)throw Error('Explicit root and QA attempt 1..3 required');
const relative='research/m31-oracle-omission-renewal-2026-10-17',prior='research/m31-normalizer-replication-2026-10-17';
const pkg=path.join(root,relative),qa=path.join(pkg,'qa'),out=path.join(qa,'attempt-'+String(attempt).padStart(2,'0'));
fs.mkdirSync(out,{recursive:false});fs.copyFileSync(__filename,path.join(out,'run.cjs'));
const base='http://localhost:8876/'+relative+'/viewer/';
const BINDING_SHA='8be075947e19308f885b9e2caef6218db0fcef26e381efa92b66d27d4373c297';
const DISPLAY_SHA='dc368b8248a2694b8ce2763bbfe8cd286338b84ad01ce1dfda6a2533e2c166fb';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=rel=>JSON.parse(fs.readFileSync(path.join(root,rel)));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const value=w=>Buffer.from(w,'hex').readDoubleBE();
const fmt=n=>n.toLocaleString('en-US');
const percent=(n,d)=>d>0?(100*n/d).toFixed(2)+'%':'undefined';
const report={scope:'Bound saved-display browser QA only; zero scientific reruns',attempt,url:base,
 browserPath:'Browser plugin not available; installed Playwright fallback explicitly authorized. Parent reported IAB unavailable.',
 viewports:[{width:1440,height:1050},{width:390,height:844}],checks:[],combinations:[],errors:[],warnings:[],requests:[],
 renderedSnapshots:0,renderedBodies:0,renderedCenterComponents:0,sourcePinCount:61,resultFileCount:4};
let browser,page;const start=Date.now();
function persist(){report.wallMs=Date.now()-start;report.within60Seconds=report.wallMs<=60000;fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');}
function check(name,ok,detail){report.checks.push({name,passed:Boolean(ok),...(detail===undefined?{}:{detail})});if(!ok)throw Error(name);}
function immutable(){
 const m=read(relative+'/source-manifest.json');check('source manifest retains 61 pins',m.files.length===61);
 const files=m.files.map(p=>{const b=fs.readFileSync(path.join(root,p.path));check('frozen pin '+p.path,b.length===p.bytes&&sha(b)===p.sha256);return {path:p.path,bytes:b.length,sha256:sha(b)};});
 const results=['analyze-attempt.json','analyze.json','check-attempt.json','check.json'].map(name=>{const p=relative+'/results/'+name,b=fs.readFileSync(path.join(root,p));return {path:p,bytes:b.length,sha256:sha(b)};});
 return {manifestSha256:sha(fs.readFileSync(path.join(pkg,'source-manifest.json'))),files,results};
}
const stop=setTimeout(()=>{report.passed=false;report.failure='55-second bounded QA stop';persist();browser?.close().catch(()=>{});},55000);
const hard=setTimeout(()=>{report.passed=false;report.failure='59.5-second hard QA stop';persist();process.exit(1);},59500);
(async()=>{let before;try{
 before=immutable();const first=path.join(qa,'IMMUTABLE-BEFORE.json');if(fs.existsSync(first))check('prior immutable baseline unchanged',eq(before,JSON.parse(fs.readFileSync(first))));else fs.writeFileSync(first,JSON.stringify(before,null,2)+'\n',{flag:'wx'});
 fs.writeFileSync(path.join(out,'immutable-before.json'),JSON.stringify(before,null,2)+'\n');
 for(const name of ['index.html','app.js','scene.js','style.css','build-binding.py'])fs.copyFileSync(path.join(pkg,'viewer',name),path.join(out,name));
 check('accepted binding digest',sha(fs.readFileSync(path.join(pkg,'viewer/binding.json')))===BINDING_SHA);
 check('accepted compact display digest',sha(fs.readFileSync(path.join(pkg,'viewer/display-data.json')))===DISPLAY_SHA);
 const analysis=read(relative+'/results/analyze.json'),checker=read(relative+'/results/check.json');check('saved analysis independently accepted',checker.passed===true&&analysis.states.length===6);
 const binding=read(relative+'/viewer/binding.json'),display=read(relative+'/viewer/display-data.json');
 const generations=Object.fromEntries(['run-a','run-b'].map(id=>[id,read(prior+'/results/generation/'+id+'.json')]));
 const lastReference=read(prior+'/results/reference/run-b-t10.json');
 const plan=['run-a','run-b'].flatMap(runId=>[0,5,10].map(t=>({id:runId+'-t'+t,runId,t})));
 browser=await chromium.launch({headless:true,args:['--disable-background-networking']});report.browserVersion=browser.version();
 page=await browser.newPage({viewport:report.viewports[0]});page.setDefaultTimeout(4500);
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());if(m.type()==='warning')report.warnings.push(m.text());});page.on('request',r=>report.requests.push(r.url()));
 // Inspect actual renderer uploads without changing their values or model code.
 await page.addInitScript(()=>{for(const kind of ['WebGLRenderingContext','WebGL2RenderingContext']){const proto=window[kind]?.prototype;if(!proto)continue;for(const name of ['bufferData','bufferSubData']){const original=proto[name];if(!original)continue;proto[name]=function(...args){const data=args[name==='bufferData'?1:2];if(data instanceof Float32Array&&data.length===16128*6)window.__qaOverlayUpload={calls:(window.__qaOverlayUpload?.calls||0)+1,first12:Array.from(data.slice(0,12))};return original.apply(this,args);};}}});
 await page.goto(base,{waitUntil:'networkidle',timeout:12000});await page.waitForFunction(()=>window.__viewState?.validEvidence||window.__viewState?.error,null,{timeout:8000});
 check('page identity',page.url()===base&&(await page.title()).includes('Oracle omission screen'));
 check('meaningful nonblank screen',(await page.locator('h1').innerText()).includes('positive interaction'));
 check('no framework error overlay',await page.locator('vite-error-overlay,nextjs-portal').count()===0);
 check('accepted snapshot rendered',await page.evaluate(()=>window.__viewState?.validEvidence&&window.__viewState.renderedBodyCount===64),await page.locator('#notice').innerText());
 check('saved independent check visible',await page.locator('#check-status').innerText()==='Passed');
 await page.screenshot({path:path.join(out,'desktop-first-viewport.png')});
 for(const state of plan)for(const tier of ['1e-8','1e-4','1e-2'])for(const tree of ['T8','T2']){
  await page.selectOption('#state',state.id);await page.selectOption('#tier',tier);await page.selectOption('#tree',tree);
  const view=await page.evaluate(()=>window.__viewState),evidence=await page.evaluate(()=>window.__evidenceState);
  const saved=analysis.states.find(s=>s.id===state.id),summary=saved.summary.find(s=>s.tier===tier),expected=summary.trees[tree];
  const frame=generations[state.runId].frames.find(f=>f.t===state.t),label=state.id+'/'+tier+'/'+tree;
  check(label+' identity',view.validEvidence&&view.stateId===state.id&&view.t===state.t&&view.run===state.runId&&view.tier===tier&&view.tree===tree&&view.renderedBodyCount===64);
  check(label+' all 64 recorded centers',view.positions.length===64&&view.positions.every((p,i)=>p.length===3&&p.every((v,k)=>v===Math.fround(value(frame.words[7*i+k])))));
  check(label+' selected and rendered link counts',view.selectedLinkCount===expected.positiveCovered&&view.renderedLinkCount===expected.positiveCovered&&view.overlayCount===expected.positiveCovered);
  check(label+' selected denominator text',(await page.locator('#selected-count').innerText())===fmt(expected.positiveCovered)+' / '+fmt(saved.positiveTerms));
  check(label+' all six rows retained',await page.locator('#all-results tr').count()===6&&evidence.denominator===6&&evidence.rows.length===6);
  const renderedRows=await page.locator('#all-results tr').evaluateAll(rows=>rows.map(row=>Array.from(row.querySelectorAll('td')).map(cell=>({first:cell.childNodes[0]?.textContent.trim(),small:cell.querySelector('small')?.textContent}))));
  for(let n=0;n<6;n++){
   const source=analysis.states[n],q=source.summary.find(s=>s.tier===tier),z=q.trees[tree];
   check(label+' table '+source.id,eq(evidence.rows[n].summary,q)&&renderedRows[n][1].first===fmt(source.positiveTerms)&&[q.optimisticCeiling,q.singletonFeasible,q.trees.T8.positiveCovered,q.trees.T2.positiveCovered].every((v,k)=>renderedRows[n][k+2].first===fmt(v)&&renderedRows[n][k+2].small===percent(v,source.positiveTerms))&&renderedRows[n][6].first===[z.groups,z.rowsCovered,z.membersCovered,z.nodeVisits].map(fmt).join(' / '));
  }
  report.combinations.push({id:state.id,tier,tree,positiveTerms:saved.positiveTerms,selectedPositive:expected.positiveCovered,renderedLinks:view.renderedLinkCount,bodyPositionsChecked:64});report.renderedSnapshots++;report.renderedBodies+=64;report.renderedCenterComponents+=192;
 }
 check('36 combinations complete',report.combinations.length===36);
 check('only last-state T2 stress has links',report.combinations.every(c=>c.selectedPositive===(c.id==='run-b-t10'&&c.tier==='1e-2'&&c.tree==='T2'?2:0)));
 const selected=analysis.states.find(s=>s.id==='run-b-t10');const reference=new Map(lastReference.prepared.map(p=>[p.id,p.value]));
 const actualPositive=new Set(lastReference.pairs.filter(p=>p.status==='positive').map(p=>[p.i,p.r,p.j].join(':')));
 const expectedEdges=selected.rows.flatMap(r=>r.tiers.find(t=>t.tier==='1e-2').trees.T2.selected.flatMap(n=>n.positiveMembers.map(j=>({receiver:r.i,rotor:r.r,source:j,endpoints:[...reference.get(j).center,...reference.get(r.i).points[r.r]].map(value)}))));
 const current=await page.evaluate(()=>window.__viewState);check('two exact stable-ID reference endpoints',expectedEdges.length===2&&expectedEdges.every(e=>actualPositive.has([e.receiver,e.rotor,e.source].join(':')))&&eq(current.edgeSamples,expectedEdges),expectedEdges);
 await page.waitForFunction(()=>window.__qaOverlayUpload?.first12?.length===12,null,{timeout:4000});
 check('actual GPU endpoints match saved reference words after float32 conversion',eq(await page.evaluate(()=>window.__qaOverlayUpload.first12),expectedEdges.flatMap(e=>e.endpoints.map(Math.fround))));
 await page.locator('#overlays').uncheck();check('overlay toggle hides geometry without changing counts',await page.evaluate(()=>window.__viewState.renderedLinkCount===0&&window.__viewState.selectedLinkCount===2));await page.locator('#overlays').check();check('overlay toggle restores two links',await page.evaluate(()=>window.__viewState.renderedLinkCount===2));
 await page.locator('#state').selectOption('run-a-t0');check('snapshot switch removes stale links',await page.evaluate(()=>window.__viewState.renderedLinkCount===0));await page.locator('#all-results tr').last().locator('button').click();check('table state control returns exact 10 s snapshot',await page.evaluate(()=>window.__viewState.stateId==='run-b-t10'&&window.__viewState.t===10&&window.__viewState.renderedLinkCount===2));
 const canvas=page.locator('#scene canvas');await canvas.scrollIntoViewIfNeeded();await page.waitForTimeout(250);const box=await canvas.boundingBox();check('visible Three.js canvas',box&&box.width>300&&box.height>300);
 const initial=await canvas.screenshot({path:path.join(out,'controls-before.png')});
 await page.mouse.move(box.x+box.width*.50,box.y+box.height*.50);await page.mouse.down();await page.mouse.move(box.x+box.width*.69,box.y+box.height*.62,{steps:12});await page.mouse.up();await page.waitForTimeout(650);
 const orbit=await canvas.screenshot({path:path.join(out,'controls-orbit.png')});check('orbit changes actual canvas',sha(initial)!==sha(orbit));
 await page.mouse.wheel(0,-180);await page.waitForTimeout(650);const zoom=await canvas.screenshot({path:path.join(out,'controls-zoom.png')});check('zoom changes actual canvas',sha(orbit)!==sha(zoom));
 await page.locator('#reset').click();await canvas.scrollIntoViewIfNeeded();await page.waitForTimeout(650);const reset=await canvas.screenshot({path:path.join(out,'controls-reset.png')});check('reset restores exact scene view',sha(reset)===sha(initial));
 await page.screenshot({path:path.join(out,'desktop-selected-overlay.png')});await page.locator('.evidence').first().scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'desktop-evidence.png')});
 check('desktop page has no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.setViewportSize(report.viewports[1]);await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(180);await page.screenshot({path:path.join(out,'mobile-first-viewport.png')});
 await page.locator('.visual').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'mobile-overlay.png')});
 await page.locator('#state').selectOption('run-a-t5');await page.locator('#tier').selectOption('1e-4');await page.locator('#tree').selectOption('T8');check('mobile controls show exact empty snapshot',await page.evaluate(()=>window.__viewState.stateId==='run-a-t5'&&window.__viewState.t===5&&window.__viewState.renderedLinkCount===0&&window.__viewState.renderedBodyCount===64));
 await page.locator('.evidence').first().scrollIntoViewIfNeeded();await page.waitForTimeout(180);await page.screenshot({path:path.join(out,'mobile-table-left.png')});const table=page.locator('.table-wrap');
 await table.evaluate(e=>e.scrollLeft=e.scrollWidth);await page.waitForTimeout(180);await page.screenshot({path:path.join(out,'mobile-table-right.png')});
 check('mobile table permits horizontal access and retains six rows',await table.evaluate(e=>e.scrollLeft>0&&e.scrollWidth>e.clientWidth&&e.querySelectorAll('tbody tr').length===6));check('mobile page has no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 check('no browser console or page errors',report.errors.length===0,report.errors);check('no browser warnings',report.warnings.length===0,report.warnings);
 check('no scientific or remote browser requests',report.requests.every(u=>u.startsWith('http://localhost:8876/')&&!u.includes('/source/')));
 for(const resource of ['binding.json','display-data.json']){
  const p=await browser.newPage({viewport:report.viewports[0]});await p.route(new URL(resource,base).href,route=>route.fulfill({status:200,contentType:'application/json',body:'{}'}));await p.goto(base,{waitUntil:'networkidle',timeout:8000});await p.waitForFunction(()=>window.__viewState?.validEvidence===false,null,{timeout:4000});
  check('corrupted '+resource+' withdraws claims and poses',await p.locator('#all-results tr').count()===6&&await p.locator('#check-status').innerText()==='Not bound'&&await p.locator('#selected-count').innerText()==='—'&&await p.locator('#state').isDisabled()&&await p.locator('#tier').isDisabled()&&await p.locator('#tree').isDisabled()&&await p.locator('#overlays').isDisabled()&&await p.locator('#scene canvas:visible').count()===0&&await p.locator('#all-results td').filter({hasText:'Not bound'}).count()===36);
  await p.screenshot({path:path.join(out,'corrupt-'+resource.replace('.json','')+'.png')});await p.close();
 }
 const referencePage=await browser.newPage({viewport:report.viewports[0]});await referencePage.goto('http://localhost:8876/'+prior+'/viewer/',{waitUntil:'networkidle',timeout:8000});await referencePage.waitForFunction(()=>window.__viewState?.validEvidence,null,{timeout:4000});await referencePage.screenshot({path:path.join(out,'reference-replication.png')});await referencePage.close();
 report.designReference='Prior replication viewer: retained dark teal panels, mint drone glyphs, responsive table and provenance layout; intentionally uses fixed snapshots and amber coefficient links.';
 report.passed=true;
}catch(error){report.passed=false;report.failure=error.message;try{await page?.screenshot({path:path.join(out,'failure.png')});}catch(_){}
}finally{
 try{if(browser)await browser.close();}catch(_){}
 try{const after=immutable();fs.writeFileSync(path.join(out,'immutable-after.json'),JSON.stringify(after,null,2)+'\n');check('all 61 frozen pins and four result files preserved',eq(before,after));report.preservationPassed=true;}catch(e){report.passed=false;report.preservationPassed=false;report.preservationFailure=e.message;}
 clearTimeout(stop);clearTimeout(hard);persist();console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,combinations:report.combinations.length,positions:report.renderedCenterComponents,wallMs:report.wallMs,preservation:report.preservationPassed,failure:report.failure}));if(!report.passed||!report.within60Seconds)process.exitCode=1;
}})();
