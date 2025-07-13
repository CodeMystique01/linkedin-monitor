# LinkedIn Monitor - Mac Installation Guide

A comprehensive guide to install and run the LinkedIn Monitor on macOS.

## 🍎 Prerequisites

- **macOS 10.15 (Catalina) or later**
- **Internet connection** for downloading dependencies
- **Terminal access** (built into macOS)

## 🚀 Quick Installation

### Method 1: Automated Setup (Recommended)

1. **Download the project:**
   ```bash
   git clone https://github.com/CodeMystique01/linkedin-monitor.git
   cd linkedin-monitor
   ```

2. **Run the automated installer:**
   ```bash
   chmod +x setup_mac.sh
   ./setup_mac.sh
   ```

3. **Configure your API keys:**
   ```bash
   nano .env
   # or open with any text editor
   ```

4. **Start the monitor:**
   ```bash
   ./run_monitor.sh
   ```

### Method 2: Manual Installation

If you prefer to install manually or the automated script doesn't work:

#### Step 1: Install Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install Python
```bash
brew install python@3.11
```

#### Step 3: Clone the Repository
```bash
git clone https://github.com/CodeMystique01/linkedin-monitor.git
cd linkedin-monitor
```

#### Step 4: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 5: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 6: Setup Configuration
```bash
cp config.env.example .env
# Edit .env with your API keys
```

## ⚙️ Configuration

### Required API Keys

1. **SerpAPI Key:**
   - Go to [https://serpapi.com/](https://serpapi.com/)
   - Sign up for a free account
   - Copy your API key from the dashboard

2. **Slack Webhook URL:**
   - Go to your Slack workspace
   - Navigate to Apps → Search for "Incoming Webhooks"
   - Add the app to your workspace
   - Choose the channel where you want alerts
   - Copy the webhook URL

### Edit Configuration File

```bash
# Open with nano
nano .env

# Or open with TextEdit
open -a TextEdit .env
```

Update the `.env` file with your API keys:

```env
# SerpAPI Configuration
SERPAPI_KEY=your_serpapi_key_here

# Slack Configuration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Monitoring Configuration
SEARCH_TERMS=YourName,YourCompany,YourProduct
CHECK_INTERVAL_MINUTES=30
MAX_RESULTS_PER_SEARCH=10
```

## 🎮 Running the Monitor

### Start the Monitor
```bash
./run_monitor.sh
```

### Run the Demo
```bash
./run_demo.sh
```

### Manual Commands
```bash
# Activate virtual environment
source venv/bin/activate

# Run the monitor
python3 linkedin_monitor.py

# Run the demo
python3 demo.py

# Deactivate virtual environment
deactivate
```

## 📱 Visualizations

### View Professional Data Flow
```bash
open professional_flow.html
```

### View Flowchart Animation
```bash
open flowchart.html
```

### View Original Visualization
```bash
open index.html
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "Permission denied" error
```bash
chmod +x setup_mac.sh
chmod +x run_monitor.sh
chmod +x run_demo.sh
```

#### 2. Python not found
```bash
# Install Python via Homebrew
brew install python@3.11

# Add to PATH (add to ~/.zshrc or ~/.bash_profile)
export PATH="/opt/homebrew/bin:$PATH"
```

#### 3. Virtual environment issues
```bash
# Remove and recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. API key errors
- Verify your SerpAPI key is correct
- Check your Slack webhook URL
- Ensure the `.env` file is in the project directory

#### 5. Network connectivity issues
```bash
# Test API connectivity
curl -I https://serpapi.com/
```

### Debug Mode

For detailed logging, edit `linkedin_monitor.py` and change:
```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## 🛠️ Advanced Setup

### Run as Background Service

#### Using launchd (Recommended)
1. Create a plist file:
```bash
cat > ~/Library/LaunchAgents/com.linkedin.monitor.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.linkedin.monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/path/to/your/linkedin-monitor/run_monitor.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/path/to/your/linkedin-monitor/monitor.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/your/linkedin-monitor/monitor_error.log</string>
</dict>
</plist>
EOF
```

2. Load the service:
```bash
launchctl load ~/Library/LaunchAgents/com.linkedin.monitor.plist
```

#### Using cron
```bash
# Edit crontab
crontab -e

# Add this line to run every 30 minutes
*/30 * * * * /path/to/your/linkedin-monitor/run_monitor.sh
```

### Custom Search Terms

Edit the `.env` file to add more search terms:
```env
SEARCH_TERMS=YourName,YourCompany,YourProduct,YourBrand,YourKeywords
```

### Different Check Intervals

```env
CHECK_INTERVAL_MINUTES=1440  # Check once per day (24 hours)
CHECK_INTERVAL_MINUTES=720   # Check twice per day (12 hours)
CHECK_INTERVAL_MINUTES=60    # Check every hour
CHECK_INTERVAL_MINUTES=30    # Check every 30 minutes
```

## 📊 Monitoring and Logs

### View Logs
```bash
# View monitor logs
tail -f linkedin_monitor.log

# View system logs (if using launchd)
tail -f ~/Library/Logs/com.linkedin.monitor.log
```

### Check Status
```bash
# Check if monitor is running
ps aux | grep linkedin_monitor

# Check virtual environment
which python3
```

## 🔒 Security Notes

- Keep your `.env` file secure and never commit it to version control
- The `seen_urls.json` file contains URLs but no sensitive data
- Consider using environment variables for production deployments
- Regularly update your dependencies: `pip install --upgrade -r requirements.txt`

## 📞 Support

If you encounter issues:

1. **Check the logs:** `tail -f linkedin_monitor.log`
2. **Run the demo:** `./run_demo.sh`
3. **Verify configuration:** Check your `.env` file
4. **Test connectivity:** Ensure internet access and API keys work

## 🎯 Quick Reference

| Command | Description |
|---------|-------------|
| `./setup_mac.sh` | Automated installation |
| `./run_monitor.sh` | Start the monitor |
| `./run_demo.sh` | Run the demo |
| `source venv/bin/activate` | Activate virtual environment |
| `deactivate` | Deactivate virtual environment |
| `open professional_flow.html` | View professional animation |
| `tail -f linkedin_monitor.log` | View live logs |

## 🚀 Next Steps

After installation:

1. **Test the setup:** Run `./run_demo.sh`
2. **Configure alerts:** Set up your Slack webhook
3. **Customize search terms:** Edit the `.env` file
4. **Monitor logs:** Check `linkedin_monitor.log`
5. **Share the project:** Star the repository on GitHub!

---

**Happy monitoring! 🎉** 