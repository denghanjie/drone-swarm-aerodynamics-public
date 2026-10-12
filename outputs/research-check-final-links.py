"""Check local references in the current benchmark delivery documents."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re, json

root = Path(__file__).resolve().parent
names = ['research-results.html', 'research-final-report.md', 'research-block-26-29-summary.md',
         'research-roadmap.md', 'research-goal-completion-audit.md', 'research-contribution-assessment.md']
names += [f'milestone-{s}-{suffix}' for s in ['26','28','29','30','31'] for suffix in ['lab.html','report.md','qa.md']]
names += ['milestone-31-summary.md','milestone-31-interim-1000.md','milestone-31-interim-5000.md',
          'milestone-31-interim-refinement.md','milestone-31-source/method.md','milestone-31-source/plotting.md',
          'research-next-controller-gate.md','research-wall-priority-physics-note.md']
records = []
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs = []
    def handle_starttag(self, tag, attrs):
        self.refs += [v for k,v in attrs if k in ['href','src'] and v]

for name in names:
    path = root/name; source = path.read_text()
    if path.suffix == '.html':
        parser = Links(); parser.feed(source); refs = parser.refs
    else:
        refs = re.findall(r'\]\(([^)]+)\)', source)
    for ref in refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc or not url.path: continue
        target = path.parent/unquote(url.path)
        assert target.exists(), (name, ref)
        records.append({'document':name, 'reference':ref, 'exists':True})
(root/'research-final-link-checks.json').write_text(json.dumps(records, indent=2))
print({'localReferencesChecked':len(records), 'documents':len(names)})
