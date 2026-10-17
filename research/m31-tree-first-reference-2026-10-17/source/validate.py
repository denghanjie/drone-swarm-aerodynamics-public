"""Independent small-corpus comparison; never imports the new dispatcher.

Group membership expansion is confined to this validation path. The candidate
itself must keep proved-zero groups as compact permutation ranges.
"""
from collections import Counter

class ValidationError(Exception):
    pass

def need(value, code):
    if not value:
        raise ValidationError(code)

def validate(full, candidate, semantic, constants):
    fields = ('id','input','prepared','planned','globalInvalid','globalGuard',
              'order','status','branch','witness','referenceClass')
    for key in fields:
        need(semantic.same_json(candidate[key], full[key]), key+'-equality')
    need(candidate.get('roots',{}) == full.get('roots',{}), 'exact-root-boxes')
    need(candidate.get('loads',{}) == full.get('loads',{}), 'exact-signed-load-boxes')
    need(candidate.get('guardEvidence') == full.get('guardEvidence'), 'guard-evidence-equality')
    need(semantic.same_json(candidate['tree'], full['tree']), 'tree-identity')
    ids = [d['id'] for d in full['input']['drones']]
    n = len(ids)
    inverse_id = {v:i for i,v in enumerate(ids)}
    plan = full['plans']['hierarchy']
    coverage = candidate['coverage']
    need(coverage['schema']=='m31-tree-first-coverage-v1' and coverage['complete'] is True, 'coverage-schema-completion')
    need(coverage['mode'] == plan['mode'], 'mode-guard')
    permutation = ([] if full['globalInvalid'] else full['tree']['permutation'] if full['tree'] is not None else ids)
    need(coverage['permutation'] == permutation, 'permutation-identity')
    if not full['globalInvalid']:
        need(sorted(permutation) == sorted(ids) and len(set(permutation)) == n, 'permutation-bijection')
    positions = {v:p for p,v in enumerate(permutation)}
    queries = coverage['queries']
    need(len(queries) == len(plan['queries']), 'query-count')
    scalar_keys, zero_keys, rules = set(), set(), Counter()
    zero_nodes = leaf_nodes = 0
    for query, expected in zip(queries, plan['queries']):
        ii,r = expected['i'], expected['r']
        need(type(query['i']) is int and query['i']==ii and type(query['id']) is int and query['id']==ids[ii]
             and type(query['r']) is int and query['r']==r, 'query-index-id-rotor')
        need(type(query['selfPosition']) is int and query['selfPosition']==positions[ids[ii]], 'self-position')
        terminals = query['terminals']
        need(len(terminals)==len(expected['terminals']), 'terminal-count')
        cursor = 0
        covered = []
        for term, old in zip(terminals,expected['terminals']):
            kind = term['kind']
            need(kind in ('zero','leaf','scan'), 'terminal-kind')
            start,end = term['start'],term['end']
            need(type(start) is int and type(end) is int and start==cursor and start<end<=n, 'range-partition')
            cursor=end
            members = sorted(inverse_id[permutation[p]] for p in range(start,end) if permutation[p]!=ids[ii])
            need(members==sorted(old['members']), 'range-membership')
            need(type(term['count']) is int and term['count']==len(members), 'self-adjusted-count')
            covered.extend(members)
            if kind in ('zero','leaf'):
                need(term['node']==old['node'] and type(term['node']) is int, 'canonical-node')
                node = full['tree']['nodes'][term['node']]
                need(start==node['start'] and end==node['end'], 'node-range')
            else:
                need(kind=='scan' and term['node'] is None and start==0 and end==n, 'fallback-scan')
            if kind=='zero':
                need(full['globalGuard']['passed'] is True, 'zero-without-guard')
                proof,_ = semantic.zero_rule(full['boxes'][term['node']], full['geometry'][ii], r, constants)
                need(term['proofRule']==proof and proof is not None, 'node-proof-rule')
                need('sourceIndices' not in term, 'zero-range-expanded')
                for jj in members:
                    need(full['lookup'][(ii,r,jj)]['oracle']['status']=='zero', 'omitted-nonzero-oracle')
                    need((ii,r,jj) not in zero_keys, 'duplicate-zero-membership')
                    zero_keys.add((ii,r,jj))
                rules[proof]+=1
                zero_nodes+=1
            else:
                if kind=='leaf':
                    need(node['left'] is None and node['right'] is None, 'nonleaf-scalar')
                    leaf_nodes+=1
                need(term['sourceIndices']==members and all(type(x) is int for x in term['sourceIndices']), 'scalar-member-list')
                for jj in members:
                    need((ii,r,jj) not in scalar_keys, 'duplicate-scalar-membership')
                    scalar_keys.add((ii,r,jj))
            need(kind==old['kind'], 'canonical-terminal-kind')
            if kind=='zero':
                need(term['proofRule']==old['rule'], 'canonical-proof-rule')
        need(cursor==n and sorted(covered)==[j for j in range(n) if j!=ii], 'complete-query-partition')
    expected_pairs = 0 if full['globalInvalid'] else full['planned']
    need(type(coverage['logicalPairs']) is int and coverage['logicalPairs']==full['planned']
         and type(coverage['requiredCoveredPairs']) is int and coverage['requiredCoveredPairs']==expected_pairs
         and type(coverage['coveredPairs']) is int and coverage['coveredPairs']==expected_pairs, 'coverage-accounting-fields')
    need(not scalar_keys.intersection(zero_keys) and len(scalar_keys)+len(zero_keys)==expected_pairs, 'complete-scene-partition')
    pairs = candidate['pairs']
    keys=[(p['ii'],p['r'],p['jj']) for p in pairs]
    need(keys==sorted(scalar_keys) and len(keys)==len(set(keys)), 'scalar-pair-canonical-membership')
    for pair,key in zip(pairs,keys):
        old=full['lookup'][key]
        for field in ('ii','jj','i','j','r','oracle'):
            need(semantic.same_json(pair[field],old[field]), 'scalar-'+field)
        need(pair.get('coefficient')==old.get('coefficient'), 'exact-positive-coefficient')
    positive=lambda target:[(p['ii'],p['r'],p['jj'],p['coefficient']) for p in target['pairs'] if p['oracle']['status']=='positive']
    need(positive(candidate)==positive(full), 'complete-positive-support')
    work=coverage['work']
    expected_work={'zeroPairs':len(zero_keys),'scalarPairs':len(scalar_keys),
                   'zeroNodes':zero_nodes,'leafVisits':leaf_nodes,
                   'positiveTerms':sum(p['oracle']['status']=='positive' for p in pairs),
                   'scalarZeroPairs':sum(p['oracle']['status']=='zero' for p in pairs),
                   'rejectedPairs':sum(p['oracle']['status']=='rejected' for p in pairs),
                   'unresolvedPairs':sum(p['oracle']['status']=='reference-undecidable' for p in pairs)}
    for key,value in expected_work.items():
        need(type(work[key]) is int and work[key]==value, 'work-'+key)
    # Traversal/preparation counters are compared to the old exact hierarchy plan.
    for key in ('preparationCalls','globalProofs','treeNodes','nodeVisits','nodeRuleTests'):
        need(type(work[key]) is int and work[key]==plan['work'][key], 'work-'+key)
    return {'passed':True,'logicalPairs':full['planned'],'coveredPairs':expected_pairs,
            'fullOraclePairs':len(full['pairs']),'scalarPairs':len(scalar_keys),'provedZeroPairs':len(zero_keys),
            'positivePairs':len(positive(full)), 'zeroProofNodes':zero_nodes,
            'zeroProofRules':dict(rules),'queries':len(queries),
            'exactPositiveCoefficients':True,'exactRoots':True,'exactSignedLoads':True,
            'canonicalDecision':{'status':full['status'],'branch':full['branch'],'witness':full['witness']}}
