from pathlib import Path
import ast,datetime,hashlib,json,subprocess,os
root=Path(os.environ['RESEARCH_ROOT']);pkg=root/'research/m31-native-tree-state1000-2026-10-17';node=os.environ['RESEARCH_NODE']
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(root)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
report={'schema':'m31-state1000-static-source-review-v1','scientificCalls':0,'executionAllowed':False,'syntax':[],'bundleSlices':[],'prerequisites':[],'admissionSources':[]}
for p in sorted((pkg/'source').iterdir()):
 if p.suffix=='.py':ast.parse(p.read_bytes());report['syntax'].append({'pin':pin(p),'method':'Python ast.parse only','passed':True})
 elif p.suffix in ('.cjs','.js'):
  proc=subprocess.run([node,'--check',str(p)],capture_output=True);assert proc.returncode==0,proc.stderr;report['syntax'].append({'pin':pin(p),'method':'Node --check only','passed':True})
 elif p.suffix=='.json':json.loads(p.read_bytes())
c=json.loads((pkg/'config.json').read_bytes());assert c['executionAllowed'] is False and c['authorization'] is None and c['launchCutoffUtc'] is None
assert not (pkg/'results').exists() and not (pkg/'source-manifest.json').exists() and not (pkg/'source-publication.json').exists()
b=json.loads((pkg/'source/source-bundle.json').read_bytes());raw=(root/b['path']).read_bytes();assert pin(root/b['path'])=={k:b[k] for k in ['path','bytes','sha256']};assert len(b['sources'])==19
for s in b['sources']:
 p=root/s['path'];assert pin(p)=={k:s[k] for k in ['path','bytes','sha256']};assert raw[s['offset']:s['offset']+s['bytes']]==p.read_bytes();report['bundleSlices'].append({'pin':pin(p),'passed':True})
a=json.loads((pkg/'review/STORAGE-ADMISSION.json').read_bytes());assert a['admitted'] is True and a['evidenceUpperBoundBytes']==137225341
for p in [a['proofPin'],*a['sourcePins']]:assert pin(root/p['path'])==p;report['admissionSources'].append(p)
pr=json.loads((pkg/'prerequisites.json').read_bytes());union={}
for item in pr['items']:
 for name in ['resultManifestPin','checkPin','attemptPin']:
  p=item[name];assert pin(root/p['path'])==p;union[p['path']]=p
 manifest=json.loads((root/item['resultManifestPin']['path']).read_bytes())
 for p in manifest['files']:
  assert pin(root/p['path'])==p
  if p['path'] in union:assert union[p['path']]==p
  union[p['path']]=p
 check=json.loads((root/item['checkPin']['path']).read_bytes());attempt=json.loads((root/item['attemptPin']['path']).read_bytes());assert check['complete'] and check['passed'] and attempt['status']=='completed'
 report['prerequisites'].append({'id':item['id'],'retainedPins':len(manifest['files']),'passed':True,'rerun':False})
# Read literals without importing the helper modules.
module=ast.parse((pkg/'source/support.py').read_bytes());mods=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MODULES' for t in n.targets))
for rel,sha in mods.values():assert pin(root/rel)['sha256']==sha and rel in union
report.update(passed=True,prerequisiteUnionPins=len(union),helperModules=len(mods),completedUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),limits='Source syntax, byte identity and metadata only. No project import, initializer, codec, query, reference, derivative or checker execution; no runtime success inferred.')
(pkg/'review/STATIC-REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['passed','prerequisiteUnionPins','helperModules','completedUtc']}))
