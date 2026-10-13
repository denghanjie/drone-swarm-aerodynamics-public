'use strict';
/* INDEPENDENT DEFERRED IO FIXTURES. No production or reviewer file is modified:
 * implementation io.cjs is loaded against an in-memory, fault-injecting FS.
 * This still counts as fixture execution and requires the shared window. */
if(process.env.JOINT_REFERENCE_WINDOW_ACTIVE!=='1')throw Error('Coordinator-authorized numerical window required');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'../implementation'),accounting=path.resolve(root,'..');
const records=[];
function test(name,fn){try{fn();records.push({name,passed:true});}catch(e){records.push({name,passed:false,error:{name:e.name,message:e.message,stack:e.stack}});}}
class MemoryFs {
 constructor(){this.files=new Map();this.dirs=new Set([accounting,root]);this.fds=new Map();this.nextfd=5;this.failWriteAfter=null;this.failRename=false;this.fsyncs=[];this.writeAttempts=0;}
 normalize(p){return path.resolve(typeof p==='number'?this.fds.get(p):p);}
 seed(relative,body,size){const p=path.resolve(root,relative);this.files.set(p,{body:Buffer.from(body),size:size??Buffer.byteLength(body)});this.mkdirSync(path.dirname(p));return p;}
 existsSync(p){p=this.normalize(p);return this.files.has(p)||this.dirs.has(p);}
 mkdirSync(p){p=this.normalize(p);while(p.startsWith(accounting)){this.dirs.add(p);if(p===accounting)break;p=path.dirname(p);}}
 readdirSync(p,{withFileTypes}={}){p=this.normalize(p);const entries=new Map();for(const d of this.dirs)if(path.dirname(d)===p)entries.set(path.basename(d),true);for(const f of this.files.keys())if(path.dirname(f)===p)entries.set(path.basename(f),false);return [...entries].map(([name,dir])=>withFileTypes?{name,isDirectory:()=>dir}:name);}
 statSync(p){p=this.normalize(p);if(this.dirs.has(p))return {size:0,isDirectory:()=>true};const f=this.files.get(p);if(!f)throw Error('ENOENT');return {size:f.size,isDirectory:()=>false};}
 openSync(p,mode){p=this.normalize(p);if(mode==='wx'){if(this.existsSync(p))throw Error('EEXIST');this.files.set(p,{body:Buffer.alloc(0),size:0});}else if(!this.existsSync(p))throw Error('ENOENT');const fd=this.nextfd++;this.fds.set(fd,p);return fd;}
 writeFileSync(fd,body){this.writeAttempts++;const p=this.normalize(fd),b=Buffer.from(body);if(this.failWriteAfter!==null){const prefix=b.subarray(0,this.failWriteAfter);this.files.set(p,{body:Buffer.from(prefix),size:prefix.length});throw Error('INJECTED_PARTIAL_WRITE');}this.files.set(p,{body:b,size:b.length});}
 readFileSync(p,encoding){const b=Buffer.from(this.files.get(this.normalize(p)).body);return encoding?b.toString(encoding):b;}
 fsyncSync(fd){this.fsyncs.push(this.normalize(fd));}
 closeSync(fd){this.fds.delete(fd);}
 renameSync(from,to){if(this.failRename)throw Error('INJECTED_RENAME_FAILURE');from=this.normalize(from);to=this.normalize(to);const f=this.files.get(from);assert.ok(f);this.files.set(to,f);this.files.delete(from);}
}
function loadIO(mem){const filename=path.join(root,'src/io.cjs'),module={exports:{}};vm.runInNewContext(fs.readFileSync(filename,'utf8'),{module,exports:module.exports,__dirname:path.dirname(filename),Buffer,process,require(id){if(id==='fs')return mem;if(id==='path')return path;if(id==='crypto')return crypto;throw Error('Unexpected dependency '+id);}},{filename});return module.exports;}
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');

test('raw byte encoding and checksum round-trip are exact little-endian Float64',()=>{
 const mem=new MemoryFs(),io=loadIO(mem),rows=[[0,-0,Math.PI,Number.MIN_VALUE]];
 const b=io.rawBytes(rows);assert.equal(b.length,32);assert.ok(Object.is(b.readDoubleLE(8),-0));assert.equal(b.readDoubleLE(16),Math.PI);assert.equal(b.readDoubleLE(24),Number.MIN_VALUE);
 const p=mem.seed('tests/inmemory.f64',b),r=io.readRaw(p,{shape:[1,1,4],bytes:32,sha256:hash(b)});assert.equal(r.row(0)[2],Math.PI);assert.ok(Object.is(r.row(0)[1],-0));
});

