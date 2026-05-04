1) go to:
https://www.docker.com/products/docker-desktop/
download docker desktop > install

2) go to:
https://github.com/astronomer/astro-cli/releases

3) download:
astro_1.41.0_windows_amd64.exe

4) Create folder named "astro-cli" in local disk C
paste file downloaded from github
rename file jadi "astro"

5) Win > env > Edit the system environment variables > System variables > Path > Edit > New > C:\astro-cli > OK

6) Open PowerShell:
$env:Path += ";C:\astro-cli"
astro version

(7) cd C:\Users\HP\Documents\GitHub\Airflow-doc ---> folder initialize
C:\astro-cli\astro.exe dev init
C:\astro-cli\astro.exe dev start
C:\astro-cli\astro.exe dev stop
C:\astro-cli\astro.exe dev parse

go to:
http://localhost:8080

Right click at dags > New File > my_first_pipeline.py ---> apa2 nama shj

C:\astro-cli\astro.exe dev restart


---------------------------------------------------------------------------------------------
REQUIREMENTS.TXT
# Astro Runtime includes the following pre-installed providers packages: https://www.astronomer.io/docs/astro/runtime-image-architecture#provider-packages
apache-airflow-providers-databricks
astronomer-cosmos  # Ini untuk run dbt
apache-airflow-providers-google # Untuk BigQuery
apache-airflow-providers-dbt-cloud
dbt-bigquery

---------------------------------------------------------------------------------------------
DOCKERFILE ---> MAINTAIN
FROM astrocrpublic.azurecr.io/runtime:3.1-14

---------------------------------------------------------------------------------------------
# KALAU TAK BOLEH BUKA localhost:8080
C:\astro-cli\astro.exe dev stop
docker system prune -f
C:\astro-cli\astro.exe dev start

---------------------------------------------------------------------------------------------
# LOCATION LOCAL FILE JSON GCP
/usr/local/airflow/include/gcp-key.json

---------------------------------------------------------------------------------------------
DAG FILE (CTH: practice_1.py)

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
            "location" : "asia-southeast1",
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
    schedule = "0 */2 * * *",
    start_date = datetime(2024, 1, 1),
    catchup = False,
    dag_id = "medallion_practice"
)



------------------------------------------------------------------------------------------

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
__________________________________________________________________________________________

create .env dalam fodler sebaris include & dags (text file) ---> akan jadi bentuk gear

GCP_PROJECT_ID=transactions-practice
GCP_DATASET_BRONZE=bronze
GCP_LOCATION=asia-southeast1
IS_PRODUCTION=False

__________________________________________________________________________________________


