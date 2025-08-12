# LinkedIn Monitor - Modern Web Application

A modern React-based LinkedIn monitoring application with FastAPI backend that tracks mentions and tags across LinkedIn.

## 🚀 Quick Start

### Option 1: Docker (Recommended)

The easiest way to run the entire application:

```bash
# 1. Clone or navigate to the project directory
cd linkedin-monitor

# 2. Copy environment configuration
cp config.env.example .env

# 3. Edit .env with your API keys
notepad .env  # On Windows
# nano .env   # On Linux/Mac

# 4. Run with Docker Compose
docker-compose up -d

# 5. Open your browser
# http://localhost:8000
```

### Option 2: Manual Setup (Development)

For development or if you prefer manual setup:

#### Backend Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install backend dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt

# 4. Configure environment variables
cp config.env.example .env
# Edit .env with your API keys

# 5. Start the backend server
cd backend
python app.py
```

#### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm start

# Frontend will run on http://localhost:3000
# Backend API runs on http://localhost:8000
```

## 🔧 Configuration

### Required API Keys

1. **SerpAPI Key** (for Google search functionality)
   - Sign up at [serpapi.com](https://serpapi.com/)
   - Copy your API key

2. **Slack Webhook URL** (for notifications)
   - Go to your Slack workspace
   - Add "Incoming Webhooks" app
   - Copy the webhook URL

### Environment Variables

Edit your `.env` file:

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

## 🌐 Web Interface

Once running, access the web interface at `http://localhost:8000`:

### Dashboard
- **Real-time monitoring status**
- **Quick action buttons** (Start/Stop monitoring, Manual check, Run scraper)
- **Configuration overview**
- **Recent mentions display**

### Configuration Page
- **Search terms management**
- **API key configuration**
- **Monitoring parameters**
- **Real-time status indicators**

### Mentions Page
- **View all mentions and tags**
- **Filter by type and date**
- **Detailed mention information**
- **Mention history management**

### Logs Page
- **Real-time log viewing**
- **Filter by log level** (Error, Warning, Info, Debug)
- **Auto-refresh capability**
- **System monitoring**

## 🔄 Running Modes

### 1. Full Web Application (Recommended)
```bash
docker-compose up -d
```
- Complete web interface
- Background monitoring
- API endpoints
- Real-time updates

### 2. API Server Only
```bash
cd backend
python app.py
```
- REST API endpoints
- No web interface
- Programmatic access

### 3. Legacy Scripts (Original functionality)
```bash
# Search-based monitoring
python linkedin_monitor.py

# Selenium-based scraping
python linkedin_mentions_scraper.py
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose build --no-cache
docker-compose up -d

# Production with nginx
docker-compose --profile production up -d
```

## 📱 Mobile Support

The web interface is fully responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones

## 🔐 Security Notes

- Keep your `.env` file secure
- Never commit API keys to version control
- Use HTTPS in production
- Consider using environment-specific configurations

## 🚨 Troubleshooting

### Common Issues

1. **Port 8000 already in use**
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8001:8000"
   ```

2. **Frontend not loading**
   - Check if backend is running on port 8000
   - Verify Docker containers are running: `docker-compose ps`

3. **API keys not working**
   - Verify `.env` file format
   - Check for trailing spaces
   - Restart containers after changes

4. **Selenium Chrome issues**
   - Chrome must be running with debug port for scraper
   - Run: `start_chrome_debug.bat` (Windows)

### Getting Help

1. Check logs: `docker-compose logs -f`
2. Verify configuration in web interface
3. Check GitHub issues for known problems
4. Review environment variable setup

## 🔄 Updates

To update the application:

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📊 Features

### ✅ Monitoring
- [x] Real-time LinkedIn mention tracking
- [x] Automated search with SerpAPI
- [x] Selenium-based direct scraping
- [x] Duplicate detection
- [x] Configurable search terms

### ✅ Notifications
- [x] Slack integration
- [x] Rich message formatting
- [x] Real-time alerts
- [x] Webhook support

### ✅ Web Interface
- [x] Modern React frontend
- [x] Real-time dashboard
- [x] Configuration management
- [x] Mention history
- [x] System logs viewing
- [x] Mobile responsive design

### ✅ Deployment
- [x] Docker containerization
- [x] Docker Compose setup
- [x] Nginx reverse proxy
- [x] Health checks
- [x] Auto-restart policies

---

**Happy Monitoring! 🚀**
