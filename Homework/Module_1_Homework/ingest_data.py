#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name_1 = params.table_name_1
    table_name_2 = params.table_name_2
    url_1 = params.url_1
    url_2 = params.url_2
    
    # ===================================================================================================
    # Info on the urls (which are the download links for the data)
    # url_1:
    # https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz
    # --> Contains data about taxi trips
    
    # url_2:
    # https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
    # --> Contains data about taxi zones
    # ===================================================================================================

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Reading the data in chunks of 100000
    df_iter = pd.read_csv(url_1, iterator=True, chunksize=100000, compression= "gzip")

    df = next(df_iter)

    # Applying some prepprocessing
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    # Ingesting the data into postgres 
    df.head(n=0).to_sql(name=table_name_1, con=engine, if_exists='replace')

    df.to_sql(name=table_name_1, con=engine, if_exists='append')


    while True: 

        try:
            t_start = time()
            
            df = next(df_iter)

            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            df.to_sql(name=table_name_1, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting taxi trip data into the postgres database")
            break


    # Ingesting taxi zone data 
    df_taxi_zones = pd.read_csv(url_2)

    df_taxi_zones.to_sql(name = table_name_2, con = engine, if_exists='replace')

    print("Finished ingesting taxi zone data into the postgres database")

# We want dockerise this script (run it as a docker container). For this we also created a Dockerfile
# which we will use to build the docker image. This docker file is in the same directory as this script.
# The code chunk below enable docker to run this script as soon as the container is started

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name_1', required=True, help='name of the first table where we will write the results to')
    parser.add_argument('--table_name_2', required=True, help='name of the second table where we will write the results to')
    parser.add_argument('--url_1', required=True, help='url of the first csv file')
    parser.add_argument('--url_2', required=True, help='url of the second csv file')


    args = parser.parse_args()

    main(args)
