### Overview
This folder contains the homework for [Module 1 of the Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform) and the necessary scripts / files to solve the questions. The questions and answers can be found in the file [Module_1_Homework_and_Answers.md](https://github.com/hugi-codes/Data-Engineering-Project/blob/main/Homework/Module_1_Homework/Module_1_Homework_and_Answers.md).

### Notes on questions 3,4,5 and 6
These questions involved querying a Postgres Database. A few notes on how the Postgres Database was setup and populated with the data required to answer the questions. 

**Docker-compose.yaml:** used to spin up a docker network with two services: Postgres and pgAdmin. These two services communicate with each other (in other words, this allows us to interact with the Postgres Database via the pgAdmin user interface). The command to start the services that constitute this network is `docker-compose up`.

**ingest_data.py:** Script to ingest data to Postgres. Postgres connection details are specified in this script. Two tables are created in order to answer the questions: taxi_zones and green_taxi_trips. These tables are downloaded from the web, the respective links can be found in ingest_data.py

**Dockerfile:** was used to build the image of the container containing ingest_data.py (and the necessary dependencies). The command used to build the image based on the Dockerfile is  `docker build -t taxi_ingest:v002 .`

The command to run ingest_data.py as a container is 

```
docker run -it 
    --network host 
    taxi_ingest:v002 
    --user=root 
    --password=root 
    --host=localhost 
    --port=5430 
    --db=ny_taxi 
    --table_name_1=green_taxi_trips 
    --table_name_2=taxi_zones 
    --url_1=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz 
    --url_2=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```
When running the ingest_data.py as a docker container, it is necessary to have executed `docker-compose up` before, to have the network up and running (network name is auto-generated and is “module_1_homework_default”).

In the `docker run` statement above, The parameters that follow the image name (*taxi_ingest:v002*) are parameters of ingest_data.py. Thanks to the library "argparse", we can pass arguments to run the python script via the command line. 

### Note on question 7
For question 7, the task was to create a GCP Bucket and Big Query Dataset in GCP via terraform. The terraform files to create these resources are main.tf and variable.tf.