'use strict';
// Standalone results reconstruction. Rebuild all coupled maxima and same-path
// loads from retained binary arrays rather than accepting the original summaries.
const fs=require('fs'),path=require('path');
const {ROOT,load,save,readSeries}=require('./io.cjs');
const {compare}=require('./coupled.cjs'),{referenceGate,validateFreeze}=require('./campaign.cjs'),{replayDriver}=require('./replay.cjs');
function reconstruct(){if(process.env.TEMPORAL_SUPERVISED!=='1'||!process.send)throw Error('Reconstruction is permitted only inside the original supervised campaign window');
 const totalDeadline=BigInt(process.env.TEMPORAL_TOTAL_DEADLINE_NS);let jobId=null,jobDeadline=null;const budgetCheck=()=>{const now=process.hrtime.bigint();if(now>totalDeadline-2000000000n||jobDeadline&&now>jobDeadline-1000000000n)throw Error('Audit cooperative deadline');};function begin(id){const at=process.hrtime.bigint();jobId=id;jobDeadline=at+45000000000n;process.send({type:'job-start',id,startMonotonicNs:String(at),deadlineMonotonicNs:String(jobDeadline)});}function end(){budgetCheck();process.send({type:'job-end',id:jobId});jobId=null;jobDeadline=null;}
 begin('raw-reconstruction');const {cfg}=validateFreeze(),campaign=load('results/campaign.json'),data=new Map();for(const id of campaign.runIds){budgetCheck();const r=load(`results/runs/${id}.json`),series=readSeries(r.commonStates.path,r.commonStates);if(series.manifest.shape[1]!==16||series.manifest.shape[2]!==17||series.manifest.shape[0]!==Math.floor(r.endTick/r.config.commonRecordTicks)+1||series.manifest.dt!==r.config.commonRecordTicks/6400||series.rows.some(row=>!row.every(Number.isFinite)))throw Error('Invalid common-state input/work contract');data.set(id,{result:r,common:series.rows});}
 const rows=[];for(const seed of cfg.seeds){const get=(p,a)=>data.get(`s${seed}-p${p}-a${a}`);if(get(4,4)&&get(2,4)&&get(1,4))rows.push({seed,type:'physics',...referenceGate(compare(get(4,4),get(2,4)),compare(get(2,4),get(1,4)),cfg.gates.physics,cfg.gates.comparisonFloors,1)});if(get(1,16)&&get(1,8)&&get(1,4))rows.push({seed,type:'air',...referenceGate(compare(get(1,16),get(1,8)),compare(get(1,8),get(1,4)),cfg.gates.airReference,cfg.gates.comparisonFloors,cfg.gates.airReferenceReduction)});}
 save('results/recomputed/reference-gates.json',rows);
 for(const row of rows){const recorded=(row.type==='physics'?campaign.gates.physics:campaign.gates.air).find(x=>x.seed===row.seed);const {type,...clean}=row;if(JSON.stringify(clean)!==JSON.stringify(recorded))throw Error('Independent raw reconstruction disagrees with recorded reference gate');}
 save('results/recomputed/verification.json',{passed:true,source:'retained hash-verified raw full17 arrays',referenceGateCount:rows.length});end();return rows;}
if(require.main===module)throw Error('Standalone numerical recomputation is disabled by the frozen resource scope. Reconstruct inside the original supervised campaign window only.');
module.exports={reconstruct};
