'use strict';
// Viewer-only QA. No builder, checker, model, solver or scientific target imports.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
const {spawn}=require('node:child_process');
const {chromium}=require('playwright');
const root=process.env.RESEARCH_ROOT,chrome=process.env.RESEARCH_CHROME;
if(!root||!chrome)throw Error('RESEARCH_ROOT and RESEARCH_CHROME are required; no private fallback paths');
const pkg='research/m31-native-fresh-transfer-2026-10-17';
const out=__dirname,base='http://localhost:8876/'+pkg+'/viewer/',limit=16*1024*1024;
const start=Date.now(),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const canonical=x=>Array.isArray(x)?'['+x.map(canonical).join(',')+']':x&&typeof x==='object'?'{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}':JSON.stringify(x);
const same=(a,b)=>canonical(a)===canonical(b),read=p=>JSON.parse(fs.readFileSync(path.join(root,p))),decode=w=>Buffer.from(w,'hex').readDoubleBE();
const plan=['fresh-a-t5','fresh-b-t5'];
const report={schema:'m31-native-fresh-viewer-camera-qa-v1',attempt:3,scope:'Focused camera/frustum and control QA only; no scientific imports, calls, checker execution or binding builds',url:base,viewports:[{width:1440,height:1050},{width:390,height:844}],checks:[],frameChecks:[],finalSelections:[],frustumChecks:[],requestSets:{},console:{},linkChecks:[],screenshots:[],passed:false,newScientificCalls:0};
let browser,context,controller,profile,exitInfo,closeInfo,before,finalizing,deadline;
let stderr='';
function clean(message){let s=String(message);for(const value of [root,profile,process.env.HOME,chrome].filter(Boolean))s=s.split(value).join('[PRIVATE_PATH]');return s.replace(/\/(?:private\/)?var\/folders\/[^\s"']+/g,'[TEMP_PATH]').slice(0,12000);}
function directoryBytes(dir){return fs.readdirSync(dir,{withFileTypes:true}).reduce((n,d)=>n+(d.isDirectory()?directoryBytes(path.join(dir,d.name)):fs.statSync(path.join(dir,d.name)).size),0);}
function write(name,content){const b=Buffer.isBuffer(content)?content:Buffer.from(JSON.stringify(content,null,2)+'\n');if(directoryBytes(out)+b.length>limit)throw Error('16 MiB aggregate QA artifact cap');fs.writeFileSync(path.join(out,name),b,{flag:'wx'});}
function check(name,passed,detail){report.checks.push({name,passed:Boolean(passed),...(detail===undefined?{}:{detail})});if(!passed)throw Error(name);}
function pin(relative){const b=fs.readFileSync(path.join(root,relative));return {path:relative,bytes:b.length,sha256:sha(b)};}
function preservation(){
 const pins=new Map(),manifest=read(pkg+'/source-manifest.json');
 for(const p of manifest.files){const actual=pin(p.path);if(!same(p,actual))throw Error('Frozen source changed: '+p.path);pins.set(p.path,actual);}
 function addTree(relative){for(const d of fs.readdirSync(path.join(root,relative),{withFileTypes:true})){const p=relative+'/'+d.name;if(d.isDirectory())addTree(p);else pins.set(p,pin(p));}}
 addTree(pkg+'/results');
 addTree(pkg+'/viewer/qa/attempt02');
 const local=pkg+'/viewer/qa/attempt03',review=read(local+'/SOURCE-PINS.json');for(const p of review.files){const relative=local+'/'+p.path,actual=pin(relative);if(actual.bytes!==p.bytes||actual.sha256!==p.sha256)throw Error('Attempt03 source changed: '+p.path);pins.set(relative,actual);}pins.set(local+'/SOURCE-PINS.json',pin(local+'/SOURCE-PINS.json'));
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
  report.wallMs=Date.now()-start;report.within120Seconds=report.wallMs<=120000;if(!report.within120Seconds)report.passed=false;
  if(!report.passed&&stderr)report.browserDiagnostic=clean(stderr);report.outputBytesBeforeReport=directoryBytes(out);write('report.json',report);
 })();return finalizing;
}
for(const signal of ['SIGTERM','SIGINT'])process.on(signal,()=>{report.passed=false;report.failure='Supervisor requested '+signal;finalize().then(()=>process.exit(1));});
function project(p,view){
 const mul=(m,v)=>[0,1,2,3].map(row=>m[row]*v[0]+m[row+4]*v[1]+m[row+8]*v[2]+m[row+12]*v[3]);
 const clip=mul(view.cameraProjection,mul(view.cameraWorldInverse,[...p,1]));
 return {w:clip[3],ndc:clip.slice(0,3).map(x=>x/clip[3])};
}
function containment(points,padding,view){
 let maximumXY=0,minimumZ=Infinity,maximumZ=-Infinity,passed=true;
 for(const p of points)for(const x of [-padding,padding])for(const y of [-padding,padding])for(const z of [-padding,padding]){
  const q=project([p[0]+x,p[1]+y,p[2]+z],view);maximumXY=Math.max(maximumXY,Math.abs(q.ndc[0]),Math.abs(q.ndc[1]));minimumZ=Math.min(minimumZ,q.ndc[2]);maximumZ=Math.max(maximumZ,q.ndc[2]);
  passed&&=q.w>0&&q.ndc.every(Number.isFinite)&&Math.abs(q.ndc[0])<.995&&Math.abs(q.ndc[1])<.995&&q.ndc[2]>-1&&q.ndc[2]<1;
 }
 return {passed,maximumXY,minimumZ,maximumZ,points:points.length,padding};
}
async function main(){
 check('explicit approved camera-only dispatch',process.env.RESEARCH_EXECUTION_CONTEXT==='tool-require-escalated'&&process.env.RESEARCH_VIEWER_QA_APPROVED==='fresh-attempt03');
 before=preservation();write('immutable-before.json',before);report.frozenFileCount=before.files.length;
 const binding=read(pkg+'/viewer/binding.json'),generation=read(pkg+'/results/generation.json'),saved=read(pkg+'/results/browser.json'),runtime=read(pkg+'/runtime.json'),recs=new Map(generation.slots.map(s=>[s.id,read(s.generation.path)]));
 check('unchanged bound numerical identities',pin(pkg+'/results/browser.json').sha256==='c61e31e1019e956151d14a0bcb56c259b3bdabc0a2c2d3e68108fa0074c4d704'&&pin(pkg+'/results/check.json').sha256==='4dd659938c20a5ca1ba691b408855f734c829194d28e553584fcf065b58367ae');
 function fileMatches(file,p){const raw=fs.readFileSync(file);return raw.length===p.bytes&&sha(raw)===p.sha256;}
 check('pinned Node runtime',fileMatches(process.execPath,runtime.node)&&process.version===runtime.node.version&&!process.env.NODE_OPTIONS&&process.execArgv.length===0);
 const contents=path.dirname(path.dirname(chrome));check('pinned installed Chrome components',runtime.chrome.files.every(p=>fileMatches(path.join(contents,p.appRelativePath),p)));check('pinned Playwright entry files',runtime.playwright.files.every(p=>fileMatches(path.join(process.env.NODE_PATH,p.moduleRelativePath),p)));
 profile=fs.mkdtempSync(path.join(os.tmpdir(),'m31-fresh-camera-qa-'));fs.chmodSync(profile,0o700);
 controller=spawn(chrome,['--headless=new','--remote-debugging-port=0','--remote-debugging-address=127.0.0.1','--user-data-dir='+profile,'--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update','--disable-features=MediaRouter','--disk-cache-size=1048576','about:blank'],{stdio:['ignore','ignore','pipe'],detached:false});
 controller.once('exit',(code,signal)=>{exitInfo={code,signal};});controller.once('close',(code,signal)=>{closeInfo={code,signal};});controller.stderr.on('data',b=>{if(stderr.length<131072)stderr+=b.toString().slice(0,131072-stderr.length);});controller.on('error',e=>{stderr+='\n'+e.message;});
 let port;for(let i=0;i<150;i++){if(exitInfo)throw Error('Chrome exited before connection');const f=path.join(profile,'DevToolsActivePort');if(fs.existsSync(f)){port=Number(fs.readFileSync(f,'utf8').split('\n')[0]);if(Number.isInteger(port)&&port>0)break;}await delay(100);}
 check('fresh owned root exposes local CDP',Number.isInteger(port)&&port>0);browser=await chromium.connectOverCDP('http://127.0.0.1:'+port,{timeout:15000});report.browserVersion=browser.version();report.playwrightVersion=require('playwright/package.json').version;check('named pinned versions',report.browserVersion===runtime.chrome.version&&report.playwrightVersion===runtime.playwright.version);
 context=await browser.newContext({viewport:report.viewports[0],serviceWorkers:'block'});await context.route('**/*',r=>new URL(r.request().url()).origin==='http://localhost:8876'?r.continue():r.abort('blockedbyclient'));
 const page=await context.newPage();observe(page,'camera-fit');await page.goto(base,{waitUntil:'networkidle',timeout:15000});await page.waitForFunction(()=>window.__freshViewerState?.render||window.__freshViewerState?.integrityFailure);await frame(page);check('bound scene ready',await page.evaluate(()=>window.__freshViewerState.bound&&window.__freshViewerState.render?.renderedBodyCount===64));
 const points=f=>Array.from({length:64},(_,i)=>f.words.slice(i*7,i*7+3).map(decode));
 async function finalCheck(id,method,scale,label){
  const state=await page.evaluate(()=>window.__freshViewerState),call=saved.calls.find(c=>c.caseId===id&&c.method===method),origins=points(recs.get(id).frames[25]);
  const segments=call.evidence.loads.map((load,i)=>{const force=load.worldForce.map(decode);return{id:load.id,force,endpoints:[...origins[i],...origins[i].map((x,k)=>x+force[k]*scale)]};});
  const fit=containment(segments.flatMap(s=>[s.endpoints.slice(0,3),s.endpoints.slice(3)]),.065,state.render);
  check(label+' all force arrows inside actual camera frustum',fit.passed&&state.render.arrowScale===scale&&same(state.render.arrowSegments,segments)&&same(state.render.uploadedArrowPositions,segments.flatMap(s=>s.endpoints.map(Math.fround))));report.frustumChecks.push({label,...fit});return state;
 }
 for(const viewport of report.viewports){
  await page.setViewportSize(viewport);await frame(page);const viewportName=viewport.width===1440?'desktop':'mobile';
  const resized=await page.evaluate(()=>window.__freshViewerState),canvasSize=await page.locator('#scene').evaluate(e=>{const r=e.getBoundingClientRect();return{width:r.width,height:r.height,clientWidth:e.clientWidth,clientHeight:e.clientHeight};});check(viewportName+' camera aspect updates on resize',Math.abs(resized.render.cameraAspect-canvasSize.width/canvasSize.height)<1e-10,{cameraAspect:resized.render.cameraAspect,...canvasSize});
  if(viewportName==='mobile'){const id=resized.runId,m=resized.method,s=resized.render.arrowScale;await finalCheck(id,m,s,'mobile immediate resize');}
  for(const id of plan){await page.selectOption('#run',id);const initial=await page.evaluate(()=>window.__freshViewerState.render.camera);for(let i=0;i<26;i++){
   await page.locator('#frame').evaluate((e,value)=>{e.value=String(value);e.dispatchEvent(new Event('input',{bubbles:true}));},i);await frame(page);const state=await page.evaluate(()=>window.__freshViewerState),expected=points(recs.get(id).frames[i]),fit=containment(expected,.20,state.render);
   check(viewportName+'/'+id+'/frame'+i+' glyphs inside actual frustum',fit.passed&&state.frameIndex===i&&state.frameTime===recs.get(id).frames[i].t&&same(state.render.positions,expected.map(p=>p.map(Math.fround)))&&state.render.camera.every((x,j)=>Math.abs(x-initial[j])<1e-10));
   report.frameChecks.push({viewport:viewportName,id,index:i,centers:64,...fit});
  }
  for(const method of ['F','L'])for(const scale of [1,4,8]){await page.selectOption('#method',method);await page.selectOption('#scale',String(scale));await frame(page);await finalCheck(id,method,scale,viewportName+'/'+id+'/'+method+'/scale'+scale);report.finalSelections.push({viewport:viewportName,id,method,scale});}
  }
  check(viewportName+' page fits viewport',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.selectOption('#run',viewportName==='desktop'?plan[0]:plan[1]);await page.locator('#final').click();await page.selectOption('#method','F');await page.selectOption('#scale','4');await page.selectOption('#drone','0');await page.locator('#reset').click();await frame(page);await finalCheck(viewportName==='desktop'?plan[0]:plan[1],'F',4,viewportName+' screenshot');await page.evaluate(()=>scrollTo(0,0));
  const image=await page.screenshot({fullPage:true}),name=viewportName+'.png';write(name,image);report.screenshots.push({path:name,bytes:image.length,sha256:sha(image)});
 }
 check('52 saved frames on both viewports',report.frameChecks.length===104);check('all final method and scale combinations',report.finalSelections.length===24);
 await page.locator('#initial').click();await page.locator('#next').click();check('endpoint and step controls',await page.evaluate(()=>window.__freshViewerState.frameIndex===1));await page.locator('#play').click();await delay(460);await page.locator('#play').click();check('playback still advances without interpolation',await page.evaluate(()=>!window.__freshViewerState.playing&&window.__freshViewerState.frameIndex>1&&Math.abs(window.__freshViewerState.frameTime-window.__freshViewerState.frameIndex*.2)<1e-12));
 await page.locator('#final').click();await page.locator('#arrows').uncheck();await frame(page);check('force toggle still works',await page.evaluate(()=>window.__freshViewerState.render.renderedArrowCount===0));await page.locator('#arrows').check();await page.locator('#reset').click();await frame(page);const resetCamera=await page.evaluate(()=>window.__freshViewerState.render.camera);
 const canvas=page.locator('#scene canvas');await canvas.scrollIntoViewIfNeeded();const area=await canvas.boundingBox();await page.mouse.move(area.x+area.width*.5,area.y+area.height*.5);await page.mouse.down();await page.mouse.move(area.x+area.width*.62,area.y+area.height*.57,{steps:10});await page.mouse.up();await delay(1000);const orbit=await page.evaluate(()=>window.__freshViewerState.render.camera);check('manual orbit remains available',!same(orbit,resetCamera));await page.locator('#previous').click();await frame(page);check('frame change preserves user camera',await page.evaluate(expected=>window.__freshViewerState.render.camera.every((x,i)=>Math.abs(x-expected[i])<.05),orbit));await page.locator('#reset').click();await frame(page);check('reset restores full-run fitted camera',await page.evaluate(expected=>window.__freshViewerState.render.camera.every((x,i)=>Math.abs(x-expected[i])<1e-10),resetCamera));
 for(const [name,events]of Object.entries(report.console))check(name+' no page errors warnings or failed requests',events.errors.length===0&&events.warnings.length===0&&events.failedRequests.length===0,events);
 const allowed=new Set([base,...['app.js','style.css','scene.js','binding.json'].map(x=>new URL(x,base).href),...binding.pins.map(p=>'http://localhost:8876/'+p.path)]);check('requests remain in reviewed local closure',Object.values(report.requestSets).flat().every(u=>allowed.has(u)));report.passed=true;
}
(async()=>{try{await Promise.race([main(),new Promise((_,reject)=>{deadline=setTimeout(()=>reject(Error('95-second focused QA deadline')),95000);})]);}catch(e){report.passed=false;report.failure=clean(e.message);}finally{await finalize();console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,frames:report.frameChecks.length,finalSelections:report.finalSelections.length,wallMs:report.wallMs,preservationPassed:report.preservationPassed,cleanup:report.cleanup,failure:report.failure}));process.exitCode=report.passed?0:1;}})();
