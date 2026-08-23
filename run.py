#!/usr/bin/env python3
"""
LuxuryShoppers Telegram Bot - Main Entry Point
Start the bot with: python run.py
"""

import logging
import sys
from config import TELEGRAM_BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the bot"""
    try:
        logger.info("Starting LuxuryShoppers Bot...")
        
        # Check if token is valid
        if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN.startswith('your_'):
            logger.error("❌ Invalid or missing TELEGRAM_BOT_TOKEN in .env file")
            print("\n⚠️  ERROR: Bot token not configured!")
            print("Please check your .env file and add a valid Telegram bot token.")
            sys.exit(1)
        
        # Import and start the bot
        from telegram_bot import main as start_bot
        start_bot()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\n✅ Bot stopped gracefully")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
