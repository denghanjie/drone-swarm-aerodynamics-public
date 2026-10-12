"""Generate the bounded benchmark synthesis only from complete frozen studies."""
from pathlib import Path
import json, csv

root = Path(__file__).resolve().parent
for stage, count in [('26', 11), ('28', 25), ('29', 48)]:
    rows = json.loads((root / f'milestone-{stage}-summary.json').read_text())
    assert len(rows) == count, (stage, len(rows))
costs = json.loads((root / 'milestone-29-costs.json').read_text())
assert costs['studyComplete']
table = ['|Drones|No airflow|Mean wake: force|Mean wake: moments|Alternative overlap|',
         '|---:|---:|---:|---:|---:|']
for count in [50, 200, 1000, 5000]:
    cells = []
    for mode in ['off', 'sum-force', 'sum-rotor', 'rss-rotor']:
        row = next(x for x in costs['groups'] if x['count'] == count and x['model'] == mode)
        cells.append(f"{row['total']:.2f} s" if row['fullWindows'] == 3 else f"{row['fullWindows']}/3 full windows; no matched cost")
    table.append('|' + str(count) + '|' + '|'.join(cells) + '|')

summary = '''# Factory-flock benchmark: what we learned

The bounded complex-environment benchmark is finished. We built the requested local 3D flock, tested it through 5,000 drones, compared clearly labeled airflow assumptions, and preserved the failures. The broader research into physically accurate, reliable drone swarms remains open.

## Goal

Find out whether drones following local group rules can travel through a complex factory, what breaks as the flock grows, and what the computation costs. Establishing real aerodynamic accuracy requires independent measurements, which we do not yet have.

## Method

Each drone reacts to nearby drones using separation, alignment and cohesion—the three Boids rules. All receive the same broad route through a factory with 34 solid obstacles and three offset openings. Each computes its own motion; there are no individual flight schedules. A rigid-body model, motor lag and a local avoidance filter translate those preferences into movement.

Starting flocks, settings and acceptance thresholds were fixed before each study. We saved the source, states and exact replay frames. We separately checked finer physics steps, more frequent airflow updates and actual calculation time. Three.js displays recorded motion; it is not performing the research integrations live.

## Results

**Small flocks get through; larger flocks reveal a navigation limit.** All six primary 50/200-drone cases in milestone26 finish. The 1,000- and 5,000-drone cases contact the first partition at16.020s and11.9525s. Smaller physics steps repeat the same affected drone and wall with approximately1mm endpoint differences. Both flocks remain connected: staying together does not imply safe passage. Only one primary seed was tested at each large count.

**Numerical agreement is mixed.** The200-drone narrow case completes at both physics steps, but final positions differ by5.45cm, exceeding the1cm criterion. The5,000 primary stops before its prescribed20s comparison checkpoint; that original criterion remains unmet. Its early-stop comparison is a separately declared supplement.

**Airflow assumptions matter, but accuracy is unresolved.** All five corrected airflow-off primary cases finish; all 15 primary cases with active airflow stop by contact or a declared model limit. A model-limit stop means the state left the range we chose to model; it is not evidence that a real drone crashes at that instant. Four physics-step checks agree. However, updating the airflow every5ms instead of10ms changes one stopping time from7.769s to8.994s. We cannot call the airflow trajectories converged merely because smaller rigid-body steps agree.

We also found and corrected a wake-length mapping error: the paper specifies opposite-motor spacing, while the earlier implementation used adjacent spacing. The erroneous20 primary runs and five uncompleted refinements remain labeled in milestone27. The corrected25-run study is milestone28. Neither version is independent physical validation. The factory walls affect obstacle avoidance, but their effects on airflow are omitted. The receiver response, overlapping wakes and controller's limited compensation remain assumptions.

**Calculation and display have different costs.** The following are median wall times for one simulated second, with three serial repeats of the same startup scene. A stopped window is excluded from full-window rankings.

''' + '\n'.join(table) + '''

These timings include local steering, physics, contact checks, airflow and in-memory recording. They exclude process startup, warmup and file serialization. Background operating-system/browser load is uncontrolled, and identical repeats show substantial runtime variation. These are descriptive session measurements rather than stable hardware guarantees. They measure startup scenes, not crowded doorways. Earlier replay measurements gave a median frame interval of about16.7ms at all four counts; that is display performance, not real-time simulation or GPU physics evidence.

## Conclusion and implications

The concept is achievable as an inspectable simulation benchmark. We have not demonstrated reliable5,000-drone factory passage, accurate multi-drone aerodynamics or a new flocking algorithm. These failures identify where the setup needs improvement or validation; they do not prove that such flocks are physically impossible. The factory social-rule ablations also finish, so this course does not establish a passage advantage for Boids.

Further work is worthwhile if it targets the unresolved scientific questions: obtain matched physical wake/force data, verify receiving-rotor response and airflow update convergence, then compare stronger navigation/control baselines under frozen tests. More visual complexity alone would add little evidence. A defensible potential contribution is a validated accuracy-versus-cost comparison for local flocks; the accuracy half is still missing.

## Records and 3D views

- [Factory missions and large-flock failures](milestone-26-lab.html) · [report](milestone-26-report.md).
- [Corrected airflow comparison](milestone-28-lab.html) · [report](milestone-28-report.md).
- [Actual workload through5,000 drones](milestone-29-lab.html) · [report](milestone-29-report.md).
- [All planned cases as CSV](research-block-26-29-trials.csv) · [Stage history](research-stage-log.md) · [eight-step roadmap](research-roadmap.md) · [completion audit](research-goal-completion-audit.md).
- [Correction record](research-wake-normalization-correction.md) · [prior-art assessment](research-contribution-assessment.md) · [physical measurement gate](research-physical-validation-gate-2026-10-12.md).
- [Artifact manifest](research-manifest.json) · [reproduction helper](research-reproduce.py).

This block retains104 completed numerical executions:11 mission cases,20 erroneous-model historical cases,25 corrected cases and48 workload repeats. Five original erroneous-model refinements are explicitly uncompleted; they are not counted as results. Development checks and previous milestones are additional records.
'''
for old,new in {'milestone26':'milestone 26','milestone27':'milestone 27','milestone28':'milestone 28','at16.020s':'at 16.020 s','and11.9525s':'and 11.9525 s','approximately1mm':'approximately 1 mm','The200':'The 200','by5.45cm':'by 5.45 cm','the1cm':'the 1 cm','The5,000':'The 5,000','prescribed20s':'prescribed 20 s','every5ms':'every 5 ms','instead of10ms':'instead of 10 ms','from7.769s':'from 7.769 s','to8.994s':'to 8.994 s','erroneous20':'erroneous 20','corrected25':'corrected 25','about16.7ms':'about 16.7 ms','reliable5,000':'reliable 5,000','through5,000':'through 5,000','retains104':'retains 104','executions:11':'executions: 11','cases,20':'cases, 20','cases,25':'cases, 25','and48':'and 48'}.items():
    summary=summary.replace(old,new)
