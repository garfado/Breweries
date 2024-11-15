import pandas as pd
from pathlib import Path

# Configuração para exibir até 50 colunas
pd.set_option('display.max_columns', 50)

# Caminho para o diretório da camada Gold
gold_dir = Path("data/gold/")

# Função para obter o arquivo Parquet mais recente
def get_latest_gold_file(gold_dir):
    gold_files = list(gold_dir.glob("*.parquet"))
    if not gold_files:
        print("Nenhum arquivo encontrado na camada Gold.")
        return None
    latest_file = max(gold_files, key=lambda x: x.stat().st_mtime)
    return latest_file

# Obter o arquivo Gold mais recente
latest_gold_file = get_latest_gold_file(gold_dir)

# Verifica se existe um arquivo para carregar
if latest_gold_file:
    # Carrega o DataFrame a partir do arquivo Parquet mais recente
    df_gold = pd.read_parquet(latest_gold_file)

    # Contagem total de registros no DataFrame
    total_records = df_gold.shape[0]
    print(f"Total de registros no DataFrame Gold: {total_records}")

    # Exibe as primeiras 20 linhas e até 50 colunas do DataFrame
    print("Primeiras 20 linhas com até 3 colunas do DataFrame Gold:")
    print(df_gold.head(10))  # Alterado para mostrar as primeiras 20 linhas

    # Contagem de registros distintos na coluna 'state'
    unique_states_count = df_gold['state'].nunique()
    print(f"\nTotal de registros únicos na coluna 'state': {unique_states_count}")

    # Exibe informações gerais sobre o DataFrame, incluindo colunas e tipos de dados
    print("\nInformações do DataFrame Gold:")
    print(df_gold.info())
else:
    print("Nenhum arquivo recente foi encontrado na camada Gold.")
