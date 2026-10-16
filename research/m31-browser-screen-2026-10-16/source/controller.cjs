'use strict';
// Source-only authored controller. Science starts solely through the frozen gate.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),os=require('node:os');
const p=path.resolve(process.argv[2]),privateDir=process.env.RESEARCH_SUPERVISOR_DIR;
const config=JSON.parse(fs.readFileSync(path.join(p,'config.json'))),runtime=JSON.parse(fs.readFileSync(path.join(p,'runtime.json')));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const assert=(ok,why)=>{if(!ok)throw Error(why);};
const json=(file,obj)=>fs.writeFileSync(file,JSON.stringify(obj)+'\n',{flag:'wx'});
const delay=ms=>new Promise(r=>setTimeout(r,ms));
const pin=(file,rel)=>{const b=fs.readFileSync(file);return {path:rel,bytes:b.length,sha256:sha(b)};};
const env=()=>({cpuModel:os.cpus()[0]?.model,logicalCores:os.cpus().length,installedRAMBytes:os.totalmem(),architecture:os.arch(),platform:os.platform(),loadAverage:os.loadavg(),headless:true,renderingDuringTiming:false,clock:'performance.now monotonic milliseconds',processIdsPublished:false});
let browser=null,active=null,output=null,pending=null,bytesWritten=0,failed=false;
async function barrier(id){
 json(path.join(privateDir,`barrier-${id}.json`),{processId:id});
 const until=performance.now()+20000,file=path.join(privateDir,`barrier-${id}-ack.json`);
 while(!fs.existsSync(file)){assert(performance.now()<until,'closure-barrier-timeout');await delay(50);}
 const ack=JSON.parse(fs.readFileSync(file));assert(ack.allOwnedBrowserProcessesAbsent&&ack.monitorHealthy,'closure-barrier-failed');return ack;
}
async function saveChunk(_source,rel,base64,final,emergency=false){
 assert(active&&output,'inactive-collector');assert(/^results\/[A-Za-z0-9_.-]+$/.test(rel),'artifact-path');
 assert(typeof base64==='string'&&base64.length<=4*Math.ceil(config.browser.chunkBytes/3)+4,'encoded-chunk-cap');
 assert(typeof final==='boolean'&&typeof emergency==='boolean','chunk-flags');
 const b=Buffer.from(base64,'base64');assert(b.length<=config.browser.chunkBytes&&b.toString('base64')===base64,'chunk-encoding');
 if(!pending){const dest=path.join(output,rel),part=dest+'.partial';assert(!fs.existsSync(dest),'exclusive-artifact');pending={rel,dest,part,fd:fs.openSync(part,'wx'),bytes:0,h:crypto.createHash('sha256'),emergency};}
 assert(pending.rel===rel&&pending.emergency===emergency,'one-inflight-artifact');
 const cap=emergency?config.limits.scientificBytes:config.limits.normalScientificBytes;
 assert(bytesWritten+b.length<=cap,'browser-output-cap');
 let offset=0;while(offset<b.length){const written=fs.writeSync(pending.fd,b,offset,b.length-offset);assert(written>0,'zero-byte-write');offset+=written;}pending.h.update(b);pending.bytes+=b.length;bytesWritten+=b.length;
 if(!final)return {acknowledgedBytes:pending.bytes,complete:false};
 fs.fsyncSync(pending.fd);fs.closeSync(pending.fd);fs.linkSync(pending.part,pending.dest);fs.unlinkSync(pending.part);
 const dirfd=fs.openSync(path.dirname(pending.dest),'r');try{fs.fsyncSync(dirfd);}finally{fs.closeSync(dirfd);}
 const actual=fs.readFileSync(pending.dest),expected=pending.h.digest('hex');assert(actual.length===pending.bytes&&sha(actual)===expected,'persisted-artifact-mismatch');
 const saved={path:rel,bytes:actual.length,sha256:expected,durable:true,exclusive:true,fsync:true,directoryFsync:true};pending=null;return saved;
}
(async()=>{
 assert(process.argv.length===3&&privateDir,'controller-arguments');assert(!process.env.NODE_OPTIONS&&process.execArgv.length===0,'runtime-flags');
 const nb=fs.readFileSync(fs.realpathSync(process.execPath));assert(nb.length===runtime.node.bytes&&sha(nb)===runtime.node.sha256&&process.version===runtime.node.version,'node-runtime');
 assert(config.schema==='m31-browser-screen-v1'&&os.arch()===runtime.architecture&&os.platform()===runtime.platform&&os.endianness()==='LE','platform-config');
 for(const x of runtime.playwright.files){const parts=x.moduleRelativePath.split('/'),base=path.dirname(require.resolve(parts.shift()+'/package.json')),file=path.join(base,...parts),b=fs.readFileSync(file);assert(b.length===x.bytes&&sha(b)===x.sha256,'playwright-entry-pin');}
 const registry=require('./process-registry.cjs'),{chromium}=require('playwright');
 const index=JSON.parse(fs.readFileSync(path.join(p,'inputs/index.json'))),gen=JSON.parse(fs.readFileSync(path.join(p,'results/generation-run.json')));
 assert(gen.supervisorSuccess&&gen.closed&&gen.childGroupAbsent,'generation-not-qualified');
 const sharedPins=[];for(const dir of ['inputs','generation'])for(const name of fs.readdirSync(path.join(p,dir))){const f=path.join(p,dir,name);if(fs.statSync(f).isFile())sharedPins.push(pin(f,dir+'/'+name));}
 const sourceNames=['browser.html','browser-bundle.js','browser.js','source-bundle.json'],sourcePins=sourceNames.map(n=>pin(path.join(__dirname,n),'source/'+n));
 const receipt=JSON.parse(fs.readFileSync(path.join(p,'source-publication.json')));
 for(let slot=0;slot<3;slot++){
  const id=config.processes[slot],started=performance.now();active=id;output=path.join(p,'runs',id);fs.mkdirSync(path.join(output,'results'),{recursive:true});bytesWritten=0;
  json(path.join(output,'invocation.lock'),{processId:id,slot,consumed:true});fs.writeFileSync(path.join(privateDir,'active-slot.tmp'),JSON.stringify({processId:id,slot,started:Date.now()}));fs.renameSync(path.join(privateDir,'active-slot.tmp'),path.join(privateDir,'active-slot.json'));
  const rec={processId:id,slot,attempted:true,complete:false,closureConfirmed:false,sourceCommit:receipt.commit,sourceManifestSha256:receipt.manifestSha256,runtimeIdentityVerified:false,browserClosed:false,allOwnedBrowserProcessesAbsent:false,inputsVerified:false,sourceServedPins:sourcePins,servedRequests:[],errors:[],environmentStart:env()};
  let timer=setTimeout(()=>{failed=true;process.stderr.write('browser-slot-wall-timeout\n');process.exit(2);},config.browser.slotWallSeconds*1000);timer.unref();
  try{
   const before=registry.entries.length;
   browser=await chromium.launch({channel:'chrome',headless:true,timeout:config.browser.launchTimeoutMs});
   assert(registry.entries.length===before+1,'single-launch-registration');
   rec.processRegistryCount=registry.entries.length-before;
   const entry=registry.entries.at(-1);rec.profileIdentitySha256=sha(entry.profileArgument);rec.launchArguments=entry.args.map(a=>a.startsWith('--user-data-dir=')?'--user-data-dir=<private-fresh-profile>':a);
   const page=await browser.newPage();page.setDefaultTimeout(20000);
   const cdp=await browser.newBrowserCDPSession(),version=await cdp.send('Browser.getVersion');
   rec.browserRuntime=version;rec.browserVersion=await browser.version();
   assert(rec.browserVersion===runtime.chrome.version,'chrome-build-identity');rec.runtimeIdentityVerified=true;
   page.on('pageerror',()=>rec.errors.push('pageerror'));page.on('console',m=>{if(m.type()==='error')rec.errors.push('console-error');});
   await page.exposeBinding('__saveChunk',saveChunk);
   const origin='http://127.0.0.1:8876';
   await page.route('**/*',async route=>{
    const u=new URL(route.request().url());let relative;
    if(u.origin!==origin){rec.errors.push('external-request');return route.abort();}
    if(u.pathname==='/research/m31-browser-screen-2026-10-16/source/'||u.pathname==='/research/m31-browser-screen-2026-10-16/source/browser.html')relative='source/browser.html';
    else if(u.pathname.startsWith('/research/m31-browser-screen-2026-10-16/source/'))relative='source/'+u.pathname.split('/').at(-1);
    else relative=u.pathname.slice(1);
    const allowed=[...sourcePins,...sharedPins].find(x=>x.path===relative);if(!allowed){rec.errors.push('unlisted-request');return route.abort();}
    const b=fs.readFileSync(path.join(p,relative));assert(b.length===allowed.bytes&&sha(b)===allowed.sha256,'served-file-changed');rec.servedRequests.push(allowed);
    await route.fulfill({status:200,contentType:relative.endsWith('.html')?'text/html':relative.endsWith('.js')?'application/javascript':relative.endsWith('.json')?'application/json':'application/octet-stream',body:b});
   });
   await page.goto(origin+'/research/m31-browser-screen-2026-10-16/source/browser.html',{waitUntil:'load'});
   await page.waitForFunction(()=>typeof window.runBrowserExperiment==='function');
   rec.pageEnvironment=await page.evaluate(()=>({visibilityState:document.visibilityState,crossOriginIsolated,hardwareConcurrency:navigator.hardwareConcurrency,userAgent:navigator.userAgent}));
   const executionConfig={...config,browserProcessId:id,runtimeEvidence:{browserVersion:rec.browserVersion,browserRuntime:rec.browserRuntime,launchArguments:rec.launchArguments,profileIdentitySha256:rec.profileIdentitySha256,environment:rec.environmentStart},sourceBundle:JSON.parse(fs.readFileSync(path.join(__dirname,'source-bundle.json')))};
   rec.executionConfigJSON=JSON.stringify(executionConfig);rec.executionConfigSha256=sha(rec.executionConfigJSON);
   const result=await page.evaluate(async({c,i})=>await window.runBrowserExperiment(c,i),{c:executionConfig,i:index});
   rec.pageResult=result;assert(result&&result.complete===true,'page-science-incomplete');assert(!pending,'unfinished-transport');
   for(const x of sharedPins){const now=pin(path.join(p,x.path),x.path);assert(now.bytes===x.bytes&&now.sha256===x.sha256,'shared-input-mutated');}
   rec.inputsVerified=true;rec.complete=true;rec.pageResult=result;assert(rec.errors.length===0,'page-errors');
  }catch(e){rec.errors.push(e.message&&/^[A-Za-z0-9 _:.=-]{1,150}$/.test(e.message)?e.message:'controller-exception-'+e.name);failed=true;}
  finally{
   if(pending){try{fs.fsyncSync(pending.fd);fs.closeSync(pending.fd);}catch(_){}rec.errors.push('unfinished-artifact');pending=null;}
   if(browser){try{await Promise.race([browser.close(),delay(20000).then(()=>{throw Error('browser-close-timeout');})]);rec.browserClosed=true;}catch(_){rec.errors.push('browser-close-failure');failed=true;}browser=null;}
   try{const ack=await barrier(id);rec.allOwnedBrowserProcessesAbsent=ack.allOwnedBrowserProcessesAbsent;rec.closureConfirmed=ack.allOwnedBrowserProcessesAbsent;rec.supervisorObservation=ack;}catch(_){rec.errors.push('closure-barrier-failure');failed=true;}
   clearTimeout(timer);rec.elapsedSeconds=(performance.now()-started)/1000;rec.artifactBytes=bytesWritten;rec.transportPending=false;rec.environmentEnd=env();
   if(rec.elapsedSeconds>900){rec.errors.push('final-slot-wall-cap');failed=true;}
   rec.scientificScheduleComplete=rec.complete;rec.complete=Boolean(rec.complete&&rec.runtimeIdentityVerified&&rec.inputsVerified&&!rec.transportPending&&rec.browserClosed&&rec.closureConfirmed&&rec.allOwnedBrowserProcessesAbsent&&rec.errors.length===0);if(!rec.complete)failed=true;
   json(path.join(output,'closure.json'),rec);active=null;
  }
  if(failed)break;
 }
 const attempted=config.processes.filter(id=>fs.existsSync(path.join(p,'runs',id,'invocation.lock')));
 json(path.join(p,'results/campaign.json'),{complete:!failed&&attempted.length===3,attempted,notAttempted:config.processes.filter(id=>!attempted.includes(id)),sourcePins,sharedPins,scientificCallsAddedOutsidePage:0});
 if(failed)process.exitCode=1;
})().catch(e=>{process.stderr.write('controller-terminal-'+e.name+'\n');process.exitCode=1;});
