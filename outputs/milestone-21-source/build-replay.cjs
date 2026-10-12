const fs=require('fs'),path=require('path'),d=__dirname;
const originals=fs.readdirSync(d).filter(f=>/^run-1101-.*-0\.0025\.json$/.test(f)).map(f=>JSON.parse(fs.readFileSync(path.join(d,f))));
const audits=[0,.1].map(delay=>JSON.parse(fs.readFileSync(path.join(d,`audit-replay-${delay}.json`))));
if(originals.length!==6)throw Error('Expected6 primary replays');fs.writeFileSync(path.join(d,'demo.json'),JSON.stringify([...originals,...audits]));console.log('8 exact replays assembled');
