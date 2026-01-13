@echo off
echo ========================================
echo   Himalayan Pet Studio - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Python found!
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created!
    echo.
) else (
    echo Virtual environment already exists.
    echo.
)

REM Activate virtual environment and install dependencies
echo Installing dependencies...
echo.
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r backend\requirements.txt

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure MySQL is running (XAMPP or standalone)
echo 2. Run migrations: python backend\manage.py migrate
echo 3. Create admin user: python backend\create_admin.py
echo 4. Double-click run.bat to start the server
echo.
pause