(root / 'research-block-26-29-summary.md').write_text(summary)
(root / 'research-final-report.md').write_text(summary.replace('# Factory-flock benchmark: what we learned', '# Research status — benchmark complete, physical validation open', 1))
with (root/'research-block-26-29-trials.csv').open('w', newline='') as stream:
    writer = csv.writer(stream)
    writer.writerow(['stage','evidenceClass','job','executionStatus','count','seed','course','airflow','kind',
                     'physicsStepS','airflowRefreshS','horizonS','recordedEndS','finishedDrones','stopReason',
                     'measuredWallMs','record'])
    for stage, evidence in [('26','modeled-navigation'),('27','erroneous-normalization-record'),
                            ('28','assumption-sensitivity'),('29','startup-cost')]:
        protocol = json.loads((root/f'milestone-{stage}-protocol.json').read_text())
        runs = {r['job']['id']:r for r in json.loads((root/f'milestone-{stage}-progress.json').read_text())}
        for j in protocol['jobs']:
            r = runs.get(j['id']); m = r['metrics'] if r else {}
            writer.writerow([stage,evidence,j['id'],'complete-record' if r else 'uncompleted',j['count'],
                             j['seed'],j['course'],j.get('aeroMode','off'),j['kind'],j['dt'],j.get('flowDt',''),
                             j['duration'],m.get('end',''),m.get('passed',''),m.get('stopReason') or '',
                             r.get('timing',{}).get('total','') if r else '',
                             f"milestone-{stage}-source/{j['id']}.json" if r else 'milestone-27-termination.json'])
print('Wrote synthesis from complete frozen studies.')
