'use strict';
// The oracle source and its aerodynamic dependency are never edited or reimplemented.
const fs=require('fs'),path=require('path'),Module=require('module'),crypto=require('crypto');
const STUDY=path.resolve(__dirname,'../..'),WORKSPACE=path.resolve(STUDY,'..'),OLD=path.join(WORKSPACE,'research-next/implementation');
const EXPECTED='41ad1b087b1d7ba77f37d9c99b61e8a7c398915c6cfa3a74ef496258de8a822a';
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function treeBytes(root){if(!fs.existsSync(root))return 0;let n=0;for(const e of fs.readdirSync(root,{withFileTypes:true})){const p=path.join(root,e.name);if(e.isSymbolicLink())throw Error('Symbolic link in accounting root');n+=e.isDirectory()?treeBytes(p):fs.statSync(p).size;}return n;}
function storage(extra=0,emergency=false){const study=treeBytes(STUDY),old=treeBytes(path.join(WORKSPACE,'research-next'));if(study+extra>16000000-(emergency?0:2000000)||study+old+extra>200000000-(emergency?0:2000000))throw Object.assign(Error('Logical retained-byte cap'),{resourceLimited:true,detail:{study,old,extra,emergency}});}
function compile(source,filename,overrides){const mod=new Module(filename,module);mod.filename=filename;mod.paths=Module._nodeModulePaths(path.dirname(filename));const native=Module.createRequire(filename);mod.require=name=>Object.hasOwn(overrides,name)?overrides[name]:native(name);mod._compile(source,filename);return mod.exports;}
function createIO(root){
 root=path.resolve(root);if(!root.startsWith(path.join(STUDY,'implementation/results')+path.sep))throw Error('I/O root must remain inside isolated results tree');
 const original=fs.readFileSync(path.join(OLD,'src/io.cjs'),'utf8');
 const target="const ROOT=path.resolve(__dirname,'..'),ACCOUNTING_ROOT=path.resolve(ROOT,'..');";
 if(original.split(target).length!==2)throw Error('Frozen I/O declaration mismatch');
 const redirected=original.replace(target,`const ROOT=${JSON.stringify(root)},ACCOUNTING_ROOT=${JSON.stringify(STUDY)};`);
 const io=compile(redirected,path.join(OLD,'src/io.cjs'),{});
 // Preserve original reserve/append/fsync/atomic rename/JSON/raw encodings; add only study resource checks.
 const atomic=io.atomicWrite,save=io.save,reserve=io.reserve;
 io.reserve=(relative,bytes,opts={})=>{const p=path.resolve(root,relative),previous=fs.existsSync(p)?fs.statSync(p).size:0;storage(Math.max(0,bytes-previous),!!opts.emergency);return reserve(relative,bytes,opts);};
 io.atomicWrite=(relative,body,opts={})=>{storage(body.length*2,!!opts.emergency);return atomic(relative,body,opts);};
 io.save=(relative,value,opts={})=>{const emergency=opts.emergency===undefined?relative.startsWith('results/failures/'):opts.emergency;const body=Buffer.from(JSON.stringify(value,(_k,v)=>typeof v==='number'&&!Number.isFinite(v)?{nonfinite:String(v)}:v,2)+'\n');storage(body.length*2,emergency);return save(relative,value,opts);};
 return io;
}
function loadAudit(variant,root,{prepare=null}={}){
 const oracle=fs.readFileSync(path.join(OLD,'src/branch-audit.cjs'));if(sha(oracle)!==EXPECTED)throw Error('Frozen oracle changed');
 const M=require(path.join(OLD,'src/exact-aero.cjs'));
 const aero=prepare?{...M,prepare}:M,io=createIO(root),file=variant==='B'?path.join(OLD,'src/branch-audit.cjs'):path.join(__dirname,'branch-audit-c1.cjs');
 if(!['B','C1'].includes(variant))throw Error('Unknown audit variant');
 return {audit:compile(fs.readFileSync(file,'utf8'),file,{'./exact-aero.cjs':aero,'./io.cjs':io}),io,M};
}
module.exports={loadAudit,createIO,sha,treeBytes,storage,STUDY,WORKSPACE,OLD};
