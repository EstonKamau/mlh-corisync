-- Enable logical replication
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_replication_slots = 4;
ALTER SYSTEM SET max_wal_senders = 4;
SELECT pg_reload_conf();

-- Create replication user
CREATE ROLE replicator WITH REPLICATION PASSWORD 'replicator_password' LOGIN;