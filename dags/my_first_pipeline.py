from airflow.decorators import dag, task
from datetime import datetime

@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=['belajar'],
)
def my_first_pipeline():

    @task()
    def ambil_data():
        print("Sedang mengambil data dari sumber...")
        return {"id": 1, "status": "aktif"}

    @task()
    def proses_data(data):
        print(f"Memproses data untuk ID: {data['id']}")
        status_baru = data['status'].upper()
        return status_baru

    @task()
    def simpan_data(status):
        print(f"Data berjaya disimpan dengan status: {status}")

    # Susun aliran kerja (The Flow)
    raw_data = ambil_data()
    processed_status = proses_data(raw_data)
    simpan_data(processed_status)

my_first_pipeline()