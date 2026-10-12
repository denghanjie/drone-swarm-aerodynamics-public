from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
files=['milestone-22-report.md','milestone-23-report.md','research-block-22-23-summary.md','research-final-report.md','research-block-22-23-qa.md','research-physical-validation-gate-2026-10-12.md']
# Readability only; leave links, code, scientific notation and established3D notation intact.
for name in files:
 p=root/name
 if not p.exists():continue
 pieces=re.split(r'(`[^`]*`|\]\([^)]*\))',p.read_text())
 for i in range(0,len(pieces),2):
  s=pieces[i]
  s=re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', s)
  s=re.sub(r'(?<=\d)(?=(?:ms|cm|mm|Hz|N|V|g|m|s)\b)', ' ', s)
  s=re.sub(r'(?<=\d)(?=primary\b|predicted\b|drone\b|planned\b|preregistered\b)', ' ', s)
  s=s.replace('Step 5','Step 5').replace('3 D','3D')
  pieces[i]=s
 p.write_text(''.join(pieces))
