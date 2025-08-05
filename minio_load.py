import boto3
import os

def upload_to_minio(bucket_name, local_folder, minio_url, access_key, secret_key):
    """
    Uploads files from a local folder to a Minio bucket.

    Args:
        bucket_name (str): The name of the Minio bucket.
        local_folder (str): The local directory containing files to upload.
        minio_url (str): The URL of the Minio service.
        access_key (str): The Minio access key.
        secret_key (str): The Minio secret key.
    """
    s3_client = boto3.client(
        's3',
        endpoint_url=minio_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=None,
        config=boto3.session.Config(signature_version='s3v4'),
        verify=False
    )

    # Create bucket if it doesn't exist
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except:
        s3_client.create_bucket(Bucket=bucket_name)

    # Upload files
    for filename in os.listdir(local_folder):
        if filename.endswith('.csv'):
            local_path = os.path.join(local_folder, filename)
            s3_client.upload_file(local_path, bucket_name, filename)
            print(f"Uploaded {filename} to {bucket_name}")

if __name__ == "__main__":
    # ... (previous data generation code) ...

    # Minio Configuration
    MINIO_BUCKET = 'raw-data'
    MINIO_URL = 'http://localhost:9000'
    MINIO_ACCESS_KEY = 'minioadmin'
    MINIO_SECRET_KEY = 'minioadmin'

    upload_to_minio(MINIO_BUCKET, 'synthetic_data', MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY)