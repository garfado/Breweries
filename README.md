# Breweries Pipeline
Pipeline de ETL para processamento de dados de cervejarias usando Python, Apache Airflow e Docker.

# Summary
1. [Introdução](#Introdução)

2. [Passo a Passo Docker](#Passo-a-Passo-Docker)
   
 - [Configuração Docker Compose](#Configuração-Docker-Compose)
 - [Executar Airflow-DAG](#Executar-Airflow-DAG)

3. [Implementação da DAG](#Implementação-da-DAG)

4. [Camadas do Pipeline](#Camadas-do-Pipeline)
 - [Camada Bronze](#Camada-Bronze)
 - [Camada Silver](#Camada-Silver)
 - [Camada Gold](#Camada-Gold)

5. [Estrutura do Repositório](#Estrutura-do-Repositório)
6. [Dependências do Projeto](#Dependências-do-Projeto)
7. [Objetivo](#Objetivo)

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

</br></br></br></br></br></br>

## Passo a Passo Docker
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
</br>
** Criando seu docker-compose.yaml

```bash
version: '3.8' 
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres_db_volume:/var/lib/postgresql/data

  webserver:
    image: apache/airflow:2.3.3
    environment:
      AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__WEBSERVER__DEFAULT_UI_USER: admin
      AIRFLOW__WEBSERVER__DEFAULT_UI_PASSWORD: admin
      AIRFLOW__WEBSERVER__SECRET_KEY: '102030'
      AIRFLOW__WEBSERVER__BASE_URL: 'http://webserver:8080'  # URL base definida
      PYTHONPATH: /opt/airflow/dags
      TZ: America/Sao_Paulo  # Ajuste do fuso horário
    depends_on:
      - postgres
    volumes:
      - ./dags:/opt/airflow/dags
      - ./data:/opt/airflow/data
      - ./logs:/opt/airflow/logs  # Montagem dos logs
    ports:
      - "8080:8080"
    command: webserver

  scheduler:
    image: apache/airflow:2.3.3
    environment:
      AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__WEBSERVER__SECRET_KEY: '102030'
      AIRFLOW__WEBSERVER__BASE_URL: 'http://webserver:8080'  # URL base alinhada com o webserver
      PYTHONPATH: /opt/airflow/dags
      TZ: America/Sao_Paulo  # Ajuste do fuso horário
    depends_on:
      - postgres
    volumes:
      - ./dags:/opt/airflow/dags
      - ./data:/opt/airflow/data
      - ./logs:/opt/airflow/logs  # Montagem dos logs para acesso pelo scheduler
    command: scheduler

volumes:
  postgres_db_volume:

```

</br>
**Verificando se o containers do Airflow e a Base de Dados estão inicializada:*

```bash
docker ps
```



**Para acessar o Airflow container:**

```bash
docker exec -it breweries_pipeline-webserver-1 sh

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

## Configuração Docker Compose 
**para ter acesso ao Airflow Container:**
```bash
docker exec -it breweries_pipeline-webserver-1 sh
```
** Localizar o arquivo principal de configuracao do Airflow:**
```bash
find / -name "airflow.cfg"
```
**Editando o arquivo de configuração do Airflow:**
```bash
vi /path/to/airflow.cfg
```
** Um breve exemplo de como desabilitar uma DAGs manualmente via linha de comando:**
```bash
sed -i 's/load_examples = True/load_examples = False/' /path/to/airflow.cfg
```

** Restart Airflow:**
```bash
exit
docker restart breweries_pipeline-webserver-1
```


## Executar Airflow-DAG
</br>
Se voce deseja criar uma DAG de exemplo, altere os exemplos atuais, abaixo um exemplo.

```bash
docker exec -it breweries_pipeline-webserver-1 sh
sed -i 's/load_examples = False/load_examples = True/' /path/to/airflow.cfg
exit
docker restart breweries_pipeline-webserver-1
```

## Implementação da DAG
Os scripts principais da DAG e de cada etapa do pipeline estão nos seguintes arquivos:
Script principal que controla a DAG breweries_dag.py

Seguencia principal DAG breweries 

![image](https://github.com/user-attachments/assets/d849e9ce-4089-47f8-bf7e-e81a1bb29f73)


Preview Breweries DAG.
![image](https://github.com/user-attachments/assets/d40d0683-7f10-40fc-bad3-2c36cd20fba4)

---

## Camadas do Pipeline
Este projeto implementa um pipeline de ETL utilizando Airflow para processar dados de cervejarias. 
O objetivo é transformar dados de uma API em diferentes camadas do pipeline:

- **Bronze**: Dados brutos extraídos da API.
- **Silver**: Dados limpos e tratados.
- **Gold**: Dados finais prontos para análises e visualizações.

----

## Camada Bronze 

Este script realiza a extração de dados da API pública de cervejarias (https://api.openbrewerydb.org/breweries)
e salva os dados brutos no formato JSON na camada Bronze. Ele inclui tratamento de erros, como falhas de conexão
ou problemas no formato da resposta, e implementa um sistema de tentativas com backoff para garantir maior resiliência.
O arquivo gerado é salvo com um timestamp único no diretório data/bronze. Nome do Script fetch_breweries.py

---

## Camada Silver 

 Este script transforma os dados brutos extraídos da camada Bronze para a camada Silver. 
 Ele realiza limpeza, tratamento e padronização dos dados como: Seleção de colunas relevantes.
 Tratamento de valores ausentes, substituindo por padrões como "unknown".
 Ajustes no formato de texto (ex.: capitalização de estados e cidades).
 Conversão de tipos de dados, como longitude e latitude.
 Os dados tratados são salvos em um arquivo Parquet no diretório data/silver, acumulando 
 os dados ao longo das execuções e eliminando duplicatas com base no identificador único (id). 
 Além disso, inclui uma coluna de data_ingestao para rastrear a data da última ingestão.
 Nome do script que faz o tratamento de dadoa Camada Silver transform_breweries.py

Preview Camada Dataframe Silver - script - check_dataframe_silver.py

![image](https://github.com/user-attachments/assets/e7b6e18f-1ed5-424c-b932-7be2bd245eff)

![image](https://github.com/user-attachments/assets/9eb04bff-c820-4050-bac0-1341aa7ea7b8)

---

## Camada Gold 

Este script realiza a agregação dos dados processados na camada Silver, consolidando informações para análises finais:
Busca o arquivo mais recente na camada Silver: Identifica o arquivo Parquet mais recente que contém os dados já limpos e transformados. Realiza a agregação: Agrupa as cervejarias por estado e tipo, gerando uma contagem do número de cervejarias em cada categoria. Salva os dados agregados na camada Gold: Os resultados são exportados em formato Parquet, com um nome único baseado no timestamp. Objetivo: Preparar os dados em um formato consolidado, pronto para consumo em análises ou visualizações.

Preview Camada Dataframe Gold - script - check_dataframe_gold.py

![image](https://github.com/user-attachments/assets/710bfe74-0a96-4732-8df6-4d268426845e)

Preview Schemma de Dados
![image](https://github.com/user-attachments/assets/b0c384e2-f14c-450c-a5e0-1e6b96300f8d)

---

## Estrutura do Repositório:

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
---

## Dependências do Projeto:

* pandas==1.5.3
* requests==2.28.2
* apache-airflow==2.6.0
---

## Objetivo 

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
