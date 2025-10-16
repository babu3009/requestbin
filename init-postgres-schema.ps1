# PowerShell script to initialize PostgreSQL schema for RequestBin
# This script creates the schema and all required tables

Write-Host "🐘 Initializing PostgreSQL Schema for RequestBin" -ForegroundColor Green
Write-Host "=" * 70

# Database connection details
$dbHost = "localhost"
$dbPort = "55234"
$dbName = "gmImNcMNjRlT"
$dbUser = "f21e30667747"
$dbPassword = "de9e43ee16df119956ce1db8582"

Write-Host ""
Write-Host "📊 Database Connection:" -ForegroundColor Cyan
Write-Host "   Host:     $dbHost"
Write-Host "   Port:     $dbPort"
Write-Host "   Database: $dbName"
Write-Host "   User:     $dbUser"
Write-Host "   Schema:   requestbin_app"
Write-Host ""

# Set password environment variable for psql
$env:PGPASSWORD = $dbPassword

Write-Host "🔧 Running Python schema initializer..." -ForegroundColor Yellow
Write-Host ""

# Run the Python schema initializer (doesn't require psql in PATH)
python init_postgres_schema.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "The Python script completed successfully!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "=" * 70
    Write-Host "❌ Schema initialization encountered an issue!" -ForegroundColor Red
    Write-Host "=" * 70
    Write-Host ""
    Write-Host "💡 Make sure:" -ForegroundColor Yellow
    Write-Host "   1. PostgreSQL is running"
    Write-Host "   2. psycopg2-binary is installed: pip install psycopg2-binary"
    Write-Host "   3. Connection details are correct"
    Write-Host ""
}

# No need to clear password as Python script handles it internally
