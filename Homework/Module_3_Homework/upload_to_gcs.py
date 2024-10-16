# Import packages
import requests
from google.cloud import storage
from io import BytesIO

# Defining function to upload parquet file to GCS bucket using download URL
def upload_to_gcs_from_url(bucket_name, destination_blob_name, file_url):
    """Downloads a file from a URL and uploads it directly to GCS."""
    
    # Initialize a GCS client
    storage_client = storage.Client()
    
    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    
    # Create a new blob (object) in the bucket
    blob = bucket.blob(destination_blob_name)

    # Stream the file from the URL
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        # Upload the file content directly from the stream
        blob.upload_from_file(BytesIO(response.content), content_type="application/octet-stream")
        print(f"File streamed and uploaded to {bucket_name}/{destination_blob_name}")
    else:
        raise Exception(f"Failed to download file: {response.status_code}")

# Main script to handle files for all months of 2022
if __name__ == "__main__":
    # The GCS bucket name
    BUCKET_NAME = "module-3-homework"
    
    # Loop through months 01 to 12
    for month in range(1, 13):
        # Format the month to two digits (e.g., 01, 02, ..., 12)
        month_str = f"{month:02d}"
        
        # Generate the file URL for the current month
        file_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-{month_str}.parquet"
        
        # Generate the destination blob name for the current month
        destination_blob_name = f"green_tripdata_2022-{month_str}.parquet"
        
        # Upload the file directly from the URL to GCS
        print(f"Starting upload for {destination_blob_name}")
        upload_to_gcs_from_url(BUCKET_NAME, destination_blob_name, file_url)
        print(f"Completed upload for {destination_blob_name}\n")
