'use strict';
// Viewer-only QA. No builder, checker, model, solver or scientific target imports.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
const {spawn}=require('node:child_process');
const {chromium}=require('playwright');
const root=process.env.RESEARCH_ROOT,chrome=process.env.RESEARCH_CHROME;
if(!root||!chrome)throw Error('RESEARCH_ROOT and RESEARCH_CHROME are required; no private fallback paths');
const pkg='research/m31-native-load-baseline-2026-10-17',auditPkg='research/m31-native-saved-audit-2026-10-17';
const out=__dirname,base='http://localhost:8876/'+pkg+'/viewer/',limit=32*1024*1024;
const start=Date.now(),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const canonical=x=>Array.isArray(x)?'['+x.map(canonical).join(',')+']':x&&typeof x==='object'?'{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}':JSON.stringify(x);
const same=(a,b)=>canonical(a)===canonical(b),read=p=>JSON.parse(fs.readFileSync(path.join(root,p))),decode=w=>Buffer.from(w,'hex').readDoubleBE();
const plan=['run-a','run-b'].flatMap(run=>[0,5,10].map(t=>({id:run+'-t'+t,run,t})));
const report={schema:'m31-native-viewer-qa-v1',attempt:2,scope:'Saved-record viewer only; no scientific imports, model calls, checker calls or projection builds',url:base,browserPath:'Regular Playwright; Browser plugin not available; named installed Chrome explicitly authorized',viewports:[{width:1440,height:1050},{width:390,height:844}],checks:[],combinations:[],requestSets:{},console:{},linkChecks:[],screenshots:[],passed:false,originalSupervisorStatus:'failed',newScientificCalls:0};
let browser,context,controller,profile,exitInfo,before,finalizing,deadline;
let stderr='';
function clean(message){let s=String(message);for(const value of [root,profile,process.env.HOME,chrome].filter(Boolean))s=s.split(value).join('[PRIVATE_PATH]');return s.replace(/\/(?:private\/)?var\/folders\/[^\s"']+/g,'[TEMP_PATH]').slice(0,12000);}
function directoryBytes(dir){return fs.readdirSync(dir,{withFileTypes:true}).reduce((n,d)=>n+(d.isDirectory()?directoryBytes(path.join(dir,d.name)):fs.statSync(path.join(dir,d.name)).size),0);}
function write(name,content){const b=Buffer.isBuffer(content)?content:Buffer.from(JSON.stringify(content,null,2)+'\n');if(directoryBytes(out)+b.length>limit)throw Error('32 MiB aggregate QA artifact cap');fs.writeFileSync(path.join(out,name),b,{flag:'wx'});}
function check(name,passed,detail){report.checks.push({name,passed:Boolean(passed),...(detail===undefined?{}:{detail})});if(!passed)throw Error(name);}
function pin(relative){const b=fs.readFileSync(path.join(root,relative));return {path:relative,bytes:b.length,sha256:sha(b)};}
function preservation(){
 const pins=new Map();
 for(const relative of [pkg+'/source-manifest.json',auditPkg+'/source-manifest.json']){
  const manifest=read(relative);pins.set(relative,pin(relative));
  for(const p of manifest.files){const actual=pin(p.path);if(!same(p,actual))throw Error('Frozen source pin changed: '+p.path);if(pins.has(p.path)&&!same(pins.get(p.path),actual))throw Error('Conflicting frozen pin');pins.set(p.path,actual);}
 }
 for(const relative of [pkg+'/source-publication.json',pkg+'/results/browser.json',pkg+'/results/browser-attempt.json',pkg+'/results/browser-journal.jsonl',auditPkg+'/source-publication.json',auditPkg+'/results/check-attempt.json',auditPkg+'/results/check.json',...['index.html','style.css','app.js','scene.js','build-display.py','binding.json','display-data.json'].map(n=>pkg+'/viewer/'+n)])pins.set(relative,pin(relative));
 return {files:[...pins.values()].sort((a,b)=>a.path.localeCompare(b.path))};
}
function observe(page,name){const events=report.console[name]={errors:[],warnings:[],failedRequests:[]};const urls=report.requestSets[name]=[];page.setDefaultTimeout(6000);page.on('pageerror',e=>events.errors.push(clean(e.message)));page.on('console',m=>{if(m.type()==='error')events.errors.push(clean(m.text()));if(m.type()==='warning')events.warnings.push(clean(m.text()));});page.on('request',r=>{if(!urls.includes(r.url()))urls.push(r.url());});page.on('requestfailed',r=>events.failedRequests.push({url:r.url(),reason:clean(r.failure()?.errorText)}));}
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const frame=page=>page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
async function gracefulCleanup(){
 const result={browserCloseRequested:false,controllerReaped:false,forcedTermination:false};
 try{await Promise.race([(async()=>{if(context)await context.close();if(browser){const session=await browser.newBrowserCDPSession();result.browserCloseRequested=true;await session.send('Browser.close');}})(),delay(4500)]);}catch(e){result.closeMessage=clean(e.message);}
 for(let i=0;i<30&&controller&&!exitInfo;i++)await delay(100);
 if(controller&&!exitInfo){result.forcedTermination=true;controller.kill('SIGTERM');for(let i=0;i<25&&!exitInfo;i++)await delay(100);}
 if(controller&&!exitInfo){controller.kill('SIGKILL');for(let i=0;i<20&&!exitInfo;i++)await delay(100);}
 result.controllerReaped=Boolean(exitInfo);result.exit=exitInfo||null;
 if(profile&&(!controller||exitInfo)){fs.rmSync(profile,{recursive:true,force:true});result.privateProfileRemoved=!fs.existsSync(profile);}
 if(controller&&(!result.controllerReaped||result.forcedTermination||exitInfo.code!==0)){report.passed=false;report.failure??='Browser controller did not close gracefully';}
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
 before=preservation();write('immutable-before.json',before);report.frozenFileCount=before.files.length;
 const binding=read(pkg+'/viewer/binding.json'),display=read(pkg+'/viewer/display-data.json'),saved=read(pkg+'/results/browser.json'),audit=read(auditPkg+'/results/check.json');
 check('actual native and independent audit identities',sha(fs.readFileSync(path.join(root,pkg+'/results/browser.json')))==='2f1a599000e782f1ac50163cf05fd046b7fb3c20e9ed350c7566b8c9fce900fe'&&sha(fs.readFileSync(path.join(root,auditPkg+'/results/check.json')))==='e4b93e1b5d03f378b2d7ac254256fcb7deb2e3371dc4dd70136ec6c376974080');
 check('compact display digest matches binding',same(pin(pkg+'/viewer/display-data.json'),{path:pkg+'/viewer/display-data.json',bytes:binding.display.bytes,sha256:binding.display.sha256}));
 check('all six states present',same(display.states.map(s=>s.id),plan.map(p=>p.id)));
 let projectedWords=0;
 for(const s of display.states){
  const caseConfig=read(pkg+'/config.json').cases.find(c=>c.id===s.id),raw=read(caseConfig.input.path);
  check(s.id+' exact raw pose words and stable IDs',same(s.ids,raw.drones.map(d=>d.id))&&same(s.poseWords,raw.drones.map(d=>[...d.state.slice(0,3),...d.state.slice(6,10)])));
  for(const method of ['F','L']){const call=saved.calls.find(c=>c.caseId===s.id&&c.method===method),shown=s.methods[method];
   check(s.id+'/'+method+' exact 64 delivered loads and field address',same(shown.loads,call.evidence.loads)&&same(s.ids,call.evidence.ids)&&shown.fieldPath==='calls['+call.sequence+'].evidence'&&same(s.poseWords,call.evidence.raw.map(d=>[...d.state.slice(0,3),...d.state.slice(6,10)])));
   check(s.id+'/'+method+' canonical complete load-word digest',shown.loadWordsSha256===sha(canonical({ids:s.ids,loads:call.evidence.loads})));
   projectedWords+=64*11;
  }
 }
 report.exactProjectedLoadWords=projectedWords;
 profile=fs.mkdtempSync(path.join(os.tmpdir(),'m31-native-viewer-qa-'));fs.chmodSync(profile,0o700);
 controller=spawn(chrome,['--headless=new','--remote-debugging-port=0','--remote-debugging-address=127.0.0.1','--user-data-dir='+profile,'--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update','--disable-features=MediaRouter','--disk-cache-size=1048576','about:blank'],{stdio:['ignore','ignore','pipe'],detached:false});
 controller.on('exit',(code,signal)=>{exitInfo={code,signal};});controller.stderr.on('data',b=>{if(stderr.length<131072)stderr+=b.toString().slice(0,131072-stderr.length);});controller.on('error',e=>{stderr+='\n'+e.message;});
 let port;
 for(let i=0;i<150;i++){if(exitInfo)throw Error('Installed Chrome exited before connection');const f=path.join(profile,'DevToolsActivePort');if(fs.existsSync(f)){port=Number(fs.readFileSync(f,'utf8').split('\n')[0]);if(Number.isInteger(port)&&port>0)break;}await delay(100);}
 check('fresh owned Chrome controller exposes local CDP',Number.isInteger(port)&&port>0);
 browser=await chromium.connectOverCDP('http://127.0.0.1:'+port,{timeout:15000});report.browserVersion=browser.version();report.playwrightVersion=require('playwright/package.json').version;
 check('named installed Chrome version',report.browserVersion==='155.0.8059.80');
 context=await browser.newContext({viewport:report.viewports[0],serviceWorkers:'block'});
 await context.route('**/*',route=>{const u=new URL(route.request().url());return u.origin==='http://localhost:8876'?route.continue():route.abort('blockedbyclient');});
 const page=await context.newPage();observe(page,'happy');
 await page.addInitScript(()=>{for(const kind of ['WebGLRenderingContext','WebGL2RenderingContext']){const proto=window[kind]?.prototype;if(!proto)continue;for(const name of ['bufferData','bufferSubData']){const original=proto[name];proto[name]=function(...args){const data=args[name==='bufferData'?1:2];if(data instanceof Float32Array&&data.length===384){window.__qaArrowUploads??=[];window.__qaArrowUploads.push(Array.from(data));if(window.__qaArrowUploads.length>12)window.__qaArrowUploads.shift();}return original.apply(this,args);};}const draw=proto.drawArrays;proto.drawArrays=function(mode,first,count){if(mode===1){window.__qaLineDraws??=[];window.__qaLineDraws.push(count);if(window.__qaLineDraws.length>30)window.__qaLineDraws.shift();}return draw.call(this,mode,first,count);};}});
 await page.goto(base,{waitUntil:'networkidle',timeout:15000});await page.waitForFunction(()=>window.__viewState?.validEvidence||window.__viewState?.error);await frame(page);
 check('page identity',page.url()===base&&(await page.title())==='Native load baseline · M31 saved evidence');
 check('meaningful first screen and WebGL body geometry',(await page.locator('h1').innerText()).includes('native loads')&&await page.evaluate(()=>window.__viewState?.validEvidence&&window.__viewState.renderedBodyCount===64));
 check('no framework error overlay',await page.locator('vite-error-overlay,nextjs-portal').count()===0);
 check('separate return, failure and audit cards',await page.locator('#native-count').innerText()==='12 / 12 returned'&&await page.locator('#supervisor-status').innerText()==='Failed · cleanup'&&await page.locator('#audit-status').innerText()==='Retained audit passed'&&await page.locator('#original-failure').isVisible());
 check('all six overview rows retain F L and parity',await page.locator('#all-results tr').evaluateAll(rows=>rows.length===6&&rows.every(r=>r.cells.length===6&&r.cells[1].textContent==='Returned'&&r.cells[2].textContent==='Qualified'&&r.cells[3].textContent==='Returned'&&r.cells[4].textContent==='Qualified'&&r.cells[5].textContent==='Same outputs')));
 const screenshot=async(name)=>{const b=await page.screenshot({fullPage:true});write(name,b);report.screenshots.push({path:name,bytes:b.length,sha256:sha(b)});};
 await screenshot('desktop.png');
 async function verifySelection(s,method,tag){
  await frame(page);const v=await page.evaluate(()=>window.__viewState),e=await page.evaluate(()=>window.__evidenceState),loads=s.methods[method].loads;
  check(tag+' correct current state and all 64 Float32 centers',v.validEvidence&&v.stateId===s.id&&v.method===method&&same(v.ids,s.ids)&&v.renderedBodyCount===64&&v.positions.length===64&&v.positions.every((p,i)=>same(p,s.poseWords[i].slice(0,3).map(w=>Math.fround(decode(w))))));
  const segments=loads.map((load,i)=>{const center=s.poseWords[i].slice(0,3).map(decode),force=load.worldForce.map(decode);return {id:load.id,force,endpoints:[...center,...center.map((x,k)=>x+force[k]*v.arrowScale)]};}).filter(s=>s.force.some(x=>x!==0));
  check(tag+' all actual force vectors and scaled double endpoints',same(v.arrowSegments,segments)&&v.arrowSegments.every(s=>s.endpoints.every(Number.isFinite))&&v.renderedArrowCount===(v.arrowsEnabled?segments.length:0));
  const uploaded=segments.flatMap(s=>s.endpoints.map(Math.fround));
  check(tag+' exposed Float32 upload values',same(v.uploadedArrowPositions,uploaded));
  if(v.arrowsEnabled){const gpu=await page.evaluate(()=>({uploads:window.__qaArrowUploads,draws:window.__qaLineDraws}));check(tag+' actual WebGL shaft upload and draw',gpu.uploads.some(a=>same(a.slice(0,uploaded.length),uploaded))&&gpu.draws.includes(2*segments.length));}
  const selected=loads.find(l=>l.id===v.droneId),expectedWords=[...selected.rotor,selected.collective,...selected.worldForce,...selected.worldMoment];
  check(tag+' selected exact words and saved audit row',same(e.selectedLoad,selected)&&same(await page.locator('#load-results code').allTextContents(),expectedWords)&&same(e.selectedAudit,audit.calls.find(c=>c.caseId===s.id&&c.method===method)));
  check(tag+' four visible accuracy categories and original failure',await page.locator('#audit-results tr').count()===4&&same(await page.locator('#audit-results td strong').allTextContents(),['Pass','Pass','Pass','Pass'])&&await page.locator('#original-failure').isVisible()&&v.originalSupervisorStatus==='failed'&&v.independentAudit==='qualified');
  check(tag+' selected exact field address',JSON.parse(await page.locator('#exact-record').textContent()).field===s.methods[method].fieldPath+'.loads['+s.ids.indexOf(v.droneId)+']');
  return v;
 }
 for(const s of display.states)for(const method of ['F','L']){
  await page.evaluate(()=>{window.__qaArrowUploads=[];window.__qaLineDraws=[];});await page.selectOption('#state',s.id);await page.selectOption('#method',method);
  await verifySelection(s,method,s.id+'/'+method);report.combinations.push({stateId:s.id,method,renderedBodies:64,forceEndpoints:64,exactProjectedLoadWords:704});
 }
 check('all twelve required combinations completed',report.combinations.length===12);
 const s=display.states[5];
 for(const scale of ['1','4','8']){await page.selectOption('#scale',scale);await verifySelection(s,'L','scale/'+scale);check('scale caption '+scale,(await page.locator('#scale-caption').innerText()).includes(scale+' scene m/N'));}
 await page.locator('#arrows').uncheck();await frame(page);check('hide arrows retains exact outputs',await page.evaluate(()=>window.__viewState.renderedArrowCount===0&&window.__viewState.arrowsEnabled===false&&window.__evidenceState.selectedLoad!==null));
 await page.locator('#arrows').check();await page.selectOption('#drone',String(s.ids[63]));await verifySelection(s,'L','alternate stable ID');check('stable ID highlight binding',await page.evaluate(()=>window.__viewState.droneId===window.__viewState.selectedId));
 await page.selectOption('#scale','4');await page.locator('#reset').click();await frame(page);const initial=await page.evaluate(()=>window.__viewState.camera);
 const canvas=page.locator('#scene canvas');await canvas.scrollIntoViewIfNeeded();const box=await canvas.boundingBox();check('visible canvas has meaningful area',box&&box.width>300&&box.height>300);
 await page.mouse.move(box.x+box.width*.5,box.y+box.height*.5);await page.mouse.down();await page.mouse.move(box.x+box.width*.68,box.y+box.height*.61,{steps:12});await page.mouse.up();await delay(700);
 check('orbit updates camera exposure',!same(initial,await page.evaluate(()=>window.__viewState.camera)));await page.locator('#reset').click();await frame(page);
 const reset=await page.evaluate(()=>window.__viewState.camera);check('reset restores default camera',reset.every((v,i)=>Math.abs(v-initial[i])<1e-10));
 await page.locator('#all-results tr').first().locator('button').click();await frame(page);check('table state navigation',await page.evaluate(()=>window.__viewState.stateId==='run-a-t0'));
 check('desktop has no horizontal page overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.setViewportSize(report.viewports[1]);await page.evaluate(()=>scrollTo(0,0));await frame(page);await screenshot('mobile.png');
 check('mobile page has no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 check('mobile controls fit their container',await page.locator('.controls').evaluate(e=>[...e.querySelectorAll('select,button,input')].every(c=>{const r=c.getBoundingClientRect(),p=e.getBoundingClientRect();return r.width>0&&r.left>=p.left&&r.right<=p.right+1;})));
 for(const table of ['#overview','#load-table','#audit-table']){const wrap=page.locator(table).locator('..');await wrap.evaluate(e=>e.scrollLeft=e.scrollWidth);check('mobile horizontal access '+table,await wrap.evaluate(e=>e.scrollWidth>e.clientWidth&&e.scrollLeft>0));}
 await page.selectOption('#state','run-a-t5');await page.selectOption('#method','F');await frame(page);check('mobile selectors update recorded selection',await page.evaluate(()=>window.__viewState.stateId==='run-a-t5'&&window.__viewState.method==='F'&&window.__viewState.renderedBodyCount===64));
 const links=await page.locator('a[href]').evaluateAll(a=>[...new Set(a.map(n=>n.href))]);
 check('corrected audit milestone summary link present',links.includes('http://localhost:8876/'+auditPkg+'/MILESTONE-SUMMARY.md'));
 for(const url of links){const response=await context.request.get(url,{timeout:10000});report.linkChecks.push({url,status:response.status()});check('local evidence link '+new URL(url).pathname,response.ok());await response.dispose();}
 const invalid=await context.newPage();observe(invalid,'corrupt-native');await invalid.route(new URL('binding.json',base).href,r=>r.fulfill({status:200,contentType:'application/json',body:'{}'}));await invalid.goto(base,{waitUntil:'networkidle'});await invalid.waitForFunction(()=>window.__viewState?.validEvidence===false);
 check('corrupt native binding clears claims and scene',await invalid.locator('#scene canvas').count()===0&&await invalid.locator('#load-results tr').count()===0&&await invalid.locator('#exact-record').textContent()==='No accepted record.'&&await invalid.locator('#all-results td').filter({hasText:'Not bound'}).count()===12&&await invalid.locator('#state,#method,#drone,#scale,#reset,#arrows').evaluateAll(cs=>cs.every(c=>c.disabled))&&await invalid.locator('#original-failure').isVisible());await invalid.close();
 const badAudit=await context.newPage();observe(badAudit,'corrupt-audit');await badAudit.route('http://localhost:8876/'+auditPkg+'/results/check.json',r=>r.fulfill({status:200,contentType:'application/json',body:'{}'}));await badAudit.goto(base,{waitUntil:'networkidle'});await badAudit.waitForFunction(()=>window.__viewState?.validEvidence===true);await frame(badAudit);
 check('corrupt audit retains native geometry and pending qualification',await badAudit.evaluate(()=>window.__viewState.renderedBodyCount===64&&window.__viewState.independentAudit==='pending'&&window.__evidenceState.auditDecision==='pending')&&await badAudit.locator('#audit-status').innerText()==='Unavailable'&&await badAudit.locator('#all-results td').filter({hasText:'Qualified'}).count()===0&&await badAudit.locator('#original-failure').isVisible());await badAudit.close();
 await page.evaluate(()=>{const select=document.getElementById('state'),option=document.createElement('option');option.value='invalid-qa-state';select.append(option);select.value=option.value;select.dispatchEvent(new Event('change'));});await frame(page);
 check('post-acceptance rejection clears stale values and geometry',await page.evaluate(()=>window.__viewState.validEvidence===false&&window.__evidenceState.bound===false)&&await page.locator('#load-results tr').count()===0&&await page.locator('#exact-record').textContent()==='No accepted record.'&&await page.locator('#original-failure').isVisible());
 for(const [name,events]of Object.entries(report.console)){check(name+' no unexpected errors or warnings',events.errors.length===0&&events.warnings.length===0&&events.failedRequests.length===0,events);}
 const allowed=new Set(['index.html','app.js','style.css','scene.js','binding.json','display-data.json'].map(n=>new URL(n,base).href));allowed.add(base);for(const p of ['manifest','publication','attempt','report'])allowed.add('http://localhost:8876/'+binding.audit[p].path);for(const n of ['three.module.js','three.core.js','OrbitControls.js'])allowed.add('http://localhost:8876/outputs/step02b-source/vendor/'+n);
 check('page requests limited to local display and bound audit files',Object.values(report.requestSets).flat().every(u=>allowed.has(u)),report.requestSets);
 report.passed=true;
}
(async()=>{try{await Promise.race([main(),new Promise((_,reject)=>{deadline=setTimeout(()=>reject(Error('215-second QA work deadline')),215000);})]);}catch(e){report.passed=false;report.failure=clean(e.message);}finally{await finalize();console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,combinations:report.combinations.length,wallMs:report.wallMs,preservationPassed:report.preservationPassed,cleanup:report.cleanup,failure:report.failure}));process.exitCode=report.passed?0:1;}})();
