"""Restricted AST tests of pure saved-review predicates; no runner is imported.

This file reads source text. Its interpreter rejects attributes/calls outside a
small allowlist. It cannot execute I/O, imports, locks, main(), timers, subprocess
or browser operations from the operational checker. All inputs are inert dicts
and synthetic bytes made in this file. Output paths are local sibling artifacts.
"""
import ast
import copy
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'check-records.py'
BEFORE = HERE / 'check-records.pre-edge-test.py.txt'
source_bytes = SOURCE.read_bytes()
source_text = source_bytes.decode()
tree = ast.parse(source_text, filename=SOURCE.name)
before_bytes = BEFORE.read_bytes()
before_text = before_bytes.decode()
before_tree = ast.parse(before_text, filename=BEFORE.name)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def predicate(parsed, label):
    matches = [n.args[0] for n in ast.walk(parsed) if isinstance(n, ast.Call)
               and isinstance(n.func, ast.Name) and n.func.id == 'require'
               and len(n.args) == 2 and isinstance(n.args[1], ast.Constant)
               and n.args[1].value == label]
    if len(matches) != 1:
        raise ValueError('predicate must occur exactly once: ' + label)
    return matches[0]

main_node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')

def assignments(name):
    return [n.value for n in main_node.body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]

helpers = {n.name:n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'digest','number'}}
if set(helpers) != {'digest','number'} or any(len(n.body) != 1 or not isinstance(n.body[0], ast.Return) for n in helpers.values()):
    raise ValueError('unexpected pure helper structure')

def evaluate(node, env):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]
        if node.id == 'int':
            return int
        if node.id == 'float':
            return float
        raise ValueError('unbound inert name: ' + node.id)
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        values = [evaluate(x, env) for x in node.elts]
        return values if isinstance(node, ast.List) else tuple(values) if isinstance(node, ast.Tuple) else set(values)
    if isinstance(node, ast.Dict):
        return {evaluate(k,env):evaluate(v,env) for k,v in zip(node.keys,node.values)}
    if isinstance(node, ast.Subscript):
        return evaluate(node.value,env)[evaluate(node.slice,env)]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not evaluate(node.operand,env)
    if isinstance(node, ast.BoolOp):
        value = evaluate(node.values[0],env)
        for child in node.values[1:]:
            if isinstance(node.op, ast.And) and not value or isinstance(node.op, ast.Or) and value:
                return value
            value = evaluate(child,env)
        return value
    if isinstance(node, ast.IfExp):
        return evaluate(node.body if evaluate(node.test,env) else node.orelse,env)
    if isinstance(node, ast.Compare):
        left = evaluate(node.left,env)
        for op,child in zip(node.ops,node.comparators):
            right = evaluate(child,env)
            if isinstance(op, ast.Eq): okay = left == right
            elif isinstance(op, ast.NotEq): okay = left != right
            elif isinstance(op, ast.Is): okay = left is right
            elif isinstance(op, ast.IsNot): okay = left is not right
            elif isinstance(op, ast.Lt): okay = left < right
            elif isinstance(op, ast.LtE): okay = left <= right
            elif isinstance(op, ast.Gt): okay = left > right
            elif isinstance(op, ast.GtE): okay = left >= right
            elif isinstance(op, ast.In): okay = left in right
            elif isinstance(op, ast.NotIn): okay = left not in right
            else: raise ValueError('comparison outside allowlist')
            if not okay:
                return False
            left = right
        return True
    if isinstance(node, (ast.GeneratorExp, ast.ListComp)):
        if len(node.generators) != 1:
            raise ValueError('only one bounded generator allowed')
        gen = node.generators[0]
        if not isinstance(gen.target, ast.Name) or gen.is_async:
            raise ValueError('unsupported generator')
        values = list(evaluate(gen.iter,env))
        if len(values) > 64:
            raise ValueError('inert generator cap')
        result = []
        for value in values:
            local = dict(env, **{gen.target.id:value})
            if all(evaluate(test,local) for test in gen.ifs):
                result.append(evaluate(node.elt,local))
        return result
    if isinstance(node, ast.Call):
        if node.keywords:
            raise ValueError('keyword calls not allowed')
        args = [evaluate(arg,env) for arg in node.args]
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name in helpers:
                function = helpers[name]
                keys = [arg.arg for arg in function.args.args]
                if len(keys) != len(args):
                    raise ValueError('helper arity')
                return evaluate(function.body[0].value,dict(zip(keys,args)))
            if name == 'all': return all(*args)
            if name == 'len': return len(*args)
            if name == 'type': return type(*args)
            if name == 'by_kind':
                return [event for event in env['events'] if event['kind'] == args[0]]
            raise ValueError('call outside allowlist: ' + name)
        if isinstance(node.func, ast.Attribute):
            owner = node.func.value
            if isinstance(owner, ast.Name) and owner.id == 'math' and node.func.attr == 'isfinite':
                return math.isfinite(*args)
            if node.func.attr == 'hexdigest' and not args and isinstance(owner, ast.Call) \
                    and isinstance(owner.func, ast.Attribute) and owner.func.attr == 'sha256' \
                    and isinstance(owner.func.value, ast.Name) and owner.func.value.id == 'hashlib' \
                    and len(owner.args) == 1 and not owner.keywords:
                return sha(evaluate(owner.args[0],env))
            if node.func.attr in {'keys','values'} and not args:
                value = evaluate(owner,env)
                if type(value) is not dict:
                    raise ValueError('dict method on non-dict')
                return value.keys() if node.func.attr == 'keys' else value.values()
        raise ValueError('attribute call outside allowlist')
    raise ValueError('AST node outside allowlist: ' + type(node).__name__)

