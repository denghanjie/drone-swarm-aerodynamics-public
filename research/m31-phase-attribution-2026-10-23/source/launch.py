from pathlib import Path
import os,sys,json,hashlib
import os
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):raise RuntimeError('optimized-Python-not-permitted')
base=Path(__file__).resolve().parent.parent;phase=sys.argv[1]
assert not os.environ.get('NODE_OPTIONS') and not os.environ.get('NODE_PATH')
runtime=json.loads((base/'runtime.json').read_bytes());node=Path(os.environ['M31_NODE']);raw=node.read_bytes()
assert len(raw)==runtime['nodeExecutableBytes'] and hashlib.sha256(raw).hexdigest()==runtime['nodeExecutableSha256']
commands={'producer':[sys.executable,str(base/'source/analyze.py')],'audit':[sys.executable,str(base/'source/audit.py')],'finalize':[sys.executable,str(base/'source/finalize.py')],'ui':[str(node),str(base/'source/ui.cjs')]}
if phase=='ui':os.environ['NODE_PATH']=str(node.parent.parent/'node_modules')
command=commands[phase];os.execv(command[0],command)
