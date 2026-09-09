import os
import requests
import json
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.models import Variable
import boto3

# Default arguments for Airflow
default_args = {
    'owner': 'ahmer',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Python function: API se data uthana aur S3 mein upload karna
def extract_and_load_to_s3():
    # 1. API Call
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url, timeout=30)
    data = response.json()
    
    # 2. S3 Connection (Airflow Variables se credentials)
    s3 = boto3.client(
        's3',
        aws_access_key_id=Variable.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=Variable.get('AWS_SECRET_KEY')
    )
    
    # 3. File ko S3 bucket mein upload karna
    bucket_name = 'opensky-bronze-ahmer-2026'
    file_name = f"raw/opensky_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(data)
    )

# DAG Definition
with DAG(
    'opensky_medallion_pipeline',
    default_args=default_args,
    schedule_interval='@hourly',
    start_date=datetime(2026, 9, 8),
    catchup=False,
    template_searchpath=['/opt/airflow/dags'] # Ab sql folder dags ke andar hai, isliye yeh path zaroori hai
) as dag:

    # Task 1: Python Operator jo API se data fetch karke S3 pe daalega
    fetch_data = PythonOperator(
        task_id='fetch_opensky_api_to_s3',
        python_callable=extract_and_load_to_s3
    )

    # Task 2: Bronze Layer (S3 se Snowflake Raw Table)
    bronze_layer = SnowflakeOperator(
        task_id='run_bronze_layer',
        snowflake_conn_id='snowflake_default',
        sql='sql/02_bronze_layer.sql'
    )

    # Task 3: Silver Layer (Raw JSON ko parse kar ke Clean Table)
    silver_layer = SnowflakeOperator(
        task_id='run_silver_layer',
        snowflake_conn_id='snowflake_default',
        sql='sql/03_silver_layer.sql'
    )

    # Task 4: Gold Layer (Analytics & Aggregation Table)
    gold_layer = SnowflakeOperator(
        task_id='run_gold_layer',
        snowflake_conn_id='snowflake_default',
        sql='sql/04_gold_layer.sql'
    )

    # Pipeline ka Sequence
    fetch_data >> bronze_layer >> silver_layer >> gold_layer