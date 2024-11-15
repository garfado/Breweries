import pandas as pd
from pathlib import Path

# Configuração de Logging
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Caminho para o diretório da camada Silver
silver_dir = Path("data/silver/")

# Função para obter o arquivo Parquet mais recente
def get_latest_silver_file(silver_dir):
    """
    Obtém o arquivo Parquet mais recente na camada Silver.
    """
    silver_files = list(silver_dir.glob("*.parquet"))
    if not silver_files:
        logging.error("Nenhum arquivo encontrado na camada Silver.")
        return None
    latest_file = max(silver_files, key=lambda x: x.stat().st_mtime)
    logging.info(f"Arquivo Silver mais recente encontrado: {latest_file}")
    return latest_file

# Obter o arquivo Silver mais recente
latest_silver_file = get_latest_silver_file(silver_dir)

# Verifica se existe um arquivo para carregar
if latest_silver_file:
    # Carrega o DataFrame a partir do arquivo Parquet mais recente
    try:
        df_silver = pd.read_parquet(latest_silver_file)
        logging.info("Arquivo Parquet carregado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao carregar o arquivo Parquet: {e}")
        df_silver = None

    if df_silver is not None:
        # Verificação e tratamento de valores nulos nas colunas 'longitude' e 'latitude'
        if df_silver[['longitude', 'latitude']].isnull().any().any():
            logging.warning("Existem valores nulos em 'longitude' ou 'latitude'.")
            
            # Preenchendo valores nulos com 0
            df_silver['longitude'] = df_silver['longitude'].fillna(0)
            df_silver['latitude'] = df_silver['latitude'].fillna(0)
            logging.info("Valores nulos em 'longitude' e 'latitude' foram preenchidos com 0.")

        # Verificar e tratar duplicatas
        duplicate_count = df_silver.duplicated(subset=['id']).sum()
        if duplicate_count > 0:
            logging.warning(f"Existem {duplicate_count} registros duplicados no DataFrame Silver.")
            df_silver = df_silver.drop_duplicates(subset=['id']).reset_index(drop=True)
            logging.info("Registros duplicados foram removidos.")

        # Garantir que a coluna 'state' está no tipo correto
        df_silver['state'] = df_silver['state'].astype('object')

        # Exibe as primeiras linhas do DataFrame
        print("\n--- Primeiras linhas do DataFrame Silver ---")
        print(df_silver.head(20))

        # Exibe informações gerais sobre o DataFrame
        print("\n--- Informações do DataFrame Silver ---")
        print(df_silver.info())

        # Exibe estatísticas descritivas
        print("\n--- Estatísticas Descritivas ---")
        print(df_silver.describe(include='all'))

else:
    logging.error("Nenhum arquivo recente foi encontrado na camada Silver.")
