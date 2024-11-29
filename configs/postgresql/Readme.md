

# PostgreSQL Configuration

This folder contains files to configure PostgreSQL for logical replication and external connections.

## Files

1. **`configure_postgres.sql`**
   - A SQL script that dynamically applies the following PostgreSQL configurations:
     - Sets `wal_level` to `logical` for logical replication.
     - Configures `max_replication_slots` and `max_replication_workers`.
     - Updates `listen_addresses` to allow connections from all IP addresses.
   - Includes a `pg_reload_conf` command to reload the updated settings.

2. **`postgresql.conf`** (Optional)
   - A sample PostgreSQL configuration file with parameters like:
     - `wal_level = logical`
     - `max_replication_slots = 4`
     - `max_replication_workers = 4`
     - `listen_addresses = '*'`
   - Use this file to manually set parameters if the `ALTER SYSTEM` approach is not preferred.

3. **`pg_hba.conf`** (Optional)
   - A sample host-based authentication configuration file.
   - Includes entries to allow replication and external connections.
   - Example:
     ```
     # TYPE  DATABASE        USER            ADDRESS                 METHOD
     host    replication     all             0.0.0.0/0               md5
     host    all             all             0.0.0.0/0               md5
     ```

## Usage

### Option 1: Apply Configurations Dynamically
1. Open a terminal and navigate to this folder.
2. Execute the SQL file to apply configurations:
   ```bash
   psql -U <your_username> -d <your_database> -f configure_postgres.sql
   ```
3. Restart PostgreSQL if required:
   ```bash
   sudo systemctl restart postgresql
   ```

### Option 2: Manual Configuration
1. Copy the provided `postgresql.conf` and `pg_hba.conf` files to your PostgreSQL configuration directory:
   ```bash
   sudo cp postgresql.conf /etc/postgresql/<version>/main/
   sudo cp pg_hba.conf /etc/postgresql/<version>/main/
   ```
2. Restart PostgreSQL to apply changes:
   ```bash
   sudo systemctl restart postgresql
   ```

## Notes
- Ensure you have the necessary permissions to modify PostgreSQL configuration.
- Changes to `listen_addresses` and some replication settings require a server restart to take effect.
- Make sure to secure your PostgreSQL server by restricting access to trusted IPs in `pg_hba.conf`.

## Troubleshooting
- Verify that the PostgreSQL server is running:
  ```bash
  sudo systemctl status postgresql
  ```
- Check the logs for any errors:
  ```bash
  sudo tail -f /var/log/postgresql/postgresql-<version>-main.log
  ```

## References
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)