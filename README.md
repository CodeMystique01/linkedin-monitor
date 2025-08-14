# LinkedIn Mentions Scraper

A Python-based tool that scrapes LinkedIn mentions notifications and sends alerts to Slack with direct post links.

## 🌟 Features

- 🔍 **Real-time LinkedIn mention detection** - Connects to existing Chrome session 
- 📱 **Slack integration** - Rich messages with clickable post links
- 🔗 **Direct post links** - Navigate directly to mentions
- 🎯 **Smart parsing** - Extracts names, mention types, and URLs
- 💾 **No login required** - Uses existing authenticated browser session
- 🎨 **Web interface** - Simple control panel for running scraper

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Slack Webhook
Edit `config.env` with your Slack webhook URL:
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 3. Start Chrome with Debug Mode
```bash
# Windows
start_chrome_debug.bat

# The script will open Chrome with remote debugging enabled
```

### 4. Run the Scraper

**Option A: Command Line**
```bash
python linkedin_mentions_scraper.py
```

**Option B: Web Interface**
```bash
# Open in browser
start scraper_frontend.html
```

**Option C: Simple Runner**
```bash
python run_mentions_scraper.py
```

## 📋 Prerequisites

- Python 3.7+
- Chrome browser
- LinkedIn account (logged in)
- Slack workspace with incoming webhooks

## ⚙️ Configuration

### Slack Webhook Setup
1. Go to your Slack workspace
2. Add "Incoming Webhooks" app
3. Choose target channel
4. Copy webhook URL to `config.env`

### Environment Variables
```env
# Required
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Optional  
CHROME_DEBUG_PORT=9222
```

## 🎯 How It Works

1. **Chrome Debug Connection** - Connects to Chrome running with `--remote-debugging-port=9222`
2. **LinkedIn Navigation** - Automatically navigates to mentions notifications
3. **Mention Extraction** - Scrapes mention notifications and extracts:
   - Person's name who mentioned you
   - Type of mention (post/comment)
   - Direct link to the post/comment
4. **Slack Notifications** - Sends rich messages with clickable links

## 📊 Output Format

Each mention generates a Slack message like:
```
👤 John Doe mentioned you in a post
🔗 View the post on LinkedIn
[Clickable link to actual LinkedIn post]
```

## 🌐 Web Interface

The included `scraper_frontend.html` provides:
- **Control Panel** - Start/stop scraper with buttons
- **Real-time Results** - View mentions as they're found
- **System Status** - Monitor Chrome and Slack connections
- **Live Logs** - Watch scraper activity in real-time

## 📁 Project Structure

```
linkedin-mentions-scraper/
├── linkedin_mentions_scraper.py  # Main scraper script
├── run_mentions_scraper.py       # Simple runner
├── scraper_frontend.html         # Web control panel
├── start_chrome_debug.bat        # Chrome debug launcher
├── config.env                    # Configuration file
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🔧 Usage Examples

### Find All Current Mentions
```bash
python linkedin_mentions_scraper.py
```

### Run with Custom Webhook
```python
from linkedin_mentions_scraper import LinkedInMentionsScraper

scraper = LinkedInMentionsScraper(
    slack_webhook_url="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
)
mentions = scraper.run()
```

## 🚨 Troubleshooting

### Chrome Connection Issues
- Ensure Chrome is running with debug mode: `start_chrome_debug.bat`
- Check port 9222 is available
- Verify Chrome debug session in browser: `http://localhost:9222`

### LinkedIn Access Issues
- Make sure you're logged into LinkedIn
- Navigate to notifications page manually first
- Check for LinkedIn rate limiting

### Slack Integration Issues
- Verify webhook URL format
- Test webhook with curl or Postman
- Check Slack app permissions

## 🔐 Security Notes

- Keep `config.env` secure and never commit to version control
- LinkedIn credentials are never stored - uses existing browser session
- Webhook URLs should be treated as sensitive information

## 📈 Automation

For regular monitoring, you can:
- Set up Windows Task Scheduler to run the script periodically
- Use cron on Linux/Mac
- Run from the web interface manually when needed

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

See LICENSE file for details.

---

**Happy Monitoring! 🚀**

Made with ❤️ for LinkedIn power users