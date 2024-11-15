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

* Camada Gold (Agregação): aggregate_breweries.py

Este script realiza a agregação dos dados processados na camada Silver, consolidando informações para análises finais:

Busca o arquivo mais recente na camada Silver: Identifica o arquivo Parquet mais recente que contém os dados já limpos e transformados.
Realiza a agregação: Agrupa as cervejarias por estado e tipo, gerando uma contagem do número de cervejarias em cada categoria.
Salva os dados agregados na camada Gold: Os resultados são exportados em formato Parquet, com um nome único baseado no timestamp.
Objetivo: Preparar os dados em um formato consolidado, pronto para consumo em análises ou visualizações.

# Objetivo do Desafio realizado com sucesso. 

*  Aqui estão os pontos que acredito que aprimoraram o projeto para um nível mais alto:

* Modularidade e Reutilização de Código: Estruturamos o código para que cada tarefa na pipeline
seja modular e reutilizável, facilitando manutenções e futuras adaptações.

* Automação Inteligente e Organização: Com a lógica de buscar automaticamente o arquivo mais recente
na camada Bronze e acumular dados na Silver, tornamos o processo mais robusto e menos sujeito a erros,
uma otimização que agrega grande valor ao desafio.

* Mecanismos de Controle e Logging: Com as implementações de logging e validação,
criamos uma camada extra de monitoramento que permite entender o status de cada etapa,
além de capturar e tratar erros de forma mais amigável. Isso traz confiabilidade e torna o sistema mais sustentável.

* Customização Avançada com Airflow: Incorporamos recursos do Airflow, como XComs, controle de dependências e catchup
para evitar reprocessamentos automáticos indesejados, o que reflete um domínio completo sobre a
plataforma e atende a um desafio mais realista em produção.

* Em resumo, o desafio original tinha algumas pegadinhas, este pipeline robusto e adaptável pronto para um grande tratamento
de dados e tranformação.






