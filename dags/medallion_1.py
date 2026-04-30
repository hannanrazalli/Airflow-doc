import os
from datetime import datetime
from pathlib import Path
from cosmos import DbtDag, ProjectConfig, ProfileConfig, RenderConfig
from cosmos.constants import LoadMode
from cosmos.profiles import GoogleCloudServiceAccountDictProfileMapping

# --- REPAIR 1: DYNAMIC PATH ---
# Ini akan cari folder project secara automatik tak kira dkt mana dia run
BASE_DIR = Path(__file__).resolve().parent.parent
DBT_PROJECT_PATH = BASE_DIR / "include" / "dbt" / "oms_dbt_proj"

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
        # --- REPAIR 2: FIX COSMOS ERROR ---
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
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    dag_id="dbt_oms_medallion",
)