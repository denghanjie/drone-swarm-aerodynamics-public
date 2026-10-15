'use strict';
// Inert fixtures only: importing the pure validator is explicitly permitted.
const assert = require('node:assert/strict');
const {validateEnvelope} = require('./validation.cjs');
const fixture = () => ({version:1,format:'uint8-values-v1',payloadId:'synthetic-control-channel-3840-v1',
  byteLength:3840,values:Array.from({length:3840},(_,i)=>(73*i+19)%256),origin:'http://127.0.0.1:8876',
  isSecureContext:true,constructionPhase:'array-ready',browserConstructionMilliseconds:1});
let checks=0;
function pass(name, mutate) {const x=fixture();if(mutate)mutate(x);const r=validateEnvelope(x);assert.equal(r.jsonBytes,Buffer.byteLength(r.json));assert(r.jsonBytes<=32768);checks++;}
function reject(name, mutate, code) {const x=fixture();mutate(x);assert.throws(()=>validateEnvelope(x),e=>e.code===code,name);checks++;}
pass('exact fixture');pass('wrong but valid byte stays admitted',x=>x.values[0]=42);pass('opaque origin retained for policy decision',x=>x.origin='null');
reject('missing key',x=>delete x.payloadId,'envelope-keys');
reject('extra key',x=>x.extra=1,'envelope-keys');
reject('symbol key',x=>x[Symbol('x')]=1,'envelope-keys');
reject('accessor envelope',x=>Object.defineProperty(x,'format',{get(){throw Error('Must not invoke');}}),'envelope-data-properties');
reject('hidden envelope property',x=>Object.defineProperty(x,'format',{value:x.format,enumerable:false}),'envelope-data-properties');
reject('wrong version',x=>x.version=2,'envelope-identity');
reject('wrong declared size',x=>x.byteLength=3839,'envelope-byte-shape');
reject('wrong actual size',x=>x.values.pop(),'values-array-length');
reject('sparse value',x=>delete x.values[1],'values-own-key-count');
reject('array extra key',x=>x.values.extra=1,'values-own-key-count');
reject('sparse plus extra',x=>{delete x.values[1];x.values.extra=1;},'values-dense-data');
reject('accessor element',x=>Object.defineProperty(x.values,'0',{get(){throw Error('Must not invoke');}}),'values-dense-data');
for(const bad of [null,undefined,'19',NaN,Infinity,-1,256,19.5,-0])reject('invalid element',x=>x.values[0]=bad,'values-uint8');
reject('typed array',x=>x.values=Uint8Array.from(x.values),'values-array-length');
reject('arbitrary origin',x=>x.origin='http://private.invalid/path','envelope-origin');
reject('string boolean',x=>x.isSecureContext='true','envelope-secure-context');
reject('nonfinite duration',x=>x.browserConstructionMilliseconds=NaN,'envelope-browser-duration');
reject('overlong duration',x=>x.browserConstructionMilliseconds=10000,'envelope-browser-duration');
assert.throws(()=>validateEnvelope(null),e=>e.code==='envelope-object');checks++;
assert.throws(()=>validateEnvelope(Object.create(null)),e=>e.code==='envelope-object');checks++;
console.log(JSON.stringify({kind:'pure-control-envelope-validation-tests',checks,passed:true,
  diagnosticExecuted:false,browserLaunched:false,networkUsed:false}));
