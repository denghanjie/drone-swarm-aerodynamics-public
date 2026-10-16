'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const [pkg,mode,id,arm,repetitionText,inputPath,outputName]=process.argv.slice(2);
if(process.argv.length!==9||path.resolve(pkg)!==path.resolve(__dirname,'..')||process.env.RESEARCH_SUPERVISION_STAGE!=='kernel-worker'||!['baseline','candidate'].includes(arm)||!['control','scheduled','lifetime'].includes(mode)||!/^\d$/.test(repetitionText))throw Error('Worker invocation mismatch');
if(Date.now()>=Date.parse('2026-10-16T23:00:00Z'))throw Error('Worker launch cutoff reached');
const root=path.resolve(pkg,'../..'),results=path.join(pkg,'results'),manifestPath=process.env.RESEARCH_SOURCE_MANIFEST_PATH;
const mb=fs.readFileSync(manifestPath),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
if(sha(mb)!==process.env.RESEARCH_EXPECTED_MANIFEST_SHA256||!/^[a-f0-9]{40}$/.test(process.env.RESEARCH_SOURCE_COMMIT||''))throw Error('Worker source identity');
for(const pin of JSON.parse(mb).files){const b=fs.readFileSync(path.join(root,pin.path));if(b.length!==pin.bytes||sha(b)!==pin.sha256)throw Error('Worker source changed');}
const output=path.resolve(results,outputName);
if(!output.startsWith(results+path.sep)||fs.existsSync(output)||process.env.NODE_OPTIONS||process.env.NODE_PATH)throw Error('Worker output or runtime mismatch');
const M=require('./'+arm+'/methods.cjs'),C=require('./baseline/canonical.cjs');
function freeze(input){return Object.freeze({drones:Object.freeze(input.drones.map(d=>Object.freeze({id:d.id,state:Object.freeze([...d.state])})))});}
function evaluate(input,identifier,kind){
 input=freeze(input);let method=null,error=null;const phases=[],start=process.hrtime.bigint();
 try{method=M.method(input,'filtered',name=>phases.push({name,offsetNs:String(process.hrtime.bigint()-start)}));}
 catch(e){error={name:e.name,message:String(e.message).split(root).join('REPOSITORY')};}
 const methodNs=String(process.hrtime.bigint()-start);
 return {id:identifier,kind,arm,repetition:Number(repetitionText),input,method,error,methodNs,phases};
}
let record;
if(mode==='lifetime'){
 const a=JSON.parse(fs.readFileSync(path.join(results,'inputs/lifetime-a.json'))),b=JSON.parse(fs.readFileSync(path.join(results,'inputs/lifetime-b.json')));
 record={arm,records:[evaluate(a,'lifetime-a','lifetime'),evaluate(b,'lifetime-b','lifetime'),evaluate(a,'lifetime-a','lifetime')]};
}else{
 if(!inputPath.startsWith('research/m31-normalizer-ablation-2026-10-17/results/inputs/')||inputPath.includes('..'))throw Error('Worker input path');
 record=evaluate(JSON.parse(fs.readFileSync(path.join(root,inputPath))),id,mode);
}
const bytes=Buffer.from(C.encode(record)+'\n');if(bytes.length>33554432)throw Error('Worker output budget');
const fd=fs.openSync(output,'wx',0o600);try{fs.writeFileSync(fd,bytes);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}
const dir=fs.openSync(path.dirname(output),'r');try{fs.fsyncSync(dir);}finally{fs.closeSync(dir);}
if(mode==='lifetime'?record.records.some(r=>r.error):record.error)process.exitCode=1;
