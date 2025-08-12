#!/usr/bin/env python3
"""
Enhanced LinkedIn Notifications Scraper
Better handling of LinkedIn's current interface structure
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
        logging.FileHandler('enhanced_linkedin_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class EnhancedLinkedInScraper:
    """Enhanced LinkedIn notifications scraper with better element detection"""
    
    def __init__(self, slack_webhook_url: str = None, debug_port: int = 9222):
        self.slack_webhook_url = slack_webhook_url or os.getenv('SLACK_WEBHOOK_URL')
        self.debug_port = debug_port
        self.driver = None
        
        if not self.slack_webhook_url:
            logger.warning("SLACK_WEBHOOK_URL not provided. Results will only be logged.")
    
    def connect_to_browser(self) -> bool:
        """Connect to existing Chrome browser session"""
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", f"localhost:{self.debug_port}")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info(f"Connected to browser session on port {self.debug_port}")
            
            current_url = self.driver.current_url
            logger.info(f"Current page: {current_url}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to browser: {e}")
            return False
    
    def wait_and_scroll(self, timeout: int = 10):
        """Wait for page load and scroll to reveal all content"""
        try:
            # Wait for basic page structure
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Scroll down to load any lazy-loaded content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            logger.info("Page scrolled and ready for scraping")
            
        except Exception as e:
            logger.error(f"Error during page preparation: {e}")
    
    def find_notification_elements(self) -> List:
        """Find all potential notification-related elements using multiple strategies"""
        elements = []
        
        # Strategy 1: Look for elements with notification-related text
        try:
            all_elements = self.driver.find_elements(By.CSS_SELECTOR, "*")
            logger.info(f"Found {len(all_elements)} total elements on page")
            
            for element in all_elements:
                try:
                    text = element.text.strip()
                    if text and len(text) < 500:  # Reasonable length filter
                        text_lower = text.lower()
                        
                        # Check for notification-related keywords
                        notification_keywords = [
                            'mention', 'tag', 'comment', 'like', 'share', 'post',
                            'notification', 'email', 'push', 'mobile', 'weekly',
                            'recommendation', 'connection', 'message', 'invitation'
                        ]
                        
                        if any(keyword in text_lower for keyword in notification_keywords):
                            # Check if this element or its children contain toggles/switches
                            has_toggle = self._check_for_toggles(element)
                            
                            elements.append({
                                'element': element,
                                'text': text,
                                'has_toggle': has_toggle,
                                'tag': element.tag_name,
                                'classes': element.get_attribute('class') or '',
                                'data_test_id': element.get_attribute('data-test-id') or ''
                            })
                            
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"Error finding notification elements: {e}")
        
        logger.info(f"Found {len(elements)} potential notification elements")
        return elements
    
    def _check_for_toggles(self, element) -> bool:
        """Check if element contains toggle switches"""
        try:
            toggle_selectors = [
                "input[type='checkbox']",
                "button[role='switch']",
                "[class*='toggle']",
                "[class*='switch']",
                "button[aria-pressed]",
                ".artdeco-toggle"
            ]
            
            for selector in toggle_selectors:
                toggles = element.find_elements(By.CSS_SELECTOR, selector)
                if toggles:
                    return True
            
            return False
            
        except Exception:
            return False
    
    def extract_notification_settings(self, elements: List) -> List[Dict[str, str]]:
        """Extract notification settings from found elements"""
        settings = []
        processed_texts = set()  # Avoid duplicates
        
        for elem_info in elements:
            try:
                element = elem_info['element']
                text = elem_info['text']
                
                # Skip if we've already processed similar text
                text_key = text.lower().strip()
                if text_key in processed_texts:
                    continue
                processed_texts.add(text_key)
                
                # Try to determine the status
                status = self._determine_status(element)
                
                # Clean up the text to get filter name
                filter_name = self._clean_filter_name(text)
                
                if filter_name and len(filter_name) > 3:  # Minimum length filter
                    setting = {
                        'name': filter_name,
                        'status': status,
                        'element_info': f"{elem_info['tag']}.{elem_info['classes'][:50]}..."
                    }
                    settings.append(setting)
                    logger.info(f"Found setting: {filter_name} - {status}")
                
            except Exception as e:
                logger.debug(f"Error processing element: {e}")
                continue
        
        return settings
    
    def _determine_status(self, element) -> str:
        """Determine if a notification setting is enabled or disabled"""
        try:
            # Check for toggle elements and their states
            toggle_selectors = [
                "input[type='checkbox']",
                "button[role='switch']",
                "[aria-pressed]",
                "[class*='toggle']",
                "[class*='switch']"
            ]
            
            for selector in toggle_selectors:
                toggles = element.find_elements(By.CSS_SELECTOR, selector)
                for toggle in toggles:
                    # Check various attributes for state
                    if toggle.get_attribute('checked') == 'true':
                        return "Enabled"
                    elif toggle.get_attribute('checked') == 'false':
                        return "Disabled"
                    elif toggle.get_attribute('aria-pressed') == 'true':
                        return "Enabled"
                    elif toggle.get_attribute('aria-pressed') == 'false':
                        return "Disabled"
                    elif 'checked' in (toggle.get_attribute('class') or '').lower():
                        return "Enabled"
                    elif 'unchecked' in (toggle.get_attribute('class') or '').lower():
                        return "Disabled"
            
            # Check element text for status indicators
            text = element.text.lower()
            if any(word in text for word in ['on', 'enabled', 'yes', 'active']):
                return "Enabled"
            elif any(word in text for word in ['off', 'disabled', 'no', 'inactive']):
                return "Disabled"
            
            # Check parent/child elements
            try:
                parent = element.find_element(By.XPATH, "..")
                parent_text = parent.text.lower()
                if any(word in parent_text for word in ['on', 'enabled', 'yes']):
                    return "Enabled"
                elif any(word in parent_text for word in ['off', 'disabled', 'no']):
                    return "Disabled"
            except:
                pass
            
            return "Unknown"
            
        except Exception as e:
            logger.debug(f"Error determining status: {e}")
            return "Unknown"
    
    def _clean_filter_name(self, text: str) -> str:
        """Clean and extract filter name from element text"""
        try:
            # Remove common status words
            status_words = ['on', 'off', 'enabled', 'disabled', 'yes', 'no', 'active', 'inactive']
            
            lines = text.split('\n')
            # Usually the first line contains the filter name
            filter_name = lines[0].strip()
            
            # Remove status words
            words = filter_name.split()
            cleaned_words = [word for word in words if word.lower() not in status_words]
            
            cleaned_name = ' '.join(cleaned_words).strip()
            
            # Remove extra whitespace and common prefixes/suffixes
            cleaned_name = ' '.join(cleaned_name.split())
            
            return cleaned_name
            
        except Exception:
            return text.strip()
    
    def send_to_slack(self, settings: List[Dict[str, str]]) -> bool:
        """Send settings to Slack"""
        if not self.slack_webhook_url:
            return False
        
        if not settings:
            return False
        
        try:
            # Send individual messages for each setting
            success_count = 0
            
            for setting in settings:
                message = {
                    "text": f"🔔 *LinkedIn Notification Setting*\n{setting['name']}: {setting['status']}"
                }
                
                response = requests.post(
                    self.slack_webhook_url,
                    json=message,
                    timeout=10
                )
                response.raise_for_status()
                
                logger.info(f"Sent to Slack: {setting['name']}: {setting['status']}")
                success_count += 1
                
                # Small delay between messages
                time.sleep(1)
            
            logger.info(f"Successfully sent {success_count}/{len(settings)} settings to Slack")
            return success_count == len(settings)
            
        except Exception as e:
            logger.error(f"Error sending to Slack: {e}")
            return False
    
    def run(self) -> List[Dict[str, str]]:
        """Main method to run the enhanced scraper"""
        settings = []
        
        try:
            if not self.connect_to_browser():
                return settings
            
            # Wait and prepare page
            self.wait_and_scroll()
            
            # Find notification elements
            elements = self.find_notification_elements()
            
            if not elements:
                logger.warning("No notification elements found")
                return settings
            
            # Extract settings
            settings = self.extract_notification_settings(elements)
            
            if settings:
                logger.info("=== EXTRACTED NOTIFICATION SETTINGS ===")
                for setting in settings:
                    logger.info(f"{setting['name']}: {setting['status']}")
                
                # Send to Slack
                self.send_to_slack(settings)
            else:
                logger.warning("No notification settings extracted")
            
            return settings
            
        except Exception as e:
            logger.error(f"Error running enhanced scraper: {e}")
            return settings


def main():
    """Main function"""
    logger.info("Starting Enhanced LinkedIn Notifications Scraper...")
    
    try:
        scraper = EnhancedLinkedInScraper()
        settings = scraper.run()
        
        if settings:
            print("\n=== NOTIFICATION SETTINGS FOUND ===")
            for setting in settings:
                print(f"{setting['name']}: {setting['status']}")
            print(f"\nTotal: {len(settings)} settings found")
        else:
            print("No notification settings were found.")
            print("Make sure you're on the LinkedIn notifications preferences page.")
        
        return 0
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
