import os
import requests
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, Updater

# Telegram bot token from Fly.io secret
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set!")

# Claude API key from Fly.io secret
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")
if not CLAUDE_API_KEY:
    raise ValueError("CLAUDE_API_KEY not set!")

# Telegram bot setup
bot = Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Function to send a message to Claude LLM
def get_claude_response(prompt: str) -> str:
    url = "https://api.anthropic.com/v1/complete"
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "model": "claude-v1",
        "prompt": prompt,
        "max_tokens_to_sample": 300
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("completion", "Claude did not respond.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I am your Claude-powered AI bot. Send me a message!")

# Handle text messages
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    update.message.reply_text("Thinking...")
    response = get_claude_response(user_message)
    update.message.reply_text(response)

# Handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Run the bot
if __name__ == "__main__":
    print("Bot is starting...")
    updater.start_polling()
    updater.idle()
