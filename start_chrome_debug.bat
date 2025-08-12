@echo off
echo Starting Chrome with Remote Debugging...
echo Port: 9222
echo Debug Directory: C:\temp\chrome_debug
echo.
echo Once Chrome opens:
echo 1. Navigate to LinkedIn and log in
echo 2. Go to: https://www.linkedin.com/mypreferences/d/categories/notifications
echo 3. Wait for the page to fully load
echo 4. Then run the LinkedIn scraper
echo.
start chrome --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_debug"
echo Chrome started with debugging enabled!
echo You can now run the scraper when ready.
pause
