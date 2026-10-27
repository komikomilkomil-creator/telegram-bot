import telebot
from telebot import types
import json
import os

TOKEN = "9120570964:AAH19JfnZhn7PLULdcJyBl_BdcZQrOUZiEg"
ADMIN_ID = 6163706312

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "products": [],
            "card_number": "6037-9917-0000-0000",
            "support_id": "@fonix_pv",
            "owner": "@komil_pv",
            "orders": {}
        }, f, ensure_ascii=False, indent=2)

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@bot.message_handler(commands=['start'])
def start(msg):
    if msg.chat.id == ADMIN_ID:
        bot.send_message(msg.chat.id, "پنل مدیریت")
    else:
        bot.send_message(msg.chat.id, "به فروشگاه خوش آمدید")

@bot.message_handler(content_types=['photo','document'])
def receipt(msg):
    if msg.chat.id == ADMIN_ID:
        return
    bot.send_message(msg.chat.id,"رسید دریافت شد، منتظر تایید باشید.")
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("تایید و ارسال کانفیگ",callback_data=f"approve_{msg.chat.id}"))
    kb.add(types.InlineKeyboardButton("رد رسید",callback_data=f"reject_{msg.chat.id}"))
    bot.send_message(ADMIN_ID,f"رسید جدید از کاربر {msg.chat.id}",reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("approve_") or c.data.startswith("reject_"))
def approve_or_reject(c):
    user_id = c.data.split("_")[1]
    if "reject" in c.data:
        bot.send_message(int(user_id),"رسید شما رد شد.")
        bot.send_message(ADMIN_ID,"رد شد.")
    else:
        bot.send_message(ADMIN_ID,f"کانفیگ کاربر {user_id} را بفرست:")
        bot.register_next_step_handler(c.message,lambda m: send_config(m,user_id))

def send_config(msg,user_id):
    bot.send_message(int(user_id),"رسید تایید شد.\n\nکانفیگ شما:\n"+msg.text)
    bot.send_message(ADMIN_ID,"کانفیگ ارسال شد.")

print("ربات روشن شد...")
bot.infinity_polling()
