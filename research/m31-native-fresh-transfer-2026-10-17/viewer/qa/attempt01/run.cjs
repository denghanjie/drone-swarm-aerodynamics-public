'use strict';
// Viewer-only QA. No builder, checker, model, solver or scientific target imports.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
const {spawn}=require('node:child_process');
const {chromium}=require('playwright');
const root=process.env.RESEARCH_ROOT,chrome=process.env.RESEARCH_CHROME;
if(!root||!chrome)throw Error('RESEARCH_ROOT and RESEARCH_CHROME are required; no private fallback paths');
const pkg='research/m31-native-fresh-transfer-2026-10-17';
const out=__dirname,base='http://localhost:8876/'+pkg+'/viewer/',limit=32*1024*1024;
const start=Date.now(),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const canonical=x=>Array.isArray(x)?'['+x.map(canonical).join(',')+']':x&&typeof x==='object'?'{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}':JSON.stringify(x);
const same=(a,b)=>canonical(a)===canonical(b),read=p=>JSON.parse(fs.readFileSync(path.join(root,p))),decode=w=>Buffer.from(w,'hex').readDoubleBE();
const plan=['fresh-a-t5','fresh-b-t5'];
const report={schema:'m31-native-fresh-viewer-qa-v1',attempt:1,scope:'Actual saved-frame viewer only; no scientific imports, calls, checker execution or binding builds',url:base,viewports:[{width:1440,height:1050},{width:390,height:844}],checks:[],frameChecks:[],finalSelections:[],requestSets:{},console:{},linkChecks:[],screenshots:[],passed:false,newScientificCalls:0};
let browser,context,controller,profile,exitInfo,closeInfo,before,finalizing,deadline;
let stderr='';
function clean(message){let s=String(message);for(const value of [root,profile,process.env.HOME,chrome].filter(Boolean))s=s.split(value).join('[PRIVATE_PATH]');return s.replace(/\/(?:private\/)?var\/folders\/[^\s"']+/g,'[TEMP_PATH]').slice(0,12000);}
function directoryBytes(dir){return fs.readdirSync(dir,{withFileTypes:true}).reduce((n,d)=>n+(d.isDirectory()?directoryBytes(path.join(dir,d.name)):fs.statSync(path.join(dir,d.name)).size),0);}
function write(name,content){const b=Buffer.isBuffer(content)?content:Buffer.from(JSON.stringify(content,null,2)+'\n');if(directoryBytes(out)+b.length>limit)throw Error('32 MiB aggregate QA artifact cap');fs.writeFileSync(path.join(out,name),b,{flag:'wx'});}
function check(name,passed,detail){report.checks.push({name,passed:Boolean(passed),...(detail===undefined?{}:{detail})});if(!passed)throw Error(name);}
function pin(relative){const b=fs.readFileSync(path.join(root,relative));return {path:relative,bytes:b.length,sha256:sha(b)};}
function preservation(){
 const pins=new Map(),manifest=read(pkg+'/source-manifest.json');
 for(const p of manifest.files){const actual=pin(p.path);if(!same(p,actual))throw Error('Frozen source changed: '+p.path);pins.set(p.path,actual);}
 function addTree(relative){for(const d of fs.readdirSync(path.join(root,relative),{withFileTypes:true})){const p=relative+'/'+d.name;if(d.isDirectory())addTree(p);else pins.set(p,pin(p));}}
 addTree(pkg+'/results');
 const inventory=read(pkg+'/viewer/SOURCE-PINS.json');for(const p of inventory.files){const relative=pkg+'/viewer/'+p.path,actual=pin(relative);if(actual.bytes!==p.bytes||actual.sha256!==p.sha256)throw Error('Frozen viewer changed: '+p.path);pins.set(relative,actual);}
 for(const relative of [pkg+'/source-manifest.json',pkg+'/source-publication.json',pkg+'/viewer/SOURCE-PINS.json'])pins.set(relative,pin(relative));
 return {files:[...pins.values()].sort((a,b)=>a.path.localeCompare(b.path))};
}
function observe(page,name){const events=report.console[name]={errors:[],warnings:[],failedRequests:[]};const urls=report.requestSets[name]=[];page.setDefaultTimeout(6000);page.on('pageerror',e=>events.errors.push(clean(e.message)));page.on('console',m=>{if(m.type()==='error')events.errors.push(clean(m.text()));if(m.type()==='warning')events.warnings.push(clean(m.text()));});page.on('request',r=>{if(!urls.includes(r.url()))urls.push(r.url());});page.on('requestfailed',r=>events.failedRequests.push({url:r.url(),reason:clean(r.failure()?.errorText)}));}
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const frame=page=>page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
async function gracefulCleanup(){
 const result={browserCloseRequested:false,controllerReaped:false,forcedTermination:false};
 try{await Promise.race([(async()=>{if(context)await context.close();if(browser){const session=await browser.newBrowserCDPSession();result.browserCloseRequested=true;await session.send('Browser.close');}})(),delay(4500)]);}catch(e){result.closeMessage=clean(e.message);}
 for(let i=0;i<30&&controller&&(!exitInfo||!closeInfo);i++)await delay(100);
 if(controller&&(!exitInfo||!closeInfo)){result.forcedTermination=true;controller.kill('SIGTERM');for(let i=0;i<25&&!exitInfo;i++)await delay(100);}
 if(controller&&(!exitInfo||!closeInfo)){controller.kill('SIGKILL');for(let i=0;i<20&&!exitInfo;i++)await delay(100);}
 result.controllerReaped=Boolean(exitInfo&&closeInfo);result.exit=exitInfo||null;result.close=closeInfo||null;
 if(profile&&(!controller||exitInfo)){fs.rmSync(profile,{recursive:true,force:true});result.privateProfileRemoved=!fs.existsSync(profile);}
 if(controller&&(!result.controllerReaped||result.forcedTermination||exitInfo.code!==0||exitInfo.signal!==null||closeInfo?.code!==0||closeInfo?.signal!==null)){report.passed=false;report.failure??='Browser controller did not close gracefully';}
 report.cleanup=result;
}
async function finalize(){
 if(finalizing)return finalizing;
 finalizing=(async()=>{clearTimeout(deadline);try{await gracefulCleanup();}catch(e){report.passed=false;report.cleanupFailure=clean(e.message);}
  try{const after=preservation();write('immutable-after.json',after);report.preservationPassed=same(before,after);check('all frozen sources, numerical records and viewer files unchanged',report.preservationPassed);}catch(e){report.passed=false;report.preservationPassed=false;report.preservationFailure=clean(e.message);}
  report.wallMs=Date.now()-start;report.within240Seconds=report.wallMs<=240000;if(!report.within240Seconds)report.passed=false;
  if(!report.passed&&stderr)report.browserDiagnostic=clean(stderr);report.outputBytesBeforeReport=directoryBytes(out);write('report.json',report);
 })();return finalizing;
}
for(const signal of ['SIGTERM','SIGINT'])process.on(signal,()=>{report.passed=false;report.failure='Supervisor requested '+signal;finalize().then(()=>process.exit(1));});
async function main(){
 check('explicit approved viewer dispatch',process.env.RESEARCH_EXECUTION_CONTEXT==='tool-require-escalated'&&process.env.RESEARCH_VIEWER_QA_APPROVED==='fresh-attempt01');
 before=preservation();write('immutable-before.json',before);report.frozenFileCount=before.files.length;
 const binding=read(pkg+'/viewer/binding.json'),generation=read(pkg+'/results/generation.json'),saved=read(pkg+'/results/browser.json'),checker=read(pkg+'/results/check.json'),runtime=read(pkg+'/runtime.json');
 check('actual bound scientific output identities',pin(pkg+'/results/browser.json').sha256==='c61e31e1019e956151d14a0bcb56c259b3bdabc0a2c2d3e68108fa0074c4d704'&&pin(pkg+'/results/check.json').sha256==='4dd659938c20a5ca1ba691b408855f734c829194d28e553584fcf065b58367ae'&&checker.qualifiedTargetCalls===4&&checker.qualifiedMovingControlCalls===8);
 const recs=new Map(generation.slots.map(s=>[s.id,read(s.generation.path)]));
 check('two saved 26-frame sequences',same(generation.slots.map(s=>s.id),plan)&&[...recs.values()].every(r=>r.frames.length===26&&r.frames[0].t===0&&r.frames[25].t===5));
 function fileMatches(file,p){const raw=fs.readFileSync(file);return raw.length===p.bytes&&sha(raw)===p.sha256;}
 check('pinned Node runtime',fileMatches(process.execPath,runtime.node)&&process.version===runtime.node.version&&!process.env.NODE_OPTIONS&&process.execArgv.length===0);
 const appContents=path.dirname(path.dirname(chrome));
 check('pinned installed Chrome components',runtime.chrome.files.every(p=>fileMatches(path.join(appContents,p.appRelativePath),p)));
 check('pinned Playwright entry files',runtime.playwright.files.every(p=>fileMatches(path.join(process.env.NODE_PATH,p.moduleRelativePath),p)));
 profile=fs.mkdtempSync(path.join(os.tmpdir(),'m31-fresh-viewer-qa-'));fs.chmodSync(profile,0o700);
 controller=spawn(chrome,['--headless=new','--remote-debugging-port=0','--remote-debugging-address=127.0.0.1','--user-data-dir='+profile,'--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update','--disable-features=MediaRouter','--disk-cache-size=1048576','about:blank'],{stdio:['ignore','ignore','pipe'],detached:false});
 controller.once('exit',(code,signal)=>{exitInfo={code,signal};});controller.once('close',(code,signal)=>{closeInfo={code,signal};});controller.stderr.on('data',b=>{if(stderr.length<131072)stderr+=b.toString().slice(0,131072-stderr.length);});controller.on('error',e=>{stderr+='\n'+e.message;});
 let port;for(let i=0;i<150;i++){if(exitInfo)throw Error('Chrome exited before connection');const f=path.join(profile,'DevToolsActivePort');if(fs.existsSync(f)){port=Number(fs.readFileSync(f,'utf8').split('\n')[0]);if(Number.isInteger(port)&&port>0)break;}await delay(100);}
 check('fresh owned Chrome root exposes local CDP',Number.isInteger(port)&&port>0);
 browser=await chromium.connectOverCDP('http://127.0.0.1:'+port,{timeout:15000});report.browserVersion=browser.version();report.playwrightVersion=require('playwright/package.json').version;
 check('named runtime versions',report.browserVersion===runtime.chrome.version&&report.playwrightVersion===runtime.playwright.version);
 context=await browser.newContext({viewport:report.viewports[0],serviceWorkers:'block'});await context.route('**/*',route=>new URL(route.request().url()).origin==='http://localhost:8876'?route.continue():route.abort('blockedbyclient'));
 const page=await context.newPage();observe(page,'actual-records');await page.goto(base,{waitUntil:'networkidle',timeout:15000});await page.waitForFunction(()=>window.__freshViewerState?.render||window.__freshViewerState?.integrityFailure);await frame(page);
 check('actual replay accepted',await page.evaluate(()=>window.__freshViewerState.bound&&window.__freshViewerState.render?.renderedBodyCount===64)&&await page.title()==='Fresh flight replay · M31 saved evidence');
 check('all operational and scientific cards',same(await page.locator('.verdicts strong').allTextContents(),['Completed','Qualified','Completed','qualified']));
 check('fixed target and control denominator',await page.locator('#all-results tr').count()===2&&await page.locator('#moving-results tr').count()===8&&await page.locator('#all-results td').filter({hasText:'qualified'}).count()===4);
 for(const id of plan){await page.selectOption('#run',id);const rec=recs.get(id);for(let i=0;i<rec.frames.length;i++){
  await page.locator('#frame').evaluate((e,value)=>{e.value=String(value);e.dispatchEvent(new Event('input',{bubbles:true}));},i);await frame(page);const v=await page.evaluate(()=>window.__freshViewerState),f=rec.frames[i];
  const expected=Array.from({length:64},(_,j)=>f.words.slice(j*7,j*7+3).map(w=>Math.fround(decode(w))));
  check(id+' frame '+i+' exact saved centers',v.bound&&v.runId===id&&v.frameIndex===i&&v.frameTime===f.t&&same(v.render.positions,expected)&&v.render.renderedBodyCount===64&&same(v.render.ids,rec.initial.drones.map(d=>d.id)));
  check(id+' frame '+i+' final-only forces',i===25?v.render.renderedArrowCount===64:v.render.renderedArrowCount===0);
  report.frameChecks.push({id,index:i,t:f.t,centers:64});
 }}
 check('all 52 recorded frames visited',report.frameChecks.length===52);
 for(const id of plan)for(const method of ['F','L']){
  await page.selectOption('#run',id);await page.locator('#final').click();await page.selectOption('#method',method);await frame(page);const v=await page.evaluate(()=>window.__freshViewerState),rec=recs.get(id),call=saved.calls.find(c=>c.caseId===id&&c.method===method),loads=call.evidence.loads;
  const segments=loads.map((l,i)=>{const center=rec.frames[25].words.slice(i*7,i*7+3).map(decode),force=l.worldForce.map(decode);return{id:l.id,force,endpoints:[...center,...center.map((x,k)=>x+force[k]*v.render.arrowScale)]};}).filter(x=>x.force.some(v=>v!==0));
  check(id+'/'+method+' exact forces and endpoints',v.qualified&&v.frameTime===5&&same(v.render.arrowSegments,segments)&&same(v.render.uploadedArrowPositions,segments.flatMap(x=>x.endpoints.map(Math.fround))));
  for(const load of [loads[0],loads[63]]){await page.selectOption('#drone',String(load.id));const exact=JSON.parse(await page.locator('#exact-record').textContent());check(id+'/'+method+' selected saved words ID '+load.id,same(exact.load,load)&&same(exact.check,checker.calls.find(c=>c.caseId===id&&c.method===method))&&same(await page.locator('#load-results code').allTextContents(),[load.rotor.join(' '),load.collective,load.worldForce.join(' '),load.worldMoment.join(' ')]));}
  report.finalSelections.push({id,method,forceVectors:64,selectedLoadIds:[loads[0].id,loads[63].id]});
 }
 await page.selectOption('#run',plan[0]);await page.locator('#initial').click();await page.locator('#play').click();await delay(470);await page.locator('#play').click();const paused=await page.evaluate(()=>window.__freshViewerState.frameIndex);await delay(260);
 check('playback advances discrete frames and pause holds',paused>0&&paused<25&&await page.evaluate(i=>!window.__freshViewerState.playing&&window.__freshViewerState.frameIndex===i,paused));
 await page.locator('#next').click();check('next stored frame',await page.evaluate(i=>window.__freshViewerState.frameIndex===i+1,paused));await page.locator('#previous').click();check('previous stored frame',await page.evaluate(i=>window.__freshViewerState.frameIndex===i,paused));
 await page.locator('#final').click();check('final endpoint is actual 5 s snapshot',await page.evaluate(()=>window.__freshViewerState.frameTime===5&&window.__freshViewerState.frameIndex===25));
 await page.selectOption('#scale','8');await frame(page);check('force display scale',await page.evaluate(()=>window.__freshViewerState.render.arrowScale===8));await page.locator('#arrows').uncheck();await frame(page);check('force toggle clears arrows',await page.evaluate(()=>window.__freshViewerState.render.renderedArrowCount===0));await page.locator('#arrows').check();await page.selectOption('#scale','4');await page.locator('#reset').click();
 await frame(page);const camera=await page.evaluate(()=>window.__freshViewerState.render.camera),canvas=page.locator('#scene canvas');await canvas.scrollIntoViewIfNeeded();const area=await canvas.boundingBox();check('meaningful scene area',area&&area.width>300&&area.height>300);await page.mouse.move(area.x+area.width*.5,area.y+area.height*.5);await page.mouse.down();await page.mouse.move(area.x+area.width*.65,area.y+area.height*.6,{steps:10});await page.mouse.up();await delay(600);check('orbit control moves camera',!same(camera,await page.evaluate(()=>window.__freshViewerState.render.camera)));await page.locator('#reset').click();await frame(page);check('reset restores camera',await page.evaluate(expected=>window.__freshViewerState.render.camera.every((x,i)=>Math.abs(x-expected[i])<1e-10),camera));
 check('desktop page width',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 const screenshot=async name=>{const bytes=await page.screenshot({fullPage:true});write(name,bytes);report.screenshots.push({path:name,bytes:bytes.length,sha256:sha(bytes)});};
 await page.selectOption('#drone','0');await page.selectOption('#method','F');await page.evaluate(()=>scrollTo(0,0));await frame(page);await screenshot('desktop.png');
 await page.setViewportSize(report.viewports[1]);await page.selectOption('#run',plan[1]);await page.locator('#final').click();await page.evaluate(()=>scrollTo(0,0));await frame(page);await screenshot('mobile.png');
 check('mobile width and usable canvas',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)&&await page.locator('#scene').evaluate(e=>e.getBoundingClientRect().width>=300));
 check('mobile control bounds',await page.locator('.controls').evaluate(e=>[...e.querySelectorAll('select,button,input')].every(c=>{const r=c.getBoundingClientRect(),p=e.getBoundingClientRect();return r.left>=p.left&&r.right<=p.right+1;})));
 for(const selector of ['#overview','#load-table']){const wrap=page.locator(selector).locator('..');await wrap.evaluate(e=>e.scrollLeft=e.scrollWidth);check('mobile table access '+selector,await wrap.evaluate(e=>e.scrollLeft>0&&e.scrollWidth>e.clientWidth));}
 const links=await page.locator('a[href]').evaluateAll(a=>[...new Set(a.map(n=>n.href))]);for(const url of links){check('local-only record link',new URL(url).origin==='http://localhost:8876');const response=await context.request.get(url,{timeout:10000});report.linkChecks.push({url,status:response.status()});check('record link '+new URL(url).pathname,response.ok());await response.dispose();}
 const corrupt=await context.newPage();observe(corrupt,'corrupt-record');await corrupt.route('http://localhost:8876/'+generation.slots[0].generation.path,r=>r.fulfill({status:200,contentType:'application/json',body:'{}'}));await corrupt.goto(base,{waitUntil:'networkidle'});await corrupt.waitForFunction(()=>window.__freshViewerState?.integrityFailure);
 check('corrupted record fails closed',await corrupt.evaluate(()=>!window.__freshViewerState.bound&&window.__freshViewerState.render===null)&&await corrupt.locator('#load-results tr').count()===0&&await corrupt.locator('#scene canvas').count()===0&&await corrupt.locator('#all-results tr').count()===2&&await corrupt.locator('#moving-results tr').count()===8);await corrupt.close();
 await page.locator('#run').evaluate(e=>{const o=document.createElement('option');o.value='invalid-fixed-slot';e.append(o);e.value=o.value;e.dispatchEvent(new Event('change',{bubbles:true}));});await frame(page);
 check('stale geometry and load words clear after rejection',await page.evaluate(()=>!window.__freshViewerState.bound&&window.__freshViewerState.render===null)&&await page.locator('#load-results tr').count()===0&&await page.locator('#exact-record').textContent()==='No accepted saved call.');
 for(const [name,events]of Object.entries(report.console))check(name+' no unexpected page errors or warnings',events.errors.length===0&&events.warnings.length===0&&events.failedRequests.length===0,events);
 const allowed=new Set([base,...['app.js','style.css','scene.js','binding.json'].map(x=>new URL(x,base).href),...binding.pins.map(p=>'http://localhost:8876/'+p.path)]);
 check('requests confined to local viewer and bound files',Object.values(report.requestSets).flat().every(u=>allowed.has(u)),report.requestSets);
 report.passed=true;
}
(async()=>{try{await Promise.race([main(),new Promise((_,reject)=>{deadline=setTimeout(()=>reject(Error('215-second QA work deadline')),215000);})]);}catch(e){report.passed=false;report.failure=clean(e.message);}finally{await finalize();console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,frames:report.frameChecks.length,finalSelections:report.finalSelections.length,wallMs:report.wallMs,preservationPassed:report.preservationPassed,cleanup:report.cleanup,failure:report.failure}));process.exitCode=report.passed?0:1;}})();
