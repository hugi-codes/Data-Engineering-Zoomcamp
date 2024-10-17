--The following SQL commands were executed in Google Big Query.

-------------------------------------------------------------------------------------------
-- SETUP: Creating an external table from parquet files stored in a GCP bucket
-- The URIS argument serves to point to the GCP bucket
-- The star * says: All files in that bucket
CREATE OR REPLACE EXTERNAL TABLE `spatial-encoder-432509-n7.module_3_homework.external_m3_green_taxi`
OPTIONS(
  FORMAT = "PARQUET",
  URIS = ["gs://module-3-homework/*"]
)
-- SETUP: Creating a Materialised Table from the External Table
-- Queries on this table will scan data stored in BigQuery’s native storage, and BigQuery 
-- has optimized this data to be read more efficiently than GCS files.
CREATE OR REPLACE TABLE `spatial-encoder-432509-n7.module_3_homework.m3_green_taxi`
  as (SELECT * FROM `spatial-encoder-432509-n7.module_3_homework.external_m3_green_taxi`);
-------------------------------------------------------------------------------------------
-- Query for Q1
SELECT COUNT(*) FROM `spatial-encoder-432509-n7.module_3_homework.m3_green_taxi`;
-------------------------------------------------------------------------------------------
-- Queries for Q2 
-- The estimated size of the data that will be read can be seen in the top right corner
-- after having a  query in a BQ query tab

-- Count distinct PULocationID in the External Table
SELECT COUNT(DISTINCT PULocationID) AS distinct_pulocations
FROM `spatial-encoder-432509-n7.module_3_homework.external_m3_green_taxi`;

-- Count distinct PULocationID in the Materialised Table
SELECT COUNT(DISTINCT PULocationID) AS distinct_pulocations
FROM `spatial-encoder-432509-n7.module_3_homework.m3_green_taxi`;
-------------------------------------------------------------------------------------------
-- Query for Q3
SELECT COUNT(*) AS zero_fare_records
FROM `spatial-encoder-432509-n7.module_3_homework.m3_green_taxi`
WHERE fare_amount = 0;
-------------------------------------------------------------------------------------------
-- Query for Q4
-- Create a new table partitioned by lpep_pickup_datetime and clustered on PULocationID
CREATE OR REPLACE TABLE `spatial-encoder-432509-n7.module_3_homework.partitioned_clustered_green_taxi`
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PULocationID AS
SELECT *
FROM `spatial-encoder-432509-n7.module_3_homework.m3_green_taxi`;
-------------------------------------------------------------------------------------------
--Queries for Q5
-- Estimated size of data to be read can be inferred the same way as in Q2.

--Query for distinct PULocationID between 06/01/2022 and 06/30/2022 in the Materialized Table
SELECT DISTINCT PULocationID
FROM `spatial-encoder-432509-n7.module_3_homework.m3_green_taxi`
WHERE lpep_pickup_datetime BETWEEN '2022-06-01' AND '2022-06-30';

--Query for distinct PULocationID between 06/01/2022 and 06/30/2022 in the Partitioned and Clustered table
SELECT DISTINCT PULocationID
FROM `spatial-encoder-432509-n7.module_3_homework.partitioned_clustered_green_taxi`
WHERE lpep_pickup_datetime BETWEEN '2022-06-01' AND '2022-06-30';


