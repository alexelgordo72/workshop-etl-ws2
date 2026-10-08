from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
sys.path.insert(0, '/opt/airflow/scripts')
from etl_functions import extraer_spotify, validar_spotify, transformar_spotify
from etl_functions import extraer_grammys, transformar_grammys, unir_datasets
from etl_functions import cargar_a_db, guardar_csv

default_args = {
    'owner': 'alexelgordo',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'etl_spotify_grammys_pipeline',
    default_args=default_args,
    description='Pipeline ETL Spotify + Grammys',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['etl', 'ws2'],
) as dag:

    # Tareas de Spotify
    t1 = PythonOperator(task_id='extract_spotify', python_callable=extraer_spotify)
    t2 = PythonOperator(task_id='validate_spotify', python_callable=validar_spotify)
    t3 = PythonOperator(task_id='transform_spotify', python_callable=transformar_spotify)

    # Tareas de Grammys
    t4 = PythonOperator(task_id='extract_grammys', python_callable=extraer_grammys)
    t5 = PythonOperator(task_id='transform_grammys', python_callable=transformar_grammys)

    # Merge y carga
    t6 = PythonOperator(task_id='merge_datasets', python_callable=unir_datasets)
    t7 = PythonOperator(task_id='load_to_db', python_callable=cargar_a_db)
    t8 = PythonOperator(task_id='save_csv', python_callable=guardar_csv)

    # Dependencias
    t1 >> t2 >> t3
    t4 >> t5
    [t3, t5] >> t6
    t6 >> [t7, t8]
