const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const url='http://127.0.0.1:8876/research/m31-current-bound-design-2026-10-16/viewer/';
const out=process.env.RESEARCH_QA_OUTPUT;fs.mkdirSync(out,{recursive:true});
const report={scope:'Display-only wrapper QA; unchanged historical Three.js replay. No science rerun or new target-array analysis.',checks:[],errors:[],warnings:[]};let browser;
function check(name,v){report.checks.push({name,passed:!!v});assert.ok(v,name);}
async function waitReady(p){await p.goto(url);await p.locator('body[data-binding=verified]').waitFor({timeout:60000});}
async function main(){
 browser=await chromium.launch({executablePath:process.env.RESEARCH_CHROME,headless:true});report.browserVersion=browser.version();
 const p=await browser.newPage({viewport:{width:1440,height:1050},deviceScaleFactor:1});p.on('pageerror',e=>report.errors.push(e.message));p.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());if(m.type()==='warning')report.warnings.push(m.text());});
 await waitReady(p);const f=p.frameLocator('#replay');
 check('design-only disclosure',(await p.locator('.notice').innerText()).includes('No new simulation or benchmark'));
 check('airflow off disclosed',(await p.locator('#replay-section').innerText()).includes('airflow off'));
 check('native guarantee remains open',(await p.locator('.reading').innerText()).includes('separate targets'));
 check('timing correction visible',(await p.locator('.correction').innerText()).includes('already excluded'));
 check('historical renderer visible',await f.locator('#scene canvas').isVisible());
 check('initial5000 actual record',await f.locator('#scene').getAttribute('data-instances')==='5000');
 await p.screenshot({path:path.join(out,'desktop.png'),fullPage:true});
 await p.locator('#focus-scene').click();await p.locator('#replay').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,'swarm.png')});
 for(const [id,n] of [['n1000-s261701-t5',1000],['n5000-s261702-t5',5000],['n5000-s261703-t5',5000]]){
  await f.locator('#case').selectOption(id);await f.locator('#scene[data-case="'+id+'"]').waitFor();check(id+' original instance count',await f.locator('#scene').getAttribute('data-instances')===String(n));
 }
 await f.locator('#frame').fill('0');await f.locator('#frame').dispatchEvent('input');check('scrub retains original control',await f.locator('#time').innerText()==='0.0 s');
 await f.locator('#play').click();await f.locator('body[data-playing=true]').waitFor();await f.locator('#scene:not([data-frame="0"])').waitFor();check('historical playback advances',Number(await f.locator('#scene').getAttribute('data-frame'))>0);await f.locator('#play').click();check('pause works',await f.locator('body').getAttribute('data-playing')==='false');
 await f.locator('#size').selectOption('1');check('display scale retained',await f.locator('#scene').getAttribute('data-size')==='1');await f.locator('#size').selectOption('4');await f.locator('#reset').click();
 await p.locator('details>summary').click();for(const href of await p.locator('a').evaluateAll(xs=>xs.map(x=>x.href))){check('link '+href.split('/').at(-1),(await p.request.get(href)).ok());}
 await p.setViewportSize({width:390,height:844});await p.evaluate(()=>window.scrollTo(0,0));check('mobile outer layout fits',await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));check('mobile historical layout fits',await f.locator('html').evaluate(e=>e.scrollWidth<=e.ownerDocument.defaultView.innerWidth+1));await p.screenshot({path:path.join(out,'mobile.png'),fullPage:true});await p.locator('#focus-scene').click();await p.locator('#replay').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,'mobile-swarm.png')});
 check('no normal-page errors',report.errors.length===0);check('no normal-page warnings',report.warnings.length===0);
 // Display faults only: no scientific code execution. Preserve each outcome.
 for(const fault of ['binding-corruption','design-corruption','historical-asset-corruption']){
  const q=await browser.newPage();const target=fault==='binding-corruption'?new URL('binding.json',url).href:fault==='design-corruption'?new URL('../ADOPTED-DESIGN.md',url).href:new URL('../../m31-browser-screen-2026-10-16/viewer/scene.js',url).href;
  await q.route(target,r=>r.fulfill({status:200,contentType:'text/plain',body:'deliberate display-only corruption'}));await q.goto(url);await q.locator('body[data-binding=failed]').waitFor();check(fault+' hides replay and claims',await q.locator('#content').isHidden()&&await q.locator('#replay').isHidden()&&await q.locator('h1').innerText()==='Evidence display stopped.');await q.close();
 }
 const late=await browser.newPage();await waitReady(late);await late.frameLocator('#replay').locator('body').evaluate(e=>{e.dataset.binding='failed';});await late.locator('body[data-binding=failed]').waitFor();check('late iframe failure clears success',await late.locator('#content').isHidden()&&!(await late.locator('#status').innerText()).includes('verified'));await late.screenshot({path:path.join(out,'late-error.png')});await late.close();
 report.passed=true;
}
main().catch(e=>{report.passed=false;report.failure=e.message;process.exitCode=1;}).finally(async()=>{await browser?.close();fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,errors:report.errors,warnings:report.warnings,failure:report.failure}));});
