# Breweries Pipeline
Pipeline de ETL para processamento de dados de cervejarias usando Python, Apache Airflow e Docker.

---

#Summary
1. [Introdução](#Introdução)

2. [Passo a Passo Instruções Docker](#Passo-a-Passo-Instruções-Docker)
 - [Instalação Docker](#Instalação-Docker)
 - [Configuração Docker Compose](#Configuração-Docker-Compose)
 - [Executar Airflow](#Executar-Airflow)

3. [Passo a Passo Airflow DAGs](Passo-a-Passo-Airflow-DAGs)
4. [Implementação da DAG](#Implementação-da-DAG)

5. [Camadas do Pipeline](#Camadas-do-Pipeline)
 - [Camada Bronze](#Camada-Bronze)
 - [Camada Silver](#Camada-Silver)
 - [Camada Gold](#Camada-Gold)

6. [Estrutura do Repositório](#Estrutura-do-Repositório)
7. [Dependências do Projeto](#Dependências-do-Projeto)
8. [Objetivo e Justificativa](#Objetivo-e-Justificativa)

---

#Introdução

Este projeto implementa um pipeline de ETL utilizando Airflow para processar dados de cervejarias. 
O objetivo é transformar dados de uma API em diferentes camadas do pipeline:

- **Bronze**: Dados brutos extraídos da API.
- **Silver**: Dados limpos e tratados.
- **Gold**: Dados finais prontos para análises e visualizações.

# Tecnologias Utilizadas

- **Python**: Para desenvolver scripts de ETL.
- **Airflow**: Para orquestrar as tarefas.
- **Docker**: Para criar um ambiente isolado e replicável.
- **Pandas**: Para manipulação de dados.
   

   
