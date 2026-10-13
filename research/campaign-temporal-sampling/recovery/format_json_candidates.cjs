// Recovery-only formatting utility. Does not load or execute campaign/browser code.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const root=__dirname;
const manifest=JSON.parse(fs.readFileSync(path.join(root,'RECOVERY-MANIFEST.json'),'utf8'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const gitsha=b=>crypto.createHash('sha1').update(Buffer.from(`blob ${b.length}\0`)).update(b).digest('hex');
const list=[...manifest.files.filter(x=>x.embeddedMap==='data'),...manifest.nestedRecoveredSidecars];
const priorPath=path.join(root,'prior-uploaded-json-blobs.json');
const prior=fs.existsSync(priorPath)?JSON.parse(fs.readFileSync(priorPath,'utf8')):{};
const results=[];
for(const f of list){
 const parsed=JSON.parse(fs.readFileSync(path.join(root,f.path),'utf8'));
 const serialized=JSON.stringify(parsed,(_k,v)=>typeof v==='number'&&!Number.isFinite(v)?{nonfinite:String(v)}:v,2)+'\n';
 const body=Buffer.from(serialized,'utf8');
 const relative=f.path.replace(/^recovered\//,'');
 const target=path.join(root,'formatted-candidates',relative);
 fs.mkdirSync(path.dirname(target),{recursive:true});
 if(fs.existsSync(target)&&!fs.readFileSync(target).equals(body))throw Error('Refusing different overwrite '+target);
 fs.writeFileSync(target,body);
 if(JSON.stringify(JSON.parse(body.toString()))!==JSON.stringify(parsed))throw Error('Semantic round-trip failed');
 const candidate=gitsha(body),expected=prior[relative]||f.priorUploadedGitBlobSha1||null;
 results.push({path:relative,sourcePath:f.path,candidatePath:path.relative(root,target),bytes:body.length,sha256:sha(body),gitBlobSha1:candidate,
  matchesRecoveredJsonSemantics:true,priorUploadedGitBlobSha1:expected,matchesPriorUploadedGitBlob:expected===null?null:candidate===expected,
  originalBytesStatus:expected===null?'unverified; candidate serialization only':candidate===expected?'matches independently verified existing Git blob':'differs from prior Git blob',
  recoveryMethod:'JSON.stringify(obj, finite-number replacer, 2) + newline, matching frozen src/io.cjs save() formatting; no scientific values recomputed'});
}
const output={schema:'json-format-reconstruction/v1',createdDuringRecovery:true,nodeVersion:process.version,
 note:'These are reconstruction candidates, separate from verbatim extracted literals. Original-file byte identity is asserted only where candidate Git blob matches an independently verified existing blob ID. For six run-record reads, see REMOTE-BLOB-VERIFICATION.json for one prior-receipt lookup versus five deterministic-candidate lookups; existence does not establish final publication.',
 records:results};
fs.writeFileSync(path.join(root,'JSON-FORMAT-RECONSTRUCTION.json'),JSON.stringify(output,null,2)+'\n');
console.log(JSON.stringify(results.map(({path,bytes,gitBlobSha1,matchesPriorUploadedGitBlob})=>({path,bytes,gitBlobSha1,matchesPriorUploadedGitBlob})),null,2));
