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
    branches: [main] # Robot jalan bila kau buat Pull Request ke main

jobs:
  dbt_and_airflow_check:
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
          pip install dbt-bigquery
          pip install pytest  # Untuk test Airflow nanti

      - name: Check dbt Models (Compile)
        run: |
          cd include/dbt/oms_dbt_proj
          dbt compile --profiles-dir . # Robot check kalau SQL kau ada error
        env:
          # Robot perlukan info ni untuk compile (tapi tak run data betul pun)
          GCP_PROJECT_ID: "dummy-project"
          GCP_LOCATION: "asia-southeast1"

      - name: Airflow DAG Integrity Test
        run: |
          pytest tests/test_dag_integrity.py # Kita akan buat fail ni kejap lagi


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

git rm --cached include/gcp-key.json ---> utk ignore file json service account