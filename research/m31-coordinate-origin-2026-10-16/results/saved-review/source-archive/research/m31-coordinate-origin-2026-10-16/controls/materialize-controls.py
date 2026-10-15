"""Pack explicit u32 literals only; no float conversion or scientific evaluation."""
import argparse, copy, hashlib, json, struct
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--baseline-controls',type=Path,required=True);args=p.parse_args()
raw=args.baseline_controls.read_bytes()
if hashlib.sha256(raw).hexdigest()!='55035545e61ca16d0c112b45e278ae94e4cb31fb7940bc8dd567cd9f95796219':
 raise SystemExit('Baseline literal controls hash mismatch')
legacy=json.loads(raw);rows=[];UNSET=0xffffffff
for original in legacy['controls']:
 row={'id':original['id'],'name':original['name'],'kind':original['kind'],'words':original['words']+[0]*8,'expectedByArm':{}}
 for arm in ['A','B','C']:
  expected=copy.deepcopy(original['expected']);expected['expectedNumericWords']={}
  if row['id']==12:
   expected['validityMask']=258055
   expected['expectedNumericWords']={'22':0x3d800000,'25':0x3d800000}
  if row['id']==15:
   expected['validityMask']=30721
   expected['expectedNumericWords']={'20':0x40800000}
  row['expectedByArm'][arm]=expected
 rows.append(row)
def extension(index,name,original_id,mutations):
 row=copy.deepcopy(rows[original_id]);row['id']=index;row['name']=name;row['words'][0]=index
 for slot,word in mutations:row['words'][slot]=word
 for arm in ['A','B','C']:
  row['expectedByArm'][arm]={'ordinal':index,'receiverID':0,'sourceID':1,'rotor':0,'status':1,'policyCode':UNSET,'validityMask':0,'routingFlags':48,'termAssertion':'zero-placeholder-not-valid','expectedNumericWords':{}}
 return row
rows.append(extension(16,'raw-low-nan-before-float-reinterpretation',12,[(32,0x7fc00000)]))
rows.append(extension(17,'nonzero-residual-padding-rejected',12,[(35,1)]))
rows.append(extension(18,'finite-residual-out-of-bound-rejected',12,[(32,0x3c23d70a)]))
last=extension(19,'nonzero-residual-C-outside-AB-reserved-low-rejection',15,[(32,0x35800000)])
last['expectedByArm']['C']={'ordinal':19,'receiverID':0,'sourceID':1,'rotor':0,'status':3,'policyCode':0,'validityMask':30721,'routingFlags':50,'termAssertion':'zero-valid','expectedNumericWords':{'20':0x40800002}}
rows.append(last)
payload=b''.join(struct.pack('<40I',*row['words']) for row in rows)
record={'status':'STATIC_U32_LITERAL_ENCODING_ONLY','recordCount':20,'inputStrideBytes':160,'outputStrideBytes':104,'inputSha256':hashlib.sha256(payload).hexdigest(),'original16InputWordsPreserved':True,'extension':'Append8raw residual words to each original32word control; add4low-field controls. A/B require all residual input words rawzero. C interprets bounded residuals.','expectedNumericWordsConvention':'Keys are absolute output record word indices8..25. Only nonzero exact dyadic vector components are asserted as rawwords; reached zero values allow signedzero. Unreached numeric words must be raw+0.','numericalExpectation':'Exact metadata/status/code/mask/flags, validzero/invalidplaceholder/positive sign, and listed direct vectorword literals only. No norm/profile magnitude oracle. No geometry/profile/reference was evaluated while preparing or encoding these inputs.','controls':rows}
root=Path(__file__).resolve().parent
(root/'controls.u32').write_bytes(payload);(root/'controls.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'records':len(rows),'bytes':len(payload),'sha256':record['inputSha256'],'activity':'u32-only literal encoding; no float conversion or scientific evaluation'}))
