#!/usr/bin/env python3
"""
LuxuryShoppers Bot - Diagnostic & Testing Script
Tests all components to ensure bot is working correctly
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("\n📋 Checking Python Version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. You have: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if all dependencies are installed"""
    print("\n📦 Checking Dependencies...")
    required_packages = [
        'telegram',
        'requests',
        'dotenv',
        'aiohttp'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n🔐 Checking Environment Variables (.env)...")
    
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ .env file not found!")
        print("Run: cp .env.example .env")
        return False
    
    print("✅ .env file found")
    
    # Load and check variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'AMAZON_ACCESS_KEY',
        'AMAZON_SECRET_KEY',
        'AMAZON_ASSOCIATE_TAG'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value and not value.startswith('your_'):
            print(f"✅ {var}: {'*' * 20}...")
        else:
            print(f"❌ {var}: NOT SET")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Please configure these variables in .env:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    return True

def check_source_files():
    """Check if all source files exist"""
    print("\n📁 Checking Source Files...")
    
    required_files = [
        'telegram_bot.py',
        'amazon_api.py',
        'config.py',
        'run.py',
        'requirements.txt',
        '.env.example',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def test_bot_token():
    """Test if bot token is valid by checking with Telegram"""
    print("\n🔗 Testing Bot Token...")
    
    try:
        import requests
        from config import TELEGRAM_BOT_TOKEN
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                print(f"✅ Bot Token Valid!")
                print(f"   Bot Username: @{bot_info.get('username')}")
                print(f"   Bot Name: {bot_info.get('first_name')}")
                return True
        else:
            print(f"❌ Bot Token Invalid! (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Error testing bot token: {e}")
        return False

def run_diagnostics():
    """Run all diagnostics"""
    print("\n" + "="*50)
    print("🔍 LuxuryShoppers Bot - Diagnostics")
    print("="*50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Source Files", check_source_files),
        ("Environment", check_env_file),
        ("Bot Token", test_bot_token),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n⚠️  Error in {check_name}: {e}")
            results[check_name] = False
    
    # Summary
    print("\n" + "="*50)
    print("📊 Diagnostic Summary")
    print("="*50)
    
    all_passed = True
    for check_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check_name}")
        if not passed:
            all_passed = False
    
    print("="*50)
    
    if all_passed:
        print("\n🎉 All checks passed! Your bot is ready to run!")
        print("\n▶️  Start the bot with: python run.py")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(run_diagnostics())
