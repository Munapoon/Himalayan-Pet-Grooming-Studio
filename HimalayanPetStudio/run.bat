@echo off
echo ========================================
echo   Himalayan Pet Studio - Starting...
echo ========================================
echo.

REM Change to backend directory
cd /d "%~dp0backend"

REM Check if virtual environment exists
if not exist "..\\.venv\\Scripts\\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to install dependencies.
    pause
    exit /b 1
)

echo Starting Django development server...
echo.
echo Server will be available at: http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Run Django server with virtual environment
"..\.venv\Scripts\python.exe" manage.py runserver

pause
