# Breweries Pipeline

Pipeline de ETL para processamento de dados de cervejarias usando Python, Apache Airflow e Docker.

---

## Summary
1. [Introduction](#introduction)
2. [Step-by-Step Instructions Docker](#step-by-step-instructions-docker)
   - [Install Docker](#install-docker)
   - [Setup Docker Compose](#setup-docker-compose)
   - [Running the Airflow Environment](#running-the-airflow-environment)
3. [Steps to Start Airflow Without Example DAGs](#steps-to-start-airflow-without-example-dags)

---

## Introduction
Este projeto implementa um pipeline de ETL utilizando Airflow para processar dados de cervejarias. O objetivo é transformar dados de uma API em diferentes camadas do pipeline:
- **Bronze**: Dados brutos extraídos da API.
- **Silver**: Dados limpos e tratados.
- **Gold**: Dados finais prontos para análises e visualizações.

### Tecnologias Utilizadas
- **Python**: Para desenvolver scripts de ETL.
- **Airflow**: Para orquestrar as tarefas.
- **Docker**: Para criar um ambiente isolado e replicável.
- **Pandas**: Para manipulação de dados.

---

## Step-by-Step Instructions Docker

### Install Docker
Antes de iniciar, é necessário instalar o Docker no seu sistema. Siga as instruções oficiais de acordo com seu sistema operacional:
- [Instalação no Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Instalação no macOS](https://docs.docker.com/desktop/install/mac-install/)
- [Instalação no Linux](https://docs.docker.com/engine/install/)

### Setup Docker Compose
1. Certifique-se de que o Docker Compose está instalado:
   ```docker compose 
   
### Setup Container Airflow

   docker-compose.yaml
   version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres_db_volume:/var/lib/postgresql/data

  webserver:
    image: apache/airflow:2.3.3
    environment:
      AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__WEBSERVER__DEFAULT_UI_USER: admin
      AIRFLOW__WEBSERVER__DEFAULT_UI_PASSWORD: admin
      AIRFLOW__WEBSERVER__SECRET_KEY: '102030'
      AIRFLOW__WEBSERVER__BASE_URL: 'http://webserver:8080'  # URL base definida
      PYTHONPATH: /opt/airflow/dags
      TZ: America/Sao_Paulo  # Ajuste do fuso horário
    depends_on:
      - postgres
    volumes:
      - ./dags:/opt/airflow/dags
      - ./data:/opt/airflow/data
      - ./logs:/opt/airflow/logs  # Montagem dos logs
    ports:
      - "8080:8080"
    command: webserver

  scheduler:
    image: apache/airflow:2.3.3
    environment:
      AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__WEBSERVER__SECRET_KEY: '102030'
      AIRFLOW__WEBSERVER__BASE_URL: 'http://webserver:8080'  # URL base alinhada com o webserver
      PYTHONPATH: /opt/airflow/dags
      TZ: America/Sao_Paulo  # Ajuste do fuso horário
    depends_on:
      - postgres
    volumes:
      - ./dags:/opt/airflow/dags
      - ./data:/opt/airflow/data
      - ./logs:/opt/airflow/logs  # Montagem dos logs para acesso pelo scheduler
    command: scheduler

volumes:
  postgres_db_volume:

### Setup Dag Airflow

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

### Setup Camada API

import requests
from datetime import datetime
from pathlib import Path
import logging
import time
import json

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_breweries(retries=3, backoff_factor=2):
    url = "https://api.openbrewerydb.org/breweries"
    attempt = 0

    while attempt < retries:
        try:
            logging.info("Iniciando requisição à API de cervejarias.")
            
            # Envio da requisição com tempo limite
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Validar se a resposta está em formato JSON esperado
            try:
                breweries_data = response.json()
            except json.JSONDecodeError as json_err:
                logging.error(f"Erro ao decodificar JSON: {json_err}")
                return None

            # Diretório de destino para dados brutos
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            bronze_path = Path(f"data/bronze/breweries_{timestamp}.json")
            bronze_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Salvando os dados brutos no arquivo JSON
            with bronze_path.open("w") as f:
                json.dump(breweries_data, f, indent=4)
            
            logging.info(f"Dados brutos salvos em {bronze_path}")
            return str(bronze_path)

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP ao tentar obter dados: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Erro de conexão: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"A requisição à API demorou muito e foi interrompida: {timeout_err}")
        except Exception as e:
            logging.error(f"Ocorreu um erro inesperado: {e}")

        # Esperar antes de uma nova tentativa, aplicando backoff
        attempt += 1
        wait_time = backoff_factor ** attempt
        logging.info(f"Tentativa {attempt} falhou. Tentando novamente em {wait_time} segundos...")
        time.sleep(wait_time)

    logging.error("Número máximo de tentativas atingido. Não foi possível obter os dados.")
    return None

# Chamada direta para executar a função ao rodar o script FILTRINN
if __name__ == "__main__":
    start_time = time.time()
    fetch_breweries()
    end_time = time.time()
    logging.info(f"Tempo de execução: {end_time - start_time:.2f} segundos")

### Setup Camada Silver 

import pandas as pd
from pathlib import Path
from datetime import datetime
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_latest_bronze_file(bronze_dir="data/bronze"):
    """
    Função para encontrar o arquivo JSON mais recente na camada Bronze.
    """
    bronze_files = list(Path(bronze_dir).glob("*.json"))
    if not bronze_files:
        logging.error("Nenhum arquivo JSON encontrado na camada Bronze.")
        return None
    
    latest_file = max(bronze_files, key=lambda x: x.stat().st_mtime)
    logging.info(f"Arquivo Bronze mais recente encontrado: {latest_file}")
    return latest_file

def transform_to_silver(file_path=None):
    """
    Transforma dados da camada Bronze para Silver, acumulando no mesmo arquivo Parquet.
    
    Parâmetros:
    - file_path (str): Caminho para o arquivo JSON específico na camada Bronze. Se não for fornecido,
      a função buscará o arquivo mais recente automaticamente.
    """
    # Se o file_path não for fornecido, busca o mais recente na camada Bronze
    if file_path is None:
        file_path = get_latest_bronze_file()
    
    if not file_path:
        logging.error("Nenhum arquivo encontrado na camada Bronze para processar.")
        return None

    silver_path = Path("data/silver/")
    silver_path.mkdir(parents=True, exist_ok=True)

    # Carregar dados novos da camada Bronze
    try:
        new_data = pd.read_json(file_path)
        logging.info("Arquivo JSON carregado com sucesso.")
    except ValueError as e:
        logging.error(f"Erro ao ler o arquivo JSON: {e}")
        raise ValueError(f"Erro ao ler o arquivo JSON: {e}")

    # Seleção de colunas e tratamento
    columns_to_keep = ["id", "name", "brewery_type", "city", "state", "country", "longitude", "latitude"]
    new_data = new_data[columns_to_keep]

    new_data['state'].fillna("unknown", inplace=True)
    new_data['brewery_type'].fillna("unknown", inplace=True)
    new_data['state'] = new_data['state'].str.strip().str.title()
    new_data['city'] = new_data['city'].str.strip().str.title()
    new_data['longitude'] = pd.to_numeric(new_data['longitude'], errors='coerce')
    new_data['latitude'] = pd.to_numeric(new_data['latitude'], errors='coerce')

    # Carregar dados já existentes na camada Silver, se houver
    silver_file = silver_path / "breweries_silver.parquet"
    if silver_file.exists():
        logging.info("Carregando dados existentes da camada Silver.")
        existing_data = pd.read_parquet(silver_file)
        combined_data = pd.concat([existing_data, new_data]).drop_duplicates(subset=['id']).reset_index(drop=True)
    else:
        combined_data = new_data

    # Adicionar coluna de data_ingestao
    combined_data['data_ingestao'] = datetime.now()

    # Salvar em Parquet na camada Silver, particionando por estado
    try:
        combined_data.to_parquet(silver_file, index=False, partition_cols=["state"], compression='snappy')
        logging.info(f"Dados acumulados e salvos na camada Silver em {silver_file}")
    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo Parquet: {e}")
        raise IOError(f"Erro ao salvar o arquivo Parquet: {e}")
    
    return str(silver_file)

if __name__ == "__main__":
    transform_to_silver()

### Setup Camada Gold
import pandas as pd
from pathlib import Path
import logging
import time  # Para esperar antes de repetir a busca pelo arquivo

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_latest_silver_file(silver_dir="data/silver"):
    """
    Função para encontrar o arquivo Parquet mais recente na camada Silver.
    
    Parâmetros:
    silver_dir (str): Caminho do diretório da camada Silver.
    
    Retorna:
    Path: O caminho do arquivo Parquet mais recente ou None se não houver arquivos.
    """
    # Localizar todos os arquivos Parquet no diretório Silver
    silver_files = list(Path(silver_dir).glob("*.parquet"))
    if not silver_files:
        logging.error("Nenhum arquivo encontrado na camada Silver. Tentando novamente em 2 segundos...")
        time.sleep(2)  # Espera 2 segundos antes de tentar novamente
        silver_files = list(Path(silver_dir).glob("*.parquet"))
        if not silver_files:
            logging.error("Nenhum arquivo encontrado na camada Silver após esperar.")
            return None
    
    # Selecionar o arquivo mais recente baseado na data de modificação
    latest_file = max(silver_files, key=lambda x: x.stat().st_mtime)
    logging.info(f"Arquivo Silver mais recente encontrado: {latest_file}")
    return latest_file

def aggregate_gold(silver_dir="data/silver/"):
    try:
        # Obter o arquivo mais recente da camada Silver
        latest_silver_file = get_latest_silver_file(silver_dir)
        if not latest_silver_file:
            logging.error("Nenhum arquivo encontrado na camada Silver para agregar.")
            return None  # Retorna None se não houver arquivos para processar

        # Leitura do arquivo Silver
        logging.info(f"Lendo dados do arquivo Silver: {latest_silver_file}")
        df = pd.read_parquet(latest_silver_file)

        # Agregação dos dados para contar o número de cervejarias por estado e tipo
        agg_df = df.groupby(['state', 'brewery_type']).size().reset_index(name='brewery_count')

        # Caminho para salvar o resultado na camada Gold com timestamp
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M-%S")
        gold_path = Path("data/gold/")
        gold_path.mkdir(parents=True, exist_ok=True)
        output_file = gold_path / f"breweries_aggregated_{timestamp}.parquet"

        # Salvar o DataFrame agregado como Parquet
        agg_df.to_parquet(output_file, index=False)
        
        logging.info(f"Dados agregados e salvos na camada Gold em {output_file}")
        return str(output_file)

    except FileNotFoundError as fnf_error:
        logging.error(f"Erro de arquivo não encontrado: {fnf_error}")
    except pd.errors.EmptyDataError as ede:
        logging.error(f"Erro: Arquivo Silver está vazio ou corrompido: {ede}")
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado durante o processo de agregação: {e}")
    
    return None

# Chamada direta para execução do script
if __name__ == "__main__":
    aggregate_gold()

