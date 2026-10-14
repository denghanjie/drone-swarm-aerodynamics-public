'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const ROOT=path.resolve(__dirname,'..'),ACCOUNTING_ROOT=path.resolve(ROOT,'..');
const HARD_CAP=200000000,FAILURE_RESERVE=2000000;
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const fileSha=p=>sha(fs.readFileSync(p));
const nonfinite=(_k,v)=>typeof v==='number'&&!Number.isFinite(v)?{nonfinite:String(v)}:v;
function retainedBytes(){let n=0;function walk(p){for(const e of fs.readdirSync(p,{withFileTypes:true})){const f=path.join(p,e.name);if(e.isDirectory())walk(f);else n+=fs.statSync(f).size;}}walk(ACCOUNTING_ROOT);return n;}
// All new raw artifacts are uncompressed; preserved transport fragments count
// at actual retained bytes in addition to their separately retained raw arrays.
function reserve(relative,bytes,{emergency=false}={}){const p=path.resolve(ROOT,relative);if(!p.startsWith(ROOT+path.sep))throw Error('Output escapes implementation root');const previous=fs.existsSync(p)?fs.statSync(p).size:0,projected=retainedBytes()-previous+bytes,limit=HARD_CAP-(emergency?0:FAILURE_RESERVE);if(projected>limit)throw Object.assign(Error('Logical retained-byte cap'),{detail:{relative,projected,limit}});return p;}
function atomicWrite(relative,body,{emergency=false}={}){const p=reserve(relative,body.length,{emergency}),tmp=relative+'.partial';reserve(tmp,body.length,{emergency});fs.mkdirSync(path.dirname(p),{recursive:true});const fd=fs.openSync(path.join(ROOT,tmp),'wx');try{fs.writeFileSync(fd,body);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}fs.renameSync(path.join(ROOT,tmp),p);const d=fs.openSync(path.dirname(p),'r');try{fs.fsyncSync(d);}finally{fs.closeSync(d);}return p;}
function save(relative,value,{emergency=relative.startsWith('results/failures/')}={}){const body=Buffer.from(JSON.stringify(value,nonfinite,2)+'\n');return atomicWrite(relative,body,{emergency});}
function load(relative){return JSON.parse(fs.readFileSync(path.resolve(ROOT,relative),'utf8'));}
function rawBytes(rows){const b=Buffer.alloc(rows.reduce((n,r)=>n+r.length*8,0));let p=0;for(const r of rows)for(const v of r){b.writeDoubleLE(v,p);p+=8;}return b;}
function writeRaw(relative,rows,metadata){if(['path','encoding','shape','bytes','sha256'].some(k=>Object.hasOwn(metadata,k)))throw Error('Reserved raw metadata key');if(!Number.isInteger(metadata.count)||rows.some(r=>r.length!==metadata.count*17))throw Error('Raw shape mismatch');const b=rawBytes(rows);atomicWrite(relative,b);const m={...metadata,path:relative,encoding:'little-endian Float64, uncompressed',shape:[rows.length,metadata.count,17],bytes:b.length,sha256:sha(b)};save(relative+'.json',m);return m;}
function readRaw(p,meta){if(!Array.isArray(meta.shape)||meta.shape.length!==3||meta.shape.some(x=>!Number.isSafeInteger(x)||x<1)||meta.shape.reduce((a,b)=>a*b,8)!==meta.bytes)throw Error('Malformed raw shape/bytes');const b=fs.readFileSync(p);if(b.length!==meta.bytes||sha(b)!==meta.sha256)throw Error('Raw identity mismatch');return {buffer:b,row(n){if(!Number.isInteger(n)||n<0||n>=meta.shape[0])throw Error('Raw row out of bounds');const width=meta.shape[1]*meta.shape[2],a=new Array(width);for(let k=0;k<width;k++)a[k]=b.readDoubleLE((n*width+k)*8);return a;}};}
function states(row,n=16){return Array.from({length:n},(_,i)=>Array.from(row.slice(i*17,(i+1)*17)));}
function manifest(){const files=[];for(const base of ['src','snapshot','configs','tests','demo']){function walk(relative){for(const f of fs.readdirSync(path.join(ROOT,relative)).sort()){const rel=path.join(relative,f);if(rel==='demo/records.json')continue;if(fs.statSync(path.join(ROOT,rel)).isDirectory())walk(rel);else files.push({path:rel,sha256:fileSha(path.join(ROOT,rel))});}}walk(base);}return {files,aggregate:sha(JSON.stringify(files))};}
module.exports={ROOT,ACCOUNTING_ROOT,HARD_CAP,FAILURE_RESERVE,sha,fileSha,save,load,reserve,atomicWrite,rawBytes,writeRaw,readRaw,states,manifest,retainedBytes};
