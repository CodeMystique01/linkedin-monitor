# LinkedIn Monitor - macOS Setup

A Python-based tool that monitors LinkedIn for tags and mentions of specified terms ("Apurv Bansal from Zenskar") and sends daily alerts to a Slack channel.

## 🍎 macOS Quick Start

### Prerequisites
- macOS 10.14 or later
- Python 3.7 or higher
- Terminal app (built into macOS)

### Installation

1. **Download the project files** to your Mac
2. **Open Terminal** (Applications → Utilities → Terminal)
3. **Navigate to the project folder**:
   ```bash
   cd /path/to/linkedin-monitor
   ```
4. **Run the setup script**:
   ```bash
   chmod +x setup_mac.sh
   ./setup_mac.sh
   ```

### Configuration

1. **Edit the `.env` file** with your API credentials:
   ```bash
   nano .env
   # or use any text editor you prefer
   ```

2. **Add your API keys**:
   ```env
   SERPAPI_KEY=your_serpapi_key_here
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```

### Testing

Test your setup:
```bash
python3 test_monitor.py
```

### Running the Monitor

Start the monitor:
```bash
python3 linkedin_monitor.py
```

## 🚀 Mac-Specific Features

- **Native Terminal Support**: Works with macOS Terminal
- **Python 3**: Uses `python3` command (standard on macOS)
- **Easy Setup**: One-command installation script
- **Background Running**: Can run in background with `nohup`

## 📱 Running in Background (Optional)

To run the monitor in the background:
```bash
nohup python3 linkedin_monitor.py > monitor.log 2>&1 &
```

To check if it's running:
```bash
ps aux | grep linkedin_monitor
```

To stop the background process:
```bash
pkill -f linkedin_monitor.py
```

## 🔧 Troubleshooting

### Python Issues
```bash
# Check Python version
python3 --version

# Install Python if needed (using Homebrew)
brew install python3
```

### Permission Issues
```bash
# Make setup script executable
chmod +x setup_mac.sh

# Run setup
./setup_mac.sh
```

### Package Installation Issues
```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Install packages
python3 -m pip install -r requirements.txt
```

## 📋 Files Included

- `linkedin_monitor.py` - Main monitoring script
- `setup_mac.sh` - macOS setup script
- `test_monitor.py` - Test configuration
- `requirements.txt` - Python dependencies
- `config.env.example` - Configuration template
- `README_MAC.md` - This file

## 🎯 What It Monitors

- **Apurv Bansal from Zenskar** specifically
- **LinkedIn tags and mentions** (`@bansalapurv`)
- **Profile links** (`linkedin.com/in/bansalapurv`)
- **Last 48 hours** of activity
- **Daily checks** (once per 24 hours)

## 💰 Cost

- **SerpAPI**: Free tier (100 searches/month)
- **Slack**: Free (Incoming Webhooks)
- **Hosting**: Run locally on your Mac

## 📞 Support

If you encounter issues:
1. Check the logs in `linkedin_monitor.log`
2. Run `python3 test_monitor.py` to verify setup
3. Ensure your API keys are correct in `.env` 