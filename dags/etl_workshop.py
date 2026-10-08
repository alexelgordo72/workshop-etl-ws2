from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
sys.path.insert(0, '/opt/airflow/scripts')
from etl_functions import (extraer_spotify, validar_spotify, transformar_spotify,
    extraer_grammys, transformar_grammys, unir_datasets, cargar_a_db, guardar_csv)

default_args = {'owner': 'alexmosquera', 'retries': 1, 'retry_delay': timedelta(minutes=2)}

with DAG('etl_spotify_grammys_pipeline', default_args=default_args,
    description='Pipeline ETL Spotify + Grammys', schedule_interval='@daily',
    start_date=datetime(2026, 1, 1), catchup=False, tags=['etl', 'ws2']) as dag:

    # Rama Spotify (CSV)
    read_csv = PythonOperator(task_id='read_csv', python_callable=extraer_spotify)
    validate_csv = PythonOperator(task_id='validate_csv', python_callable=validar_spotify)
    transform_csv = PythonOperator(task_id='transform_csv', python_callable=transformar_spotify)

    # Rama Grammys (DB)
    read_db = PythonOperator(task_id='read_db', python_callable=extraer_grammys)
    transform_db = PythonOperator(task_id='transform_db', python_callable=transformar_grammys)

    # Merge, Load y Store
    merge = PythonOperator(task_id='merge', python_callable=unir_datasets)
    load = PythonOperator(task_id='load', python_callable=cargar_a_db)
    store = PythonOperator(task_id='store', python_callable=guardar_csv)

    # Dependencias (como en el diagrama del profesor)
    read_csv >> validate_csv >> transform_csv
    read_db >> transform_db
    [transform_csv, transform_db] >> merge
    merge >> load >> store
