import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from amazon_api import AmazonAPI
from config import TELEGRAM_BOT_TOKEN

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Amazon API
amazon_api = AmazonAPI()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_message = """
Welcome to LuxuryShoppers Bot! 🛍️

I help you find and purchase products on Amazon with exclusive affiliate links.
Your purchase through my links helps support this service while giving you great deals!

Commands:
/search <product> - Search for products on Amazon
/help - Show help information
/about - Learn more about this bot

Just type or use the commands above to get started!
    """
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
📖 How to use LuxuryShoppers Bot:

1️⃣ **Search Products**: Type `/search luxury watch` to find products
2️⃣ **View Results**: I'll show you top products with prices
3️⃣ **Buy Now**: Click the affiliate link to purchase on Amazon
4️⃣ **Earn Commission**: I earn commission on every purchase through these links

Example searches:
- /search designer handbags
- /search luxury watches
- /search premium headphones

💡 Tip: Be specific with your search for better results!
    """
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send information about the bot."""
    about_text = """
About LuxuryShoppers Bot:

This bot integrates with Amazon's Product Advertising API to bring you:
✨ Real-time product searches
💰 Affiliate links for exclusive deals
🔗 Direct Amazon integration
📱 Convenient shopping from Telegram

By using our affiliate links, you support the development of this service!

Questions? Contact the developer or report issues.
    """
    await update.message.reply_text(about_text)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Search for products when /search command is used."""
    if not context.args:
        await update.message.reply_text("Please provide a search term. Example: /search luxury watch")
        return
    
    search_query = ' '.join(context.args)
    await update.message.reply_text(f"🔍 Searching for '{search_query}'... Please wait...")
    
    try:
        # Search products using Amazon API
        products = amazon_api.search_products(search_query, max_results=5)
        
        if not products:
            await update.message.reply_text("❌ No products found. Try a different search term.")
            return
        
        # Format results
        message = f"🛍️ **Search Results for '{search_query}'**\n\n"
        
        for idx, product in enumerate(products, 1):
            product_text = f"""
{idx}. **{product['title']}**
   💵 Price: {product['price']}
   🔗 ASIN: {product['asin']}
"""
            message += product_text
        
        message += "\n_Click the links below to purchase and support this service!_"
        
        # Create inline buttons for each product
        keyboard = []
        for idx, product in enumerate(products, 1):
            keyboard.append([
                InlineKeyboardButton(
                    f"Buy #{idx} - {product['title'][:30]}...",
                    url=product['affiliate_url']
                )
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error during search: {e}")
        await update.message.reply_text(f"❌ An error occurred during search: {str(e)}")

async def handle_text_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages as product searches."""
    search_query = update.message.text
    
    # Skip if message is too short or looks like a command
    if len(search_query) < 3 or search_query.startswith('/'):
        return
    
    await update.message.reply_text(f"🔍 Searching for '{search_query}'... Please wait...")
    
    try:
        products = amazon_api.search_products(search_query, max_results=5)
        
        if not products:
            await update.message.reply_text("❌ No products found. Try a different search term.")
            return
        
        # Format and send results
        message = f"🛍️ **Results for '{search_query}'**\n\n"
        
        for idx, product in enumerate(products, 1):
            product_text = f"{idx}. **{product['title']}** - {product['price']}\n"
            message += product_text
        
        keyboard = []
        for idx, product in enumerate(products, 1):
            keyboard.append([
                InlineKeyboardButton(
                    f"Buy - {product['title'][:25]}...",
                    url=product['affiliate_url']
                )
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error during search: {e}")
        await update.message.reply_text(f"❌ An error occurred: {str(e)}")

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("search", search_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_search))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()