'use strict';
// Display verification only. No scientific imports or new calculations.
const fs=require('node:fs'),path=require('node:path'),{chromium}=require('playwright');
const root=process.env.RESEARCH_ROOT,out=process.env.RESEARCH_QA_OUTPUT;
if(!root||!out)throw Error('Missing paths');fs.mkdirSync(out,{recursive:false});
const base='http://127.0.0.1:8876/research/m31-normalizer-ablation-2026-10-17/viewer/';
const historic=JSON.parse(fs.readFileSync(path.join(root,'research/m31-validator-qualification-2026-10-17/viewer/binding.json')));
const report={scope:'Failed-launch display and historical recorded-pose QA only',browserAvailability:'Browser plugin not available; existing Playwright fallback',flow:'Status page -> historical run selection/scrub/play/orbit -> truthful statuses and matching saved poses',checks:[],errors:[],warnings:[],renderedCenterComponents:0};
const check=(name,pass)=>{report.checks.push({name,passed:!!pass});if(!pass)throw Error(name);};let browser;const start=Date.now();
const timer=setTimeout(()=>{if(browser)browser.close().catch(()=>{});},59000);
(async()=>{try{
 browser=await chromium.launch({executablePath:process.env.RESEARCH_CHROME,headless:true,args:['--disable-background-networking']});report.browserVersion=browser.version();
 const page=await browser.newPage({viewport:{width:1440,height:1050}});
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());if(m.type()==='warning')report.warnings.push(m.text());});
 await page.goto(base,{waitUntil:'networkidle',timeout:15000});await page.waitForFunction(()=>window.__failureView?.validEvidence,null,{timeout:5000});
 check('page identity',page.url()===base&&(await page.title())==='Normalizer ablation · failed launch');
 check('not blank',await page.locator('h1').isVisible());check('no framework overlay',await page.locator('vite-error-overlay,nextjs-portal').count()===0);
 check('failed launch visible',(await page.locator('#notice').innerText()).includes('failed launch'));
 check('scientific gates untested',await page.locator('strong').allTextContents().then(x=>JSON.stringify(x)===JSON.stringify(['FAILED','UNTESTED','UNTESTED'])));
 check('historical distinction',(await page.locator('.history').innerText()).includes('HISTORICAL 3D REPLAY · NOT THIS ATTEMPT'));
 const frame=await page.locator('#historical').elementHandle().then(x=>x.contentFrame());await frame.waitForFunction(()=>window.__viewState?.validEvidence,null,{timeout:10000});
 for(const [id,relative]of Object.entries(historic.generationPaths)){
  const g=JSON.parse(fs.readFileSync(path.join(root,relative)));await frame.selectOption('#run',id);
  for(let i=0;i<g.frames.length;i++){
   await frame.locator('#frame').evaluate((e,x)=>{e.value=String(x);e.dispatchEvent(new Event('input'));},i);const s=await frame.evaluate(()=>window.__viewState);
   check(id+' '+i+' identity',s.validEvidence&&s.run===id&&s.frame===i&&s.t===g.frames[i].t&&s.bodyCount===64);
   check(id+' '+i+' recorded centers',s.positions.every((p,j)=>p.every((x,k)=>x===Math.fround(Buffer.from(g.frames[i].words[7*j+k],'hex').readDoubleBE()))));report.renderedCenterComponents+=192;
  }
 }
 await frame.selectOption('#run','run-a');await frame.locator('#frame').evaluate(e=>{e.value='25';e.dispatchEvent(new Event('input'));});
 await page.screenshot({path:path.join(out,'desktop.png'),fullPage:true});
 await frame.locator('#play').click();await frame.waitForFunction(()=>window.__viewState.frame>25,null,{timeout:2000});await frame.locator('#play').click();check('historical playback advances',true);
 const canvas=frame.locator('#scene canvas');await canvas.scrollIntoViewIfNeeded();const box=await canvas.boundingBox();check('WebGL visible',box&&box.width>250&&box.height>250);
 const before=await frame.evaluate(()=>window.__viewState.camera);await page.mouse.move(box.x+box.width*.5,box.y+box.height*.5);await page.mouse.down();await page.mouse.move(box.x+box.width*.7,box.y+box.height*.65,{steps:8});await page.mouse.up();await frame.waitForFunction(b=>JSON.stringify(window.__viewState.camera)!==JSON.stringify(b),before,{timeout:2000});check('orbit changes view',true);await frame.locator('#reset').click();
 for(const url of await page.locator('a').evaluateAll(es=>es.map(e=>e.href)))check('link '+new URL(url).pathname,(await page.request.get(url)).ok());
 await page.setViewportSize({width:390,height:844});await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});
 check('mobile main no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));check('mobile iframe no horizontal overflow',await frame.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));check('mobile canvas visible',await canvas.isVisible());
 check('no application errors',report.errors.length===0);check('no browser warnings',report.warnings.length===0);
 for(const resource of ['binding.json','../results/kernel-supervision.json','../results/kernel-attempt.json','../source-publication.json','../../m31-validator-qualification-2026-10-17/viewer/binding.json']){
  const p=await browser.newPage();await p.route(new URL(resource,base).href,r=>r.fulfill({status:200,contentType:'application/json',body:'{}'}));await p.goto(base,{waitUntil:'networkidle',timeout:7000});await p.waitForFunction(()=>window.__failureView?.validEvidence===false,null,{timeout:3000});check('corrupt '+resource+' hides claims/replay',await p.locator('#facts').isHidden()&&await p.locator('#historical').getAttribute('src')===null);await p.close();
 }
 report.passed=true;
}catch(e){report.passed=false;report.failure=e.message;}finally{if(browser)await browser.close();clearTimeout(timer);report.wallMs=Date.now()-start;report.within60Seconds=report.wallMs<=60000;fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,renderedCenterComponents:report.renderedCenterComponents,wallMs:report.wallMs,failure:report.failure}));if(!report.passed||!report.within60Seconds)process.exitCode=1;}})();
