from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.fetch_breweries import fetch_breweries
from scripts.transform_breweries import transform_to_silver
from scripts.aggregate_breweries import aggregate_gold

default_args = {
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

def fetch_breweries_wrapper(**kwargs):
    # Chama a função original e retorna o caminho do arquivo
    file_path = fetch_breweries()
    # Envia o caminho para o XCom
    kwargs['ti'].xcom_push(key='file_path', value=file_path)

def transform_to_silver_wrapper(**kwargs):
    """
    Wrapper para transformar dados para a camada Silver.
    """
    transform_to_silver()  # Chamada direta sem argumentos

with DAG("breweries_dag", default_args=default_args, schedule_interval="@daily", catchup=False) as dag:
    fetch_task = PythonOperator(
        task_id="fetch_breweries",
        python_callable=fetch_breweries_wrapper,
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id="transform_to_silver",
        python_callable=transform_to_silver_wrapper,
        provide_context=True
    )

    aggregate_task = PythonOperator(
        task_id="aggregate_gold",
        python_callable=aggregate_gold
    )

    # Definir a sequência das tarefas
    fetch_task >> transform_task >> aggregate_task
