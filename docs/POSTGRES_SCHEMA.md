# PostgreSQL Schema Configuration

## Overview

RequestBin now uses a dedicated PostgreSQL schema named `requestbin_app` for all database tables. This provides better organization and isolation from other applications.

## Configuration

### Environment Variable

```bash
POSTGRES_SCHEMA=requestbin_app  # Default value
```

### Files Modified

1. **requestbin/config.py** - Added `POSTGRES_SCHEMA` configuration
2. **requestbin/storage/postgresql.py** - Updated connection with schema search_path
3. **requestbin/auth_storage.py** - Updated connection with schema search_path
4. **schema.sql** - Creates and uses requestbin_app schema
5. **manifest-postgresql.yml** - Added POSTGRES_SCHEMA environment variable
6. **POSTGRESQL_DEPLOYMENT.md** - Updated documentation

## Database Structure

```
Database: requestbin
└── Schema: requestbin_app
    ├── users          (authentication data)
    ├── bins           (bin metadata)
    ├── requests       (request data)
    ├── stats          (global counters)
    └── bin_stats      (analytics view)
```

## How It Works

### 1. Schema Creation (schema.sql)

```sql
CREATE SCHEMA IF NOT EXISTS requestbin_app;
SET search_path TO requestbin_app;

-- All tables are created in requestbin_app schema
CREATE TABLE IF NOT EXISTS users (...);
CREATE TABLE IF NOT EXISTS bins (...);
-- etc.
```

### 2. Connection Configuration

Both PostgreSQL storage and auth storage use the `search_path` option:

```python
# In connection pool initialization
self.pool = ThreadedConnectionPool(
    # ... other params ...
    options=f'-c search_path={config.POSTGRES_SCHEMA}'
)
```

This ensures all queries use the `requestbin_app` schema by default.

### 3. Query Execution

No changes needed in queries! They automatically use the schema:

```python
# This query uses requestbin_app.users automatically
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```

## Deployment

### Local Development

```bash
# 1. Create database
psql -U postgres -c "CREATE DATABASE requestbin;"

# 2. Run schema (creates requestbin_app schema and tables)
psql -U postgres -d requestbin -f schema.sql

# 3. Set environment variable (optional, has default)
export POSTGRES_SCHEMA=requestbin_app

# 4. Run application
python web.py
```

### SAP BTP Cloud Foundry

Already configured in `manifest-postgresql.yml`:

```yaml
env:
  POSTGRES_SCHEMA: requestbin_app
```

Deploy:
```bash
cf push -f manifest-postgresql.yml
```

## Benefits

✅ **Namespace Isolation** - No conflicts with other applications in the same database  
✅ **Organized Structure** - All RequestBin tables in one schema  
✅ **Clean Public Schema** - System tables separate from application tables  
✅ **Security** - Schema-level permissions can be granted separately  
✅ **Easy Management** - Clear separation of concerns  

## Verification

Run the schema configuration test:

```bash
python test_schema_config.py
```

Expected output:
```
✅ ALL SCHEMA CONFIGURATION TESTS PASSED

Summary:
  • PostgreSQL schema: requestbin_app
  • Schema will be created by schema.sql
  • Connection uses: options="-c search_path=requestbin_app"
  • All tables will be in: requestbin_app schema
```

## Troubleshooting

### Schema not found error

```
ERROR: schema "requestbin_app" does not exist
```

**Solution:** Run `schema.sql` to create the schema:
```bash
psql -U postgres -d requestbin -f schema.sql
```

### Tables in wrong schema

If tables were created in `public` schema before this change:

```bash
# Option 1: Move tables to new schema
psql -U postgres -d requestbin -c "ALTER TABLE public.users SET SCHEMA requestbin_app;"
psql -U postgres -d requestbin -c "ALTER TABLE public.bins SET SCHEMA requestbin_app;"
# ... repeat for other tables

# Option 2: Drop and recreate (loses data!)
psql -U postgres -d requestbin -f schema.sql
```

### Permission issues

Grant permissions on the schema:

```sql
GRANT ALL PRIVILEGES ON SCHEMA requestbin_app TO requestbin_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA requestbin_app TO requestbin_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA requestbin_app TO requestbin_user;
GRANT USAGE ON SCHEMA requestbin_app TO requestbin_user;
```

## Migration from Previous Version

If you were using the default `public` schema:

1. **Backup your data:**
   ```bash
   pg_dump -U postgres requestbin > backup.sql
   ```

2. **Run new schema.sql:**
   ```bash
   psql -U postgres -d requestbin -f schema.sql
   ```

3. **Migrate existing data (if tables in public schema):**
   ```bash
   # Move tables to new schema
   psql -U postgres -d requestbin << EOF
   ALTER TABLE public.users SET SCHEMA requestbin_app;
   ALTER TABLE public.bins SET SCHEMA requestbin_app;
   ALTER TABLE public.requests SET SCHEMA requestbin_app;
   ALTER TABLE public.stats SET SCHEMA requestbin_app;
   EOF
   ```

4. **Update application environment:**
   ```bash
   export POSTGRES_SCHEMA=requestbin_app
   ```

5. **Restart application**

## Summary

- **Schema Name:** `requestbin_app`
- **Default:** Yes (hardcoded default in config.py)
- **Configurable:** Yes (via POSTGRES_SCHEMA environment variable)
- **Auto-created:** Yes (by schema.sql)
- **Connection:** Uses `search_path` PostgreSQL option
- **Queries:** No changes needed, automatically use schema
- **Benefits:** Isolation, organization, security

All database operations now use the `requestbin_app` schema by default! 🎉
