# LinkedIn Monitor - Modern Web Application 🚀

A comprehensive LinkedIn monitoring solution with a modern React frontend, FastAPI backend, and real-time dashboard for tracking mentions and tags across LinkedIn.

## ✨ Features

### 🖥️ Modern Web Interface
- **Real-time Dashboard** with live monitoring status
- **Configuration Management** with intuitive UI
- **Mention History** with filtering and search
- **System Logs** with real-time viewing
- **Mobile Responsive** design for all devices

### 🔍 Advanced Monitoring
- **Automated monitoring** of LinkedIn for tags and mentions
- **Dual approach**: SerpAPI search + Selenium scraping
- **Real-time alerts** via Slack integration
- **Duplicate detection** to avoid spam alerts
- **Configurable** search terms, intervals, and settings

### 🚀 Easy Deployment
- **Docker containerization** for easy setup
- **One-command deployment** with Docker Compose
- **Auto-restart policies** for reliability
- **Health checks** for monitoring
- **Nginx reverse proxy** ready for production

## 🎯 Quick Start

### Option 1: Docker (Recommended) 🐳

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/linkedin-monitor.git
cd linkedin-monitor

# 2. Configure your settings
cp config.env.example .env
# Edit .env with your API keys (see Configuration section)

# 3. Run the application
docker-compose up -d

# 4. Open your browser
# http://localhost:8000
```

### Option 2: Manual Setup (Development) 🛠️

#### Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt

# Configure environment
cp config.env.example .env
# Edit .env with your API keys

# Start backend
cd backend && python app.py
```

#### Frontend Setup
```bash
# Install and start frontend
cd frontend
npm install
npm start
```

## ⚙️ Configuration

### Required API Keys

1. **SerpAPI Key** - Get from [serpapi.com](https://serpapi.com/) (free tier available)
2. **Slack Webhook URL** - Create in your Slack workspace settings

### Environment Variables (`.env`)

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