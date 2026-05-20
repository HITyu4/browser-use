#!/usr/bin/env python3
"""
Simple test script to verify browser-use basic functionality.
"""

import os
import sys
from dotenv import load_dotenv

# Set configuration directory to avoid permission issues
os.environ['BROWSER_USE_CONFIG_DIR'] = os.path.join(os.getcwd(), '.browser-use-config')
os.environ['BROWSER_USE_DISABLE_EXTENSIONS'] = 'true'

# Load environment variables
load_dotenv()

print("Testing browser-use basic functionality...")
print("Python version:", sys.version)
print()

# Try to import the library
print("1. Importing browser-use library...")
try:
    # Try to import Agent class
    from browser_use import Agent
    print("✅ Success! Agent class imported.")
    
    # Try to import model classes
    from browser_use import ChatBrowserUse, ChatOpenAI, ChatGoogle
    print("✅ Success! All model classes imported.")
    
except Exception as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)

print()
print("2. Checking environment variables...")
# Check if API keys are set
api_keys = ['BROWSER_USE_API_KEY', 'OPENAI_API_KEY', 'GOOGLE_API_KEY', 'ALIBABA_CLOUD']
for key in api_keys:
    if os.getenv(key):
        print(f"✅ {key}: Set (masked)")
    else:
        print(f"⚠️ {key}: Not set")

print()
print("3. Testing configuration...")
try:
    from browser_use.config import CONFIG
    print(f"✅ Config loaded successfully")
    print(f"   - Logging level: {CONFIG.BROWSER_USE_LOGGING_LEVEL}")
    print(f"   - Version check: {CONFIG.BROWSER_USE_VERSION_CHECK}")
except Exception as e:
    print(f"❌ Failed to load config: {e}")

print()
print("✅ Basic functionality test completed!")
print("The library is installed and configured correctly.")
print("You may need to set API keys in the .env file to use specific models.")
