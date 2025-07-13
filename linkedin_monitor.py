#!/usr/bin/env python3
"""
LinkedIn Mention Monitor
Monitors LinkedIn for mentions of specified terms and sends alerts to Slack.
"""

import os
import time
import json
import logging
from datetime import datetime
from typing import List, Dict, Set
import requests
from dotenv import load_dotenv
import schedule

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LinkedInMonitor:
    def __init__(self):
        self.serpapi_key = os.getenv('SERPAPI_KEY')
        self.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        self.search_terms = os.getenv('SEARCH_TERMS', 'Apurv Bansal Zenskar,Apurv Bansal').split(',')
        self.check_interval = int(os.getenv('CHECK_INTERVAL_MINUTES', 1440))  # 24 hours = 1440 minutes
        self.max_results = int(os.getenv('MAX_RESULTS_PER_SEARCH', 10))
        
        # Store seen URLs to avoid duplicate alerts
        self.seen_urls: Set[str] = set()
        self.seen_urls_file = 'seen_urls.json'
        self.load_seen_urls()
        
        if not self.serpapi_key:
            raise ValueError("SERPAPI_KEY not found in environment variables")
        if not self.slack_webhook_url:
            raise ValueError("SLACK_WEBHOOK_URL not found in environment variables")
    
    def load_seen_urls(self):
        """Load previously seen URLs from file"""
        try:
            if os.path.exists(self.seen_urls_file):
                with open(self.seen_urls_file, 'r') as f:
                    self.seen_urls = set(json.load(f))
                logger.info(f"Loaded {len(self.seen_urls)} previously seen URLs")
        except Exception as e:
            logger.error(f"Error loading seen URLs: {e}")
    
    def save_seen_urls(self):
        """Save seen URLs to file"""
        try:
            with open(self.seen_urls_file, 'w') as f:
                json.dump(list(self.seen_urls), f)
        except Exception as e:
            logger.error(f"Error saving seen URLs: {e}")
    
    def search_linkedin(self, term: str) -> List[Dict]:
        """Search LinkedIn for mentions of the given term"""
        try:
            url = "https://serpapi.com/search"
            params = {
                "engine": "google",
                "q": f'"{term}" "linkedin.com/in/bibhu-prashad-nayak345" site:linkedin.com',
                "api_key": self.serpapi_key,
                "num": self.max_results,
                "gl": "us",  # Geographic location
                "hl": "en"  # Language
            }
            
            logger.info(f"Searching for term: {term}")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("organic_results", [])
            
            logger.info(f"Found {len(results)} results for '{term}'")
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching for '{term}': {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error searching for '{term}': {e}")
            return []
    
    def send_slack_alert(self, term: str, result: Dict):
        """Send alert to Slack"""
        try:
            title = result.get("title", "No title")
            link = result.get("link", "")
            snippet = result.get("snippet", "No description available")

            # Create a rich Slack message with the link as plain text
            message = {
                "text": f"🔔 *New LinkedIn tag/mention detected!*\n<{link}|View Post>\n{link}",
                "attachments": [
                    {
                        "color": "#0077B5",  # LinkedIn blue
                        "title": title,
                        "title_link": link,
                        "text": f"{snippet}\n\nLink: {link}",
                        "fields": [
                            {
                                "title": "Tagged/Mentioned",
                                "value": term,
                                "short": True
                            },
                            {
                                "title": "Detected At",
                                "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "short": True
                            }
                        ],
                        "footer": "LinkedIn Monitor",
                        "footer_icon": "https://cdn-icons-png.flaticon.com/512/174/174857.png"
                    }
                ]
            }

            response = requests.post(
                self.slack_webhook_url,
                json=message,
                timeout=10
            )
            response.raise_for_status()

            logger.info(f"Slack alert sent for '{term}' - {title} - {link}")

        except Exception as e:
            logger.error(f"Error sending Slack alert: {e}")

    def check_mentions(self):
        """Check for new mentions of all search terms"""
        logger.info("Starting LinkedIn mention check...")

        new_mentions = 0

        for term in self.search_terms:
            term = term.strip()
            if not term:
                continue

            results = self.search_linkedin(term)

            for result in results:
                link = result.get("link", "")
                if link and link not in self.seen_urls:
                    self.seen_urls.add(link)
                    logger.info(f"New mention for '{term}': {result.get('title', 'No title')} - {link}")
                    self.send_slack_alert(term, result)
                    new_mentions += 1

        # Save seen URLs after each check
        self.save_seen_urls()

        logger.info(f"Check complete. Found {new_mentions} new mentions.")
        return new_mentions
    
    def run_continuous(self):
        """Run the monitor continuously"""
        logger.info("Starting LinkedIn Monitor...")
        logger.info(f"Monitoring terms: {', '.join(self.search_terms)}")
        logger.info(f"Check interval: {self.check_interval} minutes")
        
        # Run initial check
        self.check_mentions()
        
        # Schedule regular checks
        schedule.every(self.check_interval).minutes.do(self.check_mentions)
        
        logger.info("Monitor is running. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute for scheduled tasks
        except KeyboardInterrupt:
            logger.info("Monitor stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

def main():
    """Main function"""
    try:
        monitor = LinkedInMonitor()
        monitor.run_continuous()
    except Exception as e:
        logger.error(f"Failed to start monitor: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 