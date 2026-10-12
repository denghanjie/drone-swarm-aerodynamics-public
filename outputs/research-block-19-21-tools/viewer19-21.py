from pathlib import Path
import re,json
O=Path('outputs')
def build(stage,title,intro,options,modes,labels,finding,report,summary):
 d=O/f'milestone-{stage}-source'
 s=(O/'milestone-18-source/app.js').read_text()
 s=s.replace("const records=(await Promise.all(['demo.json','diagnostic-demo.json'].map(f=>fetch('./milestone-18-source/'+f).then(r=>r.json())))).flat();",f"const records=await fetch('./milestone-{stage}-source/demo.json').then(r=>r.json());")
 s=s.replace('milestone-18-source',f'milestone-{stage}-source')
 start=s.index('function select()');end=s.index("$('scenario').onchange=select",start)
 s=s[:start]+'''function select(){const [seedText,scenario,left,right]=$('scenario').value.split(':'),seed=+seedText;runs=[left,right].map(mode=>records.find(r=>r.config.scenario===scenario&&r.config.mode===mode&&r.config.seed===seed));const names=NAMES;$('labelA').textContent=names[left];$('labelB').textContent=names[right];t=0;playing=false;last=null;$('play').textContent='Play';$('findings').textContent='Seed '+seed+' · 5 ms recorded replay. '+names[left]+': '+runs[0].metrics.passed+'/50, '+(runs[0].metrics.stopReason||'no contact stop')+'. '+names[right]+': '+runs[1].metrics.passed+'/50, '+(runs[1].metrics.stopReason||'no contact stop')+'. Smaller-step outcomes and every case are in the report.';render();views.forEach(v=>{v.setObstacle(scenario);v.reset();});}
'''.replace('NAMES',json.dumps(labels))+s[end:]
 # Stop animation immediately at its end rather than leaving button as Pause.
 (d/'app.js').write_text(s)
 h=(O/'milestone-18-interior.html').read_text()
 h=re.sub(r'<title>.*?</title>',f'<title>{title} — 3D Boids</title>',h)
 h=re.sub(r'<span>CHECKPOINT.*?</span><h1>.*?</h1><p>.*?</p>',f'<span>CHECKPOINT {stage} · LOCAL 3D FLOCKING</span><h1>{title}</h1><p>{intro}</p>',h,count=1)
 h=re.sub(r'<select disabled id="scenario">.*?</select>','<select disabled id="scenario">'+''.join(f'<option value="{value}">{label}</option>' for value,label in options)+'</select>',h)
 h=re.sub(r'<p id="studyFinding">.*?</p>',f'<p id="studyFinding">{finding}</p>',h)
 h=re.sub(r'<p><a href="research-block-15-18-summary.md">.*?</p>',f'<p><a href="{summary}">Plain-language block summary</a> · <a href="{report}">This checkpoint</a> · <a href="milestone-{stage}-summary.json">Every case</a> · <a href="milestone-{stage}-comparisons.json">Numerical checks</a> · <a href="milestone-{stage}-protocol.json">Frozen protocol</a> · <a href="research-stage-log.md">Saved stages</a></p>',h)
 h=h.replace('milestone-18-source/app.js',f'milestone-{stage}-source/app.js')
 (O/f'milestone-{stage}-lab.html').write_text(h)
if __name__=='__main__':
 build('19','Smoother rules can still trap a flock.','We replaced sequential braking rules with one calculation that balances local neighbor and wall demands. The same Boids and map guidance remain. This replay preserves the unsuccessful candidate alongside the previous controller.',[(f'{seed}:tight:interior:soft',f'Development seed {seed} · tight openings') for seed in [905,1002,1004]],[],{'interior':'Previous inward guidance','soft':'Simultaneous soft filter'},'Results are recorded in the checkpoint report. A small solver error does not guarantee passage or a consistent full trajectory.','milestone-19-report.md','research-block-19-21-summary.md')
