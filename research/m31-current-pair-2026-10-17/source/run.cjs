'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const spec=require('./spec.json'),contract=require('./result-contract.json'),adapter=require('./adapter.cjs'),pair=require('./pair.cjs');
const output=process.env.RESEARCH_RESULT_PATH;if(!output)throw Error('RESEARCH_RESULT_PATH required');const journal=fs.openSync(output+'.jsonl','wx');
fs.writeSync(journal,JSON.stringify({kind:'header',schema:contract.journalSchema,specId:spec.id})+'\n');fs.fsyncSync(journal);
function inputOf(c){const receiver=spec.baseState.slice(),source=spec.baseState.slice();source.splice(0,3,...spec.defaultSourcePosition);for(const who of ['receiver','source'])for(const [field,[start,end]]of Object.entries(spec.overrides)){const v=c[who+field];if(v){if(v.length!==end-start)throw Error('bad fixture');(who==='receiver'?receiver:source).splice(start,end-start,...v);}}return {receiver:receiver.map(s=>adapter.bits(Number(s))),source:source.map(s=>adapter.bits(Number(s))),self:c.self===true,rotor:c.rotor??spec.defaultRotor};}
const records=[];for(const c of spec.cases){const input=inputOf(c),r=pair.query(input),row={id:c.id,input,...r};records.push(row);fs.writeSync(journal,JSON.stringify({kind:'record',row})+'\n');if(records.length%16===0)fs.fsyncSync(journal);}
if(records.length!==spec.expectedRecords)throw Error('Allocation mismatch');fs.writeSync(journal,JSON.stringify({kind:'complete',records:records.length})+'\n');fs.fsyncSync(journal);fs.closeSync(journal);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');const doc={schema:contract.schema,specId:spec.id,runtime:{node:process.version,v8:process.versions.v8,platform:process.platform,arch:process.arch},sourceSha256:Object.fromEntries(contract.sourceFiles.map(n=>[n,sha(fs.readFileSync(path.join(__dirname,n)))])),constants:adapter.constantBits,records};
fs.writeFileSync(output,JSON.stringify(doc,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify({records:records.length}));
