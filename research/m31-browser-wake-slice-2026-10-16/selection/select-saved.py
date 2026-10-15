"""Authorized saved-only ranking; no pose, geometry, wake, root or GPU evaluation."""
import argparse, base64, collections, hashlib, json, math, pathlib, platform, struct, sys, zlib

MANIFEST_SHA='f45749c824579ebb522d81484ba1814eb1d9e2073f68b9df12d82e959a586626'
PRIOR='research/m31-zero-screen-2026-10-16'
EXPECTED={
 'fresh5000-I.f64':(680000,'cc17e5d23a3761f5b175c987c1ca1d8a1631f34f0502ac533365b8c8526043aa'),
 'fresh5000-source-audit.ndjson':(9519110,'2844f10cb3490bdc3756c048fa26a5430f447bcc85d0d1452df70ca911788302'),
 'fresh5000-states.f64':(680000,'6e7e813c8b4127a4fa567249f0bf685d460adc6de2dd6a59fc4444f1a153a1bb'),
}
sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 repo=pathlib.Path(a.repo).resolve();out=pathlib.Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
 assert not (out/'selection.json').exists(),'Selection already exists; do not rerank'
 manifest_bytes=(repo/PRIOR/'manifest.json').read_bytes();assert sha(manifest_bytes)==MANIFEST_SHA
 manifest=json.loads(manifest_bytes);pins={x['path']:x for x in manifest['files']}
 data={};sources=[]
 for name,(size,digest) in EXPECTED.items():
  rel=f'{PRIOR}/raw/{name}';pin=pins[rel];assert pin['bytes']==size and pin['sha256']==digest
  b=(repo/rel).read_bytes();assert len(b)==size and sha(b)==digest
  sources.append({'path':rel,'bytes':size,'sha256':digest,'use':'hash only; never decoded' if name.endswith('states.f64') else 'saved evidence selection'})
  if not name.endswith('states.f64'):data[name]=b
 matrix=data['fresh5000-I.f64'];audits=[json.loads(line) for line in data['fresh5000-source-audit.ndjson'].splitlines()]
 assert len(audits)==5000
 candidates=[]
 for i,row in enumerate(audits):
  assert row['receiver']==i and isinstance(row['contributions'],int) and row['contributions']>=0
  u=list(struct.unpack_from('<4d',matrix,17*i*8));assert all(math.isfinite(v) and v>=0 for v in u)
  candidates.append({'receiverId':i,'maximumSavedInflow':max(u),'minimumSavedInflow':min(u),'savedRotorSpread':max(u)-min(u),'savedContributionCount':row['contributions'],'winds':u})
 rules=[('largest maximum saved rotor inflow',lambda r:(-r['maximumSavedInflow'],r['receiverId'])),('largest saved contribution count among remaining IDs',lambda r:(-r['savedContributionCount'],r['receiverId'])),('smallest maximum saved rotor inflow among remaining IDs',lambda r:(r['maximumSavedInflow'],r['receiverId'])),('largest saved maximum-minus-minimum rotor inflow among remaining IDs',lambda r:(-r['savedRotorSpread'],r['receiverId']))]
 chosen=[];used=set();files=[]
 for index,(rule,key) in enumerate(rules):
  selected=min((r for r in candidates if r['receiverId'] not in used),key=key);i=selected['receiverId'];used.add(i);audit=audits[i]
  codes=zlib.decompress(base64.b64decode(audit['codesDeflateBase64']));assert len(codes)==20000==audit['codesLength'] and sha(codes)==audit['codesSha256']
  actual=[codes.count(c) for c in range(8)];assert actual==audit['codeCounts'] and sum(actual)==20000
  assert all(c in range(8) for c in codes) and actual[3]==0
  inflow_bytes=matrix[17*i*8:17*i*8+32]
  assert struct.pack('<4d',*audit['row'][:4])==inflow_bytes
  code_name=f'selected-{index}-codes.u8';sum_name=f'selected-{index}-saved-sums.f64'
  for name,b in [(code_name,codes),(sum_name,inflow_bytes)]:
   with (out/name).open('xb') as f:f.write(b)
   files.append({'name':name,'bytes':len(b),'sha256':sha(b)})
  per_rotor=[[sum(codes[4*j+k]==c for j in range(5000)) for c in range(8)] for k in range(4)]
  chosen.append({**selected,'selectedIndex':index,'rule':rule,'tieBreak':'ascending receiverId','savedSumFloat64LEHex':inflow_bytes.hex(),'savedEligibleSources':audit['eligible'],'savedCodeCounts':actual,'savedCodeCountsPerRotor':per_rotor,'savedCodePath':code_name,'savedCodeSha256':sha(codes),'savedSumsPath':sum_name,'strictlyPositiveTerms':'Not retained in prior successful source audit; not inferred from code 7 or contribution count'})
 summary={'kind':'saved-only-exposed-selection','status':'completed','selectionRuleVersion':'four-distinct-saved-ranking-v1','priorSourceCommit':'cefe6c7bb47362e90135179d22a9721b6f03bb88','receiverPublishedCommit':'2ba59cc634c4634011aa78df4caceda399761efc','priorManifestSha256':MANIFEST_SHA,'sourcePins':sources,'selected':chosen,'artifacts':files,'scriptSha256':sha(pathlib.Path(__file__).read_bytes()),'runtime':{'python':sys.version,'platform':platform.platform()},'operations':{'savedRowsRanked':5000,'selectedRows':4,'selectedCodeBytes':80000,'stateBytesDecoded':0,'newGeometry':0,'newWakeTerms':0,'rootSolves':0,'gpuDispatches':0},'limits':'Selection uses saved maxima, differences, counts and classifications only. No geometric or scientific model calculation.'}
 with (out/'selection.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
 print(json.dumps({'status':'completed','ids':[r['receiverId'] for r in chosen],'selectionSha256':sha((out/'selection.json').read_bytes()),'newGeometry':0,'newWakeTerms':0,'rootSolves':0,'gpuDispatches':0}))
if __name__=='__main__':main()
