'use strict';
const fs=require('fs'),path=require('path'),cp=require('child_process'),assert=require('assert/strict');
const root=path.resolve(process.argv[2]),pkg=path.join(root,'research/m31-cost-decision-2026-10-18'),out=path.join(pkg,'ui'),priv=path.resolve(process.argv[3]);fs.mkdirSync(out);fs.mkdirSync(priv);
let launched=0,rootExit=null,rootClose=null,closed;const spawn=cp.spawn;
cp.spawn=function(command,args,options){assert.equal(launched,0);assert.equal(fs.realpathSync(command),fs.realpathSync(process.env.COST_CHROME));const child=spawn.call(this,command,args,{...options,detached:false});launched++;child.once('exit',(code,signal)=>rootExit={code,signal});closed=new Promise(resolve=>child.once('close',(code,signal)=>{rootClose={code,signal};resolve();}));return child;};
const {chromium}=require('playwright');let browser;const checks=[],errors=[];
(async()=>{try{
 browser=await chromium.launchPersistentContext(path.join(priv,'profile'),{executablePath:process.env.COST_CHROME,headless:true,timeout:15000,args:['--disable-background-networking'],viewport:{width:1280,height:900}});cp.spawn=spawn;
 const page=browser.pages()[0];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.setDefaultTimeout(10000);
 const url='http://127.0.0.1:8876/research/m31-cost-decision-2026-10-18/viewer/';await page.goto(url);await page.waitForFunction(()=>window.__costView?.loaded);
 const state=await page.evaluate(()=>window.__costView),input=JSON.parse(fs.readFileSync(path.join(pkg,'input-words.json'),'utf8')),result=JSON.parse(fs.readFileSync(path.join(pkg,'results/analysis.json'),'utf8'));
 assert.equal(state.count,1000);assert.deepEqual(state.positions,input.drones.map(d=>d.state.slice(0,3).map(w=>Buffer.from(w,'hex').readDoubleBE())));checks.push('all1000-actual-position-words');assert.equal(state.ratio,result.medianPairedHtoF);assert.equal(state.keepGatePassed,result.keepGatePassed);checks.push('decision-and-ratio');assert.equal(await page.locator('#timings tr').count(),4);checks.push('four-method-rows');
 await page.screenshot({path:path.join(out,'desktop.png'),fullPage:true});
 const before=await page.evaluate(()=>window.__costView.camera),box=await page.locator('#scene').boundingBox();await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();await page.mouse.move(box.x+box.width/2+90,box.y+box.height/2+30,{steps:8});await page.mouse.up();await page.waitForFunction(b=>JSON.stringify(window.__costView.camera)!==JSON.stringify(b),before);checks.push('camera-orbit');
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));checks.push('mobile-width');
 await page.route('**/results/analysis.json',route=>route.fulfill({status:200,contentType:'application/json',body:'{}'}));await page.reload();await page.waitForFunction(()=>window.__costView?.error);assert.equal(await page.locator('#scene canvas').count(),0);checks.push('corrupt-result-withheld');
 assert.equal(errors.length,0);checks.push('no-console-page-errors');
 }catch(e){errors.push(String(e.message));process.exitCode=1;}finally{cp.spawn=spawn;if(browser)await browser.close();if(closed)await closed;fs.writeFileSync(path.join(out,'qa.json'),JSON.stringify({checks,errors,rootExit,rootClose,passed:errors.length===0&&rootExit?.code===0&&rootClose?.code===0},null,2)+'\n');}})();
