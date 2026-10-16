'use strict';
// Deliberate containment adaptation: Chrome joins the retained guardian's group.
// No numerical or browser scheduler flags are changed here.
const fs=require('node:fs'),cp=require('node:child_process'),path=require('node:path'),crypto=require('node:crypto');
const runtime=JSON.parse(fs.readFileSync(path.join(__dirname,'../runtime.json'))),launcher='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',launcherPin=runtime.chrome.files.find(x=>x.label==='launcher');
const privateDir=process.env.RESEARCH_SUPERVISOR_DIR;
if(!privateDir||!path.isAbsolute(privateDir))throw Error('private supervisor directory required');
const original=cp.spawn,entries=[];
cp.spawn=function(command,args,options){
 if(typeof command!=='string'||!command.endsWith('/Google Chrome'))throw Error('undeclared spawned executable');
 if(fs.realpathSync(command)!==fs.realpathSync(launcher))throw Error('unfrozen Chrome path');
 const binary=fs.readFileSync(command);if(binary.length!==launcherPin.bytes||crypto.createHash('sha256').update(binary).digest('hex')!==launcherPin.sha256)throw Error('unfrozen Chrome launcher');
 const profile=args.find(x=>typeof x==='string'&&x.startsWith('--user-data-dir='));
 if(!profile||entries.some(e=>e.profileArgument===profile))throw Error('missing or reused browser profile');
 const adjusted={...options,detached:false},child=original.call(this,command,args,adjusted);
 const entry={pid:child.pid,executable:command,profileArgument:profile,args,detachedRequested:options?.detached===true,detachedApplied:false};
 try{fs.appendFileSync(path.join(privateDir,'browser-registry.jsonl'),JSON.stringify(entry)+'\n');entries.push(entry);}catch(e){try{child.kill('SIGKILL');}catch(_){}throw e;}
 return child;
};
module.exports={entries};
