import os 
import pandas as pd
import papermill as pm
import json
import nbformat
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def run_notebook(**kwargs):
    input_notebook= '/home/user/airflow/dags/data_clean.ipynb'
    output_notebook='/home/user/airflow/dags/data_clean_2.ipynb'
    pm.execute_notebook(
        input_notebook,output_notebook,kernel_name='python3'
    )

    return output_notebook
    

def extract_first_5_rows(**kwargs):
    # Path to the JSON file saved by the notebook
    json_path = '/home/user/airflow/dags/result.json'
    
    # Read the cleaned data from JSON file
    cleaned_df = pd.read_json(json_path)
    
    # Get the first 5 rows of the cleaned DataFrame
    first_5_rows = cleaned_df.head().to_json(orient='records')
    
    # Return the first 5 rows
    return first_5_rows


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG(
    'run_notebook_and_return_first_5_rows',
    default_args=default_args,
    description='A DAG to run a Jupyter Notebook using papermill and return the first 5 rows of cleaned data',
    schedule_interval=None,
    catchup=False,
)

# Define the task to run the notebook
run_notebook_task = PythonOperator(
    task_id='run_notebook_task',
    python_callable=run_notebook,
    provide_context=True,  # Allows passing of Airflow context
    dag=dag,
)

# Define the task to print the first 5 rows
print_first_5_rows_task = PythonOperator(
    task_id='print_first_5_rows_task',
    python_callable=extract_first_5_rows,
    provide_context=True,  # Allows passing of Airflow context
    dag=dag,
)

# Set task dependencies
run_notebook_task >> print_first_5_rows_task