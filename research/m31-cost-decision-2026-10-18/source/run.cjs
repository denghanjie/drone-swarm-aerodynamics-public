'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const cp=require('child_process');
const root=path.resolve(process.argv[2]),pkg=path.join(root,'research/m31-cost-decision-2026-10-18'),out=path.join(pkg,'results'),privateDir=path.resolve(process.argv[3]);
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const write=(name,value)=>{const b=Buffer.from(JSON.stringify(value)+'\n');const fd=fs.openSync(path.join(out,name),'wx');try{fs.writeFileSync(fd,b);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}};
const read=name=>JSON.parse(fs.readFileSync(path.join(pkg,name),'utf8'));
const manifest=read('source-manifest.json'),receipt=read('source-publication.json');
if(hash(fs.readFileSync(path.join(pkg,'source-manifest.json')))!==receipt.manifestSha256||!receipt.remoteBytesEqualLocal)throw Error('public-source-gate');
for(const pin of manifest.files){const b=fs.readFileSync(path.join(root,pin.path));if(b.length!==pin.bytes||hash(b)!==pin.sha256)throw Error('source-pin');}
if(Date.now()>=Date.parse('2026-10-18T13:54:26Z'))throw Error('launch-cutoff');
const expected=fs.readFileSync(path.join(pkg,'expected.json'),'utf8').trim(),expectedHash=hash(expected);
const bundle=fs.readFileSync(path.join(root,'research/m31-native-tree-state1000-2026-10-17/source/browser-bundle.js'),'utf8');
let browser=null,completed=false,rows=0,rootExit=null,rootClose=null,launched=0,rootClosePromise;const start=Date.now();
(async()=>{try{
 const originalSpawn=cp.spawn;
 cp.spawn=function(command,args,options){
  if(launched!==0||fs.realpathSync(command)!==fs.realpathSync(process.env.COST_CHROME))throw Error('owned-browser-spawn');
  const child=originalSpawn.call(this,command,args,{...options,detached:false});launched++;
  child.once('exit',(code,signal)=>{rootExit={code,signal};});rootClosePromise=new Promise(resolve=>child.once('close',(code,signal)=>{rootClose={code,signal};resolve();}));return child;
 };
 const {chromium}=require('playwright');
 try{browser=await chromium.launchPersistentContext(path.join(privateDir,'profile'),{executablePath:process.env.COST_CHROME,headless:true,args:['--disable-background-networking','--disable-component-update','--no-first-run'],viewport:{width:1280,height:850},timeout:15000});}finally{cp.spawn=originalSpawn;}
 const cdp=await browser.newCDPSession(browser.pages()[0]);const browserVersion=await cdp.send('Browser.getVersion');
 write('environment.json',{startedUtc:new Date(start).toISOString(),node:process.version,browser:browserVersion,platform:process.platform,arch:process.arch,sourceCommit:receipt.commit,sourceManifestSha256:receipt.manifestSha256});
 const page=browser.pages()[0]||await browser.newPage();page.setDefaultTimeout(15000);
 await page.route('**/*',route=>{const u=new URL(route.request().url());return u.hostname==='127.0.0.1'&&u.port==='8876'?route.continue():route.abort();});
 await page.exposeFunction('saveActual',({row,semantic,failureBody})=>{
  const t=performance.now();if(++rows!==row.call||rows>116||typeof semantic!=='string'||Buffer.byteLength(semantic)>12*1048576)throw Error('output-bound');
  const digest=hash(semantic),name='semantic-'+digest+'.json';const blob=path.join(out,name);
  if(!fs.existsSync(blob)){const fd=fs.openSync(blob,'wx');try{fs.writeFileSync(fd,semantic);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}}
  else if(fs.readFileSync(blob,'utf8')!==semantic)throw Error('dedup-identity');
  const hostEqual=semantic===expected&&digest===expectedHash;if(failureBody!==null){const failure=JSON.stringify(failureBody);if(Buffer.byteLength(failure)+Buffer.byteLength(semantic)>12*1048576)write('failure-body-limit.json',{bytes:Buffer.byteLength(failure)});else write('actual-failure.json',failureBody);}
  write('query-'+String(rows).padStart(3,'0')+'.json',{...row,hostEqual,semanticPin:{path:name,bytes:Buffer.byteLength(semantic),sha256:digest}});
  const persistMs=performance.now()-t;if(!hostEqual)throw Error('host-semantic-mismatch');return {persistMs};
 });
 await page.exposeFunction('saveTiming',v=>write('transfer-'+String(v.call).padStart(3,'0')+'.json',v));
 await page.goto('http://127.0.0.1:8876/research/m31-cost-decision-2026-10-18/viewer/blank.html');
 await page.addScriptTag({content:fs.readFileSync(path.join(pkg,'source/browser.js'),'utf8')});
 const summary=await page.evaluate(payload=>window.runCost(payload),{inputWords:read('input-words.json'),expected:JSON.parse(expected),bundleText:bundle,deadlineUtc:'2026-10-18T13:57:26Z'});
 write('browser-summary.json',summary);completed=true;
 }catch(error){write('failure.json',{error:String(error.message).slice(0,500),completedQueries:rows});process.exitCode=1;}
 finally{if(browser)await browser.close();if(rootClosePromise)await rootClosePromise;write('browser-exit.json',{completed,rows,contextClosed:!!browser,launched,rootExit,rootClose,wallMs:Date.now()-start,finishedUtc:new Date().toISOString()});}
})();
