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

* Camada Bronze (API): fetch_breweries.py
* Camada Silver (Transformação): transform_breweries.py
* Camada Gold (Agregação): aggregate_breweries.py

Cada arquivo contém comentários detalhados e uma explicação de cada etapa.

# Objetivo do desafio 100% realizado com sucesso com upgrade. 

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
de dados e tranformacao.






