import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sqlite3
import os

def comb_col():
    home_dir= os.path.expanduser('~')
    db_path= os.path.join(home_dir,'airflow','test.db')

    conn = sqlite3.connect(db_path)

    df=pd.read_sql_query("select * from user",conn)

    df['combined']= df['id'].astype(str) + df['name'].astype(str)
    
    df.to_sql('transformed_table', conn, if_exists='replace', index=False)
    combined_data = df.to_dict(orient='records')
    conn.close()
    return combined_data


def print_combined_data(**kwargs):
    # Retrieve the combined data using XCom
    ti = kwargs['ti']
    combined_data = ti.xcom_pull(task_ids='combine_columns')
    
    # Print the combined data or process it as needed
    print("Combined Data:", combined_data)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
}

dag = DAG(
    'combine_columns_dag',
    default_args=default_args,
    description='A simple DAG to combine columns a and b from an SQLite table using Pandas',
    schedule_interval=None,
    catchup=False,
    max_active_runs=1
)


# Define the task using PythonOperator
combine_columns_task = PythonOperator(
    task_id='combine_columns',
    python_callable=comb_col,
    dag=dag,
)


print_combined_data_task = PythonOperator(
    task_id='print_combined_data',
    python_callable=print_combined_data,
    provide_context=True,  # Enables passing the context to the function
    dag=dag,
)

combine_columns_task >> print_combined_data_task