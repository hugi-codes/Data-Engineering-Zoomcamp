### Overview
This folder contains the homework for [Module 2 of the Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration) and the necessary scripts / files to solve the questions. The questions and answers can be found in the file [Module_2_Homework_and_Answers.md](https://github.com/hugi-codes/Data-Engineering-Zoomcamp/blob/main/Homework/Module_2_Homework/Module_2_Homework_and_Answers.md)

The homework for Module 2 of the Data Engineering Zoomcamp involves creating an ETL pipeline using the Workflow Orchestration tool [Mage AI](https://www.mage.ai/).

### Notes on Mage
I am running Mage on a VM that is hosted on GCP, so I had to forward the port corresponding to the Mage service to my machine, to be able to access Mage via localhost:6789. See the **docker-compose.yaml** file for more information about the dockerized Mage service. In Mage, a pipeline is a DAG and consists of blocks. Blocks are essentially files (e.g. Python, SQL etc). 

### Notes on the Python files:
* **load_green_taxi_data_api.py**: contains the code of the Data loader block in the Mage pipeline
* **transform_green_taxi_data.py**: contains the code of the Transformer block in the Mage pipeline
* **export_to_gcs.py**: contains the code of the Data Exporter block in the Mage pipeline