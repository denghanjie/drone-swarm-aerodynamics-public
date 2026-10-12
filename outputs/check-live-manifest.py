"""Small isolated regression for live-output exclusions; never edits trial data."""
from pathlib import Path
import tempfile,shutil,json,subprocess,sys
source=Path(__file__).resolve().parent/'research-refresh-manifest.py'
with tempfile.TemporaryDirectory(prefix='flock-manifest-') as temp:
 root=Path(temp);shutil.copy2(source,root/source.name);d=root/'milestone-99-source';d.mkdir()
 (d/'study.cjs').write_text('// stable source');(d/'index.json').write_text('[]')
 for name in ['finished.json','finished.f64','active.json','active.f64','checkpoint-active-20.json','progress-active.json']:(d/name).write_text(name)
 (root/'milestone-99-progress.json').write_text(json.dumps([{'job':{'id':'finished'}}]));(root/'milestone-99-execution.log').write_text('still writing')
 subprocess.run([sys.executable,str(root/source.name),'--live-stages','99'],check=True,capture_output=True)
 manifest=json.loads((root/'research-manifest.json').read_text());pinned={x['path'] for x in manifest['files']};excluded={x['path'] for x in manifest['excluded']}
 assert {'milestone-99-source/finished.json','milestone-99-source/finished.f64','milestone-99-source/study.cjs'}<=pinned
 assert {'milestone-99-source/active.json','milestone-99-source/active.f64','milestone-99-source/checkpoint-active-20.json','milestone-99-source/progress-active.json','milestone-99-source/index.json','milestone-99-progress.json','milestone-99-execution.log'}<=excluded
 assert not pinned&excluded
 subprocess.run([sys.executable,str(root/source.name)],check=True,capture_output=True)
 final=json.loads((root/'research-manifest.json').read_text());assert not final['excluded'] and not final['liveStages'];assert 'milestone-99-source/active.f64' in {x['path'] for x in final['files']}
 print('Live snapshots pin completed trials/source, exclude active output; final snapshots include all artifacts.')
