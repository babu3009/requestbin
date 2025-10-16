# Create Admin User Script for PostgreSQL Backend

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  Creating Admin User for RequestBin (PostgreSQL)" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan

# Set environment variables
$env:POSTGRES_SCHEMA = "requestbin_app"
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_PORT = "55234"
$env:POSTGRES_DB = "gmImNcMNjRlT"
$env:POSTGRES_USER = "f21e30667747"
$env:POSTGRES_PASSWORD = "de9e43ee16df119956ce1db8582"
$env:ADMIN_EMAIL = "admin@requestbin.cfapps.eu10-004.hana.ondemand.com"
$env:ADMIN_PASSWORD = "ChangeMe123!"

# Activate conda environment and run script
& C:\ProgramData\miniforge3\shell\condabin\conda-hook.ps1
conda activate requestbin

Write-Host ""
python create_admin.py

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  You can now login with:" -ForegroundColor Yellow
Write-Host "  Email:    admin@requestbin.cfapps.eu10-004.hana.ondemand.com" -ForegroundColor White
Write-Host "  Password: ChangeMe123!" -ForegroundColor White
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
