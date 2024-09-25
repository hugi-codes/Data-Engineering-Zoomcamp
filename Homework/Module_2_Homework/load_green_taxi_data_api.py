# This script is the data loader block in the Mage pipeline

import io
import pandas as pd
import requests

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    
    # url links for month 10, 11 and 12 of 2020, respectively (final quarter)
    url_green_10 = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-10.csv.gz'

    url_green_11 = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-11.csv.gz' 

    url_green_12 = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-12.csv.gz'

    # List of urls
    download_urls = [url_green_10, url_green_11, url_green_12]

    # Initialize an empty DataFrame
    final_df = pd.DataFrame()
    
    taxi_dtypes = {
                    'VendorID': pd.Int64Dtype(),
                    'passenger_count': pd.Int64Dtype(),
                    'trip_distance': float,
                    'RatecodeID':pd.Int64Dtype(),
                    'store_and_fwd_flag':str,
                    'PULocationID':pd.Int64Dtype(),
                    'DOLocationID':pd.Int64Dtype(),
                    'payment_type': pd.Int64Dtype(),
                    'fare_amount': float,
                    'extra':float,
                    'mta_tax':float,
                    'tip_amount':float,
                    'tolls_amount':float,
                    'improvement_surcharge':float,
                    'total_amount':float,
                    'congestion_surcharge':float
                }
   # native date parsing 
    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    for url in download_urls:
        temp_df = pd.read_csv(
                    url, 
                    sep=',',
                    dtype=taxi_dtypes, 
                    compression = "gzip",
                    parse_dates = parse_dates
                )
        final_df = pd.concat([final_df, temp_df], ignore_index=True)  # Append to final_df

    print(final_df.shape) # provides answer to question 1

    return final_df
