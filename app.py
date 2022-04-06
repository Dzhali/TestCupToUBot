# import everything
from flask import Flask, request #flask for webhook

#COMPARE
import telegram  #mine
import telebot #new

from telebot.credentials import bot_token, bot_user_name, URL, DB_URI
import psycopg2 #for working with db

from db import ClientDatabase
#import os.path

global bot
global TOKEN
TOKEN = bot_token

#COMPARE
bot = telegram.Bot(token=TOKEN) #mine
youtubebot = telebot.TeleBot(TOKEN) #new

app = Flask(__name__)

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()

   #COMPARE answer to start  закомментить старт основной и редирект, и удостовериться что без редиректа не работает
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


#@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   #retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)

   #print("request.json: ", request.json)
    
   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)
   
   # the first time you chat with the bot AKA the welcoming message
   if text == "/start": #тут мы сразу принимаем, а в мессадж хендлере это работает через редирект
       bot_welcome = """
       Welcome to coolAvatar bot, the bot is using the service from http://avatars.adorable.io/ to generate cool looking avatars based on the name you enter so please enter a name and the bot will reply with an avatar for your name.
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

        
 



   else:
       try:
           # clear the message we got from any non alphabets
           # text = re.sub(r"\W", "_", text)
           # create the api link for the avatar based on http://avatars.adorable.io/
           url = "https://placekitten.com/700/{}".format(text.strip())
           # reply with a photo to the name the user sent,
           # note that you can send photos by url and telegram will fetch it for you
           bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
           bot.sendMessage(chat_id=chat_id, text=request.json, reply_to_message_id=msg_id) 
           
           db_object.execute(f"SELECT number FROM users WHERE number = {text}")
           result = db_object.fetchone()

           if not result:
              status = 1
              db_object.execute("INSERT INTO users(number, status) VALUES (%s, %s)", (text, status))
              db_connection.commit()
              bot.sendMessage(chat_id=chat_id, text="db changed!", reply_to_message_id=msg_id)
           else:
               bot.sendMessage(chat_id=chat_id, text="db isn't changed!", reply_to_message_id=msg_id)
       except Exception:
           # if things went wrong
           bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)
           
   return 'ok'

#@app.route('/setwebhook', methods=['GET', 'POST']) temporary comment
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

#@app.route('/')
#def index():
    #return '.'
if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    
    #new
    youtubebot.remove_webhook()
    youtubebot.set_webhook(url='{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    #new end
    app.run(threaded=True)
    
