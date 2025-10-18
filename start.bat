@echo off
echo ========================================
echo Product Trend Automation System
echo ========================================
echo.

echo Checking if .env file exists...
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your API keys before continuing!
    echo Press any key to open .env file in notepad...
    pause
    notepad .env
    echo.
)

echo Starting Docker containers...
docker-compose up -d

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak

echo.
echo Initializing database...
docker-compose exec backend python -c "from models.database import init_db; init_db()"

echo.
echo ========================================
echo Application started successfully!
echo ========================================
echo.
echo Frontend Dashboard: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
echo.
pause
