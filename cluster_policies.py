from airflow.exceptions import AirflowClusterPolicyViolation
from bowler import Query
import json
from fissix.pytree import Leaf

def provider_blacklist_policy(dag):
    operator_list = "operator_list.json"
    with open(operator_list, 'r') as f:
        operators_status = json.load(f)
        blacklist = []
    for op in operators_status["operators"]:
        if op["status"] == 'Blacklist':
            blacklist.append(op['operator'])

    query = Query(dag)
    blacklist = query.filter(blacklist).execute(False)
    if len(blacklist) == 0:
        raise AirflowClusterPolicyViolation(
            f"Unauthorized operators found in {dag}. Please replace the following operators: {blacklist}"
        )

def provider_whitelist_policy(dag):
    operator_list = "operator_list.json"
    whitelist = []
    errors = []
    with open(operator_list, 'r') as f:
        operators_status = json.load(f)
        for op in operators_status["operators"]:
            if op["status"] == 'Whitelist':
                whitelist.append(op['operator'])

    def is_unauthorized_operator(node):
        return isinstance(node, Leaf) and node.value.endswith('Operator') and node.value not in whitelist

    query = Query(dag)
    unauthorized_operators = query.filter(is_unauthorized_operator).execute(False)
    if len(unauthorized_operators) == 0:
        errors.append(
            f"Unauthorized operators found in {dag}. Please replace the following operators: {unauthorized_operators}")
    assert not errors, "Dags used unauthorized operators:\n{}".format("\n".join(errors))