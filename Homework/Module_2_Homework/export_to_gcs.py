import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.fs as fs
import os 
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


# Set the environment variable for Google Cloud authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/src/spatial-encoder-432509-n7-10f9ce9209ed.json"

bucket_name = 'mage-zoomcamp-tim'
table_name = "green_nyc_taxi_data"
root_path = f'{bucket_name}/{table_name}'  # GCS path should be bucket name followed by the object key

@data_exporter
def export_data(data, *args, **kwargs):
    
    # Create a PyArrow table from the DataFrame
    table = pa.Table.from_pandas(data)
    
    # Initialize Google Cloud Storage filesystem (credentials are automatically read from environment)
    gcs = fs.GcsFileSystem()  # No need to pass credentials here
    
    # Write the PyArrow table to GCS as Parquet dataset with partitioning
    pq.write_to_dataset(
        table,
        root_path=root_path,           # GCS bucket and table name path
        partition_cols=["lpep_pickup_date"],  # Partition by 'lpep_pickup_date'
        filesystem=gcs                 # GCS filesystem instance
    )