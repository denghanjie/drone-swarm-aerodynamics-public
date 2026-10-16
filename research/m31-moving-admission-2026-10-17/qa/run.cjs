'use strict';
// Display QA only. No scientific imports or force evaluations.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),{chromium}=require('playwright');
const root=process.env.RESEARCH_ROOT,out=process.env.RESEARCH_QA_OUTPUT;
if(!root||!out)throw Error('Missing display paths');fs.mkdirSync(out,{recursive:false});
const pkg=path.join(root,'research/m31-moving-admission-2026-10-17'),base='http://127.0.0.1:8876/research/m31-moving-admission-2026-10-17/viewer/';
const binding=JSON.parse(fs.readFileSync(path.join(pkg,'viewer/binding.json')));
const report={scope:'Saved-evidence display verification only',checks:[],errors:[],warnings:[],renderedCenterComponents:0};
const check=(name,passed)=>{report.checks.push({name,passed:!!passed});if(!passed)throw Error(name);};
const start=Date.now();let browser;const deadline=setTimeout(()=>{if(browser)browser.close().catch(()=>{});},59000);
(async()=>{try{
 browser=await chromium.launch({executablePath:process.env.RESEARCH_CHROME,headless:true,args:['--disable-background-networking']});report.browserVersion=browser.version();
 const page=await browser.newPage({viewport:{width:1440,height:1050}});
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());if(m.type()==='warning')report.warnings.push(m.text());});
 await page.goto(base,{waitUntil:'networkidle',timeout:20000});await page.waitForFunction(()=>window.__viewState?.validEvidence,null,{timeout:15000});
 check('six scheduled rows',await page.locator('#all-results tr').count()===6);
 check('scope disclosure',(await page.locator('body').innerText()).includes('airflow off'));
 for(const [id,relative] of Object.entries(binding.generationPaths)){
  const g=JSON.parse(fs.readFileSync(path.join(root,relative)));await page.selectOption('#run',id);
  for(let f=0;f<g.frames.length;f++){
   await page.locator('#frame').evaluate((el,x)=>{el.value=String(x);el.dispatchEvent(new Event('input'));},f);
   const state=await page.evaluate(()=>window.__viewState);
   check(id+' frame '+f+' identity',state.validEvidence&&state.run===id&&state.frame===f&&state.bodyCount===64&&state.t===g.frames[f].t);
   check(id+' frame '+f+' all rendered centers',state.positions.every((p,i)=>p.every((v,k)=>v===Math.fround(Buffer.from(g.frames[f].words[7*i+k],'hex').readDoubleBE()))));report.renderedCenterComponents+=64*3;
  }
 }
 await page.selectOption('#run','run-a');await page.locator('#frame').evaluate(el=>{el.value='25';el.dispatchEvent(new Event('input'));});
 await page.screenshot({path:path.join(out,'desktop.png'),fullPage:true});
 await page.locator('#play').click();await page.waitForFunction(()=>window.__viewState.frame>25,null,{timeout:3000});await page.locator('#play').click();check('playback advances',(await page.evaluate(()=>window.__viewState.frame))>25);
 const canvas=page.locator('#scene canvas');await canvas.scrollIntoViewIfNeeded();const box=await canvas.boundingBox();check('visible WebGL canvas',box&&box.width>250&&box.height>250);
 const before=await page.evaluate(()=>window.__viewState.camera);await page.mouse.move(box.x+box.width*.5,box.y+box.height*.5);await page.mouse.down();await page.mouse.move(box.x+box.width*.68,box.y+box.height*.62,{steps:10});await page.mouse.up();
 await page.waitForFunction(b=>JSON.stringify(window.__viewState.camera)!==JSON.stringify(b),before,{timeout:2000});check('orbit responds',true);await page.locator('#reset').click();
 for(const href of await page.locator('a').evaluateAll(es=>es.map(e=>e.href))){const res=await page.request.get(href);check('link '+new URL(href).pathname,res.ok());}
 await page.setViewportSize({width:390,height:844});await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});check('mobile overflow absent',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));check('mobile canvas visible',await canvas.isVisible());
 check('no browser errors',report.errors.length===0);check('no browser warnings',report.warnings.length===0);
 const resources=['binding.json','../results/check.json','../results/index.json','../results/generation/run-a.json'];
 for(const resource of resources){const p=await browser.newPage();await p.route(new URL(resource,base).href,r=>r.fulfill({status:200,contentType:'application/json',body:'{}'}));await p.goto(base,{waitUntil:'networkidle',timeout:10000});await p.waitForFunction(()=>window.__viewState?.validEvidence===false,null,{timeout:5000});check('corrupt '+resource+' hides replay and claims',await p.locator('#scene').isHidden()&&await p.locator('#all-results tr').count()===0&&await p.locator('#play').isDisabled());await p.close();}
 report.passed=true;
}catch(e){report.passed=false;report.failure=e.message;}finally{if(browser)await browser.close();clearTimeout(deadline);report.wallMs=Date.now()-start;report.within60Seconds=report.wallMs<=60000;fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,renderedCenterComponents:report.renderedCenterComponents,wallMs:report.wallMs,failure:report.failure}));if(!report.passed||!report.within60Seconds)process.exitCode=1;}})();
