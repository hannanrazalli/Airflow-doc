import os
from datetime import datetime
from pathlib import Path

from cosmos import DbtDag, ProjectConfig, ProfileConfig, RenderConfig
from cosmos.constants import LoadMode
from cosmos.profiles import GoogleCloudServiceAccountDictProfileMapping

# 1. Path dalam Docker Astro (Standard path)
DBT_PROJECT_PATH = Path("/usr/local/airflow/include/dbt/oms_dbt_proj")

# 2. Setup Profile (Ini akan 'overwrite' profiles.yml kau)
profile_config = ProfileConfig(
    profile_name="oms_dbt_proj",
    target_name="dev",
    profile_mapping=GoogleCloudServiceAccountDictProfileMapping(
        conn_id="google_cloud_default", # Nama connection dlm Airflow UI
        profile_args={
            "project": "transactions-practice",
            "dataset": "silver", # Dataset permulaan (default)
            "location": "asia-southeast1",
        },
    ),
)

# 3. Define DAG
dbt_oms_dag = DbtDag(
    project_config=ProjectConfig(DBT_PROJECT_PATH),
    operator_args={
        "install_deps": True,
        "full_refresh": True, # <--- Tambah ni sementara untuk cuci table lama
    },
    profile_config=profile_config,
    render_config=RenderConfig(
        load_method=LoadMode.DBT_LS,
        # select=["path:models/staging/stg_transactions.sql"] # <--- Focus kat file ni je
    ),
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    dag_id="dbt_oms_medallion",
)