test('raw checksum, truncated data, malformed shapes and out-of-range samples fail closed',()=>{
 const mem=new MemoryFs(),io=loadIO(mem),b=io.rawBytes([[1,2,3,4]]),p=mem.seed('tests/inmemory.f64',b),meta={shape:[1,1,4],bytes:32,sha256:hash(b)};
 const r=io.readRaw(p,meta);for(const i of [-1,1,.5,NaN,Infinity])assert.throws(()=>r.row(i));
 for(const shape of [[],[1,4],[2,1,4],[1,0,4],[1,1,3.5]])assert.throws(()=>io.readRaw(p,{...meta,shape}));
 assert.throws(()=>io.readRaw(p,{...meta,sha256:'0'.repeat(64)}));mem.seed('tests/inmemory.f64',b.subarray(0,24));assert.throws(()=>io.readRaw(p,meta));
});

test('metadata cannot override computed raw identity',()=>{
 const mem=new MemoryFs(),io=loadIO(mem),rows=[Array(17).fill(0)];
 for(const key of ['path','encoding','shape','bytes','sha256'])assert.throws(()=>io.writeRaw('results/raw/one.f64',rows,{count:1,[key]:'untrusted'}));
 assert.equal(mem.writeAttempts,0);
});

test('atomic write syncs payload and containing directory and preserves exact bytes',()=>{
 const mem=new MemoryFs(),io=loadIO(mem),p=mem.seed('results/old.json','OLD'),body=Buffer.from('NEW');
 assert.equal(io.atomicWrite('results/old.json',body),p);assert.equal(mem.readFileSync(p,'utf8'),'NEW');assert.equal(mem.existsSync(p+'.partial'),false);
 assert.ok(mem.fsyncs.includes(p+'.partial'));assert.ok(mem.fsyncs.includes(path.dirname(p)));
});

test('mid-write interruption preserves prior durable file and raw partial bytes',()=>{
 const mem=new MemoryFs(),io=loadIO(mem),p=mem.seed('results/old.json','OLD');mem.failWriteAfter=2;
 assert.throws(()=>io.atomicWrite('results/old.json',Buffer.from('NEW-CONTENT')),/INJECTED_PARTIAL_WRITE/);
 assert.equal(mem.readFileSync(p,'utf8'),'OLD');assert.equal(mem.readFileSync(p+'.partial','utf8'),'NE');assert.equal(io.retainedBytes(),5);
 mem.failWriteAfter=null;assert.throws(()=>io.atomicWrite('results/old.json',Buffer.from('RETRY')),/EEXIST/);
 assert.equal(mem.readFileSync(p+'.partial','utf8'),'NE');
});

test('rename interruption keeps old durable file and full partial candidate',()=>{
 const mem=new MemoryFs(),io=loadIO(mem),p=mem.seed('results/old.json','OLD');mem.failRename=true;
 assert.throws(()=>io.atomicWrite('results/old.json',Buffer.from('NEW-CONTENT')),/INJECTED_RENAME_FAILURE/);
 assert.equal(mem.readFileSync(p,'utf8'),'OLD');assert.equal(mem.readFileSync(p+'.partial','utf8'),'NEW-CONTENT');
});

test('allocation includes replacement temporary duplicate and preserves failure reserve',()=>{
 const mem=new MemoryFs(),io=loadIO(mem),normal=io.HARD_CAP-io.FAILURE_RESERVE;
 mem.seed('../charged-existing','x',normal-10);mem.seed('results/old','OLD',3);
 assert.throws(()=>io.atomicWrite('results/old',Buffer.alloc(8)),/cap/i);assert.equal(mem.writeAttempts,0);
 const p=io.reserve('results/failures/small',20,{emergency:true});assert.equal(p,path.join(root,'results/failures/small'));
 assert.throws(()=>io.reserve('results/failures/too-large',io.FAILURE_RESERVE+100,{emergency:true}),/cap/i);
});

test('retained-byte accounting counts duplicate forms and partial files independently',()=>{
 const mem=new MemoryFs(),io=loadIO(mem);mem.seed('../inputs/raw','abc',111);mem.seed('../inputs/transport','def',99);mem.seed('results/file.partial','ghi',7);assert.equal(io.retainedBytes(),217);
 assert.throws(()=>io.reserve('../escape',1),/escapes/);
});

test('nonfinite failure fields survive JSON explicitly without silent null coercion',()=>{
 const mem=new MemoryFs(),io=loadIO(mem),p=io.save('results/failures/guard.json',{raw:[NaN,Infinity,-Infinity],exactStoppedState:true});
 const parsed=JSON.parse(mem.readFileSync(p,'utf8'));assert.equal(parsed.raw[0].nonfinite,'NaN');assert.equal(parsed.raw[1].nonfinite,'Infinity');assert.equal(parsed.raw[2].nonfinite,'-Infinity');assert.equal(parsed.exactStoppedState,true);
});

const report={schema:'independent-io-fault-fixtures/v1',kind:'in-memory fault injection, no genuine Boids trajectory',tests:records,passed:records.every(x=>x.passed)};
process.stdout.write(JSON.stringify(report)+'\n');if(!report.passed)process.exitCode=1;
