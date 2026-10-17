'use strict';
// Host persistence only, invoked after caller's authorization/source gates.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const NAME='research/m31-native-tree-browser-probe-2026-10-17',MiB=1048576;
const LIMITS=Object.freeze({file:32*MiB,total:256*MiB,evidence:160*MiB,private:64*MiB,downstream:30*MiB,closure:2*MiB,chunk:MiB,descriptor:2*MiB});
const need=(v,c)=>{if(!v)throw Error('store-'+c);},sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function createStore(root,privateDir,guard=()=>{}){
 const results=path.join(root,NAME,'results'),shards=path.join(results,'shards');
 need(path.isAbsolute(privateDir)&&fs.realpathSync(privateDir)===privateDir&&!privateDir.startsWith(root+path.sep)&&privateDir!==root,'private-path');
 if(!fs.existsSync(shards))fs.mkdirSync(shards);let persistenceMilliseconds=0,newBytes=0,deduplicatedBytes=0;
 function total(directory,privateMode=false){let n=0;for(const e of fs.readdirSync(directory,{withFileTypes:true})){const f=path.join(directory,e.name);if(e.isSymbolicLink()){need(privateMode,'result-symlink');n+=fs.lstatSync(f).size;continue;}if(e.isDirectory())n+=total(f,privateMode);else{const st=fs.statSync(f);need(st.isFile()&&st.size<=LIMITS.file,'file-cap');n+=st.size;}}return n;}
 function evidence(){let n=0;for(const name of ['shards','records','saved-records']){const p=path.join(results,name);if(fs.existsSync(p))n+=total(p);}return n;}
 function budget(add){guard();const privateBytes=total(privateDir,true);need(privateBytes<=LIMITS.private,'private-cap');need(evidence()+add<=LIMITS.evidence,'evidence-cap');need(total(results)+privateBytes+add+LIMITS.closure<=LIMITS.total,'aggregate-cap');}
 function write(file,bytes){need(bytes.length<=LIMITS.file,'file-cap');budget(bytes.length);const fd=fs.openSync(file,'wx',0o600);try{fs.writeFileSync(fd,bytes);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}const d=fs.openSync(path.dirname(file),'r');try{fs.fsyncSync(d);}finally{fs.closeSync(d);}newBytes+=bytes.length;return {path:path.relative(root,file),bytes:bytes.length,sha256:sha(bytes)};}
 function put(bytes){const start=performance.now();bytes=Buffer.from(bytes);need(bytes.length>0&&bytes.length<=LIMITS.chunk,'chunk-size');const hash=sha(bytes),file=path.join(shards,hash+'.bin');let p;
  if(fs.existsSync(file)){const old=fs.readFileSync(file);need(old.length===bytes.length&&old.equals(bytes),'hash-collision-or-changed-shard');deduplicatedBytes+=bytes.length;p={path:path.relative(root,file),bytes:bytes.length,sha256:hash};}
  else p=write(file,bytes);persistenceMilliseconds+=performance.now()-start;return p;
 }
 function get(p){need(p.path===NAME+'/results/shards/'+p.sha256+'.bin'&&p.bytes>0&&p.bytes<=LIMITS.chunk,'shard-pin');const bytes=fs.readFileSync(path.join(root,p.path));need(bytes.length===p.bytes&&sha(bytes)===p.sha256,'shard-identity');return bytes;}
 function record(directory,label,value){const start=performance.now();need(['records','saved-records'].includes(directory)&&/^[a-zA-Z0-9-]{1,140}$/.test(label),'record-name');const dir=path.join(results,directory);if(!fs.existsSync(dir))fs.mkdirSync(dir);const bytes=Buffer.from(JSON.stringify(value)+'\n');need(bytes.length<=LIMITS.descriptor,'descriptor-cap');const pin=write(path.join(dir,label+'.json'),bytes);persistenceMilliseconds+=performance.now()-start;return pin;}
 return {put,get,record,budget,stats:()=>({newBytes,deduplicatedBytes,persistenceMilliseconds,scope:'Exact-byte dedup only; persistence time overlaps transfer and must not be added twice'})};
}
module.exports={createStore,LIMITS};
