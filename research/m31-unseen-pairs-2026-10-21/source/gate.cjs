 'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const base=path.resolve(__dirname,'..'),root=path.resolve(base,'../..'),events=[];let operation=0;
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),load=p=>JSON.parse(fs.readFileSync(p));
function checked(p,pin){const op=++operation;for(let attempt=1;attempt<=3;attempt++){try{const b=fs.readFileSync(p);if(b.length===pin.bytes&&sha(b)===pin.sha256)return b;events.push({operation:op,attempt,path:path.relative(root,p),kind:'byte-mismatch',bytes:b.length,sha256:sha(b)});}catch(e){events.push({operation:op,attempt,path:path.relative(root,p),kind:'read-error',code:e.code||'unknown'});}}throw Error('verified-read-failed:'+path.relative(root,p));}
function gate(){const raw=fs.readFileSync(path.join(base,'source-manifest.json')),m=JSON.parse(raw),pub=load(path.join(base,'source-publication.json'));assert.equal(pub.manifestSha256,sha(raw));assert.equal(pub.remoteBytesEqualLocal,true);assert.equal(pub.committedBytesEqualLocal,true);assert.equal(pub.verifiedFilePins,m.files.length);for(const pin of m.files)checked(path.join(root,pin.path),pin);return pub;}
module.exports={base,root,events,sha,load,checked,gate};
