# Metabase Setup and Deployment

Metabase is an open-source business intelligence tool that allows you to visualize and analyze data from various data sources.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Variables](#environment-variables)
3. [Docker Compose Setup](#docker-compose-setup)
4. [Starting Metabase](#starting-metabase)
5. [Accessing Metabase](#accessing-metabase)
6. [Customizing Metabase](#customizing-metabase)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying Metabase, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- A database for Metabase to store its application data (e.g., PostgreSQL, MySQL, etc.)

---

## Environment Variables

Create an `.env` file in the same directory as your `docker-compose.yml` file and define the following variables:

```env
# Metabase application configuration
MB_DB_TYPE=postgres
MB_DB_HOST=your_database_host
MB_DB_PORT=5432
MB_DB_USER=your_database_user
MB_DB_PASS=your_database_password
MB_DB_DBNAME=your_metabase_db_name
MB_JETTY_PORT=3000
```

Replace `your_database_host`, `your_database_user`, `your_database_password`, and `your_metabase_db_name` with the actual values for your database.

---

## Docker Compose Setup

Below is a sample `docker-compose.yml` file for deploying Metabase:

```yaml
version: '3.8'

services:
  metabase:
    image: metabase/metabase:latest
    container_name: metabase
    ports:
      - "3000:3000"
    environment:
      MB_DB_TYPE: ${MB_DB_TYPE}
      MB_DB_HOST: ${MB_DB_HOST}
      MB_DB_PORT: ${MB_DB_PORT}
      MB_DB_USER: ${MB_DB_USER}
      MB_DB_PASS: ${MB_DB_PASS}
      MB_DB_DBNAME: ${MB_DB_DBNAME}
    volumes:
      - metabase-data:/metabase-data

volumes:
  metabase-data:
```

---

## Starting Metabase

To start Metabase:

1. Ensure the `.env` file is properly configured.
2. Run the following commands:

   ```bash
   docker-compose down  # Stop any running containers (if necessary)
   docker-compose up -d --build  # Start Metabase in detached mode
   ```

---

## Accessing Metabase

Once the container is running, you can access Metabase by visiting:

```
http://<your-server-ip>:3000
```

If you’re running locally, use:

```
http://localhost:3000
```

---

## Customizing Metabase

You can customize Metabase further by:

1. **Adding Plugins:** Place any Metabase plugins in the `plugins` directory inside the container’s `/metabase-data` volume.
2. **SSL/TLS Configuration:** Use a reverse proxy like Nginx or Traefik to secure your Metabase instance with HTTPS.

---

## Troubleshooting

1. **Database Connection Issues:**
   - Verify that the database credentials in the `.env` file are correct.
   - Check if the database is accessible from the Metabase container.

2. **Port Conflicts:**
   - Ensure no other service is using port `3000`. Update to a suitable port mapping in `docker-compose.yml` if needed.

3. **Logs:**
   - View container logs to debug issues:
     ```bash
     docker logs metabase
     ```