const fs=require('node:fs'),path=require('node:path');
fs.copyFileSync(path.join(__dirname,'physics.cjs'),path.join(__dirname,'physics.js'));
console.log('Browser physics synchronized with verified source.');
