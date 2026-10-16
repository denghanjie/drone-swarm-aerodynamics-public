'use strict';
// Display only: no qualification or scientific code imports.
const fs=require('node:fs'),path=require('node:path'),{chromium}=require('playwright');
const out=process.env.RESEARCH_QA_OUTPUT;fs.mkdirSync(out,{recursive:false});
const base='http://127.0.0.1:8876/research/m31-launch-qualification-2026-10-17/viewer/';
const report={scope:'Source-only status and historical UI checks',browserAvailability:'Browser plugin not available; existing Playwright fallback',checks:[],errors:[],warnings:[]};
const check=(name,p)=>{report.checks.push({name,passed:!!p});if(!p)throw Error(name);};let browser;const start=Date.now();const timer=setTimeout(()=>browser?.close().catch(()=>{}),59000);
(async()=>{try{
 browser=await chromium.launch({executablePath:process.env.RESEARCH_CHROME,headless:true,args:['--disable-background-networking']});report.browserVersion=browser.version();const page=await browser.newPage({viewport:{width:1440,height:1050}});
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());if(m.type()==='warning')report.warnings.push(m.text());});
 await page.goto(base,{waitUntil:'networkidle',timeout:15000});await page.waitForFunction(()=>window.__statusView?.validEvidence,null,{timeout:5000});
 check('page identity',page.url()===base&&(await page.title())==='Launch qualification · source only');check('not blank',await page.locator('h1').isVisible());check('no overlay',await page.locator('vite-error-overlay,nextjs-portal').count()===0);
 check('source and runtime outcomes separated',JSON.stringify(await page.locator('strong').allTextContents())===JSON.stringify(['ACCEPTED','NOT RUN','NONE']));check('eight planned cases',await page.locator('#cases tr').count()===8);check('all eight unexecuted',(await page.locator('#cases tr td:last-child').allTextContents()).every(x=>x==='NOT RUN'));
 check('deadline explanation',(await page.locator('#timing').innerText()).includes('07:11:53'));check('historical disclosure',(await page.locator('.history').innerText()).includes('HISTORICAL 3D REPLAY · NO NEW FLIGHT'));
 const frame=await page.locator('#historical').elementHandle().then(x=>x.contentFrame());await frame.waitForFunction(()=>window.__viewState?.validEvidence,null,{timeout:10000});
 await frame.selectOption('#run','run-b');await frame.locator('#frame').evaluate(e=>{e.value='25';e.dispatchEvent(new Event('input'));});let state=await frame.evaluate(()=>window.__viewState);check('historical run and scrub respond',state.run==='run-b'&&state.frame===25&&state.t===5&&state.bodyCount===64);
 await page.screenshot({path:path.join(out,'desktop.png'),fullPage:true});await frame.locator('#play').click();await frame.waitForFunction(()=>window.__viewState.frame>25,null,{timeout:2000});await frame.locator('#play').click();check('historical playback responds',true);
 for(const url of await page.locator('a').evaluateAll(es=>es.map(e=>e.href)))check('link '+new URL(url).pathname,(await page.request.get(url)).ok());
 await page.setViewportSize({width:390,height:844});await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});check('mobile no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));check('iframe no horizontal overflow',await frame.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));check('mobile canvas visible',await frame.locator('#scene canvas').isVisible());
 check('no errors',report.errors.length===0);check('no warnings',report.warnings.length===0);
 for(const name of ['binding.json','../UNEXECUTED-STATUS.json','../source-publication.json','../../m31-validator-qualification-2026-10-17/viewer/binding.json']){
 const p=await browser.newPage();await p.route(new URL(name,base).href,r=>r.fulfill({status:200,contentType:'application/json',body:'{}'}));await p.goto(base,{waitUntil:'networkidle',timeout:7000});await p.waitForFunction(()=>window.__statusView?.validEvidence===false,null,{timeout:3000});check('corrupt '+name+' hides details/replay',await p.locator('#facts').isHidden()&&await p.locator('#historical').getAttribute('src')===null);await p.close();}
 report.passed=true;
}catch(e){report.passed=false;report.failure=e.message;}finally{if(browser)await browser.close();clearTimeout(timer);report.wallMs=Date.now()-start;report.within60Seconds=report.wallMs<=60000;fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,wallMs:report.wallMs,failure:report.failure}));if(!report.passed||!report.within60Seconds)process.exitCode=1;}})();
