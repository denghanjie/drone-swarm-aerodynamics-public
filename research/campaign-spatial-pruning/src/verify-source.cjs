'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert/strict');
const {root}=require('./source.cjs'),manifest=require('../provenance.json');
for(const entry of manifest.references){const bytes=fs.readFileSync(path.join(root,entry.path));assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),entry.sha256,entry.path);}
console.log(JSON.stringify({verified:manifest.references.length,snapshot:manifest.snapshot}));
