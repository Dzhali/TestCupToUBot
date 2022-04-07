# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 22:13:16 2022

@author: Liana
"""
import os
from flask import Flask, request #flask for webhook

import telebot

from mybot.credentials import bot_token, bot_user_name, URL, DB_URI
import psycopg2 #for working with db


global TOKEN
TOKEN = bot_token

youtubebot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()

@youtubebot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.username
    youtubebot.reply_to(message, f"Hello!!!") 


@app.route('/{}'.format(TOKEN), methods=['POST'])
def redirect():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    youtubebot.process_new_updates([update])
    return "!", 200    

if __name__ == '__main__':
    youtubebot.remove_webhook()
    youtubebot.set_webhook(url='{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    app.run(host="0.0.0.0", port = int(os.environ.get("PORT", 5000)))
    

