# Apache Spark Docker Compose Setup

This folder contains a `docker-compose.yml` file to set up an Apache Spark cluster using Docker. The cluster includes one master node, two worker nodes, and a container for submitting Spark jobs.

---

## **Services**

1. **`spark-master`**
   - Runs the Spark master node.
   - Exposes ports:
     - `8080`: Spark master web UI.
     - `7077`: Spark master RPC endpoint.

2. **`spark-worker-1`**
   - Runs the first Spark worker node.
   - Connects to the Spark master at `spark://spark-master:7077`.
   - Allocates 1GB of memory and 1 core.

3. **`spark-worker-2`**
   - Runs the second Spark worker node.
   - Similar configuration as `spark-worker-1`.

4. **`spark-submit`**
   - Used to submit Spark jobs to the cluster.
   - Connects to the Spark master at `spark://spark-master:7077`.

---

## **Setup Instructions**

### 1. **Prerequisites**
- Install [Docker](https://www.docker.com/products/docker-desktop).
- Install [Docker Compose](https://docs.docker.com/compose/install/).

### 2. **Start the Cluster**
Run the following command to start all services:
```bash
docker-compose up -d
```

### 3. **Access the Spark Web UI**
The Spark master web UI is available at:
[http://localhost:8080](http://localhost:8080)

### 4. **Submit a Spark Job**
To submit a job to the cluster, access the `spark-submit` container:
```bash
docker exec -it spark-submit /bin/bash
```
Inside the container, you can submit jobs using the `spark-submit` command. Example:
```bash
spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  /path/to/your/application.jar
```

### 5. **Stop the Cluster**
To stop and remove all services, run:
```bash
docker-compose down
```

---

## **Configuration**

- **Master Node**:
  - Hostname: `spark-master`
  - Spark URL: `spark://spark-master:7077`
- **Worker Nodes**:
  - `spark-worker-1`: Allocates 1GB of memory and 1 core.
  - `spark-worker-2`: Allocates 1GB of memory and 1 core.
- **Environment Variables**:
  - All services use pre-defined environment variables to configure Spark behavior.

---

## **Logs and Debugging**

- View logs for any service:
```bash
docker logs <container_name>
```
- Example:
```bash
docker logs spark-master
```

---

## **Scaling the Cluster**

To add more workers, update the `docker-compose.yml` file by duplicating and modifying the worker service. Example for `spark-worker-3`:
```yaml
  spark-worker-3:
    image: bitnami/spark:latest
    container_name: spark-worker-3
    hostname: spark-worker-3
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      - SPARK_WORKER_MEMORY=1G
      - SPARK_WORKER_CORES=1
      - SPARK_WORKER_PORT=8883
    depends_on:
      - spark-master
```

Restart the cluster:
```bash
docker-compose up -d
```

---

## **References**

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Bitnami Spark Docker Image](https://hub.docker.com/r/bitnami/spark/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
