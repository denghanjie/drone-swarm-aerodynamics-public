"""Read frozen source text; extract three functions without importing that module."""
import re, json, hashlib
from pathlib import Path
base = Path(__file__).resolve().parents[1]
repo = base.parents[1]
p = repo / 'research/m31-body-load-2026-10-16/source/host.cjs'
data = p.read_bytes()
chunks = []
for name in ['fade', 'pairTerm', 'termAdmitted']:
    pattern = r'^function ' + name + (r'\([^\n]+\n[\s\S]*?^}\n' if name == 'pairTerm' else r'\([^\n]+\n')
    match = re.search(pattern, data.decode(), re.M)
    if not match:
        raise ValueError('Missing expected source function: ' + name)
    chunks.append(match.group(0))
assert len(chunks[1].splitlines()) == 30
output = "'use strict';\n// Exact historical function text; fresh source-accounting diagnostic only.\n" + '\n'.join(chunks) + '\nmodule.exports={fade,pairTerm,termAdmitted};\n'
(base / 'source/reference-excerpt.cjs').write_text(output)
(base / 'source/extraction.json').write_text(json.dumps({'sourcePath': str(p.relative_to(repo)), 'sourceSHA256': hashlib.sha256(data).hexdigest(), 'functions': [{'name': name, 'sha256': hashlib.sha256(chunk.encode()).hexdigest(), 'lines': len(chunk.splitlines())} for name,chunk in zip(['fade','pairTerm','termAdmitted'],chunks)], 'originalModuleImported': False, 'campaignExecuted': False}, indent=2)+'\n')
print('Extracted three source functions; none executed.')
