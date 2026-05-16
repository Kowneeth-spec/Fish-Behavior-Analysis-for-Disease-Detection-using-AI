@echo off
REM Fish Behavior Analysis - Complete Demo Runner
REM Runs all setup, demo data generation, and tracking in one command

setlocal enabledelayedexpansion

set PYTHON=c:/Users/kowne/AppData/Local/Python/pythoncore-3.14-64/python.exe
set PROJECT_DIR=%cd%

echo.
echo ============================================================
echo  Fish Behavior Tracking System - Complete Demo
echo ============================================================
echo.

REM Step 1: Verify Dependencies
echo [STEP 1/3] Verifying dependencies...
echo ============================================================
%PYTHON% test_dependencies.py
if errorlevel 1 (
    echo ✗ Dependency check failed!
    exit /b 1
)
echo.

REM Step 2: Generate Demo Data
echo [STEP 2/3] Generating synthetic demo data...
echo ============================================================
%PYTHON% demo_setup.py
if errorlevel 1 (
    echo ✗ Demo setup failed!
    exit /b 1
)
echo.

REM Step 3: Run Tracker
echo [STEP 3/3] Running DeepSORT tracker on demo data...
echo ============================================================
%PYTHON% deep_sort_app.py ^
    --sequence_dir demo_data/sequences/test_sequence ^
    --detection_file demo_data/sequences/detections.npy ^
    --output_file demo_output.txt ^
    --display False
if errorlevel 1 (
    echo ✗ Tracker failed!
    exit /b 1
)
echo.

REM Display Results
echo [RESULTS] Tracking completed successfully!
echo ============================================================
echo Output file: demo_output.txt
echo.
echo First 15 tracking results:
echo ============================================================
powershell -Command "Get-Content demo_output.txt | Select-Object -First 15"
echo.
echo Last 5 tracking results:
echo ============================================================
powershell -Command "Get-Content demo_output.txt | Select-Object -Last 5"
echo.

REM Statistics
for /f %%A in ('Find /C /V "" ^< demo_output.txt') do set COUNT=%%A
echo Total tracked detections: !COUNT!
echo.

echo ============================================================
echo ✓ Demo run complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Examine tracking results in: demo_output.txt
echo   2. Request real fish video dataset from:
echo      https://docs.google.com/forms/d/e/1FAIpQLScHzbEzj97v6YZn3EdU8Pt4aMXj5cGPe4qJ05mQrM6df54tJg/viewform
echo   3. Place video sequences in: demo_data/sequences/
echo   4. Run tracker on real data with same command structure
echo.
echo ============================================================
