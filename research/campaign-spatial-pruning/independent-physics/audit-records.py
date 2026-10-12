import gzip,json,math,re,hashlib,collections,pathlib,sys
root=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent.parent/'implementation'
summary=json.loads((root/'results/accuracy-summary.json').read_text())
seen=collections.Counter(); sample_count=sample_receivers=rows=0;mx_f=mx_m=0.; raw=root/'results/accuracy-raw.jsonl.gz'
for line in gzip.open(raw,'rb'):
    head=line[:250].decode('ascii')
    config=json.loads(head[head.index('{"seed"'):head.index('},"epsilon"')+1])
    ep=float(re.search(r'"epsilon":([0-9.]+)',head).group(1))
    key=(config['seed'],config['count'],config['family'],ep)
    seen[key]+=1;rows+=1
    if config['t'] not in [0,.5,1]:continue
    d=json.loads(line);assert 'failure' not in d;assert len(d['rows'])==config['count'];sample_count+=1
    for r in d['rows']:
        sample_receivers+=1
        assert len(r['fullWind'])==len(r['candidateWind'])==4
        assert 0<=r['omittedBound']<=ep+1e-12
        for a,b,e in zip(r['fullWind'],r['candidateWind'],r['inflowError']):
            assert abs((a-b)-e)<=1e-12
            assert -1e-12<=e<=r['omittedBound']+1e-12
        ef=math.dist(r['fullLoads']['force'],r['candidateLoads']['force']);em=math.dist(r['fullLoads']['moment'],r['candidateLoads']['moment'])
        assert abs(ef-r['forceError'])<=1e-12 and abs(em-r['momentError'])<=1e-13
        assert ef<=r['bounds']['force']+1e-12 and em<=r['bounds']['moment']+1e-13
        assert ef<=.005*.027*9.81 and em<=.0075*.027*9.81*.028
        mx_f=max(mx_f,ef);mx_m=max(mx_m,em)
assert len(seen)==4*4*3*3 and set(seen.values())=={101}
assert rows==summary['totals']['snapshots']*3==14544
receiver_count=sum(key[1]*count for key,count in seen.items());assert receiver_count==summary['totals']['receiverComparisons']==1330776
index=json.loads((root/'results/boids/index.json').read_text());boids=[]
for desc in index['records']:
    p=root/'results/boids'/desc['file'];d=json.loads(p.read_text());assert d['config']==desc['config'] and d['metrics']==desc['metrics']
    assert d['frames'][0]['states']==d['initial'];assert d['frames'][-1]['states']==d['final'];assert d['frames'][-1]['t']==d['metrics']['end']==1
    assert len(d['frames'])==51 and d['metrics']['stop'] is None
    for i,f in enumerate(d['frames']):
        assert len(f['states'])==16 and len(f['winds'])==16 and len(f['omittedBounds'])==16
        assert f['heldFieldTime']<=f['t']+1e-12
        assert all(len(s)==17 and all(math.isfinite(x) for x in s) for s in f['states'])
        if i:assert f['t']>d['frames'][i-1]['t']
    boids.append({'id':desc['id'],'frames':len(d['frames']),'seed':d['config']['seed'],'end':d['metrics']['end'],'omissions':d['metrics']['omissions'],'sourceHash':d['sourceHash'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
out={'status':'passed','rawRecords':rows,'configurationGroups':len(seen),'recordsPerGroup':101,'receiverComparisonsRecounted':receiver_count,'sampledFullRecords':sample_count,'sampledReceiverRows':sample_receivers,'sampleTimes':[0,.5,1],'sampleForceMaxN':mx_f,'sampleMomentMaxNm':mx_m,'pooledSeeds':{'development':[3301,3302],'heldout':[3391,3392]},'boids':boids,'scope':'Read-only raw record/count audit and stratified numerical self-consistency sampling; not a new physical or timing experiment.'}
(pathlib.Path(__file__).parent/'record-audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='boids'},indent=2))
