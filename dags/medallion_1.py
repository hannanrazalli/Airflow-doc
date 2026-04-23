import os
from datetime import datetime
from pathlib import Path

from cosmos import DbtDag, ProjectConfig, ProfileConfig, RenderConfig
from cosmos.constants import LoadMode
from cosmos.profiles import GoogleCloudServiceAccountDictProfileMapping

DBT_PROJECT_PATH = Path("/usr/local/airflow/include/dbt/oms_dbt_proj")

profile_config = ProfileConfig(
    profile_name = "oms_dbt_proj",
    target_name = "dev",
    profile_mapping = GoogleCloudServiceAccountDictProfileMapping(
        conn_id = "google_cloud_default",
        profile_args = {
            "project" : "transactions-practice",
            "dataset" : "bronze",
            "location" : "asia-southeast",
        },
    ),
)

dbt_dag = DbtDag(
    project_config = ProjectConfig(DBT_PROJECT_PATH),
    operator_args = {
        "install_deps" : False,
        "full_refresh" : True
    },
    profile_config = profile_config,
    render_config = RenderConfig(
        load_method = LoadMode.DBT_LS,
        dbt_deps = False
    ),
    schedule = "0 * * * *",
    start_date = datetime(2024,1,1),
    catchup = False,
    dag_id = "medallion_practice"
)