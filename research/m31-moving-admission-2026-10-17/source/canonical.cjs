'use strict';
const crypto=require('node:crypto');
// Canonical printable-ASCII JSON: recursively sorted object keys, preserved array order,
// exact safe integers only, no floats/undefined/BigInt/non-JSON objects.
function encode(value){
 if(value===null)return 'null';
 if(typeof value==='boolean')return value?'true':'false';
 if(typeof value==='string'){if(/[^\x20-\x7e]/.test(value))throw Error('Non-printable-ASCII digest string');return JSON.stringify(value);}
 if(typeof value==='number'){if(!Number.isSafeInteger(value)||Object.is(value,-0))throw Error('Noninteger digest number');return String(value);}
 if(Array.isArray(value)){if(Object.keys(value).length!==value.length||!Object.keys(value).every((k,i)=>k===String(i)))throw Error('Sparse digest array');return '['+value.map(encode).join(',')+']';}
 if(value&&typeof value==='object'&&(Object.getPrototypeOf(value)===Object.prototype||Object.getPrototypeOf(value)===null))return '{'+Object.keys(value).sort().map(k=>encode(k)+':'+encode(value[k])).join(',')+'}';
 throw Error('Non-JSON digest value');
}
const sha=text=>crypto.createHash('sha256').update(text,'utf8').digest('hex');
module.exports={encode,sha};
