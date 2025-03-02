import requests
import json
import threading
import telebot  # <-- ADD MISSING IMPORT
from flask import Flask, request

# Telegram bot token
TOKEN = "7753909536:AAEwaR_OPJWW2eESC5VyP62MHfkYsR-HcUU"
bot = telebot.TeleBot(TOKEN)

# DeepSeek API URL
API_URL = "https://deepseek.ytansh038.workers.dev/?question="

# Flask app (for status check)
app = Flask(__name__)  # <-- FIXED THIS LINE (added double underscores)

@app.route('/')
def home():
    return "DeepSeek Bot is Running!"

def run_flask():
    app.run(host="0.0.0.0", port=8000)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_question = message.text

    response = requests.get(API_URL + user_question)
    if response.status_code == 200:
        try:
            data = json.loads(response.text)
            answer = data.get("message", "NO RESPONSE.")
        except json.JSONDecodeError:
            answer = "JSON response parse karne mein error aayi."
    else:
        answer = "API request failed. Please try again later."

    bot.send_message(chat_id, answer)

# Run Flask in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Start polling the bot
bot.polling(none_stop=True)
