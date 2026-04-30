import os
from datetime import datetime
from pathlib import Path
from cosmos import DbtDag, ProjectConfig, ProfileConfig, RenderConfig
from cosmos.constants import LoadMode
from cosmos.profiles import GoogleCloudServiceAccountDictProfileMapping

# --- FIX PATH TERBARU (SANGAT PENTING) ---
# Kita guna AIRFLOW_HOME environment variable. 
# Kalau dlm Docker Astro, dia guna /usr/local/airflow. 
# Kalau dlm GitHub, dia guna path repository.
airflow_home = os.environ.get("AIRFLOW_HOME", "/usr/local/airflow")
DBT_PROJECT_PATH = Path(airflow_home) / "include" / "dbt" / "oms_dbt_proj"

profile_config = ProfileConfig(
    profile_name="oms_dbt_proj",
    target_name="dev",
    profile_mapping=GoogleCloudServiceAccountDictProfileMapping(
        conn_id="google_cloud_default",
        profile_args={
            "project": "transactions-practice",
            "dataset": "silver",
            "location": "asia-southeast1",
        },
    ),
)

dbt_oms_dag = DbtDag(
    project_config=ProjectConfig(
        DBT_PROJECT_PATH,
        install_dbt_deps=True, # Biar Cosmos tolong download deps
    ),
    operator_args={
        "install_deps": True,
        "full_refresh": True,
    },
    profile_config=profile_config,
    render_config=RenderConfig(
        load_method=LoadMode.DBT_LS,
    ),
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    dag_id="dbt_oms_medallion",
)