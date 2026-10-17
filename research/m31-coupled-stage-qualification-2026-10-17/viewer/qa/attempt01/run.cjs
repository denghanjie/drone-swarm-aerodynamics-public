'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const root=process.env.RESEARCH_ROOT,pkg='research/m31-coupled-stage-qualification-2026-10-17',out=__dirname;
const base='http://127.0.0.1:8876/'+pkg+'/viewer/',start=Date.now(),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const report={schema:'m31-coupled-viewer-qa-v1',passed:false,flow:'saved records -> branch/endpoint/stage/forces -> actual record display',browserPath:'Browser plugin not available; existing Playwright used',checks:[],selections:0,viewports:[{width:1440,height:1000},{width:390,height:844}],errors:[],newScientificCalls:0};
const read=rel=>JSON.parse(fs.readFileSync(path.join(root,rel))),decode=w=>Buffer.from(w,'hex').readDoubleBE();
const delay=ms=>new Promise(r=>setTimeout(r,ms));let context,browserRoot,exit,close,originalSpawn=cp.spawn,timer;
function check(name,ok){report.checks.push({name,passed:!!ok});if(!ok)throw Error(name);}
function write(name,data){const b=Buffer.isBuffer(data)?data:Buffer.from(JSON.stringify(data,null,2)+'\n');const total=fs.readdirSync(out).reduce((s,f)=>s+fs.statSync(path.join(out,f)).size,0);if(total+b.length>16*1024**2)throw Error('QA output cap');fs.writeFileSync(path.join(out,name),b,{flag:'wx'});}
function inventory(){const paths=new Set(read(pkg+'/source-manifest.json').files.map(p=>p.path));for(const p of read(pkg+'/viewer/VIEWER-MANIFEST.json').files)paths.add(p.path);for(const name of ['source-manifest.json','source-publication.json','viewer/VIEWER-MANIFEST.json'])paths.add(pkg+'/'+name);function add(dir){for(const d of fs.readdirSync(path.join(root,dir),{withFileTypes:true})){const rel=dir+'/'+d.name;if(d.isDirectory())add(rel);else paths.add(rel);}}add(pkg+'/results');return [...paths].sort().map(p=>{const b=fs.readFileSync(path.join(root,p));return {path:p,bytes:b.length,sha256:sha(b)};});}
const before=inventory();write('immutable-before.json',before);
const rows=fs.readFileSync(path.join(root,pkg,'results/browser-journal.jsonl'),'utf8').trim().split('\n').map(JSON.parse);
const initial=read('research/m31-native-fresh-transfer-2026-10-17/results/inputs/fresh-a-t5.json').drones;
const expected={};for(const arm of ['coupled','off'])expected[arm]={endpoints:[initial,...rows.filter(r=>r.kind==='step'&&r.body.arm===arm).map(r=>r.body.final.map(x=>({id:x.id,state:x.stateWords})))],stages:rows.filter(r=>r.kind==='stage'&&r.body.arm===arm).map(r=>r.body)};
async function hook(page){return page.evaluate(()=>window.__M31_COUPLED_VIEW__);}
async function scrub(page,index){await page.locator('#scrub').evaluate((e,i)=>{e.value=String(i);e.dispatchEvent(new Event('input',{bubbles:true}));},index);}
function positionsMatch(s,states){return s.scene?.renderedBodyCount===64&&states.every((r,i)=>r.id===s.scene.ids[i]&&r.state.slice(0,3).every((w,k)=>Math.abs(decode(w)-s.scene.positions[i][k])<2e-6));}
async function main(){
 check('within renewed window',Date.now()<Date.parse('2026-10-17T05:06:20Z'));
 cp.spawn=function(command,args,options){if(browserRoot)throw Error('one browser only');const child=originalSpawn.call(this,command,args,{...options,detached:false});browserRoot=child;child.once('exit',(code,signal)=>{exit={code,signal};});child.once('close',(code,signal)=>{close={code,signal};});return child;};
 const {chromium}=require(path.join(process.env.RESEARCH_NODE_MODULES,'playwright'));
 context=await chromium.launchPersistentContext(process.env.RESEARCH_BROWSER_PROFILE,{executablePath:process.env.RESEARCH_CHROME,headless:true,viewport:report.viewports[0],timeout:15000,args:['--disable-background-networking'],serviceWorkers:'block'});cp.spawn=originalSpawn;
 const page=context.pages()[0];page.setDefaultTimeout(7000);page.on('pageerror',e=>report.errors.push(e.name));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());});
 await context.route('**/*',r=>new URL(r.request().url()).origin==='http://127.0.0.1:8876'?r.continue():r.abort());
 await page.goto(base,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.__M31_COUPLED_VIEW__?.scene);
 check('page identity',page.url()===base&&(await page.title()).includes('M31'));
 check('meaningful content',await page.locator('h1').innerText().then(x=>x.includes('Twenty milliseconds')));
 check('no framework overlay',await page.locator('vite-error-overlay, nextjs-portal').count()===0);
 check('saved passed status',(await hook(page)).status==='Saved checks passed');
 check('64 initial positions',positionsMatch(await hook(page),initial));
 for(const arm of ['coupled','off']){
  await page.locator('#arm').selectOption(arm);await page.locator('#stages').uncheck();
  for(let i=0;i<9;i++){await scrub(page,i);check(arm+' endpoint '+i,positionsMatch(await hook(page),expected[arm].endpoints[i]));report.selections++;}
  await page.locator('#forces').check();
  for(let i=0;i<32;i++){
   await scrub(page,i);const s=await hook(page),e=expected[arm].stages[i];
   check(arm+' stage '+i,positionsMatch(s,e.nativeInput.drones)&&s.scene.stateId===e.stageId&&s.scene.renderedArrowCount===64&&s.scene.arrowSegments.every((a,j)=>a.force.every((v,k)=>v===decode(e.records[j].consumed.worldForceWords[k]))&&a.endpoints.slice(3).every((v,k)=>Math.abs(v-decode(e.nativeInput.drones[j].state[k])-2*a.force[k])<1e-12)));report.selections++;
  }
 }
 await page.locator('#arm').selectOption('coupled');await page.locator('#stages').uncheck();await scrub(page,0);await page.locator('#play').click();await page.waitForFunction(()=>window.__M31_COUPLED_VIEW__.frameIndex>0);await page.locator('#play').click();check('play pause advances saved frame',!(await hook(page)).playing&&(await hook(page)).frameIndex>0);
 await page.locator('#reset').click();await delay(180);const camera=(await hook(page)).scene.camera;
 const box=await page.locator('#scene canvas').boundingBox();await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();await page.mouse.move(box.x+box.width/2+70,box.y+box.height/2+20,{steps:8});await page.mouse.up();await delay(200);check('orbit changes camera',JSON.stringify((await hook(page)).scene.camera)!==JSON.stringify(camera));await page.locator('#reset').click();await delay(200);
 await page.locator('#forces').check();await scrub(page,0);write('desktop.png',await page.screenshot());
 await page.setViewportSize(report.viewports[1]);await delay(200);check('mobile no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));check('mobile canvas width positive',await page.locator('#scene canvas').evaluate(e=>e.getBoundingClientRect().width>200));write('mobile.png',await page.screenshot());
 check('actual data console clean',report.errors.length===0);
 const corrupt=await context.newPage();await corrupt.route('**/results/browser-journal.jsonl',r=>r.fulfill({status:200,contentType:'text/plain',body:'{}\n'}));await corrupt.goto(base,{waitUntil:'networkidle'});await corrupt.waitForFunction(()=>window.__M31_COUPLED_VIEW__?.integrityFailure);check('corrupt evidence initial only',(await hook(corrupt)).counts.every(x=>x.endpoints===0&&x.stages===0)&&positionsMatch(await hook(corrupt),initial));
 const missing=await context.newPage();await missing.route('**/'+pkg+'/results/**',r=>r.fulfill({status:404,contentType:'text/plain',body:'Not found'}));await missing.goto(base,{waitUntil:'networkidle'});await missing.waitForFunction(()=>window.__M31_COUPLED_VIEW__?.scene);check('missing evidence initial only',(await hook(missing)).status==='No motion evidence yet'&&(await hook(missing)).counts.every(x=>x.endpoints===0&&x.stages===0));
 report.passed=true;
}
(async()=>{try{await Promise.race([main(),new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error('UI work deadline')),75000);})]);}catch(e){report.failure=String(e.message).replace(/\/Users\/[^\s]+/g,'[PRIVATE_PATH]');}finally{clearTimeout(timer);cp.spawn=originalSpawn;try{if(context)await Promise.race([context.close(),delay(4000).then(()=>{throw Error('close deadline');})]);for(let i=0;i<20&&(!exit||!close);i++)await delay(100);report.cleanup={exit:exit??null,close:close??null};if(!exit||!close||exit.code!==0||close.code!==0||exit.signal!==null||close.signal!==null)report.passed=false;}catch(_){report.passed=false;report.cleanupFailure=true;}
 const after=inventory();write('immutable-after.json',after);report.preservationPassed=JSON.stringify(before)===JSON.stringify(after);report.passed&&=report.preservationPassed;report.wallMilliseconds=Date.now()-start;write('report.json',report);console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,selections:report.selections,wallMilliseconds:report.wallMilliseconds,failure:report.failure,cleanup:report.cleanup}));process.exitCode=report.passed?0:1;}})();
