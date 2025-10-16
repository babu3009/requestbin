# Test script to run RequestBin with proper conda activation

# Set environment variables for PostgreSQL
$env:STORAGE_BACKEND = "requestbin.storage.postgresql.PostgreSQLStorage"
$env:POSTGRES_SCHEMA = "requestbin_app"
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_PORT = "55234"
$env:POSTGRES_DB = "gmImNcMNjRlT"
$env:POSTGRES_USER = "f21e30667747"
$env:POSTGRES_PASSWORD = "de9e43ee16df119956ce1db8582"
$env:ADMIN_EMAIL = "admin@requestbin.cfapps.eu10-004.hana.ondemand.com"
$env:ADMIN_PASSWORD = "ChangeMe123!"
$env:AUTO_APPROVE_DOMAINS = "tarento.com,ivolve.ai"
$env:FLASK_SESSION_SECRET_KEY = "3bb25fea945db5a13bd751fbcc34e90a2b1446b6334abe52606051df02448539"
$env:MAX_REQUESTS = "200"
$env:REALM = "local"

Write-Host "Testing user-specific bin history implementation..." -ForegroundColor Green

# Initialize conda for PowerShell
& C:\ProgramData\miniforge3\shell\condabin\conda-hook.ps1
conda activate requestbin

# Run the application
python web.py
