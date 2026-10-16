const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {chromium}=require('playwright'),url='http://127.0.0.1:8876/research/m31-center-screen-2026-10-16/viewer/',out=process.env.RESEARCH_QA_OUTPUT;
fs.mkdirSync(out,{recursive:true});let browser;const report={flow:'Load audited fresh Boids viewer; select all recorded cases; scrub/play/pause; check final-only load colors; scale/orbit/reset; inspect desktop/mobile and evidence links.',browserPath:'Browser plugin not available; installed Playwright and Chrome used.',viewports:[{width:1440,height:1000},{width:390,height:844}],checks:[],errors:[],warnings:[]};
function check(name,v){report.checks.push({name,passed:!!v});assert.ok(v,name);}
async function main(){browser=await chromium.launch({executablePath:process.env.RESEARCH_CHROME,headless:true});report.browserVersion=browser.version();const page=await browser.newPage({viewport:report.viewports[0],deviceScaleFactor:1});page.setDefaultTimeout(20000);page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());if(m.type()==='warning')report.warnings.push(m.text());});page.on('response',r=>{if(r.status()>=400)report.errors.push(r.status()+' '+r.url());});
 await page.goto(url);await page.locator('body[data-binding="verified"]').waitFor();await page.locator('#scene canvas').waitFor();
 check('page identity',page.url()===url&&await page.title()==='Fresh Boids · Center screen · M31');check('meaningful heading',(await page.locator('h1').innerText()).length>15);check('no framework overlay',await page.locator('vite-error-overlay,nextjs-portal').count()===0);check('recorded and not live disclosure',(await page.locator('.notice').innerText()).includes('Recorded replay, not live'));check('airflow off disclosed',(await page.locator('.notice').innerText()).includes('off'));check('short-horizon limitation',(await page.locator('.notice').innerText()).includes('mature flock'));check('all query calls visible',await page.locator('#timings').innerText()==='42 / 42');check('independent review passed',(await page.locator('#checks').innerText()).includes('passed'));check('two matched costs',await page.locator('.bar-row').count()===2);
 await page.screenshot({path:path.join(out,'desktop.png'),fullPage:true});
 for(const [id,n] of [['n1000-s261601-t2',1000],['n5000-s261602-t2',5000],['n5000-s261603-t2',5000]]){await page.locator('#case').selectOption(id);await page.waitForFunction(x=>document.getElementById('scene').dataset.case===x,id);check(id+' instances',await page.locator('#scene').getAttribute('data-instances')===String(n));check(id+' final frame',await page.locator('#scene').getAttribute('data-frame')==='20');check(id+' paired comparison',(await page.locator('#comparison').innerText()).includes('Paired median F/L'));check(id+' final load scope',(await page.locator('#colors').innerText()).includes('Final pose only'));}

 // Every rendered body translation must come from the selected saved pose frame.
 const display=await (await page.request.get(new URL('display.json',url).href)).json();
 for(const c of display.cases){
  const data=await(await page.request.get(new URL('../'+c.poses.path,url).href)).body();
  const values=new Float64Array(data.buffer.slice(data.byteOffset,data.byteOffset+data.byteLength));
  await page.locator('#case').selectOption(c.id);await page.waitForFunction(x=>document.getElementById('scene').dataset.case===x,c.id);
  let exact=true,count=0;
  for(let f=0;f<c.frames;f++){
   await page.locator('#frame').fill(String(f));await page.locator('#frame').dispatchEvent('input');
   const snap=await page.locator('#scene').evaluate(h=>h.__researchSnapshot());
   exact&&=snap.frame===f&&snap.instances===c.n&&snap.caseId===c.id;
   for(let i=0;i<c.n;i++)for(let axis=0;axis<3;axis++){exact&&=snap.matrices[16*i+12+axis]===Math.fround(values[f*(1+7*c.n)+1+7*i+axis]);count++;}
  }
  check(c.id+' all recorded frame translations match rendered float32 matrices',exact);
  report.checks.at(-1).coordinatesCompared=count;
 }
 await page.locator('#scene').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'swarm5000.png')});
 await page.locator('#frame').fill('0');await page.locator('#frame').dispatchEvent('input');check('scrub reaches recorded start',await page.locator('#time').innerText()==='0.0 s');check('early frame excludes loads',(await page.locator('#colors').innerText()).includes('uniform blue'));const f0=await page.locator('#scene').screenshot();await page.locator('#frame').fill('20');await page.locator('#frame').dispatchEvent('input');const f20=await page.locator('#scene').screenshot();check('recorded frames change render',!f0.equals(f20));await page.locator('#play').click();await page.waitForFunction(()=>Number(document.getElementById('scene').dataset.frame)>=1&&Number(document.getElementById('scene').dataset.frame)<20);check('replay advances recorded frames',await page.locator('body').getAttribute('data-playing')==='true');await page.locator('#play').click();check('pause stops replay',await page.locator('body').getAttribute('data-playing')==='false');await page.locator('#frame').fill('20');await page.locator('#frame').dispatchEvent('input');
 await page.locator('#size').selectOption('1');check('actual display scale',await page.locator('#scene').getAttribute('data-size')==='1');await page.locator('#size').selectOption('8');check('magnified display scale',await page.locator('#scene').getAttribute('data-size')==='8');await page.locator('#size').selectOption('4');
 const before=await page.locator('#scene').screenshot(),box=await page.locator('#scene').boundingBox();await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();await page.mouse.move(box.x+box.width/2+140,box.y+box.height/2+40,{steps:8});await page.mouse.up();const after=await page.locator('#scene').screenshot();check('orbit changes rendered camera',!before.equals(after));await page.locator('#reset').click();check('reset retains case',await page.locator('#case').inputValue()==='n5000-s261603-t2');
 await page.locator('details summary').click();check('evidence detail opens',await page.locator('#pins').isVisible());
 await page.setViewportSize(report.viewports[1]);await page.evaluate(()=>window.scrollTo(0,0));await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));check('mobile no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});await page.locator('#scene').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'mobile-scene.png')});
 for(const target of await page.locator('a').evaluateAll(xs=>xs.map(x=>x.href))){const response=await page.request.get(target);check('evidence link '+target.split('/').slice(-1)[0],response.ok());}
 check('console and network health',report.errors.length===0);check('no warnings',report.warnings.length===0);
 // These are separate display fault injections against saved bytes, not science reruns.
 const binding=await(await page.request.get(new URL('binding.json',url).href)).json();
 for(const fault of ['pin-mismatch','missing-closure','table-mismatch']){
  const q=await browser.newPage({viewport:report.viewports[0]});
  const key=fault==='missing-closure'?'reviewRun':'display';
  const target=new URL('../'+binding.records[key].path,url).href;
  const original=await(await page.request.get(target)).json();
  if(fault==='missing-closure')original.closed=false;
  else if(fault==='table-mismatch')original.cases[0].methods.L.median+=123;
  else original.lead+=' altered';
  const altered=Buffer.from(JSON.stringify(original));
  const fake=structuredClone(binding);
  if(fault!=='pin-mismatch'){fake.records[key].bytes=altered.length;fake.records[key].sha256=crypto.createHash('sha256').update(altered).digest('hex');}
  await q.route('**/binding.json',r=>r.fulfill({status:200,contentType:'application/json',body:JSON.stringify(fake)}));
  await q.route(target,r=>r.fulfill({status:200,contentType:'application/json',body:altered}));
  await q.goto(url);await q.locator('body[data-binding="failed"]').waitFor();
  check(fault+' fails closed and hides claims',await q.locator('#content').isHidden()&&(await q.locator('#status').innerText()).startsWith('Display stopped:'));
  await q.close();
 }
 report.passed=true;
}
main().catch(e=>{report.passed=false;report.failure=e.message;process.exitCode=1;}).finally(async()=>{await browser?.close();fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({passed:report.passed,checks:report.checks.length,errors:report.errors,warnings:report.warnings,failure:report.failure}));});
