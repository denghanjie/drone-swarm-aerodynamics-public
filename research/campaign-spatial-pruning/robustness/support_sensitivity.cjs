'use strict';
// Separate exploratory formula-extension sensitivity; not a physical reference.
const fs=require('node:fs'),path=require('node:path');
const X=require('./fixtures.cjs'),O=require('./oracle.cjs'),{comparison}=require('./checks.cjs');
const supports={nominal:{},axial_extension:{axialFade:4,axialCutoff:5},radial_extension:{radialFade:4,radialCutoff:5},both_extensions:{axialFade:4,axialCutoff:5,radialFade:4,radialCutoff:5}};
const fixtures=[
  {id:'far_axial_3m',states:[X.state(),X.state([0,0,4])]},
  {id:'far_radial_tail',states:[X.state(),X.state([3.4*X.half(1.3),0,2.3])]},
  {id:'nominal_axial_fade',states:[X.state(),X.state([0,0,3.4])]},
  {id:'nominal_radial_fade',states:[X.state(),X.state([2.7*X.half(1.3),0,2.3])]},
  {id:'many_far_axial_tails',states:[X.state(),...Array.from({length:16},(_,i)=>X.state([.5*Math.cos(2*Math.PI*i/16),.5*Math.sin(2*Math.PI*i/16),4]))]},
  {id:'near_domain_must_still_fail',states:[X.state(),X.state([.16,0,1.1])],expectedDomainFailure:true}
];
const config={scope:'Only sensitivity to declared finite-support/fade assumptions. All-pairs formula extension is exploratory and not a higher-fidelity or calibrated reference.',supports,fixtures,
  invariant:'Same state arrays, all four receiver rotors, receiver law, source strength, near-field and tilt limits. Only named support/fade constants differ. All-pairs search covers expanded support.',sourceCommit:X.C.sourceCommit};
function main(){
  const records=fixtures.map(f=>{
    const outputs={};for(const [name,support]of Object.entries(supports)){try{outputs[name]={ok:true,fields:O.fields(f.states,'sum-rotor',support)};}catch(e){outputs[name]={ok:false,message:e.message,detail:e.detail};}}
    for(const [name,row]of Object.entries(outputs))if(row.ok&&outputs.nominal.ok){
      const difference=comparison(f.states,outputs.nominal.fields,row.fields);
      delete difference.exactPass;delete difference.approximationTolerancePass;
      row.differenceFromNominal=difference;
    }
    return {id:f.id,outputs};
  });
  fs.writeFileSync(path.join(__dirname,'raw/support_sensitivity.json'),JSON.stringify({utc:new Date().toISOString(),config,records},null,2));
  console.log(JSON.stringify(records.map(r=>({id:r.id,outputs:Object.fromEntries(Object.entries(r.outputs).map(([n,x])=>[n,x.ok?{maxInflow:x.fields.maximumInflow,difference:x.differenceFromNominal}:{domainFailure:x.message}]))})),null,2));
}
if(require.main===module)main();module.exports={config};
