"""Static record/standalone identity checks; this is not rendered browser QA."""
import argparse,hashlib,json,math,pathlib
p=argparse.ArgumentParser();p.add_argument('campaign');p.add_argument('--output',default=str(pathlib.Path(__file__).parent/'raw'/'replay-audit.json'));args=p.parse_args();root=pathlib.Path(args.campaign)
sha=lambda b:hashlib.sha256(b).hexdigest()
errors=[];records=[]
index=json.loads((root/'results/boids/index.json').read_text())
for item in index['records']:
 file=root/'results/boids'/item['file'];raw=file.read_bytes();r=json.loads(raw);n=r['config']['count'];local=[];frames=r['frames']
 if not frames:local.append('no frames')
 last=-math.inf
 for f in frames:
  if f['t']<=last:local.append('nonincreasing frame time')
  last=f['t']
  if len(f['pose'])!=n or len(f['winds'])!=n:local.append('agent count mismatch')
  if any(len(s)!=7 or not all(math.isfinite(x) for x in s) for s in f['pose']):local.append('invalid pose')
  if any(len(w)!=4 or not all(math.isfinite(x) and x>=0 for x in w) for w in f['winds']):local.append('invalid four-rotor field')
  if any(abs(math.sqrt(sum(x*x for x in s[3:7]))-1)>1e-10 for s in f['pose']):local.append('nonunit recorded quaternion')
  held=f['heldFieldTime']
  if held is not None and (held>f['t']+1e-12 or f['t']-held>r['config']['aeroDt']+1e-10):local.append('invalid held-field time')
 if frames and frames[0]['t']==0 and frames[0]['pose']!=[s[:3]+s[6:10] for s in r['initial']]:local.append('first frame differs from actual initial state')
 if frames and frames[-1]['pose']!=[s[:3]+s[6:10] for s in r['final']]:local.append('last frame differs from actual final state')
 if frames and abs(frames[-1]['t']-r['metrics']['end'])>1e-12:local.append('last frame does not match recorded end')
 if r['metrics']['complete'] and abs(r['metrics']['end']-r['config']['duration'])>1e-12:local.append('completion mislabeled')
 if item.get('metrics')!=r['metrics']:local.append('index metrics differ from record')
 records.append({'file':item['file'],'sha256':sha(raw),'frames':len(frames),'count':n,'complete':r['metrics']['complete'],'sourceHash':r['sourceHash'],'pass':not local,'errors':local})
 errors += [item['file']+': '+x for x in local]
htmlfile=root/'exact-airflow-evidence.html';html=htmlfile.read_text();decoder=json.JSONDecoder();start=html.index('const sources=')+len('const sources=');sources,end=decoder.raw_decode(html,start)
assert html[end:end+6]==',data='
data,end=decoder.raw_decode(html,end+6)
assert html[end:end+7]==',texts='
texts,end=decoder.raw_decode(html,end+7)
embedded=[]
for key,value in data.items():
 file=root/key.removeprefix('../');same=file.exists() and value==json.loads(file.read_text());embedded.append({'path':key,'matchesRaw':same});
 if not same:errors.append('embedded record differs: '+key)
for key,value in sources.items():
 if value!=(root/'demo'/key).read_text():errors.append('embedded source differs: '+key)
for item in index['records']:
 key='../results/boids/'+item['file']
 if key not in data:errors.append('record absent from standalone: '+key)
for key,value in texts.items():
 file=root/'demo'/key if key.startswith('./') else root/key.removeprefix('../')
 if value!=file.read_text():errors.append('embedded document differs: '+key)
report={'scope':'Static Three.js source and actual saved-record identity. No browser was launched and appearance, WebGL execution, downloads and interactions are not verified by this script.','pass':not errors,'errors':errors,'records':records,'embeddedRecords':embedded,'standalone':{'file':htmlfile.name,'sha256':sha(htmlfile.read_bytes()),'bytes':htmlfile.stat().st_size,'sourceModules':list(sources),'textArtifacts':list(texts)},'browserQA':'Not performed by this script'}
out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2));print(json.dumps({'pass':report['pass'],'records':len(records),'embedded':len(embedded),'errors':errors},indent=2));raise SystemExit(0 if report['pass'] else 2)
