from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, PreCheckoutQueryHandler, ContextTypes, filters
)
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "7580086418:AAGi6mVgzONAl1koEbXfk13eDYTzCeMdDWg"

# 🛍️ PRODUCTS FOR SALE - Add anything you want!
# Types: 'text', 'file', 'link', 'code', 'image'
PRODUCTS = {
    "ebook_python": {
        "name": "Python eBook",
        "price": 50,
        "emoji": "📚",
        "description": "Complete Python programming guide",
        "type": "file",
        "content": "https://example.com/python-ebook.pdf"  # or file_id
    },
    "premium_template": {
        "name": "Website Template",
        "price": 100,
        "emoji": "🎨",
        "description": "Professional HTML/CSS template",
        "type": "link",
        "content": "https://drive.google.com/file/d/xxx"
    },
    "secret_recipe": {
        "name": "Secret Recipe",
        "price": 25,
        "emoji": "🍕",
        "description": "My grandmother's secret pizza recipe",
        "type": "text",
        "content": """🍕 **Grandma's Secret Pizza Recipe**

Ingredients:
- 500g flour
- 300ml warm water
- 10g yeast
- 1 tbsp sugar
- Salt to taste
- Olive oil

Instructions:
1. Mix yeast with warm water and sugar
2. Add flour and salt, knead for 10 minutes
3. Let it rise for 2 hours
4. Roll, add toppings, bake at 250°C for 12 minutes

Enjoy! 🔥"""
    },
    "api_script": {
        "name": "API Integration Script",
        "price": 75,
        "emoji": "⚡",
        "description": "Ready-to-use API wrapper in Python",
        "type": "code",
        "content": """import requests

class APIWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.example.com"
    
    def get_data(self, endpoint):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(f"{self.base_url}/{endpoint}", headers=headers)
        return response.json()
    
    def post_data(self, endpoint, data):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(f"{self.base_url}/{endpoint}", 
                                json=data, headers=headers)
        return response.json()

# Usage
api = APIWrapper("your_api_key")
result = api.get_data("users")
print(result)"""
    },
    "crypto_course": {
        "name": "Crypto Trading Course",
        "price": 200,
        "emoji": "💰",
        "description": "Complete cryptocurrency trading masterclass",
        "type": "link",
        "content": "https://t.me/+secret_course_link"
    },
    "photoshop_preset": {
        "name": "Photoshop Presets Pack",
        "price": 30,
        "emoji": "🎭",
        "description": "10 professional photo editing presets",
        "type": "file",
        "content": "preset_pack.zip"  # You'll need to upload this file first
    },
    "business_plan": {
        "name": "Business Plan Template",
        "price": 80,
        "emoji": "📊",
        "description": "Professional startup business plan template",
        "type": "text",
        "content": """📊 **Business Plan Template**

1. Executive Summary
2. Company Description
3. Market Analysis
4. Organization & Management
5. Service/Product Line
6. Marketing & Sales
7. Financial Projections
8. Funding Requirements

Full detailed template: [Download Link]"""
    },
    "spotify_premium": {
        "name": "Spotify Premium Guide",
        "price": 15,
        "emoji": "🎵",
        "description": "How to get Spotify Premium legally",
        "type": "text",
        "content": """🎵 **Spotify Premium Guide**

Legal ways to get Spotify Premium:
1. Student discount (50% off)
2. Family plan (split with friends)
3. Free trials
4. Bundle deals with mobile carriers
5. Black Friday deals

Never use cracked accounts - support artists! 🎶"""
    },
    "workout_plan": {
        "name": "30-Day Workout Plan",
        "price": 40,
        "emoji": "💪",
        "description": "Complete home workout program",
        "type": "text",
        "content": """💪 **30-Day Home Workout Plan**

Week 1-2: Building Foundation
- Monday: Push-ups, Squats (3x15)
- Wednesday: Plank, Lunges (3x12)
- Friday: Burpees, Mountain Climbers (3x10)

Week 3-4: Intensity Boost
[Full detailed plan with videos included...]

Let's get fit! 🔥"""
    },
    "instagram_growth": {
        "name": "Instagram Growth Secrets",
        "price": 60,
        "emoji": "📸",
        "description": "Proven strategies to grow your Instagram",
        "type": "text",
        "content": """📸 **Instagram Growth Secrets 2025**

✅ Post at optimal times (9 AM, 12 PM, 6 PM)
✅ Use 20-30 relevant hashtags
✅ Engage with your niche community
✅ Create Reels (highest reach)
✅ Collaborate with micro-influencers
✅ Use Instagram Stories daily
✅ Analyze insights weekly

Detailed strategy guide included! 📈"""
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display shop catalog"""
    keyboard = []
    
    # Create 2-column layout for products
    row = []
    for product_id, product_data in PRODUCTS.items():
        button_text = f"{product_data['emoji']} {product_data['name']}"
        row.append(InlineKeyboardButton(button_text, callback_data=f"view_{product_id}"))
        
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    if row:  # Add remaining button if odd number
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🛍️ *Welcome to the Digital Shop!*\n\n"
        "We accept Telegram Stars ⭐\n"
        "Browse our products below:\n\n"
        "💫 Instant delivery after payment\n"
        "🔒 Secure transactions\n"
        "✅ Satisfaction guaranteed",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def view_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show product details"""
    query = update.callback_query
    await query.answer()
    
    product_id = query.data.replace("view_", "")
    
    if product_id not in PRODUCTS:
        await query.message.reply_text("❌ Product not found!")
        return
    
    product = PRODUCTS[product_id]
    
    # Create buy button
    keyboard = [
        [InlineKeyboardButton(f"💳 Buy for {product['price']} ⭐", 
                            callback_data=f"buy_{product_id}")],
        [InlineKeyboardButton("◀️ Back to Shop", callback_data="back_to_shop")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{product['emoji']} *{product['name']}*\n\n"
        f"📝 {product['description']}\n\n"
        f"💰 Price: *{product['price']} Stars*\n"
        f"📦 Type: {product['type'].title()}\n\n"
        f"⚡ Instant delivery after payment!",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def back_to_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to main shop"""
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    row = []
    for product_id, product_data in PRODUCTS.items():
        button_text = f"{product_data['emoji']} {product_data['name']}"
        row.append(InlineKeyboardButton(button_text, callback_data=f"view_{product_id}"))
        
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🛍️ *Welcome to the Digital Shop!*\n\n"
        "We accept Telegram Stars ⭐\n"
        "Browse our products below:\n\n"
        "💫 Instant delivery after payment\n"
        "🔒 Secure transactions\n"
        "✅ Satisfaction guaranteed",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def buy_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiate purchase"""
    query = update.callback_query
    await query.answer()
    
    product_id = query.data.replace("buy_", "")
    
    if product_id not in PRODUCTS:
        await query.message.reply_text("❌ Product not found!")
        return
    
    product = PRODUCTS[product_id]
    
    try:
        prices = [LabeledPrice(product['name'], product['price'])]
        
        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            title=f"{product['emoji']} {product['name']}",
            description=product['description'],
            payload=f"buy_{product_id}",
            provider_token="",
            currency="XTR",
            prices=prices,
            start_parameter=f"buy_{product_id}"
        )
        logger.info(f"Invoice sent: {product_id} to user {query.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error sending invoice: {e}")
        await query.message.reply_text(
            "❌ Error creating invoice. Please try again or contact support."
        )

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Validate payment"""
    query = update.pre_checkout_query
    
    product_id = query.invoice_payload.replace("buy_", "")
    
    if product_id not in PRODUCTS:
        await query.answer(ok=False, error_message="Invalid product")
    else:
        await query.answer(ok=True)
        logger.info(f"Pre-checkout approved: {product_id}")

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Deliver product after payment"""
    user = update.effective_user
    payment = update.message.successful_payment
    
    product_id = payment.invoice_payload.replace("buy_", "")
    
    if product_id not in PRODUCTS:
        await update.message.reply_text("❌ Error: Product not found!")
        return
    
    product = PRODUCTS[product_id]
    
    logger.info(f"Payment successful: {product_id} by user {user.id}")
    
    # Send confirmation
    await update.message.reply_text(
        f"✅ *Payment Successful!*\n\n"
        f"Thank you {user.first_name}! 🎉\n"
        f"You purchased: {product['emoji']} *{product['name']}*\n\n"
        f"📦 Delivering your product now...",
        parse_mode="Markdown"
    )
    
    # Deliver based on product type
    if product['type'] == 'text':
        await update.message.reply_text(
            product['content'],
            parse_mode="Markdown"
        )
    
    elif product['type'] == 'code':
        await update.message.reply_text(
            f"```python\n{product['content']}\n```",
            parse_mode="Markdown"
        )
    
    elif product['type'] == 'link':
        await update.message.reply_text(
            f"🔗 *Your Access Link:*\n\n{product['content']}\n\n"
            f"⚠️ Don't share this link with others!",
            parse_mode="Markdown"
        )
    
    elif product['type'] == 'file':
        try:
            # If it's a URL, send as text. If file_id, send as document
            if product['content'].startswith('http'):
                await update.message.reply_text(
                    f"📥 *Download Link:*\n\n{product['content']}",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_document(
                    document=product['content'],
                    caption=f"📦 {product['name']}"
                )
        except Exception as e:
            logger.error(f"Error sending file: {e}")
            await update.message.reply_text(
                f"File link: {product['content']}"
            )
    
    elif product['type'] == 'image':
        try:
            await update.message.reply_photo(
                photo=product['content'],
                caption=f"{product['emoji']} {product['name']}"
            )
        except Exception as e:
            logger.error(f"Error sending image: {e}")
            await update.message.reply_text(product['content'])
    
    # Final thank you message
    await update.message.reply_text(
        "💫 *Enjoy your purchase!*\n\n"
        "⭐ Leave us feedback if you're satisfied!\n"
        "🛍️ Type /start to see more products",
        parse_mode="Markdown"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Exception: {context.error}")

def main():
    """Start the bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(view_product, pattern="^view_"))
    app.add_handler(CallbackQueryHandler(buy_product, pattern="^buy_"))
    app.add_handler(CallbackQueryHandler(back_to_shop, pattern="^back_to_shop$"))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    app.add_error_handler(error_handler)
    
    print("🚀 Universal Telegram Shop Bot is running...")
    print("💫 Ready to sell anything with Telegram Stars!")
    logger.info("Bot started successfully")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
