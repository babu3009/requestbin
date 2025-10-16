@echo off
REM Batch file to run RequestBin with PostgreSQL backend
REM This works better than PowerShell scripts for setting environment variables

echo ========================================================================
echo Starting RequestBin with PostgreSQL Backend
echo ========================================================================
echo.

REM Storage backend configuration
set STORAGE_BACKEND=requestbin.storage.postgresql.PostgreSQLStorage
set POSTGRES_SCHEMA=requestbin_app

REM PostgreSQL connection settings
set POSTGRES_HOST=localhost
set POSTGRES_PORT=55234
set POSTGRES_DB=gmImNcMNjRlT
set POSTGRES_USER=f21e30667747
set POSTGRES_PASSWORD=de9e43ee16df119956ce1db8582

REM Authentication configuration
set ADMIN_EMAIL=admin@requestbin.cfapps.eu10-004.hana.ondemand.com
set ADMIN_PASSWORD=ChangeMe123!
set AUTO_APPROVE_DOMAINS=tarento.com,ivolve.ai

REM Session configuration
set FLASK_SESSION_SECRET_KEY=3bb25fea945db5a13bd751fbcc34e90a2b1446b6334abe52606051df02448539

REM Application settings
set MAX_REQUESTS=200
set REALM=local

echo Environment variables set:
echo   STORAGE_BACKEND: PostgreSQL
echo   POSTGRES_HOST: %POSTGRES_HOST%
echo   POSTGRES_PORT: %POSTGRES_PORT%
echo   POSTGRES_DB: %POSTGRES_DB%
echo   POSTGRES_SCHEMA: %POSTGRES_SCHEMA%
echo.
echo Starting application on http://localhost:4000
echo Login with: admin@requestbin.cfapps.eu10-004.hana.ondemand.com / ChangeMe123!
echo.
echo ========================================================================
echo.

REM Initialize conda for batch (use miniforge3 path)
call C:\ProgramData\miniforge3\Scripts\activate.bat C:\ProgramData\miniforge3

REM Activate requestbin environment
call conda activate requestbin

REM Run the application
python web.py
