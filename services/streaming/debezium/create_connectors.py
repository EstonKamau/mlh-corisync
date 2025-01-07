import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Kafka Connect REST API URL
KAFKA_CONNECT_URL = "http://localhost:8093/connectors"

# Connectors Configuration
CONNECTORS = [
    {
        "name": "mlh_uat",
        "config": {
            "topic.prefix": "tc4a",
            "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
            "tasks.max": "20",
            "database.hostname": os.getenv("DB_HOST", "localhost"),
            "database.port": os.getenv("DB_PORT", "5432"),
            "database.user": os.getenv("DB_USER", "user"),
            "database.password": os.getenv("DB_PASSWORD", "password"),
            "database.dbname": os.getenv("DB_NAME", "db_name"),
            "database.server.name": "mlh_uat",
            "plugin.name": "pgoutput",
            "slot.name": os.getenv("SLOT_NAME", "slot_name"),
            "schema.include.list": "public",
            "publication.name": os.getenv("PUBLICATION_NAME", "publication"),
            "topic.creation.default.replication.factor": 1,
            "topic.creation.default.partitions": 10,
            "topic.creation.default.cleanup.policy": "compact",
            "topic.creation.default.compression.type": "lz4"
        }
    },
    {
        "name": "mlh_production",
        "config": {
            "topic.prefix": "tc4a",
            "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
            "tasks.max": "20",
            "database.hostname": os.getenv("DB_HOST", "localhost"),
            "database.port": os.getenv("DB_PORT", "5432"),
            "database.user": os.getenv("DB_USER", "user"),
            "database.password": os.getenv("DB_PASSWORD", "password"),
            "database.dbname": os.getenv("DB_NAME", "db_name"),
            "database.server.name": "mlh_uat",
            "plugin.name": "pgoutput",
            "slot.name": os.getenv("SLOT_NAME", "slot_name"),
            "schema.include.list": "public",
            "publication.name": os.getenv("PUBLICATION_NAME", "publication"),
            "topic.creation.default.replication.factor": 1,
            "topic.creation.default.partitions": 10,
            "topic.creation.default.cleanup.policy": "compact",
            "topic.creation.default.compression.type": "lz4"
        }
    }
]

def get_connectors():
    """Fetch the list of connectors."""
    try:
        response = requests.get(KAFKA_CONNECT_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching connectors: {e}")
        return []

def create_connector(connector):
    """Create a new connector."""
    try:
        response = requests.post(
            KAFKA_CONNECT_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(connector)
        )
        if response.status_code == 201:
            print(f"Connector '{connector['name']}' created successfully.")
        elif response.status_code == 409:
            print(f"Connector '{connector['name']}' already exists.")
        else:
            print(f"Failed to create connector '{connector['name']}': {response.status_code} {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error creating connector '{connector['name']}': {e}")

def check_and_create_connector(connector):
    """Check if a connector exists and create it if it doesn't."""
    connectors = get_connectors()
    if connector["name"] in connectors:
        print(f"Connector '{connector['name']}' already exists.")
    else:
        print(f"Connector '{connector['name']}' does not exist. Creating...")
        create_connector(connector)

if __name__ == "__main__":
    # Loop through connectors and check/create
    for connector in CONNECTORS:
        check_and_create_connector(connector)