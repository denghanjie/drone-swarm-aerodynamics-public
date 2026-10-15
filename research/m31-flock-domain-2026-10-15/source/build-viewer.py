from pathlib import Path
import json,hashlib,shutil
root=Path.cwd();b=root/'research/m31-flock-domain-2026-10-15';v=b/'viewer';v.mkdir(exist_ok=True)
inputs={}
for key,path in {'result':b/'raw/result.json','metadata':root/'research/m31-restart-2026-10-15/viewer/data.json','poses':root/'research/m31-restart-2026-10-15/viewer/snapshots.bin'}.items():
 inputs[key]={'url':str(Path('../raw/result.json') if key=='result' else Path('../../m31-restart-2026-10-15/viewer')/path.name),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
r=json.loads((b/'raw/result.json').read_text());inputs['rows']={s['id']:{'url':'../raw/'+s['id']+'.ndjson','bytes':(b/'raw'/f"{s['id']}.ndjson").stat().st_size,'sha256':hashlib.sha256((b/'raw'/f"{s['id']}.ndjson").read_bytes()).hexdigest()} for s in r['snapshots']}
(v/'data.json').write_text(json.dumps(inputs,indent=2)+'\n')
shutil.copyfile(root/'research/m31-restart-2026-10-15/viewer/style.css',v/'style.css')
with (v/'style.css').open('a') as f:f.write('''\n.green{background:#62dfec}.pink{background:#ef8caa}.white{background:#fff;border:1px solid #8ba4b8}.controls input[type=number]{width:100px;padding:10px;border:1px solid #cbd8e0;border-radius:8px;min-height:42px}.legend label{cursor:pointer}.legend input{margin:0 5px 0 0}#detail{line-height:1.6;font-size:.83rem;color:#456573}.metrics{grid-template-columns:repeat(3,1fr)}.comparison{overflow:auto;margin:28px 0}table{width:100%;border-collapse:collapse;font-size:.82rem}td,th{text-align:left;padding:10px;border-bottom:1px solid #dbe3e9}th{font-weight:650}button#focus{background:#e8f5f4}@media(max-width:640px){.metrics{grid-template-columns:1fr 1fr}.lab-head{flex-direction:column}.recorded{max-width:none}}\n''')
