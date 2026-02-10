@echo off
echo ========================================
echo Student Marketplace - Flask Application
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask application...
echo Application will be available at: http://localhost:5000
echo.
echo Press CTRL+C to stop the server
echo.

python app.py

pause
