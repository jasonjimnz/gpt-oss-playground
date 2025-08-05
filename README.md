# GPT Data Analytics Platform

A comprehensive data analytics platform for generating, storing, and analyzing synthetic banking and e-commerce data. This project provides a complete environment with PostgreSQL for data storage, MinIO for object storage, Apache Superset for visualization, and Dremio for data warehousing.

## Overview

This project includes:

1. **Data Generation**: Python scripts to create synthetic banking and e-commerce data
2. **Database Schema**: SQL schema for banking and e-commerce services
3. **Data Storage**: PostgreSQL database and MinIO object storage
4. **Analytics**: BI queries and visualization tools (Apache Superset)
5. **Data Warehouse**: Dremio for advanced analytics

## Prerequisites

- Docker and Docker Compose
- Python 3.6+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd gptdata
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Start the Docker containers:
   ```
   docker-compose up -d
   ```

## Usage

### 1. Generate Synthetic Data

Generate synthetic banking and e-commerce data:

```
python data_generation.py
```

This will create CSV files in the `synthetic_data` directory.

### 2. Load Database Schema

Load the schema into PostgreSQL:

```
python load_schema.py
```

### 3. Upload Data to MinIO

Upload the generated data to MinIO:

```
python minio_load.py
```

This uploads all CSV files from the `synthetic_data` directory to the MinIO bucket 'raw-data'. The script uses these default credentials:
- MinIO URL: http://localhost:9000
- Access Key: minioadmin
- Secret Key: minioadmin

Note: If you need to modify these settings, edit the values in minio_load.py.

### 4. Load Data from MinIO to PostgreSQL

Load the data from MinIO into PostgreSQL:

```
python load_data_from_minio.py
```

This script:
1. Connects to MinIO and PostgreSQL services
2. Ensures the database schema is loaded
3. Reads CSV files from MinIO
4. Loads the data into corresponding PostgreSQL tables

The script uses these default credentials:
- PostgreSQL: host=localhost, port=5432, user=postgres, password=postgres, database=banking_db
- MinIO: url=http://localhost:9000, access_key=minioadmin, secret_key=minioadmin

### 5. Access Analytics Tools

After setting up the data, you can access the analytics tools:

- **Apache Superset**: http://localhost:8088
  - Default credentials: admin/admin
  - Connect to PostgreSQL database
  - Import BI queries from the `bi_queries` directory

- **MinIO Console**: http://localhost:9001
  - Credentials: minioadmin/minioadminpassword

- **Dremio**: http://localhost:9047
  - Set up during first login

### 5. Run BI Queries

The `bi_queries` directory contains SQL queries for various analytics:

- Banking analytics:
  - `banking_monthly_deposits.sql`: Monthly deposit trends
  - `banking_net_movement.sql`: Net cash flow
  - `banking_top_5_withdrawals.sql`: Top 5 withdrawals

- E-commerce analytics:
  - `ecommerce_inventory_alert.sql`: Low inventory alerts
  - `ecommerce_monthly_revenue.sql`: Monthly revenue
  - `ecommerce_top_10_products.sql`: Top 10 selling products

- Aggregated analytics:
  - `agg_customer_ltv.sql`: Customer lifetime value
  - `agg_marketing_roi.sql`: Marketing ROI
  - `agg_revenue_per_customer.sql`: Revenue per customer

## Project Structure

```
gptdata/
├── bi_queries/                # Business Intelligence SQL queries
├── ddl/
│   └── schema.sql            # Database schema definition
├── data_generation.py        # Script to generate synthetic data
├── docker-compose.yml        # Docker configuration
├── load_schema.py            # Script to load schema into PostgreSQL
├── load_data_from_minio.py   # Script to load data from MinIO to PostgreSQL
├── minio_load.py             # Script to upload data to MinIO
├── requirements.txt          # Python dependencies
├── superset_config.py        # Apache Superset configuration
└── synthetic_data/           # Directory containing generated CSV files
```

## Workflow

1. Generate synthetic data with `data_generation.py`
2. Load the database schema with `load_schema.py`
3. Upload data to MinIO with `minio_load.py`
4. Load data from MinIO to PostgreSQL with `load_data_from_minio.py`
5. Access Apache Superset or Dremio to run analytics queries
6. Use the BI queries in the `bi_queries` directory for analysis