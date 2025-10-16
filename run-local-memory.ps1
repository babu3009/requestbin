# PowerShell script to run RequestBin locally with Memory backend (no database needed)
# This is simpler but data is lost when the application restarts

Write-Host "🚀 Starting RequestBin with Memory backend..." -ForegroundColor Green
Write-Host ""

# Storage backend configuration - use memory storage
$env:STORAGE_BACKEND = "requestbin.storage.memory.MemoryStorage"

# Authentication configuration
$env:ADMIN_EMAIL = "admin@requestbin.cfapps.eu10-004.hana.ondemand.com"
$env:ADMIN_PASSWORD = "ChangeMe123!"
$env:AUTO_APPROVE_DOMAINS = "tarento.com,ivolve.ai"

# Session configuration
$env:FLASK_SESSION_SECRET_KEY = "3bb25fea945db5a13bd751fbcc34e90a2b1446b6334abe52606051df02448539"

# Application settings
$env:MAX_REQUESTS = "200"
$env:REALM = "local"

Write-Host "✅ Environment variables set:" -ForegroundColor Cyan
Write-Host "   STORAGE_BACKEND: Memory (no database needed)"
Write-Host "   AUTO_APPROVE_DOMAINS: tarento.com, ivolve.ai"
Write-Host ""
Write-Host "ℹ️  Memory backend: All data will be lost when you stop the application" -ForegroundColor Yellow
Write-Host "ℹ️  OTP codes will be printed to console (no SMTP needed)" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 Starting application on http://localhost:4000" -ForegroundColor Green
Write-Host ""

# Run the application
python web.py
