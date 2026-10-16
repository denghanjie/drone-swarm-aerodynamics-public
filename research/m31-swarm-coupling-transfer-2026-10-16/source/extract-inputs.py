"""Copy fixed published synthetic states; no geometry or load scoring."""
import hashlib,json,pathlib,struct,sys,math
p=pathlib.Path(__file__).resolve().parent.parent
base=pathlib.Path(sys.argv[1])
selected=[(1000,20,470998,'8adc8213f6b036f498639bf070af53d3777fe1771c34f41bb54498e48be0f304'),(5000,20,2357471,'64696f6aca0d74a00f8540f53abcb46b4bd8dd6ed387f5192506c84967ab267e'),(5000,60,2351516,'9538f037be4a62abb9a550c7ac2a7aa182556c448136c86d66d1e09492fd050b'),(5000,180,2349503,'1a4ba3d4cf3ffee87f783a2ba7e40865a438b342ff71e3ace16e5341ef208af4')]
cases=[]
for n,t,size,sha in selected:
    src=f'outputs/milestone-31-source/checkpoint-heldout-2001-{n}-wide-wall-priority-0.0025-{t}.json'
    b=(base/src).read_bytes()
    if len(b)!=size or hashlib.sha256(b).hexdigest()!=sha: raise ValueError('original source pin mismatch')
    obj=json.loads(b)
    if obj['t']!=t or len(obj['states'])!=n: raise ValueError('shape/time mismatch')
    vals=[]
    for row in obj['states']:
        if len(row)!=17 or any(type(x) not in (float,int) or not math.isfinite(x) for x in row): raise ValueError('nonfinite or malformed state')
        vals.extend(row)
    raw=struct.pack('<'+'d'*len(vals),*vals)
    if list(struct.unpack('<'+'d'*len(vals),raw))!=vals: raise ValueError('lossless extraction mismatch')
    name=f'n{n}-t{t}'
    target=p/'inputs'/f'{name}.f64'
    with target.open('xb') as f: f.write(raw)
    cases.append(dict(id=name,n=n,t=t,source=src,sourceBytes=size,sourceSha256=sha,path=str(target.relative_to(p)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
index=dict(kind='historical-airflow-off-complete-state-copy',originalPublicBase='c591ce2b195fa01b895d4ba881a44a4b92fdd703',sourceRelease='v0.1.0-public',shape='[vehicle,17]',encoding='float64le',columns=['position_x_m','position_y_m','position_z_m','velocity_x_m_s','velocity_y_m_s','velocity_z_m_s','quaternion_x','quaternion_y','quaternion_z','quaternion_w','body_omega_x_rad_s','body_omega_y_rad_s','body_omega_z_rad_s','motor_lag_thrust_0_N','motor_lag_thrust_1_N','motor_lag_thrust_2_N','motor_lag_thrust_3_N'],rotorBodyOffsets_m=[[.028,.028,0],[-.028,.028,0],[-.028,-.028,0],[.028,-.028,0]],transform='JSON numeric decoding to binary64 without filtering, rescaling, normalization or reordering; decoded binary equality checked',cases=cases)
with (p/'inputs/index.json').open('x') as f: json.dump(index,f,indent=2); f.write('\n')
print(json.dumps({'copied':len(cases),'bytes':sum(x['bytes'] for x in cases),'target_scoring':False}))
