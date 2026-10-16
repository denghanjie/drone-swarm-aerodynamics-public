'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const spec=require('./spec.json'),contract=require('./result-contract.json'),adapter=require('./adapter.cjs'),coupled=require('./coupled.cjs');
const output=process.env.RESEARCH_RESULT_PATH;if(!output)throw Error('RESEARCH_RESULT_PATH required');
const journal=fs.openSync(output+'.jsonl','wx');
function append(v){fs.writeSync(journal,JSON.stringify(v)+'\n');fs.fsyncSync(journal);}
append({kind:'header',schema:contract.journalSchema,specId:spec.id});
const records=[];
for(const scene of spec.scenes){const row=coupled.solve(scene);records.push(row);append({kind:'record',row});}
if(records.length!==spec.expectedRecords)throw Error('Allocation mismatch');
append({kind:'complete',records:records.length});fs.closeSync(journal);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const doc={schema:contract.schema,specId:spec.id,runtime:{node:process.version,v8:process.versions.v8,platform:process.platform,arch:process.arch},sourceSha256:Object.fromEntries(contract.sourceFiles.map(n=>[n,sha(fs.readFileSync(path.join(__dirname,n)))])),constants:adapter.constantBits,records};
fs.writeFileSync(output,JSON.stringify(doc,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify({records:records.length,statuses:records.reduce((m,r)=>{m[r.result.status]=(m[r.result.status]||0)+1;return m;},{})}));
