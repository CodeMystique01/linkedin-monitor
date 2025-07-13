# LinkedIn Mention Monitor

A Python-based tool that monitors LinkedIn for tags and mentions of specified terms and sends alerts to a Slack channel.

## Features

- 🔍 **Automated monitoring** of LinkedIn for tags and mentions
- 📱 **Slack integration** with rich message formatting
- 🔄 **Duplicate detection** to avoid spam alerts
- 📊 **Comprehensive logging** for monitoring and debugging
- ⚙️ **Configurable** search terms, intervals, and settings
- 💾 **Persistent storage** of seen URLs across restarts

## Prerequisites

- Python 3.7 or higher
- SerpAPI account (free tier available)
- Slack workspace with Incoming Webhooks app

## Quick Start

### 1. Clone/Download the Project
```bash
# Clone the repository
git clone <your-repository-url>
cd linkedin-monitor

# Or download and extract the ZIP file
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Copy the example configuration file:
```bash
cp config.env.example .env
```

Edit the `.env` file with your API credentials:

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

### 4. Get Your API Keys

#### SerpAPI Key
1. Go to [https://serpapi.com/](https://serpapi.com/)
2. Sign up for a free account
3. Copy your API key from the dashboard

#### Slack Webhook URL
1. Go to your Slack workspace
2. Navigate to Apps → Search for "Incoming Webhooks"
3. Add the app to your workspace
4. Choose the channel where you want alerts
5. Copy the webhook URL

### 5. Run the Monitor
```bash
python linkedin_monitor.py
```

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `SEARCH_TERMS` | `YourName,YourCompany` | Comma-separated list of terms to monitor |
| `CHECK_INTERVAL_MINUTES` | `30` | How often to check for new mentions (in minutes) |
| `MAX_RESULTS_PER_SEARCH` | `10` | Maximum results to fetch per search |

## How It Works

1. **Search**: Uses SerpAPI to search Google for LinkedIn pages containing your keywords
2. **Filter**: Checks for new URLs that haven't been seen before
3. **Alert**: Sends formatted Slack messages with mention details
4. **Store**: Saves seen URLs to avoid duplicate alerts

## Sample Slack Alert

The tool sends rich Slack messages with:
- 🔔 Alert icon and title
- 📄 LinkedIn post title and link
- 📝 Post snippet/description
- 🏷️ Tagged/mentioned term that triggered the alert
- ⏰ Detection timestamp
- 🎨 LinkedIn blue color theme

## Logging

The tool creates detailed logs in `linkedin_monitor.log` including:
- Search operations and results
- Slack alert attempts
- Error messages and debugging info
- System status updates

## Troubleshooting

### Common Issues

1. **"SERPAPI_KEY not found"**
   - Make sure you've added your SerpAPI key to the `.env` file

2. **"SLACK_WEBHOOK_URL not found"**
   - Verify your Slack webhook URL is correct in the `.env` file

3. **No alerts being sent**
   - Check the logs for error messages
   - Verify your Slack webhook is working
   - Ensure your search terms are being found

4. **Too many duplicate alerts**
   - The tool automatically tracks seen URLs
   - Check if `seen_urls.json` is being created properly

### Debug Mode

For more detailed logging, you can modify the logging level in `linkedin_monitor.py`:

```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## Cost Considerations

- **SerpAPI**: Free tier includes 100 searches/month
- **Slack**: Incoming Webhooks are free
- **Hosting**: Can run locally or on a cloud service

## Advanced Usage

### Custom Search Terms
Edit the `.env` file to add more terms:
```env
SEARCH_TERMS=YourName,YourCompany,YourProduct,YourBrand
```

### Different Check Intervals
```env
CHECK_INTERVAL_MINUTES=1440  # Check once per day (24 hours)
CHECK_INTERVAL_MINUTES=720   # Check twice per day (12 hours)
CHECK_INTERVAL_MINUTES=60    # Check every hour
CHECK_INTERVAL_MINUTES=30    # Check every 30 minutes
```

### Running as a Service

#### Windows (Task Scheduler)
1. Create a batch file `run_monitor.bat`:
```batch
@echo off
cd /d "C:\path\to\linkedin-monitor"
python linkedin_monitor.py
```

2. Set up a Windows Task Scheduler task to run this batch file

#### Linux/Mac (systemd/cron)
Create a systemd service or cron job to run the script automatically.

## Security Notes

- Keep your `.env` file secure and never commit it to version control
- The `seen_urls.json` file contains URLs but no sensitive data
- Consider using environment variables for production deployments

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

---

**Built with ❤️ by [Bibhu Prasad Nayak](https://github.com/CodeMystique01)** 