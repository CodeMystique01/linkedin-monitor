@echo off
title LinkedIn Monitor - Setup
echo =========================================
echo    LinkedIn Monitor - Setup Wizard
echo =========================================
echo.

echo Checking prerequisites...

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found
    echo Please install Python 3.7+ from https://python.org/
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Python found
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Node.js not found (needed for frontend development)
    echo You can still use Docker mode
) else (
    echo ✅ Node.js found
)

REM Check Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Docker not found (needed for easy deployment)
    echo You can still run in development mode
) else (
    echo ✅ Docker found
)

echo.
echo Setting up configuration...

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy "config.env.example" ".env"
    echo ✅ Created .env file
) else (
    echo ✅ .env file already exists
)

echo.
echo Configuration required:
echo.
echo 1. SerpAPI Key (Required)
echo    - Sign up at https://serpapi.com/
echo    - Get your free API key
echo.
echo 2. Slack Webhook URL (Required)
echo    - Go to your Slack workspace
echo    - Add "Incoming Webhooks" app
echo    - Get the webhook URL
echo.
echo 3. Search Terms (Required)
echo    - Add terms you want to monitor
echo    - Separate with commas
echo.

set /p edit_config="Edit configuration now? (y/n): "
if /i "%edit_config%"=="y" (
    notepad .env
)

echo.
echo Setup complete! Choose how to run:
echo.
echo 1. Docker (Recommended - Easy setup)
echo 2. Development Mode (Frontend + Backend)
echo 3. Legacy Scripts (Original functionality)
echo.
set /p run_choice="Enter your choice (1-3): "

if "%run_choice%"=="1" (
    call run_docker.bat
) else if "%run_choice%"=="2" (
    call run_development.bat
) else if "%run_choice%"=="3" (
    call run_legacy.bat
) else (
    echo Invalid choice. Please run setup.bat again.
    pause
)

echo.
echo Setup wizard complete!
pause
