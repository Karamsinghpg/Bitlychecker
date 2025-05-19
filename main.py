import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

TELEGRAM_BOT_TOKEN = "7762680369:AAFNlRS1BTYMtpDs89p0FqETzye2rhg3gyg"
BITLY_TOKEN = "7570cff56ba665346ba7eb4df7b5dc4e0b6027e0"

logging.basicConfig(level=logging.INFO)

def get_clicks(bitly_url):
    headers = {
        'Authorization': f'Bearer {BITLY_TOKEN}',
    }
    bitlink_id = bitly_url.replace("https://", "").replace("http://", "")
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink_id}/clicks/summary'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('total_clicks', 0)
    else:
        return f"❌ Error: {response.status_code} - Invalid or non-Bitly link."

def start(update, context):
    update.message.reply_text("👋 Welcome! Send me a Bitly link and I’ll tell you the total clicks!")

def handle_message(update, context):
    text = update.message.text.strip()
    if text.startswith("http"):
        clicks = get_clicks(text)
        update.message.reply_text(f"🔗 Total Clicks: {clicks}")
    else:
        update.message.reply_text("❗ Please send a valid Bitly URL.")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
