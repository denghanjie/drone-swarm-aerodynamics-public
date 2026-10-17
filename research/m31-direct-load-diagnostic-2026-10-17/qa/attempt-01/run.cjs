'use strict';
// Saved-record browser QA only. No scientific imports, builder runs or candidate updates.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {chromium}=require('playwright');
const root=process.env.RESEARCH_ROOT,attempt=Number(process.env.RESEARCH_QA_ATTEMPT);
if(!root||!Number.isInteger(attempt)||attempt<1||attempt>3)throw Error('Explicit repository root and bounded attempt 1..3 required');
const relative='research/m31-direct-load-diagnostic-2026-10-17',prior='research/m31-normalizer-replication-2026-10-17';
const pkg=path.join(root,relative),qa=path.join(pkg,'qa'),out=path.join(qa,'attempt-'+String(attempt).padStart(2,'0'));
fs.mkdirSync(out,{recursive:false});fs.copyFileSync(__filename,path.join(out,'run.cjs'));
const base='http://localhost:8876/'+relative+'/viewer/';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const read=relative=>JSON.parse(fs.readFileSync(path.join(root,relative))),value=w=>Buffer.from(w,'hex').readDoubleBE();
const TIERS=['1e-8','1e-4','1e-2'],METRICS=['rotor','collective','worldForce','worldMoment'];
const plan=['run-a','run-b'].flatMap(runId=>[0,5,10].map(t=>({id:runId+'-t'+t,runId,t})));
const report={scope:'Saved-data browser QA only; zero scientific imports/reruns and zero builder reruns',attempt,url:base,
 browserMethod:'Installed Chrome via Playwright fallback; Browser/IAB previously unavailable; outside-sandbox local launch authorized.',
 viewports:[{width:1440,height:1050},{width:390,height:844}],checks:[],combinations:[],overviewProjections:[],errors:[],warnings:[],requests:[],operationalRedactions:[],
 renderedSnapshots:0,renderedBodies:0,renderedCenterComponents:0,renderedLinkEndpoints:0,sourcePinCount:159,resultFileCount:4};
