"""
Script to load data from MinIO into PostgreSQL database.

This script:
1. Connects to MinIO and PostgreSQL services
2. Ensures the database schema is loaded
3. Reads CSV files from MinIO in the correct order based on schema dependencies
4. Loads the data into corresponding PostgreSQL tables

Usage:
    1. Make sure the Docker containers are running:
       docker-compose up -d
    
    2. Run minio_load.py to upload data to MinIO:
       python minio_load.py
    
    3. Run this script to load data from MinIO to PostgreSQL:
       python load_data_from_minio.py

Dependencies:
    - boto3: For MinIO/S3 operations
    - pandas: For data manipulation
    - psycopg2: For PostgreSQL operations

Note:
    Tables are loaded in a specific order to respect foreign key constraints.
    The order is defined based on the table creation sequence in schema.sql.
"""

import boto3
import pandas as pd
import psycopg2
import io
import os
from psycopg2 import sql

def connect_to_minio(minio_url, access_key, secret_key):
    """
    Connect to MinIO and return the S3 client.
    
    Args:
        minio_url (str): The URL of the MinIO service.
        access_key (str): The MinIO access key.
        secret_key (str): The MinIO secret key.
        
    Returns:
        boto3.client: The S3 client connected to MinIO.
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
    return s3_client

def connect_to_postgres(host, port, user, password, database):
    """
    Connect to PostgreSQL and return the connection.
    
    Args:
        host (str): The host of the PostgreSQL service.
        port (int): The port of the PostgreSQL service.
        user (str): The username for PostgreSQL.
        password (str): The password for PostgreSQL.
        database (str): The database name.
        
    Returns:
        psycopg2.connection: The PostgreSQL connection.
    """
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    return conn

def get_table_name_from_filename(filename):
    """
    Extract table name from filename.
    
    Args:
        filename (str): The filename.
        
    Returns:
        str: The table name.
    """
    # Remove file extension and return
    return os.path.splitext(filename)[0]

def load_data_to_postgres(conn, table_name, df):
    """
    Load data from DataFrame to PostgreSQL table.
    
    Args:
        conn (psycopg2.connection): The PostgreSQL connection.
        table_name (str): The name of the table to load data into.
        df (pd.DataFrame): The DataFrame containing the data.
        
    Returns:
        int: The number of rows inserted.
    """
    # Create a cursor
    cursor = conn.cursor()
    
    # Get column names from DataFrame
    columns = df.columns.tolist()
    
    # Create placeholders for values
    placeholders = ', '.join(['%s'] * len(columns))
    
    # Create the INSERT query
    insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(placeholders)
    )
    
    # Convert DataFrame to list of tuples and handle NaT values
    rows = []
    for row in df.values:
        # Replace NaT values with None (which becomes NULL in PostgreSQL)
        # Convert numpy.float64 to Python float to avoid passing direct NumPy type references
        processed_row = [None if pd.isna(val) or (hasattr(val, 'is_nat') and val.is_nat) 
                        else float(val) if hasattr(val, 'dtype') and 'float' in str(val.dtype) 
                        else val for val in row]
        rows.append(tuple(processed_row))
    
    # Execute the query for each row
    cursor.executemany(insert_query, rows)
    
    # Commit the transaction
    conn.commit()
    
    # Close the cursor
    cursor.close()
    
    return len(rows)

def ensure_schema_loaded(conn):
    """
    Ensure the database schema is loaded.
    
    Args:
        conn (psycopg2.connection): The PostgreSQL connection.
    """
    try:
        # Check if tables exist by querying information_schema
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        table_count = cursor.fetchone()[0]
        
        # If no tables exist, load the schema
        if table_count == 0:
            print("No tables found. Loading schema...")
            with open('./ddl/schema.sql', encoding='utf-8') as f:
                schema_sql = f.read()
                cursor.execute(schema_sql)
                conn.commit()
                print("Schema loaded successfully.")
        else:
            print(f"Found {table_count} existing tables. Schema already loaded.")
        
        cursor.close()
    except Exception as e:
        print(f"Error ensuring schema is loaded: {e}")
        raise

def main():
    """
    Main function to run the script.
    """
    # MinIO Configuration
    MINIO_BUCKET = 'raw-data'
    MINIO_URL = 'http://localhost:9000'
    MINIO_ACCESS_KEY = 'minioadmin'
    MINIO_SECRET_KEY = 'minioadmin'  # Using the correct password from docker-compose.yml
    
    # PostgreSQL Configuration
    PG_HOST = 'localhost'
    PG_PORT = 5432
    PG_USER = 'postgres'
    PG_PASSWORD = 'postgres'
    PG_DATABASE = 'banking_db'
    
    # Connect to MinIO
    s3_client = connect_to_minio(MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY)
    
    # Connect to PostgreSQL
    pg_conn = connect_to_postgres(PG_HOST, PG_PORT, PG_USER, PG_PASSWORD, PG_DATABASE)
    
    # Ensure schema is loaded
    ensure_schema_loaded(pg_conn)
    
    try:
        # Check if bucket exists
        try:
            s3_client.head_bucket(Bucket=MINIO_BUCKET)
            print(f"Bucket '{MINIO_BUCKET}' exists.")
        except:
            print(f"Bucket '{MINIO_BUCKET}' does not exist. Creating it...")
            s3_client.create_bucket(Bucket=MINIO_BUCKET)
            print(f"Bucket '{MINIO_BUCKET}' created.")
            print("Please run minio_load.py first to upload data to MinIO, then run this script again.")
            return
        
        # Define the order of tables to load based on schema.sql dependencies
        table_order = [
            'bank_customer',
            'bank_account',
            'bank_transaction',
            'ecommerce_customer',
            'ecommerce_address',
            'product_category',
            'ecommerce_product',
            'ecommerce_order',
            'ecommerce_order_item',
            'analytics_customer',
            'analytics_fct_banking',
            'analytics_fct_order',
            'analytics_fct_order_item',
            'marketing_campaign'
        ]
        
        # List objects in the bucket
        response = s3_client.list_objects_v2(Bucket=MINIO_BUCKET)
        
        if 'Contents' in response:
            # Create a list to store files by table name

            files_by_table = [
                ("0_bank_customer.csv", "bank_customer"),
                ("1_bank_account.csv", "bank_account"),
                ("2_bank_transaction.csv", "bank_transaction"),
                ("3_ecommerce_customer.csv", "ecommerce_customer"),
                ("4_ecommerce_address.csv", "ecommerce_address"),
                ("5_product_category.csv", "product_category"),
                ("6_ecommerce_product.csv", "ecommerce_product"),
                ("7_ecommerce_order.csv", "ecommerce_order"),
                ("8_ecommerce_order_item.csv", "ecommerce_order_item"),
                ("9_marketing_campaign.csv", "marketing_campaign")
            ]
            # Second pass: process files in the correct order
            for filename, table_name in files_by_table:

                print(f"Processing {filename} for table {table_name}...")
                # Get the object from MinIO
                obj_response = s3_client.get_object(Bucket=MINIO_BUCKET, Key=filename)

                # Read the CSV data into a DataFrame
                csv_content = obj_response['Body'].read()
                df = pd.read_csv(io.BytesIO(csv_content))

                # Handle data type conversions based on table name
                if table_name in ['bank_customer', 'ecommerce_customer']:
                    # Convert date columns
                    if 'date_of_birth' in df.columns:
                        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce').dt.date
                    if 'created_at' in df.columns:
                        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

                elif table_name in ['bank_account', 'ecommerce_order']:
                    # Convert date columns
                    if 'opened_at' in df.columns:
                        df['opened_at'] = pd.to_datetime(df['opened_at'], errors='coerce')
                    if 'closed_at' in df.columns:
                        # Handle NaN values in closed_at
                        df['closed_at'] = pd.to_datetime(df['closed_at'], errors='coerce')
                    if 'order_date' in df.columns:
                        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

                elif table_name == 'bank_transaction':
                    # Convert transaction_date
                    if 'transaction_date' in df.columns:
                        df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')

                elif table_name == 'marketing_campaign':
                    # Convert month to date
                    if 'month' in df.columns:
                        df['month'] = pd.to_datetime(df['month'], errors='coerce').dt.date

                # Load the data into PostgreSQL
                try:
                    rows_inserted = load_data_to_postgres(pg_conn, table_name, df)
                    print(f"Loaded {rows_inserted} rows into {table_name} table.")
                except Exception as e:
                    print(f"Error loading data into {table_name}: {e}")
                    # Continue with next file instead of stopping the entire process
                    continue
        else:
            print(f"No objects found in the {MINIO_BUCKET} bucket.")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close the PostgreSQL connection
        if pg_conn:
            pg_conn.close()

if __name__ == "__main__":
    main()