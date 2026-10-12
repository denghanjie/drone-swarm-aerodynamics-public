"""Post-hoc explanation of actual saved pre-contact updates; no new trials."""
from pathlib import Path
import json
import math

root = Path(__file__).resolve().parent.parent
source = root / 'milestone-31-source'
protocol = json.loads((root / 'milestone-31-protocol.json').read_text())
records = []
completed = 0
for job in protocol['jobs']:
    path = source / (job['id'] + '.json')
    if not path.exists():
        continue
    completed += 1
    run = json.loads(path.read_text())
    if not run['metrics']['stopReason']:
        continue
    affected = run['lastControl']['affected']
    record = dict(trial=job['id'], event=run['metrics']['failure'],
                  eventTime=run['metrics']['end'],
                  precedingControlTime=run['lastControl']['t'], walls=[])
    for drone in affected:
        for wall in drone['walls']:
            normal = wall['n'][:3]
            requested = sum(n*v for n, v in zip(normal, drone['velocity']))
            actual = sum(n*v for n, v in zip(normal, drone['actual']))
            record['walls'].append(dict(
                drone=drone['drone'], obstacle=wall['obstacle'],
                clearanceAtControl_m=0.3-1.2*wall['lower'],
                requiredOutwardVelocity_mps=wall['lower'],
                requestedOutwardVelocity_mps=requested,
                actualOutwardVelocity_mps=actual,
                commandDeficit_mps=max(0, wall['lower']-requested),
                adverseTrackingDifference_mps=max(0, requested-actual)))
    if run['metrics']['failure'].get('pair'):
        a, b = affected
        delta = [a['state'][k]-b['state'][k] for k in range(3)]
        distance = math.hypot(*delta)
        n = [x/distance for x in delta]
        pair_deficits = []
        for drone, other in [(a, b), (b, a)]:
            constraint = next((c for c in drone['pairs'] if c['neighbor'] == other['drone']), None)
            pair_deficits.append(None if constraint is None else max(
                0, constraint['lower']-sum(constraint['n'][k]*drone['velocity'][k] for k in range(3))))
        record['pairAtControl'] = dict(
            distance_m=distance,
            surfaceGap_m=distance-0.15,
            actualSeparationRate_mps=sum(n[k]*(a['actual'][k]-b['actual'][k]) for k in range(3)),
            requestedSeparationRate_mps=sum(n[k]*(a['velocity'][k]-b['velocity'][k]) for k in range(3)),
            collidingPairCommandDeficits_mps=pair_deficits,
            maximumAllPairConstraintDeficits_mps=[a['pairResidual'], b['pairResidual']])
    records.append(record)

result = dict(completedJobs=completed, plannedJobs=len(protocol['jobs']),
              scope='Post-hoc descriptions of the actual preceding control update. Positive outward velocity means moving away from the wall. Snapshot tracking differences are not uniform bounds or causal interventions.',
              contacts=records)
(root / 'milestone-31-contact-analysis.json').write_text(json.dumps(result, indent=2))
print(json.dumps(dict(completedJobs=completed, contactRecords=len(records))))
