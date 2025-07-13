#!/bin/bash

echo "🚀 LinkedIn Monitor - Unix/Linux/macOS Setup"
echo "============================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "📦 Installing dependencies..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error installing dependencies"
    exit 1
fi

echo
echo "⚙️ Setting up configuration..."
if [ ! -f .env ]; then
    if [ -f config.env.example ]; then
        cp config.env.example .env
        echo "✅ Configuration file created (.env)"
        echo "📝 Please edit .env file with your API keys:"
        echo "   - SERPAPI_KEY: Get from https://serpapi.com/"
        echo "   - SLACK_WEBHOOK_URL: Get from your Slack workspace"
        echo "   - SEARCH_TERMS: Add the terms you want to monitor"
    else
        echo "❌ config.env.example not found"
        exit 1
    fi
else
    echo "⚠️  .env file already exists. Skipping configuration setup."
fi

echo
echo "🎉 Setup complete!"
echo
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: python3 linkedin_monitor.py"
echo
echo "For help, see README.md" 