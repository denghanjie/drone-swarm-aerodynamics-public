'use strict';
const fs=require('fs'),path=require('path');
const {ROOT,reserve,sha,save}=require('./io.cjs'),{B}=require('./controller.cjs');
const fields=['command0','command1','command2','command3','neighborMask','pairMask','wallMask','steeringSpeed','desiredHorizontalSpeedNorm','torqueErrorScalar','tiltExcess','saturated','motorBoundsBase3','speedAtLimit','wallRepairIterations','wallRepairConverged','pairResidual','wallResidual'];
const mask=ids=>ids.reduce((m,i)=>m+2**i,0);
function writeControllers(id,events){
 const b=Buffer.alloc(events.length*16*fields.length*8);let offset=0;
 for(const event of events)for(const r of event.rows){const s=r.signature,values=[...r.commands,mask(s.neighbors),mask(s.pairs),mask(s.walls.map(id=>B.course.boxes.findIndex(b=>b.id===id))),r.steeringSpeed,r.desiredHorizontalSpeedNorm,r.torqueErrorScalar,r.tiltExcess,+r.saturated,s.motorBounds.reduce((n,v,i)=>n+(v+1)*3**i,0),+s.speedAtLimit,s.wallRepairIterations,s.wallRepairConverged===null?-1:+s.wallRepairConverged,r.pairResidual,r.wallResidual];for(const value of values){if(!Number.isFinite(value))throw Error('Nonfinite controller diagnostic');b.writeDoubleLE(value,offset);offset+=8;}}
 const relative=`results/controllers/${id}.f64`;require('./io.cjs').atomicWrite(relative,b);
 const meta={path:relative,shape:[events.length,16,fields.length],fields,encoding:'little-endian Float64; integer bit masks are exact',wallIds:B.course.boxes.map(b=>b.id),bytes:b.length,sha256:sha(b),events:events.map(e=>({tick:e.tick,commandsSha256:e.commandsSha256,branchSignatureSha256:e.branchSignatureSha256})),meaning:'Commands and branch inputs at each actual nonterminal controller event; vectors/constraint normals can be reconstructed only where full state was retained'};
 save(relative+'.json',meta);return meta;
}
module.exports={writeControllers,fields};
