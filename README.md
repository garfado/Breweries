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
---

## Camada Gold 

Este script realiza a agregação dos dados processados na camada Silver, consolidando informações para análises finais:
Busca o arquivo mais recente na camada Silver: Identifica o arquivo Parquet mais recente que contém os dados já limpos e transformados. Realiza a agregação: Agrupa as cervejarias por estado e tipo, gerando uma contagem do número de cervejarias em cada categoria. Salva os dados agregados na camada Gold: Os resultados são exportados em formato Parquet, com um nome único baseado no timestamp. Objetivo: Preparar os dados em um formato consolidado, pronto para consumo em análises ou visualizações.

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

## Objetivo e Justificativa. 

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
