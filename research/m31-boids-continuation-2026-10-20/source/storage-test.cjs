'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {Journal}=require('./journal.cjs');
const out=path.resolve(__dirname,'../storage'),start=performance.now();let charged=0;
const guard=()=>assert.ok(performance.now()-start<15000,'storage-fixture-wall');
const charge=n=>{charged+=n;assert.ok(charged<8*1024*1024,'storage-fixture-cap');};
const j=new Journal(out,'fixture.jsonl.gz',{guard,charge,maxRecordBytes:32768,blockBytes:65536,partBytes:32768});
const expected=fs.openSync(path.join(out,'expected.jsonl'),'wx');let x=20261020;
for(let i=0;i<40;i++){const bytes=Buffer.alloc(8192);for(let k=0;k<bytes.length;k++){x=(Math.imul(x,1664525)+1013904223)>>>0;bytes[k]=x>>>24;}const record={sequence:i,kind:'storage-fixture',body:{payload:bytes.toString('hex'),signedZeroWord:'8000000000000000',label:'Unicode Δ and escaped newline\n'}};const raw=Buffer.from(JSON.stringify(record)+'\n');let offset=0;while(offset<raw.length)offset+=fs.writeSync(expected,raw,offset,raw.length-offset);j.append(record);}
fs.fsyncSync(expected);fs.closeSync(expected);const identity=j.finish();assert.ok(identity.parts.length>1);const checks=[];
const over=new Journal(out,'oversize.jsonl.gz',{guard,charge,maxRecordBytes:8,blockBytes:8,partBytes:8});assert.throws(()=>over.append({oversize:'123456789'}),/record-size-budget/);over.closeIncomplete();checks.push('oversize raw record refused before persistence');
const budget=new Journal(out,'budget.jsonl.gz',{guard,charge(){throw Error('fixture-budget-refused');},maxRecordBytes:128,blockBytes:128,partBytes:16});budget.append({value:'preserve failed fixture'});assert.throws(()=>budget.finish(),/fixture-budget-refused/);budget.closeIncomplete();checks.push('compressed output budget refusal propagates');
assert.ok(!fs.readdirSync(out).some(x=>x.startsWith('budget.')||x.startsWith('oversize.')));
fs.writeFileSync(path.join(out,'fixture-index.json'),JSON.stringify({identity,checks,charged,source:'deterministic storage-only bytes; zero scientific modules'})+'\n',{flag:'wx'});
