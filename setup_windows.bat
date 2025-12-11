@echo off
echo ============================================
echo Notary Invoice Generator - Windows Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Install dependencies
echo Installing dependencies...
echo.
pip install -r requirements-windows.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies.
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo [SUCCESS] Setup completed!
echo ============================================
echo.
echo Next steps:
echo 1. Edit config.yaml with your business information
echo 2. Run: python example_usage_windows.py
echo    (This will create 3 sample invoices)
echo 3. Run: python invoice_generator_windows.py --interactive
echo    (This will let you create your own invoice)
echo.
echo For detailed instructions, see README_WINDOWS.md
echo.
pause
