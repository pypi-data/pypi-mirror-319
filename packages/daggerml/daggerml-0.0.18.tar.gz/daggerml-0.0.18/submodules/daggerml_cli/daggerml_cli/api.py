import os
from dataclasses import dataclass
from shutil import rmtree

from asciidag.graph import Graph as AsciiGraph
from asciidag.node import Node as AsciiNode

from daggerml_cli.repo import DEFAULT, Ctx, Error, Fn, Index, Literal, Load, Ref, Repo, unroll_datum
from daggerml_cli.util import asserting, makedirs

###############################################################################
# REPO ########################################################################
###############################################################################


def current_repo(config):
    return config.REPO


def repo_path(config):
    return config.REPO_PATH


def list_repo(config):
    if os.path.exists(config.REPO_DIR):
        return sorted(os.listdir(config.REPO_DIR))
    return []


def list_other_repo(config):
    return sorted([k for k in list_repo(config) if k != config.REPO])


def create_repo(config, name):
    config._REPO = name
    with Repo(makedirs(config.REPO_PATH), config.USER, create=True):
        pass


def use_repo(config, name):
    assert name in list_repo(config), f"no such repo: {name}"
    config.REPO = name


def delete_repo(config, name):
    path = os.path.join(config.REPO_DIR, name)
    rmtree(path)


def copy_repo(config, name):
    with Repo(config.REPO_PATH) as db:
        db.copy(os.path.join(config.REPO_DIR, name))


def gc_repo(config):
    with Repo(config.REPO_PATH) as db:
        with db.tx(True):
            return db.gc()


def dump_ref(config, ref):
    with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
        with db.tx():
            return db.dump_ref(ref)


def load_ref(config, ref):
    with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
        with db.tx(True):
            return db.load_ref(ref)


###############################################################################
# PROJECT #####################################################################
###############################################################################


def init_project(config, name, branch=Ref(DEFAULT).name):  # noqa: B008
    if name is not None:
        assert name in list_repo(config), f"repo not found: {name}"
    config.REPO = name
    use_branch(config, branch)


###############################################################################
# BRANCH ######################################################################
###############################################################################


def current_branch(config):
    return config.BRANCH


def list_branch(config):
    if os.path.exists(config.REPO_PATH):
        with Repo(config.REPO_PATH) as db:
            with db.tx():
                return sorted([k.name for k in db.heads() if k.name])
    return []


def list_other_branch(config):
    return [k for k in list_branch(config) if k != config.BRANCH]


def create_branch(config, name):
    with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
        with db.tx(True):
            db.create_branch(Ref(f"head/{name}"), db.head)
    use_branch(config, name)


def delete_branch(config, name):
    with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
        with db.tx(True):
            db.delete_branch(Ref(f"head/{name}"))


def use_branch(config, name):
    assert name in list_branch(config), f"branch not found: {name}"
    config.BRANCH = name


def merge_branch(config, name):
    with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
        with db.tx(True):
            ref = db.merge(db.head().commit, Ref(f"head/{name}")().commit)
            db.checkout(db.set_head(db.head, ref))
        return ref.name


def rebase_branch(config, name):
    with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
        with db.tx(True):
            ref = db.rebase(Ref(f"head/{name}")().commit, db.head().commit)
            db.checkout(db.set_head(db.head, ref))
        return ref.name


###############################################################################
# DAG #########################################################################
###############################################################################

def describe_dag(config, id):
    with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
        with db.tx(False):
            ref = Ref(id)
            dag = ref()
            if dag is None:
                raise Error(f'dag {id} is not in DB!')
            edges = {}
            for node_ref in dag.nodes:
                node = node_ref()
                if isinstance(node.data, Fn):
                    edges[node_ref.to] = [x.to for x in node.data.expr]
                elif isinstance(node.data, Load):
                    edges[node_ref.to] = node.data.dag.to
            return {
                'id': ref.to,
                'expr': dag.expr.to if hasattr(dag, 'expr') else None,
                'nodes': [x.to for x in dag.nodes],
                'result': dag.result.to if dag.result is not None else None,
                'error': None if dag.error is None else str(dag.error),
                'edges': edges,
            }


def list_dags(config, dag_names=()):
    if os.path.exists(config.REPO_PATH):
        with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
            with db.tx():
                result = [{'name': k, 'id': v.to, 'dag': v()} for k, v in Ctx.from_head(db.head).dags.items()]
        if len(dag_names) > 0:
            result = [x for x in result if x['name'] in dag_names]
        return result
    return []


def begin_dag(config, *, name=None, message, dag_dump=None):
    with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
        with db.tx(True):
            dag = None if dag_dump is None else db.load_ref(dag_dump)
            return db.begin(name=name, message=message, dag=dag)


###############################################################################
# NODE ########################################################################
###############################################################################

