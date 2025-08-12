@echo off
echo Starting LinkedIn Monitor (Legacy Scripts)...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file from template...
    copy "config.env.example" ".env"
    echo.
    echo Please edit .env file with your API keys.
    notepad .env
    pause
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Choose which script to run:
echo 1. LinkedIn Monitor (SerpAPI-based search)
echo 2. LinkedIn Mentions Scraper (Selenium-based)
echo 3. Both (parallel execution)
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Starting LinkedIn Monitor...
    python linkedin_monitor.py
) else if "%choice%"=="2" (
    echo Starting LinkedIn Mentions Scraper...
    echo Make sure Chrome is running with debug port!
    echo Run start_chrome_debug.bat first if needed.
    pause
    python linkedin_mentions_scraper.py
) else if "%choice%"=="3" (
    echo Starting both monitors...
    start /b python linkedin_monitor.py
    timeout /t 2 /nobreak >nul
    python linkedin_mentions_scraper.py
) else (
    echo Invalid choice. Running default monitor...
    python linkedin_monitor.py
)

pause
