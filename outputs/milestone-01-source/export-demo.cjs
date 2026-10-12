const fs=require('fs'),path=require('path'),D=require('./pair.cjs');const out=path.join(__dirname,'..');
const config={gap:.45,offset:.06,gains:{kp:1,kv:2.5,ka:100,kw:20}};
const presets=[
{id:'pair',title:'One neighbor',sources:[[.06,0,1.45]],a:{momentScale:1},b:{momentScale:0},labels:['Include uneven rotor loading','Remove its turning effect'],explanation:'The same controller can predict very different motion depending on whether uneven airflow is allowed to turn the drone.'},
{id:'group',title:'Two neighbors',sources:[[0,0,1.45],[.12,0,1.45]],a:{aggregation:'airflow'},b:{aggregation:'deficits'},labels:['Combine airflow first','Add separate lift losses'],explanation:'Both combination rules predict continued motion here. Their agreement is a consistency observation; neither has been checked against group-flight measurements.'},
{id:'wide',title:'Neighbors farther apart',sources:[[-.14,0,1.45],[.26,0,1.45]],a:{aggregation:'airflow'},b:{aggregation:'deficits'},labels:['Combine airflow first','Add separate lift losses'],explanation:'Separating the fixed sources reduces the initial lift loss. This alone does not establish stable position holding.'}
];
for(const p of presets){let a=new D.Simulation({...config,sources:p.sources,...p.a}).run(),b=new D.Simulation({...config,sources:p.sources,...p.b}).run();p.end=Math.min(a.t,b.t);p.stops=[a.stopped,b.stopped];const sample=s=>s.history.filter((v,i)=>(i%8===0||v.t===p.end)&&v.t<=p.end+1e-9).map(v=>[v.t,v.x,v.y,v.z,v.qx,v.qy,v.qz,v.qw]);p.traces=[sample(a),sample(b)];p.initialLiftLoss=[a,b].map(s=>1-s.history[0].thrust/(D.P.m*D.P.g));delete p.a;delete p.b;}
fs.writeFileSync(path.join(__dirname,'demo.json'),JSON.stringify(presets));
