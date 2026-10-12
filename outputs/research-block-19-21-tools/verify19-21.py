from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json,hashlib,subprocess,re,ast
O=Path('outputs');node='node'
errors=[];checked=[]
for n in [19,20,21]:
 for p in (O/f'milestone-{n}-source').glob('*'):
  if p.suffix in ['.js','.cjs']:
   r=subprocess.run([node,'--check',str(p)],capture_output=True,text=True);checked.append(str(p))
   if r.returncode:errors.append({'file':str(p),'syntax':r.stderr})
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ['href','src'] and v and not urlparse(v).scheme and not v.startswith('#') and not (O/unquote(v.split('#')[0])).exists():errors.append({'missingLink':v})
for p in [O/'research-results.html',*[O/f'milestone-{n}-lab.html' for n in [19,20,21]]]:Links().feed(p.read_text())
for p in [O/'research-block-19-21-summary.md',O/'research-final-report.md',O/'research-block-19-21-qa.md',*[O/f'milestone-{n}-report.md' for n in [19,20,21]]]:
 for v in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if not urlparse(v).scheme and not (O/v.split('#')[0]).exists():errors.append({'missingReportLink':v})
for n in [19,20,21]:
 artifact=json.loads((O/f'milestone-{n}-artifact-checks.json').read_text());errors.extend(c for c in artifact['softwareChecks'] if not c['passed'])
for filename in ['research-reproduce.py','research-refresh-manifest.py']:ast.parse((O/filename).read_text())
audit=json.loads((O/'milestone-21-failure-audit.json').read_text());assert all(x['exactReplay'] for x in audit)
p=json.loads((O/'milestone-21-failure-audit-protocol.json').read_text());assert all(hashlib.sha256((O/'milestone-21-source'/f).read_bytes()).hexdigest()==h for f,h in p['hashes'].items())
# Full failure states preserved, including contacts; reference count is81 executions.
records=sum(len(json.loads((O/f'milestone-{n}-study.json').read_text())) for n in [19,20,21])+len(json.loads((O/'milestone-21-failure-audit-runs.json').read_text()));assert records==81
result={'syntaxFiles':len(checked),'numericalExecutions':records,'errors':errors,'note':'Software/artifact checks do not override failed scientific criteria. New filters rejected; delayed reference contact stop remains.'}
(O/'research-block-19-21-artifact-checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert not errors
