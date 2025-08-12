@echo off
echo Starting LinkedIn Monitor with Docker...
echo.

REM Check if Docker is running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not running.
    echo Please install Docker Desktop and make sure it's running.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file from template...
    copy "config.env.example" ".env"
    echo.
    echo IMPORTANT: Please edit .env file with your API keys before continuing.
    echo - Get SerpAPI key from https://serpapi.com/
    echo - Get Slack webhook URL from your Slack workspace
    echo.
    notepad .env
    echo.
    echo Press any key to continue after configuring your API keys...
    pause
)

echo Building and starting the application...
docker-compose up -d

if %errorlevel% equ 0 (
    echo.
    echo ✅ LinkedIn Monitor is starting up!
    echo.
    echo 🌐 Web Interface: http://localhost:8000
    echo 📊 API Documentation: http://localhost:8000/docs
    echo.
    echo Useful commands:
    echo   docker-compose logs -f    (View logs)
    echo   docker-compose down       (Stop application)
    echo   docker-compose ps         (Check status)
    echo.
    echo Opening web interface in 10 seconds...
    timeout /t 10 /nobreak >nul
    start http://localhost:8000
) else (
    echo.
    echo ❌ Failed to start the application.
    echo Check the error messages above and try again.
    pause
)

pause