labels = ['worker-envelope','instrumentation-conjunction','one-post-and-bounded-written-bytes',
          'independent-persisted-byte-read','complete-sink-persistence','sink-persistence-event-projection',
          'independent-limited-transport-classification','incomplete-diagnostic-outside-review-pass-scope',
          'complete-required-new-evidence-pins','actual-completed-capture-within-allowance']
expressions = {label:predicate(tree,label) for label in labels}
for name in ['healthy','complete','status','needed']:
    nodes = assignments(name)
    if len(nodes) != (2 if name == 'healthy' else 1):
        raise ValueError('unexpected assignment extraction: ' + name)
    for index,node in enumerate(nodes,1):
        expressions['assignment:'+name+':'+str(index)] = node
for name,node in helpers.items():
    expressions['helper:'+name] = node.body[0].value

results = []
def test(name, expression, env, expected, description):
    actual = evaluate(expression,env)
    passed = type(actual) is type(expected) and actual == expected
    results.append({'case':name,'description':description,'expected':expected,'actual':actual,'passed':passed})

source_id, freeze_id = '1'*40, '2'*64
worker = {'version':1,'kind':'synthetic-transport-diagnostic','terminal':True,
          'sourceCommit':source_id,'sourceFreezeSHA256':freeze_id,'browserVersion':'wrapper-extra'}
test('wrapper-extra-field-is-allowed',expressions['worker-envelope'],
     {'worker':worker,'source':source_id,'freeze_sha':freeze_id},True,
     'A producer metadata wrapper may contain additional fields; the predicate compares its defined projection.')
bad_worker = dict(worker,sourceFreezeSHA256='3'*64)
test('wrapper-shared-field-mismatch-rejected',expressions['worker-envelope'],
     {'worker':bad_worker,'source':source_id,'freeze_sha':freeze_id},False,
     'Wrapper tolerance does not waive disagreement in a required shared field.')

ready = {k:True for k in ['server','playwright','cdpNetwork','cdpAudits','browserBinding','routes']}
inst = {'ready':ready,'eventCount':1,'attemptedEvents':1,'droppedEvents':0,'truncatedEvents':0,
        'observerExceptions':0,'callbackErrors':0,'unexpectedRedirectObservations':0,'complete':True,
        'eventCap':2048,'clock':'worker-monotonic-receipt','browserClock':'browser-performance-independent',
        'crossClockOrderingClaimed':False,'captureClosedAfterCleanup':True}

