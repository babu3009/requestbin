@echo off
REM Test the new split-panel inspect view

echo.
echo ========================================================================
echo Testing RequestBin Split-Panel Inspect View
echo ========================================================================
echo.

call C:\ProgramData\miniforge3\Scripts\activate.bat C:\ProgramData\miniforge3
call conda activate requestbin

python test_inspect_view.py

pause
