from telegram.ext import Updater
from telegram.ext import CommandHandler
from Identifier import Identifier
import logging
import time

updater = Updater(token='1765200872:AAFqsN4-tXoDrX3RssYn2IUFlGWZ8xcjRAg', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    IDF = Identifier(Tokens = ["DOGE-USD"])
    while(True):
        identifier = IDF.update()
        for token in identifier:
            if identifier[token] > 3:
                context.bot.send_message(chat_id=update.effective_chat.id, text="{} is striking {} downs".format(token, identifier["DOGE-USD"]))
                time.sleep(60)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
