import os
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
from Helper.functions import get_image, get_chat

load_dotenv()

# Get Telegram API key from environment variable
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

# Get Chat GPT API key from environment variable
CHAT_GPT_API_KEY = os.getenv('CHAT_GPT_API_KEY')

# Authenticate OpenAI API
openai.api_key = CHAT_GPT_API_KEY

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Welcome, You can ask anything from me\n@RedXvirus')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('This bot can perform the following commands\n/image -> to create image from text\n/ask -> ask anything from me')

def image_command(update: Update, context: CallbackContext) -> None:
    """Create image from text."""
    text = update.message.text.replace("/image", "").strip().lower()

    if text:
        # Get image from OpenAI Dall-E API
        res = get_image(text)

        if res:
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action='upload_photo')
            context.bot.send_photo(chat_id=update.effective_message.chat_id, photo=res, reply_to_message_id=update.message.message_id)
    else:
        context.bot.send_message(chat_id=update.effective_message.chat_id, text='You have to give some description after /image', reply_to_message_id=update.message.message_id)

def ask_command(update: Update, context: CallbackContext) -> None:
    """Get chat response from Chat GPT API."""
    text = update.message.text.replace("/ask", "").strip().lower()

    if text:
        # Get response from OpenAI GPT-3 API
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action='typing')
        res = get_chat(text)

        if res:
            context.bot.send_message(chat_id=update.effective_message.chat_id, text=res, reply_to_message_id=update.message.message_id)
    else:
        context.bot.send_message(chat_id=update.effective_message.chat_id, text='Please ask anything after /ask', reply_to_message_id=update.message.message_id)

def main() -> None:
    """Start the bot."""
    updater = Updater(TELEGRAM_API_KEY)

    # Add handlers for Telegram commands
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))
    updater.dispatcher.add_handler(CommandHandler("image", image_command))
    updater.dispatcher.add_handler(CommandHandler("ask", ask_command))

    # Start the bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if name == 'main':
    main()