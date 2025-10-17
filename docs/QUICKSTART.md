# RequestBin - Quick Start Guide

## Problem: "Bin Not found" Error

If you're seeing "Bin Not found" when trying to create a bin, this is likely due to one of these issues:

### 1. Running without proper environment configuration

**Solution:** Use the provided startup scripts

#### Option A: Memory Backend (Simplest - No database needed)
```powershell
.\run-local-memory.ps1
```

#### Option B: PostgreSQL Backend (Persistent storage)
```powershell
# First, make sure PostgreSQL is running and initialized:
createdb requestbin
psql -d requestbin -f schema.sql

# Then run:
.\run-local-postgres.ps1
```

### 2. Session/Authentication Issues

The API endpoint requires authentication. Make sure you:

1. **Register an account** at http://localhost:4000/register
   - Use an auto-approve domain (tarento.com or ivolve.ai) for instant access
   - OR use any email and wait for admin approval

2. **Verify your email** with the OTP code (printed in console if SMTP not configured)

3. **Login** at http://localhost:4000/login

4. **Then create bins** - they should work now!

### 3. Memory Backend Limitation

If using Memory backend, bins are stored in RAM and **will be lost when you restart the application**.

To persist bins across restarts, use PostgreSQL backend.

### 4. Flask Session Secret Key

The application needs a secret key for sessions. This is configured in:
- `manifest-postgresql.yml` (for SAP BTP deployment)
- Or set via environment variable: `$env:FLASK_SESSION_SECRET_KEY = "your-secret-key"`

The startup scripts handle this automatically.

## Testing

To verify everything is working:

```powershell
# Run diagnostics
python diagnose.py

# Test bin creation
python debug_bin_creation.py

# Test full workflow
python test_workflow.py
```

## Default Credentials

- **Admin Email:** admin@requestbin.local
- **Admin Password:** ChangeMe123!

Change these in production!

## Auto-Approve Domains

Users with these email domains are automatically approved:
- tarento.com
- ivolve.ai

All other domains require admin approval.

## Troubleshooting

### Check if app is running:
```powershell
# Should see Flask server on http://localhost:4000
```

### Check authentication:
1. Can you access http://localhost:4000/login?
2. Can you login with admin credentials?
3. After login, can you see "Create a RequestBin" button?

### Check logs:
- OTP codes are printed to console if SMTP is not configured
- Any errors will appear in the terminal where you started the app

### Still having issues?

1. Stop the application (Ctrl+C)
2. Run: `python diagnose.py`
3. Check the output for any errors
4. Restart with the appropriate script:
   - `.\run-local-memory.ps1` (simplest)
   - `.\run-local-postgres.ps1` (with database)
