# Data Persistence Fix

## Issue
Data was being cleared whenever the application restarted, even though PostgreSQL was configured. The bins and requests were not persisting across app restarts.

## Root Cause
The issue was in `requestbin/config.py`. The configuration was set up so that:

1. **Default behavior** (line 18): `STORAGE_BACKEND = "requestbin.storage.memory.MemoryStorage"`
   - This uses in-memory storage which clears on restart

2. **PostgreSQL configuration** was only loaded when `REALM == 'prod'` (line 113+)
   - When running locally with `REALM=local`, the PostgreSQL settings were ignored
   - The app was using MemoryStorage even though `run-postgres.bat` set the environment variable

## Solution
Modified `requestbin/config.py` to:

1. **Load STORAGE_BACKEND from environment variable first** (line 18):
   ```python
   STORAGE_BACKEND = os.environ.get('STORAGE_BACKEND', "requestbin.storage.memory.MemoryStorage")
   ```

2. **Load PostgreSQL configuration regardless of REALM** (after line 110):
   ```python
   # Load PostgreSQL configuration from environment (works for both local and prod)
   if STORAGE_BACKEND == "requestbin.storage.postgresql.PostgreSQLStorage":
       # Try VCAP_SERVICES first, then fall back to environment variables
       vcap_postgres_config = get_postgres_config_from_vcap()
       
       if vcap_postgres_config:
           # Use SAP BTP PostgreSQL service
           POSTGRES_HOST = vcap_postgres_config['host']
           # ... etc
       else:
           # Fallback to environment variables
           POSTGRES_HOST = os.environ.get('POSTGRES_HOST', POSTGRES_HOST)
           # ... etc
   ```

3. **Simplified the prod section** to avoid duplicate configuration logic

## Benefits
- ✅ Data now persists across app restarts when using PostgreSQL backend
- ✅ Works in both local (`REALM=local`) and production (`REALM=prod`) environments
- ✅ Environment variable `STORAGE_BACKEND` is respected regardless of REALM
- ✅ Bins are stored with TTL of 96 hours (4 days) as configured in `BIN_TTL`
- ✅ Automatic cleanup of expired bins via PostgreSQL queries

## Data Retention Details
- **Bin TTL**: 96 hours (4 days) - configured in `config.py` as `BIN_TTL = 96*3600`
- **Storage location**: PostgreSQL database tables:
  - `bins` table: Stores bin metadata with `expires_at` timestamp
  - `requests` table: Stores serialized request data linked to bins
- **Cleanup**: Expired bins are automatically deleted when `lookup_bin()` is called
- **Max requests per bin**: 200 (configurable via `MAX_REQUESTS` environment variable)

## Testing
To verify data persistence:

1. **Create a bin and send requests**:
   ```bash
   # Run the test script
   python test_inspect_view.py
   ```

2. **Restart the application**:
   ```bash
   # Stop with Ctrl+C, then restart
   .\run-postgres.bat
   ```

3. **Verify data is still there**:
   - Open: http://localhost:4000/YOUR_BIN_ID?inspect
   - All requests should still be visible
   - Data will persist until bin expires (96 hours from creation)

## Files Modified
- `requestbin/config.py` - Fixed storage backend configuration loading

## Configuration
The `run-postgres.bat` file sets the correct environment variables:
- `STORAGE_BACKEND=requestbin.storage.postgresql.PostgreSQLStorage`
- `POSTGRES_HOST=localhost`
- `POSTGRES_PORT=55234`
- `POSTGRES_DB=gmImNcMNjRlT`
- `POSTGRES_SCHEMA=requestbin_app`
- `REALM=local` (for local development with debug mode)
