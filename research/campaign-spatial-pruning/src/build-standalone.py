"""Create an offline HTML viewer from the same local source and retained data.

Usage: python src/build-standalone.py --esbuild /path/to/esbuild
esbuild is a build-only dependency; the generated HTML needs no dependencies.
"""
from pathlib import Path
import argparse,json,subprocess,tempfile
root=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser();parser.add_argument('--esbuild',default='esbuild');args=parser.parse_args()
with tempfile.TemporaryDirectory() as tmp:
    bundle=Path(tmp)/'viewer.js'
    subprocess.run([args.esbuild,str(root/'demo/app.js'),'--bundle','--minify','--format=esm','--target=es2022',f'--alias:three={root}/demo/vendor/three.module.js',f'--outfile={bundle}','--legal-comments=inline'],check=True,capture_output=True)
    js=bundle.read_text()
data={}
for p in [root/'results/accuracy-summary.json',root/'results/timing.json',root/'provenance.json',*sorted((root/'results/boids').glob('*.json'))]:data['../'+str(p.relative_to(root))]=json.loads(p.read_text())
text={}
for name in ['REPORT.md','PLAN.md','AMENDMENTS.md']:
    # Prefer already reviewed publication wording when staging exists.
    p=root/'publication'/name if (root/'publication'/name).exists() else root/name
    if p.exists():text['../'+name]=p.read_text()
loader="""<script>
const offlineData=DATA;
const offlineText=TEXT;
window.fetch=async function(url){const key=String(url);if(Object.hasOwn(offlineData,key))return new Response(JSON.stringify(offlineData[key]),{headers:{'Content-Type':'application/json'}});throw Error('Offline record not bundled: '+key);};
document.addEventListener('click',event=>{const a=event.target.closest('a');if(!a)return;const key=a.getAttribute('href');if(Object.hasOwn(offlineData,key)||Object.hasOwn(offlineText,key)){event.preventDefault();const isJSON=Object.hasOwn(offlineData,key),blob=new Blob([isJSON?JSON.stringify(offlineData[key],null,2):offlineText[key]],{type:isJSON?'application/json':'text/plain'}),url=URL.createObjectURL(blob),download=document.createElement('a');download.href=url;download.download=key.split('/').at(-1);download.click();setTimeout(()=>URL.revokeObjectURL(url),5000);}});
</script>""".replace('DATA',json.dumps(data,separators=(',',':')).replace('<','\\u003c')).replace('TEXT',json.dumps(text,separators=(',',':')).replace('<','\\u003c'))
html=(root/'demo/index.html').read_text()
start=html.index('<script type="importmap">');end=html.index('</script>',start)+len('</script>');html=html[:start]+html[end:]
html=html.replace('<script type="module" src="./app.js"></script>',loader+'<script type="module">'+js.replace('</script','<\\/script')+'</script>')
license=(root/'demo/vendor/THREE-LICENSE.txt').read_text()
html=html.replace('</head>','<!-- Bundled Three.js / OrbitControls license notice\n'+license.replace('--','- -')+'\n-->\n</head>')
html=html.replace('Serve this folder with Python\'s local HTTP server; opening file:// does not allow module/data loading.','This offline file should include every required record.')
(root/'wake-pruning-evidence.html').write_text(html)
print(json.dumps({'file':'wake-pruning-evidence.html','bytes':len(html.encode()),'records':len(data),'offline':True}))
