'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const spec=require('./spec.json'),contract=require('./result-contract.json'),adapter=require('./adapter.cjs'),methods=require('./methods.cjs');
const output=process.env.RESEARCH_RESULT_PATH;if(!output)throw Error('RESEARCH_RESULT_PATH required');
const LIMIT=128*1024*1024;let journalBytes=0;
function encode(v){return JSON.stringify(v)+'\n';}
function cap(v,n,label){if(Buffer.byteLength(JSON.stringify(v))>n)throw Error('Output field cap: '+label);}
function boundedStrings(v){if(typeof v==='string'){if(v.length>4096)throw Error('Output string cap');}else if(v&&typeof v==='object')for(const x of Object.values(v))boundedStrings(x);}
function fixed(v){if(typeof v==='string'&&v.length>108)throw Error('Fixed96 integer string cap');if(v&&typeof v==='object')for(const x of Object.values(v))fixed(x);}
function checkRecord(row){
 boundedStrings(row);
 for(const m of row.methods){
  for(const n of m.assembly.tree?.nodes??[]){cap(n,8192,'tree node');for(const b of [n.center,n.axis])for(const ends of b)for(const q of ends)if(q.n.length>310||q.d.length>324)throw Error('Tree rational field cap');}
  for(const q of m.assembly.queries)for(const t of q.terminals)for(const e of t.entries??[]){cap(e,384,'compact entry');if(e.result.coefficient)fixed(e.result.coefficient);}
  for(const r of m.certificate?.rows??[]){cap(r,1024,'certificate row');fixed(r);}
  for(const l of m.certificate?.loads??[]){cap(l,96*1024,'load');fixed(l.bounds);fixed(l.error);}
  if(m.certificate){fixed(m.certificate.Kbar);fixed(m.certificate.maxErrors);}
 }
}
const journal=fs.openSync(output+'.jsonl','wx');
function append(v){const line=encode(v),size=Buffer.byteLength(line);if(journalBytes+size>LIMIT)throw Error('Journal128MiB cap');fs.writeSync(journal,line);fs.fsyncSync(journal);journalBytes+=size;}
append({kind:'header',schema:contract.journalSchema,specId:spec.id});
const records=[];
for(const scene of spec.scenes){const row=methods.solve(scene);checkRecord(row);records.push(row);append({kind:'record',row});}
if(records.length!==spec.expectedRecords)throw Error('Allocation mismatch');
append({kind:'complete',records:records.length});fs.closeSync(journal);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const doc={schema:contract.schema,specId:spec.id,runtime:{node:process.version,v8:process.versions.v8,platform:process.platform,arch:process.arch},sourceSha256:Object.fromEntries(contract.sourceFiles.map(n=>[n,sha(fs.readFileSync(path.join(__dirname,n)))])),constants:adapter.constantBits,records};
const bytes=encode(doc);if(Buffer.byteLength(bytes)>LIMIT)throw Error('Result128MiB cap');
fs.writeFileSync(output,bytes,{flag:'wx'});
console.log(JSON.stringify({records:records.length,statuses:records.reduce((m,r)=>{for(const method of r.methods){const key=method.name+':'+method.result.status;m[key]=(m[key]||0)+1;}return m;},{})}));
