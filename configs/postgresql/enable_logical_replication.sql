-- Set wal_level to logical
ALTER SYSTEM SET wal_level = 'logical';

-- Set max_replication_slots to 4
ALTER SYSTEM SET max_replication_slots = 4;

-- Set max_replication_workers to 4
ALTER SYSTEM SET max_replication_workers = 4;

-- Allow connections from all IP addresses
ALTER SYSTEM SET listen_addresses = '*';

-- Reload the configuration to apply changes
SELECT pg_reload_conf();

-- Create replication user
CREATE ROLE replicator WITH REPLICATION PASSWORD 'replicator_password' LOGIN;