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
