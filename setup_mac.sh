#!/bin/bash

# LinkedIn Monitor Setup Script for macOS
echo "🔧 LinkedIn Monitor Setup for macOS"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7 or higher."
    echo "Download from: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install required packages
echo "Installing required packages..."
python3 -m pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp config.env.example .env
    echo "✅ .env file created from template"
    echo "⚠️  Please edit .env file with your actual API keys and webhook URLs"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your API keys:"
echo "   - Get SerpAPI key from: https://serpapi.com/"
echo "   - Get Slack webhook from your Slack workspace"
echo "2. Test the setup: python3 test_monitor.py"
echo "3. Run the monitor: python3 linkedin_monitor.py" 