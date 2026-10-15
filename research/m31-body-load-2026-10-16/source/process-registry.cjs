'use strict';
// Instrument process creation before loading Playwright. Preserve its spawn options
// and return value: this records separately detached browser groups for supervision.
// Registry is a private, supervisor-created local file; no PID enters public science.
const fs=require('fs'),cp=require('child_process'),path=require('path');
const registry=process.env.RESEARCH_PROCESS_REGISTRY;
if(!registry||!path.isAbsolute(registry)||!fs.existsSync(registry))throw Error('Supervisor process registry required');
const entries=[],original=cp.spawn;
cp.spawn=function(command,args,options){
 const child=original.apply(this,arguments);
 const entry={pid:child.pid??null,detached:options?.detached===true,kind:typeof command==='string'&&command.endsWith('/Google Chrome')?'chrome':'auxiliary',ownership:{executable:typeof command==='string'?command:null,profileArgument:Array.isArray(args)?args.find(x=>typeof x==='string'&&x.startsWith('--user-data-dir='))??null:null}};
 try{fs.appendFileSync(registry,JSON.stringify(entry)+'\n');entries.push(entry);}
 catch(error){if(child.pid){try{process.kill(entry.detached?-child.pid:child.pid,'SIGKILL');}catch(_){}}throw error;}
 return child;
};
module.exports={hasRegisteredBrowser:()=>entries.some(e=>e.kind==='chrome'&&e.detached&&Number.isInteger(e.pid)&&e.pid>0&&e.ownership.profileArgument),summary:()=>({registeredProcesses:entries.length,registeredDetachedGroups:entries.filter(e=>e.detached&&e.pid).length,registeredBrowser:entries.some(e=>e.kind==='chrome'&&e.detached&&e.pid)})};
