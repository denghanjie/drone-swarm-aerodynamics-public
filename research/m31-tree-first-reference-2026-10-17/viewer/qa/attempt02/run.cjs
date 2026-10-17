'use strict';
// Viewer-only QA. No builder, checker, model, solver or scientific target imports.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
const {spawn}=require('node:child_process');
const {chromium}=require('playwright');
const root=process.env.RESEARCH_ROOT,chrome=process.env.RESEARCH_CHROME;
if(!root||!chrome)throw Error('RESEARCH_ROOT and RESEARCH_CHROME are required; no private fallback paths');
const pkg='research/m31-tree-first-reference-2026-10-17';
const out=__dirname,base='http://127.0.0.1:8876/'+pkg+'/viewer/',limit=16*1024*1024;
const start=Date.now(),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const canonical=x=>Array.isArray(x)?'['+x.map(canonical).join(',')+']':x&&typeof x==='object'?'{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}':JSON.stringify(x);
const same=(a,b)=>canonical(a)===canonical(b),read=p=>JSON.parse(fs.readFileSync(path.join(root,p))),decode=w=>Buffer.from(w,'hex').readDoubleBE();
const plan=['fresh-a-t5','fresh-b-t5'];
const report={schema:'m31-tree-coverage-viewer-qa-v1',attempt:2,scope:'Saved coverage display only; no scientific imports or numerical computation',browserPath:'Browser plugin not available; installed Playwright used',url:base,viewports:[{width:1440,height:1050},{width:390,height:844}],checks:[],selections:[],requestSets:{},console:{},screenshots:[],passed:false,newScientificCalls:0};
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
 const inventory=read(pkg+'/viewer/SOURCE-PINS.json');for(const p of inventory.files){const actual=pin(p.path);if(!same(p,actual))throw Error('Viewer source changed: '+p.path);pins.set(p.path,actual);}
 const binding=read(pkg+'/viewer/binding.json');for(const p of binding.pins){const actual=pin(p.path);if(!same(p,actual))throw Error('Bound result changed: '+p.path);pins.set(p.path,actual);}
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
async function main(){
 check('approved saved-coverage viewer dispatch',process.env.RESEARCH_EXECUTION_CONTEXT==='tool-require-escalated'&&process.env.RESEARCH_VIEWER_QA_APPROVED==='tree-attempt02');
 before=preservation();write('immutable-before.json',before);report.frozenFileCount=before.files.length;
 const binding=read(pkg+'/viewer/binding.json'),runtime=read('research/m31-native-fresh-transfer-2026-10-17/runtime.json');
 function fileMatches(file,p){const raw=fs.readFileSync(file);return raw.length===p.bytes&&sha(raw)===p.sha256;}
 check('pinned Node runtime',fileMatches(process.execPath,runtime.node)&&process.version===runtime.node.version&&!process.env.NODE_OPTIONS&&process.execArgv.length===0);
 const contents=path.dirname(path.dirname(chrome));check('pinned installed Chrome components',runtime.chrome.files.every(p=>fileMatches(path.join(contents,p.appRelativePath),p)));check('pinned Playwright entry files',runtime.playwright.files.every(p=>fileMatches(path.join(process.env.NODE_PATH,p.moduleRelativePath),p)));
 profile=fs.mkdtempSync(path.join(os.tmpdir(),'m31-tree-viewer-qa-'));fs.chmodSync(profile,0o700);
 controller=spawn(chrome,['--headless=new','--remote-debugging-port=0','--remote-debugging-address=127.0.0.1','--user-data-dir='+profile,'--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update','--disable-features=MediaRouter','--disk-cache-size=1048576','about:blank'],{stdio:['ignore','ignore','pipe'],detached:false});
 controller.once('exit',(code,signal)=>{exitInfo={code,signal};});controller.once('close',(code,signal)=>{closeInfo={code,signal};});controller.stderr.on('data',b=>{if(stderr.length<131072)stderr+=b.toString().slice(0,131072-stderr.length);});controller.on('error',e=>{stderr+='\n'+e.message;});
 let port;for(let i=0;i<150;i++){if(exitInfo)throw Error('Chrome exited before connection');const f=path.join(profile,'DevToolsActivePort');if(fs.existsSync(f)){port=Number(fs.readFileSync(f,'utf8').split('\n')[0]);if(Number.isInteger(port)&&port>0)break;}await delay(100);}
 check('fresh owned root exposes local CDP',Number.isInteger(port)&&port>0);browser=await chromium.connectOverCDP('http://127.0.0.1:'+port,{timeout:15000});report.browserVersion=browser.version();report.playwrightVersion=require('playwright/package.json').version;check('named pinned versions',report.browserVersion===runtime.chrome.version&&report.playwrightVersion===runtime.playwright.version);
 context=await browser.newContext({viewport:report.viewports[0],serviceWorkers:'block'});await context.route('**/*',r=>new URL(r.request().url()).origin==='http://127.0.0.1:8876'?r.continue():r.abort('blockedbyclient'));
 const page=await context.newPage();observe(page,'main');await page.goto(base,{waitUntil:'networkidle',timeout:15000});await page.waitForFunction(()=>window.__treeViewer?.ready||window.__treeViewer?.error);await frame(page);check('bound scene ready',await page.evaluate(()=>window.__treeViewer.ready&&window.__treeViewer.render.bodyCount===64));
 check('page identity',await page.title()==='M31 · Which drone interactions can we skip?');check('not blank',await page.locator('h1').textContent()==='Which interactions can we skip?');check('all 24 rows visible in denominator',await page.locator('#results tr').count()===24);
 const expectedIndex=read(binding.result.path),full=expectedIndex.cases.reduce((s,c)=>s+c.fullOracleCalls,0),tree=expectedIndex.cases.reduce((s,c)=>s+c.treeOracleCalls,0);
 for(const [id,v]of [['full-count',full],['tree-count',tree],['avoided',full-tree]])check(id+' matches saved aggregate',await page.locator('#'+id).textContent()===v.toLocaleString('en-US'));
 for(const viewport of report.viewports){await page.setViewportSize(viewport);await frame(page);const label=viewport.width===1440?'desktop':'mobile';
  for(const id of plan){await page.selectOption('#run',id);const saved=read(binding.runs.find(x=>x.id===id).pin.path),positions=saved.input.drones.map(d=>d.state.slice(0,3).map(decode).map(Math.fround));
   for(const receiver of [0,63])for(const rotor of [0,1,2,3]){await page.selectOption('#receiver',String(receiver));await page.selectOption('#rotor',String(rotor));await frame(page);const state=await page.evaluate(()=>window.__treeViewer),query=saved.coverage.queries.find(q=>q.i===receiver&&q.r===rotor),zero=[],scalar=[];
    for(const term of query.terminals){if(term.kind==='zero')for(let i=term.start;i<term.end;i++){const source=saved.coverage.permutation[i];if(source!==saved.input.drones[receiver].id)zero.push(source);}else scalar.push(...term.sourceIndices.map(i=>saved.input.drones[i].id));}
    const positive=saved.pairs.filter(p=>p.ii===receiver&&p.r===rotor&&p.oracle.status==='positive').map(p=>p.j);
    const sort=x=>x.slice().sort((a,b)=>a-b);check(label+'/'+id+'/'+receiver+'/'+rotor+' exact saved coverage and uploaded centers',state.ready&&state.run===id&&state.receiverIndex===receiver&&state.rotor===rotor&&same(state.render.positions,positions)&&same(sort(state.zeroIds),sort(zero))&&same(sort(state.scalarIds),sort(scalar))&&same(sort(state.positiveIds),sort(positive))&&state.render.bodyCount===64&&state.render.groupCount===query.terminals.filter(t=>t.kind==='zero').length);
    report.selections.push({viewport:label,id,receiver,rotor,provedZero:zero.length,scalar:scalar.length,positive:positive.length});
   }
  }
  check(label+' no horizontal page overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.selectOption('#run',label==='desktop'?plan[0]:plan[1]);await page.selectOption('#receiver','0');await page.selectOption('#rotor','0');await page.locator('#reset').click();await frame(page);await page.evaluate(()=>scrollTo(0,0));const image=await page.screenshot({fullPage:true}),name=label+'.png';write(name,image);report.screenshots.push({path:name,bytes:image.length,sha256:sha(image)});
 }
 await page.locator('#boxes').uncheck();check('hide group boxes',await page.evaluate(()=>window.__treeViewer.render.boxesVisible===false));await page.locator('#boxes').check();check('show group boxes',await page.evaluate(()=>window.__treeViewer.render.boxesVisible===true));
 const canvas=page.locator('#scene canvas');await canvas.scrollIntoViewIfNeeded();const initial=await page.evaluate(()=>window.__treeViewer.render.camera),area=await canvas.boundingBox();await page.mouse.move(area.x+area.width*.5,area.y+area.height*.5);await page.mouse.down();await page.mouse.move(area.x+area.width*.7,area.y+area.height*.6,{steps:8});await page.mouse.up();await delay(600);check('orbit changes camera',!same(initial,await page.evaluate(()=>window.__treeViewer.render.camera)));await page.locator('#reset').click();await frame(page);check('reset restores camera',await page.evaluate(x=>window.__treeViewer.render.camera.every((v,i)=>Math.abs(v-x[i])<1e-9),initial));
 await page.locator('#receiver').evaluate(e=>{const o=document.createElement('option');o.value='99';o.textContent='Invalid QA selection';e.append(o);e.value='99';e.dispatchEvent(new Event('change',{bubbles:true}));});check('invalid selection fails closed',await page.evaluate(()=>window.__treeViewer.ready===false&&!window.__treeViewer.render&&document.querySelector('#receiver').disabled));
 const broken=await context.newPage();observe(broken,'corrupt-response');await broken.route('**/results/fresh-b-t5-tree.json',r=>r.fulfill({status:200,contentType:'application/json',body:'{}'}));await broken.goto(base,{waitUntil:'networkidle'});await broken.waitForFunction(()=>window.__treeViewer?.error);check('corrupted saved record cannot render',await broken.evaluate(()=>window.__treeViewer.ready===false&&window.__treeViewer.error==='Saved evidence hash mismatch'&&!document.querySelector('#scene canvas')));
 for(const [name,events]of Object.entries(report.console))check(name+' console and request health',events.errors.length===0&&events.warnings.length===0&&events.failedRequests.length===0,events);
 const allowed=new Set([base,...['app.js','style.css','scene.js','binding.json'].map(x=>new URL(x,base).href),...binding.pins.map(p=>'http://127.0.0.1:8876/'+p.path)]);check('all requests in local saved closure',Object.values(report.requestSets).flat().every(u=>allowed.has(u)));report.passed=true;
}
(async()=>{try{await Promise.race([main(),new Promise((_,reject)=>{deadline=setTimeout(()=>reject(Error('95-second UI QA deadline')),95000);})]);}catch(e){report.passed=false;report.failure=clean(e.message);}finally{await finalize();console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,selections:report.selections.length,wallMs:report.wallMs,preservationPassed:report.preservationPassed,cleanup:report.cleanup,failure:report.failure}));process.exitCode=report.passed?0:1;}})();
