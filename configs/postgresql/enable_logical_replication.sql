ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET max_replication_slots = 4;
ALTER SYSTEM SET max_replication_workers = 4;
ALTER SYSTEM SET listen_addresses = '*';
SELECT pg_reload_conf();
CREATE ROLE replicator WITH REPLICATION PASSWORD 'replicator_password' LOGIN;