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
