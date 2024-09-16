## Module 1 Homework

ATTENTION: At the very end of the submission form, you will be required to include a link to your GitHub repository or other public code-hosting site. This repository should contain your code for solving the homework. If your solution includes code that is not in file format (such as SQL queries or shell commands), please include these directly in the README file of your repository.

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm`

### **Answer:**  
The `--rm` tag has that text.

## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

- 0.44.0
- 1.0.0
- 23.0.1
- 58.1.0

### **Answer:**  
Executed ```docker run -it python:3.9 /bin/bash```.
Then executed ```pip list```. The answer is 0.44.0. 


# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15767
- 15612
- 15859
- 89009

### **Answer:**  
On September 18th 2019, 15612 taxi trips were made.

SQL query: 
```
SELECT COUNT(1) FROM green_taxi_trips
WHERE 1=1
  AND DATE(lpep_pickup_datetime) = '2019-09-18'
  AND DATE(lpep_dropoff_datetime) = '2019-09-18';
  ```


## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance?
Use the pick up time for your calculations.

Tip: For every trip on a single day, we only care about the trip with the longest distance. 

- 2019-09-18
- 2019-09-16
- 2019-09-26
- 2019-09-21

### **Answer:**  
The pick up day with the longest trip distance was 2019-09-26.

SQL query: 
```
SELECT DATE(lpep_pickup_datetime)
FROM green_taxi_trips
WHERE trip_distance = (SELECT MAX(trip_distance) FROM green_taxi_trips);
  ```


## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
- "Brooklyn" "Manhattan" "Queens"
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"

### **Answer:**  
The 3 pick up Boroughs that had a sum of total_amount superior to 50000 are
"Brooklyn" "Manhattan" "Queens".

SQL query: 
```
WITH modified_zones AS (
    SELECT zones."LocationID", zones."Borough" AS pick_up_borough
    FROM public.taxi_zones zones
    WHERE zones."Borough" != 'Unknown'
)
SELECT pick_up_borough, SUM(trips."total_amount") AS total_sum
FROM public.green_taxi_trips trips
JOIN modified_zones zones
    ON trips."PULocationID" = zones."LocationID"
WHERE DATE(trips.lpep_pickup_datetime) = '2019-09-18'
GROUP BY pick_up_borough
HAVING SUM(trips."total_amount") > 50000
ORDER BY total_sum DESC
LIMIT 3;
  ```


## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- JFK Airport
- Long Island City/Queens Plaza

### **Answer:**  
The answer is JFK Airport. 

SQL query: 
```
SELECT 
    tz2."Zone" AS DO_Zone
FROM 
    green_taxi_trips gtt
-- Join taxi_zones for Pickup Location
LEFT JOIN 
    taxi_zones tz1 
    ON gtt."PULocationID" = tz1."LocationID"
-- Join taxi_zones for Dropoff Location
LEFT JOIN 
    taxi_zones tz2 
    ON gtt."DOLocationID" = tz2."LocationID"
-- Filter for trips in September 2019 and Pickup Zone "Astoria"
WHERE 
    DATE(gtt."lpep_pickup_datetime") BETWEEN '2019-09-01' AND '2019-09-30'
    AND tz1."Zone" = 'Astoria'
-- Sort by largest tip_amount
ORDER BY 
    gtt."tip_amount" DESC
-- Limit to the row with the largest tip_amount
LIMIT 1;
  ```

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.

### **Answer:**  
This is the output after executing ```terraform apply```: 

```
terraform apply -var="project= spatial-encoder-432509-n7"

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "europe-west10-b"
      + max_time_travel_hours      = (known after apply)
      + project                    = "spatial-encoder-432509-n7"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)

      + access (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "terraform-demo-terra-bucket_1996_v7"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type          = "AbortIncompleteMultipartUpload"
                # (1 unchanged attribute hidden)
            }
          + condition {
              + age                    = 1
              + matches_prefix         = []
              + matches_storage_class  = []
              + matches_suffix         = []
              + with_state             = (known after apply)
                # (3 unchanged attributes hidden)
            }
        }

      + versioning (known after apply)

      + website (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value:

```


## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 29 January, 23:00 CET