def observation(exact, acknowledged, started, instrumentation=None):
    local = {'inst':copy.deepcopy(instrumentation or inst),'worker':{'errors':[],'cleanupErrors':[],'protocolDeviations':[]},
             'browser':{'acknowledged':acknowledged},'ack':acknowledged,
             'persistence':{'exact':exact},'sink':{'started':started,'closed':True,'activeWrites':0}}
    local['healthy'] = evaluate(expressions['assignment:healthy:1'],local)
    local['healthy'] = evaluate(expressions['assignment:healthy:2'],local)
    local['complete'] = evaluate(expressions['assignment:complete:1'],local)
    local['status'] = evaluate(expressions['assignment:status:1'],local)
    local['worker']['status'] = local['status']
    return local

local = observation(True,False,True)
test('exact-persistence-failed-ack-status',expressions['assignment:status:1'],local,
     'exact-persistence-acknowledgement-failed','Exact persisted bytes and a failed acknowledgement are distinct observations.')
test('exact-persistence-failed-ack-in-scope',expressions['incomplete-diagnostic-outside-review-pass-scope'],local,True,
     'A complete observation can be reviewed even when acknowledgement failed.')
local = observation(False,False,False)
test('complete-failed-fetch-status',expressions['assignment:status:1'],local,
     'transfer-failed-before-sink-acceptance','A fully observed failed fetch is not automatically incomplete instrumentation.')
test('complete-failed-fetch-in-scope',expressions['incomplete-diagnostic-outside-review-pass-scope'],local,True,
     'Complete failed transport can satisfy the review observation scope without transport success.')

incomplete_inst = dict(inst,attemptedEvents=2,droppedEvents=1,complete=False)
local = observation(False,False,False,incomplete_inst)
test('honest-incomplete-trace-conjunction',expressions['instrumentation-conjunction'],local,True,
     'An honestly false instrumentation-complete flag remains internally consistent.')
test('incomplete-trace-status',expressions['assignment:status:1'],local,'incomplete',
     'Missing trace evidence dominates a narrower failed-fetch classification.')
test('incomplete-trace-outside-pass-scope',expressions['incomplete-diagnostic-outside-review-pass-scope'],local,False,
     'Rejection means the complete-observation scope was not met, not proof of corruption.')
lying = copy.deepcopy(local);lying['inst']['complete']=True
test('incomplete-trace-cannot-claim-complete',expressions['instrumentation-conjunction'],lying,False,
     'The saved completeness flag cannot contradict a dropped-event observation.')
test('extra-post-rejected',expressions['one-post-and-bounded-written-bytes'],
     {'sink':{'postCount':2,'writtenBytes':3840,'receivedBytes':3840}},False,
     'Two actual sink POST entries exceed the adopted single application request.')

fixture = bytes((73*i+19)%256 for i in range(3840))
changed = bytes([fixture[0]^1])+fixture[1:]
expected_sha = sha(fixture)
original_meta = {'exists':True,'bytes':3840,'sha256':expected_sha,'exact':True}
bad_env = {'received':changed,'fixture':fixture,'sink':{'writtenBytes':3840},'persistence':original_meta}
test('post-record-payload-corruption-rejected',expressions['independent-persisted-byte-read'],bad_env,False,
     'A changed persisted file does not match its original saved hash/exactness report.')
actual_meta = {'exists':True,'bytes':3840,'sha256':sha(changed),'exact':False}
true_env = dict(bad_env,persistence=actual_meta)
test('honestly-recorded-wrong-content-byte-read',expressions['independent-persisted-byte-read'],true_env,True,
     'Accurate observation of nonmatching content is distinguishable from post-record corruption.')
sink_receipt = {'complete':True,'bytes':3840,'sha256':sha(changed)}
wrong_content = {'sink':{'started':True,'status':200,'receipt':sink_receipt},'persistence':actual_meta,
                 'EXPECTED_SHA':expected_sha,'events':[{'kind':'sink-persisted','data':sink_receipt}]}
