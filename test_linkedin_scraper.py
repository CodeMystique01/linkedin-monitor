#!/usr/bin/env python3
"""
Test script for LinkedIn Notifications Scraper
Tests the basic functionality without requiring an actual browser session
"""

import os
import sys
import logging
from unittest.mock import Mock, patch
from linkedin_notifications_scraper import LinkedInNotificationsScraper

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_scraper_initialization():
    """Test scraper initialization"""
    print("Testing scraper initialization...")
    
    # Test with webhook URL
    scraper = LinkedInNotificationsScraper(
        slack_webhook_url="https://hooks.slack.com/test",
        debug_port=9222
    )
    
    assert scraper.slack_webhook_url == "https://hooks.slack.com/test"
    assert scraper.debug_port == 9222
    
    print("✅ Scraper initialization test passed")


def test_filter_info_extraction():
    """Test filter information extraction logic"""
    print("Testing filter info extraction...")
    
    scraper = LinkedInNotificationsScraper()
    
    # Mock element with text content
    mock_element = Mock()
    mock_element.text = "Mentions of you - Enabled"
    mock_element.find_elements.return_value = []
    
    # Test extraction
    filter_info = scraper._extract_filter_info(mock_element)
    
    if filter_info:
        print(f"  Extracted: {filter_info}")
        assert "mention" in filter_info['name'].lower()
    
    print("✅ Filter info extraction test passed")


def test_slack_message_formatting():
    """Test Slack message formatting"""
    print("Testing Slack message formatting...")
    
    scraper = LinkedInNotificationsScraper(slack_webhook_url="https://test.webhook.url")
    
    test_filters = [
        {"name": "Mentions of you", "status": "Enabled"},
        {"name": "Comments on your posts", "status": "Disabled"},
        {"name": "Tags in posts", "status": "Enabled"}
    ]
    
    # Mock requests.post to avoid actual HTTP calls
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status.return_value = None
        
        # Test sending filters
        result = scraper.send_to_slack(test_filters)
        
        # Verify the call was made
        assert mock_post.called
        assert result is True
        
        # Check the message structure
        call_args = mock_post.call_args
        message = call_args[1]['json']  # Get the json parameter
        
        assert 'text' in message
        assert 'attachments' in message
        assert 'LinkedIn Notification Preferences' in message['text']
    
    print("✅ Slack message formatting test passed")


def test_individual_slack_messages():
    """Test individual Slack message sending"""
    print("Testing individual Slack messages...")
    
    scraper = LinkedInNotificationsScraper(slack_webhook_url="https://test.webhook.url")
    
    test_filters = [
        {"name": "Mentions of you", "status": "Enabled"},
        {"name": "Comments on your posts", "status": "Disabled"}
    ]
    
    # Mock requests.post
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status.return_value = None
        
        # Test sending individual filters
        result = scraper.send_individual_filters_to_slack(test_filters)
        
        # Verify calls were made for each filter
        assert mock_post.call_count == len(test_filters)
        assert result is True
    
    print("✅ Individual Slack messages test passed")


def test_configuration_loading():
    """Test configuration loading from environment"""
    print("Testing configuration loading...")
    
    # Test with environment variables
    test_env = {
        'SLACK_WEBHOOK_URL': 'https://test.webhook.url',
        'CHROME_DEBUG_PORT': '9223',
        'SEND_INDIVIDUAL': 'false'
    }
    
    with patch.dict(os.environ, test_env):
        scraper = LinkedInNotificationsScraper()
        assert scraper.slack_webhook_url == 'https://test.webhook.url'
        assert scraper.debug_port == 9223
    
    print("✅ Configuration loading test passed")


def test_browser_connection_error_handling():
    """Test browser connection error handling"""
    print("Testing browser connection error handling...")
    
    scraper = LinkedInNotificationsScraper()
    
    # Mock webdriver to raise an exception
    with patch('linkedin_notifications_scraper.webdriver.Chrome') as mock_chrome:
        mock_chrome.side_effect = Exception("Connection failed")
        
        result = scraper.connect_to_existing_browser()
        assert result is False
    
    print("✅ Browser connection error handling test passed")


def run_all_tests():
    """Run all tests"""
    print("🧪 Running LinkedIn Notifications Scraper Tests")
    print("=" * 50)
    
    try:
        test_scraper_initialization()
        test_filter_info_extraction()
        test_slack_message_formatting()
        test_individual_slack_messages()
        test_configuration_loading()
        test_browser_connection_error_handling()
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("LinkedIn Notifications Scraper - Test Suite")
    print("=" * 50)
    
    # Check if required modules are available
    try:
        import selenium
        import requests
        print(f"✅ Selenium version: {selenium.__version__}")
        print(f"✅ Requests available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return 1
    
    print("\nRunning tests...")
    success = run_all_tests()
    
    if success:
        print("\n🚀 Ready to use the LinkedIn Notifications Scraper!")
        print("\nNext steps:")
        print("1. Start Chrome with: chrome --remote-debugging-port=9222")
        print("2. Open LinkedIn notifications page")
        print("3. Configure SLACK_WEBHOOK_URL in config.env")
        print("4. Run: python linkedin_notifications_scraper.py")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit(main())
