"""Syntax/resource/link audit of an already-built standalone; no browser launch."""
import argparse,hashlib,json,pathlib,re,subprocess
from html.parser import HTMLParser
p=argparse.ArgumentParser();p.add_argument('campaign');p.add_argument('--output',required=True);args=p.parse_args();root=pathlib.Path(args.campaign);htmlpath=root/'exact-airflow-evidence.html';raw=htmlpath.read_bytes();html=raw.decode();dec=json.JSONDecoder();at=html.index('const sources=')+14;sources,end=dec.raw_decode(html,at);data,end=dec.raw_decode(html,end+6);texts,end=dec.raw_decode(html,end+7)
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.scripts=[];self.active=False;self.script=''
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a' and 'href'in a:self.links.append(a['href'])
  if tag=='script':self.active=True;self.script='';self.scripts.append({'attributes':a})
 def handle_data(self,t):
  if self.active:self.script+=t
 def handle_endtag(self,tag):
  if tag=='script' and self.active:self.scripts[-1]['text']=self.script;self.active=False
parser=Parse();parser.feed(html);errors=[];checks=[];scratch=pathlib.Path(__file__).parent/'qa-scratch';scratch.mkdir(exist_ok=True)
for i,item in enumerate(parser.scripts):
 if 'src'in item['attributes']:errors.append('external script source remains')
 if item['attributes'].get('type')=='module':
  f=scratch/f'final-inline-{i}.mjs';f.write_text(item['text']);r=subprocess.run(['node','--check',str(f)],capture_output=True,text=True,timeout=30);checks.append({'script':f.name,'pass':r.returncode==0,'stderr':r.stderr.replace(str(scratch),'<qa-scratch>')});
  if r.returncode:errors.append('inline module syntax failed')
for name,source in sources.items():
 f=scratch/(pathlib.Path(name).stem+'.mjs');f.write_text(source);r=subprocess.run(['node','--check',str(f)],capture_output=True,text=True,timeout=30);checks.append({'script':name,'sha256':hashlib.sha256(source.encode()).hexdigest(),'pass':r.returncode==0,'stderr':r.stderr.replace(str(scratch),'<qa-scratch>')});
 if r.returncode:errors.append('bundled module syntax failed: '+name)
links=[]
for link in parser.links:
 bundled=link in data or link in texts;links.append({'href':link,'bundled':bundled})
 if not bundled:errors.append('document link not bundled: '+link)
module_text='\n'.join(x.get('text','') for x in parser.scripts)
for expected in ["window.fetch=async",'Object.hasOwn(data,key)',"new Blob([text]",'URL.createObjectURL',"replaceAll(\"'./three.core.js'\"", "replaceAll(\"'three'\"", "replaceAll(\"'./vendor/OrbitControls.js'\""]:
 if expected not in module_text:errors.append('offline import/download mechanism missing: '+expected)
for key in ['vendor/three.core.js','vendor/three.module.js','vendor/OrbitControls.js','app.js']:
 if key not in sources:errors.append('missing bundled source '+key)
if "'./three.core.js'" not in sources['vendor/three.module.js']:errors.append('three module import substitution target absent')
if "'three'" not in sources['vendor/OrbitControls.js']:errors.append('OrbitControls import substitution target absent')
if 'MIT License' not in texts.get('./vendor/THREE-LICENSE.txt',''):errors.append('full license unavailable')
result={'scope':'Static syntax, resource and download-link coverage only. No browser/WebGL/interaction execution.','pass':not errors,'errors':errors,'standalone':{'file':htmlpath.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},'moduleChecks':checks,'links':links,'bundledJSONRecords':len(data),'bundledTextArtifacts':len(texts),'browserRun':False};pathlib.Path(args.output).write_text(json.dumps(result,indent=2));print(json.dumps({'pass':result['pass'],'errors':errors,'modules':len(checks),'links':len(links),'sha256':result['standalone']['sha256']},indent=2));raise SystemExit(0 if result['pass'] else 2)
