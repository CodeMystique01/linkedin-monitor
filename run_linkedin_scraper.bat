@echo off
echo LinkedIn Notifications Scraper
echo ==============================
echo.
echo Make sure you have:
echo 1. Chrome running with: chrome --remote-debugging-port=9222
echo 2. LinkedIn notifications page open and logged in
echo 3. SLACK_WEBHOOK_URL configured in config.env
echo.
pause
echo.
echo Starting scraper...
python linkedin_notifications_scraper.py
echo.
pause
