#!/bin/bash
set -e

# Move sql_alchemy_conn from [core] to [database]
if grep -q '^\[core\]' /opt/airflow/airflow.cfg; then
    sed -i '/^\[core\]/,/^\[/{/sql_alchemy_conn/s/^\(sql_alchemy_conn.*\)/\1/;s/^\(sql_alchemy_conn.*\)/#\1/}' /opt/airflow/airflow.cfg
    echo -e '\n[database]\nsql_alchemy_conn = postgresql+psycopg2://airflow:airflow@postgres:5437/airflow' >> /opt/airflow/airflow.cfg
fi