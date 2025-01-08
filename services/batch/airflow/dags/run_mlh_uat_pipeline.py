from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# Define default args
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'retries': 1,
}

# Define the DAG
with DAG(
    'mlh_uat_pipeline',
    default_args=default_args,
    description='Run dbt models in aptic_dbt folder',
    schedule_interval='*/20 * * * *',  # Runs every 20 minutes
    catchup=False,  
) as dag:

    # Task to run dbt
    run_dlt_pipeline = BashOperator(
        task_id='run_dlt_pipeline',
        bash_command='cd /opt/airflow/dags && python3 uat_pipeline.py',
    )

    # Task to test dbt
    run_dbt_models = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /opt/airflow/dags/corisync_dbt && dbt run --profiles-dir profile --target dev',
    )

    # Define task dependencies
    run_dlt_pipeline >> run_dbt_models
