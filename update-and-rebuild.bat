@echo off
echo ========================================
echo Updating to REAL Products Scanner
echo ========================================
echo.
echo This will rebuild containers with:
echo - Real Amazon product scraping
echo - Google Trends integration (pytrends)
echo - Reddit trending products
echo - Groq AI analysis (already configured)
echo.
echo This may take 3-5 minutes...
echo.
pause
echo.
echo Rebuilding containers with new dependencies...
docker compose up -d --build
echo.
echo Waiting for services to start...
timeout /t 15 /nobreak > nul
echo.
echo ========================================
echo Update Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Open dashboard: http://localhost:3000
echo 2. Click "Scan Trends Now"
echo 3. Wait ~30 seconds
echo 4. Check "Pending Review" for REAL products!
echo.
echo You'll now see specific products like:
echo - Apple AirPods Pro - $249.99
echo - Instant Pot Duo - $89.99
echo - Kindle Paperwhite - $149.99
echo.
pause
