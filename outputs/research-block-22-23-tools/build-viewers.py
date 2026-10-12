from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
for stage in [22,23]:
 path=root/f'milestone-{stage}-source/demo.json'
 if not path.exists():continue
 records=json.loads(path.read_text()); keys=sorted({(r['config']['seed'],r['config']['scenario'],r['config']['observationDelay']) for r in records})
 if stage==22:keys.sort(key=lambda k:(k[0]!=1103,k[2],k[0]))
 else: keys.sort(key=lambda k:(not any(r['metrics']['stopReason'] for r in records if (r['config']['seed'],r['config']['scenario'],r['config']['observationDelay'])==k),k))
 options=''.join(f'<option value="{seed}:{course}:{delay}">Seed {seed} · {"tight openings" if course=="tight" else "three obstacles"} · {round(delay*1000)} ms delay</option>' for seed,course,delay in keys)
 app=(root/'milestone-21-source/app.js').read_text().replace('milestone-21-source',f'milestone-{stage}-source')
 a=app.index('function select(){');b=app.index("\n$('contact').onclick",a)
 app=app[:a]+'''function select(){const [seedText,scenario,delayText]=$('scenario').value.split(':'),seed=+seedText,delay=+delayText;runs=['raw','predict'].map(estimator=>records.find(r=>r.config.scenario===scenario&&r.config.observationDelay===delay&&r.config.estimator===estimator&&r.config.seed===seed));$('contact').disabled=!runs.some(r=>r.metrics.stopReason);$('labelA').textContent='Use delayed positions';$('labelB').textContent='Predict current positions';t=0;playing=false;last=null;$('play').textContent='Play';$('findings').textContent='Seed '+seed+' · '+Math.round(delay*1000)+' ms delay in BOTH panels · 2.5 ms recorded replay. Original: '+runs[0].metrics.passed+'/50, '+(runs[0].metrics.stopReason||'no contact stop')+'. Prediction: '+runs[1].metrics.passed+'/50, '+(runs[1].metrics.stopReason||'no contact stop')+'. Every outcome and finer-step check is saved in the report.';render();views.forEach(v=>{v.setObstacle(scenario);v.reset();});}'''+app[b:]
 (root/f'milestone-{stage}-source/app.js').write_text(app)
 title='Can prediction compensate for delay?' if stage==22 else 'Does prediction help new flocks?'
 intro='Both flocks receive the same delayed measurements. On the right, each drone estimates current positions by continuing measured motion at the last known velocity. Separation, alignment and cohesion still use local neighbors; no leader or passage scheduler is added.'
 html=(root/'milestone-21-lab.html').read_text()
 html=html.replace('What if the flock sees the past?',title).replace('CHECKPOINT 21',f'CHECKPOINT {stage}')
 a=html.index('<p>The same 50');b=html.index('</p>',a)+4;html=html[:a]+'<p>'+intro+'</p>'+html[b:]
 html=re.sub(r'(<select disabled id="scenario">).*?(</select>)',r'\g<1>'+options+r'\g<2>',html,count=1)
 html=html.replace('Observation timing differs between the two panels; no observation noise is included.','Both panels have the same delay. Only the position estimate changes; measurement noise is off.').replace('Local neighbor links','Actual nearby drones').replace('Drag to orbit · Scroll to zoom.','Drag to orbit · Scroll to zoom. Pink links show actual displayed distances around drone 12, not the delayed or predicted observation graph.')
 if stage==22:
  finding='All three 100 ms prediction cases complete 50/50 at both physics steps, but seed 1103 fails the 1 cm trajectory-agreement check (55 cm difference). At 200 ms prediction causes contact while the original completes. Seven of eight planned numerical comparisons pass. The predictor is experimental, not a general fix.'
 else:
  rs=json.loads((root/f'milestone-{stage}-summary.json').read_text());coarse=[r for r in rs if r['config']['dt']==.0025];cmp=json.loads((root/f'milestone-{stage}-comparisons.json').read_text())
  desc=[]
  for est in ['raw','predict']:
   group=[r for r in coarse if r['config']['estimator']==est];success=sum(r['metrics']['passed']==50 and not r['metrics']['stopReason'] for r in group);contacts=sum(bool(r['metrics']['stopReason']) for r in group)
   desc.append(f'{"Original" if est=="raw" else "Prediction"}: {success}/{len(group)} complete flocks; {contacts} stopped run(s)')
  finding='Frozen tests on six new seeds and two courses at 100 ms delay. '+'. '.join(desc)+f'. {sum(c["passed"] for c in cmp)}/{len(cmp)} planned numerical comparisons pass. Development failures remain part of the evidence.'
 html=re.sub(r'(<p id="studyFinding">).*?(</p>)',r'\g<1>'+finding+r'\g<2>',html,count=1)
 a=html.index('<p><a href="research-block-19');b=html.index('</p>',a)+4
 links=f'<p><a href="research-block-22-23-summary.md">Plain-language summary</a> · <a href="milestone-{stage}-report.md">This checkpoint</a> · <a href="milestone-{stage}-summary.json">Every case</a> · <a href="milestone-{stage}-comparisons.json">Numerical checks</a> · <a href="milestone-{stage}-protocol.json">Frozen protocol</a> · <a href="milestone-22-lab.html">Development and 200 ms failure</a> · <a href="milestone-23-lab.html">Fresh flocks</a> · <a href="research-stage-log.md">Saved stages</a></p>'
 html=html[:a]+links+html[b:];html=html.replace('src="milestone-21-source/app.js"',f'src="milestone-{stage}-source/app.js"')
 (root/f'milestone-{stage}-lab.html').write_text(html)
 if stage==23:(root/'research-results.html').write_text(html)
