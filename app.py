# import everything
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,URL
import wayforpay
#from wayforpay import WayForPayAPI
 
global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)
wayForPay = WayForPayAPI(merchant_account = "www_instagram_com613" 
                         , merchant_key = "c64703e56c0d9263b5941067764b6433767b2d24"
                         , merchant_domain = "www.instagram.com")

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)

   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)
   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       # print the welcoming message
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
           #url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
           # reply with a photo to the name the user sent,
           # note that you can send photos by url and telegram will fetch it for you
           bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
           bot.sendMessage(chat_id=chat_id, text=request.json, reply_to_message_id=msg_id)
           
           # PAYMENT TEST
           invoice_data = {
           'amount': "UAH",
           'currency': "UAH",
           'dateBegin': "17.12.2021",
           'dateEnd': "18.12.2021",
           'orderReference': "WFPBI-61bc66c6a7677",
           'email': "likadgani@gmail.com" }
           
           response = wayForPay.createInvoiceRequest(invoice_data)           
           
       except Exception:
           # if things went wrong
           bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

   return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'
if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)