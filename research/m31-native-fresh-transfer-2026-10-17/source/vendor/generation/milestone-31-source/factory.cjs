'use strict';
const base=require('./factory-wide.cjs');
const variant=process.env.FLOCK_FACTORY_VARIANT||'wide';
if(!['wide','narrow'].includes(variant))throw Error('Unknown factory variant');
if(variant==='wide')module.exports=base;
else {
 const c=JSON.parse(JSON.stringify(base));c.id='factory-narrow-v1';c.name='Three factory halls — narrower openings';
 for(const [i,g] of c.gates.entries()){
  g.width=3;g.height=2.5;const y0=g.y-1.5,y1=g.y+1.5,z0=g.z-1.25,z1=g.z+1.25;
  for(const b of c.boxes.filter(b=>b.id.startsWith('partition-'+i+'-'))){
   if(b.id.endsWith('-left'))b.max[1]=y0;
   if(b.id.endsWith('-right'))b.min[1]=y1;
   if(b.id.endsWith('-below')){b.min[1]=y0;b.max[1]=y1;b.max[2]=z0;}
   if(b.id.endsWith('-above')){b.min[1]=y0;b.max[1]=y1;b.min[2]=z1;}
  }
 }
 c.description+=' Narrow variant changes only the three doorways to3×2.5m.';module.exports=c;
}
