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
