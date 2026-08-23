# LuxuryShoppers - Telegram Amazon Affiliate Bot

A Telegram bot that integrates with Amazon's Product Advertising API to search and recommend luxury products while earning affiliate commissions.

## Features

✨ **Real-time Product Search** - Search Amazon's entire catalog from Telegram
💰 **Affiliate Integration** - Earn commissions on every purchase through bot links
🔗 **Direct Amazon Links** - Seamless integration with affiliate tracking
📱 **Easy to Use** - Simple commands and natural text search support
🛍️ **Luxury Focus** - Optimized for high-end product discovery

## Prerequisites

- Python 3.8+
- Telegram Bot Token (from BotFather)
- Amazon Associates Account with:
  - Access Key ID
  - Secret Access Key
  - Associate Tag

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/youngsage22/Luxuryshoppers.git
cd Luxuryshoppers
pip install -r requirements.txt
```

### 2. Get Your Credentials

**Telegram Bot Token:**
- Chat with [@BotFather](https://t.me/botfather) on Telegram
- Create a new bot with `/newbot`
- Copy your bot token

**Amazon Associates Credentials:**
1. Sign up at [Amazon Associates](https://affiliate-program.amazon.com/)
2. Go to "Account Settings" → "API Key Management"
3. Create new API credentials
4. Get your Associate Tag from account settings

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
AMAZON_ACCESS_KEY=your_access_key_here
AMAZON_SECRET_KEY=your_secret_key_here
AMAZON_ASSOCIATE_TAG=your_associate_tag
```

### 4. Run the Bot

```bash
python telegram_bot.py
```

## How It Works

### Commands

| Command | Description |
|---------|------------|
| `/start` | Welcome message and quick start |
| `/search <product>` | Search for specific products |
| `/help` | Show detailed help information |
| `/about` | Learn about the bot |

### Usage Examples

```
User: /search luxury watches
Bot: Shows top 5 luxury watches with affiliate links

User: designer handbags
Bot: Automatically searches and returns results

User: /help
Bot: Shows all available commands and features
```

## File Structure

```
Luxuryshoppers/
├── telegram_bot.py          # Main bot implementation
├── amazon_api.py            # Amazon API integration
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md               # This file
```

## How Affiliate Commissions Work

1. User searches for products in Telegram
2. Bot returns Amazon products with affiliate links
3. User clicks the link and makes a purchase
4. Amazon tracks the purchase with your Associate Tag
5. You receive a commission (typically 1-10% depending on product category)

**Important Notes:**
- Users must click your affiliate links for tracking to work
- Direct Amazon links won't credit your account
- Commission rates vary by product category
- Keep track of your earnings in your Associates dashboard

## API Reference

### AmazonAPI Class

#### `search_products(keywords, max_results=5)`
Search for products on Amazon

**Parameters:**
- `keywords` (str): Search query
- `max_results` (int): Number of results to return

**Returns:**
- List of product dictionaries with: `asin`, `title`, `price`, `affiliate_url`

#### `get_product_details(asin)`
Get detailed information about a specific product

**Parameters:**
- `asin` (str): Amazon Standard Identification Number

**Returns:**
- Dictionary with product details and affiliate URL

## Troubleshooting

### Bot doesn't respond
- Check your Telegram Bot Token in `.env`
- Ensure the bot is running: `python telegram_bot.py`
- Check logs for error messages

### No search results
- Verify Amazon API credentials are correct
- Ensure your Associate Tag is valid
- Check internet connection

### Affiliate links not tracking
- Confirm Associate Tag is in the URL
- Test with your own account first
- Check Amazon Associates dashboard for activity

## Future Enhancements

- [ ] Product categories and filtering
- [ ] Price alerts and notifications
- [ ] User wishlist functionality
- [ ] Comparison shopping features
- [ ] Product reviews integration
- [ ] Advanced search filters

## Security Notes

⚠️ **Never commit `.env` file** - It contains sensitive credentials
✅ **Keep credentials secure** - Treat like passwords
✅ **Use environment variables** - Don't hardcode secrets
✅ **Rotate API keys regularly** - For security best practices

## Legal & Compliance

- Ensure you comply with [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/operating-agreement)
- Disclose affiliate relationships where required by law
- Follow FTC guidelines on affiliate marketing
- Don't engage in misleading practices

## Support & Issues

For issues or feature requests:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include logs and error messages

## License

This project is open source. See LICENSE file for details.

## Disclaimer

This bot is provided as-is. The developer is not responsible for:
- Affiliate program violations
- Loss of earnings or account suspension
- Product availability or pricing changes
- Amazon API changes or deprecations

Use at your own risk and comply with all terms of service.

---

**Happy Shopping! 🛍️** 

For questions or support, reach out through GitHub issues.
