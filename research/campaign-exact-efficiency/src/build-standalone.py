"""Dependency-free offline packer: exact vendored modules become local Blob URLs."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent.parent
sources={name:(root/'demo'/name).read_text() for name in ['vendor/three.core.js','vendor/three.module.js','vendor/OrbitControls.js','app.js']}
data={}
for p in sorted((root/'results').rglob('*.json')):
    # Only replay and summary records are needed in the viewer; bulky raw timing
    # fixtures remain repository links and are enumerated by timing summaries.
    if p.parent.name=='boids' or p.name=='timing-summary.json':data['../'+str(p.relative_to(root))]=json.loads(p.read_text())
if (root/'provenance.json').exists():data['../provenance.json']=json.loads((root/'provenance.json').read_text())
texts={'../'+name:(root/name).read_text() for name in ['REPORT.md','PLAN.md','AMENDMENTS.md'] if (root/name).exists()}
texts['./vendor/THREE-LICENSE.txt']=(root/'demo/vendor/THREE-LICENSE.txt').read_text()
def safe(x):return json.dumps(x,separators=(',',':')).replace('<','\\u003c')
loader='''<script type="module">
const sources=SOURCES,data=DATA,texts=TEXTS;
window.fetch=async url=>{const key=String(url);if(Object.hasOwn(data,key))return new Response(JSON.stringify(data[key]),{headers:{'Content-Type':'application/json'}});throw Error('Offline record not bundled: '+key);};
document.addEventListener('click',e=>{const a=e.target.closest('a');if(!a)return;const key=a.getAttribute('href');if(Object.hasOwn(data,key)||Object.hasOwn(texts,key)){e.preventDefault();const blob=new Blob([Object.hasOwn(data,key)?JSON.stringify(data[key],null,2):texts[key]],{type:Object.hasOwn(data,key)?'application/json':'text/plain'}),url=URL.createObjectURL(blob),d=document.createElement('a');d.href=url;d.download=key.split('/').at(-1);d.click();setTimeout(()=>URL.revokeObjectURL(url),5000);}});
const blob=text=>URL.createObjectURL(new Blob([text],{type:'text/javascript'}));
const core=blob(sources['vendor/three.core.js']);
const three=blob(sources['vendor/three.module.js'].replaceAll("'./three.core.js'",JSON.stringify(core)));
const controls=blob(sources['vendor/OrbitControls.js'].replaceAll("'three'",JSON.stringify(three)));
const app=sources['app.js'].replaceAll("'three'",JSON.stringify(three)).replaceAll("'./vendor/OrbitControls.js'",JSON.stringify(controls));
await import(blob(app));
</script>'''.replace('const sources=SOURCES,data=DATA,texts=TEXTS;',f'const sources={safe(sources)},data={safe(data)},texts={safe(texts)};')
html=(root/'demo/index.html').read_text();start=html.index('<script type="importmap">');end=html.index('</script>',start)+len('</script>');html=html[:start]+html[end:]
html=html.replace('<script type="module" src="./app.js"></script>',loader)
license=texts['./vendor/THREE-LICENSE.txt'];html=html.replace('</head>','<!-- Full bundled Three.js / OrbitControls license\n'+license.replace('--','- -')+'\n-->\n</head>')
p=root/'exact-airflow-evidence.html';p.write_text(html)
print(json.dumps({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bundledRecords':len(data),'networkDependency':False}))
