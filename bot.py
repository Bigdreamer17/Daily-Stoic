import requests
import os
import telebot
from apscheduler.schedulers.background import BackgroundScheduler


BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

Users = []


def get_daily_quote() -> dict:
    url = "https://stoic-quotes.com/api/quote"
    params = {"quote": "text", "Author": "author"}
    response = requests.get(url, params)


    return response.json()

def fetched_message():
    res = get_daily_quote()
    quote = res['text'] + '\n' + '\n' + res['author']

    return quote

# Wellcome Message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    Users.append(user_id)
    msg  = " “To be even-minded is the greatest virtue.” — Heraclitus"+ '\n'+ '\n' +"Wellcome to Daily Stoic we will send you dailt stoic quotes every day at 7:00 but if you like now instantly" + '\n' + "type /Random"
    bot.reply_to(message, msg)

# Fetch quote and send it to user
@bot.message_handler(commands=['Random'])
def sign_quote(message):
    try:
        result = fetched_message()
        bot.reply_to(message, result)
    except Exception as e:
        print(f"Error: {e}")

# Send Dailt Quotes
def send_daily_quote():
    msg = fetched_message()

    for user_id in Users:
        bot.send_message(user_id, msg)

scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_quote, 'cron', hour=19, minute=00)
scheduler.start()

bot.infinity_polling()