# Use an Airflow image with Python 3.10
FROM ubuntu:latest
FROM apache/airflow:2.10.2-python3.10

# Set environment variables
ENV AIRFLOW__CORE__EXECUTOR=CeleryExecutor
ENV AIRFLOW__METRICS__STATSD_HOST=prometheus
ENV AIRFLOW__METRICS__STATSD_PORT=8125
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5437/airflow
ENV AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres:5437/airflow

# Install additional Python packages using pip
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install prometheus_client


# Copy the metrics.ini file
COPY metrics.ini /opt/airflow/metrics.ini

# Copy DAGs and other configurations
COPY ./dags /opt/airflow/dags

# Install StatsD client library
RUN pip3 install statsd

# Copy the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY init_config.sh /usr/local/bin/init_config.sh


# Ensure permissions are set properly
USER airflow

# Set the entrypoint to the custom script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh","/usr/local/bin/init_config.sh"]