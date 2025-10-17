# 🐘 PostgreSQL Setup - Complete Guide

## ✅ Setup Complete!

Your RequestBin is now configured with PostgreSQL database:
- **Host:** localhost:55234
- **Database:** gmImNcMNjRlT
- **Schema:** requestbin_app

## 🚀 Quick Start (2 Steps)

### Step 1: Initialize Database Schema

Open PowerShell in the `requestbin` folder and run:

```powershell
conda activate requestbin
python init_postgres_schema.py
```

This will create all tables and the admin user.

### Step 2: Start the Application

```powershell
.\run-postgres.bat
```

Or if batch file doesn't work:

```powershell
conda activate requestbin
python web.py
```

(Make sure to set environment variables first - see below)

## 🌐 Access the Application

1. Open browser: **http://localhost:4000**
2. Login with:
   - **Email:** `admin@requestbin.local`
   - **Password:** `ChangeMe123!`
3. Click "Create a RequestBin" - **It will work!** ✅

## 📝 Files Created

| File | Purpose |
|------|---------|
| `init_postgres_schema.py` | Python script to initialize database (no psql needed) |
| `init-postgres-schema.ps1` | PowerShell wrapper for schema init |
| `run-postgres.bat` | Batch file to start app with all env vars set |
| `run-local-postgres.ps1` | PowerShell script to start app |
| `run-local-memory.ps1` | PowerShell script for memory backend (testing) |

## 🔧 Manual Setup (if scripts don't work)

### 1. Activate Conda Environment
```powershell
conda activate requestbin
```

### 2. Initialize Schema
```powershell
python init_postgres_schema.py
```

### 3. Set Environment Variables
```powershell
$env:STORAGE_BACKEND = "requestbin.storage.postgresql.PostgreSQLStorage"
$env:POSTGRES_SCHEMA = "requestbin_app"
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_PORT = "55234"
$env:POSTGRES_DB = "gmImNcMNjRlT"
$env:POSTGRES_USER = "f21e30667747"
$env:POSTGRES_PASSWORD = "de9e43ee16df119956ce1db8582"
$env:ADMIN_EMAIL = "admin@requestbin.local"
$env:ADMIN_PASSWORD = "ChangeMe123!"
$env:AUTO_APPROVE_DOMAINS = "tarento.com,ivolve.ai"
$env:FLASK_SESSION_SECRET_KEY = "3bb25fea945db5a13bd751fbcc34e90a2b1446b6334abe52606051df02448539"
$env:MAX_REQUESTS = "200"
$env:REALM = "local"
```

### 4. Start Application
```powershell
python web.py
```

## 🔍 Troubleshooting

### "psql is not recognized"
✅ **Solution:** Use `python init_postgres_schema.py` instead - it doesn't need psql!

### "Python was not found"
✅ **Solution:** Activate conda environment first:
```powershell
conda activate requestbin
python init_postgres_schema.py
```

### "Bin Not found" error
✅ **Solution:** Make sure you:
1. Initialized the schema (`python init_postgres_schema.py`)
2. Started app with environment variables (`.\run-postgres.bat`)
3. Logged in before creating bins

### "psycopg2 not found"
✅ **Solution:** Install it:
```powershell
conda activate requestbin
pip install psycopg2-binary
```

### Can't connect to PostgreSQL
✅ **Check:**
1. Is PostgreSQL running?
2. Is it listening on port 55234?
3. Does database `gmImNcMNjRlT` exist?
4. Can you connect manually with these credentials?

## 📊 Verify Setup

```powershell
# Run diagnostic tool
python diagnose.py

# This will show:
# - ✅ Storage backend: PostgreSQL
# - ✅ Database connection: OK
# - ✅ Tables created: 5
# - ✅ Admin user: exists
```

## 🎯 What This Fixes

The "Bin Not found" error was caused by:
- ❌ Missing PostgreSQL configuration
- ❌ Using memory storage (data lost on restart)
- ❌ Environment variables not set

Now with proper setup:
- ✅ Bins persist in PostgreSQL database
- ✅ Sessions work correctly
- ✅ Authentication works
- ✅ No data loss on restart

## 🔑 Default Credentials

**Admin Account:**
- Email: `admin@requestbin.local`
- Password: `ChangeMe123!`

**Auto-Approved Domains:**
- tarento.com
- ivolve.ai

Users with these email domains are automatically approved after email verification.

## 📚 Additional Resources

- **Full setup guide:** `POSTGRESQL_SETUP.md`
- **Quick start:** `QUICKSTART.md`
- **Deployment guide:** `POSTGRESQL_DEPLOYMENT.md`
- **Schema documentation:** `POSTGRES_SCHEMA.md`

## ✨ Success Indicators

You'll know everything is working when:
1. ✅ Schema initialization completes without errors
2. ✅ App starts and shows "Running on http://127.0.0.1:4000"
3. ✅ You can login at http://localhost:4000/login
4. ✅ "Create a RequestBin" button creates bins successfully
5. ✅ Created bins persist after app restart

---

**Need help?** Run `python diagnose.py` to check your configuration!
