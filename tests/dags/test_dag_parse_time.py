import datetime
from airflow.models import DagBag

def test_dag_load_times():
    dagbag = DagBag()
    for dag_id, dag in dagbag.dags.items():
        start_time = datetime.datetime.now()
        dagbag.process_file(dag.fileloc)
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        assert duration < datetime.timedelta(seconds=5), f"DAG {dag_id} took {duration} seconds to load"