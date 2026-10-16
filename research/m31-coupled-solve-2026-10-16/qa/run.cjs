const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const base='http://127.0.0.1:8876/research/m31-coupled-solve-2026-10-16/viewer/';
const out=process.env.RESEARCH_QA_OUTPUT;fs.mkdirSync(out,{recursive:true});
let browser;const report={flow:'Load saved-evidence viewer, select all arrangements, replay updates, inspect rejected state and mobile layout.',browserPath:'Browser plugin not available; installed Playwright and Chrome used.',checks:[],errors:[],warnings:[]};
function check(name,value){report.checks.push({name,passed:!!value});assert.ok(value,name);}
async function main(){
 browser=await chromium.launch({executablePath:process.env.RESEARCH_CHROME,headless:true});report.browserVersion=browser.version();
 const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});page.setDefaultTimeout(8000);
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());if(m.type()==='warning')report.warnings.push(m.text());});page.on('response',r=>{if(r.status()>=400)report.errors.push(String(r.status())+' '+r.url());});
 await page.goto(base);await page.locator('body[data-binding="verified"]').waitFor();await page.locator('#scene canvas').waitFor();
 check('page identity',page.url()===base&&(await page.title())==='Coupled drone loads · M31');
 check('meaningful nonblank page',(await page.locator('h1').innerText()).includes('coupled drone loads'));
 check('no framework error overlay',await page.locator('vite-error-overlay, nextjs-portal').count()===0);
 check('independent review displayed',(await page.locator('#review').innerText())==='Passed'&&(await page.locator('#review-detail').innerText()).includes('10007 checks'));
 check('explicit replay scope',(await page.locator('.notice').innerText()).includes('recorded steady-solver replay'));
 check('ordered work from saved record',(await page.locator('#work').innerText())==='32 / 32');
 await page.screenshot({path:path.join(out,'desktop.png'),fullPage:true});
 await page.locator('#play').click();await page.waitForFunction(()=>Number(document.getElementById('step').value)>=1&&Number(document.getElementById('step').value)<8);
 await page.locator('#play').click();check('replay changes saved step',Number(await page.locator('#step').inputValue())>=1&&Number(await page.locator('#step').inputValue())<8);
 await page.locator('#final').click();check('final control returns terminal step',(await page.locator('#step').inputValue())==='8');
 await page.locator('#case').selectOption('tilted-ladder');check('tilted selection updates scene',await page.locator('#scene').getAttribute('data-case')==='tilted-ladder');check('eight rows retained',await page.locator('#rows tr').count()===8);
 await page.locator('#case').selectOption('hexagon-cycle');check('cycle selection updates scene',await page.locator('#scene').getAttribute('data-case')==='hexagon-cycle');check('cycle displays ineligible direct solve',(await page.locator('#iter-detail').innerText()).includes('Ordered solve: ineligible'));
 await page.locator('#scene').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'cycle.png')});
 await page.locator('#reset').click();check('camera reset retains selected case',await page.locator('#case').inputValue()==='hexagon-cycle');
 await page.locator('#case').selectOption('near-rejection');check('rejected state disables solve replay',await page.locator('#play').isDisabled()&&await page.locator('#step').isDisabled());check('rejection counts retained',(await page.locator('#case-detail').innerText()).includes('6 admission errors'));check('rejected state has two table rows',await page.locator('#rows tr').count()===2);
 await page.screenshot({path:path.join(out,'near.png')});
 await page.setViewportSize({width:390,height:844});await page.locator('#case').selectOption('level-ladder');await page.evaluate(()=>window.scrollTo(0,0));await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
 check('mobile no horizontal document overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1));await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});
 await page.locator('#scene').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'mobile-scene.png')});
 const hrefs=await page.locator('a').evaluateAll(a=>a.map(x=>x.href));for(const url of hrefs){const response=await page.request.get(url);check('link '+url.split('/').slice(-1)[0],response.ok());}
 check('console and HTTP health',report.errors.length===0);report.passed=true;
}
main().catch(e=>{report.passed=false;report.failure=e.message;process.exitCode=1;}).finally(async()=>{await browser?.close();fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));});
