# Zookeeper Docker Setup

This folder contains a `docker-compose.yml` file for deploying a Zookeeper instance using Docker. Zookeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.

---

## **Setup Overview**

- **Zookeeper Version**: `3.4.6` (provided by the `wurstmeister/zookeeper` image).
- **Network**: Configured to use a Docker bridge network named `cori-sync-net`.

---

## **Setup Instructions**

### 1. **Prerequisites**
- Install [Docker](https://www.docker.com/products/docker-desktop).
- Install [Docker Compose](https://docs.docker.com/compose/install/).

---

### 2. **Start Zookeeper**

To start the Zookeeper container:
```bash
docker-compose up -d
```

---

### 3. **Access Zookeeper**

- **Port**: Zookeeper listens on port `2181`. You can connect using Zookeeper clients or tools:
  ```bash
  telnet localhost 2181
  ```

---

### 4. **Network**

- The `zookeeper` service is part of the `cori-sync-net` bridge network.
- Ensure other services that need to interact with Zookeeper are connected to this network.

---

### 5. **Stopping Zookeeper**

To stop and remove the Zookeeper container:
```bash
docker-compose down
```

---

## **Environment Variables**

- `ZOOKEEPER_SERVER_ID`: Defines the server ID for this Zookeeper instance.
- `ZOOKEEPER_LISTENER_PORT`: Sets the listener port (default: `2181`).

---

## **Logs and Debugging**

View logs for Zookeeper:
```bash
docker logs zookeeper
```

---

## **References**

- [Zookeeper Documentation](https://zookeeper.apache.org/)
- [Docker Hub: Wurstmeister Zookeeper](https://hub.docker.com/r/wurstmeister/zookeeper/)