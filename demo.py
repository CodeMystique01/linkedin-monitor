#!/usr/bin/env python3
"""
Demo script for LinkedIn Monitor
Shows how the program works without requiring actual API keys
"""

import json
import time
from datetime import datetime

def demo_search_results():
    """Simulate search results for demo purposes"""
    return [
        {
            "title": "Excited to share that I've joined [Company] as [Position]",
            "link": "https://www.linkedin.com/posts/example-123",
            "snippet": "I'm thrilled to announce my new role at [Company] where I'll be working on exciting projects..."
        },
        {
            "title": "Great meeting with [Your Name] today!",
            "link": "https://www.linkedin.com/posts/example-456", 
            "snippet": "Had an excellent conversation about industry trends and future collaborations..."
        }
    ]

def demo_slack_message(term, result):
    """Show what a Slack message would look like"""
    print(f"\n🔔 New LinkedIn mention detected!")
    print(f"📄 Title: {result['title']}")
    print(f"🔗 Link: {result['link']}")
    print(f"📝 Snippet: {result['snippet']}")
    print(f"🏷️ Tagged term: {term}")
    print(f"⏰ Detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

def run_demo():
    """Run the demo"""
    print("🚀 LinkedIn Monitor Demo")
    print("=" * 30)
    print("\nThis demo shows how the LinkedIn Monitor works:")
    print("1. Searches for mentions of your specified terms")
    print("2. Detects new mentions that haven't been seen before")
    print("3. Sends formatted alerts to Slack")
    print("4. Tracks seen URLs to avoid duplicate alerts")
    
    # Simulate search terms
    search_terms = ["Your Name", "Your Company", "Your Product"]
    print(f"\n📋 Monitoring terms: {', '.join(search_terms)}")
    
    # Simulate search results
    print("\n🔍 Simulating search results...")
    time.sleep(2)
    
    results = demo_search_results()
    
    print(f"✅ Found {len(results)} results")
    
    # Show what alerts would look like
    print("\n📱 Sample Slack alerts:")
    for i, result in enumerate(results):
        demo_slack_message(search_terms[i % len(search_terms)], result)
        time.sleep(1)
    
    print("\n🎉 Demo complete!")
    print("\nTo use the real monitor:")
    print("1. Get API keys from SerpAPI and Slack")
    print("2. Configure your .env file")
    print("3. Run: python linkedin_monitor.py")
    print("\nSee README.md for detailed instructions.")

if __name__ == "__main__":
    run_demo() 