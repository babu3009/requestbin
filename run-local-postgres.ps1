# PowerShell script to run RequestBin locally with PostgreSQL
# This sets all necessary environment variables for PostgreSQL backend

Write-Host "🚀 Starting RequestBin with PostgreSQL backend..." -ForegroundColor Green
Write-Host ""

# Storage backend configuration
$env:STORAGE_BACKEND = "requestbin.storage.postgresql.PostgreSQLStorage"
$env:POSTGRES_SCHEMA = "requestbin_app"

# PostgreSQL connection settings
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_PORT = "55234"
$env:POSTGRES_DB = "gmImNcMNjRlT"
$env:POSTGRES_USER = "f21e30667747"
$env:POSTGRES_PASSWORD = "de9e43ee16df119956ce1db8582"

# Authentication configuration
$env:ADMIN_EMAIL = "admin@requestbin.cfapps.eu10-004.hana.ondemand.com"
$env:ADMIN_PASSWORD = "ChangeMe123!"
$env:AUTO_APPROVE_DOMAINS = "tarento.com,ivolve.ai"

# Session configuration
$env:FLASK_SESSION_SECRET_KEY = "3bb25fea945db5a13bd751fbcc34e90a2b1446b6334abe52606051df02448539"

# SMTP configuration for OTP (development mode - logs to console)
# Leave these unset to use console logging for OTP codes
# $env:SMTP_HOST = "smtp.gmail.com"
# $env:SMTP_PORT = "587"
# $env:SMTP_USER = "your-email@gmail.com"
# $env:SMTP_PASSWORD = "your-app-password"
# $env:SMTP_USE_TLS = "true"

# Application settings
$env:MAX_REQUESTS = "200"
$env:REALM = "local"

Write-Host "✅ Environment variables set:" -ForegroundColor Cyan
Write-Host "   STORAGE_BACKEND: $env:STORAGE_BACKEND"
Write-Host "   POSTGRES_SCHEMA: $env:POSTGRES_SCHEMA"
Write-Host "   POSTGRES_HOST: $env:POSTGRES_HOST"
Write-Host "   POSTGRES_DB: $env:POSTGRES_DB"
Write-Host "   POSTGRES_USER: $env:POSTGRES_USER"
Write-Host ""
Write-Host "⚠️  Make sure PostgreSQL is running and the schema is initialized!" -ForegroundColor Yellow
Write-Host "   To initialize schema: psql -h localhost -p 55234 -U f21e30667747 -d gmImNcMNjRlT -f schema.sql" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 Starting application on http://localhost:4000" -ForegroundColor Green
Write-Host ""

# Run the application
python web.py
