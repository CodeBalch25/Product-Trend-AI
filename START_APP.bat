@echo off
echo ========================================
echo Starting Product Trend Automation
echo ========================================
echo.

cd /d "%~dp0"

echo Starting Docker containers...
docker compose up -d

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to start Docker containers
    echo Make sure Docker Desktop is running!
    echo.
    pause
    exit /b 1
)

echo.
echo Waiting for services to initialize...
timeout /t 15 /nobreak > nul

echo.
echo Initializing database...
docker compose exec -T backend python -c "from models.database import init_db; init_db()"

echo.
echo ========================================
echo Application Started Successfully!
echo ========================================
echo.
echo Frontend Dashboard: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press any key to open the dashboard in your browser...
pause > nul
start http://localhost:3000
