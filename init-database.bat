@echo off
echo Initializing database...
docker compose exec backend python -c "from models.database import init_db; init_db()"
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Database initialized successfully!
) else (
    echo.
    echo Failed to initialize database
)
pause
