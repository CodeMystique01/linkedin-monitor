#!/usr/bin/env python3
"""
LinkedIn Notification Preferences Scraper
Connects to an existing browser session to scrape LinkedIn notification preferences
for mentions and sends the results to Slack.

Requirements:
- LinkedIn notifications page must be already open in browser
- Browser must be logged in to LinkedIn
- Chrome browser with remote debugging enabled

Usage:
1. Open Chrome with remote debugging: chrome --remote-debugging-port=9222
2. Navigate to https://www.linkedin.com/mypreferences/d/categories/notifications
3. Run this script

Built with ❤️ for monitoring LinkedIn notification preferences
"""

import os
import time
import json
import logging
import requests
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_notifications_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LinkedInNotificationsScraper:
    """Scrapes LinkedIn notification preferences and sends results to Slack"""
    
    def __init__(self, slack_webhook_url: str = None, debug_port: int = 9222):
        """
        Initialize the scraper
        
        Args:
            slack_webhook_url: Slack webhook URL for sending notifications
            debug_port: Chrome remote debugging port (default: 9222)
        """
        self.slack_webhook_url = slack_webhook_url or os.getenv('SLACK_WEBHOOK_URL')
        self.debug_port = debug_port
        self.driver = None
        
        if not self.slack_webhook_url:
            logger.warning("SLACK_WEBHOOK_URL not provided. Results will only be logged.")
    
    def connect_to_existing_browser(self) -> bool:
        """
        Connect to an existing Chrome browser session with remote debugging enabled
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Configure Chrome options to connect to existing session
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", f"localhost:{self.debug_port}")
            
            # Connect to the existing browser session
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info(f"Successfully connected to existing browser session on port {self.debug_port}")
            
            # Verify we can access the current page
            current_url = self.driver.current_url
            logger.info(f"Current page URL: {current_url}")
            
            return True
            
        except WebDriverException as e:
            logger.error(f"Failed to connect to browser session: {e}")
            logger.error("Make sure Chrome is running with: chrome --remote-debugging-port=9222")
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to browser: {e}")
            return False
    
    def navigate_to_notifications_page(self) -> bool:
        """
        Navigate to LinkedIn notifications preferences page if not already there
        
        Returns:
            bool: True if on correct page, False otherwise
        """
        try:
            target_url = "https://www.linkedin.com/mypreferences/d/categories/notifications"
            current_url = self.driver.current_url
            
            if target_url in current_url:
                logger.info("Already on LinkedIn notifications preferences page")
                return True
            
            logger.info(f"Navigating to notifications page from: {current_url}")
            self.driver.get(target_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check if we're on the right page
            if "mypreferences" in self.driver.current_url:
                logger.info("Successfully navigated to notifications preferences page")
                return True
            else:
                logger.error("Failed to navigate to notifications page - might need to log in")
                return False
                
        except TimeoutException:
            logger.error("Timeout waiting for notifications page to load")
            return False
        except Exception as e:
            logger.error(f"Error navigating to notifications page: {e}")
            return False
    
    def wait_for_page_load(self, timeout: int = 15) -> bool:
        """
        Wait for the notifications page to fully load
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            bool: True if page loaded successfully
        """
        try:
            # Wait for notifications settings to be present
            WebDriverWait(self.driver, timeout).until(
                lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 
                    "[data-test-id*='notification'], .notification-setting, .pv-notification-settings__item")) > 0
            )
            
            # Additional wait for dynamic content
            time.sleep(2)
            logger.info("Page fully loaded")
            return True
            
        except TimeoutException:
            logger.error("Timeout waiting for notifications settings to load")
            return False
        except Exception as e:
            logger.error(f"Error waiting for page load: {e}")
            return False
    
    def scrape_mentions_filters(self) -> List[Dict[str, str]]:
        """
        Scrape the mentions filters and their statuses from the page
        
        Returns:
            List of dictionaries containing filter names and statuses
        """
        filters = []
        
        try:
            # Common selectors for LinkedIn notification settings
            selectors = [
                # Updated selectors for LinkedIn's current design
                "[data-test-id*='notification-setting']",
                ".pv-notification-settings__item",
                ".notification-setting",
                "[data-control-name*='notification']",
                ".artdeco-list__item",
                "[class*='notification']",
                ".pvs-list__item"
            ]
            
            elements_found = []
            
            # Try different selectors to find notification elements
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        logger.info(f"Found {len(elements)} elements with selector: {selector}")
                        elements_found.extend(elements)
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            # Remove duplicates while preserving order
            seen = set()
            unique_elements = []
            for elem in elements_found:
                elem_id = elem.get_attribute('data-test-id') or elem.get_attribute('id') or str(hash(elem.text))
                if elem_id not in seen and elem.text.strip():
                    seen.add(elem_id)
                    unique_elements.append(elem)
            
            logger.info(f"Processing {len(unique_elements)} unique notification elements")
            
            for element in unique_elements:
                try:
                    filter_info = self._extract_filter_info(element)
                    if filter_info and 'mention' in filter_info['name'].lower():
                        filters.append(filter_info)
                        logger.info(f"Found mentions filter: {filter_info['name']} - {filter_info['status']}")
                    elif filter_info:
                        # Log all filters for debugging but only add mentions-related ones
                        logger.debug(f"Found filter: {filter_info['name']} - {filter_info['status']}")
                        # Include all notification filters for comprehensive monitoring
                        filters.append(filter_info)
                        
                except Exception as e:
                    logger.debug(f"Error processing element: {e}")
                    continue
            
            # If no specific mentions filters found, try to get all notification settings
            if not filters:
                logger.warning("No mentions filters found, attempting to scrape all notification settings")
                filters = self._scrape_all_notification_settings()
            
            logger.info(f"Successfully scraped {len(filters)} notification filters")
            return filters
            
        except Exception as e:
            logger.error(f"Error scraping mentions filters: {e}")
            return []
    
    def _extract_filter_info(self, element) -> Optional[Dict[str, str]]:
        """
        Extract filter name and status from a notification setting element
        
        Args:
            element: Selenium WebElement
            
        Returns:
            Dictionary with name and status, or None if extraction fails
        """
        try:
            # Get text content
            element_text = element.text.strip()
            if not element_text:
                return None
            
            # Look for toggle switches or status indicators
            toggle_selectors = [
                "input[type='checkbox']",
                "[role='switch']",
                ".artdeco-toggle",
                "[data-test-id*='toggle']",
                ".toggle",
                "button[aria-pressed]"
            ]
            
            status = "Unknown"
            
            # Check for toggle elements
            for selector in toggle_selectors:
                toggles = element.find_elements(By.CSS_SELECTOR, selector)
                for toggle in toggles:
                    if toggle.get_attribute('checked') == 'true' or toggle.get_attribute('aria-pressed') == 'true':
                        status = "Enabled"
                        break
                    elif toggle.get_attribute('checked') == 'false' or toggle.get_attribute('aria-pressed') == 'false':
                        status = "Disabled"
                        break
                    elif 'checked' in toggle.get_attribute('class') or 'enabled' in toggle.get_attribute('class'):
                        status = "Enabled"
                        break
                if status != "Unknown":
                    break
            
            # If no toggle found, look for text indicators
            if status == "Unknown":
                text_lower = element_text.lower()
                if 'on' in text_lower or 'enabled' in text_lower or 'yes' in text_lower:
                    status = "Enabled"
                elif 'off' in text_lower or 'disabled' in text_lower or 'no' in text_lower:
                    status = "Disabled"
            
            # Extract filter name (remove status text)
            filter_name = element_text
            for status_word in ['On', 'Off', 'Enabled', 'Disabled', 'Yes', 'No']:
                filter_name = filter_name.replace(status_word, '').strip()
            
            # Clean up the filter name
            filter_name = ' '.join(filter_name.split())
            
            if filter_name:
                return {
                    'name': filter_name,
                    'status': status
                }
            
            return None
            
        except Exception as e:
            logger.debug(f"Error extracting filter info: {e}")
            return None
    
    def _scrape_all_notification_settings(self) -> List[Dict[str, str]]:
        """
        Fallback method to scrape all visible notification settings
        
        Returns:
            List of dictionaries containing filter names and statuses
        """
        filters = []
        
        try:
            # Try to find any elements that might contain notification settings
            all_elements = self.driver.find_elements(By.CSS_SELECTOR, "*")
            
            for element in all_elements:
                try:
                    text = element.text.strip()
                    if text and len(text) < 200 and any(keyword in text.lower() for keyword in 
                        ['notification', 'mention', 'tag', 'comment', 'message', 'email', 'push']):
                        
                        filter_info = self._extract_filter_info(element)
                        if filter_info and filter_info not in filters:
                            filters.append(filter_info)
                            
                except Exception:
                    continue
            
            return filters
            
        except Exception as e:
            logger.error(f"Error in fallback scraping: {e}")
            return []
    
    def send_to_slack(self, filters: List[Dict[str, str]]) -> bool:
        """
        Send the scraped filters to Slack
        
        Args:
            filters: List of filter dictionaries
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.slack_webhook_url:
            logger.warning("No Slack webhook URL configured")
            return False
        
        if not filters:
            logger.warning("No filters to send to Slack")
            return False
        
        try:
            # Format the message
            filter_lines = []
            for filter_item in filters:
                filter_lines.append(f"• {filter_item['name']}: {filter_item['status']}")
            
            message = {
                "text": "🔔 *LinkedIn Notification Preferences - Mentions Filters*",
                "attachments": [
                    {
                        "color": "#0077B5",  # LinkedIn blue
                        "title": "Current Filter Status",
                        "text": "\n".join(filter_lines),
                        "fields": [
                            {
                                "title": "Total Filters",
                                "value": str(len(filters)),
                                "short": True
                            },
                            {
                                "title": "Scraped At",
                                "value": time.strftime("%Y-%m-%d %H:%M:%S"),
                                "short": True
                            }
                        ],
                        "footer": "LinkedIn Notifications Scraper",
                        "footer_icon": "https://cdn-icons-png.flaticon.com/512/174/174857.png"
                    }
                ]
            }
            
            # Send to Slack
            response = requests.post(
                self.slack_webhook_url,
                json=message,
                timeout=10
            )
            response.raise_for_status()
            
            logger.info(f"Successfully sent {len(filters)} filters to Slack")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending to Slack: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending to Slack: {e}")
            return False
    
    def send_individual_filters_to_slack(self, filters: List[Dict[str, str]]) -> bool:
        """
        Send each filter individually to Slack
        
        Args:
            filters: List of filter dictionaries
            
        Returns:
            bool: True if all sent successfully, False if any failed
        """
        if not self.slack_webhook_url:
            logger.warning("No Slack webhook URL configured")
            return False
        
        if not filters:
            logger.warning("No filters to send to Slack")
            return False
        
        success_count = 0
        
        for filter_item in filters:
            try:
                message = {
                    "text": f"🔔 *LinkedIn Notification Filter*\n{filter_item['name']}: {filter_item['status']}"
                }
                
                response = requests.post(
                    self.slack_webhook_url,
                    json=message,
                    timeout=10
                )
                response.raise_for_status()
                
                logger.info(f"Sent to Slack: {filter_item['name']}: {filter_item['status']}")
                success_count += 1
                
                # Small delay between messages to avoid rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error sending filter '{filter_item['name']}' to Slack: {e}")
        
        logger.info(f"Successfully sent {success_count}/{len(filters)} filters to Slack")
        return success_count == len(filters)
    
    def close(self):
        """Close the browser connection"""
        if self.driver:
            try:
                # Don't quit the driver as we're using an existing session
                # Just detach from it
                logger.info("Disconnecting from browser session")
            except Exception as e:
                logger.error(f"Error closing browser connection: {e}")
    
    def run(self, send_individual: bool = True) -> List[Dict[str, str]]:
        """
        Main method to run the scraper
        
        Args:
            send_individual: Whether to send each filter individually to Slack
            
        Returns:
            List of scraped filters
        """
        filters = []
        
        try:
            # Connect to existing browser
            if not self.connect_to_existing_browser():
                logger.error("Failed to connect to browser. Make sure Chrome is running with remote debugging.")
                return filters
            
            # Navigate to notifications page if needed
            if not self.navigate_to_notifications_page():
                logger.error("Failed to navigate to notifications page")
                return filters
            
            # Wait for page to load
            if not self.wait_for_page_load():
                logger.error("Page failed to load properly")
                return filters
            
            # Scrape the filters
            filters = self.scrape_mentions_filters()
            
            if not filters:
                logger.warning("No filters were scraped")
                return filters
            
            # Log results
            logger.info("=== SCRAPED FILTERS ===")
            for filter_item in filters:
                logger.info(f"{filter_item['name']}: {filter_item['status']}")
            
            # Send to Slack
            if send_individual:
                self.send_individual_filters_to_slack(filters)
            else:
                self.send_to_slack(filters)
            
            return filters
            
        except Exception as e:
            logger.error(f"Error running scraper: {e}")
            return filters
        
        finally:
            self.close()


def main():
    """Main function"""
    
    # Configuration
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', 'YOUR_WEBHOOK_URL_HERE')
    DEBUG_PORT = int(os.getenv('CHROME_DEBUG_PORT', '9222'))
    SEND_INDIVIDUAL = os.getenv('SEND_INDIVIDUAL', 'true').lower() == 'true'
    
    logger.info("Starting LinkedIn Notifications Scraper...")
    logger.info("Make sure you have:")
    logger.info("1. Chrome running with: chrome --remote-debugging-port=9222")
    logger.info("2. LinkedIn notifications page open and logged in")
    logger.info("3. SLACK_WEBHOOK_URL configured")
    
    try:
        scraper = LinkedInNotificationsScraper(
            slack_webhook_url=SLACK_WEBHOOK_URL,
            debug_port=DEBUG_PORT
        )
        
        filters = scraper.run(send_individual=SEND_INDIVIDUAL)
        
        if filters:
            logger.info(f"Successfully scraped {len(filters)} notification filters")
            print("\n=== RESULTS ===")
            for filter_item in filters:
                print(f"{filter_item['name']}: {filter_item['status']}")
        else:
            logger.warning("No filters were scraped. Check the logs for errors.")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("Scraper stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
