# PostgreSQL Deployment Guide for RequestBin

## Overview

This guide explains how to deploy RequestBin with PostgreSQL as the storage backend, both locally and on SAP BTP Cloud Foundry.

## Why PostgreSQL?

- ✅ **Persistent Storage**: Data survives application restarts
- ✅ **Relational Queries**: Better for analytics and reporting
- ✅ **ACID Compliance**: Reliable data consistency
- ✅ **Scalability**: Handles large datasets efficiently
- ✅ **SAP BTP Native**: Available as a managed service
- ✅ **SQL Standard**: Easy to query and maintain

## Architecture

### Database Schema

The PostgreSQL storage uses three main tables:

1. **bins**: Stores bin metadata (name, created_at, expires_at, private, colors, etc.)
2. **requests**: Stores serialized request data with ordering
3. **stats**: Global counters for analytics

### Features

- Automatic cleanup of expired bins
- Connection pooling for performance
- Support for SAP BTP VCAP_SERVICES auto-configuration
- SSL/TLS support for secure connections
- Efficient indexing for fast queries

## Local Development Setup

### 1. Install PostgreSQL

**Windows:**
```bash
# Download from https://www.postgresql.org/download/windows/
# Or use Chocolatey
choco install postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Create Database

```bash
# Login as postgres user
psql -U postgres

# Create database and user
CREATE DATABASE requestbin;
CREATE USER requestbin_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE requestbin TO requestbin_user;

# Grant schema usage (will be created by schema.sql)
GRANT ALL PRIVILEGES ON SCHEMA requestbin_app TO requestbin_user;
GRANT USAGE ON SCHEMA requestbin_app TO requestbin_user;
\q
```

### 3. Initialize Schema

The schema.sql file creates the `requestbin_app` schema and all necessary tables within it.

```bash
# Run the schema initialization script
psql -U requestbin_user -d requestbin -f schema.sql
```

This will:
- Create the `requestbin_app` schema
- Create tables: users, bins, requests, stats
- Create necessary indexes
- Set up the search_path

### 4. Configure Environment

Create a `.env` file or set environment variables:

```bash
export REALM=prod
export STORAGE_BACKEND=postgresql
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=requestbin
export POSTGRES_SCHEMA=requestbin_app  # Schema name (default: requestbin_app)
export POSTGRES_USER=requestbin_user
export POSTGRES_PASSWORD=your_secure_password
export POSTGRES_SSLMODE=prefer
```

### 5. Install Dependencies

```bash
# Activate your Python environment
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python web.py
```

Visit `http://localhost:4000` to access RequestBin.

## SAP BTP Deployment

### Prerequisites

1. CF CLI installed and configured
2. Access to SAP BTP Cloud Foundry space
3. PostgreSQL service available in your SAP BTP region

### Step 1: Login to SAP BTP

```bash
cf login -a <api-endpoint> -o <org> -s <space>
```

### Step 2: Check Available PostgreSQL Services

```bash
# List available PostgreSQL services
cf marketplace | grep postgres
```

Common service names:
- `postgresql-db`
- `postgres`
- `postgresql`

### Step 3: Create PostgreSQL Service Instance

```bash
# Create a PostgreSQL service instance
cf create-service postgresql-db <plan> requestbin-postgresql

# Example with specific plan
cf create-service postgresql-db small requestbin-postgresql

# Check service creation status
cf service requestbin-postgresql
```

Wait for the service to be created (status: `create succeeded`).

### Step 4: Initialize Database Schema

You have two options to initialize the schema:

#### Option A: Use cf ssh (Recommended)

```bash
# Deploy the app first
cf push -f manifest-postgresql.yml

# SSH into the app
cf ssh requestbin-app

# Install psql client (if not available)
apt-get update && apt-get install -y postgresql-client

# Get database credentials
echo $VCAP_SERVICES | jq '.postgresql[0].credentials'

# Connect and initialize schema
psql -h <host> -U <user> -d <database> -f schema.sql

# Exit SSH
exit
```

#### Option B: Use Local psql with Service Key

```bash
# Create a service key to get credentials
cf create-service-key requestbin-postgresql requestbin-key

# Get the credentials
cf service-key requestbin-postgresql requestbin-key

# Use the credentials to connect from your local machine
psql -h <host> -U <user> -d <database> -f schema.sql
```

### Step 5: Deploy the Application

```bash
# Deploy using PostgreSQL manifest
cf push -f manifest-postgresql.yml
```

### Step 6: Verify Deployment

