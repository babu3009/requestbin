# PostgreSQL Setup Instructions

## ✅ Configuration Updated

Your PostgreSQL connection details have been configured in `run-local-postgres.ps1`:

- **Host:** localhost
- **Port:** 55234
- **Database:** gmImNcMNjRlT
- **Username:** f21e30667747
- **Password:** de9e43ee16df119956ce1db8582
- **Schema:** requestbin_app

## 🚀 Next Steps

### 1. Initialize the Database Schema

Run this command to create all tables in your PostgreSQL database:

```powershell
$env:PGPASSWORD='de9e43ee16df119956ce1db8582'; psql -h localhost -p 55234 -U f21e30667747 -d gmImNcMNjRlT -f schema.sql
```

This will:
- Create the `requestbin_app` schema
- Create all necessary tables (bins, requests, users, otps, stats)
- Set up indexes and permissions

### 2. Stop Current Application

If the app is running, press `Ctrl+C` to stop it.

### 3. Start with PostgreSQL Backend

```powershell
.\run-local-postgres.ps1
```

This will start the application with persistent PostgreSQL storage.

### 4. Login and Test

1. Open browser: http://localhost:4000
2. Login with admin credentials:
   - Email: `admin@requestbin.local`
   - Password: `ChangeMe123!`
3. Click "Create a RequestBin"
4. The bin should now persist even after app restart!

## 🔍 Troubleshooting "Bin Not found" Error

If you're still seeing "Bin Not found", check:

### ✅ Are you logged in?
- Go to http://localhost:4000/login
- Use admin credentials above
- After login, you should be redirected to home page

### ✅ Is the schema initialized?
- Run the psql command from step 1 above
- Check for any errors in the output

### ✅ Is the app using PostgreSQL?
- After running `.\run-local-postgres.ps1`, you should see:
  ```
  STORAGE_BACKEND: requestbin.storage.postgresql.PostgreSQLStorage
  ```

### ✅ Check application logs
- Look for any PostgreSQL connection errors
- OTP codes for registration will print to console

## 📝 Quick Commands Reference

**Initialize schema:**
```powershell
$env:PGPASSWORD='de9e43ee16df119956ce1db8582'; psql -h localhost -p 55234 -U f21e30667747 -d gmImNcMNjRlT -f schema.sql
```

**Start with PostgreSQL:**
```powershell
.\run-local-postgres.ps1
```

**Start with Memory (testing only):**
```powershell
.\run-local-memory.ps1
```

**Run diagnostics:**
```powershell
python diagnose.py
```

## 🎯 Why This Fixes "Bin Not found"

The error occurred because:
1. Without proper configuration, bins were stored in memory
2. Authentication wasn't working correctly
3. Sessions weren't persisting

With PostgreSQL:
- ✅ Bins are stored in database
- ✅ Sessions are properly managed
- ✅ Authentication works correctly
- ✅ Data persists across restarts
