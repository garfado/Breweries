# Breweries Pipeline
Pipeline de ETL para processamento de dados de cervejarias usando Python, Apache Airflow e Docker.

# Summary
1. [Introdução](#Introdução)

2. [Passo a Passo Docker](#Passo-a-Passo-Instruções-Docker)
 - [Instalação Docker](#Instalação-Docker)
 - [Configuração Docker Compose](#Configuração-Docker-Compose)
 - [Executar Airflow](#Executar-Airflow
 - [Step-by-Step Instrodução ao Docker](#step-by-step-instructions-docker)
 - [Steps to Start Airflow Without Example DAGs](#steps-to-start-airflow-without-example-dags)


3. [Passo a Passo Airflow DAGs](#Passo-a-Passo-Airflow-DAGs)
4. [Implementação da DAG](#Implementação-da-DAG)

5. [Camadas do Pipeline](#Camadas-do-Pipeline)
 - [Camada Bronze](#Camada-Bronze)
 - [Camada Silver](#Camada-Silver)
 - [Camada Gold](#Camada-Gold)

6. [Estrutura do Repositório](#Estrutura-do-Repositório)
7. [Dependências do Projeto](#Dependências-do-Projeto)
8. [Objetivo e Justificativa](#Objetivo-e-Justificativa)

</br></br></br></br></br></br>

## Introdução
Este repositório contém um estudo de caso sobre um banco de dados de cervejarias por localização, onde você pode examinar todo o fluxo de trabalho de engenharia de dados. este projeto suporta todas as ferramentas abaixo:

- <img src="https://static-00.iconduck.com/assets.00/airflow-icon-512x512-tpr318yf.png" alt="Airflow" width="25" style="vertical-align: middle;"/>  Airflow for orchestration
- <img src="https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png" alt="Docker" width="25" style="vertical-align: middle;"/>  Docker
- <img src="https://upload.wikimedia.org/wikipedia/commons/f/f3/Apache_Spark_logo.svg" alt="Pyspark" width="25" style="vertical-align: middle;"/>  Pyspark
- <img src="https://upload.wikimedia.org/wikipedia/commons/6/63/Databricks_Logo.png" alt="Databricks" width="25" style="vertical-align: middle;"/>  DataBricks
- <img src="https://img.icons8.com/?size=100&id=13441&format=png&color=000000" alt="Python" width="25" style="vertical-align: middle;"/>  Python for API requests
- <img src="https://img.icons8.com/?size=100&id=WHRLQdbEXQ16&format=png&color=000000" alt="GCP" width="25" style="vertical-align: middle;"/>  GCP
- <img src="https://img.icons8.com/?size=96&id=ThrCWrDxDa0v&format=png" lt="Azure" width="25" style="vertical-align: middle;"/> Azure

Este projeto implementa um pipeline de ETL utilizando Airflow para processar dados de cervejarias. 
O objetivo é transformar dados de uma API em diferentes camadas do pipeline:

- **Bronze**: Dados brutos extraídos da API.
- **Silver**: Dados limpos e tratados.
- **Gold**: Dados finais prontos para análises e visualizações.

</br></br></br></br></br></br>
## Step-by-Step Instrodução ao Docker
**Vamos Navegar pelo projeto:**

```bash
   cd /breweries_pipeline/
```
</br>


**⚠️ Atenção:**
Se você estiver executando este projeto no Windows usando o VS Code, certifique-se de que o arquivo start_airflow.sh esteja configurado com finais de linha no formato LF (Line Feed) para evitar erros.

</br>
**Inicializando o containers Docker :**

```bash
docker-compose up -d
```

**Verificando se o containers do Airflow e a Base de Dados estão inicializada.**

```bash
docker ps
```

**Para acessar o Airflow container:**

```bash
docker exec -it breweries_pipeline-webserver-1 sh
```

**Criar usuario do Airflow : Airflow container, Siga os passos abaixo:**
<br/>
This will create an admin user with the username admin and password admin.
```bash
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com
```

**Para sair Airflow container:**
```bash
exit
```

**procedimento para desativar Docker containers:**
you can stop and remove the containers:

```bash
docker-compose down
```
</br></br></br></br></br></br>
## Processo para dar Start Airflow um simples Examplo de DAGs**
**para ter acesso ao Airflow Container:**
```bash
docker exec -it breweries_pipeline-webserver-1 sh
```
**Localizar o arquivo principal de configuracao do Airflow:**
```bash
find / -name "airflow.cfg"
```
**Editando o arquivo de configuração do Airflow:**
```bash
vi /path/to/airflow.cfg
```
**Um breve exemplo de como desabilitar uma DAGs manualmente via linha de comando:**
```bash
sed -i 's/load_examples = True/load_examples = False/' /path/to/airflow.cfg
```

**Restart Airflow:**
```bash
exit
docker restart breweries_pipeline-webserver-1
```


**Examplo de como habilitar uma DAGs:**
</br>
If you want to re-enable the example DAGs, change load_examples = False back to load_examples = True.

```bash
docker exec -it breweries_pipeline-webserver-1 sh
sed -i 's/load_examples = False/load_examples = True/' /path/to/airflow.cfg
exit
docker restart breweries_pipeline-webserver-1
```
