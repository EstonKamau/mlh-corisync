
# Debezium Docker Setup

This folder contains a `docker-compose.yml` file to run a Debezium container configured to capture change data from a PostgreSQL database. Debezium uses Kafka as the event streaming platform.

---

## **Services**

1. **`debezium`**:
   - Runs the Debezium Connector service.
   - Connects to Kafka and Zookeeper for managing and storing change data events.
   - Uses a configuration file `debezium-postgresql-connector.json` for setting up the PostgreSQL connector.

---

## **Setup Instructions**

### 1. **Prerequisites**
- Ensure [Docker](https://www.docker.com/products/docker-desktop) is installed.
- Kafka and Zookeeper services must be running and accessible at the `kafka:9092` address.

### 2. **Configuration**

#### Connector Configuration
- Modify the `debezium-postgresql-connector.json` file according to your PostgreSQL database setup. Example contents:
```json
{
  "name": "postgresql-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "db_user",
    "database.password": "db_password",
    "database.dbname": "db_name",
    "database.server.name": "db_server",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_slot",
    "publication.name": "debezium_publication"
  }
}
```
- Replace the placeholders (`db_user`, `db_password`, `db_name`, etc.) with actual values.

#### Kafka and Zookeeper
- Ensure the Kafka and Zookeeper services are available and running on the network `data_platform_network`.

---

### 3. **Start the Debezium Service**
Run the following command to start the container:
```bash
docker-compose up -d
```

### 4. **Access the Debezium REST API**
Once the container is running, Debezium's REST API is available at:
[http://localhost:8083](http://localhost:8083)

---

## **Usage**

### Register a Connector
To register a new connector, make a POST request to the Debezium REST API:
```bash
curl -X POST -H "Content-Type: application/json" \
  --data @/etc/debezium/postgresql-connector.json \
  http://localhost:8083/connectors
```

### Verify Connector Status
To check the status of the connector:
```bash
curl http://localhost:8083/connectors/<connector_name>/status
```

---

## **Logs and Debugging**

- View logs for the Debezium container:
```bash
docker logs -f debezium
```

- To inspect configuration errors, check the logs for messages related to connector initialization.

---

## **Networking**

The service is part of the `data_platform_network` Docker network. Ensure other services like Kafka and Zookeeper are also connected to this network.

---

## **Stop the Service**
To stop and remove the service, run:
```bash
docker-compose down
```

---

## **References**

- [Debezium Documentation](https://debezium.io/documentation/)
- [Debezium Docker Hub](https://hub.docker.com/r/debezium/connect)
- [Kafka Documentation](https://kafka.apache.org/documentation/)