```bash
# Check application status
cf apps

# View logs
cf logs requestbin-app --recent

# Test the application
curl https://requestbin-app.cfapps.eu10-004.hana.ondemand.com
```

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STORAGE_BACKEND` | `postgresql` | Storage backend type (postgresql/redis/memory) |
| `POSTGRES_HOST` | `localhost` | PostgreSQL server hostname |
| `POSTGRES_PORT` | `5432` | PostgreSQL server port |
| `POSTGRES_DB` | `requestbin` | Database name |
| `POSTGRES_USER` | `postgres` | Database user |
| `POSTGRES_PASSWORD` | `` | Database password |
| `POSTGRES_SSLMODE` | `prefer` | SSL mode (disable/allow/prefer/require) |
| `MAX_REQUESTS` | `200` | Maximum requests per bin |
| `BIN_TTL` | `345600` | Bin lifetime in seconds (96 hours) |

### SAP BTP VCAP_SERVICES Auto-Configuration

When deployed to SAP BTP, the application automatically detects PostgreSQL service credentials from `VCAP_SERVICES` environment variable. No manual configuration needed!

The application looks for services named:
- `postgresql`
- `postgresql-db`
- `postgres`

## Database Maintenance

### Manual Cleanup of Expired Bins

```sql
-- Connect to database
psql -U requestbin_user -d requestbin

-- Run cleanup function
SELECT cleanup_expired_bins();

-- View bin statistics
SELECT * FROM bin_stats;
```

### Check Database Size

```sql
-- Database size
SELECT pg_size_pretty(pg_database_size('requestbin'));

-- Table sizes
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename::text)) as size
FROM pg_tables
WHERE schemaname = 'public';
```

### Backup and Restore

```bash
# Backup
pg_dump -U requestbin_user requestbin > requestbin_backup.sql

# Restore
psql -U requestbin_user requestbin < requestbin_backup.sql
```

## Monitoring

### Performance Queries

```sql
-- Most active bins
SELECT 
    name,
    request_count,
    created_at,
    expires_at
FROM bins
ORDER BY request_count DESC
LIMIT 10;

-- Request volume over time
SELECT 
    DATE_TRUNC('hour', created_at) as hour,
    COUNT(*) as request_count
FROM requests
WHERE created_at > NOW() - INTERVAL '24 hours'
GROUP BY hour
ORDER BY hour DESC;

-- Average request size
SELECT 
    pg_size_pretty(AVG(LENGTH(request_data))::bigint) as avg_request_size
FROM requests;
```

## Troubleshooting

### Connection Issues

**Error: "could not connect to server"**
```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# Check PostgreSQL logs
tail -f /var/log/postgresql/postgresql-*.log
```

**Error: "FATAL: password authentication failed"**
```bash
# Verify credentials
psql -U requestbin_user -d requestbin -h localhost

# Reset password if needed
ALTER USER requestbin_user WITH PASSWORD 'new_password';
```

### SAP BTP Issues

**Service binding not working**
```bash
# Check service binding
cf env requestbin-app

# Verify VCAP_SERVICES contains PostgreSQL credentials
cf ssh requestbin-app
echo $VCAP_SERVICES | jq '.postgresql'
```

**Schema not initialized**
```bash
# Connect via SSH and run schema
cf ssh requestbin-app
psql <connection_string> -f schema.sql
```

### Performance Issues

**Slow queries**
```sql
-- Check for missing indexes
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE schemaname = 'public';

-- Analyze tables
ANALYZE bins;
ANALYZE requests;
```

## Migration from Redis

If you're migrating from Redis to PostgreSQL:

1. **Deploy PostgreSQL version** alongside Redis version
2. **Export Redis data** (if needed for historical data)
3. **Switch traffic** to PostgreSQL version
4. **Monitor performance** and adjust as needed
5. **Decommission Redis** service once stable

### Note on Data Migration

The Redis and PostgreSQL storage backends use different serialization formats. Direct data migration is not supported. Start fresh with PostgreSQL, or implement a custom migration script if historical data is critical.

## Performance Tuning

### Connection Pool Settings

In `postgresql.py`, adjust connection pool settings:

```python
self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=5,      # Minimum connections
    maxconn=20,     # Maximum connections
    ...
)
```

### PostgreSQL Configuration

For production workloads, tune PostgreSQL settings:

```sql
-- In postgresql.conf
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
```

## Security Best Practices

1. **Use strong passwords** for database users
2. **Enable SSL/TLS** for database connections
3. **Limit network access** to database (firewall rules)
4. **Regular backups** of database
5. **Monitor for suspicious activity**
6. **Keep PostgreSQL updated** with security patches

## Cost Considerations (SAP BTP)

PostgreSQL services on SAP BTP are billed based on:
- Database size
- Number of connections
- IOPS (Input/Output Operations Per Second)
- Backup storage

Choose an appropriate service plan based on your expected load.

## Support

For issues or questions:
- Check application logs: `cf logs requestbin-app --recent`
- Review PostgreSQL logs on your server
- Create an issue on GitHub: https://github.com/babu3009/requestbin/issues

## Next Steps

- ✅ Deploy to SAP BTP with PostgreSQL
- ✅ Monitor performance and optimize
- ✅ Set up regular backups
- ✅ Configure alerting for errors
- ✅ Review and tune database settings
