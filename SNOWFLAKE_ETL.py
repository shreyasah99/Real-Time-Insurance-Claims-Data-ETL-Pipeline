from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from io import StringIO
from airflow.hooks.S3_hook import S3Hook
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from dotenv import load_dotenv
import os
import zipfile
import random
from datetime import datetime

# Load environment variables from .env file


def load_random_sample(csv_file, sample_size):

    # Count total rows in the CSV file
    total_rows = sum(1 for line in open(csv_file, encoding='utf-8')) - 1 # Subtract header row

    # Calculate indices of rows to skip (non-selected)
    skip_indices = random.sample(range(1, total_rows + 1), total_rows - sample_size)

    # Load DataFrame with random sample of rows
    df = pd.read_csv(csv_file, skiprows=skip_indices)

    policy_table = df[['policy_id', 'subscription_length', 'region_code', 'segment']]
    vehicles_table = df[['policy_id', 'vehicle_age', 'fuel_type', 'is_parking_sensors', 'is_parking_camera', 'rear_brakes_type', 'displacement', 'transmission_type', 'steering_type', 'turning_radius', 'gross_weight', 'is_front_fog_lights', 'is_rear_window_wiper', 'is_rear_window_washer', 'is_rear_window_defogger', 'is_brake_assist', 'is_central_locking', 'is_power_steering', 'is_day_night_rear_view_mirror', 'is_speed_alert', 'ncap_rating']]
    customers_table = df[['policy_id', 'customer_age', 'region_density']]
    claims_table = df[['policy_id', 'claim_status']]

    vehicles_table.rename(columns ={'policy_id':'vehicle_id'}, inplace = True)
    customers_table.rename(columns ={'policy_id':'customer_id'}, inplace = True)
    claims_table.rename(columns ={'policy_id':'claim_id'}, inplace = True)

    return policy_table, vehicles_table, customers_table, claims_table


def upload_df_to_s3(**kwargs):
    
    load_dotenv()

    # Setup Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Define the dataset
    dataset = 'litvinenko630/insurance-claims'

    # Define the CSV file name
    csv_file = 'Insurance claims data.csv'

    # Download the entire dataset as a zip file
    api.dataset_download_files(dataset, path='.')

    # Extract the CSV file from the downloaded zip file
    with zipfile.ZipFile('insurance-claims.zip', 'r') as zip_ref:
        zip_ref.extract(csv_file, path='.')

    policy_data, vehicles_data, customers_data, claims_data = load_random_sample(csv_file, 20)
    # Convert DataFrame to CSV string
    policy = policy_data.to_csv(index=False)
    vehicles = vehicles_data.to_csv(index=False)
    customers = customers_data.to_csv(index=False)
    claims = claims_data.to_csv(index=False)
    s3_hook = S3Hook(aws_conn_id='aws-default')
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Define S3 bucket and keys with current date and time
    s3_bucket = 'insurance-data-snowflake-etl-project'
    s3_key_policy = f'policy/policy_{current_datetime}.csv'
    s3_key_vehicles = f'vehicles/vehicles_{current_datetime}.csv'
    s3_key_customers = f'customers/customers_{current_datetime}.csv'
    s3_key_claims = f'claims/claims_{current_datetime}.csv'
    

    s3_hook.load_string(policy, key=s3_key_policy, bucket_name=s3_bucket)
    s3_hook.load_string(vehicles, key=s3_key_vehicles, bucket_name=s3_bucket)
    s3_hook.load_string(customers, key=s3_key_customers, bucket_name=s3_bucket)
    s3_hook.load_string(claims, key=s3_key_claims, bucket_name=s3_bucket)




# Load random sample of 1000 rows into DataFrame
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1)}

with DAG(
    'INSURANCE_DATA_ETL',
    default_args=default_args,
    description='EXTRACT insurance data from Kagle, normalize data and push to S3',
    schedule_interval=None,
    catchup = False) as dag:

# Tash to check if the api is ready
    is_api_available = HttpSensor(
            task_id ='is_API_available',
            http_conn_id='http-api_kaggle',
            endpoint='',
            )
    
# Task to extract and upload API data to S3 and push S3 path to XCom fro reference
    upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_df_to_s3,
        dag=dag,
        )

is_api_available >> upload_to_s3 