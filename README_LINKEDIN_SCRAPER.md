# LinkedIn Notifications Scraper

A Python script that connects to an existing browser session to scrape LinkedIn notification preferences for mentions and sends the results to Slack.

## 🚀 Features

- Connects to existing Chrome browser session (no re-authentication needed)
- Scrapes LinkedIn notification preferences for mentions and other filters
- Sends individual filter results to Slack via webhook
- Comprehensive logging and error handling
- Configurable via environment variables
- Works with LinkedIn's current interface

## 📋 Prerequisites

1. **Python 3.7+** with required packages
2. **Google Chrome** browser
3. **Active LinkedIn session** in Chrome
4. **Slack webhook URL** for notifications

## 🛠️ Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   - Copy `config.env.example` to `config.env`
   - Set your `SLACK_WEBHOOK_URL`
   - Optionally adjust `CHROME_DEBUG_PORT` (default: 9222)

## 🔧 Setup

### Step 1: Start Chrome with Remote Debugging

Start Chrome with remote debugging enabled:

**Windows:**
```cmd
chrome --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_debug"
```

**macOS:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_debug"
```

**Linux:**
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_debug"
```

### Step 2: Open LinkedIn Notifications Page

1. Navigate to LinkedIn and log in
2. Go to: `https://www.linkedin.com/mypreferences/d/categories/notifications`
3. Ensure the page is fully loaded

### Step 3: Configure Slack Webhook

1. Create a Slack app and incoming webhook
2. Add the webhook URL to your `config.env` file:
   ```
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```

## 🚀 Usage

### Method 1: Using Batch/PowerShell Scripts

**Windows (Command Prompt):**
```cmd
run_linkedin_scraper.bat
```

**Windows (PowerShell):**
```powershell
.\run_linkedin_scraper.ps1
```

### Method 2: Direct Python Execution

```bash
python linkedin_notifications_scraper.py
```

### Method 3: Programmatic Usage

```python
from linkedin_notifications_scraper import LinkedInNotificationsScraper

# Initialize scraper
scraper = LinkedInNotificationsScraper(
    slack_webhook_url="YOUR_WEBHOOK_URL",
    debug_port=9222
)

# Run scraping
filters = scraper.run(send_individual=True)

# Print results
for filter_item in filters:
    print(f"{filter_item['name']}: {filter_item['status']}")
```

## ⚙️ Configuration Options

Environment variables in `config.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `SLACK_WEBHOOK_URL` | Slack incoming webhook URL | Required |
| `CHROME_DEBUG_PORT` | Chrome remote debugging port | 9222 |
| `SEND_INDIVIDUAL` | Send each filter individually to Slack | true |

## 📝 Output Format

The script outputs filters in the format:
```
Filter Name: Status
```

Example:
```
Mentions of you: Enabled
Comments on your posts: Disabled
Tags in posts: Enabled
```

## 🔍 How It Works

1. **Browser Connection**: Connects to existing Chrome session using remote debugging
2. **Page Navigation**: Navigates to LinkedIn notifications preferences (if not already there)
3. **Element Detection**: Uses multiple CSS selectors to find notification settings
4. **Status Extraction**: Determines filter status from toggle states and text content
5. **Slack Integration**: Sends results to Slack via webhook
6. **Logging**: Comprehensive logging of all operations

## 🐛 Troubleshooting

### Common Issues

**"Failed to connect to browser session"**
- Ensure Chrome is running with `--remote-debugging-port=9222`
- Check if port 9222 is available
- Try a different port and update `CHROME_DEBUG_PORT`

**"No filters were scraped"**
- Ensure you're logged into LinkedIn
- Verify you're on the correct notifications page
- Check browser console for JavaScript errors
- Try refreshing the LinkedIn page

**"Timeout waiting for notifications settings"**
- Page may be loading slowly
- Try increasing the timeout in the script
- Check your internet connection
- Ensure LinkedIn is not blocking automated access

**Slack webhook errors**
- Verify your webhook URL is correct
- Check Slack app permissions
- Test webhook URL manually with curl

### Debug Mode

Enable debug logging by modifying the logging level:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Testing Webhook

Test your Slack webhook:
```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test message"}' \
  YOUR_WEBHOOK_URL
```

## 📊 LinkedIn Interface Changes

LinkedIn frequently updates their interface. If the scraper stops working:

1. Check the browser developer tools to inspect new element structures
2. Update CSS selectors in the `scrape_mentions_filters()` method
3. The script includes multiple fallback selectors for robustness

## 🔒 Security Considerations

- The script connects to an existing browser session (no credential storage)
- Webhook URLs should be kept secure
- Consider using environment variables for sensitive configuration
- Regular monitoring of LinkedIn's terms of service

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section
2. Review the logs in `linkedin_notifications_scraper.log`
3. Ensure all prerequisites are met
4. Test with a fresh Chrome session

---

**Note**: This tool is for personal use and monitoring your own LinkedIn notification preferences. Please respect LinkedIn's terms of service and use responsibly.
