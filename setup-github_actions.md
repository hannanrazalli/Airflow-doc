Step 1: Initialized Git
Buka terminal kat VS Code kau.
git remote -v (untuk check kalau dah link dengan GitHub).
Kalau belum, buat repo baru kat GitHub dan ikut instruction dia untuk git push kod kau


Step 2: Buat Folder Workflow
Dalam folder Airflow-doc, buat folder baru bernama .github
Dalam folder .github, buat folder bernama workflows
Dalam folder workflows, buat satu fail bernama ci_check.yml.
Struktur dia akan jadi: Airflow-doc/.github/workflows/ci_check.yml


Step 3: Tulis Kod CI (Guna Template Senior)

name: Data_Pipeline_CI_Check

on:
  pull_request:
    branches: [main]

jobs:
  ci_validation:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install Dependencies
        run: |
          pip install dbt-bigquery pytest

      - name: Validate dbt Models (Dry Run)
        run: |
          cd include/dbt/oms_dbt_proj
          
          # Kita buat profile dummy. Tak perlukan key .json yang betul pun!
          echo "oms_dbt_proj:
            outputs:
              dev:
                type: bigquery
                method: service-account
                project: dummy-project
                dataset: dummy-dataset
                threads: 1
                keyfile: dummy-key.json # Fail ni tak wujud pun tak apa untuk compile
            target: dev" > profiles.yml
          
          # Guna 'dbt parse' atau 'dbt compile'. 
          # Ia akan check syntax SQL tanpa perlu connect ke BigQuery.
          dbt compile --profiles-dir .
        env:
          DBT_PROFILES_DIR: .

      - name: Airflow DAG Integrity Test
        run: |
          # Check kalau DAG Airflow kau ada syntax error
          export AIRFLOW_HOME=$(pwd)
          pytest tests/test_dag_integrity.py


Step 4: Buat Fail "DAG Integrity Test" (Penting!)
Buat folder tests dalam root Airflow-doc (sebaris dengan dags dan include).
Buat fail test_dag_integrity.py dlm folder tu.

import pytest
from airflow.models import DagBag

def test_dag_loading():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert len(dagbag.import_errors) == 0, f"DAG import errors: {dagbag.import_errors}"


Step 5: Test Pipeline Kau!
Buat Branch Baru: Kat VS Code terminal, taip: git checkout -b feature/test-ci
Edit Sikit Kod: Contohnya, tambah satu comment kat dalam stg_transactions.sql
Push:
- git add .
- git commit -m "Testing my first CI pipeline"
- git push origin feature/test-ci

2. Cara setelkan Error "Push cannot contain secrets"
git rm --cached include/gcp-key.json ---> utk ignore file json service account

Step B: Update .gitignore
Buka fail .gitignore kat folder root kau.
include/gcp-key.json
.env



Senior Logic" – Habis tu macam mana Robot CI nak access BigQuery?
Pergi ke repo GitHub kau kat browser.
Klik Settings > Secrets and variables > Actions.
Klik New repository secret.
Nama: GCP_SA_KEY.
Value: Copy semua isi kandungan dalam fail gcp-key.json kau dan paste kat situ.


git add --all
git commit -m "Cleanup secret key and prepare for CI"
git push origin feature/test-ci
