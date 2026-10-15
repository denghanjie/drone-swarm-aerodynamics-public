#!/usr/bin/env python3
"""Build the exact fixed-state velocity display from saved diagnostic records."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--evidence-root',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[1];source=root/'results/order-probe.json';data=json.loads(source.read_text());cases=[]
for c in data['cases']:
    cp=a.evidence_root/f"outputs/milestone-31-source/checkpoint-heldout-{c['seed']}-1000-{c['course']}-wall-priority-0.0025-20.json"
    states=json.loads(cp.read_text())['states']
    assert all(row['position']==states[row['i']][:3] for row in c['rows'])
    rows=[{'i':x['i'],'pose':states[x['i']][:3]+states[x['i']][6:10],'neighbors':x['neighborIDs'],'natural':x['natural']['velocity'],'pairs':x['reversePairs']['velocity'],'social':x['reverseSocial']['velocity'],'difference':x['pairDifference']} for x in c['rows']]
    geometry=json.loads((a.evidence_root/f"outputs/milestone-31-source/factory-{c['course']}.json").read_text())
    cases.append({'course':c['course'],'seed':c['seed'],'summary':c['pairSummary'],'socialSummary':c['socialSummary'],'rows':rows,'geometry':geometry})
(root/'viewer/data.json').write_text(json.dumps({'source':'../results/order-probe.json','sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'time':20,'cases':cases},separators=(',',':'))+'\n')
