@echo off
REM CanConnect Streamlit Setup Script for Windows

echo.
echo ===================================
echo CanConnect Streamlit Setup
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version

echo.
echo [2/4] Creating virtual environment...
python -m venv venv

echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [4/4] Installing dependencies...
pip install -r requirements.txt

echo.
echo ===================================
echo Setup Complete!
echo ===================================
echo.
echo Next steps:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate.bat
echo.
echo 2. Run the application:
echo    streamlit run app.py
echo.
echo 3. Make sure PostgreSQL is running before starting the app
echo.
pause
