### Overview
This folder contains the homework for [Module 3 of the Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/03-data-warehouse) and the necessary scripts / files to solve the questions. The questions and answers can be found in the file [Module_3_Homework_and_Answers.md](https://github.com/hugi-codes/Data-Engineering-Zoomcamp/blob/main/Homework/Module_3_Homework/Module_3_Homework_and_Answers.md)

The homework involves loading data to a GCP bucket and then creating an External Table and a Materialised Table, which are queried in Big Query. Furthermore, techniques such as partitioning and clustering are leveraged to increase query performance. 

The data used for this homework is the [2022 green taxi data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). The data for each month of 2022 is stored in its corresponding Parquet file, meaning that in total there are 12 parquet files.

### Notes on the Python files:
* **upload_to_gcs.py**: script that uploads parquet files of the green taxi data to a GCP bucket
* **m3_homework_queries.sql**: contains the SQL queries that provide the answers to the questions

Regarding the upload of Parquet files to GCP using Python via a download URL: In order for Python and GCP to be able to authenticate, you can use the ```EXPORT CREDENTIALS ``` command to create and download a service account key file, which contains the necessary credentials. This key file must then be set in your environment or passed to the Google Cloud Storage client to establish authenticated access to your GCP resources.