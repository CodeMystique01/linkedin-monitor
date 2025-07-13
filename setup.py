#!/usr/bin/env python3
"""
Setup script for LinkedIn Monitor
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def setup_config():
    """Set up configuration file"""
    print("⚙️ Setting up configuration...")
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping configuration setup.")
        return True
    
    # Copy example config
    if os.path.exists('config.env.example'):
        shutil.copy('config.env.example', '.env')
        print("✅ Configuration file created (.env)")
        print("📝 Please edit .env file with your API keys:")
        print("   - SERPAPI_KEY: Get from https://serpapi.com/")
        print("   - SLACK_WEBHOOK_URL: Get from your Slack workspace")
        print("   - SEARCH_TERMS: Add the terms you want to monitor")
        return True
    else:
        print("❌ config.env.example not found")
        return False

def main():
    """Main setup function"""
    print("🚀 LinkedIn Monitor Setup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Setup configuration
    if not setup_config():
        return 1
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python linkedin_monitor.py")
    print("\nFor help, see README.md")
    
    return 0

if __name__ == "__main__":
    exit(main()) 