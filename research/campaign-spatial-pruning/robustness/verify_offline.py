"""Static bundle identity/syntax verification. Does not render a browser."""
import hashlib,json,pathlib,re,subprocess
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parent
html_file=ROOT/'wake-pruning-evidence.html'
html=html_file.read_text()
def assignment(name):
    at=html.index('const '+name+'=')+len('const '+name+'=')
    return json.JSONDecoder().raw_decode(html[at:])[0]
data,text=assignment('offlineData'),assignment('offlineText')
records=[]
for key,value in data.items():
    local=ROOT/key.removeprefix('../')
    disk=json.loads(local.read_text())
    records.append({'embeddedKey':key,'matchesCurrentRawJSON':disk==value,'sha256':hashlib.sha256(local.read_bytes()).hexdigest()})
index=data['../results/boids/index.json']
checks=[]
for record in index['records']:
    key='../results/boids/'+record['file'];r=data[key]
    checks.append({'id':record['id'],'configMatchesIndex':r['config']==record['config'],
                   'frameCount':len(r['frames']),'allFramesHave16FullStates':all(len(f['states'])==16 and all(len(s)==17 for s in f['states']) for f in r['frames']),
                   'allFramesHaveFourHeldRotorFields':all(len(f['winds'])==16 and all(len(x)==4 for x in f['winds']) for f in r['frames']),
                   'firstT':r['frames'][0]['t'],'lastT':r['frames'][-1]['t'],'plannedDuration':r['config']['duration'],
                   'sourceHash':r['sourceHash'],'stop':r['metrics']['stop']})
scripts=re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',html,re.S)
syntax=[]
out=BASE/'raw'/'viewer_qa';out.mkdir(parents=True,exist_ok=True)
for i,script in enumerate(scripts):
    p=out/f'extracted_inline_{i}.mjs';p.write_text(script)
    result=subprocess.run(['node','--check',str(p)],capture_output=True,text=True)
    syntax.append({'inlineScript':i,'exitCode':result.returncode,'stderr':result.stderr})
    p.unlink()
result={'scope':'Static offline bundle identity and JS syntax only; browser rendering/controls/mobile/network-disabled file opening remain unverified.',
        'htmlSha256':hashlib.sha256(html_file.read_bytes()).hexdigest(),'bytes':html_file.stat().st_size,
        'embeddedJSON':records,'embeddedTextKeys':list(text),'boidsRecords':checks,'syntax':syntax,
        'externalScriptSrc':re.findall(r'<script[^>]+src=["\']([^"\']+)',html),
        'sampledScientificLabels':{'pruningFailure':'no demonstrated useful speed win' in html.lower(),'oneSecondLimit':'one-second test' in html,'savedStates':'saved states' in html,'unvalidated':'unvalidated' in html,'notThroughput':'Rendering speed is not numerical simulation throughput' in html},
        'allEmbeddedDataMatch':all(r['matchesCurrentRawJSON'] for r in records),
        'oneSecondOutcomesOnly':all(x['lastT']==x['plannedDuration']==1 for x in checks)}
(out/'offline_static.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
