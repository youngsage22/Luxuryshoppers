import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Amazon Associates Configuration
AMAZON_ACCESS_KEY = os.getenv('AMAZON_ACCESS_KEY')
AMAZON_SECRET_KEY = os.getenv('AMAZON_SECRET_KEY')
AMAZON_ASSOCIATE_TAG = os.getenv('AMAZON_ASSOCIATE_TAG')
AMAZON_API_REGION = os.getenv('AMAZON_API_REGION', 'US')

# API Endpoints
AMAZON_API_ENDPOINT = 'https://api.amazon.com'
AMAZON_PRODUCT_API_VERSION = '2013-08-24'

# Validation
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables")
if not all([AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOCIATE_TAG]):
    raise ValueError("Amazon API credentials are not set in environment variables")