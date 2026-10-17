'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const root=process.env.RESEARCH_ROOT,pkg='research/m31-native-tree-state1000-2026-10-17',out=__dirname,base='http://127.0.0.1:8876/'+pkg+'/viewer/';
const start=Date.now(),sha=b=>crypto.createHash('sha256').update(b).digest('hex'),decode=w=>Buffer.from(w,'hex').readDoubleBE(),read=rel=>JSON.parse(fs.readFileSync(path.join(root,rel)));
const report={schema:'m31-tree-layout-ui-qa-v1',passed:false,flow:'disabled source status, calculated bound, earlier saved N1000 geometry, mobile, invalid status rejection',browserPath:'Browser plugin not available; existing Playwright used',checks:[],stateSelections:0,receiverSelections:0,viewports:[{width:1440,height:1000},{width:390,height:844}],errors:[],newScientificCalls:0};
let context,browserRoot,exit,close,timer;const originalSpawn=cp.spawn,delay=ms=>new Promise(r=>setTimeout(r,ms));
function check(name,ok){report.checks.push({name,passed:!!ok});if(!ok)throw Error(name);}
function write(name,value){const b=Buffer.isBuffer(value)?value:Buffer.from(JSON.stringify(value,null,2)+'\n');const total=fs.readdirSync(out).reduce((s,f)=>s+fs.statSync(path.join(out,f)).size,0);if(total+b.length>16*1024**2)throw Error('QA output cap');fs.writeFileSync(path.join(out,name),b,{flag:'wx'});}
function inventory(){const paths=[pkg+'/viewer/index.html',pkg+'/config.json',pkg+'/review/STORAGE-ADMISSION.json']; const old='research/m31-tree-witness-layout-2026-10-17';for(const p of read(old+'/viewer/VIEWER-MANIFEST.json').files)paths.push(p.path);return [...new Set(paths)].sort().map(p=>{const b=fs.readFileSync(path.join(root,p));return {path:p,bytes:b.length,sha256:sha(b)};});}
const before=inventory();write('immutable-before.json',before);
async function main(){
 check('within renewed window',Date.now()+90000<Date.parse('2026-10-17T05:06:20Z'));
 cp.spawn=function(command,args,options){if(browserRoot)throw Error('one browser only');const child=originalSpawn.call(this,command,args,{...options,detached:false});browserRoot=child;child.once('exit',(code,signal)=>{exit={code,signal};});child.once('close',(code,signal)=>{close={code,signal};});return child;};
 const {chromium}=require(path.join(process.env.RESEARCH_NODE_MODULES,'playwright'));
 context=await chromium.launchPersistentContext(process.env.RESEARCH_BROWSER_PROFILE,{executablePath:process.env.RESEARCH_CHROME,headless:true,viewport:report.viewports[0],timeout:15000,args:['--disable-background-networking'],serviceWorkers:'block'});cp.spawn=originalSpawn;
 const page=context.pages()[0];page.setDefaultTimeout(7000);page.on('pageerror',e=>report.errors.push(e.name));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());});
 await context.route('**/*',r=>new URL(r.request().url()).origin==='http://127.0.0.1:8876'?r.continue():r.abort());
 await page.goto(base,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.__sourceStatus&&window.__sourcePreview,{},{timeout:20000});
 check('disabled draft visible',await page.locator('#status').innerText()==='Prepared source · execution disabled');
 check('source status and bound',await page.evaluate(()=>window.__sourceStatus.disabled&&window.__sourceStatus.scientificCalls===0&&window.__sourceStatus.bound===137225341));
 check('prior N1000 explicit',await page.evaluate(()=>window.__sourcePreview.priorRecord&&window.__sourcePreview.renderedCount===1000));
 const frame=page.frames().find(f=>f!==page.mainFrame()&&f.url().includes('m31-tree-witness-layout'));
 check('actual recorded geometry',await frame.evaluate(()=>window.__probeView.loaded&&window.__probeView.caseId==='tree-t0-n1000-a'&&window.__probeView.positions.length===1000&&window.__probeView.validated===false));
 check('no simulation imports',(await page.locator('script[src]').count())===0);
 write('desktop-initial.png',await page.screenshot());await page.locator('#preview').scrollIntoViewIfNeeded();write('desktop-workbench.png',await page.screenshot());
 await page.setViewportSize(report.viewports[1]);await page.evaluate(()=>scrollTo(0,0));await delay(150);check('mobile no overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));write('mobile-initial.png',await page.screenshot());await page.locator('#preview').scrollIntoViewIfNeeded();await delay(150);write('mobile-workbench.png',await page.screenshot());
 check('console clean',report.errors.length===0);
 const p=await context.newPage();await p.route('**/config.json',r=>r.fulfill({status:200,contentType:'application/json',body:JSON.stringify({executionAllowed:true,authorization:'test',launchCutoffUtc:null})}));await p.goto(base,{waitUntil:'networkidle'});await p.waitForFunction(()=>document.querySelector('#status').textContent==='Source status unavailable');check('enabled source does not show disabled',await p.evaluate(()=>!window.__sourceStatus));await p.close();
 report.passed=true;
}
(async()=>{try{await Promise.race([main(),new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error('UI work deadline')),75000);})]);}catch(e){report.failure=String(e.message).replace(/\/Users\/[^\s]+/g,'[PRIVATE_PATH]');}finally{clearTimeout(timer);cp.spawn=originalSpawn;try{if(context)await Promise.race([context.close(),delay(4000).then(()=>{throw Error('close deadline');})]);for(let i=0;i<20&&(!exit||!close);i++)await delay(100);report.cleanup={exit:exit??null,close:close??null};if(!exit||!close||exit.code!==0||close.code!==0||exit.signal!==null||close.signal!==null)report.passed=false;}catch(_){report.passed=false;report.cleanupFailure=true;}const after=inventory();write('immutable-after.json',after);report.preservationPassed=JSON.stringify(before)===JSON.stringify(after);report.passed&&=report.preservationPassed;report.wallMilliseconds=Date.now()-start;write('report.json',report);console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,stateSelections:report.stateSelections,receiverSelections:report.receiverSelections,wallMilliseconds:report.wallMilliseconds,failure:report.failure,cleanup:report.cleanup}));process.exitCode=report.passed?0:1;}})();