test('baseline-defect-byte-count-not-fixture-equality',predicate(before_tree,'complete-sink-persistence'),wrong_content,False,
     'Preserved pre-freeze predicate incorrectly rejected coherently recorded byte-count completion with wrong content.')
test('corrected-byte-count-not-fixture-equality',expressions['complete-sink-persistence'],wrong_content,True,
     'Corrected predicate binds completed byte count and receipt to actual persisted bytes; fixture equality stays separate.')
test('corrected-persistence-event-projection',expressions['sink-persistence-event-projection'],
     {'sink':wrong_content['sink'],'persisted_event':sink_receipt},True,
     'The sink event must match the actual receipt shared fields.')

needed = evaluate(expressions['assignment:needed:1'],{})
missing = {name:{} for name in needed if name != 'results/result.json'}
test('absent-result-manifest-rejected',expressions['complete-required-new-evidence-pins'],
     {'needed':needed,'pins':missing},False,
     'A manifest made from present files cannot meet required evidence without the result; no operational file I/O is simulated.')
execution = {'toolSessionCompleted':True,'actualCaptureExitCode':1,'actualFullElapsedSeconds':1.0}
test('nonzero-external-exit-rejected',expressions['actual-completed-capture-within-allowance'],
     {'execution':execution},False,'A retained summary cannot replace actual completed capture exit 0.')
test('zero-completed-external-exit-in-scope',expressions['actual-completed-capture-within-allowance'],
     {'execution':dict(execution,actualCaptureExitCode=0)},True,'Positive control for the exact externally completed exit predicate.')
test('yield-is-not-external-completion',expressions['actual-completed-capture-within-allowance'],
     {'execution':dict(execution,actualCaptureExitCode=0,toolSessionCompleted=False)},False,
     'A yielded session cannot satisfy actual tool completion.')

extractions = []
for label,node in expressions.items():
    text = ast.get_source_segment(source_text,node)
    extractions.append({'label':label,'source':'check-records.py','line':node.lineno,
                        'expression':text,'expressionSHA256':sha(text.encode()),
                        'ast':ast.dump(node,include_attributes=False)})
old = predicate(before_tree,'complete-sink-persistence')
old_text = ast.get_source_segment(before_text,old)
extractions.append({'label':'baseline:complete-sink-persistence','source':BEFORE.name,'line':old.lineno,
                    'expression':old_text,'expressionSHA256':sha(old_text.encode()),
                    'ast':ast.dump(old,include_attributes=False)})
source_pins = [{'path':SOURCE.name,'bytes':len(source_bytes),'sha256':sha(source_bytes)},
               {'path':BEFORE.name,'bytes':len(before_bytes),'sha256':sha(before_bytes)}]
extraction_record = {'kind':'inert-pure-predicate-extractions','sourcePins':source_pins,
                     'operationalSourceImported':False,'operationalCheckerInvoked':False,
                     'extractions':extractions}
for name,value in [('INERT-PREDICATES.json',extraction_record),
                   ('INERT-TEST-RESULTS.json',{'kind':'inert-schema-edge-test-results','sourcePins':source_pins,
                      'interpreterSource':{'path':Path(__file__).name,'bytes':Path(__file__).stat().st_size,
                                           'sha256':sha(Path(__file__).read_bytes())},
                      'operationalSourceImported':False,'operationalCheckerInvoked':False,
                      'browserOrExperimentInvoked':False,'passed':all(x['passed'] for x in results),
                      'testCount':len(results),'tests':results,
                      'fixture':{'bytes':3840,'sha256':expected_sha,'construction':'byte[i]=(73*i+19)%256',
                                 'changedFixture':'first byte xor 1','changedSHA256':sha(changed)}})]:
    with (HERE/name).open('x') as handle:
        handle.write(json.dumps(value,indent=2)+'\n')
print(json.dumps({'testCount':len(results),'passed':all(x['passed'] for x in results),
                  'operationalCheckerInvoked':False,'sourceSHA256':sha(source_bytes)}))
raise SystemExit(0 if all(x['passed'] for x in results) else 1)
