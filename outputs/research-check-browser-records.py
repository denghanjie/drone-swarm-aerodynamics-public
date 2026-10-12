"""Compare UI-observed outcomes with completed saved experiment records."""
from pathlib import Path
import json, sys

root = Path(__file__).resolve().parent
modes = {'off':'No airflow', 'sum-force':'Mean wake · force only',
         'sum-rotor':'Mean wake · rotor moments', 'rss-rotor':'Alternative overlap · rotor moments'}
checks = []
for stage in sys.argv[1:] or ['26', '28', '29']:
    index = json.loads((root/f'milestone-{stage}-source/index.json').read_text())
    views = json.loads((root/f'milestone-{stage}-browser-cases.json').read_text())
    assert len(index) == len(views), stage
    for entry, view in zip(index, views):
        r = json.loads((root/f'milestone-{stage}-source'/entry['file']).read_text())
        j, m = r['job'], r['metrics']
        label = f"{j['count']} drones · seed {j['seed']} · {j['course']} · "
        if stage != '26': label += modes[j['aeroMode']] + ' · '
        label += j['kind']
        assert view['trial'] == label, (stage, j['id'], view['trial'])
        times = view['clock'].removesuffix(' s').split(' / ')
        assert all(abs(float(t)-m['end']) <= .000501 for t in times), j['id']
        if stage != '29':
            assert view['completed'] == f"{m['passed']} / {j['count']}", j['id']
        else:
            assert abs(float(view['completed'].removesuffix(' s'))-r['timing']['total']/1000) <= .00501, j['id']
        if m['stopReason']:
            assert m['stopReason'] in view['status'], j['id']
            failure = m['failure']
            if failure.get('drone') is not None:
                assert f"Drone {failure['drone']}" in view['status'], j['id']
            for hit in failure.get('hits', []):
                assert hit['id'] in view['status'], j['id']
        checks.append({'stage':stage, 'job':j['id'], 'passed':True})
(root/'research-browser-outcome-checks.json').write_text(json.dumps(checks, indent=2))
print({'matchedVisibleOutcomes':len(checks), 'stages':sys.argv[1:] or ['26','28','29']})
