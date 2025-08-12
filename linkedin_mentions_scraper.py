#!/usr/bin/env python3
"""
LinkedIn Mentions Scraper
Scrapes LinkedIn mentions from the notifications page and sends them to Slack
Assumes LinkedIn notifications page with "Mentions" tab is already open in Chrome
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
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv('config.env')  # Also load from config.env if present

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_mentions_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LinkedInMentionsScraper:
    """Scrapes LinkedIn mentions from the notifications page and sends to Slack"""
    
    def __init__(self, slack_webhook_url: str = None, debug_port: int = 9222):
        """
        Initialize the mentions scraper
        
        Args:
            slack_webhook_url: Slack webhook URL for sending messages
            debug_port: Chrome debug port (default 9222)
        """
        # You can modify this webhook URL easily here
        self.slack_webhook_url = slack_webhook_url or os.getenv('SLACK_WEBHOOK_URL')
        
        # Fallback to check if webhook URL is still placeholder
        if self.slack_webhook_url and "YOUR_SLACK_WEBHOOK_URL_HERE" in self.slack_webhook_url:
            self.slack_webhook_url = None
        self.debug_port = debug_port
        self.driver = None
        
        if not self.slack_webhook_url:
            logger.warning("Please set the SLACK_WEBHOOK_URL in the script or environment variable")
    
    def connect_to_browser(self) -> bool:
        """
        Connect to existing Chrome browser session with debug port enabled
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", f"localhost:{self.debug_port}")
            
            # Connect to existing Chrome session
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info(f"Connected to browser session on port {self.debug_port}")
            
            current_url = self.driver.current_url
            logger.info(f"Current page: {current_url}")
            
            # Verify we're on LinkedIn
            if "linkedin.com" not in current_url:
                logger.warning("Not currently on LinkedIn. Please navigate to LinkedIn first.")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to browser: {e}")
            logger.error("Make sure Chrome is running with --remote-debugging-port=9222")
            return False
    
    def navigate_to_mentions_tab(self) -> bool:
        """
        Navigate to the Mentions tab in LinkedIn notifications if not already there
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            current_url = self.driver.current_url
            
            # Check if we're already on the mentions notifications page
            if "notifications/?filter=mentions" in current_url:
                logger.info("Already on LinkedIn mentions notifications page!")
                return True
            
            # Navigate to the actual notifications page (not settings)
            if "mypreferences" in current_url:
                logger.info("Currently on notifications settings page, navigating to actual notifications...")
                self.driver.get("https://www.linkedin.com/notifications/?filter=mentions_all")
                time.sleep(5)
                return True
            
            # If not on any notifications page, go to the main notifications page
            if "notifications" not in current_url:
                logger.info("Navigating to LinkedIn notifications page...")
                self.driver.get("https://www.linkedin.com/notifications/")
                time.sleep(5)
            
            # Look for and click the Mentions tab
            logger.info("Looking for Mentions tab...")
            
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # First, let's debug what's available on the page
            self._debug_page_elements()
            
            # Extended list of selectors for the Mentions tab
            mentions_tab_selectors = [
                # Direct text matches
                "//button[contains(text(), 'Mentions')]",
                "//a[contains(text(), 'Mentions')]", 
                "//span[contains(text(), 'Mentions')]",
                "//div[contains(text(), 'Mentions')]",
                "//li[contains(text(), 'Mentions')]",
                
                # Case insensitive
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mentions')]",
                "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mentions')]",
                "//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mentions')]",
                
                # Parent element patterns
                "//span[contains(text(), 'Mentions')]/parent::*",
                "//span[contains(text(), 'Mentions')]/ancestor::button",
                "//span[contains(text(), 'Mentions')]/ancestor::a",
                
                # Data attributes
                "[data-test-mentions-tab]",
                "[data-test*='mentions']",
                "[data-control-name*='mentions']",
                
                # Aria labels
                "[aria-label*='Mentions']",
                "[aria-label*='mentions']",
                
                # Class patterns
                "[class*='mentions']",
                "button[class*='tab'][class*='mention']",
                "a[class*='tab'][class*='mention']",
                
                # LinkedIn specific patterns
                ".artdeco-tab[aria-label*='Mention']",
                ".pvs-navigation__item[aria-label*='Mention']",
                
                # Generic tab patterns with mentions
                "nav button:contains('Mentions')",
                "nav a:contains('Mentions')",
                ".nav-item:contains('Mentions')",
                ".tab:contains('Mentions')"
            ]
            
            mentions_tab = None
            found_selector = None
            
            for selector in mentions_tab_selectors:
                try:
                    if selector.startswith("//"):
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        # Verify the element is actually clickable and visible
                        if element.is_displayed() and element.is_enabled():
                            mentions_tab = element
                            found_selector = selector
                            logger.info(f"Found Mentions tab using selector: {selector}")
                            break
                    
                    if mentions_tab:
                        break
                        
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            if mentions_tab:
                try:
                    # Try different click methods
                    logger.info("Attempting to click Mentions tab...")
                    
                    # Method 1: Direct click
                    try:
                        mentions_tab.click()
                        logger.info("Clicked Mentions tab (direct click)")
                    except:
                        # Method 2: JavaScript click
                        self.driver.execute_script("arguments[0].click();", mentions_tab)
                        logger.info("Clicked Mentions tab (JavaScript click)")
                    
                    time.sleep(3)  # Wait for content to load
                    return True
                    
                except Exception as e:
                    logger.error(f"Failed to click Mentions tab: {e}")
                    return False
            else:
                logger.warning("Could not find Mentions tab.")
                logger.info("Available page elements logged above for debugging.")
                # Try to proceed anyway - maybe we're already on the right tab
                return True
                
        except Exception as e:
            logger.error(f"Error navigating to Mentions tab: {e}")
            return False
    
    def _debug_page_elements(self):
        """Debug method to log available page elements for troubleshooting"""
        try:
            logger.info("=== DEBUGGING PAGE ELEMENTS ===")
            
            # Look for any buttons
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            logger.info(f"Found {len(buttons)} buttons on page")
            for i, button in enumerate(buttons[:10]):  # Show first 10
                try:
                    text = button.text.strip()
                    if text:
                        logger.debug(f"Button {i+1}: '{text}'")
                except:
                    pass
            
            # Look for any links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            logger.info(f"Found {len(links)} links on page")
            for i, link in enumerate(links[:10]):  # Show first 10
                try:
                    text = link.text.strip()
                    if text:
                        logger.debug(f"Link {i+1}: '{text}'")
                except:
                    pass
            
            # Look for navigation elements
            nav_elements = self.driver.find_elements(By.TAG_NAME, "nav")
            logger.info(f"Found {len(nav_elements)} nav elements")
            
            # Look for elements containing "mention" text
            all_elements = self.driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mention')]")
            logger.info(f"Found {len(all_elements)} elements containing 'mention' text")
            for i, element in enumerate(all_elements[:5]):  # Show first 5
                try:
                    text = element.text.strip()
                    if text:
                        logger.info(f"Element with 'mention' {i+1}: '{text[:100]}'")
                except:
                    pass
            
            logger.info("=== END DEBUG ===")
            
        except Exception as e:
            logger.debug(f"Error in debug method: {e}")
    
    def scroll_and_load_mentions(self):
        """Scroll the page to load all visible mentions"""
        try:
            logger.info("Scrolling to load all mentions...")
            
            # Scroll down gradually to load content
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            while True:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            logger.info("Finished loading all mentions")
            
        except Exception as e:
            logger.error(f"Error during scrolling: {e}")
    
    def extract_mentions(self) -> List[Dict[str, str]]:
        """
        Extract all mention notifications from the current page
        
        Returns:
            List of dictionaries containing mention information
        """
        mentions = []
        
        try:
            # Wait for content to load
            time.sleep(3)
            
            # Various selectors to find mention notifications
            mention_selectors = [
                # Generic notification items
                "[data-test-notification-item]",
                ".notification-item",
                ".feed-shared-update-v2",
                "[class*='notification']",
                "[class*='mention']",
                # LinkedIn specific patterns
                ".artdeco-list__item",
                "[data-control-name*='notification']",
                ".pv-profile-section__card",
                # Broader selectors
                "article",
                "li[class*='notification']",
                "div[class*='notification']"
            ]
            
            all_potential_mentions = []
            
            # Try each selector to find notification elements
            for selector in mention_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()
                        if text and ("mention" in text.lower() or "tagged" in text.lower()):
                            all_potential_mentions.append(element)
                            logger.debug(f"Found potential mention with selector {selector}: {text[:100]}...")
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            # If no specific mentions found, look more broadly
            if not all_potential_mentions:
                logger.info("No specific mentions found, searching more broadly...")
                # Look for any text containing mention-related keywords
                all_elements = self.driver.find_elements(By.CSS_SELECTOR, "*")
                
                for element in all_elements:
                    try:
                        text = element.text.strip()
                        if text and len(text) > 10 and len(text) < 500:  # Reasonable length
                            text_lower = text.lower()
                            if any(keyword in text_lower for keyword in [
                                "mentioned you", "tagged you", "mentioned you in", 
                                "tagged you in", "mentioned your name"
                            ]):
                                all_potential_mentions.append(element)
                    except:
                        continue
            
            logger.info(f"Found {len(all_potential_mentions)} potential mention elements")
            
            # Process each potential mention
            processed_texts = set()  # Avoid duplicates
            
            for element in all_potential_mentions:
                try:
                    text = element.text.strip()
                    
                    # Skip if we've already processed this text
                    if text in processed_texts:
                        continue
                    processed_texts.add(text)
                    
                    # Extract mention information
                    mention_info = self._parse_mention_text(text)
                    
                    if mention_info:
                        mentions.append(mention_info)
                        logger.info(f"Extracted mention: {mention_info['formatted_message']}")
                    
                except Exception as e:
                    logger.debug(f"Error processing mention element: {e}")
                    continue
            
            return mentions
            
        except Exception as e:
            logger.error(f"Error extracting mentions: {e}")
            return mentions
    
    def _parse_mention_text(self, text: str) -> Optional[Dict[str, str]]:
        """
        Parse mention text to extract name and type
        
        Args:
            text: Raw text from the mention element
            
        Returns:
            Dictionary with parsed mention information or None
        """
        try:
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            if not lines:
                return None
            
            mention_keywords = ["mentioned you", "tagged you", "mentioned your name"]
            
            # Look for mention-related content
            mention_found = False
            for line in lines:
                if any(keyword in line.lower() for keyword in mention_keywords):
                    mention_found = True
                    break
            
            if not mention_found:
                return None
            
            # Try to extract person's name (usually the first line or contains a name pattern)
            person_name = None
            mention_type = "post"  # default
            
            # Look for patterns like "John Doe mentioned you in a post"
            for line in lines:
                line_lower = line.lower()
                
                if "mentioned you in a" in line_lower:
                    # Extract name and type
                    parts = line.split("mentioned you in a")
                    if len(parts) >= 2:
                        person_name = parts[0].strip()
                        mention_type = parts[1].strip().split()[0] if parts[1].strip() else "post"
                    break
                elif "mentioned you in" in line_lower:
                    parts = line.split("mentioned you in")
                    if len(parts) >= 2:
                        person_name = parts[0].strip()
                        mention_type = parts[1].strip().split()[0] if parts[1].strip() else "post"
                    break
                elif "mentioned you" in line_lower:
                    person_name = line.split("mentioned you")[0].strip()
                    mention_type = "post"
                    break
                elif "tagged you" in line_lower:
                    person_name = line.split("tagged you")[0].strip()
                    mention_type = "post"
                    break
            
            # If no clear pattern, try to extract name from first line
            if not person_name and lines:
                first_line = lines[0]
                # Remove common words and get potential name
                words = first_line.split()
                if len(words) >= 2:
                    person_name = " ".join(words[:2])  # Take first two words as name
            
            if person_name:
                # Clean up the name
                person_name = person_name.strip('"\'.,!?:;')
                
                # Clean up mention type
                mention_type = mention_type.strip('"\'.,!?:;')
                if not mention_type:
                    mention_type = "post"
                
                # Format the final message
                formatted_message = f"{person_name} mentioned you in a {mention_type}"
                
                return {
                    'person_name': person_name,
                    'mention_type': mention_type,
                    'formatted_message': formatted_message,
                    'raw_text': text
                }
            
            return None
            
        except Exception as e:
            logger.debug(f"Error parsing mention text: {e}")
            return None
    
    def send_mentions_to_slack(self, mentions: List[Dict[str, str]]) -> bool:
        """
        Send mention messages to Slack
        
        Args:
            mentions: List of mention dictionaries
            
        Returns:
            bool: True if all messages sent successfully
        """
        if not mentions:
            logger.info("No mentions to send to Slack")
            return True
        
        if not self.slack_webhook_url:
            logger.error("Slack webhook URL not configured. Please set SLACK_WEBHOOK_URL.")
            return False
        
        try:
            success_count = 0
            
            # Send a summary message first
            summary_message = {
                "text": f"🔔 LinkedIn Mentions Update: Found {len(mentions)} new mention(s)"
            }
            
            response = requests.post(
                self.slack_webhook_url,
                json=summary_message,
                timeout=10
            )
            response.raise_for_status()
            logger.info("Sent summary message to Slack")
            
            # Send individual mention messages
            for mention in mentions:
                message = {
                    "text": f"👤 {mention['formatted_message']}"
                }
                
                response = requests.post(
                    self.slack_webhook_url,
                    json=message,
                    timeout=10
                )
                response.raise_for_status()
                
                logger.info(f"Sent to Slack: {mention['formatted_message']}")
                success_count += 1
                
                # Small delay between messages to avoid rate limiting
                time.sleep(1)
            
            logger.info(f"Successfully sent {success_count}/{len(mentions)} mentions to Slack")
            return success_count == len(mentions)
            
        except Exception as e:
            logger.error(f"Error sending mentions to Slack: {e}")
            return False
    
    def run(self) -> List[Dict[str, str]]:
        """
        Main method to run the mentions scraper
        
        Returns:
            List of extracted mentions
        """
        mentions = []
        
        try:
            # Connect to browser
            if not self.connect_to_browser():
                logger.error("Failed to connect to browser")
                return mentions
            
            # Navigate to mentions tab
            if not self.navigate_to_mentions_tab():
                logger.error("Failed to navigate to mentions tab")
                return mentions
            
            # Load all mentions by scrolling
            self.scroll_and_load_mentions()
            
            # Extract mentions
            mentions = self.extract_mentions()
            
            if mentions:
                logger.info("=== EXTRACTED MENTIONS ===")
                for mention in mentions:
                    logger.info(f"• {mention['formatted_message']}")
                
                # Send to Slack
                self.send_mentions_to_slack(mentions)
            else:
                logger.info("No mentions found")
            
            return mentions
            
        except Exception as e:
            logger.error(f"Error running mentions scraper: {e}")
            return mentions
        
        finally:
            # Note: We don't close the driver since we want to keep the existing session
            logger.info("Mentions scraper completed")
    
    def close(self):
        """Close the browser driver (optional - keeps existing session alive)"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser driver closed")


def main():
    """Main function to run the LinkedIn mentions scraper"""
    logger.info("Starting LinkedIn Mentions Scraper...")
    
    try:
        # You can modify the webhook URL here or set it as an environment variable
        scraper = LinkedInMentionsScraper(
            slack_webhook_url="YOUR_SLACK_WEBHOOK_URL_HERE"  # Replace with your webhook URL
        )
        
        mentions = scraper.run()
        
        if mentions:
            print("\n=== LINKEDIN MENTIONS FOUND ===")
            for i, mention in enumerate(mentions, 1):
                print(f"{i}. {mention['formatted_message']}")
            print(f"\nTotal: {len(mentions)} mentions found and sent to Slack")
        else:
            print("No mentions were found.")
            print("Make sure you're on the LinkedIn notifications page with the Mentions tab open.")
        
        # Optionally close the driver (uncomment if you want to close the browser)
        # scraper.close()
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
