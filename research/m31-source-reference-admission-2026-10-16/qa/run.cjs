const fs=require('fs'),path=require('path'),crypto=require('crypto');
const {chromium}=require('playwright');
const pkg=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);fs.mkdirSync(out,{recursive:true});
const url='http://127.0.0.1:8876/research/m31-source-reference-admission-2026-10-16/viewer/';
const result=JSON.parse(fs.readFileSync(path.join(pkg,'results/result.json'))),report={kind:'display-only-qa',scientificExecution:false,checks:[],console:[],screenshots:[]};
let browser;const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
function check(name,pass,detail=''){report.checks.push({name,pass:!!pass,detail});if(!pass)throw Error(name+': '+detail);}
async function shot(page,name,locator){const b=await (locator||page).screenshot({path:path.join(out,name),timeout:5000});report.screenshots.push({path:name,sha256:hash(b),bytes:b.length});}
async function run(){
 browser=await chromium.launch({executablePath:process.env.RESEARCH_CHROME,headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});page.setDefaultTimeout(5000);
 page.on('pageerror',e=>report.console.push({kind:'pageerror',message:e.message}));page.on('console',m=>{if(['error','warning'].includes(m.type()))report.console.push({kind:m.type(),message:m.text()});});
 page.on('response',r=>{if(r.status()>=400)report.console.push({kind:'http-error',status:r.status(),url:r.url()});});
 await page.goto(url,{waitUntil:'networkidle'});await page.waitForFunction(()=>document.body.dataset.binding!=='pending');
 check('bound evidence',await page.locator('body').getAttribute('data-binding')==='verified');
 await page.waitForFunction(()=>!document.getElementById('reset').disabled);
 check('Three.js canvas',await page.locator('#scene canvas').count()===1);
 check('primary L2 metric',await page.locator('#l2').innerText()===(100*result.radially_weighted_relative_L2_using_offboard2_reference).toFixed(1)+'%');
 check('max discrepancy',await page.locator('#max').innerText()===result.max_absolute_normalized_discrepancy.toFixed(3));
 const actual=await page.locator('#rows tr').evaluateAll(rows=>rows.map(r=>[...r.cells].map(c=>c.title)));
 check('all saved table values',JSON.stringify(actual)===JSON.stringify(result.union_knot_records.map(r=>[r.r_over_l,r.g1,r.g2,r.difference_g2_minus_g1].map(String))));
 check('complete saved JSON',JSON.stringify(JSON.parse(await page.locator('#result-json').textContent()))===JSON.stringify(result));
 await shot(page,'desktop.png');await page.locator('#scene').scrollIntoViewIfNeeded();await shot(page,'desktop-scene.png',page.locator('#scene'));
 const fmt=n=>Number(n.toPrecision(7)).toString();
 for(const mode of ['normalized','target']){await page.selectOption('#units',mode);for(let i=0;i<result.union_knot_records.length;i++){
  const r=result.union_knot_records[i];await page.locator('#probe').evaluate((el,n)=>{el.value=String(n);el.dispatchEvent(new Event('input',{bubbles:true}));},i);
  const text=await page.locator('#probe-output').innerText(),scale=mode==='target'?9.66:1;
  check(`${mode} probe ${i}`,text.includes(fmt(r.g1*scale))&&text.includes(fmt(r.g2*scale))&&(await page.locator('#scene').getAttribute('aria-label')).includes(String(r.r_over_l)));
 }}
 await page.selectOption('#units','normalized');await page.locator('#probe').evaluate(el=>{el.value='2';el.dispatchEvent(new Event('input',{bubbles:true}));});
 const initial=hash(await page.locator('#scene').screenshot());await page.check('#overlay');
 check('overlay changes graph',hash(await page.locator('#scene').screenshot())!==initial&&(await page.locator('#scene').getAttribute('aria-label')).includes('overlaid'));await page.uncheck('#overlay');
 const box=await page.locator('#scene canvas').boundingBox();await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();await page.mouse.move(box.x+box.width/2+80,box.y+box.height/2+25,{steps:5});await page.mouse.up();
 check('orbit changes graph',hash(await page.locator('#scene').screenshot())!==initial);await page.click('#reset');check('reset restores graph',hash(await page.locator('#scene').screenshot())===initial);
 await page.setViewportSize({width:390,height:844});await page.evaluate(()=>window.scrollTo(0,0));await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
 check('mobile no page overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await shot(page,'mobile.png');await page.locator('#scene').scrollIntoViewIfNeeded();await shot(page,'mobile-scene.png',page.locator('#scene'));check('mobile visible canvas',await page.locator('#scene canvas').isVisible());
 check('no browser errors',report.console.length===0,JSON.stringify(report.console));
 await page.route('**/results/result.json',async route=>{const s=fs.readFileSync(path.join(pkg,'results/result.json'),'utf8'),changed=s.replace('0.258146831346001','0.258146831346002');check('same-length corruption fixture',changed!==s&&Buffer.byteLength(changed)===Buffer.byteLength(s));await route.fulfill({status:200,contentType:'application/json',body:changed});});
 await page.reload({waitUntil:'networkidle'});await page.waitForFunction(()=>document.body.dataset.binding==='failed');check('corruption refuses display',await page.locator('#evidence').isHidden()&&(await page.locator('#status').innerText()).includes('SHA-256 mismatch')&&await page.locator('#scene canvas').count()===0);await shot(page,'corruption-refused.png');
}
const deadline=setTimeout(()=>{report.timeout=true;browser?.close();},60000);
run().then(()=>{report.pass=true;}).catch(e=>{report.pass=false;report.error=e.message;process.exitCode=1;}).finally(async()=>{clearTimeout(deadline);await browser?.close();fs.writeFileSync(path.join(out,'qa.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({pass:report.pass,checks:report.checks.length,error:report.error}));});
