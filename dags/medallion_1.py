import os
from datetime import datetime
from pathlib import Path
from cosmos import DbtDag, ProjectConfig, ProfileConfig, RenderConfig
from cosmos.constants import LoadMode
from cosmos.profiles import GoogleCloudServiceAccountDictProfileMapping

# --- CARI PATH SECARA DINAMIK ---
# Path fail ini: repo/dags/medallion_1.py
# .parent adalah folder 'dags'
# .parent.parent adalah root repository
# CURRENT_FILE = Path(__file__).resolve()
# REPO_ROOT = CURRENT_FILE.parent.parent
DBT_PROJECT_PATH = Path(os.getenv("AIRFLOW_HOME", "/usr/local/airflow")) / "include" / "dbt" / "oms_dbt_proj"

GCP_PROJECT = os.getenv("GCP_PROJECT_ID", "transactions-practice")
GCP_DATASET = os.getenv("GCP_DATASET_BRONZE", "bronze")
GCP_LOCATION = os.getenv("GCP_LOCATION", "asia-southeast1")

profile_config = ProfileConfig(
    profile_name="oms_dbt_proj",
    target_name="dev",
    profile_mapping=GoogleCloudServiceAccountDictProfileMapping(
        conn_id="google_cloud_default",
        profile_args={
            "project": GCP_PROJECT,
            "dataset": GCP_DATASET,
            "location": GCP_LOCATION,
        },
    ),
)

dbt_oms_dag = DbtDag(
    project_config=ProjectConfig(
        project_name="oms_dbt_proj",
        dbt_project_path=DBT_PROJECT_PATH,
        install_dbt_deps=True,
    ),
    operator_args={
        "install_deps": True,
        "full_refresh": True,
    },
    profile_config=profile_config,
    render_config=RenderConfig(
        load_method=LoadMode.DBT_LS,
    ),
    schedule="0 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    dag_id="dbt_oms_medallion",
)