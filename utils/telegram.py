from itertools import islice
from telegram.ext import Updater, CommandHandler
from telegram import ChatAction
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


class Handlers:

    @staticmethod
    def start(update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text=f'Olá, sou a Ada. O ID dessa conversa é {update.message.chat_id}. Se você é o administrador da Ada, sabe o que fazer.')

class TelegramHandler:

    SLICE_LENGTH = 4096
    
    def __init__(self, api_token: str, conversations = list):
        self.updater = Updater(api_token, use_context=True)
        self.conversations = conversations
        self.updater.dispatcher.add_handler(CommandHandler('start', Handlers.start))
            
    def poll(self):
        self.updater.start_polling()

    def broadcast(self, message):
        bot = self.updater.bot
        for chunk in self.chunks(message):
            for conversation in self.conversations:
                bot.send_chat_action(chat_id=conversation, action=ChatAction.TYPING)
                bot.send_message(chat_id=conversation, text=chunk)
            
    @classmethod
    def chunks(cls, message):
        n = cls.SLICE_LENGTH
        it = iter(message)
        while True:
            chunk = ''.join(islice(it, n))
            if not chunk:
                return
            yield chunk