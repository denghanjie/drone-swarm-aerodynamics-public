'use strict';
// Presentation-only QA. Never navigates to or invokes the diagnostic page.
const fs=require('fs'),path=require('path'),{chromium}=require('playwright');
const base=path.resolve(__dirname),url='http://127.0.0.1:8876/research/m31-control-channel-2026-10-16/viewer/';
const qa=path.join(base,'qa');fs.mkdirSync(qa,{recursive:false});
const report={kind:'control-channel-viewer-qa',browserPlugin:'not available',mode:'regular installed Playwright; presentation only',url,groups:[],errors:[],screenshots:[]};
const check=(v,m)=>{if(!v)throw Error(m);};
(async()=>{let browser;
 try{browser=await chromium.launch({executablePath:process.env.RESEARCH_CHROME_EXECUTABLE,headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 await page.goto(url);await page.waitForSelector('body[data-ready="true"]',{timeout:15000});
 check(page.url()===url&&(await page.title()).includes('Control-channel'),'Page identity');
 check((await page.locator('main').innerText()).length>500,'Meaningful page');
 check(await page.locator('canvas').count()===1,'One WebGL diagram');report.groups.push('identity, nonblank, canvas and evidence-ready');
 const artifact=JSON.parse(fs.readFileSync(path.join(base,'evidence.json')));
 check(await page.locator('#outcome').innerText()===artifact.summary.outcome,'Actual outcome');
 check(await page.locator('#review').innerText()===artifact.summary.review,'Actual review');
 check(await page.locator('#receipts .receipt').count()===artifact.files.length,'All backing files verified');
 report.groups.push('actual outcome, review and backing-file counts');
 for(let i=0;i<5;i++){await page.locator('#stages button').nth(i).click();check(await page.locator('#stage-name').innerText()===artifact.stages[i].name,'Stage content');}
 report.groups.push('five stage controls');
 await page.locator('#event').selectOption(String(artifact.events.length-1));check(await page.locator('#next').isDisabled(),'Last event boundary');
 await page.locator('#event').selectOption('0');check(await page.locator('#previous').isDisabled(),'First event boundary');
 await page.locator('#next').click();check(await page.locator('body').getAttribute('data-event')==='1','Next event');
 await page.locator('#previous').click();check(await page.locator('body').getAttribute('data-event')==='0','Previous event');report.groups.push('event selector and boundaries');
 await page.locator('#reset').click();check(await page.locator('body').getAttribute('data-camera')==='reset','Camera reset');
 await page.locator('#scene').scrollIntoViewIfNeeded();const box=await page.locator('#scene').boundingBox();
 await page.mouse.move(box.x+box.width*.5,box.y+box.height*.5);await page.mouse.down();await page.mouse.move(box.x+box.width*.6,box.y+box.height*.55,{steps:5});await page.mouse.up();await page.locator('#reset').click();report.groups.push('orbit and reset');
 await page.locator('h1').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(qa,'desktop.png'),fullPage:true});report.screenshots.push('desktop.png');
 await page.setViewportSize({width:390,height:844});await page.locator('#stages button').last().click();
 check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Mobile horizontal overflow');
 await page.locator('h1').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(qa,'mobile.png'),fullPage:true});report.screenshots.push('mobile.png');report.groups.push('desktop and mobile layout');
 const targets=await page.locator('footer a').evaluateAll(es=>es.map(e=>e.href));
 for(const target of targets){const response=await page.request.get(target);check(response.ok(),'Footer target unavailable');}
 report.groups.push('all footer targets');
 await page.route('**/raw/trace.public.ndjson',route=>route.fulfill({status:200,body:'corrupt QA fixture'}));await page.reload();
 await page.waitForSelector('body[data-binding="failed"]');check(await page.locator('canvas').count()===0,'Corrupt evidence must hide diagram');
 check(await page.locator('#outcome').innerText()==='Unavailable','Corrupt evidence cannot show result');
 await page.unroute('**/raw/trace.public.ndjson');await page.reload();await page.waitForSelector('body[data-ready="true"]');report.groups.push('corrupt backing bytes rejected and recovery');
 check(errors.length===0,'Console or page errors');report.groups.push('console/page health');report.passed=true;
 }catch(e){report.passed=false;report.errors.push(e.message);}finally{if(browser)await browser.close();fs.writeFileSync(path.join(qa,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({passed:report.passed,groups:report.groups.length,errors:report.errors}));process.exitCode=report.passed?0:1;}
})();
