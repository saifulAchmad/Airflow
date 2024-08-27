from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sqlite3

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'sqlite_query_dag',
    default_args=default_args,
    description='A DAG to query SQLite database',
    schedule_interval=timedelta(days=1),
)

# Define the Python function to query SQLite
def query_sqlite_users():
    # Path to your SQLite database
    db_path = 'test.db'
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute the SQL query
    cursor.execute("SELECT * FROM user")
    
    # Fetch all rows and print them
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    # Close the connection
    conn.close()

# Create a PythonOperator to run the query
run_sqlite_query = PythonOperator(
    task_id='query_sqlite_users',
    python_callable=query_sqlite_users,
    dag=dag,
)

# Set the task dependencies (only one task here)
run_sqlite_query
