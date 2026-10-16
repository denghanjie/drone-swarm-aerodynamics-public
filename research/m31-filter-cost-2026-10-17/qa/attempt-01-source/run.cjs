'use strict';
// Display-only, saved JSON and browser UI. Never import a scientific module.
const fs=require('node:fs'),path=require('node:path'),{chromium}=require('playwright');
const root=process.env.RESEARCH_ROOT,out=process.env.RESEARCH_QA_OUTPUT,chrome=process.env.RESEARCH_CHROME;
if(!root||!out||!chrome)throw Error('Local display paths required');
fs.mkdirSync(out,{recursive:false});
const pkg=path.join(root,'research/m31-filter-cost-2026-10-17');
const raw=JSON.parse(fs.readFileSync(path.join(pkg,'results/timing-index.json'),'utf8'));
const base='http://127.0.0.1:8876/research/m31-filter-cost-2026-10-17/viewer/';
const report={scope:'Display-only saved group/timing evidence; no scientific calls.',flow:'Verified checkpoint loads; six group selections and receiver/rotor controls update saved geometry and counts; orbit responds; corrupted evidence hides claims.',browserAvailability:'Browser plugin not available; installed Playwright/Chrome fallback',checks:[],errors:[],warnings:[]};
const start=Date.now();let browser,page;
const check=(name,passed)=>{report.checks.push({name,passed:!!passed});if(!passed)throw Error(name);};
const deadline=setTimeout(()=>{if(browser)browser.close().catch(()=>{});},60000);
(async()=>{try{
 browser=await chromium.launch({executablePath:chrome,headless:true,args:['--disable-background-networking']});report.browserVersion=browser.version();
 page=await browser.newPage({viewport:{width:1440,height:1050}});
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());if(m.type()==='warning')report.warnings.push(m.text());});
 await page.goto(base,{waitUntil:'networkidle',timeout:25000});await page.waitForFunction(()=>document.body.dataset.binding==='verified',null,{timeout:25000});
 check('page identity',page.url()===base&&(await page.title()).includes('filter save time'));
 check('meaningful content',(await page.locator('h1').innerText()).includes('shortcut'));
 check('no framework overlay',await page.locator('vite-error-overlay,nextjs-portal').count()===0);
 check('numerical qualification visible',await page.locator('body').getAttribute('data-qualification')==='passed');
 check('six table rows',await page.locator('#timings tr').count()===6);
 check('60 calls visible',(await page.locator('#trials-count').innerText()).includes('60'));
 check('18 controls visible',(await page.locator('#controls-count').innerText()).includes('18 / 18'));
 check('practical gate agrees',(await page.locator('#benefit').innerText()).includes(raw.primaryBenefitPassed?'passed':'missed'));
 check('static scope disclosure',(await page.locator('body').innerText()).includes('does not simulate flight'));
 for(const [si,s] of raw.scenes.entries()){
  const saved=JSON.parse(fs.readFileSync(path.join(pkg,s.path),'utf8')),m=saved.methods[1];
  await page.selectOption('#group-case',s.id);await page.waitForFunction(id=>document.body.dataset.sceneReady===id,s.id,{timeout:15000});
  check(s.id+' drone count',Number(await page.locator('#pair-canvas').getAttribute('data-drones'))===saved.input.drones.length);
  const centers=m.prepared.map(d=>({id:d.id,position:d.value.center.map(b=>Buffer.from(b,'hex').readDoubleBE())})),origin=[0,1,2].map(k=>(Math.min(...centers.map(d=>d.position[k]))+Math.max(...centers.map(d=>d.position[k])))*.5);
  const visible=await page.evaluate(()=>window.__m31VisibleCenters());check(s.id+' all rendered center components',visible.length===centers.length&&visible.every((d,i)=>d.id===centers[i].id&&d.position.every((v,k)=>v===centers[i].position[k]-origin[k])));
  for(const [i,r] of [[0,0],[saved.input.drones.length-1,3]]){
   await page.selectOption('#receiver',String(i));await page.selectOption('#rotor',String(r));
   const q=m.assembly.queries.find(q=>q.i===i&&q.r===r),f=q.terminals.reduce((n,t)=>n+(t.filterZeros??[]).length,0),e=q.terminals.reduce((n,t)=>n+(t.entries??[]).filter(e=>e.result.status==='positive').length,0),z=q.terminals.filter(t=>t.kind==='zero');
   check(s.id+' receiver '+i+' rotor '+r,Number(await page.locator('#pair-canvas').getAttribute('data-receiver'))===i&&Number(await page.locator('#pair-canvas').getAttribute('data-rotor'))===r);
   check(s.id+' fast zeros '+i,Number(await page.locator('#pair-canvas').getAttribute('data-fast-zeros'))===f);
   check(s.id+' positive links '+i,Number(await page.locator('#pair-canvas').getAttribute('data-visible-edges'))===e);
   check(s.id+' hierarchy coverage '+i,Number(await page.locator('#pair-canvas').getAttribute('data-pruned'))===z.reduce((n,t)=>n+t.count,0));
  }
  const summary=raw.summaries[si],row=await page.locator('#timings tr').nth(si).innerText();
  check(s.id+' timing ratio',row.includes((Number(summary.medianPairedRatio.n)/Number(summary.medianPairedRatio.d)).toFixed(3)+'×'));
 }
 await page.selectOption('#group-case',raw.scenes[0].id);await page.waitForFunction(id=>document.body.dataset.sceneReady===id,raw.scenes[0].id);await page.screenshot({path:path.join(out,'desktop.png'),fullPage:false});
 await page.locator('#pair-canvas').scrollIntoViewIfNeeded();const canvas=page.locator('#pair-canvas canvas'),b=await canvas.boundingBox();check('Three.js canvas visible',b&&b.width>200&&b.height>250);
 const before=await page.locator('#pair-canvas').getAttribute('data-camera');await page.mouse.move(b.x+b.width*.5,b.y+b.height*.5);await page.mouse.down();await page.mouse.move(b.x+b.width*.65,b.y+b.height*.58,{steps:12});await page.mouse.up();
 check('orbit camera responds',before!==await page.locator('#pair-canvas').getAttribute('data-camera'));await page.screenshot({path:path.join(out,'group.png'),fullPage:false});
 for(const href of await page.locator('a').evaluateAll(xs=>xs.map(a=>a.href))){const r=await page.request.get(href);check('link '+new URL(href).pathname,r.ok());}
 await page.setViewportSize({width:390,height:844});await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:path.join(out,'mobile.png'),fullPage:false});
 check('mobile no horizontal page overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.locator('#pair-canvas').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'mobile-group.png'),fullPage:false});
 check('mobile canvas',await canvas.isVisible());
 check('no display errors',report.errors.length===0);check('no display warnings',report.warnings.length===0);
 for(const resource of ['binding.json','../results/timing-index.json','../results/independent-check.json','../'+raw.scenes[0].path]){
  const p=await browser.newPage(),url=new URL(resource,base).href;
  await p.route(url,route=>route.fulfill({status:200,contentType:'application/json',body:'{}'}));
  await p.goto(base,{waitUntil:'networkidle',timeout:15000});await p.waitForFunction(()=>document.body.dataset.binding==='failed',null,{timeout:15000});
  check('corrupt '+resource+' hides claims',await p.locator('#content').isHidden()&&(await p.locator('#status').innerText()).includes('stopped'));await p.close();
 }
 report.passed=true;
}catch(e){report.passed=false;report.failure=String(e.message).replaceAll(root,'REPOSITORY_ROOT').replaceAll(out,'QA_OUTPUT');if(page)await page.screenshot({path:path.join(out,'failure.png'),fullPage:false}).catch(()=>{});
}finally{clearTimeout(deadline);if(browser)await browser.close();report.wallSeconds=(Date.now()-start)/1000;fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,wallSeconds:report.wallSeconds,failure:report.failure}));if(!report.passed)process.exitCode=1;}})();
