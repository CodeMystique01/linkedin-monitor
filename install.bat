@echo off
echo 🚀 LinkedIn Monitor - Windows Setup
echo ===================================
echo.

echo 📦 Installing dependencies...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Error installing dependencies
    pause
    exit /b 1
)

echo.
echo ⚙️ Setting up configuration...
if not exist .env (
    if exist config.env.example (
        copy config.env.example .env
        echo ✅ Configuration file created (.env)
        echo 📝 Please edit .env file with your API keys:
        echo    - SERPAPI_KEY: Get from https://serpapi.com/
        echo    - SLACK_WEBHOOK_URL: Get from your Slack workspace
        echo    - SEARCH_TERMS: Add the terms you want to monitor
    ) else (
        echo ❌ config.env.example not found
        pause
        exit /b 1
    )
) else (
    echo ⚠️  .env file already exists. Skipping configuration setup.
)

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Run: python linkedin_monitor.py
echo.
echo For help, see README.md
pause 