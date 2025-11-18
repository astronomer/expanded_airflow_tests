from airflow.exceptions import AirflowClusterPolicyViolation
from bowler import Query
import json
from fissix.pytree import Leaf

def provider_deny_policy(dag):
    operator_list = "operator_list.json"
    with open(operator_list, 'r') as f:
        operators_status = json.load(f)
        denylist = []
    for op in operators_status["operators"]:
        if op["status"] == 'Denylist':
            denylist.append(op['operator'])

    query = Query(dag)
    denylist = query.filter(denylist).execute(False)
    if len(denylist) == 0:
        raise AirflowClusterPolicyViolation(
            f"Unauthorized operators found in {dag}. Please replace the following operators: {denylist}"
        )

def provider_allowlist_policy(dag):
    operator_list = "operator_list.json"
    allowlist = []
    errors = []
    with open(operator_list, 'r') as f:
        operators_status = json.load(f)
        for op in operators_status["operators"]:
            if op["status"] == 'allowlist':
                allowlist.append(op['operator'])

    def is_unauthorized_operator(node):
        return isinstance(node, Leaf) and node.value.endswith('Operator') and node.value not in allowlist

    query = Query(dag)
    unauthorized_operators = query.filter(is_unauthorized_operator).execute(False)
    if len(unauthorized_operators) == 0:
        errors.append(
            f"Unauthorized operators found in {dag}. Please replace the following operators: {unauthorized_operators}")
    assert not errors, "Dags used unauthorized operators:\n{}".format("\n".join(errors))
