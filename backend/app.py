#!/usr/bin/env python3
"""
LinkedIn Monitor Backend API
FastAPI backend for the LinkedIn monitoring system
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Import our existing monitor classes
import sys
sys.path.append('..')
from linkedin_monitor import LinkedInMonitor
from linkedin_mentions_scraper import LinkedInMentionsScraper

# Load environment variables
load_dotenv()
load_dotenv('../config.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="LinkedIn Monitor API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class MonitorConfig(BaseModel):
    search_terms: List[str]
    check_interval: int
    max_results: int
    serpapi_key: Optional[str] = None
    slack_webhook_url: Optional[str] = None

class MonitorStatus(BaseModel):
    is_running: bool
    last_check: Optional[str]
    total_mentions: int
    seen_urls_count: int

class MentionResult(BaseModel):
    person_name: str
    mention_type: str
    formatted_message: str
    timestamp: str

# Global variables
monitor_instance = None
scraper_instance = None
monitoring_active = False
last_check_time = None
mention_history = []

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "LinkedIn Monitor API", "version": "1.0.0"}

@app.get("/api/status")
async def get_status():
    """Get current monitoring status"""
    global monitor_instance, monitoring_active, last_check_time
    
    seen_urls_count = 0
    if monitor_instance:
        seen_urls_count = len(monitor_instance.seen_urls)
    
    return MonitorStatus(
        is_running=monitoring_active,
        last_check=last_check_time,
        total_mentions=len(mention_history),
        seen_urls_count=seen_urls_count
    )

@app.get("/api/config")
async def get_config():
    """Get current configuration"""
    return {
        "search_terms": os.getenv('SEARCH_TERMS', 'YourName,YourCompany').split(','),
        "check_interval": int(os.getenv('CHECK_INTERVAL_MINUTES', 30)),
        "max_results": int(os.getenv('MAX_RESULTS_PER_SEARCH', 10)),
        "has_serpapi_key": bool(os.getenv('SERPAPI_KEY')),
        "has_slack_webhook": bool(os.getenv('SLACK_WEBHOOK_URL'))
    }

@app.post("/api/config")
async def update_config(config: MonitorConfig):
    """Update monitoring configuration"""
    try:
        # Update environment variables (for current session)
        if config.search_terms:
            os.environ['SEARCH_TERMS'] = ','.join(config.search_terms)
        
        os.environ['CHECK_INTERVAL_MINUTES'] = str(config.check_interval)
        os.environ['MAX_RESULTS_PER_SEARCH'] = str(config.max_results)
        
        if config.serpapi_key:
            os.environ['SERPAPI_KEY'] = config.serpapi_key
        
        if config.slack_webhook_url:
            os.environ['SLACK_WEBHOOK_URL'] = config.slack_webhook_url
        
        # Recreate monitor instance with new config
        global monitor_instance
        if monitor_instance:
            monitor_instance = LinkedInMonitor()
        
        return {"message": "Configuration updated successfully"}
    
    except Exception as e:
        logger.error(f"Error updating config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/monitor/start")
async def start_monitoring(background_tasks: BackgroundTasks):
    """Start the LinkedIn monitoring"""
    global monitor_instance, monitoring_active
    
    try:
        if monitoring_active:
            return {"message": "Monitoring is already active"}
        
        # Initialize monitor
        monitor_instance = LinkedInMonitor()
        monitoring_active = True
        
        # Start monitoring in background
        background_tasks.add_task(run_monitor_background)
        
        logger.info("LinkedIn monitoring started")
        return {"message": "Monitoring started successfully"}
    
    except Exception as e:
        logger.error(f"Error starting monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/monitor/stop")
async def stop_monitoring():
    """Stop the LinkedIn monitoring"""
    global monitoring_active
    
    monitoring_active = False
    logger.info("LinkedIn monitoring stopped")
    return {"message": "Monitoring stopped successfully"}

@app.post("/api/monitor/check")
async def manual_check():
    """Manually trigger a mention check"""
    global monitor_instance, last_check_time
    
    try:
        if not monitor_instance:
            monitor_instance = LinkedInMonitor()
        
        # Run check
        new_mentions = monitor_instance.check_mentions()
        last_check_time = datetime.now().isoformat()
        
        return {
            "message": f"Check completed. Found {new_mentions} new mentions",
            "new_mentions": new_mentions,
            "timestamp": last_check_time
        }
    
    except Exception as e:
        logger.error(f"Error during manual check: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scraper/run")
async def run_scraper():
    """Run the LinkedIn mentions scraper"""
    global scraper_instance, mention_history
    
    try:
        if not scraper_instance:
            scraper_instance = LinkedInMentionsScraper()
        
        mentions = scraper_instance.run()
        
        # Add to history
        for mention in mentions:
            mention_result = MentionResult(
                person_name=mention['person_name'],
                mention_type=mention['mention_type'],
                formatted_message=mention['formatted_message'],
                timestamp=datetime.now().isoformat()
            )
            mention_history.append(mention_result.dict())
        
        return {
            "message": f"Scraper completed. Found {len(mentions)} mentions",
            "mentions": mentions,
            "total_mentions": len(mention_history)
        }
    
    except Exception as e:
        logger.error(f"Error running scraper: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mentions")
async def get_mentions(limit: int = 50):
    """Get recent mentions"""
    global mention_history
    
    # Return the most recent mentions
    recent_mentions = mention_history[-limit:] if len(mention_history) > limit else mention_history
    return {
        "mentions": recent_mentions,
        "total": len(mention_history)
    }

@app.delete("/api/mentions")
async def clear_mentions():
    """Clear mention history"""
    global mention_history
    
    mention_history.clear()
    return {"message": "Mention history cleared"}

@app.get("/api/logs")
async def get_logs(lines: int = 100):
    """Get recent log entries"""
    try:
        log_files = ['backend.log', '../linkedin_monitor.log', '../linkedin_mentions_scraper.log']
        all_logs = []
        
        for log_file in log_files:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = f.readlines()
                    recent_logs = logs[-lines:] if len(logs) > lines else logs
                    for log in recent_logs:
                        all_logs.append({"file": log_file, "line": log.strip()})
        
        # Sort by timestamp (rough sort)
        all_logs.sort(key=lambda x: x['line'][:19] if len(x['line']) > 19 else x['line'])
        
        return {"logs": all_logs[-lines:]}
    
    except Exception as e:
        logger.error(f"Error reading logs: {e}")
        return {"logs": [], "error": str(e)}

async def run_monitor_background():
    """Background task to run the monitor"""
    global monitor_instance, monitoring_active, last_check_time
    
    while monitoring_active:
        try:
            if monitor_instance:
                new_mentions = monitor_instance.check_mentions()
                last_check_time = datetime.now().isoformat()
                logger.info(f"Background check completed. Found {new_mentions} new mentions")
            
            # Wait for the configured interval
            import asyncio
            await asyncio.sleep(monitor_instance.check_interval * 60 if monitor_instance else 1800)  # Default 30 minutes
        
        except Exception as e:
            logger.error(f"Error in background monitoring: {e}")
            await asyncio.sleep(300)  # Wait 5 minutes before retrying

# Serve static files (React frontend)
app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
