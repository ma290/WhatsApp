from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.ext import CallbackContext
import pymongo
import logging

# MongoDB Connection
client = pymongo.MongoClient("mongodb+srv://dnRNNJffpUcy948:wBWvTI3xgOXBjAVO@cluster0.cdzla.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["whatsapp_data"]
users_collection = db["users"]

# Enable logging for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TELEGRAM_TOKEN = "8008506874:AAEupeno1WnUtbEZM4O2wVUHGoGqzwWtbnE"

# Define the start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the bot! Use the inline buttons to set file and message.')

    # Create inline buttons
    keyboard = [
        [InlineKeyboardButton("Set File", callback_data='set_file')],
        [InlineKeyboardButton("Set Message", callback_data='set_message')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose an option:', reply_markup=reply_markup)

# Handle button clicks
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'set_file':
        query.edit_message_text(text="Send me the file you want to set.")
        return
    if query.data == 'set_message':
        query.edit_message_text(text="Send me the message you want to set.")
        return

# Handle received messages (set message or file)
def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Check if it's a file or a text message
    if update.message.document:
        file = update.message.document
        file_path = file.file_id
        users_collection.update_one({"user_id": user_id}, {"$set": {"file": file_path}}, upsert=True)
        update.message.reply_text("File has been set!")
    elif update.message.text:
        text = update.message.text
        users_collection.update_one({"user_id": user_id}, {"$set": {"message": text}}, upsert=True)
        update.message.reply_text("Message has been set!")

# Main function to start the bot
def main():
    updater = Updater(TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text | Filters.document, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
