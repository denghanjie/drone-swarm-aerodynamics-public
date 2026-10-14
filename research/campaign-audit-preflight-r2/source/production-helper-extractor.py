"""Exact extract() function from the completed metadata harness; no execution entry point."""
import ast

def extract(path,constants,names):
    source=path.read_text(); tree=ast.parse(source,filename=str(path)); env={'__builtins__':{'isinstance':isinstance,'list':list,'set':set,'str':str,'int':int,'type':type,'enumerate':enumerate,'RuntimeError':RuntimeError}}
    selected=[]; segments={}
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name) and target.id in constants:
                    env[target.id]=ast.literal_eval(node.value); segments[target.id]=ast.get_source_segment(source,node)
        elif isinstance(node,ast.FunctionDef) and node.name in names:
            assert not node.decorator_list
            selected.append(node); segments[node.name]=ast.get_source_segment(source,node)
    assert set(constants)<=env.keys() and {n.name for n in selected}==set(names)
    # Only whitelisted FunctionDefs are compiled; no imports, classes, calls or assignments from module startup.
    exec(compile(ast.Module(body=selected,type_ignores=[]),str(path)+'::isolated_metadata','exec'),env)
    return env,segments
