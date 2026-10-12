const fs=require('fs'),path=require('path'),dir=__dirname;
const r=fs.readdirSync(dir).filter(x=>/^run-.*-0\.005\.json$/.test(x)).map(x=>JSON.parse(fs.readFileSync(path.join(dir,x))));
const reference=JSON.parse(fs.readFileSync(path.join(dir,'../milestone-19-source/demo.json'))).filter(r=>r.config.mode==='soft');
if(r.length!==9||reference.length!==3)throw Error('Expected9 candidate and3 reference replays');fs.writeFileSync(path.join(dir,'demo.json'),JSON.stringify([...reference,...r]));console.log('12 exact replays assembled');
