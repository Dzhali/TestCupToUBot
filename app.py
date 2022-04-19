# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 22:13:16 2022

@author: Liana
"""
import os
from flask import Flask, request #flask for webhook

import telebot
#for getting mobile number
from telebot import types


from mybot.credentials import bot_token, bot_user_name, URL, DB_URI
import psycopg2 #for working with db


global TOKEN
TOKEN = bot_token

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()

@bot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.username
    bot.reply_to(message, f"Hello!!!") 

@bot.message_handler(commands=["number"])
def phone(message):
    #формирование запроса к пользователю
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text='Send phone',request_contact=True) #создаем кнопку
    keyboard.add(button_phone) #добавляем кнопку в чат
    bot.send_message(message.chat.id, 'Number', reply_markup=keyboard)

@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        print(message.contact)
    
    contact = message.contact
    chat_id = message.chat.id
    msg_id = message.message_id
    
    db_object.execute(f"SELECT number FROM users WHERE number = {contact}")
    result = db_object.fetchone()

    if not result:
        status = 1
        db_object.execute("INSERT INTO users(number, status) VALUES (%s, %s)", (contact, status))
        db_connection.commit()
        bot.sendMessage(chat_id=chat_id, text="db changed!", reply_to_message_id=msg_id)
    else:
        bot.sendMessage(chat_id=chat_id, text="db isn't changed!", reply_to_message_id=msg_id)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def redirect():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200    

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    app.run(host="0.0.0.0", port = int(os.environ.get("PORT", 5000)))
    

