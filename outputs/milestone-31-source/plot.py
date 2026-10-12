"""Plot exact saved finish times for the three matched primary comparisons."""
from pathlib import Path
import hashlib
import json
import os

root = Path(__file__).resolve().parent.parent
os.environ.setdefault('MPLCONFIGDIR', str(root.parent / 'work' / 'mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

cases = [(1000, 2001, 'wide'), (1000, 2002, 'narrow'), (5000, 2001, 'wide')]
colors = {'baseline': '#c34f28', 'wall-priority': '#146d91'}
fig, axes = plt.subplots(1, 3, figsize=(15, 5.1), sharex=True, sharey=True)
sources = []
for ax, (count, seed, course) in zip(axes, cases):
    for filter_name in ['wall-priority', 'baseline']:
        name = f'heldout-{seed}-{count}-{course}-{filter_name}-0.0025.json'
        run = json.loads((root / 'milestone-31-source' / name).read_text())
        assert run['job']['kind'] == 'heldout' and run['config']['duration'] == 180
        m = run['metrics']
        times = sorted(t for t in run['crossings'] if t is not None)
        assert len(times) == m['passed'] and all(0 < t <= m['end'] for t in times)
        x = [0] + times + [m['end']]
        y = [0] + [100*i/count for i in range(1, len(times)+1)] + [100*m['passed']/count]
        color = colors[filter_name]
        ax.step(x, y, where='post', color=color, linewidth=2, zorder=3)
        if m['stopReason']:
            ax.plot(m['end'], y[-1], 'x', color=color, markersize=8, markeredgewidth=2, zorder=4)
            label = 'Contact' if 'contact' in m['stopReason'] else 'Model limit'
            ax.annotate(f'{label}: {m["end"]:.3f} s', (m['end'], y[-1]),
                        xytext=(12, 20 if filter_name == 'baseline' else 42),
                        textcoords='offset points', fontsize=9, color=color,
                        arrowprops=dict(arrowstyle='-', color=color, linewidth=0.8))
        else:
            ax.plot(m['end'], y[-1], 'o', color=color, markersize=4, zorder=4)
        if filter_name == 'wall-priority':
            ax.text(.03, .95, f'Corrected: {m["passed"]:,} / {count:,} finished',
                    transform=ax.transAxes, ha='left', va='top', fontsize=9.5,
                    bbox=dict(facecolor='white', edgecolor='none', alpha=.9))
        plotted_data = dict(count=count, seed=seed, course=course, filter=filter_name,
                            crossings=run['crossings'], end=m['end'], stop=m['stopReason'])
        digest = hashlib.sha256(json.dumps(plotted_data, sort_keys=True, allow_nan=False).encode()).hexdigest()
        sources.append(dict(file=name, plottedDataSha256=digest, **plotted_data))
    ax.set_title(f'{count:,} drones · {course} doors\nSeed {seed}', fontsize=12, pad=12)
    ax.set_xlim(0, 186)
    ax.set_ylim(-4, 108)
    ax.set_xticks([0, 60, 120, 180])
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlabel('Simulated time (s)', fontsize=10)
    ax.grid(axis='y', color='#dce3e9', linewidth=.7, zorder=0)
    ax.spines[['top', 'right']].set_visible(False)
    ax.spines[['bottom', 'left']].set_color('#9ca9b3')
    ax.tick_params(labelsize=9)
axes[0].set_ylabel('Flock finished (%)', fontsize=10)
fig.suptitle('Do the drones finish the factory course?', fontsize=18, x=.07, ha='left', y=.98)
fig.text(.07, .895, 'Matched controller comparisons · ideal observations · airflow off · primary 2.5 ms step', fontsize=10, color='#536777')
fig.legend(handles=[Line2D([0], [0], color=colors['baseline'], lw=2, label='Original controller'),
                    Line2D([0], [0], color=colors['wall-priority'], lw=2, label='Wall-priority controller'),
                    Line2D([0], [0], color='#343b42', marker='x', lw=0, label='Run stopped')],
           loc='lower center', bbox_to_anchor=(.5, .055), ncol=3, frameon=False, fontsize=10)
fig.text(.07, .025, 'Curves stop with the recorded run. Each panel compares identical starts; differences between panels do not isolate doorway width.', fontsize=9, color='#536777')
fig.subplots_adjust(left=.07, right=.985, top=.76, bottom=.24, wspace=.13)
fig.savefig(root / 'milestone-31-passage.png', dpi=160, facecolor='white')
fig.savefig(root / 'milestone-31-passage.pdf', facecolor='white', metadata={'CreationDate': None, 'ModDate': None})
plt.close(fig)
(root / 'milestone-31-figure-sources.json').write_text(json.dumps(dict(matplotlibVersion=matplotlib.__version__, sources=sources), indent=2))
print(json.dumps(dict(plottedRuns=len(sources), figure='milestone-31-passage.png')))
