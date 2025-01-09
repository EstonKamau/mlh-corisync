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
    'mlh_production_pipeline',
    default_args=default_args,
    description='Run dbt models in aptic_dbt folder',
    schedule_interval='*/20 * * * *',  # Runs every 20 minutes
    catchup=False,  
) as dag:

    # Task to run dlt pipeline
    run_production_dlt_pipeline = BashOperator(
        task_id='run_production_dlt_pipeline',
        bash_command='cd /opt/airflow/dags && python3 production_pipeline.py',
    )

    # Task to dbt
    run_production_dbt_models = BashOperator(
        task_id='run_production_dbt_models',
        bash_command='cd /opt/airflow/dags/corisync_dbt && dbt run --vars \'{"etl_schema": "mlh_etl_production"}\' --profiles-dir profile --target prod',
    )

    # Define task dependencies
    run_production_dlt_pipeline >> run_production_dbt_models
