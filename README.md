# Breweries Pipeline
Pipeline de ETL para processamento de dados de cervejarias usando Python, Apache Airflow e Docker.

---

## Summary
1. [Introdução](#introduction)
2. [Passo a Passo Instruções Docker](#step-by-step-instructions-docker)
   - [Instalação Docker](#install-docker)
   - [configuração Docker Compose](#setup-docker-compose)
   - [Executar Airflow ](#running-the-airflow-environment)
3. [Passo a Passo Airflow DAGs](#steps-to-start-airflow-without-example-dags)
4. [Implementação da DAG](#implementação-da-dag)

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
   ```bash
   docker compose version
## Configuração do Docker Compose para o Airflow
docker compose up airflow-init
docker compose up
Acesse o Airflow na URL: http://localhost:8080.

## Steps to Start Airflow Without Example DAGs
Certifique-se de que a variável de ambiente AIRFLOW__CORE__LOAD_EXAMPLES está configurada como False. Isso impede a criação de DAGs de exemplo.
environment:
  - AIRFLOW__CORE__LOAD_EXAMPLES=False
    
No arquivo docker-compose.yaml, adicione o seguinte comando no serviço webserver.
command: webserver

Suba o ambiente:
docker compose up

Verifique no Airflow UI que nenhum DAG de exemplo foi carregado, usando a URL acima.

Implementação da DAG
Os scripts principais da DAG e de cada etapa do pipeline estão nos seguintes arquivos:

## Implementação DAG: breweries_dag.py

Os scripts principais da DAG e de cada etapa do pipeline estão nos seguintes arquivos:
Cada arquivo contém comentários detalhados e uma explicação de cada etapa.


* Camada Bronze (API): fetch_breweries.py

Este script realiza a extração de dados da API pública de cervejarias (https://api.openbrewerydb.org/breweries)
e salva os dados brutos no formato JSON na camada Bronze. Ele inclui tratamento de erros, como falhas de conexão
ou problemas no formato da resposta, e implementa um sistema de tentativas com backoff para garantir maior resiliência.
O arquivo gerado é salvo com um timestamp único no diretório data/bronze.
  
* Camada Silver (Transformação): transform_breweries.py

Este script transforma os dados brutos extraídos da camada Bronze para a camada Silver. 
Ele realiza limpeza, tratamento e padronização dos dados, 
como: Seleção de colunas relevantes.
Tratamento de valores ausentes, substituindo por padrões como "unknown".
Ajustes no formato de texto (ex.: capitalização de estados e cidades).
Conversão de tipos de dados, como longitude e latitude.
Os dados tratados são salvos em um arquivo Parquet no diretório data/silver, acumulando 
os dados ao longo das execuções e eliminando duplicatas com base no identificador único (id). 
Além disso, inclui uma coluna de data_ingestao para rastrear a data da última ingestão.

# Preview Camada Dataframe Silver - script - check_dataframe_silver.py

![image](https://github.com/user-attachments/assets/e7b6e18f-1ed5-424c-b932-7be2bd245eff)

![image](https://github.com/user-attachments/assets/9eb04bff-c820-4050-bac0-1341aa7ea7b8)


* Camada Gold (Agregação): aggregate_breweries.py

Este script realiza a agregação dos dados processados na camada Silver, consolidando informações para análises finais:

Busca o arquivo mais recente na camada Silver: Identifica o arquivo Parquet mais recente que contém os dados já limpos e transformados.
Realiza a agregação: Agrupa as cervejarias por estado e tipo, gerando uma contagem do número de cervejarias em cada categoria.
Salva os dados agregados na camada Gold: Os resultados são exportados em formato Parquet, com um nome único baseado no timestamp.
Objetivo: Preparar os dados em um formato consolidado, pronto para consumo em análises ou visualizações.

# Preview Camada Dataframe Gold - script - check_dataframe_gold.py

![image](https://github.com/user-attachments/assets/710bfe74-0a96-4732-8df6-4d268426845e)

# Preview Schemma de Dados
![image](https://github.com/user-attachments/assets/b0c384e2-f14c-450c-a5e0-1e6b96300f8d)


# Estrutura do Repositório:

* ├── dags/
* │   ├── breweries_dag.py
* │   ├── scripts/
* │       ├── fetch_breweries.py
* │       ├── transform_breweries.py
* │       ├── aggregate_breweries.py
* ├── data/
* │   ├── bronze/
* │   ├── silver/
* │   ├── gold/
* ├── docker-compose.yaml
* ├── README.md

# Dependências do projeto, como pandas, requests, apache-airflow, para facilitar a instalação:

* pandas==1.5.3
* requests==2.28.2
* apache-airflow==2.6.0

# Objetivo do Desafio realizado com sucesso. 

*  Aqui estão os pontos importantes que pode justificar este projeto entrar em produção:

* Modularidade e Reutilização de Código: Estruturamos o código para que cada tarefa na pipeline
seja modular e reutilizável, facilitando manutenções e futuras adaptações.

* Automação Inteligente com a lógica de buscar automaticamente o arquivo mais recente
na camada Bronze e acumular dados na Silver, tornamos o processo mais robusto e menos sujeito a erros,
uma otimização que agrega grande valor ao desafio.

* Mecanismos de Controle e Logging: Com as implementações de logging e validação,
foi criada uma camada extra de monitoramento que permite entender o status de cada etapa,
além de capturar e tratar erros de forma mais amigável. Isso traz confiabilidade e torna o sistema mais sustentável.

* Customização Avançada com Airflow: foi aplicado no Airflow os parametros XComs e controle de dependências e catchup
para evitar reprocessamentos automáticos indesejados, com isto a plataforma vai ser aplicada em produção de forma segura.

* Em resumo, o desafio busca um tratamento de dados e integração entre linguagns e orquestradores e integração com cloud,
foi criado um pipeline robusto e adaptável pronto para um grande tratamento de dados e tranformação tudo de forma automatica.

* Este pipeline, pode ser aplicado em ambientes com GCP - Azure e AWS.
