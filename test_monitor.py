#!/usr/bin/env python3
"""
Test script for LinkedIn Monitor
Verifies configuration and tests API connections
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test if all required environment variables are set"""
    print("🔧 Testing Environment Configuration")
    print("=" * 40)
    
    required_vars = {
        'SERPAPI_KEY': 'SerpAPI Key',
        'SLACK_WEBHOOK_URL': 'Slack Webhook URL'
    }
    
    missing_vars = []
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {description}: {'*' * len(value)}")
        else:
            print(f"❌ {description}: NOT SET")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        return False
    
    print("\n✅ All required environment variables are set")
    return True

def test_serpapi():
    """Test SerpAPI connection"""
    print("\n🔍 Testing SerpAPI Connection")
    print("=" * 40)
    
    api_key = os.getenv('SERPAPI_KEY')
    
    try:
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": "test site:linkedin.com",
            "api_key": api_key,
            "num": 1
        }
        
        print("Making test API call...")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if "error" in data:
            print(f"❌ SerpAPI Error: {data['error']}")
            return False
        
        print("✅ SerpAPI connection successful")
        print(f"   Found {len(data.get('organic_results', []))} test results")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ SerpAPI connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error testing SerpAPI: {e}")
        return False

def test_slack():
    """Test Slack webhook"""
    print("\n📱 Testing Slack Webhook")
    print("=" * 40)
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    
    try:
        test_message = {
            "text": "🧪 LinkedIn Monitor Test Message",
            "attachments": [
                {
                    "color": "#0077B5",
                    "title": "Test Alert",
                    "text": "This is a test message to verify Slack integration is working correctly.",
                    "fields": [
                        {
                            "title": "Test Status",
                            "value": "✅ Working",
                            "short": True
                        }
                    ],
                    "footer": "LinkedIn Monitor Test",
                    "footer_icon": "https://cdn-icons-png.flaticon.com/512/174/174857.png"
                }
            ]
        }
        
        print("Sending test message to Slack...")
        response = requests.post(webhook_url, json=test_message, timeout=10)
        response.raise_for_status()
        
        print("✅ Slack webhook test successful")
        print("   Check your Slack channel for the test message")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Slack webhook test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error testing Slack: {e}")
        return False

def test_search_terms():
    """Test search terms configuration"""
    print("\n🔎 Testing Search Terms")
    print("=" * 40)
    
    search_terms = os.getenv('SEARCH_TERMS', 'Apurv,Zenskar').split(',')
    
    print(f"Configured search terms: {', '.join(search_terms)}")
    
    if not search_terms or not any(term.strip() for term in search_terms):
        print("❌ No valid search terms configured")
        return False
    
    print("✅ Search terms configured correctly")
    return True

def main():
    """Run all tests"""
    print("🧪 LinkedIn Monitor Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Search Terms", test_search_terms),
        ("SerpAPI", test_serpapi),
        ("Slack", test_slack)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your LinkedIn Monitor is ready to run.")
        print("Run 'python linkedin_monitor.py' to start monitoring.")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before running the monitor.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 