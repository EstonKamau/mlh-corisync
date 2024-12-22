
# Airflow with Docker Compose, Loki, StatsD, Prometheus, and Grafana

This folder contains a setup for running Apache Airflow in Docker Compose, along with monitoring and logging using Loki, StatsD, Prometheus, and Grafana.

---

## Folder Structure

```
.
├── docker-compose.yml  # Defines services for Airflow, Loki, StatsD, Prometheus, and Grafana
├── dags/               # Directory for Airflow DAGs
├── Dockerfile 
├── entrypoint.sh       # Airflow entry point
├── init-config.yaml         
├── loki-config              # Configuration file for Loki
├── prometheus.yml         # Configuration file for Prometheus
├── promtail-config.yaml
├── statsd_mapping.yml
├── requirements.txt         
└── README.md           # Documentation for the setup
```

---

## Components

1. **Airflow**: Workflow orchestration tool for managing data pipelines.
2. **Loki**: Centralized logging system for Airflow and other services.
3. **StatsD**: Collects metrics from Airflow and sends them to Prometheus.
4. **Prometheus**: Time-series database for monitoring metrics.
5. **Grafana**: Dashboard and visualization tool for logs and metrics.

---

## Prerequisites

- Install [Docker](https://www.docker.com/products/docker-desktop).
- Install [Docker Compose](https://docs.docker.com/compose/install/).
- At least 4GB of free memory for running the services.

---

## Usage

### 1. **Start Services**
Navigate to the folder containing the `docker-compose.yml` file and run:
```bash
docker-compose up -d
```

### 2. **Access the Services**
- **Airflow Web UI**: [http://localhost:8080](http://localhost:8080)
  - Default credentials: `airflow` / `airflow`
- **Grafana**: [http://localhost:3000](http://localhost:3000)
  - Default credentials: `admin` / `admin`
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Loki Logs** (via Grafana Explore): [http://localhost:3000/explore](http://localhost:3000/explore)

### 3. **Add DAGs**
Place your DAG files in the `dags/` folder. Airflow will automatically detect them.

### 4. **Monitoring**
- Use **Grafana Dashboards** to visualize metrics collected by Prometheus and logs collected by Loki.
- Pre-configured dashboards can be found in the `grafana/` folder.

### 5. **Stop Services**
To stop all services, run:
```bash
docker-compose down
```

---

## Configuration Details

- **Airflow Logs**: Logs are routed to Loki for centralized log management.
- **StatsD**: Metrics from Airflow are sent to StatsD and scraped by Prometheus.
- **Prometheus Configuration**:
  - Config files are stored in the `prometheus/` folder.
  - Scrapes metrics from StatsD and other services.
- **Grafana Dashboards**:
  - Dashboards are automatically provisioned from the `grafana/` folder.
- **Loki Configuration**:
  - Loki config files are in the `loki/` folder.

---

## Troubleshooting

1. **Check Logs**:
   - To view logs for all services:
     ```bash
     docker-compose logs -f
     ```

2. **Airflow Issues**:
   - Ensure DAGs are placed in the `dags/` folder.
   - Restart Airflow services if DAGs are not detected:
     ```bash
     docker-compose restart airflow-scheduler
     ```

3. **Grafana Login Issue**:
   - Reset password by accessing the `grafana` container:
     ```bash
     docker exec -it <grafana_container_name> grafana-cli admin reset-admin-password <new_password>
     ```

---

## References

- [Apache Airflow Documentation](https://airflow.apache.org/)
- [Loki Documentation](https://grafana.com/oss/loki/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/).