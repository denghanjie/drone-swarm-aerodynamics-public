#!/usr/bin/env python3
"""Download and verify the versioned release's research evidence. Python 3.9+."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,shutil,subprocess,tarfile,tempfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archive',type=Path,help='Use a previously downloaded archive');p.add_argument('--verify-only',action='store_true');args=p.parse_args()
m=json.loads((ROOT/'data/research-data-manifest.json').read_text());entries={e['path']:e for e in m['files']}
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def target(name):
 path=PurePosixPath(name)
 if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0]!='outputs':raise SystemExit('Unsafe archive path: '+name)
 dest=ROOT.joinpath(*path.parts)
 if not dest.resolve().is_relative_to(ROOT.resolve()):raise SystemExit('Path escapes checkout: '+name)
 return dest
missing=[]
for name,e in entries.items():
 dest=target(name)
 if not dest.exists():missing.append(name)
 elif not dest.is_file() or dest.stat().st_size!=e['bytes'] or digest(dest)!=e['sha256']:
  raise SystemExit('Local evidence differs; preserved without overwrite: '+name)
if not missing:
 print(f'All {len(entries)} evidence files verified.');raise SystemExit(0)
if args.verify_only:raise SystemExit(f'{len(missing)} evidence files missing; run this script without --verify-only to restore them.')
(ROOT/'work').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='research-data-',dir=ROOT/'work') as tmp:
 archive=args.archive.resolve() if args.archive else Path(tmp)/m['asset']
 if not args.archive:
  if not shutil.which('gh'):raise SystemExit('Install GitHub CLI and authenticate with gh auth login, or supply --archive.')
  subprocess.run(['gh','release','download',m['release'],'--repo',m['repository'],'--pattern',m['asset'],'--dir',tmp],check=True)
 if archive.stat().st_size!=m['archiveBytes'] or digest(archive)!=m['archiveSha256']:raise SystemExit('Archive checksum/size mismatch; no evidence restored.')
 seen=set()
 with tarfile.open(archive,'r|gz') as bundle:
  for member in bundle:
   if member.name not in entries or member.name in seen or not member.isfile():raise SystemExit('Unexpected archive member: '+member.name)
   e=entries[member.name];dest=target(member.name);seen.add(member.name)
   if member.size!=e['bytes']:raise SystemExit('Member size mismatch: '+member.name)
   if member.name not in missing:continue
   # Write and verify outside the destination before installing each missing file.
   staged=Path(tmp)/'current-member';h=hashlib.sha256()
   with bundle.extractfile(member) as source,staged.open('wb') as out:
    while chunk:=source.read(1024*1024):h.update(chunk);out.write(chunk)
   if h.hexdigest()!=e['sha256']:raise SystemExit('Member checksum mismatch: '+member.name)
   dest.parent.mkdir(parents=True,exist_ok=True)
   if dest.exists():raise SystemExit('Destination appeared during restore; not overwritten: '+member.name)
   os.replace(staged,dest)
 if seen!=entries.keys():raise SystemExit('Archive does not contain every expected evidence file.')
print(f'Restored {len(missing)} missing evidence files with verified SHA-256 checksums.')