const start=Date.now();let browser,page,before;
function operational(message,label){
 const original=String(message),clean=original.replaceAll(process.env.HOME||'[HOME_UNSET]','[HOME]').replace(/\/(?:private\/)?var\/folders\/[^\s"']+/g,'[TEMP_PROFILE_PATH]');
 if(original!==clean){const privateDir=path.join('/tmp','m31-direct-qa-private','attempt-'+String(attempt).padStart(2,'0'));fs.mkdirSync(privateDir,{recursive:true});const n=report.operationalRedactions.length+1;fs.writeFileSync(path.join(privateDir,n+'-original.txt'),original);fs.writeFileSync(path.join(privateDir,n+'-public.txt'),clean);report.operationalRedactions.push({label,originalSha256:sha(original),publicSha256:sha(clean),rule:'Only operational home/temp-profile paths redacted; original privately retained.'});}
 return clean;
}
function persist(){report.wallMs=Date.now()-start;report.within60Seconds=report.wallMs<=60000;fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');}
function check(name,ok,detail){report.checks.push({name,passed:Boolean(ok),...(detail===undefined?{}:{detail})});if(!ok)throw Error(name);}
function immutable(){
 const manifest=read(relative+'/source-manifest.json');check('manifest retains 159 frozen pins',manifest.files.length===159);
 const files=manifest.files.map(p=>{const b=fs.readFileSync(path.join(root,p.path));check('frozen pin '+p.path,b.length===p.bytes&&sha(b)===p.sha256);return {path:p.path,bytes:b.length,sha256:sha(b)};});
 const results=['analyze-attempt.json','analyze.json','check-attempt.json','check.json'].map(name=>{const p=relative+'/results/'+name,b=fs.readFileSync(path.join(root,p));return {path:p,bytes:b.length,sha256:sha(b)};});
 return {manifestSha256:sha(fs.readFileSync(path.join(pkg,'source-manifest.json'))),files,results};
}
const decimal=q=>{if(q.n==='0')return '0';const n=q.n,d=q.d;return ((Number(n.slice(0,16))/Number(d.slice(0,16)))*10**((n.length-Math.min(16,n.length))-(d.length-Math.min(16,d.length)))).toExponential(3);};
const errorText=(a,b)=>a==='A'?'≈ ['+decimal(b.l)+', '+decimal(b.u)+']':'Upper ≈ '+decimal(b.u);
const label=(s,a)=>s==='pass'?(a==='A'?'Pass':'Certified'):s==='definite-fail'?'Definite fail':s==='not-certified'?'Not certified':'Unresolved';
const selectedTier=(a,t)=>a.tiers.find(x=>x.tier===t);
const stop=setTimeout(()=>{report.passed=false;report.failure='55-second bounded browser QA stop';persist();browser?.close().catch(()=>{});},55000);
const hard=setTimeout(()=>{report.passed=false;report.failure='59.5-second hard browser QA stop';persist();process.exit(1);},59500);
(async()=>{try{
 before=immutable();check('accepted manifest digest',before.manifestSha256==='93d26849dcd0a86d18b254f8eb5babc3d13e0f46d08efc92dfc2bc5cef79635b');
 const baseline=path.join(qa,'IMMUTABLE-BEFORE.json');if(fs.existsSync(baseline))check('prior QA immutable baseline retained',eq(before,JSON.parse(fs.readFileSync(baseline))));else fs.writeFileSync(baseline,JSON.stringify(before,null,2)+'\n',{flag:'wx'});
 fs.writeFileSync(path.join(out,'immutable-before.json'),JSON.stringify(before,null,2)+'\n');
 for(const n of ['index.html','app.js','scene.js','style.css','build-binding.py'])fs.copyFileSync(path.join(pkg,'viewer',n),path.join(out,n));
 check('accepted display digest',sha(fs.readFileSync(path.join(pkg,'viewer/display-data.json')))==='4da9f4965d686f04ef1ac082cdd6e01a5f7054684c03ea43ea7eb37e895ea9ad');
 check('accepted binding digest',sha(fs.readFileSync(path.join(pkg,'viewer/binding.json')))==='286d6b3d49acf01cdd594f6a42f46961ad0dd4258682b1e23e7c2ee045d2f970');
 const analysis=read(relative+'/results/analyze.json'),checker=read(relative+'/results/check.json');
 check('accepted saved computation',checker.passed===true&&checker.firstFailure===null&&analysis.proposalCount===12&&analysis.states.length===6);
 const generations=Object.fromEntries(['run-a','run-b'].map(run=>[run,read(prior+'/results/generation/'+run+'.json')]));
 const states=new Map(analysis.states.map(s=>[s.id,s]));
 const expectedLinks=new Map(plan.map(p=>{
  const s=states.get(p.id),r=read(prior+'/results/reference/'+p.id+'.json'),geometry=new Map(r.prepared.map(v=>[v.id,v.value]));
  const positives=new Set(r.pairs.filter(v=>v.status==='positive').map(v=>[v.i,v.r,v.j].join(':')));
  const links=s.mask.map(({i,r,j})=>({receiver:i,rotor:r,source:j,endpoints:[...geometry.get(j).center,...geometry.get(i).points[r]].map(value)}));
  check(p.id+' actual stable-ID mask is positive and exact size',links.length===Math.ceil(s.positiveTerms/10)&&links.every(v=>positives.has([v.receiver,v.rotor,v.source].join(':'))));
  return [p.id,links];
 }));
 browser=await chromium.launch({headless:true,channel:'chrome',args:['--disable-background-networking']});report.browserVersion=browser.version();
 function observe(p){p.setDefaultTimeout(4500);p.on('pageerror',e=>report.errors.push(operational(e.message,'pageerror')));p.on('console',m=>{if(m.type()==='error')report.errors.push(operational(m.text(),'console-error'));if(m.type()==='warning')report.warnings.push(operational(m.text(),'console-warning'));});p.on('request',r=>report.requests.push(r.url()));}
 page=await browser.newPage({viewport:report.viewports[0]});observe(page);
 await page.addInitScript(()=>{for(const kind of ['WebGLRenderingContext','WebGL2RenderingContext']){const proto=window[kind]?.prototype;if(!proto)continue;for(const name of ['bufferData','bufferSubData']){const original=proto[name];proto[name]=function(...args){const data=args[name==='bufferData'?1:2];if(data instanceof Float32Array&&data.length===16128*6)window.__qaOverlayUpload={calls:(window.__qaOverlayUpload?.calls||0)+1,first240:Array.from(data.slice(0,240))};return original.apply(this,args);};}const draw=proto.drawArrays;proto.drawArrays=function(mode,first,count){if(mode===1){window.__qaLineDraws??=[];window.__qaLineDraws.push(count);if(window.__qaLineDraws.length>100)window.__qaLineDraws.shift();}return draw.call(this,mode,first,count);};}});
 const frame=async()=>page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
 await page.goto(base,{waitUntil:'networkidle',timeout:10000});await page.waitForFunction(()=>window.__viewState?.validEvidence||window.__viewState?.error,null,{timeout:6000});
 check('correct page identity',page.url()===base&&(await page.title()).includes('Direct-load diagnostic'));
 check('meaningful rendered page',(await page.locator('h1').innerText()).includes('weakest tenth')&&await page.evaluate(()=>window.__viewState?.validEvidence&&window.__viewState.renderedBodyCount===64));
 check('no framework error overlay',await page.locator('vite-error-overlay,nextjs-portal').count()===0);
 check('integrity distinct from strict negative result',await page.locator('#check-status').innerText()==='Passed'&&await page.locator('#full-count').innerText()==='6 / 6 pass'&&await page.locator('#omit-count').innerText()==='0 / 6 pass');
 await page.screenshot({path:path.join(out,'desktop-first-viewport.png')});
 async function checkOverview(tier,metric,tag){
  const rows=await page.locator('#all-results tr').evaluateAll(rows=>rows.map(row=>({id:row.dataset.state,cells:Array.from(row.cells).map(c=>({status:c.dataset.status,strong:c.querySelector('strong')?.textContent,small:c.querySelector('small')?.textContent,text:c.textContent,title:c.title}))})));
  check(tag+' keeps all six rows',rows.length===6&&eq(rows.map(v=>v.id),plan.map(v=>v.id)));
  for(let n=0;n<6;n++){
   const s=analysis.states[n],full=s.proposals[0],omit=s.proposals[1],r=rows[n];
   check(tag+' '+s.id+' saved denominator',r.cells[1].text===s.mask.length+' / '+s.positiveTerms);
   const audits=[['A',full.A],['B',full.B],['A',omit.A],['B',omit.B],['C',omit.C]];
   check(tag+' '+s.id+' five audit statuses and normalized errors',audits.every(([name,a],i)=>{const c=r.cells[i+2],status=selectedTier(a,tier).overall,b=a.maxErrors[metric];return c.status===status&&c.strong===label(status,name)&&c.small===errorText(name,b)&&c.title==='Exact saved error interval: ['+b.l.n+'/'+b.l.d+', '+b.u.n+'/'+b.u.d+']';}));
  }
 }
 for(const p of plan)for(const proposal of ['full','omit10'])for(const tier of TIERS){
  await page.selectOption('#state',p.id);await page.selectOption('#proposal',proposal);await page.selectOption('#tier',tier);await page.evaluate(()=>window.__qaLineDraws=[]);await frame();
  const view=await page.evaluate(()=>window.__viewState),evidence=await page.evaluate(()=>window.__evidenceState),s=states.get(p.id),q=s.proposals.find(v=>v.id===proposal),f=generations[p.runId].frames.find(f=>f.t===p.t),expected=proposal==='full'?[]:expectedLinks.get(p.id),tag=p.id+'/'+proposal+'/'+tier;
  check(tag+' scene identity and all 64 poses',view.validEvidence&&view.stateId===p.id&&view.run===p.runId&&view.t===p.t&&view.proposal===proposal&&view.tier===tier&&view.renderedBodyCount===64&&view.positions.length===64&&view.positions.every((v,i)=>v.length===3&&v.every((x,k)=>x===Math.fround(value(f.words[7*i+k])))));
  check(tag+' exact stable-ID link endpoints/count',view.selectedLinkCount===expected.length&&view.renderedLinkCount===expected.length&&eq(view.edgeSamples,expected));
  const lineDraws=await page.evaluate(()=>window.__qaLineDraws.filter(n=>n>0&&n<=80));check(tag+' actual overlay draw counts',expected.length?lineDraws.length>0&&lineDraws.every(n=>n===2*expected.length):lineDraws.length===0);
  if(expected.length){const gpu=await page.evaluate(()=>window.__qaOverlayUpload?.first240);check(tag+' real Float32 overlay upload',gpu&&eq(gpu.slice(0,6*expected.length),expected.flatMap(v=>v.endpoints.map(Math.fround))));}
  check(tag+' six saved summary rows and same selected candidate',evidence.denominator===6&&evidence.rows.length===6&&eq(evidence.selectedAudits,Object.fromEntries((proposal==='full'?['A','B']:['A','B','C']).map(a=>[a,{maxErrors:q[a].maxErrors,tiers:q[a].tiers}]))));
  const details=await page.locator('#detail-results tr').evaluateAll(rows=>rows.map(r=>({metric:r.dataset.category,cells:Array.from(r.cells).slice(1).map(c=>({status:c.dataset.status,strong:c.querySelector('strong')?.textContent,small:c.querySelector('small')?.textContent,text:c.textContent}))})));
  check(tag+' all four category decisions and errors',details.length===4&&details.every((r,n)=>r.metric===METRICS[n]&&['A','B','C'].every((a,k)=>{const c=r.cells[k];if(a==='C'&&proposal==='full')return c.status===undefined&&c.text.includes('Not applicable');const status=selectedTier(q[a],tier).categories[r.metric];return c.status===status&&c.strong===label(status,a)&&c.small===errorText(a,q[a].maxErrors[r.metric]);})));
  check(tag+' B/C never labeled actual failure',await page.locator('#detail-results td[data-audit="B"], #detail-results td[data-audit="C"]').evaluateAll(cells=>cells.every(c=>c.dataset.status==='pass'||c.dataset.status==='not-certified')));
  report.combinations.push({id:p.id,proposal,tier,bodyPositionsChecked:64,links:expected.length});report.renderedSnapshots++;report.renderedBodies+=64;report.renderedCenterComponents+=192;report.renderedLinkEndpoints+=expected.length*2;
 }
 check('all 36 state/candidate/tier combinations complete',report.combinations.length===36);
 for(const tier of TIERS)for(const metric of METRICS){await page.selectOption('#tier',tier);await page.selectOption('#category',metric);await checkOverview(tier,metric,'overview/'+tier+'/'+metric);report.overviewProjections.push({tier,metric,states:6});}
 check('all 12 category/tier overview projections complete',report.overviewProjections.length===12);
 await page.selectOption('#category','rotor');await page.selectOption('#tier','1e-8');await page.locator('#all-title').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'desktop-strict-overview.png')});
 check('strict overview retains all six A failures',await page.locator('#all-results tr').evaluateAll(rows=>rows.every(r=>r.cells[4].dataset.status==='definite-fail')));
 await page.selectOption('#tier','1e-2');await page.locator('#all-title').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'desktop-stress-overview.png')});
 check('stress retains A0 B0 failures and four A passes',eq(await page.locator('#all-results tr').evaluateAll(rows=>rows.map(r=>r.cells[4].dataset.status)),['definite-fail','pass','pass','definite-fail','pass','pass']));
 check('B/C stress certify only A10 B10',await page.locator('#all-results tr').evaluateAll(rows=>rows.every((r,i)=>r.cells[5].dataset.status===([2,5].includes(i)?'pass':'not-certified')&&r.cells[6].dataset.status===r.cells[5].dataset.status)));
 await page.locator('#detail-title').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'desktop-selected-errors.png')});
 await page.locator('#overlays').uncheck();await frame();check('overlay toggle hides geometry but preserves mask',await page.evaluate(()=>window.__viewState.renderedLinkCount===0&&window.__viewState.selectedLinkCount===17));await page.locator('#overlays').check();await frame();check('overlay restoration',await page.evaluate(()=>window.__viewState.renderedLinkCount===17));
 await page.selectOption('#proposal','full');await frame();check('full control clears omitted geometry and C',await page.evaluate(()=>window.__viewState.renderedLinkCount===0&&window.__viewState.selectedLinkCount===0)&&await page.locator('#detail-results td').filter({hasText:'Not applicable'}).count()===4);
 await page.selectOption('#proposal','omit10');await page.locator('#all-results tr').first().locator('button').click();await frame();check('table button switches snapshot and exact mask',await page.evaluate(()=>window.__viewState.stateId==='run-a-t0'&&window.__viewState.t===0&&window.__viewState.renderedLinkCount===39));
 await page.selectOption('#state','run-b-t10');await frame();
 const canvas=page.locator('#scene canvas');await canvas.scrollIntoViewIfNeeded();await page.waitForTimeout(180);const box=await canvas.boundingBox();check('meaningful visible canvas',box&&box.width>300&&box.height>300);
 const initial=await canvas.screenshot({path:path.join(out,'controls-before.png')});await page.mouse.move(box.x+box.width*.5,box.y+box.height*.5);await page.mouse.down();await page.mouse.move(box.x+box.width*.69,box.y+box.height*.62,{steps:12});await page.mouse.up();await page.waitForTimeout(650);const orbit=await canvas.screenshot({path:path.join(out,'controls-orbit.png')});check('orbit changes rendered pixels',sha(initial)!==sha(orbit));
 await page.mouse.wheel(0,-180);await page.waitForTimeout(650);const zoom=await canvas.screenshot({path:path.join(out,'controls-zoom.png')});check('zoom changes rendered pixels',sha(orbit)!==sha(zoom));await page.locator('#reset').click();await canvas.scrollIntoViewIfNeeded();await page.waitForTimeout(650);const reset=await canvas.screenshot({path:path.join(out,'controls-reset.png')});check('reset restores exact original canvas',sha(initial)===sha(reset));await page.screenshot({path:path.join(out,'desktop-selected-overlay.png')});
 check('desktop page has no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.setViewportSize(report.viewports[1]);await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(180);await page.screenshot({path:path.join(out,'mobile-first-viewport.png')});await page.locator('.visual').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'mobile-overlay.png')});
 await page.selectOption('#state','run-a-t5');await page.selectOption('#proposal','full');await page.selectOption('#tier','1e-4');await frame();check('mobile controls retain recorded pose and zero-deletion control',await page.evaluate(()=>window.__viewState.stateId==='run-a-t5'&&window.__viewState.t===5&&window.__viewState.renderedBodyCount===64&&window.__viewState.renderedLinkCount===0));
 await page.selectOption('#proposal','omit10');await page.selectOption('#tier','1e-2');await page.selectOption('#category','worldMoment');await checkOverview('1e-2','worldMoment','mobile-overview');
 await page.locator('#all-title').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'mobile-table-left.png')});const table=page.locator('#overview').locator('..');await table.evaluate(e=>e.scrollLeft=e.scrollWidth);await page.waitForTimeout(180);await page.screenshot({path:path.join(out,'mobile-table-right.png')});check('mobile table scroll retains all six rows',await table.evaluate(e=>e.scrollLeft>0&&e.scrollWidth>e.clientWidth&&e.querySelectorAll('tbody tr').length===6));check('mobile page has no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 for(const resource of ['binding.json','display-data.json']){
  const p=await browser.newPage({viewport:report.viewports[0]});observe(p);await p.route(new URL(resource,base).href,r=>r.fulfill({status:200,contentType:'application/json',body:'{}'}));await p.goto(base,{waitUntil:'networkidle',timeout:8000});await p.waitForFunction(()=>window.__viewState?.validEvidence===false,null,{timeout:4000});
  check('corrupt '+resource+' withdraws all claims and geometry',await p.locator('#all-results tr').count()===6&&await p.locator('#all-results td').filter({hasText:'Not bound'}).count()===36&&await p.locator('#detail-results tr').count()===4&&await p.locator('#detail-results td').filter({hasText:'Not bound'}).count()===12&&await p.locator('#check-status').innerText()==='Not bound'&&await p.locator('#full-count').innerText()==='— / 6'&&await p.locator('#omit-count').innerText()==='— / 6'&&await p.locator('#scene canvas:visible').count()===0&&await p.locator('#state,#proposal,#tier,#category,#overlays,#reset').evaluateAll(cs=>cs.every(c=>c.disabled)));
  await p.screenshot({path:path.join(out,'corrupt-'+resource.replace('.json','')+'.png')});await p.close();
 }
 check('no console or page errors',report.errors.length===0,report.errors);check('no console warnings',report.warnings.length===0,report.warnings);check('browser requests only local display assets',report.requests.every(u=>u.startsWith('http://localhost:8876/')&&!u.includes('/source/')&&!u.includes('/results/')));
 report.passed=true;
}catch(e){report.passed=false;report.failure=operational(e.message,'attempt-failure');try{await page?.screenshot({path:path.join(out,'failure.png')});}catch(_){}
}finally{
 try{await browser?.close();}catch(_){}
 try{const after=immutable();fs.writeFileSync(path.join(out,'immutable-after.json'),JSON.stringify(after,null,2)+'\n');check('all 159 frozen pins and four accepted results preserved',eq(before,after));report.preservationPassed=true;}catch(e){report.passed=false;report.preservationPassed=false;report.preservationFailure=operational(e.message,'preservation-failure');}
 clearTimeout(stop);clearTimeout(hard);persist();console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,combinations:report.combinations.length,overviewProjections:report.overviewProjections.length,centerComponents:report.renderedCenterComponents,linkEndpoints:report.renderedLinkEndpoints,wallMs:report.wallMs,preservation:report.preservationPassed,failure:report.failure}));if(!report.passed||!report.within60Seconds)process.exitCode=1;
}})();
