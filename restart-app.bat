@echo off
echo ========================================
echo Restarting Product Trend Automation
echo ========================================
echo.
echo Restarting all containers...
docker compose restart
echo.
echo Waiting for services to stabilize...
timeout /t 10 /nobreak > nul
echo.
echo ========================================
echo Application restarted successfully!
echo ========================================
echo.
echo Your updates are now live:
echo - Groq AI enabled (FREE & FAST)
echo - Hugging Face enabled (FREE)
echo - All frontend pages working
echo.
echo Dashboard: http://localhost:3000
echo API: http://localhost:8000
echo.
pause
