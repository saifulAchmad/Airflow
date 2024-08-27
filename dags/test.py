from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 21),
    'email_on_failure': False,
    'email_on_retry': False,
}

# Define the DAG
dag = DAG(
    'simple_dag',
    default_args=default_args,
    description='A simple DAG',
    schedule_interval=timedelta(days=1),  
)

# Define the tasks
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    dag=dag,
)

t3 = BashOperator(
    task_id='print_hello',
    bash_command='echo "Hello World"',
    dag=dag,
)

# Set the task dependencies
t1 >> t2 >> t3