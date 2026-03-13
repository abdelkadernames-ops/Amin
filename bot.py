import os
os.system("pip install pyTelegramBotAPI --no-cache-dir")

import random
import unicodedata
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "PUT_NEW_TOKEN_HERE"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

COUNTRIES = {

    "Germany": {
        "phone_code": "+49",
        "mobile_prefixes": ["15","16","17"],
        "cities": ["Berlin","Hamburg","Munich","Cologne","Frankfurt"],
        "streets": ["Hauptstrasse","Bahnhofstrasse","Gartenweg","Schulstrasse"],
        "postal": ["10115","20095","80331","50667","60311"],
        "domains": ["gmail.de","web.de","gmx.de"],
        "first": ["Thomas","Michael","Daniel","Peter"],
        "last": ["Muller","Schmidt","Fischer","Becker"]
    },

    "USA": {
        "phone_code": "+1",
        "mobile_prefixes": ["202","303","404","505"],
        "cities": ["New York","Los Angeles","Chicago","Houston"],
        "streets": ["Main St","Broadway","Park Ave","2nd Street"],
        "postal": ["10001","90001","60601","77001"],
        "domains": ["gmail.com","yahoo.com","outlook.com"],
        "first": ["James","John","Robert","Michael"],
        "last": ["Smith","Johnson","Brown","Taylor"]
    }

}

def remove_accents(text):
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))


def generate(country):

    data = COUNTRIES[country]

    first = random.choice(data["first"])
    last = random.choice(data["last"])
    city = random.choice(data["cities"])
    street = random.choice(data["streets"])
    postal = random.choice(data["postal"])

    address = f"{street} {random.randint(1,150)}"

    phone = data["phone_code"] + random.choice(data["mobile_prefixes"]) + str(random.randint(1000000,9999999))

    email = f"{remove_accents(first.lower())}.{remove_accents(last.lower())}@{random.choice(data['domains'])}"

    return (
        f"🌍 <b>{country} Identity</b>\n\n"
        f"👤 Name: {first} {last}\n"
        f"🏠 Address: {address}\n"
        f"🏙 City: {city}\n"
        f"📮 Postal Code: {postal}\n"
        f"📞 Phone: {phone}\n"
        f"📧 Email: {email}"
    )


@bot.message_handler(commands=["start"])
def start(message):

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(
        KeyboardButton("🇩🇪 Germany"),
        KeyboardButton("🇺🇸 USA")
    )

    bot.send_message(
        message.chat.id,
        "Welcome 👋\nChoose country:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: True)
def handle(message):

    if "Germany" in message.text:
        bot.send_message(message.chat.id, generate("Germany"))

    elif "USA" in message.text:
        bot.send_message(message.chat.id, generate("USA"))


print("Bot running...")
bot.infinity_polling()