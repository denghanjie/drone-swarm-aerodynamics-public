"""Audit immutable full-mission results and render a reproducible readout."""
from pathlib import Path
import json,math,struct,hashlib,csv,statistics
root=Path(__file__).resolve().parent.parent;d=root/'milestone-31-source';protocol=json.loads((root/'milestone-31-protocol.json').read_text());runs=[];checks=[]
def save(name,obj):(root/name).write_text(json.dumps(obj,indent=2))
def check(ok,label):
 checks.append(dict(passed=bool(ok),check=label))
 if not ok:raise AssertionError(label)
def frames(r):
 raw=(d/r['replay']['file']).read_bytes();w=r['replay']['valuesPerFrame'];check(len(raw)==8*w*r['replay']['frames'],'binary bytes '+r['job']['id']);v=struct.unpack('<'+'d'*(len(raw)//8),raw);return [v[i:i+w] for i in range(0,len(v),w)]
def event_identity(m):
 f=m['failure']
 return None if f is None else dict(reason=m['stopReason'],drone=f.get('drone'),pair=f.get('pair'),obstacles=[b['id'] for b in f.get('hits',[])])
for rel,h in protocol['sourceHashes'].items():check(hashlib.sha256((d/rel).read_bytes()).hexdigest()==h,'frozen '+rel)
check((d/'wall-filter.cjs').read_bytes()==(root/'milestone-30-source/wall-filter.cjs').read_bytes(),'frozen controller identical to milestone30')
for job in protocol['jobs']:
 r=json.loads((d/(job['id']+'.json')).read_text());runs.append(r);n=job['count'];f=frames(r)
 check(all(r['config'][k]==job[k] for k in ['seed','count','dt','duration','filter']) and r['config']['course']==json.loads((d/('factory-'+job['course']+'.json')).read_text())['id'],'configuration '+job['id'])
 check(r['config']['airflow']=='off' and r['config']['observation']=='ideal' and r['config']['mode']=='boids','scope '+job['id'])
 check(r['replay']['valuesPerFrame']==1+7*n,'frame layout '+job['id'])
 check(len(r['initial'])==n and len(r['final'])==n and len(r['crossings'])==n and all(len(s)==17 for s in r['initial']+r['final']),'state dimensions '+job['id'])
 check(all(math.isfinite(v) for s in r['initial']+r['final'] for v in s),'finite states '+job['id'])
 check(all(math.isfinite(v) for row in f for v in row),'finite poses '+job['id'])
 check(all(math.isfinite(v) for v in r['diagnostics'].values()),'finite diagnostics '+job['id'])
 check(f[0][0]==0 and f[-1][0]==round(r['metrics']['end'],6),'frame endpoints '+job['id'])
 check(all(f[i][0]<f[i+1][0] for i in range(len(f)-1)),'ordered frames '+job['id'])
 for states,frame in [(r['initial'],f[0]),(r['final'],f[-1])]:check(all(list(frame[1+7*i:8+7*i])==s[:3]+s[6:10] for i,s in enumerate(states)),'exact poses '+job['id'])
 check(all(abs(sum(s[k]*s[k] for k in range(6,10))-1)<1e-10 for s in r['final']),'unit quaternions '+job['id'])
 check(r['diagnostics']['updates']==n*math.ceil(r['metrics']['end']/.01-1e-8),'control count '+job['id'])
 check(r['metrics']['end']<=job['duration'] and (r['metrics']['stopReason'] is not None or r['metrics']['end']==job['duration']),'terminal accounting '+job['id'])
 check(r['metrics']['passed']==sum(t is not None for t in r['crossings']),'crossing count '+job['id'])
 check(all(t is None or 0<t<=r['metrics']['end'] for t in r['crossings']),'crossing times '+job['id'])
 if r['metrics']['stopReason']:
  check(0<r['metrics']['end']-r['lastControl']['t']<=.01000001,'preceding control timing '+job['id'])
  affected=r['metrics']['failure'].get('pair',[r['metrics']['failure'].get('drone')]);check([a['drone'] for a in r['lastControl']['affected']]==affected,'affected identities '+job['id'])
  for a in r['lastControl']['affected']:
   check(len(a['state'])==17 and all(math.isfinite(v) for v in a['state']),'precontrol state '+job['id'])
   check(a['actual']==a['state'][3:6],'actual precontrol velocity '+job['id'])
   check(len(a['actuator']['u'])==4 and all(0<=u<=2.25*.027*9.81/4 for u in a['actuator']['u']),'motor targets '+job['id'])
   check(all('obstacle' in w for w in a['walls']) and all('neighbor' in q for q in a['pairs']),'constraint identities '+job['id'])
for seed,n,course in [(2001,1000,'wide'),(2002,1000,'narrow'),(2001,5000,'wide')]:
 pair=[r for r in runs if r['job']['kind']=='heldout' and all(r['job'][k]==v for k,v in [('seed',seed),('count',n),('course',course)])];check(len(pair)==2 and pair[0]['initial']==pair[1]['initial'],'matched initial '+str((seed,n,course)))
# Check the old development window without rerunning or changing its historical source.
dev=next(r for r in runs if r['job']['kind']=='development');cp_path=d/('checkpoint-'+dev['job']['id']+'-20.json');check(cp_path.exists(),'development reached retained20s checkpoint')
checkpoint=json.loads(cp_path.read_text());prior=json.loads((d/protocol['developmentCheckpointReference']).read_text());check(checkpoint['states']==prior['final'],'exact development20s continuation');save('milestone-31-continuation-check.json',dict(exactFullStateAgreement=True,count=5000,t=20,reference=protocol['developmentCheckpointReference']))
comparisons=[]
for b in runs:
 if b['job']['kind'] not in ['refinement','window-refinement']:continue
 a=next(r for r in runs if r['job']['kind']=='heldout' and all(r['job'][k]==b['job'][k] for k in ['seed','count','course','filter']))
 check(a['initial']==b['initial'],'refinement initial '+b['job']['id']);limit=b['job']['duration'];status='full mission';am=a['metrics']
 if b['job']['kind']=='window-refinement':
  if a['metrics']['end']>=limit:
   cp=d/('checkpoint-'+a['job']['id']+'-'+str(limit)+'.json');check(cp.exists(),'primary window checkpoint exists');cp=json.loads(cp.read_text());am=dict(end=cp['t'],passed=cp['passed'],stopReason=cp['stopReason'],failure=a['metrics']['failure'] if a['metrics']['end']==limit else None);status='first 60 s only; primary checkpoint used'
  else:status='primary stopped before 60 s; early-stop comparison only'
 fa={round(f[0],8):f for f in frames(a) if f[0]<=limit};fb={round(f[0],8):f for f in frames(b)};times=sorted(set(fa)&set(fb));position_profile=[]
 for t in times:
  errors=sorted(math.dist(fa[t][1+7*i:4+7*i],fb[t][1+7*i:4+7*i]) for i in range(a['config']['count']))
  position_profile.append(dict(t=t,maximum=max(errors),median=statistics.median(errors),p95NearestRank=errors[math.ceil(.95*len(errors))-1]))
 maximum=max(row['maximum'] for row in position_profile);first_exceed=next((row['t'] for row in position_profile if row['maximum']>=.01),None);bm=b['metrics'];same=event_identity(am)==event_identity(bm) and am['stopReason']==bm['stopReason'];count=am['passed']==bm['passed'];gap=abs(am['end']-bm['end'])
 comparisons.append(dict(coarse=a['job']['id'],fine=b['job']['id'],scope=status,commonSavedTimes=times,positionDifferenceAtSavedTimes=position_profile,firstSavedTimeAtOrAboveOneCentimeter=first_exceed,maximumSynchronizedPositionDifference=maximum,withinOneCentimeter=maximum<.01,terminalTimes=[am['end'],bm['end']],sameEventIdentity=same,samePassageCount=count,terminalTimeDifference=gap,passed=maximum<.01 and same and count and gap<.01))
save('milestone-31-comparisons.json',comparisons)
# Prespecified descriptive motion flag uses only the final unfinished cohort.
progress=[]
for r in runs:
 f=frames(r);available={round(row[0],8):row for row in f};end=math.floor(r['metrics']['end']);ids=[i for i,x in enumerate(r['crossings']) if x is None];start=end-10
 displacement=None if not ids or start<0 or start not in available or end not in available else sum(available[end][1+7*i]-available[start][1+7*i] for i in ids)/len(ids)
 progress.append(dict(trial=r['job']['id'],unfinished=len(ids),timeWindow=[start,end] if displacement is not None else None,meanForwardDisplacement=displacement,lowProgressFlag=None if displacement is None else displacement<.2,interpretation='Descriptive last10s motion of final unfinished cohort; not permanent deadlock and not an early-stop rule.'))
save('milestone-31-motion-checks.json',progress)
# Exact commands sent before contact, including the flight-controller motor targets.
traces=[]
for r in runs:
 if r['metrics']['stopReason']:traces.append(dict(trial=r['job']['id'],event=r['metrics']['failure'],stopReason=r['metrics']['stopReason'],eventTime=r['metrics']['end'],**r['lastControl']))
save('milestone-31-precontact-commands.json',traces)
index=[dict(config=r['config'],metrics=r['metrics'],job=r['job'],file=r['job']['id']+'.json',geometry='factory-'+r['job']['course']+'.json') for r in runs]
hist_path=d/protocol['historicalBaseline'];hist=json.loads(hist_path.read_text());index.append(dict(config={**hist['config'],'filter':'baseline'},metrics=hist['metrics'],job={**hist['job'],'kind':'historical baseline'},file=protocol['historicalBaseline'],geometry='factory-wide.json',replayDir='../milestone-26-source/'));(d/'index.json').write_text(json.dumps(index))
with (root/'milestone-31-trials.csv').open('w',newline='') as f:
 writer=csv.writer(f);writer.writerow(['role','seed','count','doors','filter','dt_s','planned_horizon_s','actual_end_s','passed','stop','failure','minimum_connected_fraction','minimum_sampled_obstacle_clearance_m','minimum_sampled_pair_distance_m','wall_residual_max_mps','pair_residual_max_mps','wall_request_violations_after','pair_request_violations_after','repair_iteration_limit_updates','repair_max_iterations','low_progress_flag'])
 for r,p in zip(runs,progress):
  j=r['job'];m=r['metrics'];v=r['diagnostics'];writer.writerow([j['kind'],j['seed'],j['count'],j['course'],j['filter'],j['dt'],j['duration'],m['end'],m['passed'],m['stopReason'] or '',json.dumps(m['failure']),m['minimumConnectedFraction'],m['minimumSampledObstacleClearance'],m['minimumSampledSeparation'],v['maxWallAfter'],v['maxPairAfter'],v['wallViolationsAfter'],v['pairViolationsAfter'],v['unconverged'],v['maxIterations'],p['lowProgressFlag']])
save('milestone-31-artifact-checks.json',dict(checks=len(checks),passed=all(c['passed'] for c in checks),details=checks))
text='''# Milestone 31 — full factory missions

The question is whether the wall-priority correction that helped during the first20seconds can carry a large flock through the complete factory. The controller is fixed; local3D Boids and shared route guidance remain active. Airflow is off and observations ideal. These are simulation results, not physical validation.

## Results

|Role|Seed|Drones|Doors|Filter|Step ms|Horizon s|End s|Finished|Outcome|
|---|---:|---:|---|---|---:|---:|---:|---:|---|
'''
for r in runs:
 j=r['job'];m=r['metrics'];text+=f"|{j['kind']}|{j['seed']}|{j['count']}|{j['course']}|{j['filter']}|{j['dt']*1000:g}|{j['duration']}|{m['end']:.5f}|{m['passed']}/{j['count']}|{m['stopReason'] or 'horizon reached'}|\n"
text+='\nOne contact stops the whole run. An unfinished drone is not an independently observed collision. Reaching the180-second horizon with unfinished drones is not automatically a permanent jam. Completed drones keep flying and remain included in connectivity and contact checks.\n\n## Numerical refinement\n\n'
for c in comparisons:text+=f"- **{c['fine']}** — {c['scope']}. Maximum synchronized position difference {c['maximumSynchronizedPositionDifference']:.8g} m at {len(c['commonSavedTimes'])} common saved times through {c['commonSavedTimes'][-1]} s. 1 cm criterion: {c['withinOneCentimeter']}; first saved time at or above 1 cm: {c['firstSavedTimeAtOrAboveOneCentimeter']} s; event identity:{c['sameEventIdentity']}; count:{c['samePassageCount']}; end times:{c['terminalTimes']}; combined criterion:{c['passed']}.\n"
text+='\nThese comparisons cover exact recorded poses, not an error bound between frames. The5,000-drone refinement cannot validate any later part of a full mission. Numerical agreement is not measured-flight agreement. The three new baseline contact cases use the primary step only; this milestone does not independently refine each baseline collision time.\n\n## Does an unfinished flock still move?\n\n|Trial|Final unfinished|Window s|Mean forward displacement m|Low-progress flag|\n|---|---:|---|---:|---|\n'
for p in progress:
 window='not available' if p['timeWindow'] is None else ' to '.join(map(str,p['timeWindow']))
 displacement='not assessed' if p['meanForwardDisplacement'] is None else f"{p['meanForwardDisplacement']:.4f}"
 flag='not assessed' if p['lowProgressFlag'] is None else ('yes' if p['lowProgressFlag'] else 'no')
 text+=f"|{p['trial']}|{p['unfinished']}|{window}|{displacement}|{flag}|\n"

text+='\nThis prespecified descriptive flag uses the final unfinished drones over the last complete10-second recorded interval. A mean advance below0.2m raises the flag; it does not establish permanent deadlock. A null/blank flag means it was not assessed because no unfinished cohort or full ten-second window was available. It does not change when the simulation stops.\n\n## Contact diagnostics\n\nObstacle and neighboring-drone IDs, actual states, requested velocities and motor targets are saved in [the pre-contact traces](milestone-31-precontact-commands.json). These are the actual preceding control update, not a reconstruction at the contact state. Motor targets differ from the lagged thrusts stored in the state. A compliant wall command does not guarantee pair safety or instantaneous tracking.\n\n## Records and limits\n\n[3D replay](milestone-31-lab.html) · [Frozen protocol](milestone-31-protocol.json) · [Method](milestone-31-source/method.md) · [Trial CSV](milestone-31-trials.csv) · [Artifact audit](milestone-31-artifact-checks.json) · [Interface checks](milestone-31-checks.json) · [Exact20-second continuation check](milestone-31-continuation-check.json) · [Controller-output audit](milestone-31-control-audit.json) · [Post-hoc contact explanation](milestone-31-contact-analysis.json) · [Why the wall margin helps](research-wall-priority-physics-note.md).\n\nAll earlier numerical sources remain preserved. Count changes grow the starting cloud at fixed nominal spacing; they do not measure fixed-volume density scaling. The wide and narrow1,000-drone scenarios use different seeds, so geometry and seed effects are not isolated across them; the controller comparisons within each scenario are matched. Two subprocesses may overlap, so elapsed times are not a scaling benchmark. No general navigation safety, physical accuracy, airflow validity or algorithmic novelty is established.\n'
diagnostic_text='## Controller diagnostics\n\n|Trial|Wall-request violations after filtering|Pair-request violations after filtering|Repair stop criterion unmet|Maximum wall deficit m/s|\n|---|---:|---:|---:|---:|\n'
for r in runs:
 v=r['diagnostics'];unconverged=v['unconverged'] if r['config']['filter']=='wall-priority' else 'not applied'
 diagnostic_text+=f"|{r['job']['id']}|{v['wallViolationsAfter']}|{v['pairViolationsAfter']}|{unconverged}|{v['maxWallAfter']:.8g}|\n"
diagnostic_text+='\nViolation counts use the frozen 1e-7 m/s threshold and count drone-control updates, not distinct drones or contacts. The repair stop criterion requires both feasible residual and a sufficiently small iterate change. Reaching its 512-iteration limit is reported even if the returned request is feasible; constraint residuals and mission outcomes remain separate. Wall priority can soften pair avoidance. Neither a low residual nor a completed mission establishes physical safety.\n\n'
text=text.replace('## Records and limits',diagnostic_text+'## Records and limits')
if (root/'milestone-31-passage.png').exists():
 text=text.replace('## Results','## Passage over time\n\n![Fraction of each matched flock crossing the finish line](milestone-31-passage.png)\n\nCurves use the exact saved finish times and stop at the recorded end. These are individual matched cases, not averages or statistical safety rates. [Vector PDF](milestone-31-passage.pdf) · [Figure data and hashes](milestone-31-figure-sources.json) · [Plot reproduction](milestone-31-source/plotting.md).\n\n## Results',1)
# Plain-language synopsis uses actual outcomes, including negative results.
primary=[r for r in runs if r['job']['kind'] in ['heldout','development']];candidate=[r for r in primary if r['config']['filter']=='wall-priority'];base=[r for r in primary if r['config']['filter']=='baseline']
intro=f"## Plain-language finding\n\nThe corrected controller completes the whole course with every drone and no stop in {sum(r['metrics']['passed']==r['config']['count'] and r['metrics']['stopReason'] is None for r in candidate)}/{len(candidate)} primary cases. The matched fresh-seed baselines complete in {sum(r['metrics']['passed']==r['config']['count'] and r['metrics']['stopReason'] is None for r in base)}/{len(base)} cases. These small, prescribed case sets are not statistical safety rates.\n\n"
if any(r['metrics']['stopReason'] for r in candidate):intro+='The short-window wall improvement is insufficient for reliable full missions. The new failures need diagnosis and numerical checks before selecting another controller change; do not promote this controller as a solved navigation method.\n\n'
elif any(r['metrics']['passed']<r['config']['count'] for r in candidate):intro+='The candidate avoids contact in these primary runs but leaves drones unfinished at the 180-second limit. The motion records distinguish continued movement from low progress; longer runs would be needed to establish eventual completion.\n\n'
else:intro+='The candidate passes these prescribed primary missions. Broader geometry, delayed observations and physical validation remain separate gates.\n\n'
disconnected=[r for r in candidate if r['metrics']['minimumConnectedFraction']<1]
if disconnected:
 intro+='Complete passage does not mean the flock stayed fully connected throughout. The lowest sampled largest-group fractions were '+', '.join(f"{r['job']['kind']} seed {r['config']['seed']}, {r['config']['count']:,} drones: {r['metrics']['minimumConnectedFraction']:.6g}" for r in disconnected)+'. The trial CSV retains every sampled minimum.\n\n'
intro+=f"The prescribed finer-step checks meet all numerical criteria in {sum(c['passed'] for c in comparisons)}/{len(comparisons)} comparisons. The 5,000-drone check covers only the first 60 seconds."+'\n\n'
if any(not c['passed'] for c in comparisons):intro+='A failed numerical criterion remains a limitation even when both runs complete the course. Read the separate trajectory, event and passage-count comparisons below before treating the motion as numerically resolved.\n\n'
intro+='The development 5,000-drone case reuses an earlier starting flock. It is reported separately from the fresh-seed comparisons and does not receive a full-mission refinement in this protocol.\n\n'
intro_target='## Passage over time' if '## Passage over time' in text else '## Results'
text=text.replace(intro_target,intro+intro_target,1)
for a,b in [('first20seconds','first 20 seconds'),('local3D','local 3D'),('the180-second','the 180-second'),('difference{','difference {'),('The5,000','The 5,000'),('complete10-second','complete 10-second'),('below0.2m','below 0.2 m'),('Exact20-second','Exact 20-second'),('narrow1,000','narrow 1,000')]:text=text.replace(a,b)
(root/'milestone-31-report.md').write_text(text)
print(json.dumps(dict(runs=len(runs),checks=len(checks),comparisons=[{k:v for k,v in c.items() if k not in ['commonSavedTimes','positionDifferenceAtSavedTimes']} for c in comparisons]),indent=2))
