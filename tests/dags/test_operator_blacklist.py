import json
from airflow.models import DagBag
from bowler import Query
from fissix.pytree import Leaf

def operator_blacklist():
    operator_list = "operator_list.json"
    dagbag = DagBag()
    blacklist = []

    with open(operator_list, 'r') as f:
        operators_status = json.load(f)

        for op in operators_status["operators"]:
            if op["status"] == 'Blacklist':
                blacklist.append(op['operator'])

    for dag_id, dag in dagbag.dags.items():
        errors = []
        query = Query(dag)
        blacklist = query.filter(blacklist).execute(False)
        if len(blacklist) == 0:
            errors.append(f"Unauthorized operators found in {dag_id}. Please replace the following operators: {blacklist}")
    assert not errors,  "Dags used unauthorized operators:\n{}".format("\n".join(errors))

def operator_whitelist():
    operator_list = "operator_list.json"
    dagbag = DagBag()
    whitelist = []

    with open(operator_list, 'r') as f:
        operators_status = json.load(f)
        for op in operators_status["operators"]:
            if op["status"] == 'Whitelist':
                whitelist.append(op['operator'])

        def is_unauthorized_operator(node):
            return isinstance(node, Leaf) and node.value.endswith('Operator') and node.value not in whitelist

    for dag_id, dag in dagbag.dags.items():
        errors = []
        query = Query(dag)
        unauthorized_operators = query.filter(is_unauthorized_operator).execute(False)
        if len(unauthorized_operators) == 0:
            errors.append(f"Unauthorized operators found in {dag_id}. Please replace the following operators: {unauthorized_operators}")
        assert not errors,  "Dags used unauthorized operators:\n{}".format("\n".join(errors))