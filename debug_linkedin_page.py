#!/usr/bin/env python3
"""
Debug script to inspect the current LinkedIn page structure
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_page():
    """Debug the current LinkedIn page"""
    try:
        # Connect to existing Chrome session
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
        driver = webdriver.Chrome(options=chrome_options)
        
        print(f"Current URL: {driver.current_url}")
        print(f"Page Title: {driver.title}")
        
        # Wait a bit for any dynamic content
        time.sleep(3)
        
        print("\n=== Page Source (first 1000 chars) ===")
        print(driver.page_source[:1000])
        print("...")
        
        # Look for common elements
        print("\n=== Looking for notification-related elements ===")
        
        selectors_to_try = [
            "button", "input", "div", "span", "a",
            "[data-test-id]", "[class*='notification']", 
            "[class*='toggle']", "[class*='switch']",
            ".artdeco-button", ".artdeco-toggle"
        ]
        
        for selector in selectors_to_try:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"\nFound {len(elements)} elements with selector: {selector}")
                    # Show first few elements
                    for i, elem in enumerate(elements[:3]):
                        try:
                            text = elem.text.strip()
                            if text:
                                print(f"  Element {i+1}: {text[:100]}")
                        except:
                            pass
            except Exception as e:
                print(f"Error with selector {selector}: {e}")
        
        # Try to find specific notification-related text
        print("\n=== Looking for notification-related text ===")
        try:
            body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            notification_keywords = ['mention', 'notification', 'email', 'push', 'alert', 'setting']
            
            for keyword in notification_keywords:
                if keyword in body_text:
                    print(f"Found keyword '{keyword}' in page text")
        except Exception as e:
            print(f"Error checking page text: {e}")
        
        # Check current URL and suggest navigation
        current_url = driver.current_url
        target_url = "https://www.linkedin.com/mypreferences/d/categories/notifications"
        
        if target_url not in current_url:
            print(f"\n=== Navigation Suggestion ===")
            print(f"Current URL: {current_url}")
            print(f"Target URL: {target_url}")
            print("You may need to manually navigate to the notifications preferences page")
        
        # Try to find all clickable elements with notification-related text
        print("\n=== Clickable elements with notification-related text ===")
        try:
            clickable_elements = driver.find_elements(By.CSS_SELECTOR, "a, button, [role='button']")
            for elem in clickable_elements:
                try:
                    text = elem.text.strip().lower()
                    if any(keyword in text for keyword in ['notification', 'setting', 'preference', 'mention']):
                        print(f"Clickable: '{elem.text.strip()}' - {elem.tag_name}")
                except:
                    pass
        except Exception as e:
            print(f"Error finding clickable elements: {e}")
        
        print("\n=== Debug complete ===")
        
    except Exception as e:
        print(f"Error in debug: {e}")

if __name__ == "__main__":
    debug_page()
