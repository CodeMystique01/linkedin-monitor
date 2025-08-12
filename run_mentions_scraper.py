#!/usr/bin/env python3
"""
Simple runner script for LinkedIn Mentions Scraper
"""

from linkedin_mentions_scraper import LinkedInMentionsScraper
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

def main():
    """Run the mentions scraper with your Slack webhook URL"""
    
    # ====== CONFIGURATION ======
    # Replace this with your actual Slack webhook URL
    SLACK_WEBHOOK_URL = "YOUR_SLACK_WEBHOOK_URL_HERE"
    
    # Chrome debug port (default is 9222)
    DEBUG_PORT = 9222
    
    print("=== LinkedIn Mentions Scraper ===")
    print("Make sure:")
    print("1. Chrome is running with --remote-debugging-port=9222")
    print("2. You're logged into LinkedIn") 
    print("3. LinkedIn notifications page is open")
    print("4. You've set your Slack webhook URL below")
    print()
    
    if SLACK_WEBHOOK_URL == "YOUR_SLACK_WEBHOOK_URL_HERE":
        print("⚠️  Please edit this script and set your SLACK_WEBHOOK_URL")
        print("   You can get a webhook URL from: https://api.slack.com/messaging/webhooks")
        return 1
    
    # Create and run the scraper
    scraper = LinkedInMentionsScraper(
        slack_webhook_url=SLACK_WEBHOOK_URL,
        debug_port=DEBUG_PORT
    )
    
    mentions = scraper.run()
    
    if mentions:
        print(f"✅ Found and sent {len(mentions)} mentions to Slack!")
    else:
        print("ℹ️  No new mentions found")
    
    return 0

if __name__ == "__main__":
    exit(main())
