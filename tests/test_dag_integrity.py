import pytest
from airflow.models import DagBag

def test_dag_loading():
    # include_examples=False supaya dia tak check DAG sample Airflow
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    
    # Ini akan tangkap syntax error, missing provider, atau logic error dalam DAG
    assert len(dagbag.import_errors) == 0, f"DAG import errors: {dagbag.import_errors}"