def describe_node(config, id):
    with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
        with db.tx(False):
            ref = Ref(id)
            dag = ref()
            if dag is None:
                raise Error(f'dag {id} is not in DB!')
            edges = {}
            for node_ref in dag.nodes:
                node = node_ref()
                if isinstance(node.data, Fn):
                    edges[node_ref.to] = [x.to for x in node.data.expr]
                elif isinstance(node.data, Load):
                    edges[node_ref.to] = node.data.dag.to
            return {
                'id': ref.to,
                'expr': dag.expr.to if hasattr(dag, 'expr') else None,
                'nodes': [x.to for x in dag.nodes],
                'result': dag.result.to if dag.result is not None else None,
                'error': None if dag.error is None else str(dag.error),
                'edges': edges,
            }


###############################################################################
# INDEX #######################################################################
###############################################################################

def list_indexes(config):
    if os.path.exists(config.REPO_PATH):
        with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
            with db.tx():
                return [{'id': x.to, 'index': x()} for x in db.indexes()]
    return []


def delete_index(config, index: Ref):
    with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
        with db.tx(True):
            assert isinstance(index(), Index)
            db.delete(index)
    return True


###############################################################################
# API #########################################################################
###############################################################################


def _invoke_method(f):
    _, fname = f.__name__.split('_', 1)
    _invoke_method.fn_map[fname] = f
    return f
_invoke_method.fn_map = {}

@_invoke_method
def invoke_start_fn(db, index, expr, retry=False):
    with db.tx(True):
        fn = db.start_fn(expr=expr, retry=retry)
        dump = fn().dump
        cache_key = fn().fndag.to
        return [fn, cache_key, dump]

@_invoke_method
def invoke_get_fn_result(db, index, waiter_ref):
    with db.tx(True):
        result = db.get_fn_result(index, waiter_ref)
        if isinstance(result, Ref) and result().error is not None:
            return result().error
        return result

@_invoke_method
def invoke_put_literal(db, index, data):
    with db.tx(True):
        from daggerml_cli.repo import Index
        assert isinstance(index(), Index)
        datum = db.put_datum(data)
        return db.put_node(Literal(datum), index=index)

@_invoke_method
def invoke_put_load(db, index, load_dag):
    with db.tx(True):
        return db.put_node(Load(asserting(db.get_dag(load_dag))), index=index)

@_invoke_method
def invoke_commit(db, index, result):
    with db.tx(True):
        return db.commit(res_or_err=result, index=index)

@_invoke_method
def invoke_get_node_value(db, _, node: Ref):
    with db.tx():
        return db.get_node_value(node)

@_invoke_method
def invoke_get_expr(db, index):
    with db.tx():
        return index().dag().expr

@_invoke_method
def invoke_unroll(db, index, node):
    with db.tx():
        return unroll_datum(node().value())


def invoke_api(config, token, data):
    db = None

    def no_such_op(name):
        def inner(*_args, **_kwargs):
            raise ValueError(f"no such op: {name}")
        return inner

    try:
        # db = token if token else Repo(config.REPO_PATH, config.USER, config.BRANCHREF)
        with Repo(config.REPO_PATH, config.USER, config.BRANCHREF) as db:
            op, args, kwargs = data
            return _invoke_method.fn_map.get(op, no_such_op(op))(db, token, *args, **kwargs)
    except Exception as e:
        raise Error.from_ex(e) from e


###############################################################################
# COMMIT ######################################################################
###############################################################################


def list_commit(config):
    if os.path.exists(config.REPO_PATH):
        with Repo(config.REPO_PATH, head=config.BRANCHREF) as db:
            with db.tx():
                return [(x.to, x()) for x in db.objects('commit')]
    return []


def commit_log_graph(config):
    @dataclass
    class GNode:
        commit: Ref
        parents: list[Ref]
        children: list[Ref]

    with Repo(config.REPO_PATH, config.USER, head=config.BRANCHREF) as db:
        with db.tx():
            def walk_names(x, head=None):
                if x and x[0]:
                    k = names[x[0]] if x[0] in names else x[0].name
                    tag1 = " HEAD" if head and head.to == db.head.to else ""
                    tag2 = f" {head.name}" if head else ""
                    names[x[0]] = f"{k}{tag1}{tag2}"
                    [walk_names(p) for p in x[1]]
            def walk_nodes(x):
                if x and x[0]:
                    if x[0] not in nodes:
                        parents = [walk_nodes(y) for y in x[1] if y]
                        nodes[x[0]] = AsciiNode(names[x[0]], parents=parents)
                    return nodes[x[0]]
            names = {}
            nodes = {}
            log = dict(asserting(db.log("head")))
            ks = [db.head, *[k for k in log.keys() if k != db.head]]
            [walk_names(log[k], head=k) for k in ks]
            heads = [walk_nodes(log[k]) for k in ks]
            AsciiGraph().show_nodes(heads)


def revert_commit(config, commit):
    raise NotImplementedError("not implemented")
