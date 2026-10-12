const fs=require('node:fs'),path=require('node:path');
const read=n=>fs.readFileSync(path.join(__dirname,n),'utf8');
fs.writeFileSync(path.join(__dirname,'../step-02-drone-lab.html'),read('template.html').replace('/*PHYSICS*/',()=>read('physics.cjs')).replace('/*APP*/',()=>read('app.js')));
